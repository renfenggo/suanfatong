# Stage3E Batch6 full_30 Merge 执行模板

## 一、前置条件

### 1.1 当前图谱基准状态（Batch5 Fix Lite 完成后）

| 指标 | 当前值 | 要求 |
|------|--------|------|
| item_count | 1617 | 1617 |
| section_count | 65 | 65 |
| validate-only | passed | passed |
| resolved_pre_mismatches | [] | [] |
| dangling_refs | [] | [] |
| direct_pre_cycle | null | null |
| product_metadata_validation | passed | passed |
| Batch5 Review/Fix Lite | 已完成 | 已完成 |

### 1.2 必须等待 2号线程返回的文件

在启动 Batch6 full_30 Merge 之前，必须确认以下文件已就绪：

| # | 文件 | 状态 |
|---|------|------|
| 1 | `data/thread2_stage3e_batch6_full30_candidate_plan.json` | ⏳ 等待 2号返回 |
| 2 | `data/thread2_stage3e_batch6_full30_dynamic_precheck.json` | ⏳ 等待 2号返回 |
| 3 | `docs/thread2_stage3e_batch6_full30_precheck_report.md` | ⏳ 等待 2号返回 |

### 1.3 合并前确认清单

启动合并前，必须逐项确认以下条件全部满足：

| # | 条件 | 检查方法 |
|---|------|----------|
| 1 | item_count = 1617 | 读取当前主图谱 |
| 2 | section_count = 65 | 读取当前主图谱 |
| 3 | validate-only = passed | 运行 `--validate-only` |
| 4 | selected_candidates 数量符合预期 | 读取 `candidate_plan.json` → `selected_candidates` |
| 5 | recommendation 符合预期 | 读取 `dynamic_precheck.json` → `recommendation` |
| 6 | recommended_merge_count 符合预期 | 读取 `dynamic_precheck.json` → `recommended_merge_count` |
| 7 | dependency_cleanup_required 判断 | 读取 `dynamic_precheck.json` → `dependency_cleanup_required` |
| 8 | 所有候选未在 Batch1~5 合并过 | 交叉比对 Batch1~5 mapping 文件 |
| 9 | 候选 direct_pre 全部为 item id | 遍历检查 |
| 10 | 候选 direct_pre 不含 section id | 遍历检查 |
| 11 | 不需要新 section | 检查 target_section 是否已存在 |
| 12 | 无候选依赖环 | 读取 `dynamic_precheck.json` → 或内存图谱预检测 |

如果任一条件不满足，停止并报告，不要合并。

---

## 二、合并流程（recommendation = ready_for_1号线程_merge_full30）

> 适用于 2号线程返回 `recommendation: "ready_for_1号线程_merge_full30"` 且 `dependency_cleanup_required: false` 的情况。

### Step 1：备份

```bash
Copy-Item merged_knowledge_graph_item_dependencies_refined.json `
    backups\merged_knowledge_graph_item_dependencies_refined_before_stage3e_batch6_full30.json
```

### Step 2：读取候选计划

```python
import json

with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
    graph = json.load(f)

with open("data/thread2_stage3e_batch6_full30_candidate_plan.json", 'r', encoding='utf-8') as f:
    candidate_plan = json.load(f)

# 确认推荐模式
assert candidate_plan.get("meta", {}).get("recommendation") == "ready_for_1号线程_merge_full30", \
    f"推荐模式不匹配: {candidate_plan.get('meta', {}).get('recommendation')}"

selected_candidates = candidate_plan["selected_candidates"]
print(f"候选数量: {len(selected_candidates)}")
assert len(selected_candidates) == 30, f"预期 30 个候选，实际 {len(selected_candidates)}"
```

### Step 3：构建 item_by_id 索引

```python
item_by_id = {}
for category in graph["categories"]:
    for section in category["sections"]:
        for item in section["items"]:
            item_by_id[item["id"]] = item
```

### Step 4：分配 item_id 并构建新增节点

```python
# 确认 item_count 基线
assert len(item_by_id) == 1617

