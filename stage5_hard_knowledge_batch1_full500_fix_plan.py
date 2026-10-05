#!/usr/bin/env python3
"""Stage5-HardKnowledge Batch1 full500 Dependency Shrink & Merge/Collapse Plan
Generates per-node direct_pre shrink plans and template node merge decisions.
Does NOT modify main graph."""

import json, re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
REVIEW_PATH = "data/stage5_hard_knowledge_batch1_full500_added_items_review.json"
MAPPING_PATH = "data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json"

OUT_SHRINK = "data/stage5_hard_knowledge_batch1_full500_direct_pre_shrink_plan.json"
OUT_SHRINK_PATCH = "data/stage5_hard_knowledge_batch1_full500_direct_pre_shrink_patch_preview.json"
OUT_MERGE = "data/stage5_hard_knowledge_batch1_full500_merge_collapse_resolution_plan.json"
OUT_DECISION = "data/stage5_hard_knowledge_batch1_full500_next_action_decision.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch1_full500_dependency_and_collapse_plan_report.md"

print("=" * 60)
print("Stage5 Batch1 full500 Dependency Shrink & Merge/Collapse Plan")
print("=" * 60)

# ============================================================
# 1. LOAD
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)
with open(REVIEW_PATH, "r", encoding="utf-8") as f:
    review = json.load(f)
with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    mapping = json.load(f)

items_by_id = {}
item_section = {}
section_items = defaultdict(list)
for cat in graph["categories"]:
    for sec in cat["sections"]:
        sec_id = sec["id"]
        for item in sec["items"]:
            iid = item["id"]
            items_by_id[iid] = item
            item_section[iid] = sec_id
            section_items[sec_id].append(iid)

dep_fix_rids = [r for r in review["reviews"] if r["review_decision"] == "needs_dependency_fix"]
tpl_rids = [r for r in review["reviews"] if r["review_decision"] == "needs_merge_or_collapse"]
print(f"  Dep fix: {len(dep_fix_rids)}, Template: {len(tpl_rids)}")

# ============================================================
# 2. IDENTIFY PURE ITEMS (not templates) for shrink
# ============================================================
tpl_ids = set(r["item_id"] for r in tpl_rids)
pure_dep_fix = [r for r in dep_fix_rids if r["item_id"] not in tpl_ids]
tpl_dep_fix = [r for r in dep_fix_rids if r["item_id"] in tpl_ids]

print(f"  Pure dep fix (non-template): {len(pure_dep_fix)}")
print(f"  Template dep fix: {len(tpl_dep_fix)}")

# ============================================================
# 3. BUILD SECTION CORE ITEMS
# For each section, find foundational items (first items, low-level)
# ============================================================
section_core = {}
for sec_id, iids in section_items.items():
    items_in_sec = [(iid, items_by_id[iid]) for iid in iids]
    # Sort by ID numeric part to get the "first" items
    items_in_sec.sort(key=lambda x: int(x[0].split(".")[-1]) if x[0].split(".")[-1].isdigit() else 9999)
    # Take first 2-4 items as section core
    core = [iid for iid, _ in items_in_sec[:4]]
    section_core[sec_id] = core

