# Stage3E Batch5 smaller_15 候选选择与动态预审报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T10:00:00.000Z
- **主图谱状态**: 未修改

## 当前主图谱状态

| 检查项 | 结果 |
|--------|------|
| item_count | 1602（应为 1602）|
| section_count | 65 |
| validate-only | passed ✓ |
| resolved_pre_mismatches | [] |
| dangling_refs | [] |
| direct_pre_cycle | null |
| product_metadata_validation.passed | true |
| passed | true |
| stable_checkpoint | 已完成 |

## 原 Batch5 候选概况

| 属性 | 值 |
|------|-----|
| 原 batch_5 候选数量 | 30 |
| 风险等级 | optional_remaining（全部 yellow） |
| Section 分布 | {'3.13': 30}（全部 3.13） |
| 系列组成 | DSU Advanced(1)、Mergeable Heap(10)、Li Chao Tree(8)、Segment Tree Beats(9)、Segment Tree Variants(2) |

## smaller_15 选择标准

1. 只选 15 个候选
2. 优先选择父概念清晰、依赖明确的核心算法变体
3. 避免 problem_patterns 优先同步候选
4. 避免 high duplicate risk 候选
5. 避免 needs_expert_review 高风险候选
6. 不选择 red/high risk/强 manual_review 候选
7. 所有候选均为 yellow 等级
8. 保持系列分布均衡

## 入选 15 个候选列表

| # | 候选 | 名称 | 系列 | 教育评分 | 选择理由 |
|---|------|------|------|---------|---------|
| 1 | cand.ds.dsu_advanced.undo_stack | 高级并查集：Undo Stack | 高级并查集 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 2 | cand.ds.heap_mergeable.binomial_heap | 可并堆：Binomial Heap | 可并堆 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 3 | cand.ds.heap_mergeable.fibonacci_heap | 可并堆：Fibonacci Heap | 可并堆 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 4 | cand.ds.heap_mergeable.leftist_heap | 可并堆：Leftist Heap | 可并堆 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 5 | cand.ds.heap_mergeable.pairing_heap | 可并堆：Pairing Heap | 可并堆 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 6 | cand.ds.heap_mergeable.skew_heap | 可并堆：Skew Heap | 可并堆 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 7 | cand.ds.li_chao_tree.coordinate_compressed | 李超线段树：Coordinate Compressed | 李超线段树 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 8 | cand.ds.li_chao_tree.dynamic | 李超线段树：动态版 | 李超线段树 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 9 | cand.ds.li_chao_tree.persistent | 李超线段树：可持久化版 | 李超线段树 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 10 | cand.ds.li_chao_tree.segment_insertion | 李超线段树：Segment Insertion | 李超线段树 | 8 | 核心算法变体，有独立竞赛教育价值 |
| 11 | cand.ds.segment_tree_beats.historical_maximum | Segment Tree Beats：Historical Maximum | Segment Tree Beats | 8 | 核心算法变体，有独立竞赛教育价值 |
| 12 | cand.ds.segment_tree_beats.range_add_max | Segment Tree Beats：Range Add Max | Segment Tree Beats | 8 | 核心算法变体，有独立竞赛教育价值 |
| 13 | cand.ds.segment_tree_beats.range_chmin.codex1 | Segment Tree Beats：区间取 min 变体 1 | Segment Tree Beats | 8 | 核心算法变体，有独立竞赛教育价值 |
| 14 | cand.ds.segment_tree_variants.dynamic_segment_tree | 线段树变体：Dynamic Segment Tree | 线段树变体 | 7 | 核心算法变体，有独立竞赛教育价值 |
| 15 | cand.ds.segment_tree_variants.gcd_segment_tree | 线段树变体：Gcd Segment Tree | 线段树变体 | 7 | 核心算法变体，有独立竞赛教育价值 |

## 排除候选及原因

| # | 候选 | 名称 | 系列 | 排除原因 |
|---|------|------|------|---------|
| 1 | cand.ds.heap_mergeable.double_ended_priority_queue | 可并堆：Double Ended Priority Queue | 可并堆 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 2 | cand.ds.heap_mergeable.heap_with_decrease_key | 可并堆：Heap With Decrease Key | 可并堆 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 3 | cand.ds.heap_mergeable.lazy_deletion_heap | 可并堆：Lazy Deletion Heap | 可并堆 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 4 | cand.ds.heap_mergeable.meldable_priority_queue | 可并堆：Meldable Priority Queue | 可并堆 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 5 | cand.ds.heap_mergeable.persistent_heap | 可并堆：Persistent Heap | 可并堆 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 6 | cand.ds.li_chao_tree.maximum_query | 李超线段树：Maximum Query | 李超线段树 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 7 | cand.ds.li_chao_tree.minimum_query | 李超线段树：Minimum Query | 李超线段树 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 8 | cand.ds.li_chao_tree.on_tree | 李超线段树：On Tree | 李超线段树 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 9 | cand.ds.li_chao_tree.rollback | 李超线段树：回滚版 | 李超线段树 | 同系列中教育区分度相对较低，优先保留核心变体 |
| 10 | cand.ds.segment_tree_beats.beats_amortized_analysis | Segment Tree Beats：Beats Amortized Analysis | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |
| 11 | cand.ds.segment_tree_beats.beats_proof | Segment Tree Beats：Beats Proof | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |
| 12 | cand.ds.segment_tree_beats.beats_with_assignment | Segment Tree Beats：Beats With Assignment | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |
| 13 | cand.ds.segment_tree_beats.range_min_max_sum | Segment Tree Beats：Range Min Max Sum | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |
| 14 | cand.ds.segment_tree_beats.range_modulo | Segment Tree Beats：Range Modulo | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |
| 15 | cand.ds.segment_tree_beats.second_maximum_invariant | Segment Tree Beats：Second Maximum Invariant | Segment Tree Beats | 同系列中教育区分度相对较低，优先保留核心变体 |

## 动态预审结果

| 检查项 | 结果 |
|--------|------|
| 是否与 Batch1~4 已合并 candidate 重复 | 无 |
| 是否包含 high risk 候选 | 无 |
| 是否包含 manual_review 候选 | 无 |
| 是否包含 problem_patterns 优先候选 | 无 |
| 是否需要新 section | 否 |
| direct_pre 是否全部为 item id | 是 |
| 是否包含 section id 依赖 | 否 |
| 是否存在候选依赖环 | 否 |
| 2.21 / 3.13 分布 | 0 / 15 |

### Section ID 依赖检查

**无 section id 依赖。** 所有 candidate 的 direct_pre 均为具体 item id。

### 依赖映射风险
**无依赖映射风险。**

### Section 分布
| Section | 数量 |
|---------|------|
| 2.21（高级图论扩展） | 0 |
| 3.13（高级数据结构扩展） | 15 |

## 总推荐

- **recommendation**: ready_for_1号线程_merge
- **recommended_merge_count**: 15
- **是否建议交给 1号线程合并**: 是

**建议步骤**:
1. 1号线程执行 Batch5 smaller_15 合并
2. 合并后运行 validate-only 验证
3. 生成 candidate_to_item_id_mapping

## 主图谱状态

- **主图谱是否修改**: **否**
- **本次任务**: 候选选择与动态预审，不涉及图谱修改
- **下一步**: 1号线程执行 Batch5 smaller_15 合并

---

报告生成时间: 2026-05-25T10:00:00.000Z
生成者: GLM5
任务类型: Stage3E Batch5 smaller_15 候选选择与动态预审
主图谱修改状态: 否
