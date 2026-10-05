# Stage3E 1482→1602 双重风险节点分级报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-22T23:45:00.000Z
- **主图谱状态**: 未修改
- **当前基线**: item_count=1602, section_count=65, validate-only=passed

## 分级统计

| 分级 | 数量 | 说明 |
|------|------|------|
| **双重风险节点总数** | **39** | |
| **P0-A** | **3** | 阻塞Batch5，需人工确认 |
| **P0-B** | **36** | 不阻塞，可B级复查 |
| **defer** | **0** | 不阻塞，后续整理 |

## 按系列分级分布

| 系列 | 总数 | P0-A | P0-B | defer |
|------|------|------|------|-------|
| 上下界网络流（Flow with Lower Bounds） | 1 | 0 | 1 | 0 |
| 全局最小割（Global Min-Cut） | 5 | 0 | 5 | 0 |
| 其他 | 1 | 0 | 1 | 0 |
| 动态最小生成树（Dynamic MST） | 6 | 0 | 6 | 0 |
| 可持久化结构（Persistent DS） | 1 | 0 | 1 | 0 |
| 平面图（Planar Graph） | 5 | 1 | 4 | 0 |
| 序列维护结构 | 4 | 0 | 4 | 0 |
| 有向生成树（Directed MST） | 6 | 1 | 5 | 0 |
| 特殊图（Special Graph） | 5 | 1 | 4 | 0 |
| 高级 RMQ 变体 | 4 | 0 | 4 | 0 |
| 高级并查集 | 1 | 0 | 1 | 0 |

## 重点系列分级详情

### 1. 动态最小生成树（Dynamic MST）
- **2.21.88**: 动态最小生成树：Batch Recomputation → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.89**: 动态最小生成树：Certificate Graph → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.90**: 动态最小生成树：Divide Conquer Approach → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.91**: 动态最小生成树：Edge Deletion → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.92**: 动态最小生成树：Edge Insertion → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.93**: 动态最小生成树：Sensitivity Analysis → **P0-B** | 变体节点，可暂时接受现有 parent 候选

### 2. 有向生成树（Directed MST）
- **2.21.76**: 有向生成树：Branching Theorem → **P0-A** | 高级/学术概念
- **2.21.77**: 有向生成树：Maximum Arborescence → **P0-B** | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.78**: 有向生成树：Minimum Arborescence → **P0-B** | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.79**: 有向生成树：Rooted Arborescence → **P0-B** | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.80**: 有向生成树：Super Root Model → **P0-B** | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.81**: 有向生成树：Weighted Directed Mst → **P0-B** | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受

### 3. 全局最小割（Global Min-Cut）
- **2.21.95**: 全局最小割：Pair Min Cut → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.96**: 全局最小割：Random Contraction → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.97**: 全局最小割：Recursive Contraction → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.98**: 全局最小割：Sparsification → **P0-B** | 变体节点，可暂时接受现有 parent 候选
- **2.21.99**: 全局最小割：Undirected Min Cut → **P0-B** | 变体节点，可暂时接受现有 parent 候选

### 4. 平面图（Planar Graph）
- **2.21.106**: 平面图：Dual Shortest Path → **P0-A** | 平面图对偶是核心概念，需要确认父概念
- **2.21.107**: 平面图：Face Traversal → **P0-B** | 平面图变体，可暂时接受现有 parent 候选
- **2.21.108**: 平面图：Outerplanar Graph → **P0-B** | 平面图变体，可暂时接受现有 parent 候选
- **2.21.109**: 平面图：Planar Min Cut → **P0-B** | 平面图变体，可暂时接受现有 parent 候选
- **2.21.110**: 平面图：Planar Separator → **P0-B** | 平面图变体，可暂时接受现有 parent 候选

### 5. 特殊图（Special Graph）
- **2.21.112**: 特殊图：Bipartite Complement → **P0-B** | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.113**: 特殊图：Condensation Dag → **P0-B** | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.114**: 特殊图：Functional Graph → **P0-B** | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.115**: 特殊图：Interval Graph → **P0-B** | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.117**: 特殊图：Tournament Graph → **P0-A** | 质量等级 D 严重存疑

### 6. 序列维护结构（Sequence Structure）
- **3.13.117**: 序列维护结构：Persistent Sequence → **P0-B** | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.118**: 序列维护结构：Range Hash Maintenance → **P0-B** | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.119**: 序列维护结构：Sequence Split Merge → **P0-B** | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.120**: 序列维护结构：Text Editor Model → **P0-B** | 序列维护变体，可暂时接受现有 parent 候选

