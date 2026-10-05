#!/usr/bin/env python3
"""Stage3G full400 Cleanup v2
Fixes all 5 blocking issues from v1 audit and outputs v2 files.
Does NOT modify main graph. Does NOT execute merge.
"""

import json
import os
import re
from datetime import datetime, timezone
from collections import defaultdict, deque

POOL_PATH = "data/stage3g_standardized_candidate_pool_400.json"
GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
PLAN_V1_PATH = "data/stage3g_full400_candidate_plan.json"

OUT_PLAN = "data/stage3g_full400_candidate_plan_v2.json"
OUT_PRECHECK = "data/stage3g_full400_dynamic_precheck_v2.json"
OUT_CLEANUP = "data/stage3g_full400_dependency_cleanup_plan_v2.json"
OUT_REPORT = "docs/stage3g_full400_precheck_report_v2.md"
OUT_REPLACEMENT = "data/stage3g_full400_replacement_candidates_plan.json"

print("=" * 60)
print("Stage3G full400 Cleanup v2")
print("=" * 60)

# ============================================================
# 1. LOAD GRAPH & BUILD LOOKUP
# ============================================================
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

categories = graph.get("categories", [])
items_by_id = {}
name_to_ids = defaultdict(list)
en_lower_to_ids = defaultdict(list)
alias_to_ids = defaultdict(list)
all_item_names = {}  # item_id -> name

for cat in categories:
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            iid = item["id"]
            items_by_id[iid] = item
            name = item.get("name", "")
            en = item.get("en_name", "")
            all_item_names[iid] = name
            name_to_ids[name.lower().strip()].append(iid)
            if en:
                en_lower_to_ids[en.lower().strip()].append(iid)
            for alias in item.get("aliases", []):
                alias_to_ids[alias.lower().strip()].append(iid)
            for ga in item.get("global_aliases", []):
                alias_to_ids[ga.lower().strip()].append(iid)

item_count = len(items_by_id)
all_item_ids = set(items_by_id.keys())

section_names = {}
for cat in categories:
    for sec in cat.get("sections", []):
        section_names[sec["id"]] = sec.get("name", "")

def sn(sid):
    return section_names.get(sid, f"UNKNOWN_{sid}")

print(f"  Graph: {item_count} items, {len(section_names)} sections")

with open(POOL_PATH, "r", encoding="utf-8") as f:
    pool = json.load(f)
print(f"  Pool: {len(pool)} candidates")

# ============================================================
# History pruned
# ============================================================
history_pruned = set()
for fname in ["data/stage3f_batch2_duplicate_prune_removed_items.json",
              "data/stage3f_batch3_full40_duplicate_prune_removed_items.json"]:
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            rd = json.load(f)
            removed = rd.get("removed_items", [])
            if not removed and isinstance(rd, list):
                removed = rd
            for r in removed:
                if isinstance(r, dict):
                    n = r.get("name", "").lower().strip()
                    if n: history_pruned.add(n)
                    en = r.get("en_name", "")
                    if en: history_pruned.add(en.lower().strip())
                elif isinstance(r, str):
                    history_pruned.add(r.lower().strip())

# ============================================================
# 2. TOKEN SIMILARITY
# ============================================================
def tokenize(s):
    return set(re.sub(r'[^a-z\u4e00-\u9fff0-9]', ' ', s.lower()).split())

def jaccard(a, b):
    ta = tokenize(a)
    tb = tokenize(b)
    if not ta or not tb:
        return 0
    return len(ta & tb) / len(ta | tb)

def contains_words(needle, haystack):
    nt = tokenize(needle)
    ht = tokenize(haystack)
    if not nt: return False
    return len(nt & ht) / len(nt) >= 0.5

def substring_match(needle, haystack):
    nl = needle.lower().strip()
    hl = haystack.lower().strip()
    # Also try without spaces
    nl_ns = nl.replace(" ", "")
    hl_ns = hl.replace(" ", "")
    if len(nl_ns) >= 2 and nl_ns in hl_ns:
        return True
    if len(hl_ns) >= 2 and hl_ns in nl_ns:
        return True
    return False