# 分配 item_id：按 section 分组，各 section 内续接最大 id
def assign_item_ids(candidates, item_by_id):
    section_max = {}
    for cid, item in item_by_id.items():
        parts = cid.split(".")
        if len(parts) >= 3:
            sec = f"{parts[0]}.{parts[1]}"
            num = int(parts[2])
            section_max[sec] = max(section_max.get(sec, 0), num)
    
    new_items = []
    for candidate in candidates:
        sec = candidate["target_section"]
        section_max[sec] = section_max.get(sec, 0) + 1
        new_id = f"{sec}.{section_max[sec]}"
        candidate["item_id"] = new_id
        new_items.append(new_id)
    return new_items

new_item_ids = assign_item_ids(selected_candidates, item_by_id)

# 构建完整 metadata
new_items_by_id = {}
for candidate in selected_candidates:
    item_id = candidate["item_id"]
    item = {
        "id": item_id,
        "name": candidate["name"],
        "en_name": candidate.get("en_name", ""),
        "direct_pre": candidate.get("direct_pre", []),
        "rel": candidate.get("rel", []),
        "resolved_pre": [],
        "review_status": {
            "need_manual_review": True,
            "review_priority": "B"
        },
        "product_metadata": {
            "tracks": candidate.get("tracks", ["advanced_data_structure"]),
            "audience": ["university_icpc", "advanced_competitive_programmer"],
            "visibility": "expert",
            "learning_path_policy": {
                "unlock_mode": "free",
                "required": []
            },
            "localization_status": "en_needed",
            "content_status": "needs_content"
        },
        "tags": [],
        "aliases": [],
        "pickup_group": []
    }
    new_items_by_id[item_id] = item
```

### Step 5：检查 direct_pre 有效性

```python
# 检查所有 direct_pre 为正式 item id（非 section id 格式）
section_id_pattern = re.compile(r"^\d+\.\d+$")
for item_id, item in new_items_by_id.items():
    for dep in item.get("direct_pre", []):
        if section_id_pattern.match(dep):
            raise ValueError(f"{item_id} 的 direct_pre 包含 section id: {dep}")
        if dep not in item_by_id and dep not in new_items_by_id:
            raise ValueError(f"{item_id} 的 direct_pre 悬空引用: {dep}")

print("  ✅ 所有 direct_pre 均为有效 item id，无 section id")
```

### Step 6：插入新增节点到对应 section

```python
for item_id, item in new_items_by_id.items():
    section_id = ".".join(item_id.split(".")[:2])
    found = False
    for category in graph["categories"]:
        for section in category["sections"]:
            if section["id"] == section_id:
                section["items"].append(item)
                found = True
                break
        if found:
            break
    if not found:
        raise ValueError(f"未找到 section {section_id}，可能需要创建新 section")
```

### Step 7：合并 item_by_id（旧节点 + 新增节点）

```python
full_item_by_id = {**item_by_id, **new_items_by_id}
```

### Step 8：使用官方 compute_resolved 计算 resolved_pre

```python
def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out

def compute_resolved(edges, item_ids):
    memo, visiting = {}, set()
    
    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))
                out.append(dep)
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])
        return memo[node]
    
    return {item_id: resolve(item_id) for item_id in item_ids}

# 构建边表
edges = {}
for item_id in full_item_by_id:
    edges[item_id] = list(full_item_by_id[item_id].get("direct_pre", []) or [])

# 计算 resolved_pre
resolved_results = compute_resolved(edges, set(full_item_by_id.keys()))
```

#### resolved_pre 计算规则（必须遵守）

1. 基于 **完整内存图谱**（旧节点 1617 + 新增 30 个）的 `full_item_by_id` 计算
2. DFS + memoization + visiting set 环检测
3. 先展开 dep 的 resolved_pre，再追加 dep 本身
4. `unique()` 保持首次出现顺序
5. 不排序
6. 过滤 section id（compute_resolved 已内置检查）
7. 排除自身

### Step 9：只写回新增节点的 resolved_pre

```python
for item_id in new_item_ids:
    if item_id in resolved_results:
        new_items_by_id[item_id]["resolved_pre"] = resolved_results[item_id]

print(f"  ✅ 只写回了 {len(new_item_ids)} 个新增节点的 resolved_pre，旧节点未被修改")
```

**关键约束**：
- **不覆盖** 旧节点 resolved_pre
- **不覆盖** Batch1~5 节点的 resolved_pre
- 只写回当前 Batch6 新增节点的 resolved_pre

### Step 10：更新 meta.validation_baseline

```python
if "meta" not in graph:
    graph["meta"] = {}
