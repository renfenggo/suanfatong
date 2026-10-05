# Problem Patterns 正式生成准备清单 — Stage3G 之后

## 总览

| 指标 | 数值 |
|:-----|:---:|
| 主图谱 item_count | 2165 |
| 主图谱 section_count | 65 |
| validate-only passed | ✅ |
| 候选总数（可正式生成） | 23 |
| **Batch3 ready drafts** | **3** |
| **Stage3G P1 候选** | **8** |
| **Stage3G P2 候选（合并后）** | **9** |
| merge_with_existing（不新生成） | 9 |
| defer（不生成） | 65 |
| **建议立即生成** | **0（需等 blocker 清除）** |
| **推荐首轮生成数量** | **方案 B: 11 个** |

---

## 第一组：patterns_batch3 既有 ready 候选（3 个）

### ✅ ALL READY — 已通过全部检查

| # | Pattern ID | 名称 | 来源 | 领域 |
|:-:|:-----------|:-----|:-----|:-----|
| 1 | pat.dominance_counting | 多维支配关系计数 | Stage3F Batch1 (3.13.182) | 计数 / 多维偏序 |
| 2 | pat.mobius_inversion_application | 莫比乌斯反演应用 | Stage3F Batch2 (4.9.5) | 计数 / 数论反演 |
| 3 | pat.euler_function_application | 欧拉函数应用 | Stage3F Batch3 (4.9.6) | 计数 / 积性函数 |

### Readiness 检查（CR-01 ~ CR-08）

| Pattern | draft 完整 | 无 ready 重复 | 无 batch2 重复 | required_items 可映射 | related_items 可映射 | boundary_note | 无需人工复查 |
|:--------|:---------:|:-----------:|:------------:|:-------------------:|:-------------------:|:-----------:|:-----------:|
| dominance_counting | ✅ | ✅ | ✅ | ✅ [3.7.1,3.7.2] | ✅ [3.13.181,3.13.179,3.13.180] | ✅ | ✅ |
| mobius_inversion | ✅ | ✅ | ✅ | ✅ [4.9.2,4.3.10] | ✅ [4.9.4,4.9.6,4.1.5] | ✅ | ✅ |
| euler_function | ✅ | ✅ | ✅ | ✅ [4.1.10,4.1.11] | ✅ [4.9.5,1.7.25,4.1.5] | ✅ | ✅ |

**结论**：3 个全部 READY，可直接合成 patterns_batch3.json。

---

## 第二组：Stage3G P1 优先候选（8 个）

### ⚠️ NEEDS DRAFT PREVIEW — triage 已通过，需准备 draft

| # | Pattern ID | 名称 | source_item | 领域 |
|:-:|:-----------|:-----|:------------|:-----|
| 1 | pat.congruence_shortest_path_modeling | 同余最短路 | 2.15.19 | 图论 / 数论建模 |
| 2 | pat.parallel_binary_search | 整体二分应用 | 2.4.52 | 分治 / 离线查询 |
| 3 | pat.two_pointer_sliding_window | 双指针/滑动窗口建模 | 2.9.136 | 基础算法 / 线性扫描 |
| 4 | pat.meet_in_the_middle | 折半搜索 | 2.9.138 | 搜索 / 枚举优化 |
| 5 | pat.max_density_subgraph | 最大密度子图 | 2.16.39 | 图论 / 网络流建模 |
| 6 | pat.mixed_graph_euler_circuit | 混合图欧拉回路 | 2.16.40 | 图论 / 网络流建模 |
| 7 | pat.matrix_exponentiation_dp | DP与矩阵乘法优化 | 2.8.189 | DP优化 / 线性代数 |
| 8 | pat.generating_function_dp | 生成函数与DP | 4.3.43 | 组合数学 / 多项式 |

### Readiness 检查

| Pattern | triage 通过 | boundary_note 需求 | 与 ready 重复 | 与 batch2 重复 | 与 batch3 重复 |
|:--------|:---------:|:-----------------:|:-----------:|:------------:|:-----------:|
| congruence_shortest_path | ✅ | ⚠️ 需 (vs pat.shortest_path_modeling) | ❌ | ❌ | ❌ |
| parallel_binary_search | ✅ | ⚠️ 需 (vs pat.binary_search_answer) | ❌ | ❌ | ❌ |
| two_pointer_sliding_window | ✅ | ❌ | ❌ | ❌ | ❌ |
| meet_in_the_middle | ✅ | ❌ | ❌ | ❌ | ❌ |
| max_density_subgraph | ✅ | ⚠️ 需 (vs pat.network_flow_modeling) | ❌ | ❌ | ❌ |
| mixed_graph_euler_circuit | ✅ | ⚠️ 需 (vs pat.network_flow_modeling) | ❌ | ❌ | ❌ |
| matrix_exponentiation_dp | ✅ | ⚠️ 需 (合并 2.9.144 + vs pat.dp_matrix_exponentiation) | ❌ | ❌ | ❌ |
| generating_function_dp | ✅ | ⚠️ 需 (vs pat.combinatorial_counting) | ❌ | ❌ | ❌ |

