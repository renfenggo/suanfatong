# Patterns Batch2 Manual Review Decision Memo

## Expert Decision Memo for 2 Manual Review Candidates

> **重要声明：本文件是专家决策备忘录，为 2 个 manual_review 候选项提供详细的决策分析和推荐。当前阶段只做决策备忘录，不生成正式 patterns。等待用户确认决策后执行。**

---

## Executive Summary

| 候选 | item_id | 推荐决策 | 是否进入 Batch2 |
|------|---------|---------|:------------:|
| **Project Selection** | 2.21.131 | 合并到 ready pattern `pat.project_selection_closure` | ❌（Batch2 Draft 关闭） |
| **Stable Marriage** | 2.21.143 | 保留为独立模式 `pat.stable_matching_pattern` | ✅ 进入 Batch2 |

---

## 候选一：Project Selection（2.21.131）

### 基本信息

| 字段 | 内容 |
|------|------|
| item_id | 2.21.131 |
| 名称 | 上下界网络流：Project Selection |
| 候选 pattern_id | pat.network_flow_project_selection |
| Batch2 Draft | pat.network_flow_project_selection（项目选择建模） |
| 已有 ready pattern | **pat.project_selection_closure**（最大权闭合子图） |
| 边界审查结论 | 建议合并到 pat.network_flow_closure |
| duplicate_risk | high |

### 关键发现：ready pattern 已存在

边界审查后发现的**重要事实**：

```
patterns_v0_1_ready.json 中已存在：
  pattern_id: "pat.project_selection_closure"
  name: "最大权闭合子图"
  category: "Graph Modeling Patterns"
  recognition_signals: ["选择项目会强制选择依赖项", "收益可正可负", "求最大总收益"]
  required_items: ["2.21.29", "2.16.3"]
  example_problem_refs: ["Project Selection"]
  source: "patterns_batch1_thread3"
```

这意味着：
1. **最大权闭合子图模式已就绪**，且已引用 Project Selection 作为示例
2. 创建独立的 `pat.network_flow_project_selection` 将与已有模式**严重重叠**
3. Project Selection 本质上就是最大权闭合子图的**直接应用**

### 决策选项分析

#### 选项 A（推荐）：合并到 pat.project_selection_closure

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ✅ 不增加，保持现有 83 个 |
| 语义一致性 | ✅ 本质相同，合并消除重叠 |
| 用户识别 | ⚠️ 需要教育用户"最大权闭合子图"概念 |
| 维护成本 | ✅ 最低，无需新建模式 |
| 与边界审查一致性 | ✅ 完全一致 |

**具体操作**：
1. 将 2.21.131 知识库候选的内容和题面参考补充到 `pat.project_selection_closure` 的 `description` 和 `example_problem_refs`
2. 关闭 `pat.network_flow_project_selection` 对应的 Batch2 Draft
3. 在 Batch2 正式生成时跳过此候选

#### 选项 B：保留为独立模式

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ❌ 增加 1 个，且与已有模式重叠 |
| 语义一致性 | ❌ 两个模式本质相同，用户困惑 |
| 用户识别 | ✅ "Project Selection" 名称直观 |
| 维护成本 | ❌ 最高，需要维护两个相似模式 |
| 与边界审查一致性 | ❌ 推翻边界审查结论 |

**潜在问题**：用户会问"项目选择模式"和"最大权闭合子图模式"有什么区别？答案将是"没有本质区别"，这将导致模式体系信誉受损。

#### 选项 C：合并到 pat.min_cut_selection

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ✅ 不增加 |
| 语义一致性 | ⚠️ 项目选择与最小割选择有关，但与闭合子图更贴切 |
| 覆盖范围 | ❌ pat.min_cut_selection 不专门处理闭包子图结构 |

### 推荐决策

```
▸ 推荐：合并到 pat.project_selection_closure
▸ 理由：
  1. ready pattern 已存在且功能完整
  2. 项目选择在本质上就是最大权闭合子图的直接应用
  3. 创建独立模式会导致两个几乎相同的模式共存
  4. 合并后 Batch2 正式生成数从 13 调整为 12
▸ 是否需要用户确认：是
```

### 执行后 Batch2 调整

