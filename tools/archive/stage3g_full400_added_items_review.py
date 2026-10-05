#!/usr/bin/env python3
"""Stage3G full400 Added Items Review
Reviews all 400 newly added nodes for quality, duplicates, dependency issues.
Does NOT modify main graph. Does NOT apply patches.
"""

import json
import os
import re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
MAPPING_PATH = "data/stage3g_full400_candidate_to_item_id_mapping.json"
SUMMARY_PATH = "data/stage3g_full400_added_items_summary.json"
CLEANUP_PATH = "data/stage3g_full400_dependency_cleanup_plan_v2.json"
PRECHECK_PATH = "data/stage3g_full400_dynamic_precheck_v2.json"
POOL_PATH = "data/stage3g_standardized_candidate_pool_400.json"

OUT_REVIEW = "data/stage3g_full400_added_items_review.json"
OUT_REPORT = "docs/stage3g_full400_added_items_review_report.md"
OUT_PATCH = "data/stage3g_full400_review_status_patch_preview.json"
OUT_DEP_FIX = "data/stage3g_full400_dependency_fix_candidates.json"
OUT_PP_SYNC = "data/stage3g_full400_problem_pattern_sync_candidates.json"
OUT_MERGE = "data/stage3g_full400_merge_or_collapse_candidates.json"

print("=" * 60)
print("Stage3G full400 Added Items Review")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    mapping_data = json.load(f)
mappings = mapping_data["mappings"]

with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
    summary = json.load(f)

with open(CLEANUP_PATH, "r", encoding="utf-8") as f:
    cleanup_data = json.load(f)

with open(PRECHECK_PATH, "r", encoding="utf-8") as f:
    precheck_data = json.load(f)

with open(POOL_PATH, "r", encoding="utf-8") as f:
    pool = json.load(f)

# Build lookup maps
added_item_ids = {m["item_id"] for m in mappings}
candidate_to_item = {m["candidate_id"]: m for m in mappings}
item_to_candidate = {m["item_id"]: m for m in mappings}
item_id_to_name = {m["item_id"]: m["name"] for m in mappings}

# Build pool lookup
pool_by_cid = {c["candidate_id"]: c for c in pool}

# Build cleanup lookup
cleanup_by_cid = {}
for ci in cleanup_data.get("cleanup_items", []):
    cleanup_by_cid[ci["candidate_id"]] = ci

# Extract all items from graph
all_items = {}
all_items_list = []
old_items = {}
new_items = {}
old_names_lower = set()
new_names_lower = set()

sections = {}
for cat in graph.get("categories", []):
    for sec in cat.get("sections", []):
        sid = sec["id"]
        sections[sid] = {"id": sid, "name": sec.get("name", ""), "items": []}
        for item in sec.get("items", []):
            iid = item["id"]
            all_items[iid] = item
            all_items_list.append(item)
            sections[sid]["items"].append(iid)
            if iid in added_item_ids:
                new_items[iid] = item
                new_names_lower.add(item.get("name", "").lower().strip())
            else:
                old_items[iid] = item
                old_names_lower.add(item.get("name", "").lower().strip())

print(f"  Total items: {len(all_items)} (old: {len(old_items)}, new: {len(new_items)})")

# Build name/en_name/alias lookup for dedup
old_name_to_ids = defaultdict(list)
old_en_to_ids = defaultdict(list)
old_alias_to_ids = defaultdict(list)
for iid, item in old_items.items():
    n = item.get("name", "").lower().strip()
    if n:
        old_name_to_ids[n].append(iid)
    en = item.get("en_name", "").lower().strip()
    if en:
        old_en_to_ids[en].append(iid)
    for a in item.get("aliases", []):
        old_alias_to_ids[a.lower().strip()].append(iid)
    for ga in item.get("global_aliases", []):
        old_alias_to_ids[ga.lower().strip()].append(iid)

def tokenize(s):
    return set(re.sub(r'[^a-z0-9\u4e00-\u9fff]', ' ', s.lower()).split())

def jaccard(a, b):
    ta = tokenize(a)
    tb = tokenize(b)
    if not ta or not tb:
        return 0
    return len(ta & tb) / len(ta | tb)

