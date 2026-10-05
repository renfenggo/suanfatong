import json, re
from datetime import datetime, timezone
from collections import Counter, defaultdict

GRAPH = "merged_knowledge_graph_item_dependencies_refined.json"
CLEANED = "data/stage5_hard_knowledge_cleaned_candidates.json"
B1_MAP = "data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json"
B1_REMOVED = "data/stage5_hard_knowledge_batch1_full500_branch_b_removed_or_merged_items.json"
OUT_PLAN = "data/stage5_hard_knowledge_batch2_full600_candidate_plan.json"
OUT_PRECHECK = "data/stage5_hard_knowledge_batch2_full600_dynamic_precheck.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch2_full600_precheck_report.md"

ts = datetime.now(timezone.utc).isoformat()
print("=" * 60)
print("Stage5-HardKnowledge Batch2 full600 Candidate Plan & Precheck")
print("=" * 60)

with open(GRAPH, "r", encoding="utf-8") as f:
    graph = json.load(f)
with open(CLEANED, "r", encoding="utf-8") as f:
    cleaned = json.load(f)
with open(B1_MAP, "r", encoding="utf-8") as f:
    b1_map = json.load(f)
with open(B1_REMOVED, "r", encoding="utf-8") as f:
    b1_removed = json.load(f)

allc = cleaned["all_classified"]
b1_cids = set(m["candidate_id"] for m in b1_map["mappings"])
b1_removed_cids = set(r["item_id"] for r in b1_removed.get("removed", []))
b1_removed_names = set(r["name"].split("(")[0].strip() for r in b1_removed.get("removed", []))

items_by_id = {}
item_section = {}
all_item_names = set()
all_en_names = set()
for cat in graph["categories"]:
    for sec in cat["sections"]:
        for it in sec["items"]:
            items_by_id[it["id"]] = it
            item_section[it["id"]] = sec["id"]
            n = it["name"].lower().replace(" ", "").replace("(","").replace(")","")
            all_item_names.add(n)
            en = it.get("en_name", "").lower().strip()
            if en: all_en_names.add(en)

total = len(items_by_id)
sec_count = len(set(item_section.values()))
print(f"Graph: {total} items, {sec_count} sections")

ready = [c for c in allc if c["decision"] == "ready_core"]
reserve = [c for c in allc if c["decision"] == "reserve_useful"]

remaining_ready = [c for c in ready if c["candidate_id"] not in b1_cids]
print(f"Remaining ready_core: {len(remaining_ready)}")

rc_cat = Counter(c["category"] for c in remaining_ready)
print(f"  Categories: {dict(rc_cat)}")

# SUBJECT→SECTION mapping from Batch1 mapping patterns
section_by_subcat = {}
for m in b1_map["mappings"]:
    sc = m.get("subcategory", "")
    ts = m.get("target_section", "")
    if sc and ts and sc not in section_by_subcat:
        section_by_subcat[sc] = ts

print(f"\nSubcategory→Section from Batch1: {len(section_by_subcat)} mappings")

# Resolve missing sections - manual mapping
FALLBACK_SECTION = {
    "构造题硬知识": "2.20",
    "线性代数进阶": "2.17",
    "数据结构嵌套": "3.13",
    "贪心模型": "2.6",
    "数论进阶": "4.1",
    "并查集扩展": "3.5",
    "搜索进阶": "2.7",
    "交互题硬知识": "2.20",
    "组合计数进阶": "4.3",
    "多项式与生成函数": "4.3",
    "根号算法": "2.4",
    "单调结构": "1.4",
    "图论建模": "2.9",
    "DP优化": "2.8",
}
for sc, sid in FALLBACK_SECTION.items():
    if sc not in section_by_subcat:
        section_by_subcat[sc] = sid

# ==== SECTION CORE ITEMS ====
section_core = {}
for sid in set(item_section.values()):
    iids = [it["id"] for cat in graph["categories"] for sec in cat["sections"]
            if sec["id"] == sid for it in sec["items"]]
    sorted_iids = sorted(iids, key=lambda x: int(x.split(".")[-1]) if x.split(".")[-1].isdigit() else 0)
    section_core[sid] = sorted_iids[:4]

