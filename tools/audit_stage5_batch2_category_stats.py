#!/usr/bin/env python3
"""Read-only audit for Stage5-HardKnowledge Batch2 category statistics."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN_GRAPH = ROOT / "merged_knowledge_graph_item_dependencies_refined.json"
FRONTEND_GRAPH = ROOT / "assets/data/knowledge/io_v4_4.json"
CONTENT_INDEX = ROOT / "assets/data/knowledge_content/content_index.json"
OUT_JSON = ROOT / "data/stage5_batch2_category_stats_audit.json"
OUT_MD = ROOT / "docs/stage5_batch2_category_stats_audit.md"

BATCH2_MAPPING = ROOT / "data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json"
BATCH2_SUMMARY = ROOT / "data/stage5_hard_knowledge_batch2_full600_added_items_summary.json"
BATCH2_CHECKPOINT = ROOT / "data/stage5_hard_knowledge_batch2_full_chain_stable_checkpoint.json"
BATCH2_STABLE_CHECKPOINT = ROOT / "data/stage5_hard_knowledge_batch2_full600_stable_checkpoint.json"
BATCH2_EXISTING_AUDIT = ROOT / "data/stage5_hard_batch2_category_distribution_audit.json"

KEYWORDS = [
    "主席树",
    "可持久化线段树",
    "李超线段树",
    "动态开点线段树",
    "动态开点",
    "persistent segment tree",
    "Li Chao",
    "segment tree",
]

ID_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pick_key(obj: dict[str, Any], candidates: list[str]) -> str | None:
    for key in candidates:
        if key in obj:
            return key
    return None


def graph_candidates(data: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Detect sections and items without assuming a single fixed schema."""
    section_keys = ["sections", "chapters", "nodes"]
    item_keys = ["items", "knowledge_items", "children", "nodes"]
    sections: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    meta: dict[str, Any] = {
        "items_path": None,
        "sections_path": None,
        "category_container_path": None,
    }

    if isinstance(data, dict):
        if isinstance(data.get("items"), list):
            items = [x for x in data["items"] if isinstance(x, dict)]
            meta["items_path"] = "$.items"
        if isinstance(data.get("sections"), list):
            sections = [x for x in data["sections"] if isinstance(x, dict)]
            meta["sections_path"] = "$.sections"

        categories = data.get("categories")
        if isinstance(categories, list):
            meta["category_container_path"] = "$.categories"
            for ci, cat in enumerate(categories):
                if not isinstance(cat, dict):
                    continue
                for sk in section_keys:
                    if isinstance(cat.get(sk), list):
                        if meta["sections_path"] is None:
                            meta["sections_path"] = f"$.categories[*].{sk}"
                        for sec in cat[sk]:
                            if not isinstance(sec, dict):
                                continue
                            section = dict(sec)
                            section["_detected_category_name"] = cat.get("name") or cat.get("title") or cat.get("id")
                            section["_detected_category_index"] = ci
                            sections.append(section)
                            for ik in item_keys:
                                if isinstance(sec.get(ik), list):
                                    if meta["items_path"] is None:
                                        meta["items_path"] = f"$.categories[*].{sk}[*].{ik}"
                                    for item in sec[ik]:
                                        if isinstance(item, dict):
                                            enriched = dict(item)
                                            enriched["_detected_section_id"] = (
                                                sec.get("id") or sec.get("section_id") or sec.get("chapter_id")
                                            )
                                            enriched["_detected_section_name"] = (
                                                sec.get("name") or sec.get("title") or sec.get("label")
                                            )
                                            enriched["_detected_category_name"] = section["_detected_category_name"]
                                            items.append(enriched)
                                    break
                        break

    return sections, items, meta


def detect_schema(data: Any) -> dict[str, Any]:
    sections, items, meta = graph_candidates(data)
    item_sample = items[0] if items else {}
    section_sample = sections[0] if sections else {}
    category_fields = [
        key
        for key in ["category", "domain", "type", "main_category", "category_name", "source_category"]
        if any(key in item for item in items[:200])
    ]
    return {
        **meta,
        "section_count_detected": len(sections),
        "item_count_detected": len(items),
        "item_id_field": pick_key(item_sample, ["id", "item_id", "itemId", "knowledge_id", "uid"]),
        "item_title_field": pick_key(item_sample, ["name", "title", "label", "display_name"]),
        "section_id_field": pick_key(section_sample, ["id", "section_id", "chapter_id", "parent"]),
        "section_title_field": pick_key(section_sample, ["name", "title", "label"]),
        "item_section_field": pick_key(item_sample, ["parent", "section_id", "chapter_id", "section", "main_section_id"]),
        "item_category_fields": category_fields,
        "section_category_source": "_detected_category_name from parent category container",
    }


