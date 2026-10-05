# Patterns Batch1 Fix Report

## Summary

- 修复前 pattern 总数：99
- 修复后 pattern 总数：99
- 应用 patch 数量：21
- needs_fix 实际修复数量：58
- merge_with_existing 处理数量：2
- move_to_knowledge_items 输出数量：5
- 修复后 A/B/C 数量：A=4, B=12, C=83
- required_items 无法映射数量：0
- related_items 无法映射数量：0
- 是否仍有重复 pattern：否
- 是否建议进入 Batch2：否，建议先人工确认 A/B 项后再开 Batch2。
- 主图谱是否被修改：否

## Flow Modeling

Flow Modeling 已收窄为 Basic Flow Modeling：只覆盖源汇、容量、守恒、最大流/可行流。Minimum Cut Selection、Bipartite Matching as Flow、Min-Cost Flow Assignment、Maximum Closure Project Selection 被标为子模式或相关模式；Lower-Bound Flow Modeling 未在 Batch1 中新增，明确留作后续单独模式。

## Tree Query Layering

Tree Query Patterns 已按题面特征分层：Tree Path Query 关注路径聚合/修改，LCA Query Pattern 保留为其子模式，Virtual Tree Key-Node Pattern 关注关键点压缩，Subtree Query with Euler Tour 关注子树连续区间，Rerooting Tree DP 明确归入 Tree DP 子模式而不是查询模板定义。

## Move To Knowledge Items Candidates

- pat.sparse_table_idempotent: Static Idempotent Range Query Candidate -> 数据结构 / RMQ
- pat.coordinate_compression: Coordinate Compression Pattern -> 基础技巧 / 离散化
- pat.kmp_string_matching: KMP String Matching -> 字符串算法
- pat.z_algorithm_pattern: Z Algorithm Pattern -> 字符串算法
- pat.manacher_palindrome: Manacher Palindrome Pattern -> 字符串算法

## Merge Or Deferred

- pat.trie_prefix_query: retain_as_subpattern -> pat.trie_multi_pattern; Trie 前缀查询与多模式前缀匹配近重复，但动态前缀计数场景仍有题型价值；暂保留为子模式，不删除。
- pat.lca_binary_lifting: retain_as_subpattern -> pat.tree_path_query; LCA 查询是树上路径查询的基础子模式；改名为 LCA Query Pattern，强调题型触发信号而不是倍增算法定义。

## Validation

- fixed JSON 合法：是
- pattern_id 不重复：是
- i18n_key 不重复：是
- 必需字段完整：是
- 枚举合法：是
- required_items 全部可映射：是
- related_items 全部可映射：是
- 未生成 Batch2：是
- 未修改主图谱：是

## Notes

本阶段只输出 fixed 文件和 patterns_ 前缀审计文件；move_to_knowledge_items 仅作为候选清单，不写入主图谱。
