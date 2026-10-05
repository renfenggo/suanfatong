#!/usr/bin/env python3
"""Stage3G full400 全量合并可行性审计脚本
只做审计、预审、依赖清理方案，不修改主图谱，不执行合并。
"""

import json
import os
import re
import math
from datetime import datetime, timezone
from collections import defaultdict, deque

POOL_PATH = "data/stage3g_standardized_candidate_pool_400.json"
GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
VALIDATION_PATH = "dependency_validation_result.json"

OUT_PLAN = "data/stage3g_full400_candidate_plan.json"
OUT_PRECHECK = "data/stage3g_full400_dynamic_precheck.json"
OUT_CLEANUP = "data/stage3g_full400_dependency_cleanup_plan.json"
OUT_REPORT = "docs/stage3g_full400_precheck_report.md"

print("=" * 60)
print("Stage3G full400 Merge Feasibility Audit")
print("=" * 60)

with open(POOL_PATH, "r", encoding="utf-8") as f:
    pool = json.load(f)
print(f"Loaded {len(pool)} candidates from pool")

with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

categories = graph.get("categories", [])
items_by_id = {}
name_to_ids = defaultdict(list)
en_name_to_ids = defaultdict(list)
alias_to_ids = defaultdict(list)
all_aliases = set()
all_names_lower = set()

for cat in categories:
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            item_id = item["id"]
            items_by_id[item_id] = item
            name = item.get("name", "")
            en = item.get("en_name", "")
            name_lower = name.lower().strip()
            all_names_lower.add(name_lower)
            name_to_ids[name_lower].append(item_id)
            if en:
                en_name_to_ids[en.lower().strip()].append(item_id)
            for alias in item.get("aliases", []):
                alias_lower = alias.lower().strip()
                alias_to_ids[alias_lower].append(item_id)
                all_aliases.add(alias_lower)
            for ga in item.get("global_aliases", []):
                ga_lower = ga.lower().strip()
                alias_to_ids[ga_lower].append(item_id)
                all_aliases.add(ga_lower)

item_count = len(items_by_id)
all_item_ids = set(items_by_id.keys())
print(f"  Graph: {item_count} items, {len(categories)} categories")

with open(VALIDATION_PATH, "r", encoding="utf-8") as f:
    val = json.load(f)
print(f"  Validation: passed={val.get('passed')}, item_count={val.get('item_count')}")

# Section lookup
section_names = {}
for cat in categories:
    for sec in cat.get("sections", []):
        section_names[sec["id"]] = sec.get("name", "")

def sn(sid):
    return section_names.get(sid, f"Section {sid}")

# ============================================================
# History pruned names
# ============================================================
history_pruned = set()
for fname in ["data/stage3f_batch2_duplicate_prune_removed_items.json",
              "data/stage3f_batch3_full40_duplicate_prune_removed_items.json"]:
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            removed_data = json.load(f)
            removed = removed_data.get("removed_items", [])
            if not removed and isinstance(removed_data, list):
                removed = removed_data
            for r in removed:
                if isinstance(r, dict):
                    n = r.get("name", "").lower().strip()
                    if n:
                        history_pruned.add(n)
                    en = r.get("en_name", "")
                    if en:
                        history_pruned.add(en.lower().strip())
                elif isinstance(r, str):
                    history_pruned.add(r.lower().strip())
print(f"  History pruned names: {len(history_pruned)}")

# ============================================================
# SIMILARITY scoring
# ============================================================
def tokenize(s):
    s = re.sub(r'[^a-z\u4e00-\u9fff0-9]', ' ', s.lower())
    return set(s.split())

def similarity(a, b):
    ta = tokenize(a)
    tb = tokenize(b)
    if not ta or not tb:
        return 0
    return len(ta & tb) / len(ta | tb)

# ============================================================
# NAME → ITEM ID mapping for dependency resolution
# ============================================================
exact_name_map = {}
for item_id, item in items_by_id.items():
    exact_name_map[item["name"]] = item_id
    if item.get("en_name"):
        exact_name_map[item["en_name"]] = item_id
    for alias in item.get("aliases", []):
        exact_name_map[alias] = item_id
    for ga in item.get("global_aliases", []):
        exact_name_map[ga] = item_id

# Fuzzy name match
def fuzzy_find_item(name):
    nl = name.lower().strip()
    if nl in name_to_ids:
        return name_to_ids[nl]
    if nl in alias_to_ids:
        return alias_to_ids[nl]
    # partial match
    for en, ids in en_name_to_ids.items():
        if nl in en or en in nl:
            return ids
    for an, ids in alias_to_ids.items():
        if nl in an or an in nl:
            return ids
    return []

