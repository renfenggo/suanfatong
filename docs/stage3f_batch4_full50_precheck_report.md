# Stage3F Batch4 Full50 预审报告

**生成时间**: 2026-05-25 09:27:13 UTC
**生成者**: GLM5 (2号线程)
**任务类型**: 候选计划 + 动态预审（仅验证，不合并）

---

## 1. 当前主图谱状态

| 指标 | 值 |
|------|-----|
| item_count | 1716 |
| 预期 item_count | 1716 |
| section_count | 65 |
| validate-only passed | True |
| 主图谱是否修改 | 否 |

## 2. Batch4 Full50 候选列表

| # | candidate_id | name | section | risk | source | confidence |
|---|-------------|------|---------|------|--------|------------|
| 1 | cand.graph.closure_model.penalty_modeling | 最大权闭合子图：Penalty Modeling | 2.21 | green | external_b1 | high |
| 2 | cand.graph.dynamic_connectivity.connectivity_snapshots | 动态图连通性：Connectivity Snapshots | 2.21 | green | external_b1 | high |
| 3 | cand.graph.dynamic_connectivity.dynamic_biconnectivity | 动态图连通性：Dynamic Biconnectivity | 2.21 | green | external_b1 | high |
| 4 | cand.graph.dynamic_connectivity.dynamic_bridge | 动态图连通性：Dynamic Bridge | 2.21 | green | external_b1 | high |
| 5 | cand.graph.global_min_cut.minimum_cut_modeling | 全局最小割：Minimum Cut Modeling | 2.21 | green | external_b1 | high |
| 6 | cand.graph.scc_dag.component_topo_order | 强连通分量 DAG：Component Topo Order | 2.21 | green | external_b1 | high |
| 7 | cand.graph.scc_dag.scc_dp | 强连通分量 DAG：Scc Dp | 2.21 | green | external_b1 | high |
| 8 | cand.graph.difference_constraints.modeling.raw | 差分约束系统建模 | 2.21 | yellow | external_b1 | high |
| 9 | cand.graph.dynamic_connectivity.fully_dynamic_overview | 动态图连通性：Fully Dynamic Overview | 2.21 | yellow | external_b1 | high |
| 10 | cand.graph.hall_theorem.applications | Hall 定理及应用 | 2.21 | yellow | external_b1 | high |
| 11 | cand.graph.max_weight_closure.problem | 最大权闭合子图 | 2.21 | yellow | external_b1 | high |
| 12 | cand.graph.planar_graph.embedding_basics | 平面图：Embedding Basics | 2.21 | yellow | external_b1 | high |
| 13 | cand.graph.shortest_path_advanced.eppstein_k_shortest | 高级最短路：Eppstein K Shortest | 2.21 | yellow | external_b1 | high |
| 14 | cand.graph.shortest_path_advanced.johnson_potentials | 高级最短路：Johnson Potentials | 2.21 | yellow | external_b1 | high |
| 15 | cand.graph.shortest_path_advanced.min_cost_path_cover | 高级最短路：Min Cost Path Cover | 2.21 | yellow | external_b1 | high |
| 16 | cand.graph.shortest_path_advanced.replacement_paths | 高级最短路：Replacement Paths | 2.21 | yellow | external_b1 | high |
| 17 | cand.graph.shortest_path_advanced.resource_constrained | 高级最短路：Resource Constrained | 2.21 | yellow | external_b1 | high |
| 18 | cand.graph.shortest_path_advanced.yen_k_shortest | 高级最短路：Yen K Shortest | 2.21 | yellow | external_b1 | high |
| 19 | cand.graph.shortest_path_advanced.zero_one_bfs_modeling | 高级最短路：Zero One Bfs Modeling | 2.21 | yellow | external_b1 | high |
| 20 | cand.graph.two_sat.modeling_techniques | 2-SAT 建模技巧 | 2.21 | yellow | external_b1 | high |
| 21 | cand.ds.dsu_advanced.component_aggregate | 高级并查集：Component Aggregate | 3.13 | yellow | external_b1 | high |
| 22 | cand.ds.dsu_advanced.distance | 高级并查集：Distance | 3.13 | yellow | external_b1 | high |
| 23 | cand.ds.dsu_advanced.offline_dynamic_connectivity | 高级并查集：Offline Dynamic Connectivity | 3.13 | yellow | external_b1 | high |
| 24 | cand.ds.dsu_advanced.small_to_large | 高级并查集：Small To Large | 3.13 | yellow | external_b1 | high |
| 25 | cand.ds.dsu_advanced.weighted | 高级并查集：Weighted | 3.13 | yellow | external_b1 | high |
| 26 | cand.ds.li_chao_tree.cht_comparison | 李超线段树：Cht Comparison | 3.13 | yellow | external_b1 | high |
| 27 | cand.ds.persistent_structure.retroactive_overview | 可持久化结构：Retroactive Overview | 3.13 | yellow | external_b1 | high |
| 28 | cand.ds.segment_tree_variants.matrix_segment_tree | 线段树变体：Matrix Segment Tree | 3.13 | yellow | external_b1 | high |
| 29 | cand.ds.segment_tree_variants.merge.codex1 | 线段树变体：Merge 变体 1 | 3.13 | yellow | external_b1 | high |
| 30 | cand.ds.segment_tree_variants.persistent_segment_tree | 线段树变体：Persistent Segment Tree | 3.13 | yellow | external_b1 | high |
| 31 | cand.ds.segment_tree_variants.range_assign_lazy | 线段树变体：Range Assign Lazy | 3.13 | yellow | external_b1 | high |
| 32 | cand.ds.segment_tree_variants.segment_tree_of_vectors | 线段树变体：Segment Tree Of Vectors | 3.13 | yellow | external_b1 | high |
| 33 | cand.ds.segment_tree_variants.segment_tree_over_time | 线段树变体：Segment Tree Over Time | 3.13 | yellow | external_b1 | high |
| 34 | cand.ds.segment_tree_variants.two_dimensional_segment_tree | 线段树变体：Two Dimensional Segment Tree | 3.13 | yellow | external_b1 | high |
| 35 | cand.ds.succinct_probabilistic.van_emde_boas_overview | 简洁与概率结构：Van Emde Boas Overview | 3.13 | yellow | external_b1 | high |
| 36 | cand.dp.game.basic | 博弈DP基础 | 2.8 | yellow | external_b2 | high |
| 37 | cand.dp.game.grundy | Grundy数DP | 2.8 | yellow | external_b2 | high |
| 38 | cand.dp.matrix.basic | 矩阵DP基础 | 2.8 | yellow | external_b2 | high |
| 39 | cand.dp.matrix.fast_power | 矩阵快速幂DP | 2.8 | yellow | external_b2 | high |
| 40 | cand.dp.probability.expectation | 期望DP | 2.8 | yellow | external_b2 | high |
| 41 | cand.dp.probability.markov | 马尔可夫链DP | 2.8 | yellow | external_b2 | high |
| 42 | cand.math.graph.gaussian_elimination_gf2 | GF(2)上的高斯消元 | 4.5 | yellow | external_b2 | high |
| 43 | cand.math.graph.matrix_tree | 矩阵树定理 | 4.5 | yellow | external_b2 | high |
| 44 | cand.string.string_matching.sunday | Sunday算法 | 2.10 | yellow | external_b2 | medium |
| 45 | cand.math.linear_recurrence.basic | 线性递推基础 | 4.4 | yellow | external_b2 | medium |
| 46 | cand.math.linear_recurrence.kitamasa | Kitamasa算法 | 4.4 | yellow | external_b2 | medium |
| 47 | cand.string.duval_algorithm.minimal_rotation | Duval算法最小表示 | 2.10 | medium | external_b2 | high |
| 48 | cand.string.hashing.2d_rolling_hash | 二维滚动哈希 | 2.10 | medium | external_b2 | high |
| 49 | cand.string.hashing.collision_strategy | 哈希碰撞处理策略 | 2.10 | medium | external_b2 | high |

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

