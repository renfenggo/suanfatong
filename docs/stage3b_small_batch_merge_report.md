# Stage 3B Small Batch Merge Report

- Backup success: True
- Backup file: `C:\Users\renfenggo\Documents\trae_projects\suanfatong\backups\merged_knowledge_graph_item_dependencies_refined_before_stage3b.json`
- Before item_count: 1349
- After item_count: 1421
- Actual added item count: 72
- Metadata-only candidate count: 0
- Created new section count: 1
- Created section: `3.13` 高级数据结构扩展 (数据结构)
- Section id conflict found: False
- Section conflict handling: []
- add_new merged count: 64
- add_as_subtopic handled count: 8
- Dangling refs count: 0
- direct_pre cycle: None
- resolved_pre mismatch count: 0
- validation passed: True
- Low-confidence review table sync needed: yes, add 72 new candidate-origin rows in a later review pass

## add_as_subtopic Handling
- `cand.graph.offline_dynamic_connectivity.seg_divide` -> `2.21.36`: added_as_new_item_with_parent_concept (2.9.1 图论)
- `cand.graph.flow_bounds.feasible_circulation` -> `2.21.37`: added_as_new_item_with_parent_concept (2.16.3 上下界网络流)
- `cand.graph.matching_cover.blossom_algorithm` -> `2.21.38`: added_as_new_item_with_parent_concept (2.15.1 匹配与覆盖)
- `cand.graph.graph_modeling.difference_constraints` -> `2.21.39`: added_as_new_item_with_parent_concept (2.9.1 图论建模)
- `cand.ds.segment_tree_variants.merge` -> `3.13.33`: added_as_new_item_with_parent_concept (3.7.2 线段树变体)
- `cand.ds.li_chao_tree.static` -> `3.13.34`: added_as_new_item_with_parent_concept (2.8.109 李超线段树)
- `cand.ds.wavelet_tree.range_kth` -> `3.13.35`: added_as_new_item_with_parent_concept (3.7.2 小波树)
- `cand.ds.dsu_advanced.rollback` -> `3.13.36`: added_as_new_item_with_parent_concept (3.4.1 高级并查集)

## Manual Review Needed
- All Stage3B added nodes keep `review_status.need_manual_review = true`.
- Prioritize add_as_subtopic nodes and raw-cleaned DeepSeek candidates before expanding the next batch.