### 7. 高级 RMQ 变体
- **3.13.111**: 高级 RMQ：Cache Friendly Rmq → **P0-B** | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.112**: 高级 RMQ：Plus Minus One Rmq → **P0-B** | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.114**: 高级 RMQ：Sparse Table 2D → **P0-B** | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.115**: 高级 RMQ：Static Range Mode → **P0-B** | RMQ 高级变体，可暂时接受现有 parent 候选

### 8. 上下界网络流（Flow with Lower Bounds）
- **2.21.126**: 上下界网络流：Edge Lower Bound Transform → **P0-B** | 网络流变体，父概念可暂时接受

### 其他系列
- **2.21.111**: 强连通分量 DAG：Implication Graph（其他）→ **P0-B** | 有明确父概念候选，可暂时接受
- **3.13.110**: 可持久化结构：Version Dag（可持久化结构（Persistent DS））→ **P0-B** | 实现变体节点，可暂时接受现有 parent 候选
- **3.13.142**: 高级并查集：可持久化版（高级并查集）→ **P0-B** | 有明确父概念候选，可暂时接受

## 最阻塞 Batch5 的节点列表
- 🔴 **2.21.76**: 有向生成树：Branching Theorem（有向生成树（Directed MST））
- 🔴 **2.21.106**: 平面图：Dual Shortest Path（平面图（Planar Graph））
- 🔴 **2.21.117**: 特殊图：Tournament Graph（特殊图（Special Graph））

## 需要人工确认的 Top 10 节点
1. 🔴 **2.21.76**: 有向生成树：Branching Theorem（有向生成树（Directed MST））→ P0-A
2. 🔴 **2.21.117**: 特殊图：Tournament Graph（特殊图（Special Graph））→ P0-A
3. 🔴 **2.21.106**: 平面图：Dual Shortest Path（平面图（Planar Graph））→ P0-A
4. 🟡 **2.21.77**: 有向生成树：Maximum Arborescence（有向生成树（Directed MST））→ P0-B
5. 🟡 **2.21.78**: 有向生成树：Minimum Arborescence（有向生成树（Directed MST））→ P0-B
6. 🟡 **2.21.79**: 有向生成树：Rooted Arborescence（有向生成树（Directed MST））→ P0-B
7. 🟡 **2.21.80**: 有向生成树：Super Root Model（有向生成树（Directed MST））→ P0-B
8. 🟡 **2.21.81**: 有向生成树：Weighted Directed Mst（有向生成树（Directed MST））→ P0-B
9. 🟡 **2.21.88**: 动态最小生成树：Batch Recomputation（动态最小生成树（Dynamic MST））→ P0-B
10. 🟡 **2.21.89**: 动态最小生成树：Certificate Graph（动态最小生成树（Dynamic MST））→ P0-B

## Batch5 建议

### 是否建议继续 Batch5？

**建议: 可以继续，但需先处理 P0-A 节点**

- P0-A 阻塞节点: 3 个
- P0-B 不阻塞节点: 36 个
- defer 节点: 0 个

### 如果继续 Batch5，是否仍建议 smaller_15？

**建议: smaller_15**

**理由**:
1. 3 个 P0-A 节点需要在 Batch5 前确认父概念
2. 这些节点主要是高级/学术概念，父概念选择错误会影响后续节点
3. 建议人工确认后再以 smaller_15 启动 Batch5

## 完整分级清单

### P0-A（3 个）- 阻塞 Batch5
- **2.21.76**: 有向生成树：Branching Theorem（有向生成树（Directed MST））
  - 建议: expert_confirm_before_batch5 | 高级/学术概念
  - 候选父概念: 2.21, 2.6.4
- **2.21.106**: 平面图：Dual Shortest Path（平面图（Planar Graph））
  - 建议: expert_confirm_before_batch5 | 平面图对偶是核心概念，需要确认父概念
  - 候选父概念: 2.21, 2.9
- **2.21.117**: 特殊图：Tournament Graph（特殊图（Special Graph））
  - 建议: expert_confirm_before_batch5 | 质量等级 D 严重存疑
  - 候选父概念: 2.21

### P0-B（36 个）- 不阻塞
- **2.21.77**: 有向生成树：Maximum Arborescence（有向生成树（Directed MST））
  - 建议: keep_with_B_review | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.78**: 有向生成树：Minimum Arborescence（有向生成树（Directed MST））
  - 建议: keep_with_B_review | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.79**: 有向生成树：Rooted Arborescence（有向生成树（Directed MST））
  - 建议: keep_with_B_review | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.80**: 有向生成树：Super Root Model（有向生成树（Directed MST））
  - 建议: keep_with_B_review | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.81**: 有向生成树：Weighted Directed Mst（有向生成树（Directed MST））
  - 建议: keep_with_B_review | 变体节点，可根据 Chu-Liu/Edmonds 的父概念暂时接受
