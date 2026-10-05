# Stage3E Batch5 smaller_15 Merge 报告

**生成时间**: 2026-05-25 10:21:44
**生成人**: 1号线程 / GLM5

---

## 1. 前置条件检查

| 条件 | 结果 |
|------|------|
| item_count | ✅ |
| section_count | ✅ |
| validate_passed | ✅ |
| selected_count | ✅ |
| recommendation | ✅ |
| recommended_merge_count | ✅ |
| cleanup_required | ✅ |
| no_section_id_deps | ✅ |
| no_cycle | ✅ |
| no_new_section | ✅ |

---

## 2. 执行摘要

| 项目 | 数值 |
|------|------|
| 备份是否成功 | ✅ backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_batch5_smaller15.json |
| 合并前 item_count | 1602 |
| 合并后 item_count | 1617 |
| 实际新增 item 数 | 15 |
| 是否创建新 section | ❌ 否 |
| 新增节点进入 section | 3.13 高级数据结构扩展 |
| 是否只合并 smaller_15 的 15 个候选 | ✅ 是 |
| direct_pre 是否无 section id | ✅ 是 |
| 悬空引用是否为 0 | ✅ 是 (0) |
| direct_pre 是否无环 | ✅ 是 |
| resolved_pre_mismatches 是否为 0 | ✅ 是 (0) |
| product_metadata_validation 是否 passed | ✅ {'passed': True} |
| report_matches_json 是否 true | ✅ True |
| validation 是否 passed | ✅ True |
| 是否生成 rollback plan | ✅ data/stage3e_batch5_smaller15_rollback_plan.json |

---

## 3. 新增节点列表

| # | item_id | 名称 | en_name | direct_pre | resolved_pre 数量 |
|---|---------|------|---------|------------|-------------------|
| 1 | 3.13.143 | 高级并查集：Undo Stack | Advanced DSU: Undo Stack | 3.4.1 | 13 |
| 2 | 3.13.144 | 可并堆：Binomial Heap | Mergeable Heap: Binomial Heap | 3.2.3 | 7 |
| 3 | 3.13.145 | 可并堆：Fibonacci Heap | Mergeable Heap: Fibonacci Heap | 3.2.3 | 7 |
| 4 | 3.13.146 | 可并堆：Leftist Heap | Mergeable Heap: Leftist Heap | 3.2.3 | 7 |
| 5 | 3.13.147 | 可并堆：Pairing Heap | Mergeable Heap: Pairing Heap | 3.2.3 | 7 |
| 6 | 3.13.148 | 可并堆：Skew Heap | Mergeable Heap: Skew Heap | 3.2.3 | 7 |
| 7 | 3.13.149 | 李超线段树：Coordinate Compressed | Li Chao Tree: Coordinate Compressed | 2.8.28, 3.7.2 | 27 |
| 8 | 3.13.150 | 李超线段树：动态版 | Li Chao Tree: Dynamic | 2.8.28, 3.7.2 | 27 |
| 9 | 3.13.151 | 李超线段树：可持久化版 | Li Chao Tree: Persistent | 2.8.28, 3.7.2 | 27 |
| 10 | 3.13.152 | 李超线段树：Segment Insertion | Li Chao Tree: Segment Insertion | 2.8.28, 3.7.2 | 27 |
| 11 | 3.13.153 | Segment Tree Beats：Historical Maximum | Segment Tree Beats: Historical Maximum | 3.7.2, 3.7.3 | 18 |
| 12 | 3.13.154 | Segment Tree Beats：Range Add Max | Segment Tree Beats: Range Add Max | 3.7.2, 3.7.3 | 18 |
| 13 | 3.13.155 | Segment Tree Beats：区间取 min 变体 1 | Segment Tree Beats: Range Chmin Variant 1 | 3.7.2, 3.7.3 | 18 |
| 14 | 3.13.156 | 线段树变体：Dynamic Segment Tree | Segment Tree Variants: Dynamic Segment Tree | 3.7.2 | 17 |
| 15 | 3.13.157 | 线段树变体：Gcd Segment Tree | Segment Tree Variants: Gcd Segment Tree | 3.7.2 | 17 |

---

## 4. 验证结果

| 检查项 | 期望值 | 实际值 | 状态 |
|--------|--------|--------|------|
| item_count | 1617 | 1617 | ✅ |
| expected_item_count | 1617 | 1617 | ✅ |
| section_count | 65 | 65 | ✅ |
| dangling_refs | [] | [] | ❌ |
| direct_pre_cycle | null | None | ❌ |
| resolved_pre_mismatches | [] | [] | ❌ |
| report_matches_json | True | True | ✅ |
| passed | True | True | ✅ |

---

## 5. 限制遵守确认

| 限制 | 遵守情况 |
|------|---------|
| 合并前备份主图谱 | ✅ |
| 不修改已有 item id | ✅ |
| 不删除 item | ✅ |
| 不重排 section | ✅ |
| 不创建新 section | ✅ |
| 只合并 Batch5 smaller_15 的 15 个候选 | ✅ |
| 全部新增节点进入 3.13 | ✅ |
| direct_pre 全部使用正式 item id | ✅ |
| direct_pre 不含 section id | ✅ |
| learning_path_policy unlock_mode 不为 null | ✅ |
| resolved_pre 只写回新增节点 | ✅ |
| 不覆盖旧节点 resolved_pre | ✅ |
| 不继续 Batch6 | ✅ |
| validate-only 失败已恢复备份 | {'✅ 未触发' if all_valid else '❌ 已触发恢复'} |

---

**最终状态**: ✅ 合并成功，主图谱稳定于 item_count=1617
**不得继续 Batch6**: ✅ 已遵守