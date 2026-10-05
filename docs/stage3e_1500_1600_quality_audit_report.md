# Stage3E 1500-1600 Quality Audit Report

## 1. 审查范围

本次只审查 Stage3E Aggressive Batch1~Batch4 新增节点，不修改主图谱、不修改依赖、不新增/删除 item。主图谱当前验证快照：item_count=1602，section_count=65，passed=true，report_matches_json=true。

## 2. 数量概览

- 新增节点总数：120
- Batch1：30
- Batch2：30
- Batch3：30
- Batch4：30
- A/B/C/D/E 分布：A=6，B=41，C=9，D=33，E=31
- 建议保留数量：56
- 建议合并/精简数量：33
- 建议转入 problem_patterns 数量：31
- 高重复风险数量：2
- 依赖可疑数量：75

## 3. 各系列质量结论

- Advanced Balanced Tree：10 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"B":4,"D":6}
- Flow With Lower Bounds：8 个，整体可保留，评级分布 {"E":2,"B":6}
- Matroid in Graphs：7 个，专家级内容，建议低优先展示并人工复查，评级分布 {"B":7}
- Virtual Tree Applications：7 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"E":7}
- Matching and Cover：7 个，整体可保留，评级分布 {"A":4,"E":1,"B":2}
- Maximum Closure：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"E":5,"A":1}
- Directed MST：6 个，整体可保留，评级分布 {"B":4,"D":1,"E":1}
- Dominator Tree：6 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"D":6}
- Dynamic MST：6 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"D":6}
- Global Min-Cut：6 个，整体可保留，评级分布 {"B":6}
- Planar Graph：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"E":3,"B":3}
- Graph Modeling：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"E":6}
- Special Graph：5 个，整体可保留，评级分布 {"B":5}
- Offline DS Framework：5 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"B":1,"E":3,"A":1}
- Advanced RMQ：5 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"D":5}
- Sequence Maintenance：5 个，整体可保留，评级分布 {"C":3,"E":2}
- Succinct/Probabilistic Structure：5 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"D":5}
- Persistent Data Structure：4 个，过度拆分风险高，建议合并为上级知识点并保留子主题，评级分布 {"D":4}
- Tree Decomposition DS：4 个，整体可保留，评级分布 {"C":4}
- Multidimensional DS：2 个，整体可保留，评级分布 {"B":2}
- Advanced DSU：2 个，整体可保留，评级分布 {"C":2}
- SCC Condensation DAG：1 个，整体可保留，评级分布 {"B":1}
- 2.21：1 个，更偏题型/建模模式，建议迁移到 problem_patterns，评级分布 {"E":1}

## 4. 最值得保留的 20 个节点