EXTRA_PREREQ = {
    "DP": ["2.8.1", "2.8.2"],
    "动态规划": ["2.8.1"],
    "最短路": ["2.13.2"],
    "Dijkstra": ["2.13.2"],
    "Floyd": ["2.13.4"],
    "Bellman": ["2.13.30"],
    "SPFA": ["2.13.6"],
    "网络流": ["2.11.1"],
    "最大流": ["2.11.2"],
    "最小割": ["2.9.20"],
    "费用流": ["2.9.24"],
    "二分图": ["2.9.15"],
    "匹配": ["2.9.17"],
    "连通性": ["2.9.1"],
    "强连通": ["2.9.4"],
    "双连通": ["2.9.5"],
    "拓扑排序": ["2.9.10"],
    "差分约束": ["2.9.23"],
    "最小生成树": ["2.13.1"],
    "Kruskal": ["2.13.7"],
    "Prim": ["2.13.8"],
    "线段树": ["3.7.2"],
    "树状数组": ["3.3.1"],
    "平衡树": ["3.8.2"],
    "Treap": ["3.8.3"],
    "Splay": ["3.8.4"],
    "可持久化": ["3.13.15"],
    "并查集": ["3.5.1"],
    "堆": ["1.5.1"],
    "优先队列": ["1.5.1"],
    "单调队列": ["1.4.4"],
    "单调栈": ["1.4.3"],
    "BFS": ["2.9.2"],
    "DFS": ["2.7.1"],
    "搜索": ["2.7.1"],
    "A*": ["2.7.22"],
    "IDA*": ["2.7.23"],
    "剪枝": ["2.7.18"],
    "启发式": ["2.7.20"],
    "模拟退火": ["2.7.25"],
    "爬山": ["2.7.24"],
    "遗传算法": ["2.7.26"],
    "深度优先": ["2.7.1"],
    "回溯": ["2.7.6"],
    "DLX": ["2.7.28"],
    "Meet": ["2.7.27"],
    "数位": ["2.8.3"],
    "区间": ["2.8.2"],
    "背包": ["2.8.1"],
    "树形": ["2.8.5"],
    "状态压缩": ["2.8.4"],
    "概率": ["4.6.1"],
    "期望": ["4.6.1"],
    "马尔可夫": ["4.6.4"],
    "贝叶斯": ["4.6.3"],
    "随机": ["4.6.2"],
    "蒙特卡洛": ["4.6.5"],
    "方差": ["4.6.7"],
    "博弈": ["4.5.1"],
    "Nim": ["4.5.2"],
    "SG": ["4.5.3"],
    "威佐夫": ["4.5.5"],
    "不平等": ["4.5.8"],
    "阶梯": ["4.5.7"],
    "数论": ["4.1.1"],
    "欧拉": ["4.1.5"],
    "质数": ["4.1.2"],
    "素数": ["4.1.2"],
    "筛": ["4.1.3"],
    "同余": ["4.1.7"],
    "裴蜀": ["4.1.12"],
    "逆元": ["4.1.9"],
    "莫比乌斯": ["4.1.17"],
    "原根": ["4.1.16"],
    "二次剩余": ["4.1.13"],
    "积性": ["4.1.15"],
    "狄利克雷": ["4.1.18"],
    "多项式": ["2.18.2"],
    "FFT": ["2.18.2"],
    "NTT": ["2.18.3"],
    "FWT": ["2.18.4"],
    "生成函数": ["4.3.14"],
    "组合": ["4.3.1"],
    "斯特林": ["4.3.6"],
    "错排": ["4.3.5"],
    "卡特兰": ["4.3.3"],
    "排列": ["4.3.1"],
    "线性": ["2.17.1"],
    "高斯": ["2.17.1"],
    "异或": ["2.17.3"],
    "矩阵": ["2.17.2"],
    "行列式": ["2.17.8"],
    "矩阵树": ["2.17.12"],
    "字符串": ["2.10.1"],
    "哈希": ["2.10.2"],
    "KMP": ["2.10.3"],
    "自动机": ["2.10.5"],
    "后缀": ["2.10.7"],
    "Manacher": ["2.10.10"],
    "Z函数": ["2.10.9"],
    "字典树": ["2.10.4"],
    "Trie": ["2.10.4"],
    "Lyndon": ["2.10.12"],
    "回文": ["2.10.11"],
    "AC自动机": ["2.10.5"],
    "分块": ["2.4.1"],
    "莫队": ["2.4.2"],
    "根号": ["2.4.1"],
    "整除": ["2.4.3"],
    "数论分块": ["2.4.7"],
    "贪心": ["2.6.1"],
    "区间调度": ["2.6.2"],
    "Huffman": ["2.6.12"],
    "反悔": ["2.6.11"],
    "构造": ["2.20.1"],
    "归纳": ["2.20.2"],
    "染色": ["2.20.5"],
    "递归": ["2.20.4"],
    "对称": ["2.20.6"],
    "模": ["2.20.7"],
    "交互": ["2.20.8"],
    "奇偶": ["2.20.3"],
    "倍增": ["2.18.1"],
    "二分": ["2.18.5"],
    "整体二分": ["2.18.5"],
    "CDQ分治": ["2.18.6"],
    "扫描线": ["3.7.10"],
    "树链剖分": ["3.7.7"],
    "LCA": ["3.2.1"],
    "凸包": ["4.7.2"],
    "几何": ["4.7.1"],
    "计算几何": ["4.7.1"],
    "三角": ["4.7.4"],
    "圆": ["4.7.5"],
    "最近点": ["4.7.6"],
    "半平面": ["4.7.7"],
    "旋转卡壳": ["4.7.3"],
    "Pick定理": ["4.7.8"],
    "快速幂": ["2.16.1"],
    "逆序对": ["3.3.2"],
}

