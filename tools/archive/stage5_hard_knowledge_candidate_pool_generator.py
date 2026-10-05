#!/usr/bin/env python3
"""Stage5 v2: Expand candidate pool to ~1200 with batch generation."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"

with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)

items_by_id = {}
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
            n = item.get("name", "").lower().strip().replace(" ", "")
            en = item.get("en_name", "").lower().strip().replace(" ", "")
            if n: name_lower_set.add(n)
            if en: en_lower_set.add(en)
            for a in item.get("aliases", []):
                alias_lower_set.add(a.lower().strip().replace(" ", ""))
            for ga in item.get("global_aliases", []):
                alias_lower_set.add(ga.lower().strip().replace(" ", ""))
            sec_counts[sid] += 1

item_count = len(items_by_id)
print(f"  Graph: {item_count} items")

def sn(sid):
    return sections.get(sid, f"UNKNOWN_{sid}")

def tokenize(s):
    return set(re.sub(r'[^a-z0-9\u4e00-\u9fff]', ' ', s.lower()).split())

def jaccard(a, b):
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb: return 0
    return len(ta & tb) / len(ta | tb)

def is_dup(name, en_name):
    nl = name.lower().strip().replace(" ", "")
    if nl in name_lower_set: return True
    enl = en_name.lower().strip().replace(" ", "")
    if enl and enl in name_lower_set: return True
    if enl and enl in en_lower_set: return True
    # Quick similarity check against all items
    for iid, item in items_by_id.items():
        sim = max(jaccard(name, item.get("name", "")), jaccard(en_name, item.get("en_name", "")))
        if sim >= 0.85: return True
    return False

# ============================================================
# BATCH CANDIDATE DEFINITIONS
# ============================================================
# Format: (prefix, en_prefix, target_section, items_list)
# Each item: (name_suffix, en_suffix, candidate_type, risk, conf, direct_pre, reason)

BATCHES = []

# --- 1.1 Greedy Models (expand to ~75) ---
BATCHES.append(("贪心", "greedy", "2.6", [
    ("：双机调度问题", "_two_machine_scheduling", "modeling_pattern", "green", "high", ["贪心", "排序"], "双机流水线调度Johnson算法"),
    ("：多机调度近似", "_multiprocessor_scheduling", "modeling_pattern", "yellow", "medium", ["贪心", "调度"], "多机调度的贪心近似算法"),
    ("：带权区间调度", "_weighted_interval_scheduling", "modeling_pattern", "green", "high", ["贪心", "DP"], "带权区间调度的DP+贪心解法"),
    ("：贪心+堆维护", "_greedy_with_heap", "implementation_variant", "green", "high", ["贪心", "堆"], "贪心过程中用堆维护候选集"),
    ("：贪心+并查集", "_greedy_with_union_find", "implementation_variant", "green", "high", ["贪心", "并查集"], "贪心+并查集的典型模式(如Kruskal)"),
    ("：最小生成树应用(Kruskal)", "_kruskal_applications", "application_case", "green", "high", ["最小生成树", "贪心", "并查集"], "Kruskal算法在各类MST问题中的应用"),
    ("：Prim算法应用", "_prim_applications", "application_case", "green", "high", ["最小生成树", "贪心", "堆"], "Prim算法在稠密图MST中的应用"),
    ("：次小生成树", "_second_mst", "application_case", "yellow", "medium", ["最小生成树"], "严格次小生成树的求法"),
    ("：最小瓶颈生成树", "_minimum_bottleneck_st", "application_case", "green", "high", ["最小生成树"], "最小瓶颈生成树=MST的性质"),
    ("：贪心正确性验证方法", "_greedy_correctness", "theorem_or_property", "green", "high", ["贪心"], "贪心正确性验证：交换论证/归纳法/反例"),
    ("：贪心与DP的边界", "_greedy_vs_dp_boundary", "bridge_concept", "green", "high", ["贪心", "DP"], "何时贪心最优、何时必须DP的判断"),
    ("：贪心构造法", "_greedy_construction", "modeling_pattern", "yellow", "medium", ["贪心", "构造"], "贪心策略指导的构造方法"),
    ("：栈贪心", "_stack_greedy", "implementation_variant", "green", "high", ["贪心", "栈"], "利用栈维护贪心选择的模式"),
    ("：双指针贪心", "_two_pointer_greedy", "implementation_variant", "green", "high", ["贪心", "双指针"], "双指针配合贪心的典型模式"),
]))

# --- 1.2 Construction (expand 2.20 to ~25) ---
BATCHES.append(("构造", "constructive", "2.20", [
    ("：数列构造", "_sequence", "modeling_pattern", "yellow", "medium", ["构造", "数列"], "满足特定条件的数列构造"),
    ("：图构造进阶", "_graph_advanced", "modeling_pattern", "yellow", "medium", ["构造", "图论"], "图论中的高级构造性问题"),
    ("：博弈构造", "_game_construction", "modeling_pattern", "yellow", "medium", ["构造", "博弈论"], "博弈中的构造性策略"),
    ("：贪心构造策略", "_greedy_strategy", "modeling_pattern", "yellow", "medium", ["贪心", "构造"], "贪心思想指导的构造方法"),
    ("：构造题常见技巧", "_common_techniques", "bridge_concept", "green", "high", ["构造"], "构造题的通用技巧与思路"),
    ("：构造性证明", "_constructive_proof", "theorem_or_property", "yellow", "medium", ["构造", "数学"], "构造性证明方法"),
    ("：反例构造", "_counterexample", "application_case", "green", "high", ["构造"], "构造反例的方法与技巧"),
]))

# --- 1.3 Interactive (expand 2.20 to ~15) ---
BATCHES.append(("交互", "interactive", "2.20", [
    ("：查询优化策略", "_query_optimization", "modeling_pattern", "yellow", "medium", ["交互"], "交互题中的查询次数优化"),
    ("：确定性问题交互", "_deterministic", "modeling_pattern", "green", "high", ["交互", "二分"], "确定性问题交互的二分策略"),
    ("：随机化交互策略", "_randomized", "modeling_pattern", "yellow", "medium", ["交互", "随机化"], "随机化在交互中的应用"),
    ("：IO交互实现", "_io_implementation", "implementation_variant", "green", "high", ["交互"], "交互题的I/O实现细节"),
    ("：评委程序理解", "_understanding_judge", "bridge_concept", "green", "high", ["交互"], "理解交互题中评委程序的逻辑"),
]))

# --- 1.4 Search (expand 2.7 to ~25) ---
BATCHES.append(("搜索", "search", "2.7", [
    ("进阶：A*估价函数设计", "_a_star_heuristic_design", "implementation_variant", "yellow", "medium", ["A*搜索"], "A*算法中估价函数的设计原则"),
    ("进阶：搜索+位运算状态", "_bitmask_state", "implementation_variant", "green", "high", ["搜索", "位运算"], "用位掩码压缩搜索状态"),
    ("进阶：记忆化搜索优化", "_memoization_optimization", "implementation_variant", "green", "high", ["DFS", "记忆化"], "记忆化搜索的哈希优化与状态编码"),
    ("进阶：Dancing Links X实现", "_dlx_implementation", "implementation_variant", "yellow", "medium", ["Dancing Links"], "DLX算法的实现细节"),
    ("进阶：数独求解器", "_sudoku_solver", "application_case", "green", "high", ["搜索", "剪枝"], "数独求解：搜索+剪枝的综合应用"),
    ("进阶：N皇后问题", "_n_queens", "application_case", "green", "high", ["搜索", "位运算"], "N皇后问题的位运算加速搜索"),
    ("进阶：搜索顺序优化", "_search_ordering", "implementation_variant", "green", "high", ["搜索", "剪枝"], "搜索顺序对效率的影响与优化"),
    ("进阶：分支限界法", "_branch_and_bound", "core_concept", "yellow", "medium", ["搜索", "剪枝"], "分支限界法：系统化的最优性剪枝"),
]))

# --- 1.5 DP Variants (expand to ~80) ---
BATCHES.append(("DP", "dp", "2.8", [
    ("变体：WQS二分(凸优化DP)", "_wqs_binary_search", "core_concept", "medium", "low", ["DP优化", "二分"], "WQS二分：凸/凹DP的费用附加"),
    ("变体：自动机DP进阶", "_automaton_dp_advanced", "implementation_variant", "yellow", "medium", ["自动机DP"], "AC自动机/PAM上的DP进阶"),
    ("变体：轮廓线DP", "_contour_dp", "core_concept", "yellow", "medium", ["状压DP", "轮廓线"], "轮廓线DP：逐格转移的状态压缩"),
    ("变体：数位DP常见模型", "_digit_dp_models", "modeling_pattern", "green", "high", ["数位DP"], "数位DP的常见模型总结"),
    ("变体：树形背包", "_tree_knapsack", "modeling_pattern", "yellow", "medium", ["树形DP", "背包DP"], "树上背包问题与DFS序优化"),
    ("变体：环形区间DP", "_circular_interval_dp", "implementation_variant", "yellow", "medium", ["区间DP", "环形"], "环形区间DP的断链策略"),
    ("变体：高维前缀和优化DP", "_sos_dp", "implementation_variant", "yellow", "medium", ["状压DP", "前缀和"], "子集DP/SOS DP高维前缀和优化"),
    ("变体：连通性DP", "_connectivity_dp", "core_concept", "medium", "low", ["插头DP", "轮廓线"], "连通性状态压缩DP"),
    ("变体：单调队列优化DP", "_monotone_queue_dp", "implementation_variant", "green", "high", ["DP优化", "单调队列"], "单调队列优化1D/1D DP转移"),
    ("变体：矩阵快速幂优化DP", "_matrix_expo_dp", "implementation_variant", "green", "high", ["DP优化", "矩阵"], "矩阵快速幂加速线性递推DP"),
    ("变体：CDQ分治优化DP", "_cdq_dp_opt", "implementation_variant", "yellow", "medium", ["DP优化", "CDQ分治"], "CDQ分治优化多维DP"),
    ("变体：线段树分治优化DP", "_segtree_dc_dp", "implementation_variant", "yellow", "medium", ["DP优化", "线段树分治"], "线段树分治优化带删边的DP"),
    ("变体：分块优化DP", "_sqrt_dp", "implementation_variant", "yellow", "medium", ["DP优化", "分块"], "分块优化DP转移的根号技巧"),
]))

# --- 1.6 Graph Bridge (expand to ~40) ---
BATCHES.append(("图论", "graph", "2.9", [
    ("衔接：无向图双连通分量", "_biconnected_component", "core_concept", "green", "high", ["割边", "割点"], "双连通分量的Tarjan算法"),
    ("衔接：有向图的强连通性应用", "_scc_applications", "application_case", "green", "high", ["强连通分量"], "SCC缩图后的DAG应用"),
    ("衔接：缩点后DP", "_scc_dp", "modeling_pattern", "green", "high", ["强连通分量", "DP"], "SCC缩点后在DAG上做DP"),
    ("衔接：基环树", "_functional_graph", "core_concept", "green", "high", ["图", "环"], "基环树(外向树/内向树)的性质与处理"),
    ("衔接：基环树DP", "_functional_graph_dp", "modeling_pattern", "yellow", "medium", ["基环树", "DP"], "基环树上的DP问题"),
    ("衔接：绝对中心", "_absolute_center", "application_case", "yellow", "medium", ["最短路", "图论"], "图的绝对中心与最小半径"),
    ("衔接：图论与贪心结合", "_graph_greedy", "bridge_concept", "green", "high", ["图论", "贪心"], "图论问题中的贪心策略"),
    ("衔接：图论与分治结合", "_graph_divide_conquer", "bridge_concept", "yellow", "medium", ["图论", "分治"], "图论中的分治策略"),
    ("衔接：最短路变体总结", "_shortest_path_variants", "bridge_concept", "green", "high", ["最短路"], "最短路的各种变体与应用场景"),
]))

# --- 1.7 String (expand to ~25) ---
BATCHES.append(("字符串", "string", "2.10", [
    ("进阶：后缀自动机应用", "_sam_applications", "application_case", "yellow", "medium", ["后缀自动机"], "SAM在子串计数/出现次数中的应用"),
    ("进阶：广义后缀自动机", "_generalized_sam", "core_concept", "medium", "low", ["后缀自动机"], "多串广义后缀自动机"),
    ("进阶：AC自动机进阶应用", "_aho_corasick_advanced", "application_case", "yellow", "medium", ["AC自动机"], "AC自动机的多模式匹配进阶"),
    ("进阶：字符串匹配算法对比", "_string_matching_comparison", "bridge_concept", "green", "high", ["字符串匹配"], "KMP/Z/后缀数组等匹配方法对比"),
    ("进阶：周期与border理论", "_period_border_theory", "theorem_or_property", "yellow", "medium", ["字符串"], "字符串周期性与border理论"),
    ("进阶：后缀数组与LCP", "_sa_lcp_applications", "application_case", "green", "high", ["后缀数组", "LCP"], "LCP数组在子串问题中的应用"),
    ("进阶：字符串哈希应用集", "_hash_applications", "application_case", "green", "high", ["字符串哈希"], "字符串哈希的典型应用场景总结"),
]))

# --- 1.8 Root/Sqrt Algorithms (expand to ~30) ---
BATCHES.append(("根号", "sqrt", "2.4", [
    ("算法：值域分块", "_value_blocking", "implementation_variant", "yellow", "medium", ["分块"], "值域分块：按值域区间维护信息"),
    ("算法：树上莫队", "_tree_mo_algorithm", "core_concept", "yellow", "medium", ["莫队", "树"], "树上路径的莫队算法(欧拉序)"),
    ("算法：带修莫队", "_mo_with_update", "core_concept", "yellow", "medium", ["莫队"], "支持修改操作的莫队算法"),
    ("算法：回滚莫队", "_rollback_mo", "implementation_variant", "yellow", "medium", ["莫队"], "回滚莫队：只支持add/只支持del"),
    ("算法：分块区间加区间和", "_block_range_add_sum", "implementation_variant", "green", "high", ["分块"], "分块实现区间加法与区间求和"),
    ("算法：分块区间众数", "_block_mode_query", "implementation_variant", "yellow", "medium", ["分块"], "分块实现区间众数查询"),
    ("算法：根号分治(按大小分类)", "_sqrt_classification_by_size", "modeling_pattern", "yellow", "medium", ["根号分治"], "度数/出现次数按根号分两类处理"),
    ("算法：根号预处理", "_sqrt_preprocessing", "implementation_variant", "green", "high", ["分块", "预处理"], "根号级预处理加速查询"),
]))

# --- 1.9 Data Structure Extensions (expand to ~40) ---
BATCHES.append(("数据结构", "ds", "3.13", [
    ("衔接：动态开点线段树", "_dynamic_segtree", "implementation_variant", "green", "high", ["线段树"], "动态开点线段树：值域大时按需建节点"),
    ("衔接：权值线段树", "_weight_segtree", "core_concept", "green", "high", ["线段树"], "权值线段树：维护值域信息"),
    ("衔接：线段树合并", "_segtree_merge", "implementation_variant", "yellow", "medium", ["线段树"], "线段树合并：树上信息合并"),
    ("衔接：线段树分裂", "_segtree_split", "implementation_variant", "yellow", "medium", ["线段树"], "线段树分裂操作"),
    ("衔接：扫描线与线段树", "_scanline_segtree", "modeling_pattern", "green", "high", ["线段树", "扫描线"], "扫描线+线段树求矩形面积并"),
    ("衔接：树状数组进阶应用", "_bit_advanced", "application_case", "green", "high", ["树状数组"], "树状数组的高维/差分/前缀max应用"),
    ("衔接：平衡树进阶应用", "_balanced_tree_advanced", "application_case", "yellow", "medium", ["平衡树"], "Splay/Treap的进阶应用场景"),
    ("衔接：分块与莫队总结", "_block_mo_summary", "bridge_concept", "green", "high", ["分块", "莫队"], "分块与莫队的选择指南"),
    ("衔接：可持久化线段树进阶", "_persistent_segtree_advanced", "implementation_variant", "yellow", "medium", ["可持久化线段树"], "可持久化线段树的进阶应用"),
    ("衔接：字典树进阶", "_trie_advanced", "application_case", "green", "high", ["Trie"], "字典树的进阶：01-Trie/可持久化Trie"),
]))

# --- 1.10 Bridge/Comparison Nodes (expand to ~30) ---
BATCHES.append(("衔接", "bridge", "2.18", [
    ("：从暴力到优化的思维链", "_brute_to_optimized_chain", "bridge_concept", "green", "high", ["暴力", "优化"], "暴力→二分→数据结构的典型优化路径"),
    ("：从O(n^2)到O(nlogn)", "_n2_to_nlogn", "bridge_concept", "green", "high", ["复杂度"], "O(n^2)到O(nlogn)的常见优化手法"),
    ("：常见问题模型识别", "_problem_model_identification", "bridge_concept", "green", "high", [], "从题目条件识别问题模型的思维方法"),
    ("：多解法对比思维", "_multi_solution_comparison", "bridge_concept", "green", "high", [], "一题多解的对比分析方法"),
    ("：算法选择决策树", "_algorithm_decision_tree", "bridge_concept", "green", "high", [], "各类问题的算法选择决策树"),
    ("：竞赛常见陷阱", "_common_traps", "bridge_concept", "green", "high", [], "竞赛编程中的常见陷阱总结"),
    ("：特殊性质发现方法", "_special_property_discovery", "bridge_concept", "green", "high", [], "发现题目特殊性质的方法论"),
    ("：对拍与正确性验证", "_stress_testing", "bridge_concept", "green", "high", ["对拍"], "对拍验证算法正确性的工程方法"),
]))

# ============================================================
# MATH BATCHES
# ============================================================

MATH_BATCHES = []

# --- 2.1 Number Theory (expand to ~40) ---
MATH_BATCHES.append(("数论", "nt", "4.1", [
    ("：扩展欧拉定理", "_euler_theorem_extended", "theorem_or_property", "yellow", "medium", ["欧拉函数", "模运算"], "扩展欧拉定理处理大指数取模"),
    ("：费马小定理应用", "_fermat_little_app", "theorem_or_property", "green", "high", ["模运算", "质数"], "费马小定理在逆元/加密中的应用"),
    ("：Wilson定理", "_wilson_theorem", "theorem_or_property", "green", "high", ["数论", "阶乘"], "Wilson定理与阶乘取模"),
    ("：约数函数求和", "_divisor_function_sum", "application_case", "yellow", "medium", ["数论函数", "筛法"], "约数个数/约数和的前缀和计算"),
    ("：素数分布与估计", "_prime_distribution", "theorem_or_property", "green", "high", ["质数", "数论"], "素数定理与素数计数"),
    ("：分解质因数进阶", "_prime_factorization_advanced", "implementation_variant", "green", "high", ["质数", "因数分解"], "大数分解的优化方法"),
    ("：RSA加密与数论", "_rsa_cryptography", "application_case", "yellow", "medium", ["质数", "模运算"], "RSA加密背后的数论原理"),
    ("：同余方程组", "_congruence_systems", "core_concept", "yellow", "medium", ["CRT", "模运算"], "同余方程组的解法"),
    ("：逆元的各种求法", "_inverse_methods", "implementation_variant", "green", "high", ["模运算", "逆元"], "扩展GCD/费马/递推求逆元"),
    ("：阶与原根判定", "_order_primitive_root", "core_concept", "yellow", "medium", ["原根", "数论"], "模p下的阶计算与原根判定方法"),
]))

# --- 2.2 Combinatorics (expand to ~30) ---
MATH_BATCHES.append(("组合", "comb", "4.3", [
    ("：组合数取模方法总结", "_comb_mod_methods", "bridge_concept", "green", "high", ["组合数", "模运算"], "组合数取模的各种方法对比"),
    ("：容斥原理经典应用", "_inclusion_exclusion_classic", "application_case", "green", "high", ["容斥"], "容斥原理的经典应用模型"),
    ("：多重集组合", "_multiset_combination", "modeling_pattern", "green", "high", ["组合", "容斥"], "多重集的组合与排列"),
    ("：斯特林数应用", "_stirling_applications", "application_case", "yellow", "medium", ["斯特林数"], "斯特林数在计数中的应用"),
    ("：排列的循环分解", "_permutation_cycle_decomposition", "theorem_or_property", "green", "high", ["排列", "置换群"], "排列的循环分解与性质"),
    ("：抽屉原理", "_pigeonhole_principle", "theorem_or_property", "green", "high", ["计数"], "抽屉原理在竞赛中的应用"),
    ("：鸽巢原理进阶", "_pigeonhole_advanced", "application_case", "green", "high", ["抽屉原理"], "鸽巢原理的进阶应用技巧"),
    ("：母函数应用", "_generating_function_apps", "application_case", "yellow", "medium", ["生成函数"], "生成函数在竞赛计数中的应用"),
]))

# --- 2.3 Probability (expand to ~25) ---
MATH_BATCHES.append(("概率", "prob", "4.6", [
    ("：全概率公式", "_law_total_probability", "theorem_or_property", "green", "high", ["概率"], "全概率公式在算法中的应用"),
    ("：Bayes公式", "_bayes_theorem", "theorem_or_property", "green", "high", ["概率"], "贝叶斯公式与后验概率"),
    ("：期望DP典型模型", "_expectation_dp_models", "modeling_pattern", "green", "high", ["期望", "DP"], "期望DP的典型建模方法"),
    ("：概率不等式", "_probability_inequalities", "theorem_or_property", "yellow", "medium", ["概率"], "Markov/Chebyshev/Chernoff不等式"),
    ("：随机变量与分布", "_random_variables", "core_concept", "green", "high", ["概率"], "离散随机变量的期望与方差"),
    ("：大数定律", "_law_large_numbers", "theorem_or_property", "yellow", "medium", ["概率", "随机化"], "大数定律在随机化算法中的保证"),
]))

# --- 2.4 Game Theory (expand to ~20) ---
MATH_BATCHES.append(("博弈", "game", "4.5", [
    ("：阶梯Nim", "_staircase_nim", "application_case", "green", "high", ["Nim游戏"], "阶梯Nim：奇数位上的Nim"),
    ("：反博弈", "_miserable_game", "application_case", "yellow", "medium", ["博弈论"], "反博弈(最后一个操作者输)"),
    ("：组合博弈的合并", "_composite_game_sum", "theorem_or_property", "yellow", "medium", ["SG函数", "Nim"], "组合博弈的Sprague-Grundy合并"),
    ("：删边游戏", "_edge_deletion_game", "application_case", "yellow", "medium", ["博弈论", "图论"], "图上的删边博弈"),
    ("：博弈与搜索结合", "_game_search", "modeling_pattern", "green", "high", ["博弈论", "搜索"], "博弈状态图搜索与Alpha-Beta剪枝"),
]))

# --- 2.5 Geometry (expand to ~20) ---
MATH_BATCHES.append(("几何", "geo", "4.7", [
    ("：点线面关系判定", "_point_line_plane", "core_concept", "green", "high", ["几何"], "计算几何中点线面关系的判定方法"),
    ("：多边形面积", "_polygon_area", "core_concept", "green", "high", ["几何", "叉积"], "多边形面积的叉积计算"),
    ("：点在多边形内判定", "_point_in_polygon", "core_concept", "green", "high", ["几何"], "射线法/转角法判定点在多边形内"),
    ("：最近点对", "_closest_pair", "application_case", "green", "high", ["分治", "几何"], "平面最近点对的分治算法"),
    ("：圆的几何计算", "_circle_geometry", "core_concept", "green", "high", ["几何"], "圆的交/切/包含等计算"),
    ("：向量运算基础", "_vector_operations", "core_concept", "green", "high", ["几何", "向量"], "向量的点积/叉积及其几何意义"),
    ("：线段相交判定", "_segment_intersection", "implementation_variant", "green", "high", ["几何", "叉积"], "线段相交的快速判定"),
]))

# --- 2.6 Linear Algebra (expand to ~15) ---
MATH_BATCHES.append(("线代", "linalg", "2.17", [
    ("：矩阵运算基础", "_matrix_operations", "core_concept", "green", "high", ["矩阵"], "矩阵加法/乘法/转置的基础运算"),
    ("：高斯消元应用集", "_gaussian_applications", "application_case", "green", "high", ["高斯消元"], "高斯消元在方程组/期望/异或中的应用"),
    ("：矩阵的秩", "_matrix_rank", "theorem_or_property", "green", "high", ["矩阵", "线性代数"], "矩阵的秩及其应用"),
    ("：逆矩阵", "_inverse_matrix", "core_concept", "yellow", "medium", ["矩阵"], "逆矩阵的求法与应用"),
]))

# --- 2.7 Discrete Math (expand to ~15) ---
MATH_BATCHES.append(("离散", "discrete", "4.4", [
    ("：图着色与色数", "_graph_coloring", "core_concept", "yellow", "medium", ["图论", "组合"], "图的着色问题与色数"),
    ("：Ramsey理论初步", "_ramsey_theory", "theorem_or_property", "medium", "low", ["组合", "图论"], "Ramsey数与Ramsey理论入门"),
    ("：置换群与对称群", "_permutation_group", "core_concept", "yellow", "medium", ["群论", "排列"], "置换群的基本概念"),
    ("：容斥与反演总结", "_inclusion_exclusion_inversion_summary", "bridge_concept", "yellow", "medium", ["容斥", "反演"], "容斥与反演方法的统一框架"),
]))

# --- 2.8 Math Bridge (expand to ~15) ---
MATH_BATCHES.append(("数学桥梁", "math_bridge", "4.0", [
    ("：竞赛中常用的不等式", "_competition_inequalities", "theorem_or_property", "green", "high", ["数学"], "竞赛中常用的放缩/AM-GM/Cauchy不等式"),
    ("：竞赛中的数列求和技巧", "_sequence_sum_techniques", "bridge_concept", "green", "high", ["数列", "求和"], "数列求和的常用技巧与方法"),
    ("：构造反例的数学思维", "_counterexample_construction", "bridge_concept", "green", "high", ["构造", "数学"], "数学中构造反例的思维方法"),
    ("：特殊值法", "_special_values_method", "bridge_concept", "green", "high", ["数学"], "取特殊值验证/猜想的技巧"),
    ("：对称性与不变量", "_symmetry_invariants", "theorem_or_property", "green", "high", ["数学"], "对称性与不变量在竞赛中的应用"),
    ("：常见数学公式速查", "_math_formula_reference", "bridge_concept", "green", "high", ["数学"], "竞赛中常用数学公式速查表"),
]))

# ============================================================
# GENERATE ALL CANDIDATES
# ============================================================
print(f"\n  Generating candidates from batches...")

candidates = []
existing_names = set()
cid = 0

for batch in BATCHES:
    prefix, en_prefix, sec, items_list = batch
    for item_def in items_list:
        name = prefix + item_def[0]
        en_name = en_prefix + item_def[1]
        nl = name.lower().strip().replace(" ", "")
        if nl in existing_names or is_dup(name, en_name):
            continue
        existing_names.add(nl)
        cid += 1
        candidates.append({
            "candidate_id": f"stage5.algo.{cid:04d}",
            "name": name, "en_name": en_name,
            "category": "algorithm_data_structure",
            "sub_category": prefix,
            "target_section": sec, "section_name": sn(sec),
            "candidate_type": item_def[2],
            "risk_band": item_def[3], "mapping_confidence": item_def[4],
            "suggested_direct_pre_names": item_def[5],
            "similar_existing_items": [],
            "duplicate_risk_note": "",
            "learning_value_note": item_def[6],
            "selection_reason": item_def[6]
        })

algo_count = len(candidates)
print(f"  Algo candidates: {algo_count}")

for batch in MATH_BATCHES:
    prefix, en_prefix, sec, items_list = batch
    for item_def in items_list:
        name = prefix + item_def[0]
        en_name = en_prefix + item_def[1]
        nl = name.lower().strip().replace(" ", "")
        if nl in existing_names or is_dup(name, en_name):
            continue
        existing_names.add(nl)
        cid += 1
        candidates.append({
            "candidate_id": f"stage5.math.{cid:04d}",
            "name": name, "en_name": en_name,
            "category": "contest_math",
            "sub_category": prefix,
            "target_section": sec, "section_name": sn(sec),
            "candidate_type": item_def[2],
            "risk_band": item_def[3], "mapping_confidence": item_def[4],
            "suggested_direct_pre_names": item_def[5],
            "similar_existing_items": [],
            "duplicate_risk_note": "",
            "learning_value_note": item_def[6],
            "selection_reason": item_def[6]
        })

math_count = len(candidates) - algo_count
print(f"  Math candidates: {math_count}")
print(f"  Total: {len(candidates)}")

# ============================================================
# DEDUP CHECK ON FINAL POOL
# ============================================================
print(f"\n  Running dedup check on {len(candidates)} candidates...")

risk_dist = defaultdict(int)
conf_dist = defaultdict(int)
sec_dist = defaultdict(int)
sub_cat_dist = defaultdict(int)
type_dist = defaultdict(int)
dup_stats = defaultdict(int)

for c in candidates:
    nl = c["name"].lower().strip().replace(" ", "")
    enl = c["en_name"].lower().strip().replace(" ", "")
    
    dup_risk = "none"
    similar = []
    
    if nl in name_lower_set:
        dup_risk = "exact_name_match"
        for existing_name_raw, ids in defaultdict(list, {}).items():
            pass
        for existing_nl in name_lower_set:
            if existing_nl == nl:
                dup_risk = "exact_name_match"
                break
    
    if dup_risk == "none" and enl and enl in en_lower_set:
        dup_risk = "exact_en_match"
    
    if dup_risk == "none":
        sims = []
        for iid, item in items_by_id.items():
            sim = max(jaccard(c["name"], item.get("name", "")), jaccard(c["en_name"], item.get("en_name", "")))
            if sim > 0.3:
                sims.append({"item_id": iid, "name": item.get("name", ""), "similarity": round(sim, 3)})
        sims.sort(key=lambda x: -x["similarity"])
        similar = sims[:3]
        if sims and sims[0]["similarity"] >= 0.85:
            dup_risk = "high_similarity"
        elif sims and sims[0]["similarity"] >= 0.65:
            dup_risk = "medium_similarity"
    
    c["similar_existing_items"] = similar
    c["duplicate_risk_note"] = dup_risk
    if dup_risk in ("exact_name_match", "exact_en_match", "high_similarity"):
        c["risk_band"] = "red"
    
    dup_stats[dup_risk] += 1
    risk_dist[c["risk_band"]] += 1
    conf_dist[c["mapping_confidence"]] += 1
    sec_dist[c["target_section"]] += 1
    sub_cat_dist[c["sub_category"]] += 1
    type_dist[c["candidate_type"]] += 1

green_yellow = sum(1 for c in candidates if c["risk_band"] in ("green", "yellow"))
first_batch = min(green_yellow, 400)

print(f"\n{'=' * 60}")
print(f"  FINAL SUMMARY")
print(f"{'=' * 60}")
print(f"  Total: {len(candidates)}")
print(f"  Algo+DS: {algo_count}")
print(f"  Math: {math_count}")
print(f"  Risk: {dict(risk_dist)}")
print(f"  Conf: {dict(conf_dist)}")
print(f"  Dup: {dict(dup_stats)}")
print(f"  Green+Yellow: {green_yellow}")
print(f"  First batch: {first_batch}")

# ============================================================
# OUTPUT
# ============================================================
ts = datetime.now(timezone.utc).isoformat()

plan = {
    "meta": {"generated_by": "stage5_hard_knowledge_candidate_pool_generator",
             "generated_at": ts, "baseline_item_count": item_count,
             "main_graph_modified": False, "merge_executed": False},
    "target": {"total": 1200, "algo_ds_target": 800, "math_target": 400},
    "actual": {"total": len(candidates), "algo_ds": algo_count, "math": math_count},
    "risk_distribution": dict(risk_dist),
    "confidence_distribution": dict(conf_dist),
    "section_distribution": dict(sec_dist),
    "sub_category_distribution": dict(sub_cat_dist),
    "candidate_type_distribution": dict(type_dist),
    "duplicate_risk_stats": dict(dup_stats),
    "suggested_first_batch": first_batch,
    "recommendation": "do_not_merge_directly",
    "next_steps": "Need more candidates to reach 1200 target. Expand sub-categories with detailed variants."
}
with open("data/stage5_hard_knowledge_candidate_pool_plan.json", "w", encoding="utf-8") as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)
print(f"    [OK] data/stage5_hard_knowledge_candidate_pool_plan.json")

with open("data/stage5_hard_knowledge_candidate_pool_1200.json", "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "total": len(candidates)}, "candidates": candidates}, f, ensure_ascii=False, indent=2)
print(f"    [OK] data/stage5_hard_knowledge_candidate_pool_1200.json")

precheck = {
    "meta": {"generated_at": ts, "baseline_item_count": item_count},
    "dedup_results": {
        "total_candidates": len(candidates),
        "exact_name_match": dup_stats.get("exact_name_match", 0),
        "exact_en_match": dup_stats.get("exact_en_match", 0),
        "high_similarity": dup_stats.get("high_similarity", 0),
        "medium_similarity": dup_stats.get("medium_similarity", 0),
        "none": dup_stats.get("none", 0),
        "red_flagged": sum(1 for c in candidates if c["risk_band"] == "red"),
        "merge_safe": green_yellow
    },
    "candidates_with_issues": [c for c in candidates if c["duplicate_risk_note"] not in ("none", "")]
}
with open("data/stage5_hard_knowledge_duplicate_precheck.json", "w", encoding="utf-8") as f:
    json.dump(precheck, f, ensure_ascii=False, indent=2)
print(f"    [OK] data/stage5_hard_knowledge_duplicate_precheck.json")

with open("docs/stage5_hard_knowledge_candidate_pool_report.md", "w", encoding="utf-8") as f:
    f.write("# Stage5 硬知识候选池规划报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")
    f.write("## 1. 基线确认\n\n")
    f.write(f"| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| 当前基线 | **{item_count}** |\n")
    f.write(f"| Section 数 | {len(sections)} |\n\n")
    f.write("## 2. 候选总数\n\n")
    f.write(f"| 类别 | 数量 |\n|------|------|\n")
    f.write(f"| 算法与数据结构 | {algo_count} |\n")
    f.write(f"| 竞赛数学 | {math_count} |\n")
    f.write(f"| **总计** | **{len(candidates)}** |\n")
    f.write(f"| 目标 | 1200 |\n")
    f.write(f"| 缺口 | {1200 - len(candidates)} |\n\n")
    f.write("## 3. risk_band 分布\n\n")
    for r in ["green", "yellow", "medium", "red"]:
        f.write(f"- {r}: {risk_dist.get(r, 0)}\n")
    f.write("\n## 4. mapping_confidence 分布\n\n")
    for c in ["high", "medium", "low"]:
        f.write(f"- {c}: {conf_dist.get(c, 0)}\n")
    f.write("\n## 5. 各 section 分布\n\n")
    f.write("| Section | 名称 | 候选数 |\n|---------|------|--------|\n")
    for sid in sorted(sec_dist.keys()):
        f.write(f"| {sid} | {sn(sid)} | {sec_dist[sid]} |\n")
    f.write(f"\n## 6. 重复风险统计\n\n")
    for dk, dv in sorted(dup_stats.items()):
        f.write(f"- {dk}: {dv}\n")
    f.write(f"\n## 7. 建议第一批合并数量\n\n{first_batch}\n\n")
    f.write(f"## 8. 是否建议直接合并\n\n**否**\n\n")
    f.write(f"## 9. 是否修改主图谱\n\n**否**\n\n")
    f.write(f"## 10. 后续分批建议\n\n")
    f.write(f"1. 当前已生成 {len(candidates)} 个候选，目标 1200\n")
    f.write(f"2. 需要进一步细化各子类，补充更多实现变体和应用场景\n")
    f.write(f"3. 建议分批：第一批 {first_batch} 个 green+yellow，后续逐步扩展\n\n")
    f.write(f"---\n*本报告自动生成*\n")
print(f"    [OK] docs/stage5_hard_knowledge_candidate_pool_report.md")

print(f"\nDone. No graph modifications.")
