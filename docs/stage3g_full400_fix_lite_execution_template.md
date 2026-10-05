# Stage3G full400 Fix Lite 执行模板

## 基本信息

- **批次**: Stage3G full400
- **当前状态**: Merge 已完成，item_count=2165, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Review 返回后执行 Fix Lite（仅修改 review_status）
- **执行者**: 1号线程 / DeepSeek V4 Pro
- **依据**: v2 文件（candidate_plan_v2 + dynamic_precheck_v2 + dependency_cleanup_plan_v2）
- **主图谱**: 未修改（本模板不执行任何修改）

---

## 一、等待 2号 Review 输出的文件列表

在执行 Fix Lite 之前，必须确认以下 5 个 Review 输出文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3g_full400_added_items_review.json` | 逐节点 Review 结论 | item_id, verdict (approve/C/B/A), suggested_priority |
| 2 | `data/stage3g_full400_review_status_patch_preview.json` | review_status 补丁预览 | item_id, old_review_priority, new_review_priority, old_need_manual_review, new_need_manual_review |
| 3 | `data/stage3g_full400_dependency_fix_candidates.json` | 依赖修复候选 | candidate_id, item_id, issue_type, suggested_direct_pre |
| 4 | `data/stage3g_full400_problem_pattern_sync_candidates.json` | problem_pattern 同步候选 | candidate_id, item_id, pattern_type, action |
| 5 | `data/stage3g_full400_merge_or_collapse_candidates.json` | 建议合并/折叠的候选 | candidate_id, item_id, target_item_id, action |

**前置条件检查（执行 Fix Lite 前必须全部满足）**：

| 检查项 | 期望值 | 实际值（由执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 2165 | |
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
│   ├── 是 → 分支 C（暂停，先执行 Dependency Fix Plan）
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
1. 只修改剩余 400 个新增节点的 review_status
2. 根据 Review 结论降级：建议降 C 的设 `review_priority = "C"`、`need_manual_review = false`
3. 建议保留 B 的设 `review_priority = "B"`、`need_manual_review = true`
4. 建议保留 A 的设 `review_priority = "A"`、`need_manual_review = true`
5. 不改 direct_pre / resolved_pre / rel
6. 不改旧节点（1765 个）

**成功标准**：
- item_count = 2165（不变）
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

**适用场景**：Review 发现部分新增节点存在依赖问题（direct_pre 为空/过长/section ref 等）。

**处理流程**：
1. 暂停普通 Fix Lite
2. 读取 `dependency_fix_candidates.json` 获取问题列表
3. 不自动猜测 direct_pre
4. 生成 Dependency Fix Plan（含修复建议 + 风险分析）
5. 等人工确认后再执行
6. 修复完成后重新运行 validate-only

---

## 三、标准 Fix Lite 执行流程（分支 A 的详细步骤）

### Step 1: 加载数据

```
加载文件:
  - merged_knowledge_graph_item_dependencies_refined.json
  - data/stage3g_full400_added_items_review.json
  - data/stage3g_full400_review_status_patch_preview.json
  - data/stage3g_full400_candidate_to_item_id_mapping.json
```

### Step 2: 前置条件验证

```
逐项检查前置条件表中的所有条件
任一不满足 → 停止，报告，不执行 Fix Lite
```

### Step 3: 备份主图谱

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400_fix_lite.json
```

### Step 4: 打 review_status 补丁

```
对每个 Review 结论中的新增节点（共 400 个）：
  建议降 C 的:
    review_status.need_manual_review = false
    review_status.review_priority = "C"
  建议保留 B 的:
    review_status.need_manual_review = true
    review_status.review_priority = "B"
  建议保留 A 的:
    review_status.need_manual_review = true
    review_status.review_priority = "A"
  不修改已通过 Duplicate Prune 删除的节点
  不修改旧节点
```

### Step 5: 写入图谱

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
```

### Step 6: 运行 validate-only

```
python refine_item_dependencies.py --validate-only \
  --input merged_knowledge_graph_item_dependencies_refined.json \
  --report item_dependency_refinement_report.md \
  --low-conf low_confidence_dependency_review.json \
  --validation dependency_validation_result.json \
  --strict
```

### Step 7: 验证结果

| 检查项 | 期望值 |
|--------|:------:|
| item_count | **2165**（或 Duplicate Prune 后的值） |
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
1. data/stage3g_full400_fix_lite_applied_patch.json
2. data/stage3g_full400_fix_lite_validation_result.json
3. docs/stage3g_full400_fix_lite_report.md
```

---

## 四、失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
2. 不要修改旧节点
3. 不要修改 direct_pre / resolved_pre / rel
4. 输出失败字段和具体节点列表
5. 停止，不要继续 Stage3G Batch2
```

---

## 五、报告必须包含

| # | 内容 |
|---|------|
| 1 | 三分支决策路径（A/B/C） |
| 2 | 备份是否成功 |
| 3 | Fix Lite 实际处理节点数（过滤已删除的） |
| 4 | 降为 C 数量 |
| 5 | 保留 B 数量 |
| 6 | 保留 A 数量 |
| 7 | 是否修改 direct_pre / resolved_pre / rel（必须为否，除非分支 C） |
| 8 | 是否新增/删除/合并 item（否，除非分支 B） |
| 9 | 是否处理 problem_patterns（否，仅记录） |
| 10 | item_count 前后变化 |
| 11 | validate-only 是否 passed |
| 12 | 是否建议生成 Stable Checkpoint |
