# Stage3G full400 Merge 执行模板

## 基本信息

- **批次**: Stage3G full400
- **当前状态**: 主图谱 item_count=1765, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 full400 全量审计完成后，执行合并
- **执行者**: 1号线程 / DeepSeek V4 Pro
- **执行条件**: 2号审计通过 + 所有前置条件满足
- **主图谱**: 未修改（本模板不执行任何修改）
- **来源文件**: `data/stage3g_standardized_candidate_pool_400.json`

---

## 一、2号审计所需输出（等待中）

在执行合并前，必须确认以下 4 个 2号审计输出文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3g_full400_candidate_plan.json` | 最终候选合并计划 | selected_candidates, recommendation, recommended_merge_count |
| 2 | `data/stage3g_full400_dynamic_precheck.json` | 动态预审结果 | item_id 分配, section 分配, risk_band_per_candidate |
| 3 | `data/stage3g_full400_dependency_cleanup_plan.json` | 依赖清理计划 | cleaned_direct_pre_item_ids, cleaned_rel_item_ids, dependency_mapping_risk |
| 4 | `docs/stage3g_full400_precheck_report.md` | 预审报告 | dependency_cleanup_required, section_ref_dependencies, excluded 清单 |

### 2号审计必须确认的检查项

| # | 检查项 | 期望值 |
|:-:|--------|:----:|
| R1 | recommendation | `ready_for_1号线程_merge_full400` |
| R2 | recommended_merge_count | 400 |
| R3 | dependency_cleanup_required | false |
| R4 | dependency_mapping_risk | [] |
| R5 | section_ref_dependencies | [] |
| R6 | excluded_duplicate_or_near_duplicate | [] |
| R7 | excluded_already_merged_candidates | [] |
| R8 | needs_new_section | false |
| R9 | candidate_dependency_cycle | false |
| R10 | validate-only (预审阶段) | passed = true |

---

## 二、合并前前置条件检查（执行时逐项确认）

### 2.1 图谱状态检查

| # | 检查项 | 期望值 | 实际值（由执行时填写） |
|:-:|--------|:------:|:--------------------:|
| P1 | item_count | 1765 | |
| P2 | section_count | 65 | |
| P3 | validate-only | passed = true | |
| P4 | report_matches_json | true | |

### 2.2 2号审计输出检查

| # | 检查项 | 期望值 | 实际值（由执行时填写） |
|:-:|--------|:------:|:--------------------:|
| P5 | selected_candidates 数量 | 400 | |
| P6 | recommendation | ready_for_1号线程_merge_full400 | |
| P7 | recommended_merge_count | 400 | |
| P8 | dependency_cleanup_required | false | |
| P9 | dependency_mapping_risk | [] | |
| P10 | section_ref_dependencies | [] | |
| P11 | needs_new_section | false | |
| P12 | excluded_duplicate_or_near_duplicate | [] | |
| P13 | excluded_already_merged_candidates | [] | |
| P14 | candidate_dependency_cycle | false | |

### 2.3 风险带分布确认

| risk_band | 数量 | 说明 |
|:---------:|:----:|------|
| green | 165 | 直接合并，无需额外处理 |
| yellow | 168 | 合并，须确保 direct_pre 已确认 |
| medium | 47 | 合并前逐项确认依赖映射 |
| red | 20 | **不允许合并**（2号须在审计中排除） |

如果 selected_candidates 中仍包含 red 候选 → **停止合并，报告阻塞**。

### 2.4 候选数据分布（来源：`data/stage3g_standardized_candidate_pool_400.json`）

| 维度 | 分布 |
|:-----|:-----|
| 目标 section 数 | 28 |
| candidate_type | core_concept=259, modeling_pattern=87, implementation_variant=38, theorem_or_property=14, application_case=2 |
| 置信度 | high=165, medium=132, low=103 |

**主要 section 分布**：

| Section | 候选数 | 占比 |
|:-------:|:------:|:----:|
| 2.9 (图基础与遍历) | 129 | 32.3% |
| 2.8 (DP 专题) | 45 | 11.3% |
| 3.13 (高级数据结构) | 26 | 6.5% |
| 3.8 (哈希) | 21 | 5.3% |
| 2.10 (字符串算法) | 21 | 5.3% |
| 2.1 (基础算法) | 17 | 4.3% |
| 2.21 (高级图论) | 17 | 4.3% |
| 4.1 (离散数学) | 16 | 4.0% |
| 4.3 (组合数学) | 15 | 3.8% |
| 4.16 (博弈论) | 15 | 3.8% |
| 其他 18 个 section | 78 | 19.5% |

---

## 三、合并规则

### 3.1 候选筛选规则

1. **只合并 2号审计通过的 400 个 selected_candidates**
2. **不允许合并 risk_band = red 的候选**（即使误入选 selected_candidates，也禁止合并）
3. **不允许合并候选池中的 duplicate / unresolved dependency 候选**
4. **不允许合并任何非 selected_candidates 中的候选**
5. **不允许硬凑候选数**（如果 selected_candidates 不含正好 400 个安全候选，以实际为准）

### 3.2 direct_pre 规则

1. 所有 direct_pre 必须使用正式 item id（如 `2.9.1`），不允许使用 section id（如 `2.9`）
2. **不允许整节展开**：direct_pre 不能包含某个 section 的全部条目
3. 每个节点 direct_pre 原则上控制在 **3～8 个**
4. 特殊情况最多 **12 个**，需标注原因（如多领域交叉依赖）
5. 对 47 个 medium 风险候选，必须逐项确认 direct_pre 指向正式 item id
6. 必须使用 dependency_cleanup_plan 中的 `cleaned_direct_pre_item_ids` / `cleaned_rel_item_ids`

### 3.3 新增节点 metadata 规则

| 字段 | 规则 |
|:-----|:-----|
| id | 2号预审分配的正式 item id，格式为 `X.Y.Z` |
| name, en_name, aliases, global_aliases | 从候选池映射 |
| level | 从预审结果确定 |
| direct_pre | 只允许正式 item id |
| resolved_pre | 先用官方 `compute_resolved` 计算后写入，仅写入新增节点 |
| rel | 使用 cleaned_rel_item_ids |
| tracks, audience, visibility | 从预审结果确定 |
| learning_path_policy | 必须完整，unlock_mode 不允许为 null |
| localization_status, content_status | 设置默认值 |
| platform_tags | 从候选类型推导 |
| review_status | 初始设置 need_manual_review=true, review_priority="B" |

### 3.4 visibility 合法值

只允许使用：`core` / `advanced` / `expert` / `optional`
不允许使用 `intermediate` 或任何其他值。

### 3.5 unlock_mode 规则

推荐 `expert_branch`，**不允许为 null**。

### 3.6 resolved_pre 必须沿用成功策略

1. 先生成 400 个新增 item，resolved_pre 先设为 `[]`
2. 将 400 个新增 item 插入图谱内存结构（不写文件）
3. 基于"旧节点 + 新增400节点"建立完整 item_by_id
4. 使用官方 `compute_resolved` 逻辑计算 resolved_pre
5. **只把计算结果写入新增 400 个节点**
6. **旧节点 resolved_pre 保持原样，绝对不要覆盖**

### 3.7 安全护栏

| 规则 | 说明 |
|:-----|:-----|
| 合并前必须备份 | `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400.json` |
| 不修改已有 item id | 旧节点 id 不能变 |
| 不删除 item | 不执行删除操作 |
| 不重排 section | section 顺序不变 |
| 不创建新 section | 只能用已有 section |
| 新增节点进入预审指定的已有 section | 不能随意分配 section |
| direct_pre 不允许包含 section id | 必须是完整 item id |
| validate-only 失败必须恢复备份 | 不能留下半成品 |

---

## 四、合并执行流程

### Step 1: 加载数据

```
加载:
  - merged_knowledge_graph_item_dependencies_refined.json
  - data/stage3g_full400_candidate_plan.json
  - data/stage3g_full400_dynamic_precheck.json
  - data/stage3g_full400_dependency_cleanup_plan.json
