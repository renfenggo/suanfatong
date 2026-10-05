# Patterns Batch2 Formal Generation Template

> **重要声明：本文件是正式生成 Patterns Batch2 的模板和操作指南。当前阶段只准备模板，不生成正式 patterns。等待用户明确指令后再生成。**

---

## 1. 生成概览

### 建议生成数量

| 分类 | 数量 | 状态 |
|------|------|------|
| **ready_to_generate_now** | **7** | 直接生成，无前置条件 |
| **needs_boundary_note_attached** | **6** | 携带边界说明后生成 |
| **hold_for_manual_review** | **2** | 暂缓，等待专家审核 |
| **batch3_later_candidates** | **7** | 暂缓，建议 Batch3 处理 |
| **建议正式 Batch2 生成** | **13** | |

### Batch2 候选总览

```
Batch2 正式生成（13个）
├── 第一组：ready_to_generate_now（7个）
│   ├── pat.circulation_optimization（最小费用循环流）
│   ├── pat.cycle_optimization_modeling（最小平均环建模）
│   ├── pat.state_machine_modeling（状态图建模）
│   ├── pat.path_cover_modeling（最小路径覆盖）
│   ├── pat.bounded_matching_modeling（带边界二分图匹配）
│   ├── pat.flow_bounds_transformation（流量边界变换）
│   └── pat.min_flow_modeling（最小流建模）
│
└── 第二组：needs_boundary_note_attached（6个）
    ├── pat.k_shortest_modeling（K短路建模）← 需与 K短路算法区分
    ├── pat.layered_graph_modeling（分层图建模）← 需与分层图最短路区分
    ├── pat.node_demand_modeling（节点需求流建模）← Demands + Node Demand 合并
    ├── pat.max_flow_with_bounds（带边界最大流）← 需与流量边界变换区分
    ├── pat.shortest_path_potentials（Johnson势函数）← 需与最短路建模区分
    └── pat.node_demand_modeling（已合并，同第三个）
```

### 暂缓候选

| 分类 | 数量 | 说明 |
|------|------|------|
| hold_for_manual_review | 2 | Project Selection, Stable Marriage |
| batch3_later_candidates | 7 | 最大权闭合子图×2, 虚树×3, 离线算法×2 |

---

## 2. 生成字段规范

每个正式 pattern 必须包含以下字段。参考已有 ready pattern（如 `pat.two_sum`）的格式。

### 必需字段

```json
{
  "pattern_id": "pat.xxx",
  "name": "中文名称",
  "en_name": "English Name",
  "category": "分类",
  "description": "模式描述（只写建模方法和识别要点，不复制题面）",
  "recognition_signals": [
    "识别信号1（3~5条，可操作、可验证）",
    "识别信号2",
    "识别信号3"
  ],
  "required_items": [
    "2.xx.xx",
    "2.xx.xx"
  ],
  "related_items": [
    "2.xx.xx"
  ],
  "common_transforms": [
    "常见转化方法1（2~4条，具体的建模步骤）",
    "常见转化方法2"
  ],
  "typical_complexities": [
    "时间复杂度分析",
    "空间复杂度分析",
    "适用规模参考"
  ],
  "tracks": ["icpc", "noi"],
  "audience": ["competitive_programming"],
  "difficulty": "intermediate | advanced | expert",
  "visibility": "core | public",
  "example_problem_refs": [],
  "i18n_key": "pattern.xxx",
  "source": "patterns_batch2",
  "review_status": {
    "need_manual_review": true,
    "review_priority": "A | B | C",
    "review_note": ""
  }
}
```

### 字段规则

