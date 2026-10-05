# Stage3F Batch3 Problem Patterns Sync Triage Template

## Usage

This template is used **after** Thread 2's Batch3 full_40 Review produces:

```
data/stage3f_batch3_full40_problem_pattern_sync_candidates.json
```

For each candidate in that file, run through the checklist below and produce a triage record.

---

## Input Sources

| Source | File | Status |
|:-------|:-----|:-------|
| Batch3 sync candidates | `data/stage3f_batch3_full40_problem_pattern_sync_candidates.json` | ⏳ pending from Thread 2 Review |
| Ready patterns (83) | `data/patterns_v0_1_ready.json` | ✅ loaded |
| Batch2 patterns (13) | `data/patterns_batch2.json` | ✅ generated |
| Batch2 patterns (full list) | `data/patterns_backlog_status_after_stage3f_batch2.json` | ✅ available |
| Dominance Counting | `data/patterns_order_statistics_suite_generation_checklist.json` | ✅ prepared |
| Knowledge graph | `merged_knowledge_graph_item_dependencies_refined.json` | ✅ available |

---

## Per-Candidate Triage Checklist

### Stage 1: Basic Info

| Field | Value |
|:------|:------|
| item_id | |
| name | |
| knowledge_item_type | |
| review_priority (from graph) | |
| source review result | |

### Stage 2: Duplicate Check

| # | Check | Result (pass / fail / note) |
|:-:|:------|:---------------------------|
| 1 | 是否与 ready patterns 重复（83 个中任意 ID 或语义重叠） | |
| 2 | 是否与 patterns_batch2 重复（13 个中任意 ID 或语义重叠） | |
| 3 | 是否与 Dominance Counting suite 相关或有重叠 | |
| 4 | 是否属于 modeling_pattern 而非纯知识点（core_concept / theorem / impl）| |

### Stage 3: Suitability Assessment

| # | Check | Result (Y / N / ?) |
|:-:|:------|:------------------|
| 5 | 是否有明确的识别信号（题面可据以识别该模式的线索） | |
| 6 | 是否有固定的转化路径（从问题到解法的建模步骤） | |
| 7 | 是否有多样化的建模选择（不止一种实现方式） | |
| 8 | 是否需要 boundary_note（与 ready/batch2 patterns 有语义重叠时） | |
| 9 | 是否需要人工复查 | |

### Stage 4: Decision

| Field | Value |
|:------|:------|
| **priority** | P0 / P1 / P2 / defer |
| **decision** | create_new_draft_later / merge_with_existing / defer / manual_review |
| **suggested_pattern_id** | |
| **matched_existing_pattern** | (if merge_with_existing) |
| **matched_batch2_pattern** | (if merge_with_existing) |
| **boundary_note_required** | true / false |
| **boundary_note_targets** | [list of pattern_ids] |
| **reason** | |

---

## Triage Decision Matrix

| decision | Meaning | Next Step |
|:---------|:--------|:----------|
| **create_new_draft_later** | Candidate is a valid modeling pattern, no existing coverage | Prepare draft preview → add to batch3 |
| **merge_with_existing** | Candidate is already covered by an existing pattern | Record merge target, no new pattern |
| **defer** | Candidate is algorithm-only, signal too narrow, or not suitable | Keep as knowledge item only |
| **manual_review** | Boundary unclear, needs human judgment | Flag for human reviewer |

## Priority Levels

| Priority | Meaning | Typical Criteria |
|:---------|:--------|:-----------------|
| **P0** | Must have | Core modeling pattern, broad coverage, B+ priority |
| **P1** | Should have | Clear modeling pattern, good coverage, B priority |
| **P2** | Nice to have | Niche but valid modeling pattern, C+ priority |
| **defer** | Not suitable | Algorithm-only, too narrow, or duplicate |

---

## Ready Patterns Reference (83, for duplicate check)

### Interview Patterns (20)
pat.two_sum, pat.three_sum, pat.prefix_sum_hashmap, pat.sliding_window_fixed_size, pat.sliding_window_variable, pat.fast_slow_pointer, pat.merge_intervals, pat.cyclic_sort, pat.top_k_frequent, pat.k_way_merge, pat.binary_search_on_answer, pat.binary_search_on_range, pat.binary_search_first_last, pat.monotonic_stack_smaller, pat.monotonic_stack_larger, pat.stack_simulation, pat.bracket_matching, pat.lru_cache_management, pat.linked_list_in_place_reversal, pat.heap_top_k

### Graph/Search Patterns (10)
pat.bfs_shortest_path_unweighted, pat.bfs_state_expansion, pat.bfs_multi_source, pat.bfs_grid_shortest_path, pat.dfs_connected_component, pat.dfs_backtracking, pat.dfs_memoization, pat.topological_sort_dependent, pat.topological_sort_dp, pat.union_find_connectivity

### Graph Modeling Patterns (14)
pat.shortest_path_modeling, pat.dijkstra_priority_queue, pat.bellman_ford_detection, pat.floyd_warshall_all_pairs, pat.minimum_spanning_tree, pat.max_flow_min_cut, pat.min_cut_selection, pat.bipartite_matching_modeling, pat.network_flow_modeling, pat.negative_cycle_detection, pat.dag_dp_modeling, pat.eulerian_path_modeling, pat.hamiltonian_path_modeling, pat.graph_coloring_modeling

