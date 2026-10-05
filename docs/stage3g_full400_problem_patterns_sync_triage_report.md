# Stage3G full400 Problem Patterns Sync Triage 报告

## 概况

| 指标 | 值 |
|:-----|:---:|
| **候选总数** | **94** |
| **create_new_draft_later** | **20** |
| **merge_with_existing** | **9** |
| **defer** | **65** |
| **manual_review** | **0** |
| **P0** | 0 |
| **P1** | 8 |
| **P2** | 12 |
| **defer（含 merge_with_existing）** | 74 |

---

## 输入验证

| 检查 | 结果 |
|:-----|:----:|
| full400 Merge 完成 (1765 → 2165) | ✅ |
| full400 Review 完成 (400/400 approve) | ✅ |
| full400 Fix Lite 完成 (400 demote to C) | ✅ |
| Stable Checkpoint 已生成 | ✅ |
| sync_candidates total = 94 | ✅ |
| validate-only passed | ✅ |
| item_count = 2165, section_count = 65 | ✅ |

---

## 分级详情

### P1 — 推荐进入 patterns_batch4（8 个）

| # | item_id | Pattern ID | 名称 | 识别信号 |
|:-:|:--------|:-----------|:-----|:---------|
| 1 | 2.4.52 | pat.parallel_binary_search | 整体二分应用 | 多组离线查询，答案具有单调性，值域二分+分治递归 |
| 2 | 2.8.189 | pat.matrix_exponentiation_dp | DP与矩阵乘法优化 | 线性递推/状态转移图，N很大但转移维度小，DP→矩阵→快速幂 |
| 3 | 2.9.136 | pat.two_pointer_sliding_window | 双指针/滑动窗口建模 | 连续子数组/子串满足约束条件，O(n)单次扫描 |
| 4 | 2.9.138 | pat.meet_in_the_middle | 折半搜索 | N≤40的枚举/组合问题，一半指数枚举+合并 |
| 5 | 2.15.19 | pat.congruence_shortest_path_modeling | 同余最短路 | 给定若干数，求能拼出的最小/最大不可表示数 |
| 6 | 2.16.39 | pat.max_density_subgraph | 最大密度子图 | 子图边权/点权密度优化，参数搜索+最小割 |
| 7 | 2.16.40 | pat.mixed_graph_euler_circuit | 混合图欧拉回路 | 有向边+无向边→欧拉回路判定→网络流定向 |
| 8 | 4.3.43 | pat.generating_function_dp | 生成函数与DP | 多项式系数对应方案数，卷积=背包合并 |

### P2 — 可进入 patterns_batch4 或后续 batch（12 个）

| # | item_id | Pattern ID | 名称 | 备注 |
|:-:|:--------|:-----------|:-----|:-----|
| 1 | 2.2.23 | pat.binary_search_answer | 二分答案判定 | ⚠️ 需检查 ready patterns 中是否已有覆盖 |
| 2 | 2.3.28 | pat.interval_scheduling_extended | 区间调度进阶 | ⚠️ 需与 pat.greedy_interval_scheduling 边界说明 |
| 3 | 2.6.10 | pat.interval_point_selection | 区间选点问题 | ⚠️ 与区间调度互补，需边界说明 |
| 4 | 2.8.177 | pat.dp_on_automaton | DP与自动机(KMP自动机DP) | ⚠️ 与 pat.dp_state_machine 边界说明 |
| 5 | 2.8.200 | pat.knapsack_counting | 背包总方案数 | ⚠️ 需检查与 pat.counting_knapsack 的关系 |
| 6 | 2.9.40 | pat.super_source_sink_modeling | 超级源点与超级汇点 | ⚠️ 与 pat.network_flow_modeling 边界说明 |
| 7 | 2.9.42 | pat.difference_constraints_advanced | 差分约束进阶 | ⚠️ 与 pat.shortest_path_modeling 边界说明 |
| 8 | 2.9.43 | pat.state_compression_graph | 状态压缩图 | ⚠️ 与 pat.state_compression_modeling 建议合并 |
| 9 | 2.9.133 | pat.binary_lifting_pattern | 倍增思想 | |
| 10 | 2.9.135 | pat.prefix_sum_difference_extended | 前缀和与差分扩展 | ⚠️ 与 pat.fenwick_prefix_maintenance 边界说明 |
| 11 | 2.9.139 | pat.state_compression_modeling | 状态压缩建模 | ⚠️ 与 2.9.43 和 pat.bitmask_dp_pattern 边界说明 |
| 12 | 2.9.144 | pat.matrix_modeling_pattern | 矩阵乘法建模 | ⚠️ 与 2.8.189 (pat.matrix_exponentiation_dp) 建议合并 |