# Map node name keywords to specific prereq sections/items
KEYWORD_PREREQS = {
    # DP section (2.8) topics
    "DP": {"section": "2.8", "items": section_core.get("2.8", [])[:3]},
    "动态规划": {"section": "2.8", "items": section_core.get("2.8", [])[:3]},
    "凸包": {"section": "2.8", "extra": ["2.8.1"]},
    "分治": {"section": "2.1", "extra": ["2.1.1"]},
    "线段树": {"section": "3.7", "extra": ["3.7.2"]},
    "堆": {"section": "1.5", "extra": ["1.5.1"]},
    "队列": {"section": "1.4", "extra": ["1.4.1"]},
    "前缀": {"section": "2.8", "extra": ["2.8.1"]},
    "后缀": {"section": "2.8", "extra": ["2.8.1"]},
    "自动机": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "矩阵": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    "树状数组": {"section": "3.3", "extra": ["3.3.1"]},
    "最短路": {"section": "2.2", "extra": ["2.2.1", "2.2.3"]},
    "网络流": {"section": "2.11", "extra": section_core.get("2.11", [])[:2]},
    "生成函数": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "连通性": {"section": "2.9", "extra": ["2.9.1"]},
    # Search section (2.7)
    "搜索": {"section": "2.7", "extra": section_core.get("2.7", [])[:2]},
    "A*": {"section": "2.7", "extra": ["2.7.1"]},
    "IDA*": {"section": "2.7", "extra": ["2.7.1"]},
    "DLX": {"section": "2.7", "extra": ["2.7.1"]},
    "迭代加深": {"section": "2.7", "extra": ["2.7.1"]},
    "Meet-in-the-Middle": {"section": "2.7", "extra": ["2.7.1"]},
    "爬山": {"section": "2.7", "extra": ["2.7.1"]},
    "模拟退火": {"section": "2.7", "extra": ["2.7.1"]},
    "启发式": {"section": "2.7", "extra": ["2.7.1"]},
    # Greedy (2.6)
    "贪心": {"section": "2.6", "extra": section_core.get("2.6", [])[:2]},
    "区间调度": {"section": "2.6", "extra": section_core.get("2.6", [])[:2]},
    "区间覆盖": {"section": "2.6", "extra": section_core.get("2.6", [])[:2]},
    "反悔贪心": {"section": "2.6", "extra": section_core.get("2.6", [])[:2]},
    "Huffman": {"section": "2.6", "extra": section_core.get("2.6", [])[:2]},
    # Construction (2.20)
    "构造": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "奇偶": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "染色": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "递归": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "归纳": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "对称": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "模": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    "交互": {"section": "2.20", "extra": section_core.get("2.20", [])[:2]},
    # Graph (2.9)
    "图": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "二分图": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "最小割": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "费用流": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "差分约束": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "闭合子图": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    "匹配": {"section": "2.9", "extra": section_core.get("2.9", [])[:2]},
    # SQRT (2.4)
    "分块": {"section": "2.4", "extra": section_core.get("2.4", [])[:2]},
    "莫队": {"section": "2.4", "extra": section_core.get("2.4", [])[:2]},
    "根号": {"section": "2.4", "extra": section_core.get("2.4", [])[:2]},
    "整除": {"section": "2.4", "extra": section_core.get("2.4", [])[:2]},
    # DS (3.13)
    "并查集": {"section": "3.5", "extra": section_core.get("3.5", [])[:2]},
    "平衡树": {"section": "3.8", "extra": section_core.get("3.8", [])[:2]},
    "可持久化": {"section": "3.13", "extra": section_core.get("3.13", [])[:2]},
    "整体二分": {"section": "2.18", "extra": ["2.18.5"]},
    "扫描线": {"section": "3.7", "extra": ["3.7.2"]},
    # Number theory (4.1)
    "数论": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "欧拉": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "质数": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "素数": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "二次剩余": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "裴蜀": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "连分数": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "佩尔": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "积性": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "狄利克雷": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "筛": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "莫比乌斯": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "原根": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    "同余": {"section": "4.1", "extra": section_core.get("4.1", [])[:2]},
    # Combinatorics (4.3)
    "组合": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "斯特林": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "排列": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "错排": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "染色": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "多项式": {"section": "4.3", "extra": section_core.get("4.3", [])[:2]},
    "FFT": {"section": "2.18", "extra": ["2.18.2"]},
    "NTT": {"section": "2.18", "extra": ["2.18.2"]},
    "子集卷积": {"section": "2.18", "extra": ["2.18.2"]},
    "FWT": {"section": "2.18", "extra": ["2.18.2"]},
    # Linear algebra (2.17)
    "高斯消元": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    "异或": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    "线性": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    "行列式": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    "矩阵树": {"section": "2.17", "extra": section_core.get("2.17", [])[:2]},
    # Probability (4.6)
    "概率": {"section": "4.6", "extra": section_core.get("4.6", [])[:2]},
    "期望": {"section": "4.6", "extra": section_core.get("4.6", [])[:2]},
    "贝叶斯": {"section": "4.6", "extra": section_core.get("4.6", [])[:2]},
    "方差": {"section": "4.6", "extra": section_core.get("4.6", [])[:2]},
    # Game theory (4.5)
    "博弈": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    "Nim": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    "SG": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    "阶梯": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    "威佐夫": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    "不平等": {"section": "4.5", "extra": section_core.get("4.5", [])[:2]},
    # Geometry (4.7)
    "几何": {"section": "4.7", "extra": section_core.get("4.7", [])[:2]},
    "凸包": {"section": "4.7", "extra": section_core.get("4.7", [])[:2]},
    "最近点": {"section": "4.7", "extra": section_core.get("4.7", [])[:2]},
    "圆": {"section": "4.7", "extra": section_core.get("4.7", [])[:2]},
    "三角": {"section": "4.7", "extra": section_core.get("4.7", [])[:2]},
    # String (2.10)
    "字符串": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "字典树": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "哈希": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "KMP": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "后缀": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "Manacher": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
    "Lyndon": {"section": "2.10", "extra": section_core.get("2.10", [])[:2]},
}

