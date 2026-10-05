"""Stage5 Batch2 可持久化线段树节点章节最小修正。

将 7 个可持久化线段树相关节点从 section 2.1 迁移到 3.13：
- 主图谱: merged_knowledge_graph_item_dependencies_refined.json
- 前端图谱: assets/data/knowledge/io_v4_4.json
- 内容索引: 仅当保存了 section 元信息时才同步

只修改:
- item.parent: 2.1 -> 3.13
- item 在 categories[].sections[].items 中的物理位置（从 2.1 移到 3.13）

不修改:
- id, name, direct_pre, rel, resolved_pre, content path, content 正文
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

FROM_SECTION_ID = "2.1"
TO_SECTION_ID = "3.13"
TO_SECTION_NAME = "高级数据结构扩展"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_section(graph, section_id: str):
    for cat in graph.get("categories", []):
        for sec in cat.get("sections", []):
            if sec.get("id") == section_id:
                return cat, sec
    return None, None


def collect_items_map(graph):
    """id -> (cat_idx, sec_idx, item_idx)"""
    idx = {}
    for ci, cat in enumerate(graph.get("categories", [])):
        for si, sec in enumerate(cat.get("sections", [])):
            for ii, item in enumerate(sec.get("items", [])):
                idx[item["id"]] = (ci, si, ii)
    return idx


def migrate_items(graph, target_ids):
    """把 target_ids 从 2.1 移到 3.13，并更新 parent 字段。"""
    moved = []
    # 找到源 section 和目标 section
    _, src_sec = find_section(graph, FROM_SECTION_ID)
    _, dst_sec = find_section(graph, TO_SECTION_ID)
    if src_sec is None:
        raise RuntimeError(f"source section {FROM_SECTION_ID} not found")
    if dst_sec is None:
        raise RuntimeError(f"target section {TO_SECTION_ID} not found")

    # 从源 section 中取出目标 items（保持原顺序）
    remaining = []
    taken = []
    for item in src_sec.get("items", []):
        if item["id"] in target_ids:
            taken.append(item)
        else:
            remaining.append(item)
    src_sec["items"] = remaining

    # 按 TARGET_IDS 顺序追加到目标 section 末尾
    taken_map = {it["id"]: it for it in taken}
    for nid in target_ids:
        it = taken_map.get(nid)
        if it is None:
            raise RuntimeError(f"target item {nid} not found in source section")
        old_parent = it.get("parent")
        it["parent"] = TO_SECTION_ID
        dst_sec["items"].append(it)
        moved.append({
            "id": it["id"],
            "name": it.get("name", ""),
            "old_section_id": FROM_SECTION_ID,
            "old_section_name": src_sec.get("name", ""),
            "new_section_id": TO_SECTION_ID,
            "new_section_name": TO_SECTION_NAME,
            "old_parent": old_parent,
            "new_parent": TO_SECTION_ID,
        })

    return moved


def verify_graph(graph, label: str):
    """基本计数与目标节点位置校验。"""
    total = 0
    target_section = {}
    for cat in graph.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                total += 1
                if item["id"] in TARGET_IDS:
                    target_section[item["id"]] = sec["id"]
    print(f"[{label}] item_count={total}")
    for nid in TARGET_IDS:
        loc = target_section.get(nid, "MISSING")
        ok = loc == TO_SECTION_ID
        print(f"  {nid}: section={loc} {'OK' if ok else 'FAIL'}")
    return total, target_section


def build_id_set(graph):
    ids = set()
    for cat in graph.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                ids.add(item["id"])
    return ids


def compute_batch2_stats(graph, batch2_ids):
    sec_major = Counter()
    item_cat = Counter()
    for cat in graph.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                if item["id"] not in batch2_ids:
                    continue
                prefix = sec["id"].split(".")[0]
                if prefix == "2":
                    sec_major["算法"] += 1
                elif prefix == "3":
                    sec_major["数据结构"] += 1
                elif prefix == "4":
                    sec_major["数学"] += 1
                c = item.get("category")
                if c:
                    item_cat[c] += 1
    return dict(sec_major), dict(item_cat)


def main():
    audit = load_json(AUDIT_JSON)
    batch2_source_path = ROOT / audit.get("batch2_id_source", "")
    batch2_ids = set()
    if batch2_source_path.exists():
        baseline = load_json(batch2_source_path)
        baseline_ids = set()
        for cat in baseline.get("categories", []):
            for sec in cat.get("sections", []):
                for item in sec.get("items", []):
                    baseline_ids.add(item["id"])
        # 读取当前主图谱用于差集
        main_graph_pre = load_json(MAIN_GRAPH)
        current_ids = build_id_set(main_graph_pre)
        batch2_ids = current_ids - baseline_ids

    # 修正前统计
    sec_before, cat_before = compute_batch2_stats(main_graph_pre, batch2_ids)

    # 修正主图谱
    moved_main = migrate_items(main_graph_pre, set(TARGET_IDS))
    save_json(MAIN_GRAPH, main_graph_pre)
    print(f"主图谱已修正，迁移 {len(moved_main)} 个节点")

    # 修正前端图谱
    frontend_graph = load_json(FRONTEND_GRAPH)
    moved_fe = migrate_items(frontend_graph, set(TARGET_IDS))
    save_json(FRONTEND_GRAPH, frontend_graph)
    print(f"前端图谱已修正，迁移 {len(moved_fe)} 个节点")

    # 内容索引：检查是否有 section 字段
    content_index = load_json(CONTENT_INDEX)
    ci_has_section = False
    # content_index 本身只有 parts 元信息，不保存 item 级 section
    # 进一步确认：检查 parts 文件内是否有 section_id/section_name
    sample_part_path = None
    for part in content_index.get("parts", []):
        sample_part_path = ROOT / part["path"]
        if sample_part_path.exists():
            break
    if sample_part_path:
        sample = load_json(sample_part_path)
        items = sample if isinstance(sample, list) else sample.get("items", [])
        if items and isinstance(items[0], dict):
            ci_has_section = any(
                k in items[0] for k in ("section_id", "section_name")
            )

    content_index_changed = False
    if ci_has_section:
        # 遍历所有 part 同步 section 字段
        for part in content_index.get("parts", []):
            part_path = ROOT / part["path"]
            if not part_path.exists():
                continue
            part_data = load_json(part_path)
            items = part_data if isinstance(part_data, list) else part_data.get("items", [])
            changed = False
            for it in items:
                if isinstance(it, dict) and it.get("item_id") in TARGET_IDS:
                    if "section_id" in it:
                        it["section_id"] = TO_SECTION_ID
                        changed = True
                    if "section_name" in it:
                        it["section_name"] = TO_SECTION_NAME
                        changed = True
            if changed:
                save_json(part_path, part_data)
                content_index_changed = True
        print(f"内容索引 part 文件已同步 section 字段: {content_index_changed}")
    else:
        print("内容索引未保存 item 级 section 元信息，无需同步")

    # 验证
    main_total, main_target_sec = verify_graph(main_graph_pre, "main")
    fe_total, fe_target_sec = verify_graph(frontend_graph, "frontend")

    main_ids = build_id_set(main_graph_pre)
    fe_ids = build_id_set(frontend_graph)
    ids_consistent = main_ids == fe_ids

    # 内容覆盖
    covered_ids = set()
    for part in content_index.get("parts", []):
        part_path = ROOT / part["path"]
        if not part_path.exists():
            continue
        part_data = load_json(part_path)
        items = part_data if isinstance(part_data, list) else part_data.get("items", [])
        if not isinstance(items, list):
            continue
        for it in items:
            if isinstance(it, dict):
                iid = it.get("item_id") or it.get("id")
                if iid:
                    covered_ids.add(iid)
    content_covers = len(main_ids - covered_ids) == 0
    batch2_covered = len(batch2_ids - covered_ids) == 0

    # 修正后统计
    sec_after, cat_after = compute_batch2_stats(main_graph_pre, batch2_ids)
    sec_after_fe, _ = compute_batch2_stats(frontend_graph, batch2_ids)

    # direct_pre/rel/resolved_pre 完整性：只确认字段仍然存在
    pre_check = {}
    for cat in main_graph_pre.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                if item["id"] in TARGET_IDS:
                    pre_check[item["id"]] = {
                        "direct_pre_present": "direct_pre" in item,
                        "rel_present": "rel" in item,
                        "resolved_pre_present": "resolved_pre" in item,
                    }

    report = {
        "fix_time": "2026-06-16",
        "target_ids": TARGET_IDS,
        "from_section_id": FROM_SECTION_ID,
        "to_section_id": TO_SECTION_ID,
        "to_section_name": TO_SECTION_NAME,
        "moved_main": moved_main,
        "moved_frontend": moved_fe,
        "files_modified": [
            str(MAIN_GRAPH.relative_to(ROOT)),
            str(FRONTEND_GRAPH.relative_to(ROOT)),
        ],
        "content_index_changed": content_index_changed,
        "content_index_has_section_field": ci_has_section,
        "verification": {
            "main_item_count": main_total,
            "frontend_item_count": fe_total,
            "content_index_source_item_count": content_index.get("source_item_count"),
            "main_frontend_same_ids": ids_consistent,
            "content_covers_all": content_covers,
            "batch2_content_covered": batch2_covered,
            "batch2_id_count": len(batch2_ids),
            "target_nodes_section": main_target_sec,
            "target_nodes_section_frontend": fe_target_sec,
            "pre_fields_check": pre_check,
        },
        "batch2_stats_before_fix": {
            "section_major_category": sec_before,
            "item_category": cat_before,
        },
        "batch2_stats_after_fix": {
            "section_major_category": sec_after,
            "item_category": cat_after,
            "frontend_section_major_category": sec_after_fe,
        },
    }

    out_path = ROOT / "data" / "stage5_batch2_persistent_segment_tree_section_fix_report.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"修复报告已写入: {out_path}")


if __name__ == "__main__":
    main()
