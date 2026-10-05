# Stage3E Batch5 smaller_15 Review 模板

> **本模板由 2号线程 / GLM5 生成**
> 生成时间: 2026-05-25T10:00:00.000Z
> 说明：本模板为 Review 准备工作，实际 Review 需在 Batch5 Merge 完成后基于真实新增节点执行。

---

## 1. Batch5 基本信息

| 项目 | 内容 |
|------|------|
| Batch ID | stage3e_batch5_smaller15 |
| 预计新增节点数 | 15 |
| 预计新增 section | 3.13（高级数据结构扩展） |
| 预计 Merge 后 item_count | 1617 |
| 当前基线 item_count | 1602 |
| 预计新增 section_count | 65（无新 section） |
| 融合模式 | add_as_subtopic |
| 系列数 | 5 |
| 全部 risk_band | yellow |
| 无 section id 依赖 | ✓（动态预审已确认） |
| problem_patterns 无冲突 | ✓（与 sync_triage 已核对） |
| candidate_dependency_cycle | false |

### 1.1 系列分布

| 系列 | 候选数 | 类型倾向 |
|------|--------|---------|
| 高级并查集 | 1 | implementation_variant |
| 可并堆 | 5 | implementation_variant / core_concept |
| 李超线段树 | 4 | implementation_variant |
| Segment Tree Beats | 3 | implementation_variant / core_concept |
| 线段树变体 | 2 | implementation_variant |

### 1.2 预计新增节点列表

| # | candidate_id | 名称 | 系列 | direct_pre | 教育评分 |
|---|-------------|------|------|-----------|---------|
| 1 | cand.ds.dsu_advanced.undo_stack | 高级并查集：Undo Stack | 高级并查集 | 3.4.1 | 8 |
| 2 | cand.ds.heap_mergeable.binomial_heap | 可并堆：Binomial Heap | 可并堆 | 3.2.3 | 8 |
| 3 | cand.ds.heap_mergeable.fibonacci_heap | 可并堆：Fibonacci Heap | 可并堆 | 3.2.3 | 8 |
| 4 | cand.ds.heap_mergeable.leftist_heap | 可并堆：Leftist Heap | 可并堆 | 3.2.3 | 8 |
| 5 | cand.ds.heap_mergeable.pairing_heap | 可并堆：Pairing Heap | 可并堆 | 3.2.3 | 8 |
| 6 | cand.ds.heap_mergeable.skew_heap | 可并堆：Skew Heap | 可并堆 | 3.2.3 | 8 |
| 7 | cand.ds.li_chao_tree.coordinate_compressed | 李超线段树：Coordinate Compressed | 李超线段树 | 2.8.28, 3.7.2 | 8 |
| 8 | cand.ds.li_chao_tree.dynamic | 李超线段树：动态版 | 李超线段树 | 2.8.28, 3.7.2 | 8 |
| 9 | cand.ds.li_chao_tree.persistent | 李超线段树：可持久化版 | 李超线段树 | 2.8.28, 3.7.2 | 8 |
| 10 | cand.ds.li_chao_tree.segment_insertion | 李超线段树：Segment Insertion | 李超线段树 | 2.8.28, 3.7.2 | 8 |
| 11 | cand.ds.segment_tree_beats.historical_maximum | Segment Tree Beats：Historical Maximum | Segment Tree Beats | 3.7.2, 3.7.3 | 8 |
| 12 | cand.ds.segment_tree_beats.range_add_max | Segment Tree Beats：Range Add Max | Segment Tree Beats | 3.7.2, 3.7.3 | 8 |
| 13 | cand.ds.segment_tree_beats.range_chmin.codex1 | Segment Tree Beats：区间取 min 变体 1 | Segment Tree Beats | 3.7.2, 3.7.3 | 8 |
| 14 | cand.ds.segment_tree_variants.dynamic_segment_tree | 线段树变体：Dynamic Segment Tree | 线段树变体 | 3.7.2 | 7 |
| 15 | cand.ds.segment_tree_variants.gcd_segment_tree | 线段树变体：GCD Segment Tree | 线段树变体 | 3.7.2 | 7 |

---

## 2. Review 检查维度

### 2.1 核心质量检查（每节点必查）

| # | 维度 | 判断标准 | 可能的取值 |
|---|------|---------|-----------|
| 1 | 是否适合作为 knowledge_item | 节点是否有独立的教育/竞赛价值 | keep / needs_review / reject |
| 2 | 是否是 implementation_variant | 该节点是核心概念还是实现变体 | core / variant / unclear |
| 3 | 是否存在过度拆分 | 同系列多个节点是否有足够区分度 | ok / borderline / over_split |
| 4 | 是否与 3.7/3.10/3.13 已有节点重复 | 检查名称、语义、依赖关系 | no_overlap / partial_overlap / duplicate |
| 5 | direct_pre 是否合理 | direct_pre 数量、质量、是否过泛 | ok / too_few / too_broad / wrong |
| 6 | 是否应进入 problem_patterns | 是否有建模/识别信号价值 | keep_in_knowledge / sync_to_patterns / unclear |
| 7 | parent_concept 是否明确 | 父概念是否有清晰归属 | clear / weak / missing |
| 8 | learning_path_policy 是否合理 | 是否适合学习路径 | core / advanced_only / encyclopedia_only |
| 9 | review_priority 建议 | 后续复查等级 | A / B / C |

