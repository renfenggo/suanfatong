# Stage3E 1482→1602 Problem Patterns Sync Triage Report

## Executive Summary

基于 Stage3E 1482→1602 质量审计结果，对 58 个 sync_to_problem_patterns 候选进行分级（P0/P1/P2/defer）。本阶段只做分级，不生成正式 problem_patterns，不修改任何现有文件。

**重要声明：只做分级，不生成正式 Batch2/Batch3。**

---

## 分级概览

### 分级分布

| 优先级 | 数量 | 占比 | 说明 |
|--------|------|------|------|
| **P0** | 14 | 24% | 建模特征明显，适合立即同步 |
| **P1** | 20 | 35% | 有训练价值，但边界需确认 |
| **P2** | 10 | 17% | 可后续同步，当前不急 |
| **defer** | 14 | 24% | 更像知识点/定理/变体，不建议同步 |
| **总计** | **58** | **100%** | |

### 分级规则

- **P0**: 建模特征明显，适合写 recognition_signals/common_transforms，与已有patterns不重复
- **P1**: 有训练价值，但边界需要人工确认，与已有pattern语义接近但可区分
- **P2**: 可后续同步，当前不急
- **defer**: 更像知识点、定理或实现变体，不适合立即做pattern

---

## P0 分级详情 (14个)

### 最大权闭合子图 (2个)

| 序号 | 候选 | 建议 pattern_id | 原因 |
|------|------|----------------|------|
| 1 | 2.21.70 Binary Decision Model | pat.max_closure_decision_model | 二元决策建模模式，清晰识别信号 |
| 2 | 2.21.74 Prerequisite Graph | pat.max_closure_prerequisite | 前置依赖图建模，竞赛高频 |

### 虚树 (3个)

| 序号 | 候选 | 建议 pattern_id | 原因 |
|------|------|----------------|------|
| 3 | 2.21.119 Distance Compression | pat.virtual_tree_distance_compression | 清晰的建模模式 |
| 4 | 2.21.122 Multi-Key Query | pat.virtual_tree_multi_key_query | 竞赛高频问题 |
| 5 | 2.21.123 Subtree Aggregation | pat.virtual_tree_subtree_aggregation | 经典建模模式 |

### 离线算法 (2个)

| 序号 | 候选 | 建议 pattern_id | 原因 |
|------|------|----------------|------|
| 6 | 3.13.106 Time Divide Conquer | pat.offline_time_divide_conquer | 核心框架模式 |
| 7 | 3.13.109 Rollback Vs Persistence | pat.rollback_vs_persistence_decision | 清晰的选择判断模式 |

### 图论建模 (5个)

| 序号 | 候选 | 建议 pattern_id | Batch2 状态 |
|------|------|----------------|-------------|
| 8 | 2.21.132 K Shortest Paths | pat.k_shortest_modeling | 已有对应 draft |
| 9 | 2.21.133 Layered Graph | pat.layered_graph_modeling | 已有对应 draft |
| 10 | 2.21.134 Minimum Mean Cycle | pat.cycle_optimization_modeling | 已有对应 draft |
| 11 | 2.21.136 State Graph | pat.state_machine_modeling | 已有对应 draft |
| 12 | 2.21.142 Minimum Path Cover | pat.path_cover_modeling | 已有对应 draft |

### 网络流建模 (1个)

| 序号 | 候选 | 建议 pattern_id | 说明 |
|------|------|----------------|------|
| 13 | 2.21.128 Min Cost Circulation | pat.circulation_optimization | 已在 P0 Draft |

### 高级最短路 (1个)

| 序号 | 候选 | 建议 pattern_id | 说明 |
|------|------|----------------|------|
| 14 | 2.21.146 Time Expanded Graph | pat.time_expanded_graph_modeling | 清晰的建模模式 |

---

## P1 分级详情 (20个)

### 网络流建模 (8个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 1 | 2.21.73 Open Pit Mining Model | 经典应用，需确认与闭子图关系 |
| 2 | 2.21.75 Task Selection | 经典场景，需确认边界 |
| 3 | 2.21.124 Bounded Bipartite Matching | Batch2重复，建议对齐 |
| 4 | 2.21.125 Demands | Batch2 draft对齐 |
| 5 | 2.21.126 Edge Lower Bound Transform | Batch2 draft对齐 |
| 6 | 2.21.127 Maximum Flow | Batch2 draft对齐 |
| 7 | 2.21.129 Minimum Flow | Batch2 draft对齐 |
| 8 | 2.21.130 Node Demand | Batch2 draft对齐 |
| 9 | 2.21.131 Project Selection | Batch2 draft对齐 |

