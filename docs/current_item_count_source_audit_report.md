# 当前知识点数量来源核查报告

## 结论

当前最新基线应为 **2165**，不是 1765。

如果之前读到 1765，来源是旧阶段结果或 Stage3G 合并前历史记录：Stage3G full400 的流程是 **1765 → 2165**，其中 1765 表示合并前数量，不表示当前图谱数量。

后续扩充应使用 **2165 个知识点** 作为基线。

## 文件核查结果

| 文件 | 当前/生成数量 | 1765 是否出现 | 判断 |
|---|---:|---|---|
| `merged_knowledge_graph_item_dependencies_refined.json` | item_count=2165，section_count=65 | 否 | 当前主图谱，应作为权威来源之一 |
| `assets/data/knowledge/io_v4_4.json` | item_count=2165，section_count=65 | 否 | 当前前端图谱，已同步到 2165 |
| `data/stage3g_full400_stable_checkpoint.json` | state_item_count=2165，state_section_count=65 | 是，`item_count_before=1765` | 1765 是 Stage3G 合并前历史值，合并后为 2165 |
| `docs/stage3g_full400_stable_checkpoint_report.md` | 当前 item_count=2165，当前 section_count=65 | 是，报告记录 `1765 → 2165` | 1765 是历史过程说明 |
| `data/io_v4_4_export_sync_audit.json` | main_graph_item_count=2165，io_v4_4_item_count=2165 | 否 | 同步审计确认主图谱和前端图谱一致 |
| `docs/io_v4_4_export_sync_report.md` | 主图谱 2165，io_v4_4.json 2165 | 否；另有旧前端 1349 的同步前记录 | 同步报告确认已同步到 2165 |
| `assets/data/knowledge_content/reports/content_validation_result.json` | source_item_count=2165，generated_item_count=2165 | 否 | Stage4 内容包覆盖 2165 |
| `assets/data/knowledge_content/content_index.json` | source_item_count=2165，generated_item_count=2165 | 否 | 内容索引以 2165 为源基线 |

## 哪些文件显示 2165

1. `merged_knowledge_graph_item_dependencies_refined.json`
2. `assets/data/knowledge/io_v4_4.json`
3. `data/stage3g_full400_stable_checkpoint.json`
4. `docs/stage3g_full400_stable_checkpoint_report.md`
5. `data/io_v4_4_export_sync_audit.json`
6. `docs/io_v4_4_export_sync_report.md`
7. `assets/data/knowledge_content/reports/content_validation_result.json`
8. `assets/data/knowledge_content/content_index.json`

## 哪些文件显示 1765

只有 Stage3G 历史记录显示 1765：

1. `data/stage3g_full400_stable_checkpoint.json`
   - 字段：`pipeline_history.stage3g_full400_merge.item_count_before`
   - 含义：Stage3G full400 合并前的旧数量。

2. `docs/stage3g_full400_stable_checkpoint_report.md`
   - 文本：合并前 `1765`、合并结果 `1765 → 2165`
   - 含义：阶段演进记录，不是当前数量。

## 应以哪个文件为准

当前数量应以这些文件共同确认为准：

1. `merged_knowledge_graph_item_dependencies_refined.json`
2. `assets/data/knowledge/io_v4_4.json`
3. `data/io_v4_4_export_sync_audit.json`
4. `assets/data/knowledge_content/reports/content_validation_result.json`
5. `assets/data/knowledge_content/content_index.json`

它们共同指向：当前主图谱、前端图谱和 Stage4 内容包基线均为 **2165**。

## 最终判断

当前应使用 **2165** 作为后续扩充基线。

1765 不是当前状态；它只代表 Stage3G full400 合并前的旧状态。如果之前读到 1765，说明读取的是旧文件、旧检查点字段，或报告中的历史阶段结果。
