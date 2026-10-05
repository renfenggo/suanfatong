# 内容资产 Source of Truth（ADR-004 落地标注）

> 冻结于 M0（2026-10-05）。变更需走 ADR。

## 唯一权威文件

| 角色 | 文件 | 规则 |
|---|---|---|
| **Draft 源**（编辑/评审） | `merged_knowledge_graph_item_dependencies_refined.json`（仓库根） | 3240 节点，global schema（en_name/tracks/visibility/review_status…）。内容变更只发生在这里。 |
| **Publish 产物**（App 消费） | `assets/data/knowledge/io_v4_4.json` | legacy schema。由 publish mapper 从 Draft 源生成（M1 建立 `tools/publish/`），**禁止手改**。 |

## 规则

1. 业务代码只允许读 `assets/data/knowledge/io_v4_4.json`，不得引用其他图谱副本。
2. 任何图谱/内容分片的发布必须经过 validator（节点数守恒、ID 唯一、依赖引用存在、无环）。
3. `assets/data/knowledge_content/`（content_index + 33 分片）为 Draft 内容资产，M1 正式接入。
4. 历史副本与一次性管线脚本统一归档于 `tools/archive/`（只读留档，不参与构建）。
5. `data/` 目录为管线审计产物区，非 App 资产。

## 修复记录（M0）

- 发现 `.gitignore` 第 56 行裸名 `io_v4_4.json` 误伤 assets 下的 Publish 产物（从未入库）→ 已改为根锚定 `/io_v4_4.json` 并将 8.3MB 正式资产入库。
- `assets/data/knowledge/` 内 2 个 before_sync 历史备份（~15MB）移至 `tools/archive/`，安装包瘦身。