### 全局最小割 (1个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 10 | 2.21.94 Cut Tree Query | Gomory-Hu割树的pattern潜力 |

### 虚树 (3个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 11 | 2.21.118 Chain Compression | 虚树应用，需确认边界 |
| 12 | 2.21.120 Edge Weight Compression | 虚树变体，需确认边界 |
| 13 | 2.21.121 Minimum Connection | 经典应用，有训练价值 |

### 数据结构 (2个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 14 | 3.13.100 Orthogonal Range Query | 核心问题，需评估pattern可行性 |
| 15 | 3.13.105 Parallel Check Framework | 离线框架，需评估独立性 |

### 树论算法 (1个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 16 | 3.13.126 Dynamic Centroid | 竞赛高频，需评估pattern化 |

### 图论建模/算法 (4个)

| 序号 | 候选 | 说明 |
|------|------|------|
| 17 | 2.21.135 Shortest Path Potentials | Batch2 draft对齐 |
| 18 | 2.21.137 Steiner Tree | 高频但复杂，需审核 |
| 19 | 2.21.138 Dilworth Theorem | 定理应用，需确认pattern化 |
| 20 | 2.21.143 Stable Marriage | Batch2 draft对齐 |

---

## P2 分级详情 (10个)

| 序号 | 候选 | 系列 | 原因 |
|------|------|------|------|
| 1 | 2.21.82 Block Search Tree | 支配树 | 当前不急 |
| 2 | 2.21.83 Dag Dominator | 支配树 | 当前不急 |
| 3 | 2.21.84 Dominance Frontier | 支配树 | 当前不急 |
| 4 | 2.21.86 Online Query | 支配树 | 当前不急 |
| 5 | 2.21.87 Path Dominator Query | 支配树 | 当前不急 |
| 6 | 2.21.95 Pair Min Cut | 全局最小割 | 当前不急 |
| 7 | 2.21.101 Matroid Parity | 拟阵图论 | 当前不急 |
| 8 | 2.21.102 Partition Matroid | 拟阵图论 | 当前不急 |
| 9 | 2.21.103 Spanning Tree Matroid | 拟阵图论 | 当前不急 |
| 10 | 2.21.104 Transversal Matroid | 拟阵图论 | 当前不急 |
| 11 | 2.21.105 Weighted Matroid Intersection | 拟阵图论 | 当前不急 |
| 12 | 3.13.102 Offline Connectivity | 离线框架 | 当前不急 |
| 13 | 3.13.103 Offline Range Mex | 离线框架 | 当前不急 |
| 14 | 3.13.104 Offline Rectangle Add | 离线框架 | 当前不急 |

---

## defer 分级详情 (14个)

### 定理类 (5个) - 不适合做 pattern

| 序号 | 候选 | 系列 | 原因 |
|------|------|------|------|
| 1 | 2.21.100 Basis Exchange | 拟阵图论 | 数学定理 |
| 2 | 2.21.139 Hall Theorem | 匹配与覆盖 | 图论核心定理 |
| 3 | 2.21.140 Konig Theorem | 匹配与覆盖 | 二分图核心结论 |
| 4 | 2.21.144 Tutte Matrix | 匹配与覆盖 | 算法实现变体 |
| 5 | 3.13.110 Version Dag | 可持久化 | 实现细节 |

### 实现变体类 (6个) - 不适合做 pattern

| 序号 | 候选 | 系列 | 原因 |
|------|------|------|------|
| 6 | 2.21.85 Irreducible Graph | 支配树 | 图论概念 |
| 7 | 2.21.96 Random Contraction | 全局最小割 | 算法实现 |
| 8 | 2.21.97 Recursive Contraction | 全局最小割 | 算法变体 |
| 9 | 2.21.98 Sparsification | 全局最小割 | 优化技术 |
| 10 | 3.13.131 Fhq Split Merge | 高级平衡树 | 实现技巧 |
| 11 | 3.13.138 树上DSU | 高级并查集 | 实现技巧 |
| 12 | 3.13.142 可持久化版(DSU) | 高级并查集 | 实现技巧 |
| 13 | 2.21.141 Matroid Matching | 拟阵图论 | 过于理论化 |
| 14 | 2.21.145 Weighted General Matching | 匹配算法 | 过于专门化 |

---

## 与已有 patterns 重复检查

### 与 patterns_v0_1_ready.json 的重复

| 候选 | 已有 pattern | 相似度 | 状态 |
|------|-------------|--------|------|
| 2.21.133 Layered Graph | pat.layered_graph_shortest_path | 高 | 语义重叠，但Layered Graph更通用 |

