# Stage3F Batch4 full49 Merge Report

**生成时间**: 2026-05-25 17:52:35
**执行者**: 1号线程 / GLM5
**阶段**: Stage3F Batch4 full49 Merge

## 1. 基本信息

| 项目 | 值 |
|------|-----|
| 是否使用 full49 v2 文件 | ✅ 是 |
| 是否使用 full50 文件 | ❌ 否 |
| 备份是否成功 | ✅ |
| 合并前 item_count | 1716 |
| 合并后 item_count | 1765 |
| 实际新增 item 数 | 49 |
| 是否创建新 section | ❌ 否 |

## 2. 新增节点 Section 分布

| Section | 数量 | 节点 ID 范围 |
|---------|:----:|-------------|
| 2.21 | 20 | 2.21.152, 2.21.153, 2.21.154, 2.21.155, 2.21.156... |
| 3.13 | 15 | 3.13.192, 3.13.193, 3.13.194, 3.13.195, 3.13.196... |
| 2.8 | 6 | 2.8.151, 2.8.152, 2.8.153, 2.8.154, 2.8.155... |
| 4.5 | 2 | 4.5.17, 4.5.18 |
| 2.10 | 4 | 2.10.39, 2.10.40, 2.10.41, 2.10.42 |
| 4.4 | 2 | 4.4.15, 4.4.16 |

## 3. 3 个 Medium 风险候选依赖确认

| 候选 | 名称 | 目标 Section | 依赖状态 |
|------|------|:-----------:|:--------:|
| cand.string.string_matching.sunday | Sunday算法 | 2.10 | ✅ 所有 218 个 direct_pre 均已确认 |
| cand.math.linear_recurrence.basic | 线性递推基础 | 4.4 | ✅ 所有 88 个 direct_pre 均已确认 |
| cand.math.linear_recurrence.kitamasa | Kitamasa算法 | 4.4 | ✅ 所有 88 个 direct_pre 均已确认 |

## 4. 安全护栏检查

| 检查项 | 状态 |
|--------|:----:|
| direct_pre 是否无 section id | ✅ 是 |
| 悬空引用是否为 0 | ✅ 是 |
| direct_pre 是否无环 | ✅ 是 |
| resolved_pre_mismatches 是否为 0 | ✅ 是 |
| 旧节点 resolved_pre 是否未覆盖 | ✅ 是 |
| 是否生成 rollback plan | ✅ 是 |

## 5. Validate-only 结果

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

## 6. 下一步建议

1. ✅ **建议进入 Stage3F Batch4 Review**（对 49 个新增节点做 review_status 降级）
2. ❌ **不继续 Stage3F Batch5**
