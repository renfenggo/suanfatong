# Stage3E Batch5 smaller_15 Merge 执行模板

## 一、前置条件

### 1.1 当前图谱基准状态

| 指标 | 当前值 | 要求 |
|------|--------|------|
| item_count | 1602 | 1602 |
| section_count | 65 | 65 |
| validate-only | passed | passed |
| resolved_pre_mismatches | [] | [] |
| dangling_refs | [] | [] |
| direct_pre_cycle | null | null |
| product_metadata_validation | passed | passed |
| report_matches_json | true | true |

### 1.2 必须等待 2号线程返回的文件

在启动 Batch5 Merge 之前，必须确认以下文件已就绪：

| # | 文件 | 状态 |
|---|------|------|
| 1 | `data/thread2_stage3e_aggressive_batch5_selected_candidates.json` | ⏳ 等待 2号返回 |
| 2 | `data/thread2_stage3e_aggressive_batch5_static_precheck.json` | ⏳ 等待 2号返回 |
| 3 | `data/thread2_stage3e_aggressive_batch5_dynamic_precheck.json` | ⏳ 等待 2号返回 |
| 4 | `data/thread2_stage3e_aggressive_batch5_dependency_cleanup.json` | ⏳ 等待 2号返回 |
| 5 | `data/thread2_stage3e_aggressive_batch5_cleaned_dependency_plan.json` | ⏳ 等待 2号返回 |

### 1.3 P0-A 节点确认

