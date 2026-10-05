# Order Statistics / Dominance Query Pattern Suite Plan 报告

## 套件概况

| 指标 | 结果 |
|:----|:----:|
| **套件名称** | Order Statistics / Dominance Query Pattern Suite |
| **总候选成员** | 4 |
| **生成 pattern** | 1（pat.dominance_counting） |
| **保持为知识项** | 3（CDQ 分治、MST 2D、Bitset 矩形查询） |
| **ready pattern 冲突** | 0 |
| **batch2 pattern 冲突** | 0 |

---

## 套件架构

```
┌─────────────────────────────────────────────────────────┐
│  Order Statistics / Dominance Query Pattern Suite        │
│                                                         │
│  ┌─ Pattern Layer（问题建模 — 生成独立 pattern）──────┐ │
│  │  pat.dominance_counting       ★ 推荐生成           │ │
│  │  多维支配关系计数                                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                         ↓ 引用                           │
│  ┌─ Implementation Layer（算法实现 — 知识项）─────────┐ │
│  │  3.13.181  CDQ Divide Conquer   (core_concept)     │ │
│  │  3.13.179  MST 2D Dominance     (impl_variant)     │ │
│  │  3.13.180  Bitset Rect Query    (impl_variant)     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─ Related Ready Patterns ───────────────────────────┐ │
│  │  pat.offline_query_pattern        (general)        │ │
│  │  pat.fenwick_prefix_maintenance   (tool)           │ │
│  │  pat.coordinate_sweep_compression (preprocessing)  │ │
│  │  pat.sweep_line_pattern           (sibling)        │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 成员明细

### 1. pat.dominance_counting — 建议生成

| 属性 | 值 |
|:----|:----|
| **来源** | 3.13.182 Multidimensional: Dominance Counting |
| **类型** | `modeling_pattern` |
| **优先级** | **B**（Batch1 唯一保留 B 级的节点） |
| **套件角色** | 核心模式 — 问题识别与建模 |
| **状态** | ✅ **ready_later** |

**主用途**：统计满足多维偏序关系的点对数量。

**边界说明**：与实现层节点（CDQ、MST 2D、Bitset）是抽象建模 vs 具体实现的关系，通过 related_items 引用即可。

**推荐操作**：在 future batch 中生成正式 pattern。

---

### 2. CDQ Divide Conquer（3.13.181）— 不生成 pattern

| 属性 | 值 |
|:----|:----|
| **类型** | `core_concept` |
| **优先级** | C |
| **套件角色** | 主流实现算法 |
| **状态** | ❌ **defer** |

**理由**：core_concept 类型不适合 pattern。算法框架的识别信号单一，没有多样化的建模选择。在 pat.dominance_counting 的 related_items 中引用即可。

---

### 3. Merge Sort Tree 2D Dominance（3.13.179）— 不生成 pattern

| 属性 | 值 |
|:----|:----|
| **类型** | `implementation_variant` |
| **优先级** | C |
| **套件角色** | 二维场景的具体实现方案 |
| **状态** | ❌ **defer** |

**理由**：implementation_variant 类型，仅解决二维支配查询。作为知识图谱中的实现参考节点即可。

---

### 4. Bitset Rectangle Query（3.13.180）— 不生成 pattern

| 属性 | 值 |
|:----|:----|
| **类型** | `implementation_variant` |
| **优先级** | C |
| **套件角色** | Bitset 优化实现方案 |
| **状态** | ❌ **defer** |

**理由**：implementation_variant 类型。作为知识图谱中的优化技巧节点即可。

---

## 与 ready patterns 的关系

| ready pattern | 关系 | 说明 |
|:-------------|:----:|------|
| pat.offline_query_pattern | general_vs_specific | Dominance Counting 是离线查询的特例（多维偏序计数） |
| pat.fenwick_prefix_maintenance | uses_as_tool | BIT 是 Dominance Counting 合并阶段的常用工具 |
| pat.coordinate_sweep_compression | uses_as_preprocessing | 离散化是可能的预处理步骤 |
| pat.sweep_line_pattern | sibling | 扫描线也排序后扫描，但处理几何/区间事件 |
| pat.order_statistic_maintenance | unrelated | 动态数据结构，不相关 |

无 ready pattern 冲突 ✅

---

## 生成策略

| 策略 | 值 |
|:-----|:----|
| **推荐方式** | suite_generation |
| **生成 pattern** | `pat.dominance_counting` 一个 |
| **引用实现节点** | 3.13.181（CDQ）、3.13.179（MST 2D）、3.13.180（Bitset） |
| **建议批次** | future patterns batch（next_batch） |
| **排除生成** | CDQ 分治、MST 2D、Bitset 矩形查询（均不适合 pattern） |

---

## 声明

| 项目 | 状态 |
|:----|:----:|
| ✅ Suite Plan 已完成 | **是** |
| ❌ 是否生成正式 patterns | **否** |
| ❌ 是否修改主图谱 | **否** |
| ❌ 是否修改 patterns_v0_1_ready.json | **否** |
| ❌ 是否修改 patterns_batch2.json | **否** |

---

**报告结束** | Suite Plan 完成。推荐在 future batch 中生成 pat.dominance_counting，CDQ 分治等 3 个节点保持为知识项。