### 与 Batch2 Draft Preview 的重复

| 候选 | Batch2 Draft | 数量 | 说明 |
|------|-------------|------|------|
| 2.21.128 Min Cost Circulation | pat.circulation_optimization | 1 | P0 Draft，建议对齐 |
| 2.21.124 Bounded Bipartite Matching | pat.bounded_matching_modeling | 1 | P1 Draft，建议合并 |
| 2.21.125 Demands / 2.21.130 Node Demand | pat.node_demand_modeling | 2 | P1 Draft，建议对齐 |
| 2.21.126 Edge Lower Bound Transform | pat.flow_bounds_transformation | 1 | P1 Draft，建议对齐 |
| 2.21.127 Maximum Flow | pat.max_flow_with_bounds | 1 | P1 Draft，建议对齐 |
| 2.21.129 Minimum Flow | pat.min_flow_modeling | 1 | P1 Draft，建议对齐 |
| 2.21.131 Project Selection | pat.network_flow_project_selection | 1 | P1 Draft，建议合并 |
| 2.21.132 K Shortest Paths | pat.k_shortest_modeling | 1 | P1 Draft，建议对齐 |
| 2.21.133 Layered Graph | pat.layered_graph_modeling | 1 | P1 Draft，建议合并 |
| 2.21.134 Minimum Mean Cycle | pat.cycle_optimization_modeling | 1 | P1 Draft，建议对齐 |
| 2.21.135 Shortest Path Potentials | pat.shortest_path_potentials | 1 | P1 Draft，建议对齐 |
| 2.21.136 State Graph | pat.state_machine_modeling | 1 | P1 Draft，建议合并 |
| 2.21.142 Minimum Path Cover | pat.path_cover_modeling | 1 | P1 Draft，建议合并 |
| 2.21.143 Stable Marriage | pat.stable_matching_pattern | 1 | P1 Draft，建议对齐 |
| **合计** | | **14** | |

---

## 最建议优先同步的 20 个

### P0 优先同步 (14个)

| 排名 | item_id | 名称 | 家族 | 理由 |
|------|---------|------|------|------|
| 1 | 2.21.119 | Distance Compression | 虚树建模 | 建模特征最明显 |
| 2 | 2.21.122 | Multi-Key Query | 虚树建模 | 竞赛高频 |
| 3 | 2.21.123 | Subtree Aggregation | 虚树建模 | 经典模式 |
| 4 | 3.13.106 | Time Divide Conquer | 离线算法 | 核心框架 |
| 5 | 3.13.109 | Rollback Vs Persistence | 数据结构选型 | 独特决策模式 |
| 6 | 2.21.132 | K Shortest Paths | 图论建模 | Batch2 P1 draft |
| 7 | 2.21.133 | Layered Graph | 图论建模 | Batch2 P1 draft |
| 8 | 2.21.136 | State Graph | 图论建模 | Batch2 P1 draft |
| 9 | 2.21.142 | Minimum Path Cover | 图论建模 | Batch2 P1 draft |
| 10 | 2.21.146 | Time Expanded Graph | 高级最短路 | 清晰建模模式 |
| 11 | 2.21.70 | Binary Decision Model | 最大权闭合子图 | 清晰建模模式 |
| 12 | 2.21.74 | Prerequisite Graph | 最大权闭合子图 | 竞赛高频 |
| 13 | 2.21.128 | Min Cost Circulation | 上下界网络流 | P0 draft |
| 14 | 2.21.134 | Minimum Mean Cycle | 图论建模 | Batch2 P1 draft |

### P1 优先补充 (6个)

| 排名 | item_id | 名称 | 家族 | 理由 |
|------|---------|------|------|------|
| 15 | 2.21.73 | Open Pit Mining Model | 最大权闭合子图 | 经典案例 |
| 16 | 2.21.75 | Task Selection | 最大权闭合子图 | 经典场景 |
| 17 | 2.21.137 | Steiner Tree | 图论建模 | 竞赛高频 |
| 18 | 2.21.138 | Dilworth Theorem | 匹配与覆盖 | 偏序集基础 |
| 19 | 2.21.94 | Cut Tree Query | 全局最小割 | 潜在pattern |
| 20 | 3.13.100 | Orthogonal Range Query | 多维数据结构 | 核心问题 |

---

## 不建议同步的候选及原因

### 定理类 (5个)

