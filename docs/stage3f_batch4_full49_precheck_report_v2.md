# Stage3F Batch4 Full49 预审报告 v2 (Dependency Cleanup 后)

**生成时间**: 2026-05-25 09:35:31 UTC
**生成者**: GLM5 (2号线程)
**任务类型**: 候选计划 v2 + 动态预审 v2（依赖清理后，仅验证，不合并）

---

## 1. 当前主图谱状态

| 指标 | 值 |
|------|-----|
| item_count | 1716 |
| 预期 item_count | 1716 |
| section_count | 65 |
| validate-only passed | True |
| 主图谱是否修改 | 否 |

## 2. Batch4 Full49 候选列表 (v2)

| # | candidate_id | name | section | risk | source | manual_review |
|---|-------------|------|---------|------|--------|---------------|
| 1 | cand.graph.closure_model.penalty_modeling | 最大权闭合子图：Penalty Modeling | 2.21 | green | external_b1 | 否 |
| 2 | cand.graph.dynamic_connectivity.connectivity_snapshots | 动态图连通性：Connectivity Snapshots | 2.21 | green | external_b1 | 否 |
| 3 | cand.graph.dynamic_connectivity.dynamic_biconnectivity | 动态图连通性：Dynamic Biconnectivity | 2.21 | green | external_b1 | 否 |
| 4 | cand.graph.dynamic_connectivity.dynamic_bridge | 动态图连通性：Dynamic Bridge | 2.21 | green | external_b1 | 否 |
| 5 | cand.graph.global_min_cut.minimum_cut_modeling | 全局最小割：Minimum Cut Modeling | 2.21 | green | external_b1 | 否 |
| 6 | cand.graph.scc_dag.component_topo_order | 强连通分量 DAG：Component Topo Order | 2.21 | green | external_b1 | 否 |
| 7 | cand.graph.scc_dag.scc_dp | 强连通分量 DAG：Scc Dp | 2.21 | green | external_b1 | 否 |
| 8 | cand.graph.difference_constraints.modeling.raw | 差分约束系统建模 | 2.21 | yellow | external_b1 | 否 |
| 9 | cand.graph.dynamic_connectivity.fully_dynamic_overview | 动态图连通性：Fully Dynamic Overview | 2.21 | yellow | external_b1 | 否 |
| 10 | cand.graph.hall_theorem.applications | Hall 定理及应用 | 2.21 | yellow | external_b1 | 否 |
| 11 | cand.graph.max_weight_closure.problem | 最大权闭合子图 | 2.21 | yellow | external_b1 | 否 |
| 12 | cand.graph.planar_graph.embedding_basics | 平面图：Embedding Basics | 2.21 | yellow | external_b1 | 否 |
| 13 | cand.graph.shortest_path_advanced.eppstein_k_shortest | 高级最短路：Eppstein K Shortest | 2.21 | yellow | external_b1 | 否 |
| 14 | cand.graph.shortest_path_advanced.johnson_potentials | 高级最短路：Johnson Potentials | 2.21 | yellow | external_b1 | 否 |
| 15 | cand.graph.shortest_path_advanced.min_cost_path_cover | 高级最短路：Min Cost Path Cover | 2.21 | yellow | external_b1 | 否 |
| 16 | cand.graph.shortest_path_advanced.replacement_paths | 高级最短路：Replacement Paths | 2.21 | yellow | external_b1 | 否 |
| 17 | cand.graph.shortest_path_advanced.resource_constrained | 高级最短路：Resource Constrained | 2.21 | yellow | external_b1 | 否 |
| 18 | cand.graph.shortest_path_advanced.yen_k_shortest | 高级最短路：Yen K Shortest | 2.21 | yellow | external_b1 | 否 |
| 19 | cand.graph.shortest_path_advanced.zero_one_bfs_modeling | 高级最短路：Zero One Bfs Modeling | 2.21 | yellow | external_b1 | 否 |
| 20 | cand.graph.two_sat.modeling_techniques | 2-SAT 建模技巧 | 2.21 | yellow | external_b1 | 否 |
| 21 | cand.ds.dsu_advanced.component_aggregate | 高级并查集：Component Aggregate | 3.13 | yellow | external_b1 | 否 |
| 22 | cand.ds.dsu_advanced.distance | 高级并查集：Distance | 3.13 | yellow | external_b1 | 否 |
| 23 | cand.ds.dsu_advanced.offline_dynamic_connectivity | 高级并查集：Offline Dynamic Connectivity | 3.13 | yellow | external_b1 | 否 |
| 24 | cand.ds.dsu_advanced.small_to_large | 高级并查集：Small To Large | 3.13 | yellow | external_b1 | 否 |
| 25 | cand.ds.dsu_advanced.weighted | 高级并查集：Weighted | 3.13 | yellow | external_b1 | 否 |
| 26 | cand.ds.li_chao_tree.cht_comparison | 李超线段树：Cht Comparison | 3.13 | yellow | external_b1 | 否 |
| 27 | cand.ds.persistent_structure.retroactive_overview | 可持久化结构：Retroactive Overview | 3.13 | yellow | external_b1 | 否 |
| 28 | cand.ds.segment_tree_variants.matrix_segment_tree | 线段树变体：Matrix Segment Tree | 3.13 | yellow | external_b1 | 否 |
| 29 | cand.ds.segment_tree_variants.merge.codex1 | 线段树变体：Merge 变体 1 | 3.13 | yellow | external_b1 | 否 |
| 30 | cand.ds.segment_tree_variants.persistent_segment_tree | 线段树变体：Persistent Segment Tree | 3.13 | yellow | external_b1 | 否 |
| 31 | cand.ds.segment_tree_variants.range_assign_lazy | 线段树变体：Range Assign Lazy | 3.13 | yellow | external_b1 | 否 |
| 32 | cand.ds.segment_tree_variants.segment_tree_of_vectors | 线段树变体：Segment Tree Of Vectors | 3.13 | yellow | external_b1 | 否 |
| 33 | cand.ds.segment_tree_variants.segment_tree_over_time | 线段树变体：Segment Tree Over Time | 3.13 | yellow | external_b1 | 否 |
| 34 | cand.ds.segment_tree_variants.two_dimensional_segment_tree | 线段树变体：Two Dimensional Segment Tree | 3.13 | yellow | external_b1 | 否 |
| 35 | cand.ds.succinct_probabilistic.van_emde_boas_overview | 简洁与概率结构：Van Emde Boas Overview | 3.13 | yellow | external_b1 | 否 |
| 36 | cand.dp.game.basic | 博弈DP基础 | 2.8 | yellow | external_b2 | 否 |
| 37 | cand.dp.game.grundy | Grundy数DP | 2.8 | yellow | external_b2 | 否 |
| 38 | cand.dp.matrix.basic | 矩阵DP基础 | 2.8 | yellow | external_b2 | 否 |
| 39 | cand.dp.matrix.fast_power | 矩阵快速幂DP | 2.8 | yellow | external_b2 | 否 |
| 40 | cand.dp.probability.expectation | 期望DP | 2.8 | yellow | external_b2 | 否 |
| 41 | cand.dp.probability.markov | 马尔可夫链DP | 2.8 | yellow | external_b2 | 否 |
| 42 | cand.math.graph.gaussian_elimination_gf2 | GF(2)上的高斯消元 | 4.5 | yellow | external_b2 | 否 |
| 43 | cand.math.graph.matrix_tree | 矩阵树定理 | 4.5 | yellow | external_b2 | 否 |
| 44 | cand.string.string_matching.sunday | Sunday算法 | 2.10 | yellow | external_b2 | 是 |
| 45 | cand.math.linear_recurrence.basic | 线性递推基础 | 4.4 | yellow | external_b2 | 是 |
| 46 | cand.math.linear_recurrence.kitamasa | Kitamasa算法 | 4.4 | yellow | external_b2 | 是 |
| 47 | cand.string.duval_algorithm.minimal_rotation | Duval算法最小表示 | 2.10 | medium | external_b2 | 否 |
| 48 | cand.string.hashing.2d_rolling_hash | 二维滚动哈希 | 2.10 | medium | external_b2 | 否 |
| 49 | cand.string.hashing.collision_strategy | 哈希碰撞处理策略 | 2.10 | medium | external_b2 | 否 |