### DP Patterns (17)
pat.linear_dp_sequence, pat.knapsack_01, pat.knapsack_unbounded, pat.knapsack_bounded, pat.lis_dp, pat.lcs_dp, pat.edit_distance_dp, pat.interval_dp, pat.tree_dp, pat.digit_dp, pat.bitmask_dp, pat.dp_on_tree_path, pat.dp_divide_and_conquer, pat.dp_knuth_optimization, pat.lucas_combination_mod, pat.state_compressed_bfs, pat.probability_ev_dp

### Data Structure Maintenance Patterns (13)
pat.fenwick_prefix_maintenance, pat.segment_tree_range_query, pat.segment_tree_lazy_propagation, pat.segment_tree_binary_search, pat.disjoint_set_union, pat.monotonic_queue_sliding, pat.square_root_decomposition, pat.order_statistic_maintenance, pat.trie_prefix_tree, pat.persistent_data_structure, pat.coordinate_sweep_compression, pat.randomized_hash_check, pat.prefix_xor_hashmap

### Tree Query Patterns (6)
pat.lca_binary_lifting, pat.tree_diameter, pat.tree_centroid, pat.tree_prefix_sum, pat.tree_mo_algorithm, pat.heavy_light_decomposition

### String Matching Patterns (8)
pat.kmp_prefix_function, pat.rolling_hash_substring, pat.suffix_array_lcp, pat.suffix_automaton, pat.aho_corasick_matching, pat.string_dp_wildcard, pat.z_function, pat.manacher_palindrome

### Competitive Modeling Patterns (11)
pat.offline_query_pattern, pat.sweep_line_pattern, pat.meet_in_the_middle, pat.constructive_invariant, pat.greedy_exchange_argument, pat.binary_lifting_state_jump, pat.modular_counting_pattern, pat.inclusion_exclusion_counting, pat.coordinate_sweep_compression, pat.randomized_hash_check, pat.lis_dp

---

## Batch2 Patterns Reference (13, for duplicate check)

| pattern_id | Title | Category |
|:-----------|:------|:---------|
| pat.circulation_optimization | 最小费用循环流 | 网络流建模 |
| pat.cycle_optimization_modeling | 最小平均环建模 | 图论建模 |
| pat.state_machine_modeling | 状态图建模 | 图论建模 |
| pat.path_cover_modeling | 最小路径覆盖 | 图论建模 |
| pat.bounded_matching_modeling | 带边界二分图匹配 | 网络流建模 |
| pat.flow_bounds_transformation | 流量边界变换 | 网络流建模 |
| pat.min_flow_modeling | 最小流建模 | 网络流建模 |
| pat.k_shortest_modeling | K短路建模 | 图论建模 |
| pat.layered_graph_modeling | 分层图建模 | 图论建模 |
| pat.node_demand_modeling | 节点需求流建模 | 网络流建模 |
| pat.max_flow_with_bounds | 带边界最大流 | 网络流建模 |
| pat.shortest_path_potentials | Johnson势函数 | 最短路优化 |
| pat.stable_matching_pattern | 稳定婚姻问题 | 匹配算法 |

**Merge action**: `2.21.131 Project Selection` → `pat.min_cut_selection` (no separate pattern)

---

## Dominance Counting Suite Reference

| Candidate | Status | Note |
|:----------|:-------|:-----|
| pat.dominance_counting (3.13.182) | ✅ prepared for batch3 | modeling_pattern, B级 |
| CDQ Divide Conquer (3.13.181) | ❌ defer | core_concept, 在 dominance counting 中引用 |
| MST 2D Dominance (3.13.179) | ❌ defer | implementation_variant |
| Bitset Rectangle Query (3.13.180) | ❌ defer | implementation_variant |

**Suite relationship**: If a Batch3 candidate is related to Order Statistics / multidimensional queries, check the suite plan first.

---

## Pending Triage Before Batch3

| Candidate | Source | Status |
|:----------|:-------|:-------|
| 4.9.5 莫比乌斯反演应用 | Stage3F Batch2 Review | ⏳ move_to_problem_patterns, not yet triaged |

If Batch3 Review also produces candidates related to number theory, consider triaging 4.9.5 together with them.

---

## Triage Output Format

Produce one record per candidate in `data/stage3f_batch3_problem_patterns_sync_triage.json`:

```json
{
  "item_id": "",
  "name": "",
  "suggested_pattern_id": "",
  "priority": "P0 | P1 | P2 | defer",
  "decision": "create_new_draft_later | merge_with_existing | defer | manual_review",
  "knowledge_item_type": "",
  "matched_existing_pattern": "",
  "matched_batch2_pattern": "",
  "boundary_note_required": true,
  "boundary_note_targets": [],
  "existing_coverage_assessment": {
    "ready_patterns_cover": false,
    "batch2_patterns_cover": false,
    "dominance_counting_suite_related": false,
    "overlap_with_existing": "none | partial | full",
    "overlap_detail": ""
  },
  "suitable_as_pattern": true,
  "suitable_reason": "",
  "recommended_timing": "",
  "reason": ""
}
```

---

## Declarations

| Item | Status |
|:-----|:-------|
| ✅ Template prepared | **True** |
| ❌ Generate formal patterns_batch3 now | **False** |
| ✅ Must wait for Stage3F Batch3 Review / Fix Lite | **True** |
| ❌ Modify main graph | **False** |
| ❌ Modify existing patterns | **False** |

---

*Template prepared by GLM5 (Thread 3). Apply after Thread 2 outputs `stage3f_batch3_full40_problem_pattern_sync_candidates.json`.*
