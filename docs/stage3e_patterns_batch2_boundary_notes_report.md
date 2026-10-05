# Stage3E Patterns Batch2 Boundary Notes Report

## Executive Summary

基于 Stage3E Patterns Batch2 Merge Readiness 结果，为 6 个 needs_boundary_note 候选写边界说明，为 2 个 manual_review 候选写审核问题清单。本阶段只写边界说明和审核问题，不生成正式 patterns。

**重要声明：只写边界说明和审核问题，不生成正式 patterns。**

---

## 处理概览

### 处理分布

| 类型 | 数量 | 说明 |
|------|------|------|
| **boundary_note 候选** | 6 | 已写边界说明 |
| **manual_review 候选** | 2 | 已写审核问题清单 |
| **总计** | **8** | |

### Duplicate Risk 分布

| 风险级别 | 数量 | 候选 |
|---------|------|------|
| high | 2 | 2.21.132 (K Shortest), 2.21.133 (Layered Graph) |
| medium | 4 | 2.21.125, 2.21.130, 2.21.127, 2.21.135 |

### 推荐合并行为

| 行为 | 数量 | 候选 |
|------|------|------|
| merge_with_boundary_note | 3 | 2.21.132, 2.21.133, 2.21.135 |
| merge_together | 2 | 2.21.125 + 2.21.130 |
| keep_separate_with_note | 1 | 2.21.127 |

---

## 边界说明详情（6个）

### 1. K Shortest Paths — K短路建模 vs K短路算法

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.132 图论建模：K Shortest Paths |
| **Batch2 Draft** | pat.k_shortest_modeling |
| **冲突对象** | pat.k_shortest_paths（另一 Batch2 Draft） |
| **重复风险** | 🔴 high |
| **推荐行为** | merge_with_boundary_note |

**边界说明摘要：**

两个模式在本质上处理的是同一种问题类型（K 最短路径），但侧重点不同：

- **pat.k_shortest_modeling（K短路建模）**：侧重问题识别和建模方法
- **pat.k_shortest_paths（Yen K短路）**：侧重算法实现细节

**建议在正式 Batch2 中合并为一个统一模式**，以 pat.k_shortest_modeling 为正式名称，在模式内容中分为建模层和算法层两个层次。

### 2. Layered Graph — 分层图建模 vs 分层图最短路

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.133 图论建模：Layered Graph |
| **Batch2 Draft** | pat.layered_graph_modeling |
| **冲突对象** | pat.layered_graph_shortest_path（ready pattern） |
| **重复风险** | 🔴 high |
| **推荐行为** | merge_with_boundary_note |

**边界说明摘要：**

两个模式是通用与特例的关系：

- **pat.layered_graph_modeling（分层图建模）**：通用建模模式，可应用于最短路、最大流等多种问题
- **pat.layered_graph_shortest_path（分层图最短路）**：专门问题模式，只针对分层图上的最短路

**建议保留两个模式**，在 pat.layered_graph_modeling 中说明其通用性，在 pat.layered_graph_shortest_path 中说明其是分层图建模的一个具体应用。

### 3 & 4. Demands + Node Demand — 合并处理

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.125 Demands + 2.21.130 Node Demand |
| **Batch2 Draft** | pat.node_demand_modeling |
| **重复风险** | 🟡 medium |
| **推荐行为** | merge_together（合并处理） |

**边界说明摘要：**

两个知识库候选本质相同，都是描述节点有流量需求/供应的网络流建模：

- Demands 强调流量需求场景
- Node Demand 强调节点约束场景

**建议合并为一个统一模式** pat.node_demand_modeling，涵盖两种场景。

### 5. Maximum Flow — 带边界最大流 vs 流量边界变换

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.127 上下界网络流：Maximum Flow |
| **Batch2 Draft** | pat.max_flow_with_bounds |
| **冲突对象** | pat.flow_bounds_transformation（另一 Batch2 Draft） |
| **重复风险** | 🟡 medium |
| **推荐行为** | keep_separate_with_note |

**边界说明摘要：**

两个模式是通用方法与具体应用的关系：

