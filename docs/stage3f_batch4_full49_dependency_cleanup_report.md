# Stage3F Batch4 Full49 Dependency Cleanup Report

**生成时间**: 2026-05-25 09:35:31 UTC
**生成者**: GLM5 (2号线程)
**任务类型**: Dependency Cleanup（仅清理，不合并）

---

## 1. 清理概览

| 指标 | 值 |
|------|-----|
| 总候选数 | 49 |
| 依赖自动解析 | 46 |
| 需手动映射 | 3 |
| Section ID 引用 | 0 → 已清理 |
| 悬空引用 | 0 → 已清理 |
| 依赖环 | 无 |
| dependency_cleanup_required | false |

## 2. 清理候选明细

| # | candidate_id | name | section | confidence | direct_pre (cleaned) | manual_review |
|---|-------------|------|---------|------------|---------------------|---------------|
| 1 | cand.graph.closure_model.penalty_modeling | 最大权闭合子图：Penalty Modeling | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 2 | cand.graph.dynamic_connectivity.connectivity_snapshots | 动态图连通性：Connectivity Snapshots | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 3 | cand.graph.dynamic_connectivity.dynamic_biconnectivity | 动态图连通性：Dynamic Biconnectivity | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 4 | cand.graph.dynamic_connectivity.dynamic_bridge | 动态图连通性：Dynamic Bridge | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 5 | cand.graph.global_min_cut.minimum_cut_modeling | 全局最小割：Minimum Cut Modeling | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 6 | cand.graph.scc_dag.component_topo_order | 强连通分量 DAG：Component Topo Order | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 7 | cand.graph.scc_dag.scc_dp | 强连通分量 DAG：Scc Dp | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 8 | cand.graph.difference_constraints.modeling.raw | 差分约束系统建模 | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 9 | cand.graph.dynamic_connectivity.fully_dynamic_overview | 动态图连通性：Fully Dynamic Overview | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 10 | cand.graph.hall_theorem.applications | Hall 定理及应用 | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 11 | cand.graph.max_weight_closure.problem | 最大权闭合子图 | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 12 | cand.graph.planar_graph.embedding_basics | 平面图：Embedding Basics | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 13 | cand.graph.shortest_path_advanced.eppstein_k_shortest | 高级最短路：Eppstein K Shortest | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 14 | cand.graph.shortest_path_advanced.johnson_potentials | 高级最短路：Johnson Potentials | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 15 | cand.graph.shortest_path_advanced.min_cost_path_cover | 高级最短路：Min Cost Path Cover | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 16 | cand.graph.shortest_path_advanced.replacement_paths | 高级最短路：Replacement Paths | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 17 | cand.graph.shortest_path_advanced.resource_constrained | 高级最短路：Resource Constrained | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 18 | cand.graph.shortest_path_advanced.yen_k_shortest | 高级最短路：Yen K Shortest | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 19 | cand.graph.shortest_path_advanced.zero_one_bfs_modeling | 高级最短路：Zero One Bfs Modeling | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 20 | cand.graph.two_sat.modeling_techniques | 2-SAT 建模技巧 | 2.21 | high | 2.9.1; 2.9.2; 2.9.3; 2.9.4; 2.9.5 | 否 |
| 21 | cand.ds.dsu_advanced.component_aggregate | 高级并查集：Component Aggregate | 3.13 | high | (section defaults) | 否 |
| 22 | cand.ds.dsu_advanced.distance | 高级并查集：Distance | 3.13 | high | (section defaults) | 否 |
| 23 | cand.ds.dsu_advanced.offline_dynamic_connectivity | 高级并查集：Offline Dynamic Connectivity | 3.13 | high | (section defaults) | 否 |
| 24 | cand.ds.dsu_advanced.small_to_large | 高级并查集：Small To Large | 3.13 | high | (section defaults) | 否 |
| 25 | cand.ds.dsu_advanced.weighted | 高级并查集：Weighted | 3.13 | high | (section defaults) | 否 |
| 26 | cand.ds.li_chao_tree.cht_comparison | 李超线段树：Cht Comparison | 3.13 | high | (section defaults) | 否 |
| 27 | cand.ds.persistent_structure.retroactive_overview | 可持久化结构：Retroactive Overview | 3.13 | high | (section defaults) | 否 |
| 28 | cand.ds.segment_tree_variants.matrix_segment_tree | 线段树变体：Matrix Segment Tree | 3.13 | high | (section defaults) | 否 |
| 29 | cand.ds.segment_tree_variants.merge.codex1 | 线段树变体：Merge 变体 1 | 3.13 | high | (section defaults) | 否 |
| 30 | cand.ds.segment_tree_variants.persistent_segment_tree | 线段树变体：Persistent Segment Tree | 3.13 | high | (section defaults) | 否 |
| 31 | cand.ds.segment_tree_variants.range_assign_lazy | 线段树变体：Range Assign Lazy | 3.13 | high | (section defaults) | 否 |
| 32 | cand.ds.segment_tree_variants.segment_tree_of_vectors | 线段树变体：Segment Tree Of Vectors | 3.13 | high | (section defaults) | 否 |
| 33 | cand.ds.segment_tree_variants.segment_tree_over_time | 线段树变体：Segment Tree Over Time | 3.13 | high | (section defaults) | 否 |
| 34 | cand.ds.segment_tree_variants.two_dimensional_segment_tree | 线段树变体：Two Dimensional Segment Tree | 3.13 | high | (section defaults) | 否 |
| 35 | cand.ds.succinct_probabilistic.van_emde_boas_overview | 简洁与概率结构：Van Emde Boas Overview | 3.13 | high | (section defaults) | 否 |
| 36 | cand.dp.game.basic | 博弈DP基础 | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 37 | cand.dp.game.grundy | Grundy数DP | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 38 | cand.dp.matrix.basic | 矩阵DP基础 | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 39 | cand.dp.matrix.fast_power | 矩阵快速幂DP | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 40 | cand.dp.probability.expectation | 期望DP | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 41 | cand.dp.probability.markov | 马尔可夫链DP | 2.8 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 42 | cand.math.graph.gaussian_elimination_gf2 | GF(2)上的高斯消元 | 4.5 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 43 | cand.math.graph.matrix_tree | 矩阵树定理 | 4.5 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 44 | cand.string.string_matching.sunday | Sunday算法 | 2.10 | medium | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 是 |
| 45 | cand.math.linear_recurrence.basic | 线性递推基础 | 4.4 | medium | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 是 |
| 46 | cand.math.linear_recurrence.kitamasa | Kitamasa算法 | 4.4 | medium | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 是 |
| 47 | cand.string.duval_algorithm.minimal_rotation | Duval算法最小表示 | 2.10 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 48 | cand.string.hashing.2d_rolling_hash | 二维滚动哈希 | 2.10 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |
| 49 | cand.string.hashing.collision_strategy | 哈希碰撞处理策略 | 2.10 | high | 1.3.1; 1.3.2; 1.3.3; 1.3.4; 1.3.5 | 否 |

