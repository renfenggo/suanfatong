# Stage3F Batch3 full_40 Merge 执行模板

## 基本信息

- **批次**: Stage3F Batch3 full_40
- **当前状态**: Stage3F Batch2 Stable Checkpoint 已完成，item_count=1677, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Batch3 full_40 候选计划和动态预审返回后执行 Merge
- **执行者**: 1号线程 / GLM5
- **主图谱**: 未修改（本模板不执行任何修改）
- **预计合并目标**: item_count 1677 → **1717**
- **预计合并候选数**: **40**

---

## 一、等待 2号线程输出的文件列表

在执行 Merge 之前，必须确认以下 3 个文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3f_batch3_full40_candidate_plan.json` | 静态候选计划 | candidate_id, target_section, name, en_name, aliases, level, direct_pre, rel, tracks, audience |
| 2 | `data/stage3f_batch3_full40_dynamic_precheck.json` | 动态预审结果 | recommendation, recommended_merge_count, selected_candidates, excluded_already_merged, excluded_duplicate, excluded_high_risk, dependency_cleanup_required, needs_new_section, candidate_dependency_cycle, near_duplicate_notes |
| 3 | `docs/stage3f_batch3_full40_precheck_report.md` | 动态预审报告 | 详细预审过程说明 |

---

## 二、前置条件检查

### 2.1 图谱状态检查

| 检查项 | 期望值 | 实际值（执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 1677 | |
| section_count | 65 | |
| validate-only passed | true | |
| report_matches_json | true | |
| resolved_pre_mismatches | [] | |
| dangling_refs | [] | |

### 2.2 动态预审结果检查

| 检查项 | 期望值 | 说明 |
|--------|:------:|------|
| recommendation | **ready_for_1号线程_merge_full40** | 必须是 full_40 专用标识 |
| recommended_merge_count | **40** | 严格等于 40 |
| selected_candidates 数量 | **40** | 严格等于 40 |
| dependency_cleanup_required | **false** | 如果 true → **暂停，不合并** |
| needs_new_section | **false** | 如果 true → **暂停，不合并** |
| candidate_dependency_cycle | **false** | 如果 true → **暂停，不合并** |
| excluded_already_merged | **[]** | 必须为空 |
| excluded_duplicate | **[]** | 必须为空 |
| excluded_high_risk | **[]** | 允许非空（高风险可合并），但不建议超过 5 |

**停闸条件（任意一条满足即停止）**：

```
If recommendation != "ready_for_1号线程_merge_full40":
  停止，报告 recommendation 不匹配

If recommended_merge_count != 40:
  停止，报告数量不一致

If dependency_cleanup_required == true:
  停止，需要先执行依赖清理

If needs_new_section == true:
  停止，不支持创建新 section

If candidate_dependency_cycle == true:
  停止，候选间存在依赖环

If len(excluded_duplicate) > 0:
  停止，存在候选与已有节点重复

If len(excluded_already_merged) > 0:
  停止，存在候选已被合并
```

---

## 三、执行流程

### Step 1: 数据加载

```
加载文件:
  - merged_knowledge_graph_item_dependencies_refined.json  (主图谱)
  - data/stage3f_batch3_full40_candidate_plan.json         (候选计划)
  - data/stage3f_batch3_full40_dynamic_precheck.json       (动态预审)

构建 item_by_id 索引
构建 section_by_id 索引
```

### Step 2: 前置条件验证

```
逐项检查 2.1 和 2.2 中的所有条件
任一不满足 → 停止，输出报告，不执行合并
```

### Step 3: 备份主图谱

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch3_full40.json
```

### Step 4: 分配 item_id

```
对每个 selected_candidate:
  1. 确定 target_section（来自 candidate_plan）
  2. 检查 section 内现有最大 item id
  3. 分配新 id = section.max_id + 1
  4. 更新 section.max_id

输出: candidate_to_item_id_mapping
```

### Step 5: 构建 40 个新增节点

```
对每个候选，构建完整节点:
  id, name, en_name, aliases, global_aliases, level,
  direct_pre, resolved_pre=[], rel, tracks, audience, visibility,
  learning_path_policy, localization_status, content_status,
  platform_tags, review_status

review_status 初始值:
  need_manual_review = true
  review_priority = "B"  (待 Review 时降为 C 或保留 B)

learning_path_policy:
  unlock_mode = "expert_branch"
```

### Step 6: 插入节点到 section

```
逐个插入到 candidate_plan 指定的已有 section
不创建新 section
不重排已有 item id
```

### Step 7: 构建完整 item_by_id

```
旧节点 (1677) + 新增节点 (40) = 1717 节点
```

### Step 8: 计算 resolved_pre

