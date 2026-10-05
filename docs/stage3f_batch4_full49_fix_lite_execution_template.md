# Stage3F Batch4 full_49 Fix Lite 执行模板

## 基本信息

- **批次**: Stage3F Batch4 full_49
- **当前状态**: Merge 已完成，item_count=1765, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Review 返回后执行 Fix Lite（仅修改 review_status）
- **执行者**: 1号线程 / GLM5
- **依据**: v2 文件（candidate_plan_v2 + dynamic_precheck_v2 + dependency_cleanup_plan）
- **主图谱**: 未修改（本模板不执行任何修改）

---

## 一、等待 2号 Review 输出的文件列表

在执行 Fix Lite 之前，必须确认以下 5 个 Review 输出文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3f_batch4_full49_added_items_review.json` | 逐节点 Review 结论 | item_id, verdict (approve/C/B/A), suggested_priority |
| 2 | `data/stage3f_batch4_full49_review_status_patch_preview.json` | review_status 补丁预览 | item_id, old_review_priority, new_review_priority, old_need_manual_review, new_need_manual_review |
| 3 | `data/stage3f_batch4_full49_dependency_fix_candidates.json` | 依赖修复候选 | candidate_id, item_id, issue_type, suggested_direct_pre |
| 4 | `data/stage3f_batch4_full49_problem_pattern_sync_candidates.json` | problem_pattern 同步候选 | candidate_id, item_id, pattern_type, action |
| 5 | `data/stage3f_batch4_full49_merge_or_collapse_candidates.json` | 建议合并/折叠的候选 | candidate_id, item_id, target_item_id, action |

**前置条件检查（执行 Fix Lite 前必须全部满足）**：

| 检查项 | 期望值 | 实际值（由执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 1765 | |
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

## 二、三分支决策树

执行 Fix Lite 时，根据 2号 Review 的输出内容选择分支：

```
读取 2号 Review 输出文件
│
├── dependency_fix_candidates 是否非空？
│   ├── 是 → 分支 C（暂停，先生成 Dependency Fix Plan）
│   └── 否 → 继续检查
│
├── merge_or_collapse_candidates 是否非空？
│   ├── 是 → 分支 B（先执行 Duplicate Resolution Plan）
│   └── 否 → 继续检查
│
├── 以上均空 → 分支 A（标准 Fix Lite，只修改 review_status）
```

### 分支 A：标准 Fix Lite（dependency_fix_candidates 为空 + merge_or_collapse_candidates 为空）

**适用场景**：Review 认为所有新增节点都合理，不需要依赖修复或重复处理。

**执行内容**：
1. 只修改剩余 49 个新增节点的 review_status
2. 根据 Review 结论降级：建议降 C 的设 `review_priority = "C"`、`need_manual_review = false`
3. 建议保留 B 的设 `review_priority = "B"`、`need_manual_review = true`
4. 不改直接 pre / resolved_pre / rel
5. 不改旧节点

**成功标准**：
- item_count = 1765（不变）
- section_count = 65
- dangling_refs = []
- direct_pre_cycle = null
- resolved_pre_mismatches = []
- product_metadata_validation.passed = true
- report_matches_json = true
- passed = true

### 分支 B：先执行 Duplicate Resolution Plan（merge_or_collapse_candidates 非空）

**适用场景**：Review 发现部分新增节点与已有节点重复。

**处理流程**：
1. 暂停普通 Fix Lite
2. 读取 `merge_or_collapse_candidates.json` 获取重复列表
3. 对每个候选做安全删除分析：
   - 检查全图谱 direct_pre 入边
   - 检查全图谱 resolved_pre 入边
   - 检查全图谱 rel 入边
4. 生成 Duplicate Resolution Plan（四方案对比）
5. 等用户确认方案后执行 Duplicate Prune
6. Duplicate Prune 完成后回到 Fix Lite 分支 A

**如果删除后 item_count 变化**，需要更新 validation_baseline。

### 分支 C：先做 Dependency Fix Plan（dependency_fix_candidates 非空）

**适用场景**：Review 发现部分新增节点 direct_pre 存在 section ref 或其他依赖问题。

**处理流程**：
1. 暂停普通 Fix Lite
2. 读取 `dependency_fix_candidates.json` 获取问题列表
3. 生成 Dependency Fix Plan（含风险分析）
4. 等人工确认后再执行
5. 不自动修改 direct_pre

---

## 三、标准 Fix Lite 执行流程（分支 A 的详细步骤）

### Step 1: 加载数据

```
加载文件:
  - merged_knowledge_graph_item_dependencies_refined.json  (主图谱)
  - data/stage3f_batch4_full49_added_items_review.json     (Review 结论)
  - data/stage3f_batch4_full49_review_status_patch_preview.json  (补丁预览)
```

### Step 2: 前置条件验证

```
逐项检查前置条件表中的所有条件
任一不满足 → 停止，报告，不执行 Fix Lite
```

### Step 3: 备份主图谱

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch4_full49_fix_lite.json
```

### Step 4: 打 review_status 补丁

```
对每个 Review 结论中的新增节点（共 49 个）：
  建议降 C 的:
    review_status.need_manual_review = false
    review_status.review_priority = "C"
  建议保留 B 的:
    review_status.need_manual_review = true
    review_status.review_priority = "B"
  建议保留 A 的:
    review_status.need_manual_review = true
    review_status.review_priority = "A"
  不修改已删除节点
  不修改旧节点
```

### Step 5: 写入图谱

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
```

### Step 6: 运行 validate-only

```
python refine_item_dependencies.py --validate-only ^
  --input merged_knowledge_graph_item_dependencies_refined.json ^
  --report item_dependency_refinement_report.md ^
  --low-conf low_confidence_dependency_review.json ^
  --validation dependency_validation_result.json ^
  --strict
```

### Step 7: 验证结果

| 检查项 | 期望值 |
|--------|:------:|
| item_count | **1765**（或 Duplicate Prune 后的值） |
| expected_item_count | 与 item_count 一致 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

### Step 8: 输出结果文件

```
1. data/stage3f_batch4_full49_fix_lite_applied_patch.json
2. data/stage3f_batch4_full49_fix_lite_validation_result.json
3. docs/stage3f_batch4_full49_fix_lite_report.md
```

---

## 四、失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
   -> shutil.copy2(backup_path, merged_knowledge_graph_item_dependencies_refined.json)
2. 不要修改旧节点
3. 输出失败字段和具体节点列表
4. 停止，不要继续 Stage3F Batch5
```

---

## 五、报告必须包含

| # | 内容 |
|---|------|
| 1 | 三分支决策路径（A/B/C） |
| 2 | 备份是否成功 |
| 3 | Fix Lite 实际处理节点数 |
| 4 | 降为 C 数量 |
| 5 | 保留 B 数量 |
| 6 | 保留 A 数量 |
| 7 | 是否修改 direct_pre / resolved_pre / rel（必须为否） |
| 8 | 是否新增/删除/合并 item（否，除非分支 B） |
| 9 | 是否处理 problem_patterns 同步（否） |
| 10 | item_count 前后变化 |
| 11 | validate-only 是否 passed |
| 12 | 是否建议生成 Stable Checkpoint |
