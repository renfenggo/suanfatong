# Patterns Backlog Status After Stage3F Batch2

## 全景概览

| 类别 | 数量 | 说明 |
|:----|:----:|:-----|
| Batch1 Ready Patterns | **83** | 已就绪基线 |
| Batch2 正式生成 | **13** | 2026-05-23 生成，12/12 验证通过 |
| Batch2 Merge Actions | **1** | Project Selection → pat.min_cut_selection |
| Future Batch3 候选 | **1** | Dominance Counting（已准备就绪） |
| 待 Triage 候选 | **1** | 莫比乌斯反演应用（4.9.5） |
| 已 Defer 候选 | **5** | BM 算法, Min_25 筛, CDQ 分治, MST 2D, Bitset 矩形查询 |
| 当前建议生成 Batch3 | **否** | 建议先等 Stage3F Batch3 Review 完成 |

---

## 1. ✅ 已正式生成：patterns_batch2

**验证结果：ALL PASSED（12/12）**

### 网络流建模（6）

| pattern_id | 标题 | 难度 |
|:-----------|:-----|:----:|
| pat.circulation_optimization | 最小费用循环流 | expert |
| pat.bounded_matching_modeling | 带边界二分图匹配 | advanced |
| pat.flow_bounds_transformation | 流量边界变换 | advanced |
| pat.min_flow_modeling | 最小流建模 | advanced |
| pat.node_demand_modeling | 节点需求流建模 | advanced |
| pat.max_flow_with_bounds | 带边界最大流 | advanced |

### 图论建模（4+1）

| pattern_id | 标题 | 难度 |
|:-----------|:-----|:----:|
| pat.cycle_optimization_modeling | 最小平均环建模 | advanced |
| pat.state_machine_modeling | 状态图建模 | intermediate |
| pat.path_cover_modeling | 最小路径覆盖 | advanced |
| pat.k_shortest_modeling | K短路建模 | advanced |
| pat.layered_graph_modeling | 分层图建模 | advanced |

### 最短路优化（1）

| pattern_id | 标题 | 难度 |
|:-----------|:-----|:----:|
| pat.shortest_path_potentials | Johnson势函数 | advanced |

### 匹配算法（1）

| pattern_id | 标题 | 难度 |
|:-----------|:-----|:----:|
| pat.stable_matching_pattern | 稳定婚姻问题 | advanced |

### Merge Action

| 源 | 目标 | 原因 |
|:---|:-----|:-----|
| 2.21.131 Project Selection | pat.min_cut_selection | 经典应用场景，不单独成 pattern |

---

## 2. 📋 Future Batch3 候选

### Dominance Counting（3.13.182）— 已准备就绪

| 属性 | 值 |
|:-----|:----|
| **优先级** | P1 |
| **类型** | modeling_pattern |
| **Triage** | create_new_draft_later ✅ |
| **Draft Preview** | ✅ 已完成 |
| **Boundary Review** | ✅ RETAIN |
| **Suite Plan** | ✅ 已完成 |
| **Generation Checklist** | ✅ 已完成 |
| **Ready to Generate** | ⚠️ 是，但需等 Batch3 Review 完成 |

**前置条件**：
1. Stage3F Batch3 Review / Fix Lite 完成
2. 用户发出生成 patterns_batch3.json 指令

**待补充**（可选改进）：
- 与 pat.sweep_line_pattern 的边界说明
- 场景对比表（Dominance Counting vs 离线查询 vs 扫描线）

---

## 3. ⏳ 待 Triage 候选

### 莫比乌斯反演应用（4.9.5）— 未完成 Triage

| 属性 | 值 |
|:-----|:----|
| **来源** | Stage3F Batch2 Added Items Review |
| **Review 结果** | move_to_problem_patterns |
| **Item 类型** | modeling_pattern |
| **Triage 状态** | ❌ 未完成 |

**已知信息**：
- direct_pre: 4.9.2 莫比乌斯反演
- 所属 section: 4.9 狄利克雷卷积/莫比乌斯反演
- tracks: icpc, advanced_math, noi
- review_priority: C

**待判断事项**：
1. 识别信号是否足够独特（倍数/因子计数、gcd 统计、容斥转化）
2. 是否与 ready pattern `pat.inclusion_exclusion_counting` 有语义重叠
3. 是否需要 boundary_note
4. 最终决策：create_new_draft_later | defer | manual_review

---

## 4. ❌ Defer 候选

| 候选 | 来源 | 原因 | 重新评估条件 |
|:----|:----:|:-----|:-----------|
| Berlekamp-Massey (2.17.20) | Batch1 Triage | algorithm_only，识别信号单一 | 除非出现"线性递推求解模式"统一建模 |
| Min_25 筛 (4.9.3) | Batch1 Triage | algorithm_only，无多样化建模路径 | 除非将多个积性函数方法统一建模 |
| CDQ 分治 (3.13.181) | Suite Plan | core_concept，不适合 pattern | 在 Dominance Counting 中引用即可 |
| MST 2D Dominance (3.13.179) | Suite Plan | implementation_variant | 在 Dominance Counting 中引用即可 |
| Bitset Rectangle Query (3.13.180) | Suite Plan | implementation_variant | 在 Dominance Counting 中引用即可 |

---

## 5. 🔮 Stage3F Batch3 潜在来源

| 属性 | 值 |
|:-----|:----|
| **当前状态** | Stage3F Batch3 full_40 Merge in progress |
| **预计新增知识项** | ~80+ |
| **预期 problem_pattern 候选** | 待 merge 完成后从 added_items_review 中提取 |
| **估算批次容量** | 类似 Batch2 经验，少量 candidate |

---

## 6. Backlog 流水线总览

```
Batch1 Ready (83) ────────────────────────────────────────── 已就绪
     │
Batch2 Generated (13 patterns + 1 merge) ────────────────── 已正式生成
     │
     ├── Future Batch3 候选 (1)
     │   └─ Dominance Counting ── ready ✅
     │
     ├── 待 Triage (1)
     │   └─ 莫比乌斯反演应用 ── pending triage
     │
     ├── Defer (5)
     │   ├─ Berlekamp-Massey
     │   ├─ Min_25 筛
     │   ├─ CDQ 分治
     │   ├─ MST 2D Dominance
     │   └─ Bitset Rectangle Query
     │
     └── Stage3F Batch3 Merge (in progress)
         └─ ~80+ 新增知识项 → 可能产生新候选
```

---

## 7. 推荐结论

| 决策 | 结论 |
|:-----|:----:|
| 是否建议现在生成 patterns_batch3 | ❌ **否** |
| 是否建议等 Stage3F Batch3 Review 后统一生成 | ✅ **是** |
| 是否修改主图谱 | ❌ **否** |
| 是否修改已有 patterns | ❌ **否** |

**下一步行动**：
1. 完成 Stage3F Batch3 full_40 Merge
2. 完成 Batch3 Added Items Review → 标记 move_to_problem_patterns 候选
3. 完成 Batch3 Problem Patterns Sync Triage
4. 对 4.9.5 莫比乌斯反演应用 完成 triage
5. 结合 Batch3 结果 + Dominance Counting + 莫比乌斯反演，统一规划 patterns_batch3
6. 收到用户指令后生成 patterns_batch3.json

---

**报告结束** | Backlog 状态已整理。建议暂缓生成，等 Stage3F Batch3 完成后统一规划。