### 2.2 系列专项检查

#### 高级并查集（Undo Stack）
- 检查点：与已有 3.4.1（基本并查集）的区分度
- 检查点：Undo 操作在竞赛中的出现频率
- 检查点：是否应标记为 advanced_only

#### 可并堆系列（5个）
- 检查点：Binomial / Fibonacci / Leftist / Pairing / Skew Heap 是否各有独立教育价值
- 检查点：是否部分节点可降级为 C 级复查
- 检查点：Fibonacci Heap 的实现复杂度与竞赛实用性
- 检查点：Skew Heap 与 Leftist Heap 是否合并

#### 李超线段树系列（4个）
- 检查点：4 个变体的区分度
- 检查点：Persistent 李超树是否与 problem_patterns 同步冲突
- 检查点：Coordinate Compressed 与 Dynamic 是否可合并
- 检查点：所有变体的 direct_pre（2.8.28 斜率优化, 3.7.2 线段树）是否合适

#### Segment Tree Beats 系列（3个）
- 检查点：Historical Maximum / Range Add Max / Range Chmin 的核心价值
- 检查点：区间取 min 变体 1 是否过于具体
- 检查点：是否应增加 Beats 核心概念说明

#### 线段树变体系列（2个）
- 检查点：Dynamic Segment Tree 与 3.7.2 的区分度
- 检查点：GCD Segment Tree 是否重复（已有类似线段树节点）

---

## 3. Review 决策选项

每个节点给予以下review_decision之一：

| 决策 | 含义 | 后续行动 |
|------|------|---------|
| keep_as_core_item | 独立核心概念 | 保留，A级复查 |
| keep_as_implementation_variant | 有价值实现变体 | 保留，B级复查 |
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
| `data/stage3e_batch5_smaller15_added_items_review.json` | 15个新增节点的逐项审查结论 |
| `docs/stage3e_batch5_smaller15_added_items_review_report.md` | Review 完整报告 |
| `data/stage3e_batch5_smaller15_review_status_patch_preview.json` | review_status 补丁预览 |
| `data/stage3e_batch5_smaller15_dependency_fix_candidates.json` | 依赖修复候选 |
| `data/stage3e_batch5_smaller15_problem_pattern_sync_candidates.json` | Problem Patterns 同步候选 |
| `data/stage3e_batch5_smaller15_merge_or_collapse_candidates.json` | 合并/折叠候选 |

---

## 5. 预期质量参考

| 维度 | 预期 | 参考来源 |
|------|------|---------|
| Grade A 比例 | ~60%（9个） | 基于教育评分 >=8 的候选 |
| Grade B 比例 | ~40%（6个） | 教育评分 7 的变体 |
| Grade C/D/E 比例 | 0 | 较小变体已排除 |
| parent_concept clear | 100% | 全部为 3.13 |
| 需同步 problem_patterns | ~3~5 个 | Persistent Li Chao 等 |
| 需降为 C 级复查 | ~5~8 个 | 可并堆扩展等 |
| 需合并/折叠 | 0~2 个 | 最坏情况下 |

---

## 6. Review 注意事项

### 6.1 基于前序审计的经验

1. **1482→1602 审计结论**：整体 Grade A/B 占 94.2%，Batch5 候选选择延续了高质量标准
2. **39 个双重风险节点已分级**：P0-A = 3（已复核不阻塞），P0-B = 36
3. **problem_patterns sync 无冲突**：P0 sync 的 14 个已确认不与 Batch5 冲突
4. **section id 依赖已清除**：Batch5 动态预审已确认无 section id
5. **parent_concept 问题**：Batch1~4 中 parent weak 问题较多，Batch5 全部为 3.13 归属清晰

### 6.2 重点关注

- 可并堆 5 个节点是否真正都需要独立 item，还是其中部分可降级
- 李超线段树的 4 个变体界限是否清晰
- Segment Tree Beats 区间取 min 变体 1 是核心操作还是过度变体
- Dynamic Segment Tree 与 3.7.2 线段树的区别是否足够

### 6.3 Review Sequence

1. 先执行 validate-only 确认 Merge 后主图谱状态
2. 逐节点核查 added_items 信息
3. 填写 review_decision 和 quality_grade
4. 检查 direct_pre 是否完整
5. 标记 problem_patterns 同步候选
6. 标记合并/折叠候选（如果有）
7. 生成 review_status 补丁预览
8. 生成完整 Review 报告

---

*本模板不执行 Review，不修改主图谱。*
*待 Batch5 Merge 成功后基于真实新增节点执行 Review。*
