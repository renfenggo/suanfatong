# Stage3F Batch3 Full40 Problem Patterns Sync Triage 报告

## 分级概况

| 指标 | 结果 |
|:----|:----:|
| **候选总数** | **2** |
| **create_new_draft_later** | **1**（欧拉函数应用） |
| **merge_with_existing** | **0** |
| **defer** | **1**（线段树变体：Split） |
| **manual_review** | **0** |
| **是否生成正式 patterns** | ❌ **否** |
| **是否修改主图谱** | ❌ **否** |

---

## 候选 1：欧拉函数应用（4.9.6）✅ create_new_draft_later

### 基础信息

| 属性 | 值 |
|:-----|:----|
| **Item ID** | 4.9.6 |
| **知识项类型** | `modeling_pattern` |
| **Review 结果** | approve, sync_to_problem_patterns=true |
| **所属 Section** | 4.9 高级数学 |
| **直接前置** | 4.1.10（欧拉函数）, 4.1.11 |
| **tracks** | icpc, advanced_math, noi |

### 适配性评估

| 检查项 | 结果 | 说明 |
|:-------|:----:|:-----|
| 与 ready patterns 重复 | ❌ 无 | pat.inclusion_exclusion_counting 有部分交集但不同 |
| 与 batch2 patterns 重复 | ❌ 无 | 全部为图论/网络流，不相关 |
| 与 Dominance Counting suite 相关 | ❌ 无 | 不同领域 |
| 属于 modeling_pattern | ✅ 是 | Review 已标记 item_type=modeling_pattern |
| 有明确识别信号 | ✅ 是 | 互质计数 / gcd 统计 / 欧拉降幂 / 阶乘互质部分 |
| 有固定转化路径 | ✅ 是 | 筛法求欧拉函数 + 根据场景使用互质性质/降幂 |
| 是否需要 boundary_note | ✅ 是 | 与 pat.inclusion_exclusion_counting、pat.modular_counting_pattern |
| 是否需要人工复查 | ❌ 否 | AI 可直接决策 |

### 决策

```
decision: create_new_draft_later
priority: P1
suggested_pattern_id: pat.euler_function_application
```

### 与 4.9.5 莫比乌斯反演应用的关系

两者同属 4.9 高级数学 Section，都是积性函数应用类 modeling_pattern：

| 维度 | 欧拉函数应用 (4.9.6) | 莫比乌斯反演应用 (4.9.5) |
|:----|:--------------------|:------------------------|
| 核心工具 | 欧拉函数 φ(n) | 莫比乌斯函数 μ(n) |
| 典型场景 | 互质计数、降幂、阶乘互质 | 倍数/因子计数、gcd 统计、容斥转化 |
| 待 triage 状态 | ✅ 已完成 | ⏳ 待完成 |

**建议**：在 batch3 中统一处理，reference 关系。

---

## 候选 2：线段树变体：Split（3.13.190）❌ defer

### 基础信息

| 属性 | 值 |
|:-----|:----|
| **Item ID** | 3.13.190 |
| **知识项类型** | `implementation_variant` |
| **Review 结果** | approve, **sync_to_problem_patterns=false** |
| **所属 Section** | 3.13 高级数据结构扩展 |
| **直接前置** | 3.7.2（线段树） |
| **rel** | 3.7.22（线段树分裂，已存在） |

### 适配性评估

| 检查项 | 结果 | 说明 |
|:-------|:----:|:-----|
| 与 ready patterns 重复 | ❌ 无 | 但问题不在此 |
| 与 batch2 patterns 重复 | ❌ 无 | 不相关 |
| 属于 modeling_pattern | ❌ 否 | **类型为 implementation_variant** |
| 有明确识别信号 | ❌ 否 | Split 是操作，不是问题类型 |
| 有固定转化路径 | ❌ 否 | 操作本身固定，不存在建模选择 |
| 是否需要 boundary_note | ❌ 不需要 | 不生成 pattern |
| 是否需要人工复查 | ❌ 否 | AI 可直接决策 |

### 关键发现：sync_candidates.json 与 Review 数据不一致

```
sync_candidates.json:  suggested_item_type = "modeling_pattern"  ← 不准确
added_items_review.json: item_type = "implementation_variant"    ← 正确
                         sync_to_problem_patterns = false        ← 不推荐
```

本 triage 以 **Review 数据**为准。Sync candidates 文件中的类型建议不准确。

### 决策

```
decision: defer
priority: defer
suggested_pattern_id: (无)
reason: implementation_variant_only
```

**不生成 pattern。** 保持为知识图谱算法节点。已在图谱中与 3.7.22（线段树分裂）建立 rel 关系。

---

## 积分性函数应用模式套件建议

将 4.9 系列的积性函数应用节点组合为一个小型模式组：

```
批注：隐式模式组（非正式 suite）
├─ 4.9.5 莫比乌斯反演应用  → 待 triage
├─ 4.9.6 欧拉函数应用      → create_new_draft_later ✅
└─ 4.9.x 可能新增的其他积性函数应用
```

**处理策略**：
- 每个节点生成**独立 pattern**（各自有独立的识别信号）
- 通过 `related_items` 相互引用建立关联
- 在 `boundary_note` 中说明与彼此的边界

---

## 更新后的 Backlog 状态

```
Batch1 Ready (83) ───────────────────────────── 已就绪
Batch2 Generated (13 + 1 merge) ─────────────── 已生成
Batch3 候选 (已 triage):
  ├─ Dominance Counting (3.13.182)     → create_new_draft_later ✅
  ├─ 欧拉函数应用 (4.9.6)              → create_new_draft_later ✅ (本 triage)
  ├─ 莫比乌斯反演应用 (4.9.5)           → 待 triage (from batch2)
  └─ 线段树 Split (3.13.190)           → defer ❌ (本 triage)
已 defer:
  ├─ Berlekamp-Massey
  ├─ Min_25 筛
  ├─ CDQ 分治 / MST 2D / Bitset
  └─ 线段树变体：Split (新增)
```

---

## 推荐结论

| 决策 | 结论 |
|:-----|:----:|
| 是否建议现在生成 patterns_batch3 | ❌ **否** |
| 是否建议先等 4.9.5 莫比乌斯反演应用 triage | ✅ **是** |
| 是否建议统一规划 batch3 内容后再生成 | ✅ **是** |
| 是否修改主图谱 | ❌ **否** |
| 是否修改已有 patterns | ❌ **否** |

---

**报告结束** | Triage 完成。2 个候选已处理：1 个推荐进入 batch3，1 个 defer。
