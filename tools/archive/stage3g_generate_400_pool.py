#!/usr/bin/env python3
"""
Stage3G: Generate 400 Standardized Candidate Pool
不修改主图谱，不执行合并
"""
import json, os, re
from collections import Counter
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def load(path):
    with open(os.path.join(BASE_DIR, path), 'r', encoding='utf-8') as f:
        return json.load(f)

print("=" * 60)
print("Stage3G Generate 400 Standardized Candidate Pool")
print("=" * 60)

# Load graph and build dedup index
graph = load("merged_knowledge_graph_item_dependencies_refined.json")
dvr = load("dependency_validation_result.json")

all_items = {}
dedup_names = set()
dedup_en_names = set()
dedup_aliases = set()
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            all_items[item["id"]] = item
            n = item.get("name", "").strip()
            if n:
                dedup_names.add(n.lower())
            en = item.get("en_name", "").strip()
            if en:
                dedup_en_names.add(en.lower())
            for alias in item.get("aliases", []) or []:
                a = alias.strip().lower()
                if a:
                    dedup_aliases.add(a)
            for galias in item.get("global_aliases", []) or []:
                ga = galias.strip().lower()
                if ga:
                    dedup_aliases.add(ga)

print(f"  Existing: {len(all_items)} items")
print(f"  Dedup names: {len(dedup_names)}, en_names: {len(dedup_en_names)}, aliases: {len(dedup_aliases)}")

# Also load stage3f pruned items' names
pruned_names = set()
for f in ["data/stage3f_batch2_duplicate_prune_removed_items.json",
          "data/stage3f_batch3_full40_duplicate_prune_removed_items.json"]:
    try:
        pr_data = load(f)
        for pr in pr_data.get("removed_items", []):
            n = pr.get("name", "").strip()
            if n:
                pruned_names.add(n.lower())
    except: pass

print(f"  History pruned names: {len(pruned_names)}")

def is_duplicate(name, en_name):
    nl = name.strip().lower() if name else ""
    enl = en_name.strip().lower() if en_name else ""
    # Exact name match
    if nl in dedup_names:
        return True
    if enl and enl in dedup_en_names:
        return True
    if nl in dedup_aliases:
        return True
    if nl in pruned_names:
        return True
    # Fuzzy: check if this name is too similar to existing names
    for dn in dedup_names:
        # One contains the other
        if len(nl) > 5 and len(dn) > 5:
            if nl in dn or dn in nl:
                return True
            # Check word overlap
            words_nl = set(nl.replace("：", ":").replace("_", " ").split())
            words_dn = set(dn.replace("：", ":").replace("_", " ").split())
            if len(words_nl & words_dn) >= min(len(words_nl), len(words_dn)) * 0.8 and len(words_nl & words_dn) >= 2:
                return True
    return False

# ============================================================
# Define 400 candidates across 12 themes
# ============================================================
candidates = []

# Track generated IDs to avoid duplicates
generated_cids = set()
generated_names = set()

def make_cid(theme, name):
    safe = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '_', name.lower())[:50]
    safe = re.sub(r'_+', '_', safe).strip('_')
    cid = f"cand.{theme}.{safe}"
    if cid in generated_cids:
        for i in range(2, 99):
            cid2 = f"{cid}_{i}"
            if cid2 not in generated_cids:
                return cid2, True
    return cid, True

def add_candidate(theme_display, theme_id, name, en_name, target_section, section_name,
                  risk_band, mapping_confidence, suggested_parent, direct_pre_suggestions,
                  is_problem_pattern, candidate_type, selection_reason, dup_note, value_note):
    cid, _ = make_cid(theme_id, name)

    # Dedup check
    dup_risk = is_duplicate(name, en_name)
    if dup_risk:
        mapping_confidence = "low"
        if risk_band == "green":
            risk_band = "yellow"

    cand = {
        "candidate_id": cid,
        "name": name,
        "en_name": en_name,
        "source": "stage3g_generated",
        "target_section": target_section,
        "section_name": section_name,
        "theme": theme_display,
        "risk_band": risk_band,
        "mapping_confidence": mapping_confidence,
        "suggested_parent_concept": suggested_parent,
        "direct_pre_name_suggestion": direct_pre_suggestions[:8],
        "possible_problem_pattern": is_problem_pattern,
        "candidate_type": candidate_type,
        "selection_reason": selection_reason,
        "duplicate_risk_note": dup_note if dup_risk else "",
        "learning_value_note": value_note
    }
    candidates.append(cand)
    generated_cids.add(cid)
    return cand

# ============================================================
# Section name lookup
# ============================================================
section_names = {}
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        section_names[sec["id"]] = sec.get("name", "")
def sn(sid):
    return section_names.get(sid, sid)

# ============================================================
# THEME 1: 图论专题 (55)
# ============================================================
T = "图论专题"
TI = "graph"
GS = ["2.9","2.11","2.12","2.13","2.14","2.15","2.16","2.17","2.21"]

def gs(sid):
    return sid, sn(sid)

graph_cands = [
    ("图论建模：超级源点与超级汇点", "graph_modeling_super_source", "2.9", "green", "high",
     "图建模基础", ["超级源点", "超级汇点", "图建模基础", "最大流", "最短路"],
     "modeling_pattern", False, "超级源/汇点是建模中常用的技巧", ""),
    ("图论建模：分层图", "graph_modeling_layered", "2.9", "green", "high",
     "图建模基础", ["分层图", "图建模基础", "最短路", "DP状态图"],
     "modeling_pattern", False, "分层图是竞赛常见模型", ""),
    ("图论建模：差分约束进阶", "graph_modeling_diff_constraints_advanced", "2.9", "yellow", "medium",
     "图建模基础", ["差分约束", "图建模基础", "最短路", "SPFA"],
     "modeling_pattern", False, "高级差分约束建模技巧", ""),
    ("图论建模：状态压缩图", "graph_modeling_state_compress", "2.9", "yellow", "medium",
     "图建模基础", ["图建模基础", "状态压缩", "BFS", "最短路径"],
     "modeling_pattern", False, "状态压缩与图结合建模", ""),
    ("拓扑排序进阶：字典序拓扑", "topo_sort_lexicographical", "2.11", "green", "high",
     "拓扑排序", ["拓扑排序", "优先队列", "DAG", "贪心"],
     "core_concept", False, "字典序拓扑是实战常见需求", ""),
    ("拓扑排序进阶：拓扑计数", "topo_sort_counting", "2.11", "yellow", "medium",
     "拓扑排序", ["拓扑排序", "DP", "DAG", "组合计数"],
     "theorem_or_property", False, "DAG拓扑序计数", ""),
    ("欧拉路径进阶：Hierholzer算法", "euler_hierholzer", "2.11", "green", "high",
     "欧拉路径", ["欧拉路径", "DFS", "图的遍历", "环路"],
     "core_concept", False, "Hierholzer是欧拉路径高效算法", ""),
    ("欧拉路径进阶：中国邮路问题", "euler_chinese_postman", "2.11", "medium", "low",
     "欧拉路径", ["欧拉路径", "最短路", "匹配", "图论建模"],
     "application_case", False, "中国邮路是最短路+匹配+欧拉的综合应用", ""),
    ("最小生成树进阶：次小生成树", "mst_second_best", "2.12", "green", "high",
     "最小生成树", ["最小生成树", "LCA", "树链", "倍增"],
     "core_concept", False, "次小生成树是经典扩展问题", ""),
    ("最小生成树进阶：最小瓶颈生成树", "mst_bottleneck", "2.12", "green", "high",
     "最小生成树", ["最小生成树", "瓶颈", "Kruskal"],
     "core_concept", False, "瓶颈生成树与MST的关系", ""),
    ("最小生成树进阶：生成树计数", "mst_counting", "2.12", "medium", "low",
     "最小生成树", ["最小生成树", "矩阵树定理", "行列式"],
     "theorem_or_property", True, "生成树计数运用矩阵树定理", ""),
    ("LCA进阶：Tarjan离线LCA", "lca_tarjan_offline", "2.14", "green", "high",
     "LCA", ["LCA", "并查集", "DFS", "离线算法"],
     "core_concept", False, "Tarjan离线LCA是重要算法", ""),
    ("LCA进阶：LCA与树上差分", "lca_tree_diff", "2.14", "green", "high",
     "LCA", ["LCA", "树上差分", "前缀和", "树"],
     "core_concept", True, "树上差分+LCA是路径统计的标准方法", ""),
    ("树论：树的重心进阶", "tree_centroid_advanced", "2.14", "green", "high",
     "树", ["树的重心", "DFS", "树形DP"],
     "core_concept", False, "树的重心性质与分治应用", ""),
    ("树论：树的直径进阶应用", "tree_diameter_advanced", "2.14", "green", "high",
     "树", ["树直径", "DFS", "BFS", "树形DP"],
     "core_concept", False, "树直径的两遍DFS求法和扩展应用", ""),
    ("树论：树哈希", "tree_hash", "2.14", "yellow", "medium",
     "树", ["树", "哈希", "字符串哈希", "同构"],
     "core_concept", False, "树哈希解决树同构问题", ""),
    ("树论：点分治进阶", "divide_and_conquer_on_tree_advanced", "2.14", "yellow", "medium",
     "树分治", ["点分治", "树", "重心", "路径统计"],
     "core_concept", False, "点分治的进阶应用", ""),
    ("树论：边分治", "edge_conquer_on_tree", "2.14", "medium", "low",
     "树分治", ["点分治", "树", "重构", "路径"],
     "implementation_variant", False, "边分治是点分治的补充", ""),
    ("最短路进阶：0-1BFS变体", "shortest_01bfs_variant", "2.15", "green", "high",
     "最短路", ["0-1BFS", "最短路", "双端队列", "边权"],
     "core_concept", False, "0-1BFS在01权图高效求最短路", ""),
    ("最短路进阶：同余最短路", "shortest_congruence", "2.15", "yellow", "medium",
     "最短路", ["最短路", "同余", "Dijkstra", "模运算"],
     "modeling_pattern", True, "同余最短路是建模方法", ""),
    ("最短路进阶：K短路(A*)", "shortest_k_a_star", "2.15", "yellow", "medium",
     "最短路", ["最短路", "A*", "启发式", "堆"],
     "core_concept", False, "A*算法求K短路", ""),
    ("最短路进阶：最小环", "shortest_min_cycle", "2.15", "yellow", "medium",
     "最短路", ["最短路", "Floyd", "Dijkstra", "环"],
     "core_concept", False, "有向图/无向图最小环多种求法", ""),
    ("最大流进阶：Dinic进阶优化", "max_flow_dinic_optimized", "2.16", "green", "high",
     "最大流", ["最大流", "Dinic", "弧优化", "BFS分层"],
     "core_concept", False, "Dinic的当前弧优化和多路增广", ""),
    ("最大流进阶：ISAP算法", "max_flow_isap", "2.16", "green", "high",
     "最大流", ["最大流", "Dinic", "SAP", "增广"],
     "core_concept", False, "ISAP是Dinic的改进版", ""),
    ("最大流进阶：HLPP预流推进", "max_flow_hlpp", "2.16", "medium", "low",
     "最大流", ["最大流", "Dinic", "预流推进", "余量"],
     "core_concept", False, "HLPP是最快的最大流算法", ""),
    ("费用流进阶：最小费用最大流(Dinic+SPFA)", "min_cost_flow_dinic_spfa", "2.16", "green", "high",
     "费用流", ["费用流", "Dinic", "SPFA", "最短路"],
     "core_concept", False, "Dinic+SPFA实现最小费用流", ""),
    ("费用流进阶：最小费用流(Primal-Dual)", "min_cost_flow_primal_dual", "2.16", "yellow", "medium",
     "费用流", ["费用流", "Dijkstra", "势能", "Johnson"],
     "core_concept", False, "势能转化的Primal-Dual算法", ""),
    ("费用流进阶：上下界费用流", "min_cost_flow_bounds", "2.16", "medium", "low",
     "费用流", ["费用流", "上下界", "可行流", "网络流"],
     "core_concept", False, "带上下界的费用流", ""),
    ("最大流建模：最大权闭合子图进阶", "max_flow_closure_advanced", "2.16", "yellow", "medium",
     "最大流建模", ["最大权闭合子图", "最小割", "最大流", "图建模"],
     "modeling_pattern", True, "最大权闭合子图的多种变体", ""),
    ("最大流建模：最大密度子图", "max_flow_density_subgraph", "2.16", "yellow", "medium",
     "最大流建模", ["最大权闭合子图", "最小割", "分数规划", "二分数值"],
     "modeling_pattern", True, "最大密度子图是闭合子图的扩展", ""),
    ("最大流建模：混合图欧拉回路", "max_flow_mixed_euler", "2.16", "medium", "low",
     "最大流建模", ["网络流", "欧拉回路", "流量平衡", "图论"],
     "modeling_pattern", True, "混合图欧拉回路转化为网络流", ""),
    ("二分图进阶：二分图完美匹配(KM算法)", "bipartite_km", "2.17", "green", "high",
     "二分图", ["二分图匹配", "匈牙利", "KM", "最大权匹配"],
     "core_concept", False, "KM算法求最大权完美匹配", ""),
    ("二分图进阶：一般图匹配(Tutte矩阵)", "general_matching_tutte", "2.17", "medium", "low",
     "二分图", ["一般图匹配", "Tutte矩阵", "行列式", "随机化"],
     "theorem_or_property", False, "Tutte矩阵判断一般图完美匹配", ""),
    ("二分图进阶：稳定婚姻问题", "bipartite_stable_marriage", "2.17", "green", "high",
     "二分图", ["二分图匹配", "GS算法", "稳定匹配", "贪心"],
     "application_case", False, "Gale-Shapley稳定婚姻算法", ""),
    ("线性代数进阶：矩阵加速递推", "linear_algebra_matrix_dp", "2.17", "green", "high",
     "线性代数", ["矩阵快速幂", "递推", "斐波那契", "DP"],
     "core_concept", False, "矩阵加速是竞赛常用技巧", ""),
    ("线性代数进阶：矩阵树定理进阶", "linear_algebra_matrix_tree_advanced", "2.17", "yellow", "medium",
     "线性代数", ["矩阵树定理", "行列式", "Kirchhoff", "生成树"],
     "theorem_or_property", False, "矩阵树定理的扩展应用", ""),
    ("SCC/DAG进阶：2-SAT方案输出", "scc_twosat_output", "2.21", "green", "high",
     "强连通分量", ["2-SAT", "SCC", "Tarjan", "拓扑序"],
     "core_concept", False, "2-SAT判断+方案构造", ""),
    ("SCC/DAG进阶：DAG最小路径覆盖", "scc_dag_min_path_cover", "2.21", "yellow", "medium",
     "DAG", ["DAG", "二分图匹配", "路径覆盖", "拆点"],
     "modeling_pattern", True, "DAG最小路径覆盖转化为二分图匹配", ""),
    ("SCC/DAG进阶：DAG最长反链(Dilworth)", "scc_dag_dilworth", "2.21", "yellow", "medium",
     "DAG", ["DAG", "Dilworth", "偏序集", "最小链覆盖"],
     "theorem_or_property", False, "Dilworth定理在竞赛中的应用", ""),
    ("SCC/DAG进阶：可达性统计(Bitset优化)", "scc_dag_reachability_bitset", "2.21", "green", "high",
     "DAG", ["DAG", "拓扑排序", "Bitset", "可达性"],
     "core_concept", True, "Bitset优化DAG可达性统计", ""),
    ("动态树：树链剖分(LCT辅助)", "dynamic_tree_hld_lct", "3.13", "medium", "low",
     "树链剖分", ["LCT", "树链剖分", "Splay", "动态树"],
     "core_concept", False, "LCT与树链剖分的配合", ""),
    ("动态树：树上路径并集", "dynamic_tree_path_union", "3.13", "medium", "low",
     "动态树", ["LCT", "并查集", "路径", "树"],
     "core_concept", False, "LCT维护路径并集", ""),
    ("特殊图：竞赛图", "special_graph_tournament", "2.21", "yellow", "medium",
     "竞赛图", ["竞赛图", "哈密顿路径", "SCC", "图论"],
     "core_concept", False, "竞赛图的性质与应用", ""),
    ("特殊图：弦图", "special_graph_chordal", "2.21", "medium", "low",
     "弦图", ["弦图", "完美消除序列", "MCS", "图论"],
     "core_concept", False, "弦图与完美消除序列", ""),
    ("特殊图：平面图", "special_graph_planar", "2.21", "medium", "low",
     "平面图", ["平面图", "欧拉公式", "对偶图", "图论"],
     "core_concept", False, "平面图性质及其应用", ""),
    ("特殊图：仙人掌图进阶", "special_graph_cactus_advanced", "2.21", "yellow", "medium",
     "仙人掌图", ["仙人掌图", "圆方树", "DP", "图论"],
     "core_concept", False, "仙人掌图的圆方树转化", ""),
    ("图论专题：图同构", "graph_isomorphism", "2.21", "red", "low",
     "图同构", ["图同构", "哈希", "树哈希", "难解问题"],
     "theorem_or_property", False, "图同构判定是NP难题", ""),
    ("图论专题：图着色", "graph_coloring", "2.21", "red", "low",
     "图着色", ["图着色", "贪心", "四色定理", "NP-hard"],
     "core_concept", False, "图着色问题是重要NP问题", ""),
    ("图论专题：Steiner树进阶", "steiner_tree_advanced", "2.21", "medium", "low",
     "Steiner树", ["Steiner树", "DP", "SPFA", "子集"],
     "core_concept", False, "Steiner树DP解法", ""),
    ("图论专题：最小树形图(朱刘)", "min_arborescence_chuliu", "2.21", "yellow", "medium",
     "最小树形图", ["最小树形图", "有向生成树", "朱刘算法", "贪心"],
     "core_concept", False, "朱刘算法求有向图MST", ""),
    ("图论专题：最小树形图进阶", "min_arborescence_advanced", "2.21", "medium", "low",
     "最小树形图", ["最小树形图", "朱刘", "缩点", "有向图"],
     "implementation_variant", False, "最小树形图的优化实现", ""),
    ("图论专题：最大密度子图(参数搜索)", "max_density_param_search", "2.21", "medium", "low",
     "最大密度子图", ["最大密度子图", "分数规划", "网络流", "二分"],
     "modeling_pattern", True, "参数搜索求最大密度子图", ""),
    ("图论专题：Gomory-Hu树", "gomory_hu_tree", "2.21", "yellow", "medium",
     "全局最小割", ["最小割", "Gomory-Hu", "全局最小割", "分治"],
     "core_concept", False, "Gomory-Hu树压缩任意点对最小割", ""),
    ("图论专题：Stoer-Wagner全局最小割", "stoer_wagner", "2.21", "yellow", "medium",
     "全局最小割", ["最小割", "Stoer-Wagner", "全局最小割", "无向图"],
     "core_concept", False, "Stoer-Wagner算法求无向图全局最小割", ""),
    ("图论专题：离线动态连通性(线段树分治)", "offline_dynamic_connectivity", "2.21", "green", "high",
     "动态连通性", ["并查集", "线段树", "分治", "可撤销并查集"],
     "core_concept", False, "线段树分治处理离线动态连通性", ""),
]
for c in graph_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason, _ = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充图论知识覆盖")
graph_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {graph_count}")

