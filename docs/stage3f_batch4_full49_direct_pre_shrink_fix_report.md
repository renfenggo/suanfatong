# Stage3F Batch4 full49 direct_pre Shrink Fix Report

**生成时间**: 2026-05-25 20:46:50
**执行者**: 1号线程 / GLM5
**阶段**: Stage3F Batch4 direct_pre Shrink Fix

## 1. 缩减统计

| 项目 | 值 |
|------|-----|
| 缩减节点总数 | 34 |
| direct_pre 总数变化 | 4824 → 138 |
| 平均 direct_pre 变化 | 141.9 → 4.1 |
| resolved_pre 重算节点数 | 34 |
| 直接修改的节点 | 34 |
| 下游同步重算节点 | 0 |

## 2. Manual Review 节点处理情况

| item_id | 名称 | new_direct_pre |
|---------|------|---------------|
  - 2.10.39 (Sunday算法): new_direct_pre = ['2.10.1', '2.10.2', '1.6.16', '1.6.1']
  - 4.4.15 (线性递推基础): new_direct_pre = ['4.1.1', '4.1.15', '2.1.3', '2.1.40', '2.12.2']
  - 4.4.16 (Kitamasa算法): new_direct_pre = ['2.12.2', '2.12.11', '4.4.15']

## 3. 安全护栏检查

| 检查项 | 状态 |
|--------|:----:|
| 是否修改 rel | ❌ 否 |
| 是否修改 review_status | ❌ 否 |
| 是否新增/删除 item | ❌ 否 |
| 是否修改非 affected 节点 resolved_pre | ❌ 否 |
| 3 个 manual_review 节点是否已处理 | ✅ 是 |
| direct_pre 是否无 section id | ✅ 是 |
| direct_pre 是否无 self reference | ✅ 是 |

## 4. Validate-only 结果

| 检查项 | 结果 |
|--------|:----:|
| item_count = 1765 | ✅ |
| expected_item_count = 1765 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| product_metadata_validation.passed = true | ✅ |
| report_matches_json = true | ✅ |
| passed = true | ✅ |

## 5. 下一步建议

1. ✅ **建议下一步执行 Stage3F Batch4 Fix Lite**（review_status 降级）
2. ❌ **不继续 Stage3F Batch5**
