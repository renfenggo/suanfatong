# -*- coding: utf-8 -*-
"""生成 item_part_index.json：item_id -> 分片文件名 的显式映射索引。

背景（ADR-004 / M1-4）：
- assets/data/knowledge_content/ 下 33 个分片覆盖全部 3240 个图谱节点，
  但分片顺序与 io_v4_4 图谱 App 侧展平顺序（categories 按 _categorySortOrder
  排序后 sections/items 顺序）完全不一致，无法用 start_index/end_index 区间
  推算 item_id 所在分片。
- 因此离线生成显式映射（item_part_index.json），App 运行时按需加载单个分片，
  不把 33 个分片一次性全解码到内存。

校验（不过则退出码 1，不产出索引）：
1. 分片 item_id 总数 == content_index.generated_item_count
2. item_id 无重复
3. 分片 id 集合与 io_v4_4 图谱展平 id 集合完全一致
"""
import json
import os
import sys

ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
)
CONTENT_DIR = os.path.join(ROOT, "assets", "data", "knowledge_content")
INDEX_PATH = os.path.join(CONTENT_DIR, "content_index.json")
GRAPH_PATH = os.path.join(ROOT, "assets", "data", "knowledge", "io_v4_4.json")
OUT_PATH = os.path.join(CONTENT_DIR, "item_part_index.json")

# 与 lib/models/knowledge_graph.dart 的 _categorySortOrder 保持一致
CATEGORY_SORT_ORDER = ["C++语法", "算法", "数据结构", "算法竞赛数学", "C++编程/调试技巧"]


def flatten_graph_ids(graph):
    order = {name: i for i, name in enumerate(CATEGORY_SORT_ORDER)}
    cats = sorted(
        graph["categories"],
        key=lambda c: order.get(c.get("name"), len(order)),
    )
    ids = []
    for cat in cats:
        for section in cat.get("sections", []):
            for item in section.get("items", []):
                ids.append(item.get("id"))
    return ids


def main():
    with open(INDEX_PATH, encoding="utf-8") as f:
        index = json.load(f)

    expected = index.get("generated_item_count")
    parts = index["parts"]
    item_to_part = {}
    total = 0
    for part in parts:
        path = os.path.join(ROOT, part["path"])
        with open(path, encoding="utf-8") as f:
            arr = json.load(f)
        if not isinstance(arr, list):
            print(f"[FAIL] 分片不是数组: {part['path']}")
            sys.exit(1)
        for entry in arr:
            item_id = entry.get("item_id")
            if not item_id:
                print(f"[FAIL] 分片 {part['filename']} 存在空 item_id")
                sys.exit(1)
            if item_id in item_to_part:
                print(f"[FAIL] item_id 重复: {item_id}")
                sys.exit(1)
            item_to_part[item_id] = part["filename"]
            total += 1

    if expected is not None and total != expected:
        print(f"[FAIL] 分片总数 {total} != 索引声明 {expected}")
        sys.exit(1)

    with open(GRAPH_PATH, encoding="utf-8") as f:
        graph = json.load(f)
    graph_ids = flatten_graph_ids(graph)

    if set(item_to_part) != set(graph_ids):
        missing = set(graph_ids) - set(item_to_part)
        extra = set(item_to_part) - set(graph_ids)
        print(f"[FAIL] id 集合不一致; 缺失 {len(missing)}: {sorted(missing)[:5]}; "
              f"多余 {len(extra)}: {sorted(extra)[:5]}")
        sys.exit(1)

    out = {
        "version": 1,
        "source_index": "assets/data/knowledge_content/content_index.json",
        "source_index_version": index.get("version", ""),
        "source_graph": "assets/data/knowledge/io_v4_4.json",
        "item_count": total,
        "part_count": len(parts),
        "items": item_to_part,
    }
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")

    print(f"[OK] item_count={total} part_count={len(parts)} -> {os.path.relpath(OUT_PATH, ROOT)}")


if __name__ == "__main__":
    main()