# ============================================================
# THEME 2: 数据结构专题 (50)
# ============================================================
T = "数据结构专题"
TI = "ds"

ds_cands = [
    ("并查集进阶：可持久化并查集", "dsu_persistent", "3.13", "yellow", "medium",
     "并查集", ["并查集", "可持久化", "主席树", "可持久化数组"],
     "implementation_variant", False, "可持久化并查集使用可持久化数组"),
    ("并查集进阶：可撤销并查集", "dsu_rollback", "3.1", "green", "high",
     "并查集", ["并查集", "启发式合并", "撤销", "栈"],
     "implementation_variant", False, "可撤销并查集处理时间回溯"),
    ("线段树进阶：Segment Tree Beats", "segtree_beats", "3.13", "yellow", "medium",
     "线段树", ["线段树", "势能", "区间最值", "复杂度"],
     "implementation_variant", False, "Segment Tree Beats区间取min操作"),
    ("线段树进阶：线段树分裂合并", "segtree_split_merge", "3.13", "yellow", "medium",
     "线段树", ["线段树", "权值线段树", "合并", "分裂"],
     "implementation_variant", False, "线段树分裂合并解决区间划分"),
    ("线段树进阶：线段树分治", "segtree_divide_conquer", "3.13", "green", "high",
     "线段树", ["线段树", "分治", "可撤销", "时间维"],
     "core_concept", False, "线段树分治处理时间维度问题"),
    ("树状数组进阶：树状数组二分", "bit_binary_search", "3.3", "green", "high",
     "树状数组", ["树状数组", "二分", "前缀和", "BIT"],
     "core_concept", False, "树状数组上二分求第k小"),
    ("树状数组进阶：多维树状数组", "bit_multidimensional", "3.3", "yellow", "medium",
     "树状数组", ["树状数组", "多维", "CDQ分治", "二维偏序"],
     "implementation_variant", False, "高维树状数组应用"),
    ("平衡树进阶：FHQ Treap可持久化", "fhq_treap_persistent", "3.5", "yellow", "medium",
     "平衡树", ["FHQ Treap", "可持久化", "分裂合并", "平衡树"],
     "implementation_variant", False, "FHQ Treap的可持久化版本"),
    ("平衡树进阶：Splay区间操作", "splay_interval", "3.5", "green", "high",
     "平衡树", ["Splay", "区间", "翻转", "LCT基础"],
     "core_concept", False, "Splay维护区间操作"),
    ("平衡树进阶：Treap实现", "treap_implementation", "3.5", "green", "high",
     "平衡树", ["Treap", "BST", "堆", "随机化"],
     "core_concept", False, "Treap树堆实现"),
    ("堆进阶：可并堆(左偏树)", "heap_leftist", "3.2", "green", "high",
     "堆", ["堆", "左偏树", "可并堆", "合并"],
     "core_concept", False, "左偏树实现可合并堆"),
    ("堆进阶：斐波那契堆", "heap_fibonacci", "3.2", "red", "low",
     "堆", ["堆", "斐波那契", "摊还", "优先队列"],
     "core_concept", False, "斐波那契堆理论高效但常数大"),
    ("堆进阶：配对堆", "heap_pairing", "3.2", "medium", "low",
     "堆", ["堆", "配对标", "可并堆", "Dijkstra优化"],
     "core_concept", False, "配对堆是实用可并堆"),
    ("ST表进阶：二维ST表", "st_2d", "3.3", "yellow", "medium",
     "ST表", ["ST表", "二维", "RMQ", "倍增"],
     "implementation_variant", False, "二维ST表处理矩阵RMQ"),
    ("分块进阶：莫队算法", "mo_algorithm", "3.3", "green", "high",
     "分块", ["分块", "莫队", "离线", "区间查询"],
     "core_concept", False, "莫队算法处理离线区间查询"),
    ("分块进阶：带修莫队", "mo_with_update", "3.13", "yellow", "medium",
     "分块", ["莫队", "在线修改", "分块", "区间"],
     "implementation_variant", False, "支持单点修改的莫队"),
    ("分块进阶：回滚莫队", "mo_rollback", "3.13", "yellow", "medium",
     "分块", ["莫队", "回滚", "分块", "离线"],
     "implementation_variant", False, "回滚莫队处理只加不减场景"),
    ("分块进阶：树上莫队", "mo_on_tree", "3.13", "yellow", "medium",
     "分块", ["莫队", "树", "括号序", "LCA"],
     "core_concept", False, "树上莫队将树转化为序列处理"),
    ("K-D Tree", "kd_tree", "3.13", "yellow", "medium",
     "空间数据结构", ["空间划分", "最近邻", "剪枝", "多维"],
     "core_concept", False, "K-D Tree处理k维空间查询"),
    ("K-D Tree进阶：最近邻搜索", "kd_tree_nearest", "3.13", "medium", "low",
     "K-D Tree", ["K-D Tree", "最近邻", "剪枝", "多维"],
     "core_concept", False, "K-D Tree最邻近搜索"),
    ("CDQ分治进阶：三维偏序", "cdq_3d", "3.13", "green", "high",
     "CDQ分治", ["CDQ分治", "偏序", "归并排序", "树状数组"],
     "core_concept", False, "CDQ分治处理三维偏序问题"),
    ("CDQ分治进阶：CDQ套CDQ", "cdq_nested", "3.13", "red", "low",
     "CDQ分治", ["CDQ分治", "偏序", "归并", "多维"],
     "implementation_variant", False, "嵌套CDQ处理四维偏序"),
    ("整体二分", "parallel_binary_search", "3.13", "green", "high",
     "整体二分", ["二分", "分治", "树状数组", "离线"],
     "core_concept", False, "整体二分处理多查询二分问题"),
    ("整体二分进阶：带修改整体二分", "parallel_binary_search_with_update", "3.13", "medium", "low",
     "整体二分", ["整体二分", "单点修改", "第k大", "树状数组"],
     "implementation_variant", False, "支持单点修改的整体二分"),
    ("哈希进阶：布隆过滤器", "bloom_filter", "3.8", "yellow", "medium",
     "哈希", ["哈希", "布隆", "概率", "位图"],
     "core_concept", False, "布隆过滤器处理集合隶属查询"),
    ("哈希进阶：一致性哈希", "consistent_hashing", "3.8", "red", "low",
     "哈希", ["哈希", "一致性", "分布式", "虚拟节点"],
     "core_concept", False, "一致性哈希在工程中的使用"),
    ("可持久化进阶：可持久化Trie", "persistent_trie", "3.13", "green", "high",
     "可持久化", ["Trie", "可持久化", "二进制", "异或"],
     "core_concept", False, "可持久化Trie处理最大异或对"),
    ("可持久化进阶：可持久化平衡树", "persistent_balanced_tree", "3.13", "medium", "low",
     "可持久化", ["FHQ Treap", "可持久化", "平衡树", "分裂合并"],
     "implementation_variant", False, "可持久化平衡树的实现"),
    ("分块进阶：块状链表", "block_linked_list", "3.3", "yellow", "medium",
     "分块", ["分块", "链表", "数组", "根号"],
     "core_concept", False, "块状链表结合数组与链表优势"),
    ("分块进阶：分块打表", "block_precompute_table", "3.3", "yellow", "medium",
     "分块", ["分块", "预处理", "表", "空间换时间"],
     "modeling_pattern", True, "分块思想应用于打表优化"),
    ("字符串数据结构：后缀数组SA-IS算法", "suffix_array_sais", "3.8", "medium", "low",
     "后缀数组", ["后缀数组", "SA-IS", "线性时间", "字符串"],
     "core_concept", False, "SA-IS线性时间构建后缀数组"),
    ("字符串数据结构：后缀自动机(SAM)进阶", "sam_advanced", "3.8", "yellow", "medium",
     "后缀自动机", ["后缀自动机", "子串", "出现次数", "字符串本质"],
     "core_concept", False, "SAM的高级应用"),
    ("字符串数据结构：广义后缀自动机", "sam_generalized", "3.8", "yellow", "medium",
     "后缀自动机", ["后缀自动机", "多串", "Trie", "SAM构建"],
     "implementation_variant", False, "广义SAM处理多字符串"),
    ("字符串数据结构：回文自动机(PAM)", "pam", "3.8", "green", "high",
     "回文自动机", ["回文自动机", "回文", "子串", "字符串"],
     "core_concept", False, "回文自动机是回文处理利器"),
    ("字符串数据结构：后缀树", "suffix_tree", "3.8", "medium", "low",
     "后缀树", ["后缀树", "后缀数组", "后缀自动机", "字符串"],
     "core_concept", False, "后缀树是后缀结构的顶层抽象"),
    ("RMQ进阶：四毛子算法", "rmq_four_russian", "3.3", "red", "low",
     "RMQ", ["ST表", "RMQ", "±1RMQ", "分块"],
     "core_concept", False, "四毛子算法实现O(n)-O(1)RMQ"),
    ("树链剖分进阶：边权转点权", "hld_edge_to_vertex", "3.5", "green", "high",
     "树链剖分", ["树链剖分", "边权", "点权", "线段树"],
     "modeling_pattern", True, "边权转点权是树剖标准技巧"),
    ("树链剖分进阶：动态DP", "hld_dynamic_dp", "3.13", "yellow", "medium",
     "树链剖分", ["树链剖分", "DP", "矩阵", "线段树"],
     "core_concept", False, "动态DP在树链上的应用"),
    ("树链剖分进阶：长链剖分", "hld_long_chain", "3.13", "yellow", "medium",
     "树链剖分", ["树链剖分", "长链", "DP", "深度"],
     "implementation_variant", False, "长链剖分优化深度相关DP"),
    ("Link-Cut Tree进阶：维护子树信息", "lct_subtree", "3.13", "medium", "low",
     "LCT", ["LCT", "子树信息", "Splay", "虚实链"],
     "core_concept", False, "LCT维护子树信息的方法"),
    ("Link-Cut Tree进阶：LCT处理边权", "lct_edge_weight", "3.13", "medium", "low",
     "LCT", ["LCT", "边权", "换根", "最小生成树"],
     "implementation_variant", False, "LCT处理动态边权问题"),
    ("Link-Cut Tree进阶：LCT维护最小生成树", "lct_mst", "3.13", "yellow", "medium",
     "LCT", ["LCT", "最小生成树", "动态MST", "边权"],
     "core_concept", False, "LCT维护动态最小生成树"),
    ("平衡树进阶：WBLT", "wblt", "3.5", "medium", "low",
     "平衡树", ["WBLT", "平衡树", "叶加权", "BST"],
     "core_concept", False, "加权平衡树(WBLT)实现"),
    ("珂朵莉树(ODT)", "odt", "3.13", "green", "high",
     "珂朵莉树", ["珂朵莉树", "ODT", "区间赋值", "set"],
     "implementation_variant", False, "珂朵莉树处理随机数据区间操作"),
    ("笛卡尔树", "cartesian_tree", "3.13", "green", "high",
     "笛卡尔树", ["笛卡尔树", "RMQ", "堆", "BST"],
     "core_concept", False, "笛卡尔树是堆与BST的结合"),
    ("最小值栈/队列", "min_stack_queue", "3.2", "green", "high",
     "栈与队列", ["栈", "队列", "滑动窗口", "单调队列"],
     "core_concept", False, "最小值栈/队列O(1)查询最小值"),
    ("图存储进阶：十字链表", "graph_cross_linked_list", "3.9", "medium", "low",
     "图存储", ["图存储", "十字链表", "邻接表", "邻接矩阵"],
     "implementation_variant", False, "十字链表存储有向图"),
    ("图存储进阶：链式前向星", "graph_forward_star", "3.9", "green", "high",
     "图存储", ["邻接表", "数组", "边集", "遍历"],
     "core_concept", False, "链式前向星是竞赛标准存图方式"),
    ("集合进阶：bitset优化", "bitset_optimization", "3.13", "green", "high",
     "位集", ["bitset", "位运算", "压位", "优化"],
     "modeling_pattern", True, "bitset优化是竞赛常见优化手段"),
    ("集合进阶：压位Trie(二进制Trie)", "bitset_binary_trie", "3.13", "yellow", "medium",
     "位集", ["Trie", "二进制", "异或", "最大异或对"],
     "core_concept", False, "二进制Trie处理异或相关问题"),
]
for c in ds_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充数据结构知识覆盖")
ds_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {ds_count}")