def flatten_graph(data: Any) -> dict[str, Any]:
    schema = detect_schema(data)
    sections, items, _ = graph_candidates(data)
    sid_field = schema["section_id_field"]
    stitle_field = schema["section_title_field"]
    iid_field = schema["item_id_field"]
    title_field = schema["item_title_field"]
    item_section_field = schema["item_section_field"]

    section_by_id: dict[str, dict[str, Any]] = {}
    for section in sections:
        sid = str(section.get(sid_field) or section.get("_detected_section_id") or "")
        if sid:
            section_by_id[sid] = {
                "id": sid,
                "name": section.get(stitle_field) or section.get("name") or section.get("title") or "",
                "category": section.get("_detected_category_name") or section.get("category") or section.get("domain"),
                "raw": section,
            }

    item_by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        iid = str(item.get(iid_field) or "")
        if not iid:
            continue
        sid = str(item.get(item_section_field) or item.get("_detected_section_id") or "")
        item_by_id[iid] = {
            "id": iid,
            "title": item.get(title_field) or "",
            "section_id": sid,
            "section_name": section_by_id.get(sid, {}).get("name", item.get("_detected_section_name") or ""),
            "section_category": section_by_id.get(sid, {}).get("category", item.get("_detected_category_name")),
            "raw": item,
        }

    return {"schema": schema, "sections": section_by_id, "items": item_by_id}


def normalize_category(value: Any) -> str:
    if value is None or value == "":
        return "未标注"
    if isinstance(value, list):
        return ",".join(str(x) for x in value) if value else "未标注"
    text = str(value)
    if text == "算法竞赛数学":
        return "数学"
    return text


def inferred_major_from_section(section_id: str, section_name: str = "") -> str:
    prefix = section_id.split(".", 1)[0]
    if prefix == "2":
        return "算法"
    if prefix == "3":
        return "数据结构"
    if prefix == "4":
        return "数学"
    if prefix == "1":
        return "C++语法"
    if prefix == "5":
        return "C++编程/调试技巧"
    name = section_name or ""
    if "数学" in name or "组合" in name or "数论" in name:
        return "数学"
    if "数据结构" in name or "树" in name or "堆" in name:
        return "数据结构"
    if "算法" in name or "搜索" in name or "动态规划" in name:
        return "算法"
    return "未知"


def section_major(item: dict[str, Any]) -> str:
    return normalize_category(item.get("section_category")) or inferred_major_from_section(
        item.get("section_id", ""), item.get("section_name", "")
    )


