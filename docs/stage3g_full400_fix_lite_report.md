# Stage3G full400 Fix Lite Report

**生成时间**: 2026-05-25 23:24:14
**执行者**: 1号线程 / DeepSeek V4 Pro
**阶段**: Stage3G full400 轻量修复
**分支选择**: 分支 A（dependency_fix_candidates 空 + merge_or_collapse_candidates 空）

## 1. 前置条件确认

| 检查项 | 期望值 | 实际值 | 状态 |
|--------|:------:|:------:|:----:|
| item_count | 2165 | 2165 | ✅ |
| section_count | 65 | 65 | ✅ |
| validate-only passed | true | true | ✅ |
| dependency_fix_candidates 为空 | 0 | 0 | ✅ |
| merge_or_collapse_candidates 为空 | 0 | 0 | ✅ |
| patches 数量 | 400 | 400 | ✅ |
| patches 全为 Stage3G 新节点 | true | true | ✅ |

## 2. 修复统计

| 项目 | 值 |
|:-----|:--:|
| Stage3G full400 新增节点数 | 400 |
| 实际处理节点数 | 400 |
| 降为 C 数量 | 400 |
| 保留 B 数量 | 0 |
| 保留 A 数量 | 0 |

## 3. 操作范围

| 操作 | 执行？ |
|:-----|:-----:|
| 修改 direct_pre | ❌ 否 |
| 修改 resolved_pre | ❌ 否 |
| 修改 rel | ❌ 否 |
| 新增 item | ❌ 否 |
| 删除 item | ❌ 否 |
| 合并 item | ❌ 否 |
| 修改旧节点 | ❌ 否 |
| 处理 problem_patterns | ❌ 否 |

## 4. Problem Patterns Sync Candidates

| 项目 | 值 |
|:-----|:--:|
| 候选数量 | 94 |
| 本次处理 | ❌ 未处理，仅记录 |

## 5. Validate-only 结果

| 检查项 | 期望值 | 实际值 | 状态 |
|--------|:------:|:------:|:----:|
| item_count | 2165 | 2165 | ✅ |
| expected_item_count | 2165 | 2165 | ✅ |
| section_count | 65 | 65 | ✅ |
| dangling_refs | [] | [] | ✅ |
| direct_pre_cycle | null | None | ✅ |
| resolved_pre_mismatches | [] | [] | ✅ |
| product_metadata_validation.passed | true | True | ✅ |
| report_matches_json | true | True | ✅ |
| passed | true | True | ✅ |

## 6. 安全护栏

| 检查项 | 状态 |
|:-------|:----:|
| 备份成功 | ✅ |
| 旧节点未修改 | ✅ |
| direct_pre 未修改 | ✅ |
| resolved_pre 未修改 | ✅ |
| rel 未修改 | ✅ |
| 失败回滚机制 | ✅ |

## 7. 下一步建议

1. ✅ **建议生成 Stage3G full400 Stable Checkpoint**
2. ❌ **不建议继续 Stage3G Batch2**（等待 Stage3G full400 Complete 后再决策）