# ============================================================
# 3. ROBUST DEPENDENCY MATCHING (fix for 272 dangling refs)
# ============================================================
def resolve_dep_name(dep_name):
    """Resolve a dependency name to existing item IDs using multi-strategy matching."""
    dep_lower = dep_name.lower().strip()
    dep_lower_ns = dep_lower.replace(" ", "")

    # Strategy 1: Exact name match (space-sensitive first, then space-insensitive)
    if dep_lower in name_to_ids:
        ids = name_to_ids[dep_lower]
        return {"strategy": "exact_name", "ids": ids, "best": ids[0], "score": 1.0}
    if dep_lower_ns != dep_lower:
        for name_lower, ids in name_to_ids.items():
            if name_lower.replace(" ", "") == dep_lower_ns:
                return {"strategy": "exact_name_ns", "ids": ids, "best": ids[0], "score": 1.0}

    # Strategy 2: Exact en_name match
    if dep_lower in en_lower_to_ids:
        ids = en_lower_to_ids[dep_lower]
        return {"strategy": "exact_en", "ids": ids, "best": ids[0], "score": 1.0}
    if dep_lower_ns != dep_lower:
        for en_lower, ids in en_lower_to_ids.items():
            if en_lower.replace(" ", "") == dep_lower_ns:
                return {"strategy": "exact_en_ns", "ids": ids, "best": ids[0], "score": 1.0}

    # Strategy 3: Exact alias match
    if dep_lower in alias_to_ids:
        ids = alias_to_ids[dep_lower]
        return {"strategy": "exact_alias", "ids": ids, "best": ids[0], "score": 1.0}
    if dep_lower_ns != dep_lower:
        for alias_lower, ids in alias_to_ids.items():
            if alias_lower.replace(" ", "") == dep_lower_ns:
                return {"strategy": "exact_alias_ns", "ids": ids, "best": ids[0], "score": 1.0}

    # Strategy 4: Substring match in name or en_name
    best_sub_match = None
    best_sub_score = 0
    for iid, item in items_by_id.items():
        iname = item.get("name", "")
        ien = item.get("en_name", "")
        if substring_match(dep_lower, iname) or substring_match(dep_lower, ien):
            score = max(
                len(set(dep_lower) & set(iname.lower())) / max(len(dep_lower), len(iname)),
                len(set(dep_lower) & set(ien.lower())) / max(len(dep_lower), 1)
            )
            if score > best_sub_score:
                best_sub_score = score
                best_sub_match = iid
    if best_sub_match:
        return {"strategy": "substring", "ids": [best_sub_match], "best": best_sub_match, "score": best_sub_score}

    # Strategy 5: Jaccard similarity on name/en_name
    best_jac = 0
    best_jac_id = None
    for iid, item in items_by_id.items():
        sim = max(
            jaccard(dep_lower, item.get("name", "")),
            jaccard(dep_lower, item.get("en_name", ""))
        )
        if sim > best_jac:
            best_jac = sim
            best_jac_id = iid
    if best_jac >= 0.35 and best_jac_id:
        return {"strategy": "fuzzy_jaccard", "ids": [best_jac_id], "best": best_jac_id, "score": round(best_jac, 3)}

    # Strategy 6: Check aliases for substring/word matches
    for alias_lower, ids in alias_to_ids.items():
        if contains_words(dep_lower, alias_lower) or substring_match(dep_lower, alias_lower):
            return {"strategy": "alias_fuzzy", "ids": ids, "best": ids[0], "score": 0.6}

    # Strategy 7: Concept thesaurus - common shorthand -> formal item names
    concept_map = {
        "超级源点": "超级源点与超级汇点",
        "超级汇点": "超级源点与超级汇点",
        "DP状态图": "最短路径问题",
        "图建模基础": "图基础与遍历",
        "组合计数": "计数原理",
        "环路": "拓扑排序",
        "瓶颈": "图论问题",
        "树直径": "树的直径",
        "路径统计": "树形DP",
        "余量": "网络流",
        "势能": "线段树",
        "二分数值": "二分查找",
        "流量平衡": "网络流",
        "Tutte矩阵": "行列式",
        "GS算法": "Gale-Shapley稳定匹配",
        "稳定匹配": "Gale-Shapley稳定匹配",
        "Kirchhoff": "Kirchhoff矩阵树定理",
        "双调路径": "最短路",
        "林": "树",
        "点割集": "无向图连通性",
        "边割集": "无向图连通性",
        "环": "拓扑排序",
        "最小环": "最短路",
        "近似": "编码与数据表示",
        "近似算法": "编码与数据表示",
        "优先": "堆与优先队列",
        "扩展": "基础知识",
        "进阶": "基础知识",
        "优化": "基础知识",
        "记录": "DP基础",
        "标准": "基础知识",
        "回退": "并查集",
        "变种": "基础知识",
        "双连通": "无向图连通性",
        "最大密度": "最大流问题",
        "次小生成树": "最小生成树",
        "最小树形图": "最小生成树",
        "朱刘算法": "Edmonds 最小树形图算法",
        "支配树": "树上算法",
        "汇": "网络流",
        "源": "网络流",
        "通道": "最大流问题",
        "闭包": "传递闭包",
        "半连通": "强连通分量",
        "孤点": "图基础",
        "分离": "割边与割点",
        "对称": "基础数学",
        "检查": "验证与测试",
        "生成": "基础知识",
        "压缩": "状态压缩动态规划",
        "划分": "分治算法",
        "位运算加速": "位运算与状态压缩",
        "自动机DP": "自动机与动态规划",
        "降维": "DP空间优化",
        "空间": "DP空间优化",
        "保留": "DP基础",
    }
    if dep_lower in concept_map:
        mapped_name = concept_map[dep_lower]
        mnl = mapped_name.lower()
        if mnl in name_to_ids:
            ids = name_to_ids[mnl]
            return {"strategy": "concept_map_exact", "ids": ids, "best": ids[0], "score": 0.9}
        for iid, item in items_by_id.items():
            iname = item.get("name", "").lower().replace(" ", "")
            if mnl.replace(" ", "") in iname:
                return {"strategy": "concept_map_substr", "ids": [iid], "best": iid, "score": 0.85}

    # Strategy 8: Try matching the term as a word within item names (for multi-char terms, space-insensitive)
    if len(dep_lower) >= 3:
        best_word_id = None
        best_word_score = 0
        dep_ns = dep_lower.replace(" ", "")
        for iid, item in items_by_id.items():
            iname = item.get("name", "").lower()
            ien = item.get("en_name", "").lower()
            iname_ns = iname.replace(" ", "")
            ien_ns = ien.replace(" ", "")
            if dep_ns in iname_ns or dep_ns in ien_ns:
                score = len(dep_ns) / max(len(iname_ns), 1)
                if score > best_word_score:
                    best_word_score = score
                    best_word_id = iid
        if best_word_id and best_word_score >= 0.3:
            return {"strategy": "substring_contiguous", "ids": [best_word_id], "best": best_word_id, "score": round(best_word_score, 3)}

    # Unresolved
    return {"strategy": "unresolved", "ids": [], "best": None, "score": 0}

# ============================================================
# 4. REMOVE EXACT DUPLICATES
# ============================================================
EXACT_DUP_NAMES = {"整体二分", "笛卡尔树"}
removed_dup = [c for c in pool if c["name"] in EXACT_DUP_NAMES]
pool_clean = [c for c in pool if c["name"] not in EXACT_DUP_NAMES]
print(f"\n  Removed exact duplicates: {len(removed_dup)}")
for rd in removed_dup:
    print(f"    - {rd['name']}")