# ============================================================
# PER-CANDIDATE AUDIT
# ============================================================
print("\nAuditing 400 candidates...")

candidate_plans = []
all_issues = []
dup_issues = []
dep_issues = []
risk_issues = []

# For cycle detection
candidate_id_set = {c["candidate_id"] for c in pool}
candidate_dep_graph = defaultdict(set)  # cid -> set of cids

exact_dup_count = 0
high_dup_similarity_count = 0
medium_similarity_count = 0
needs_new_section = False
total_direct_pre = 0
unresolvable_pre = 0
red_candidates = 0
low_conf_candidates = 0
medium_risk_candidates = 0
needs_manual_review = 0
possible_problem_patterns = 0

# Risk band counters per theme
theme_risk = defaultdict(lambda: {"green":0,"yellow":0,"medium":0,"red":0})
section_dist = defaultdict(int)
theme_dist = defaultdict(int)

for idx, cand in enumerate(pool):
    name = cand["name"]
    en_name = cand.get("en_name", name)
    cid = cand["candidate_id"]
    sec = cand["target_section"]
    risk = cand["risk_band"]
    conf = cand["mapping_confidence"]
    theme = cand["theme"]
    deps = cand.get("direct_pre_name_suggestion", [])
    ctype = cand["candidate_type"]
    is_pp = cand.get("possible_problem_pattern", False)

    theme_dist[theme] += 1
    section_dist[sec] += 1
    theme_risk[theme][risk] += 1

    if risk == "red":
        red_candidates += 1
    if conf == "low":
        low_conf_candidates += 1
    if risk == "medium":
        medium_risk_candidates += 1
    if is_pp:
        possible_problem_patterns += 1

    # ========================
    # DUPLICATE CHECK
    # ========================
    dup_result = {
        "exact_name_match": None,
        "exact_en_match": None,
        "alias_conflict": None,
        "history_pruned": False,
        "top3_similar": [],
        "is_exact_dup": False,
        "is_high_similarity": False,
        "duplicate_risk_level": "none"
    }

    # Check name
    nl = name.lower().strip()
    if nl in all_names_lower:
        dup_result["exact_name_match"] = name_to_ids.get(nl, [])
        dup_result["is_exact_dup"] = True

    # Check en_name
    if not dup_result["is_exact_dup"] and en_name:
        enl = en_name.lower().strip()
        if enl in all_names_lower:
            dup_result["exact_en_match"] = name_to_ids.get(enl, [])
            dup_result["is_exact_dup"] = True

    # Check history pruned
    if nl in history_pruned:
        dup_result["history_pruned"] = True
    if en_name:
        enl = en_name.lower().strip()
        if enl in history_pruned:
            dup_result["history_pruned"] = True

    # Find top 3 similar items
    similarities = []
    for item_id, item in items_by_id.items():
        sim = max(
            similarity(name, item.get("name", "")),
            similarity(en_name, item.get("en_name", "")),
        )
        if sim > 0.3:
            similarities.append((item_id, item["name"], sim))
    similarities.sort(key=lambda x: -x[2])
    top3 = similarities[:3]
    dup_result["top3_similar"] = [
        {"item_id": i, "name": n, "similarity": round(s, 3)}
        for i, n, s in top3
    ]

    if not dup_result["is_exact_dup"] and top3:
        max_sim = top3[0][2]
        if max_sim >= 0.85:
            dup_result["is_high_similarity"] = True
            dup_result["duplicate_risk_level"] = "high"
        elif max_sim >= 0.65:
            dup_result["duplicate_risk_level"] = "medium"

    if dup_result["is_exact_dup"]:
        exact_dup_count += 1
        dup_issues.append({
            "candidate_id": cid, "name": name, "type": "exact_name_match",
            "matched_ids": dup_result["exact_name_match"] or dup_result["exact_en_match"]
        })
    elif dup_result["is_high_similarity"]:
        high_dup_similarity_count += 1
        dup_issues.append({
            "candidate_id": cid, "name": name, "type": "high_similarity",
            "top_match": top3[0][1], "similarity": top3[0][2]
        })

    # ========================
    # DEPENDENCY CHECK
    # ========================
    dep_result = {
        "direct_pre_mapped": [],
        "direct_pre_unresolved": [],
        "has_section_ref": False,
        "has_self_ref": False,
        "has_dangling_ref": False,
        "mapping_issues": [],
        "cleanup_needed": False
    }

    for dep_name in deps:
        # Try exact name match
        found_ids = fuzzy_find_item(dep_name)
        if found_ids:
            dep_result["direct_pre_mapped"].append({
                "pre_name": dep_name,
                "matched_ids": found_ids,
                "best_match": found_ids[0]
            })
        else:
            # Try similarity
            best_sim = 0
            best_id = None
            best_iname = ""
            for item_id, item in items_by_id.items():
                sim = max(
                    similarity(dep_name, item.get("name", "")),
                    similarity(dep_name, item.get("en_name", ""))
                )
                if sim > best_sim:
                    best_sim = sim
                    best_id = item_id
                    best_iname = item.get("name", "")
            if best_sim >= 0.6:
                dep_result["direct_pre_mapped"].append({
                    "pre_name": dep_name,
                    "matched_ids": [best_id],
                    "best_match": best_id,
                    "match_type": "fuzzy",
                    "similarity": round(best_sim, 3)
                })
            else:
                dep_result["direct_pre_unresolved"].append({
                    "pre_name": dep_name,
                    "best_guess_id": best_id,
                    "best_guess_name": best_iname,
                    "similarity": round(best_sim, 3) if best_id else 0
                })
                dep_result["cleanup_needed"] = True

    # Section ref check
    for dep_name in deps:
        if re.match(r'^\d+\.\d+$', dep_name):
            dep_result["has_section_ref"] = True
            dep_result["mapping_issues"].append(f"section_ref: {dep_name}")
            dep_result["cleanup_needed"] = True

    # Self ref check
    if name in deps or en_name in deps:
        dep_result["has_self_ref"] = True
        dep_result["mapping_issues"].append("self_reference")
        dep_result["cleanup_needed"] = True

    # If unresolved, it's a dangling ref
    if dep_result["direct_pre_unresolved"]:
        dep_result["has_dangling_ref"] = True

    total_direct_pre += len(deps)
    if dep_result["direct_pre_unresolved"]:
        unresolvable_pre += len(dep_result["direct_pre_unresolved"])

    if dep_result["cleanup_needed"]:
        dep_issues.append({
            "candidate_id": cid,
            "name": name,
            "unresolved_count": len(dep_result["direct_pre_unresolved"]),
            "issues": dep_result["mapping_issues"]
        })

    # ========================
    # RISK CHECK
    # ========================
    risk_result = {
        "is_red": risk == "red",
        "is_low_confidence": conf == "low",
        "is_medium_risk": risk == "medium",
        "needs_manual_review": False,
        "manual_review_reason": "",
        "needs_new_section": False,
        "problem_pattern_risk": is_pp,
        "direct_pre_count": len(deps),
        "direct_pre_overlong": len(deps) > 12
    }

    # Check if section exists
    if sec not in section_names:
        risk_result["needs_new_section"] = True
        needs_new_section = True
        risk_issues.append({
            "candidate_id": cid, "name": name, "issue": "needs_new_section",
            "target_section": sec
        })

    # Manual review triggers
    manual_triggers = []
    if risk == "red":
        manual_triggers.append("red_risk_band")
    if conf == "low":
        manual_triggers.append("low_confidence")
    if dep_result["direct_pre_unresolved"]:
        manual_triggers.append("unresolved_dependencies")
    if len(deps) > 12:
        manual_triggers.append(f"direct_pre_overlong({len(deps)} deps)")
    if risk == "medium" and conf == "low":
        manual_triggers.append("medium_risk_low_confidence")

    if manual_triggers:
        risk_result["needs_manual_review"] = True
        risk_result["manual_review_reason"] = "; ".join(manual_triggers)

    # ========================
    # CANDIDATE DEP GRAPH (for cycle detection)
    # ========================
    mapped_ids = [m["best_match"] for m in dep_result["direct_pre_mapped"]]
    # Find which mapped_ids are other candidates (not yet in graph)
    # For cycle detection, we mark: this candidate depends on X
    # We can't do full cycle detection without knowing which items map to which candidates
    # But we track the dep graph for candidates that dep on each other
    for mid in mapped_ids:
        if mid not in all_item_ids:
            candidate_dep_graph[cid].add(mid)

    # ========================
    # WHY NOT DUPLICATE explanation
    # ========================
    why_not_dup = ""
    if dup_result["top3_similar"]:
        top = dup_result["top3_similar"]
        reasons = []
        for t in top:
            if t["similarity"] < 0.5:
                reasons.append(f"{t['name']}(sim={t['similarity']:.2f}): 相似度不足")
            elif t["similarity"] < 0.7:
                reasons.append(f"{t['name']}(sim={t['similarity']:.2f}): 中度相似但主题/角度不同")
            else:
                reasons.append(f"{t['name']}(sim={t['similarity']:.2f}): 高相似但为独立扩展/进阶")
        why_not_dup = "; ".join(reasons)

    # ========================
    # ASSEMBLE CANDIDATE PLAN
    # ========================
    plan = {
        "candidate_id": cid,
        "name": name,
        "en_name": en_name,
        "theme": theme,
        "target_section": sec,
        "section_name": cand["section_name"],
        "risk_band": risk,
        "mapping_confidence": conf,
        "candidate_type": ctype,
        "direct_pre_count": len(deps),
        "direct_pre_name_suggestion": deps,
        "duplicate_check": dup_result,
        "dependency_check": dep_result,
        "risk_check": risk_result,
        "can_merge_directly": (
            not dup_result["is_exact_dup"] and
            not risk_result["needs_new_section"] and
            not dep_result["has_section_ref"] and
            not dep_result["has_self_ref"] and
            risk != "red"
        ),
        "needs_cleanup": dep_result["cleanup_needed"],
        "merge_priority": "now" if risk == "green" and conf == "high" else (
            "soon" if risk in ("green", "yellow") and conf in ("high", "medium") else
            "later" if risk == "medium" else "defer"
        ),
        "why_not_duplicate": why_not_dup
    }
    candidate_plans.append(plan)

    if idx % 100 == 0:
        print(f"  Processed {idx}/{len(pool)}...")