def find_prereqs(name, subcategory):
    prereqs = set()
    sid = section_by_subcat.get(subcategory, "2.1")
    core = section_core.get(sid, [])[:2]
    for iid in core:
        if iid in items_by_id:
            prereqs.add(iid)

    for kw, ids in EXTRA_PREREQ.items():
        if kw in name:
            for iid in ids:
                if iid in items_by_id:
                    prereqs.add(iid)
            if len(prereqs) >= 6:
                break

    if len(prereqs) < 2:
        for iid in core[2:]:
            if iid in items_by_id:
                prereqs.add(iid)
                if len(prereqs) >= 2:
                    break

    result = list(prereqs)[:6]
    if len(result) < 2:
        all_section = section_core.get(sid, [])
        result = [iid for iid in all_section[:3] if iid in items_by_id]

    result = [p for p in result if p.count(".") >= 2]
    return result

# ==== SELECT CANDIDATES ====
selected = []
seen_names = set()
seen_by_category = Counter()

def norm_name(n):
    return n.lower().replace(" ", "").replace("(", "").replace(")", "")

def is_duplicate_name(cand):
    nn = norm_name(cand["name"])
    if nn in all_item_names:
        return True
    cn_only = cand["name"].split("(")[0].strip().lower().replace(" ", "")
    if cn_only in all_item_names:
        return True
    if nn in seen_names:
        return True
    return False

def is_template_junk(cand):
    n = cand["name"]
    if cand.get("is_template") and cand.get("template_like_risk", "low") == "high":
        return True
    if cand.get("is_intra_dup"):
        return True
    junk_kw = ["边界压缩", "可合并状态", "在线转移", "离线转移", "分段决策",
               "的浅层", "的深层", "的中间层", "训练心理", "解题心理",
               "代码实现技巧", "解题分析", "桥梁能力"]
    for kw in junk_kw:
        if kw in n:
            return True
    return False

def is_reserve_ok(cand):
    if cand.get("duplicate_risk") == "high":
        return False
    if cand.get("template_like_risk") == "high" and cand.get("is_template"):
        return False
    if cand.get("is_intra_dup"):
        return False
    if is_template_junk(cand):
        return False
    return True

TARGET_DIST = {"算法": 255, "数据结构": 145, "数学": 200}
MAX_TOTAL = 600

# Step 1: All remaining ready_core (342)
for c in remaining_ready:
    if is_duplicate_name(c):
        continue
    if is_template_junk(c):
        continue
    selected.append(c)
    seen_names.add(norm_name(c["name"]))

rc_selected = len(selected)
rc_cat_selected = dict(Counter(c["category"] for c in selected))
print(f"\nStep1 ready_core selected: {rc_selected}")
print(f"  {rc_cat_selected}")

