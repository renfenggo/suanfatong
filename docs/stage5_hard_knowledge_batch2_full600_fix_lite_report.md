# Stage5-HardKnowledge Batch2 full600 Post-Relocation Fix Lite 报告

- **生成时间**：2026-05-27T04:47:35Z
- **任务**：对 600 个 Batch2 新增节点应用 Fix Lite 补丁（仅更新轻量 review 字段）

---

## 1. 执行前检查

| 检查项 | 结果 |
|:-------|:--:|
| item_count = 3,240 | ✅ |
| section_count = 65 | ✅ |
| readiness recommendation | ✅ |
| patch 数量 = 600 | ✅ |
| 所有 patch item_id 存在于图谱 | ✅ |
| 所有 patch 均为 Batch2 新增节点 | ✅ |
| 不包含旧 2640 节点 | ✅ |
| 所有节点当前为 pending_review | ✅ |

---

## 2. Fix Lite 摘要

| 指标 | 值 |
|:-----|:--:|
| Fix Lite 前 item_count | **3,240** |
| Fix Lite 后 item_count | **3240** |
| 处理节点 | **600** |
| Priority A | **0** |
| Priority B | **369** |
| Priority C | **231** |

### 处理说明

- **C（231 个）**: 无风险节点，标记为 reviewed，可进入下一阶段
- **B（369 个）**: 模板后缀/低质量 reserve 节点，标记为 reviewed 但保留 B 优先级需后续观察
- **A（0 个）**: 无

---

## 3. 修改范围

| 是否修改 | 答案 |
|:---------|:--:|
| direct_pre | **否** |
| resolved_pre | **否** |
| rel | **否** |
| name | **否** |
| 旧 2640 节点 | **否** |
| io_v4_4.json | **否** |
| 内容包 | **否** |
| 前端代码 | **否** |

### 实际修改的字段

仅修改以下字段（仅对 600 个 Batch2 新增节点）：

- `review_status`: pending_review → reviewed
- `review_priority`: 无 → B/C

---

## 4. 验证结果

| 验证项 | 结果 |
|:-------|:--:|
| item_count = 3,240 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| duplicate_ids = 0 | ✅ |
| patch review 字段正确 | ✅ |
| 旧 2640 review 字段未变 | ✅ |
| product_metadata_ok | ✅ |
| **passed** | **✅** |

---

## 5. 备份

```
backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch2_full600_fix_lite_20260527_124735.json
```

---

## 6. 建议

- ✅ **建议生成 Stage5-HardKnowledge Batch2 Stable Checkpoint**
- ❌ 不要继续 Batch3