# ============================================================
# THEME 3: 动态规划专题 (45)
# ============================================================
T = "动态规划专题"
TI = "dp"

dp_cands = [
    ("DP优化：决策单调性(四边形不等式)", "dp_opt_quadrangle", "2.8", "yellow", "medium",
     "DP优化", ["DP", "四边形不等式", "决策单调性", "分治优化"],
     "core_concept", False, "四边形不等式优化DP"),
    ("DP优化：WQS二分(带权二分)", "dp_opt_wqs", "2.8", "yellow", "medium",
     "DP优化", ["DP", "WQS", "二分", "凸优化"],
     "core_concept", False, "WQS二分优化带限制DP"),
    ("DP优化：斜率优化进阶", "dp_opt_convex_hull_trick", "2.8", "green", "high",
     "DP优化", ["斜率优化", "凸包", "单调队列", "DP"],
     "core_concept", False, "斜率优化处理DP转移优化"),
    ("DP优化：Li Chao线段树", "dp_opt_li_chao", "2.8", "green", "high",
     "DP优化", ["线段树", "凸包", "直线", "最小值"],
     "core_concept", False, "Li Chao线段树处理直线DP"),
    ("DP优化：Knuth优化", "dp_opt_knuth", "2.8", "yellow", "medium",
     "DP优化", ["DP", "Knuth", "四边形不等式", "区间DP"],
     "core_concept", False, "Knuth优化区间DP"),
    ("数位DP进阶：数位DP与自动机", "digit_dp_automaton", "2.8", "yellow", "medium",
     "数位DP", ["数位DP", "自动机", "AC自动机", "Digit DP"],
     "core_concept", False, "数位DP与自动机结合处理复杂约束"),
    ("数位DP进阶：数位DP(sum/product约束)", "digit_dp_sum_product", "2.8", "green", "high",
     "数位DP", ["数位DP", "数位和", "数位积", "模"],
     "core_concept", False, "数位DP处理数位和/积约束"),
    ("区间DP进阶：环上区间DP", "interval_dp_cycle", "2.8", "green", "high",
     "区间DP", ["区间DP", "环形", "破环成链", "DP"],
     "core_concept", False, "环上区间DP破环成链处理"),
    ("区间DP进阶：区间DP与四边形不等式", "interval_dp_quadrangle", "2.8", "yellow", "medium",
     "区间DP", ["区间DP", "四边形不等式", "决策单调", "优化"],
     "core_concept", False, "四边形不等式优化区间DP"),
    ("树形DP进阶：换根DP(二次扫描)", "tree_dp_reroot", "2.8", "green", "high",
     "树形DP", ["树形DP", "换根", "二次扫描", "树"],
     "core_concept", False, "换根DP处理根变化的最值"),
    ("树形DP进阶：树形背包", "tree_dp_knapsack", "2.8", "green", "high",
     "树形DP", ["树形DP", "背包", "树上背包", "DP"],
     "core_concept", False, "树形背包的复杂度优化"),
    ("树形DP进阶：树形DP与直径", "tree_dp_diameter", "2.8", "yellow", "medium",
     "树形DP", ["树形DP", "直径", "树", "最远点"],
     "core_concept", False, "树形DP求树直径及扩展"),
    ("状压DP进阶：高维前缀和(SOS DP)", "bitmask_dp_sos", "2.8", "green", "high",
     "状压DP", ["状压DP", "SOS DP", "前缀和", "子集"],
     "core_concept", False, "SOS DP处理子集/超集DP"),
    ("状压DP进阶：插头DP(轮廓线)", "bitmask_dp_plug", "2.8", "yellow", "medium",
     "状压DP", ["状压DP", "插头DP", "轮廓线", "连通性DP"],
     "core_concept", False, "插头DP处理连通性相关问题"),
    ("状压DP进阶：DP套DP(自动机DP)", "bitmask_dp_auto_dp", "2.8", "medium", "low",
     "状压DP", ["状压DP", "DP套DP", "自动机", "KMP自动机"],
     "core_concept", False, "DP套DP解决计数问题"),
    ("概率DP进阶：期望DP与高斯消元", "prob_dp_gaussian", "2.8", "yellow", "medium",
     "概率DP", ["概率DP", "期望", "高斯消元", "马尔可夫链"],
     "core_concept", True, "期望DP配合高斯消元求解"),
    ("概率DP进阶：概率生成函数", "prob_dp_generating_function", "2.8", "red", "low",
     "概率DP", ["概率DP", "生成函数", "期望", "概率"],
     "theorem_or_property", False, "概率生成函数处理期望"),
    ("计数DP：卡特兰数DP", "counting_dp_catalan", "2.8", "green", "high",
     "计数DP", ["计数DP", "卡特兰数", "组合", "递推"],
     "core_concept", False, "卡特兰数及其DP应用"),
    ("计数DP：斯特林数", "counting_dp_stirling", "2.8", "yellow", "medium",
     "计数DP", ["计数DP", "斯特林数", "组合", "划分"],
     "core_concept", False, "第一类和第二类斯特林数"),
    ("计数DP：容斥DP", "counting_dp_inclusion_exclusion", "2.8", "yellow", "medium",
     "计数DP", ["计数DP", "容斥原理", "组合", "DP"],
     "modeling_pattern", True, "容斥DP处理复杂计数"),
    ("计数DP：Burnside引理与Polya计数", "counting_dp_burnside", "2.8", "yellow", "medium",
     "计数DP", ["计数DP", "Burnside", "Polya", "群论"],
     "theorem_or_property", False, "Burnside引理处理等价类计数"),
    ("DP进阶：DP与自动机(KMP自动机DP)", "dp_kmp_automaton", "2.8", "yellow", "medium",
     "DP与自动机", ["KMP", "自动机", "DP", "字符串"],
     "modeling_pattern", True, "KMP自动机DP处理字符串约束"),
    ("DP进阶：DP与AC自动机", "dp_ac_automaton", "2.8", "green", "high",
     "DP与自动机", ["AC自动机", "DP", "多串", "字符串"],
     "core_concept", False, "AC自动机上DP处理多串约束"),
    ("DP进阶：DP与SAM", "dp_sam", "2.8", "medium", "low",
     "DP与自动机", ["后缀自动机", "DP", "子串", "字符串"],
     "core_concept", False, "SAM上DP处理子串问题"),
    ("博弈DP进阶：不平等博弈", "game_dp_unequal", "2.8", "medium", "low",
     "博弈DP", ["博弈DP", "不平等博弈", "surreal number", "SG函数"],
     "core_concept", False, "不平等博弈与surreal number"),
    ("博弈DP进阶：Multi-SG", "game_dp_multi_sg", "2.8", "yellow", "medium",
     "博弈DP", ["博弈DP", "SG函数", "Multi-SG", "分裂"],
     "core_concept", False, "Multi-SG处理分裂局面"),
    ("博弈DP进阶：Every-SG", "game_dp_every_sg", "2.8", "medium", "low",
     "博弈DP", ["博弈DP", "SG函数", "Every-SG", "全子游戏"],
     "core_concept", False, "Every-SG处理所有子游戏"),
    ("DP进阶：DP状态压缩与记忆化搜索", "dp_memoization_advanced", "2.8", "green", "high",
     "DP优化", ["DP", "记忆化搜索", "状态压缩", "剪枝"],
     "modeling_pattern", True, "记忆化搜索与状态设计技巧"),
    ("DP进阶：DP状态设计技巧", "dp_state_design", "2.8", "green", "high",
     "DP设计", ["DP", "状态设计", "转移方程", "边界"],
     "modeling_pattern", True, "DP状态设计是核心能力"),
    ("DP进阶：高维DP降维", "dp_dimension_reduction", "2.8", "yellow", "medium",
     "DP优化", ["DP", "降维", "滚动数组", "空间优化"],
     "modeling_pattern", True, "高维DP空间压缩技巧"),
    ("单调队列优化DP进阶", "dp_opt_monotone_queue_advanced", "2.8", "green", "high",
     "DP优化", ["单调队列", "DP", "滑动窗口", "优化"],
     "core_concept", False, "单调队列优化DP的标准模型"),
    ("数据结构优化DP进阶：线段树优化", "dp_opt_segtree", "2.8", "green", "high",
     "DP优化", ["线段树", "DP", "区间最值", "点修改"],
     "modeling_pattern", True, "线段树优化DP转移"),
    ("数据结构优化DP进阶：树状数组优化", "dp_opt_bit", "2.8", "green", "high",
     "DP优化", ["树状数组", "DP", "LIS", "偏序"],
     "modeling_pattern", True, "树状数组优化LIS等经典DP"),
    ("DP进阶：DP与生成函数", "dp_generating_function", "2.8", "red", "low",
     "DP与数学", ["生成函数", "DP", "多项式", "计数"],
     "theorem_or_property", False, "生成函数处理DP计数"),
    ("DP进阶：DP与矩阵乘法优化", "dp_matrix_optimization", "2.8", "green", "high",
     "DP优化", ["矩阵快速幂", "DP", "递推", "线性递推"],
     "modeling_pattern", True, "矩阵快速幂优化线性递推DP"),
    ("环形DP进阶", "dp_cycle_advanced", "2.8", "yellow", "medium",
     "环形DP", ["环形DP", "破环成链", "区间DP", "DP"],
     "core_concept", False, "环形DP通用处理技巧"),
    ("双状态DP进阶", "dp_dual_state", "2.8", "green", "high",
     "DP设计", ["DP", "双状态", "0/1状态", "分类讨论"],
     "modeling_pattern", True, "双状态DP处理交替选择"),
    ("DP进阶：后效性处理(高斯消元DP)", "dp_gaussian_elimination", "2.8", "yellow", "medium",
     "DP优化", ["DP", "高斯消元", "后效性", "概率DP"],
     "core_concept", False, "高斯消元解决DP后效性"),
    ("DP进阶：插头DP进阶(多回路)", "dp_plug_multi_loop", "2.8", "medium", "low",
     "插头DP", ["插头DP", "多回路", "轮廓线", "连通性"],
     "implementation_variant", False, "插头DP处理多回路问题"),
    ("DP进阶：旅行商问题(TSP)状压DP", "dp_tsp", "2.8", "green", "high",
     "状压DP", ["状压DP", "TSP", "Hamilton", "子集DP"],
     "core_concept", False, "TSP问题状压DP解法"),
    ("DP进阶：DAG上DP进阶", "dp_dag_advanced", "2.8", "green", "high",
     "DAG DP", ["DAG", "DP", "拓扑排序", "最长路"],
     "core_concept", False, "DAG上DP处理递推关系"),
    ("DP进阶：DP退火", "dp_annealing", "2.8", "red", "low",
     "DP交叉", ["模拟退火", "DP", "随机化", "优化"],
     "implementation_variant", False, "随机化优化DP尝试"),
    ("DP进阶：LIM", "dp_lim", "2.8", "red", "low",
     "DP极限", ["DP", "极限", "多项式", "优化"],
     "core_concept", False, "LIM(Lagrange Interpolation Method)"),
    ("DP进阶：凸优化技巧", "dp_convex_optimization", "2.8", "medium", "low",
     "DP优化", ["凸优化", "DP", "凸包", "WQS"],
     "core_concept", False, "凸优化技巧用于DP"),
    ("DP进阶：插头DP(轮廓线DP)", "dp_plug", "2.8", "yellow", "medium",
     "DP进阶", ["插头DP", "轮廓线", "状态压缩", "棋盘"],
     "core_concept", False, "插头DP处理棋盘连通性DP"),
]
for c in dp_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充DP知识覆盖")
dp_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {dp_count}")

# ============================================================
# THEME 4: 信奥数学 (40)
# ============================================================
T = "信奥数学"
TI = "math"

