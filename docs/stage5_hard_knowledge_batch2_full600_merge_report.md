# Stage5-HardKnowledge Batch2 full600 合并报告

- **生成时间**：2026-05-26T14:35:55Z
- **任务**：将 600 个硬知识候选合并到主图谱

---

## 1. 合并前检查（16 项全部通过）

| item_count_before_2640 | ✅ |
| section_count_65 | ✅ |
| recommendation_ready | ✅ |
| selected_candidate_count_600 | ✅ |
| recommended_merge_count_600 | ✅ |
| dependency_cleanup_required_false | ✅ |
| needs_new_section_false | ✅ |
| candidate_dependency_cycle_false | ✅ |
| excluded_duplicate_empty | ✅ |
| section_ref_dependencies_empty | ✅ |
| direct_pre_over_limit_empty | ✅ |
| whole_section_expansion_risk_empty | ✅ |
| manual_review_candidates_empty | ✅ |
| dp_2_to_6 | ✅ |
| no_whole_section_expansion | ✅ |

---

## 2. 合并摘要

| 指标 | 值 |
|:-----|:--|
| 合并前 item_count | **2,640** |
| 合并后 item_count | **3240** |
| 新增节点 | **600** |
| section_count | **65**（无新建 section） |

### 来源分布

| 来源 | 数量 |
|:-----|:--:|
| ready_core | 339 |
| reserve_useful | 261 |

### 分类分布

| 分类 | 数量 |
|:-----|:--:|
| 数学 | 200 |
| 数据结构 | 145 |
| 算法 | 255 |

### Section 分布（新增节点最多的 15 个 section）

| Section | 章节名 | 新增 |
|:-------|:-----|:--:|
| 2.20 | 交互题与构造题技巧 | 120 |
| 4.1 | 整数与数论基础 | 100 |
| 2.8 | 动态规划 | 78 |
| 3.13 | 高级数据结构扩展 | 76 |
| 4.3 | 计数与组合 | 64 |
| 2.1 | 基础算法思想 | 62 |
| 2.17 | 线性代数与插值专题 | 33 |
| 2.6 | 贪心 | 30 |
| 2.7 | 搜索 | 23 |
| 2.4 | 前缀、差分、离散化、分块 | 7 |
| 2.9 | 图基础与遍历 | 4 |
| 4.7 | 几何基础 | 3 |

### direct_pre 分布

| 前置数 | 候选数 |
|:--:|:--:|
| 2 | 157 |
| 3 | 292 |
| 4 | 123 |
| 5 | 24 |
| 6 | 4 |

### 子分类分布

| 子分类 | 数量 |
|:-------|:--:|
| 数论进阶 | 98 |
| 构造题硬知识 | 94 |
| DP优化 | 78 |
| 线段树进阶 | 62 |
| 数据结构嵌套 | 43 |
| 组合计数进阶 | 40 |
| 线性代数进阶 | 33 |
| 贪心模型 | 30 |
| 并查集扩展 | 29 |
| 交互题硬知识 | 26 |
| 多项式与生成函数 | 24 |
| 搜索进阶 | 23 |
| 根号算法 | 7 |
| 单调结构 | 4 |
| 图论建模 | 4 |
| 计算几何进阶 | 3 |
| 数论深水区 | 2 |

---

## 3. 验证结果

| 验证项 | 结果 | 状态 |
|:-------|:--:|:--:|
| item_count = 3,240 | 3240 | ✅ |
| section_count = 65 | 65 | ✅ |
| new_items = 600 | 600 | ✅ |
| dangling_refs = [] | 0 | ✅ |
| direct_pre section refs = 0 | 0 | ✅ |
| direct_pre > 8 | 0 | ✅ |
| direct_pre_cycle = null | None | ✅ |
| resolved_pre_mismatches = [] | 0 | ✅ |
| duplicate_ids = false | False | ✅ |
| product_metadata_validation | passed | ✅ |
| **passed** | **True** | **✅** |

---

## 4. 旧节点保护

| 检查项 | 结果 |
|:-------|:--|
| 旧 2640 节点 id 不变 | ✅ |
| 旧节点 name 未修改 | ✅ |
| 旧节点 direct_pre 未修改 | ✅ |
| 旧节点 rel 未修改 | ✅ |
| resolved_pre 旧节点变化 | 0 个（仅因新节点加入传递闭包） |
| 是否修改 io_v4_4.json | **否** |
| 是否修改内容包 | **否** |
| 是否修改前端代码 | **否** |
| 是否继续 Batch3 | **否** |
| 是否存在 direct_pre 整节展开 | **否** |

---

## 5. 输出文件

| # | 文件 |
|:-:|------|
| 1 | `data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json` |
| 2 | `data/stage5_hard_knowledge_batch2_full600_added_items_summary.json` |
| 3 | `data/stage5_hard_knowledge_batch2_full600_validation_result.json` |
| 4 | `data/stage5_hard_knowledge_batch2_full600_rollback_plan.json` |

## 6. 备份

```
backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch2_full600_20260526_223555.json
```

---

## 7. 建议

- ✅ **建议进入 Stage5-HardKnowledge Batch2 full600 Review**
- ❌ **不要继续 Batch3**
- 下一步：执行 Review / Fix Lite，再同步 io_v4_4.json 和生成内容包

---

*合并报告生成于 2026-05-26T14:35:55Z*