1. 2.21.71 最大权闭合子图：Maximum Weight Closure [A]：最大权闭合子图是稳定核心概念，适合作为独立知识点长期保留。
2. 2.21.76 有向生成树：Branching Theorem [B]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。
3. 2.21.77 有向生成树：Maximum Arborescence [B]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。
4. 2.21.78 有向生成树：Minimum Arborescence [B]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。
5. 2.21.81 有向生成树：Weighted Directed Mst [B]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。
6. 2.21.94 全局最小割：Cut Tree Query [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
7. 2.21.95 全局最小割：Pair Min Cut [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
8. 2.21.96 全局最小割：Random Contraction [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
9. 2.21.97 全局最小割：Recursive Contraction [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
10. 2.21.98 全局最小割：Sparsification [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
11. 2.21.99 全局最小割：Undirected Min Cut [B]：全局最小割系列概念稳定，但需补充边界和依赖说明。
12. 2.21.100 拟阵图论：Basis Exchange [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
13. 2.21.101 拟阵图论：Matroid Parity [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
14. 2.21.102 拟阵图论：Partition Matroid [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
15. 2.21.103 拟阵图论：Spanning Tree Matroid [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
16. 2.21.104 拟阵图论：Transversal Matroid [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
17. 2.21.105 拟阵图论：Weighted Matroid Intersection [B]：拟阵相关内容稳定但偏专家级，建议低优先展示并人工复查。
18. 2.21.107 平面图：Face Traversal [B]：平面图概念可保留，但属于专家扩展，需人工确认范围。
19. 2.21.108 平面图：Outerplanar Graph [B]：平面图概念可保留，但属于专家扩展，需人工确认范围。
20. 2.21.110 平面图：Planar Separator [B]：平面图概念可保留，但属于专家扩展，需人工确认范围。

## 5. 最需要人工复查的 20 个节点

1. 2.21.70 最大权闭合子图：Binary Decision Model [E/move_to_problem_patterns]：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。；依赖问题=none
2. 2.21.72 最大权闭合子图：Minimum Cut Transform [E/move_to_problem_patterns]：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。；依赖问题=none
3. 2.21.73 最大权闭合子图：Open Pit Mining Model [E/move_to_problem_patterns]：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。；依赖问题=suspicious_same_pre
4. 2.21.74 最大权闭合子图：Prerequisite Graph [E/move_to_problem_patterns]：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。；依赖问题=suspicious_same_pre
5. 2.21.75 最大权闭合子图：Task Selection [E/move_to_problem_patterns]：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。；依赖问题=suspicious_same_pre
6. 2.21.76 有向生成树：Branching Theorem [B/keep_manual_review]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。；依赖问题=none
7. 2.21.77 有向生成树：Maximum Arborescence [B/keep_manual_review]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。；依赖问题=none
8. 2.21.78 有向生成树：Minimum Arborescence [B/keep_manual_review]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。；依赖问题=none
9. 2.21.79 有向生成树：Rooted Arborescence [D/merge_later]：更像有向生成树的子概念，建议并入上级节点。；依赖问题=suspicious_same_pre
10. 2.21.80 有向生成树：Super Root Model [E/move_to_problem_patterns]：Super Root Model 是建模技巧，不宜作为独立百科节点。；依赖问题=suspicious_same_pre
11. 2.21.81 有向生成树：Weighted Directed Mst [B/keep_manual_review]：有向生成树核心概念可保留，但应与上级 Directed MST 边界统一。；依赖问题=suspicious_same_pre
12. 2.21.82 支配树：Bridge Relation [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=none
13. 2.21.83 支配树：Dag Dominator [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=none
14. 2.21.84 支配树：Dominance Frontier [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=none
15. 2.21.85 支配树：Dominator Tree Dp [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=suspicious_same_pre
16. 2.21.86 支配树：Online Query [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=suspicious_same_pre
17. 2.21.87 支配树：Path Dominator Query [D/merge_later]：支配树系列拆分过细，适合合并为支配树核心节点下的子主题。；依赖问题=suspicious_same_pre
18. 2.21.88 动态最小生成树：Batch Recomputation [D/merge_later]：动态 MST 系列实现/场景变体过多，建议合并精简。；依赖问题=missing_core_pre
19. 2.21.89 动态最小生成树：Certificate Graph [D/merge_later]：动态 MST 系列实现/场景变体过多，建议合并精简。；依赖问题=missing_core_pre
20. 2.21.90 动态最小生成树：Divide Conquer Approach [D/merge_later]：动态 MST 系列实现/场景变体过多，建议合并精简。；依赖问题=missing_core_pre

## 6. 最可能过度拆分的系列

- Advanced Balanced Tree：10 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 3.13.131, 3.13.132, 3.13.133, 3.13.134, 3.13.135, 3.13.136, 3.13.137, 3.13.138, 3.13.139, 3.13.140
- Matroid in Graphs：7 个，专家级内容，建议低优先展示并人工复查，涉及 2.21.100, 2.21.101, 2.21.102, 2.21.103, 2.21.104, 2.21.105, 2.21.141
- Virtual Tree Applications：7 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 2.21.118, 2.21.119, 2.21.120, 2.21.121, 2.21.122, 2.21.123, 3.13.130
- Maximum Closure：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 2.21.70, 2.21.71, 2.21.72, 2.21.73, 2.21.74, 2.21.75
- Dominator Tree：6 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 2.21.82, 2.21.83, 2.21.84, 2.21.85, 2.21.86, 2.21.87
- Dynamic MST：6 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 2.21.88, 2.21.89, 2.21.90, 2.21.91, 2.21.92, 2.21.93
- Planar Graph：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 2.21.106, 2.21.107, 2.21.108, 2.21.109, 2.21.110, 2.21.116
- Graph Modeling：6 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 2.21.132, 2.21.133, 2.21.134, 2.21.135, 2.21.136, 2.21.137
- Offline DS Framework：5 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 3.13.102, 3.13.103, 3.13.104, 3.13.105, 3.13.106
- Advanced RMQ：5 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 3.13.111, 3.13.112, 3.13.113, 3.13.114, 3.13.115
- Succinct/Probabilistic Structure：5 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 3.13.121, 3.13.122, 3.13.123, 3.13.124, 3.13.125
- Persistent Data Structure：4 个，过度拆分风险高，建议合并为上级知识点并保留子主题，涉及 3.13.107, 3.13.108, 3.13.109, 3.13.110
- 2.21：1 个，更偏题型/建模模式，建议迁移到 problem_patterns，涉及 2.21.146

## 7. problem_patterns 迁移建议

1. 2.21.70 最大权闭合子图：Binary Decision Model -> pattern.maximum_closure_binary_decision_model：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。
2. 2.21.72 最大权闭合子图：Minimum Cut Transform -> pattern.maximum_closure_minimum_cut_transform：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。
3. 2.21.73 最大权闭合子图：Open Pit Mining Model -> pattern.maximum_closure_open_pit_mining_model：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。
4. 2.21.74 最大权闭合子图：Prerequisite Graph -> pattern.maximum_closure_prerequisite_graph：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。
5. 2.21.75 最大权闭合子图：Task Selection -> pattern.maximum_closure_task_selection：更像最大权闭合子图的建模/转化套路，应转入 problem_patterns。
6. 2.21.80 有向生成树：Super Root Model -> pattern.directed_mst_super_root_model：Super Root Model 是建模技巧，不宜作为独立百科节点。
7. 2.21.106 平面图：Dual Shortest Path -> pattern.planar_graph_dual_shortest_path：更像平面图对偶建模/转化套路。
8. 2.21.109 平面图：Planar Min Cut -> pattern.planar_graph_planar_min_cut：更像平面图对偶建模/转化套路。
9. 2.21.116 特殊图：Planar Dual Graph -> pattern.special_graph_planar_dual_graph：更像平面图对偶建模/转化套路。
10. 2.21.118 虚树：Colored Points -> pattern.virtual_tree_colored_points：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
11. 2.21.119 虚树：Distance Compression -> pattern.virtual_tree_distance_compression：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
12. 2.21.120 虚树：Edge Weight Compression -> pattern.virtual_tree_edge_weight_compression：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
13. 2.21.121 虚树：Minimum Connection -> pattern.virtual_tree_minimum_connection：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
14. 2.21.122 虚树：Multi-Key Query -> pattern.virtual_tree_multi_key_query：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
15. 2.21.123 虚树：Subtree Aggregation -> pattern.virtual_tree_subtree_aggregation：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
16. 3.13.103 离线数据结构框架：Offline Range Mex -> pattern.offline_data_structure_framework_offline_range_mex：离线数据结构的具体题型套路，应转 problem_patterns。
17. 3.13.104 离线数据结构框架：Offline Rectangle Add -> pattern.offline_data_structure_framework_offline_rectangle_add：离线数据结构的具体题型套路，应转 problem_patterns。
18. 3.13.105 离线数据结构框架：Parallel Check Framework -> pattern.offline_data_structure_framework_parallel_check_framework：离线数据结构的具体题型套路，应转 problem_patterns。
19. 3.13.118 序列维护结构：Range Hash Maintenance -> pattern.sequence_maintenance_structure_range_hash_maintenance：更像序列维护应用模型，应转 problem_patterns。
20. 3.13.120 序列维护结构：Text Editor Model -> pattern.sequence_maintenance_structure_text_editor_model：更像序列维护应用模型，应转 problem_patterns。
21. 3.13.130 树分治维护：Virtual Tree Plus Hld -> pattern.tree_decomposition_data_structure_virtual_tree_plus_hld：虚树系列多为查询场景和建模套路，适合 problem_patterns 或子主题。
22. 2.21.124 上下界网络流：Bounded Bipartite Matching -> pattern.flow_with_lower_bounds_bounded_bipartite_matching：上下界网络流具体建模题型，应进入 problem_patterns。
23. 2.21.131 上下界网络流：Project Selection -> pattern.flow_with_lower_bounds_project_selection：上下界网络流具体建模题型，应进入 problem_patterns。
24. 2.21.132 图论建模：K Shortest Paths -> pattern.graph_modeling_k_shortest_paths：图论建模系列核心价值在题型转化，应转 problem_patterns。
25. 2.21.133 图论建模：Layered Graph -> pattern.graph_modeling_layered_graph：图论建模系列核心价值在题型转化，应转 problem_patterns。
26. 2.21.134 图论建模：Minimum Mean Cycle -> pattern.graph_modeling_minimum_mean_cycle：图论建模系列核心价值在题型转化，应转 problem_patterns。
27. 2.21.135 图论建模：Shortest Path Potentials -> pattern.graph_modeling_shortest_path_potentials：图论建模系列核心价值在题型转化，应转 problem_patterns。
28. 2.21.136 图论建模：State Graph -> pattern.graph_modeling_state_graph：图论建模系列核心价值在题型转化，应转 problem_patterns。
29. 2.21.137 图论建模：Steiner Tree -> pattern.graph_modeling_steiner_tree：图论建模系列核心价值在题型转化，应转 problem_patterns。
30. 2.21.142 匹配与覆盖：Minimum Path Cover -> pattern.matching_and_cover_minimum_path_cover：最小路径覆盖通常作为匹配转化题型训练。
31. 2.21.146 高级最短路：Time Expanded Graph -> pattern.advanced_shortest_path_time_expanded_graph：更像题型建模/转化套路，核心价值在识别题意并映射到已知算法。

## 8. Batch5 建议

不建议直接继续 Batch5。更稳妥的模式是 pause_and_cleanup：先处理 Stage3E Batch1~4 中的建模套路、同前置密集变体和专家级过细节点。如果业务上必须继续，建议缩小到 15 个，并只允许 A/B 级核心概念进入。

## 9. 最终结论

1. 1500~1600 这批节点整体质量：中等偏可用。核心概念不少，但混入了较多建模套路、实现变体和专家级细分节点。
2. 是否存在明显“为了扩数量而过度拆分”的问题：存在，尤其是 Dominator Tree、Dynamic MST、Persistent Structure、Advanced RMQ、Succinct/Probabilistic、Advanced Balanced Tree 等系列。
3. 最值得保留的系列：Maximum Closure 的核心节点、Global Min-Cut、Special Graph、Offline DS Framework 中的框架节点、Tree Decomposition DS、Matching/Cover 中的定理节点、部分 Advanced Balanced Tree 核心实现。
4. 最应该合并/精简的系列：Persistent Data Structure、Advanced RMQ、Succinct/Probabilistic Structure、Dynamic MST、Dominator Tree、Virtual Tree Applications、高级平衡树中的实现变体。
5. 应转 problem_patterns 的节点：详见 data/stage3e_1500_1600_quality_audit.json 中 problem_pattern_migration_suggestions，优先处理 Project Selection、K Shortest Paths、Layered/State Graph、Time Expanded Graph、Maximum Closure 应用模型、Virtual Tree 查询模型。
6. 是否建议继续 Batch5：不建议立即继续。
7. 如果继续 Batch5：不要一次 30 个，缩小到 15 个，并采用严格白名单。

主图谱是否被修改：否。