def find_prereqs_by_name(name, section_id):
    """Find 2-6 reasonable direct_pre items based on node name and section."""
    prereqs = set()
    
    # 1. Add section core items (first 1-2 items in the section)
    sec_core = section_core.get(section_id, [])
    for iid in sec_core[:2]:
        if iid in items_by_id:
            prereqs.add(iid)
    
    # 2. Add topic-specific prereqs based on name keywords
    for kw, info in KEYWORD_PREREQS.items():
        if kw in name:
            extras = info.get("extra", [])
            for eid in extras:
                if eid in items_by_id and eid not in prereqs:
                    prereqs.add(eid)
                    break
            if len(prereqs) >= 6:
                break
    
    # 3. If still too few, add more section core items
    if len(prereqs) < 2:
        for iid in sec_core[2:]:
            if iid in items_by_id and iid not in prereqs:
                prereqs.add(iid)
                if len(prereqs) >= 3:
                    break
    
    # 4. Ensure 2-6 range
    result = list(prereqs)[:6]
    if len(result) < 2:
        # Just take first 2 items from section
        result = [iid for iid in section_items.get(section_id, [])[:2] if iid in items_by_id]
    
    return result

# ============================================================
# 4. GENERATE PURE DEP FIX SHRINK PLANS
# ============================================================
print(f"\n  Generating shrink plans for {len(pure_dep_fix)} pure dep-fix nodes...")

shrink_plans = []
for r in pure_dep_fix:
    iid = r["item_id"]
    item = items_by_id[iid]
    name = item.get("name", "")
    sec_id = item_section[iid]
    old_pre = item.get("direct_pre", [])
    old_cnt = len(old_pre)
    
    new_pre = find_prereqs_by_name(name, sec_id)
    
    # Validate: no self-ref, no section ref, no empty
    new_pre = [p for p in new_pre if p != iid and p.count(".") >= 2]
    if len(new_pre) < 2:
        # Fallback: use section core
        new_pre = [cid for cid in section_core.get(sec_id, [])[:3] if cid != iid and cid.count(".") >= 2]
    
    shrink_plans.append({
        "item_id": iid,
        "name": name,
        "section": sec_id,
        "old_direct_pre_count": old_cnt,
        "old_direct_pre": old_pre,
        "new_direct_pre": new_pre,
        "new_direct_pre_count": len(new_pre),
        "shrink_reason": f"Section-wide pre assignment reduced to {len(new_pre)} core prerequisites based on topic keywords"
    })

print(f"  Generated {len(shrink_plans)} pure shrink plans")
# Validate
valid = sum(1 for sp in shrink_plans if 2 <= len(sp["new_direct_pre"]) <= 6)
print(f"  Valid (2-6 pre): {valid}/{len(shrink_plans)}")

# ============================================================
# 5. GENERATE TEMPLATE MERGE DECISIONS (32 nodes)
# ============================================================
print(f"\n  Generating merge/collapse decisions for {len(tpl_rids)} template nodes...")