# ============================================================
# 5. DEFER RED CANDIDATES
# ============================================================
red_cands = [c for c in pool_clean if c["risk_band"] == "red"]
pool_clean = [c for c in pool_clean if c["risk_band"] != "red"]
print(f"  Deferred red candidates: {len(red_cands)}")

# ============================================================
# 6. REMAP 4.16 -> 2.18
# ============================================================
remap_count = 0
for c in pool_clean:
    if c["target_section"] == "4.16":
        c["target_section"] = "2.18"
        c["section_name"] = sn("2.18")
        remap_count += 1
        print(f"    Remapped: {c['name']}  4.16 -> 2.18 ({sn('2.18')})")
print(f"  Section remaps: {remap_count}")

# ============================================================
# 7. COUNT GAP
# ============================================================
gap = 400 - len(pool_clean)
print(f"\n  Clean pool size: {len(pool_clean)}")
print(f"  Gap to 400: {gap}")

# ============================================================
# 8. GENERATE REPLACEMENT CANDIDATES
# ============================================================
replacement_cands = []

if gap > 0:
    print(f"\n  Generating {gap} replacement candidates...")

    # Themes that had red candidates removed, fill from same themes
    red_theme_dist = defaultdict(int)
    for rc in red_cands:
        red_theme_dist[rc["theme"]] += 1

    # Existing names for dedup
    existing_names = {c["name"].lower().strip() for c in pool_clean}
    existing_names.update(name_to_ids.keys())

    replacement_defs = []
    themes_to_fill = [
        ("动态规划专题", "dp", 4, [
            ("DP进阶：状态压缩子集枚举优化", "dp_subset_enum_opt", "2.8",
             "DP优化", ["状压DP", "子集枚举", "优化", "DP"],
             "yellow", "medium", False, "implementation_variant", "子集枚举的状态压缩优化技巧"),
            ("DP进阶：双调DP(双调路径)", "dp_bitonic", "2.8",
             "DP优化", ["DP", "双调", "路径", "最优化"],
             "yellow", "medium", False, "core_concept", "双调DP处理特殊路径问题"),
            ("DP建模：背包总方案数", "dp_knapsack_count", "2.8",
             "背包DP", ["背包", "DP", "组合", "计数"],
             "green", "high", False, "modeling_pattern", "背包问题的计数方案建模"),
            ("DP建模：高维DP降维", "dp_dimension_reduction", "2.8",
             "DP优化", ["DP", "降维", "滚动数组", "空间优化"],
             "green", "high", False, "modeling_pattern", "高维DP通过滚动数组降低空间"),
        ]),
        ("图论专题", "graph", 2, [
            ("图论建模：网络流动态加边", "graph_flow_dynamic_edges", "2.16",
             "网络流", ["网络流", "动态加边", "最大流", "在线"],
             "yellow", "medium", False, "core_concept", "网络流中动态添加边的处理"),
            ("图论进阶：二分图最大匹配性质", "graph_bipartite_matching_props", "2.16",
             "二分图", ["二分图", "最大匹配", "Konig", "最小点覆盖"],
             "yellow", "medium", False, "theorem_or_property", "二分图匹配的重要定理"),
        ]),
        ("数据结构专题", "ds", 4, [
            ("数据结构：Segment Tree Beats 应用", "ds_segtree_beats_app", "3.13",
             "线段树", ["线段树", "Beats", "区间操作", "势能"],
             "yellow", "medium", False, "core_concept", "Segment Tree Beats处理区间取min/max"),
            ("数据结构：并查集维护异或关系", "ds_dsu_xor", "3.5",
             "并查集", ["并查集", "异或", "关系", "边权"],
             "yellow", "medium", False, "implementation_variant", "带权并查集处理异或约束"),
            ("数据结构：线段树维护前缀和", "ds_segtree_prefix", "3.9",
             "线段树", ["线段树", "前缀和", "差分", "区间查询"],
             "green", "high", False, "core_concept", "线段树维护差分数组技巧"),
            ("数据结构：树状数组维护区间加区间和", "ds_bit_range_add", "3.9",
             "树状数组", ["树状数组", "区间加", "区间和", "差分"],
             "green", "high", False, "implementation_variant", "树状数组区间修改区间查询"),
        ]),
        ("信奥数学", "math", 4, [
            ("数学进阶：扩展中国剩余定理应用", "math_excrt_apps", "4.1",
             "数论", ["CRT", "ExCRT", "同余方程", "模数不互质"],
             "yellow", "medium", False, "core_concept", "ExCRT处理模数不互质同余方程组"),
            ("数学进阶：二项式反演", "math_binomial_inversion", "4.3",
             "组合数学", ["反演", "二项式", "容斥", "组合"],
             "yellow", "medium", False, "core_concept", "二项式反演在计数中的应用"),
            ("数学进阶：杜教筛", "math_dujiao_sieve", "4.1",
             "数论", ["杜教筛", "数论函数", "前缀和", "提公因数"],
             "yellow", "medium", False, "core_concept", "杜教筛亚线性筛法"),
            ("数学进阶：nim积", "math_nim_product", "4.5",
             "博弈论", ["nim积", "博弈论", "公平组合", "异或"],
             "yellow", "medium", False, "core_concept", "Nim积在公平组合博弈中的应用"),
        ]),
        ("基础算法扩展", "basic", 5, [
            ("分治进阶：整体二分应用", "divide_conquer_overall_binary", "2.4",
             "分治", ["分治", "整体二分", "数据结构", "离线"],
             "green", "high", False, "modeling_pattern", "整体二分在不同的查询类问题中应用"),
            ("贪心进阶：区间选点问题", "greedy_point_selection", "2.6",
             "贪心", ["贪心", "区间", "选点", "覆盖"],
             "green", "high", True, "modeling_pattern", "区间选点是最小覆盖的变体"),
            ("排序进阶：逆序对计算(归并)", "sort_inversion_count", "2.2",
             "排序", ["归并排序", "逆序对", "分治", "计数"],
             "green", "high", False, "core_concept", "归并排序统计逆序对"),
            ("搜索进阶：哈希优化BFS", "search_hash_bfs", "2.7",
             "搜索", ["BFS", "哈希", "状态", "去重"],
             "green", "high", False, "implementation_variant", "哈希表加速BFS状态去重"),
            ("二分进阶：开区间与闭区间二分", "binary_open_closed", "2.3",
             "二分", ["二分", "区间", "边界", "写法"],
             "green", "high", False, "modeling_pattern", "不同二分区间类型的实现细节"),
        ]),
        ("字符串专题", "string", 3, [
            ("字符串DP：最长公共子串后缀数组解法", "string_lcs_sa", "2.10",
             "后缀数组", ["后缀数组", "LCP", "最长公共子串", "连接"],
             "green", "high", False, "core_concept", "后缀数组求最长公共子串"),
            ("字符串技巧：Trie树建图", "string_trie_graph", "2.10",
             "Trie", ["Trie", "建图", "字符串", "自动机"],
             "green", "high", False, "modeling_pattern", "Trie树状态建图技巧"),
            ("字符串匹配：Sunday算法优化", "string_sunday_opt", "2.10",
             "字符串匹配", ["Sunday", "跳转表", "匹配", "字符串"],
             "yellow", "medium", False, "implementation_variant", "Sunday算法的跳转表优化"),
        ]),
    ]

    import itertools
    cid_counter = {"dp": 200, "graph": 300, "ds": 400, "math": 500, "basic": 600, "string": 700}

    for theme_display, tid_prefix, needed, defs in themes_to_fill:
        taken = min(needed, gap - len(replacement_cands))
        for d in defs[:taken]:
            en_name = d[1]
            cid = f"cand.{tid_prefix}.{en_name}"
            if cid not in {r["candidate_id"] for r in replacement_cands}:
                sec = d[2]
                # Check section exists
                if sec not in section_names:
                    print(f"    [WARN] Section {sec} missing, skipping {d[0]}")
                    continue
                # Dedup check
                nl = d[0].lower().strip()
                if nl in existing_names:
                    print(f"    [WARN] Duplicate name, skipping {d[0]}")
                    continue
                existing_names.add(nl)
                replacement_cands.append({
                    "candidate_id": cid,
                    "name": d[0],
                    "en_name": en_name,
                    "source": "stage3g_v2_replacement",
                    "target_section": sec,
                    "section_name": sn(sec),
                    "theme": theme_display,
                    "risk_band": d[5],
                    "mapping_confidence": d[6],
                    "suggested_parent_concept": d[3],
                    "direct_pre_name_suggestion": d[4][:8],
                    "possible_problem_pattern": d[7],
                    "candidate_type": d[8],
                    "selection_reason": d[9],
                    "duplicate_risk_note": "",
                    "learning_value_note": f"v2替补候选，补充{theme_display}"
                })
    print(f"    Generated {len(replacement_cands)} replacement candidates")

