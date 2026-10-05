# Stage3E Batch6 full_30 Review 模板

> **本模板由 2号线程 / GLM5 生成**
> 生成时间: 2026-05-25T10:40:00.000Z
> 说明：本模板为 Review 准备工作，实际 Review 需在 Batch6 Merge 完成后基于真实新增节点执行。

---

## 1. Batch6 基本信息

| 项目 | 内容 |
|------|------|
| Batch ID | stage3e_batch6_full30 |
| 预计新增节点数 | 30 |
| 预计 Merge 后 item_count | 1617 → **1647** |
| 预计 section_count | 65（无新 section） |
| 涉及 section | **3.13**（21 个）、**2.21**（7 个）、**2.15**（2 个） |

### 1.1 系列分布

| 系列组 | 候选数 | 所属 section | 来源 |
|--------|--------|-------------|------|
| 李超线段树变体 | 4 | 3.13 | batch5 剩余 |
| 可并堆变体 | 5 | 3.13 | batch5 剩余 |
| Segment Tree Beats 变体 | 6 | 3.13 | batch5 剩余 |
| Dynamic Tree 系列 | 5 | 3.13 | Stage3F Reserve |
| Bitset Linear Basis | 1 | 3.13 | Stage3F Reserve |
| 匹配与覆盖 | 5 | 2.21 / 2.15 | Stage3F Reserve |
| 上下界网络流 | 2 | 2.21 | Stage3F Reserve |
| 图论闭合子图 | 2 | 2.21 | Stage3F Reserve（已替换已合并候选） |

### 1.2 预计新增节点列表

**3.13 高级数据结构扩展（21 个）**

| # | candidate_id | 名称 | 系列 |
|---|-------------|------|------|
| 1 | cand.ds.li_chao_tree.on_tree | 李超线段树：On Tree | 李超线段树 |
| 2 | cand.ds.li_chao_tree.rollback | 李超线段树：回滚版 | 李超线段树 |
| 3 | cand.ds.li_chao_tree.maximum_query | 李超线段树：Maximum Query | 李超线段树 |
| 4 | cand.ds.li_chao_tree.minimum_query | 李超线段树：Minimum Query | 李超线段树 |
| 5 | cand.ds.heap_mergeable.lazy_deletion_heap | 可并堆：Lazy Deletion Heap | 可并堆 |
| 6 | cand.ds.heap_mergeable.persistent_heap | 可并堆：Persistent Heap | 可并堆 |
| 7 | cand.ds.heap_mergeable.heap_with_decrease_key | 可并堆：Heap With Decrease Key | 可并堆 |
| 8 | cand.ds.heap_mergeable.double_ended_priority_queue | 可并堆：Double Ended Priority Queue | 可并堆 |
| 9 | cand.ds.heap_mergeable.meldable_priority_queue | 可并堆：Meldable Priority Queue | 可并堆 |
| 10 | cand.ds.segment_tree_beats.range_min_max_sum | Beats：Range Min Max Sum | Segment Tree Beats |
| 11 | cand.ds.segment_tree_beats.range_modulo | Beats：Range Modulo | Segment Tree Beats |
| 12 | cand.ds.segment_tree_beats.beats_amortized_analysis | Beats：Beats Amortized Analysis | Segment Tree Beats |
| 13 | cand.ds.segment_tree_beats.beats_proof | Beats：Beats Proof | Segment Tree Beats |
| 14 | cand.ds.segment_tree_beats.beats_with_assignment | Beats：Beats With Assignment | Segment Tree Beats |
| 15 | cand.ds.segment_tree_beats.second_maximum_invariant | Beats：Second Maximum Invariant | Segment Tree Beats |
| 16 | cand.ds.dynamic_tree.cut_link_connectivity | Dynamic Tree: Cut Link Connectivity | Dynamic Tree |
| 17 | cand.ds.dynamic_tree.dynamic_lca | Dynamic Tree: Dynamic Lca | Dynamic Tree |
| 18 | cand.ds.dynamic_tree.path_lazy_tag | Dynamic Tree: Path Lazy Tag | Dynamic Tree |
| 19 | cand.ds.dynamic_tree.reroot_query | Dynamic Tree: Reroot Query | Dynamic Tree |
| 20 | cand.ds.dynamic_tree.virtual_subtree_aggregate | Dynamic Tree: Virtual Subtree Aggregate | Dynamic Tree |
| 21 | cand.ds.bitset_linear_basis.basis_on_tree | Bitset Linear Basis: Basis On Tree | Bitset Linear Basis |

**2.21 高级图论扩展（7 个）**

