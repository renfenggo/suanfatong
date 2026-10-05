# Patterns v0.1 Finalize Report

## Summary

- patterns_batch1_fixed 总数：99
- patterns_v0_1_ready 数量：83
- A/B 人工审核数量：16（A=4, B=12）
- move_to_knowledge_items 数量：5
- 是否有 required_items 无法映射：否
- 是否有 related_items 无法映射：否
- 是否有 pattern_id 重复：否
- 是否有 i18n_key 重复：否
- 是否建议进入 Batch2：否，A/B 未确认前不进入 Batch2。
- 主图谱是否被修改：否

## v0.1 Baseline

ready 数为 83，满足 ready >= 80 的规则，可将 patterns_v0_1_ready.json 作为第一版可用题型模式库基线。A/B 项保持在人工审核清单中，不阻塞 v0.1 基线试用，但阻塞 Batch2 数据生成。

## Category Distribution

- Interview Patterns: 20
- Graph/Search Patterns: 10
- Graph Modeling Patterns: 14
- DP Patterns: 17
- Data Structure Maintenance Patterns: 13
- Tree Query Patterns: 6
- String Matching Patterns: 8
- Competitive Modeling Patterns: 11

## Path Counts

- beginner 路径数量：20
- interview 路径数量：30
- icpc 路径数量：79
- noi 路径数量：11

## Manual Review

- A 优先级：4
- B 优先级：12
- 主要类型：Flow 层级拆分、2-SAT 映射确认、Trie/LCA 子模式确认、若干算法项迁移到 knowledge_items。

## Move To Knowledge Items Handoff

- pat.sparse_table_idempotent: Static Idempotent Range Query Candidate -> 数据结构 / RMQ
- pat.coordinate_compression: Coordinate Compression Pattern -> 基础技巧 / 离散化
- pat.kmp_string_matching: KMP String Matching -> 字符串算法
- pat.z_algorithm_pattern: Z Algorithm Pattern -> 字符串算法
- pat.manacher_palindrome: Manacher Palindrome Pattern -> 字符串算法

## Batch2 Planning Only

- 补齐 Flow Modeling 子模式：Lower-Bound Flow、Max Flow Feasibility、Min-Cut Selection Variants。
- 补齐图论建模高级套路：matching cover、cut/closure variants、state graph with resources。
- 补齐 DP 高级模式：斜率优化、四边形不等式、插头/连通性 DP 的细分边界。
- 补齐字符串题型层：多模式统计、周期/Border 建模、后缀结构查询模式。
- 补齐数据结构维护层：动态区间第 k、可撤销结构、时间分治、二维离线查询。

## Guardrails

- 未覆盖 patterns_batch1_fixed.json。
- 未修改 merged_knowledge_graph_item_dependencies_refined.json。
- 未修改 knowledge_items。
- 未修改 dependency_validation_result.json。
- 未修改 item_dependency_refinement_report.md。
- 未生成 Batch2 数据。