### merge_with_existing（9 个）

| # | item_id | 名称 | 合并目标 Pattern | 来源 |
|:-:|:--------|:-----|:-----------------|:----:|
| 1 | 2.8.175 | 容斥DP | pat.inclusion_exclusion_counting | ready |
| 2 | 2.9.41 | 分层图 | pat.layered_graph_modeling | batch2 |
| 3 | 2.9.126 | 离线处理建模 | pat.offline_query_pattern | ready |
| 4 | 2.9.127 | 在线转离线 | pat.offline_query_pattern | ready |
| 5 | 2.9.134 | 差分约束建模 | pat.shortest_path_modeling | ready |
| 6 | 2.9.137 | 离散化建模 | pat.coordinate_sweep_compression | ready |
| 7 | 2.9.142 | 网络流建模 | pat.network_flow_modeling | ready |
| 8 | 2.16.38 | 最大权闭合子图进阶 | pat.min_cut_selection | ready |
| 9 | 2.21.173 | DAG最小路径覆盖 | pat.path_cover_modeling | batch2 |

### defer — 不适合模式库（65 个）

#### 通用元方法论（30 个，2.9.121-2.9.150 中除 P1/P2 外的部分）

这些是"如何思考建模"的方法论条目，不属于具体题型模式：

| range | 内容 |
|:------|:-----|
| 2.9.121-2.9.125 | 最优化/决策/计数/构造/交互 问题建模 |
| 2.9.128-2.9.132 | 分治/增量/等效转换/正难则反/二分答案 建模 |
| 2.9.140-2.9.150 | 贪心证明/图论建模/博弈论/概率期望/组合数学/数论/数据范围/特殊性质/暴力 建模 |

#### 编程风格与调试（21 个）

| range | 内容 |
|:------|:-----|
| 2.9.106-2.9.120 | 代码组织/调试技巧/代码复用/STL技巧/编码规范 |
| 2.18.18-2.18.24 | print调试法/静态分析/二分定位bug/复原测试/断言/边界测试/随机测试 |

#### 比赛策略（7 个）

| items | 内容 |
|:------|:-----|
| 2.9.154-2.9.163 | 时间分配/题目难度识别/暴力与正解权衡/部分分/对拍/猜结论/复盘 |

#### STL/编程惯用法（2 个）

| items | 内容 |
|:------|:-----|
| 2.9.55, 2.9.69 | STL unique/remove/erase 惯用法、copy/transform 惯用法 |

#### 实现技术/技巧（7 个）

| items | 内容 |
|:------|:-----|
| 2.2.25-2.2.26 | 实数二分精度、答案判定 |
| 2.5.21, 2.5.23 | 搜索剪枝、DFS序回溯 |
| 3.3.29, 3.5.24, 3.13.228 | 分块打表、边权转点权、bitset优化 |

#### 过于模糊/非题型（5 个）

| items | 原因 |
|:------|:-----|
| 2.1.76 | 递归转迭代是编程技巧 |
| 2.3.27 | 交换论证是证明技巧 |
| 2.3.29 | 开闭区间是实现细节 |
| 2.8.183-2.8.185 | DP状态压缩/设计/降维是元方法论 |
| 2.8.187-2.8.188 | 线段树/树状数组优化DP是实现技术 |
| 2.8.191 | 双状态DP描述模糊 |
| 2.8.201 | 与 2.8.185 重复 |
| 2.10.59-2.10.63 | 字符串建模/哈希/Trie建图是实现技术 |
| 2.16.41 | 网络流动态加边是 core_concept |
| 2.21.183 | 最大密度子图(参数搜索) 与 2.16.39 重复 |

---

## 生成时需合并的候选对

在正式生成 patterns_batch4 之前，以下候选对建议合并为一个 pattern：

