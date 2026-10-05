#!/usr/bin/env python3
"""Stage5-HardKnowledge Batch1 Candidate Plan & Dynamic Precheck
Selects 200 from ready_core, runs dedup/dependency checks.
Does NOT modify main graph. Does NOT merge."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
RC_PATH = "data/stage5_hard_knowledge_ready_core_candidates.json"
CAND_PATH = "data/stage5_hard_knowledge_candidates.json"

OUT_PLAN = "data/stage5_hard_knowledge_batch1_candidate_plan.json"
OUT_PRECHECK = "data/stage5_hard_knowledge_batch1_dynamic_precheck.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch1_precheck_report.md"

print("=" * 60)
print("Stage5-HardKnowledge Batch1 Plan & Dynamic Precheck")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

with open(RC_PATH, "r", encoding="utf-8") as f:
    rc_data = json.load(f)

with open(CAND_PATH, "r", encoding="utf-8") as f:
    all_candidates = json.load(f)

rc_candidates = rc_data["candidates"]
print(f"  Graph: loading...")

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
print(f"  Ready core candidates: {len(rc_candidates)}")

# Build all-candidate name index for intra-pool dedup
all_cand_names = {}
for c in all_candidates:
    all_cand_names[c["name"].lower().replace(" ", "")] = c["name"]

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
    enl = name.lower().replace(" ", "")
    if enl in items_by_en:
        return items_by_en[enl]
    # Try alias
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

# Map section categories
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

# Map subcategory to likely direct_pre names
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
# 3. SELECT BATCH1 - 200 candidates with balanced distribution
# ============================================================
print(f"\n  Selecting Batch1 candidates...")

TARGET_TOTAL = 200
TARGET_ALGO = 85
TARGET_DS = 50
TARGET_MATH = 65

# Sort by quality_score desc, then subcategory for diversity
cat_targets = {"算法": TARGET_ALGO, "数据结构": TARGET_DS, "数学": TARGET_MATH}

selected = []
selected_names = set()

for cat, target in cat_targets.items():
    cat_cands = [c for c in rc_candidates if c["category"] == cat]
    # Sort: quality desc, then spread across subcategories
    # Group by subcategory and take evenly
    subcat_groups = defaultdict(list)
    for c in cat_cands:
        subcat_groups[c["subcategory"]].append(c)

    # Calculate per-subcategory quota
    n_subcats = len(subcat_groups)
    base_quota = target // n_subcats
    remainder = target % n_subcats

    cat_selected = []
    subcat_list = sorted(subcat_groups.keys())

    for i, sc in enumerate(subcat_list):
        quota = base_quota + (1 if i < remainder else 0)
        sc_cands = subcat_groups[sc]
        # Sort by quality_score desc, difficulty asc
        sc_cands.sort(key=lambda x: (-x["quality_score"], x.get("difficulty", 5)))
        for c in sc_cands[:quota]:
            nl = c["name"].lower().replace(" ", "")
            if nl not in selected_names:
                selected_names.add(nl)
                cat_selected.append(c)

    # If under target, add more from largest subcategories
    if len(cat_selected) < target:
        deficit = target - len(cat_selected)
        remaining = [c for c in cat_cands if c["name"].lower().replace(" ", "") not in selected_names]
        remaining.sort(key=lambda x: (-x["quality_score"], x.get("difficulty", 5)))
        for c in remaining[:deficit]:
            nl = c["name"].lower().replace(" ", "")
            if nl not in selected_names:
                selected_names.add(nl)
                cat_selected.append(c)

    # If over target, trim
    if len(cat_selected) > target:
        cat_selected = cat_selected[:target]

    selected.extend(cat_selected)

print(f"  Selected: {len(selected)} candidates")
sel_cat = defaultdict(int)
sel_subcat = defaultdict(int)
for c in selected:
    sel_cat[c["category"]] += 1
    sel_subcat[c["subcategory"]] += 1
for cat, cnt in sel_cat.items():
    print(f"    {cat}: {cnt}")

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

for c in selected:
    name = c["name"]
    cn_name = extract_cn_name(name)
    en_name = extract_en_name(name)
    nl = name.lower().replace(" ", "")
    cnl = cn_name.lower().replace(" ", "")

    checks = {"candidate_id": c["candidate_id"], "name": name, "category": c["category"],
              "subcategory": c["subcategory"], "issues": [], "warnings": []}

    # 1. Exact name dup with existing graph
    if cnl in name_lower_set:
        checks["issues"].append(f"exact_name_dup: {cnl}")
        excluded_dup.append(name)
        dup_count += 1

    # 2. en_name dup
    enl = en_name.lower().replace(" ", "") if en_name else ""
    if enl and enl in en_lower_set:
        checks["issues"].append(f"exact_en_dup: {enl}")
        excluded_dup.append(name)
        dup_count += 1

    # 3. Alias conflict
    if cnl in alias_lower_set:
        checks["warnings"].append(f"alias_conflict: {cnl}")

    # 4. Intra-pool dup (between selected candidates)
    for c2 in selected:
        if c2["candidate_id"] == c["candidate_id"]:
            continue
        sim = jaccard(name, c2["name"])
        if sim >= 0.8:
            checks["issues"].append(f"intra_pool_high_sim: {c2['name']} ({sim:.2f})")
            high_sim_count += 1

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

    # 6. Direct_pre mapping check
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

    # 7. Check if direct_pre contains section id (should not)
    for mp in mapped_pre:
        iid = mp["item_id"]
        if "." not in iid or iid.count(".") < 1:
            checks["issues"].append(f"section_ref_in_pre: {iid}")
            section_ref_deps.append(iid)

    # 8. Dangling ref check - will the candidate create a dangling ref?
    # (Not applicable yet since we're not merging)

    # 9. Dependency cycle check (can't form cycles since candidates aren't in graph yet)

    # 10. New section check
    target_sec = SECTION_MAP.get(subcat, "")
    if target_sec and target_sec not in sections:
        checks["warnings"].append(f"new_section_needed: {target_sec}")
        needs_new_section = True

    # 11. Template re-check
    if c.get("is_template", False):
        checks["issues"].append("is_template_should_not_be_in_ready_core")
        needs_cleanup = True

    # 12. Should move to merge_or_collapse?
    if c.get("granularity_risk") == "high":
        checks["warnings"].append("granularity_risk_high_maybe_merge")

    if checks["issues"]:
        manual_review.append({"candidate_id": c["candidate_id"], "name": name,
                             "issues": checks["issues"]})
        if any("dup" in i or "high_sim" in i for i in checks["issues"]):
            needs_cleanup = True

    precheck_results.append(checks)

# Determine recommendation
clean_count = sum(1 for p in precheck_results if not p["issues"])
issue_count = len(precheck_results) - clean_count

if dup_count > 0 or issue_count > 10:
    recommendation = "needs_cleanup_before_merge"
elif issue_count > 0:
    recommendation = "needs_cleanup_before_merge"
else:
    recommendation = "ready_for_1号线程_merge_stage5_hard_batch1"

recommended_merge = len(selected) - dup_count

print(f"\n{'=' * 60}")
print(f"  PRECHECK RESULTS")
print(f"{'=' * 60}")
print(f"  Selected: {len(selected)}")
print(f"  Clean: {clean_count}")
print(f"  With issues: {issue_count}")
print(f"  Duplicates found: {dup_count}")
print(f"  High similarity: {high_sim_count}")
print(f"  Manual review needed: {len(manual_review)}")
print(f"  Recommended merge: {recommended_merge}")
print(f"  Recommendation: {recommendation}")

# ============================================================
# 5. OUTPUT FILES
# ============================================================
print(f"\n  Writing outputs...")
ts = datetime.now(timezone.utc).isoformat()

# Plan
plan = {
    "meta": {
        "generated_at": ts, "baseline_item_count": item_count,
        "selected_count": len(selected),
        "category_distribution": dict(sel_cat),
        "subcategory_distribution": dict(sel_subcat),
        "main_graph_modified": False, "merge_executed": False,
    },
    "candidates": []
}

for c in selected:
    subcat = c["subcategory"]
    target_sec = SECTION_MAP.get(subcat, "")
    prereq_names = SUBCAT_PREREQS.get(subcat, [])
    mapped = []
    for pn in prereq_names:
        found = find_item_by_name(pn)
        if found:
            mapped.append(found["id"])

    plan["candidates"].append({
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
    })

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
    "precheck_details": precheck_results,
    "summary": {
        "clean_candidates": clean_count,
        "candidates_with_issues": issue_count,
        "duplicate_count": dup_count,
        "high_similarity_count": high_sim_count,
    }
}

with open(OUT_PRECHECK, "w", encoding="utf-8") as f:
    json.dump(precheck, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PRECHECK}")

# Report
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch1 候选计划与动态预审报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")

    f.write("## 1. 当前基线\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 基线节点数 | **{item_count}** |\n")
    f.write(f"| Section 数 | {len(sections)} |\n")
    f.write(f"| Ready core 候选池 | 842 |\n\n")

    f.write("## 2. Batch1 选择数量\n\n**200** (从 842 个 ready_core 中选择)\n\n")

    f.write("## 3. 三大类分布\n\n")
    f.write("| 类别 | 数量 | 目标 |\n|------|------|------|\n")
    for cat in ["算法", "数据结构", "数学"]:
        cnt = sel_cat.get(cat, 0)
        tgt = cat_targets.get(cat, 0)
        f.write(f"| {cat} | {cnt} | {tgt} |\n")

    f.write(f"\n## 4. 子类分布\n\n")
    f.write("| 子类 | 类别 | 数量 |\n|------|------|------|\n")
    for sc, cnt in sorted(sel_subcat.items(), key=lambda x: -x[1]):
        cat = next((c["category"] for c in selected if c["subcategory"] == sc), "")
        f.write(f"| {sc} | {cat} | {cnt} |\n")

    f.write(f"\n## 5. 查重结果\n\n")
    f.write(f"| 检查项 | 结果 |\n|--------|------|\n")
    f.write(f"| 精确名称重复 | {dup_count} |\n")
    f.write(f"| 高相似度 (>=0.85) | {high_sim_count} |\n")
    f.write(f"| 候选间高相似 | {high_sim_count} |\n")
    f.write(f"| 别名冲突 | {sum(1 for p in precheck_results if any('alias' in w for w in p['warnings']))} |\n")
    f.write(f"| 排除的重复候选 | {len(set(excluded_dup))} |\n\n")

    f.write(f"## 6. 依赖映射结果\n\n")
    mapped_count = sum(1 for p in precheck_results if p["mapped_direct_pre"])
    unmapped_count = sum(1 for p in precheck_results if p["unmapped_direct_pre"])
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 有映射前置的候选 | {mapped_count} |\n")
    f.write(f"| 有未映射前置的候选 | {unmapped_count} |\n")
    f.write(f"| Section引用依赖 | {len(set(section_ref_deps))} |\n\n")

    f.write(f"## 7. 是否需要依赖清理\n\n")
    f.write(f"**{'是' if needs_cleanup else '否'}**\n\n")
    if needs_cleanup:
        f.write(f"- 重复候选需排除: {len(set(excluded_dup))}\n")
        f.write(f"- 需人工审核: {len(manual_review)}\n\n")

    f.write(f"## 8. 是否建议合并\n\n**否** — 本任务只做计划和预审。\n\n")
    f.write(f"## 9. 是否修改主图谱\n\n**否**\n\n")

    f.write(f"## 10. 预审结论\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| recommendation | **{recommendation}** |\n")
    f.write(f"| recommended_merge_count | {recommended_merge} |\n")
    f.write(f"| clean_candidates | {clean_count} |\n")
    f.write(f"| candidates_with_issues | {issue_count} |\n")
    f.write(f"| manual_review_needed | {len(manual_review)} |\n\n")

    f.write(f"## 11. 下一步建议\n\n")
    if recommendation.startswith("ready"):
        f.write(f"1. 当前 Batch1 可交由 1号线程 执行合并\n")
        f.write(f"2. 建议合并数量: {recommended_merge}\n")
        f.write(f"3. 合并后基线将变为 {item_count} + {recommended_merge} = {item_count + recommended_merge}\n")
    else:
        f.write(f"1. 需要先清理以下问题:\n")
        f.write(f"   - 排除 {len(set(excluded_dup))} 个重复候选\n")
        f.write(f"   - 审核 {len(manual_review)} 个有问题的候选\n")
        f.write(f"2. 清理后重新运行预审\n")
        f.write(f"3. 通过后再交由 1号线程 执行合并\n")
    f.write(f"\n---\n*本报告自动生成*\n")

print(f"    [OK] {OUT_REPORT}")

print(f"\n{'=' * 60}")
print(f"  Batch1 Plan Complete")
print(f"{'=' * 60}")
print(f"  Selected: {len(selected)}")
print(f"  Recommendation: {recommendation}")
print(f"  Recommended merge: {recommended_merge}")
print(f"  No graph modifications.")
