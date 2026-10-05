# Stage3E Problem Patterns Sync Conflict Resolution Report

## Executive Summary

基于 Stage3E 1482→1602 Problem Patterns Sync Triage 结果，对 34 个 P0/P1 候选进行冲突分辨率分析。本阶段只做冲突合并规划，不生成正式 patterns，不修改任何已有文件。

**重要声明：只做冲突合并规划，不生成正式 patterns。**

---

## Resolution Statistics

### 整体统计

| 分辨率类型 | 数量 | 占比 | 说明 |
|-----------|------|------|------|
| **reuse_existing_ready_pattern** | 0 | 0% | 无直接适用 ready pattern |
| **merge_with_batch2_draft** | 15 | 44% | 与 Batch2 draft 对齐 |
| **create_new_draft_later** | 7 | 21% | 新建 draft，建议 Batch3 |
| **manual_review** | 12 | 35% | 需专家审核 |
| **defer_due_to_overlap** | 0 | 0% | 无需因重叠暂缓 |
| **总计** | **34** | **100%** | |

### 按优先级分布

| 分辨率类型 | P0 | P1 | 合计 |
|-----------|----|----|------|
| merge_with_batch2_draft | 6 | 9 | 15 |
| create_new_draft_later | 7 | 0 | 7 |
| manual_review | 1 | 11 | 12 |
| **合计** | **14** | **20** | **34** |

### High Similarity Conflicts

| 候选 | 冲突对象 | 级别 | 分辨率 |
|------|---------|------|--------|
| 2.21.133 Layered Graph | pat.layered_graph_shortest_path + pat.layered_graph_modeling | high | merge_with_batch2_draft |
| 2.21.131 Project Selection | pat.network_flow_project_selection + pat.network_flow_closure | high | merge_with_batch2_draft |

---

## Resolution Details

### P0 - merge_with_batch2_draft (6个)

这些候选与 Batch2 Draft Preview 中的模式完全对应，建议在正式 Batch2 生成时直接合并。

| 序号 | item_id | 名称 | Batch2 Draft | 状态 |
|------|---------|------|-------------|------|
| 1 | **2.21.128** | Min Cost Circulation | pat.circulation_optimization | P0 Draft |
| 2 | **2.21.132** | K Shortest Paths | pat.k_shortest_modeling | P1 Draft |
| 3 | **2.21.133** | Layered Graph | pat.layered_graph_modeling | P1 Draft |
| 4 | **2.21.134** | Minimum Mean Cycle | pat.cycle_optimization_modeling | P1 Draft |
| 5 | **2.21.136** | State Graph | pat.state_machine_modeling | P1 Draft |
| 6 | **2.21.142** | Minimum Path Cover | pat.path_cover_modeling | P1 Draft |

**处理建议：** 在正式生成 Batch2 时，将这 6 个知识库候选的内容（如题面参考、训练数据等）对齐到对应的 Batch2 正式模式。不需要新建模式，直接复用已有 draft。

### P0 - create_new_draft_later (7个)

这些候选是 P0 建模特征明显但不在 Batch2 中的新模式，建议在 Batch3 中创建新 draft。

| 序号 | item_id | 名称 | 建议 pattern_id | 建议 Batch |
|------|---------|------|----------------|------------|
| 1 | **2.21.70** | Binary Decision Model | pat.max_closure_decision_model | Batch3 |
| 2 | **2.21.74** | Prerequisite Graph | pat.max_closure_prerequisite | Batch3 |
| 3 | **2.21.119** | Distance Compression | pat.virtual_tree_distance_compression | Batch3 |
| 4 | **2.21.122** | Multi-Key Query | pat.virtual_tree_multi_key_query | Batch3 |
| 5 | **2.21.123** | Subtree Aggregation | pat.virtual_tree_subtree_aggregation | Batch3 |
| 6 | **3.13.106** | Time Divide Conquer | pat.offline_time_divide_conquer | Batch3 |
| 7 | **3.13.109** | Rollback Vs Persistence | pat.rollback_vs_persistence_decision | Batch3 |

**处理建议：** 在 Batch3 规划中创建这些候选的 draft。注意以下几点：
- 2.21.70 和 2.21.74 应与 pat.network_flow_closure 保持边界说明
- 2.21.119/122/123 都是虚树相关模式，需考虑是否统一为虚树系列
- 3.13.109 是独特的选择判断模式，在现有 patterns 中无类似内容

### P0 - manual_review (1个)

| 序号 | item_id | 名称 | 冲突对象 | 原因 |
|------|---------|------|---------|------|
| 1 | **2.21.146** | Time Expanded Graph | pat.time_expanded_graph (ready) | 与现有 ready pattern 语义接近，需要专家审核边界 |

