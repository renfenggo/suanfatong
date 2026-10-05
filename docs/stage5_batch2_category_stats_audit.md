# Stage5 Batch2 Category Stats Audit

- 审计时间: `2026-06-16T10:23:00+08:00`

## 输入文件

| 类型 | 路径 |
| --- | --- |
| main_graph | merged_knowledge_graph_item_dependencies_refined.json |
| frontend_graph | assets\data\knowledge\io_v4_4.json |
| content_index | assets\data\knowledge_content\content_index.json |

## 自动探测 Schema

### 主图谱

```json
{
  "items_path": "$.categories[*].sections[*].items",
  "sections_path": "$.categories[*].sections",
  "category_container_path": "$.categories",
  "section_count_detected": 65,
  "item_count_detected": 3240,
  "item_id_field": "id",
  "item_title_field": "name",
  "section_id_field": "id",
  "section_title_field": "name",
  "item_section_field": "parent",
  "item_category_fields": [
    "category"
  ],
  "section_category_source": "_detected_category_name from parent category container"
}
```

### 前端图谱

```json
{
  "items_path": "$.categories[*].sections[*].items",
  "sections_path": "$.categories[*].sections",
  "category_container_path": "$.categories",
  "section_count_detected": 65,
  "item_count_detected": 3240,
  "item_id_field": "id",
  "item_title_field": "name",
  "section_id_field": "id",
  "section_title_field": "name",
  "item_section_field": "parent",
  "item_category_fields": [],
  "section_category_source": "_detected_category_name from parent category container"
}
```

## Batch2 ID 来源

| 字段 | 值 |
| --- | --- |
| batch2_id_source | backups\merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch2_full600_20260526_223555.json |
| batch2_id_status | derived_current_minus_baseline; mapping_source_hit_count=573/600 |
| batch2_id_count | 600 |

## 一致性检查

| 检查项 | 结果 |
| --- | --- |
| main_item_count | 3240 |
| frontend_item_count | 3240 |
| content_index_source_item_count | 3240 |
| content_index_generated_item_count | 3240 |
| content_package_count | 33 |
| content_loaded_item_count | 3240 |
| main_frontend_same_ids | True |
| content_missing_main_count | 0 |
| batch2_content_covered_count | 600 |
| batch2_content_missing_count | 0 |

## 分类统计对比

### stats_by_section_major_category

| 分类 | 数量 |
| --- | --- |
| 数学 | 167 |
| 数据结构 | 110 |
| 算法 | 323 |

### stats_by_section_major_category_inferred_from_prefix

| 分类 | 数量 |
| --- | --- |
| 数学 | 167 |
| 数据结构 | 110 |
| 算法 | 323 |

### stats_by_item_category_field

```json
{
  "category": {
    "数据结构": 145,
    "数学": 200,
    "算法": 255
  }
}
```

### stats_by_frontend_category_field

```json
{
  "<no category/domain/type field detected>": {
    "未标注": 600
  }
}
```

### stats_by_merge_report

```json
{
  "markdown": {
    "数学": 200,
    "数据结构": 145,
    "算法": 255
  },
  "json": {
    "path": "data\\stage5_hard_knowledge_batch2_full600_added_items_summary.json",
    "category_distribution": {
      "算法": 255,
      "数据结构": 145,
      "数学": 200
    },
    "section_distribution": {
      "2.7": 23,
      "2.20": 120,
      "2.6": 30,
      "2.4": 7,
      "3.13": 76,
      "4.1": 100,
      "4.3": 64,
      "2.17": 33,
      "2.9": 4,
      "2.8": 78,
      "4.7": 3,
      "2.1": 62
    }
  }
}
```

### stats_by_checkpoint_report

```json
{
  "markdown": {
    "算法": 433,
    "数据结构": 0,
    "数学": 167
  },
  "json_full_chain": {
    "path": "data\\stage5_hard_knowledge_batch2_full_chain_stable_checkpoint.json",
    "batch2_summary": {
      "new_nodes": 600,
      "new_content": 600,
      "content_part_total": 33,
      "old_parts": 27,
      "batch2_new_parts": 6,
      "category_distribution": {
        "algorithm": 433,
        "data_structure": 0,
        "math": 167
      },
      "source_tier_distribution": {
        "ready_core": 339,
        "reserve_useful": 261
      },
      "fix_lite_distribution": {
        "A": 0,
        "B": 369,
        "C": 231
      }
    },
    "section_relocation_summary": {
      "2.1": {
        "before": 142,
        "after": 115
      },
      "3.13": {
        "before": 353,
        "after": 367
      },
      "3.7": {
        "before": 39,
        "after": 52
      },
      "relocated_nodes": 27
    }
  },
  "json_stable": {
    "path": "data\\stage5_hard_knowledge_batch2_full600_stable_checkpoint.json",
    "batch2_distribution": {
      "category": {
        "算法": 255,
        "数据结构": 145,
        "数学": 200
      },
      "source": {
        "ready_core": 339,
        "reserve_useful": 261
      },
      "subcategory": {
        "搜索进阶": 23,
        "构造题硬知识": 94,
        "贪心模型": 30,
        "根号算法": 7,
        "并查集扩展": 29,
        "数据结构嵌套": 43,
        "单调结构": 4,
        "数论进阶": 98,
        "组合计数进阶": 40,
        "多项式与生成函数": 24,
        "线性代数进阶": 33,
        "图论建模": 4,
        "交互题硬知识": 26,
        "DP优化": 78,
        "数论深水区": 2,
        "计算几何进阶": 3,
        "线段树进阶": 62
      },
      "direct_pre": {
        "4": 123,
        "3": 292,
        "5": 24,
        "2": 157,
        "6": 4
      },
      "section": {
        "2.7": 23,
        "2.20": 120,
        "2.6": 30,
        "2.4": 7,
        "3.13": 76,
        "4.1": 100,
        "4.3": 64,
        "2.17": 33,
        "2.9": 4,
        "2.8": 78,
        "4.7": 3,
        "2.1": 62
      }
    }
  },
  "existing_audit": {
    "path": "data\\stage5_hard_batch2_category_distribution_audit.json",
    "original_merge_report_distribution": {
      "算法": 255,
      "数据结构": 145,
      "数学": 200,
      "total": 600
    },
    "checkpoint_report_distribution": {
      "algorithm": 433,
      "data_structure": 0,
      "math": 167,
      "total": 600
    },
    "corrected_distribution": {
      "by_candidate_category": {
        "算法": 255,
        "数据结构": 145,
        "数学": 200
      },
      "by_item_category_field": {
        "算法": 255,
        "数据结构": 145,
        "数学": 200
      },
      "by_graph_section_parent": {
        "算法": 330,
        "数据结构": 103,
        "算法竞赛数学": 167
      },
      "by_corrected_section_prefix": {
        "算法": 330,
        "数据结构": 103,
        "数学": 167
      }
    },
    "root_cause": {
      "file": "_gen_full_chain_checkpoint.py",
      "line": 89,
      "buggy_code": "if sec_prefix in (\"2\", \"3\"): algo_count += 1",
      "explanation": "Section 3.x = 数据结构, but script treats both 2.x and 3.x as algorithm. ds_count is never incremented.",
      "fix": "if sec_prefix == \"2\": algo_count += 1\\nelif sec_prefix == \"3\": ds_count += 1"
    }
  }
}
```