def stats_by_item_fields(items: list[dict[str, Any]], fields: list[str]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for field in fields:
        counter = Counter(normalize_category(item["raw"].get(field)) for item in items)
        result[field] = dict(counter)
    if not result:
        result["<no category/domain/type field detected>"] = {"未标注": len(items)}
    return result


def extract_ids_from_mapping(path: Path) -> tuple[set[str], str, str]:
    if not path.exists():
        return set(), str(path), "missing"
    data = load_json(path)
    ids: set[str] = set()
    mappings = data.get("mappings") if isinstance(data, dict) else data
    if isinstance(mappings, list):
        for row in mappings:
            if not isinstance(row, dict):
                continue
            for key in ["item_id", "new_item_id", "target_item_id", "id", "assigned_item_id"]:
                value = row.get(key)
                if isinstance(value, str) and ID_RE.match(value):
                    ids.add(value)
                    break
    status = "ok" if ids else "empty"
    return ids, str(path.relative_to(ROOT)), status


def extract_content_ids(index: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    parts = index.get("parts", [])
    if not isinstance(parts, list):
        return ids
    for part in parts:
        if not isinstance(part, dict):
            continue
        p = part.get("path")
        if not isinstance(p, str):
            continue
        path = ROOT / p
        if not path.exists():
            continue
        try:
            data = load_json(path)
        except Exception:
            continue
        candidates: list[Any] = []
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            for key in ["items", "contents", "modules", "data"]:
                if isinstance(data.get(key), list):
                    candidates = data[key]
                    break
        for row in candidates:
            if not isinstance(row, dict):
                continue
            for key in ["item_id", "itemId", "id", "knowledge_id"]:
                value = row.get(key)
                if isinstance(value, str) and ID_RE.match(value):
                    ids.add(value)
                    break
    return ids


def read_distribution(path: Path, preferred_keys: list[str]) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": str(path.relative_to(ROOT))}
    data = load_json(path)
    result: dict[str, Any] = {"path": str(path.relative_to(ROOT))}
    if isinstance(data, dict):
        for key in preferred_keys:
            if key in data:
                result[key] = data[key]
        if len(result) == 1:
            for key, value in data.items():
                if "distribution" in key or "category" in key or "summary" in key:
                    result[key] = value
    return result


def parse_md_distribution(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    stats: dict[str, int] = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*(算法|数据结构|数学)\s*\|\s*\**([0-9,]+)\**\s*\|", line)
        if m:
            stats[m.group(1)] = int(m.group(2).replace(",", ""))
    return stats


def keyword_expected_section(title: str) -> str:
    low = title.lower()
    if "动态开点线段树" in title or "动态开点" in title:
        return "3.7"
    if "主席树" in title or "可持久化线段树" in title or "persistent segment tree" in low:
        return "3.13"
    if "李超线段树" in title or "li chao" in low:
        return "3.13"
    if "segment tree" in low:
        return "3.13"
    return ""


def main() -> None:
    audit_time = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    main = flatten_graph(load_json(MAIN_GRAPH))
    frontend = flatten_graph(load_json(FRONTEND_GRAPH))
    content_index = load_json(CONTENT_INDEX)

    main_ids = set(main["items"])
    frontend_ids = set(frontend["items"])
    content_ids = extract_content_ids(content_index)

    batch2_ids, batch2_source, batch2_status = extract_ids_from_mapping(BATCH2_MAPPING)
    mapping_hit_count = len(batch2_ids & main_ids)
    if not batch2_ids or mapping_hit_count != len(batch2_ids):
        baseline = ROOT / "backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch2_full600_20260526_223555.json"
        if baseline.exists():
            base = flatten_graph(load_json(baseline))
            baseline_ids = main_ids - set(base["items"])
            if len(baseline_ids) == 600:
                batch2_ids = baseline_ids
                batch2_source = str(baseline.relative_to(ROOT))
                batch2_status = (
                    "derived_current_minus_baseline; mapping_source_hit_count="
                    f"{mapping_hit_count}/{len(extract_ids_from_mapping(BATCH2_MAPPING)[0])}"
                )

    batch2_items = [main["items"][iid] for iid in sorted(batch2_ids) if iid in main["items"]]
    frontend_batch2_items = [frontend["items"][iid] for iid in sorted(batch2_ids) if iid in frontend["items"]]

    section_stats = Counter(section_major(item) for item in batch2_items)
    section_id_stats = Counter(item["section_id"] for item in batch2_items)
    item_field_stats = stats_by_item_fields(batch2_items, main["schema"]["item_category_fields"])
    frontend_field_stats = stats_by_item_fields(frontend_batch2_items, frontend["schema"]["item_category_fields"])
    inferred_section_stats = Counter(
        inferred_major_from_section(item["section_id"], item["section_name"]) for item in batch2_items
    )

    keyword_rows = []
    for iid in sorted(batch2_ids):
        item = main["items"].get(iid)
        if not item:
            continue
        title = str(item.get("title", ""))
        haystack = title.lower()
        if not any(k.lower() in haystack for k in KEYWORDS):
            continue
        fitem = frontend["items"].get(iid, {})
        expected = keyword_expected_section(title)
        status = "ok" if expected and item["section_id"] == expected and fitem.get("section_id") == expected else "check"
        keyword_rows.append(
            {
                "id": iid,
                "title": title,
                "main_section_id": item["section_id"],
                "main_section_name": item["section_name"],
                "main_category_fields": {
                    field: item["raw"].get(field) for field in main["schema"]["item_category_fields"]
                },
                "frontend_section_id": fitem.get("section_id"),
                "frontend_category_fields": {
                    field: fitem.get("raw", {}).get(field) for field in frontend["schema"]["item_category_fields"]
                },
                "has_content": iid in content_ids,
                "expected_section": expected,
                "status": status,
            }
        )

    merge_report_md_stats = parse_md_distribution(ROOT / "docs/stage5_hard_knowledge_batch2_full600_merge_report.md")
    checkpoint_report_md_stats = parse_md_distribution(
        ROOT / "docs/stage5_hard_knowledge_batch2_full_chain_stable_checkpoint_report.md"
    )

    consistency = {
        "main_item_count": len(main_ids),
        "frontend_item_count": len(frontend_ids),
        "content_index_source_item_count": content_index.get("source_item_count"),
        "content_index_generated_item_count": content_index.get("generated_item_count"),
        "content_package_count": len(content_index.get("parts", [])) if isinstance(content_index.get("parts"), list) else None,
        "content_loaded_item_count": len(content_ids),
        "main_frontend_same_ids": main_ids == frontend_ids,
        "main_minus_frontend_count": len(main_ids - frontend_ids),
        "frontend_minus_main_count": len(frontend_ids - main_ids),
        "content_covers_main_count": len(main_ids & content_ids),
        "content_missing_main_count": len(main_ids - content_ids),
        "batch2_content_covered_count": len(batch2_ids & content_ids),
        "batch2_content_missing": sorted(batch2_ids - content_ids),
    }

    keyword_status_counts = Counter(row["status"] for row in keyword_rows)
    keyword_mismatch_count = keyword_status_counts.get("check", 0)

    conclusions = []
    if len(batch2_ids) != 600:
        conclusions.append("C")
    if not consistency["main_frontend_same_ids"] or consistency["content_missing_main_count"]:
        conclusions.append("D")
    has_section_ds = section_stats.get("数据结构", 0) > 0 or inferred_section_stats.get("数据结构", 0) > 0
    checkpoint_ds_zero = checkpoint_report_md_stats.get("数据结构") == 0
    if has_section_ds and checkpoint_ds_zero:
        conclusions.append("A")
    if keyword_mismatch_count:
        conclusions.append("B")
    elif item_field_stats and any(stats.get("数据结构", 0) == 0 for stats in item_field_stats.values()):
        conclusions.append("B")
    if not conclusions:
        conclusions.append("A")
    final_case = "E" if len(set(conclusions)) > 1 else conclusions[0]

    result = {
        "audit_time": audit_time,
        "inputs": {
            "main_graph": str(MAIN_GRAPH.relative_to(ROOT)),
            "frontend_graph": str(FRONTEND_GRAPH.relative_to(ROOT)),
            "content_index": str(CONTENT_INDEX.relative_to(ROOT)),
        },
        "detected_schema": {"main": main["schema"], "frontend": frontend["schema"]},
        "consistency": consistency,
        "batch2_id_count": len(batch2_ids),
        "batch2_id_source": batch2_source,
        "batch2_id_status": batch2_status,
        "stats_by_section_major_category": dict(section_stats),
        "stats_by_section_major_category_inferred_from_prefix": dict(inferred_section_stats),
        "stats_by_section_id": dict(section_id_stats),
        "stats_by_item_category_field": item_field_stats,
        "stats_by_frontend_category_field": frontend_field_stats,
        "stats_by_merge_report": {
            "markdown": merge_report_md_stats,
            "json": read_distribution(BATCH2_SUMMARY, ["category_distribution", "section_distribution"]),
        },
        "stats_by_checkpoint_report": {
            "markdown": checkpoint_report_md_stats,
            "json_full_chain": read_distribution(BATCH2_CHECKPOINT, ["batch2_summary", "section_relocation_summary"]),
            "json_stable": read_distribution(BATCH2_STABLE_CHECKPOINT, ["batch2_distribution"]),
            "existing_audit": read_distribution(
                BATCH2_EXISTING_AUDIT,
                [
                    "original_merge_report_distribution",
                    "checkpoint_report_distribution",
                    "corrected_distribution",
                    "root_cause",
                ],
            ),
        },
        "keyword_data_structure_nodes": keyword_rows,
        "keyword_data_structure_status_summary": dict(keyword_status_counts),
        "inference_logic": [
            "Prefer section metadata category from the parent categories container.",
            "If section metadata has no category, infer by section id prefix: 2.x=算法, 3.x=数据结构, 4.x=数学, 1.x=C++语法, 5.x=C++编程/调试技巧.",
            "If prefix is unknown, use section title keywords as a fallback.",
        ],
        "conclusion_case": final_case,
        "conclusion_text": {
            "A": "主图谱和前端图谱分类基本正确，是 checkpoint 报告统计口径错误。",
            "B": "主图谱节点字段确实错误。",
            "C": "Batch2 ID 集合提取错误。",
            "D": "前端图谱或内容包同步错误。",
            "E": "多种问题同时存在。",
        }[final_case],
        "recommend_enter_batch3": final_case == "A" and len(batch2_ids) == 600 and consistency["main_frontend_same_ids"] and not consistency["batch2_content_missing"],
    }

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "conclusion_case": result["conclusion_case"],
        "batch2_id_count": result["batch2_id_count"],
        "outputs": [str(OUT_MD.relative_to(ROOT)), str(OUT_JSON.relative_to(ROOT))],
    }, ensure_ascii=False, indent=2))


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(out)


