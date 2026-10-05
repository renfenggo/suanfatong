# Stage3G full400 全量合并可行性审计报告

**生成时间**: 2026-05-25T14:28:25.100857+00:00
**审计脚本**: stage3g_full400_audit.py

## 1. 总体结论

| 指标 | 值 |
|------|-----|
| 候选总数 | 400 |
| 可以直接合并 | 363 |
| 需要依赖清理 | 272 |
| 精确重复 | 2 |
| 高度近似 | 0 |
| 需要人工复核 | 0 |
| red候选 | 20 |
| low confidence | 103 |
| 建议 | **needs_cleanup_before_full400_merge** |
| 建议合并数 | 363 |
| 修改主图谱 | 否 |
| 执行合并 | 否 |

## 2. 阻塞项列表

- ❌ exact_duplicate_count=2
- ❌ needs_new_section=true
- ❌ self_ref_dependencies=1
- ❌ dangling_refs=272
- ❌ red_candidates=20 (建议暂缓)

## 3. 各主题分布与风险

| Theme | 候选数 | green | yellow | medium | red |
|-------|--------|-------|--------|--------|-----|
| C++语法高级细节 | 25 | 13 | 8 | 2 | 2 |
| STL与常用库细节 | 30 | 16 | 14 | 0 | 0 |
| 信奥数学 | 40 | 9 | 19 | 8 | 4 |
| 动态规划专题 | 45 | 17 | 18 | 6 | 4 |
| 图论专题 | 55 | 18 | 21 | 14 | 2 |
| 基础算法扩展 | 35 | 20 | 11 | 3 | 1 |
| 字符串专题 | 35 | 15 | 14 | 4 | 2 |
| 数据结构专题 | 50 | 13 | 23 | 10 | 4 |
| 比赛相关知识 | 15 | 8 | 7 | 0 | 0 |
| 编程技巧 | 25 | 16 | 8 | 0 | 1 |
| 调试方法 | 15 | 10 | 5 | 0 | 0 |
| 题型建模方法 | 30 | 10 | 20 | 0 | 0 |

## 4. 依赖质量

| 指标 | 值 |
|------|-----|
| direct_pre 总数 | 1598 |
| 平均每个候选 | 4.0 |
| 最大 direct_pre | 5 |
| 无法解析的 pre | 457 |
| section ref 数量 | 0 |
| self ref 数量 | 1 |
| 悬空引用数量 | 272 |
| 候选依赖环 | 否 |

## 5. Section 分布

| Section | 名称 | 候选数 |
|---------|------|--------|
| 2.1 | 基础算法思想 | 17 |
| 2.10 | 字符串算法 | 21 |
| 2.11 | 位运算与状态压缩 | 4 |
| 2.12 | 数值与矩阵专题 | 3 |
| 2.14 | 树上算法 | 7 |
| 2.15 | 连通分量与特殊图 | 4 |
| 2.16 | 二分图、匹配与网络流 | 9 |
| 2.17 | 线性代数与插值专题 | 5 |
| 2.2 | 排序与顺序统计 | 4 |
| 2.21 | 高级图论扩展 | 17 |
| 2.3 | 二分与答案搜索 | 3 |
| 2.4 | 前缀、差分、离散化、分块 | 4 |
| 2.5 | 双指针与滑动窗口 | 7 |
| 2.8 | 动态规划 | 45 |
| 2.9 | 图基础与遍历 | 129 |
| 3.1 | 线性结构 | 1 |
| 3.13 | 高级数据结构扩展 | 26 |
| 3.2 | 栈与队列 | 4 |
| 3.3 | 集合与映射 | 7 |
| 3.5 | 堆 | 5 |
| 3.8 | 字符串结构 | 21 |
| 3.9 | 图存储结构 | 2 |
| 4.1 | 整数与数论基础 | 16 |
| 4.16 | Section 4.16 | 15 |
| 4.3 | 计数与组合 | 15 |
| 4.4 | 离散数学基础 | 2 |
| 4.5 | 图与树的数学基础 | 3 |
| 4.6 | 概率与期望 | 4 |

## 6. Merge Priority 分布

| Priority | 数量 | 含义 |
|----------|------|------|
| now | 165 | green + high confidence，立即合并 |
| soon | 132 | green/yellow + high/medium，早期合并 |
| later | 47 | medium/low，后期合并 |
| defer | 56 | red/low confidence，暂缓 |

## 7. 是否建议一次合并 400

❌ **不建议一次合并 400**。阻塞项如下：