if "validation_baseline" not in graph["meta"]:
    graph["meta"]["validation_baseline"] = {}
graph["meta"]["validation_baseline"]["item_count"] = 1647
graph["meta"]["validation_baseline"]["section_count"] = 65
```

### Step 11：写入图谱文件

```python
with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
```

### Step 12：运行 validate-only

```bash
python refine_item_dependencies.py --validate-only ^
    --input merged_knowledge_graph_item_dependencies_refined.json ^
    --report item_dependency_refinement_report.md ^
    --low-conf low_confidence_dependency_review.json ^
    --validation dependency_validation_result.json ^
    --strict
```

### Step 13：验证成功标准（full_30）

| 检查项 | 期望值 |
|--------|--------|
| item_count | **1647** |
| expected_item_count | **1647** |
| section_count | 65 |
| duplicate_item_ids | [] |
| dangling_refs | [] |
| direct_pre_cycle | null |
| self_in_resolved_pre | [] |
| direct_pre_section_refs | 0 |
| resolved_pre_section_refs.count | 0 |
| rel_section_refs.count | 0 |
| direct_pre_item_ref_ratio | 1.0 |
| report_matches_json | true |
| low_conf_ids_not_in_graph | [] |
| parent_concept_self_refs | [] |
| product_metadata_validation.passed | true |
| resolved_pre_mismatches | [] |
| passed | true |

### Step 14：验证失败时恢复备份

```python
import shutil
shutil.copy2("backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_batch6_full30.json",
             "merged_knowledge_graph_item_dependencies_refined.json")
```

验证失败时输出 mismatch 详情：
- `resolved_pre_mismatches` 节点列表
- 各节点的 `expected_len` / `actual_len`
- `missing` 和 `extra` 项明细

---

## 三、合并流程（recommendation = use_fallback_20）

> 适用于 2号线程返回 `recommendation: "use_fallback_20"` 的情况。

### 差异说明

| 项目 | full_30 | fallback_20 |
|------|---------|-------------|
| 候选数量 | 30 | 20 |
| 目标 item_count | 1647 | **1637** |
| 来源 | batch_5 剩余 15 + Reserve 15 | batch_5 剩余 15 + Reserve 5 |
| 预期 section_count | 65 | 65 |

### 流程变更

与第二章 full_30 流程相同，但做如下调整：

1. **Step 2**: 读取 `candidate_plan.json` 中 `selected_candidates` 数量应为 20
2. **Step 10**: `validation_baseline.item_count = 1637`
3. **Step 13**: item_count 预期值改为 **1637**

其余步骤（备份、构建、计算 resolved_pre、写入、validate-only）完全一致。

### 验证成功标准（fallback_20）

| 检查项 | 期望值 |
|--------|--------|
| item_count | **1637** |
| expected_item_count | **1637** |
| 其余条件 | 与 full_30 一致 |

---

## 四、合并流程（recommendation = needs_dependency_cleanup_before_merge）

> 适用于 2号线程返回 `recommendation: "needs_dependency_cleanup_before_merge"` 的情况。

### 处理流程

```
Step 1: 备份
  ↓
Step 2: 读取 cleaned_dependency_plan.json（由 2号线程生成）
  ↓
Step 3: 读取 dependency_cleanup_rules（由 2号线程生成）
  ↓
Step 4: 按 cleanup_rules 修改候选的 direct_pre
  │        - 替换 section id 为正式 item id
  │        - 补充语义缺失的依赖
  │        - 移除循环依赖
  ↓
Step 5: 确认修改后 direct_pre 不含 section id、不含悬空引用、不含 cycle
  ↓
Step 6: 将候选插入内存图谱（同第二章 Step 6~9）
  ↓