math_cands = [
    ("数论进阶：杜教筛", "math_dujiao_sieve", "4.1", "yellow", "medium",
     "数论积性函数", ["数论", "积性函数", "莫比乌斯", "狄利克雷卷积"],
     "core_concept", False, "杜教筛快速求积性函数前缀和"),
    ("数论进阶：Min_25筛", "math_min25_sieve", "4.1", "medium", "low",
     "数论", ["数论", "Min_25", "素数", "积性函数"],
     "core_concept", False, "Min_25筛是高级数论筛法"),
    ("数论进阶：洲阁筛", "math_zhou_sieve", "4.1", "red", "low",
     "数论", ["数论", "洲阁筛", "素数", "积性函数"],
     "core_concept", False, "洲阁筛是复杂筛法"),
    ("数论进阶：二次剩余(Cipolla算法)", "math_quadratic_residue", "4.1", "yellow", "medium",
     "数论", ["二次剩余", "Cipolla", "模运算", "勒让德符号"],
     "core_concept", False, "Cipolla算法求二次剩余"),
    ("数论进阶：原根与阶", "math_primitive_root_advanced", "4.1", "green", "high",
     "数论", ["原根", "阶", "欧拉函数", "模运算"],
     "core_concept", False, "原根与阶的性质和应用"),
    ("数论进阶：大步小步(BSGS)进阶", "math_bsgs_advanced", "4.1", "yellow", "medium",
     "数论", ["BSGS", "离散对数", "模方程", "哈希"],
     "core_concept", False, "BSGS求解离散对数问题"),
    ("数论进阶：扩展BSGS(exBSGS)", "math_exbsgs", "4.1", "yellow", "medium",
     "数论", ["BSGS", "exBSGS", "离散对数", "模不互质"],
     "core_concept", False, "exBSGS处理模数不互质情况"),
    ("数论进阶：中国剩余定理(CRT)进阶", "math_crt_advanced", "4.1", "green", "high",
     "数论", ["中国剩余定理", "CRT", "同余", "模方程组"],
     "core_concept", False, "CRT解模线性方程组"),
    ("数论进阶：扩展CRT(exCRT)", "math_excrt", "4.1", "green", "high",
     "数论", ["CRT", "exCRT", "模不互质", "扩展欧几里得"],
     "core_concept", False, "exCRT处理模数不互质"),
    ("数论进阶：Pollard-Rho进阶", "math_pollard_rho_advanced", "4.1", "yellow", "medium",
     "数论", ["Pollard-Rho", "Miller-Rabin", "大数分解", "随机化"],
     "core_concept", False, "Pollard-Rho大整数因子分解"),
    ("多项式：FFT进阶(三次变两次)", "poly_fft_advanced", "4.3", "yellow", "medium",
     "多项式", ["FFT", "复数", "卷积", "DFT"],
     "core_concept", False, "FFT三次变两次优化"),
    ("多项式：NTT(数论变换)", "poly_ntt", "4.3", "green", "high",
     "多项式", ["FFT", "NTT", "原根", "模数"],
     "core_concept", False, "NTT在模域下的快速傅里叶变换"),
    ("多项式：FNTT(分治NTT)", "poly_fntt", "4.3", "medium", "low",
     "多项式", ["NTT", "分治", "卷积", "CDQ"],
     "core_concept", False, "分治NTT处理自卷积"),
    ("多项式：多项式求逆", "poly_inverse", "4.3", "yellow", "medium",
     "多项式", ["多项式", "NTT", "求逆", "卷积"],
     "core_concept", False, "多项式求逆及其应用"),
    ("多项式：多项式ln/exp", "poly_ln_exp", "4.3", "medium", "low",
     "多项式", ["多项式", "ln", "exp", "微积分"],
     "core_concept", False, "多项式ln和exp运算"),
    ("多项式：多项式快速幂", "poly_fast_power", "4.3", "medium", "low",
     "多项式", ["多项式", "快速幂", "ln/exp", "卷积"],
     "core_concept", False, "多项式快速幂的ln/exp方法"),
    ("多项式：多项式多点求值", "poly_multi_point_eval", "4.3", "red", "low",
     "多项式", ["多项式", "求值", "NTT", "分治"],
     "core_concept", False, "多项式多点求值算法"),
    ("多项式：多项式快速插值", "poly_fast_interpolation", "4.3", "red", "low",
     "多项式", ["多项式", "插值", "NTT", "多点求值"],
     "core_concept", False, "多项式快速插值算法"),
    ("多项式：生成函数基础", "poly_generating_function_basics", "4.3", "yellow", "medium",
     "组合数学", ["生成函数", "多项式", "数列", "计数"],
     "core_concept", False, "生成函数解决组合计数"),
    ("多项式：指数型生成函数(EGF)", "poly_egf", "4.3", "medium", "low",
     "组合数学", ["EGF", "生成函数", "排列", "exp"],
     "core_concept", False, "指数型生成函数处理标号对象"),
    ("多项式：生成函数与DP", "poly_generating_function_dp", "4.3", "yellow", "medium",
     "组合数学", ["生成函数", "DP", "背包", "卷积"],
     "modeling_pattern", True, "生成函数优化DP背包"),
    ("组合计数进阶：容斥原理进阶", "combinatorics_inclusion_exclusion_advanced", "4.3", "green", "high",
     "组合数学", ["容斥原理", "组合计数", "集合", "子集"],
     "core_concept", False, "容斥原理在计数中的应用"),
    ("组合计数进阶：反演(莫比乌斯/二项式)", "combinatorics_mobius_inversion", "4.3", "green", "high",
     "组合数学", ["莫比乌斯反演", "二项式反演", "容斥", "数论"],
     "core_concept", False, "莫比乌斯反演与二项式反演"),
    ("组合计数进阶：CFS(计数公式系统)", "combinatorics_cfs", "4.3", "medium", "low",
     "组合数学", ["组合计数", "CFS", "递推", "公式"],
     "theorem_or_property", False, "组合计数公式系统"),
    ("组合计数进阶：Newton恒等式", "combinatorics_newton", "4.3", "red", "low",
     "组合数学", ["Newton", "幂和", "对称多项式", "恒等式"],
     "theorem_or_property", False, "Newton恒等式处理幂和"),
    ("概率论进阶：期望线性性应用", "probability_expectation_linearity", "4.6", "green", "high",
     "概率论", ["期望", "线性性", "概率", "DP"],
     "core_concept", True, "期望线性性是竞赛重要工具"),
    ("概率论进阶：全期望公式", "probability_total_expectation", "4.6", "yellow", "medium",
     "概率论", ["期望", "全期望", "条件期望", "递归"],
     "theorem_or_property", False, "全期望公式处理递推期望"),
    ("概率论进阶：随机化算法(蒙特卡洛)", "probability_monte_carlo", "4.6", "yellow", "medium",
     "随机化", ["蒙特卡洛", "随机化", "概率", "采样"],
     "core_concept", False, "蒙特卡洛方法"),
    ("概率论进阶：马尔可夫链进阶", "probability_markov_chain_advanced", "4.6", "medium", "low",
     "概率论", ["马尔可夫链", "转移", "稳态", "概率"],
     "core_concept", False, "马尔可夫链稳态分布"),
    ("数论进阶：Lucas定理进阶", "math_lucas_advanced", "4.1", "yellow", "medium",
     "数论组合", ["Lucas", "组合数", "模素数", "CRT"],
     "core_concept", False, "Lucas定理求大组合数模素数"),
    ("数论进阶：扩展Lucas", "math_exlucas", "4.1", "medium", "low",
     "数论组合", ["Lucas", "exLucas", "CRT", "阶乘"],
     "core_concept", False, "扩展Lucas处理模合数情形"),
    ("数论进阶：欧拉函数进阶", "math_euler_phi_advanced", "4.1", "yellow", "medium",
     "数论", ["欧拉函数", "积性函数", "欧拉定理", "降幂"],
     "core_concept", False, "欧拉函数的高级性质"),
    ("数论进阶：莫比乌斯反演进阶", "math_mobius_advanced", "4.1", "yellow", "medium",
     "数论", ["莫比乌斯", "数论分块", "整除", "积性函数"],
     "core_concept", False, "莫比乌斯反演与数论分块"),
    ("数论进阶：数论分块(整除分块)", "math_number_theory_block", "4.1", "green", "high",
     "数论", ["整除", "分块", "数论", "求和"],
     "core_concept", False, "数论分块O(sqrt(n))处理求和"),
    ("数论进阶：积性函数线性筛", "math_linear_sieve", "4.1", "green", "high",
     "数论", ["欧拉筛", "积性函数", "线性筛", "素数"],
     "core_concept", False, "线性筛求积性函数"),
    ("图论数学：Cayley定理", "math_cayley", "4.5", "yellow", "medium",
     "图论数学", ["Cayley", "生成树", "计数", "完全图"],
     "theorem_or_property", False, "Cayley定理：n^(n-2)棵生成树"),
    ("图论数学：Kirchhoff矩阵树定理进阶", "math_kirchhoff_advanced", "4.5", "yellow", "medium",
     "图论数学", ["矩阵树定理", "Kirchhoff", "生成树", "行列式"],
     "theorem_or_property", False, "Kirchhoff定理拓展应用"),
    ("线性代数进阶：线性基应用", "math_linear_basis_applications", "4.5", "green", "high",
     "线性代数", ["线性基", "异或", "极大独立集", "贪心"],
     "core_concept", False, "线性基处理异或相关问题"),
    ("离散数学：集合论应用", "math_set_theory_applications", "4.4", "yellow", "medium",
     "离散数学", ["集合", "关系", "偏序", "等价"],
     "core_concept", False, "集合论在OI竞赛中的直接应用"),
    ("离散数学：布尔代数与逻辑", "math_boolean_algebra", "4.4", "yellow", "medium",
     "离散数学", ["布尔代数", "逻辑", "真值表", "对偶"],
     "core_concept", False, "布尔代数与逻辑运算应用"),
]
for c in math_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充数学知识覆盖")
math_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {math_count}")

# ============================================================
# THEME 5: 基础算法扩展 (35)
# ============================================================
T = "基础算法扩展"
TI = "basic_algo"

basic_cands = [
    ("分治进阶：CDQ分治", "cdq_divide_conquer", "2.1", "green", "high",
     "分治", ["分治", "归并", "逆序对", "偏序"],
     "core_concept", False, "CDQ分治处理多维偏序"),
    ("分治进阶：点分治", "divide_conquer_on_tree_basic", "2.1", "green", "high",
     "树分治", ["分治", "树", "重心", "路径"],
     "core_concept", False, "点分治是树分治基础"),
    ("分治进阶：分治FFT", "divide_conquer_fft", "2.1", "yellow", "medium",
     "分治", ["FFT", "CDQ", "分治", "卷积"],
     "core_concept", False, "分治FFT处理自卷积"),
    ("分治进阶：分治NTT", "divide_conquer_ntt", "2.1", "medium", "low",
     "分治", ["NTT", "CDQ", "分治", "卷积"],
     "implementation_variant", False, "分治NTT是分治FFT模域版本"),
    ("倍增进阶：ST表上倍增", "binary_lifting_st", "2.1", "green", "high",
     "倍增", ["倍增", "ST表", "RMQ", "预处理"],
     "core_concept", False, "ST表是倍增思想经典应用"),
    ("倍增进阶：树上倍增进阶", "binary_lifting_tree_advanced", "2.1", "green", "high",
     "倍增", ["LCA", "倍增", "树", "祖先"],
     "core_concept", False, "树上倍增求LCA及扩展"),
    ("二分进阶：二分答案判定", "binary_search_answer", "2.2", "green", "high",
     "二分", ["二分", "答案", "判定", "贪心"],
     "modeling_pattern", True, "二分答案是最优化问题常见解法"),
    ("二分进阶：三分法", "ternary_search", "2.2", "green", "high",
     "二分", ["三分", "凸函数", "二分", "极值"],
     "core_concept", False, "三分法求单峰函数极值"),
    ("二分进阶：实数二分精度处理", "binary_search_float_precision", "2.2", "green", "high",
     "二分", ["二分", "实数", "精度", "浮点"],
     "modeling_pattern", True, "实数二分的精度控制技巧"),
    ("贪心进阶：反悔贪心", "greedy_regret", "2.3", "yellow", "medium",
     "贪心", ["贪心", "反悔", "堆", "后悔"],
     "core_concept", False, "反悔贪心解决可撤销贪心"),
    ("贪心进阶：交换论证法", "greedy_exchange_argument", "2.3", "yellow", "medium",
     "贪心", ["贪心", "交换论证", "排序", "不等式"],
     "modeling_pattern", True, "交换论证法是贪心正确性证明工具"),
    ("排序进阶：基数排序", "sort_radix_sort", "2.4", "green", "high",
     "排序", ["排序", "基数", "桶", "稳定排序"],
     "core_concept", False, "基数排序O(n)排序算法"),
    ("排序进阶：计数排序", "sort_counting_sort", "2.4", "green", "high",
     "排序", ["排序", "计数", "桶", "值域"],
     "core_concept", False, "计数排序O(n+k)整数排序"),
    ("排序进阶：拓扑排序(计数排序应用)", "sort_topological_count", "2.4", "yellow", "medium",
     "排序", ["计数排序", "拓扑排序", "桶", "逆序"],
     "implementation_variant", False, "计数排序在拓扑问题中的应用"),
    ("随机化算法：模拟退火", "randomized_simulated_annealing", "2.1", "yellow", "medium",
     "随机化", ["模拟退火", "随机化", "概率", "优化"],
     "core_concept", False, "模拟退火解决组合优化"),
    ("随机化算法：遗传算法", "randomized_genetic", "2.1", "red", "low",
     "随机化", ["遗传算法", "交叉", "变异", "进化"],
     "core_concept", False, "遗传算法在竞赛中的使用"),
    ("随机化算法：随机增量", "randomized_incremental", "2.1", "yellow", "medium",
     "随机化", ["随机", "增量", "期望", "概率"],
     "core_concept", False, "随机增量法求最小圆覆盖"),
    ("随机化算法：Treap随机化", "randomized_treap", "2.1", "green", "high",
     "随机化", ["Treap", "BST", "堆", "随机优先级"],
     "core_concept", False, "随机化平衡树Treap"),
    ("随机化算法：随机哈希", "randomized_hashing", "2.1", "green", "high",
     "随机化", ["哈希", "随机化", "碰撞", "同构"],
     "core_concept", True, "随机哈希防止构造数据"),
    ("搜索进阶：双向搜索", "search_bidirectional", "2.5", "green", "high",
     "搜索", ["BFS", "DFS", "双向", "meet-in-the-middle"],
     "core_concept", False, "双向搜索(meet-in-the-middle)"),
    ("搜索进阶：迭代加深搜索(IDA*)", "search_iterative_deepening", "2.5", "green", "high",
     "搜索", ["DFS", "剪枝", "启发式", "深度"],
     "core_concept", False, "IDA*是迭代加深与A*的结合"),
    ("搜索进阶：A*算法", "search_a_star", "2.5", "green", "high",
     "搜索", ["BFS", "启发式", "估价", "最短路"],
     "core_concept", False, "A*算法结合启发式搜索"),
    ("搜索进阶：DLX精确覆盖", "search_dlx", "2.5", "yellow", "medium",
     "搜索", ["DLX", "精确覆盖", "舞蹈链", "回溯"],
     "core_concept", False, "舞蹈链(DLX)解决精确覆盖问题"),
    ("搜索进阶：剪枝技巧", "search_pruning_techniques", "2.5", "green", "high",
     "搜索", ["DFS", "剪枝", "优化", "可行性"],
     "modeling_pattern", True, "搜索剪枝是竞赛必备技巧"),
    ("递归进阶：尾递归优化", "recursion_tail_optimization", "2.1", "yellow", "medium",
     "递归", ["递归", "尾递归", "迭代", "栈"],
     "core_concept", False, "尾递归的迭代化优化"),
    ("递归进阶：递归转迭代", "recursion_to_iteration", "2.1", "green", "high",
     "递归", ["递归", "栈模拟", "迭代", "DFS"],
     "modeling_pattern", True, "递归转迭代避免栈溢出"),
    ("递推进阶：线性递推(特征方程)", "recurrence_characteristic", "2.1", "yellow", "medium",
     "递推", ["递推", "特征方程", "线性递推", "矩阵"],
     "core_concept", False, "特征方程解线性递推"),
    ("递推进阶：BM算法(递推检测)", "recurrence_berlekamp_massey", "2.1", "medium", "low",
     "递推", ["Berlekamp-Massey", "递推", "线性递推", "插值"],
     "core_concept", False, "BM算法自动检测线性递推"),
    ("递推进阶：常系数线性递推优化", "recurrence_linear_opt", "2.1", "medium", "low",
     "递推", ["线性递推", "矩阵快速幂", "多项式取模", "优化"],
     "core_concept", False, "常系数线性递推的快速求解"),
    ("字符串基础进阶：字符串哈希进阶(双哈希)", "string_hash_double", "2.10", "green", "high",
     "字符串哈希", ["字符串哈希", "双哈希", "冲突", "子串"],
     "core_concept", False, "双哈希提高安全性"),
    ("字符串基础进阶：哈希表与滚动哈希", "string_hash_rolling", "2.10", "green", "high",
     "字符串哈希", ["滚动哈希", "子串", "字符串哈希", "滑动窗口"],
     "core_concept", False, "滚动哈希O(1)获取子串哈希"),
    ("字符串基础进阶：Border树", "string_border_tree", "2.10", "yellow", "medium",
     "KMP", ["KMP", "Border", "失配", "前缀函数"],
     "core_concept", False, "KMP自动机的Border树结构"),
    ("字符串基础进阶：Z算法(扩展KMP)", "string_z_algorithm_advanced", "2.10", "yellow", "medium",
     "Z算法", ["Z算法", "扩展KMP", "前缀匹配", "LCP"],
     "core_concept", False, "Z算法求每个后缀与模式串LCP"),
    ("字符串基础进阶：最小表示法", "string_minimal_rotation", "2.10", "green", "high",
     "最小表示法", ["最小表示法", "循环同构", "字符串", "同构"],
     "core_concept", False, "字符串最小表示法求循环同构"),
    ("二分进阶：答案判定技巧", "binary_answer_check", "2.2", "green", "high",
     "二分", ["二分", "答案", "验证", "判定函数"],
     "modeling_pattern", True, "二分答案的判定函数设计技巧"),
    ("贪心进阶：区间调度进阶", "greedy_interval_scheduling", "2.3", "green", "high",
     "贪心", ["区间调度", "贪心", "端点排序", "覆盖"],
     "modeling_pattern", True, "区间类问题的贪心解法系统总结"),
    ("排序进阶：外部排序", "sort_external", "2.4", "yellow", "medium",
     "排序", ["外部排序", "归并", "磁盘", "大数据"],
     "implementation_variant", False, "外部排序处理大规模数据"),
    ("随机化算法：随机排列", "randomized_permutation", "2.1", "yellow", "medium",
     "随机化", ["随机排列", "Fisher-Yates", "洗牌", "随机化"],
     "implementation_variant", False, "随机排列生成的正确方法"),
    ("搜索进阶：双向BFS优化", "search_bidirectional_bfs", "2.5", "green", "high",
     "搜索", ["BFS", "双向", "剪枝", "最短路"],
     "core_concept", False, "双向BFS的优化实现技巧"),
    ("搜索进阶：DFS序与回溯", "search_dfs_order", "2.5", "green", "high",
     "搜索", ["DFS", "顺序", "回溯", "树"],
     "modeling_pattern", True, "DFS序和回溯在搜索中的应用"),
]
# Fix: these basic_cands include some string ones, move them to string section later
basic_cands_fixed = [c for c in basic_cands if not c[2].startswith("2.10") and not c[2].startswith("3.8")]
for c in basic_cands_fixed:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充基础算法知识覆盖")
basic_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {basic_count}")