| 字段 | 规则 |
|------|------|
| pattern_id | 使用 `pat.xxx` 格式，与 draft_preview 中的 draft_pattern_id 一致 |
| name | 中文名称，简洁明确 |
| en_name | 英文名称，使用驼峰或空格分隔 |
| category | 在 [图论建模, 网络流建模, 最短路优化, 匹配算法, 图论算法] 中选择 |
| description | 只写建模方法和识别要点，**不允许复制题面** |
| recognition_signals | **3~5条**，可操作、可验证 |
| common_transforms | **2~4条**，具体的建模步骤 |
| required_items | 全部映射到知识图谱 item id（如 2.16.3） |
| related_items | 可选的关联知识点 |
| typical_complexities | 包含时间和空间复杂度分析 |
| tracks | 在 [icpc, noi, interview, beginner, university_cp] 中选择 |
| difficulty | intermediate / advanced / expert |
| visibility | core / public |
| example_problem_refs | 只保存 problem metadata（来源、题号、ID），**不允许复制题面** |
| source | 统一为 `patterns_batch2` |
| boundary_note | **仅对 needs_boundary_note_attached 候选**：添加边界说明字段 |

### 限制

1. **不允许复制题面**：只能保存 problem metadata（来源、题号、ID）
2. **不允许生成训练题**：只保存模式描述和识别方法
3. **不允许写成长篇讲义**：保持简洁，聚焦于建模方法和识别信号
4. **required_items / related_items 必须全部映射到知识图谱 item id**

---

## 3. 分类生成说明

### 3.1 ready_to_generate_now（7个）

直接生成，无前置条件。将 Batch2 Draft Preview 内容按正式格式封装即可。

#### 候选清单

| 序号 | item_id | 知识库名称 | target_pattern_id | 源 draft |
|------|---------|-----------|-------------------|----------|
| 1 | 2.21.128 | Min Cost Circulation | pat.circulation_optimization | patterns_batch2_p0_draft_preview.json |
| 2 | 2.21.134 | Minimum Mean Cycle | pat.cycle_optimization_modeling | patterns_batch2_p1_draft_preview.json |
| 3 | 2.21.136 | State Graph | pat.state_machine_modeling | patterns_batch2_p1_draft_preview.json |
| 4 | 2.21.142 | Minimum Path Cover | pat.path_cover_modeling | patterns_batch2_p1_draft_preview.json |
| 5 | 2.21.124 | Bounded Bipartite Matching | pat.bounded_matching_modeling | patterns_batch2_p1_draft_preview.json |
| 6 | 2.21.126 | Edge Lower Bound Transform | pat.flow_bounds_transformation | patterns_batch2_p1_draft_preview.json |
| 7 | 2.21.129 | Minimum Flow | pat.min_flow_modeling | patterns_batch2_p1_draft_preview.json |

#### 生成步骤

1. 从对应 draft_preview 中提取 draft 内容
2. 按正式字段规范重新封装
3. 设置 `source` 为 `patterns_batch2`
4. 设置 `review_status.need_manual_review` 为 `true`（新生成模式需要审核）
5. 设置 `review_status.review_priority` 为 `A`
6. 合并知识库候选中的题面参考和训练数据到 `example_problem_refs`

---

### 3.2 needs_boundary_note_attached（6个）

携带边界说明后生成。每个候选必须包含 `boundary_note` 字段。

#### 候选清单

| 序号 | item_id | 知识库名称 | target_pattern_id | 边界说明来源 |
|------|---------|-----------|-------------------|-------------|
| 1 | 2.21.132 | K Shortest Paths | pat.k_shortest_modeling | boundary_notes.json |
| 2 | 2.21.133 | Layered Graph | pat.layered_graph_modeling | boundary_notes.json |
| 3 | 2.21.125 | Demands | pat.node_demand_modeling | boundary_notes.json |
| 4 | 2.21.130 | Node Demand | pat.node_demand_modeling | boundary_notes.json |
| 5 | 2.21.127 | Maximum Flow | pat.max_flow_with_bounds | boundary_notes.json |
| 6 | 2.21.135 | Shortest Path Potentials | pat.shortest_path_potentials | boundary_notes.json |

#### 边界说明格式

在每个模式中添加 `boundary_note` 字段：

