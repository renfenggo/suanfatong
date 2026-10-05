# Stage3F Batch3 full_40 Merge Report

**生成时间**: 2026-05-25 16:45:15
**执行者**: 1号线程 / GLM5
**依据**: v2 文件 (candidate_plan_v2 + dynamic_precheck_v2 + dependency_cleanup_plan)

## 1. 基本信息

| 项目 | 值 |
|------|-----|
| 使用 v2 文件 | ✅ 是 |
| 备份是否成功 | ✅ backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch3_full40.json |
| 合并前 item_count | 1677 |
| 合并后 item_count | 1717 |
| 实际新增 item 数 | 40 |
| 新增 section 数 | 0 |
| 11 个清洗候选是否使用 cleaned_direct_pre_item_ids | ✅ 是 |

## 2. Section 分布

| Section | 名称 | 新增数量 |
|---------|------|:--------:|
| 2.8 | 动态规划 | 8 |
| 2.10 | 字符串算法 | 5 |
| 3.8 | 字符串结构 | 2 |
| 4.1 | 整数与数论基础 | 4 |
| 4.9 | 高级数学与群论 | 4 |
| 2.17 | 线性代数与插值专题 | 2 |
| 2.18 | 综合高级技巧专题 | 4 |
| 2.21 | 高级图论扩展 | 5 |
| 3.13 | 高级数据结构扩展 | 6 |
| **总计** | - | **40** |

## 3. 清洗候选（11 个，来自 dependency_cleanup_plan）

| item_id | 名称 | 使用 cleaned_direct_pre |
|---------|------|:---------------------:|
| 2.21.147 | 强连通分量 DAG：Dag Reachability | ✅ ['2.15.1', '2.9.7'] |
| 2.21.148 | 动态图连通性：Divide And Conquer On Time | ✅ ['2.1.34', '3.4.1'] |
| 2.21.149 | 强连通分量 DAG：Dominating Components | ✅ ['2.15.1', '2.15.10'] |
| 2.21.150 | 动态图连通性：Edge Interval Model | ✅ ['2.21.27', '3.4.1'] |
| 2.21.151 | 强连通分量 DAG：Minimum Edges To Strong | ✅ ['2.15.1', '2.15.10'] |
| 3.13.186 | 位集与线性基：Rollback Linear Basis | ✅ ['2.18.3', '3.13.49'] |
| 3.13.187 | 位集与线性基：Maximum Xor Query | ✅ ['2.18.3', '2.17.6'] |
| 3.13.188 | 位集与线性基：Rank Over Gf2 | ✅ ['2.18.3', '2.17.8'] |
| 3.13.189 | 位集与线性基：Basis With Deletion | ✅ ['2.18.3', '3.13.49'] |
| 3.13.190 | 线段树变体：Split | ✅ ['3.7.2'] |
| 3.13.191 | 高级并查集：Parity | ✅ ['3.4.1', '3.4.4'] |

## 4. Validate-only 结果

| 检查项 | 结果 |
|--------|:----:|
| item_count = 1717 | {"✅" if v_item_count == 1717 else "❌"} |
| expected_item_count = 1717 | {"✅" if v_expected == 1717 else "❌"} |
| section_count = 65 | {"✅" if v_section_count == 65 else "❌"} |
| direct_pre 无 section id | ✅ |
| 悬空引用 = 0 | {"✅" if len(v_dangling) == 0 else "❌"} |
| direct_pre 无环 | {"✅" if v_cycle is None else "❌"} |
| resolved_pre_mismatches = 0 | {"✅" if len(v_mismatches) == 0 else "❌"} |
| product_metadata_validation passed | {"✅" if v_metadata.get('passed', False) == True else "❌"} |
| report_matches_json = true | {"✅" if v_report_matches == True else "❌"} |
| validation passed | {"✅" if v_passed == True else "❌"} |
| 是否生成 rollback plan | ✅ 是 |

## 5. 执行摘要