# ============================================================
# 2. PER-NODE REVIEW
# ============================================================
print(f"\n  Reviewing {len(new_items)} new items...")

reviews = []
stats = defaultdict(int)
theme_stats = defaultdict(lambda: {"total": 0, "approve": 0, "keep_a": 0, "keep_b": 0, "demote_c": 0,
                                     "dep_fix": 0, "pp_sync": 0, "merge_collapse": 0, "section_review": 0})

dep_fix_candidates = []
pp_sync_candidates = []
merge_candidates = []
patch_preview_items = []

new_by_name = {}
for iid, item in new_items.items():
    name = item.get("name", "")
    nl = name.lower().strip()
    new_by_name[nl] = iid

for idx, (iid, item) in enumerate(new_items.items()):
    name = item.get("name", "")
    en_name = item.get("en_name", "")
    section_id = item.get("id", "").rsplit(".", 1)[0] if "." in item.get("id", "") else ""
    deps = item.get("direct_pre", [])
    resolved = item.get("resolved_pre", [])
    review_status = item.get("review_status", "C")
    rel = item.get("rel", [])
    tracks = item.get("tracks", [])
    audience = item.get("audience", [])
    visibility = item.get("visibility", "public")
    problem_patterns = item.get("problem_patterns", [])
    parent_concept = item.get("parent_concept", "")

    cand = item_to_candidate.get(iid, {})
    cid = cand.get("candidate_id", "")
    cand_type_orig = cand.get("candidate_type", "core_concept")
    risk_band = cand.get("risk_band", "green")
    is_repl = cand.get("is_replacement", False)
    theme = ""
    pool_entry = pool_by_cid.get(cid, {})
    if pool_entry:
        theme = pool_entry.get("theme", "")

    issues = []
    warnings = []
    suggested_patch = {}
    review_result = "approve"
    new_priority = "C"
    item_type = cand_type_orig

    nl = name.lower().strip()
    enl = en_name.lower().strip() if en_name else ""

    # ---------- 1. DUPLICATE CHECK ----------
    # vs old items
    exact_dup_old = None
    if nl in old_name_to_ids:
        exact_dup_old = old_name_to_ids[nl]
    if not exact_dup_old and enl and enl in old_name_to_ids:
        exact_dup_old = old_name_to_ids[enl]
    if not exact_dup_old and enl and enl in old_en_to_ids:
        exact_dup_old = old_en_to_ids[enl]

    # vs new items (other new items with same name)
    new_dup_count = sum(1 for nid, ni in new_items.items() if nid != iid and ni.get("name", "").lower().strip() == nl)

    # High similarity vs old
    high_sim_old = []
    for oid, oitem in old_items.items():
        sim = max(jaccard(name, oitem.get("name", "")), jaccard(en_name, oitem.get("en_name", "")))
        if sim >= 0.80:
            high_sim_old.append({"item_id": oid, "name": oitem.get("name", ""), "similarity": round(sim, 3)})
    high_sim_old.sort(key=lambda x: -x["similarity"])

    # High similarity vs new
    high_sim_new = []
    for nid, nitem in new_items.items():
        if nid != iid:
            sim = jaccard(name, nitem.get("name", ""))
            if sim >= 0.85:
                high_sim_new.append({"item_id": nid, "name": nitem.get("name", ""), "similarity": round(sim, 3)})
    high_sim_new.sort(key=lambda x: -x["similarity"])

    has_blocking_issue = False

    if exact_dup_old:
        issues.append(f"exact_duplicate_with_old: {exact_dup_old}")
        has_blocking_issue = True
        suggested_patch["merge_with"] = exact_dup_old[0]
    if new_dup_count > 0:
        issues.append(f"duplicate_with_new_peer: {new_dup_count} other new items")
        has_blocking_issue = True
    if high_sim_old and not exact_dup_old:
        top = high_sim_old[0]
        if top["similarity"] >= 0.90:
            issues.append(f"near_duplicate_old: {top['name']} (sim={top['similarity']})")
            has_blocking_issue = True
    if high_sim_new:
        top = high_sim_new[0]
        warnings.append(f"near_duplicate_new: {top['name']} (sim={top['similarity']})")

    # ---------- 2. DIRECT_PRE QUALITY ----------
    if not deps:
        is_root_like = (
            "入门" in name or "基础" in name or "概述" in name or
            "基本" in name or "概念" in name or "原理" in name or
            "调试" in name or "规则" in name or "赛制" in name or
            "工具" in name or "配置" in name or "环境" in name or
            "引用" in name or "override" in name or "final" in name or
            cand_type_orig == "application_case" or
            "C++" in name or "比赛" in name or "竞赛" in name
        )
        if not is_root_like:
            issues.append("empty_direct_pre_not_justified")
            has_blocking_issue = True
        else:
            warnings.append("empty_direct_pre_reasonable")

    if len(deps) > 12:
        issues.append(f"direct_pre_overlong:{len(deps)}")
        has_blocking_issue = True

    section_like_deps = [d for d in deps if re.match(r'^\d+\.\d+$', str(d))]
    if section_like_deps:
        issues.append(f"section_ref_in_direct_pre: {section_like_deps}")
        has_blocking_issue = True

    # Cleanup plan unresolved deps -> informational only (skipped during merge)
    cu = cleanup_by_cid.get(cid, {})
    unresolved_count = len(cu.get("unresolved_pre", []))
    if unresolved_count > 0:
        warnings.append(f"skipped_unresolved_pre:{unresolved_count} (informational, merge successful)")

    # ---------- 3. PROBLEM PATTERN CHECK ----------
    pp_candidate = (
        cand_type_orig == "modeling_pattern" or
        "建模" in name or "题型" in name or
        "转化" in name or "构建" in name
    )
    if pp_candidate and not problem_patterns:
        warnings.append("suggested_sync_to_problem_patterns")

    # ---------- 4. ITEM TYPE CHECK ----------
    if cand_type_orig == "unclear" or not cand_type_orig:
        if "建模" in name or "题型" in name or "转化" in name:
            item_type = "modeling_pattern"
        elif "定理" in name or "性质" in name or "结论" in name:
            item_type = "theorem_or_property"
        elif "实现" in name or "技巧" in name or "优化" in name or "变体" in name:
            item_type = "implementation_variant"
        elif "应用" in name or "案例" in name or "场景" in name:
            item_type = "application_case"
        if item_type != cand_type_orig:
            warnings.append(f"item_type_refined: {cand_type_orig} -> {item_type}")

    # ---------- 5. SECTION REVIEW ----------
    if not section_id or section_id not in sections:
        issues.append("section_review_needed")
        has_blocking_issue = True

    # ---------- 6. FINAL REVIEW RESULT ----------
    if has_blocking_issue:
        dup_related = any("duplicate" in i or "near_duplicate" in i for i in issues)
        dep_related = any("direct_pre" in i or "empty_direct" in i or "section_ref" in i for i in issues)
        sec_related = any("section_review" in i for i in issues)
        if dup_related:
            review_result = "needs_merge_or_collapse"
        elif sec_related:
            review_result = "needs_section_review"
        elif dep_related:
            review_result = "needs_dependency_fix"
        else:
            review_result = "keep_manual_review"
    else:
        review_result = "approve"

    # ---------- 7. PRIORITY ASSIGNMENT ----------
    if review_result in ("needs_merge_or_collapse", "needs_dependency_fix", "needs_section_review"):
        new_priority = "A"
    elif review_result == "keep_manual_review":
        new_priority = "B"
    else:
        new_priority = "C"

    need_manual = new_priority in ("A", "B")

    # pp_sync is a suggestion, not a blocking issue
    pp_sync_suggestion = "suggested_sync_to_problem_patterns" in " ".join(warnings)

    # ---------- 8. STATS ----------
    if review_result == "approve":
        stats["approve"] += 1
    if review_result == "needs_dependency_fix":
        stats["needs_dependency_fix"] += 1
    if review_result == "needs_merge_or_collapse":
        stats["needs_merge_or_collapse"] += 1
    if review_result == "move_to_problem_patterns":
        stats["move_to_problem_patterns"] += 1
    if review_result == "needs_section_review":
        stats["needs_section_review"] += 1
    if review_result == "keep_manual_review":
        stats["keep_manual_review"] += 1

    if new_priority == "A":
        stats["priority_A"] += 1
    elif new_priority == "B":
        stats["priority_B"] += 1
    else:
        stats["priority_C"] += 1

    t = theme or "unknown"
    theme_stats[t]["total"] += 1
    if review_result == "approve":
        theme_stats[t]["approve"] += 1
    if new_priority == "A":
        theme_stats[t]["keep_a"] += 1
    elif new_priority == "B":
        theme_stats[t]["keep_b"] += 1
    else:
        theme_stats[t]["demote_c"] += 1
    if review_result == "needs_dependency_fix":
        theme_stats[t]["dep_fix"] += 1
    if pp_sync_suggestion:
        theme_stats[t]["pp_sync"] += 1
    if review_result == "needs_merge_or_collapse":
        theme_stats[t]["merge_collapse"] += 1
    if review_result == "needs_section_review":
        theme_stats[t]["section_review"] += 1

    # ---------- 8. BUILD REVIEW ----------
    review_entry = {
        "id": iid,
        "name": name,
        "series": section_id,
        "section_name": sections.get(section_id, {}).get("name", ""),
        "review_result": review_result,
        "new_review_priority": new_priority,
        "need_manual_review": need_manual,
        "item_type": item_type,
        "issues": issues,
        "warnings": warnings,
        "suggested_patch": suggested_patch,
        "reason": "; ".join(issues) if issues else ("no issues found; " + "; ".join(warnings)) if warnings else "no issues found",
        "candidate_id": cid,
        "candidate_type_original": cand_type_orig,
        "risk_band": risk_band,
        "is_replacement": is_repl,
        "theme": theme,
        "direct_pre_count": len(deps),
        "resolved_pre_count": len(resolved),
        "rel_count": len(rel),
        "dup_check": {
            "exact_dup_old": exact_dup_old,
            "new_dup_count": new_dup_count,
            "high_sim_old_top3": high_sim_old[:3],
            "high_sim_new_top3": high_sim_new[:3]
        }
    }
    reviews.append(review_entry)

    # Collect for output files
    if review_result == "needs_dependency_fix":
        dep_fix_candidates.append({
            "id": iid, "name": name, "candidate_id": cid, "theme": theme,
            "unresolved_deps": cu.get("unresolved_pre", []),
            "issues": issues
        })
    if pp_sync_suggestion:
        pp_sync_candidates.append({
            "id": iid, "name": name, "candidate_id": cid, "theme": theme,
            "item_type": item_type, "issues": issues,
            "suggested_problem_patterns": [name]
        })
    if review_result == "needs_merge_or_collapse":
        merge_candidates.append({
            "id": iid, "name": name, "candidate_id": cid, "theme": theme,
            "merge_with": suggested_patch.get("merge_with", ""),
            "issues": issues
        })

    if suggested_patch or new_priority != review_status:
        patch_preview_items.append({
            "id": iid, "name": name,
            "field": "review_status" if new_priority != review_status else ("review_status"),
            "old_value": review_status, "new_value": new_priority,
            "reason": "; ".join(issues) if issues else "promoted to manual review"
        })

    if (idx + 1) % 100 == 0:
        print(f"    Reviewed {idx + 1}/{len(new_items)}...")