```
Project Selection 移除后，Batch2 正式生成调整为：
  ready_to_generate_now: 7（不变）
  needs_boundary_note_attached: 5（移除 Project Selection 的 draft）
  hold_for_manual_review: 1（仅保留 Stable Marriage）
  Batch2 建议生成总数: 12（原 13 - 1）
```

---

## 候选二：Stable Marriage（2.21.143）

### 基本信息

| 字段 | 内容 |
|------|------|
| item_id | 2.21.143 |
| 名称 | 匹配与覆盖：Stable Marriage |
| 候选 pattern_id | pat.stable_matching_pattern |
| Batch2 Draft | pat.stable_matching_pattern（稳定婚姻问题） |
| 已有 ready pattern | 无直接匹配（pat.bipartite_matching_modeling 语义不同） |
| 边界审查结论 | 无重复风险 |
| duplicate_risk | none |

### 关键比较：稳定婚姻 vs 二分图匹配

| 维度 | Stable Marriage | Bipartite Matching |
|------|----------------|-------------------|
| **匹配性质** | 强稳定性约束 | 容量约束（1对1或多对多） |
| **核心算法** | Gale-Shapley（延迟接受） | Hopcroft-Karp / 匈牙利算法 |
| **输入特征** | 偏好排序列表 | 二分图邻接关系 |
| **输出目标** | 稳定匹配（无阻塞对） | 最大匹配 / 完美匹配 |
| **约束类型** | 偏好顺序约束 | 容量/边约束 |
| **典型变体** | 不稳定对、最优策略 | 最小点覆盖、最大独立集 |

**结论：两个模式的边界清晰，无语义重叠。**

### 决策选项分析

#### 选项 A（推荐）：保留为独立模式

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ⚠️ 增加 1 个（当前 83 → 84） |
| 算法独特性 | ✅ Gale-Shapley 是独特算法，与一般匹配完全不同 |
| 识别信号 | ✅ 偏好排序 + 稳定性约束 + 一对一配对 |
| 竞赛频率 | ⚠️ 中等偏低，但作为体系补充有价值 |
| 维护价值 | ✅ 经典算法模式，教材和训练中常见 |

**边界说明**：需在模式中说明与 `pat.bipartite_matching_modeling` 的边界：
> 稳定婚姻是偏好排序下的强稳定性约束特殊匹配，适用 Gale-Shapley 算法；二分图匹配是容量约束的通用匹配，适用匈牙利算法或网络流。

#### 选项 B：移动到知识库

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ✅ 不增加 |
| 内容保留 | ✅ 算法内容保留在知识库 |
| pattern 训练 | ❌ 用户无法通过 pattern 识别稳定婚姻问题 |
| 体系完整性 | ❌ 匹配算法体系缺少一环 |

#### 选项 C：合并到二分图匹配建模

| 考量 | 说明 |
|------|------|
| 模式数量影响 | ✅ 不增加 |
| 语义匹配度 | ❌ 两种匹配的性质差异大，强行合并不自然 |
| 用户混淆 | ❌ 用户可能将偏好匹配和容量匹配混淆 |

### 推荐决策

```
▸ 推荐：保留为独立模式 pat.stable_matching_pattern
▸ 理由：
  1. Gale-Shapley 算法与一般二分图匹配在方法上完全不同
  2. 识别信号（偏好排序、稳定性约束）独特清晰
  3. 经典算法模式在体系完整性上有重要价值
  4. 与 pat.bipartite_matching_modeling 边界清晰
  5. 合并到知识库或二分图匹配都会丢失模式价值
▸ 附加条件：需在模式中添加与二分图匹配建模的边界说明
▸ 是否需要用户确认：是
```

### 边界说明模板

```json
{
  "boundary_note": {
    "related_patterns": [
      {
        "pattern_id": "pat.bipartite_matching_modeling",
        "relationship": "sibling",
        "note": "稳定婚姻是偏好排序下的强稳定性约束匹配，适用 Gale-Shapley 算法；二分图匹配是容量约束的通用匹配，适用匈牙利算法或网络流。两者的识别信号、输入格式和输出目标均不同。"
      }
    ],
    "usage_guide": "当题面明确给出偏好排序、要求稳定配对时使用此模式；当题面关注匹配数量最大化时使用 pat.bipartite_matching_modeling"
  }
}
```

---

## 综合决策对 Batch2 的影响