# Step 2: Fill gaps from reserve_useful
reserve_filtered = [c for c in reserve if not is_duplicate_name(c) and is_reserve_ok(c)]
reserve_filtered = [c for c in reserve_filtered if c.get("quality_score", 0) >= 2]
reserve_filtered.sort(key=lambda c: (
    c.get("quality_score", 0),
    0 if c.get("is_over_split") else 1,
    0 if c.get("granularity_risk") == "low" else 1,
    0 if c.get("duplicate_risk", "low") == "low" else 1),
    reverse=True)

print(f"  Reserve filtered: {len(reserve_filtered)} passing quality gates")

# First pass: high quality (qs=3)
for c in reserve_filtered:
    if len(selected) >= MAX_TOTAL:
        break
    cat = c["category"]
    if seen_by_category.get(cat, 0) + rc_cat_selected.get(cat, 0) >= TARGET_DIST.get(cat, 300):
        continue
    selected.append(c)
    seen_names.add(norm_name(c["name"]))
    seen_by_category[cat] = seen_by_category.get(cat, 0) + 1

# Second pass: fill remaining
for c in reserve_filtered:
    if len(selected) >= MAX_TOTAL:
        break
    if c in selected:
        continue
    cat = c["category"]
    if seen_by_category.get(cat, 0) + rc_cat_selected.get(cat, 0) >= TARGET_DIST.get(cat, 300):
        continue
    selected.append(c)
    seen_names.add(norm_name(c["name"]))
    seen_by_category[cat] = seen_by_category.get(cat, 0) + 1

final_cat = Counter(c["category"] for c in selected)
print(f"\nFinal selected: {len(selected)}")
print(f"  {dict(final_cat)}")
print(f"  Ready_core: {rc_selected}, Reserve_useful: {len(selected)-rc_selected}")

# ==== GENERATE SUGGESTED DIRECT_PRE ====
print(f"\nGenerating suggested_direct_pre...")
candidate_plans = []
for c in selected:
    name = c["name"]
    subcat = c["subcategory"]
    sid = section_by_subcat.get(subcat, "2.1")
    pre = find_prereqs(name, subcat)
    candidate_plans.append({
        "candidate_id": c["candidate_id"],
        "name": name,
        "category": c["category"],
        "subcategory": subcat,
        "target_section": sid,
        "source_tier": "ready_core" if c["decision"] == "ready_core" else "reserve_useful",
        "quality_score": c.get("quality_score", 0),
        "difficulty": c.get("difficulty", ""),
        "duplicate_risk": c.get("duplicate_risk", ""),
        "granularity_risk": c.get("granularity_risk", ""),
        "suggested_direct_pre": pre,
        "suggested_direct_pre_count": len(pre),
    })

over_limit = [p for p in candidate_plans if p["suggested_direct_pre_count"] > 8]
under_min = [p for p in candidate_plans if p["suggested_direct_pre_count"] < 2]
section_ref = [p for p in candidate_plans if any(x.count(".") < 2 for x in p["suggested_direct_pre"])]

print(f"  Direct pre > 8: {len(over_limit)}")
print(f"  Direct pre < 2: {len(under_min)}")
print(f"  Section refs: {len(section_ref)}")

# ==== PRE-CHECKS ====
print(f"\nRunning pre-checks...")

# 1. name exact dedup
exact_dup = []
for p in candidate_plans:
    nn = norm_name(p["name"])
    if nn in all_item_names:
        exact_dup.append(p["candidate_id"])

# 2. en_name dedup (candidates don't have en_name, skip)

# 3. alias conflict check
alias_conflicts = []
for p in candidate_plans:
    cn_only = p["name"].split("(")[0].strip()
    for existing_n in list(all_item_names)[:1000]:
        if cn_only.lower() in existing_n.lower():
            alias_conflicts.append(p["candidate_id"])
            break

# 4. intra-candidate duplicate
intra_names = [norm_name(p["name"]) for p in candidate_plans]
intra_dup = [p["candidate_id"] for i, p in enumerate(candidate_plans) if intra_names.count(intra_names[i]) > 1]

# 5. high-similarity intra-batch
similar_pairs = []
for i in range(len(candidate_plans)):
    for j in range(i+1, len(candidate_plans)):
        n1 = candidate_plans[i]["name"].split("(")[0].strip().lower()
        n2 = candidate_plans[j]["name"].split("(")[0].strip().lower()
        t1 = set(n1)
        t2 = set(n2)
        if len(t1 & t2) / max(len(t1|t2), 1) > 0.8:
            similar_pairs.append((candidate_plans[i]["candidate_id"], candidate_plans[j]["candidate_id"]))

# 6. Batch1 merged/removed duplicate
b1_removed_dup = [p["candidate_id"] for p in candidate_plans if norm_name(p["name"]) in {norm_name(n) for n in b1_removed_names}]

# 7. Direct pre all mappable
unmapped_pre = []
for p in candidate_plans:
    for iid in p["suggested_direct_pre"]:
        if iid not in items_by_id:
            unmapped_pre.append((p["candidate_id"], iid))

# 8. Section id in pre (already checked)

# 9. Pre over 8 (already checked)

# 10. Whole-section expansion risk
whole_section_risk = over_limit

# 11. Dangling refs
dangling_refs = unmapped_pre

# 12. Dependency cycle (simple check: all pre are existing items, no new nodes)
dep_cycle = False

# 13. New section needed
needs_new_section_cands = [p for p in candidate_plans if p["target_section"] not in set(item_section.values())]

# 14. Manual review candidates
manual_review = [p["candidate_id"] for p in candidate_plans if p["suggested_direct_pre_count"] < 2 or p.get("granularity_risk") == "high"]

# 15. Merge/collapse candidates
merge_collapse_cands = [p["candidate_id"] for p in candidate_plans if p.get("granularity_risk") == "high" or p.get("duplicate_risk") == "high"]

# Excluded items
excluded_dup = exact_dup + intra_dup
excluded_already = b1_removed_dup

dependency_cleanup_req = len(over_limit) > 0 or len(under_min) > 0 or len(section_ref) > 0 or len(unmapped_pre) > 0

has_issues = dependency_cleanup_req or len(needs_new_section_cands) > 0 or len(excluded_dup) > 0

recommendation = "ready_for_1号线程_merge_stage5_hard_batch2_full600"
if has_issues:
    recommendation = "needs_cleanup_before_merge"

precheck_result = {
    "baseline_item_count": total,
    "selected_candidate_count": len(candidate_plans),
    "recommendation": recommendation,
    "recommended_merge_count": len(candidate_plans),
    "dependency_cleanup_required": dependency_cleanup_req,
    "needs_new_section": len(needs_new_section_cands) > 0,
    "candidate_dependency_cycle": dep_cycle,
    "excluded_duplicate_or_near_duplicate": excluded_dup,
    "excluded_already_merged_candidates": excluded_already,
    "section_ref_dependencies": [p["candidate_id"] for p in section_ref],
    "manual_review_candidates": manual_review,
    "direct_pre_over_limit_candidates": [p["candidate_id"] for p in over_limit],
    "whole_section_expansion_risk_candidates": [p["candidate_id"] for p in whole_section_risk],
}

print(f"  Recommendation: {recommendation}")
print(f"  Dep cleanup required: {dependency_cleanup_req}")
print(f"  Needs new section: {len(needs_new_section_cands) > 0}")

# ==== OUTPUTS ====
print(f"\nWriting 3 output files...")

plan_out = {
    "meta": {"generated_at": ts, "baseline_item_count": total,
             "selected_candidate_count": len(candidate_plans),
             "ready_core_count": rc_selected,
             "reserve_useful_count": len(selected) - rc_selected,
             "main_graph_modified": False},
    "category_distribution": dict(final_cat),
    "subcategory_distribution": dict(Counter(p["subcategory"] for p in candidate_plans)),
    "candidates": candidate_plans
}
with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PLAN}")

precheck_out = {"meta": {"generated_at": ts, "main_graph_modified": False},
                "precheck": precheck_result}
with open(OUT_PRECHECK, "w", encoding="utf-8") as f:
    json.dump(precheck_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PRECHECK}")

