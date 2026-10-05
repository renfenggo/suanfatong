# Bellman-Ford resolved_pre 清理后只读复查报告

**生成时间**: 2026-05-26T14:30:00Z
**审计类型**: 只读复查，未修改任何文件

---

## 1. 清理是否成功

**是 ✅** — resolved_pre 中 250 条 `1.5.16` 残留已全部清理为 0。

### 清理前后对比

| 指标 | 清理前 | 清理后 | 本次复查 |
|:-----|:--:|:--:|:--:|
| item_count | 2640 | 2640 | **2640** ✅ |
| section_count | 65 | 65 | **65** ✅ |
| `1.5.16` 存在 | ❌ | ❌ | **❌** ✅ |
| `2.13.30` 存在 | ✅ | ✅ | **✅** ✅ |
| direct_pre `1.5.16` | 0 | 0 | **0** ✅ |
| rel `1.5.16` | 0 | 0 | **0** ✅ |
| resolved_pre `1.5.16` | **250** ⚠️ | **0** ✅ | **0** ✅ |

---

## 2. 是否仍有旧 ID 残留

**否** ✅ — 对全图 2640 个节点的 `direct_pre`、`resolved_pre`、`rel` 进行完整扫描，未发现任何 `1.5.16` 引用。

| 扫描字段 | 残留数量 |
|:---------|:------:|
| direct_pre → 1.5.16 | **0** ✅ |
| resolved_pre → 1.5.16 | **0** ✅ |
| rel → 1.5.16 | **0** ✅ |

---

## 3. 是否存在依赖异常

**否** ✅

| 检查项 | 结果 |
|:-------|:--:|
| dangling_refs | **0** |
| direct_pre_cycle | **null** |
| resolved_pre_mismatches | **0** |
| duplicate item_ids | **0** |
| validate-only passed | **true** ✅ |
| product_metadata_validation.passed | **true** ✅ |

---

## 4. 是否误改 direct_pre / rel

**否** ✅

| 字段 | 是否被修改 |
|:-----|:--------:|
| direct_pre | **否** (2.13.30 仍为 `['2.9.2', '2.13.2']`) ✅ |
| rel | **否** (2.13.30 仍为 `['2.13.2', '2.13.4', '2.13.6']`) ✅ |
| resolved_pre | **是** (仅此字段，250→0 清理) ✅ |
| name / section / parent | **否** |
| io_v4_4.json | **否** |
| 内容包 | **否** |
| 前端代码 | **否** |

---

## 5. 是否修改任何文件

**否** ✅ — 本任务为只读复查，未修改 `merged_knowledge_graph_item_dependencies_refined.json` 或任何其他文件。

---

## 6. 是否继续 Batch2

**否** ✅

---

## 7. 是否建议 1号 生成迁移后稳定检查点

**是** ✅ — 当前图谱状态稳定：
- item_count = 2640
- section_count = 65
- validate-only passed = true
- resolved_pre 无残留
- dangling_refs = []
- direct_pre_cycle = null
- resolved_pre_mismatches = []

建议 1号 在 `assets/data/knowledge_content/checkpoints/` 下生成 `bellman_ford_post_migrate_stable.checkpoint.json`。

---

## 8. 复查证据

### 2.13.30 当前状态
```
id:        2.13.30
name:      Bellman-Ford 算法
section:   2.13
parent:    2.13
direct_pre:['2.9.2', '2.13.2']
rel:       ['2.13.2', '2.13.4', '2.13.6']
```

### Section 1.5 当前状态
- 共 22 个节点：1.5.1 … 1.5.15, 1.5.17 … 1.5.23
- 1.5.16 已不存在 ✅
- ID 间隙仅影响视觉排序，不影响功能

### Section 2.13 当前状态
- 共 30 个节点：2.13.1 … 2.13.30
- 2.13.30 Bellman-Ford 已加入 ✅

---

## 9. 最终裁定

| 裁决项 | 结论 |
|:-------|:--:|
| cleanup 成功 | ✅ |
| 旧 ID 残留 | 0 |
| 依赖异常 | 无 |
| 是否修改任何文件 | **否** |
| 是否继续 Batch2 | **否** |
| 建议生成稳定检查点 | **是** |

---

*本报告由只读复查脚本自动生成，未修改任何文件*
