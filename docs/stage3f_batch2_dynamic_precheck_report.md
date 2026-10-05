# Stage3F Batch2 动态预审报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T13:30:00.000Z
- **任务**: Stage3F Batch2 动态预审
- **主图谱状态**: 未修改

## 1. 主图谱状态

| 检查项 | 实际值 | 预期值 | 结果 |
|--------|--------|--------|------|
| item_count | 1661 | 1661 | ✓ |
| section_count | 65 | 65 | ✓ |
| validate-only passed | True | true | ✓ |
| dangling_refs | 0 | 0 | ✓ |
| direct_pre_cycle | None | null | ✓ |
| report_matches_json | True | true | ✓ |
| product_metadata_validation.passed | True | true | ✓ |
| Stage3F Batch1 Fix Lite | 已完成 | - | ✓ |

## 2. 候选来源

| 来源 | 计划数 | 通过数 |
|------|--------|--------|
| external_b2 | 20 | 20 |
| **总计** | 20 | **20** |

## 3. 排除候选

### 已合并候选
无（全部 candidate_id 不在历史 mapping 中）

### 名称/别名重复
无

## 4. 重点候选近重复排查

| candidate_id | name | 图谱相似 item | 结论 |
|-------------|------|--------------|------|
| cand.math.combinatorial.lucas | Lucas定理 | Lucas, 扩展Lucas定理 | 可区分, 建议保留但使用时注意语义边界 |
| cand.dp.optimization.monotone_queue | 单调队列优化 | 单调队列优化 DP, 单调队列优化多重背包, 单调队列 | 可区分, 建议保留但使用时注意语义边界 |
| cand.dp.optimization.monotone_queue_sliding | 滑动窗口DP | 滑动窗口 | 可区分, 建议保留但使用时注意语义边界 |

## 5. 入选候选列表 (20)

| # | Section | candidate_id | 名称 | Risk |
|---|---------|-------------|------|------|
| 1 | 2.10 | cand.string.z_algorithm.basic | Z算法基础 | yellow |
| 2 | 2.10 | cand.string.z_algorithm.pattern_matching | Z算法模式匹配应用 | yellow |
| 3 | 2.10 | cand.string.ex_kmp.basic | 扩展KMP算法基础 | yellow |
| 4 | 2.10 | cand.string.kmp_automaton.basic | KMP自动机基础 | yellow |
| 5 | 2.10 | cand.string.ac_automaton.applications | AC自动机高级应用 | yellow |
| 6 | 2.10 | cand.string.ac_failure_tree.analysis | AC自动机失败树分析 | yellow |
| 7 | 4.1 | cand.math.prime_testing.miller_rabin | Miller-Rabin素数测试 | yellow |
| 8 | 4.1 | cand.math.prime_factorization.pollard_rho | Pollard Rho分解 | yellow |
| 9 | 4.1 | cand.math.primitive_root.basic | 原根基础 | yellow |
| 10 | 4.1 | cand.math.discrete_log.bsgs | BSGS离散对数 | yellow |
| 11 | 4.1 | cand.math.discrete_log.exbsgs | 扩展BSGS | yellow |
| 12 | 3.8 | cand.string.lcp_rmq.optimization | LCP RMQ优化 | yellow |
| 13 | 3.8 | cand.string.sam_parent_tree.structure | SAM父树结构 | yellow |
| 14 | 3.8 | cand.string.eertree.construction | 回文树Eertree构建 | yellow |
| 15 | 4.3 | cand.math.combinatorial.lucas | Lucas定理 | yellow |
| 16 | 4.3 | cand.math.combinatorial.catalan | Catalan数 | yellow |
| 17 | 4.9 | cand.math.dirichlet_convolution.basic | 狄利克雷卷积基础 | yellow |
| 18 | 4.9 | cand.math.mobius_inversion.applications | 莫比乌斯反演应用 | yellow |
| 19 | 2.18 | cand.dp.optimization.monotone_queue | 单调队列优化 | yellow |
| 20 | 2.18 | cand.dp.optimization.monotone_queue_sliding | 滑动窗口DP | yellow |

## 6. Section 分布

| Section | 名称 | 数量 |
|---------|------|------|
| 2.10 | 字符串算法 | 6 |
| 2.18 | 综合高级技巧 | 2 |
| 3.8 | 字符串结构 | 3 |
| 4.1 | 整数与数论基础 | 5 |
| 4.3 | 计数与组合 | 2 |
| 4.9 | 高级数学与群论 | 2 |

## 7. 依赖检查

| 检查项 | 结果 |
|--------|------|
| 是否存在 section ref 依赖 | 否 |
| dependency_cleanup_required | 否 |
| 是否存在候选依赖环 | 否 |
| 是否需要新 section | 否 |

## 8. 推荐结论

| 项目 | 结果 |
|------|------|
| **recommendation** | **ready_for_1号线程_merge** |
| **recommended_merge_count** | **20** |
| **是否建议交给 1号合并** | 是 |
| **主图谱是否修改** | **否** |

## 9. 下一步

1. ✅ 动态预审通过，建议 1号线程合并全部 20 个候选
2. 1号线程执行 Merge
3. validate-only 验证 (item_count = 1681)
4. 2号线程执行 Review

---

*本预审不修改主图谱，仅输出动态预审结果。*