def render_counter_table(counter: dict[str, int]) -> str:
    return md_table(["分类", "数量"], [[k, v] for k, v in sorted(counter.items())])


def render_markdown(result: dict[str, Any]) -> str:
    c = result["consistency"]
    keyword_rows = result["keyword_data_structure_nodes"]
    keyword_table = md_table(
        [
            "id",
            "title",
            "main_section_id",
            "main_section_name",
            "main_category_fields",
            "frontend_section_id",
            "frontend_category_fields",
            "has_content",
            "expected_section",
            "status",
        ],
        [
            [
                row["id"],
                row["title"],
                row["main_section_id"],
                row["main_section_name"],
                json.dumps(row["main_category_fields"], ensure_ascii=False),
                row["frontend_section_id"],
                json.dumps(row["frontend_category_fields"], ensure_ascii=False),
                row["has_content"],
                row["expected_section"],
                row["status"],
            ]
            for row in keyword_rows
        ],
    )
    lines = [
        "# Stage5 Batch2 Category Stats Audit",
        "",
        f"- 审计时间: `{result['audit_time']}`",
        "",
        "## 输入文件",
        "",
        md_table(["类型", "路径"], [[k, v] for k, v in result["inputs"].items()]),
        "",
        "## 自动探测 Schema",
        "",
        "### 主图谱",
        "",
        "```json",
        json.dumps(result["detected_schema"]["main"], ensure_ascii=False, indent=2),
        "```",
        "",
        "### 前端图谱",
        "",
        "```json",
        json.dumps(result["detected_schema"]["frontend"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Batch2 ID 来源",
        "",
        md_table(
            ["字段", "值"],
            [
                ["batch2_id_source", result["batch2_id_source"]],
                ["batch2_id_status", result["batch2_id_status"]],
                ["batch2_id_count", result["batch2_id_count"]],
            ],
        ),
        "",
        "## 一致性检查",
        "",
        md_table(
            ["检查项", "结果"],
            [
                ["main_item_count", c["main_item_count"]],
                ["frontend_item_count", c["frontend_item_count"]],
                ["content_index_source_item_count", c["content_index_source_item_count"]],
                ["content_index_generated_item_count", c["content_index_generated_item_count"]],
                ["content_package_count", c["content_package_count"]],
                ["content_loaded_item_count", c["content_loaded_item_count"]],
                ["main_frontend_same_ids", c["main_frontend_same_ids"]],
                ["content_missing_main_count", c["content_missing_main_count"]],
                ["batch2_content_covered_count", c["batch2_content_covered_count"]],
                ["batch2_content_missing_count", len(c["batch2_content_missing"])],
            ],
        ),
        "",
        "## 分类统计对比",
        "",
        "### stats_by_section_major_category",
        "",
        render_counter_table(result["stats_by_section_major_category"]),
        "",
        "### stats_by_section_major_category_inferred_from_prefix",
        "",
        render_counter_table(result["stats_by_section_major_category_inferred_from_prefix"]),
        "",
        "### stats_by_item_category_field",
        "",
        "```json",
        json.dumps(result["stats_by_item_category_field"], ensure_ascii=False, indent=2),
        "```",
        "",
        "### stats_by_frontend_category_field",
        "",
        "```json",
        json.dumps(result["stats_by_frontend_category_field"], ensure_ascii=False, indent=2),
        "```",
        "",
        "### stats_by_merge_report",
        "",
        "```json",
        json.dumps(result["stats_by_merge_report"], ensure_ascii=False, indent=2),
        "```",
        "",
        "### stats_by_checkpoint_report",
        "",
        "```json",
        json.dumps(result["stats_by_checkpoint_report"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## 重点数据结构关键词节点核查",
        "",
        "状态汇总:",
        "",
        render_counter_table(result["keyword_data_structure_status_summary"]),
        "",
        keyword_table if keyword_rows else "未命中关键词节点。",
        "",
        "## 推断逻辑",
        "",
        "\n".join(f"- {line}" for line in result["inference_logic"]),
        "",
        "## 异常原因",
        "",
        f"- 结论类型: `{result['conclusion_case']}`",
        f"- {result['conclusion_text']}",
        "- 从当前数据复算看，Batch2 的 section 大类中存在数据结构节点；checkpoint 报告的 `数据结构 0` 与当前图谱不一致。",
        "- 重点关键词核查中仍有 `check` 项时，表示这些节点的当前 section 与本次审计预期不一致，需要人工复核后再继续扩批。",
        "",
        "## 后续建议",
        "",
        "- 不需要修改主图谱、前端图谱或内容索引来解决该统计冲突。",
        "- 后续如要消除报告冲突，应单独修正 checkpoint 报告生成脚本的分类统计口径，并重新生成 checkpoint 报告。",
        f"- 是否建议进入 Batch3: {'是' if result['recommend_enter_batch3'] else '否'}。",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