# Report
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch2 full600 候选计划与动态预审报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")
    f.write(f"## 1. 当前基线\n\n**{total}** items, **{sec_count}** sections\n\n")
    f.write(f"## 2. 候选来源分布\n\n")
    f.write(f"| 来源 | 数量 |\n|------|------|\n")
    f.write(f"| ready_core (剩余) | {rc_selected} |\n")
    f.write(f"| reserve_useful (精选) | {len(selected)-rc_selected} |\n")
    f.write(f"| **总计** | **{len(candidate_plans)}** |\n\n")
    f.write(f"## 3. 算法/数据结构/数学分布\n\n")
    f.write(f"| Category | 目标 | 实际 |\n|----------|------|------|\n")
    for cat in ["算法", "数据结构", "数学"]:
        target = TARGET_DIST.get(cat, "-")
        actual = final_cat.get(cat, 0)
        status = "✅" if abs(actual - target) <= 20 else "⚠️"
        f.write(f"| {cat} | {target} | {status} {actual} |\n")
    f.write(f"\n## 4. 子类分布\n\n")
    f.write(f"| Subcategory | Count |\n|------------|------|\n")
    for sc, cnt in Counter(p["subcategory"] for p in candidate_plans).most_common(20):
        f.write(f"| {sc} | {cnt} |\n")
    f.write(f"\n## 5. 查重结果\n\n")
    f.write(f"| 检查项 | 数量 |\n|--------|------|\n")
    f.write(f"| 与已有 2640 节点精确重名 | {len(exact_dup)} |\n")
    f.write(f"| Batch1 已合并节点重名 | {len(b1_removed_dup)} |\n")
    f.write(f"| 候选内部重复 | {len(intra_dup)} |\n")
    f.write(f"| 候选间高相似 | {len(similar_pairs)} |\n")
    f.write(f"\n## 6. 依赖映射结果\n\n")
    f.write(f"| 检查项 | 数量 |\n|--------|------|\n")
    f.write(f"| 全部映射到正式 item_id | {len(candidate_plans) - len(unmapped_pre)}/{len(candidate_plans)} |\n")
    f.write(f"| 无法映射 | {len(unmapped_pre)} |\n")
    f.write(f"| section id refs | {len(section_ref)} |\n")
    f.write(f"\n## 7. direct_pre 数量分布\n\n")
    pre_counts = Counter(p["suggested_direct_pre_count"] for p in candidate_plans)
    f.write(f"| Count | 候选数 |\n|-------|--------|\n")
    for cnt in sorted(pre_counts.keys()):
        f.write(f"| {cnt} | {pre_counts[cnt]} |\n")
    f.write(f"\n## 8. 是否存在整节展开风险\n\n")
    f.write(f"**{'否' if len(whole_section_risk) == 0 else f'是 — {len(whole_section_risk)} 个候选 over limit'}**\n\n")
    f.write(f"## 9. 是否需要依赖清理\n\n")
    f.write(f"**{'否' if not dependency_cleanup_req else '是'}**\n\n")
    f.write(f"## 10. 是否需要新 section\n\n")
    f.write(f"**{'否' if len(needs_new_section_cands) == 0 else f'是 — {len(needs_new_section_cands)} 个'}**\n\n")
    f.write(f"## 11. 是否建议合并\n\n")
    f.write(f"**{'是 — ready_for_1号线程_merge' if recommendation.startswith('ready') else '否 — needs_cleanup_before_merge'}**\n\n")
    f.write(f"## 12. 合并后预计 item_count\n\n")
    f.write(f"**{total + len(candidate_plans)}** (2640 + {len(candidate_plans)})\n\n")
    f.write(f"## 13. 是否修改主图谱\n\n**否** ✅\n\n")
    f.write(f"## 14. 是否继续自动 Batch3\n\n**否** ✅\n\n")
    f.write(f"## 15. 下一步建议\n\n")
    if recommendation.startswith("ready"):
        f.write("1. 1号线程执行 merge 操作\n")
        f.write("2. 合并后运行 validate-only\n")
        f.write("3. 生成内容包\n\n")
    else:
        f.write("1. 先清理依赖问题\n")
        f.write("2. 修复后重新预审\n\n")
    f.write("---\n*本报告自动生成，未修改任何文件*\n")

print(f"  [OK] {OUT_REPORT}")
print(f"\n{'=' * 60}")
print(f"  Plan Complete")
print(f"{'=' * 60}")
print(f"  Candidates: {len(candidate_plans)}")
print(f"  Ready_core: {rc_selected}, Reserve: {len(selected)-rc_selected}")
print(f"  Recommendation: {recommendation}")
print(f"  No graph modifications.")
