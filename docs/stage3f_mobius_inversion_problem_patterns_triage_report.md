# 莫比乌斯反演应用 Problem Pattern Triage 报告

## 分级概况

| 指标 | 结果 |
|:----|:----:|
| **候选总数** | **1** |
| **create_new_draft_later** | **1**（莫比乌斯反演应用） |
| **merge_with_existing** | **0** |
| **defer** | **0** |
| **manual_review** | **0** |
| **是否生成正式 patterns** | ❌ **否** |
| **是否修改主图谱** | ❌ **否** |

---

## 候选：莫比乌斯反演应用（4.9.5）✅ create_new_draft_later

### 基础信息

| 属性 | 值 |
|:-----|:----|
| **Item ID** | 4.9.5 |
| **知识项类型** | `modeling_pattern` |
| **Review 结果** | `move_to_problem_patterns` |
| **所属 Section** | 4.9 狄利克雷卷积/莫比乌斯反演 |
| **直接前置** | 4.9.2（莫比乌斯反演） |
| **Level** | L4 |
| **tracks** | icpc, advanced_math, noi |
| **Review 优先级** | C |

### 知识图谱中的位置

```
4.9 高级数学
├── 4.9.1 二项式反演
├── 4.9.2 莫比乌斯反演 (理论基础)
├── 4.9.3 Min_25筛 (已 defer，algorithm_only)
├── 4.9.4 狄利克雷卷积基础
├── 4.9.5 莫比乌斯反演应用 (本候选) ★
├── 4.9.6 欧拉函数应用 (已 triage: create_new_draft_later)
└── 4.9.x ...
```

### 适配性评估

| 检查项 | 结果 | 说明 |
|:-------|:----:|:-----|
| 与 ready patterns 重复 | ❌ 无 | pat.inclusion_exclusion_counting 有数学关联但覆盖不同 |
| 与 batch2 patterns 重复 | ❌ 无 | 全部为图论/网络流，不相关 |
| 与 Dominance Counting suite 相关 | ❌ 无 | 不同领域（计数模式 vs 数论反演） |
| 属于 modeling_pattern | ✅ 是 | Review 已标记 item_type=modeling_pattern |
| 有明确识别信号 | ✅ 是 | 倍数/因子关系统计、gcd/lcm 条件、积性函数前缀和 |
| 有固定转化路径 | ✅ 是 | 莫比乌斯函数转换 + Dirichlet 卷积 + 数论分块/筛法 |
| 是否有多样化建模选择 | ✅ 是 | 线性筛 / 数论分块 / Dirichlet 前缀和 等多种实现路径 |
| 是否需要 boundary_note | ✅ 是 | 与 pat.inclusion_exclusion_counting、pat.euler_function_application |
| 是否需要人工复查 | ❌ 否 | AI 可直接决策 |

### 与 pat.inclusion_exclusion_counting 的边界

```
pat.inclusion_exclusion_counting（容斥计数）
├── 识别信号：至少/至多条件交叠、直接计数重复、集合数量小
├── 转化路径：按子集奇偶加减
└── 适用场景：集合交并计数、错排、子集容斥

pat.mobius_inversion_application（莫比乌斯反演应用） ← 本候选
├── 识别信号：倍数/因子关系统计、gcd/lcm 条件、积性函数转化
├── 转化路径：莫比乌斯函数 μ(n) 转换 + Dirichlet 卷积 + 数论分块
└── 适用场景：[gcd=i] 统计、互质对计数、积性函数前缀和

边界：容斥计数是通用组合数学工具，莫比乌斯反演是数论中的系统化容斥表达。
    两者在部分场景（如互质计数）可互相推导，但莫比乌斯反演有更高效的数学结构（Dirichlet 卷积）和竞赛专用优化（数论分块、线性筛预处理）。
```

### 与 4.9.6 欧拉函数应用的关系

| 维度 | 莫比乌斯反演应用 (4.9.5) | 欧拉函数应用 (4.9.6) |
|:----|:------------------------|:--------------------|
| 核心函数 | μ(n) 莫比乌斯函数 | φ(n) 欧拉函数 |
| 核心操作 | 因子倍数关系转换 | 互质关系计数、降幂 |
| 典型场景 | [gcd=i] 统计、互质对、积性函数求和 | 互质计数、a^b mod m 降幂、阶乘互质 |
| 共同范式 | 筛法预处理 + 公式推导 + 数论分块 | 筛法预处理 + 公式推导 + 数论分块 |

**结论**：各自独立成 pattern，通过 related_items 相互引用，在 batch3 中同批次处理。

---

## 数论模式套件建议

```
Number Theory / Multiplicative Function Application Pattern Suite
（隐式套件，通过 related_items + boundary_note 互联）

├─ pat.mobius_inversion_application（4.9.5）
│   ├── 倍数/因子关系统计
│   ├── gcd/lcm 条件计数
│   └── 容斥的数论函数表达
│
└─ pat.euler_function_application（4.9.6）
    ├── 互质计数
    ├── 欧拉降幂
    └── 阶乘互质部分提取
```

**处理策略**：
- 每个节点生成**独立 pattern**（各自的识别信号和转化路径独立）
- 通过 `related_items` 相互引用
- 在 `boundary_note` 中说明与彼此的边界

---

## Batch3 候选池现已完整

经过 Batch1/Batch2/Batch3 三个 triage 轮次，所有候选已处理完毕：

| # | 候选 | 来源 Batch | Triage 决策 | 优先级 |
|:-:|:----|:---------:|:-----------:|:------:|
| 1 | Dominance Counting (3.13.182) | Batch1 | create_new_draft_later | P1 |
| 2 | 莫比乌斯反演应用 (4.9.5) | Batch2 | create_new_draft_later | P1 |
| 3 | 欧拉函数应用 (4.9.6) | Batch3 | create_new_draft_later | P1 |

**已 defer（6 个）**：
Berlekamp-Massey, Min_25 筛, CDQ 分治, MST 2D Dominance, Bitset Rect Query, 线段树 Split

---

## 推荐结论

| 决策 | 结论 |
|:-----|:----:|
| 是否建议现在生成 patterns_batch3 | ❌ **否** |
| 是否建议等用户指令 | ✅ **是** |
| 是否建议与欧拉函数应用组成数论套件 | ✅ **是**（隐式套件） |
| 是否修改主图谱 | ❌ **否** |
| 是否修改已有 patterns | ❌ **否** |

**下一步行动**：
1. ✅ Batch3 所有候选 triage 已完成
2. ⏳ 等待用户发出"生成 patterns_batch3.json"指令
3. ⏳ 按顺序生成：Dominance Counting → 欧拉函数应用 → 莫比乌斯反演应用

---

**报告结束** | 莫比乌斯反演应用 triage 完成。结论：create_new_draft_later，P1，与欧拉函数应用组成数论模式套件。