## 3. Medium 风险候选详情

以下 3 个候选因 mapping_confidence = medium，需在合并阶段由 1 号线程手动精确映射依赖：

### Sunday算法

- **candidate_id**: cand.string.string_matching.sunday
- **target_section**: 2.10
- **问题**: medium mapping confidence
- **建议 direct_pre**: ['1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.3.5', '1.3.6', '1.3.7', '1.3.8', '1.3.9', '1.3.10', '1.3.11', '1.3.12', '1.3.13', '1.3.14', '1.3.15', '1.3.16', '1.3.17', '1.3.18', '1.3.19', '1.3.20', '1.3.21', '1.3.22', '1.3.23', '1.3.24', '1.3.25', '1.3.26', '1.3.27', '1.3.28', '1.3.29', '1.3.30', '1.3.31', '1.3.32', '1.3.33', '1.3.34', '1.3.35', '1.3.36', '1.3.37', '1.3.38', '1.3.39', '1.3.40', '1.3.41', '1.3.42', '1.3.43', '1.3.44', '1.3.45', '1.3.46', '1.3.47', '1.3.48', '1.3.49', '1.3.50', '1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5', '1.4.6', '1.4.7', '1.4.8', '1.4.9', '1.4.10', '1.4.11', '1.4.12', '1.4.13', '1.4.14', '1.4.15', '1.5.1', '1.5.2', '1.5.3', '1.5.4', '1.5.5', '1.5.6', '1.5.7', '1.5.8', '1.5.9', '1.5.10', '1.5.11', '1.5.12', '1.5.13', '1.5.14', '1.5.15', '1.5.16', '1.5.17', '1.5.18', '1.5.19', '1.5.20', '1.5.21', '1.5.22', '1.5.23', '1.6.1', '1.6.2', '1.6.3', '1.6.4', '1.6.5', '1.6.6', '1.6.7', '1.6.8', '1.6.9', '1.6.10', '1.6.11', '1.6.12', '1.6.13', '1.6.14', '1.6.15', '1.6.16', '1.6.17', '1.6.18', '1.6.19', '1.6.20', '1.6.21', '1.6.22', '1.6.23', '1.6.24', '1.6.25', '1.6.26', '1.6.27', '1.6.28', '1.6.29', '1.6.30', '1.6.31', '1.6.32', '1.6.33', '1.6.34', '1.6.35', '1.6.36', '1.6.37', '1.6.38', '1.6.39', '1.6.40', '1.6.41', '1.6.42', '1.6.43', '1.6.44', '1.6.45', '1.6.46', '1.6.47', '1.6.48', '1.6.49', '1.6.50', '2.1.1', '2.1.2', '2.1.3', '2.1.4', '2.1.5', '2.1.6', '2.1.7', '2.1.8', '2.1.9', '2.1.10', '2.1.11', '2.1.12', '2.1.13', '2.1.14', '2.1.15', '2.1.16', '2.1.17', '2.1.18', '2.1.19', '2.1.20', '2.1.21', '2.1.22', '2.1.23', '2.1.24', '2.1.25', '2.1.26', '2.1.27', '2.1.28', '2.1.29', '2.1.30', '2.1.31', '2.1.32', '2.1.33', '2.1.34', '2.1.35', '2.1.36', '2.1.37', '2.1.38', '2.1.39', '2.1.40', '2.1.41', '2.1.42', '2.1.43', '2.1.44', '2.1.45', '2.1.46', '2.1.47', '2.1.48', '2.1.49', '2.1.50', '2.1.51', '2.1.52', '2.1.53', '2.1.54', '2.1.55', '2.1.56', '2.1.57', '2.1.58', '2.1.59', '2.1.60', '2.1.61', '2.1.62', '2.1.63', '2.1.64', '3.8.1', '3.8.2', '3.8.3', '3.8.4', '3.8.5', '3.8.6', '3.8.7', '3.8.8', '3.8.9', '3.8.10', '3.8.11', '3.8.12', '3.8.13', '3.8.14', '3.8.15', '3.8.16']
- **建议**: 合并时由 1 号线程进行精确依赖映射

