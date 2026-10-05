# Stage3F Batch3 full_40 Duplicate Prune Report

**生成时间**: 2026-05-25 17:08:24
**执行者**: 1号线程 / GLM5
**方案**: 方案 C（删除 KMP算法详解，保留 Border树结构）

## 1. 基本信息

| 项目 | 值 |
|------|-----|
| 删除前 item_count | 1717 |
| 删除后 item_count | 1716 |
| 删除节点 | 2.10.39 KMP算法详解 |
| 对应的已有重复节点 | 2.10.2 (KMP) |
| 保留的候选合并节点 | 2.10.35 Border树结构 |
| section_count | 65（不变） |

## 2. 入边依赖检查

| 依赖类型 | 是否有依赖 |
|:--------:|:----------:|
| direct_pre 入边 | ❌ 无 |
| resolved_pre 入边 | ❌ 无 |
| rel 入边 | ❌ 无 |
| 是否产生 dangling_refs | ❌ 否 |

## 3. Validate-only 结果

| 检查项 | 结果 |
|--------|:----:|
| item_count = 1716 | ✅ |
| expected_item_count = 1716 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| product_metadata_validation.passed = true | ✅ |
| report_matches_json = true | ✅ |
| passed = true | ✅ |

## 4. 执行摘要

| 项目 | 状态 |
|------|:----:|
| 备份是否成功 | ✅ |
| 删除前 item_count | 1717 |
| 删除后 item_count | 1716 |
| 删除节点 | 2.10.39 KMP算法详解 |
| 是否修改 direct_pre / resolved_pre / rel | ❌ 否 |
| 是否重排 item id | ❌ 否 |
| 是否创建新 section | ❌ 否 |
| validate-only 是否 passed | ✅ |
| 是否生成 rollback plan | ✅ |

## 5. 下一步建议

1. 进入 **Stage3F Batch3 Fix Lite**，只处理剩余 39 个新增节点的 review_status
2. 排除已删除的 2.10.39
3. 2.10.35 Border树结构保持 Review 决定的 C 优先级
4. 不继续 Stage3F Batch4
