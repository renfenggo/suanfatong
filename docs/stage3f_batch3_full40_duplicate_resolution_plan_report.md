# Stage3F Batch3 full_40 Duplicate Resolution Plan Report

**生成时间**: 2026-05-25 18:35
**执行者**: 1号线程 / GLM5
**检查类型**: 重复处理方案分析（不修改主图谱）
**主图谱状态**: 未修改

---

## 一、前置状态确认

| 检查项 | 值 |
|--------|:----:|
| item_count | 1717 |
| section_count | 65 |
| validate-only passed | ✅ true |
| resolved_pre_mismatches | [] |
| dangling_refs | [] |
| direct_pre_cycle | null |
| product_metadata_validation.passed | true |
| report_matches_json | true |

---

## 二、merge_or_collapse_candidates 分析

### 候选 1：2.10.39 KMP算法详解

#### 基本信息

| 字段 | 值 |
|------|-----|
| item_id | 2.10.39 |
| 名称 | KMP算法详解 |
| Section | 2.10（字符串算法） |
| 所属批次 | Stage3F Batch3 新增 |
| 被怀疑重复对象 | 2.10.2（KMP） |
| Review 结论 | **needs_merge_or_collapse** ✅ |
| Review 建议优先级 | C |

#### 入边依赖检查

| 依赖类型 | 是否有依赖 | 依赖节点列表 |
|:--------:|:----------:|:-----------:|
| direct_pre 引用 | ❌ 无 | [] |
| resolved_pre 引用 | ❌ 无 | [] |
| rel 引用 | ❌ 无 | [] |
| **全图谱依赖** | **❌ 无** | **安全删除** |

#### 重复程度判断

| 维度 | 判断 |
|:----|:----:|
| 重复级别 | **exact（确切重复）** |
| 已有节点 | 2.10.2（KMP）已完整覆盖 KMP 基本概念 |
| 新增内容 | "详解"版本可能含 next 数组构造细节、多种变体 |
| 是否有独立教育价值 | 否，内容应合并到 2.10.2 的文档/notes 中 |
| 处理建议 | **delete_new_duplicate（删除新增重复节点）** |

---

### 候选 2：2.10.35 Border树结构

#### 基本信息

| 字段 | 值 |
|------|-----|
| item_id | 2.10.35 |
| 名称 | Border树结构 |
| Section | 2.10（字符串算法） |
| 所属批次 | Stage3F Batch3 新增 |
| 被怀疑重复对象 | 2.10.16（KMP的失配树） |
| Review 结论 | **approve(C)**, needs_merge_or_collapse=false ✅ |
| Review 建议优先级 | C |

#### 入边依赖检查

| 依赖类型 | 是否有依赖 | 依赖节点列表 |
|:--------:|:----------:|:-----------:|
| direct_pre 引用 | ❌ 无 | [] |
| resolved_pre 引用 | ❌ 无 | [] |
| rel 引用 | ❌ 无 | [] |
| **全图谱依赖** | **❌ 无** | **安全（但不应删除）** |

#### 重复程度判断

| 维度 | 判断 |
|:----|:----:|
| 重复级别 | **medium（高度相关但不同视角）** |
| 已有节点 | 2.10.16（KMP的失配树） |
| 差异 | Border树侧重字符串border的树形结构/周期边界；失配树侧重fail指针树形结构/失配转移 |
| 是否有独立教育价值 | **是**，不同抽象视角 |
| merge_or_collapse 建议 | "建议保留并标记rel关系, 不合并" |
| 处理建议 | **keep_and_add_rel_later（保留，后续添加 rel 关系）** |

---

## 三、核对清单