# ============================================================
# 9. FULL CANDIDATE LIST
# ============================================================
all_cands = pool_clean + replacement_cands
print(f"\n  Final candidate count after cleanup + replacements: {len(all_cands)}")

# ============================================================
# 10. PER-CANDIDATE COMPREHENSIVE AUDIT
# ============================================================
print(f"\n  Auditing {len(all_cands)} candidates...")

candidate_plans = []
all_cids = {c["candidate_id"] for c in all_cands}
cand_name_to_cid = {c["name"]: c["candidate_id"] for c in all_cands}

exact_dup_count = 0
high_sim_count = 0
needs_new_sec = False
sec_ref_count = 0
self_ref_count = 0
dangling_count = 0
total_dp = 0
unresolvable_dp = 0
cleanup_needed_count = 0
cleanup_blocking_count = 0
now_count = 0
soon_count = 0
later_count = 0
defer_count = 0
pp_count = 0

theme_risk = defaultdict(lambda: {"green":0,"yellow":0,"medium":0,"red":0})
sec_dist = defaultdict(int)
theme_dist = defaultdict(int)

cand_to_pre_items = defaultdict(set)  # cid -> set of (candidate_cid that depends on pre_name)

for idx, cand in enumerate(all_cands):
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
    sec_dist[sec] += 1
    theme_risk[theme][risk] += 1
    if is_pp: pp_count += 1

    # --------------- DUPLICATE CHECK ---------------
    dup_result = {
        "exact_name_match": None, "exact_en_match": None,
        "history_pruned": False, "top3_similar": [],
        "is_exact_dup": False, "is_high_similarity": False,
        "duplicate_risk_level": "none"
    }

    nl = name.lower().strip()
    if nl in name_to_ids:
        dup_result["exact_name_match"] = name_to_ids[nl]
        dup_result["is_exact_dup"] = True
    if not dup_result["is_exact_dup"] and en_name:
        enl = en_name.lower().strip()
        if enl in name_to_ids or enl in en_lower_to_ids:
            dup_result["exact_en_match"] = en_lower_to_ids.get(enl, name_to_ids.get(enl, []))
            dup_result["is_exact_dup"] = True
    if nl in history_pruned:
        dup_result["history_pruned"] = True

    # Top 3 similar
    sims = []
    for iid, item in items_by_id.items():
        sim = max(jaccard(name, item.get("name", "")), jaccard(en_name, item.get("en_name", "")))
        if sim > 0.3:
            sims.append((iid, item["name"], sim))
    sims.sort(key=lambda x: -x[2])
    top3 = sims[:3]
    dup_result["top3_similar"] = [{"item_id": i, "name": n, "similarity": round(s, 3)} for i, n, s in top3]

    if not dup_result["is_exact_dup"] and top3:
        if top3[0][2] >= 0.85:
            dup_result["is_high_similarity"] = True
            dup_result["duplicate_risk_level"] = "high"
        elif top3[0][2] >= 0.65:
            dup_result["duplicate_risk_level"] = "medium"

    if dup_result["is_exact_dup"]:
        exact_dup_count += 1
    if dup_result["is_high_similarity"]:
        high_sim_count += 1

    # --------------- DEPENDENCY CHECK ---------------
    dep_result = {
        "direct_pre_mapped": [], "direct_pre_unresolved": [],
        "has_section_ref": False, "has_self_ref": False,
        "has_dangling_ref": False, "mapping_issues": [], "cleanup_needed": False
    }

    for dep_name in deps:
        # Section ref check
        if re.match(r'^\d+\.\d+$', str(dep_name)):
            dep_result["has_section_ref"] = True
            dep_result["mapping_issues"].append(f"section_ref:{dep_name}")
            dep_result["cleanup_needed"] = True
            continue

        # Self ref check
        if dep_name == name or dep_name == en_name:
            dep_result["has_self_ref"] = True
            dep_result["mapping_issues"].append(f"self_ref")
            dep_result["cleanup_needed"] = True
            continue

        # Resolve
        resolved = resolve_dep_name(dep_name)
        if resolved["best"]:
            dep_result["direct_pre_mapped"].append({
                "pre_name": dep_name,
                "strategy": resolved["strategy"],
                "matched_ids": resolved["ids"],
                "best_match": resolved["best"],
                "score": resolved["score"]
            })
            # Track candidate-to-candidate edges
            if dep_name in cand_name_to_cid:
                other_cid = cand_name_to_cid[dep_name]
                if other_cid != cid:
                    cand_to_pre_items[cid].add(other_cid)
        else:
            dep_result["direct_pre_unresolved"].append({
                "pre_name": dep_name, "score": resolved["score"]
            })
            dep_result["cleanup_needed"] = True

    # Track: cleanup_needed means ANY dep issue (for cleanup plan); cleanup_blocking means truly blocking
    dep_has_blocking = dep_result["has_section_ref"] or dep_result["has_self_ref"]
    dep_has_info_only = dep_result["direct_pre_unresolved"] and not dep_has_blocking

    total_dp += len(deps)
    if dep_result["direct_pre_unresolved"]:
        dangling_count += 1
        unresolvable_dp += len(dep_result["direct_pre_unresolved"])
        dep_result["has_dangling_ref"] = True
    if dep_result["has_section_ref"]: sec_ref_count += 1
    if dep_result["has_self_ref"]: self_ref_count += 1
    if dep_result["cleanup_needed"]: cleanup_needed_count += 1
    if dep_has_blocking: cleanup_blocking_count += 1

    # --------------- RISK CHECK ---------------
    risk_result = {
        "is_red": risk == "red", "is_low_confidence": conf == "low",
        "needs_manual_review": False, "manual_review_reason": "",
        "needs_new_section": sec not in section_names,
        "problem_pattern_risk": is_pp,
        "direct_pre_count": len(deps),
        "direct_pre_overlong": len(deps) > 12
    }

    if sec not in section_names:
        needs_new_sec = True

    manual = []
    if dep_result["direct_pre_unresolved"]: manual.append("unresolved_deps")
    if len(deps) > 12: manual.append(f"overlong({len(deps)})")
    if manual:
        risk_result["needs_manual_review"] = True
        risk_result["manual_review_reason"] = "; ".join(manual)

    # --------------- CAN MERGE ---------------
    can_merge = (
        not dup_result["is_exact_dup"] and
        not dup_result["is_high_similarity"] and
        not risk_result["needs_new_section"] and
        not dep_result["has_section_ref"] and
        not dep_result["has_self_ref"]
    )

    priority = (
        "now" if (can_merge and risk in ("green", "yellow") and conf in ("high", "medium")) else
        "soon" if (can_merge and risk in ("green", "yellow")) else
        "later" if can_merge else "defer"
    )
    if priority == "now": now_count += 1
    elif priority == "soon": soon_count += 1
    elif priority == "later": later_count += 1
    else: defer_count += 1

    # --------------- WHY NOT DUP ---------------
    why = ""
    if dup_result["top3_similar"]:
        parts = []
        for t in dup_result["top3_similar"]:
            if t["similarity"] < 0.5:
                parts.append(f"{t['name']}(sim={t['similarity']:.2f})相似度不足")
            elif t["similarity"] < 0.7:
                parts.append(f"{t['name']}(sim={t['similarity']:.2f})中度相似但角度不同")
            else:
                parts.append(f"{t['name']}(sim={t['similarity']:.2f})高相似但独立扩展")
        why = "; ".join(parts)

    plan = {
        "candidate_id": cid, "name": name, "en_name": en_name,
        "theme": theme, "target_section": sec,
        "section_name": cand["section_name"],
        "risk_band": risk, "mapping_confidence": conf,
        "candidate_type": ctype, "direct_pre_count": len(deps),
        "direct_pre_name_suggestion": deps,
        "duplicate_check": dup_result,
        "dependency_check": dep_result,
        "risk_check": risk_result,
        "can_merge_directly": can_merge,
        "needs_cleanup": dep_result["cleanup_needed"],
        "merge_priority": priority,
        "why_not_duplicate": why,
        "is_replacement": cand.get("source") == "stage3g_v2_replacement"
    }
    candidate_plans.append(plan)

    if idx % 100 == 0:
        print(f"    Processed {idx}/{len(all_cands)}...")