```
沿用 Stage3E / Stage3F 成功策略:
  1. 新增 40 节点 resolved_pre 先设为 []
  2. 插入图谱内存结构
  3. 基于完整 item_by_id (1717) 使用官方 compute_resolved 逻辑
  4. 只将计算结果写入新增 40 节点
  5. 旧节点 resolved_pre 保持原样，绝对不覆盖
```

### Step 9: 更新 validation_baseline

```
validation_baseline.item_count = 1717
validation_baseline.section_count = 65
```

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
| item_count | **1717** |
| expected_item_count | 1717 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

**任意一项不满足 → 恢复备份，停止，输出详细失败报告。**

### Step 14: 输出结果文件

| # | 文件路径 | 说明 |
|---|---------|------|
| 1 | `data/stage3f_batch3_full40_candidate_to_item_id_mapping.json` | candidate_id → item_id 映射 |
| 2 | `data/stage3f_batch3_full40_added_items_summary.json` | 新增节点汇总（section 分布） |
| 3 | `data/stage3f_batch3_full40_validation_result.json` | validate-only 结果 |
| 4 | `data/stage3f_batch3_full40_rollback_plan.json` | 回滚计划 |
| 5 | `docs/stage3f_batch3_full40_merge_report.md` | Merge 报告 |

---

## 四、resolved_pre 计算规范

### 4.1 策略

```
1. 新增 40 个节点时，resolved_pre 设为 []
2. 将新旧共 1717 节点全部插入 item_by_id
3. 对每个新增节点调用 compute_resolved(item_id, item_by_id)
   - DFS + memoization 递归展开
   - visiting set 环检测
   - 先递归展开 direct_pre 的 resolved_pre
   - 再追加 direct_pre 本身
   - unique 去重保持顺序
   - 排除自身 id
4. 只写回新增节点
5. 旧节点不动
```

### 4.2 禁止操作

```
❌ 禁止手动修改 resolved_pre 数组
❌ 禁止覆盖旧节点 resolved_pre
❌ 禁止跳过 compute_resolved 直接赋值
❌ 禁止使用非官方 resolved_pre 计算逻辑
```

---

## 五、失败处理

### 5.1 恢复备份

```
If 任意验证项失败:
  1. shutil.copy2(BACKUP_PATH, GRAPH_PATH)
  2. 输出失败详情:
     - 哪个检查项失败
     - 期望值 vs 实际值
     - 涉及节点列表
  3. 在 Merge 报告中标记 FAILED
  4. 停止，不继续 Batch4
```

### 5.2 备份文件清单

| 备份文件 | 时机 |
|---------|------|
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2.json` | Batch2 Merge 前 |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2_duplicate_prune.json` | Batch2 Prune 前 |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch2_fix_lite.json` | Batch2 Fix Lite 前 |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch3_full40.json` | **Batch3 Merge 前（本次）** |

---

## 六、合并后输出文件

| # | 文件路径 | 必须生成 |
|---|---------|:-------:|
| 1 | `data/stage3f_batch3_full40_candidate_to_item_id_mapping.json` | ✅ |
| 2 | `data/stage3f_batch3_full40_added_items_summary.json` | ✅ |
| 3 | `data/stage3f_batch3_full40_validation_result.json` | ✅ |
| 4 | `data/stage3f_batch3_full40_rollback_plan.json` | ✅ |
| 5 | `docs/stage3f_batch3_full40_merge_report.md` | ✅ |

---

## 七、完成条件

```
1. ✅ 40 个候选已分配 item_id 并插入图谱
2. ✅ 未创建新 section
3. ✅ resolved_pre 只写入新增节点
4. ✅ 未修改旧节点
5. ✅ item_count = 1717
6. ✅ section_count = 65
7. ✅ dangling_refs = []
8. ✅ direct_pre_cycle = null
9. ✅ resolved_pre_mismatches = []
10. ✅ product_metadata_validation.passed = true
11. ✅ report_matches_json = true
12. ✅ passed = true
13. ✅ 备份已生成
14. ✅ 未继续 Stage3F Batch4
```

---

## 八、参考

| 文件 | 用途 |
|------|------|
| `merged_knowledge_graph_item_dependencies_refined.json` | 主图谱（起始 state=1677） |
| `data/stage3f_batch3_full40_candidate_plan.json` | 候选计划（2号待生成） |
| `data/stage3f_batch3_full40_dynamic_precheck.json` | 动态预审（2号待生成） |
| `data/stage3f_batch2_stable_checkpoint.json` | Batch2 检查点（基线参考） |
| `refine_item_dependencies.py` | 官方 resolved_pre 计算逻辑 |
| `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch3_full40.json` | Merge 前备份（本次生成） |

---

*本模板仅用于准备 Batch3 full_40 Merge 执行计划，不修改主图谱，不执行任何合并操作。等待 2号线程 batch3_full40 候选计划和动态预审返回后，基于本模板执行 Merge。*
