# Stage3F Batch2 静态候选计划报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T13:20:00.000Z
- **任务**: Stage3F Batch2 静态候选计划（不做动态预审）
- **主图谱状态**: 未修改 (item_count=1661, section_count=65)

## 1. 候选池状态

| 指标 | 数量 |
|------|------|
| **标准化候选池总计** | **129** |
| **Batch1 已使用** | **20** |
| **Batch2 可用余量** | **109** |
| **Batch2 入选** | **20** |

## 2. Batch2 候选列表 (20 个)

### 2.10 字符串算法（6 个）

| # | candidate_id | 名称 | Risk | 来源 |
|---|-------------|------|------|------|
| 1 | cand.string.z_algorithm.basic | Z算法基础 | yellow | external_b2 |
| 2 | cand.string.z_algorithm.pattern_matching | Z算法模式匹配应用 | yellow | external_b2 |
| 3 | cand.string.ex_kmp.basic | 扩展KMP算法基础 | yellow | external_b2 |
| 4 | cand.string.kmp_automaton.basic | KMP自动机基础 | yellow | external_b2 |
| 5 | cand.string.ac_automaton.applications | AC自动机高级应用 | yellow | external_b2 |
| 6 | cand.string.ac_failure_tree.analysis | AC自动机失败树分析 | yellow | external_b2 |

### 4.1 整数与数论基础（5 个）

| # | candidate_id | 名称 | Risk | 来源 |
|---|-------------|------|------|------|
| 1 | cand.math.prime_testing.miller_rabin | Miller-Rabin素数测试 | yellow | external_b2 |
| 2 | cand.math.prime_factorization.pollard_rho | Pollard Rho分解 | yellow | external_b2 |
| 3 | cand.math.primitive_root.basic | 原根基础 | yellow | external_b2 |
| 4 | cand.math.discrete_log.bsgs | BSGS离散对数 | yellow | external_b2 |
| 5 | cand.math.discrete_log.exbsgs | 扩展BSGS | yellow | external_b2 |

### 3.8 字符串结构（3 个）

| # | candidate_id | 名称 | Risk | 来源 |
|---|-------------|------|------|------|
| 1 | cand.string.lcp_rmq.optimization | LCP RMQ优化 | yellow | external_b2 |
| 2 | cand.string.sam_parent_tree.structure | SAM父树结构 | yellow | external_b2 |
| 3 | cand.string.eertree.construction | 回文树Eertree构建 | yellow | external_b2 |

### 2.8 动态规划（0 个）

| # | candidate_id | 名称 | Risk | 来源 |
|---|-------------|------|------|------|

### 其他 Section（6 个）

| # | Section | candidate_id | 名称 | Risk | 来源 |
|---|---------|-------------|------|------|------|
| 1 | 4.3 | cand.math.combinatorial.lucas | Lucas定理 | yellow | external_b2 |
| 2 | 4.3 | cand.math.combinatorial.catalan | Catalan数 | yellow | external_b2 |
| 3 | 4.9 | cand.math.dirichlet_convolution.basic | 狄利克雷卷积基础 | yellow | external_b2 |
| 4 | 4.9 | cand.math.mobius_inversion.applications | 莫比乌斯反演应用 | yellow | external_b2 |
| 5 | 2.18 | cand.dp.optimization.monotone_queue | 单调队列优化 | yellow | external_b2 |
| 6 | 2.18 | cand.dp.optimization.monotone_queue_sliding | 滑动窗口DP | yellow | external_b2 |

## 3. 分布统计

### 按来源

| 来源 | 数量 |
|------|------|
| external_b2 | 20 |

### 按 Section

| Section | 名称 | 数量 |
|---------|------|------|
| 2.10 | 字符串算法 | 6 |
| 2.18 | 综合高级技巧 | 2 |
| 3.8 | 字符串结构 | 3 |
| 4.1 | 整数与数论基础 | 5 |
| 4.3 | 计数与组合 | 2 |
| 4.9 | 高级数学与群论 | 2 |

### 按 Risk

| Risk | 数量 |
|------|------|
| yellow | 20 |

## 4. 排除候选说明

| 排除原因 | 数量 |
|---------|------|
| Batch1 已使用 | 20 |
| section_capacity_limited（2.21/3.13 延后） | 46 |
| not_in_top_20（优先薄弱区） | 43 |

## 5. 潜在风险标记

| 风险类型 | 数量 |
|---------|------|
| 可能需要 dependency cleanup | 20 |
| 可能需要同步 problem_patterns | 0 |

## 6. 推荐结论

| 项目 | 结果 |
|------|------|
| **建议后续做动态预审** | **是** |
| **主图谱是否修改** | **否** |
| **是否生成正式 Batch2** | **否**（只是静态计划） |

## 7. 与 Batch1 的对比

| 维度 | Batch1 | Batch2 |
|------|--------|--------|
| 主要来源 | carry_over + reserve + B2 | B2 (薄弱区优先) |
| Section 重点 | 2.8(9个) / 3.13(4个) / 3.8(3个) | 2.10 / 4.1 / 3.8 / 2.8 |
| DP 数量 | 9 个 | 少量补充 |
| 数据结构 | 4 个 (3.13) | 0 个（延后） |
| 数学专题 | 3 个 | 数论+组合+高级数学 |

## 8. 下一步

1. ✅ Stage3F Batch2 静态候选计划完成（20 个候选）
2. 🔲 执行 Stage3F Batch2 动态预审
3. 🔲 1号线程执行 Merge
4. 🔲 2号线程执行 Review

---

*本计划不修改主图谱，不生成正式合并批次。*
