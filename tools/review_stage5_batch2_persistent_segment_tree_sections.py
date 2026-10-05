"""Stage5 Batch2 可持久化线段树节点章节归属复核（只读）。

从审计报告中提取 7 个 status=check 的可持久化线段树相关节点，
逐个输出复核信息并判断是否应迁移到 3.13 高级数据结构扩展。

输出:
- data/stage5_batch2_persistent_segment_tree_section_review.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAIN_GRAPH = ROOT / "merged_knowledge_graph_item_dependencies_refined.json"
FRONTEND_GRAPH = ROOT / "assets" / "data" / "knowledge" / "io_v4_4.json"
CONTENT_INDEX = ROOT / "assets" / "data" / "knowledge_content" / "content_index.json"
AUDIT_JSON = ROOT / "data" / "stage5_batch2_category_stats_audit.json"

TARGET_IDS = [
    "2.1.95",
    "2.1.96",
    "2.1.97",
    "2.1.98",
    "2.1.99",
    "2.1.100",
    "2.1.101",
]

# 数据结构本体判断关键词
DS_BODY_KEYWORDS = [
    "节点语义",
    "合并操作",
    "分裂操作",
    "区间修改模型",
    "区间查询模型",
    "持久化版本关系",
    "动态空间复杂度",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_items(graph):
    for cat in graph.get("categories", []):
        for sec in cat.get("sections", []):
            sec_category = cat.get("name")
            for item in sec.get("items", []):
                yield sec_category, sec, item


def build_item_index(graph):
    idx = {}
    for cat_name, sec, item in iter_items(graph):
        idx[item["id"]] = {
            "item": item,
            "section": sec,
            "section_category": cat_name,
        }
    return idx


def main():
    audit = load_json(AUDIT_JSON)
    main_graph = load_json(MAIN_GRAPH)
    frontend_graph = load_json(FRONTEND_GRAPH)
    content_index = load_json(CONTENT_INDEX)

    main_idx = build_item_index(main_graph)
    frontend_idx = build_item_index(frontend_graph)

    # 内容覆盖集合
    covered_ids = set()
    for part in content_index.get("parts", []):
        part_path = ROOT / part["path"]
        if not part_path.exists():
            continue
        part_data = load_json(part_path)
        items = part_data.get("items") if isinstance(part_data, dict) else part_data
        if not isinstance(items, list):
            continue
        for it in items:
            if isinstance(it, dict) and "id" in it:
                covered_ids.add(it["id"])

    keyword_nodes = audit.get("keyword_data_structure_nodes", [])
    check_nodes = [n for n in keyword_nodes if n.get("status") == "check"]

    reviews = []
    for nid in TARGET_IDS:
        audit_node = next((n for n in check_nodes if n["id"] == nid), None)
        main_info = main_idx.get(nid)
        fe_info = frontend_idx.get(nid)

        if not main_info or not fe_info:
            reviews.append({
                "id": nid,
                "error": "node not found in main or frontend graph",
            })
            continue

        item = main_info["item"]
        sec = main_info["section"]
        title = item.get("name", "")
        is_ds_body = any(k in title for k in DS_BODY_KEYWORDS)
        item_category = item.get("category", "")
        should_migrate = (
            is_ds_body
            and item_category == "数据结构"
            and sec["id"] == "2.1"
        )
        reason = (
            "节点为可持久化线段树数据结构本体（结构/操作/复杂度），"
            "category=数据结构，同类主席树/李超线段树节点已位于 3.13，"
            "应从 2.1 基础算法思想迁移到 3.13 高级数据结构扩展。"
            if should_migrate
            else "保留原章节：节点非数据结构本体或属于算法应用。"
        )

        reviews.append({
            "id": nid,
            "title": title,
            "main_section_id": sec["id"],
            "main_section_name": sec.get("name", ""),
            "main_section_category": main_info["section_category"],
            "main_item_category": item_category,
            "main_item_subcategory": item.get("subcategory", ""),
            "frontend_section_id": fe_info["section"]["id"],
            "frontend_section_name": fe_info["section"].get("name", ""),
            "has_content": nid in covered_ids,
            "is_data_structure_body": is_ds_body,
            "recommended_section_id": "3.13" if should_migrate else sec["id"],
            "recommended_section_name": "高级数据结构扩展" if should_migrate else sec.get("name", ""),
            "decision": "migrate" if should_migrate else "keep",
            "reason": reason,
            "audit_expected_section": audit_node.get("expected_section") if audit_node else None,
            "audit_status": audit_node.get("status") if audit_node else None,
        })

    migrate_count = sum(1 for r in reviews if r.get("decision") == "migrate")
    keep_count = sum(1 for r in reviews if r.get("decision") == "keep")

    # Batch2 分类统计（基于当前图谱）
    batch2_source_path = ROOT / audit.get("batch2_id_source", "")
    batch2_ids = set()
    if batch2_source_path.exists():
        baseline = load_json(batch2_source_path)
        baseline_ids = {
            it["id"]
            for cat_name, sec, it in iter_items(baseline)
        }
        current_ids = set(main_idx.keys())
        batch2_ids = current_ids - baseline_ids

    # section 大类统计
    sec_major_stats = Counter()
    item_cat_stats = Counter()
    fe_sec_major_stats = Counter()
    for nid in batch2_ids:
        m = main_idx.get(nid)
        f = frontend_idx.get(nid)
        if m:
            prefix = m["section"]["id"].split(".")[0]
            if prefix == "2":
                sec_major_stats["算法"] += 1
            elif prefix == "3":
                sec_major_stats["数据结构"] += 1
            elif prefix == "4":
                sec_major_stats["数学"] += 1
            cat = m["item"].get("category")
            if cat:
                item_cat_stats[cat] += 1
        if f:
            prefix = f["section"]["id"].split(".")[0]
            if prefix == "2":
                fe_sec_major_stats["算法"] += 1
            elif prefix == "3":
                fe_sec_major_stats["数据结构"] += 1
            elif prefix == "4":
                fe_sec_major_stats["数学"] += 1

    output = {
        "review_time": "2026-06-16",
        "target_ids": TARGET_IDS,
        "total_reviewed": len(reviews),
        "migrate_count": migrate_count,
        "keep_count": keep_count,
        "reviews": reviews,
        "batch2_stats_before_fix": {
            "section_major_category": dict(sec_major_stats),
            "item_category": dict(item_cat_stats),
            "frontend_section_major_category": dict(fe_sec_major_stats),
            "batch2_id_count": len(batch2_ids),
        },
    }

    out_path = ROOT / "data" / "stage5_batch2_persistent_segment_tree_section_review.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"复核完成: 共 {len(reviews)} 个节点, 迁移 {migrate_count}, 保留 {keep_count}")
    print(f"报告已写入: {out_path}")


if __name__ == "__main__":
    main()
