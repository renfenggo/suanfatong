# Stage3F Batch4 稳定检查点报告

**生成时间**: 2026-05-25 21:56:43
**执行者**: 1号线程 / GLM5
**检查点文件**: `data/stage3f_batch4_stable_checkpoint.json`

---

## 1. 当前图谱状态

| 指标 | 值 |
|:-----|:--:|
| item_count | 1765 |
| section_count | 65 |
| Batch4 新增节点 | 49 |
| item_count 变化 | 1716 → 1765 |
| section_count 变化 | 65 → 65 (不变) |

## 2. Validate-only 状态

| 检查项 | 结果 |
|:-------|:----:|
| passed | ✅ |
| expected_item_count = 1765 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| product_metadata_validation.passed | ✅ |
| report_matches_json | ✅ |

## 3. Batch4 full49 Merge 结果

| 指标 | 值 |
|:-----|:--:|
| 合并前 item_count | 1716 |
| 合并后 item_count | 1765 |
| 新增节点数 | 49 |
| 候选计划数 | 49 |
| 实际新增 | 49 |
| 使用 full49 v2 文件 | ✅ 是 |
| 未使用 full50 文件 | ✅ 是 |

## 4. direct_pre 缩减修复结果

| 指标 | 值 |
|:-----|:--:|
| 缩减节点总数 | 34 |
| direct_pre 总数变化 | 4824 → 138 |
| 平均 direct_pre 变化 | 141.9 → 4.1 |
| 3 个人工复核节点 | ✅ 已处理 (Sunday算法、线性递推基础、Kitamasa算法) |

## 5. Fix Lite 结果

| 指标 | 值 |
|:-----|:--:|
| 处理节点数 | 49 |
| 降为 C | 40 |
| 保留 B | 8 |
| 保留 A | 1 |
| 保留 A 节点 | 4.5.18 矩阵树定理 |
| 修改 direct_pre | ❌ 否 |
| 修改 resolved_pre | ❌ 否 |
| 修改 rel | ❌ 否 |
| 修改旧节点 | ❌ 否 |

## 6. 未处理问题

| 问题 | 状态 |
|:-----|:----:|
| dependency_fix_candidates | ✅ 已处理 (通过 direct_pre shrink fix) |
| merge_or_collapse_candidates | ✅ 空 |
| problem_pattern_sync_candidates | ⚠️ 6 个候选，仅记录未处理 |

### Problem Pattern 候选清单 (6 个)

| item_id | name | section |
|:--------|:-----|:-------:|
| 2.21.152 | 最大权闭合子图：Penalty Modeling | 2.21 |
| 2.21.156 | 全局最小割：Minimum Cut Modeling | 2.21 |
| 2.21.159 | 差分约束系统建模 | 2.21 |
| 2.21.161 | Hall 定理及应用 | 2.21 |
| 2.21.170 | 高级最短路：Zero One Bfs Modeling | 2.21 |
| 2.21.171 | 2-SAT 建模技巧 | 2.21 |

## 7. 主图谱修改状态

| 操作 | 状态 |
|:-----|:----:|
| 本次生成检查点修改主图谱 | ❌ 否 |
| 修改 merged_knowledge_graph_item_dependencies_refined.json | ❌ 否 |
| 修改 dependency_validation_result.json | ❌ 否 |
| 修改 item_dependency_refinement_report.md | ❌ 否 |
| 修改 refine_item_dependencies.py | ❌ 否 |

## 8. 下一步建议

| 建议 | 结论 |
|:-----|:----:|
| 继续 Stage3F Batch5 | 可以，但需先确认候选池剩余数量 |
| 处理 problem_patterns (6 个 candidate) | 可选，等用户指令 |
| 处理 patterns_batch3 剩余 | 可选，等用户指令 |
| 生成 Stable Checkpoint | ✅ 已完成 |

## 9. 可用备份

| # | 备份文件 | 说明 |
|:-:|:---------|:-----|
| 1 | `backups/..._before_stage3f_batch4_full49.json` | Merge 前 |
| 2 | `backups/..._before_stage3f_batch4_direct_pre_shrink.json` | direct_pre 缩减前 |
| 3 | `backups/..._before_stage3f_batch4_fix_lite.json` | Fix Lite 前 |

---

**生成时间**: 2026-05-25 21:56:43
**主图谱未修改**