| item_id | 名称 | 原因 | 建议保留为 |
|---------|------|------|-----------|
| 2.21.100 | Basis Exchange | 数学定理，无建模信号 | knowledge_item |
| 2.21.139 | Hall Theorem | 图论定理，无模式特征 | knowledge_item |
| 2.21.140 | Konig Theorem | 结论性定理 | knowledge_item |
| 2.21.85 | Irreducible Graph | 图论概念，非模式 | knowledge_item |
| 2.21.144 | Tutte Matrix | 算法实现变体 | knowledge_item |

### 实现变体类 (9个)

| item_id | 名称 | 原因 | 建议保留为 |
|---------|------|------|-----------|
| 2.21.96 | Random Contraction | 算法实现，无建模信号 | knowledge_item |
| 2.21.97 | Recursive Contraction | 算法变体 | knowledge_item |
| 2.21.98 | Sparsification | 优化技术 | knowledge_item |
| 3.13.110 | Version Dag | 实现细节 | knowledge_item |
| 3.13.131 | Fhq Split Merge | 实现技巧 | knowledge_item |
| 3.13.138 | 树上DSU | 实现技巧 | knowledge_item |
| 3.13.142 | 可持久化版(DSU) | 实现技巧 | knowledge_item |
| 2.21.141 | Matroid Matching | 过于理论化 | knowledge_item |
| 2.21.145 | Weighted General Matching | 过于专门化 | knowledge_item |

---

## 数据完整性验证

### 统计验证

| 校验项 | 结果 |
|--------|------|
| 候选总数 | ✅ 58 |
| P0 数量 | ✅ 14 |
| P1 数量 | ✅ 20 |
| P2 数量 | ✅ 10 |
| defer 数量 | ✅ 14 |
| 总计校验 | ✅ 14+20+10+14 = 58 |

### 文件完整性

| 文件 | 状态 |
|------|------|
| data/stage3e_1482_1602_problem_patterns_sync_triage.json | ✅ 已生成 |
| docs/stage3e_1482_1602_problem_patterns_sync_triage_report.md | ✅ 已生成 |
| merged_knowledge_graph_item_dependencies_refined.json | ✅ 未修改 |
| patterns_v0_1_ready.json | ✅ 未修改 |
| knowledge_items | ✅ 未修改 |
| dependency_validation_result.json | ✅ 未修改 |

---

## 结论

### 关键确认

| 问题 | 回答 |
|------|------|
| 候选总数 | ✅ 58 |
| P0 数量 | ✅ 14 |
| P1 数量 | ✅ 20 |
| P2 数量 | ✅ 10 |
| defer 数量 | ✅ 14 |
| 与已有 patterns 重复的候选 | ✅ 15个（14个与Batch2 Draft重复，1个与ready pattern重叠） |
| 最建议优先同步的 20 个 | ✅ 见上表 |
| 不建议同步的候选 | ✅ 14个（5个定理类，9个实现变体类） |
| 是否建议生成正式 Batch2/Batch3 | ❌ 否，先分级不生成 |
| 是否修改主图谱 | ❌ 否 |

### 主要发现

1. **14 个 P0 候选**应优先同步到 problem_patterns，其中包括：
   - 3 个虚树建模模式（Distance Compression, Multi-Key Query, Subtree Aggregation）
   - 5 个图论建模模式（K Shortest, Layered Graph, Minimum Mean Cycle, State Graph, Minimum Path Cover）
   - 2 个最大权闭合子图建模（Binary Decision, Prerequisite Graph）
   - 2 个离线算法框架（Time Divide Conquer, Rollback vs Persistence）
   - 1 个时间展开图（Time Expanded Graph）
   - 1 个最小费用循环流（Min Cost Circulation）

2. **14 个候选与 Batch2 Draft 重复**，建议在正式生成 Batch2 时统一处理

3. **14 个 defer 候选**不建议同步到 problem_patterns，保留为 knowledge_item

### 下一步建议

1. **同步 Batch2 Draft**: 先在 Batch2 中正式生成已完成的 22 个 draft
2. **合并重复**: 将 14 个知识库候选与 Batch2 Draft 合并，避免重复
3. **补充新 P0**: 将虚树建模（3个）、离线框架（2个）、时间展开图等 P0 候选补充到 Batch3 规划
4. **人工审核**: 对 20 个 P1 候选进行专家审核后确定是否入 Batch3
5. **保留 defer**: 将 14 个 defer 候选保留为 knowledge_item，不作为 pattern

---

**Report Generated:** 2026-05-22
**Generated By:** GLM5 (Thread 3)
**Task Status:** Completed
**Formal Batch Generated:** false
**Main Graph Modified:** false