**审核要点：**
- 此候选是"时间展开图的建模模式"，现有 pat.time_expanded_graph 覆盖的内容可能不同
- 需要确认：是全新的建模模式，还是现有 pattern 的不同表述？
- 建议专家组评估后决定：保留为新模式、合并到现有模式、或放弃

### P1 - merge_with_batch2_draft (9个)

| 序号 | item_id | 名称 | Batch2 Draft | 边界建议 |
|------|---------|------|-------------|----------|
| 1 | **2.21.124** | Bounded Bipartite Matching | pat.bounded_matching_modeling | 直接对齐 |
| 2 | **2.21.125** | Demands | pat.node_demand_modeling | 与 2.21.130 合并处理 |
| 3 | **2.21.126** | Edge Lower Bound Transform | pat.flow_bounds_transformation | 直接对齐 |
| 4 | **2.21.127** | Maximum Flow | pat.max_flow_with_bounds | 直接对齐 |
| 5 | **2.21.129** | Minimum Flow | pat.min_flow_modeling | 直接对齐 |
| 6 | **2.21.130** | Node Demand | pat.node_demand_modeling | 与 2.21.125 合并处理 |
| 7 | **2.21.131** | Project Selection | pat.network_flow_project_selection | 边界审查建议合并到 pat.network_flow_closure |
| 8 | **2.21.135** | Shortest Path Potentials | pat.shortest_path_potentials | 直接对齐 |
| 9 | **2.21.143** | Stable Marriage | pat.stable_matching_pattern | 直接对齐 |

### P1 - manual_review (11个)

这些候选有训练价值但边界需要专家确认。

| 序号 | item_id | 名称 | 审核要点 |
|------|---------|------|---------|
| 1 | **2.21.73** | Open Pit Mining Model | 作为最大权闭合子图案例，是否独立为模式 |
| 2 | **2.21.75** | Task Selection | 作为最大权闭合子图案例，是否独立为模式 |
| 3 | **2.21.94** | Cut Tree Query | Gomory-Hu割树的模式潜力评估 |
| 4 | **2.21.118** | Chain Compression | 虚树应用，与核心虚树模式的边界 |
| 5 | **2.21.120** | Edge Weight Compression | 虚树变体，与核心虚树模式的边界 |
| 6 | **2.21.121** | Minimum Connection | 虚树应用，是否独立为模式 |
| 7 | **3.13.100** | Orthogonal Range Query | 数据结构核心问题，是否适合做模式 |
| 8 | **3.13.105** | Parallel Check Framework | 离线算法模式可行性 |
| 9 | **3.13.126** | Dynamic Centroid | 树论算法是否适合做模式 |
| 10 | **2.21.137** | Steiner Tree | 竞赛高频，但复杂度和可行性评估 |
| 11 | **2.21.138** | Dilworth Theorem | 与 pat.partial_order_matching 的边界 |

---

## 优先进入正式 Batch2 的候选

以下候选可以直接进入正式 Batch2，因为它们已有完整的 draft preview，只需在正式生成时合并知识库内容：

| 优先级 | item_id | Batch2 Draft | 说明 |
|--------|---------|-------------|------|
| P0 | 2.21.128 | pat.circulation_optimization | P0 draft，优先处理 |
| P0 | 2.21.132 | pat.k_shortest_modeling | 建模模式，需处理与 pat.k_shortest_paths 的语义重叠 |
| P0 | 2.21.133 | pat.layered_graph_modeling | 需说明与 pat.layered_graph_shortest_path 的边界 |
| P0 | 2.21.134 | pat.cycle_optimization_modeling | 清晰，可直接对齐 |
| P0 | 2.21.136 | pat.state_machine_modeling | 清晰，可直接对齐 |
| P0 | 2.21.142 | pat.path_cover_modeling | 清晰，可直接对齐 |
| P1 | 2.21.124 | pat.bounded_matching_modeling | 清晰，可直接对齐 |
| P1 | 2.21.126 | pat.flow_bounds_transformation | 清晰，可直接对齐 |
| P1 | 2.21.127 | pat.max_flow_with_bounds | 清晰，可直接对齐 |
| P1 | 2.21.129 | pat.min_flow_modeling | 清晰，可直接对齐 |
| P1 | 2.21.135 | pat.shortest_path_potentials | 清晰，可直接对齐 |
| P1 | 2.21.143 | pat.stable_matching_pattern | 清晰，可直接对齐 |
| P1 | 2.21.130 | pat.node_demand_modeling | 与 2.21.125 合并 |
| P1 | 2.21.125 | pat.node_demand_modeling | 与 2.21.130 合并 |
| P1 | 2.21.131 | pat.network_flow_project_selection | 需处理合并到 pat.network_flow_closure |

**共 15 个候选**可以进入正式 Batch2，其中 6 个 P0，9 个 P1。

