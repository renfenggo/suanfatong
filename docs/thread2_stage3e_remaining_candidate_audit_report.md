# Thread2 Stage3E Remaining Candidate Audit Report

Thread 2 performed candidate audit only. No candidate was merged and the main graph was not modified. Stage3D mappings were included as already merged exclusions.

## Required Summary

| Metric | Count |
|---|---:|
| 外部候选总数 | 340 |
| 已合并数量 | 133 |
| 未合并数量 | 207 |
| 推荐 Stage3E 合并数量 | 85 |
| Stage3E 白名单数量 | 80 |
| 建议转 problem_patterns 数量 | 35 |
| 建议 reject / merge 数量 | 1 |
| manual_review 数量 | 86 |
| high duplicate risk 数量 | 1 |
| 依赖问题数量 | 0 |
| 是否成功排除 Stage3D 已合并的 25 个 candidate | 是 |
| 主图谱是否被修改 | 否 |
| validate-only 是否 passed | 是 |

## Merged Mapping Counts

- Stage3B: 72
- Stage3C: 36
- Stage3D: 25
- Total merged excluded: 133

## Main Graph Baseline

- Stable baseline: item_count = 1482, section_count = 65, validate-only = passed.
- Observed scan: item_count = 1482, section_count = 65.
- Protected files were read only: merged graph, dependency validation, refinement report, and refine script.
- Read-only validate-only result: passed = true, item_count = 1482, section_count = 65.

## Stage3E Whitelist

Whitelist size: 80. Criteria: low/medium duplicate risk, mapped direct_pre, existing target section, not problem_pattern, not manual_review, not high duplicate risk, no new section, preferred add_new/add_as_subtopic. Sorting prioritizes existing sections 2.21 and 3.13.

Whitelist section distribution: {"2.21":54,"3.13":26}