```

### Step 2: 前置条件验证

```
逐项检查 R1-R10 和 P1-P14
任一不满足 → 停止，报告阻塞项
```

### Step 3: 备份主图谱

```
cp -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3g_full400.json
```

### Step 4: 为 400 个候选分配正式 item id

```
按2号预审结果分配，不自行编造
不得与已有 item id 冲突
```

### Step 5: 构建新增节点

```
为每个候选构建完整 item 对象，补齐 metadata
direct_pre 使用 cleaned_direct_pre_item_ids
rel 使用 cleaned_rel_item_ids
resolved_pre 先设为 []
review_status: need_manual_review=true, review_priority="B"
```

### Step 6: 将新增节点插入对应 section

```
按2号预审的 section 分配结果插入
不创建新 section
```

### Step 7: 计算 resolved_pre

```
1. 建立完整 item_by_id（旧 + 新）
2. 使用官方 compute_resolved 计算
3. 只写入新增 400 个节点
4. 旧节点 resolved_pre 不覆盖
```

### Step 8: 更新 validation_baseline

```
graph["meta"]["validation_baseline"] = {
    "item_count": 2165,
    "section_count": 65
}
```

### Step 9: 写入图谱

```
写出 merged_knowledge_graph_item_dependencies_refined.json
同步 merged_knowledge_graph.json
重新生成 item_dependency_refinement_report.md（确保 report_matches_json 后续通过）
```

### Step 10: 运行 validate-only

```
python refine_item_dependencies.py --validate-only \
  --input merged_knowledge_graph_item_dependencies_refined.json \
  --report item_dependency_refinement_report.md \
  --low-conf low_confidence_dependency_review.json \
  --validation dependency_validation_result.json \
  --strict