# Group template nodes by parent topic
PARENT_PATTERNS = {
    "凸包维护 DP": r".*凸包维护 DP.*",
    "分治转移 DP": r".*分治转移 DP.*",
    "线段树维护 DP": r".*线段树维护 DP.*",
    "堆维护 DP": r".*堆维护 DP.*",
    "队列维护 DP": r".*队列维护 DP.*",
    "前缀最值 DP": r".*前缀最值 DP.*",
    "后缀最值 DP": r".*后缀最值 DP.*",
    "DP 与最短路融合模型": r".*DP.*最短路.*",
    "DP 与网络流融合模型": r".*DP.*网络流.*",
    "DP 与字符串自动机融合模型": r".*DP.*字符串.*",
    "DP 与生成函数融合模型": r".*DP.*生成函数.*",
    "DP 与数据结构查询融合模型": r".*DP.*数据结构.*",
    "DP 与连通性状态融合模型": r".*DP.*连通性.*",
}

parent_groups = defaultdict(list)
for r in tpl_rids:
    iid = r["item_id"]
    item = items_by_id[iid]
    name = item.get("name", "")
    matched = False
    for parent, pat in PARENT_PATTERNS.items():
        if re.match(pat, name):
            parent_groups[parent].append((iid, name))
            matched = True
            break
    if not matched:
        parent_groups[name].append((iid, name))

print(f"  Parent groups: {len(parent_groups)}")
for parent, items in sorted(parent_groups.items()):
    print(f"    {parent}: {len(items)} items")

# For each group: keep first as "keep_rename", rest as "merge_into_parent"
merge_decisions = []
for parent, group_items in sorted(parent_groups.items()):
    # Sort by item_id for consistency
    group_items.sort(key=lambda x: x[0])
    
    # The first one becomes the "parent" - keep_rename
    keeper_iid, keeper_name = group_items[0]
    sec_id = item_section[keeper_iid]
    new_pre = find_prereqs_by_name(keeper_name, sec_id)
    
    # Generate suggested new name for the merged concept
    # Extract the parent topic from the name
    cn_name = keeper_name.split("(")[0].strip() if "(" in keeper_name else keeper_name
    suggested_name = cn_name
    
    for gi, (iid, name) in enumerate(group_items):
        if gi == 0:
            # Keeper
            merge_decisions.append({
                "item_id": iid,
                "name": name,
                "decision": "keep_with_dependency_shrink",
                "target_parent_item_id": iid,
                "target_parent_name": parent,
                "suggested_new_name": parent,
                "suggested_direct_pre": new_pre,
                "reason": f"Keep as merged parent for {len(group_items)} template sub-nodes with reduced direct_pre"
            })
        else:
            # Merged into keeper
            merge_decisions.append({
                "item_id": iid,
                "name": name,
                "decision": "merge_into_parent",
                "target_parent_item_id": keeper_iid,
                "target_parent_name": parent,
                "suggested_new_name": parent,
                "suggested_direct_pre": [],
                "reason": f"Merge into {parent} (over-split sub-node)"
            })

print(f"  Merge decisions: {len(merge_decisions)}")
keep_count = sum(1 for m in merge_decisions if m["decision"] in ("keep_with_dependency_shrink", "keep_rename"))
merge_count = sum(1 for m in merge_decisions if m["decision"] == "merge_into_parent")
print(f"  Keep: {keep_count}, Merge into parent: {merge_count}")

# Also add shrink plans for keep-template nodes (they have 234 pre too)
keeper_shrink = []
for md in merge_decisions:
    if md["decision"] == "keep_with_dependency_shrink":
        iid = md["item_id"]
        item = items_by_id[iid]
        old_pre = item.get("direct_pre", [])
        keeper_shrink.append({
            "item_id": iid,
            "name": md["name"],
            "section": item_section[iid],
            "old_direct_pre_count": len(old_pre),
            "old_direct_pre": old_pre,
            "new_direct_pre": md["suggested_direct_pre"],
            "new_direct_pre_count": len(md["suggested_direct_pre"]),
            "shrink_reason": f"Template keeper node: section-wide 234 pre reduced to {len(md['suggested_direct_pre'])} core prerequisites"
        })