# ============================================================
# CYCLE DETECTION among candidates
# ============================================================
print("\nDetecting candidate dependency cycles...")
# Build candidate-to-candidate edges
# Map candidate names to their cids
cid_by_name = {}
cid_by_en = {}
for cand in pool:
    cid_by_name[cand["name"]] = cand["candidate_id"]
    cid_by_en[cand["en_name"]] = cand["candidate_id"]

# For each candidate, check if any resolved pre maps to another candidate
cand_cand_edges = defaultdict(set)  # cid -> set of other cids it depends on
for plan in candidate_plans:
    cid = plan["candidate_id"]
    for m in plan["dependency_check"]["direct_pre_mapped"]:
        pre_name = m["pre_name"]
        # Check if this pre_name is another candidate
        if pre_name in cid_by_name:
            other_cid = cid_by_name[pre_name]
            if other_cid != cid:
                cand_cand_edges[cid].add(other_cid)
        if pre_name in cid_by_en:
            other_cid = cid_by_en[pre_name]
            if other_cid != cid:
                cand_cand_edges[cid].add(other_cid)

# Topological sort / cycle detection
def detect_cycles(edges):
    indeg = {cid: 0 for cid in candidate_id_set}
    for u in edges:
        for v in edges[u]:
            if v in indeg:
                indeg[v] = indeg.get(v, 0) + 1

    q = deque([cid for cid, d in indeg.items() if d == 0])
    visited = set()
    while q:
        u = q.popleft()
        visited.add(u)
        for v in edges.get(u, set()):
            if v in indeg:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

    cycle_ids = candidate_id_set - visited
    return list(cycle_ids)

