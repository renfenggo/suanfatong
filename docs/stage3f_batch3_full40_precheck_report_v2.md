# Stage3F Batch3 Full40 动态预审报告 v2

## 基本信息

| 项目 | 值 |
|------|------|
| **批次** | Stage3F Batch3 Full40 v2 |
| **候选数** | 40 |
| **生成时间** | 2026-05-25T17:30:00 |
| **主图谱修改** | 否 |

## 当前主图谱状态

| 检查项 | 结果 |
|--------|------|
| item_count = 1677 | ✅ |
| section_count = 65 | ✅ |
| validate-only passed | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |

## Dependency Cleanup 前后对比

| 检查项 | v1 结果 | v2 结果 |
|--------|---------|---------|
| dependency_cleanup_required | true | **false** ✅ |
| dependency_mapping_risk | 11 个 | **0 个** ✅ |
| section_ref_dependencies | 0 | **0** ✅ |

## 预审检查清单

| 检查维度 | 结果 |
|---------|------|
| selected_candidates 数量 | **40** ✅ |
| excluded_already_merged_candidates | **0** ✅ |
| excluded_duplicate_or_near_duplicate | **0** ✅ |
| high_risk_candidates | **0** ✅ |
| manual_review_candidates | **0** ✅ |
| needs_new_section | **false** ✅ |
| candidate_dependency_cycle | **false** ✅ |
| 所有 direct_pre 为 item id | **true** ✅ |
| 无 section id 引用 | **true** ✅ |

## 综合建议

| 项目 | 建议 |
|------|------|
| **recommendation** | **ready_for_1号线程_merge_full40** |
| **recommended_merge_count** | **40** |
| 主图谱修改 | **否** |

---

*v2 版本已修复 dependency_cleanup_required = true 问题。可直接交给 1号线程合并。*
