# Stage3G Problem Patterns Sync Triage Template

## Usage

This template is used **after** Thread 2's Stage3G full400 audit completes.

### Pipeline

```
Thread 2: Stage3G full400 Audit ──→ 输出审计结果
                                      │
                                      ▼
Thread 3: 对 possible_problem_pattern 候选进行 triage
         （使用本模板 + checklist）
                                      │
                                      ▼
    输出: stage3g_problem_patterns_sync_triage.json + report
                                      │
                                      ▼
    合并：Batch3 候选 (3) + Stage3G 候选 → Batch4 规划
                                      │
                                      ▼
    等待：主图谱合并、复查、轻量修复完成
                                      │
                                      ▼
    用户指令 → 生成正式 patterns 文件
```

### Context Diagram

```
┌──────────────────────────────────────────────────────┐
│                   Patterns Pipeline                    │
├──────────────────────────────────────────────────────┤
│  Batch1 Ready (83)    ──── 已就绪                      │
│  Batch2 Generated (13) ──── 已正式生成                  │
│  Batch3 Drafts (3):                                    │
│    ├─ pat.dominance_counting         待生成              │
│    ├─ pat.mobius_inversion_application 待生成            │
│    └─ pat.euler_function_application  待生成            │
│  Stage3G (400 pool):                                   │
│    └─ possible_problem_pattern ~98 个 ──→ 本 template │
│         ↓ triage                                      │
│         ├─ create_new_draft_later → Batch4             │
│         ├─ merge_with_existing → 已有 pattern          │
│         ├─ defer → 不生成                              │
│         └─ manual_review → 人工                        │
└──────────────────────────────────────────────────────┘
```

---

## Input Sources

| Source | File | Status |
|:-------|:-----|:-------|
| Stage3G 400 candidate pool | `data/stage3g_standardized_candidate_pool_400.json` | ✅ generated |
| Stage3G generation summary | `data/stage3g_candidate_pool_400_generation_summary.json` | ✅ available |
| Ready patterns (83) | `data/patterns_v0_1_ready.json` | ✅ loaded |
| Batch2 patterns (13) | `data/patterns_batch2.json` | ✅ generated |
| Batch3 draft candidates (3) | `data/patterns_batch3_draft_preview_bundle.json` | ✅ draft_preview |
| Thread 2 audit results | `data/stage3g_full400_audit_result.json` (expected) | ⏳ pending |

---

## Per-Candidate Triage Checklist

### Stage 1: Basic Info

| Field | Value |
|:------|:------|
| candidate_id | e.g. `cand.graph.最短路进阶_同余最短路` |
| item_name | |
| stage3g_candidate_type | modeling_pattern / core_concept / theorem_or_property / etc. |
| possible_problem_pattern (flag) | true / false |
| risk_band | green / yellow / medium / red |
| mapping_confidence | high / medium / low |

### Stage 2: Duplicate Check (4 dimensions)

| # | Check | Result (pass / fail / note) | Reference |
|:-:|:------|:---------------------------|:----------|
| 1 | 是否与 **ready patterns** (83) 重复 | | `patterns_v0_1_ready.json` |
| 2 | 是否与 **patterns_batch2** (13) 重复 | | `patterns_batch2.json` |
| 3 | 是否与 **patterns_batch3 drafts** (3) 重复 | | `patterns_batch3_draft_preview_bundle.json` |
| 4 | 是否属于 **modeling_pattern** 而非纯知识点 | | stage3g_candidate_type |

### Stage 3: Suitability Assessment

| # | Check | Result (Y / N / ?) |
|:-:|:------|:------------------|
| 5 | 是否有明确的题型识别信号？ | |
| 6 | 是否有清晰的建模转化路径？ | |
| 7 | 是否需要 boundary_note？ | |
| 8 | 是否需要人工复查？ | |
| 9 | 是否建议进入 future patterns_batch4？ | |
| 10 | 是否 defer？ | |

### Stage 4: Decision

| Field | Value |
|:------|:------|
| **priority** | P0 / P1 / P2 / defer |
| **decision** | create_new_draft_later / merge_with_existing / defer / manual_review |
| **suggested_pattern_id** | e.g. `pat.congruence_shortest_path` |
| **matched_existing_pattern** | (if merge_with_existing) |
| **matched_batch2_pattern** | (if merge_with_existing) |
| **matched_batch3_draft** | (if covered by batch3 draft) |
| **boundary_note_required** | true / false |
| **boundary_note_targets** | [list of pattern_ids] |
| **reason** | |

---

## Stage3G 400 Pool Quick Reference

### Summary Statistics

| Metric | Value |
|:-------|:------|
| Total candidates | 400 |
| possible_problem_pattern = true | **~98** |
| By type: modeling_pattern | 87 |
| By type: core_concept | 259 |
| By type: implementation_variant | 38 |
| By type: theorem_or_property | 14 |
| By type: application_case | 2 |
| By risk: green | 165 |
| By risk: yellow | 168 |
| By risk: medium | 47 |
| By risk: red | 20 |
| By confidence: high | 165 |
| By confidence: medium | 132 |
| By confidence: low | 103 |

