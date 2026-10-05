# Stage3F Batch4 full_49 Merge 执行模板

## 基本信息

- **批次**: Stage3F Batch4 full_49
- **当前状态**: Stage3F Batch3 已完成，item_count=1716, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Batch4 full49 依赖清洗和动态预审 v2 返回后执行 Merge
- **执行者**: 1号线程 / GLM5
- **主图谱**: 未修改（本模板不执行任何修改）
- **预计合并目标**: item_count 1716 → **1765**
- **预计合并候选数**: **49**（原计划 50，因候选池不足改为 49）

---

## 一、等待 2号线程输出的文件列表

在执行 Merge 之前，必须确认以下 5 个文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3f_batch4_full49_dependency_cleanup_plan.json` | 依赖清洗计划 | cleaned_direct_pre, remaining_section_refs |
| 2 | `data/stage3f_batch4_full49_candidate_plan_v2.json` | 候选计划 v2 | candidate_id, target_section, name, en_name, cleaned_direct_pre_item_ids, direct_pre, rel |
| 3 | `data/stage3f_batch4_full49_dynamic_precheck_v2.json` | 动态预审 v2 | recommendation, recommended_merge_count, selected_candidates, dependency_cleanup_required, dependency_mapping_risk, section_ref_dependencies |
| 4 | `docs/stage3f_batch4_full49_dependency_cleanup_report.md` | 依赖清洗报告 | 详细清洗过程说明 |
| 5 | `docs/stage3f_batch4_full49_precheck_report_v2.md` | 动态预审报告 v2 | 详细预审过程说明 |

**重要：禁止读取或使用任何 stage3f_batch4_full50_* 文件。**

---

## 二、前置条件检查

### 2.1 图谱状态检查

| 检查项 | 期望值 | 实际值（执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 1716 | |
| section_count | 65 | |
| validate-only passed | true | |
| report_matches_json | true | |
| resolved_pre_mismatches | [] | |
| dangling_refs | [] | |
| direct_pre_cycle | null | |

### 2.2 动态预审 v2 结果检查

| 检查项 | 期望值 | 说明 |
|--------|:------:|------|
| recommendation | **ready_for_1号线程_merge_full49** | 必须是 full49 专用标识 |
| recommended_merge_count | **49** | 严格等于 49 |
| selected_candidates 数量 | **49** | 严格等于 49 |
| dependency_cleanup_required | **false** | 如果 true → **暂停，不合并** |
| dependency_mapping_risk | **[]** | 必须为空 |
| section_ref_dependencies | **[]** | 必须为空 |
| needs_new_section | **false** | 如果 true → **暂停，不合并** |
| candidate_dependency_cycle | **false** | 如果 true → **暂停，不合并** |
| excluded_already_merged_candidates | **[]** | 必须为空 |
| excluded_duplicate_or_near_duplicate | **[]** | 必须为空 |

### 2.3 停闸条件

**任意一条满足即停止，不执行合并**：

```
If recommendation != "ready_for_1号线程_merge_full49":
  停止，报告 recommendation 不匹配

If recommended_merge_count != 49:
  停止，报告数量不一致

If dependency_cleanup_required == true:
  停止，需要先执行依赖清理，不降级

If len(dependency_mapping_risk) > 0:
  停止，存在依赖映射风险

If len(section_ref_dependencies) > 0:
  停止，存在 section id 引用依赖未清理

If needs_new_section == true:
  停止，不支持创建新 section

If candidate_dependency_cycle == true:
  停止，候选间存在依赖环

If len(excluded_duplicate_or_near_duplicate) > 0:
  停止，存在候选与已有节点重复，先做 duplicate resolution

If len(excluded_already_merged_candidates) > 0:
  停止，存在候选已被合并
```

---

## 三、执行流程

### Step 1: 数据加载

```
加载文件:
  - merged_knowledge_graph_item_dependencies_refined.json    (主图谱)
  - data/stage3f_batch4_full49_candidate_plan_v2.json        (候选计划 v2)
  - data/stage3f_batch4_full49_dynamic_precheck_v2.json      (动态预审 v2)
  - data/stage3f_batch4_full49_dependency_cleanup_plan.json  (依赖清洗计划)

构建 item_by_id 索引
构建 section_by_id 索引

确认所有输入文件名均包含 full49，不包含 full50
```

### Step 2: 前置条件验证

```
逐项检查 2.1 和 2.2 中的所有条件
任一不满足 → 停止，输出报告，不执行合并
```

### Step 3: 备份主图谱

```
cp ->
backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch4_full49.json
```

### Step 4: 分配 item_id

```
对每个 selected_candidate:
  1. 确定 target_section（来自 candidate_plan_v2）
  2. 检查 section 内现有最大 item id
  3. 分配新 id = section.max_id + 1
  4. 不重排已有 item id
  5. 更新 section.max_id 用于同 section 下一个候选用

