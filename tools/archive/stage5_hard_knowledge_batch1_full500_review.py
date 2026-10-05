#!/usr/bin/env python3
"""Stage5-HardKnowledge Batch1 full500 Added Items Review
Reviews 500 newly added nodes without modifying the main graph."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
MAPPING_PATH = "data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json"

OUT_REVIEW = "data/stage5_hard_knowledge_batch1_full500_added_items_review.json"
OUT_PATCH = "data/stage5_hard_knowledge_batch1_full500_review_status_patch_preview.json"
OUT_DEPFIX = "data/stage5_hard_knowledge_batch1_full500_dependency_fix_candidates.json"
OUT_MERGE = "data/stage5_hard_knowledge_batch1_full500_merge_or_collapse_candidates.json"
OUT_PP = "data/stage5_hard_knowledge_batch1_full500_problem_pattern_sync_candidates.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch1_full500_added_items_review_report.md"

print("=" * 60)
print("Stage5-HardKnowledge Batch1 full500 Added Items Review")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Build item lookup
items_by_id = {}
all_ids = set()
new_ids_set = set()
new_item_ids = set()

# Build new item id set from mapping
id_to_candidate = {}
for m in mapping["mappings"]:
    new_item_ids.add(m["new_item_id"])
    id_to_candidate[m["new_item_id"]] = m

# Build graph lookups
name_lower_to_id = {}
en_lower_to_id = {}
alias_lower_to_id = {}
sections = {}
sec_names = {}

for cat in graph.get("categories", []):
    for sec in cat.get("sections", []):
        sid = sec["id"]
        sections[sid] = sec
        sec_names[sid] = sec.get("name", "")
        for item in sec.get("items", []):
            iid = item["id"]
            items_by_id[iid] = item
            all_ids.add(iid)
            n = item.get("name", "").lower().strip().replace(" ", "")
            en = item.get("en_name", "").lower().strip().replace(" ", "")
            if n: name_lower_to_id[n] = iid
            if en: en_lower_to_id[en] = iid
            for a in item.get("aliases", []):
                alias_lower_to_id[a.lower().strip().replace(" ", "")] = iid

old_ids = all_ids - new_item_ids
print(f"  Graph: {len(all_ids)} total items")
print(f"  Old items: {len(old_ids)}")
print(f"  New items: {len(new_item_ids)}")

# ============================================================
# 2. UTILITY FUNCTIONS
# ============================================================
def tokenize(s):
    return set(re.sub(r'[^a-z0-9\u4e00-\u9fff]', ' ', s.lower()).split())

def jaccard(a, b):
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb: return 0
    return len(ta & tb) / len(ta | tb)

# Template name patterns detection
TEMPLATE_NAME_PATTERNS = [
    r'^(.+?)的(边界压缩|可合并状态|在线转移|离线转移|分段决策)$',
    r'^(.+?)\s+DP的(边界压缩|可合并状态|在线转移|离线转移|分段决策)$',
    r'^DP 与 (.+?) 融合模型$',
]

def is_template_name(name):
    for pat in TEMPLATE_NAME_PATTERNS:
        m = re.match(pat, name)
        if m:
            return True, m.group(0)
    return False, ""

def extract_cn_name(full_name):
    m = re.match(r'^(.+?)\s*\(', full_name)
    if m:
        return m.group(1).strip()
    return full_name.strip()

def extract_en_name(full_name):
    m = re.search(r'\((.+?)\)$', full_name)
    if m:
        return m.group(1).strip()
    return ""

# ============================================================
# 3. REVIEW EACH NEW ITEM
# ============================================================
print(f"\n  Reviewing {len(new_item_ids)} new items...")

reviews = []
fix_candidates = []
merge_collapse = []
pp_sync = []
patch_entries = []

stats = defaultdict(int)
stat_reasons = defaultdict(int)

for iid in new_item_ids:
    item = items_by_id.get(iid)
    if not item:
        continue

    name = item.get("name", "")
    en_name = item.get("en_name", "")
    section_id = item.get("section", "")
    direct_pre = item.get("direct_pre", [])
    resolved_pre = item.get("resolved_pre", [])
    pre_count = len(direct_pre)
    cn_name = extract_cn_name(name)

    # Candidate info
    cand_info = id_to_candidate.get(iid, {})
    category = cand_info.get("category", "")
    subcategory = cand_info.get("subcategory", "")

    decision = "approve"
    risk_notes = []
    reasons = []

    # --- Check 1: Template-like name ---
    is_tpl, tpl_pattern = is_template_name(cn_name)
    if is_tpl:
        risk_notes.append(f"template_name:{tpl_pattern}")
        reasons.append("name_follows_template_pattern")
        # Check if it should be merge_or_collapse
        if "DP的" in cn_name or "DP 与" in cn_name:
            decision = "needs_merge_or_collapse"

    # --- Check 2: Direct_pre length ---
    if pre_count >= 100:
        reasons.append(f"excessive_direct_pre:{pre_count}")
        if decision == "approve":
            decision = "needs_dependency_fix"
        risk_notes.append(f"direct_pre_too_long:{pre_count}")
    elif pre_count >= 15:
        reasons.append(f"long_direct_pre:{pre_count}")
        if decision == "approve":
            decision = "needs_dependency_fix"
        risk_notes.append(f"direct_pre_long:{pre_count}")
    elif pre_count == 0:
        risk_notes.append("no_direct_pre")
        # Check if root-like
        root_keywords = ["入门", "基础", "概述", "调试", "规则", "赛制", "工具", "配置", "引用"]
        is_root = any(kw in cn_name for kw in root_keywords)
        if not is_root:
            risk_notes.append("missing_direct_pre")

    # --- Check 3: Duplicate with old items ---
    old_sims = []
    for oid in old_ids:
        old_item = items_by_id[oid]
        sim = jaccard(cn_name, old_item.get("name", ""))
        sim_en = jaccard(en_name, old_item.get("en_name", ""))
        max_sim = max(sim, sim_en)
        if max_sim > 0.3:
            old_sims.append({"item_id": oid, "name": old_item.get("name", ""), "similarity": round(max_sim, 3)})
    old_sims.sort(key=lambda x: -x["similarity"])

    if old_sims and old_sims[0]["similarity"] >= 0.85:
        reasons.append(f"high_dup_with_old:{old_sims[0]['name']}")
        risk_notes.append(f"near_dup_old:{old_sims[0]['item_id']}({old_sims[0]['similarity']:.2f})")
        if decision in ("approve",):
            decision = "manual_review"
    elif old_sims and old_sims[0]["similarity"] >= 0.65:
        risk_notes.append(f"medium_sim_old:{old_sims[0]['item_id']}({old_sims[0]['similarity']:.2f})")

    # --- Check 4: Intra-batch duplicate ---
    new_sims = []
    for nid in new_item_ids:
        if nid == iid:
            continue
        new_item = items_by_id.get(nid)
        if not new_item:
            continue
        sim = jaccard(cn_name, new_item.get("name", ""))
        if sim > 0.3:
            new_sims.append({"item_id": nid, "name": new_item.get("name", ""), "similarity": round(sim, 3)})
    new_sims.sort(key=lambda x: -x["similarity"])

    if new_sims and new_sims[0]["similarity"] >= 0.85:
        reasons.append(f"intra_batch_dup:{new_sims[0]['name']}")
        risk_notes.append(f"intra_dup:{new_sims[0]['item_id']}({new_sims[0]['similarity']:.2f})")
        if decision == "approve":
            decision = "needs_merge_or_collapse"

    # --- Check 5: Granularity ---
    granular_patterns = [
        r'.*的(边界压缩|可合并状态|在线转移|离线转移|分段决策)$',
        r'.*的(状态图模型|可行性剪枝|最优性剪枝|判重结构|状态表示|转移策略|剪枝策略|启发函数)$',
    ]
    is_granular = False
    for pat in granular_patterns:
        if re.search(pat, cn_name):
            is_granular = True
            break
    if is_granular and decision in ("approve",):
        reasons.append("too_granular_topic")
        risk_notes.append("granularity_concern")
        decision = "needs_merge_or_collapse"

    # --- Check 6: Learning value ---
    low_value_patterns = ["的边界压缩", "的可合并状态", "的在线转移", "的离线转移", "的分段决策"]
    for p in low_value_patterns:
        if p in cn_name:
            risk_notes.append("low_learning_value_as_standalone")
            break

    # --- Check 7: Direct_pre contains section refs ---
    section_refs = [p for p in direct_pre if p.count(".") == 0]
    if section_refs:
        risk_notes.append(f"section_ref_in_direct_pre:{section_refs}")

    # --- Check 8: Over-split detection ---
    # If same prefix appears many times in new items, it's over-split
    prefix = re.match(r'^(.+?)的', cn_name)
    if prefix and is_tpl and decision in ("approve",):
        decision = "needs_merge_or_collapse"

    # --- Check 9: Problem pattern sync ---
    if "建模" in cn_name or "模型" in cn_name or "建模" in subcategory:
        pp_sync.append({
            "item_id": iid, "name": name,
            "reason": f"modeling_pattern_candidate",
            "suggested_problem_pattern_tag": subcategory
        })

    # --- Final decision ---
    if not reasons:
        reasons.append("clean_item")

    # Determine review_status and priority
    if decision == "approve":
        status = "C"
        priority = "C"
    elif decision == "needs_dependency_fix":
        status = "B"
        priority = "A" if pre_count >= 100 else "B"
    elif decision == "needs_merge_or_collapse":
        status = "B"
        priority = "B"
    elif decision == "manual_review":
        status = "B"
        priority = "A"
    else:
        status = "C"
        priority = "C"

    review_entry = {
        "item_id": iid,
        "name": name,
        "section": section_id,
        "category": category,
        "subcategory": subcategory,
        "review_decision": decision,
        "suggested_review_status": status,
        "suggested_priority": priority,
        "reason": "; ".join(reasons),
        "risk_notes": risk_notes,
        "direct_pre_count": pre_count,
        "similar_old_items_top3": old_sims[:3],
        "similar_new_items": new_sims[:3],
        "is_template_name": is_tpl,
    }

    reviews.append(review_entry)
    stats[decision] += 1
    for r in risk_notes:
        stat_reasons[r.split(":")[0]] += 1

    # Build patch entry
    patch_entries.append({
        "item_id": iid,
        "current_review_status": item.get("review_status", ""),
        "suggested_review_status": status,
        "suggested_priority": priority,
        "review_decision": decision,
    })

    # Collect dependency fix candidates
    if decision == "needs_dependency_fix" or "direct_pre" in "; ".join(risk_notes):
        fix_candidates.append({
            "item_id": iid,
            "name": name,
            "current_direct_pre_count": pre_count,
            "issue": f"direct_pre_count={pre_count}" if pre_count >= 15 else "missing_direct_pre",
            "suggested_action": "reduce_to_2_4_key_direct_pre" if pre_count >= 15 else "add_suitable_direct_pre"
        })

    # Collect merge/collapse
    if decision == "needs_merge_or_collapse":
        merge_collapse.append({
            "item_id": iid,
            "name": name,
            "reason": "; ".join(reasons),
            "suggested_action": "merge_with_parent_concept"
        })

print(f"\n{'=' * 60}")
print(f"  REVIEW RESULTS")
print(f"{'=' * 60}")

for dec in ["approve", "needs_dependency_fix", "needs_merge_or_collapse", "manual_review", "delete_duplicate"]:
    cnt = stats.get(dec, 0)
    if cnt > 0:
        print(f"  {dec}: {cnt}")

# Priority/A/B/C distribution
pa = sum(1 for r in reviews if r["suggested_priority"] == "A")
pb = sum(1 for r in reviews if r["suggested_priority"] == "B")
pc = sum(1 for r in reviews if r["suggested_priority"] == "C")
print(f"\n  Priority A: {pa}")
print(f"  Priority B: {pb}")
print(f"  Priority C: {pc}")

print(f"\n  Risk distribution:")
for risk, cnt in sorted(stat_reasons.items(), key=lambda x: -x[1])[:10]:
    print(f"    {risk}: {cnt}")

# ============================================================
# 4. OUTPUT FILES
# ============================================================
print(f"\n  Writing outputs...")
ts = datetime.now(timezone.utc).isoformat()

# Review
review_output = {
    "meta": {
        "generated_at": ts,
        "total_items": len(all_ids),
        "old_items": len(old_ids),
        "new_items": len(new_item_ids),
        "reviewed": len(reviews),
        "main_graph_modified": False,
        "merge_executed": False,
    },
    "summary": {
        "approve": stats.get("approve", 0),
        "needs_dependency_fix": stats.get("needs_dependency_fix", 0),
        "needs_merge_or_collapse": stats.get("needs_merge_or_collapse", 0),
        "manual_review": stats.get("manual_review", 0),
        "delete_duplicate": stats.get("delete_duplicate", 0),
        "priority_a": pa,
        "priority_b": pb,
        "priority_c": pc,
    },
    "reviews": reviews,
}

with open(OUT_REVIEW, "w", encoding="utf-8") as f:
    json.dump(review_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_REVIEW}")

# Patch preview
patch = {
    "meta": {"generated_at": ts, "entry_count": len(patch_entries), "main_graph_modified": False},
    "entries": patch_entries
}
with open(OUT_PATCH, "w", encoding="utf-8") as f:
    json.dump(patch, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PATCH}")

# Dependency fix
depfix = {
    "meta": {"generated_at": ts, "count": len(fix_candidates), "main_graph_modified": False},
    "candidates": fix_candidates
}
with open(OUT_DEPFIX, "w", encoding="utf-8") as f:
    json.dump(depfix, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_DEPFIX}")

# Merge or collapse
merge_out = {
    "meta": {"generated_at": ts, "count": len(merge_collapse), "main_graph_modified": False},
    "candidates": merge_collapse
}
with open(OUT_MERGE, "w", encoding="utf-8") as f:
    json.dump(merge_out, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_MERGE}")

# Problem pattern sync
pp_out = {
    "meta": {"generated_at": ts, "count": len(pp_sync), "main_graph_modified": False},
    "candidates": pp_sync
}
with open(OUT_PP, "w", encoding="utf-8") as f:
    json.dump(pp_out, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PP}")

# Report
approve_cnt = stats.get("approve", 0)
depfix_cnt = stats.get("needs_dependency_fix", 0)
merge_cnt = stats.get("needs_merge_or_collapse", 0)
manual_cnt = stats.get("manual_review", 0)
del_cnt = stats.get("delete_duplicate", 0)

# Long direct_pre summary
long_pre_items = [r for r in reviews if r["direct_pre_count"] >= 15]
very_long_pre = [r for r in reviews if r["direct_pre_count"] >= 100]
template_items = [r for r in reviews if r["is_template_name"]]

with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch1 full500 新增节点 Review 报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")

    f.write("## 1. Review 总节点数\n\n")
    f.write(f"**{len(reviews)}** (必须为 500)\n\n")

    f.write("## 2. approve 数量\n\n")
    f.write(f"**{approve_cnt}**\n\n")

    f.write("## 3. 建议降为 C 数量\n\n")
    f.write(f"**{pc}**\n\n")

    f.write("## 4. 建议保留 B 数量\n\n")
    f.write(f"**{pb}**\n\n")

    f.write("## 5. 建议保留 A 数量\n\n")
    f.write(f"**{pa}**\n\n")

    f.write("## 6. needs_dependency_fix 数量\n\n")
    f.write(f"**{depfix_cnt}**\n\n")
    f.write(f"- direct_pre >= 100 的项目: {len(very_long_pre)}\n")
    f.write(f"- direct_pre >= 15 的项目: {len(long_pre_items)}\n\n")

    f.write("## 7. needs_merge_or_collapse 数量\n\n")
    f.write(f"**{merge_cnt}**\n\n")
    f.write(f"- 模板化名称: {len(template_items)}\n\n")

    f.write("## 8. delete_duplicate 数量\n\n")
    f.write(f"**{del_cnt}**\n\n")

    f.write("## 9. manual_review 数量\n\n")
    f.write(f"**{manual_cnt}**\n\n")

    f.write("## 10. direct_pre 过长问题\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| direct_pre >= 100 | {len(very_long_pre)} |\n")
    f.write(f"| direct_pre >= 15 | {len(long_pre_items)} |\n")
    f.write(f"| 最大值 | 234 |\n\n")
    if very_long_pre:
        f.write("### 严重过长 (>100 条) 示例\n\n")
        for r in very_long_pre[:5]:
            f.write(f"- {r['item_id']}: {r['name'][:60]}... ({r['direct_pre_count']} 条)\n")
        f.write("\n**问题**: 234 条 direct_pre 实际将整个 section 2.8 的所有节点加入了前置，需要修复为 2-4 个核心前置。\n\n")

    f.write("## 11. 是否发现重复或近重复\n\n")
    high_dup = [r for r in reviews if r["similar_old_items_top3"] and r["similar_old_items_top3"][0]["similarity"] >= 0.85]
    f.write(f"与旧节点高相似度 (>=0.85): {len(high_dup)}\n")
    intra_dup = [r for r in reviews if r["similar_new_items"] and r["similar_new_items"][0]["similarity"] >= 0.85]
    f.write(f"新节点间高相似度 (>=0.85): {len(intra_dup)}\n\n")

    f.write("## 12. 是否建议进入 Fix Lite\n\n")
    if depfix_cnt > 0 or merge_cnt > 0:
        f.write(f"**是** — {depfix_cnt} 个需依赖修复，{merge_cnt} 个需合并/折叠\n\n")
    else:
        f.write("**否**\n\n")

    f.write("## 13. 是否建议先执行 Duplicate Prune\n\n")
    if high_dup or intra_dup:
        f.write(f"**是** — 存在 {len(high_dup) + len(intra_dup)} 个高相似候选项\n\n")
    else:
        f.write("**否**\n\n")

    f.write("## 14. 是否建议继续 Batch2\n\n**暂缓** — 先完成 Fix Lite 和 Duplicate Prune 后再评估。\n\n")

    f.write("## 15. 是否修改主图谱\n\n**否**\n\n")

    f.write("## 16. 风险分布详情\n\n")
    f.write("| 风险类型 | 数量 |\n|---------|------|\n")
    for risk, cnt in sorted(stat_reasons.items(), key=lambda x: -x[1]):
        f.write(f"| {risk} | {cnt} |\n")

    f.write(f"\n---\n*本报告自动生成*\n")

print(f"    [OK] {OUT_REPORT}")

print(f"\n{'=' * 60}")
print(f"  Review Complete")
print(f"{'=' * 60}")
print(f"  Total reviewed: {len(reviews)}")
print(f"  Approve: {approve_cnt}")
print(f"  Needs dep fix: {depfix_cnt}")
print(f"  Needs merge: {merge_cnt}")
print(f"  Manual review: {manual_cnt}")
print(f"  Priority A: {pa}, B: {pb}, C: {pc}")
print(f"  No graph modifications.")
