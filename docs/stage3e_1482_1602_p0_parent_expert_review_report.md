# Stage3E 1482→1602 P0 行动清单报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-22T23:30:00.000Z
- **主图谱状态**: 未修改
- **当前基线**: item_count=1602, section_count=65, validate-only=passed

## P0 节点统计

| 类别 | 数量 |
|------|------|
| **P0 节点总数** | **68** |
| parent_concept weak/missing | 68 |
| needs_expert_review | 39 |
| 双重风险节点（高优先级） | 39 |

## 按系列分组统计

| 系列 | 总数 | parent_weak | expert_review | 双重风险 |
|------|------|-------------|---------------|---------|
| 上下界网络流（Flow with Lower Bounds） | 8 | 8 | 1 | 1 |
| 全局最小割（Global Min-Cut） | 6 | 6 | 5 | 5 |
| 其他 | 2 | 2 | 1 | 1 |
| 动态最小生成树（Dynamic MST） | 6 | 6 | 6 | 6 |
| 匹配与覆盖 | 7 | 7 | 0 | 0 |
| 可持久化结构（Persistent DS） | 4 | 4 | 1 | 1 |
| 图论建模 | 6 | 6 | 0 | 0 |
| 平面图（Planar Graph） | 6 | 6 | 5 | 5 |
| 序列维护结构 | 5 | 5 | 4 | 4 |
| 有向生成树（Directed MST） | 6 | 6 | 6 | 6 |
| 特殊图（Special Graph） | 5 | 5 | 5 | 5 |
| 高级 RMQ 变体 | 5 | 5 | 4 | 4 |
| 高级并查集 | 2 | 2 | 1 | 1 |

## 最优先处理的 20 个节点
- 🔴 **2.21.117**: 特殊图：Tournament Graph（batch2, Grade D）
  - 问题: parent_concept_missing, needs_expert_review | 建议: add_parent_concept
  - 当前父概念: 2.21 | 建议: 2.21
- 🔴 **2.21.76**: 有向生成树：Branching Theorem（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.77**: 有向生成树：Maximum Arborescence（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.78**: 有向生成树：Minimum Arborescence（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.79**: 有向生成树：Rooted Arborescence（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.80**: 有向生成树：Super Root Model（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.81**: 有向生成树：Weighted Directed Mst（batch1, Grade C）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.88**: 动态最小生成树：Batch Recomputation（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.89**: 动态最小生成树：Certificate Graph（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.90**: 动态最小生成树：Divide Conquer Approach（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.91**: 动态最小生成树：Edge Deletion（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.92**: 动态最小生成树：Edge Insertion（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.93**: 动态最小生成树：Sensitivity Analysis（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.6.4
- 🔴 **2.21.95**: 全局最小割：Pair Min Cut（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.16.3
- 🔴 **2.21.96**: 全局最小割：Random Contraction（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.16.3
- 🔴 **2.21.97**: 全局最小割：Recursive Contraction（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.16.3
- 🔴 **2.21.98**: 全局最小割：Sparsification（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.16.3
- 🔴 **2.21.99**: 全局最小割：Undirected Min Cut（batch1, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.16.3
- 🔴 **2.21.106**: 平面图：Dual Shortest Path（batch2, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.9
- 🔴 **2.21.107**: 平面图：Face Traversal（batch2, Grade B）
  - 问题: parent_concept_weak, needs_expert_review | 建议: review_before_batch5
  - 当前父概念: 2.21 | 建议: 2.21, 2.9

## 详细 P0 清单

### 系列：最大权闭合子图（Maximum Closure）
无P0节点

### 系列：有向生成树（Directed MST）
- **2.21.76**: 有向生成树：Branching Theorem - parent_concept_weak, needs_expert_review（high）
- **2.21.77**: 有向生成树：Maximum Arborescence - parent_concept_weak, needs_expert_review（high）
- **2.21.78**: 有向生成树：Minimum Arborescence - parent_concept_weak, needs_expert_review（high）
- **2.21.79**: 有向生成树：Rooted Arborescence - parent_concept_weak, needs_expert_review（high）
- **2.21.80**: 有向生成树：Super Root Model - parent_concept_weak, needs_expert_review（high）
- **2.21.81**: 有向生成树：Weighted Directed Mst - parent_concept_weak, needs_expert_review（high）

### 系列：支配树（Dominator Tree）

### 系列：动态最小生成树（Dynamic MST）
- **2.21.88**: 动态最小生成树：Batch Recomputation - parent_concept_weak, needs_expert_review（high）
- **2.21.89**: 动态最小生成树：Certificate Graph - parent_concept_weak, needs_expert_review（high）
- **2.21.90**: 动态最小生成树：Divide Conquer Approach - parent_concept_weak, needs_expert_review（high）
- **2.21.91**: 动态最小生成树：Edge Deletion - parent_concept_weak, needs_expert_review（high）
- **2.21.92**: 动态最小生成树：Edge Insertion - parent_concept_weak, needs_expert_review（high）
- **2.21.93**: 动态最小生成树：Sensitivity Analysis - parent_concept_weak, needs_expert_review（high）