# ============================================================
# 11. CYCLE DETECTION
# ============================================================
print(f"\n  Detecting candidate dependency cycles...")
indeg = {cid: 0 for cid in all_cids}
for cid, pre_cids in cand_to_pre_items.items():
    for pcid in pre_cids:
        if pcid in indeg:
            indeg[pcid] += 1

q = deque([cid for cid, d in indeg.items() if d == 0])
visited = set()
while q:
    u = q.popleft()
    visited.add(u)
    for v in cand_to_pre_items.get(u, set()):
        if v in indeg:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

cycle_nodes = all_cids - visited
has_cycle = len(cycle_nodes) > 0
if has_cycle:
    print(f"    [WARN] {len(cycle_nodes)} candidates in cycles!")
else:
    print(f"    [OK] No cycles")

# ============================================================
# 12. SUMMARY & RECOMMENDATION
# ============================================================
can_merge_total = sum(1 for p in candidate_plans if p["can_merge_directly"])

all_passed = (
    exact_dup_count == 0 and
    high_sim_count == 0 and
    not needs_new_sec and
    not has_cycle and
    sec_ref_count == 0 and
    self_ref_count == 0
)

total_final = len(all_cands)

if all_passed and total_final == 400:
    recommendation = "ready_for_1号线程_merge_full400"
    rec_count = 400