| candidate_id | name | risk | action | target_section |
|---|---|---|---|---|
| cand.graph.closure_model.binary_decision_model | 最大权闭合子图：Binary Decision Model | low | add_new | 2.21 高级图论扩展 |
| cand.graph.closure_model.maximum_weight_closure | 最大权闭合子图：Maximum Weight Closure | low | add_new | 2.21 高级图论扩展 |
| cand.graph.closure_model.minimum_cut_transform | 最大权闭合子图：Minimum Cut Transform | low | add_new | 2.21 高级图论扩展 |
| cand.graph.closure_model.open_pit_mining_model | 最大权闭合子图：Open Pit Mining Model | low | add_new | 2.21 高级图论扩展 |
| cand.graph.closure_model.prerequisite_graph | 最大权闭合子图：Prerequisite Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.closure_model.task_selection | 最大权闭合子图：Task Selection | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.branching_theorem | 有向生成树：Branching Theorem | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.maximum_arborescence | 有向生成树：Maximum Arborescence | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.minimum_arborescence | 有向生成树：Minimum Arborescence | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.rooted_arborescence | 有向生成树：Rooted Arborescence | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.super_root_model | 有向生成树：Super Root Model | low | add_new | 2.21 高级图论扩展 |
| cand.graph.directed_mst.weighted_directed_mst | 有向生成树：Weighted Directed Mst | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.bridge_relation | 支配树：Bridge Relation | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.dag_dominator | 支配树：Dag Dominator | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.dominance_frontier | 支配树：Dominance Frontier | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.dominator_tree_dp | 支配树：Dominator Tree Dp | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.online_query | 支配树：Online Query | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dominator_tree.path_dominator_query | 支配树：Path Dominator Query | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.batch_recomputation | 动态最小生成树：Batch Recomputation | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.certificate_graph | 动态最小生成树：Certificate Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.divide_conquer_approach | 动态最小生成树：Divide Conquer Approach | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.edge_deletion | 动态最小生成树：Edge Deletion | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.edge_insertion | 动态最小生成树：Edge Insertion | low | add_new | 2.21 高级图论扩展 |
| cand.graph.dynamic_mst.sensitivity_analysis | 动态最小生成树：Sensitivity Analysis | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.cut_tree_query | 全局最小割：Cut Tree Query | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.pair_min_cut | 全局最小割：Pair Min Cut | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.random_contraction | 全局最小割：Random Contraction | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.recursive_contraction | 全局最小割：Recursive Contraction | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.sparsification | 全局最小割：Sparsification | low | add_new | 2.21 高级图论扩展 |
| cand.graph.global_min_cut.undirected_min_cut | 全局最小割：Undirected Min Cut | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.basis_exchange | 拟阵图论：Basis Exchange | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.matroid_parity | 拟阵图论：Matroid Parity | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.partition_matroid | 拟阵图论：Partition Matroid | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.spanning_tree_matroid | 拟阵图论：Spanning Tree Matroid | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.transversal_matroid | 拟阵图论：Transversal Matroid | low | add_new | 2.21 高级图论扩展 |
| cand.graph.matroid_graph.weighted_matroid_intersection | 拟阵图论：Weighted Matroid Intersection | low | add_new | 2.21 高级图论扩展 |
| cand.graph.planar_graph.dual_shortest_path | 平面图：Dual Shortest Path | low | add_new | 2.21 高级图论扩展 |
| cand.graph.planar_graph.face_traversal | 平面图：Face Traversal | low | add_new | 2.21 高级图论扩展 |
| cand.graph.planar_graph.outerplanar_graph | 平面图：Outerplanar Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.planar_graph.planar_min_cut | 平面图：Planar Min Cut | low | add_new | 2.21 高级图论扩展 |
| cand.graph.planar_graph.planar_separator | 平面图：Planar Separator | low | add_new | 2.21 高级图论扩展 |
| cand.graph.scc_dag.implication_graph | 强连通分量 DAG：Implication Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.bipartite_complement | 特殊图：Bipartite Complement | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.condensation_dag | 特殊图：Condensation Dag | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.functional_graph | 特殊图：Functional Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.interval_graph | 特殊图：Interval Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.planar_dual_graph | 特殊图：Planar Dual Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.special_graph.tournament_graph | 特殊图：Tournament Graph | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.colored_points | 虚树：Colored Points | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.distance_compression | 虚树：Distance Compression | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.edge_weight_compression | 虚树：Edge Weight Compression | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.minimum_connection | 虚树：Minimum Connection | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.multi_key_query | 虚树：Multi-Key Query | low | add_new | 2.21 高级图论扩展 |
| cand.graph.virtual_tree.subtree_aggregation | 虚树：Subtree Aggregation | low | add_new | 2.21 高级图论扩展 |
| cand.ds.multidimensional.orthogonal_range_query | 多维数据结构：Orthogonal Range Query | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.multidimensional.parallel_binary_search | 多维数据结构：Parallel Binary Search | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.offline_framework.event_sweep_with_tree | 离线数据结构框架：Event Sweep With Tree | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.offline_framework.offline_range_mex | 离线数据结构框架：Offline Range Mex | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.offline_framework.offline_rectangle_add | 离线数据结构框架：Offline Rectangle Add | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.offline_framework.parallel_check_framework | 离线数据结构框架：Parallel Check Framework | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.offline_framework.time_divide_conquer | 离线数据结构框架：Time Divide Conquer | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.persistent_structure.fat_node_method | 可持久化结构：Fat Node Method | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.persistent_structure.path_copying_method | 可持久化结构：Path Copying Method | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.persistent_structure.rollback_vs_persistence | 可持久化结构：Rollback Vs Persistence | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.persistent_structure.version_dag | 可持久化结构：Version Dag | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.rmq_sparse.cache_friendly_rmq | 高级 RMQ：Cache Friendly Rmq | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.rmq_sparse.plus_minus_one_rmq | 高级 RMQ：Plus Minus One Rmq | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.rmq_sparse.range_idempotent_query | 高级 RMQ：Range Idempotent Query | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.rmq_sparse.sparse_table_2d | 高级 RMQ：Sparse Table 2D | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.rmq_sparse.static_range_mode | 高级 RMQ：Static Range Mode | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.sequence_structure.order_maintenance | 序列维护结构：Order Maintenance | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.sequence_structure.persistent_sequence | 序列维护结构：Persistent Sequence | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.sequence_structure.range_hash_maintenance | 序列维护结构：Range Hash Maintenance | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.sequence_structure.sequence_split_merge | 序列维护结构：Sequence Split Merge | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.sequence_structure.text_editor_model | 序列维护结构：Text Editor Model | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.succinct_probabilistic.compressed_trie | 简洁与概率结构：Compressed Trie | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.succinct_probabilistic.perfect_hashing | 简洁与概率结构：Perfect Hashing | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.succinct_probabilistic.succinct_bitvector_rank | 简洁与概率结构：Succinct Bitvector Rank | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.succinct_probabilistic.succinct_select | 简洁与概率结构：Succinct Select | low | add_new | 3.13 高级数据结构扩展 |
| cand.ds.succinct_probabilistic.xor_filter | 简洁与概率结构：Xor Filter | low | add_new | 3.13 高级数据结构扩展 |

