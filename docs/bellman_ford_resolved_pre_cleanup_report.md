# Bellman-Ford resolved_pre 缓存残留清理报告

- **生成时间**：2026-05-26T13:52:57Z
- **任务**：清理 resolved_pre 中 `1.5.16` 的传递闭包缓存残留

---

## 1. 清理前状态

| 指标 | 值 |
|:-----|:--|
| resolved_pre 中 `1.5.16` 残留节点数 | **250** |
| direct_pre 中 `1.5.16` 引用数 | 0 |
| rel 中 `1.5.16` 引用数 | 0 |

> 根因：迁移脚本移走了 `1.5.16` → `2.13.30` 后，只更新了 `direct_pre` 和 `rel`，但没有重新展开全图的 `resolved_pre` 传递闭包。这 250 个节点原本在依赖链中引用了 `1.5.16`，迁移后 `resolved_pre` 未刷新。

## 2. 清理操作

- 遍历全部 2,640 个节点
- 对每个节点基于当前 `direct_pre` 重新展开传递闭包
- 更新 `resolved_pre` 字段
- 未修改任何其他字段

## 3. 清理后状态

| 指标 | 清理前 | 清理后 |
|:-----|:--:|:--:|
| item_count | 2,640 | **2,640** |
| section_count | 65 | **65** |
| `1.5.16` 是否存在 | ❌ | ❌ |
| `2.13.30` 是否存在 | ✅ | ✅ |
| direct_pre `1.5.16` | 0 | **0** |
| rel `1.5.16` | 0 | **0** |
| resolved_pre `1.5.16` | **250** | **0** ✅ |
| dangling_refs | — | **0** |
| direct_pre_cycle | — | **None** |
| resolved_pre_mismatches | — | **0** |
| resolved_pre 变化节点数 | — | **2018** |

## 4. 修改确认

| 检查项 | 结果 |
|:-------|:--:|
| 是否修改 direct_pre | **否** |
| 是否修改 rel | **否** |
| 是否修改 name | **否** |
| 是否修改 section | **否** |
| 是否新增/删除节点 | **否** |
| 是否修改 io_v4_4.json | **否** |
| 是否修改内容包 | **否** |
| 是否修改前端代码 | **否** |
| 是否继续 Batch2 | **否** |

## 5. 验证结果

| 验证项 | 结果 |
|:-------|:--:|
| item_count = 2640 | ✅ |
| section_count = 65 | ✅ |
| `1.5.16` 不存在 | ✅ |
| `2.13.30` 存在 | ✅ |
| direct_pre `1.5.16` = 0 | ✅ |
| rel `1.5.16` = 0 | ✅ |
| resolved_pre `1.5.16` = 0 | ✅ |
| dangling_refs = [] | ✅ |
| direct_pre_cycle = None | ✅ |
| resolved_pre_mismatches = [] | ✅ |
| duplicate_ids = False | ✅ |
| **passed** | **✅** |

## 6. 建议

- ✅ **建议生成 Bellman-Ford 迁移后稳定检查点**，确认全链路数据一致
- ❌ **不要继续 Batch2**：本任务仅清理 resolved_pre 缓存，不涉及任何扩展操作

## 7. 备份

```
backups/merged_knowledge_graph_item_dependencies_refined_before_bellman_resolved_pre_cleanup_20260526_215257.json
```

---

*清理报告生成于 2026-05-26T13:52:57Z*