| 候选 A | 候选 B | 建议合并为 | 理由 |
|:-------|:-------|:----------|:-----|
| 2.8.189 DP矩阵乘法优化 | 2.9.144 矩阵乘法建模 | pat.matrix_exponentiation_dp | 同一模式的不同表述 |
| 2.9.43 状态压缩图 | 2.9.139 状态压缩建模 | pat.state_compression_modeling | 同一模式的不同层面 |
| 2.16.39 最大密度子图 | 2.21.183 最大密度子图(参数搜索) | pat.max_density_subgraph | 2.21.183 已 defer，内容合并到 2.16.39 |

合并后有效 batch4 候选总数：**20 → 17**

---

## 与已有 Patterns 的关系

### 与 ready patterns (83) 的关系

| 检查 | 结果 |
|:-----|:----:|
| 直接重复（已 merge_with_existing） | 6 个 (pat.inclusion_exclusion, offline_query, shortest_path, coordinate_sweep, network_flow, min_cut) |
| 语义重叠需 boundary_note | 多个 (binary_search_answer vs ? , interval_scheduling vs greedy_interval, etc.) |
| 完全无关 | 其余 |

### 与 batch2 patterns (13) 的关系

| 检查 | 结果 |
|:-----|:----:|
| 直接重复（已 merge_with_existing） | 2 个 (pat.layered_graph_modeling, pat.path_cover_modeling) |
| 语义重叠 | pat.knapsack_counting 可能与某个 batch2 pattern 相关 |

### 与 batch3 drafts (3) 的关系

| 检查 | 结果 |
|:-----|:----:|
| 与 pat.dominance_counting 重叠 | ❌ 无 |
| 与 pat.mobius_inversion_application 重叠 | ❌ 无 |
| 与 pat.euler_function_application 重叠 | ❌ 无 |
| 潜在相关 | pat.generating_function_dp (4.3.43) 与数论函数生成函数有交汇 |

---

## 推荐 Batch4 生成策略

### 当前状态

```
Batch1 Ready:    83 个 ← ready
Batch2 Generated: 13 个 ← done
Batch3 Drafts:     3 个 ← pending (需等 Batch4 full49 完成)
Stage3G P1:        8 个 ← 本次 triage
Stage3G P2:       12 个 ← 本次 triage (含 3 对需合并)
```

### 推荐计划

| 阶段 | 内容 | 数量 |
|:-----|:-----|:----:|
| **Step 1** | 等待 Stage3F Batch4 full49 完成 | — |
| **Step 2** | 生成 patterns_batch3（3 个） | 3 |
| **Step 3** | 生成 patterns_batch4 优先级 P1（8 个） | 8 |
| **Step 4** | 合并后生成 patterns_batch4 优先级 P2（9-10 个） | ~9 |
| **Step 5** | 所有 defer / merge 候选作为知识回顾记录 | 74 |

### 建议合并 + 生成顺序（合并后 17 个）

| 优先级 | 数量 | Pattern IDs |
|:------:|:----:|:------------|
| P1 | 8 | congruence_shortest_path, parallel_binary_search, mixed_graph_euler, max_density_subgraph, generating_function_dp, matrix_exponentiation_dp, two_pointer_sliding_window, meet_in_the_middle |
| P2 | 9 | binary_search_answer, interval_scheduling_extended, interval_point_selection, dp_on_automaton, knapsack_counting, super_source_sink, difference_constraints_advanced, state_compression_modeling, binary_lifting_pattern, prefix_sum_difference_extended |

*注：P2 中 2.9.43 与 2.9.139 合并、2.9.144 与 2.8.189 合并后减少 2 个*

---

## 声明

| 约束 | 结果 |
|:-----|:----:|
| ✅ 候选总数 | **94** |
| ✅ create_new_draft_later | **20** |
| ✅ merge_with_existing | **9** |
| ✅ defer | **65** |
| ✅ manual_review | **0** |
| ❌ 是否建议现在生成正式 patterns | **否** |
| ❌ 是否修改主图谱 | **否** |
| ❌ 是否修改已有 patterns | **否** |
| ❌ 是否修改 batch3 drafts | **否** |
| ✅ 建议等 Batch3 + Stage3F Batch4 full49 完成后统一生成 | **是** |

---

*Triage 执行完毕 | 94 个候选全部分级 | 0 个 manual_review | 主图谱和已有 patterns 均未修改*
