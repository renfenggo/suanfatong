# Stage3F Batch4 full_49 Duplicate Prune 模板

## 基本信息

- **批次**: Stage3F Batch4 full_49
- **当前状态**: Merge 已完成，item_count=1765, section_count=65, validate-only=passed
- **本模板用途**: 当 2号 Review 发现 merge_or_collapse_candidates 非空时执行
- **执行者**: 1号线程 / GLM5
- **执行条件**: 仅在 Fix Lite 的分支 B 场景下使用

---

## 一、前置条件

在执行 Duplicate Prune 前，必须满足以下条件：

| 检查项 | 期望值 | 说明 |
|--------|:------:|------|
| item_count | 1765 | Merge 完成后的状态 |
| section_count | 65 | |
| validate-only passed | true | |
| merge_or_collapse_candidates 非空 | | Review 发现的重复/折叠节点 |
| 这些节点均为 Batch4 新增节点 | | 只删除 Stage3F Batch4 新增的，不删旧节点 |

---

## 二、Duplicate Resolution 流程

### 2.1 读取 merge_or_collapse_candidates

从 `data/stage3f_batch4_full49_merge_or_collapse_candidates.json` 读取：

```json
{
  "candidates": [
    {
      "item_id": "...",
      "name": "...",
      "target_item_id": "...",
      "duplicate_reason": "...",
      "recommended_action": "remove"
    }
  ]
}
```

### 2.2 安全删除前检查

对每个候选节点，必须检查**全图谱入边依赖**：

1. **direct_pre 入边检查**：扫描全图谱 1765 个节点，统计 direct_pre 列表中是否包含候选节点 id。
2. **resolved_pre 入边检查**：扫描全图谱 resolved_pre 列表。
3. **rel 入边检查**：扫描全图谱 rel 列表。
4. 如果任一类入边非空 → **不安全，不能自动删除**。

### 2.3 四方案对比

对每个重复候选生成四方案：

| 方案 | 操作 | 适用条件 |
|:----:|------|---------|
| **方案 A** | 删除新增重复节点 | duplicate_level=exact, 无入边依赖 |
| **方案 B** | 保留新增节点，标记 review_priority=B | duplicate_level=medium, 有独立教育价值 |
| **方案 C** | 混合方案：精确重复删除，近似重复保留 | 有多个候选，水平和风险不同 |
| **方案 D** | 全部人工复查 | 依赖复杂或 duplicate_level=low |

### 2.4 删除执行步骤

```
1. 备份主图谱
   -> backups/stage3f_batch4_full49_duplicate_prune_backup.json

2. 从对应 section 的 items 列表中移除节点
   只删除节点对象，不修改其他任何内容

3. 更新 validation_baseline
   graph["meta"]["validation_baseline"] = {
     "item_count": 1765 - 删除数,
     "section_count": 65
   }

4. 写道图谱
5. 运行 validate-only
6. 验证 9 项全部通过
7. 输出结果文件
```

---

## 三、安全护栏

| 规则 | 说明 |
|:----|:-----|
| 只删除 Batch4 新增节点 | 不能删除旧节点 |
| 不重排 item id | 删除后剩余节点 id 不变 |
| 不修改 direct_pre / resolved_pre / rel | 任何其他字段都不能改 |
| 不修改旧节点 | 旧节点内容绝对不能动 |
| 不重排 section | section 数量和顺序不变 |
| 删除前必须检查入边 | 有入边依赖的不能自动删除 |
| validate-only 失败必须恢复 | 不得留下半成品 |

---

## 四、四方案报告模板

### 方案 A：删除确认重复节点

```
删除节点列表：
  - item_id: xxx (name: xxx)
    重复已有节点: xxx
    duplicate_level: exact/high/medium
    入边依赖: 无

删除后 item_count: 1765 → 17XX
```

### 方案 B：不删除，只标记 B

```
保留节点列表：
  - item_id: xxx (name: xxx)
    关联已有节点: xxx
    duplicate_level: medium/low
    保留原因: 有独立教育价值/不同抽象视角
    后续操作: 可人工添加 rel 关系
```

### 方案 C：混合方案

```
删除节点：
  - item_id: xxx (exact duplicate, 无入边)

保留节点：
  - item_id: xxx (medium duplicate, 保留 B)
```

### 方案 D：全部人工复查

```
原因：所有候选均有入边依赖或 duplicate_level 过低
```

---

## 五、成功标准

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 1765 - 删除数 |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |
