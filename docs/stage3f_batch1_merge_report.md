# Stage3F Batch1 Merge Report

**生成时间**: 2026-05-25 12:30:01
**执行者**: 1号线程 / GLM5
**依据**: data/stage3f_batch1_dynamic_precheck.json (recommendation=ready_for_1号线程_merge)

## 1. 前置条件

| 条件 | 结果 |
|------|------|
| item_count = 1641 | ✅ |
| section_count = 65 | ✅ |
| selected_candidates = 20 | ✅ |
| recommendation = ready_for_1号线程_merge | ✅ |
| recommended_merge_count = 20 | ✅ |
| dependency_cleanup_required = false | ✅ |
| candidate_dependency_cycle = false | ✅ |
| needs_new_section = false | ✅ |
| section_ref_dependencies = [] | ✅ |
| no excluded_already_merged | ✅ |
| no excluded_duplicate | ✅ |

## 2. 执行摘要

| 项目 | 数值 |
|------|:----:|
| 备份是否成功 | ✅ backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch1.json |
| 合并前 item_count | 1641 |
| 合并后 item_count | 1661 |
| 实际新增 item 数 | 20 |
| 新增 section 数 | 0 |
| direct_pre 无 section id | ✅ 是 |
| 悬空引用 = 0 | ✅ 是 |
| direct_pre 无环 | ✅ 是 |
| resolved_pre_mismatches = 0 | ✅ 是 |
| product_metadata_validation passed | ✅ 是 |
| report_matches_json | ✅ True |
| validation passed | ✅ True |
| 是否生成 rollback plan | ✅ 是 |

## 3. Section 分布

| Section | 名称 | 新增数量 |
|---------|------|:--------:|
| 2.17 | 线性代数与插值专题 | 1 |
| 2.18 | 综合高级技巧专题 | 1 |
| 2.8 | 动态规划 | 9 |
| 3.13 | 高级数据结构扩展 | 4 |
| 3.8 | 字符串结构 | 3 |
| 4.3 | 计数与组合 | 1 |
| 4.9 | 高级数学与群论 | 1 |
| **总计** | - | **20** |

## 4. 新增节点列表

| item_id | 名称 | section | direct_pre | review_priority |
|---------|------|:-------:|:----------:|:--------------:|
| 3.13.182 | Multidimensional: Dominance Counting | 3.13 | 3.7.1,3.7.2 | B |
| 3.13.183 | Merge Sort Tree: Memory Optimization | 3.13 | 3.7.2,1.3.1 | B |
| 3.13.184 | Merge Sort Tree: Offline Inversion | 3.13 | 3.7.2,1.3.1 | B |
| 3.13.185 | Merge Sort Tree: Persistent Variant | 3.13 | 3.7.2,1.3.1,3.11.1 | B |
| 2.8.134 | 复杂数位DP | 2.8 | 2.8.110,2.8.20 | B |
| 2.8.135 | 换根DP | 2.8 | 2.8.27,2.8.104 | B |
| 2.8.136 | 轮廓DP基础 | 2.8 | 2.8.114,2.8.41 | B |
| 2.8.137 | 插头DP基础 | 2.8 | 2.8.119,2.8.114 | B |
| 3.8.9 | 后缀数组SA-IS算法 | 3.8 | 3.8.3 | B |
| 3.8.10 | 广义SAM构建 | 3.8 | 3.8.4 | B |
| 3.8.11 | 后缀树Ukkonen算法 | 3.8 | 3.8.7,3.8.8 | B |
| 2.18.9 | 斜率优化高级 | 2.18 | 2.8.98,2.18.4 | B |
| 2.17.20 | Berlekamp-Massey算法 | 2.17 | 2.17.11 | B |
| 4.3.32 | 扩展Lucas定理 | 4.3 | 4.3.15,4.3.21 | B |
| 4.9.3 | Min_25筛 | 4.9 | 4.9.1,4.9.2 | B |
| 2.8.138 | 数位DP基础 | 2.8 | 2.8.20,2.8.110 | B |
| 2.8.139 | 树DP基础 | 2.8 | 2.8.27 | B |
| 2.8.140 | 树的直径DP | 2.8 | 2.8.27,2.8.105 | B |
| 2.8.141 | 树的重心DP | 2.8 | 2.8.27 | B |
| 2.8.142 | 拓扑排序DP | 2.8 | 2.8.23,2.8.95 | B |

## 5. 验证结果

| 检查项 | 期望 | 实际 | 状态 |
|--------|:----:|:----:|:----:|
| item_count | 1661 | 1661 | ✅ |
| expected_item_count | 1661 | 1661 | ✅ |
| section_count | 65 | 65 | ✅ |
| dangling_refs | 0 | 0 | ✅ |
| direct_pre_cycle | None | None | ✅ |
| resolved_pre_mismatches | 0 | 0 | ✅ |
| product_metadata_validation | passed | passed | ✅ |
| report_matches_json | true | true | ✅ |
| passed | true | true | ✅ |

## 6. 结论

**✅ Stage3F Batch1 Merge 成功！主图谱已从 1641 升级到 1661**

- 新增 20 个节点，分布在 7 个 section
- 基于 Stage3F Batch1 动态预审 (recommendation=ready_for_1号线程_merge)
- 所有 9 项验证检查通过
- 未继续 Stage3F Batch2