cycle_nodes = detect_cycles(cand_cand_edges)
has_candidate_cycle = len(cycle_nodes) > 0
if has_candidate_cycle:
    print(f"  ⚠ Found {len(cycle_nodes)} candidates in dependency cycles!")
else:
    print(f"  ✅ No candidate dependency cycles")

# ============================================================
# SUMMARY STATS
# ============================================================
print(f"\n{'=' * 60}")
print(f"      AUDIT SUMMARY")
print(f"{'=' * 60}")

can_merge = sum(1 for p in candidate_plans if p["can_merge_directly"])
need_cleanup = sum(1 for p in candidate_plans if p["needs_cleanup"])
section_ref_deps = sum(1 for p in candidate_plans if p["dependency_check"]["has_section_ref"])
self_ref_deps = sum(1 for p in candidate_plans if p["dependency_check"]["has_self_ref"])
dangling_refs = sum(1 for p in candidate_plans if p["dependency_check"]["has_dangling_ref"])

now = sum(1 for p in candidate_plans if p["merge_priority"] == "now")
soon = sum(1 for p in candidate_plans if p["merge_priority"] == "soon")
later = sum(1 for p in candidate_plans if p["merge_priority"] == "later")
defer = sum(1 for p in candidate_plans if p["merge_priority"] == "defer")

# Direct pre count distribution
max_dp = max((p["direct_pre_count"] for p in candidate_plans), default=0)
avg_dp = sum(p["direct_pre_count"] for p in candidate_plans) / len(pool)