# ============================================================
# THEME 6: 字符串专题 (35) - remaining after moving from basic_algo
# ============================================================
T = "字符串专题"
TI = "string"

string_cands = [
    ("字符串基础进阶：字符串哈希进阶(双哈希)", "string_hash_double_final", "2.10", "green", "high",
     "字符串哈希", ["字符串哈希", "双哈希", "冲突", "子串"],
     "core_concept", False, "双哈希提高安全性和正确性"),
    ("字符串基础进阶：滚动哈希", "string_rolling_hash", "2.10", "green", "high",
     "字符串哈希", ["滚动哈希", "子串", "O(1)", "滑动窗口"],
     "core_concept", False, "滚动哈希O(1)子串哈希查询"),
    ("字符串基础进阶：Border树", "string_border_tree_final", "2.10", "yellow", "medium",
     "KMP", ["KMP", "Border", "前缀函数", "失配链"],
     "core_concept", False, "KMP自动机Border树结构"),
    ("字符串基础进阶：Z算法(扩展KMP)", "string_z_algorithm_final", "2.10", "yellow", "medium",
     "Z算法", ["Z算法", "扩展KMP", "前缀匹配", "LCP"],
     "core_concept", False, "Z算法O(n)求LCP"),
    ("字符串基础进阶：最小表示法", "string_min_rot_final", "2.10", "green", "high",
     "最小表示法", ["最小表示法", "循环同构", "字符串", "同构"],
     "core_concept", False, "最小表示法求循环同构"),
    ("字符串匹配进阶：多模式匹配(AC自动机)", "string_ac_automaton_advanced", "3.8", "green", "high",
     "AC自动机", ["AC自动机", "Trie", "失配", "多模式匹配"],
     "core_concept", False, "AC自动机处理多模式匹配"),
    ("字符串匹配进阶：AC自动机DP进阶", "string_ac_dp_advanced", "3.8", "yellow", "medium",
     "AC自动机", ["AC自动机", "DP", "自动机DP", "字符串"],
     "core_concept", False, "AC自动机上DP进阶"),
    ("字符串匹配进阶：AC自动机(fail树)", "string_ac_fail_tree", "3.8", "yellow", "medium",
     "AC自动机", ["AC自动机", "fail树", "DFS序", "树"],
     "core_concept", False, "AC自动机fail树的拓扑结构"),
    ("后缀结构进阶：后缀数组应用", "string_sa_applications", "3.8", "green", "high",
     "后缀数组", ["后缀数组", "LCP", "RMQ", "不同子串"],
     "core_concept", False, "后缀数组应用：不同子串数/LCP"),
    ("后缀结构进阶：后缀数组(height数组)", "string_sa_height", "3.8", "green", "high",
     "后缀数组", ["后缀数组", "height", "LCP", "RMQ"],
     "core_concept", False, "height数组是后缀数组核心"),
    ("后缀结构进阶：后缀自动机(SAM)进阶", "string_sam_applications", "3.8", "yellow", "medium",
     "后缀自动机", ["后缀自动机", "endpos", "子串", "parent树"],
     "core_concept", False, "SAM处理子串计数/出现次数"),
    ("后缀结构进阶：广义SAM", "string_sam_generalized_final", "3.8", "yellow", "medium",
     "后缀自动机", ["广义SAM", "多串", "Trie", "SAM"],
     "implementation_variant", False, "广义SAM处理多字符串问题"),
    ("后缀结构进阶：后缀树", "string_suffix_tree_final", "3.8", "medium", "low",
     "后缀树", ["后缀树", "后缀数组", "SAM", "线性构造"],
     "core_concept", False, "后缀树是后缀结构的理论抽象"),
    ("回文结构：回文自动机(PAM)", "string_pam_final", "3.8", "green", "high",
     "回文自动机", ["PAM", "回文", "不同回文", "回文后缀"],
     "core_concept", False, "PAM处理回文子串问题"),
    ("回文结构：Manacher进阶", "string_manacher_advanced", "2.10", "green", "high",
     "Manacher", ["Manacher", "回文", "最长回文", "中心扩展"],
     "core_concept", False, "Manacher算法O(n)回文串"),
    ("字符串处理：表达式求值", "string_expression_eval", "2.10", "green", "high",
     "字符串处理", ["栈", "后缀表达式", "递归", "运算符"],
     "core_concept", True, "表达式求值是字符串处理综合应用"),
    ("字符串处理：大数处理", "string_big_number", "2.10", "green", "high",
     "字符串处理", ["字符串", "大数", "高精度", "加法乘法"],
     "core_concept", False, "字符串实现大数处理"),
    ("字符串处理：正则表达式", "string_regex", "2.10", "red", "low",
     "字符串处理", ["正则", "匹配", "DP", "自动机"],
     "core_concept", False, "正则表达式在竞赛中的应用"),
    ("字符串处理：文本压缩", "string_text_compression", "2.10", "red", "low",
     "字符串处理", ["压缩", "Huffman", "LZ", "编码"],
     "core_concept", False, "文本压缩算法基础"),
    ("字符串问题：最长公共子串(LCS)", "string_lcs", "2.10", "green", "high",
     "字符串DP", ["DP", "LCS", "子串", "字符串"],
     "core_concept", False, "最长公共子串DP解法"),
    ("字符串问题：最长公共子序列(LCS)", "string_lcs_seq", "2.10", "green", "high",
     "字符串DP", ["DP", "子序列", "LCS", "序列"],
     "core_concept", False, "最长公共子序列多种解法"),
    ("字符串问题：编辑距离", "string_edit_distance", "2.10", "green", "high",
     "字符串DP", ["DP", "编辑距离", "Levenshtein", "字符串"],
     "core_concept", False, "编辑距离DP计算字符串差异"),
    ("字符串问题：最长回文子序列", "string_lps", "2.10", "yellow", "medium",
     "字符串DP", ["DP", "回文", "子序列", "区间DP"],
     "core_concept", False, "最长回文子序列区间DP"),
    ("字符串问题：最长重复子串", "string_lrs", "2.10", "yellow", "medium",
     "字符串问题", ["后缀数组", "重复", "最长", "LCP"],
     "core_concept", False, "最长重复子串后缀数组解法"),
    ("字符串匹配：Rabin-Karp算法", "string_rk", "2.10", "green", "high",
     "字符串匹配", ["Rabin-Karp", "哈希", "模式匹配", "滚动哈希"],
     "core_concept", False, "Rabin-Karp随机化匹配算法"),
    ("字符串匹配：Shift-Or算法", "string_shift_or", "2.10", "medium", "low",
     "字符串匹配", ["Shift-Or", "位运算", "模式匹配", "模糊匹配"],
     "core_concept", False, "Shift-Or位运算加速匹配"),
    ("字符串匹配：BM算法", "string_bm", "2.10", "yellow", "medium",
     "字符串匹配", ["BM", "坏字符", "好后缀", "模式匹配"],
     "core_concept", False, "Boyer-Moore高效匹配算法"),
    ("Trie进阶：可持久化Trie", "trie_persistent", "3.8", "green", "high",
     "Trie", ["Trie", "可持久化", "异或", "二进制"],
     "core_concept", False, "可持久化Trie处理异或最值"),
    ("Trie进阶：0-1 Trie", "trie_01", "3.8", "green", "high",
     "Trie", ["Trie", "二进制", "异或", "最大异或"],
     "core_concept", False, "0-1 Trie处理异或相关问题"),
    ("Trie进阶：Trie与AC自动机", "trie_ac_automaton", "3.8", "green", "high",
     "Trie", ["Trie", "AC自动机", "多模式", "失配指针"],
     "core_concept", False, "Trie是AC自动机的基础结构"),
    ("字符串建模：字符串问题建模技巧", "string_modeling", "2.10", "yellow", "medium",
     "字符串建模", ["字符串", "建模", "模式", "问题转化"],
     "modeling_pattern", True, "字符串问题的建模方法总结"),
    ("字符串技巧：滚动哈希进阶应用", "string_rolling_hash_apps", "2.10", "green", "high",
     "字符串哈希", ["滚动哈希", "回文检测", "模式匹配", "LCP"],
     "modeling_pattern", True, "滚动哈希的多种竞赛应用"),
    ("后缀结构：后缀数组DC3构造", "string_sa_dc3", "3.8", "medium", "low",
     "后缀数组", ["后缀数组", "DC3", "线性构造", "分治"],
     "implementation_variant", False, "DC3算法O(n)构建后缀数组"),
    ("字符串匹配：Finite Automaton", "string_fa", "2.10", "medium", "low",
     "字符串匹配", ["有限自动机", "模式匹配", "自动机", "转移"],
     "core_concept", False, "有限自动机字符串匹配基础"),
    ("字符串匹配：Aho-Corasick加强", "string_ac_advanced", "3.8", "yellow", "medium",
     "AC自动机", ["AC自动机", "DP", "拓扑", "自动机优化"],
     "core_concept", False, "AC自动机的DP和fail树优化"),
]
for c in string_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充字符串知识覆盖")
string_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {string_count}")

# ============================================================
# THEME 7: STL与常用库细节 (30)
# ============================================================
T = "STL与常用库细节"
TI = "stl"