# Combine all shrink plans
all_shrink = shrink_plans + keeper_shrink
print(f"  Added {len(keeper_shrink)} keeper shrink plans")
print(f"  Total shrink plans: {len(all_shrink)}")

# ============================================================
# 6. NEXT ACTION DECISION
# ============================================================
# Branch A: all template nodes kept (just shrink), no deletions → pure dependency fix
# Branch B: some template nodes need deletion or merging → merge + shrink
# Branch C: uncertain items exist

uncertain = sum(1 for m in merge_decisions if m["decision"] in ("manual_review",))
has_deletions = sum(1 for m in merge_decisions if m["decision"] == "delete_duplicate") > 0
has_merges = merge_count > 0

if uncertain > 0:
    branch = "C"
    branch_reason = f"存在 {uncertain} 个不确定节点需人工决定"
elif has_merges or has_deletions:
    branch = "B"
    branch_reason = f"存在 {merge_count} 个需合并节点" + (f", {sum(1 for m in merge_decisions if m['decision']=='delete_duplicate')} 个需删除" if has_deletions else "")
else:
    branch = "A"
    branch_reason = "32 个模板化节点全部保留，仅需缩减 direct_pre"

next_action = {
    "branch": branch,
    "branch_label": {
        "A": "纯依赖缩减 — 模板节点全部保留，只需执行 direct_pre shrink",
        "B": "合并+缩减 — 需要先执行节点合并，再执行 direct_pre shrink",
        "C": "不确定 — 存在需人工审核的节点"
    }[branch],
    "reason": branch_reason,
    "shrink_plan_count": len(all_shrink),
    "merge_decisions_count": len(merge_decisions),
    "keep_count": keep_count,
    "merge_into_parent_count": merge_count,
    "delete_count": sum(1 for m in merge_decisions if m["decision"] == "delete_duplicate"),
    "manual_review_count": uncertain,
}

print(f"\n  Branch: {branch} - {next_action['branch_label']}")

# ============================================================
# 7. OUTPUT
# ============================================================
print(f"\n  Writing 5 output files...")
ts = datetime.now(timezone.utc).isoformat()

# 1. Shrink plan
shrink_output = {
    "meta": {"generated_at": ts, "total_shrink_plans": len(all_shrink),
             "main_graph_modified": False},
    "plans": all_shrink
}
with open(OUT_SHRINK, "w", encoding="utf-8") as f:
    json.dump(shrink_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_SHRINK}")

# 2. Shrink patch preview
patch_entries = []
for sp in all_shrink:
    patch_entries.append({
        "item_id": sp["item_id"],
        "current_direct_pre_count": sp["old_direct_pre_count"],
        "new_direct_pre_count": sp["new_direct_pre_count"],
        "new_direct_pre": sp["new_direct_pre"],
    })
for md in merge_decisions:
    if md["decision"] in ("keep_with_dependency_shrink", "keep_rename") and md["suggested_direct_pre"]:
        patch_entries.append({
            "item_id": md["item_id"],
            "current_direct_pre_count": len(items_by_id[md["item_id"]].get("direct_pre", [])),
            "new_direct_pre_count": len(md["suggested_direct_pre"]),
            "new_direct_pre": md["suggested_direct_pre"],
        })

shrink_patch = {
    "meta": {"generated_at": ts, "total_patches": len(patch_entries), "main_graph_modified": False},
    "patches": patch_entries
}
with open(OUT_SHRINK_PATCH, "w", encoding="utf-8") as f:
    json.dump(shrink_patch, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_SHRINK_PATCH}")

# 3. Merge resolution plan
merge_output = {
    "meta": {"generated_at": ts, "total_template_nodes": len(tpl_rids),
             "parent_groups": len(parent_groups), "decisions": len(merge_decisions),
             "main_graph_modified": False},
    "decisions": merge_decisions
}
with open(OUT_MERGE, "w", encoding="utf-8") as f:
    json.dump(merge_output, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_MERGE}")