print(f"\n  Review complete.")

# ============================================================
# 3. DIRECT_PRE QUALITY STATS
# ============================================================
dp_stats = {"empty": 0, "1-3": 0, "4-6": 0, "7-12": 0, "12+": 0, "total": 0, "avg": 0}
for r in reviews:
    cnt = r["direct_pre_count"]
    dp_stats["total"] += cnt
    if cnt == 0:
        dp_stats["empty"] += 1
    elif cnt <= 3:
        dp_stats["1-3"] += 1
    elif cnt <= 6:
        dp_stats["4-6"] += 1
    elif cnt <= 12:
        dp_stats["7-12"] += 1
    else:
        dp_stats["12+"] += 1
dp_stats["avg"] = round(dp_stats["total"] / max(len(reviews), 1), 1)

# ============================================================
# 4. OUTPUT FILES
# ============================================================
print(f"\n  Writing outputs...")

# --- REVIEW JSON ---
review_output = {
    "meta": {
        "generated_by": "stage3g_full400_added_items_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False,
        "patches_applied": False,
        "review_applied": False,
        "total_reviewed": len(reviews),
        "total_added": len(new_items),
        "item_count_before": len(old_items),
        "item_count_current": len(all_items)
    },
    "summary": {
        "approve": stats.get("approve", 0),
        "keep_manual_review_A": stats.get("priority_A", 0),
        "keep_manual_review_B": stats.get("priority_B", 0),
        "demote_to_C": stats.get("priority_C", 0),
        "needs_dependency_fix": stats.get("needs_dependency_fix", 0),
        "needs_merge_or_collapse": stats.get("needs_merge_or_collapse", 0),
        "suggested_problem_pattern_sync": len(pp_sync_candidates),
        "needs_section_review": stats.get("needs_section_review", 0),
        "keep_manual_review": stats.get("keep_manual_review", 0)
    },
    "direct_pre_quality": dp_stats,
    "theme_review": {t: dict(ts) for t, ts in sorted(theme_stats.items())},
    "reviews": reviews
}
with open(OUT_REVIEW, "w", encoding="utf-8") as f:
    json.dump(review_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_REVIEW}")

