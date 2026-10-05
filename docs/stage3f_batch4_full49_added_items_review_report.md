# Stage3F Batch4 Full49 Added Items Review Report

**生成时间**: 2026-05-25 09:59:16 UTC
**生成者**: GLM5 (2号线程)
**任务类型**: Added Items Review（仅复查，不修改主图谱）

---

## 1. 概览

| 指标 | 值 |
|------|-----|
| Batch4 新增节点 | 49 |
| 合并前 item_count | 1716 |
| 合并后 item_count | 1765 |
| section_count | 65 |
| validate-only passed | True |
| dangling_refs | 0 |
| direct_pre_cycle | None |
| resolved_pre_mismatches | 0 |

## 2. 复查结果汇总

| 复查结果 | 数量 | 说明 |
|----------|------|------|
| approve | 15 | 自动审批通过 |
| keep_manual_review | 3 | 需人工确认 direct_pre 映射 |
| needs_dependency_fix | 31 | direct_pre 过长，需缩减 |
| move_to_problem_patterns | 0 | 建议同步到 problem_patterns |
| needs_merge_or_collapse | 0 | 与已有节点重复 |
| **合计** | 49 | |

## 3. 优先级分布

| 优先级 | 数量 |
|--------|------|
| A | 1 |
| B | 8 |
| C | 40 |

## 4. 按 Section 分布

| Section | 名称 | 新增 | direct_pre 问题 | 评估 |
|---------|------|------|---------------|------|
| 2.10 | 字符串算法 | 4 | 3/4 个 | ⚠️ 需依赖修复 |
| 2.21 | 高级图论扩展 | 20 | 20/20 个 | ⚠️ 密集新增，注意过度拆分 |
| 2.8 | 动态规划 | 6 | 6/6 个 | ⚠️ 需依赖修复 |
| 3.13 | 高级数据结构扩展 | 15 | 0 | ⚠️ 密集新增，注意过度拆分 |
| 4.4 | 离散数学基础 | 2 | 0 | ✅ 正常 |
| 4.5 | 图与树的数学基础 | 2 | 2/2 个 | ⚠️ 需依赖修复 |

## 5. 节点复查明细