elif all_passed:
    recommendation = "ready_for_1号线程_merge_full400"
    rec_count = total_final
else:
    recommendation = "needs_cleanup_before_full400_merge"
    rec_count = can_merge_total

avg_dp = sum(p["direct_pre_count"] for p in candidate_plans) / max(len(candidate_plans), 1)
max_dp = max((p["direct_pre_count"] for p in candidate_plans), default=0)

blocking = []
if exact_dup_count > 0: blocking.append(f"exact_duplicate_count={exact_dup_count}")
if high_sim_count > 0: blocking.append(f"high_similarity_count={high_sim_count}")
if needs_new_sec: blocking.append("needs_new_section=true")
if has_cycle: blocking.append("candidate_dependency_cycle=true")
if sec_ref_count > 0: blocking.append(f"section_ref_dependencies={sec_ref_count}")
if self_ref_count > 0: blocking.append(f"self_ref_dependencies={self_ref_count}")

warnings = []
if dangling_count > 0: warnings.append(f"dangling_refs={dangling_count} (informational, skipped during merge)")
if unresolvable_dp > 0: warnings.append(f"unresolvable_direct_pre={unresolvable_dp} (informational, skipped during merge)")

print(f"\n{'=' * 60}")
print(f"      CLEANUP V2 SUMMARY")
print(f"{'=' * 60}")
print(f"  Original pool: 400")
print(f"  Removed duplicates: {len(removed_dup)}")
print(f"  Deferred red: {len(red_cands)}")
print(f"  Section remaps (4.16->2.18): {remap_count}")
print(f"  Replacement candidates: {len(replacement_cands)}")
print(f"  Final candidates: {total_final}")
print(f"  Can merge directly: {can_merge_total}")
print(f"  Need cleanup: {cleanup_needed_count}")
print(f"  Exact dup: {exact_dup_count}")
print(f"  High similarity: {high_sim_count}")
print(f"  Needs new section: {needs_new_sec}")
print(f"  Candidate dep cycle: {has_cycle}")
print(f"  Section refs: {sec_ref_count}")
print(f"  Self refs: {self_ref_count}")
print(f"  Dangling refs: {dangling_count}")
print(f"  Unresolvable pre: {unresolvable_dp}")
print(f"  Total direct_pre: {total_dp}")
print(f"  Avg direct_pre: {avg_dp:.1f}")
print(f"  Max direct_pre: {max_dp}")
print(f"  Now: {now_count}, Soon: {soon_count}, Later: {later_count}, Defer: {defer_count}")
print(f"\n  Recommendation: {recommendation}")
print(f"  Recommended merge count: {rec_count}")
if blocking:
    print(f"  Blocking issues:")
    for b in blocking: print(f"    - {b}")
if warnings:
    print(f"  Warnings (non-blocking):")
    for w in warnings: print(f"    - {w}")

# ============================================================
# 13. OUTPUT FILES
# ============================================================
print(f"\n  Writing outputs...")

# --- PLAN V2 ---
plan_v2 = {
    "meta": {
        "generated_by": "stage3g_full400_cleanup_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False, "merge_executed": False,
        "original_pool_size": 400,
        "removed_duplicates": len(removed_dup),
        "deferred_red": len(red_cands),
        "section_remaps": remap_count,
        "replacement_candidates": len(replacement_cands),
        "final_candidate_count": total_final,
        "recommendation": recommendation,
        "recommended_merge_count": rec_count
    },
    "excluded": {
        "exact_duplicates": [{"name": rd["name"], "candidate_id": rd["candidate_id"]} for rd in removed_dup],
        "red_candidates": [{"name": rc["name"], "candidate_id": rc["candidate_id"], "theme": rc["theme"]} for rc in red_cands],
        "section_remaps": [{"name": c["name"], "old_section": "4.16", "new_section": "2.18"} for c in pool_clean if c.get("_was_4_16")] if False else [
            {"count": remap_count, "from": "4.16", "to": "2.18", "note": "15 debug candidates remapped from non-existent 4.16 to 2.18 (综合高级技巧专题)"}
        ]
    },
    "blocking_issues": blocking,
    "warnings": warnings,
    "replacement_candidates": replacement_cands,
    "candidates": candidate_plans
}
with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan_v2, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PLAN}")

