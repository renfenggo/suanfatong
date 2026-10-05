# Stage3E Batch6 Pre-Merge Duplicate Guard 模板

## 一、背景

在 Batch6 full_30 Merge 前置检查中，2号线程 v1 dynamic_precheck 的 `already_merged_candidates: []` 出现了 **漏检**：实际发现 8 个候选已在 Batch3/Batch4 合并过，但预审报告未检出。

为防止类似漏检再次发生，本模板定义一套完整的 Merge 前重复检查守卫流程。

## 二、检查层级

### Level 1：candidate_id 精确匹配（必检）

对每个 BatchX 待合并候选，逐一遍历 **Batch1~Batch(X-1) 全部 candidate_to_item_id_mapping.json**，检查 candidate_id 是否已在之前批次中出现。

**检查文件**：
- `data/stage3e_aggressive_batch1_candidate_to_item_id_mapping.json`
- `data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json`
- `data/stage3e_aggressive_batch3_candidate_to_item_id_mapping.json`
- `data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json`
- `data/stage3e_batch5_smaller15_candidate_to_item_id_mapping.json`

**判断逻辑**：
```python
all_graph_item_ids = set(item["id"] for item in full_graph_items)
already_merged = set()

# 对每个 mapping 文件
for bf in batch_mapping_files:
    d = json.load(open(bf))
    if isinstance(d, list):
        for m in d:
            # 必须确认 item_id 真的在图谱中（而非仅存在于 mapping 文件）
            if m.get("item_id") and m["item_id"] in all_graph_item_ids:
                already_merged.add(m["candidate_id"])
    elif isinstance(d, dict):
        for cid, iid in d.items():
            if iid and iid in all_graph_item_ids:
                already_merged.add(cid)
```

**检查要点**：
- ✅ 必须同时验证 `item_id` 是否存在于当前主图谱（而非仅看 mapping 文件）
- ✅ 如果 candidate_id 在 mapping 中但 `item_id` 不在图谱中，说明该候选虽已分配但未被合并，不算重复

**风险**：candidate_id 精确匹配只能检出 **同一候选池来源** 的重复，不同池（如 codex_pool vs reserve_pool）的同名节点需要 Level 2。

---

### Level 2：name / en_name 近重复检查（必检）

对每个候选的 `name` 和 `en_name`，与当前图谱全部 item 的名称进行模糊匹配。

**匹配规则**：
```python
def is_duplicate_name(candidate_name, existing_items):
    """检查候选名称是否与已存在节点近重复"""
    for item in existing_items:
        # 精确匹配
        if candidate_name == item.get("name", ""):
            return True, "exact_name_match"
        if candidate_name == item.get("en_name", ""):
            return True, "exact_en_name_match"
        
        # 去空格/标点后的匹配
        c_clean = re.sub(r"[：\-/\s]", "", candidate_name)
        e_clean = re.sub(r"[：\-/\s]", "", item.get("name", ""))
        if c_clean == e_clean:
            return True, "clean_name_match"
        
        # 英文名核心词匹配（取第一个主要部分）
        c_en_core = candidate_name.split(":")[-1].strip() if ":" in candidate_name else candidate_name
        e_en_core = item.get("en_name", "").split(":")[-1].strip() if ":" in item.get("en_name", "") else item.get("en_name", "")
        if c_en_core and c_en_core == e_en_core:
            return True, "en_core_match"
    
    return False, None
```

**已发现的近重复案例**：
| candidate_id | 候选名称 | 图谱已有名称 | 图谱 item_id | 匹配类型 |
|-------------|----------|-------------|-------------|----------|
| `cand.graph.flow_bounds.demands` | 上下界网络流：Demands | 上下界网络流：Demands | 2.21.125 | exact_name_match |
| `cand.graph.flow_bounds.edge_lower_bound_transform` | 上下界网络流：Edge Lower Bound Transform | 上下界网络流：Edge Lower Bound Transform | 2.21.126 | exact_name_match |

这两个候选的 candidate_id 与 Batch3 mapping 中不同（代码池来源不同），但 **名称完全一致**，Level 1 无法检出，必须依赖 Level 2。

---

### Level 3：aliases 交叉检查（建议）