- exact_duplicate_count=2
- needs_new_section=true
- self_ref_dependencies=1
- dangling_refs=272
- red_candidates=20 (建议暂缓)

建议先解决阻塞项，或分批次合并。可直接合并的候选数：363。

## 8. 是否导致依赖过密

✅ direct_pre 平均 4.0，最大 5，不会造成依赖过密。

## 9. Problem Pattern 候选

共 98 个候选标记为 problem_pattern（仅标记，不正式生成模式）：

| 候选 | Theme | Risk |
|------|-------|------|
| 最小生成树进阶：生成树计数 | 图论专题 | medium |
| LCA进阶：LCA与树上差分 | 图论专题 | green |
| 最短路进阶：同余最短路 | 图论专题 | yellow |
| 最大流建模：最大权闭合子图进阶 | 图论专题 | yellow |
| 最大流建模：最大密度子图 | 图论专题 | yellow |
| 最大流建模：混合图欧拉回路 | 图论专题 | medium |
| SCC/DAG进阶：DAG最小路径覆盖 | 图论专题 | yellow |
| SCC/DAG进阶：可达性统计(Bitset优化) | 图论专题 | yellow |
| 图论专题：最大密度子图(参数搜索) | 图论专题 | medium |
| 分块进阶：分块打表 | 数据结构专题 | yellow |
| 树链剖分进阶：边权转点权 | 数据结构专题 | green |
| 集合进阶：bitset优化 | 数据结构专题 | yellow |
| 概率DP进阶：期望DP与高斯消元 | 动态规划专题 | yellow |
| 计数DP：容斥DP | 动态规划专题 | yellow |
| DP进阶：DP与自动机(KMP自动机DP) | 动态规划专题 | yellow |
| DP进阶：DP状态压缩与记忆化搜索 | 动态规划专题 | green |
| DP进阶：DP状态设计技巧 | 动态规划专题 | green |
| DP进阶：高维DP降维 | 动态规划专题 | yellow |
| 数据结构优化DP进阶：线段树优化 | 动态规划专题 | green |
| 数据结构优化DP进阶：树状数组优化 | 动态规划专题 | green |
| DP进阶：DP与矩阵乘法优化 | 动态规划专题 | green |
| 双状态DP进阶 | 动态规划专题 | green |
| 多项式：生成函数与DP | 信奥数学 | yellow |
| 概率论进阶：期望线性性应用 | 信奥数学 | green |
| 二分进阶：二分答案判定 | 基础算法扩展 | green |
| 二分进阶：实数二分精度处理 | 基础算法扩展 | green |
| 贪心进阶：交换论证法 | 基础算法扩展 | yellow |
| 随机化算法：随机哈希 | 基础算法扩展 | green |
| 搜索进阶：剪枝技巧 | 基础算法扩展 | green |
| 递归进阶：递归转迭代 | 基础算法扩展 | green |
| ... (68 more) | | |

## 11. 建议修复方案

- **exact_duplicate**: `整体二分` → remove_from_pool
  - 候选 "整体二分" 与已有节点重复，应从候选池移除
- **exact_duplicate**: `笛卡尔树` → remove_from_pool
  - 候选 "笛卡尔树" 与已有节点重复，应从候选池移除
- **needs_new_section**: `调试基础：GDB入门` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试基础：GDB进阶命令` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试基础：print调试法` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试基础：静态分析` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试技巧：二分定位bug` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试技巧：复原测试法` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试技巧：断言辅助调试` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试技巧：边界测试` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试技巧：随机测试` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试场景：RE(运行时错误)排查` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试场景：TLE(超时)优化` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试场景：WA(答案错误)排查` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试场景：MLE(内存超限)排查` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试工具：Valgrind内存检测` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **needs_new_section**: `调试工具：AddressSanitizer` → reassign_section
  - Section 4.16 不存在，建议重新分配到 2.9 (C++与STL) 或其他已有 section
  - 建议 section: 2.9
- **self_reference**: `笛卡尔树` → remove_self_from_pre
  - direct_pre_name_suggestion 中包含自身，需移除

## 12. 高危重复风险主题

- KMP / 扩展KMP / Z算法 / Border树
- Lucas / Miller-Rabin / BSGS / 欧拉函数 / 莫比乌斯反演
- 单调队列优化 / 斜率优化 / 状压DP / 概率DP
- 线段树 Split / Merge / 分裂 / 合并 / Beats
- SCC DAG / 动态连通性 / 缩点 / DAG
- 线性基 Range / Merge / Deletion / Rollback

---
*本报告由 stage3g_full400_audit.py 自动生成*
*不修改主图谱，不执行合并*