# 4. Next action decision
with open(OUT_DECISION, "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "main_graph_modified": False},
               "next_action": next_action}, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_DECISION}")

# 5. Report
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch1 full500 依赖缩减与合并折叠方案报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")

    f.write("## 1. 依赖缩减方案\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 需要缩减 direct_pre 的节点总数 | {len(all_shrink)} |\n")
    f.write(f"| 缩减后 2-6 条的节点 | {valid + len(keeper_shrink)} |\n")
    f.write(f"| 各 section 分布 | — |\n\n")

    sec_shrink = defaultdict(int)
    for sp in all_shrink:
        sec_shrink[sp["section"]] += 1
    f.write("| Section | 需缩减节点数 |\n|---------|------------|\n")
    for sec_id in sorted(sec_shrink.keys()):
        f.write(f"| {sec_id} | {sec_shrink[sec_id]} |\n")

    f.write(f"\n### 缩减示例（前 10 个）\n\n")
    f.write("| item_id | name | old_pre | new_pre |\n|---------|------|---------|--------|\n")
    for sp in all_shrink[:10]:
        old_cnt = sp["old_direct_pre_count"]
        new_cnt = sp["new_direct_pre_count"]
        name_short = sp["name"][:40]
        new_pre_str = ", ".join(sp["new_direct_pre"])
        f.write(f"| {sp['item_id']} | {name_short}... | {old_cnt} | {new_pre_str} ({new_cnt}) |\n")

    f.write("\n## 2. 模板节点合并折叠决策\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 模板化节点总数 | {len(tpl_rids)} |\n")
    f.write(f"| 父主题组数 | {len(parent_groups)} |\n")
    f.write(f"| keep_with_dependency_shrink | {keep_count} |\n")
    f.write(f"| merge_into_parent | {merge_count} |\n")
    f.write(f"| 预计合并后剩余节点 | {keep_count} |\n\n")

    f.write("### 各父主题合并详情\n\n")
    f.write("| 父主题 | 原始子节点数 | 处理方式 | 保留 item_id |\n|--------|------------|---------|-------------|\n")
    for parent, group_items in sorted(parent_groups.items()):
        keeper = next(m["item_id"] for m in merge_decisions if m["target_parent_name"] == parent and m["decision"] == "keep_with_dependency_shrink")
        f.write(f"| {parent} | {len(group_items)} | 合并为1个 | {keeper} |\n")

    f.write(f"\n## 3. 下一步分支决策\n\n")
    f.write(f"**分支 {branch}** — {next_action['branch_label']}\n\n")
    f.write(f"理由: {branch_reason}\n\n")

    if branch == "B":
        f.write(f"### 执行顺序\n\n")
        f.write(f"1. 先执行 {merge_count} 个节点的合并（merge_into_parent）\n")
        f.write(f"2. 再对 {len(all_shrink)} 个保留节点执行 direct_pre 缩减\n")
        f.write(f"3. 合并后正式节点数减少 {merge_count} → 保留 {keep_count} 个\n")
    elif branch == "A":
        f.write(f"### 执行顺序\n\n")
        f.write(f"1. 对 {len(all_shrink)} 个节点执行 direct_pre 缩减\n")
        f.write(f"2. 无需节点合并\n")
    else:
        f.write(f"### 需要人工决策\n\n")
        f.write(f"1. 先处理 {uncertain} 个不确定节点\n")
        f.write(f"2. 确认后按分支 A 或 B 执行\n")

    f.write(f"\n## 4. 主图谱状态\n\n")
    f.write(f"**否** — 未修改主图谱\n\n")
    f.write(f"---\n*本报告自动生成*\n")

print(f"    [OK] {OUT_REPORT}")

print(f"\n{'=' * 60}")
print(f"  Plan Complete")
print(f"{'=' * 60}")
print(f"  Shrink plans: {len(all_shrink)}")
print(f"  Merge decisions: {len(merge_decisions)}")
print(f"  Branch: {branch}")
print(f"  No graph modifications.")
