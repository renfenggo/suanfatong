# Stage3G full400 Duplicate Prune 模板

## 基本信息

- **批次**: Stage3G full400
- **当前状态**: Merge 已完成，item_count=2165, section_count=65, validate-only=passed
- **本模板用途**: 当 2号 Review 发现 merge_or_collapse_candidates 非空时，执行重复节点安全删除
- **触发条件**: `data/stage3g_full400_merge_or_collapse_candidates.json` 存在且非空
- **执行者**: 1号线程 / DeepSeek V4 Pro
- **主图谱**: 未修改（本模板不执行任何修改）

---

## 一、Duplicate Prune 触发前提

只有在同时满足以下条件时，才进入 Duplicate Prune 流程：

```
1. 2号 Review 输出文件 data/stage3g_full400_merge_or_collapse_candidates.json 存在
2. 该文件非空（至少 1 个候选 merge/collapse）
3. 当前未处于 Fix Lite 执行中（Fix Lite 必须暂停）
```

---

## 二、入边依赖安全扫描（删除前必须完成）

删除一个节点前，必须扫描全图谱中所有引用该节点的入边。以下四种引用类型都必须检查：

### 安全检查表

| 检查项 | 扫描方式 | 必须为 0？ | 如果不为 0 怎么办 |
|--------|---------|:----------:|------------------|
| direct_pre 入边 | 遍历所有节点的 direct_pre，检查是否包含目标节点 ID | 是 | 报错，不能删除。需人工处理。 |
| resolved_pre 入边 | 遍历所有节点的 resolved_pre，检查是否包含目标节点 ID | 是 | 报错，不能删除。需人工处理。 |
| rel 入边 | 遍历所有节点的 rel，检查是否包含目标节点 ID | 是 | 报错，不能删除。需人工处理。 |
| low_confidence 引用 | 检查 low_confidence_dependency_review.json 中是否有引用 | 否（仅记录） | 记录在案，不阻止删除 |

### 如果有入边依赖

```
不要强行删除。
输出节点 ID + 依赖者列表，标记为 needs_manual_resolution。
跳过该节点，处理下一个。
在最终报告中列出所有跳过的节点。
```

---

## 三、四方案对比表（对每个重复组生成）

对每个 merge_or_collapse_candidate，生成以下四方案对比：

| 方案 | 操作 | 对图谱影响 | 推荐场景 | 风险 |
|------|------|-----------|---------|------|
| A: keep_new | 保留新节点，删除旧节点 | 旧节点被移除，其依赖者需重定向 | 新节点元数据更完整 | 高：旧节点可能有大量入边 |
| B: keep_old | 保留旧节点，删除新节点 | 新节点被移除，无入边问题 | 新节点无入边依赖 | 低：推荐首选 |
| C: merge | 合并到旧节点，新节点删 | update old's en_name/aliases/global_aliases | 需要保留新节点元数据 | 中：合并逻辑复杂 |
| D: keep_both | 不删除，标记为 related | 两个都保留，加入彼此的 rel | 两个都有独特价值 | 无 |
| E: skip | 不处理，标记为 needs_manual_review | 两个都保留 | 无法自动决策 | 无 |

---

## 四、Duplicate Prune 执行流程

### Step 1: 加载数据

```
加载:
  - merged_knowledge_graph_item_dependencies_refined.json
  - data/stage3g_full400_merge_or_collapse_candidates.json
  - data/stage3g_full400_candidate_to_item_id_mapping.json
```

### Step 2: 前置条件确认

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 2165 |
| section_count | 65 |
| validate-only passed | true |
| merge_or_collapse_candidates 非空 | true |

### Step 3: 备份

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400_duplicate_prune.json
```

### Step 4: 逐候选安全扫描 + 生成方案

```
对每个 merge_or_collapse_candidate：
  1. 提取 old_item_id 和 new_item_id
  2. 扫描全图谱 direct_pre 入边
  3. 扫描全图谱 resolved_pre 入边
  4. 扫描全图谱 rel 入边
  5. 根据入边情况推荐方案（B 优先）
  6. 输出到方案表
```

### Step 5: 执行删除（用户确认后）

```
如果选择方案 B（删除新节点）：
  1. 从对应 section 的 items 列表中移除
  2. 从 candidate_id_map 中移除
  3. 记录到删除日志
  4. 不修改旧节点

如果选择方案 A（删除旧节点）：
  1. 从旧节点 section 移除
  2. 将所有引用旧节点的 direct_pre/resolved_pre/rel 替换为新节点 ID
  3. 验证替换后无循环/空引用
```

### Step 6: 写入

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
更新 validation_baseline.item_count
```

### Step 7: 验证

```
python refine_item_dependencies.py --validate-only --strict ...
```

### Step 8: 输出结果

```
1. data/stage3g_full400_duplicate_prune_result.json
2. data/stage3g_full400_duplicate_prune_validation.json
3. docs/stage3g_full400_duplicate_prune_report.md
4. data/stage3g_full400_duplicate_prune_skipped.json（有入边依赖的跳过项）
```

---

## 五、成功标准

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 根据删除操作变化（= 2165 - 删除数） |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

---

## 六、失败恢复

```
1. 立即恢复备份
2. 不要留下半删除的图谱
3. 输出失败原因和节点列表
4. 被跳过的节点（有入边依赖）不是失败，是预期行为
```

---

## 七、报告必须包含

| # | 内容 |
|---|------|
| 1 | 触发类型（merge_or_collapse_candidates 数量） |
| 2 | 每个候选的四方案对比表 |
| 3 | 用户选择方案 |
| 4 | 实际删除数量和 item_id 列表 |
| 5 | 跳过数量和原因（入边依赖） |
| 6 | 是否有方案 A（删除旧节点） |
| 7 | 删除前后 item_count |
| 8 | 是否更新 validation_baseline |
| 9 | validate-only 是否 passed |
| 10 | 是否建议回到 Fix Lite |