stl_cands = [
    ("STL容器：deque底层实现", "stl_deque_impl", "2.9", "green", "high",
     "STL容器", ["deque", "双端队列", "分段", "迭代器"],
     "core_concept", False, "deque分段数组结构"),
    ("STL容器：priority_queue底层(堆)", "stl_pq_heap", "2.9", "green", "high",
     "STL容器", ["priority_queue", "堆", "二叉堆", "比较器"],
     "core_concept", False, "优先队列底层堆实现"),
    ("STL容器：set/multiset/map底层(红黑树)", "stl_rb_tree", "2.9", "green", "high",
     "STL容器", ["set", "map", "红黑树", "平衡树"],
     "core_concept", False, "红黑树是set/map底层结构"),
    ("STL容器：unordered_set/map底层(哈希表)", "stl_hash_table", "2.9", "green", "high",
     "STL容器", ["unordered_set", "哈希表", "桶", "冲突"],
     "core_concept", False, "哈希表是无序容器底层结构"),
    ("STL容器：bitset使用", "stl_bitset", "2.9", "green", "high",
     "STL容器", ["bitset", "位运算", "压缩", "布尔"],
     "core_concept", False, "bitset位压缩容器"),
    ("STL容器：array/forward_list", "stl_array_fwd_list", "2.9", "green", "high",
     "STL容器", ["array", "forward_list", "C++11", "线性容器"],
     "core_concept", False, "C++11新增容器array/forward_list"),
    ("STL算法：sort底层(introspect)", "stl_sort_intro", "2.9", "green", "high",
     "STL算法", ["sort", "introspect", "快排", "堆排"],
     "core_concept", False, "sort是混合排序(introspect)"),
    ("STL算法：nth_element原理", "stl_nth_element", "2.9", "green", "high",
     "STL算法", ["nth_element", "快速选择", "O(n)", "中位数"],
     "core_concept", False, "nth_element快速选择算法"),
    ("STL算法：lower_bound/upper_bound底层", "stl_binary_search_impl", "2.9", "green", "high",
     "STL算法", ["lower_bound", "upper_bound", "二分", "有序"],
     "core_concept", False, "二分查找在有序序列上的实现"),
    ("STL算法：next_permutation原理", "stl_next_perm", "2.9", "green", "high",
     "STL算法", ["next_permutation", "排列", "算法", "字典序"],
     "core_concept", False, "next_permutation生成下一排列"),
    ("STL算法：merge/inplace_merge", "stl_merge", "2.9", "green", "high",
     "STL算法", ["merge", "归并", "有序", "原地合并"],
     "core_concept", False, "merge归并两个有序序列"),
    ("STL算法：unique/remove/erase惯用法", "stl_unique_erase", "2.9", "green", "high",
     "STL算法", ["unique", "remove", "erase", "去重"],
     "modeling_pattern", True, "unique+erase去重惯用法"),
    ("STL函数对象：lambda表达式进阶", "stl_lambda_advanced", "2.9", "green", "high",
     "STL函数对象", ["lambda", "捕获", "泛型", "C++14"],
     "core_concept", False, "lambda表达式完整用法"),
    ("STL函数对象：function/bind", "stl_function_bind", "2.9", "yellow", "medium",
     "STL函数对象", ["function", "bind", "函数包装", "回调"],
     "core_concept", False, "function/bind函数式编程"),
    ("STL函数对象：仿函数与比较器", "stl_functor_comp", "2.9", "green", "high",
     "STL函数对象", ["仿函数", "比较器", "operator()", "优先级"],
     "core_concept", False, "仿函数作为STL比较器"),
    ("STL迭代器：迭代器类型", "stl_iterator_types", "2.9", "green", "high",
     "STL迭代器", ["迭代器", "随机访问", "双向", "输入输出"],
     "core_concept", False, "STL迭代器分类体系"),
    ("STL迭代器：istream_iterator/ostream_iterator", "stl_stream_iter", "2.9", "yellow", "medium",
     "STL迭代器", ["istream_iterator", "ostream_iterator", "流", "迭代器"],
     "core_concept", False, "流迭代器在竞赛中的应用"),
    ("STL迭代器：back_inserter/inserter", "stl_insert_iter", "2.9", "green", "high",
     "STL迭代器", ["back_inserter", "inserter", "插入", "赋值"],
     "core_concept", False, "插入迭代器"),
    ("STL工具：pair/tuple", "stl_pair_tuple", "2.9", "green", "high",
     "STL工具", ["pair", "tuple", "结构化绑定", "C++17"],
     "core_concept", False, "pair/tuple/C++17结构化绑定"),
    ("STL工具：optional/variant/any(C++17)", "stl_optional_variant", "2.9", "yellow", "medium",
     "STL工具", ["optional", "variant", "any", "C++17"],
     "core_concept", False, "C++17新增类型安全容器"),
    ("STL工具：string_view(C++17)", "stl_string_view", "2.9", "yellow", "medium",
     "STL工具", ["string_view", "字符串视图", "C++17", "零拷贝"],
     "core_concept", False, "string_view零拷贝子串引用"),
    ("STL算法：partial_sort/stable_sort", "stl_partial_stable", "2.9", "green", "high",
     "STL算法", ["partial_sort", "stable_sort", "排序", "部分排序"],
     "core_concept", False, "partial_sort部分排序"),
    ("STL算法：minmax_element/accumulate", "stl_minmax_accum", "2.9", "green", "high",
     "STL算法", ["minmax_element", "accumulate", "数值", "极值"],
     "core_concept", False, "minmax_element同时求最大最小"),
    ("STL算法：iota/fill_n/generate", "stl_iota_generate", "2.9", "green", "high",
     "STL算法", ["iota", "fill_n", "generate", "数值生成"],
     "core_concept", False, "iota递增填充"),
    ("STL容器适配器：stack/queue/priority_queue", "stl_adapter", "2.9", "green", "high",
     "STL容器", ["stack", "queue", "priority_queue", "适配器"],
     "core_concept", False, "STL容器适配器"),
    ("STL算法：copy/transform惯用法", "stl_copy_transform", "2.9", "green", "high",
     "STL算法", ["copy", "transform", "复制", "转换"],
     "modeling_pattern", True, "copy/transform通用数据操作"),
    ("STL算法：remove_if/partition", "stl_remove_partition", "2.9", "yellow", "medium",
     "STL算法", ["remove_if", "partition", "筛选", "划分"],
     "core_concept", False, "remove_if条件删除"),
    ("STL算法：set_union/intersection/difference", "stl_set_ops", "2.9", "green", "high",
     "STL算法", ["set_union", "set_intersection", "集合运算", "有序"],
     "core_concept", False, "有序序列的集合运算"),
    ("STL性能：vector扩容机制", "stl_vector_growth", "2.9", "green", "high",
     "STL性能", ["vector", "reserve", "扩容", "摊销"],
     "core_concept", False, "vector动态扩容策略"),
    ("STL性能：emplace_back vs push_back", "stl_emplace_push", "2.9", "green", "high",
     "STL性能", ["emplace_back", "push_back", "移动语义", "构造"],
     "core_concept", False, "emplace_back原地构造更高效率"),
]
for c in stl_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充STL与库细节知识覆盖")
stl_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {stl_count}")

# ============================================================
# THEME 8: C++语法高级细节 (25)
# ============================================================
T = "C++语法高级细节"
TI = "cpp"

cpp_cands = [
    ("C++内存模型：栈与堆", "cpp_memory_model", "2.9", "green", "high",
     "C++基础", ["栈", "堆", "内存", "生命周期"],
     "core_concept", False, "C++栈与堆内存管理"),
    ("C++引用：左值/右值引用", "cpp_lvalue_rvalue", "2.9", "yellow", "medium",
     "C++11", ["左值", "右值", "移动语义", "&&"],
     "core_concept", False, "左值/右值引用与移动语义"),
    ("C++11：移动语义与完美转发", "cpp_move_forward", "2.9", "yellow", "medium",
     "C++11", ["移动语义", "std::move", "完美转发", "forward"],
     "core_concept", False, "移动语义与完美转发"),
    ("C++11：auto/decltype类型推导", "cpp_auto_decltype", "2.9", "green", "high",
     "C++11", ["auto", "decltype", "类型推导", "模板"],
     "core_concept", False, "auto/decltype类型推导规则"),
    ("C++11：范围for循环", "cpp_range_for", "2.9", "green", "high",
     "C++11", ["for", "范围", "迭代", "容器"],
     "core_concept", False, "范围for循环遍历容器"),
    ("C++11：nullptr与智能指针", "cpp_nullptr_smart_ptr", "2.9", "green", "high",
     "C++11", ["nullptr", "shared_ptr", "unique_ptr", "内存"],
     "core_concept", False, "nullptr与三种智能指针"),
    ("C++11：override/final/default/delete", "cpp_override_final", "2.9", "green", "high",
     "C++11", ["override", "final", "default", "delete"],
     "core_concept", False, "特殊成员函数控制"),
    ("C++14：泛型lambda/返回值推导", "cpp_lambda_cpp14", "2.9", "yellow", "medium",
     "C++14", ["lambda", "泛型", "auto", "推导"],
     "core_concept", False, "C++14增强的lambda"),
    ("C++17：if constexpr", "cpp_if_constexpr", "2.9", "yellow", "medium",
     "C++17", ["if constexpr", "编译期", "模板", "分支"],
     "core_concept", False, "编译期条件分支if constexpr"),
    ("C++17：结构化绑定", "cpp_structured_binding", "2.9", "green", "high",
     "C++17", ["结构化绑定", "tuple", "pair", "解包"],
     "core_concept", False, "结构化绑定解包pair/tuple"),
    ("C++17：折叠表达式", "cpp_fold_expression", "2.9", "medium", "low",
     "C++17", ["折叠", "变参模板", "...,", "化简"],
     "core_concept", False, "变参模板折叠表达式"),
    ("C++20：概念(concept)", "cpp_concept", "2.9", "red", "low",
     "C++20", ["concept", "requires", "模板约束", "类型"],
     "core_concept", False, "C++20概念约束模板"),
    ("C++20：范围(range)库", "cpp_ranges", "2.9", "red", "low",
     "C++20", ["ranges", "视图", "管道", "惰性求值"],
     "core_concept", False, "C++20范围库"),
    ("C++模板：特化与偏特化", "cpp_template_specialize", "2.9", "yellow", "medium",
     "C++模板", ["特化", "偏特化", "模板", "类型"],
     "core_concept", False, "模板特化与偏特化"),
    ("C++模板：SFINAE", "cpp_sfinae", "2.9", "medium", "low",
     "C++模板", ["SFINAE", "enable_if", "模板", "重载"],
     "core_concept", False, "SFINAE模板匹配机制"),
    ("C++模板：变参模板", "cpp_variadic_template", "2.9", "yellow", "medium",
     "C++模板", ["变参模板", "...,", "包展开", "递归"],
     "core_concept", False, "变参模板处理不定参数"),
    ("C++运算符重载：输入输出重载", "cpp_io_overload", "2.9", "green", "high",
     "C++特性", ["运算符重载", "cin", "cout", "友元"],
     "core_concept", False, "自定义类型的IO运算符重载"),
    ("C++运算符重载：类型转换", "cpp_type_conversion", "2.9", "green", "high",
     "C++特性", ["类型转换", "implicit", "explicit", "转换运算符"],
     "core_concept", False, "类型转换运算符重载"),
    ("C++异常：异常安全编程", "cpp_exception_safety", "2.9", "yellow", "medium",
     "C++特性", ["异常", "捕获", "noexcept", "RAII"],
     "core_concept", False, "异常安全的RAII编程"),
    ("C++特性：constexpr与编译期计算", "cpp_constexpr", "2.9", "yellow", "medium",
     "C++11", ["constexpr", "编译期", "常量", "constexpr函数"],
     "core_concept", False, "constexpr编译期计算"),
    ("C++特性：inline与内联优化", "cpp_inline", "2.9", "green", "high",
     "C++基础", ["inline", "内联", "ODR", "链接"],
     "core_concept", False, "inline函数内联优化"),
    ("C++特性：volatile/mutable", "cpp_volatile_mutable", "2.9", "green", "high",
     "C++基础", ["volatile", "mutable", "const", "内存"],
     "core_concept", False, "volatile/mutable修饰符"),
    ("C++编译：头文件与编译单元", "cpp_compile_units", "2.9", "green", "high",
     "C++基础", ["头文件", "编译单元", "链接", "ODR"],
     "core_concept", False, "头文件与编译单元关系"),
    ("C++编译：预处理器与宏", "cpp_preprocessor_macro", "2.9", "green", "high",
     "C++基础", ["预处理器", "#define", "宏", "条件编译"],
     "core_concept", False, "预处理器宏定义与条件编译"),
    ("C++特性：位域与联合体", "cpp_bitfield_union", "2.9", "green", "high",
     "C++基础", ["位域", "union", "内存对齐", "压缩"],
     "core_concept", False, "位域与联合体实现数据压缩"),
]
for c in cpp_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充C++语法高级细节")
cpp_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {cpp_count}")

# ============================================================
# THEME 9: 编程技巧 (25)
# ============================================================
T = "编程技巧"
TI = "skills"