# --- PATCH PREVIEW ---
patch_output = {
    "meta": {
        "generated_by": "stage3g_full400_added_items_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "patches_preview_only": True,
        "do_not_apply": True,
        "total_patches": len(patch_preview_items)
    },
    "patches": patch_preview_items
}
with open(OUT_PATCH, "w", encoding="utf-8") as f:
    json.dump(patch_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PATCH}")

# --- DEP FIX CANDIDATES ---
dep_fix_output = {
    "meta": {
        "generated_by": "stage3g_full400_added_items_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_needs_dependency_fix": len(dep_fix_candidates)
    },
    "candidates": dep_fix_candidates
}
with open(OUT_DEP_FIX, "w", encoding="utf-8") as f:
    json.dump(dep_fix_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_DEP_FIX}")

# --- PROBLEM PATTERN SYNC ---
pp_output = {
    "meta": {
        "generated_by": "stage3g_full400_added_items_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_suggested_sync": len(pp_sync_candidates)
    },
    "candidates": pp_sync_candidates
}
with open(OUT_PP_SYNC, "w", encoding="utf-8") as f:
    json.dump(pp_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PP_SYNC}")

# --- MERGE / COLLAPSE ---
merge_output = {
    "meta": {
        "generated_by": "stage3g_full400_added_items_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_needs_merge_or_collapse": len(merge_candidates)
    },
    "candidates": merge_candidates
}
with open(OUT_MERGE, "w", encoding="utf-8") as f:
    json.dump(merge_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_MERGE}")