| # | item_id | name | section | type | result | priority | direct_pre | issues |
|---|--------|------|---------|------|--------|----------|-----------|--------|
| 1 | 2.10.39 | Sunday算法 | 2.10 | core_concept | keep_manual_review | C | 218 | direct_pre 过长 (218个)，可能包含大量泛化依赖; direct_pre (218) 接近整节 item 数 (41)，疑似整节引用 |
| 2 | 2.10.40 | Duval算法最小表示 | 2.10 | core_concept | needs_dependency_fix | C | 218 | direct_pre 过长 (218个)，可能包含大量泛化依赖; direct_pre (218) 接近整节 item 数 (41)，疑似整节引用 |
| 3 | 2.10.41 | 二维滚动哈希 | 2.10 | core_concept | needs_dependency_fix | C | 218 | direct_pre 过长 (218个)，可能包含大量泛化依赖; direct_pre (218) 接近整节 item 数 (41)，疑似整节引用 |
| 4 | 2.10.42 | 哈希碰撞处理策略 | 2.10 | core_concept | needs_dependency_fix | C | 218 | direct_pre 过长 (218个)，可能包含大量泛化依赖; direct_pre (218) 接近整节 item 数 (41)，疑似整节引用 |
| 5 | 2.21.152 | 最大权闭合子图：Penalty Modeling | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 6 | 2.21.153 | 动态图连通性：Connectivity Snapshots | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 7 | 2.21.154 | 动态图连通性：Dynamic Biconnectivity | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 8 | 2.21.155 | 动态图连通性：Dynamic Bridge | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 9 | 2.21.156 | 全局最小割：Minimum Cut Modeling | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 10 | 2.21.157 | 强连通分量 DAG：Component Topo Order | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 11 | 2.21.158 | 强连通分量 DAG：Scc Dp | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 12 | 2.21.159 | 差分约束系统建模 | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 13 | 2.21.160 | 动态图连通性：Fully Dynamic Overview | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 14 | 2.21.161 | Hall 定理及应用 | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 15 | 2.21.162 | 最大权闭合子图 | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 16 | 2.21.163 | 平面图：Embedding Basics | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 17 | 2.21.164 | 高级最短路：Eppstein K Shortest | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 18 | 2.21.165 | 高级最短路：Johnson Potentials | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 19 | 2.21.166 | 高级最短路：Min Cost Path Cover | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 20 | 2.21.167 | 高级最短路：Replacement Paths | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 21 | 2.21.168 | 高级最短路：Resource Constrained | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 22 | 2.21.169 | 高级最短路：Yen K Shortest | 2.21 | core_concept | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 23 | 2.21.170 | 高级最短路：Zero One Bfs Modeling | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 24 | 2.21.171 | 2-SAT 建模技巧 | 2.21 | modeling_pattern | needs_dependency_fix | C | 113 | direct_pre 过长 (113个)，可能包含大量泛化依赖 |
| 25 | 2.8.151 | 博弈DP基础 | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 26 | 2.8.152 | Grundy数DP | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 27 | 2.8.153 | 矩阵DP基础 | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 28 | 2.8.154 | 矩阵快速幂DP | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 29 | 2.8.155 | 期望DP | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 30 | 2.8.156 | 马尔可夫链DP | 2.8 | core_concept | needs_dependency_fix | C | 202 | direct_pre 过长 (202个)，可能包含大量泛化依赖; direct_pre (202) 接近整节 item 数 (156)，疑似整节引用 |
| 31 | 3.13.192 | 高级并查集：Component Aggregate | 3.13 | core_concept | approve | B | 0 | - |
| 32 | 3.13.193 | 高级并查集：Distance | 3.13 | core_concept | approve | B | 0 | - |
| 33 | 3.13.194 | 高级并查集：Offline Dynamic Connectivity | 3.13 | core_concept | approve | B | 0 | - |
| 34 | 3.13.195 | 高级并查集：Small To Large | 3.13 | core_concept | approve | B | 0 | - |
| 35 | 3.13.196 | 高级并查集：Weighted | 3.13 | core_concept | approve | B | 0 | - |
| 36 | 3.13.197 | 李超线段树：Cht Comparison | 3.13 | core_concept | approve | B | 0 | - |
| 37 | 3.13.198 | 可持久化结构：Retroactive Overview | 3.13 | core_concept | approve | B | 0 | - |
| 38 | 3.13.199 | 线段树变体：Matrix Segment Tree | 3.13 | implementation_variant | approve | C | 0 | - |
| 39 | 3.13.200 | 线段树变体：Merge 变体 1 | 3.13 | implementation_variant | approve | C | 0 | - |
| 40 | 3.13.201 | 线段树变体：Persistent Segment Tree | 3.13 | implementation_variant | approve | C | 0 | - |
| 41 | 3.13.202 | 线段树变体：Range Assign Lazy | 3.13 | implementation_variant | approve | C | 0 | - |
| 42 | 3.13.203 | 线段树变体：Segment Tree Of Vectors | 3.13 | implementation_variant | approve | C | 0 | - |
| 43 | 3.13.204 | 线段树变体：Segment Tree Over Time | 3.13 | implementation_variant | approve | C | 0 | - |
| 44 | 3.13.205 | 线段树变体：Two Dimensional Segment Tree | 3.13 | implementation_variant | approve | C | 0 | - |
| 45 | 3.13.206 | 简洁与概率结构：Van Emde Boas Overview | 3.13 | core_concept | approve | B | 0 | - |
| 46 | 4.4.15 | 线性递推基础 | 4.4 | core_concept | keep_manual_review | C | 88 | direct_pre 过长 (88个)，可能包含大量泛化依赖; direct_pre (88) 接近整节 item 数 (16)，疑似整节引用 |
| 47 | 4.4.16 | Kitamasa算法 | 4.4 | core_concept | keep_manual_review | C | 88 | direct_pre 过长 (88个)，可能包含大量泛化依赖; direct_pre (88) 接近整节 item 数 (16)，疑似整节引用 |
| 48 | 4.5.17 | GF(2)上的高斯消元 | 4.5 | core_concept | needs_dependency_fix | C | 152 | direct_pre 过长 (152个)，可能包含大量泛化依赖; direct_pre (152) 接近整节 item 数 (18)，疑似整节引用 |
| 49 | 4.5.18 | 矩阵树定理 | 4.5 | theorem_or_property | needs_dependency_fix | A | 152 | direct_pre 过长 (152个)，可能包含大量泛化依赖; direct_pre (152) 接近整节 item 数 (18)，疑似整节引用 |

