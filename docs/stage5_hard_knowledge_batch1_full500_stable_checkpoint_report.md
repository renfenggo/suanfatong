# Stage5-HardKnowledge Batch1 full500 Stable Checkpoint 报告

- **生成时间**: 2026-05-26T08:20:00.000Z
- **检查点类型**: Stable Checkpoint
- **主图谱是否修改**: 否
- **io_v4_4.json 是否修改**: 否
- **前端代码是否修改**: 否
- **Batch2 是否继续**: 否

---

## 1. Batch1 full500 完整流水线

| 阶段 | 操作 | item_count | 通过 | 备份文件 |
|:----|:-----|:---------:|:---:|:--------|
| **初始基线** | — | 2,165 | — | — |
| **Merge** | +500 候选节点合并 | 2,165 → **2,665** | ✅ | `backups/..._before_stage5_hard_batch1_full500.json` |
| **Branch B Fix** | -25 模板化子节点折叠 + 282 节点 direct_pre 缩减 | 2,665 → **2,640** | ✅ | `backups/..._before_stage5_hard_batch1_full500_branch_b_fix.json` |
| **Fix Lite** | 475 节点 review 字段更新（B=7, C=468） | 2,640 → **2,640** | ✅ | `backups/..._before_stage5_hard_batch1_full500_fix_lite.json` |
| **Stable Checkpoint** | 只读快照 | **2,640** | ✅ | — |

### 净变化

- full500 原始合并：**500**
- 合并/折叠删除：**−25**
- 净新增 Stage5 节点：**475**
- 旧 2165 节点保留：**2,165**（未修改）
- **总节点数：2,640**

---

## 2. 当前稳定状态

| 指标 | 值 | 验证结果 |
|:-----|:--:|:-------:|
| item_count | **2,640** | ✅ |
| section_count | **65** | ✅ |
| dangling_refs | [] | ✅ |
| direct_pre_cycle | null | ✅ |
| section refs in direct_pre | 0 | ✅ |
| duplicate item_ids | 0 | ✅ |
| resolved_pre_mismatches | 0 | ✅ |
| product_metadata_validation | passed | ✅ |
| old_2165 nodes modified | 0 | ✅ |
| direct_pre/resolved_pre/rel modified | false | ✅ |
| **validate-only passed** | **true** | ✅ |

---

## 3. 优先级分布

| 优先级 | 数量 | 说明 |
|:-----:|:---:|:-----|
| **B** | **7** | 7 个 keeper 父主题节点（DP 优化专题父节点） |
| **C** | **468** | 普通 Stage5 Batch1 节点，依赖已缩减、review 已标记 |
| **A** | **0** | — |

---

## 4. 分类分布（净新增 475 节点）

| 分类 | 原始合并 | 折叠后净增 |
|:-----|:-------:|:--------:|
| 算法 | 210 | +210 |
| 数据结构 | 120 | +120 |
| 数学 | 170 | +170 |
| **合计** | **500** | **+475**（−25 模板化子节点） |

### Section 分布（净新增）

| Section | 名称 | 净增 |
|:------:|:-----|:---:|
| 2.4 | 前缀、差分、离散化、分块 | 23 |
| 2.6 | 贪心 | 30 |
| 2.7 | 搜索 | 43 |
| 2.8 | 动态规划 | 38（−25 折叠后净增 13） |
| 2.9 | 图基础与遍历 | 35 |
| 2.10 | 字符串算法 | 18 |
| 2.17 | 线性代数与插值专题 | 24 |
| 2.20 | 交互题与构造题技巧 | 64 |
| 3.13 | 高级数据结构扩展 | 79 |
| 4.1 | 数论基础 | 39 |
| 4.3 | 计数与组合 | 48 |
| 4.5 | 图与树的数学基础 | 24 |
| 4.6 | 概率与期望 | 20 |
| 4.7 | 几何基础 | 15 |

---

## 5. pending_items

| # | 任务 | 状态 | 说明 |
|:-:|:----|:----|:-----|
| 1 | `io_v4_4.json` 同步到 2640 | ❌ 未开始 | 当前仍为 2165，需同步到 2640 |
| 2 | Stage5 Batch1 内容包生成 | ❌ 未开始 | 新增 475 节点尚无学习内容包 |
| 3 | problem_pattern_sync_candidates | ❌ 未开始 | 待处理 |
| 4 | Stage5-HardKnowledge Batch2 | ❌ 未开始 | 待初始化 |
| 5 | bridge ability 候选池 | ❌ 未开始 | 代码实现/解题分析/训练管理候选池待生成 |

---

## 6. 备份文件索引