- **2.21.88**: 动态最小生成树：Batch Recomputation（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.89**: 动态最小生成树：Certificate Graph（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.90**: 动态最小生成树：Divide Conquer Approach（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.91**: 动态最小生成树：Edge Deletion（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.92**: 动态最小生成树：Edge Insertion（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.93**: 动态最小生成树：Sensitivity Analysis（动态最小生成树（Dynamic MST））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.95**: 全局最小割：Pair Min Cut（全局最小割（Global Min-Cut））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.96**: 全局最小割：Random Contraction（全局最小割（Global Min-Cut））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.97**: 全局最小割：Recursive Contraction（全局最小割（Global Min-Cut））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.98**: 全局最小割：Sparsification（全局最小割（Global Min-Cut））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.99**: 全局最小割：Undirected Min Cut（全局最小割（Global Min-Cut））
  - 建议: keep_with_B_review | 变体节点，可暂时接受现有 parent 候选
- **2.21.107**: 平面图：Face Traversal（平面图（Planar Graph））
  - 建议: keep_with_B_review | 平面图变体，可暂时接受现有 parent 候选
- **2.21.108**: 平面图：Outerplanar Graph（平面图（Planar Graph））
  - 建议: keep_with_B_review | 平面图变体，可暂时接受现有 parent 候选
- **2.21.109**: 平面图：Planar Min Cut（平面图（Planar Graph））
  - 建议: keep_with_B_review | 平面图变体，可暂时接受现有 parent 候选
- **2.21.110**: 平面图：Planar Separator（平面图（Planar Graph））
  - 建议: keep_with_B_review | 平面图变体，可暂时接受现有 parent 候选
- **2.21.111**: 强连通分量 DAG：Implication Graph（其他）
  - 建议: keep_with_B_review | 有明确父概念候选，可暂时接受
- **2.21.112**: 特殊图：Bipartite Complement（特殊图（Special Graph））
  - 建议: keep_with_B_review | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.113**: 特殊图：Condensation Dag（特殊图（Special Graph））
  - 建议: keep_with_B_review | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.114**: 特殊图：Functional Graph（特殊图（Special Graph））
  - 建议: keep_with_B_review | 特殊图变体，可暂时接受现有 parent 候选
- **2.21.115**: 特殊图：Interval Graph（特殊图（Special Graph））
  - 建议: keep_with_B_review | 特殊图变体，可暂时接受现有 parent 候选
- **3.13.110**: 可持久化结构：Version Dag（可持久化结构（Persistent DS））
  - 建议: keep_with_B_review | 实现变体节点，可暂时接受现有 parent 候选
- **3.13.111**: 高级 RMQ：Cache Friendly Rmq（高级 RMQ 变体）
  - 建议: keep_with_B_review | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.112**: 高级 RMQ：Plus Minus One Rmq（高级 RMQ 变体）
  - 建议: keep_with_B_review | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.114**: 高级 RMQ：Sparse Table 2D（高级 RMQ 变体）
  - 建议: keep_with_B_review | RMQ 优化变体，可暂时接受现有 parent 候选
- **3.13.115**: 高级 RMQ：Static Range Mode（高级 RMQ 变体）
  - 建议: keep_with_B_review | RMQ 高级变体，可暂时接受现有 parent 候选
- **3.13.117**: 序列维护结构：Persistent Sequence（序列维护结构）
  - 建议: keep_with_B_review | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.118**: 序列维护结构：Range Hash Maintenance（序列维护结构）
  - 建议: keep_with_B_review | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.119**: 序列维护结构：Sequence Split Merge（序列维护结构）
  - 建议: keep_with_B_review | 序列维护变体，可暂时接受现有 parent 候选
- **3.13.120**: 序列维护结构：Text Editor Model（序列维护结构）
  - 建议: keep_with_B_review | 序列维护变体，可暂时接受现有 parent 候选
- **2.21.126**: 上下界网络流：Edge Lower Bound Transform（上下界网络流（Flow with Lower Bounds））
  - 建议: keep_with_B_review | 网络流变体，父概念可暂时接受
- **3.13.142**: 高级并查集：可持久化版（高级并查集）
  - 建议: keep_with_B_review | 有明确父概念候选，可暂时接受

### defer（0 个）- 后续整理

## 主图谱状态

- **主图谱是否修改**: **否**
- **本次任务**: 仅双重风险节点分级，不涉及图谱修改
- **下一步**: 处理 P0-A 阻塞节点后启动 Batch5

---

报告生成时间: 2026-05-22T23:45:00.000Z
生成者: GLM5
任务类型: Stage3E 1482→1602 Dual Risk Triage
主图谱修改状态: 否