## 6. 重复/近重复检查结果

未发现重复/近重复候选。


## 7. 被排除候选及原因

- **已合并候选排除**: 80 个（Batch1: 20, Batch2: 20, Batch3: 40）
- **重复/近重复排除**: 0 个
- **总排除**: 80 个
- **可用未选**: 0 个

## 8. Dependency Cleanup 评估

| 检查项 | 结果 |
|--------|------|
| dependency_cleanup_required | True |
| dependency_mapping_risk 数 | 3 |
| section 密集警告数 | 2 |

映射风险候选：

- cand.string.string_matching.sunday: medium mapping confidence
- cand.math.linear_recurrence.basic: medium mapping confidence
- cand.math.linear_recurrence.kitamasa: medium mapping confidence

## 9. 合并建议

| 建议 | 值 |
|------|-----|
| 建议操作 | needs_dependency_cleanup_before_merge |
| recommended_merge_count | 49 |
| 主图谱是否修改 | 否 |

**结论**: 预审存在需处理的问题，建议先执行 dependency cleanup 后再合并。

## 10. 动态预审检查明细

| 检查项 | 状态 | 详情 |
|--------|------|------|
| item_count | ✅ pass | item_count = 1716, 预期 1716 |
| validate_only_passed | ✅ pass | validate-only passed = True |
| duplicate_check | ✅ pass | 严格重复守卫已执行，排除 0 个重复候选 |
| candidate_id_history_conflict | ✅ pass | 无候选 ID 冲突 |
| name_en_name_alias_conflict | ✅ pass | 无名称冲突 |
| high_risk_red_candidates | ✅ pass | 0 个 high risk/red 候选 |
| manual_review_strong_risk | ✅ pass | 0 个 manual_review 候选 |
| needs_new_section | ✅ pass | 是否需要新 section: False |
| dependency_mapping | ⚠️ warn | 3 个候选映射风险 |
| section_distribution | ℹ️ info | 6 个 section 涉及, 2 个 section 候选密集 |
| candidate_dependency_cycle | ✅ pass | 未检测到候选依赖环 |
| dependency_cleanup_required | ℹ️ info | dependency_cleanup_required = True |

## 11. 最终结论

- **候选数**: 49/50
- **推荐操作**: needs_dependency_cleanup_before_merge
- **主图谱修改**: 否
- **仅运行 validate-only**: 是
- **未执行 Merge**: 是
- **未自动降级**: 是