skills_cands = [
    ("IO优化：快读快写模板", "skill_fast_io", "2.9", "green", "high",
     "IO优化", ["快读", "快写", "getchar", "putchar"],
     "implementation_variant", False, "自定义快读快写提高IO速度"),
    ("IO优化：关闭同步流", "skill_ios_sync", "2.9", "green", "high",
     "IO优化", ["ios", "sync", "tie", "cin"],
     "implementation_variant", False, "关闭cin/cout同步提高速度"),
    ("IO优化：文件读写重定向", "skill_file_io", "2.9", "green", "high",
     "IO优化", ["freopen", "文件IO", "重定向", "竞赛"],
     "implementation_variant", False, "freopen文件输入输出重定向"),
    ("性能优化：编译优化选项", "skill_compile_opt", "2.9", "green", "high",
     "性能优化", ["O2", "编译优化", "g++", "速度"],
     "core_concept", False, "O2/O3编译优化"),
    ("性能优化：内存对齐与缓存", "skill_memory_align", "2.9", "yellow", "medium",
     "性能优化", ["内存对齐", "缓存", "结构体", "性能"],
     "core_concept", False, "内存对齐对性能的影响"),
    ("性能优化：循环展开与内联", "skill_loop_unroll", "2.9", "yellow", "medium",
     "性能优化", ["循环展开", "内联", "指令", "流水线"],
     "implementation_variant", False, "循环展开优化"),
    ("性能优化：指针与数组性能差异", "skill_ptr_array_perf", "2.9", "green", "high",
     "性能优化", ["指针", "数组", "索引", "速度"],
     "core_concept", False, "指针与数组在不同场景下的性能差异"),
    ("代码组织：namespace使用", "skill_namespace", "2.9", "green", "high",
     "代码风格", ["namespace", "命名空间", "冲突", "std"],
     "core_concept", False, "合理使用namespace避免命名冲突"),
    ("代码组织：头文件包含与guard", "skill_header_guard", "2.9", "green", "high",
     "代码风格", ["#pragma once", "头文件保护", "include", "循环"],
     "core_concept", False, "头文件保护避免重复包含"),
    ("代码组织：using与typedef最佳实践", "skill_using_typedef", "2.9", "green", "high",
     "代码风格", ["using", "typedef", "类型别名", "可读性"],
     "modeling_pattern", True, "using/typedef最佳实践"),
    ("调试技巧：assert使用", "skill_assert", "2.9", "green", "high",
     "调试技巧", ["assert", "断言", "调试", "验证"],
     "modeling_pattern", True, "assert在竞赛调试中的使用"),
    ("调试技巧：静态断言(static_assert)", "skill_static_assert", "2.9", "yellow", "medium",
     "调试技巧", ["static_assert", "编译期", "断言", "模板"],
     "core_concept", False, "编译期断言static_assert"),
    ("调试技巧：条件编译(debug/release)", "skill_define_debug", "2.9", "green", "high",
     "调试技巧", ["#ifdef", "DEBUG", "条件编译", "发布"],
     "modeling_pattern", True, "条件编译区分调试与发布模式"),
    ("代码安全：整数溢出检测", "skill_int_overflow", "2.9", "green", "high",
     "代码安全", ["整数溢出", "__int128", "long long", "安全检查"],
     "core_concept", True, "整数溢出问题是竞赛常见bug"),
    ("代码安全：数组越界检查", "skill_array_bounds", "2.9", "green", "high",
     "代码安全", ["数组越界", "vector", "at()", "栈破坏"],
     "core_concept", True, "数组越界检查与防护"),
    ("代码安全：野指针与空指针", "skill_null_ptr", "2.9", "green", "high",
     "代码安全", ["野指针", "空指针", "悬垂", "内存"],
     "core_concept", True, "野指针问题是常见运行时错误"),
    ("代码复用：函数化封装", "skill_function_encap", "2.9", "green", "high",
     "代码风格", ["函数", "封装", "模块", "可复用"],
     "modeling_pattern", True, "代码函数化封装提高可读性"),
    ("代码复用：模板化编程", "skill_template_code", "2.9", "green", "high",
     "代码风格", ["模板", "泛型", "代码复用", "类型无关"],
     "modeling_pattern", True, "模板实现通用算法"),
    ("代码复用：常用宏定义", "skill_macro_tips", "2.9", "green", "high",
     "代码风格", ["#define", "for", "rep", "宏"],
     "implementation_variant", False, "常用宏定义简化代码"),
    ("代码复用：函数指针与回调", "skill_func_ptr", "2.9", "yellow", "medium",
     "代码风格", ["函数指针", "回调", "比较器", "策略"],
     "core_concept", False, "函数指针实现策略模式"),
    ("时间优化：clock计时", "skill_clock_timing", "2.9", "green", "high",
     "调试技巧", ["clock", "计时", "性能", "超时检测"],
     "implementation_variant", False, "clock()函数测量程序运行时间"),
    ("时间优化：rdtsc指令", "skill_rdtsc", "2.9", "red", "low",
     "调试技巧", ["rdtsc", "计时", "指令", "纳秒"],
     "core_concept", False, "rdtsc纳秒级计时"),
    ("STL技巧：reserve预分配", "skill_reserve", "2.9", "green", "high",
     "STL技巧", ["reserve", "vector", "预分配", "效率"],
     "modeling_pattern", True, "reserve预分配避免动态扩容"),
    ("STL技巧：swap技巧", "skill_swap_trick", "2.9", "green", "high",
     "STL技巧", ["swap", "vector", "shrink_to_fit", "释放"],
     "modeling_pattern", True, "swap技巧释放vector内存"),
    ("编码规范：命名规范与注释", "skill_naming_style", "2.9", "green", "high",
     "代码风格", ["命名规范", "注释", "可读性", "维护"],
     "modeling_pattern", True, "一致的命名规范提高代码可读性"),
]
for c in skills_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充编程技巧知识覆盖")
skills_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {skills_count}")

# ============================================================
# THEME 10: 题型建模方法 (30)
# ============================================================
T = "题型建模方法"
TI = "modeling"

modeling_cands = [
    ("建模方法：最优化问题建模", "model_optimization", "2.9", "yellow", "medium",
     "建模基础", ["最优化", "建模", "目标函数", "约束"],
     "modeling_pattern", True, "竞赛最优化问题的通用建模方法"),
    ("建模方法：决策问题建模", "model_decision", "2.9", "yellow", "medium",
     "建模基础", ["决策", "可行解", "二分", "验证"],
     "modeling_pattern", True, "决策问题转化为验证问题"),
    ("建模方法：计数问题建模", "model_counting", "2.9", "yellow", "medium",
     "建模基础", ["计数", "组合", "排列", "分类讨论"],
     "modeling_pattern", True, "计数问题的分类与DP建模"),
    ("建模方法：构造问题建模", "model_construction", "2.9", "yellow", "medium",
     "建模基础", ["构造", "归纳", "模式构造", "特例"],
     "modeling_pattern", True, "构造类问题的从特殊到一般建模"),
    ("建模方法：交互问题建模", "model_interactive", "2.9", "yellow", "medium",
     "建模基础", ["交互", "查询", "反馈", "二分"],
     "modeling_pattern", True, "交互式问题的建模与策略设计"),
    ("建模方法：离线处理建模", "model_offline", "2.9", "yellow", "medium",
     "建模基础", ["离线", "CDQ", "分治", "排序"],
     "modeling_pattern", True, "离线处理思想将动态问题转化为静态"),
    ("建模方法：在线转离线", "model_online_to_offline", "2.9", "yellow", "medium",
     "建模基础", ["在线", "离线", "预处理", "批处理"],
     "modeling_pattern", True, "在线问题离线化的常见技巧"),
    ("建模方法：分治建模", "model_divide_conquer", "2.9", "yellow", "medium",
     "建模基础", ["分治", "划分", "合并", "递归"],
     "modeling_pattern", True, "分治思想在建模中的应用"),
    ("建模方法：增量处理建模", "model_incremental", "2.9", "yellow", "medium",
     "建模基础", ["增量", "维护", "在线", "更新"],
     "modeling_pattern", True, "增量式处理数据变化"),
    ("建模方法：等效转换", "model_equivalence", "2.9", "yellow", "medium",
     "建模基础", ["转换", "等价", "同构", "简化"],
     "modeling_pattern", True, "问题等效转化简化复杂度"),
    ("建模方法：正难则反", "model_reverse_thinking", "2.9", "green", "high",
     "建模基础", ["补集", "逆向", "排除", "差分"],
     "modeling_pattern", True, "正难则反的逆向思维建模"),
    ("建模方法：二分答案建模", "model_binary_answer", "2.9", "green", "high",
     "建模基础", ["二分答案", "验证", "最优化", "可行性"],
     "modeling_pattern", True, "二分答案将最优化转可行性"),
    ("建模方法：倍增思想", "model_binary_lifting", "2.9", "green", "high",
     "建模基础", ["倍增", "二进制", "LCA", "ST表"],
     "modeling_pattern", True, "倍增思想在多种场景的应用"),
    ("建模方法：差分约束建模", "model_diff_constraint", "2.9", "yellow", "medium",
     "建模基础", ["差分约束", "最短路", "不等式", "SPFA"],
     "modeling_pattern", True, "差分约束将不等式转化为图论"),
    ("建模方法：前缀和与差分扩展", "model_prefix_diff", "2.9", "green", "high",
     "建模基础", ["前缀和", "差分", "二维", "子矩阵"],
     "modeling_pattern", True, "前缀和与差分的多维扩展应用"),
    ("建模方法：双指针/滑动窗口建模", "model_two_pointers", "2.9", "green", "high",
     "建模基础", ["双指针", "滑动窗口", "单调", "区间"],
     "modeling_pattern", True, "双指针和滑动窗口模式的建模"),
    ("建模方法：离散化建模", "model_discretization", "2.9", "green", "high",
     "建模基础", ["离散化", "压缩", "映射", "值域"],
     "modeling_pattern", True, "离散化将大规模值域映射到小范围"),
    ("建模方法：折半搜索(meet-in-the-middle)", "model_meet_in_the_middle", "2.9", "green", "high",
     "建模基础", ["折半搜索", "meet-in-the-middle", "子集", "状态压缩"],
     "modeling_pattern", True, "折半搜索将指数级复杂度减半"),
    ("建模方法：状态压缩建模", "model_bitmask_dp", "2.9", "yellow", "medium",
     "建模基础", ["状压", "二进制", "子集", "DP"],
     "modeling_pattern", True, "状态压缩处理组合最优化问题"),
    ("建模方法：贪心建模证明", "model_greedy_proof", "2.9", "yellow", "medium",
     "建模基础", ["贪心", "证明", "交换论证", "反证"],
     "modeling_pattern", True, "贪心算法的正确性证明方法"),
    ("建模方法：图论建模技巧", "model_graph_construction", "2.9", "yellow", "medium",
     "建模基础", ["图论", "建图", "虚拟节点", "分层图"],
     "modeling_pattern", True, "图论问题的高级建图技巧"),
    ("建模方法：网络流建模", "model_network_flow", "2.9", "yellow", "medium",
     "建模基础", ["网络流", "最大流", "最小割", "费用流"],
     "modeling_pattern", True, "网络流问题建模技巧"),
    ("建模方法：博弈论建模", "model_game_theory", "2.9", "yellow", "medium",
     "建模基础", ["博弈论", "SG函数", "Nim", "公平组合"],
     "modeling_pattern", True, "博弈论问题的SG函数建模"),
    ("建模方法：矩阵乘法建模", "model_matrix_mult", "2.9", "yellow", "medium",
     "建模基础", ["矩阵", "递推", "转移矩阵", "加速"],
     "modeling_pattern", True, "矩阵快速幂加速递推建模"),
    ("建模方法：概率期望建模", "model_prob_exp", "2.9", "yellow", "medium",
     "建模基础", ["概率", "期望", "DP", "全概率"],
     "modeling_pattern", True, "概率期望问题的DP建模"),
    ("建模方法：组合数学建模", "model_combinatorics", "2.9", "yellow", "medium",
     "建模基础", ["组合", "排列", "容斥", "递推"],
     "modeling_pattern", True, "组合计数问题的数学建模"),
    ("建模方法：数论建模", "model_number_theory", "2.9", "yellow", "medium",
     "建模基础", ["数论", "模运算", "同余", "素数"],
     "modeling_pattern", True, "数论问题的数学建模方法"),
    ("建模方法：数据范围分析", "model_scale_analysis", "2.9", "green", "high",
     "建模基础", ["数据范围", "复杂度", "算法选择", "限制"],
     "modeling_pattern", True, "根据数据范围确定算法复杂度"),
    ("建模方法：特殊性质利用", "model_special_property", "2.9", "green", "high",
     "建模基础", ["特殊性质", "单调性", "对称性", "周期性"],
     "modeling_pattern", True, "利用问题特殊性质降低复杂度"),
    ("建模方法：暴力与优化", "model_brute_opt", "2.9", "green", "high",
     "建模基础", ["暴力", "剪枝", "优化", "分块"],
     "modeling_pattern", True, "从暴力到优化的系统方法"),
]
for c in modeling_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充题型建模方法知识覆盖")
modeling_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {modeling_count}")

# ============================================================
# THEME 11: 比赛相关知识 (15)
# ============================================================
T = "比赛相关知识"
TI = "contest"

contest_cands = [
    ("比赛规则：NOI系列赛制", "contest_noi_rules", "2.9", "green", "high",
     "竞赛基础", ["NOI", "赛制", "IOI", "提交"],
     "core_concept", False, "NOI系列竞赛赛制与评分规则"),
    ("比赛规则：ACM赛制", "contest_acm_rules", "2.9", "green", "high",
     "竞赛基础", ["ACM", "ICPC", "组队", "罚时"],
     "core_concept", False, "ACM/ICPC赛制与罚时规则"),
    ("比赛规则：OI与ACM区别", "contest_oi_vs_acm", "2.9", "green", "high",
     "竞赛基础", ["OI", "ACM", "区别", "策略"],
     "core_concept", False, "OI/ACM赛制的策略差异"),
    ("比赛策略：时间分配策略", "contest_time_manage", "2.9", "yellow", "medium",
     "竞赛策略", ["时间分配", "解题顺序", "权衡", "全局"],
     "modeling_pattern", True, "竞赛时间分配与解题顺序策略"),
    ("比赛策略：题目难度识别", "contest_difficulty_ident", "2.9", "yellow", "medium",
     "竞赛策略", ["难度评估", "读题", "预估", "样例"],
     "modeling_pattern", True, "快速识别题目难度的技巧"),
    ("比赛策略：暴力与正解权衡", "contest_violence_balance", "2.9", "yellow", "medium",
     "竞赛策略", ["暴力", "正解", "部分分", "权衡"],
     "modeling_pattern", True, "暴力拿部分分与正解的时间权衡"),
    ("比赛策略：部分分策略", "contest_partial_score", "2.9", "yellow", "medium",
     "竞赛策略", ["部分分", "子任务", "暴力", "特殊性质"],
     "modeling_pattern", True, "子任务部分分的最大化策略"),
    ("比赛技巧：对拍调试", "contest_duipai", "2.9", "green", "high",
     "竞赛技巧", ["对拍", "暴力", "验证", "正确性"],
     "modeling_pattern", True, "对拍是竞赛最可靠调试方法"),
    ("比赛技巧：批量数据测试", "contest_batch_test", "2.9", "green", "high",
     "竞赛技巧", ["批量测试", "脚本", "自动", "验证"],
     "implementation_variant", False, "批量自动化测试程序"),
    ("比赛技巧：常见陷阱", "contest_common_traps", "2.9", "green", "high",
     "竞赛技巧", ["陷阱", "边界", "特殊值", "输入"],
     "core_concept", True, "竞赛中常见的陷阱与注意事项"),
    ("比赛技巧：猜结论与打表", "contest_guess_table", "2.9", "yellow", "medium",
     "竞赛技巧", ["打表", "找规律", "猜想", "验证"],
     "modeling_pattern", True, "通过打表/猜结论辅助解题"),
    ("比赛心理：压力管理", "contest_stress_mgmt", "2.9", "yellow", "medium",
     "竞赛心理", ["心理", "压力", "情绪", "注意力"],
     "core_concept", False, "竞赛中的心理调节与压力管理"),
    ("比赛心理：复盘总结", "contest_review", "2.9", "green", "high",
     "竞赛心理", ["复盘", "总结", "错题", "提高"],
     "modeling_pattern", True, "赛后复盘总结提升技巧"),
    ("比赛工具：本地环境配置", "contest_env_setup", "2.9", "green", "high",
     "竞赛工具", ["环境", "编译器", "IDE", "配置"],
     "implementation_variant", False, "竞赛本地环境配置最佳实践"),
    ("比赛工具：Vim/VS Code竞赛配置", "contest_editor_config", "2.9", "yellow", "medium",
     "竞赛工具", ["编辑器", "Vim", "VS Code", "插件"],
     "implementation_variant", False, "编辑器竞赛相关配置"),
]
for c in contest_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充比赛相关知识覆盖")
contest_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {contest_count}")