| # | 阶段 | 备份文件 |
|:-:|:----|:---------|
| 1 | Merge 前 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch1_full500.json` |
| 2 | Branch B 修复前 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch1_full500_branch_b_fix.json` |
| 3 | Fix Lite 前 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch1_full500_fix_lite.json` |

---

## 7. 输出文件索引

| 阶段 | 文件 |
|:----|:-----|
| **Precheck** | `data/stage5_hard_knowledge_batch1_full500_candidate_plan.json`<br>`data/stage5_hard_knowledge_batch1_full500_dynamic_precheck.json`<br>`docs/stage5_hard_knowledge_batch1_full500_precheck_report.md` |
| **Merge** | `data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json`<br>`data/stage5_hard_knowledge_batch1_full500_added_items_summary.json`<br>`data/stage5_hard_knowledge_batch1_full500_validation_result.json`<br>`data/stage5_hard_knowledge_batch1_full500_rollback_plan.json`<br>`docs/stage5_hard_knowledge_batch1_full500_merge_report.md` |
| **Review & Plan** | `data/stage5_hard_knowledge_batch1_full500_added_items_review.json`<br>`data/stage5_hard_knowledge_batch1_full500_review_status_patch_preview.json`<br>`data/stage5_hard_knowledge_batch1_full500_dependency_fix_candidates.json`<br>`data/stage5_hard_knowledge_batch1_full500_merge_or_collapse_candidates.json`<br>`data/stage5_hard_knowledge_batch1_full500_direct_pre_shrink_plan.json`<br>`data/stage5_hard_knowledge_batch1_full500_direct_pre_shrink_patch_preview.json`<br>`data/stage5_hard_knowledge_batch1_full500_merge_collapse_resolution_plan.json`<br>`data/stage5_hard_knowledge_batch1_full500_next_action_decision.json`<br>`data/stage5_hard_knowledge_batch1_full500_problem_pattern_sync_candidates.json`<br>`docs/stage5_hard_knowledge_batch1_full500_added_items_review_report.md`<br>`docs/stage5_hard_knowledge_batch1_full500_dependency_and_collapse_plan_report.md` |
| **Branch B Fix** | `data/stage5_hard_knowledge_batch1_full500_branch_b_applied_patch.json`<br>`data/stage5_hard_knowledge_batch1_full500_branch_b_removed_or_merged_items.json`<br>`data/stage5_hard_knowledge_batch1_full500_branch_b_direct_pre_shrink_applied.json`<br>`data/stage5_hard_knowledge_batch1_full500_branch_b_validation_result.json`<br>`docs/stage5_hard_knowledge_batch1_full500_branch_b_fix_report.md` |
| **Post-Branch-B & Fix Lite** | `data/stage5_hard_knowledge_batch1_full500_post_branch_b_review.json`<br>`data/stage5_hard_knowledge_batch1_full500_post_branch_b_fix_lite_patch_preview.json`<br>`data/stage5_hard_knowledge_batch1_full500_post_branch_b_fix_lite_readiness.json`<br>`docs/stage5_hard_knowledge_batch1_full500_post_branch_b_review_report.md`<br>`data/stage5_hard_knowledge_batch1_full500_fix_lite_applied_patch.json`<br>`data/stage5_hard_knowledge_batch1_full500_fix_lite_validation_result.json`<br>`docs/stage5_hard_knowledge_batch1_full500_fix_lite_report.md` |
| **Stable Checkpoint** | `data/stage5_hard_knowledge_batch1_full500_stable_checkpoint.json`<br>`docs/stage5_hard_knowledge_batch1_full500_stable_checkpoint_report.md` |

---

## 8. 现阶段不建议启动 Batch2 的原因

1. **io_v4_4.json 尚未同步**：当前前端图谱仍为 2165，需先同步到 2640
2. **前端读取验证未执行**：2640 节点的图谱需验证前端兼容性
3. **内容包未生成**：475 个新增节点尚无学习内容
4. **problem_pattern 未处理**：有 problem_pattern_sync_candidates 待处理

建议按以下顺序推进：

> **同步 io_v4_4.json** → **前端读取验证** → **内容包生成** → **Batch2**

---

## 9. 下一步建议

| 优先级 | 任务 | 说明 |
|:-----:|:----|:-----|
| P0 | 同步 `io_v4_4.json` 到 2640 | 导出主图谱到前端可读格式 |
| P1 | 前端读取验证 | 确认前端能正常加载和展示 2640 节点 |
| P2 | Stage5 Batch1 内容包生成 | 为 475 个新增节点生成学习内容 |
| P3 | problem_pattern 处理 | 处理已有的 sync_candidates |
| P4 | Batch2 规划 | 从剩余 ready_core 池中选择候选 |

---

## 10. 结论

| 检查项 | 结果 |
|:-------|:--:|
| 当前状态是否稳定 | ✅ **稳定** — 所有验证通过 |
| 是否修改主图谱 | **否** |
| 是否修改 io_v4_4.json | **否** |
| 是否修改前端代码 | **否** |
| 是否继续 Batch2 | **否**（暂不建议） |
| 建议生成 Stable Checkpoint | ✅ **已生成** |

---

*报告自动生成于 2026-05-26T08:20:00.000Z*