### Themes (12 themes, 400 candidates)

| Theme | Count | Description |
|:------|:-----:|:------------|
| 图论专题 | 55 | Graph theory modeling / algorithms |
| 数据结构专题 | 50 | Data structure variants |
| 动态规划专题 | 45 | DP patterns and optimizations |
| 信奥数学 | 40 | Math / number theory |
| 基础算法扩展 | 35 | Algorithm extensions |
| 字符串专题 | 35 | String algorithms |
| STL与常用库细节 | 30 | STL details |
| 题型建模方法 | 30 | Problem modeling methods |
| C++语法高级细节 | 25 | C++ advanced syntax |
| 编程技巧 | 25 | Programming techniques |
| 比赛相关知识 | 15 | Contest-related knowledge |
| 调试方法 | 15 | Debugging methods |

### Possible Problem Pattern Concentration

By theme, candidates with `possible_problem_pattern=true` are expected to concentrate in:
- **题型建模方法** (30 candidates, high concentration of modeling patterns)
- **图论专题** (55 candidates, many modeling techniques like super source/sink, congruence shortest path)
- **动态规划专题** (45 candidates, DP modeling patterns)
- **数据结构专题** (50 candidates, some may have modeling value)
- **信奥数学** (40 candidates, number theory modeling)

---

## Existing Patterns Reference

### Ready Patterns (83) — Key Boundary Patterns

Pay special attention to these ready patterns when checking for semantic overlap:

| pattern_id | Name | Category | Risk of overlap |
|:-----------|:-----|:---------|:---------------:|
| pat.inclusion_exclusion_counting | 容斥计数 | Competitive Modeling | ⚠️ with number theory candidates |
| pat.modular_counting_pattern | 取模计数模式 | Competitive Modeling | ⚠️ with counting candidates |
| pat.offline_query_pattern | 离线查询模式 | Competitive Modeling | ⚠️ with offline optimization candidates |
| pat.sweep_line_pattern | 扫描线模式 | Competitive Modeling | ⚠️ with event-based candidates |
| pat.coordinate_sweep_compression | 离散化扫描 | Competitive Modeling | ⚠️ preprocessing step |
| pat.fenwick_prefix_maintenance | BIT前缀维护 | Data Structure | ⚠️ implementation tool |
| pat.shortest_path_modeling | 最短路建模 | Graph Modeling | ⚠️ with graph modeling candidates |
| pat.network_flow_modeling | 网络流建模 | Graph Modeling | ⚠️ with flow modeling candidates |
| pat.min_cut_selection | 最小割选择建模 | Graph Modeling | ⚠️ with cut/closure candidates |
| pat.bipartite_matching_modeling | 二分图匹配建模 | Graph Modeling | ⚠️ with matching candidates |