**结论**：8 个全部 triage 通过，无重复，需在正式生成前准备 draft preview（recognition_signals, common_transforms, pitfalls, boundary_note）。

---

## 第三组：Stage3G P2 后续候选（12 → 9）

### 需要处理的 3 组合并

| # | 合并结果 Pattern ID | 源 item | 说明 |
|:-:|:-------------------|:--------|:-----|
| 1 | pat.matrix_exponentiation_dp | 2.8.189 (P1) + 2.9.144 (P2) | 矩阵乘法建模并入 DP矩阵乘法优化 |
| 2 | pat.state_compression_modeling | 2.9.43 (P2) + 2.9.139 (P2) | 状态压缩图与状态压缩建模合并 |
| 3 | pat.max_density_subgraph | 2.16.39 (P1) + 2.21.183 (defer) | 最大密度子图(参数搜索)已 defer |

### 合并后 P2 候选（9 个）

| # | Pattern ID | 名称 | source_item |
|:-:|:-----------|:-----|:------------|
| 1 | pat.binary_search_answer | 二分答案判定 | 2.2.23 |
| 2 | pat.interval_scheduling_extended | 区间调度进阶 | 2.3.28 |
| 3 | pat.interval_point_selection | 区间选点问题 | 2.6.10 |
| 4 | pat.dp_on_automaton | DP与自动机 | 2.8.177 |
| 5 | pat.knapsack_counting | 背包总方案数 | 2.8.200 |
| 6 | pat.super_source_sink_modeling | 超级源汇建模 | 2.9.40 |
| 7 | pat.difference_constraints_advanced | 差分约束进阶 | 2.9.42 |
| 8 | pat.binary_lifting_pattern | 倍增思想 | 2.9.133 |
| 9 | pat.prefix_sum_difference_extended | 前缀和与差分扩展 | 2.9.135 |

**结论**：9 个全部 triage 通过，需在正式生成前准备 draft preview + boundary_note。

---

## merge_with_existing（9 个 — 不生成新 pattern）

| # | source_item | 名称 | 合并到 | target 来源 |
|:-:|:------------|:-----|:-------|:----------:|
| 1 | 2.8.175 | 容斥DP | pat.inclusion_exclusion_counting | ready |
| 2 | 2.9.41 | 分层图 | pat.layered_graph_modeling | batch2 |
| 3 | 2.9.126 | 离线处理建模 | pat.offline_query_pattern | ready |
| 4 | 2.9.127 | 在线转离线 | pat.offline_query_pattern | ready |
| 5 | 2.9.134 | 差分约束建模 | pat.shortest_path_modeling | ready |
| 6 | 2.9.137 | 离散化建模 | pat.coordinate_sweep_compression | ready |
| 7 | 2.9.142 | 网络流建模 | pat.network_flow_modeling | ready |
| 8 | 2.16.38 | 最大权闭合子图进阶 | pat.min_cut_selection | ready |
| 9 | 2.21.173 | DAG最小路径覆盖 | pat.path_cover_modeling | batch2 |

**处理建议**：记录到 target pattern 的 metadata 中（expanded_from / covers 字段），不生成新 pattern。

---

## defer（65 个 — 保留为知识图谱条目）

| 类别 | 数量 | 示例 |
|:-----|:---:|:-----|
| 通用元方法论 | 30 | 最优化/决策/计数/构造/交互/分治/增量/等效转换/正难则反/贪心证明/图论/博弈/概率/组合/数论/数据范围等"建模方法" |
| 编程风格/调试 | 21 | 代码组织/调试技巧/代码复用/STL技巧/命名规范/print调试/静态分析/断言/边界测试/随机测试等 |
| 比赛策略 | 7 | 时间分配/题目难度/暴力权衡/部分分/对拍/猜结论/复盘 |
| STL惯用法 | 2 | unique/remove/erase / copy/transform |
| 实现技术/模糊 | 5+ | 递归转迭代/交换论证/搜索剪枝/分块打表/边权转点权/bitset优化/DP降维等 |