| # | candidate_id | 名称 | 系列 |
|---|-------------|------|------|
| 22 | cand.graph.matching_cover.minimum_path_cover | 匹配与覆盖：Minimum Path Cover | 匹配与覆盖 |
| 23 | cand.graph.matching_cover.dilworth_theorem | 匹配与覆盖：Dilworth Theorem | 匹配与覆盖 |
| 24 | cand.graph.matching_cover.blossom_algorithm | 匹配与覆盖：Blossom Algorithm | 匹配与覆盖 |
| 25 | cand.graph.matching_cover.weighted_general_matching | 匹配与覆盖：Weighted General Matching | 匹配与覆盖 |
| 26 | cand.graph.flow_bounds.demands | 上下界网络流：Demands | 上下界网络流 |
| 27 | cand.graph.flow_bounds.edge_lower_bound_transform | 上下界网络流：Edge Lower Bound Transform | 上下界网络流 |
| 28 | cand.graph.flow_bounds.minimum_flow | 上下界网络流：Minimum Flow | 上下界网络流 |

**2.15 二分图匹配（2 个）**

| # | candidate_id | 名称 | 系列 |
|---|-------------|------|------|
| 29 | cand.graph.matching_cover.stable_marriage | 匹配与覆盖：Stable Marriage | 匹配与覆盖 |
| 30 | cand.graph.matching_cover.konig_theorem | 匹配与覆盖：Konig Theorem | 匹配与覆盖 |

---

## 2. Review 检查维度

### 2.1 核心质量检查（每节点必查）

| # | 维度 | 判断标准 | 可能的取值 |
|---|------|---------|-----------|
| 1 | 是否适合作为 knowledge_item | 节点是否有独立的教育/竞赛价值 | keep / needs_review / reject |
| 2 | 是否是 implementation_variant | 该节点是核心概念还是实现变体 | core / variant / modeling / theorem |
| 3 | 是否存在过度拆分 | 同系列多个节点是否有足够区分度 | ok / borderline / over_split |
| 4 | 是否与已有节点重复 | 检查名称、语义、依赖关系 | no_overlap / partial_overlap / duplicate |
| 5 | direct_pre 是否合理 | direct_pre 数量、质量、是否过泛 | ok / too_few / too_broad / wrong |
| 6 | 是否应进入 problem_patterns | 是否有建模/识别信号价值 | keep_in_knowledge / sync_to_patterns / unclear |
| 7 | parent_concept 是否明确 | 父概念是否有清晰归属 | clear / weak / missing |
| 8 | learning_path_policy 是否合理 | 是否适合学习路径 | core / advanced_only / encyclopedia_only |
| 9 | review_priority 建议 | 后续复查等级 | A / B / C |

### 2.2 系列专项检查

#### 李超线段树变体（4 个）
- **On Tree**：树上李超树的独立价值是否足够 vs 基本李超树 + 树剖
- **Rollback**：回滚功能的竞赛出现频率
- **Maximum Query vs Minimum Query**：与已合并的 Dynamic / CC 版是否界限清晰
- **过度拆分风险**：4 个变体是否都应该独立存在

#### 可并堆变体（5 个）
- **Lazy Deletion Heap**：懒删除的实用性 vs 标准堆
- **Persistent Heap**：可持久化堆的竞赛出现频率
- **Heap With Decrease Key**：decrease-key 是否仅为 Fibonacci 的配套操作
- **Double Ended Priority Queue**：与双端队列 3.2.3 的关系
- **Meldable Priority Queue**：抽象概念 vs 具体实现
- **过度拆分风险**：5 个可并堆变体是否部分可合并

#### Segment Tree Beats 变体（6 个）
- **Beats Amortized Analysis / Beats Proof**：这 2 个是理论概念而非算法实现，是否更适合作为 theorem_or_property 而不是 implementation_variant
- **Beats With Assignment / Second Maximum Invariant / Range Modulo**：竞赛中使用频率
- **Range Min Max Sum**：与已合并的 Historical Max / Range Add Max / Range Chmin 的关系
- **过度拆分风险**：6 个 Beats 变体是 Batch6 中最大的过度拆分风险组

#### Dynamic Tree 系列（5 个）
- **Cut Link Connectivity / Dynamic LCA / Path Lazy Tag / Reroot Query / Virtual Subtree Aggregate**：5 个 Dynamic Tree 操作变体是否各有独立教育价值
- **与已有 3.13 节点的关系**：确认无重复
- **竞赛频率**：Dynamic Tree 整体为高级内容，确认 advanced_only

#### Bitset Linear Basis: Basis On Tree
- **与 3.13 已有线性基节点的关系**：确认不重复
- **树上线性基的独立价值**：与静态线性基的区分度

#### 匹配与覆盖 + 上下界网络流（7 个，2.21/2.15）
- **Stable Marriage**：独立算法，确认无重复
- **Minimum Path Cover / Dilworth Theorem**：两个偏序相关节点，是否可合并或同步 patterns
- **Blossom Algorithm**：一般图最大匹配的经典算法，确认复杂度说明
- **Konig Theorem**：属于 theorem，确认 item_type
- **Weighted General Matching**：高级匹配算法，确认竞赛实用性
- **上下界网络流 Demands / Edge Lower Bound Transform / Minimum Flow**：三个上下界变体，确认与 2.16.3 网络流基础的区分度

