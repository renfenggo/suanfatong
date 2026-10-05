# Stage3G full400 Merge Report

**生成时间**: 2026-05-25 22:56:20
**执行者**: 1号线程 / DeepSeek V4 Pro
**阶段**: Stage3G full400 Merge (v2)

## 1. 文件来源

| 项目 | 状态 |
|:-----|:----:|
| 使用 v2 文件 | ✅ 是 |
| 未使用 v1 文件 | ✅ 是 |

## 2. 基本信息

| 项目 | 值 |
|:-----|:--:|
| 合并前 item_count | 1765 |
| 合并后 item_count | 2165 |
| 实际新增节点数 | 400 |
| section_count | 65 |
| 是否创建新 section | ❌ 否 |
| 是否写入未解析依赖 | ❌ 否 |

## 3. 新增节点 Section 分布

| Section | 数量 |
|:-------:|:----:|
| 2.1 | 16 |
| 2.10 | 22 |
| 2.11 | 4 |
| 2.12 | 3 |
| 2.14 | 7 |
| 2.15 | 4 |
| 2.16 | 11 |
| 2.17 | 5 |
| 2.18 | 15 |
| 2.2 | 5 |
| 2.21 | 15 |
| 2.3 | 4 |
| 2.4 | 5 |
| 2.5 | 7 |
| 2.6 | 1 |
| 2.7 | 1 |
| 2.8 | 45 |
| 2.9 | 126 |
| 3.1 | 1 |
| 3.13 | 24 |
| 3.2 | 3 |
| 3.3 | 6 |
| 3.5 | 6 |
| 3.8 | 20 |
| 3.9 | 4 |
| 4.1 | 17 |
| 4.3 | 13 |
| 4.4 | 2 |
| 4.5 | 4 |
| 4.6 | 4 |

## 4. 依赖处理

| 项目 | 值 |
|:-----|:--:|
| direct_pre 全部为正式 item id | ✅ 是 |
| direct_pre 无 section id | ✅ 是 |
| 跳过未解析依赖 | 0 |
| direct_pre=[] 候选 | 5 |
| 直接合并候选 (>0 direct_pre) | 395 |

### direct_pre=[] 候选清单

cand.cpp.c_引用_左值_右值引用, cand.cpp.c_11_override_final_default_delete, cand.contest.比赛规则_acm赛制, cand.contest.比赛技巧_猜结论与打表, cand.contest.比赛工具_vim_vs_code竞赛配置

## 5. Validate-only 结果

| 检查项 | 结果 |
|:-------|:----:|
| item_count = 2165 | ✅ |
| expected_item_count = 2165 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| product_metadata_validation.passed = true | ✅ |
| report_matches_json = true | ✅ |
| passed = true | ✅ |

## 6. 安全护栏

| 检查项 | 状态 |
|:-------|:----:|
| 旧节点 direct_pre 未修改 | ✅ |
| 旧节点 resolved_pre 未覆盖 | ✅ |
| 旧节点 rel 未修改 | ✅ |
| 是否生成 rollback plan | ✅ 是 |

## 7. 下一步建议

1. ✅ **建议进入 Stage3G full400 Review**（对 400 个新增节点做 review_status 降级）
2. ❌ **不继续 Stage3G Batch2**