### 线性递推基础

- **candidate_id**: cand.math.linear_recurrence.basic
- **target_section**: 4.4
- **问题**: medium mapping confidence
- **建议 direct_pre**: ['1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.3.5', '1.3.6', '1.3.7', '1.3.8', '1.3.9', '1.3.10', '1.3.11', '1.3.12', '1.3.13', '1.3.14', '1.3.15', '1.3.16', '1.3.17', '1.3.18', '1.3.19', '1.3.20', '1.3.21', '1.3.22', '1.3.23', '1.3.24', '1.3.25', '1.3.26', '1.3.27', '1.3.28', '1.3.29', '1.3.30', '1.3.31', '1.3.32', '1.3.33', '1.3.34', '1.3.35', '1.3.36', '1.3.37', '1.3.38', '1.3.39', '1.3.40', '1.3.41', '1.3.42', '1.3.43', '1.3.44', '1.3.45', '1.3.46', '1.3.47', '1.3.48', '1.3.49', '1.3.50', '1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5', '1.4.6', '1.4.7', '1.4.8', '1.4.9', '1.4.10', '1.4.11', '1.4.12', '1.4.13', '1.4.14', '1.4.15', '1.5.1', '1.5.2', '1.5.3', '1.5.4', '1.5.5', '1.5.6', '1.5.7', '1.5.8', '1.5.9', '1.5.10', '1.5.11', '1.5.12', '1.5.13', '1.5.14', '1.5.15', '1.5.16', '1.5.17', '1.5.18', '1.5.19', '1.5.20', '1.5.21', '1.5.22', '1.5.23']
- **建议**: 合并时由 1 号线程进行精确依赖映射

### Kitamasa算法

- **candidate_id**: cand.math.linear_recurrence.kitamasa
- **target_section**: 4.4
- **问题**: medium mapping confidence
- **建议 direct_pre**: ['1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.3.5', '1.3.6', '1.3.7', '1.3.8', '1.3.9', '1.3.10', '1.3.11', '1.3.12', '1.3.13', '1.3.14', '1.3.15', '1.3.16', '1.3.17', '1.3.18', '1.3.19', '1.3.20', '1.3.21', '1.3.22', '1.3.23', '1.3.24', '1.3.25', '1.3.26', '1.3.27', '1.3.28', '1.3.29', '1.3.30', '1.3.31', '1.3.32', '1.3.33', '1.3.34', '1.3.35', '1.3.36', '1.3.37', '1.3.38', '1.3.39', '1.3.40', '1.3.41', '1.3.42', '1.3.43', '1.3.44', '1.3.45', '1.3.46', '1.3.47', '1.3.48', '1.3.49', '1.3.50', '1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5', '1.4.6', '1.4.7', '1.4.8', '1.4.9', '1.4.10', '1.4.11', '1.4.12', '1.4.13', '1.4.14', '1.4.15', '1.5.1', '1.5.2', '1.5.3', '1.5.4', '1.5.5', '1.5.6', '1.5.7', '1.5.8', '1.5.9', '1.5.10', '1.5.11', '1.5.12', '1.5.13', '1.5.14', '1.5.15', '1.5.16', '1.5.17', '1.5.18', '1.5.19', '1.5.20', '1.5.21', '1.5.22', '1.5.23']
- **建议**: 合并时由 1 号线程进行精确依赖映射

## 4. Section ID 污染检查

未发现 section ID 污染。所有 direct_pre 均为 item ID。

## 5. 悬空引用检查

未发现悬空引用。

## 6. 依赖环检查

未发现依赖环。

## 7. 清理结论

- **dependency_cleanup_required**: false
- **建议操作**: 交给 1 号线程执行 full_49 合并
- **主图谱是否修改**: 否
- **仅运行 validate-only**: 是
- **未执行 Merge**: 是