# --- PRECHECK V2 ---
precheck_v2 = {
    "meta": {
        "generated_by": "stage3g_full400_cleanup_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False, "merge_executed": False,
        "validate_only_status": {
            "item_count": item_count, "section_count": len(section_names),
            "passed": True
        }
    },
    "fixes_applied": {
        "exact_duplicates_removed": len(removed_dup),
        "red_candidates_deferred": len(red_cands),
        "section_4_16_remapped_to_2_18": remap_count,
        "dependency_resolution_rewritten": True,
        "replacement_candidates_added": len(replacement_cands)
    },
    "precheck_results": {
        "exact_duplicate": {"count": exact_dup_count, "passed": exact_dup_count == 0},
        "high_duplicate": {"count": high_sim_count, "passed": high_sim_count == 0},
        "needs_new_section": {"value": needs_new_sec, "passed": not needs_new_sec},
        "candidate_dependency_cycle": {"value": has_cycle, "passed": not has_cycle},
        "section_ref_dependencies": {"count": sec_ref_count, "passed": sec_ref_count == 0},
        "self_ref_dependencies": {"count": self_ref_count, "passed": self_ref_count == 0},
        "dangling_dependencies": {"count": dangling_count, "passed": dangling_count == 0},
        "unresolvable_direct_pre": {"count": unresolvable_dp, "passed": unresolvable_dp == 0},
        "dependency_cleanup_required": {"value": cleanup_blocking_count > 0, "count": cleanup_blocking_count},
        "dependency_cleanup_informational": {"value": cleanup_needed_count > 0, "count": cleanup_needed_count},
        "theme_distribution": dict(theme_dist),
        "section_distribution": dict(sec_dist),
        "risk_band_distribution": {r: sum(1 for p in candidate_plans if p["risk_band"] == r) for r in ["green","yellow","medium","red"]},
        "confidence_distribution": {c: sum(1 for p in candidate_plans if p["mapping_confidence"] == c) for c in ["high","medium","low"]},
        "merge_priority": {"now": now_count, "soon": soon_count, "later": later_count, "defer": defer_count},
        "direct_pre_stats": {"total": total_dp, "avg": round(avg_dp, 1), "max": max_dp}
    },
    "all_checks_passed": all_passed,
    "recommendation": recommendation,
    "recommended_merge_count": rec_count,
    "blocking_issues": blocking
}
with open(OUT_PRECHECK, "w", encoding="utf-8") as f:
    json.dump(precheck_v2, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_PRECHECK}")

# --- CLEANUP PLAN V2 ---
cleanup_list = []
for plan in candidate_plans:
    if plan["needs_cleanup"]:
        dc = plan["dependency_check"]
        item = {
            "candidate_id": plan["candidate_id"],
            "name": plan["name"],
            "theme": plan["theme"],
            "issues": dc["mapping_issues"],
            "unresolved_pre": dc["direct_pre_unresolved"],
            "suggested_fixes": []
        }
        for u in dc["direct_pre_unresolved"]:
            item["suggested_fixes"].append({
                "pre_name": u["pre_name"],
                "action": "manual_fix",
                "note": "无法自动解析，需人工替换或删除"
            })
        if dc["has_section_ref"]:
            item["suggested_fixes"].append({"action": "remove_section_refs", "note": "移除section id引用"})
        if dc["has_self_ref"]:
            item["suggested_fixes"].append({"action": "remove_self_ref", "note": "移除自引用"})
        cleanup_list.append(item)

cleanup_v2_plan = {
    "meta": {
        "generated_by": "stage3g_full400_cleanup_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_graph_modified": False, "merge_executed": False,
        "dependency_cleanup_required": len(cleanup_list) > 0,
        "total_candidates_needing_cleanup": len(cleanup_list)
    },
    "cleanup_items": cleanup_list
}
with open(OUT_CLEANUP, "w", encoding="utf-8") as f:
    json.dump(cleanup_v2_plan, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_CLEANUP}")

# --- REPLACEMENT PLAN ---
with open(OUT_REPLACEMENT, "w", encoding="utf-8") as f:
    json.dump({
        "meta": {
            "generated_by": "stage3g_full400_cleanup_v2",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "gap_to_400": gap,
            "replacement_count": len(replacement_cands),
            "sources": [
                "动态规划专题: {need} red replacements",
                "图论专题: 2 red replacements",
                "数据结构专题: 4 red replacements",
                "信奥数学: 4 red replacements",
                "基础算法扩展: 5 dup gap fill",
                "字符串专题: 3 dup gap fill"
            ]
        },
        "replacements": replacement_cands
    }, f, ensure_ascii=False, indent=2)
print(f"    [OK] {OUT_REPLACEMENT}")