- **pat.max_flow_with_bounds**：专门求解带上下界的最大流问题
- **pat.flow_bounds_transformation**：通用的边界变换方法，可应用于多种问题

**建议保留为两个独立模式**并说明边界：求解带上下界的最大流时使用 pat.max_flow_with_bounds，需要通用的边界变换方法时使用 pat.flow_bounds_transformation。

### 6. Shortest Path Potentials — Johnson势函数 vs 最短路建模

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.135 图论建模：Shortest Path Potentials |
| **Batch2 Draft** | pat.shortest_path_potentials |
| **冲突对象** | pat.shortest_path_modeling（ready pattern） |
| **重复风险** | 🟡 medium |
| **推荐行为** | merge_with_boundary_note |

**边界说明摘要：**

两个模式是通用与专门的关系：

- **pat.shortest_path_potentials（Johnson势函数）**：专门针对全节点对最短路和负权边处理
- **pat.shortest_path_modeling（最短路建模）**：针对一般最短路问题

**建议保留为独立模式**，提供适用场景对比表帮助用户选择。

---

## 审核问题清单详情（2个）

### 1. Project Selection — 项目选择建模

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.131 上下界网络流：Project Selection |
| **Batch2 Draft** | pat.network_flow_project_selection |
| **冲突对象** | pat.network_flow_closure（Batch2 Draft，边界审查建议合并） |
| **推荐默认决策** | merge_into_network_flow_closure |

**审核问题清单：**

| 序号 | 问题 | 关键点 |
|------|------|--------|
| 1 | 项目选择建模与最大权闭合子图在本质上是否相同？ | 边界审查认为相同 |
| 2 | 如果合并，项目选择建模的独特价值是什么？ | 可作为最大权闭合子图的应用示例 |
| 3 | 保留独立模式的理由是否充分？ | 名称更直观，但增加模式数量 |
| 4 | 实际竞赛中，"项目选择"问题是否足够常见？ | 如果频率低，不需要独立模式 |
| 5 | 如果保留，如何与最大权闭合子图区分边界？ | 需要在描述中明确说明 |

**推荐：** 合并到 pat.network_flow_closure（方案 A）

### 2. Stable Marriage — 稳定婚姻问题

| 项目 | 内容 |
|------|------|
| **知识库候选** | 2.21.143 匹配与覆盖：Stable Marriage |
| **Batch2 Draft** | pat.stable_matching_pattern |
| **冲突对象** | 无直接冲突，但需要评估模式合理性 |
| **推荐默认决策** | keep_as_pattern |

**审核问题清单：**

| 序号 | 问题 | 关键点 |
|------|------|--------|
| 1 | 稳定婚姻在竞赛中出现频率如何？ | 频率较低但内容经典 |
| 2 | 与二分图匹配建模的边界在哪里？ | 特殊匹配约束 vs 一般匹配 |
| 3 | 识别信号是否足够清晰和独特？ | 偏好排序、稳定性约束独特 |
| 4 | 是否更适合作为知识点而非 pattern？ | 算法经典，但变体有限 |
| 5 | 与 Batch2 Draft 的关系如何处理？ | 如果确认需要，直接合并 |

**推荐：** 保留为独立模式（方案 A）

---

## 进入正式 Batch2 建议

### 可以直接进入的候选（6个）

这些候选已有明确的边界说明，只需在正式生成时添加相应边界说明即可：

| 序号 | item_id | 名称 | 需要添加的边界说明 |
|------|---------|------|------------------|
| 1 | **2.21.132** | K Shortest Paths | 说明与 pat.k_shortest_paths 的边界，建议合并 |
| 2 | **2.21.133** | Layered Graph | 说明与 pat.layered_graph_shortest_path 的边界 |
| 3 | **2.21.125** | Demands | 说明与 2.21.130 合并处理 |
| 4 | **2.21.130** | Node Demand | 说明与 2.21.125 合并处理 |
| 5 | **2.21.127** | Maximum Flow | 说明与 pat.flow_bounds_transformation 的边界 |
| 6 | **2.21.135** | Shortest Path Potentials | 说明与 pat.shortest_path_modeling 的边界 |