## 6. 3 个 Medium 风险候选依赖复查

### Sunday算法 (2.10.39)

- **candidate_id**: cand.string.string_matching.sunday
- **direct_pre 数**: 218
- **resolved_pre 数**: 298
- **contains section ref**: 否
- ⚠️ direct_pre 过多 (218)，可能存在将 resolved_pre 误当作 direct_pre
- **问题**: direct_pre 过长 (218个)，可能包含大量泛化依赖; direct_pre (218) 接近整节 item 数 (41)，疑似整节引用; medium 风险候选，需人工确认 direct_pre 是否为必要前置
- **复查结论**: direct_pre 过长 (218个)，可能包含大量泛化依赖

### 线性递推基础 (4.4.15)

- **candidate_id**: cand.math.linear_recurrence.basic
- **direct_pre 数**: 88
- **resolved_pre 数**: 137
- **contains section ref**: 否
- ⚠️ direct_pre 过多 (88)，可能存在将 resolved_pre 误当作 direct_pre
- **问题**: direct_pre 过长 (88个)，可能包含大量泛化依赖; direct_pre (88) 接近整节 item 数 (16)，疑似整节引用; medium 风险候选，需人工确认 direct_pre 是否为必要前置
- **复查结论**: direct_pre 过长 (88个)，可能包含大量泛化依赖

### Kitamasa算法 (4.4.16)

- **candidate_id**: cand.math.linear_recurrence.kitamasa
- **direct_pre 数**: 88
- **resolved_pre 数**: 137
- **contains section ref**: 否
- ⚠️ direct_pre 过多 (88)，可能存在将 resolved_pre 误当作 direct_pre
- **问题**: direct_pre 过长 (88个)，可能包含大量泛化依赖; direct_pre (88) 接近整节 item 数 (16)，疑似整节引用; medium 风险候选，需人工确认 direct_pre 是否为必要前置
- **复查结论**: direct_pre 过长 (88个)，可能包含大量泛化依赖

## 7. 2.21 / 3.13 密集新增分析

### 2.21 高级图论扩展

- 本次新增: 20
- 节内总 item 数: 171
- 新增占比: 11.7%
- 需依赖修复: 20
- 建议同步 problem_patterns: 0
- **评估**: ⚠️ 密集新增 + 大范围 direct_pre 过长，建议进入 Fix Lite
  - 2.21.152 最大权闭合子图：Penalty Modeling: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.153 动态图连通性：Connectivity Snapshots: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.154 动态图连通性：Dynamic Biconnectivity: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.155 动态图连通性：Dynamic Bridge: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.156 全局最小割：Minimum Cut Modeling: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.157 强连通分量 DAG：Component Topo Order: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.158 强连通分量 DAG：Scc Dp: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.159 差分约束系统建模: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.160 动态图连通性：Fully Dynamic Overview: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.161 Hall 定理及应用: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.162 最大权闭合子图: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.163 平面图：Embedding Basics: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.164 高级最短路：Eppstein K Shortest: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.165 高级最短路：Johnson Potentials: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.166 高级最短路：Min Cost Path Cover: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.167 高级最短路：Replacement Paths: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.168 高级最短路：Resource Constrained: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.169 高级最短路：Yen K Shortest: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.170 高级最短路：Zero One Bfs Modeling: direct_pre 过长 (113个)，可能包含大量泛化依赖
  - 2.21.171 2-SAT 建模技巧: direct_pre 过长 (113个)，可能包含大量泛化依赖

### 3.13 高级数据结构扩展

- 本次新增: 15
- 节内总 item 数: 174
- 新增占比: 8.6%
- 需依赖修复: 0
- 建议同步 problem_patterns: 0
- **评估**: ✅ 合理

## 8. 建议同步到 Problem Patterns