## 重点数据结构关键词节点核查

状态汇总:

| 分类 | 数量 |
| --- | --- |
| ok | 28 |

| id | title | main_section_id | main_section_name | main_category_fields | frontend_section_id | frontend_category_fields | has_content | expected_section | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.100 | 可持久化线段树的持久化版本关系 (可持久化线段树 Persistent Version Relation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.101 | 可持久化线段树的动态空间复杂度 (可持久化线段树 Dynamic Space Complexity) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.95 | 可持久化线段树的节点语义 (可持久化线段树 Node Semantics) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.96 | 可持久化线段树的合并操作 (可持久化线段树 Merge Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.97 | 可持久化线段树的分裂操作 (可持久化线段树 Split Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.98 | 可持久化线段树的区间修改模型 (可持久化线段树 Range Update Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 2.1.99 | 可持久化线段树的区间查询模型 (可持久化线段树 Range Query Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.386 | 主席树的节点语义 (主席树 Node Semantics) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.387 | 主席树的合并操作 (主席树 Merge Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.388 | 主席树的分裂操作 (主席树 Split Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.389 | 主席树的区间修改模型 (主席树 Range Update Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.390 | 主席树的区间查询模型 (主席树 Range Query Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.391 | 主席树的持久化版本关系 (主席树 Persistent Version Relation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.392 | 主席树的动态空间复杂度 (主席树 Dynamic Space Complexity) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.393 | 李超线段树的节点语义 (李超线段树 Node Semantics) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.394 | 李超线段树的合并操作 (李超线段树 Merge Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.395 | 李超线段树的分裂操作 (李超线段树 Split Operation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.396 | 李超线段树的区间修改模型 (李超线段树 Range Update Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.397 | 李超线段树的区间查询模型 (李超线段树 Range Query Model) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.398 | 李超线段树的持久化版本关系 (李超线段树 Persistent Version Relation) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.13.399 | 李超线段树的动态空间复杂度 (李超线段树 Dynamic Space Complexity) | 3.13 | 高级数据结构扩展 | {"category": "数据结构"} | 3.13 | {} | True | 3.13 | ok |
| 3.7.46 | 动态开点线段树的节点语义 (动态开点线段树 Node Semantics) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.47 | 动态开点线段树的合并操作 (动态开点线段树 Merge Operation) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.48 | 动态开点线段树的分裂操作 (动态开点线段树 Split Operation) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.49 | 动态开点线段树的区间修改模型 (动态开点线段树 Range Update Model) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.50 | 动态开点线段树的区间查询模型 (动态开点线段树 Range Query Model) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.51 | 动态开点线段树的持久化版本关系 (动态开点线段树 Persistent Version Relation) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |
| 3.7.52 | 动态开点线段树的动态空间复杂度 (动态开点线段树 Dynamic Space Complexity) | 3.7 | 区间维护结构 | {"category": "数据结构"} | 3.7 | {} | True | 3.7 | ok |

## 推断逻辑

- Prefer section metadata category from the parent categories container.
- If section metadata has no category, infer by section id prefix: 2.x=算法, 3.x=数据结构, 4.x=数学, 1.x=C++语法, 5.x=C++编程/调试技巧.
- If prefix is unknown, use section title keywords as a fallback.

## 异常原因

- 结论类型: `A`
- 主图谱和前端图谱分类基本正确，是 checkpoint 报告统计口径错误。
- 从当前数据复算看，Batch2 的 section 大类中存在数据结构节点；checkpoint 报告的 `数据结构 0` 与当前图谱不一致。
- 重点关键词核查中仍有 `check` 项时，表示这些节点的当前 section 与本次审计预期不一致，需要人工复核后再继续扩批。

## 后续建议

- 不需要修改主图谱、前端图谱或内容索引来解决该统计冲突。
- 后续如要消除报告冲突，应单独修正 checkpoint 报告生成脚本的分类统计口径，并重新生成 checkpoint 报告。
- 是否建议进入 Batch3: 是。