### 仍需暂缓的候选（2个）

| 序号 | item_id | 名称 | 原因 |
|------|---------|------|------|
| 1 | **2.21.131** | Project Selection | 专家审核后才能决定合并方案 |
| 2 | **2.21.143** | Stable Marriage | 专家审核后才能决定是否保留为模式 |

---

## 边界说明格式参考

以下是在正式模式中添加边界说明的参考格式：

### 模式描述中的边界说明

```markdown
## 边界说明

本模式与 [其他模式名称] 的区别：

- **本模式**：[描述本模式的独特定位]
- **[其他模式]**：[描述其他模式的定位]
- **使用建议**：[指导用户在两者之间选择]
```

### 模式之间的交叉引用

```markdown
## 关联模式

- [pat.xxx] — [简要说明关系]
- [pat.yyy] — [简要说明关系]
```

---

## 数据完整性验证

### 统计校验

| 校验项 | 结果 | 说明 |
|--------|------|------|
| boundary_note 候选数量 | ✅ 6 | 与 merge_readiness 一致 |
| manual_review 候选数量 | ✅ 2 | 与任务要求一致 |
| 总计 | ✅ 8 | 6 + 2 = 8 |
| high duplicate risk | ✅ 2 | K Shortest, Layered Graph |
| 可以进入正式 Batch2 | ✅ 6 | 6 个 boundary_note 候选 |
| 仍需暂缓 | ✅ 2 | 2 个 manual_review 候选 |

### 文件完整性

| 文件 | 状态 |
|------|------|
| data/stage3e_patterns_batch2_boundary_notes.json | ✅ 已生成 |
| docs/stage3e_patterns_batch2_boundary_notes_report.md | ✅ 已生成 |
| patterns_batch2_p0_draft_preview.json | ✅ 未修改 |
| patterns_batch2_p1_draft_preview.json | ✅ 未修改 |
| patterns_v0_1_ready.json | ✅ 未修改 |
| merged_knowledge_graph_item_dependencies_refined.json | ✅ 未修改 |

---

## 结论

### 关键确认

| 问题 | 回答 |
|------|------|
| boundary_note 候选数量 | ✅ 6 |
| manual_review 候选数量 | ✅ 2 |
| high duplicate risk 候选 | ✅ 2（K Shortest, Layered Graph） |
| 可以进入正式 Batch2 的候选 | ✅ 6（全部 boundary_note 候选） |
| 仍需暂缓的候选 | ✅ 2（Project Selection, Stable Marriage） |
| 是否生成正式 patterns | ❌ 否 |
| 是否修改主图谱 | ❌ 否 |
| 是否修改 patterns_v0_1_ready.json | ❌ 否 |

### 最终状态

```
8 个待处理候选
├── 6 个 boundary_note（已写完边界说明，可进入 Batch2）
│   ├── 2.21.132 K Shortest → merge_with_boundary_note
│   ├── 2.21.133 Layered Graph → merge_with_boundary_note
│   ├── 2.21.125 Demands → merge_together（与 2.21.130）
│   ├── 2.21.130 Node Demand → merge_together（与 2.21.125）
│   ├── 2.21.127 Maximum Flow → keep_separate_with_note
│   └── 2.21.135 Shortest Path Potentials → merge_with_boundary_note
└── 2 个 manual_review（已写完审核问题清单，需专家决策）
    ├── 2.21.131 Project Selection → 推荐合并到 network_flow_closure
    └── 2.21.143 Stable Marriage → 推荐保留为独立模式
```

### 下一步建议

1. **正式生成 Batch2**：将 6 个 boundary_note 候选连同 7 个 ready 候选一起进入正式 Batch2 生成
2. **专家审核**：对 2 个 manual_review 候选进行专家评审
3. **决策执行**：根据专家决策结果，决定是合并还是保留

---

**Report Generated:** 2026-05-22
**Generated By:** GLM5 (Thread 3)
**Task Status:** Completed
**Formal Batch Generated:** false
**Main Graph Modified:** false