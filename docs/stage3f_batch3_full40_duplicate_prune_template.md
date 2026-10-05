# Stage3F Batch3 full_40 Duplicate Prune 模板

## 基本信息

- **批次**: Stage3F Batch3 full_40
- **当前状态**: Merge 已完成，item_count=1717, section_count=65, validate-only=passed
- **本模板用途**: 当 2号 Review 发现 merge_or_collapse_candidates 非空时执行
- **执行者**: 1号线程 / GLM5
- **执行条件**: 仅在 Fix Lite 的分支 B 场景下使用

---

## 一、前置条件

在执行 Duplicate Prune 前，必须满足以下条件：

| 检查项 | 期望值 | 说明 |
|--------|:------:|------|
| item_count | 1717 | Merge 完成后的状态 |
| section_count | 65 | |
| validate-only passed | true | |
| merge_or_collapse_candidates 非空 | | Review 发现的重复/折叠节点 |
| 这些节点均为 Batch3 新增节点 | | 只删除 Stage3F Batch3 新增的，不删旧节点 |

---

## 二、Duplicate Resolution 流程

### 2.1 读取 merge_or_collapse_candidates

从 `data/stage3f_batch3_full40_merge_or_collapse_candidates.json` 读取：

```json
{
  "candidates": [
    {
      "item_id": "...",
      "name": "...",
      "target_item_id": "...",
      "duplicate_reason": "...",
      "recommended_action": "remove"  // 或 merge
    }
  ]
}
```

### 2.2 安全删除前检查

对每个候选节点，必须检查**全图谱入边依赖**：

```
对于候选节点 X，检查：
1. 全图谱所有节点的 direct_pre 是否包含 X
2. 全图谱所有节点的 resolved_pre 是否包含 X
3. 全图谱所有节点的 rel 是否包含 X
```

**如果存在入边依赖**：
- 输出所有依赖 X 的节点列表
- 标记 X 为 cannot_prune（不能安全删除）
- 等待人工决策如何处理依赖

**如果无入边依赖**：
- 标记 X 为 safe_to_prune（可以安全删除）

### 2.3 安全删除执行

对每个 safe_to_prune 的节点：

```
Step 1: 记录删除前状态
  -> 节点 id、名称、section、direct_pre、resolved_pre、rel

Step 2: 从所在 section 的 items 列表中移除

Step 3: 验证
  -> 确认节点已从图谱中删除
  -> 确认无 dangling_refs（因为已检查过入边）
```

### 2.4 删除后处理

```
Step 4: 更新 validation_baseline
  -> graph["meta"]["validation_baseline"]["item_count"] = 1717 - 删除数量
  -> graph["meta"]["validation_baseline"]["section_count"] = 65（不变）

Step 5: 写入主图谱

Step 6: 运行 validate-only
  -> python refine_item_dependencies.py --validate-only --input merged_knowledge_graph_item_dependencies_refined.json --report item_dependency_refinement_report.md --low-conf low_confidence_dependency_review.json --validation dependency_validation_result.json --strict

Step 7: 验证结果
  -> item_count = 1717 - 删除数量
  -> section_count = 65
  -> dangling_refs = []
  -> direct_pre_cycle = null
  -> resolved_pre_mismatches = []
  -> product_metadata_validation.passed = true
  -> report_matches_json = true
  -> passed = true
```

---

## 三、方案对比（删除 vs 保留）

### 方案 A：删除（推荐用于确切重复）

| 条件 | 适用场景 |
|------|---------|
| 新增节点与旧节点名称/内容完全相同 | ✅ 采用方案 A |
| 新增节点是旧节点的确切子集 | ✅ 采用方案 A |
| 新增节点是重复概念的不同命名 | ✅ 采用方案 A |
| 新增节点与旧节点功能等价 | ✅ 采用方案 A |

### 方案 B：保留 + 标记 duplicate pending

| 条件 | 适用场景 |
|------|---------|
| 新增节点与旧节点高度相关但侧重点不同 | ✅ 采用方案 B |
| 新增节点是旧节点的变体/扩展 | ✅ 采用方案 B |
| 无法确定是否应直接删除 | ✅ 采用方案 B（等待人工） |

### 方案 C：合并（merge to existing）

| 条件 | 适用场景 |
|------|---------|
| 新增节点的内容应合并到旧节点中 | ✅ 采用方案 C |
| 新增节点的某些 direct_pre 应追加到旧节点 | ✅ 采用方案 C |

---

## 四、风险检查清单

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | 删除前是否检查全图谱入边依赖 | 遍历所有节点的 direct_pre / resolved_pre / rel |
| 2 | 删除前是否备份 | 备份到 backups/ 目录 |
| 3 | 是否只删新增节点，不删旧节点 | 验证 item_id 属于 added_item_ids |
| 4 | 删除后是否有 dangling_refs | 运行 validate-only 检查 |
| 5 | 删除后 validation_baseline 是否更新 | 检查 meta.validation_baseline.item_count |
| 6 | 删除后 validate-only 是否通过 | 检查 dependency_validation_result.json |
| 7 | 是否生成了输出文件 | applied_patch / validation_result / report |
| 8 | 是否不继续 Batch4 | 确认无 Batch4 触发 |

---

## 五、Duplicate Prune 成功标准

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 1717 - 删除数 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

---

## 六、失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
   -> shutil.copy2(backup_path, merged_knowledge_graph_item_dependencies_refined.json)
2. 输出失败原因
3. 不要继续 Fix Lite
```

---

## 七、输出文件

| # | 文件路径 | 内容 |
|---|---------|------|
| 1 | data/stage3f_batch3_full40_duplicate_prune_applied_patch.json | 已删除/合并的节点记录 |
| 2 | data/stage3f_batch3_full40_duplicate_prune_validation_result.json | validate-only 结果快照 |
| 3 | data/stage3f_batch3_full40_duplicate_prune_removed_items.json | 已删除节点详情 |
| 4 | docs/stage3f_batch3_full40_duplicate_prune_report.md | Duplicate Prune 执行报告 |

---

## 八、Duplicate Prune 完成后

1. 回到 Fix Lite 分支 B 的"Duplicate Prune 完成后再执行 Fix Lite"步骤
2. 备份当前图谱（prune 后的状态）
3. 对剩余新增节点执行 review_status 降级
4. 运行 validate-only 并验证
5. 不要继续 Batch4