| # | 检查项 | 结果 |
|---|--------|:----:|
| 1 | 候选是否全部是 Stage3F Batch3 新增节点 | ✅ 是（2.10.39、2.10.35 均在 added_item_ids 中） |
| 2 | 是否有其他节点 direct_pre 引用它们 | ❌ 无 |
| 3 | 是否有其他节点 resolved_pre 引用它们 | ❌ 无 |
| 4 | 是否有其他节点 rel 引用它们 | ❌ 无 |
| 5 | 删除是否会造成 dangling_refs | ❌ 不会（2.10.39 无入边；2.10.35 无入边但不建议删除） |
| 6 | 如果删除 2.10.39，item_count 会变为 | 1716 |
| 7 | 是否应该先保留不删除 | 2.10.39 → 不保留，明确删除；2.10.35 → 保留 |

---

## 四、方案对比

### 方案 A：删除明确重复节点，再 Fix Lite

| 项目 | 值 |
|------|-----|
| 删除 | 2.10.39（KMP算法详解） |
| 保留 | 2.10.35（Border树结构） |
| 删除后 item_count | 1716 |
| 风险 | **低** — 2.10.39 无入边依赖，安全删除 |
| 优点 | 清除重复，图谱干净 |
| 缺点 | 2.10.35 的 rel 关系需后续添加 |

### 方案 B：不删除，全部标记 B/manual_review

| 项目 | 值 |
|------|-----|
| 删除 | 无 |
| 保留 | 2.10.39 + 2.10.35 |
| 风险 | **中** — 2.10.39 保留会造成 KMP 双节点冗余 |
| 优点 | 最简单，不动图谱 |
| 缺点 | Review 已明确标记 needs_merge_or_collapse，不处理浪费 Review 结果 |

### 方案 C（推荐）：只删除 KMP算法详解，Border树结构保留

| 项目 | 值 |
|------|-----|
| 删除 | 2.10.39（KMP算法详解） |
| 保留 | 2.10.35（Border树结构） |
| 删除后 item_count | 1716 |
| 风险 | **低** — 精确匹配 Review 结论 |
| 优点 | 完全匹配 Review 结论（2.10.39=needs_merge_or_collapse✅, 2.10.35=approve C✅） |
| 后续 | Fix Lite 只处理剩余 39 个新增节点 |

### 方案 D：全部人工复查

| 项目 | 值 |
|------|-----|
| 风险 | 低但低效率 |
| 适用场景 | 如果对 2.10.39 的删除有疑虑 |

---

## 五、推荐方案 C

**推荐方案 C：删除 KMP算法详解(2.10.39)，Border树结构(2.10.35)保留**

### 推荐理由

1. **完全匹配 Review 结论**
   - 2.10.39 在 Review 中标记为 `needs_merge_or_collapse=true`
   - 2.10.35 在 Review 中标记为 `approve(C)`, `needs_merge_or_collapse=false`
   - merge_or_collapse_candidates.json 也建议 Border树"保留并标记rel关系"

2. **安全删除 2.10.39**
   - 全图谱无任何节点 direct_pre/resolved_pre/rel 引用 2.10.39
   - 删除不会造成 dangling_refs
   - 删除后 item_count = 1716

3. **保留 2.10.35 的独立价值**
   - Border树和失配树是同一底层数据结构的不同抽象视角
   - Border树侧重border/周期边界，失配树侧重fail指针/失配转移
   - 有独立教育价值

### 执行步骤

```
1. 删除 2.10.39（KMP算法详解）从 2.10 section
2. 更新 meta.validation_baseline.item_count = 1716
3. 运行 validate-only 并验证
4. 输出 Duplicate Prune 文件
5. 然后执行 Fix Lite（只处理剩余 39 个节点）
6. Fix Lite 中不修改 2.10.35（保持 C）
7. 不继续 Batch4
```

---

## 六、Fix Lite 计划（方案 C 执行后）

| 项目 | 值 |
|:-----|:----:|
| 删除后 item_count | 1716 |
| 剩余新增节点数 | 39 |
| 排除节点 | 2.10.39（已删除） |
| validation_baseline | item_count=1716, section_count=65 |
| Fix Lite 范围 | 仅 review_status 降级 |
| 2.10.35 的 rel 关系 | 暂不处理，标记为后续任务 |
