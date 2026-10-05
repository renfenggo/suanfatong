# Stage3E Final Checkpoint Report

**生成时间**: 2026-05-25T12:20:04.000Z
**生成者**: 1号线程 / GLM5
**版本**: 1.0.0（含报告一致性修复）

---

## 1. 当前主图谱状态

| 检查项 | 实际值 | 预期值 | 结果 |
|--------|--------|--------|:----:|
| item_count | 1641 | 1641 | ✅ |
| expected_item_count | 1641 | 1641 | ✅ |
| section_count | 65 | 65 | ✅ |
| dangling_refs | 0 | 0 | ✅ |
| direct_pre_cycle | null | null | ✅ |
| resolved_pre_mismatches | 0 | 0 | ✅ |
| product_metadata_validation.passed | true | true | ✅ |
| report_matches_json | true | true | ✅ |
| passed | true | true | ✅ |

## 2. 报告一致性修复说明

| 项目 | 修复前 | 修复后 |
|------|:------:|:------:|
| official passed | false | **true** |
| report_matches_json | false | **true** |
| refined 主图谱知识内容修改 | — | ❌ 否 |
| item_count | 1641 | **1641** |

**修复内容**:
- 同步 `merged_knowledge_graph.json` 至 1641 节点版本（从 refined file 复制）
- 重新生成 `item_dependency_refinement_report.md`，使用当前 refined 图谱统计
- 重新运行 validate-only → `report_matches_json=true` → `passed=true`

## 3. Stage3E 各批次新增数量

| 批次 | 新增数量 | 目标 section | Merge | Review | Fix Lite |
|------|:--------:|:------------:|:-----:|:------:|:--------:|
| Batch1 | 30 | 2.21 | ✅ | ✅ | ✅ |
| Batch2 | 30 | 3.13 / 2.21 | ✅ | ✅ | ✅ |
| Batch3 | 30 | 3.13 / 2.21 | ✅ | ✅ | ✅ |
| Batch4 | 30 | 3.13 / 2.21 | ✅ | ✅ | ✅ |
| Batch5 smaller_15 | 15 | 3.13 | ✅ | ✅ | ✅ |
| Batch6 fallback_24 | 24 | 3.13 | ✅ | ✅ | ✅ |
| **总计** | **159** | - | **6/6** | **6/6** | **6/6** |

## 4. Batch7 预审结果

| 项目 | 数值 |
|------|:----:|
| 可用候选（去重后） | 96 |
| 安全候选 | 1 |
| 名称重复排除 | 95 |
| 入选候选 | dominance_counting（唯一） |

**评估**: 候选池基本耗尽。

| 项目 | 建议 |
|------|:----:|
| dominance_counting | 📦 暂存 Stage3F |
| 是否继续 Batch7 | ❌ 否 |
| 是否进入 Stage3F | ✅ 是 |

## 5. 结论

| 检查项 | 结果 |
|--------|:----:|
| Stage3E 是否正式完成 | ✅ **是** |
| 主图谱是否修改 | ❌ **否** |
| refined 知识内容是否修改 | ❌ **否** |
| official passed | ✅ **true** |
| 继续 Batch7 | ❌ **否** |
| 进入 Stage3F | ✅ **是** |