- 2.21.152 最大权闭合子图：Penalty Modeling (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
- 2.21.156 全局最小割：Minimum Cut Modeling (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
- 2.21.159 差分约束系统建模 (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
- 2.21.161 Hall 定理及应用 (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
- 2.21.170 高级最短路：Zero One Bfs Modeling (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
- 2.21.171 2-SAT 建模技巧 (2.21): 建模/应用/技巧类节点，可同步到 problem_patterns
## 9. 建议合并/折叠

无建议合并节点。

## 10. 建议依赖修复

以下节点 direct_pre 过长，需在 Fix Lite 阶段缩减至必要前置：

| item_id | name | direct_pre | 所在 Section |
|---------|------|-----------|-------------|
| 2.10.39 | Sunday算法 | 218 | 2.10 |
| 2.10.40 | Duval算法最小表示 | 218 | 2.10 |
| 2.10.41 | 二维滚动哈希 | 218 | 2.10 |
| 2.10.42 | 哈希碰撞处理策略 | 218 | 2.10 |
| 2.21.152 | 最大权闭合子图：Penalty Modeling | 113 | 2.21 |
| 2.21.153 | 动态图连通性：Connectivity Snapshots | 113 | 2.21 |
| 2.21.154 | 动态图连通性：Dynamic Biconnectivity | 113 | 2.21 |
| 2.21.155 | 动态图连通性：Dynamic Bridge | 113 | 2.21 |
| 2.21.156 | 全局最小割：Minimum Cut Modeling | 113 | 2.21 |
| 2.21.157 | 强连通分量 DAG：Component Topo Order | 113 | 2.21 |
| 2.21.158 | 强连通分量 DAG：Scc Dp | 113 | 2.21 |
| 2.21.159 | 差分约束系统建模 | 113 | 2.21 |
| 2.21.160 | 动态图连通性：Fully Dynamic Overview | 113 | 2.21 |
| 2.21.161 | Hall 定理及应用 | 113 | 2.21 |
| 2.21.162 | 最大权闭合子图 | 113 | 2.21 |
| 2.21.163 | 平面图：Embedding Basics | 113 | 2.21 |
| 2.21.164 | 高级最短路：Eppstein K Shortest | 113 | 2.21 |
| 2.21.165 | 高级最短路：Johnson Potentials | 113 | 2.21 |
| 2.21.166 | 高级最短路：Min Cost Path Cover | 113 | 2.21 |
| 2.21.167 | 高级最短路：Replacement Paths | 113 | 2.21 |
| 2.21.168 | 高级最短路：Resource Constrained | 113 | 2.21 |
| 2.21.169 | 高级最短路：Yen K Shortest | 113 | 2.21 |
| 2.21.170 | 高级最短路：Zero One Bfs Modeling | 113 | 2.21 |
| 2.21.171 | 2-SAT 建模技巧 | 113 | 2.21 |
| 2.8.151 | 博弈DP基础 | 202 | 2.8 |
| 2.8.152 | Grundy数DP | 202 | 2.8 |
| 2.8.153 | 矩阵DP基础 | 202 | 2.8 |
| 2.8.154 | 矩阵快速幂DP | 202 | 2.8 |
| 2.8.155 | 期望DP | 202 | 2.8 |
| 2.8.156 | 马尔可夫链DP | 202 | 2.8 |
| 4.4.15 | 线性递推基础 | 88 | 4.4 |
| 4.4.16 | Kitamasa算法 | 88 | 4.4 |
| 4.5.17 | GF(2)上的高斯消元 | 152 | 4.5 |
| 4.5.18 | 矩阵树定理 | 152 | 4.5 |

**建议修复方案**: 将 direct_pre 从当前全量前置节 item 列表缩减为仅包含直接依赖的核心概念（通常 3-10 个），其余依赖可通过 resolved_pre 继承。具体做法：删除 section-level 批量引用，只保留对直接前置概念的 item 级引用。
## 11. 结论与建议

| 建议项 | 值 |
|-------|-----|
| 是否建议进入 Fix Lite | **是** |
| Fix Lite 内容 | 依赖修复 + direct_pre 缩减 |
| 是否建议继续 Stage3F Batch5 | 建议先 Fix Lite |
| 主图谱是否修改 | 否 |

**⚠️ 核心问题**: 批量新增的 2.21 高级图论扩展（20个）和 2.10 字符串算法（4个）等节点的 direct_pre 被设置为整节全部前置 item（113~218个），而非仅直接依赖的核心概念。这会导致依赖图过于稠密，影响后续推理性能。建议在 Fix Lite 阶段精简。

**最终结论**: Batch4 full49 合并完成，主图谱状态正常。
部分节点需先进入 Fix Lite 处理依赖修复，再继续 Batch5。