# ============================================================
# THEME 12: 调试方法 (15)
# ============================================================
T = "调试方法"
TI = "debug"

debug_cands = [
    ("调试基础：GDB入门", "debug_gdb_basics", "4.16", "green", "high",
     "调试工具", ["GDB", "断点", "单步", "变量"],
     "core_concept", False, "GDB基本调试命令"),
    ("调试基础：GDB进阶命令", "debug_gdb_advanced", "4.16", "yellow", "medium",
     "调试工具", ["GDB", "条件断点", "回溯", "观察点"],
     "core_concept", False, "GDB高级调试技巧"),
    ("调试基础：print调试法", "debug_print_method", "4.16", "green", "high",
     "调试方法", ["print", "调试", "cout", "信息输出"],
     "modeling_pattern", True, "最通用的print调试方法"),
    ("调试基础：静态分析", "debug_static_analysis", "4.16", "green", "high",
     "调试方法", ["静态分析", "代码审查", "逻辑", "走读"],
     "modeling_pattern", True, "不运行代码的静态调试方法"),
    ("调试技巧：二分定位bug", "debug_binary_bug", "4.16", "green", "high",
     "调试技巧", ["二分", "bug定位", "注释", "隔离"],
     "modeling_pattern", True, "用二分法快速定位bug位置"),
    ("调试技巧：复原测试法", "debug_reproduce", "4.16", "green", "high",
     "调试技巧", ["复现", "最小样例", "构造", "测试"],
     "modeling_pattern", True, "构造最简样例复现bug"),
    ("调试技巧：断言辅助调试", "debug_assert_method", "4.16", "green", "high",
     "调试技巧", ["assert", "断言", "前置条件", "不变式"],
     "modeling_pattern", True, "断言在调试中的应用"),
    ("调试技巧：边界测试", "debug_boundary_test", "4.16", "green", "high",
     "调试技巧", ["边界", "极端", "空", "最大最小"],
     "modeling_pattern", True, "边界值是bug高发区域"),
    ("调试技巧：随机测试", "debug_random_test", "4.16", "yellow", "medium",
     "调试技巧", ["随机测试", "fuzzing", "压力", "覆盖"],
     "modeling_pattern", True, "随机测试暴露出隐藏bug"),
    ("调试场景：RE(运行时错误)排查", "debug_re_segfault", "4.16", "green", "high",
     "常见错误", ["RE", "段错误", "数组越界", "栈溢出"],
     "core_concept", True, "运行时错误的原因与排查方法"),
    ("调试场景：TLE(超时)优化", "debug_tle_opt", "4.16", "green", "high",
     "常见错误", ["TLE", "超时", "复杂度", "优化"],
     "core_concept", True, "TLE的原因分析与优化方向"),
    ("调试场景：WA(答案错误)排查", "debug_wa_analysis", "4.16", "green", "high",
     "常见错误", ["WA", "答案错误", "逻辑", "边界"],
     "core_concept", True, "答案错误的系统排查方法"),
    ("调试场景：MLE(内存超限)排查", "debug_mle_analysis", "4.16", "yellow", "medium",
     "常见错误", ["MLE", "内存超限", "压缩", "优化"],
     "core_concept", True, "内存超限的原因与优化策略"),
    ("调试工具：Valgrind内存检测", "debug_valgrind", "4.16", "yellow", "medium",
     "调试工具", ["Valgrind", "内存泄漏", "非法访问", "工具"],
     "implementation_variant", False, "Valgrind检测内存泄漏"),
    ("调试工具：AddressSanitizer", "debug_asan", "4.16", "yellow", "medium",
     "调试工具", ["AddressSanitizer", "ASan", "编译选项", "检测"],
     "implementation_variant", False, "AddressSanitizer编译期检测工具"),
]
for c in debug_cands:
    name, cid_part, sec, risk, conf, parent, deps, ctype, is_pp, reason = c
    add_candidate(T, TI, name, name, sec, sn(sec), risk, conf, parent, deps, is_pp, ctype, reason, "", "独立补充调试方法知识覆盖")
debug_count = len([c for c in candidates if c["theme"] == T])
print(f"  Theme {T}: {debug_count}")

# ============================================================
# FINAL STATS & OUTPUT
# ============================================================
print(f"\n{'='*60}")
print(f"      Stage3G 400 Candidate Pool Generation Summary")
print(f"{'='*60}")

total = len(candidates)
print(f"\nTotal candidates generated: {total}")

# Theme distribution
theme_dist = {}
for c in candidates:
    t = c["theme"]
    theme_dist[t] = theme_dist.get(t, 0) + 1
print(f"\n--- Theme Distribution (target: 400) ---")
for t, cnt in sorted(theme_dist.items(), key=lambda x: -x[1]):
    print(f"  {t}: {cnt}")

# Section distribution
sec_dist = {}
for c in candidates:
    s = c["target_section"]
    sec_dist[s] = sec_dist.get(s, 0) + 1

# Risk band distribution
risk_dist = {"green": 0, "yellow": 0, "medium": 0, "red": 0}
for c in candidates:
    r = c["risk_band"]
    risk_dist[r] = risk_dist.get(r, 0) + 1

# Confidence distribution
conf_dist = {"high": 0, "medium": 0, "low": 0}
for c in candidates:
    conf = c["mapping_confidence"]
    conf_dist[conf] = conf_dist.get(conf, 0) + 1

# Type distribution
type_dist = {}
for c in candidates:
    ct = c["candidate_type"]
    type_dist[ct] = type_dist.get(ct, 0) + 1

# Problem patterns count
pp_count = sum(1 for c in candidates if c["possible_problem_pattern"])

# Duplicate stats
dup_count = sum(1 for c in candidates if c.get("duplicate_risk_note") and c["duplicate_risk_note"] != "")

print(f"\n--- Risk Band Distribution ---")
for r, cnt in sorted(risk_dist.items()):
    print(f"  {r}: {cnt}")

print(f"\n--- Confidence Distribution ---")
for conf, cnt in sorted(conf_dist.items()):
    print(f"  {conf}: {cnt}")

print(f"\n--- Candidate Type Distribution ---")
for ct, cnt in sorted(type_dist.items(), key=lambda x: -x[1]):
    print(f"  {ct}: {cnt}")

print(f"\n--- Other Stats ---")
print(f"  Section count: {len(sec_dist)}")
print(f"  Possible problem patterns: {pp_count}")
print(f"  Duplicate risk notes: {dup_count}")

# OUTPUT JSON
OUTPUT_JSON = "data/stage3g_standardized_candidate_pool_400.json"
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)
print(f"\n✅ Candidate pool written to: {OUTPUT_JSON}")

# OUTPUT SUMMARY
OUTPUT_SUMMARY = "data/stage3g_candidate_pool_400_generation_summary.json"
summary = {
    "generation_time": datetime.now(timezone.utc).isoformat(),
    "source": "stage3g_generated",
    "total_candidates": total,
    "target_sections": sorted(list(sec_dist.keys())),
    "section_count": len(sec_dist),
    "theme_distribution": {t: theme_dist[t] for t in sorted(theme_dist.keys())},
    "risk_band_distribution": risk_dist,
    "confidence_distribution": conf_dist,
    "candidate_type_distribution": type_dist,
    "possible_problem_pattern_count": pp_count,
    "duplicate_flagged_count": dup_count,
    "green_candidates": risk_dist.get("green", 0),
    "yellow_candidates": risk_dist.get("yellow", 0),
    "medium_candidates": risk_dist.get("medium", 0),
    "red_candidates": risk_dist.get("red", 0),
    "high_confidence": conf_dist.get("high", 0),
    "medium_confidence": conf_dist.get("medium", 0),
    "low_confidence": conf_dist.get("low", 0),
    "modified_main_graph": False,
    "executed_merge": False,
    "recommend_stage3g_batch1": True,
    "stage3g_batch1_suggested_count": 40,
    "stage3g_batch1_priority": "green / high confidence",
    "note": "Stage3G 400 candidate pool only; no merge, no main graph modification"
}
with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"✅ Summary written to: {OUTPUT_SUMMARY}")

# OUTPUT REPORT
OUTPUT_REPORT = "docs/stage3g_standardized_candidate_pool_400_report.md"
with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
    f.write(f"# Stage3G 标准化候选池 400 报告\n\n")
    f.write(f"**生成时间**: {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write(f"## 1. 总体统计\n\n")
    f.write(f"| 指标 | 值 |\n")
    f.write(f"|------|-----|\n")
    f.write(f"| 候选总数 | {total} |\n")
    f.write(f"| 覆盖主题数 | {len(theme_dist)} |\n")
    f.write(f"| 覆盖 Section 数 | {len(sec_dist)} |\n")
    f.write(f"| 修改主图谱 | 否 |\n")
    f.write(f"| 执行合并 | 否 |\n")
    f.write(f"| 建议进入 Stage3G Batch1 | 是 |\n")
    f.write(f"| Stage3G Batch1 建议数量 | 40 |\n")
    f.write(f"| Batch1 优先选择 | green / high confidence |\n\n")

    f.write(f"## 2. Theme 分布\n\n")
    f.write(f"| Theme | 数量 | 规划目标 |\n")
    f.write(f"|-------|------|----------|\n")
    plan_map = {"图论专题":55,"数据结构专题":50,"动态规划专题":45,"信奥数学":40,
                "基础算法扩展":35,"字符串专题":35,"题型建模方法":30,"STL与常用库细节":30,
                "C++语法高级细节":25,"编程技巧":25,"比赛相关知识":15,"调试方法":15}
    for t in sorted(theme_dist.keys(), key=lambda x: -theme_dist[x]):
        target = plan_map.get(t, "N/A")
        f.write(f"| {t} | {theme_dist[t]} | {target} |\n")

    f.write(f"\n## 3. Risk Band 分布\n\n")
    f.write(f"| Risk Band | 数量 |\n")
    f.write(f"|-----------|------|\n")
    for r in ["green", "yellow", "medium", "red"]:
        f.write(f"| {r} | {risk_dist.get(r, 0)} |\n")

    f.write(f"\n## 4. Confidence 分布\n\n")
    f.write(f"| Confidence | 数量 |\n")
    f.write(f"|------------|------|\n")
    for conf in ["high", "medium", "low"]:
        f.write(f"| {conf} | {conf_dist.get(conf, 0)} |\n")

    f.write(f"\n## 5. Candidate Type 分布\n\n")
    f.write(f"| Type | 数量 |\n")
    f.write(f"|------|------|\n")
    for ct in sorted(type_dist.keys(), key=lambda x: -type_dist[x]):
        f.write(f"| {ct} | {type_dist[ct]} |\n")

    f.write(f"\n## 6. 其他指标\n\n")
    f.write(f"- possible_problem_pattern 标记数: {pp_count}\n")
    f.write(f"- 标记重复风险候选数: {dup_count}\n")
    f.write(f"- green 候选数: {risk_dist.get('green', 0)}（适合早期批次）\n")
    f.write(f"- red 候选数: {risk_dist.get('red', 0)}（只作备选，不进入前几批）\n")
    f.write(f"- high confidence 数: {conf_dist.get('high', 0)}\n")

    f.write(f"\n## 7. 初步查重结果\n\n")
    f.write(f"- 与当前 1765 个主图谱节点进行 name/en_name/aliases/global_aliases 查重\n")
    f.write(f"- 与历史删除节点进行查重\n")
    f.write(f"- 精确匹配和模糊匹配双重检测\n")
    f.write(f"- 重复候选自动跳过并记录\n\n")

    f.write(f"## 8. 高危主题重复风险\n\n")
    f.write(f"以下主题为高危重复区，需在后续合并中特别注意：\n")
    f.write(f"1. KMP / 扩展KMP / Z算法 / Border树\n")
    f.write(f"2. Lucas / Miller-Rabin / BSGS / 欧拉函数 / 莫比乌斯反演\n")
    f.write(f"3. 单调队列优化 / 斜率优化 / 状压DP / 概率DP\n")
    f.write(f"4. 线段树 Split / Merge / 分裂 / 合并 / Beats\n")
    f.write(f"5. SCC DAG / 动态连通性 / 缩点 / DAG\n")
    f.write(f"6. 线性基 Range / Merge / Deletion / Rollback\n")

    f.write(f"\n## 9. Section 分布\n\n")
    f.write(f"| Section | 候选数 |\n")
    f.write(f"|---------|--------|\n")
    sn_map = {"2.1":"基础算法","2.2":"二分与贪心","2.3":"排序","2.4":"分治算法",
              "2.5":"搜索","2.9":"C++与STL","2.10":"字符串基础",
              "2.12":"数值与矩阵","2.17":"线性代数与插值",
              "3.1":"栈","3.2":"队列","3.3":"链表","3.4":"树","3.5":"并查集",
              "3.6":"堆","3.7":"哈希表","3.8":"字符串结构","3.9":"树状数组",
              "3.10":"线段树","3.11":"平衡树","3.12":"分块","3.13":"图论基础",
              "3.14":"最短路","3.15":"最小生成树","3.16":"网络流",
              "3.17":"差分约束","4.1":"数论基础","4.2":"组合数学","4.3":"线性代数",
              "4.4":"概率论","4.5":"博弈论","4.6":"数学其他","4.7":"动态规划基础",
              "4.8":"背包DP","4.9":"区间DP","4.10":"树形DP","4.11":"状态压缩DP",
              "4.12":"数位DP","4.13":"优化DP","4.14":"图论DP","4.15":"字符串DP",
              "4.16":"调试与错误","5.1":"排序算法","5.2":"字符串匹配","5.3":"图论问题",
              "5.4":"网络流","5.5":"数学问题","5.6":"动态规划","5.7":"搜索",
              "5.8":"构造题","5.9":"交互题","5.10":"综合题"}
    for s in sorted(sec_dist.keys()):
        sname = sn_map.get(s, "")
        f.write(f"| {s} {sname} | {sec_dist[s]} |\n")

    f.write(f"\n---\n")
    f.write(f"*本报告由 stage3g_generate_400_pool.py 自动生成*\n")
    f.write(f"*不修改主图谱，不执行合并*\n")
print(f"✅ Report written to: {OUTPUT_REPORT}")

print(f"\n{'='*60}")
print(f"      Stage3G 400 Candidate Pool Generation Complete")
print(f"{'='*60}")
print(f"\n下一步建议: Stage3G Batch1 - 选择 40 个 green/high confidence 候选进行合并")