# Stage3G full400 Dependency Fix 模板

## 基本信息

- **批次**: Stage3G full400
- **当前状态**: Merge 已完成，item_count=2165, section_count=65, validate-only=passed
- **本模板用途**: 当 2号 Review 发现 dependency_fix_candidates 非空时，执行依赖修复
- **触发条件**: `data/stage3g_full400_dependency_fix_candidates.json` 存在且非空
- **执行者**: 1号线程 / DeepSeek V4 Pro
- **主图谱**: 未修改（本模板不执行任何修改）
- **依据**: v2 dependency_cleanup_plan + 2号 Review 修正

---

## 一、Dependency Fix 触发前提

只有在同时满足以下条件时，才进入 Dependency Fix 流程：

```
1. 2号 Review 输出文件 data/stage3g_full400_dependency_fix_candidates.json 存在
2. 该文件非空（至少 1 个候选需要依赖修复）
3. 当前以分支 C 模式暂停 Fix Lite
```

---

## 二、依赖修复原则（严格遵守）

### 禁止操作

| 禁止项 | 说明 |
|--------|------|
| ❌ 自动猜测 direct_pre | 不基于名称/模糊匹配自动填充依赖 |
| ❌ 写入 section_id 到 direct_pre | direct_pre 必须是完整的三段式 item_id |
| ❌ 写入未解析字符串 | 不得把中文名、英文名写进 direct_pre |
| ❌ 修改旧节点依赖 | 不碰旧节点（1765 个）的 direct_pre / resolved_pre / rel |
| ❌ 修改旧节点 resolved_pre | resolved_pre 只写入新增节点 |
| ❌ 直接 copy v1 的 direct_pre | v1 中的 direct_pre 可能包含未解析依赖，只能作参考 |

### 允许操作

| 允许项 | 说明 |
|--------|------|
| ✅ 从 v2 dependency_check 中取 best_match | v2 中已解析成功的正式 item_id 可以直接写入 |
| ✅ 人工指定 direct_pre | 2号 Review 中明确建议的 item_id 可以直接写入 |
| ✅ direct_pre = [] | 如果确实没有合适的依赖，direct_pre 可以为空 |
| ✅ resolved_pre 重算 | 修复 direct_pre 后必须重新 compute_resolved |

---

## 三、依赖修复流程

### Step 1: 加载数据

```
加载:
  - merged_knowledge_graph_item_dependencies_refined.json
  - data/stage3g_full400_dependency_fix_candidates.json
  - data/stage3g_full400_candidate_plan_v2.json（参考 best_match）
  - data/stage3g_full400_dependency_cleanup_plan_v2.json（参考）
  - data/stage3g_full400_candidate_to_item_id_mapping.json
```

### Step 2: 前置条件确认

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 2165 |
| section_count | 65 |
| validate-only passed | true |
| dependency_fix_candidates 非空 | true |

### Step 3: 备份

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400_dependency_fix.json
```

### Step 4: 逐候选构建修复方案

```
对每个 dependency_fix_candidate：
  1. 确认候选在新的图谱中对应的 item_id
  2. 查找 v2 dependency_check.direct_pre_mapped 中的 best_match
  3. 检查 best_match 是否全部为有效的正式 item_id（三段式，存在）
  4. 对有效 item_id 写入 direct_pre
  5. 对无效/未解析的跳过（记录到报告）
  6. 构建修复后 direct_pre 列表
  7. 对 candidate_id_map 中的 item_id → 执行修复
  8. 不修改旧节点（1765 个）
```

### Step 5: 重建 resolved_pre

```
只重算被修复的节点的 resolved_pre
不覆盖旧节点的 resolved_pre
使用 compute_resolved 函数
```

### Step 6: 写入

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
```

### Step 7: 运行 validate-only

```
python refine_item_dependencies.py --validate-only --strict ...
```

### Step 8: 验证

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 2165（不变） |
| expected_item_count | 2165 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

### Step 9: 失败恢复

```
如果 validate-only 失败：
  1. 立即恢复备份
  2. 逐排查：
     - 是否写了未解析字符串到 direct_pre
     - 是否引用了不存在的 item_id
     - 是否引入了依赖循环
     - 是否误改了旧节点
  3. 人工修复后重新验证
```

### Step 10: 输出结果

```
1. data/stage3g_full400_dependency_fix_applied.json
2. data/stage3g_full400_dependency_fix_validation.json
3. data/stage3g_full400_dependency_fix_skipped.json
4. docs/stage3g_full400_dependency_fix_report.md
```

---

## 四、成功标准

与 Fix Lite 分支 A 相同的 9 项 + 额外 3 项：

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 2165 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |
| **修复节点数** | = dependency_fix_candidates 数量 |
| **direct_pre 全部正式 item_id** | true |
| **旧节点依赖未修改** | true |

---

## 五、报告必须包含

| # | 内容 |
|---|------|
| 1 | 触发修复的 dependency_fix_candidates 数量 |
| 2 | 每个修复节点的 before/after direct_pre |
| 3 | 每个修复节点的 before/after resolved_pre |
| 4 | 跳过未解析依赖的数量和原因 |
| 5 | 是否从 v2 best_match 获取依赖 |
| 6 | 是否有人工指定的依赖 |
| 7 | 修复前后 direct_pre 引用总数变化 |
| 8 | 是否修改旧节点（必须为否） |
| 9 | validate-only 是否 passed |
| 10 | 是否建议回到 Fix Lite |