Full ready patterns list (83) — see [patterns_v0_1_ready.json](file:///c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\patterns_v0_1_ready.json)

### Batch2 Patterns (13) — All Graph/Flow

| pattern_id | Title | Category |
|:-----------|:------|:---------|
| pat.circulation_optimization | 最小费用循环流 | 网络流建模 |
| pat.cycle_optimization_modeling | 最小平均环建模 | 图论建模 |
| pat.state_machine_modeling | 状态图建模 | 图论建模 |
| pat.path_cover_modeling | 最小路径覆盖 | 图论建模 |
| pat.bounded_matching_modeling | 带边界二分图匹配 | 网络流建模 |
| pat.flow_bounds_transformation | 流量边界变换 | 网络流建模 |
| pat.min_flow_modeling | 最小流建模 | 网络流建模 |
| pat.k_shortest_modeling | K短路建模 | 图论建模 |
| pat.layered_graph_modeling | 分层图建模 | 图论建模 |
| pat.node_demand_modeling | 节点需求流建模 | 网络流建模 |
| pat.max_flow_with_bounds | 带边界最大流 | 网络流建模 |
| pat.shortest_path_potentials | Johnson势函数 | 最短路优化 |
| pat.stable_matching_pattern | 稳定婚姻问题 | 匹配算法 |

**Merge action**: `2.21.131 Project Selection` → `pat.min_cut_selection` (no separate pattern)

### Batch3 Draft Candidates (3) — Not Yet Generated

| pattern_id | Title | Domain | Status |
|:-----------|:------|:-------|:-------|
| pat.dominance_counting | 多维支配关系计数 | 计数模式 / 多维偏序 | ✅ READY |
| pat.mobius_inversion_application | 莫比乌斯反演应用 | 计数模式 / 数论反演 | ✅ READY |
| pat.euler_function_application | 欧拉函数应用 | 计数模式 / 积性函数 | ✅ READY |

Draft details: [data/patterns_batch3_draft_preview_bundle.json](file:///c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\patterns_batch3_draft_preview_bundle.json)

---

## Stage3G-Specific Handling Notes

### 1. possible_problem_pattern=true but candidate_type≠modeling_pattern

Some candidates may have `possible_problem_pattern=true` but are typed as `core_concept` or `theorem_or_property`. These need **extra scrutiny**:

- **core_concept + flagged**: Assess whether the concept has genuine pattern-level recognition signals. E.g., "LCA与树上差分" has clear recognition signals (路径统计、差分标记) and could be a valid pattern despite being typed as core_concept.
- **theorem_or_property + flagged**: Usually algorithm-only, mark as defer. E.g., "生成树计数" is a theorem application, not a pattern.
- **implementation_variant + flagged**: Usually defer. Implementation variants rarely have pattern-level signals.

### 2. Risk Band and Priority Mapping

| Risk Band | Confidence | Suggested Priority | Suggested Action |
|:----------|:----------:|:------------------:|:-----------------|
| green | high | P1 | High priority for Batch4 |
| yellow | high | P2 | Consider for Batch4 or later |
| green | medium | P2 | Lower priority |
| yellow | medium | defer | Defer unless very strong signal |
| red / medium | any | defer | Not recommended |

### 3. Batch3 Overlap Handling

If a Stage3G candidate overlaps with a Batch3 draft:
- **If partially overlapping**: Mark `batch3_drafts_cover = partial`, add boundary_note, but still generate as independent pattern.
- **If fully covered**: Mark `batch3_drafts_cover = true`, decision = defer, reason = "covered_by_batch3_draft".
- **If clearly distinct sibling pattern**: Mark `batch3_drafts_cover = false`, but add `related_items` reference.

### 4. Scale Control for Batch4

Stage3G may produce many viable candidates. To control batch4 size:
- **Batch4 primary**: green + high + modeling_pattern candidates only (~estimated 30-50)
- **Batch4 secondary**: green + high + possible_problem_pattern but non-modeling (if signal very clear)
- **Defer to later**: yellow/medium + all others

---

## Triage Decision Matrix

| decision | Meaning | Next Step |
|:---------|:--------|:----------|
| **create_new_draft_later** | Valid modeling pattern, no existing coverage | Prepare draft preview → add to batch4 queue |
| **merge_with_existing** | Already covered by an existing pattern | Record merge target as note, no new pattern |
| **defer** | Algorithm-only, too narrow, or not suitable | Keep as knowledge item only |
| **manual_review** | Boundary unclear, needs human judgment | Flag for human reviewer |

## Priority Levels

| Priority | Meaning | Typical Criteria |
|:---------|:--------|:-----------------|
| **P0** | Must have | Core modeling pattern, broad coverage, B+ priority |
| **P1** | Should have | Clear modeling pattern, good coverage, B priority |
| **P2** | Nice to have | Niche but valid modeling pattern, C+ priority |
| **defer** | Not suitable | Algorithm-only, too narrow, duplicate, or risk too high |

---

## Triage Output Format

For each candidate, produce one record in:

**File**: `data/stage3g_problem_patterns_sync_triage.json`

```json
{
  "candidate_id": "cand.graph.最短路进阶_同余最短路",
  "item_name": "最短路进阶：同余最短路",
  "suggested_pattern_id": "pat.congruence_shortest_path",
  "priority": "P1",
  "decision": "create_new_draft_later",
  "stage3g_candidate_type": "modeling_pattern",
  "stage3g_possible_problem_pattern": true,
  "matched_existing_pattern": "",
  "matched_batch2_pattern": "",
  "matched_batch3_draft": "",
  "boundary_note_required": true,
  "boundary_note_targets": ["pat.shortest_path_modeling"],
  "existing_coverage_assessment": {
    "ready_patterns_cover": false,
    "batch2_patterns_cover": false,
    "batch3_drafts_cover": false,
    "overlap_with_existing": "partial",
    "overlap_detail": "pat.shortest_path_modeling covers general shortest path; congruence shortest path is a special modeling technique (mod-based graph construction)."
  },
  "suitable_as_pattern": true,
  "suitable_reason": "Clear recognition signals and transformation path.",
  "recommended_timing": "patterns_batch4",
  "reason": "valid_modeling_pattern"
}
```

---

## Declarations

| Item | Status |
|:-----|:-------|
| ✅ Template prepared | **True** |
| ❌ Generate formal patterns now | **False** |
| ✅ Must wait for Stage3G full400 audit results | **True** |
| ✅ Must wait for main graph merge, review, fix | **True** |
| ❌ Modify main graph | **False** |
| ❌ Modify existing patterns | **False** |
| ❌ Modify batch3 draft files | **False** |

---

*Template prepared by DeepSeek V4 Pro (Thread 3). Apply after Thread 2 outputs Stage3G full400 audit results.*
