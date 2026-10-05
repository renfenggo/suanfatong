# Stage3F Batch2 Duplicate Prune Report

**生成时间**: 2026-05-25 15:49:00
**执行者**: 1号线程 / GLM5
**操作**: 删除 4 个 Stage3F Batch2 新增重复节点

## 1. 前置条件

| 条件 | 结果 |
|------|:----:|
| 删除前 item_count = 1681 | ✅ |
| 4 个待删除节点均存在 | ✅ |
| 4 个节点均为 Stage3F Batch2 新增 | ✅ |
| 无 direct_pre 入边依赖 | ✅ |
| 无 resolved_pre 入边依赖 | ✅ |
| 无 rel 入边依赖 | ✅ |
| 删除后不产生 dangling_refs | ✅ |

## 2. 删除节点清单

| item_id | 名称 | 所在 section | 对应已有重复节点 |
|---------|------|:-----------:|:--------------:|
| 2.10.31 | 扩展KMP算法基础 | 2.10 | 2.10.17（扩展 KMP） |
| 4.1.30 | Miller-Rabin素数测试 | 4.1 | 4.1.18（素数判定：Miller-Rabin） |
| 4.3.33 | Lucas定理 | 4.3 | 4.3.15（Lucas）+ 4.3.21（组合数计算：Lucas） |
| 2.18.10 | 单调队列优化 | 2.18 | 2.8.26（单调队列优化 DP） |

## 3. 执行摘要

| 项目 | 值 |
|------|-----|
| 备份是否成功 | ✅ backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2_duplicate_prune.json |
| 删除前 item_count | 1681 |
| 删除后 item_count | 1677 |
| 实际删除 item 数 | 4 |
| 是否有入边依赖 | ❌ 否（0 个节点引用） |
| 是否产生 dangling_refs | ❌ 否 |
| 是否修改 direct_pre / resolved_pre / rel | ❌ 否（只删除节点，不修改其他节点） |
| 是否重排 item id | ❌ 否 |

## 4. Validate-only 结果

| 检查项 | 结果 |
|--------|:----:|
| item_count = 1677 | ✅ |
| expected_item_count = 1677 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| product_metadata_validation.passed = true | ✅ |
| report_matches_json = true | ✅ |
| passed = true | ✅ |

## 5. 总体结论

| 项目 | 状态 |
|------|:----:|
| Duplicate Prune 是否成功 | ✅ 成功 |
| 是否需要恢复备份 | 否 |

## 6. 下一步建议

- 建议进入 Stage3F Batch2 Fix Lite（只修改剩余 16 个节点的 review_status）
- 注意 Fix Lite 时排除已删除的 4 个节点
- 不要直接继续 Stage3F Batch3