**处理建议**：已在知识图谱中作为独立知识点存在，不生成 pattern。保留 triage 记录作为历史参考。

---

## 三种生成方案

### 方案 A：仅生成 patterns_batch3（3 个）

| 指标 | 值 |
|:-----|:--|
| 数量 | 3 |
| 风险 | 🟢 低 |
| 工作量 | 低（draft 已就绪） |
| 覆盖 | 计数模式 / 多维偏序 + 数论反演 + 积性函数 |

**优点**：最快交付，无需准备新 draft。
**缺点**：仅 3 个 pattern，Stage3G 8 个高价值 P1 候选推迟。

### 方案 B：生成 batch3 + Stage3G P1（11 个）⭐ 推荐

| 指标 | 值 |
|:-----|:--|
| 数量 | 11 (3 batch3 + 8 P1) |
| 风险 | 🟡 中 |
| 工作量 | 中（需为 8 个 P1 准备 draft preview） |
| 覆盖 | 计数 + 图论建模 + DP优化 + 数论建模 + 基础算法 |

模式分布：
```
计数模式 (3):
  pat.dominance_counting          多维支配关系计数
  pat.mobius_inversion_application 莫比乌斯反演应用
  pat.euler_function_application   欧拉函数应用

图论建模 (3):
  pat.congruence_shortest_path_modeling 同余最短路
  pat.max_density_subgraph              最大密度子图
  pat.mixed_graph_euler_circuit         混合图欧拉回路

基础算法 (2):
  pat.two_pointer_sliding_window 双指针/滑动窗口
  pat.meet_in_the_middle         折半搜索

DP优化 / 数学建模 (3):
  pat.parallel_binary_search      整体二分
  pat.matrix_exponentiation_dp    DP矩阵乘法优化
  pat.generating_function_dp      生成函数与DP
```

**优点**：平衡交付速度与覆盖广度，P1 候选信号清晰价值高，与 batch3 不重叠。
**缺点**：需为 8 个 P1 候选准备 draft preview。

### 方案 C：生成 batch3 + P1 + P2（约 20 个）

| 指标 | 值 |
|:-----|:--|
| 数量 | 20 (3 + 8 + 9) |
| 风险 | 🔴 高 |
| 工作量 | 高（需为 17 个新候选准备 draft preview） |
| 覆盖 | 最完整 |

**优点**：一次性完成所有候选，后续无积压。
**缺点**：工作量大，P2 部分候选信号不如 P1 清晰，15-20 个同时生成的质量风险较高。

---

## 推荐结论

### 推荐方案 B

| 阶段 | 内容 | 数量 |
|:-----|:-----|:---:|
| **Phase 1** | 生成 patterns_batch3.json | 3 |
| **Phase 1** | 为 8 个 P1 候选准备 draft preview | 8 |
| **Phase 1** | 生成 patterns_batch4.json | 8 |
| **Phase 2** | 评估 P2 候选 → patterns_batch5 | ~9 |

### 执行前置条件（blockers）

| # | 条件 | 状态 |
|:-:|:-----|:----:|
| 1 | Stage3F Batch4 full49 dependency cleanup (Thread 2) | 🔄 in_progress |
| 2 | 用户发出正式生成指令 | ⏳ pending |

### merge_with_existing 处理

9 个 merge 候选记录到 target pattern 的 metadata（expanded_from / covers 字段），不生成新 pattern。

### defer 处理

65 个 defer 候选中：30 个元方法论 + 21 个编程调试 + 7 个比赛策略 + 其余实现技术。**全部保留在知识图谱中作为独立知识点**，不生成 pattern。triage 记录保留供审计。

---

## 声明

| 约束 | 结果 |
|:-----|:----:|
| ❌ 现在生成正式 patterns | **否** |
| ✅ 建议等 blocker 清除后生成 | **是（推荐方案 B）** |
| ❌ 修改主图谱 | **否** |
| ❌ 修改 patterns_v0_1_ready.json | **否** |
| ❌ 修改 patterns_batch2.json | **否** |
| ❌ 修改 patterns_batch3 草案文件 | **否** |
| ✅ 候选总数 | **23** |
| ✅ 建议首轮生成 | **11（方案 B）** |
| ✅ 建议后续生成 | **9（P2 候选）** |
| ✅ merge_with_existing 记录 | **9（不生成新 pattern）** |
| ✅ defer 保留记录 | **65（保留为知识图谱条目）** |

---

*准备清单整理完毕 | 主图谱和所有已有 patterns 均未修改*