## Problem Pattern Redirect Candidates (sample)

| candidate_id | name | risk | action | reason |
|---|---|---|---|---|
| cand.graph.hall_theorem.applications | Hall 定理及应用 | medium | manual_review | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.two_sat.modeling_techniques | 2-SAT 建模技巧 | medium | manual_review | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.difference_constraints.modeling.raw | 差分约束系统建模 | medium | manual_review | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.max_weight_closure.problem | 最大权闭合子图 | medium | manual_review | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.johnson_potentials | 高级最短路：Johnson Potentials | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.graph_modeling.2_sat_modeling | 图论建模：2 Sat Modeling | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.yen_k_shortest | 高级最短路：Yen K Shortest | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.scc_dag.dag_reachability | 强连通分量 DAG：Dag Reachability | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.eppstein_k_shortest | 高级最短路：Eppstein K Shortest | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.divide_and_conquer_on_time | 动态图连通性：Divide And Conquer On Time | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.scc_dag.dominating_components | 强连通分量 DAG：Dominating Components | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.replacement_paths | 高级最短路：Replacement Paths | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.edge_interval_model | 动态图连通性：Edge Interval Model | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.scc_dag.minimum_edges_to_strong | 强连通分量 DAG：Minimum Edges To Strong | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.resource_constrained | 高级最短路：Resource Constrained | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.fully_dynamic_overview | 动态图连通性：Fully Dynamic Overview | medium | manual_review | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.global_min_cut.minimum_cut_modeling | 全局最小割：Minimum Cut Modeling | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.scc_dag.scc_dp | 强连通分量 DAG：Scc Dp | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.dynamic_bridge | 动态图连通性：Dynamic Bridge | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.scc_dag.component_topo_order | 强连通分量 DAG：Component Topo Order | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.min_cost_path_cover | 高级最短路：Min Cost Path Cover | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.dynamic_biconnectivity | 动态图连通性：Dynamic Biconnectivity | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.shortest_path_advanced.zero_one_bfs_modeling | 高级最短路：Zero One Bfs Modeling | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.dynamic_connectivity.connectivity_snapshots | 动态图连通性：Connectivity Snapshots | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.graph.closure_model.penalty_modeling | 最大权闭合子图：Penalty Modeling | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.parity | 高级并查集：Parity | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.distance | 高级并查集：Distance | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.weighted | 高级并查集：Weighted | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.small_to_large | 高级并查集：Small To Large | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.bitset_linear_basis.rollback_linear_basis | 位集与线性基：Rollback Linear Basis | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.offline_dynamic_connectivity | 高级并查集：Offline Dynamic Connectivity | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.bitset_linear_basis.maximum_xor_query | 位集与线性基：Maximum Xor Query | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.bitset_linear_basis.rank_over_gf2 | 位集与线性基：Rank Over Gf2 | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.dsu_advanced.component_aggregate | 高级并查集：Component Aggregate | medium | add_as_subtopic | move_to_problem_patterns or looks like application/model/problem-pattern |
| cand.ds.bitset_linear_basis.basis_with_deletion | 位集与线性基：Basis With Deletion | low | add_new | move_to_problem_patterns or looks like application/model/problem-pattern |

## Duplicate Or Reject Candidates

| candidate_id | name | risk | action | reason |
|---|---|---|---|---|
| cand.graph.virtual_tree.construction | 虚树构建 | high | merge_with_existing | high duplicate risk or recommended reject/merge_with_existing |

## Manual Review / Dependency Notes

- manual_review candidates are excluded from the whitelist.
- high duplicate risk candidates are excluded from the whitelist.
- Stage3B/Stage3C/Stage3D merged candidates are excluded from the whitelist.
- dependency_issue candidates are excluded until direct_pre suggestions can be mapped to existing item/section ids.
- Stage3E should consume data/thread2_stage3e_candidate_whitelist.json as an allow-list, not as an automatic merge command.