| 项目 | 状态 |
|------|:----:|
| 备份是否成功 | ✅ |
| 合并前 item_count | 1677 |
| 合并后 item_count | 1717 |
| 实际新增 item 数 | 40 |
| 新增 section 数 | 0 |
| 11 个清洗候选使用 cleaned_direct_pre | ✅ |
| direct_pre 无 section id | ✅ |
| 悬空引用 = 0 | ✅ |
| direct_pre 无环 | ✅ |
| resolved_pre_mismatches = 0 | ✅ |
| product_metadata_validation passed | ✅ |
| report_matches_json = true | ✅ |
| validation passed | ✅ |
| 是否生成 rollback plan | ✅ |

## 6. 需要人工复查的新增节点

| item_id | 名称 | 原因 |
|---------|------|------|
| 2.8.143 | DAG最长路DP | yellow_risk |
| 2.8.144 | 状态压缩DP基础 | yellow_risk |
| 2.8.145 | 旅行商问题DP | yellow_risk |
| 2.8.146 | 子集DP基础 | yellow_risk |
| 2.8.147 | 子集枚举优化 | yellow_risk |
| 2.8.148 | 自动机DP基础 | yellow_risk |
| 2.8.149 | 自动机矩阵DP | yellow_risk |
| 2.8.150 | 概率DP基础 | yellow_risk |
| 2.10.35 | Border树结构 | yellow_risk |
| 2.10.36 | Manacher算法 | yellow_risk |
| 2.10.37 | Boyer-Moore算法 | yellow_risk |
| 2.10.38 | Rabin-Karp算法 | yellow_risk |
| 2.10.39 | KMP算法详解 | yellow_risk |
| 3.8.15 | Lyndon分解基础 | yellow_risk |
| 3.8.16 | Runs重复子串分析 | yellow_risk |
| 4.1.35 | Legendre符号 | yellow_risk |
| 4.1.36 | Tonelli-Shanks算法 | yellow_risk |
| 4.1.37 | 扩展中国剩余定理 | yellow_risk |
| 4.1.38 | Garner算法 | yellow_risk |
| 4.9.6 | 欧拉函数应用 | yellow_risk |
| 4.9.7 | 杜教筛 | yellow_risk |
| 4.9.8 | Burnside引理 | yellow_risk |
| 4.9.9 | Polya计数定理 | yellow_risk |
| 2.17.21 | 快速沃尔什变换 | yellow_risk |
| 2.17.22 | 子集卷积 | yellow_risk |
| 2.18.12 | 斜率优化基础 | yellow_risk |
| 2.18.13 | 分治DP优化 | yellow_risk |
| 2.18.14 | Knuth优化 | yellow_risk |
| 2.18.15 | WQS二分优化 | yellow_risk |
| 2.21.147 | 强连通分量 DAG：Dag Reachability | cleaned_dependency |
| 2.21.148 | 动态图连通性：Divide And Conquer On Time | cleaned_dependency |
| 2.21.149 | 强连通分量 DAG：Dominating Components | cleaned_dependency |
| 2.21.150 | 动态图连通性：Edge Interval Model | cleaned_dependency |
| 2.21.151 | 强连通分量 DAG：Minimum Edges To Strong | cleaned_dependency |
| 3.13.186 | 位集与线性基：Rollback Linear Basis | cleaned_dependency |
| 3.13.187 | 位集与线性基：Maximum Xor Query | cleaned_dependency |
| 3.13.188 | 位集与线性基：Rank Over Gf2 | cleaned_dependency |
| 3.13.189 | 位集与线性基：Basis With Deletion | cleaned_dependency |
| 3.13.190 | 线段树变体：Split | cleaned_dependency |
| 3.13.191 | 高级并查集：Parity | cleaned_dependency |

## 7. 下一步建议

- 等待 2号线程执行 Stage3F Batch3 full_40 Review
- Review 完成后执行 Fix Lite
- 不要直接继续 Stage3F Batch4