```json
{
  "boundary_note": {
    "related_patterns": [
      {
        "pattern_id": "pat.xxx",
        "relationship": "general_vs_specific | sibling | application_of | merge_candidate",
        "note": "与 pat.xxx 的边界说明"
      }
    ],
    "usage_guide": "在什么场景下使用此模式，什么场景下使用关联模式"
  }
}
```

#### 各候选边界说明 Check

- [ ] **pat.k_shortest_modeling**：添加与 pat.k_shortest_paths 的边界说明，区建模层和算法层
- [ ] **pat.layered_graph_modeling**：添加与 pat.layered_graph_shortest_path 的边界说明，通用vs特例
- [ ] **pat.node_demand_modeling**：合并 Demands + Node Demand，涵盖两种场景
- [ ] **pat.max_flow_with_bounds**：添加与 pat.flow_bounds_transformation 的边界说明
- [ ] **pat.shortest_path_potentials**：添加与 pat.shortest_path_modeling 的边界说明

---

### 3.3 hold_for_manual_review（2个）

暂缓，等待专家审核。

| 序号 | item_id | 名称 | target_pattern_id | 审核要点 |
|------|---------|------|-------------------|---------|
| 1 | 2.21.131 | Project Selection | pat.network_flow_project_selection | 是否合并到 pat.network_flow_closure |
| 2 | 2.21.143 | Stable Marriage | pat.stable_matching_pattern | 是否保留为独立 pattern |

**审核问题来源**：`stage3e_patterns_batch2_boundary_notes.json` 中的 `manual_reviews` 部分。

---

### 3.4 batch3_later_candidates（7个）

暂缓，建议 Batch3 处理。

| 序号 | item_id | 名称 | 建议 pattern_id |
|------|---------|------|----------------|
| 1 | 2.21.70 | Binary Decision Model | pat.max_closure_decision_model |
| 2 | 2.21.74 | Prerequisite Graph | pat.max_closure_prerequisite |
| 3 | 2.21.119 | Distance Compression | pat.virtual_tree_distance_compression |
| 4 | 2.21.122 | Multi-Key Query | pat.virtual_tree_multi_key_query |
| 5 | 2.21.123 | Subtree Aggregation | pat.virtual_tree_subtree_aggregation |
| 6 | 3.13.106 | Time Divide Conquer | pat.offline_time_divide_conquer |
| 7 | 3.13.109 | Rollback Vs Persistence | pat.rollback_vs_persistence_decision |

---

## 4. 重点边界说明

### 4.1 K短路建模 vs K短路算法

**pat.k_shortest_modeling（K短路建模）**：
- 侧重问题识别：如何判断题目需要求解 K 最短路径
- 侧重建模方法：将多路径优化问题转化为最短路扩展问题
- 侧重适用场景：多条路径备选方案
- 不聚焦于单一算法实现

**pat.k_shortest_paths（Yen K短路）**：
- 侧重算法实现：Yen 算法的具体步骤和复杂度
- 侧重路径扩展：基于最短路树的候选路径生成
- 侧重优化技巧：路径排序和剪枝

**生成建议**：建议合并为一个模式，涵盖建模和算法两个层次。如果分开保留，需在 `boundary_note` 中明确区分。

### 4.2 分层图建模 vs 分层图最短路

**pat.layered_graph_modeling（分层图建模）**：
- 通用建模模式，可应用于最短路、最大流、DP 等多种问题
- 强调分层图的构建方法和通用转化技巧
- 识别信号：时间阶段、层级顺序、状态演变

**pat.layered_graph_shortest_path（分层图最短路）**：
- 专门问题模式，只针对分层图上的最短路径问题
- 是分层图建模的一个具体应用特例
- 强调分层图上的最短路求解

**生成建议**：保留两个模式，在 `boundary_note` 中说明通用与特例的关系。

### 4.3 Demands + Node Demand 合并

- 2.21.125 Demands 和 2.21.130 Node Demand 本质相同
- 都是处理节点有流量需求/供应的网络流建模
- 建议合并到 `pat.node_demand_modeling`
- 合并后涵盖两种场景：节点需求（节点有供应/需求）和流量需求（节点级别的流量约束）