### 系列：全局最小割（Global Min-Cut）
- **2.21.94**: 全局最小割：Cut Tree Query - parent_concept_weak（medium）
- **2.21.95**: 全局最小割：Pair Min Cut - parent_concept_weak, needs_expert_review（high）
- **2.21.96**: 全局最小割：Random Contraction - parent_concept_weak, needs_expert_review（high）
- **2.21.97**: 全局最小割：Recursive Contraction - parent_concept_weak, needs_expert_review（high）
- **2.21.98**: 全局最小割：Sparsification - parent_concept_weak, needs_expert_review（high）
- **2.21.99**: 全局最小割：Undirected Min Cut - parent_concept_weak, needs_expert_review（high）

### 系列：拟阵图论（Matroid）

### 系列：匹配与覆盖（Matching and Cover）
- **2.21.138**: 匹配与覆盖：Dilworth Theorem - parent_concept_weak（medium）
- **2.21.139**: 匹配与覆盖：Hall Theorem - parent_concept_weak（medium）
- **2.21.140**: 匹配与覆盖：Konig Theorem - parent_concept_weak（medium）
- **2.21.142**: 匹配与覆盖：Minimum Path Cover - parent_concept_weak（medium）
- **2.21.143**: 匹配与覆盖：Stable Marriage - parent_concept_weak（medium）
- **2.21.144**: 匹配与覆盖：Tutte Matrix - parent_concept_weak（medium）
- **2.21.145**: 匹配与覆盖：Weighted General Matching - parent_concept_weak（medium）

### 系列：可持久化结构（Persistent Data Structure）
- **3.13.107**: 可持久化结构：Fat Node Method - parent_concept_weak（medium）
- **3.13.108**: 可持久化结构：Path Copying Method - parent_concept_weak（medium）
- **3.13.109**: 可持久化结构：Rollback Vs Persistence - parent_concept_weak（medium）
- **3.13.110**: 可持久化结构：Version Dag - parent_concept_weak, needs_expert_review（high）

### 系列：高级RMQ变体（RMQ Variants）
- **3.13.111**: 高级 RMQ：Cache Friendly Rmq - parent_concept_weak, needs_expert_review（high）
- **3.13.112**: 高级 RMQ：Plus Minus One Rmq - parent_concept_weak, needs_expert_review（high）
- **3.13.113**: 高级 RMQ：Range Idempotent Query - parent_concept_weak（medium）
- **3.13.114**: 高级 RMQ：Sparse Table 2D - parent_concept_weak, needs_expert_review（high）
- **3.13.115**: 高级 RMQ：Static Range Mode - parent_concept_weak, needs_expert_review（high）

### 系列：简洁与概率结构（Succinct / Probabilistic）

### 系列：序列维护结构（Sequence Structure）
- **3.13.116**: 序列维护结构：Order Maintenance - parent_concept_weak（medium）
- **3.13.117**: 序列维护结构：Persistent Sequence - parent_concept_weak, needs_expert_review（high）
- **3.13.118**: 序列维护结构：Range Hash Maintenance - parent_concept_weak, needs_expert_review（high）
- **3.13.119**: 序列维护结构：Sequence Split Merge - parent_concept_weak, needs_expert_review（high）
- **3.13.120**: 序列维护结构：Text Editor Model - parent_concept_weak, needs_expert_review（high）

### 系列：树分治维护（Tree Decomposition DS）

### 系列：图论建模（Graph Modeling）
- **2.21.132**: 图论建模：K Shortest Paths - parent_concept_weak（medium）
- **2.21.133**: 图论建模：Layered Graph - parent_concept_weak（medium）
- **2.21.134**: 图论建模：Minimum Mean Cycle - parent_concept_weak（medium）
- **2.21.135**: 图论建模：Shortest Path Potentials - parent_concept_weak（medium）
- **2.21.136**: 图论建模：State Graph - parent_concept_weak（medium）
- **2.21.137**: 图论建模：Steiner Tree - parent_concept_weak（medium）

### 系列：高级平衡树（Advanced Balanced Tree）

### 系列：高级并查集（Advanced DSU）
- **3.13.141**: 高级并查集：Dsu On Tree - parent_concept_weak（medium）
- **3.13.142**: 高级并查集：可持久化版 - parent_concept_weak, needs_expert_review（high）

### 系列：平面图（Planar Graph）
- **2.21.106**: 平面图：Dual Shortest Path - parent_concept_weak, needs_expert_review（high）
- **2.21.107**: 平面图：Face Traversal - parent_concept_weak, needs_expert_review（high）
- **2.21.108**: 平面图：Outerplanar Graph - parent_concept_weak, needs_expert_review（high）
- **2.21.109**: 平面图：Planar Min Cut - parent_concept_weak, needs_expert_review（high）
- **2.21.110**: 平面图：Planar Separator - parent_concept_weak, needs_expert_review（high）
- **2.21.116**: 特殊图：Planar Dual Graph - parent_concept_weak（medium）