输出: candidate_to_item_id_mapping
```

### Step 5: 构建 49 个新增节点

```
对每个候选，构建完整节点:
  id, name, en_name, aliases, global_aliases, level,
  direct_pre, resolved_pre=[], rel, tracks, audience, visibility,
  learning_path_policy, localization_status, content_status,
  platform_tags, review_status
```

**direct_pre 使用规则**：
- 优先使用 `candidate_plan_v2` 中的 `cleaned_direct_pre_item_ids`
- 如果 `cleaned_direct_pre_item_ids` 为空或未定义，使用 `direct_pre`（必须是三段式 item id）
- 所有 direct_pre 必须为正式 item id（三段式），不允许 section id

**review_status 初始值**：
- `need_manual_review = true`
- `review_priority = "B"`（待 Review 时降为 C 或保留 B）

**learning_path_policy**：
- `unlock_mode = "expert_branch"`（推荐）

### Step 6: 插入节点到 section

```
逐个插入到 candidate_plan_v2 指定的已有 section
不创建新 section
不重排已有 item id
不修改已有节点
```

### Step 7: 构建完整 item_by_id

```
旧节点 (1716) + 新增节点 (49) = 1765 节点
```

### Step 8: 计算 resolved_pre

**必须沿用 Stage3 成功策略**：

```
1. 新增 49 节点 resolved_pre 先设为 []
2. 将 49 个新增 item 插入图谱内存结构
3. 基于"旧节点 + 新增49节点"建立完整 item_by_id
4. 使用官方 compute_resolved 逻辑计算 resolved_pre
   -> DFS + memoization + visiting set 环检测
   -> unique 去重保持顺序
   -> 排除自身 id
5. 只把计算结果写入新增 49 个节点
6. 旧节点 resolved_pre 保持原样，绝对不要覆盖
```

### Step 9: 更新 validation_baseline

```
graph["meta"]["validation_baseline"] = {
  "item_count": 1765,
  "section_count": 65
}
```

**重要：目标 item_count 是 1765 而不是 1766。**

### Step 10: 写入主图谱

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
```

### Step 11: 重新生成报告

```
基于当前图谱状态生成 item_dependency_refinement_report.md
确保统计数字与图谱一致
```

### Step 12: 运行 validate-only

```
python refine_item_dependencies.py --validate-only ^
  --input merged_knowledge_graph_item_dependencies_refined.json ^
  --report item_dependency_refinement_report.md ^
  --low-conf low_confidence_dependency_review.json ^
  --validation dependency_validation_result.json ^
  --strict
```

### Step 13: 验证结果

| 检查项 | 期望值 |
|--------|:------:|
| item_count | **1765** |
| expected_item_count | 1765 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

### Step 14: 输出结果文件

```
1. data/stage3f_batch4_full49_candidate_to_item_id_mapping.json
2. data/stage3f_batch4_full49_added_items_summary.json
3. data/stage3f_batch4_full49_validation_result.json
4. data/stage3f_batch4_full49_rollback_plan.json
5. docs/stage3f_batch4_full49_merge_report.md
```

---

## 四、失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
   -> shutil.copy2(backup_path, merged_knowledge_graph_item_dependencies_refined.json)
2. 不要修改旧节点 resolved_pre
3. 输出 mismatch 节点列表和 expected_len / actual_len
4. 停止，不要继续 Stage3F Batch5
```

---

## 五、Merge 报告必须包含

| # | 内容 |
|---|------|
| 1 | 备份是否成功 |
| 2 | 合并前 item_count |
| 3 | 合并后 item_count（必须是 1765） |
| 4 | 实际新增 item 数（必须是 49） |
| 5 | 新增节点分别进入哪些 section |
| 6 | 是否创建新 section（必须为否） |
| 7 | direct_pre 是否无 section id |
| 8 | 悬空引用是否为 0 |
| 9 | direct_pre 是否无环 |
| 10 | resolved_pre_mismatches 是否为 0 |
| 11 | product_metadata_validation 是否 passed |
| 12 | report_matches_json 是否 true |
| 13 | validation 是否 passed |
| 14 | 是否生成 rollback plan |
| 15 | 需要人工复查的新增节点列表 |

---

## 六、注意事项

1. **只合并 selected_candidates 中的 49 个候选**
2. **不要合并非 selected_candidates**
3. **不使用任何 full50 文件**
4. **目标 item_count 是 1765，不是 1766**
5. **不要硬凑第 50 个候选**
6. **如果 dependency_cleanup_required = true，暂停，不降级**
7. **如果停闸条件触发，必须停止并报告**
8. **validate-only 失败必须恢复备份**
9. **旧节点 resolved_pre 绝对不要覆盖**
10. **不要继续 Stage3F Batch5**
