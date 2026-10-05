# Stage3E Batch6 medium_20 静态候选计划报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T10:30:00.000Z
- **任务**: Stage3E Batch6 medium_20 静态候选筛选
- **主图谱状态**: 未修改
- **本任务**: 仅静态筛选，不包含动态预审

## 1. 前提状态确认

| 项目 | 状态 |
|------|------|
| Batch5 smaller_15 Merge | 已完成 (1617) |
| Batch5 Review | 已完成 |
| 1号线程执行 Batch5 Fix Lite | 进行中 |
| **本任务** | **静态筛选，不依赖 Fix Lite 后图谱** |

## 2. 候选来源统计

| 来源 | 候选数 |
|------|--------|
| 原 batch_5 总候选 | 30 |
| smaller_15 已合并 | 15 |
| **batch_5 剩余候选人** | **15** |
| Stage3F Reserve 可用 3.13 候选 | 13 |
| Stage3F Reserve 可用其他候选 | 11 |
| **Batch6 目标选出** | **20** |

## 3. 入选 20 个候选列表

### 3.1 从 batch_5 剩余入选 (15 个)

| # | candidate_id | 名称 | 系列 | 风险 | 说明 |
|---|-------------|------|------|------|------|
| 1 | cand.ds.li_chao_tree.on_tree | 李超线段树：On Tree | 3.13 | yellow | medium_risk |
| 2 | cand.ds.li_chao_tree.rollback | 李超线段树：回滚版 | 3.13 | yellow | medium_risk |
| 3 | cand.ds.heap_mergeable.lazy_deletion_heap | 可并堆：Lazy Deletion Heap | 3.13 | yellow | medium_risk |
| 4 | cand.ds.heap_mergeable.persistent_heap | 可并堆：Persistent Heap | 3.13 | yellow | medium_risk |
| 5 | cand.ds.segment_tree_beats.range_min_max_sum | Segment Tree Beats：Range Min Max Sum | 3.13 | yellow | medium_risk |
| 6 | cand.ds.heap_mergeable.heap_with_decrease_key | 可并堆：Heap With Decrease Key | 3.13 | yellow | medium_risk |
| 7 | cand.ds.heap_mergeable.double_ended_priority_queue | 可并堆：Double Ended Priority Queue | 3.13 | yellow | medium_risk |
| 8 | cand.ds.segment_tree_beats.range_modulo | Segment Tree Beats：Range Modulo | 3.13 | yellow | medium_risk |
| 9 | cand.ds.li_chao_tree.maximum_query | 李超线段树：Maximum Query | 3.13 | yellow | medium_risk |
| 10 | cand.ds.li_chao_tree.minimum_query | 李超线段树：Minimum Query | 3.13 | yellow | medium_risk |
| 11 | cand.ds.segment_tree_beats.beats_amortized_analysis | Segment Tree Beats：Beats Amortized Analysis | 3.13 | yellow | medium_risk |
| 12 | cand.ds.segment_tree_beats.beats_proof | Segment Tree Beats：Beats Proof | 3.13 | yellow | medium_risk |
| 13 | cand.ds.heap_mergeable.meldable_priority_queue | 可并堆：Meldable Priority Queue | 3.13 | yellow | medium_risk |
| 14 | cand.ds.segment_tree_beats.beats_with_assignment | Segment Tree Beats：Beats With Assignment | 3.13 | yellow | medium_risk |
| 15 | cand.ds.segment_tree_beats.second_maximum_invariant | Segment Tree Beats：Second Maximum Invariant | 3.13 | yellow | medium_risk |

### 3.2 从 Stage3F Reserve 补充 (5 个)

| # | candidate_id | 名称 | target_section | 风险 | 说明 |
|---|-------------|------|---------------|------|------|
| 1 | cand.ds.bitset_linear_basis.basis_on_tree | Bitset Linear Basis: Basis On Tree | 3.13 | green | 低风险 |
| 2 | cand.ds.dynamic_tree.cut_link_connectivity | Dynamic Tree: Cut Link Connectivity | 3.13 | green | 低风险 |
| 3 | cand.ds.dynamic_tree.dynamic_lca | Dynamic Tree: Dynamic Lca | 3.13 | green | 低风险 |
| 4 | cand.ds.dynamic_tree.path_lazy_tag | Dynamic Tree: Path Lazy Tag | 3.13 | green | 低风险 |
| 5 | cand.ds.dynamic_tree.reroot_query | Dynamic Tree: Reroot Query | 3.13 | green | 低风险 |

## 4. 排除候选及原因

### 4.1 batch_5 剩余未入选 (0 个)

| # | candidate_id | 名称 | 排除原因 |
|---|-------------|------|---------|

## 5. 候选系列分布 (selected)

| 系列/Section | 数量 |
|-------------|------|
| 3.13 高级数据结构扩展 | 20 |
| 2.21 高级图论扩展 | 0 |
| 2.15 二分图匹配 | 0 |
| 其他 | 0 |

## 6. 静态风险标记

| 风险类型 | 数量 | 说明 |
|---------|------|------|
| section_ref_dependency | 0 | direct_pre 含 section 引用 |
| medium_risk (yellow) | 15 | 需要风险关注 |
| problem_patterns 风险 | 0 | 已核对 triage 文件，无重叠 |
| high/red 风险 | 0 | 未选择 |

## 7. 推荐行动

| 项目 | 建议 |
|------|------|
| 是否需要 dependency cleanup | 否 |
| 是否等 Batch5 Fix Lite 后做动态预审 | **是** |
| 下一步 | 1号线程完成 Batch5 Fix Lite → 2号线程执行 Batch6 动态预审 |
| 动态预审重点 | section id 依赖、候选重复、高危风险、环检测 |

## 8. 结论

```
总览:
  目标: 20 个
  实际筛选: 20 个
  ├─ 原 batch_5 剩余:  15 个
  └─ Stage3F Reserve: 5 个
  风险等级: 全部 green/yellow
  problem_patterns 冲突: 0
  主图谱修改: 否
```

**注意**:
- 本计划为静态筛选，只标记潜在风险，不执行 direct_pre 映射修复
- 建议等 1号线程 Batch5 Fix Lite 完成后，再执行动态预审
- 动态预审将确认 item_count、validate-only、section id 依赖、候选重复、环检测等
