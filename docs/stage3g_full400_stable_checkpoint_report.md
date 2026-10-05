# Stage3G full400 Stable Checkpoint Report

**生成时间**: 2026-05-25 23:30:00
**执行者**: 1号线程 / DeepSeek V4 Pro
**阶段**: Stage3G full400 Stable Checkpoint
**操作类型**: 只读（主图谱未修改）

---

## 一、当前图谱快照

| 项目 | 值 |
|:-----|:--:|
| item_count | **2165** |
| section_count | **65** |
| validate-only passed | ✅ true |
| dangling_refs | ✅ [] |
| direct_pre_cycle | ✅ null |
| resolved_pre_mismatches | ✅ [] |
| product_metadata_validation.passed | ✅ true |
| report_matches_json | ✅ true |
| direct_pre_item_ref_ratio | 1.0 |
| direct_pre_section_refs | 0 |

---

## 二、管线历程

### Stage3G full400 Merge

| 项目 | 值 |
|:-----|:--:|
| 时间 | 2026-05-25 22:56 |
| 合并前 item_count | 1765 |
| 合并后 item_count | **2165** |
| 新增节点数 | 400 |
| 创建新 section | ❌ 否 |
| 写入未解析依赖 | ❌ 否 |
| validate-only 通过 | ✅ 是 |
| 使用 v2 文件 | ✅ 是 |
| 未使用 v1 文件 | ✅ 是 |
| 直接合并候选 (>0 direct_pre) | 395 |
| direct_pre=[] 候选 | 5 |

**Section 分布**：28 个 sections，最大 section 2.9（126），2.8（45）

**风险评估**：green=176, yellow=177, medium=47, red=0

**候选类型**：core_concept=253, modeling_pattern=93, implementation_variant=41, theorem_or_property=11, application_case=2

**替换候选**：22（填充 red/duplicate 移除后的空缺）

---

### Stage3G full400 Review（2号线程）

| 项目 | 值 |
|:-----|:--:|
| 时间 | 2026-05-25 15:09 |
| 审查节点数 | **400** |
| approve | **400** |
| needs_dependency_fix | 0 |
| needs_merge_or_collapse | 0 |
| suggested_problem_pattern_sync | 94 |
| needs_section_review | 0 |
| keep_manual_review_A | 0 |
| keep_manual_review_B | 0 |
| demote_to_C | 400 |
| direct_pre avg | 3.0 |
| 主图谱修改 | ❌ 否 |

**结论**：400 个新增节点全部 approve，全部建议降为 C，无依赖修复需求，无合并/折叠需求。

---

### Stage3G full400 Fix Lite

| 项目 | 值 |
|:-----|:--:|
| 时间 | 2026-05-25 23:24 |
| 分支选择 | **分支 A（标准 Fix Lite）** |
| 实际处理节点数 | **400** |
| 降为 C | **400** |
| 保留 B | 0 |
| 保留 A | 0 |
| 修改 direct_pre | ❌ 否 |
| 修改 resolved_pre | ❌ 否 |
| 修改 rel | ❌ 否 |
| 修改旧节点 | ❌ 否 |
| 新增/删除/合并 item | ❌ 否 |
| 处理 problem_patterns | ❌ 否 |
| validate-only 通过 | ✅ 是 |

---

## 三、待处理项

### Problem Pattern Sync Candidates

| 项目 | 值 |
|:-----|:--:|
| 候选总数 | **94** |
| 处理状态 | ❌ 未处理（仅记录） |

| Theme | 数量 |
|:------|:----:|
| 题型建模方法 | 30 |
| 图论专题 | 10 |
| 动态规划专题 | 9 |
| 基础算法扩展 | 8 |
| 编程技巧 | 8 |
| 比赛相关知识 | 7 |
| 调试方法 | 7 |
| 数据结构专题 | 3 |
| STL与常用库细节 | 2 |
| 字符串专题 | 2 |
| 信奥数学 | 1 |
| 其他 | 7 |

**建议**：
- 可选处理 patterns_batch3 / Stage3G problem_patterns 同步
- 等待用户指令后再决策

### Stage3G Batch2

- **建议**：❌ 暂不建议
- **原因**：需先决定是否处理 94 个 problem_pattern_sync_candidates

---

## 四、备份清单

| # | 文件 |
|:-:|------|
| 1 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400.json` |
| 2 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400_fix_lite.json` |

---

## 五、关键文件索引

| 类型 | 文件路径 |
|:-----|---------|
| 主图谱 | `merged_knowledge_graph_item_dependencies_refined.json` |
| 候选映射 | `data/stage3g_full400_candidate_to_item_id_mapping.json` |
| 当前验证 | `dependency_validation_result.json` |
| Merge 验证 | `data/stage3g_full400_validation_result.json` |
| Fix Lite 验证 | `data/stage3g_full400_fix_lite_validation_result.json` |
| Fix Lite 补丁 | `data/stage3g_full400_fix_lite_applied_patch.json` |
| Review 报告 | `docs/stage3g_full400_added_items_review_report.md` |
| Fix Lite 报告 | `docs/stage3g_full400_fix_lite_report.md` |
| Merge 报告 | `docs/stage3g_full400_merge_report.md` |
| Problem Pattern 候选 | `data/stage3g_full400_problem_pattern_sync_candidates.json` |
| Stable Checkpoint | `data/stage3g_full400_stable_checkpoint.json` |

---

## 六、总结

| 项目 | 状态 |
|:-----|:----:|
| 当前 item_count / section_count | 2165 / 65 ✅ |
| validate-only 状态 | passed ✅ |
| Merge 结果 | 1765 → 2165 ✅ |
| Review 结果 | 400 全部 approve ✅ |
| Fix Lite 结果 | 400 全部降为 C ✅ |
| 保留 B 数量 | 0 ✅ |
| 保留 A 数量 | 0 ✅ |
| dependency_fix_candidates 为空 | ✅ |
| merge_or_collapse_candidates 为空 | ✅ |
| problem_pattern_sync_candidates | 94，仅记录未处理 ✅ |
| 是否修改主图谱 | ❌ 否（本 checkpoint 为只读） |
| 是否建议继续 Stage3G Batch2 | ❌ 暂不建议 |
| 是否建议先处理 patterns_batch3 / Stage3G problem_patterns | 可选，等用户指令 |
