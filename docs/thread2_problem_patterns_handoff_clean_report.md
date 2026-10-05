# 2号线程 Problem Patterns Handoff 清洗报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T13:00:00.000Z
- 任务类型: problem_patterns handoff 清洗
- 主图谱状态: 未修改
- 输出对象: 3号线程

## 统计数据

### 总体统计

- 原始 handoff 数量: 36
- 清洗后数量: 34
- 去重数量: 0
- 已有 pattern 重复数量: 0
- 被排除数量: 2

### 优先级分布

- P0 数量: 7
- P1 数量: 18
- P2 数量: 9

### 分类统计

- 图论建模: 13
- 网络流建模: 8
- 最短路优化: 5
- 匹配算法: 1
- 高级匹配: 2
- 图论算法: 3
- 动态算法: 0
- 离线算法: 1
- 数据结构应用: 1

## 清洗规则应用

### 1. 重复去除
- 检查了重复的 candidate_id
- 去除了 0 个重复候选

### 2. 已有模式检查
- 与 patterns_v0_1_ready.json 中的 pattern_id 进行了比对
- 发现 0 个重复
- 重复候选仍在 clean handoff 中，但已在 reason 中标记

### 3. 知识点排除
- 根据关键词识别了更像知识点而非问题模式的候选
- 排除了 2 个候选
- 排除关键词: 算法、数据结构、技巧、方法、实现、概述等

## 排除候选列表

以下候选被排除因为它们更像知识点而非问题模式：


### 2-SAT 建模技巧 (cand.graph.two_sat.modeling_techniques)
- 英文名: 2-SAT Modeling Techniques
- 排除原因: 更像知识点而非问题模式
- 原始分类: 图论建模
- 原始 pattern_id: graph_modeling_2sat

### 动态图连通性：Fully Dynamic Overview (cand.graph.dynamic_connectivity.fully_dynamic_overview)
- 英文名: Dynamic Connectivity: Fully Dynamic Overview
- 排除原因: 更像知识点而非问题模式
- 原始分类: 动态算法
- 原始 pattern_id: dynamic_graph_algorithms

## Clean Handoff 概览

清洗后的 handoff 候选按照分类分布：


### 图论建模 (13 个)
- Hall 定理及应用 (pattern_matching_hall) [优先级: P2]
- 差分约束系统建模 (graph_modeling_diff_constraints) [优先级: P2]
- 图论建模：2 Sat Modeling (graph_modeling_2sat_detailed) [优先级: P2]
- 匹配与覆盖：Hall Theorem (matching_hall_theorem) [优先级: P2]
- 图论建模：Layered Graph (layered_graph_modeling) [优先级: P1]
- 匹配与覆盖：Dilworth Theorem (partial_order_matching) [优先级: P1]
- 图论建模：State Graph (state_machine_modeling) [优先级: P2]
- 匹配与覆盖：Minimum Path Cover (path_cover_modeling) [优先级: P1]
- 图论建模：Shortest Path Potentials (potential_method_modeling) [优先级: P1]
- 图论建模：K Shortest Paths (k_shortest_modeling) [优先级: P1]
- 图论建模：Minimum Mean Cycle (cycle_optimization_modeling) [优先级: P1]
- 匹配与覆盖：Konig Theorem (konig_theorem_pattern) [优先级: P2]
- 图论建模：Steiner Tree (steiner_tree_modeling) [优先级: P0]

### 网络流建模 (8 个)
- 最大权闭合子图 (network_flow_closure) [优先级: P1]
- 上下界网络流：Project Selection (network_flow_project_selection) [优先级: P1]
- 上下界网络流：Minimum Flow (min_flow_modeling) [优先级: P1]
- 上下界网络流：Edge Lower Bound Transform (flow_bounds_transformation) [优先级: P1]
- 上下界网络流：Maximum Flow (max_flow_with_bounds) [优先级: P1]
- 上下界网络流：Min Cost Circulation (circulation_optimization) [优先级: P0]
- 上下界网络流：Node Demand (node_demand_modeling) [优先级: P1]
- 上下界网络流：Bounded Bipartite Matching (bounded_matching_modeling) [优先级: P1]

### 最短路优化 (5 个)
- 高级最短路：Johnson Potentials (shortest_path_potentials) [优先级: P1]
- 高级最短路：Yen K Shortest (k_shortest_paths) [优先级: P1]
- 高级最短路：Eppstein K Shortest (k_shortest_advanced) [优先级: P0]
- 高级最短路：Replacement Paths (shortest_path_robustness) [优先级: P0]
- 高级最短路：Resource Constrained (constrained_shortest_path) [优先级: P0]

### 匹配算法 (1 个)
- 匹配与覆盖：Stable Marriage (stable_matching_pattern) [优先级: P2]

### 高级匹配 (2 个)
- 匹配与覆盖：Matroid Matching (matroid_matching_pattern) [优先级: P0]
- 匹配与覆盖：Tutte Matrix (matching_complexity_pattern) [优先级: P0]

### 图论算法 (3 个)
- 强连通分量 DAG：Dag Reachability (dag_reachability) [优先级: P2]
- 强连通分量 DAG：Dominating Components (scc_applications) [优先级: P1]
- 强连通分量 DAG：Minimum Edges To Strong (dag_to_strongly_connected) [优先级: P2]

### 离线算法 (1 个)
- 动态图连通性：Divide And Conquer On Time (offline_divide_conquer) [优先级: P1]

### 数据结构应用 (1 个)
- 动态图连通性：Edge Interval Model (interval_data_structure) [优先级: P1]


## 优先级说明

- **P0**: expert 级别，最高优先级
- **P1**: advanced 级别，高优先级
- **P2**: intermediate 级别，普通优先级

## 重要提醒

1. **主图谱未修改**: 本次清洗过程严格遵守不修改主图谱的限制
2. **已有模式**: 标记了与 patterns_v0_1_ready.json 中 pattern_id 重复的候选
3. **知识点排除**: 排除了更像知识点而非问题模式的候选
4. **不要生成新 pattern 正文**: 本次只整理清单，不生成 pattern 内容
5. **不要修改 patterns_v0_1_ready.json**: 清洗过程没有修改现有 patterns 文件

## 输出文件

1. `data/thread2_problem_patterns_handoff_clean.json` - 清洗后的 handoff 清单
2. `docs/thread2_problem_patterns_handoff_clean_report.md` - 本报告

## 3号线程使用建议

1. 优先处理 P0 级别的候选
2. 注意检查与已有 pattern_id 重复的候选
3. 对于被排除的候选，如果确认为问题模式，可重新考虑
4. 按照 pattern_category 分类处理，保持结构化

---

报告生成时间: 2026-05-22T13:00:00.000Z
生成者: 2号线程
主图谱修改状态: 否