```

### Step 11: 验证结果

| # | 检查项 | 期望值 |
|:-:|--------|:----:|
| V1 | item_count | **2165** |
| V2 | expected_item_count | **2165** |
| V3 | section_count | 65 |
| V4 | dangling_refs | [] |
| V5 | direct_pre_cycle | null |
| V6 | resolved_pre_mismatches | [] |
| V7 | product_metadata_validation.passed | true |
| V8 | report_matches_json | true |
| V9 | passed | true |

### Step 12: 输出结果文件

```
1. data/stage3g_full400_candidate_to_item_id_mapping.json
2. data/stage3g_full400_added_items_summary.json
3. data/stage3g_full400_validation_result.json
4. data/stage3g_full400_rollback_plan.json
5. docs/stage3g_full400_merge_report.md
```

---

## 五、合并失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
   -> shutil.copy2(backup_path, merged_knowledge_graph_item_dependencies_refined.json)
2. 不要修改旧节点 direct_pre / resolved_pre / rel
3. 输出失败字段和具体节点列表（dangling_refs / mismatch / section_ref 等）
4. 停止，不要继续 Stage3G Batch2
```

---

## 六、合并完成报告必须包含

| # | 内容 |
|---|------|
| 1 | 是否使用 2号审计通过的 full400 文件 |
| 2 | 备份是否成功 |
| 3 | 合并前 item_count (1765) |
| 4 | 合并后 item_count (2165) |
| 5 | 实际新增 item 数 (400) |
| 6 | 新增节点分别进入哪些 section（含各 section 新增数） |
| 7 | risk_band 分布（green/yellow/medium 各合并了多少；red 是否已排除） |
| 8 | 47 个 medium 风险候选是否全部确认 |
| 9 | 是否创建新 section（必须为否） |
| 10 | direct_pre 是否无 section id |
| 11 | 悬空引用是否为 0 |
| 12 | direct_pre 是否无环 |
| 13 | resolved_pre_mismatches 是否为 0 |
| 14 | 旧节点 resolved_pre 是否未覆盖 |
| 15 | product_metadata_validation 是否 passed |
| 16 | report_matches_json 是否 true |
| 17 | validation 是否 passed |
| 18 | 是否生成 rollback plan |
| 19 | 是否建议进入 Stage3G Fix Lite |

---

## 七、后续阶段预览

| 阶段 | 说明 |
|:-----|:-----|
| Stage3G Fix Lite | 对 400 个新增节点降级 review_status |
| Stage3G Review | 2号对 400 个节点做语义审查 |
| Stage3G Stable Checkpoint | 生成阶段性稳定检查点 |
| Stage3G Batch2 | 不自动继续，等用户指令 |