## 3. 按 Source 分布

| Source | 数量 |
|--------|------|
| external_b1 | 35 |
| external_b2 | 14 |

## 4. 按 Section 分布

| Section | 数量 |
|---------|------|
| 2.10 | 4 |
| 2.21 | 20 |
| 2.8 | 6 |
| 3.13 | 15 |
| 4.4 | 2 |
| 4.5 | 2 |

## 5. 按 Risk Band 分布

| Risk Band | 数量 |
|-----------|------|
| green | 7 |
| medium | 3 |
| yellow | 39 |

## 6. Dependency Cleanup 结果

| 检查项 | 状态 |
|--------|------|
| dependency_cleanup_required | false - 清理已完成 |
| dependency_mapping_risk | [] - 已清理 |
| section_ref_dependencies | [] - 已清理 |
| section ID in direct_pre | 无 |
| 悬空引用 | 无 |
| 依赖环 | 无 |

## 7. 动态预审检查明细 (v2)

| 检查项 | 状态 | 详情 |
|--------|------|------|
| item_count | PASS | item_count = 1716, 预期 1716 |
| selected_candidate_count | PASS | 49 candidates selected |
| validate_only_passed | PASS | validate-only passed = True |
| dependency_cleanup_required | PASS | dependency_cleanup_required = false (cleanup completed) |
| dependency_mapping_risk | PASS | dependency_mapping_risk = [] (all cleaned) |
| section_ref_dependencies | PASS | section_ref_dependencies = [] |
| needs_new_section | PASS | needs_new_section = false |
| duplicate_check | PASS | excluded_duplicate_or_near_duplicate = [] |
| excluded_already_merged | PASS | 已排除80个历史已使用候选 |
| candidate_dependency_cycle | PASS | candidate_dependency_cycle = false |
| direct_pre_section_id_check | PASS | direct_pre 全部为 item id，不含 section id |
| manual_review_candidates | INFO | 3 candidates marked for manual review (medium confidence) |
| recommendation | PASS | ready_for_1号线程_merge_full49 |

## 8. 合并建议

| 建议 | 值 |
|------|-----|
| 建议操作 | ready_for_1号线程_merge_full49 |
| recommended_merge_count | 49 |
| 主图谱是否修改 | 否 |

## 9. 最终结论

- **候选数**: 49/49
- **推荐操作**: ready_for_1号线程_merge_full49
- **主图谱修改**: 否
- **仅运行 validate-only**: 是
- **未执行 Merge**: 是
- **dependency_cleanup_required**: false
- **3 个 medium 风险候选已标记 manual_review，需在合并阶段由 1 号线程处理**