Step 7: 运行 validate-only（同第二章 Step 12~14）
```

### cleanup 规则

1. **section id 替换**: direct_pre 中不能包含 `2.21`, `3.13` 等 section id
2. **悬空引用检查**: 所有 direct_pre 引用的 item id 必须存在于图谱中
3. **循环依赖检查**: 修改后不能产生 direct_pre cycle
4. **最小修改原则**: 只修改明确指出的问题节点，不修改其他节点

### 验证成功标准

- full_30 清理后: item_count = 1647
- fallback_20 清理后: item_count = 1637

---

## 五、新增节点 metadata 要求

每个新增节点必须包含以下字段：

```python
{
    "id": "3.13.xxx",            # item id
    "name": "节点中文名",         # 中文名称
    "en_name": "English Name",   # 英文名称
    "direct_pre": ["3.x.x"],     # 直接前置依赖（只含正式 item id）
    "rel": ["3.x.x"],            # 强相关（可选）
    "resolved_pre": [],          # 由 compute_resolved 自动计算
    "review_status": {
        "need_manual_review": True,
        "review_priority": "B"   # 初始为 B，Review 阶段调整
    },
    "product_metadata": {
        "tracks": ["advanced_data_structure"],
        "audience": ["university_icpc", "advanced_competitive_programmer"],
        "visibility": "expert",
        "learning_path_policy": {
            "unlock_mode": "free",
            "required": []
        },
        "localization_status": "en_needed",
        "content_status": "needs_content"
    },
    "tags": [],
    "aliases": [],
    "pickup_group": []
}
```

---

## 六、关键风险与应急

| 风险 | 等级 | 应对 |
|------|------|------|
| 新增节点 direct_pre 含 section id | ⚠️ 高 | 必须在插入前替换为正式 item id |
| 新增节点 direct_pre 悬空引用 | ⚠️ 高 | 必须检查所有引用的 item id 存在于图谱 |
| 新增节点产生 cycle | ⚠️ 高 | 插入前用 compute_resolved 预检测 |
| resolved_pre 覆盖旧节点 | ⚠️ 中 | 严格限定只写回新增节点 |
| metadata 字段缺失 | ⚠️ 中 | 检查所有必需字段 |
| product_metadata_validation 失败 | ⚠️ 中 | 补全缺失字段 |
| 报告文件不一致（report_matches_json） | ⚠️ 中 | 更新报告后运行 validate-only |
| 候选超过 recommended_merge_count | ⚠️ 高 | 严格不超过 2号推荐数量 |
| full_30 中混入非候选池节点 | ⚠️ 高 | 只在 selected_candidates 范围内操作 |

---

## 七、禁止事项

1. ❌ **不得继续 Batch7**（Batch6 完成后必须停止）
2. ❌ 不得修改旧节点 direct_pre / resolved_pre / rel
3. ❌ 不得删除已有节点
4. ❌ 不得重排 section
5. ❌ 不得创建新 section（除非 2号线程明确要求并给出 section 定义）
6. ❌ 不得在 validate-only 失败时强行提交
7. ❌ 不得合并未在 `selected_candidates` 中的候选
8. ❌ 不得修改 review_status（由后续 Fix Lite 处理）
9. ❌ 不得修改 Batch1~5 已合并节点的 resolved_pre

---

## 八、后续路径

```
2号返回 Batch6 full_30 候选文件
  ↓
执行本模板（根据 recommendation 选择对应流程）
  ↓
validate-only 通过
  ↓
输出结果文件
  ├─ data/stage3e_batch6_full30_candidate_to_item_id_mapping.json
  ├─ data/stage3e_batch6_full30_added_items_summary.json
  ├─ data/stage3e_batch6_full30_validation_result.json
  ├─ data/stage3e_batch6_full30_rollback_plan.json
  └─ docs/stage3e_batch6_full30_merge_report.md
  ↓
等待人工审核 Review / Fix Lite
  ↓
生成 Stable Checkpoint
  ↓
讨论是否继续后续阶段（默认不继续 Batch7）
```

---

## 附录：参考实现

### 官方 compute_resolved

代码位置: [refine_item_dependencies.py:L1336-L1351](file:///c:/Users/renfenggo/Documents/trae_projects/suanfatong/refine_item_dependencies.py#L1336-L1351)

```python
def compute_resolved(edges, item_ids):
    memo, visiting = {}, set()
    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))
                out.append(dep)
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])
        return memo[node]
    return {item_id: resolve(item_id) for item_id in item_ids}
```

### Batch3/4/5 成功模式

本模板的 resolved_pre 计算方式借鉴了 Batch3、Batch4 和 Batch5 的验证通过模式：

1. **先插入**：将新增节点先放入内存图谱的 full_item_by_id
2. **再计算**：基于完整 full_item_by_id 使用官方 `compute_resolved` 计算
3. **只写回新增**：只更新新增节点的 resolved_pre，不覆盖旧节点
4. **validate-only 验证**：用官方 validator 确保所有条件满足
