# Stage3F Batch2 Fix Lite 执行模板

## 基本信息

- **批次**: Stage3F Batch2
- **当前状态**: Merge 已完成，item_count=1681, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Review 返回后执行 Fix Lite（仅修改 review_status）
- **执行者**: 1号线程 / GLM5
- **主图谱**: 未修改（本模板不执行任何修改）

---

## 一、等待 2号 Review 输出的文件列表

在执行 Fix Lite 之前，必须确认以下 5 个 Review 输出文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3f_batch2_added_items_review.json` | 逐节点 Review 结论 | item_id, verdict (approve/C/B/A), suggested_priority |
| 2 | `data/stage3f_batch2_review_status_patch_preview.json` | review_status 补丁预览 | item_id, old_review_priority, new_review_priority, old_need_manual_review, new_need_manual_review |
| 3 | `data/stage3f_batch2_dependency_fix_candidates.json` | 依赖修复候选 | candidate_id, item_id, issue_type, suggested_direct_pre |
| 4 | `data/stage3f_batch2_problem_pattern_sync_candidates.json` | problem_pattern 同步候选 | candidate_id, item_id, pattern_type, action |
| 5 | `data/stage3f_batch2_merge_or_collapse_candidates.json` | 建议合并/折叠的候选 | candidate_id, item_id, target_item_id, action |

**前置条件检查（执行 Fix Lite 前必须全部满足）**：

| 检查项 | 期望值 | 实际值（由执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 1681 | |
| section_count | 65 | |
| validate-only passed | true | |
| resolved_pre_mismatches | [] | |
| dangling_refs | [] | |
| direct_pre_cycle | null | |
| product_metadata_validation.passed | true | |
| report_matches_json | true | |
| passed | true | |
| 2号 Review 5 个输出文件全部存在 | true | |

---

## 二、Fix Lite 执行流程

### 2.1 如果 dependency_fix_candidates 为空

标准 Fix Lite 流程（只修改 review_status）：

```
Step 1: 备份主图谱
  -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2_fix_lite.json

Step 2: 读取 data/stage3f_batch2_review_status_patch_preview.json
  -> 验证 patches 列表
  -> 验证每条的 item_id 属于 Stage3F Batch2 新增 20 个节点
  -> 验证 old_review_priority 和 old_need_manual_review 与当前图谱一致

Step 3: 逐个应用 patch（仅修改 review_status）
  -> 修改 review_status.review_priority: B → C 或 B → B（keep-B）
  -> 修改 review_status.need_manual_review: true → false（clear manual review）
  -> 绝对不修改 direct_pre / resolved_pre / rel
  -> 绝对不修改旧节点

Step 4: 写入主图谱

Step 5: 运行 validate-only
  -> python refine_item_dependencies.py --validate-only --input merged_knowledge_graph_item_dependencies_refined.json --report item_dependency_refinement_report.md --low-conf low_confidence_dependency_review.json --validation dependency_validation_result.json --strict

Step 6: 验证结果
  -> item_count = 1681
  -> section_count = 65
  -> dangling_refs = []
  -> direct_pre_cycle = null
  -> resolved_pre_mismatches = []
  -> product_metadata_validation.passed = true
  -> report_matches_json = true
  -> passed = true

Step 7: 输出结果文件
  -> data/stage3f_batch2_fix_lite_applied_patch.json（已应用的 patch 记录）
  -> data/stage3f_batch2_fix_lite_validation_result.json（验证结果）
  -> docs/stage3f_batch2_fix_lite_report.md（Fix Lite 报告）
