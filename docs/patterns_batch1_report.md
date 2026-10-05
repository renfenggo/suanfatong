# Problem Patterns Batch 1 Report

## Summary

- pattern 总数：99
- 主图谱是否被修改：否
- 输出范围：仅生成 patterns_ 前缀文件，未合并任何 candidate 到主图谱。
- thread2_problem_pattern_redirect_candidates.json：不存在，未读取到可同步项。

## Category Counts

- Interview Patterns: 20
- Graph/Search Patterns: 10
- Graph Modeling Patterns: 14
- DP Patterns: 17
- Data Structure Maintenance Patterns: 13
- Tree Query Patterns: 6
- String Matching Patterns: 8
- Competitive Modeling Patterns: 11

## Required Coverage Counts

- interview pattern 数量：20
- graph modeling pattern 数量：14
- DP pattern 数量：17
- data structure pattern 数量：13

## Stage3b Sync

- cand.graph.closure_model.project_selection / source_item_id=2.21.29 -> pat.project_selection_closure (synced_into_batch1)
- cand.graph.graph_modeling.difference_constraints / source_item_id=2.21.39 -> pat.difference_constraints_modeling (synced_into_batch1)

## Required Items Mapping

- required_items 是否有无法映射项：否
- 所有 required_items / related_items 均能在当前主图谱文本中通过 item id 找到。

## Manual Review Needed

- pat.two_sat_modeling (2-SAT Modeling)
- pat.project_selection_closure (Maximum Closure Project Selection)
- pat.automaton_dp (Automaton DP Pattern)
- pat.profile_dp (Profile DP Pattern)
- pat.persistent_segment_tree_kth (Persistent Segment Tree K-th)
- pat.divide_conquer_offline (Parallel Binary Search Pattern)

## Guardrails

- 未修改 merged_knowledge_graph_item_dependencies_refined.json
- 未修改 dependency_validation_result.json
- 未修改 item_dependency_refinement_report.md
- 未合并任何 candidate 到主图谱