---

## 需要暂缓的候选

以下候选建议暂缓到 Batch3 或后续处理：

| 状态 | 数量 | item_id | 说明 |
|------|------|---------|------|
| **Batch3 创建新 draft** | 7 | 2.21.70, 2.21.74, 2.21.119, 2.21.122, 2.21.123, 3.13.106, 3.13.109 | P0 但不在 Batch2 中 |
| **需专家审核** | 12 | 2.21.73, 2.21.75, 2.21.94, 2.21.118, 2.21.120, 2.21.121, 2.21.137, 2.21.138, 2.21.146, 3.13.100, 3.13.105, 3.13.126 | P1 需边界确认 |

### 暂缓建议

1. **Batch3 候选（7个）：** P0 但不在 Batch2 范围，建议在 Batch3 中创建
   - 最大权闭合子图子模式（2个）：Binary Decision Model, Prerequisite Graph
   - 虚树系列（3个）：Distance Compression, Multi-Key Query, Subtree Aggregation
   - 离线算法（2个）：Time Divide Conquer, Rollback Vs Persistence

2. **专家审核候选（12个）：**
   - 最大权闭合子图案例（2个）：Open Pit Mining, Task Selection
   - 虚树应用变体（3个）：Chain Compression, Edge Weight, Minimum Connection
   - 数据结构模式（2个）：Orthogonal Range Query, Parallel Check Framework
   - 树论算法（1个）：Dynamic Centroid
   - 图论建模（2个）：Steiner Tree, Time Expanded Graph
   - 定理应用（1个）：Dilworth Theorem
   - 全局最小割（1个）：Cut Tree Query

---

## 数据完整性验证

### 统计校验

| 校验项 | 结果 | 说明 |
|--------|------|------|
| P0 数量 | ✅ 14 | 与 triage 一致 |
| P1 数量 | ✅ 20 | 与 triage 一致 |
| 总计 | ✅ 34 | P0 14 + P1 20 = 34 |
| merge_with_batch2_draft | ✅ 15 | P0:6 + P1:9 = 15 |
| create_new_draft_later | ✅ 7 | 全部为 P0 |
| manual_review | ✅ 12 | P0:1 + P1:11 = 12 |
| 总计校验 | ✅ 15+7+12 = 34 | |

### 边界案例检查

| 复杂案例 | 处理方式 | 风险 |
|---------|---------|------|
| 2.21.133 (Layered Graph) | merge_with_batch2_draft | 中等 - 同时与 ready pattern 和 batch2 draft 重叠 |
| 2.21.131 (Project Selection) | merge_with_batch2_draft | 低 - 只是需要考虑合并到 pat.network_flow_closure |
| 2.21.146 (Time Expanded Graph) | manual_review | 中等 - 与 ready pattern 语义接近 |

---

## 后续工作建议

### 近期行动（Batch2 正式生成）

1. **合并 15 个候选到对应的 Batch2 draft**
   - 将知识库中的题面参考、训练数据等对齐到正式模式
   - 处理 2.21.131 与 pat.network_flow_closure 的合并
   - 处理 2.21.133 与 pat.layered_graph_shortest_path 的边界说明

2. **K短路模式的语义重叠处理**
   - 将 pat.k_shortest_modeling 与 pat.k_shortest_paths 合并
   - 知识库候选 2.21.132 提供此模式的来源

### 中期行动（Batch3 规划）

3. **创建 7 个新 draft**
   - 最大权闭合子图子模式（2个）
   - 虚树系列（3个）
   - 离线算法（2个）

### 长期行动（专家审核）

4. **专家组审核 12 个候选**
   - 确认边界、独立性、可行性
   - 审核后可决定进入 Batch3 或放弃

---

## 关键确认

| 问题 | 回答 |
|------|------|
| P0/P1 总数 | ✅ 34 |
| reuse_existing_ready_pattern 数量 | ✅ 0 |
| merge_with_batch2_draft 数量 | ✅ 15 |
| create_new_draft_later 数量 | ✅ 7 |
| manual_review 数量 | ✅ 12 |
| high similarity 冲突列表 | ✅ 2（Layered Graph, Project Selection） |
| 优先进入正式 Batch2 的候选 | ✅ 15 |
| 需要暂缓的候选 | ✅ 19（7 个 Batch3 + 12 个需审核） |
| 是否生成正式 patterns | ❌ 否 |
| 是否修改主图谱 | ❌ 否 |
| 是否修改 patterns_v0_1_ready.json | ❌ 否 |

---

**Report Generated:** 2026-05-22
**Generated By:** GLM5 (Thread 3)
**Task Status:** Completed
**Formal Batch Generated:** false
**Main Graph Modified:** false
**Knowledge Items Modified:** false