# Stage3F Batch1 动态预审报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T12:40:00.000Z
- **任务**: Stage3F Batch1 动态预审
- **主图谱状态**: 未修改

## 1. 主图谱状态

| 检查项 | 实际值 | 预期值 | 结果 |
|--------|--------|--------|------|
| item_count | 1641 | 1641 | ✓ |
| section_count | 65 | 65 | ✓ |
| Stage3E | 已完成 | - | ✓ |

## 2. 候选来源

| 来源 | 计划数 | 通过数 |
|------|--------|--------|
| carry_over | 1 | 1 |
| reserve_pool | 3 | 3 |
| external_b2 | 16 | 16 |
| **总计** | 20 | **20** |

## 3. 排除候选

### 已合并候选
无 (全部 candidate_id 不在历史 mapping 中)

### 名称/别名重复
无

## 4. 重点候选近重复排查

| candidate_id | name | 图谱相似 item | 结论 |
|-------------|------|--------------|------|
| cand.dp.digit.basic | 数位DP基础 | 数位DP | 可区分, 建议保留但使用时注意语义边界 |
| cand.dp.tree.diameter | 树的直径DP | 树的直径 | 可区分, 建议保留但使用时注意语义边界 |
| cand.dp.tree.centroid | 树的重心DP | 树的重心 | 可区分, 建议保留但使用时注意语义边界 |
| cand.dp.dag.topological | 拓扑排序DP | 拓扑排序 | 可区分, 建议保留但使用时注意语义边界 |
| cand.string.suffix_array.sa_is | 后缀数组SA-IS算法 | 后缀数组 | 可区分, 建议保留但使用时注意语义边界 |
| cand.math.combinatorial.exlucas | 扩展Lucas定理 | Lucas | 可区分, 建议保留但使用时注意语义边界 |

## 5. 入选候选列表 (20)

| # | 来源 | Section | 名称 | Risk |
|---|------|---------|------|------|
| 1 | carry_over | 3.13 | Multidimensional: Dominance Counting | green |
| 2 | reserve_pool | 3.13 | Merge Sort Tree: Memory Optimization | green |
| 3 | reserve_pool | 3.13 | Merge Sort Tree: Offline Inversion | green |
| 4 | reserve_pool | 3.13 | Merge Sort Tree: Persistent Variant | green |
| 5 | external_b2 | 2.8 | 复杂数位DP | green |
| 6 | external_b2 | 2.8 | 换根DP | green |
| 7 | external_b2 | 2.8 | 轮廓DP基础 | green |
| 8 | external_b2 | 2.8 | 插头DP基础 | green |
| 9 | external_b2 | 3.8 | 后缀数组SA-IS算法 | green |
| 10 | external_b2 | 3.8 | 广义SAM构建 | green |
| 11 | external_b2 | 3.8 | 后缀树Ukkonen算法 | green |
| 12 | external_b2 | 2.18 | 斜率优化高级 | green |
| 13 | external_b2 | 2.17 | Berlekamp-Massey算法 | green |
| 14 | external_b2 | 4.3 | 扩展Lucas定理 | green |
| 15 | external_b2 | 4.9 | Min_25筛 | green |
| 16 | external_b2 | 2.8 | 数位DP基础 | yellow |
| 17 | external_b2 | 2.8 | 树DP基础 | yellow |
| 18 | external_b2 | 2.8 | 树的直径DP | yellow |
| 19 | external_b2 | 2.8 | 树的重心DP | yellow |
| 20 | external_b2 | 2.8 | 拓扑排序DP | yellow |

## 6. Section 分布

| Section | 名称 | 数量 |
|---------|------|------|
| 2.17 | 线性代数 | 1 |
| 2.18 | 综合高级技巧 | 1 |
| 2.8 | 动态规划 | 9 |
| 3.13 | 高级数据结构扩展 | 4 |
| 3.8 | 字符串结构 | 3 |
| 4.3 | 计数与组合 | 1 |
| 4.9 | 高级数学与群论 | 1 |

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
3. validate-only 验证 (item_count = 1661)
4. 2号线程执行 Review

---

*本预审不修改主图谱，仅输出动态预审结果。*