```

### 2.2 如果 dependency_fix_candidates 非空

**处理策略：暂停，不自动修改 direct_pre**

```
1. 输出警告：dependency_fix_candidates 非空，需要人工介入
2. 只应用 review_status patch（如果 2号 Review 确认可以单独执行）
3. 将 dependency_fix_candidates 记录到 Fix Lite 报告的风险部分
4. 标记 dependency_fix 为 pending，等待人工决策后再执行
5. 不自动修改任何 direct_pre / resolved_pre / rel
```

### 2.3 如果 merge_or_collapse_candidates 非空

**处理策略：暂停，不自动合并/删除节点**

```
1. 输出警告：merge_or_collapse_candidates 非空，需要人工介入
2. 仅当 2号 Review 明确指示可以单独执行 review_status patch 时，才继续 Fix Lite
3. 将 merge_or_collapse_candidates 记录到 Fix Lite 报告的风险部分
4. 标记 merge/collapse 为 pending，等待人工决策后再执行
5. 不自动合并/删除任何 item
```

### 2.4 如果 problem_pattern_sync_candidates 非空

**处理策略：只记录不处理**

```
1. 将 problem_pattern_sync_candidates 记录到 Fix Lite 报告的"已知问题"部分
2. 标记 sync_to_patterns 为需要人工后续处理
3. 不自动创建或修改任何 problem_pattern
4. 不影响 Fix Lite 主流程
```

---

## 三、review_status patch 应用规则

### 3.1 允许的修改

| 字段 | 允许修改 | 说明 |
|------|:-------:|------|
| review_status.review_priority | ✅ 是 | B→C 或 B→B（keep-B），以下发 patch 为准 |
| review_status.need_manual_review | ✅ 是 | true→false（清除人工复查标记） |
| review_status.review_status_reason | ✅ 是 | 可添加降级说明（可选） |

### 3.2 不允许的修改

| 字段 | 允许修改 | 说明 |
|------|:-------:|------|
| direct_pre | ❌ 否 | 绝对不允许修改 |
| resolved_pre | ❌ 否 | 绝对不允许修改 |
| rel | ❌ 否 | 绝对不允许修改 |
| id | ❌ 否 | 不允许修改 |
| name / en_name | ❌ 否 | 不允许修改 |
| level | ❌ 否 | 不允许修改 |
| tracks | ❌ 否 | 不允许修改 |
| learning_path_policy | ❌ 否 | 不允许修改 |
| 旧节点任何字段 | ❌ 否 | 不允许修改任何旧节点 |

### 3.3 新增节点白名单（仅允许修改这 20 个节点的 review_status）

| item_id | 名称 | patch 前 review_priority | 预期 patch 后 |
|---------|------|:------------------------:|:------------:|
| 2.10.29 | Z算法基础 | B | C |
| 2.10.30 | Z算法模式匹配应用 | B | C |
| 2.10.31 | 扩展KMP算法基础 | B | C |
| 2.10.32 | KMP自动机基础 | B | C |
| 2.10.33 | AC自动机高级应用 | B | C |
| 2.10.34 | AC自动机失败树分析 | B | C |
| 4.1.30 | Miller-Rabin素数测试 | B | C |
| 4.1.31 | Pollard Rho分解 | B | C |
| 4.1.32 | 原根基础 | B | C |
| 4.1.33 | BSGS离散对数 | B | C |
| 4.1.34 | 扩展BSGS | B | C |
| 3.8.12 | LCP RMQ优化 | B | C |
| 3.8.13 | SAM父树结构 | B | C |
| 3.8.14 | 回文树Eertree构建 | B | C |
| 4.3.33 | Lucas定理 | B | C |
| 4.3.34 | Catalan数 | B | C |
| 4.9.4 | 狄利克雷卷积基础 | B | C |
| 4.9.5 | 莫比乌斯反演应用 | B | C |
| 2.18.10 | 单调队列优化 | B | C |
| 2.18.11 | 滑动窗口DP | B | C |

**注意**：以上 patch 预测基于 Batch1 模式。执行时必须以 2号线程生成的 `data/stage3f_batch2_review_status_patch_preview.json` 的实际内容为准。保留 B 的节点可能在 Review 中被指定。

### 3.4 keep-B 节点处理规则

| 规则 | 说明 |
|------|------|
| keep-B 节点保留 review_priority=B | 不降为 C |
| keep-B 节点 need_manual_review | 根据 patch 决定：如果 patch 中 new_need_manual_review=false 则清除，如果为 true 则保留 |
| keep-B 节点是否需要额外标注 | 建议在 review_status 中添加 reason 字段注明 keep-B 原因 |

---

## 四、validate-only 成功标准

执行 Fix Lite 后，validate-only 必须全部满足以下条件：

```
1. item_count = 1681
2. section_count = 65
3. duplicate_item_ids = []
4. dangling_refs = []
5. direct_pre_cycle = null
6. self_in_resolved_pre = []
7. direct_pre_section_refs = 0
8. direct_pre_item_ref_ratio = 1.0
9. resolved_pre_mismatches = []
10. product_metadata_validation.passed = true
11. report_matches_json = true
12. passed = true
```

**任意一项不满足 → 立即恢复备份，停止，不要继续 Batch3。**

---

## 五、失败处理

### 5.1 验证失败时的恢复步骤

```
If validate-only 任一条件不满足:
  1. shutil.copy2(BACKUP_PATH, GRAPH_PATH)  # 恢复备份
  2. 输出 mismatch/error 详情
  3. 在 Fix Lite 报告中标记 FAILED
  4. 停止，不要继续 Stage3F Batch3
```

### 5.2 备份策略

| 备份文件 | 时机 | 说明 |
|---------|------|------|
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2.json` | Merge 前 | 已存在（Merge 阶段生成） |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2_fix_lite.json` | Fix Lite 执行前 | Fix Lite 开始前立即生成 |
| 恢复时使用最近备份 | 失败时 | 优先使用 Fix Lite 前备份 |

---

## 六、Fix Lite 输出文件

| # | 文件路径 | 说明 | 必须生成 |
|---|---------|------|:-------:|
| 1 | `data/stage3f_batch2_fix_lite_applied_patch.json` | 已应用的 review_status patch 记录 | ✅ |
| 2 | `data/stage3f_batch2_fix_lite_validation_result.json` | Fix Lite 后 validate-only 结果 | ✅ |
| 3 | `data/stage3f_batch2_fix_lite_risk_checklist.json` | 风险清单（本轮已预生成） | ✅ |
| 4 | `docs/stage3f_batch2_fix_lite_report.md` | Fix Lite 完整报告 | ✅ |

---

## 七、完成条件

```
1. ✅ review_status patch 已应用（仅 20 个新增节点）
2. ✅ 未修改 direct_pre / resolved_pre / rel
3. ✅ 未修改旧节点
4. ✅ 未新增/删除/合并 item
5. ✅ item_count = 1681
6. ✅ section_count = 65
7. ✅ validate-only passed
8. ✅ 备份已生成
9. ✅ 未继续 Stage3F Batch3
```

---

## 八、参考文件

| 文件 | 用途 |
|------|------|
| `data/stage3f_batch2_candidate_to_item_id_mapping.json` | 确认 20 个新增节点的 item_id |
| `data/stage3f_batch2_added_items_summary.json` | 确认新增节点的 section 分布和 direct_pre |
| `data/stage3f_batch2_validation_result.json` | Fix Lite 前的验证基线 |
| `data/stage3f_batch2_review_status_patch_preview.json` | review_status patch（2号线程待生成） |
| `data/stage3f_batch2_review_checklist.json` | Review 检查清单 |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2.json` | Merge 前备份（验证基线） |

---

*本模板仅用于准备 Fix Lite 执行计划，不修改主图谱，不执行任何修改操作。等待 2号线程 Review 返回后，基于本模板执行 Fix Lite。*
