#!/usr/bin/env python3
"""Stage5-HardKnowledge Batch1 full500 Candidate Plan & Dynamic Precheck
Expands from 200 to 500, preserves original 200, adds 300 more from ready_core.
Does NOT modify main graph. Does NOT merge."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
RC_PATH = "data/stage5_hard_knowledge_ready_core_candidates.json"
B1_PATH = "data/stage5_hard_knowledge_batch1_candidate_plan.json"

OUT_PLAN = "data/stage5_hard_knowledge_batch1_full500_candidate_plan.json"
OUT_PRECHECK = "data/stage5_hard_knowledge_batch1_full500_dynamic_precheck.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch1_full500_precheck_report.md"

print("=" * 60)
print("Stage5-HardKnowledge Batch1 full500 Plan & Dynamic Precheck")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

with open(RC_PATH, "r", encoding="utf-8") as f:
    rc_data = json.load(f)

with open(B1_PATH, "r", encoding="utf-8") as f:
    b1_data = json.load(f)

rc_candidates = rc_data["candidates"]
b1_candidates = b1_data["candidates"]

# Build graph indices
items_by_id = {}
items_by_name = {}
items_by_en = {}
items_by_alias = {}
name_lower_set = set()
en_lower_set = set()
alias_lower_set = set()
sections = {}
sec_counts = defaultdict(int)

for cat in graph.get("categories", []):
    for sec in cat.get("sections", []):
        sid = sec["id"]
        sections[sid] = sec.get("name", "")
        for item in sec.get("items", []):
            iid = item["id"]
            items_by_id[iid] = item
            n = item.get("name", "").strip()
            en = item.get("en_name", "").strip()
            if n:
                items_by_name[n.lower().replace(" ", "")] = item
                name_lower_set.add(n.lower().replace(" ", ""))
            if en:
                items_by_en[en.lower().replace(" ", "")] = item
                en_lower_set.add(en.lower().replace(" ", ""))
            for a in item.get("aliases", []):
                alias_lower_set.add(a.lower().strip().replace(" ", ""))
                items_by_alias[a.lower().strip().replace(" ", "")] = item
            for ga in item.get("global_aliases", []):
                alias_lower_set.add(ga.lower().strip().replace(" ", ""))
                items_by_alias[ga.lower().strip().replace(" ", "")] = item
            sec_counts[sid] += 1

item_count = len(items_by_id)
print(f"  Graph: {item_count} items, {len(sections)} sections")
print(f"  Ready core: {len(rc_candidates)}")
print(f"  Original B1: {len(b1_candidates)}")

# ============================================================
# 2. UTILITY FUNCTIONS
# ============================================================
def tokenize(s):
    return set(re.sub(r'[^a-z0-9\u4e00-\u9fff]', ' ', s.lower()).split())

def jaccard(a, b):
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb: return 0
    return len(ta & tb) / len(ta | tb)

def sn(sid):
    return sections.get(sid, f"UNKNOWN_{sid}")

def find_item_by_name(name):
    nl = name.lower().replace(" ", "")
    if nl in items_by_name:
        return items_by_name[nl]
    if nl in items_by_en:
        return items_by_en[nl]
    if nl in items_by_alias:
        return items_by_alias[nl]
    return None

def extract_cn_name(full_name):
    m = re.match(r'^(.+?)\s*\(', full_name)
    if m:
        return m.group(1).strip()
    return full_name.strip()

def extract_en_name(full_name):
    m = re.search(r'\((.+?)\)', full_name)
    if m:
        return m.group(1).strip()
    return ""

SECTION_MAP = {
    "搜索进阶": "2.7", "构造题硬知识": "2.20", "贪心模型": "2.6",
    "交互题硬知识": "2.20", "图论建模": "2.9", "DP优化": "2.8",
    "DP融合模型": "2.8", "图论衔接": "2.9",
    "数据结构嵌套": "3.13", "并查集扩展": "3.13", "根号算法": "2.4",
    "单调结构": "3.13", "字符串数据结构": "2.10", "持久化结构": "3.13",
    "数论进阶": "4.1", "线性代数进阶": "2.17", "组合计数进阶": "4.3",
    "多项式与生成函数": "4.3", "博弈论": "4.5", "概率期望": "4.6",
    "计算几何进阶": "4.7", "数论深水区": "4.1",
}

SUBCAT_PREREQS = {
    "搜索进阶": ["搜索", "DFS", "BFS"],
    "构造题硬知识": ["构造"],
    "贪心模型": ["贪心"],
    "交互题硬知识": ["交互"],
    "图论建模": ["图论"],
    "DP优化": ["DP", "动态规划"],
    "DP融合模型": ["DP", "动态规划"],
    "图论衔接": ["图论"],
    "数据结构嵌套": ["线段树", "树状数组"],
    "并查集扩展": ["并查集"],
    "根号算法": ["分块"],
    "单调结构": ["单调栈", "单调队列"],
    "字符串数据结构": ["Trie", "字符串"],
    "持久化结构": ["可持久化"],
    "数论进阶": ["数论"],
    "线性代数进阶": ["矩阵", "线性代数"],
    "组合计数进阶": ["组合", "计数"],
    "多项式与生成函数": ["FFT", "多项式"],
    "博弈论": ["博弈论", "SG函数"],
    "概率期望": ["概率", "期望"],
    "计算几何进阶": ["计算几何"],
    "数论深水区": ["数论"],
}

# ============================================================
# 3. SELECT FULL500
# ============================================================
print(f"\n  Selecting full500 candidates...")

TARGET_TOTAL = 500
TARGET_ALGO = 210
TARGET_DS = 120
TARGET_MATH = 170

cat_targets = {"算法": TARGET_ALGO, "数据结构": TARGET_DS, "数学": TARGET_MATH}

# Step 1: Preserve original B1 200
b1_ids = set(c["candidate_id"] for c in b1_candidates)
b1_names = set(c["name"].lower().replace(" ", "") for c in b1_candidates)

selected = list(b1_candidates)
selected_ids = set(b1_ids)
selected_names = set(b1_names)

b1_cat = defaultdict(int)
for c in b1_candidates:
    b1_cat[c["category"]] += 1
print(f"  Original B1 preserved: {len(selected)}")
for cat, cnt in b1_cat.items():
    print(f"    {cat}: {cnt}")

# Step 2: Calculate how many more needed per category
additional_needed = {}
for cat, target in cat_targets.items():
    already = b1_cat.get(cat, 0)
    additional_needed[cat] = target - already
print(f"\n  Additional needed:")
for cat, need in additional_needed.items():
    print(f"    {cat}: {need}")

# Step 3: Select additional from remaining ready_core
remaining_rc = [c for c in rc_candidates if c["candidate_id"] not in selected_ids]

for cat, need in additional_needed.items():
    if need <= 0:
        continue
    cat_remaining = [c for c in remaining_rc if c["category"] == cat]
    # Sort by quality desc, difficulty asc
    cat_remaining.sort(key=lambda x: (-x["quality_score"], x.get("difficulty", 5)))

    # Spread across subcategories
    subcat_groups = defaultdict(list)
    for c in cat_remaining:
        subcat_groups[c["subcategory"]].append(c)

    subcat_list = sorted(subcat_groups.keys())
    n_subcats = len(subcat_groups)
    base_quota = max(1, need // max(n_subcats, 1))

    added = 0
    for sc in subcat_list:
        if added >= need:
            break
        quota = min(base_quota + 1, need - added)
        sc_cands = subcat_groups[sc]
        for c in sc_cands[:quota]:
            nl = c["name"].lower().replace(" ", "")
            if nl not in selected_names:
                selected.append(c)
                selected_ids.add(c["candidate_id"])
                selected_names.add(nl)
                added += 1
                if added >= need:
                    break

    # If still under, fill from remaining
    if added < need:
        deficit = need - added
        still_remaining = [c for c in cat_remaining if c["candidate_id"] not in selected_ids]
        still_remaining.sort(key=lambda x: (-x["quality_score"], x.get("difficulty", 5)))
        for c in still_remaining[:deficit]:
            nl = c["name"].lower().replace(" ", "")
            if nl not in selected_names:
                selected.append(c)
                selected_ids.add(c["candidate_id"])
                selected_names.add(nl)

# If over 500, trim
if len(selected) > TARGET_TOTAL:
    # Keep B1, trim from additional
    b1_set = set(b1_ids)
    additional = [c for c in selected if c["candidate_id"] not in b1_set]
    additional = additional[:TARGET_TOTAL - len(b1_candidates)]
    selected = list(b1_candidates) + additional

print(f"\n  Final selection: {len(selected)}")

sel_cat = defaultdict(int)
sel_subcat = defaultdict(int)
b1_preserved = 0
new_added = 0
for c in selected:
    sel_cat[c["category"]] += 1
    sel_subcat[c["subcategory"]] += 1
    if c["candidate_id"] in b1_ids:
        b1_preserved += 1
    else:
        new_added += 1

for cat, cnt in sel_cat.items():
    print(f"    {cat}: {cnt}")
print(f"    B1 preserved: {b1_preserved}")
print(f"    New added: {new_added}")

# ============================================================
# 4. DYNAMIC PRECHECK
# ============================================================
print(f"\n  Running dynamic precheck on {len(selected)} candidates...")

precheck_results = []
excluded_dup = []
excluded_already_merged = []
section_ref_deps = []
manual_review = []
needs_cleanup = False
needs_new_section = False
dep_cycle = False
dup_count = 0
high_sim_count = 0
alias_conflict_count = 0
intra_high_sim = 0
subcat_concentration = {}

# Check subcategory concentration
max_subcat_pct = 0
for sc, cnt in sel_subcat.items():
    pct = cnt / len(selected) * 100
    subcat_concentration[sc] = {"count": cnt, "pct": round(pct, 1)}
    if pct > max_subcat_pct:
        max_subcat_pct = pct

# Any subcategory > 20% is concerning
if max_subcat_pct > 20:
    needs_cleanup = True
    print(f"  WARNING: Subcategory concentration > 20%: {max_subcat_pct:.1f}%")

for c in selected:
    name = c["name"]
    cn_name = extract_cn_name(name)
    en_name = extract_en_name(name)
    cnl = cn_name.lower().replace(" ", "")

    checks = {"candidate_id": c["candidate_id"], "name": name,
              "category": c["category"], "subcategory": c["subcategory"],
              "from_original_b1": c["candidate_id"] in b1_ids,
              "issues": [], "warnings": []}

    # 1. Exact name dup
    if cnl in name_lower_set:
        checks["issues"].append(f"exact_name_dup: {cn_name}")
        excluded_dup.append(name)
        dup_count += 1

    # 2. en_name dup
    enl = en_name.lower().replace(" ", "") if en_name else ""
    if enl and enl in en_lower_set:
        checks["issues"].append(f"exact_en_dup: {en_name}")
        excluded_dup.append(name)
        dup_count += 1

    # 3. Alias conflict
    if cnl in alias_lower_set:
        checks["warnings"].append(f"alias_conflict: {cn_name}")
        alias_conflict_count += 1

    # 4. Intra-pool dup
    for c2 in selected:
        if c2["candidate_id"] == c["candidate_id"]:
            continue
        sim = jaccard(name, c2["name"])
        if sim >= 0.8:
            checks["issues"].append(f"intra_pool_high_sim: {c2['name']} ({sim:.2f})")
            intra_high_sim += 1

    # 5. High similarity with existing graph
    best_sim = 0
    best_match = ""
    for iid, item in items_by_id.items():
        sim = jaccard(cn_name, item.get("name", ""))
        if sim > best_sim:
            best_sim = sim
            best_match = item.get("name", "")
    if best_sim >= 0.85:
        checks["issues"].append(f"high_similarity_existing: {best_match} ({best_sim:.2f})")
        excluded_dup.append(name)
        dup_count += 1
    elif best_sim >= 0.65:
        checks["warnings"].append(f"medium_similarity_existing: {best_match} ({best_sim:.2f})")

    # 6. Direct_pre mapping
    subcat = c["subcategory"]
    prereq_names = SUBCAT_PREREQS.get(subcat, [])
    mapped_pre = []
    unmapped_pre = []
    for pn in prereq_names:
        found = find_item_by_name(pn)
        if found:
            mapped_pre.append({"name": pn, "item_id": found["id"]})
        else:
            unmapped_pre.append(pn)

    checks["mapped_direct_pre"] = mapped_pre
    checks["unmapped_direct_pre"] = unmapped_pre

    if unmapped_pre:
        checks["warnings"].append(f"unmapped_prereqs: {unmapped_pre}")

    # 7. Section ref in direct_pre
    for mp in mapped_pre:
        iid = mp["item_id"]
        if "." not in iid or iid.count(".") < 1:
            checks["issues"].append(f"section_ref_in_pre: {iid}")
            section_ref_deps.append(iid)

    # 8-9. Dangling refs and cycles: not applicable (not merged yet)

    # 10. New section check
    target_sec = SECTION_MAP.get(subcat, "")
    if target_sec and target_sec not in sections:
        checks["warnings"].append(f"new_section_needed: {target_sec}")
        needs_new_section = True

    # 11. Template re-check
    if c.get("is_template", False):
        checks["issues"].append("is_template_should_not_be_in_ready_core")
        needs_cleanup = True

    # 12. Should merge_or_collapse?
    if c.get("granularity_risk") == "high":
        checks["warnings"].append("granularity_risk_high_maybe_merge")

    if checks["issues"]:
        manual_review.append({"candidate_id": c["candidate_id"], "name": name,
                             "issues": checks["issues"],
                             "from_original_b1": c["candidate_id"] in b1_ids})
        if any("dup" in i or "high_sim" in i for i in checks["issues"]):
            needs_cleanup = True

    precheck_results.append(checks)

clean_count = sum(1 for p in precheck_results if not p["issues"])
issue_count = len(precheck_results) - clean_count

if dup_count > 0 or issue_count > 10:
    recommendation = "needs_cleanup_before_merge"
elif issue_count > 0:
    recommendation = "needs_cleanup_before_merge"
else:
    recommendation = "ready_for_1号线程_merge_stage5_hard_batch1_full500"

recommended_merge = len(selected) - dup_count

print(f"\n{'=' * 60}")
print(f"  PRECHECK RESULTS")
print(f"{'=' * 60}")
print(f"  Selected: {len(selected)}")
print(f"  Clean: {clean_count}")
print(f"  With issues: {issue_count}")
print(f"  Duplicates: {dup_count}")
print(f"  High similarity: {high_sim_count}")
print(f"  Intra-pool high sim: {intra_high_sim}")
print(f"  Alias conflicts: {alias_conflict_count}")
print(f"  Manual review: {len(manual_review)}")
print(f"  Recommended merge: {recommended_merge}")
print(f"  Recommendation: {recommendation}")
print(f"  Max subcat concentration: {max_subcat_pct:.1f}%")

# ============================================================
# 5. OUTPUT FILES
# ============================================================
print(f"\n  Writing outputs...")
ts = datetime.now(timezone.utc).isoformat()

# Build plan candidates
plan_candidates = []
for c in selected:
    subcat = c["subcategory"]
    target_sec = SECTION_MAP.get(subcat, "")
    prereq_names = SUBCAT_PREREQS.get(subcat, [])
    mapped = []
    for pn in prereq_names:
        found = find_item_by_name(pn)
        if found:
            mapped.append(found["id"])

    plan_candidates.append({
        "candidate_id": c["candidate_id"],
        "name": c["name"],
        "cn_name": extract_cn_name(c["name"]),
        "en_name": extract_en_name(c["name"]),
        "category": c["category"],
        "subcategory": subcat,
        "target_section": target_sec,
        "section_name": sn(target_sec) if target_sec else "",
        "difficulty": c.get("difficulty", 7),
        "quality_score": c.get("quality_score", 4),
        "duplicate_risk": c.get("duplicate_risk", "low"),
        "granularity_risk": c.get("granularity_risk", "low"),
        "template_like_risk": c.get("template_like_risk", "low"),
        "suggested_direct_pre": mapped,
        "suggested_direct_pre_names": prereq_names,
        "from_original_b1": c["candidate_id"] in b1_ids,
    })

plan = {
    "meta": {
        "generated_at": ts,
        "baseline_item_count": item_count,
        "selected_count": len(selected),
        "original_b1_preserved": b1_preserved,
        "newly_added": new_added,
        "category_distribution": dict(sel_cat),
        "subcategory_distribution": dict(sel_subcat),
        "main_graph_modified": False,
        "merge_executed": False,
    },
    "candidates": plan_candidates
}

with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PLAN}")

# Precheck
precheck = {
    "baseline_item_count": item_count,
    "selected_candidate_count": len(selected),
    "recommendation": recommendation,
    "recommended_merge_count": recommended_merge,
    "dependency_cleanup_required": needs_cleanup,
    "needs_new_section": needs_new_section,
    "candidate_dependency_cycle": dep_cycle,
    "excluded_duplicate_or_near_duplicate": list(set(excluded_dup)),
    "excluded_already_merged_candidates": excluded_already_merged,
    "section_ref_dependencies": list(set(section_ref_deps)),
    "manual_review_candidates": manual_review,
    "summary": {
        "clean_candidates": clean_count,
        "candidates_with_issues": issue_count,
        "duplicate_count": dup_count,
        "high_similarity_count": high_sim_count,
        "intra_pool_high_sim": intra_high_sim,
        "alias_conflict_count": alias_conflict_count,
        "max_subcategory_concentration_pct": round(max_subcat_pct, 1),
    },
    "subcategory_concentration": subcat_concentration,
    "precheck_details": precheck_results,
}

with open(OUT_PRECHECK, "w", encoding="utf-8") as f:
    json.dump(precheck, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PRECHECK}")

# Report
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch1 full500 候选计划与动态预审报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")

    f.write("## 1. 当前基线\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 基线节点数 | **{item_count}** |\n")
    f.write(f"| Section 数 | {len(sections)} |\n")
    f.write(f"| Ready core 候选池 | 842 |\n\n")

    f.write("## 2. full500 选择数量\n\n")
    f.write(f"**{len(selected)}** (从 842 个 ready_core 中选择)\n\n")

    f.write("## 3. 原 200 个是否全部保留\n\n")
    f.write(f"**是** — 全部 {b1_preserved} 个原 Batch1 候选已保留。\n\n")

    f.write("## 4. 新增补充 300 个的来源\n\n")
    f.write(f"从剩余 {len(rc_candidates) - len(b1_candidates)} 个 ready_core 候选中补充 {new_added} 个。\n\n")

    f.write("## 5. 算法/数据结构/数学分布\n\n")
    f.write("| 类别 | 数量 | 目标 |\n|------|------|------|\n")
    for cat in ["算法", "数据结构", "数学"]:
        cnt = sel_cat.get(cat, 0)
        tgt = cat_targets.get(cat, 0)
        f.write(f"| {cat} | {cnt} | {tgt} |\n")

    f.write(f"\n## 6. 子类分布\n\n")
    f.write("| 子类 | 类别 | 数量 | 占比 |\n|------|------|------|------|\n")
    for sc, cnt in sorted(sel_subcat.items(), key=lambda x: -x[1]):
        cat = next((c["category"] for c in selected if c["subcategory"] == sc), "")
        pct = cnt / len(selected) * 100
        f.write(f"| {sc} | {cat} | {cnt} | {pct:.1f}% |\n")

    f.write(f"\n## 7. 查重结果\n\n")
    f.write(f"| 检查项 | 结果 |\n|--------|------|\n")
    f.write(f"| 精确名称重复 | {dup_count} |\n")
    f.write(f"| 高相似度 (>=0.85) | {high_sim_count} |\n")
    f.write(f"| 候选间高相似 (>=0.8) | {intra_high_sim} |\n")
    f.write(f"| 别名冲突 | {alias_conflict_count} |\n")
    f.write(f"| 排除的重复候选 | {len(set(excluded_dup))} |\n\n")

    f.write(f"## 8. 依赖映射结果\n\n")
    mapped_count = sum(1 for p in precheck_results if p["mapped_direct_pre"])
    unmapped_count = sum(1 for p in precheck_results if p["unmapped_direct_pre"])
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 有映射前置的候选 | {mapped_count} |\n")
    f.write(f"| 有未映射前置的候选 | {unmapped_count} |\n")
    f.write(f"| Section引用依赖 | {len(set(section_ref_deps))} |\n\n")

    f.write(f"## 9. 是否需要依赖清理\n\n")
    f.write(f"**{'是' if needs_cleanup else '否'}**\n\n")

    f.write(f"## 10. 是否需要新 section\n\n")
    f.write(f"**{'是' if needs_new_section else '否'}**\n\n")

    f.write(f"## 11. 是否建议合并\n\n**否** — 本任务只做计划和预审。\n\n")

    f.write(f"## 12. 合并后预计 item_count\n\n")
    f.write(f"**{item_count} + {recommended_merge} = {item_count + recommended_merge}**\n\n")

    f.write(f"## 13. 是否修改主图谱\n\n**否**\n\n")

    f.write(f"## 14. 预审结论\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| recommendation | **{recommendation}** |\n")
    f.write(f"| recommended_merge_count | {recommended_merge} |\n")
    f.write(f"| clean_candidates | {clean_count} |\n")
    f.write(f"| candidates_with_issues | {issue_count} |\n")
    f.write(f"| manual_review_needed | {len(manual_review)} |\n")
    f.write(f"| max_subcat_concentration | {max_subcat_pct:.1f}% |\n\n")

    f.write(f"## 15. 下一步建议\n\n")
    if recommendation.startswith("ready"):
        f.write(f"1. 当前 full500 可交由 1号线程 执行合并\n")
        f.write(f"2. 建议合并数量: {recommended_merge}\n")
        f.write(f"3. 合并后基线将变为 {item_count} + {recommended_merge} = **{item_count + recommended_merge}**\n")
        f.write(f"4. 之后可从剩余 ready_core 中选择 Batch2\n")
    else:
        f.write(f"1. 需要先清理以下问题:\n")
        f.write(f"   - 排除 {len(set(excluded_dup))} 个重复候选\n")
        f.write(f"   - 审核 {len(manual_review)} 个有问题的候选\n")
        f.write(f"2. 清理后重新运行预审\n")
        f.write(f"3. 通过后再交由 1号线程 执行合并\n")
    f.write(f"\n---\n*本报告自动生成*\n")

print(f"    [OK] {OUT_REPORT}")

print(f"\n{'=' * 60}")
print(f"  full500 Plan Complete")
print(f"{'=' * 60}")
print(f"  Selected: {len(selected)}")
print(f"  B1 preserved: {b1_preserved}")
print(f"  New added: {new_added}")
print(f"  Recommendation: {recommendation}")
print(f"  Recommended merge: {recommended_merge}")
print(f"  Projected total: {item_count + recommended_merge}")
print(f"  No graph modifications.")