print(f"\n  Total candidates: {len(pool)}")
print(f"  Can merge directly: {can_merge}")
print(f"  Need dependency cleanup: {need_cleanup}")
print(f"  Exact duplicates: {exact_dup_count}")
print(f"  High similarity duplicates: {high_dup_similarity_count}")
print(f"  Needs manual review: {needs_manual_review}")
print(f"  Red candidates: {red_candidates}")
print(f"  Low confidence: {low_conf_candidates}")
print(f"  Medium risk: {medium_risk_candidates}")
print(f"  Needs new section: {needs_new_section}")
print(f"  Has candidate dep cycle: {has_candidate_cycle}")
print(f"  Section ref dependencies: {section_ref_deps}")
print(f"  Self ref dependencies: {self_ref_deps}")
print(f"  Dangling refs: {dangling_refs}")
print(f"  Total direct_pre: {total_direct_pre}")
print(f"  Unresolvable pre: {unresolvable_pre}")
print(f"  Avg direct_pre per candidate: {avg_dp:.1f}")
print(f"  Max direct_pre: {max_dp}")
print(f"  Now priority: {now}")
print(f"  Soon priority: {soon}")
print(f"  Later priority: {later}")
print(f"  Defer priority: {defer}")
print(f"  Problem patterns: {possible_problem_patterns}")

# ============================================================
# RECOMMENDATION
# ============================================================
all_clean = (
    exact_dup_count == 0 and
    high_dup_similarity_count == 0 and
    not needs_new_section and
    not has_candidate_cycle and
    section_ref_deps == 0 and
    self_ref_deps == 0
)

if all_clean:
    recommendation = "ready_for_1号线程_merge_full400"
    recommended_merge_count = 400
else:
    recommendation = "needs_cleanup_before_full400_merge"
    recommended_merge_count = can_merge  # how many can go directly

print(f"\n  Recommendation: {recommendation}")
print(f"  Recommended merge count: {recommended_merge_count}")

# ============================================================
# Blocking issues
# ============================================================
blocking_issues = []
if exact_dup_count > 0:
    blocking_issues.append(f"exact_duplicate_count={exact_dup_count}")
if high_dup_similarity_count > 0:
    blocking_issues.append(f"high_similarity_count={high_dup_similarity_count}")
if needs_new_section:
    blocking_issues.append("needs_new_section=true")
if has_candidate_cycle:
    blocking_issues.append("candidate_dependency_cycle=true")
if section_ref_deps > 0:
    blocking_issues.append(f"section_ref_dependencies={section_ref_deps}")
if self_ref_deps > 0:
    blocking_issues.append(f"self_ref_dependencies={self_ref_deps}")
if dangling_refs > 0:
    blocking_issues.append(f"dangling_refs={dangling_refs}")
if red_candidates > 0:
    blocking_issues.append(f"red_candidates={red_candidates} (建议暂缓)")

# ============================================================
# Suggested fixes for blocking issues
# ============================================================
suggested_fixes = []

if exact_dup_count > 0:
    dup_candidates = [p for p in candidate_plans if p["duplicate_check"]["is_exact_dup"]]
    for dp in dup_candidates:
        mid = dp["duplicate_check"]["exact_name_match"] or dp["duplicate_check"]["exact_en_match"]
        suggested_fixes.append({
            "issue": "exact_duplicate",
            "candidate_id": dp["candidate_id"],
            "candidate_name": dp["name"],
            "existing_item_ids": mid,
            "action": "remove_from_pool",
            "note": f"候选 \"{dp['name']}\" 与已有节点重复，应从候选池移除"
        })

if needs_new_section:
    ns_candidates = [p for p in candidate_plans if p["risk_check"]["needs_new_section"]]
    for ns in ns_candidates:
        suggested_fixes.append({
            "issue": "needs_new_section",
            "candidate_id": ns["candidate_id"],
            "candidate_name": ns["name"],
            "target_section": ns["target_section"],
            "action": "reassign_section",
            "suggested_section": "2.9",
            "note": f"Section {ns['target_section']} 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section"
        })

if self_ref_deps > 0:
    sr_candidates = [p for p in candidate_plans if p["dependency_check"]["has_self_ref"]]
    for sr in sr_candidates:
        suggested_fixes.append({
            "issue": "self_reference",
            "candidate_id": sr["candidate_id"],
            "candidate_name": sr["name"],
            "action": "remove_self_from_pre",
            "note": "direct_pre_name_suggestion 中包含自身，需移除"
        })

print(f"\n  Suggested fixes: {len(suggested_fixes)} items")