对候选的 `aliases`、`global_aliases`、`tags` 与现有节点的对应字段交叉比对。

```python
def check_aliases_overlap(candidate, existing_items):
    cand_aliases = set(candidate.get("aliases", []) + candidate.get("global_aliases", []))
    for item in existing_items:
        item_aliases = set(item.get("aliases", []) + item.get("global_aliases", []))
        overlap = cand_aliases & item_aliases
        if overlap:
            return True, overlap
    return False, set()
```

---

### Level 4：direct_pre 指向已有同名节点时的风险检查（建议）

如果候选的 `direct_pre` 中某个引用的目标节点与候选本身同名或同义，说明该候选可能是重复的。

```python
def check_direct_pre_duplicate_risk(candidate, item_by_id):
    """候选的 direct_pre 是否指向与候选同名的节点"""
    for dep_id in candidate.get("direct_pre", []):
        dep_item = item_by_id.get(dep_id)
        if dep_item:
            dep_name = dep_item.get("name", "")
            cand_name = candidate.get("name", "")
            if dep_name == cand_name:
                return True, f"direct_pre {dep_id} 与候选同名: {dep_name}"
    return False, None
```

---

### Level 5：section 目标一致性检查（建议）

检查候选的 `target_section` 与对应已存在节点的实际 section 是否一致。

```python
def check_section_consistency(candidate, existing_items):
    """如果候选名称出现在已有节点中，检查 section 是否匹配"""
    for item in existing_items:
        if candidate.get("name") == item.get("name", ""):
            actual_sec = ".".join(item["id"].split(".")[:2])
            target_sec = candidate.get("target_section", "")
            if actual_sec != target_sec:
                return True, f"section 不一致: 实际在 {actual_sec}, 候选目标 {target_sec}"
    return False, None
```

**已发现的 section 不一致案例**：
| candidate_id | 候选 target_section | 图谱实际 section |
|-------------|-------------------|-----------------|
| `cand.graph.matching_cover.stable_marriage` | 2.15 | **2.21**（2.21.143） |
| `cand.graph.matching_cover.konig_theorem` | 2.15 | **2.21**（2.21.140） |

---

## 三、已发现的重复候选清单

### 3.1 Batch4 重复（6 个）

| # | candidate_id | 图谱 item_id | 图谱名称 | 合并批次 |
|---|-------------|-------------|----------|---------|
| 1 | `cand.graph.matching_cover.stable_marriage` | 2.21.143 | 匹配与覆盖：Stable Marriage | Batch4 |
| 2 | `cand.graph.matching_cover.minimum_path_cover` | 2.21.142 | 匹配与覆盖：Minimum Path Cover | Batch4 |
| 3 | `cand.graph.matching_cover.dilworth_theorem` | 2.21.138 | 匹配与覆盖：Dilworth Theorem | Batch4 |
| 4 | `cand.graph.matching_cover.konig_theorem` | 2.21.140 | 匹配与覆盖：Konig Theorem | Batch4 |
| 5 | `cand.graph.matching_cover.weighted_general_matching` | 2.21.145 | 匹配与覆盖：Weighted General Matching | Batch4 |
| 6 | `cand.graph.flow_bounds.minimum_flow` | 2.21.129 | 上下界网络流：Minimum Flow | Batch4 |

### 3.2 Batch3 重复（2 个，Level 1 + Level 2 联合检出）

| # | candidate_id | 图谱 item_id | 图谱名称 | 合并批次 |
|---|-------------|-------------|----------|---------|
| 7 | `cand.graph.flow_bounds.demands` | 2.21.125 | 上下界网络流：Demands | Batch3 |
| 8 | `cand.graph.flow_bounds.edge_lower_bound_transform` | 2.21.126 | 上下界网络流：Edge Lower Bound Transform | Batch3 |

### 3.3 未被重复影响的候选（22 个）

除去以上 8 个重复，Batch6 full_30 剩余 **22 个有效候选**（不是 24，而是 22）：
- 3.13 系列（李超线段树、可并堆、Segment Tree Beats 等）：15 个
- 3.13 Dynamic Tree 系列（virtual_subtree_aggregate 等）：5 个
- 3.13 Bitset Linear Basis：1 个
- 2.21 匹配系列（blossom_algorithm）：1 个