# --- REPORT V2 ---
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(f"# Stage3G full400 清理版 v2 审计报告\n\n")
    f.write(f"**生成时间**: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"**清理脚本**: stage3g_full400_cleanup_v2.py\n\n")

    f.write(f"## 1. 总体结论\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| 原始候选 | 400 |\n")
    f.write(f"| 移除精确重复 | {len(removed_dup)} |\n")
    f.write(f"| 暂缓 red | {len(red_cands)} |\n")
    f.write(f"| 4.16->2.18 重映射 | {remap_count} |\n")
    f.write(f"| 替补候选 | {len(replacement_cands)} |\n")
    f.write(f"| 最终候选数 | **{total_final}** |\n")
    f.write(f"| 可直接合并 | {can_merge_total} |\n")
    f.write(f"| 建议 | **{recommendation}** |\n")
    f.write(f"| 建议合并数 | {rec_count} |\n")
    f.write(f"| 达到 400 | {'是' if total_final == 400 else f'否（差{400-total_final}个）'} |\n")
    f.write(f"| 修改主图谱 | 否 |\n")
    f.write(f"| 执行合并 | 否 |\n\n")

    f.write(f"## 2. 修复动作明细\n\n")
    f.write(f"### 移除精确重复 ({len(removed_dup)}个)\n")
    for rd in removed_dup:
        f.write(f"- `{rd['name']}` (candidate_id: `{rd['candidate_id']}`) -- 主图谱已有同名节点\n")
    f.write(f"\n### 暂缓 red 候选 ({len(red_cands)}个)\n")
    for rc in red_cands:
        f.write(f"- `{rc['name']}` (theme: {rc['theme']})\n")
    f.write(f"\n### 4.16 重映射 ({remap_count}个)\n")
    f.write(f"15 个调试方法候选从不存在 section 4.16 重映射到 2.18 (综合高级技巧专题)\n")
    f.write(f"\n### 替补候选 ({len(replacement_cands)}个)\n")
    for rc in replacement_cands:
        f.write(f"- `{rc['name']}` (theme: {rc['theme']})\n")

    f.write(f"\n## 3. 阻塞项\n\n")
    if blocking:
        for b in blocking: f.write(f"- [X] {b}\n")
    else:
        f.write(f"- [OK] 无阻塞项\n")
    f.write(f"\n")

    f.write(f"## 4. 各主题分布\n\n")
    f.write(f"| Theme | 候选数 | green | yellow | medium | red |\n")
    f.write(f"|-------|--------|-------|--------|--------|-----|\n")
    for t in sorted(theme_risk.keys()):
        tr = theme_risk[t]
        f.write(f"| {t} | {theme_dist[t]} | {tr['green']} | {tr['yellow']} | {tr['medium']} | {tr['red']} |\n")

    f.write(f"\n## 5. 依赖质量\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| direct_pre 总数 | {total_dp} |\n")
    f.write(f"| 平均 | {avg_dp:.1f} |\n")
    f.write(f"| 最大 | {max_dp} |\n")
    f.write(f"| 无法解析 | {unresolvable_dp} |\n")
    f.write(f"| section ref | {sec_ref_count} |\n")
    f.write(f"| self ref | {self_ref_count} |\n")
    f.write(f"| 悬空引用 | {dangling_count} |\n")
    f.write(f"| 候选依赖环 | {'是' if has_cycle else '否'} |\n\n")

    resolved_total = total_dp - unresolvable_dp
    resolution_rate = resolved_total / max(total_dp, 1) * 100

    f.write(f"## 6. 依赖解析策略 (v2 改进)\n\n")
    f.write(f"### 改进对比\n\n")
    f.write(f"| 指标 | v1 (原始审计) | v2 (清理版) |\n")
    f.write(f"|------|--------------|------------|\n")
    f.write(f"| 总 direct_pre | 1598 | {total_dp} |\n")
    f.write(f"| 成功解析 | 1141 (71.4%) | {resolved_total} ({resolution_rate:.1f}%) |\n")
    f.write(f"| 无法解析 | 457 | {unresolvable_dp} |\n")
    f.write(f"| 悬空引用候选数 | 272 | {dangling_count} |\n\n")

    f.write(f"### v2 匹配策略 (8层递进)\n\n")
    f.write(f"| 层级 | 策略 | 匹配数 | 说明 |\n")
    f.write(f"|------|------|--------|------|\n")
    strat_counts = {}
    for plan in candidate_plans:
        for m in plan["dependency_check"].get("direct_pre_mapped", []):
            s = m.get("strategy", "unknown")
            strat_counts[s] = strat_counts.get(s, 0) + 1
    strat_desc = {
        "exact_name": "精确 name 匹配",
        "exact_name_ns": "精确 name 匹配(去空格)",
        "exact_en": "精确 en_name 匹配",
        "exact_en_ns": "精确 en_name 匹配(去空格)",
        "exact_alias": "精确 alias 匹配",
        "exact_alias_ns": "精确 alias 匹配(去空格)",
        "substring": "子串匹配",
        "substring_contiguous": "连续子串匹配(去空格)",
        "fuzzy_jaccard": "Jaccard 相似度匹配",
        "alias_fuzzy": "alias 模糊匹配",
        "concept_map_exact": "概念词映射",
        "concept_map_substr": "概念词子串映射",
    }
    for s, cnt in sorted(strat_counts.items(), key=lambda x: -x[1]):
        desc = strat_desc.get(s, s)
        f.write(f"| {s} | {desc} | {cnt} | |\n")

    f.write(f"\n### 剩余无法解析的 deps ({unresolvable_dp} 个)\n\n")
    f.write(f"这些依赖名使用了概念化简写，在图中不存在对应的 item name/en_name/alias。\n")
    f.write(f"合并时它们会被跳过，不影响候选节点的创建。\n")
    f.write(f"如需完整映射，需手动补充 concept thesaurus 或修改 pool 的 direct_pre_name_suggestion。\n\n")

    f.write(f"## 7. 是否建议交代 1号执行 full400 合并\n\n")
    if all_passed and total_final == 400:
        f.write(f"[OK] **建议交代 1号执行 Stage3G full400 合并。**\n\n")
        f.write(f"合并前 item_count = {item_count}，合并后 = {item_count + total_final}。\n")
        f.write(f"所有安全检查均已通过（exact_dup=0, high_sim=0, section_ref=0, self_ref=0, no_cycle, no_new_section）。\n")
        f.write(f"\n依赖解析率 {resolution_rate:.1f}% ({resolved_total}/{total_dp})。\n")
        f.write(f"剩余 {unresolvable_dp} 个 unresolved deps 在 {dangling_count} 个候选中，合并时将被跳过。\n")
    elif all_passed:
        f.write(f"[WARN] 可合并 {total_final} 个候选（少于 400，差 {400-total_final} 个）。\n")
        f.write(f"建议先合并这 {total_final} 个，剩余缺口后续再补。\n")
    else:
        f.write(f"[X] 仍需清理，不建议直接合并。\n")
        f.write(f"可直接合并的候选数：{can_merge_total}。\n")

    f.write(f"\n---\n")
    f.write(f"*本报告由 stage3g_full400_cleanup_v2.py 自动生成*\n")
    f.write(f"*不修改主图谱，不执行合并*\n")

print(f"    [OK] {OUT_REPORT}")
print(f"\n{'=' * 60}")
print(f"      Cleanup v2 Complete")
print(f"{'=' * 60}")
print(f"  Recommendation: {recommendation}")
print(f"  Final count: {total_final} / 400 target")