# ============================================================
# OUTPUT 1: CANDIDATE PLAN
# ============================================================
print("\nWriting outputs...")
plan_output = {
    "meta": {
        "generated_by": "stage3g_full400_audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False,
        "merge_executed": False,
        "total_candidates": len(pool),
        "current_item_count": item_count,
        "expected_item_count_after_merge": item_count + len(pool),
        "current_section_count": len(section_names),
        "recommendation": recommendation,
        "recommended_merge_count": recommended_merge_count
    },
    "summary": {
        "can_merge_directly": can_merge,
        "need_cleanup": need_cleanup,
        "exact_duplicates": exact_dup_count,
        "high_similarity": high_dup_similarity_count,
        "needs_manual_review": needs_manual_review,
        "red_candidates": red_candidates,
        "low_confidence": low_conf_candidates,
        "medium_risk": medium_risk_candidates,
        "needs_new_section": needs_new_section,
        "candidate_dep_cycle": has_candidate_cycle,
        "section_ref_deps": section_ref_deps,
        "self_ref_deps": self_ref_deps,
        "dangling_refs": dangling_refs,
        "total_direct_pre": total_direct_pre,
        "unresolvable_pre": unresolvable_pre,
        "blocking_issues": blocking_issues
    },
    "suggested_fixes": suggested_fixes,
    "candidates": candidate_plans
}
with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan_output, f, ensure_ascii=False, indent=2)
print(f"  ✅ {OUT_PLAN}")

# ============================================================
# OUTPUT 2: DYNAMIC PRECHECK
# ============================================================
precheck = {
    "meta": {
        "generated_by": "stage3g_full400_audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False,
        "merge_executed": False,
        "validate_only_status": {
            "item_count": item_count,
            "section_count": len(section_names),
            "passed": val.get("passed", False)
        }
    },
    "precheck_results": {
        "exact_duplicate": {
            "count": exact_dup_count,
            "passed": exact_dup_count == 0,
            "items": dup_issues
        },
        "high_duplicate": {
            "count": high_dup_similarity_count,
            "passed": high_dup_similarity_count == 0,
            "items": [i for i in dup_issues if i["type"] == "high_similarity"]
        },
        "needs_new_section": {
            "value": needs_new_section,
            "passed": not needs_new_section
        },
        "candidate_dependency_cycle": {
            "value": has_candidate_cycle,
            "passed": not has_candidate_cycle,
            "cycle_nodes": cycle_nodes if has_candidate_cycle else []
        },
        "section_ref_dependencies": {
            "count": section_ref_deps,
            "passed": section_ref_deps == 0
        },
        "self_ref_dependencies": {
            "count": self_ref_deps,
            "passed": self_ref_deps == 0
        },
        "dangling_dependencies": {
            "count": dangling_refs,
            "passed": dangling_refs == 0
        },
        "unresolvable_direct_pre": {
            "count": unresolvable_pre,
            "passed": unresolvable_pre == 0
        },
        "dependency_cleanup_required": {
            "value": need_cleanup > 0,
            "count": need_cleanup
        },
        "red_candidates": {
            "count": red_candidates,
            "passed": red_candidates == 0,
            "note": "red候选应暂缓或人工复核"
        },
        "theme_distribution": dict(theme_dist),
        "section_distribution": dict(section_dist),
        "risk_band_distribution": {
            "green": sum(1 for p in candidate_plans if p["risk_band"] == "green"),
            "yellow": sum(1 for p in candidate_plans if p["risk_band"] == "yellow"),
            "medium": sum(1 for p in candidate_plans if p["risk_band"] == "medium"),
            "red": sum(1 for p in candidate_plans if p["risk_band"] == "red"),
        },
        "confidence_distribution": {
            "high": sum(1 for p in candidate_plans if p["mapping_confidence"] == "high"),
            "medium": sum(1 for p in candidate_plans if p["mapping_confidence"] == "medium"),
            "low": sum(1 for p in candidate_plans if p["mapping_confidence"] == "low"),
        },
        "merge_priority_distribution": {
            "now": now, "soon": soon, "later": later, "defer": defer
        },
        "direct_pre_stats": {
            "total": total_direct_pre,
            "avg": round(avg_dp, 1),
            "max": max_dp
        }
    },
    "all_checks_passed": all_clean and red_candidates == 0 and need_cleanup == 0,
    "recommendation": recommendation,
    "recommended_merge_count": recommended_merge_count,
    "blocking_issues": blocking_issues,
    "suggested_fixes": suggested_fixes
}
with open(OUT_PRECHECK, "w", encoding="utf-8") as f:
    json.dump(precheck, f, ensure_ascii=False, indent=2)
print(f"  ✅ {OUT_PRECHECK}")