### 系列：特殊图（Special Graph）
- **2.21.112**: 特殊图：Bipartite Complement - parent_concept_weak, needs_expert_review（high）
- **2.21.113**: 特殊图：Condensation Dag - parent_concept_weak, needs_expert_review（high）
- **2.21.114**: 特殊图：Functional Graph - parent_concept_weak, needs_expert_review（high）
- **2.21.115**: 特殊图：Interval Graph - parent_concept_weak, needs_expert_review（high）
- **2.21.117**: 特殊图：Tournament Graph - parent_concept_missing, needs_expert_review（high）

### 系列：虚树（Virtual Tree）

### 系列：上下界网络流（Flow with Lower Bounds）
- **2.21.124**: 上下界网络流：Bounded Bipartite Matching - parent_concept_weak（medium）
- **2.21.125**: 上下界网络流：Demands - parent_concept_weak（medium）
- **2.21.126**: 上下界网络流：Edge Lower Bound Transform - parent_concept_weak, needs_expert_review（high）
- **2.21.127**: 上下界网络流：Maximum Flow - parent_concept_weak（medium）
- **2.21.128**: 上下界网络流：Min Cost Circulation - parent_concept_weak（medium）
- **2.21.129**: 上下界网络流：Minimum Flow - parent_concept_weak（medium）
- **2.21.130**: 上下界网络流：Node Demand - parent_concept_weak（medium）
- **2.21.131**: 上下界网络流：Project Selection - parent_concept_weak（medium）

## 双重风险节点（高风险优先处理）
- 🔴 **2.21.76**: 有向生成树：Branching Theorem - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.77**: 有向生成树：Maximum Arborescence - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.78**: 有向生成树：Minimum Arborescence - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.79**: 有向生成树：Rooted Arborescence - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.80**: 有向生成树：Super Root Model - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.81**: 有向生成树：Weighted Directed Mst - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.88**: 动态最小生成树：Batch Recomputation - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.89**: 动态最小生成树：Certificate Graph - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.90**: 动态最小生成树：Divide Conquer Approach - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.91**: 动态最小生成树：Edge Deletion - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.92**: 动态最小生成树：Edge Insertion - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.93**: 动态最小生成树：Sensitivity Analysis - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.95**: 全局最小割：Pair Min Cut - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.96**: 全局最小割：Random Contraction - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.97**: 全局最小割：Recursive Contraction - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.98**: 全局最小割：Sparsification - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.99**: 全局最小割：Undirected Min Cut - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.106**: 平面图：Dual Shortest Path - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.107**: 平面图：Face Traversal - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.108**: 平面图：Outerplanar Graph - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.109**: 平面图：Planar Min Cut - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.110**: 平面图：Planar Separator - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.111**: 强连通分量 DAG：Implication Graph - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.112**: 特殊图：Bipartite Complement - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.113**: 特殊图：Condensation Dag - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.114**: 特殊图：Functional Graph - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.115**: 特殊图：Interval Graph - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.117**: 特殊图：Tournament Graph - parent_concept_missing, needs_expert_review | 建议: add_parent_concept
- 🔴 **3.13.110**: 可持久化结构：Version Dag - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.111**: 高级 RMQ：Cache Friendly Rmq - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.112**: 高级 RMQ：Plus Minus One Rmq - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.114**: 高级 RMQ：Sparse Table 2D - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.115**: 高级 RMQ：Static Range Mode - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.117**: 序列维护结构：Persistent Sequence - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.118**: 序列维护结构：Range Hash Maintenance - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.119**: 序列维护结构：Sequence Split Merge - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.120**: 序列维护结构：Text Editor Model - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **2.21.126**: 上下界网络流：Edge Lower Bound Transform - parent_concept_weak, needs_expert_review | 建议: review_before_batch5
- 🔴 **3.13.142**: 高级并查集：可持久化版 - parent_concept_weak, needs_expert_review | 建议: review_before_batch5

## Batch5 准备建议

### 是否建议先修 parent_concept 再继续 Batch5？

**建议: 先处理 P0 后再继续 Batch5**

**理由**:
1. P0 节点共 68 个
2. 其中 39 个高风险节点需优先处理
3. 68 个节点存在父概念弱/缺失问题
4. 39 个节点需专家审查

### 如果继续 Batch5，是否仍建议 smaller_15？

**建议: smaller_15**

**理由**:
1. 虽有 P0 问题但整体质量良好（Grade A/B 占 94.2%）
2. 缩小 batch size 可降低每次合并的风险
3. 快速迭代有利于尽早发现依赖问题

**建议步骤**:
1. 先处理 39 个高风险双重风险节点
2. 补充 parent_concept
3. 完成 expert_review
4. 以 smaller_15 模式启动 Batch5

## 主图谱状态

- **主图谱是否修改**: **否**
- **本次任务**: 仅整理 P0 清单，不涉及图谱修改
- **下一步**: 应用 P0 清单修复

---

报告生成时间: 2026-05-22T23:30:00.000Z
生成者: GLM5
任务类型: Stage3E 1482→1602 P0 行动清单
主图谱修改状态: 否