---

## 四、处理规则

### 规则 1：发现重复必须停止

> **如果任何 Level 1~5 检查发现重复，必须停止合并，不得自动排除重复后继续。**

不允许以下自动行为：
- ❌ 不允许自动去掉重复后继续合并剩余的 22/24 个
- ❌ 不允许自动降级为 fallback_20
- ❌ 不允许自动选择另一组候选

### 规则 2：等待 2号 v2 动态预审

> 必须以 2号线程重新生成的 v2 动态预审结果为准。

```python
v2_precheck = json.load(open("data/thread2_stage3e_batch6_full30_dynamic_precheck_v2.json"))
if v2_precheck["already_merged_candidates"] == [] and \
   v2_precheck["recommendation"] == "ready_for_1号线程_merge_full30":
    # 确认 v2 已修复重复漏检问题
    # 可以继续执行合并
    pass
else:
    # 仍然有重复 → 继续等待
    pass
```

### 规则 3：重复检查必须在 validate-only 之前独立执行

重复检查是 **独立于 validate-only** 的前置步骤，validate-only 通过不代表没有重复。

---

## 五、检查脚本模板

```python
import json, re

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
CANDIDATE_PLAN_PATH = "data/thread2_stage3e_batch6_full30_candidate_plan.json"
BATCH_MAPPING_FILES = [
    "data/stage3e_aggressive_batch1_candidate_to_item_id_mapping.json",
    "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json",
    "data/stage3e_aggressive_batch3_candidate_to_item_id_mapping.json",
    "data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json",
    "data/stage3e_batch5_smaller15_candidate_to_item_id_mapping.json",
]

def run_duplicate_guard():
    graph = json.load(open(GRAPH_PATH))
    candidate_plan = json.load(open(CANDIDATE_PLAN_PATH))
    
    # Build existing item set by ID and name lookup
    all_items = []
    all_item_ids = set()
    name_to_items = {}
    for cat in graph["categories"]:
        for sec in cat["sections"]:
            for item in sec["items"]:
                all_items.append(item)
                all_item_ids.add(item["id"])
                name_to_items.setdefault(item["name"], []).append(item)
                if item.get("en_name"):
                    name_to_items.setdefault(item["en_name"], []).append(item)
    
    # Level 1: candidate_id exact match
    already_merged_ids = set()
    for bf in BATCH_MAPPING_FILES:
        d = json.load(open(bf))
        if isinstance(d, list):
            for m in d:
                if m.get("item_id") and m["item_id"] in all_item_ids:
                    already_merged_ids.add(m["candidate_id"])
        elif isinstance(d, dict):
            for cid, iid in d.items():
                if iid and iid in all_item_ids:
                    already_merged_ids.add(cid)
    
    # Level 2: name near-duplicate check
    issues = []
    for c in candidate_plan["candidates"]:
        cid = c["candidate_id"]
        name = c["name"]
        
        # Level 1 check
        if cid in already_merged_ids:
            issues.append({
                "candidate_id": cid,
                "name": name,
                "check_level": "L1_candidate_id",
                "detail": f"candidate_id 已在之前批次合并过",
            })
            continue
        
        # Level 2 name check
        if name in name_to_items:
            for existing in name_to_items[name]:
                issues.append({
                    "candidate_id": cid,
                    "name": name,
                    "check_level": "L2_name_exact",
                    "detail": f"名称 '{name}' 已存在于图谱 {existing['id']}",
                })
    
    return {
        "total_candidates": len(candidate_plan["candidates"]),
        "duplicates_found": len(issues),
        "issues": issues,
        "guard_passed": len(issues) == 0,
    }
```

---

## 六、当前状态声明

| 事项 | 状态 |
|------|------|
| 当前是否执行合并 | **否** |
| 当前是否修改主图谱 | **否** |
| 当前主图谱 item_count | 1617（未修改） |
| 合并是否被阻止 | **是，重复守卫拦截** |
| 是否等待 2号 v2 动态预审 | **是** |
| 等待文件 | `data/thread2_stage3e_batch6_full30_dynamic_precheck_v2.json` |
| 预期 v2 修复项 | `already_merged_candidates` 必须包含 8 个重复候选 |