---

## 3. Review 决策选项

每个节点给予以下 review_decision 之一：

| 决策 | 含义 | 后续行动 |
|------|------|---------|
| keep_as_core_item | 独立核心概念 | 保留，A 级复查 |
| keep_as_implementation_variant | 有价值实现变体 | 保留，B 或 C 级复查 |
| keep_as_theorem_or_property | 定理/性质节点 | 保留，C 级复查 |
| keep_as_application_case | 应用案例 | 保留，挂载父概念 |
| sync_to_problem_patterns | 同步到 patterns | 保留，额外同步 |
| collapse_to_parent | 合并到父节点 | 折叠为 subtopic |
| merge_with_existing | 与已有节点合并 | 删除或合并 ID |
| reject_later | 暂不采纳 | 从图谱移除 |
| needs_expert_review | 需要专家复查 | B/A 级审查 |

---

## 4. Review 输出文件列表

Merge 成功后，Review 阶段应生成以下文件：

| 文件 | 说明 |
|------|------|
| `data/stage3e_batch6_full30_added_items_review.json` | 30 个新增节点的逐项审查结论 |
| `docs/stage3e_batch6_full30_added_items_review_report.md` | Review 完整报告 |
| `data/stage3e_batch6_full30_review_status_patch_preview.json` | review_status 补丁预览 |
| `data/stage3e_batch6_full30_dependency_fix_candidates.json` | 依赖修复候选 |
| `data/stage3e_batch6_full30_problem_pattern_sync_candidates.json` | Problem Patterns 同步候选 |
| `data/stage3e_batch6_full30_merge_or_collapse_candidates.json` | 合并/折叠候选 |

---

## 5. 预期质量参考

| 维度 | 预期 | 说明 |
|------|------|------|
| Grade A 保留 | ~2~4 个 | Blossom Algorithm / Dilworth Theorem 等独立理论节点 |
| Grade B 保留 | ~6~8 个 | Dynamic Tree 系列 / Stable Marriage / Konig Theorem |
| 降为 C | ~18~22 个 | 批量化 implementation_variant |
| parent_concept clear | 30/30 | 全部归属 3.13/2.21/2.15 |
| 需同步 problem_patterns | ~2~4 个 | 匹配建模类最可能 |
| 需合并/折叠 | ~2~4 个 | Beats 理论节点（Amortized Analysis / Proof）最可能 |
| 需依赖修复 | 0 | 动态预审已确认无 section 引用 |

**需要注意的过度拆分风险组**：
1. **Segment Tree Beats 6 个变体**：Amortized Analysis 和 Proof 可能更适合作为 theorem_or_property 或 collapse
2. **可并堆 5 个变体**：Heap With Decrease Key 可能可合并到 Fibonacci Heap；Meldable Priority Queue 可能过于抽象
3. **李超线段树 4 个变体**：Maximum Query / Minimum Query 可能与 Dynamic 版区别不明显

---

## 6. Review 注意事项

### 6.1 基于前序审计的经验

1. **Batch6 候选质量对比 Batch5 较低**：前 15 个（原 batch5 剩余 yellow）教育区分度低于已合并的 smaller_15，需更严格复查
2. **首次引入多 section**：2.15 和 2.21 为首次跨 section 扩展，需确认 parent_concept 归属
3. **Dynamic Tree 系列为全新子领域**：5 个操作变体需确认是否有足够的独立性
4. **problem_patterns 冲突**：已核对 sync_triage P0/P1 列表，确认无直接冲突
5. **2 个已合并替换候选**（binary_decision_model / maximum_weight_closure 已被替换），替换后的候选需特别关注

### 6.2 重点关注

- Beats Amortized Analysis / Beats Proof → 是否应改为 theorem_or_property
- Heap With Decrease Key → 是否可合并到 Fibonacci Heap
- Meldable Priority Queue → 是否为过度抽象
- Maximum Query / Minimum Query → 与 Dynamic 版的区分度
- Dynamic Tree 5 个变体 → 是否可降为 3 个核心操作
- 上下界网络流 3 个变体 → 区分度评估

### 6.3 Review Sequence

1. 先执行 validate-only 确认 Merge 后主图谱状态
2. 确认 item_count = 1647，section_count = 65
3. 逐节点核查 added_items 信息
4. 优先复查过度拆分风险组（Beats / 可并堆 / 李超树）
5. 再复查新系列（Dynamic Tree / 匹配与覆盖 / 上下界网络流）
6. 填写 review_decision 和 quality_grade
7. 检查 direct_pre 是否完整
8. 标记 problem_patterns 同步候选
9. 标记合并/折叠候选
10. 生成 review_status 补丁预览
11. 生成完整 Review 报告

---

*本模板不执行 Review，不修改主图谱。*
*待 Batch6 Merge 成功后基于真实新增节点执行 Review。*