### 决策前

| 分类 | 数量 | 说明 |
|------|:----:|------|
| ready_to_generate_now | 7 | 不变 |
| needs_boundary_note_attached | 6 | 包括 Project Selection |
| hold_for_manual_review | 2 | Project Selection + Stable Marriage |
| **建议 Batch2 生成** | **13** | |

### 决策后

| 分类 | 数量 | 变更 |
|------|:----:|------|
| ready_to_generate_now | 7 | 不变 |
| needs_boundary_note_attached | 5 | **-1**（Project Selection 转入 merge_to_ready） |
| hold_for_manual_review | 1 | **-1**（Stable Marriage 决定保留） |
| ready→补充 | 1 | **+1**（2.21.131 内容合并到 pat.project_selection_closure） |
| **建议 Batch2 生成** | **12** | **-1**（原 13 → 12） |

### 更新后的 Batch2 正式生成清单（12个）

```
Batch2 正式生成（12个）
├── ready_to_generate_now（7个）
│   ├── pat.circulation_optimization
│   ├── pat.cycle_optimization_modeling
│   ├── pat.state_machine_modeling
│   ├── pat.path_cover_modeling
│   ├── pat.bounded_matching_modeling
│   ├── pat.flow_bounds_transformation
│   └── pat.min_flow_modeling
│
└── needs_boundary_note_attached（5个）
    ├── pat.k_shortest_modeling          ← +boundary_note
    ├── pat.layered_graph_modeling        ← +boundary_note
    ├── pat.node_demand_modeling          ← 合并 Demands + Node Demand
    ├── pat.max_flow_with_bounds          ← +boundary_note
    ├── pat.shortest_path_potentials      ← +boundary_note
    └── pat.stable_matching_pattern       ← +boundary_note（与二分图匹配）
```

---

## 执行确认清单

### ✅ 如果确认合并 Project Selection

- [ ] 将 2.21.131 的题面参考和训练数据补充到 `pat.project_selection_closure`
- [ ] 更新 `pat.project_selection_closure` 的 `example_problem_refs`
- [ ] 关闭 `pat.network_flow_project_selection` 的 Batch2 Draft
- [ ] Batch2 建议生成数更新为 12

### ✅ 如果确认保留 Stable Marriage

- [ ] `pat.stable_matching_pattern` 进入 Batch2 正式生成
- [ ] 添加与 `pat.bipartite_matching_modeling` 的边界说明
- [ ] 合并 2.21.143 知识库内容和 Batch2 Draft

### ✅ 无论决策结果

- [ ] **是否生成正式 patterns_batch2.json：否**（等待用户明确指令）
- [ ] **是否修改 patterns_v0_1_ready.json：否**（等待用户确认后执行修改）
- [ ] **是否修改主图谱：否**
- [ ] **是否应用 patch：否**

---

## 附录：决策树

### Project Selection 决策树

```
2.21.131 Project Selection
│
├── [推荐] 合并到 pat.project_selection_closure
│   ├── 效果：关闭 Batch2 Draft，补充 ready pattern
│   ├── 模式数：不增加
│   └── 风险：低
│
├── 保留为独立模式
│   ├── 效果：与 ready pattern 平行存在
│   ├── 模式数：+1（与现有模式重叠）
│   └── 风险：高（用户混淆）
│
└── 合并到 pat.min_cut_selection
    ├── 效果：作为最小割选择建模的应用特例
    ├── 模式数：不增加
    └── 风险：中（覆盖角度偏）
```

### Stable Marriage 决策树

```
2.21.143 Stable Marriage
│
├── [推荐] 保留为独立模式
│   ├── 效果：进入 Batch2，合并 Draft
│   ├── 模式数：+1
│   └── 风险：低（边界清晰）
│
├── 移动到知识库
│   ├── 效果：放弃 Draft，保留内容
│   ├── 模式数：不增加
│   └── 风险：中（失去模式识别价值）
│
└── 合并到二分图匹配
    ├── 效果：作为特例提及
    ├── 模式数：不增加
    └── 风险：中（特殊性丢失）
```

---

**Memo Status:** Awaiting User Confirmation
**Formal Patterns Generated:** false
**Main Graph Modified:** false
**Generated At:** 2026-05-22
**Generated By:** GLM5 (Thread 3)