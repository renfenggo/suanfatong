# Bellman-Ford 迁移专项只读审计报告

**生成时间**: 2026-05-26T13:38:48.267704+00:00

## 一、审计结论

**结论: 迁移成功 ✅**

## 二、主图谱一致性

| 检查项 | 结果 |
|--------|------|
| item_count = 2640 | ✅ |
| section_count = 65 | ✅ |
| 1.5.16 不存在 | ✅ |
| 2.13.30 存在 | ✅ |
| 2.13.30 名称含 Bellman-Ford | ✅ |
| 2.13.30 parent = 2.13 | ✅ |
| 2.13.30 section = 2.13 | ✅ |
| direct_pre 无 1.5.16 引用 | ✅ |
| rel 无 1.5.16 引用 | ✅ |
| 无重复 item_id | ✅ |
| resolved_pre 含 1.5.16 | 250 个节点 ⚠️ |

> **注**: resolved_pre 为传递闭包缓存字段，250 个节点仍引用 1.5.16。需重新运行依赖展开脚本清理，不阻塞功能。

## 三、前端图谱一致性 (io_v4_4.json)

| 检查项 | 结果 |
|--------|------|
| io_v4_4 item_count = 2640 | ✅ |
| io_v4_4 无 1.5.16 | ✅ |
| io_v4_4 有 2.13.30 | ✅ |
| 2.13.30 字段完整 | ✅ |
| direct_pre 无 section ref | ✅ |
| direct_pre 无 dangling ref | ✅ |

## 四、内容覆盖一致性

| 检查项 | 结果 |
|--------|------|
| Section 1.5 学习单元 = 22/22 | ✅ |
| Section 1.5 不含 Bellman-Ford | ✅ |
| Section 2.13 含 2.13.30 | ✅ |
| content items 含 2.13.30 | ✅ |
| content items 不含 1.5.16 | ✅ |
| content_index 覆盖 batch2_part6 | ✅ |
| 无孤儿内容 | ✅ |
| 无缺失内容 | ✅ |

## 五、前端页面风险

| 风险项 | 状态 | 说明 |
|--------|------|------|
| Section 1.5 排序跳号 | ⚠️ 低风险 | ID 1.5.15→1.5.17 存在间隙，前端排序可能产生空占位 |
| Section 2.13 显示 2.13.30 | ✅ | 2.13.30 已加入 Section 2.13，正常显示 |
| 搜索 Bellman-Ford | ✅ | io_v4_4 2.13.30 name='Bellman-Ford 算法'，搜索命中 |
| Dijkstra/Floyd/SPFA 关联 | ✅ | rel=['2.13.2','2.13.4','2.13.6'] 双向可达 |
| BFS/Dijkstra 前置 | ✅ | direct_pre=['2.9.2','2.13.2'] 可跳转 |

## 六、归档与历史文件

| 检查项 | 结果 |
|--------|------|
| 迁移备份 5 个文件 | ✅ |
| checkpoint 残留 1.5.16 | ⚠️ 历史记录 |

### 备份文件清单

- ✅ `backups/merged_knowledge_graph_item_dependencies_refined_before_bellman_migrate_20260526_204014.json`
- ✅ `backups/io_v4_4_before_bellman_migrate_20260526_204014.json`
- ✅ `backups/section_1_5_units_before_bellman_migrate_20260526_204014.json`
- ✅ `backups/section_2_13_units_before_bellman_migrate_20260526_204014.json`
- ✅ `backups/stage4_batch2_part_006_before_bellman_migrate_20260526_204014.json`

## 七、最终裁定

| 裁决 | 结论 |
|------|------|
| 迁移是否成功 | ✅ 是 |
| 旧 ID 残留 (direct_pre/rel) | 0 条 ✅ |
| 内容孤儿 | 无 ✅ |
| 前端图谱不一致 | 无 ✅ |
| 章节页面风险 | 低（仅 ID 跳号）⚠️ |
| 是否建议新检查点 | 是 ✅ |
| 是否修改任何文件 | 否 ✅ |
| 是否继续 Batch2 | 否 ✅ |

## 八、注意事项

1. **resolved_pre 残留**: 250 个节点仍缓存 1.5.16 在传递闭包中。建议 1号 重新运行 `refine_item_dependencies.py` 生成新的 resolved_pre。此为轻度残留，不影响图谱正确性和前端展示。
2. **checkpoint 残留**: `stage4_batch2_part_006.checkpoint.json` 为历史审计文件，保留原始生成时的 item_id 列表。1.5.16 出现在该文件中属正常，不构成功能性问题。
3. **Section 1.5 ID 间隙**: 1.5.16 被移除后，产生 1.5.15→1.5.17 间隙。前端排序通常按自然序显示，间隙不影响功能。如需消除间隙，可重新编号但非本次任务范围。

---
*本报告由 Bellman-Ford Migration Audit 自动生成，未修改任何文件*