### 4.4 带边界最大流 vs 流量边界变换

**pat.max_flow_with_bounds（带边界最大流）**：
- 专门求解带上下界的最大流问题
- 是流量边界变换的一个具体应用

**pat.flow_bounds_transformation（流量边界变换）**：
- 通用的边界变换方法
- 可应用于最大流、最小流、费用流等多种问题

**生成建议**：保留为两个独立模式，在 `boundary_note` 中说明具体应用与通用方法的关系。

### 4.5 Johnson势函数 vs 最短路建模

**pat.shortest_path_potentials（Johnson势函数）**：
- 专门针对全节点对最短路问题
- 专门处理负权边的势函数变换方法
- 两阶段算法：Bellman-Ford → Dijkstra

**pat.shortest_path_modeling（最短路建模）**：
- 针对一般最短路问题
- 通用的图到最短路问题的转化方法

**生成建议**：保留为独立模式，在 `boundary_note` 中提供适用场景对比表。

---

## 5. 质量检查清单

### 5.1 每个 pattern 的检查项

- [ ] pattern_id 命名规范（pat.xxx）
- [ ] 所有必需字段完整
- [ ] recognition_signals 3~5条
- [ ] common_transforms 2~4条
- [ ] typical_complexities 包含时间/空间/规模
- [ ] required_items 全部映射到知识图谱 item id
- [ ] related_items 可选但建议填写
- [ ] 不包含题面内容
- [ ] 不包含训练题
- [ ] 不是长篇讲义
- [ ] source 设置为 patterns_batch2
- [ ] review_status 设置正确

### 5.2 跨 pattern 的检查项

- [ ] 与 83 个 ready patterns 不重复
- [ ] 6 个 needs_boundary_note 候选已添加 boundary_note
- [ ] 3 个 high duplicate risk 候选已处理（K Shortest, Layered Graph, Project Selection）
- [ ] Demands + Node Demand 已合并

### 5.3 文件完整性检查

- [ ] 正式 patterns_batch2.json 包含 13 个 pattern
- [ ] 正式 patterns_batch2.json 的格式与 patterns_v0_1_ready.json 一致
- [ ] 元数据正确（generated_by, generated_at 等）

---

## 6. 生成执行确认

### 执行前确认

- [ ] 用户已发出明确指令："生成正式 patterns_batch2.json"
- [ ] 专家审核已完成（如需待审核的候选）
- [ ] hold_for_manual_review 候选的决策已确定

### 执行后确认

- [ ] patterns_batch2.json 已生成（在 data/ 目录下）
- [ ] patterns_v0_1_ready.json 未修改（只增加新文件）
- [ ] 主图谱未修改
- [ ] knowledge_items 未修改
- [ ] 边界说明已正确附加

---

## 7. 模板参考：已有 pattern 结构

参考 `patterns_v0_1_ready.json` 中已有 pattern 的结构：

```json
{
  "pattern_id": "pat.xxx",
  "name": "模式中文名",
  "en_name": "Pattern English Name",
  "category": "Category Name",
  "description": "模式描述",
  "recognition_signals": ["信号1", "信号2", ...],
  "required_items": ["x.x.x", "x.x.x"],
  "related_items": ["x.x.x"],
  "common_transforms": ["转化1", "转化2", ...],
  "typical_complexities": ["复杂度1", "复杂度2", ...],
  "tracks": ["icpc", "noi"],
  "audience": ["competitive_programming"],
  "difficulty": "intermediate",
  "visibility": "core",
  "example_problem_refs": [],
  "i18n_key": "pattern.xxx",
  "source": "patterns_batch2",
  "review_status": {
    "need_manual_review": true,
    "review_priority": "A",
    "review_note": ""
  }
}
```

---

**Template Status:** Ready (awaiting user instruction)
**Formal Patterns Generated:** false
**Main Graph Modified:** false
**Generated At:** 2026-05-22