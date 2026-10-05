# Stage5-HardKnowledge Batch1 full500 Fix Lite 报告

- 执行时间: 2026-05-26T16:16:10

## 修复前状态

- item_count = **2640**
- section_count = 65

## Fix Lite 应用

- 处理节点数量: **475**
- 优先级分布: A=0 / B=7 / C=468

## 依赖字段修改检查

| 字段 | 是否修改 |
|:-----|:-------:|
| direct_pre | **否** (0) |
| resolved_pre | **否** (0) |
| rel | **否** (0) |

## 旧节点修改检查

| 检查项 | 结果 |
|:-------|:---:|
| 旧 2165 节点被修改 | **否** (0) |
| io_v4_4.json 被修改 | **否** |

## Validate-only 结果

| 检查项 | 结果 |
|:-------|:--:|
| item_count = 2640 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ (0) |
| direct_pre_cycle = null | ✅ |
| section refs = 0 | ✅ (0) |
| duplicates = 0 | ✅ (0) |
| product_metadata OK | ✅ |
| dep_fields_modified = 0 | ✅ |
| old_nodes_modified = 0 | ✅ |
| **passed = true** | **✅** |

## 建议

**建议生成 Stage5-HardKnowledge Batch1 full500 Stable Checkpoint。**
Fix Lite 验证全部通过。所有 475 个剩余 Stage5 Batch1 节点已标记优先级。
数据已准备就绪，可生成 Stable Checkpoint 进入下一阶段。

## 是否继续 Batch2

**否**

## 备份文件

`backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch1_full500_fix_lite.json`

---
*报告自动生成于 2026-05-26T16:16:10*