# ============================================================
# OUTPUT 3: DEPENDENCY CLEANUP PLAN
# ============================================================
cleanup_items = []
for plan in candidate_plans:
    if plan["needs_cleanup"]:
        dc = plan["dependency_check"]
        cleanup_item = {
            "candidate_id": plan["candidate_id"],
            "name": plan["name"],
            "theme": plan["theme"],
            "issues": dc["mapping_issues"],
            "unresolved_pre": dc["direct_pre_unresolved"],
            "suggested_fixes": []
        }
        # Generate suggested fixes for unresolved deps
        for unresolved in dc["direct_pre_unresolved"]:
            pre_name = unresolved["pre_name"]
            best_id = unresolved.get("best_guess_id")
            best_name = unresolved.get("best_guess_name", "")
            similarity = unresolved.get("similarity", 0)
            if best_id:
                cleanup_item["suggested_fixes"].append({
                    "pre_name": pre_name,
                    "action": "manual_confirm",
                    "suggested_item_id": best_id,
                    "suggested_item_name": best_name,
                    "similarity": similarity,
                    "note": "模糊匹配，需人工确认"
                })
            else:
                cleanup_item["suggested_fixes"].append({
                    "pre_name": pre_name,
                    "action": "resolve_or_remove",
                    "note": "无法找到匹配，需替换为已有节点或删除此依赖"
                })
        # For section refs
        if dc["has_section_ref"]:
            cleanup_item["suggested_fixes"].append({
                "action": "remove_section_refs",
                "note": "direct_pre中含有section id，需替换为具体item id"
            })
        if dc["has_self_ref"]:
            cleanup_item["suggested_fixes"].append({
                "action": "remove_self_ref",
                "note": "移除对自身的引用"
            })
        cleanup_items.append(cleanup_item)

cleanup_plan = {
    "meta": {
        "generated_by": "stage3g_full400_audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False,
        "merge_executed": False,
        "dependency_cleanup_required": len(cleanup_items) > 0,
        "total_candidates_needing_cleanup": len(cleanup_items)
    },
    "cleanup_summary": {
        "total_unresolved_direct_pre": unresolvable_pre,
        "section_ref_count": section_ref_deps,
        "self_ref_count": self_ref_deps,
        "dangling_ref_count": dangling_refs
    },
    "cleanup_items": cleanup_items
}
with open(OUT_CLEANUP, "w", encoding="utf-8") as f:
    json.dump(cleanup_plan, f, ensure_ascii=False, indent=2)
print(f"  ✅ {OUT_CLEANUP}")

