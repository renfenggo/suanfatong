# Patterns Batch1 Review Report

## Summary

- pattern 总数：99
- approve 数量：27
- needs_fix 数量：58
- duplicate 数量：0
- merge_with_existing 数量：2
- move_to_knowledge_items 数量：5
- keep_manual_review 数量：7
- required_items 问题数量：0
- 主图谱是否被修改：否
- 是否建议进入 Patterns Batch1 Fix：是
- 是否建议开始 Batch2：否，建议先完成 Batch1 Fix 后再开 Batch2。

## Key Findings

- Two Sum Pattern 与 Prefix Sum + HashMap 不重复：前者是 pair complement lookup，后者是 subarray prefix-difference counting。
- Sliding Window Fixed / Variable 边界基本正确，但建议在 Fix 中强化 fixed length vs feasibility-driven shrink 的描述。
- Binary Search on Answer 的 required_items 可接受，不应把每类 check 算法放入 required_items。
- Difference Constraints Modeling 已作为 stage3b 同步 pattern 保留，建议显式声明不重复合并 knowledge_item。
- Flow Modeling 过宽，需要拆清最大流基础、最小割选择、最大权闭合、费用流；上下界流不应塞入当前基础 Flow Modeling。
- DP Patterns 主体区分清楚：背包、区间、树形、数位、自动机、状压、轮廓线均可保留，但 Automaton/Profile 需要人工审核措辞。
- Tree Query Patterns 中 Tree Path Query 与 LCA/HLD/Virtual Tree 的层级关系需要在 Fix 中写清。
- Data Structure Maintenance Patterns 中部分条目偏 knowledge_item，尤其 ST 表、坐标离散化、KMP/Z/Manacher 类算法命名。

## Duplicate / Near-Duplicate Patterns

- pat.two_sum <-> pat.prefix_sum_hashmap: not_duplicate; Two Sum uses complement existence for one/two indices; Prefix Sum + HashMap uses historical prefix counts for subarray sums. They share HashMap but recognition signals and transforms are different.
- pat.sliding_window_fixed_size <-> pat.sliding_window_variable_size: not_duplicate; Fixed window has invariant length k and one-in/one-out updates; variable window relies on monotone feasibility and left contraction.
- pat.flow_modeling <-> pat.min_cut_selection: near_duplicate; Flow Modeling is a broad umbrella while Minimum Cut Selection is a specific max-flow/min-cut transform; keep both only if Flow Modeling is made explicitly introductory.
- pat.flow_modeling <-> pat.project_selection_closure: near_duplicate; Maximum Closure Project Selection is a specialized min-cut modeling pattern synced from stage3b; Flow Modeling should not duplicate its selection/dependency details.
- pat.flow_modeling <-> pat.min_cost_flow_assignment: not_duplicate; Min-cost Flow Assignment adds cost objective and assignment/transport signals, separate from capacity-only flow modeling.
- pat.shortest_path_modeling <-> pat.layered_graph_shortest_path: near_duplicate; Layered Graph Shortest Path is a common specialization of shortest-path modeling for limited special operations; keep as child pattern.
- pat.grid_graph_modeling <-> pat.island_problems: near_duplicate; Grid Graph Modeling is general state-to-node modeling; Island Problems is a connected-component family on binary grids.
- pat.dag_dependency_modeling <-> pat.course_schedule: near_duplicate; Course Schedule is an interview-facing DAG dependency case; DAG Dependency Modeling is a broader competitive modeling pattern.
- pat.trie_prefix_query <-> pat.trie_multi_pattern: near_duplicate; Both center on Trie prefixes; one is data-structure maintenance, the other string multi-pattern matching. Needs clearer boundary or merge in fix phase.
- pat.kmp_string_matching <-> pat.z_algorithm_pattern: near_duplicate; Both solve single-pattern string matching; KMP and Z are different transforms but may be too algorithm-item-like without stronger problem signals.
- pat.knapsack_dp <-> pat.complete_knapsack_dp: not_duplicate; 0/1 versus unbounded item reuse has different loop direction and recognition signals.
- pat.tree_path_query <-> pat.lca_binary_lifting: near_duplicate; Tree Path Query uses LCA/HLD/segment tree as a combined query pattern; LCA Binary Lifting is a prerequisite technique and may be closer to knowledge_item.
- pat.tree_dp <-> pat.rerooting_tree_dp: near_duplicate; Rerooting is a distinct all-roots extension of tree DP; keep but clarify parent/child relationship.
- pat.coordinate_compression <-> pat.coordinate_sweep_compression: near_duplicate; Coordinate Compression alone is mostly a technique/knowledge item; compressed coordinate sweep is a clearer competitive pattern.

## Priority Fix List

- [B] pat.sliding_window_fixed_size: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [B] pat.sliding_window_variable_size: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [B] pat.binary_search_on_answer: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [B] pat.difference_constraints_modeling: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [A] pat.flow_modeling: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [A] pat.two_sat_modeling: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [B] pat.project_selection_closure: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [B] pat.automaton_dp: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [B] pat.profile_dp: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [B] pat.persistent_segment_tree_kth: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [A] pat.sparse_table_idempotent: move_to_knowledge_items; Entry is currently phrased as an algorithm/data-structure technique rather than a reusable problem-pattern family.
- [A] pat.trie_prefix_query: merge_with_existing; Boundary overlaps with a broader existing pattern and should be merged or made explicitly subordinate.
- [A] pat.coordinate_compression: move_to_knowledge_items; Entry is currently phrased as an algorithm/data-structure technique rather than a reusable problem-pattern family.
- [B] pat.tree_path_query: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [B] pat.lca_binary_lifting: merge_with_existing; Boundary overlaps with a broader existing pattern and should be merged or made explicitly subordinate.
- [B] pat.virtual_tree_pattern: needs_fix; Pattern is useful but needs clearer boundary, mapping, or wording before final acceptance.
- [B] pat.kmp_string_matching: move_to_knowledge_items; Entry is currently phrased as an algorithm/data-structure technique rather than a reusable problem-pattern family.
- [B] pat.z_algorithm_pattern: move_to_knowledge_items; Entry is currently phrased as an algorithm/data-structure technique rather than a reusable problem-pattern family.
- [B] pat.suffix_array_lcp_query: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.
- [B] pat.manacher_palindrome: move_to_knowledge_items; Entry is currently phrased as an algorithm/data-structure technique rather than a reusable problem-pattern family.
- [B] pat.divide_conquer_offline: keep_manual_review; Valuable pattern, but needs human confirmation of item mapping, naming, or layer boundary before applying fixes.

## Stage3b Sync Check

- cand.graph.closure_model.project_selection -> pat.project_selection_closure: synced_into_batch1
- cand.graph.graph_modeling.difference_constraints -> pat.difference_constraints_modeling: synced_into_batch1

## Required Items Review

- 无 required_items 无法映射项。
- 主要问题不是映射失败，而是若干 related_items 使用了通用占位项，建议 Batch1 Fix 替换为更具体的邻接知识点。

## Guardrails

- 未修改 merged_knowledge_graph_item_dependencies_refined.json。
- 未修改 knowledge_items。
- 未生成第二批 pattern。
- 本次只生成 review 与 patch preview，未应用 patch。
