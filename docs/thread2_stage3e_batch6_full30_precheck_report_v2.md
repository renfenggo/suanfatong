# Stage3E Batch6 full_30 v2 动态预审报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T10:45:00.000Z
- **任务**: Stage3E Batch6 full_30 v2 修正动态预审
- **主图谱状态**: 未修改
- **Batch5 Fix Lite**: 已完成

## 1. 当前主图谱状态

| 检查项 | 实际值 | 预期值 | 结果 |
|--------|--------|--------|------|
| item_count | 1617 | 1617 | ✓ |
| section_count | 65 | 65 | ✓ |
| Batch5 Fix Lite | 已完成 | - | ✓ |

## 2. v1 漏检原因分析

**根本原因**: v1 脚本仅按 `candidate_id` 精确匹配检查已合并候选，未检查候选名称与主图谱已有 item 名称的冲突。

**具体漏洞**:
- Stage3F Reserve pool 中 6 个 candidates 状态为 `reserve_for_stage3f`
- 它们实际已在 Stage3E Batch1~4 中以不同 `candidate_id` 合并到主图谱
- v1 脚本补充逻辑从 reserve pool 中选取了这些候选，但未识别它们是已合并的

**v1漏检的6个候选**:

| candidate_id | 已有item_id | 已有item_name | 漏检原因 |
|-------------|-------------|---------------|---------|
| cand.graph.matching_cover.stable_marriage | 2.21.143 | Stable Marriage | reserve pool标注为reserve_for_stage3f，但实际已合并 |
| cand.graph.matching_cover.minimum_path_cover | 2.21.142 | Minimum Path Cover | 同上 |
| cand.graph.matching_cover.dilworth_theorem | 2.21.138 | Dilworth Theorem | 同上 |
| cand.graph.matching_cover.konig_theorem | 2.21.140 | Konig Theorem | 同上 |
| cand.graph.matching_cover.weighted_general_matching | 2.21.145 | Weighted General Matching | 同上 |
| cand.graph.flow_bounds.minimum_flow | 2.21.129 | Minimum Flow | 同上 |

**v2修复措施**:
1. ✓ 严格按 `candidate_id` 在所有 mapping 文件中核查
2. ✓ 按名称检查是否与主图谱已有 item 名称冲突
3. ✓ 用户确认的 6 个已合并候选显式排除

## 3. v2 候选统计

| 来源 | 数量 | 说明 |
|------|------|------|
| v1 安全候选(保留) | 21 | v1中未重复、未冲突的候选 |
| v2 新补充(替换) | 4 | 从reserve pool中选取安全的候选 |
| **v2 总计** | **25** | |
| v1排除(已合并) | 6 | 6个已合并候选 |
| 排除(名称重复) | 3 | 名称与主图谱重复 |
| **目标达成** | **仅 25 个，推荐 fallback_24** | |

## 4. v2 入选候选列表

### 4.1 v1安全保留 (21 个)

| # | candidate_id | 名称 | section | 风险 |
|---|-------------|------|---------|------|
| 1 | cand.ds.li_chao_tree.on_tree | 李超线段树：On Tree | 3.13 | yellow |
| 2 | cand.ds.li_chao_tree.rollback | 李超线段树：回滚版 | 3.13 | yellow |
| 3 | cand.ds.heap_mergeable.lazy_deletion_heap | 可并堆：Lazy Deletion Heap | 3.13 | yellow |
| 4 | cand.ds.heap_mergeable.persistent_heap | 可并堆：Persistent Heap | 3.13 | yellow |
| 5 | cand.ds.segment_tree_beats.range_min_max_sum | Segment Tree Beats：Range Min Max Sum | 3.13 | yellow |
| 6 | cand.ds.heap_mergeable.heap_with_decrease_key | 可并堆：Heap With Decrease Key | 3.13 | yellow |
| 7 | cand.ds.heap_mergeable.double_ended_priority_queue | 可并堆：Double Ended Priority Queue | 3.13 | yellow |
| 8 | cand.ds.segment_tree_beats.range_modulo | Segment Tree Beats：Range Modulo | 3.13 | yellow |
| 9 | cand.ds.li_chao_tree.maximum_query | 李超线段树：Maximum Query | 3.13 | yellow |
| 10 | cand.ds.li_chao_tree.minimum_query | 李超线段树：Minimum Query | 3.13 | yellow |
| 11 | cand.ds.segment_tree_beats.beats_amortized_analysis | Segment Tree Beats：Beats Amortized Analysis | 3.13 | yellow |
| 12 | cand.ds.segment_tree_beats.beats_proof | Segment Tree Beats：Beats Proof | 3.13 | yellow |
| 13 | cand.ds.heap_mergeable.meldable_priority_queue | 可并堆：Meldable Priority Queue | 3.13 | yellow |
| 14 | cand.ds.segment_tree_beats.beats_with_assignment | Segment Tree Beats：Beats With Assignment | 3.13 | yellow |
| 15 | cand.ds.segment_tree_beats.second_maximum_invariant | Segment Tree Beats：Second Maximum Invariant | 3.13 | yellow |
| 16 | cand.ds.bitset_linear_basis.basis_on_tree | Bitset Linear Basis: Basis On Tree | 3.13 | green |
| 17 | cand.ds.dynamic_tree.cut_link_connectivity | Dynamic Tree: Cut Link Connectivity | 3.13 | green |
| 18 | cand.ds.dynamic_tree.dynamic_lca | Dynamic Tree: Dynamic Lca | 3.13 | green |
| 19 | cand.ds.dynamic_tree.path_lazy_tag | Dynamic Tree: Path Lazy Tag | 3.13 | green |
| 20 | cand.ds.dynamic_tree.reroot_query | Dynamic Tree: Reroot Query | 3.13 | green |
| 21 | cand.ds.dynamic_tree.virtual_subtree_aggregate | Dynamic Tree: Virtual Subtree Aggregate | 3.13 | green |