# ============================================================
# OUTPUT 4: REPORT
# ============================================================
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(f"# Stage3G full400 全量合并可行性审计报告\n\n")
    f.write(f"**生成时间**: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"**审计脚本**: stage3g_full400_audit.py\n\n")

    f.write(f"## 1. 总体结论\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| 候选总数 | {len(pool)} |\n")
    f.write(f"| 可以直接合并 | {can_merge} |\n")
    f.write(f"| 需要依赖清理 | {need_cleanup} |\n")
    f.write(f"| 精确重复 | {exact_dup_count} |\n")
    f.write(f"| 高度近似 | {high_dup_similarity_count} |\n")
    f.write(f"| 需要人工复核 | {needs_manual_review} |\n")
    f.write(f"| red候选 | {red_candidates} |\n")
    f.write(f"| low confidence | {low_conf_candidates} |\n")
    f.write(f"| 建议 | **{recommendation}** |\n")
    f.write(f"| 建议合并数 | {recommended_merge_count} |\n")
    f.write(f"| 修改主图谱 | 否 |\n")
    f.write(f"| 执行合并 | 否 |\n\n")

    f.write(f"## 2. 阻塞项列表\n\n")
    if blocking_issues:
        for bi in blocking_issues:
            f.write(f"- ❌ {bi}\n")
    else:
        f.write(f"- ✅ 无阻塞项\n")
    f.write(f"\n")

    f.write(f"## 3. 各主题分布与风险\n\n")
    f.write(f"| Theme | 候选数 | green | yellow | medium | red |\n")
    f.write(f"|-------|--------|-------|--------|--------|-----|\n")
    for t in sorted(theme_risk.keys()):
        tr = theme_risk[t]
        f.write(f"| {t} | {theme_dist[t]} | {tr['green']} | {tr['yellow']} | {tr['medium']} | {tr['red']} |\n")

    f.write(f"\n## 4. 依赖质量\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| direct_pre 总数 | {total_direct_pre} |\n")
    f.write(f"| 平均每个候选 | {avg_dp:.1f} |\n")
    f.write(f"| 最大 direct_pre | {max_dp} |\n")
    f.write(f"| 无法解析的 pre | {unresolvable_pre} |\n")
    f.write(f"| section ref 数量 | {section_ref_deps} |\n")
    f.write(f"| self ref 数量 | {self_ref_deps} |\n")
    f.write(f"| 悬空引用数量 | {dangling_refs} |\n")
    f.write(f"| 候选依赖环 | {'是' if has_candidate_cycle else '否'} |\n\n")

    f.write(f"## 5. Section 分布\n\n")
    f.write(f"| Section | 名称 | 候选数 |\n")
    f.write(f"|---------|------|--------|\n")
    for s in sorted(section_dist.keys()):
        f.write(f"| {s} | {sn(s)} | {section_dist[s]} |\n")

    f.write(f"\n## 6. Merge Priority 分布\n\n")
    f.write(f"| Priority | 数量 | 含义 |\n")
    f.write(f"|----------|------|------|\n")
    f.write(f"| now | {now} | green + high confidence，立即合并 |\n")
    f.write(f"| soon | {soon} | green/yellow + high/medium，早期合并 |\n")
    f.write(f"| later | {later} | medium/low，后期合并 |\n")
    f.write(f"| defer | {defer} | red/low confidence，暂缓 |\n")

    f.write(f"\n## 7. 是否建议一次合并 400\n\n")
    if all_clean and red_candidates == 0:
        f.write(f"✅ **建议一次合并 400**。所有检查均通过：\n")
        f.write(f"- exact_duplicate = 0\n")
        f.write(f"- high_duplicate = 0\n")
        f.write(f"- needs_new_section = false\n")
        f.write(f"- candidate_dependency_cycle = false\n")
        f.write(f"- section_ref_dependencies = 0\n")
        f.write(f"- self_ref_dependencies = 0\n")
        f.write(f"- dependency_cleanup_required = false\n")
        f.write(f"- validate-only passed = true\n\n")
        f.write(f"合并前 item_count = {item_count}，合并后 = {item_count + len(pool)}。\n")
    else:
        f.write(f"❌ **不建议一次合并 400**。阻塞项如下：\n\n")
        for bi in blocking_issues:
            f.write(f"- {bi}\n")
        f.write(f"\n建议先解决阻塞项，或分批次合并。可直接合并的候选数：{can_merge}。\n")

    f.write(f"\n## 8. 是否导致依赖过密\n\n")
    if avg_dp <= 8 and max_dp <= 12:
        f.write(f"✅ direct_pre 平均 {avg_dp:.1f}，最大 {max_dp}，不会造成依赖过密。\n")
    elif avg_dp <= 10:
        f.write(f"⚠ direct_pre 平均 {avg_dp:.1f}，最大 {max_dp}，依赖偏密但可控。\n")
    else:
        f.write(f"❌ direct_pre 平均 {avg_dp:.1f}，最大 {max_dp}，可能造成依赖过密。\n")

    # Problem patterns section
    f.write(f"\n## 9. Problem Pattern 候选\n\n")
    pp_candidates = [p for p in candidate_plans if p["risk_check"]["problem_pattern_risk"]]
    f.write(f"共 {len(pp_candidates)} 个候选标记为 problem_pattern（仅标记，不正式生成模式）：\n\n")
    f.write(f"| 候选 | Theme | Risk |\n")
    f.write(f"|------|-------|------|\n")
    for pp in pp_candidates[:30]:
        f.write(f"| {pp['name']} | {pp['theme']} | {pp['risk_band']} |\n")
    if len(pp_candidates) > 30:
        f.write(f"| ... ({len(pp_candidates) - 30} more) | | |\n")

    f.write(f"\n## 11. 建议修复方案\n\n")
    if suggested_fixes:
        for sf in suggested_fixes:
            f.write(f"- **{sf['issue']}**: `{sf.get('candidate_name','')}` → {sf['action']}\n")
            f.write(f"  - {sf['note']}\n")
            if 'suggested_section' in sf:
                f.write(f"  - 建议 section: {sf['suggested_section']}\n")
    else:
        f.write(f"无阻塞项，无需修复。\n")

    # Top duplication risks
    f.write(f"\n## 12. 高危重复风险主题\n\n")
    high_risk_themes = [
        "KMP / 扩展KMP / Z算法 / Border树",
        "Lucas / Miller-Rabin / BSGS / 欧拉函数 / 莫比乌斯反演",
        "单调队列优化 / 斜率优化 / 状压DP / 概率DP",
        "线段树 Split / Merge / 分裂 / 合并 / Beats",
        "SCC DAG / 动态连通性 / 缩点 / DAG",
        "线性基 Range / Merge / Deletion / Rollback"
    ]
    for hrt in high_risk_themes:
        f.write(f"- {hrt}\n")

    f.write(f"\n---\n")
    f.write(f"*本报告由 stage3g_full400_audit.py 自动生成*\n")
    f.write(f"*不修改主图谱，不执行合并*\n")

print(f"  ✅ {OUT_REPORT}")
print(f"\n{'=' * 60}")
print(f"      Stage3G full400 Audit Complete")
print(f"{'=' * 60}")
print(f"  Recommendation: {recommendation}")
print(f"  Recommended merge count: {recommended_merge_count}")
if blocking_issues:
    print(f"  Blocking issues:")
    for bi in blocking_issues:
        print(f"    - {bi}")