根据 [stage3e_p0a_three_node_review.json](file:///c:/Users/renfenggo/Documents/trae_projects/suanfatong/data/stage3e_p0a_three_node_review.json):
- 3 个 P0-A 节点均不阻塞 Batch5（blocks_batch5_count = 0）
- 2.21.76 (Branching Theorem): 需后续补父概念，不阻塞
- 2.21.106 (Dual Shortest Path): 可接受，不阻塞
- 2.21.117 (Tournament Graph): 需后续补父概念，不阻塞
- **结论**: Batch5 可以 proceed

### 1.4 smaller_15 候选上限

- 每次最多 **15 个候选**
- 优先选择 **P0-B** 节点（36 个候选可用），已确认 36 个 P0-B 均不阻塞 Batch5
- 候选应有明确的依赖关系和清晰的边界

---

## 二、合并流程（dependency_cleanup_required = false）

> 适用于 2号线程返回的 `dependency_cleanup.json` 中 `dependency_cleanup_required = false` 的情况。

### Step 1：备份

```bash
Copy-Item merged_knowledge_graph_item_dependencies_refined.json `
    backups\merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch5.json
```

### Step 2：读取候选并构建内存图谱

```python
import json

with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
    graph = json.load(f)

with open("data/thread2_stage3e_aggressive_batch5_cleaned_dependency_plan.json", 'r', encoding='utf-8') as f:
    candidates = json.load(f)

item_by_id = {}
for category in graph["categories"]:
    for section in category["sections"]:
        for item in section["items"]:
            item_by_id[item["id"]] = item
```

### Step 3：将候选插入到内存图谱的对应 section

```python
new_item_ids = []
new_items_by_id = {}

for candidate in candidates:
    item = {
        "id": candidate["item_id"],
        "name": candidate["name"],
        "en_name": candidate.get("en_name", ""),
        "direct_pre": candidate["direct_pre"],  # 使用清洗后的依赖
        "rel": candidate.get("rel", []),
        "resolved_pre": [],  # 暂留空，Step 4 计算
        "review_status": {
            "need_manual_review": True,
            "review_priority": "B"
        },
        # ... metadata
    }
    new_item_ids.append(item["id"])
    new_items_by_id[item["id"]] = item
    
    # 插入到对应 section
    section_id = candidate["section_id"]
    for category in graph["categories"]:
        for section in category["sections"]:
            if section["id"] == section_id:
                section["items"].append(item)
```

### Step 4：合并 item_by_id (旧节点 + 新增节点)

```python
full_item_by_id = {**item_by_id, **new_items_by_id}
```

### Step 5：使用官方 compute_resolved 计算 resolved_pre

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

edges = {
    item_id: [d for d in full_item_by_id[item_id].get("direct_pre", []) if d in full_item_by_id]
    for item_id in full_item_by_id
}

resolved_results = compute_resolved(edges, set(full_item_by_id.keys()))
```

#### resolved_pre 计算规则（必须遵守）

1. 基于 **完整内存图谱**（旧节点 + 新增节点）的 `item_by_id` 计算
2. DFS + memoization
3. 先展开 direct_pre 的 resolved_pre，再追加 direct_pre 本身
4. `unique()` 保持首次出现顺序
5. 不排序
6. 过滤 section id
7. 排除自身

### Step 6：只写回新增节点的 resolved_pre

```python
for item_id in new_item_ids:
    if item_id in resolved_results:
        new_items_by_id[item_id]["resolved_pre"] = resolved_results[item_id]
```

**关键约束**：
- **不覆盖** 旧节点 resolved_pre
- **不覆盖** 其他 Batch 节点 resolved_pre（除非 validate-only 明确指出 mismatch）
- 只写回当前 Batch5 新增节点的 resolved_pre

### Step 7：写入图谱文件

```python
with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
```

### Step 8：运行 validate-only

```bash
python refine_item_dependencies.py --validate-only ^
    --input merged_knowledge_graph_item_dependencies_refined.json ^
    --report item_dependency_refinement_report.md ^
    --low-conf low_confidence_dependency_review.json ^
    --validation dependency_validation_result.json ^
    --strict
```

### Step 9：验证成功标准

| 检查项 | 期望值 |
|--------|--------|
| item_count | **1617** (1602 + N，N ≤ 15) |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

### Step 10：如果验证失败

```bash
# 恢复备份
Copy-Item backups\merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch5.json `
    merged_knowledge_graph_item_dependencies_refined.json
```

---

## 三、合并流程（dependency_cleanup_required = true）

> 适用于 2号线程返回的 `dependency_cleanup.json` 中 `dependency_cleanup_required = true` 的情况。

### 处理流程

```
Step 1: 备份
  ↓
Step 2: 读取 thread2 返回的 cleaned_dependency_plan.json
  ↓
Step 3: 读取 dependency_cleanup.json 中的 cleanup_rules
  ↓
Step 4: 按 cleanup_rules 修改候选的 direct_pre
  │        - 替换 section id 为正式 item id
  │        - 补充语义缺失的依赖
  │        - 移除循环依赖
  ↓
Step 5: 确认修改后 direct_pre 不含 section id、不含悬空引用、不含 cycle
  ↓
Step 6: 将候选插入内存图谱
  ↓
Step 7: 合并 item_by_id，使用官方 compute_resolved 重算新增节点 resolved_pre
  ↓
Step 8: 运行 validate-only
  ↓
Step 9: 验证通过 → 完成
  ↓
Step 10: 验证失败 → 恢复备份
```

### cleanup 规则

1. **section id 替换**: direct_pre 中不能包含 `2.21`, `3.13` 等 section id
2. **悬空引用检查**: 所有 direct_pre 引用的 item id 必须存在于图谱中
3. **循环依赖检查**: 修改后不能产生 direct_pre cycle
4. **最小修改原则**: 只修改明确指出的问题节点，不修改其他节点

---

## 四、新增节点 metadata 要求

每个新增节点必须包含以下字段：

```python
{
    "id": "2.21.xxx",           # item id
    "name": "节点中文名",         # 中文名称
    "en_name": "English Name",   # 英文名称
    "direct_pre": ["2.x.x"],     # 直接前置依赖（只含正式 item id）
    "rel": ["2.x.x"],            # 强相关（可选）
    "resolved_pre": [],          # 由 compute_resolved 自动计算
    "review_status": {
        "need_manual_review": True,
        "review_priority": "B"   # 初始为 B，Review 阶段调整
    },
    "product_metadata": {
        "tracks": ["advanced_graph"],
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

## 五、validate-only 成功标准（汇总）

```json
{
    "item_count": 1617,
    "section_count": 65,
    "duplicate_item_ids": [],
    "dangling_refs": [],
    "direct_pre_cycle": null,
    "self_in_resolved_pre": [],
    "direct_pre_section_refs": 0,
    "resolved_pre_section_refs": {"count": 0, "refs": []},
    "rel_section_refs": {"count": 0, "refs": []},
    "direct_pre_item_ref_ratio": 1.0,
    "report_matches_json": true,
    "low_conf_ids_not_in_graph": [],
    "parent_concept_self_refs": [],
    "product_metadata_validation": {"passed": true},
    "resolved_pre_mismatches": [],
    "passed": true
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
| 报告文件不一致 | ⚠️ 低 | 运行 validate-only 后自动更新 |
| 候选超过 15 个 | ⚠️ 高 | 严格限制 ≤15，超出的候选排入下一 batch |

---

## 七、禁止事项

1. ❌ 不得继续 Batch6（即使本 batch 只有少量候选）
2. ❌ 不得修改旧节点 direct_pre / resolved_pre / rel
3. ❌ 不得删除已有节点
4. ❌ 不得重排 section
5. ❌ 不得创建新 section（除非 2号线程明确要求并给出 section 定义）
6. ❌ 不得在 validate-only 失败时强行提交

---

## 八、后续路径

```
2号返回 Batch5 候选文件
  ↓
执行本模板 Step 1~9
  ↓
validate-only 通过
  ↓
输出结果文件
  ├─ data/stage3e_aggressive_batch5_merge_applied_patch.json
  ├─ data/stage3e_aggressive_batch5_merge_validation_result.json
  └─ docs/stage3e_aggressive_batch5_merge_report.md
  ↓
等待人工审核 Review / Fix Lite
  ↓
生成 Stable Checkpoint
  ↓
讨论是否继续 Batch6（需额外决策，默认不继续）
```

---

## 附录：参考实现

### Batch3/Batch4 成功模式

本模板的 resolved_pre 计算方式借鉴了 Batch3 和 Batch4 的验证通过模式：

1. **先插入**：将新增节点先放入内存图谱的 item_by_id
2. **再计算**：基于完整 item_by_id 使用官方 `compute_resolved` 计算
3. **只写回新增**：只更新新增节点的 resolved_pre，不覆盖旧节点
4. **validate-only 验证**：用官方 validator 确保所有条件满足

### compute_resolved 官方实现

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

---

**模板生成时间**: 2026-05-25
**生成人**: 1号线程 / GLM5
**主图谱是否修改**: ❌ 否（本模板仅作规划，不执行合并）