# --- REPORT ---
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(f"# Stage3G full400 新增节点复查报告\n\n")
    f.write(f"**生成时间**: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"**复查脚本**: stage3g_full400_added_items_review.py\n\n")

    f.write(f"## 1. 总体结论\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| 新增节点总数 | 400 |\n")
    f.write(f"| 原始节点数 | {len(old_items)} |\n")
    f.write(f"| 当前节点数 | {len(all_items)} |\n")
    f.write(f"| approve (无需操作) | {stats.get('approve', 0)} |\n")
    f.write(f"| 降为 C (无需人工) | {stats.get('priority_C', 0)} |\n")
    f.write(f"| 保留 B (建议人工复查) | {stats.get('priority_B', 0)} |\n")
    f.write(f"| 保留 A (必须人工复查) | {stats.get('priority_A', 0)} |\n")
    f.write(f"| needs_dependency_fix | {stats.get('needs_dependency_fix', 0)} |\n")
    f.write(f"| suggested_problem_pattern_sync | {len(pp_sync_candidates)} |\n")
    f.write(f"| needs_merge_or_collapse | {stats.get('needs_merge_or_collapse', 0)} |\n")
    f.write(f"| needs_section_review | {stats.get('needs_section_review', 0)} |\n")
    f.write(f"| keep_manual_review | {stats.get('keep_manual_review', 0)} |\n")
    f.write(f"| 修改主图谱 | 否 |\n")
    f.write(f"| 应用补丁 | 否 |\n\n")

    f.write(f"## 2. 各主题复查结论\n\n")
    f.write(f"| Theme | 总数 | approve | A | B | C | dep_fix | pp_sync | merge | sec_review |\n")
    f.write(f"|-------|-------|---------|---|---|---|---------|---------|-------|------------|\n")
    for t in sorted(theme_stats.keys()):
        ts = theme_stats[t]
        f.write(f"| {t} | {ts['total']} | {ts['approve']} | {ts['keep_a']} | {ts['keep_b']} | {ts['demote_c']} | {ts['dep_fix']} | {ts['pp_sync']} | {ts['merge_collapse']} | {ts['section_review']} |\n")

    f.write(f"\n## 3. direct_pre 质量统计\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| direct_pre 总数 | {dp_stats['total']} |\n")
    f.write(f"| 平均 | {dp_stats['avg']} |\n")
    f.write(f"| empty (0) | {dp_stats['empty']} |\n")
    f.write(f"| 1-3 | {dp_stats['1-3']} |\n")
    f.write(f"| 4-6 | {dp_stats['4-6']} |\n")
    f.write(f"| 7-12 | {dp_stats['7-12']} |\n")
    f.write(f"| 12+ | {dp_stats['12+']} |\n\n")

    f.write(f"## 4. 是否建议进入 full400 轻量修复\n\n")
    has_blocking = (stats.get("needs_merge_or_collapse", 0) > 0 or
                    stats.get("needs_dependency_fix", 0) > 0)
    if has_blocking:
        f.write(f"[WARN] 建议先执行轻量修复：\n")
        f.write(f"- needs_merge_or_collapse: {stats.get('needs_merge_or_collapse', 0)} 个\n")
        f.write(f"- needs_dependency_fix: {stats.get('needs_dependency_fix', 0)} 个\n")
        f.write(f"\n请审查 `stage3g_full400_review_status_patch_preview.json` 后手动修复。\n")
    else:
        f.write(f"[OK] 无需轻量修复，所有节点可直接进入 C 级。\n")

    f.write(f"\n## 5. 是否建议继续 Stage3G Batch2\n\n")
    if stats.get("needs_merge_or_collapse", 0) <= 5 and stats.get("needs_dependency_fix", 0) <= 30:
        f.write(f"[OK] 阻塞项较少，建议继续 Stage3G Batch2。\n")
        f.write(f"当前 item_count={len(all_items)}，Batch2 可继续扩展。\n")
    else:
        f.write(f"[WARN] 阻塞项较多，建议先执行轻量修复再继续 Batch2。\n")

    f.write(f"\n---\n")
    f.write(f"*本报告由 stage3g_full400_added_items_review.py 自动生成*\n")
    f.write(f"*不修改主图谱，不应用补丁*\n")

print(f"    [OK] {OUT_REPORT}")

# ============================================================
# 5. SUMMARY
# ============================================================
print(f"\n{'=' * 60}")
print(f"      REVIEW SUMMARY")
print(f"{'=' * 60}")
print(f"  Total reviewed: {len(reviews)}")
print(f"  Approve (no action): {stats.get('approve', 0)}")
print(f"  Priority C: {stats.get('priority_C', 0)}")
print(f"  Priority B: {stats.get('priority_B', 0)}")
print(f"  Priority A: {stats.get('priority_A', 0)}")
print(f"  Needs dep fix: {stats.get('needs_dependency_fix', 0)}")
print(f"  Needs merge/collapse: {stats.get('needs_merge_or_collapse', 0)}")
print(f"  Move to PP: {stats.get('move_to_problem_patterns', 0)}")
print(f"  Needs section review: {stats.get('needs_section_review', 0)}")
print(f"\n  Done. No patches applied. No graph modified.")