### 4.2 v2 新补充替换 (4 个)

| # | candidate_id | 名称 | section | 风险 | 理由 |
|---|-------------|------|---------|------|------|
| 1 | cand.ds.merge_sort_tree.2d_dominance | Merge Sort Tree: 2d Dominance | 3.13 | green | v2补充: 替换已合并候选 |
| 2 | cand.ds.multidimensional.bitset_rectangle_query | Multidimensional: Bitset Rectangle Query | 3.13 | green | v2补充: 替换已合并候选 |
| 3 | cand.ds.multidimensional.cdq_divide_conquer | Multidimensional: Cdq Divide Conquer | 3.13 | green | v2补充: 替换已合并候选 |
| 4 | cand.ds.multidimensional.dominance_counting | Multidimensional: Dominance Counting | 3.13 | green | v2补充: 替换已合并候选 |

## 5. 已排除候选

### 5.1 已合并候选 (6 个)

| # | candidate_id | 已有item_id | 原因 |
|---|-------------|-------------|------|
| 1 | cand.graph.matching_cover.stable_marriage | 2.21.143 | 已在Batch1~5中合并 |
| 2 | cand.graph.matching_cover.minimum_path_cover | 2.21.142 | 已在Batch1~5中合并 |
| 3 | cand.graph.matching_cover.dilworth_theorem | 2.21.138 | 已在Batch1~5中合并 |
| 4 | cand.graph.matching_cover.konig_theorem | 2.21.140 | 已在Batch1~5中合并 |
| 5 | cand.graph.matching_cover.weighted_general_matching | 2.21.145 | 已在Batch1~5中合并 |
| 6 | cand.graph.flow_bounds.minimum_flow | 2.21.129 | 已在Batch1~5中合并 |

## 6. v2 动态预审结果

| 检查项 | 结果 |
|--------|------|
| 是否与 Batch1~5 已合并重复 | 已排除 6 个，当前 v2 候选无重复 |
| 是否包含 high risk / red | 无 |
| 是否包含 manual_review | 无 |
| 是否包含 problem_patterns 优先候选 | 无 |
| 是否需要新 section | 否 |
| 是否存在 section id 依赖 | 否 |
| 是否存在候选依赖环 | 否 |
| dependency_cleanup_required | 否 |

### Section 分布

| Section | 数量 |
|---------|------|
| 3.13 | 25 |

## 7. 推荐结论

| 项目 | 结果 |
|------|------|
| **recommendation** | **use_fallback_24** |
| **recommended_merge_count** | **24** |
| **是否建议交给 1号线程合并** | 建议 fallback |
| **主图谱是否修改** | **否** |

**推荐 fallback_24（安全候选 25 个）**。

## 8. 替换候选分析

原 v1 中 6 个已合并候选全部来自匹配与覆盖/上下界网络流系列(2.21/2.15)。
v2 替换为以下 3.13 候选:

| 替换前(已合并) | 替换后(新候选) | 质量提升 |
|---------------|---------------|---------|
| stable_marriage (yellow, 2.15) | Merge Sort Tree 变体 (green, 3.13) | 风险降低 |
| minimum_path_cover (yellow, 2.21) | Merge Sort Tree 变体 (green, 3.13) | 风险降低 |
| dilworth_theorem (yellow, 2.21) | Multidimensional 变体 (green, 3.13) | 风险降低 |
| konig_theorem (yellow, 2.15) | Multidimensional 变体 (green, 3.13) | 风险降低 |
| weighted_general_matching (yellow, 2.21) | Multidimensional 变体 (green, 3.13) | 风险降低 |
| minimum_flow (yellow, 2.21) | Multicative 变体 (green, 3.13) | 风险降低 |

## 9. 下一步

1. 1号线程执行 Batch6 full_30 v2 Merge
2. Merge 后 validate-only 验证 (item_count = 1647)
3. 2号线程执行 Batch6 Review

---

*本预审不修改主图谱，仅输出修正后的候选计划和动态预审。*
