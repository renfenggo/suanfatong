import csv
import json
import re
import shutil
from collections import Counter, defaultdict, deque
from copy import deepcopy
from pathlib import Path


BASE = Path(__file__).resolve().parent
ORIGINAL_JSON = BASE / "io_v4_4.json"
MAPPINGS_JSON = BASE / "advanced_knowledge_mappings.json"
MERGED_JSON = BASE / "merged_knowledge_graph.json"
BACKUP_JSON = BASE / "merged_knowledge_graph.analysis_only_backup.json"
MANUAL_REVIEW_JSON = BASE / "manual_review_table.json"
MANUAL_REVIEW_CSV = BASE / "manual_review_table.csv"
MANUAL_REVIEW_MD = BASE / "manual_review_table.md"
STATS_JSON = BASE / "real_fusion_statistics.json"
REPORT_MD = BASE / "real_fusion_report.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path, data):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_name(value):
    value = re.sub(r"\([^)]*\)", "", value)
    value = re.sub(r"（[^）]*）", "", value)
    value = re.sub(r"^(排序|贪心|枚举|递归|分治|搜索|图的遍历|网络流|线段树|字符串|DP|动态规划)[：:]", "", value)
    value = re.sub(r"[/,，、\s\-_:：]+", "", value)
    return value.lower()


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def add_unique(target, values):
    for value in ensure_list(values):
        if value not in target:
            target.append(value)


def section_level_to_item_level(section_level, name):
    if section_level in {"L1", "L2", "L3", "L4", "L5"}:
        level = section_level
    else:
        level = "L2"

    advanced_keywords = [
        "支配树",
        "圆方树",
        "虚树",
        "后缀自动机",
        "后缀数组",
        "LCT",
        "Link-Cut",
        "可持久化",
        "网络流",
        "费用流",
        "上下界",
        "半平面交",
        "Burnside",
        "Polya",
        "莫比乌斯反演",
        "二项式反演",
        "主席树",
        "Top Tree",
        "动态图",
    ]
    non_mainstream_keywords = ["机器学习", "数据库", "操作系统", "汇编", "线程安全", "死锁"]

    if any(k.lower() in name.lower() for k in non_mainstream_keywords):
        return "L5"
    if any(k.lower() in name.lower() for k in advanced_keywords):
        return "L4"
    return level


def build_indexes(kg):
    categories_by_name = {}
    sections_by_id = {}
    items_by_id = {}
    section_items = {}

    for category in kg["categories"]:
        categories_by_name[category["name"]] = category
        for section in category.get("sections", []):
            sections_by_id[section["id"]] = section
            section_items[section["id"]] = section.setdefault("items", [])
            for item in section.get("items", []):
                items_by_id[item["id"]] = item
    return categories_by_name, sections_by_id, items_by_id, section_items


def initialize_original_items(kg):
    for category in kg["categories"]:
        for section in category.get("sections", []):
            section_pre = ensure_list(section.get("pre"))
            section_rel = ensure_list(section.get("rel"))
            for item in section.get("items", []):
                item.setdefault("alias", [])
                item.setdefault("parent", section["id"])
                item.setdefault("direct_pre", [section["id"]])
                item.setdefault("resolved_pre", [section["id"], *section_pre])
                item.setdefault("rel", list(section_rel))
                item["level"] = item.get("level") or section_level_to_item_level(section.get("level"), item.get("name", ""))
                item["source"] = ["json"]
                item["docx_ids"] = []
                item["merge_type"] = "original"


def next_item_id(section):
    prefix = section["id"] + "."
    max_suffix = 0
    for item in section.get("items", []):
        item_id = str(item.get("id", ""))
        if item_id.startswith(prefix):
            suffix = item_id[len(prefix) :]
            if suffix.isdigit():
                max_suffix = max(max_suffix, int(suffix))
    return f"{section['id']}.{max_suffix + 1}"


def next_section_id(category_name, kg):
    prefixes = {
        "C++语法": "1",
        "算法": "2",
        "数据结构": "3",
        "算法竞赛数学": "4",
        "C++编程/调试技巧": "5",
    }
    prefix = prefixes[category_name]
    max_num = 0
    for category in kg["categories"]:
        if category["name"] != category_name:
            continue
        for section in category.get("sections", []):
            match = re.match(rf"^{re.escape(prefix)}\.(\d+)$", str(section.get("id", "")))
            if match:
                max_num = max(max_num, int(match.group(1)))
    return f"{prefix}.{max_num + 1}"


def classify_pattern_match(docx_name, section):
    normalized_docx = normalize_name(docx_name)
    best = None
    best_score = 0

    for item in section.get("items", []):
        item_name = item.get("name", "")
        normalized_item = normalize_name(item_name)
        if not normalized_item:
            continue

        score = 0
        if normalized_docx == normalized_item:
            score = 100
        elif normalized_item in normalized_docx or normalized_docx in normalized_item:
            score = 80
        else:
            item_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", item_name.lower()))
            docx_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", docx_name.lower()))
            if item_tokens and docx_tokens:
                overlap = len(item_tokens & docx_tokens)
                score = overlap * 10

        if score > best_score:
            best_score = score
            best = item

    if best and best_score >= 60:
        return "subtopic_of_existing_node", best
    return "new_item_under_existing_section", None


NEW_SECTION_DEPENDENCIES = {
    "随机化与启发式算法": {
        "pre": ["1.3", "1.4", "1.5", "2.1", "2.7", "4.6"],
        "rel": ["2.18", "5.7"],
    },
    "交互题与构造题技巧": {
        "pre": ["1.3", "1.4", "1.5", "2.1", "2.6", "5.7"],
        "rel": ["4.4", "5.9"],
    },
    "高级图论扩展": {
        "pre": ["2.9", "2.13", "2.14", "2.15", "3.9", "5.5"],
        "rel": ["2.16", "3.11"],
    },
    "高级数学与群论": {
        "pre": ["4.1", "4.2", "4.3", "4.4"],
        "rel": ["2.8", "2.18"],
    },
    "竞赛工程化与优化": {
        "pre": ["1.3", "1.8", "5.4", "5.7", "5.9"],
        "rel": ["2.18"],
    },
    "算法竞赛心理与策略": {
        "pre": [],
        "rel": ["5.7", "5.9"],
    },
}


def create_new_sections(kg, mappings):
    categories_by_name, sections_by_id, _, _ = build_indexes(kg)
    grouped = {}

    for row in mappings["new_sections"]:
        suggested = row["suggested_section"]
        key = (suggested["category"], suggested["name"])
        grouped.setdefault(key, {"suggested": suggested, "rows": []})["rows"].append(row)

    created_sections = []
    for (category_name, section_name), payload in grouped.items():
        category = categories_by_name[category_name]
        section_id = next_section_id(category_name, kg)
        suggested = payload["suggested"]
        deps = NEW_SECTION_DEPENDENCIES.get(section_name, {"pre": [], "rel": []})
        section = {
            "id": section_id,
            "name": section_name,
            "level": suggested.get("level", "L3"),
            "pre": list(deps["pre"]),
            "rel": list(deps["rel"]),
            "created_from": "docx_new_section_suggestion",
            "keywords": suggested.get("keywords", []),
            "items": [],
        }
        category.setdefault("sections", []).append(section)
        sections_by_id[section_id] = section
        section["_created_category"] = category_name
        created_sections.append(section)

        for row in payload["rows"]:
            item = make_docx_item(
                section,
                row["docx_name"],
                row["docx_id"],
                "new_item_in_new_section",
                mapping_reason=row.get("reason", ""),
            )
            section["items"].append(item)

    return created_sections


def make_docx_item(section, name, docx_id, merge_type, parent_concept=None, mapping_reason=""):
    item_id = next_item_id(section)
    rel = list(ensure_list(section.get("rel")))
    item = {
        "id": item_id,
        "name": name,
        "alias": [],
        "parent": section["id"],
        "level": section_level_to_item_level(section.get("level"), name),
        "direct_pre": [section["id"]],
        "resolved_pre": [section["id"], *ensure_list(section.get("pre"))],
        "rel": rel,
        "source": ["docx"],
        "docx_ids": [docx_id],
        "merge_type": merge_type,
        "mapping_reason": mapping_reason,
    }
    if parent_concept:
        item["parent_concept"] = {
            "id": parent_concept["id"],
            "name": parent_concept["name"],
        }
        add_unique(item["rel"], [parent_concept["id"]])
    return item


def apply_exact_matches(mappings, items_by_id):
    merged = 0
    unique_items = set()
    for row in mappings["exact_matches"]:
        item = items_by_id.get(row["item_id"])
        if not item:
            continue
        item.setdefault("alias", [])
        if normalize_name(row["docx_name"]) != normalize_name(item["name"]):
            add_unique(item["alias"], [row["docx_name"]])
        add_unique(item.setdefault("source", ["json"]), ["docx"])
        add_unique(item.setdefault("docx_ids", []), [row["docx_id"]])
        item["merge_type"] = "same_concept"
        item["exact_match_reason"] = row.get("reason", "")
        merged += 1
        unique_items.add(item["id"])
    return merged, len(unique_items)


def apply_pattern_matches(mappings, sections_by_id):
    counts = Counter()
    added = 0
    for row in mappings["pattern_matches"]:
        section = sections_by_id[row["section_id"]]
        merge_type, parent_concept = classify_pattern_match(row["docx_name"], section)
        item = make_docx_item(
            section,
            row["docx_name"],
            row["docx_id"],
            merge_type,
            parent_concept=parent_concept,
            mapping_reason=row.get("reason", ""),
        )
        item["mapping_score"] = row.get("score")
        section.setdefault("items", []).append(item)
        counts[merge_type] += 1
        added += 1
    return added, counts


def write_manual_review(mappings):
    rows = []
    for row in mappings["manual_review"]:
        rows.append(
            {
                "docx_id": row["docx_id"],
                "docx_name": row["docx_name"],
                "status": "needs_manual_review",
                "reason": row.get("reason", ""),
                "suggested_action": "人工判断归属章节、是否应纳入主图谱、以及是否只是已有节点别名",
            }
        )

    dump_json(MANUAL_REVIEW_JSON, rows)
    with MANUAL_REVIEW_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["docx_id", "docx_name", "status", "reason", "suggested_action"],
        )
        writer.writeheader()
        writer.writerows(rows)
    md_lines = [
        "# 人工审核表",
        "",
        "| docx_id | docx_name | reason | suggested_action |",
        "|---:|---|---|---|",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['docx_id']} | {row['docx_name']} | {row['reason']} | {row['suggested_action']} |"
        )
    MANUAL_REVIEW_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return rows


def validate_graph(kg):
    section_ids = []
    item_ids = []
    dangling = []
    section_edges = []

    for category in kg["categories"]:
        for section in category.get("sections", []):
            section_ids.append(section["id"])
            for item in section.get("items", []):
                item_ids.append(item["id"])

    section_set = set(section_ids)
    item_set = set(item_ids)
    id_like = re.compile(r"^\d+(?:\.\d+)*[A-Z]?$")

    for category in kg["categories"]:
        for section in category.get("sections", []):
            for field in ["pre", "rel"]:
                for ref in ensure_list(section.get(field)):
                    if id_like.match(str(ref)) and ref not in section_set:
                        dangling.append({"scope": "section", "id": section["id"], "field": field, "ref": ref})
                    if field == "pre" and ref in section_set:
                        section_edges.append((ref, section["id"]))
            for item in section.get("items", []):
                for field in ["direct_pre", "resolved_pre", "rel"]:
                    for ref in ensure_list(item.get(field)):
                        if id_like.match(str(ref)) and ref not in section_set and ref not in item_set:
                            dangling.append({"scope": "item", "id": item["id"], "field": field, "ref": ref})

    indeg = {sid: 0 for sid in section_set}
    adj = defaultdict(list)
    for pre, section in section_edges:
        adj[pre].append(section)
        indeg[section] += 1

    queue = deque([sid for sid, degree in indeg.items() if degree == 0])
    seen = []
    while queue:
        sid = queue.popleft()
        seen.append(sid)
        for nxt in adj[sid]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    cycle_nodes = [sid for sid, degree in indeg.items() if degree > 0]
    return {
        "duplicate_section_ids": [sid for sid, count in Counter(section_ids).items() if count > 1],
        "duplicate_item_ids": [iid for iid, count in Counter(item_ids).items() if count > 1],
        "dangling_references": dangling,
        "section_pre_cycle_nodes": cycle_nodes,
    }


def collect_counts(kg):
    category_distribution = {}
    for category in kg["categories"]:
        original = 0
        exact = 0
        docx_added = 0
        for section in category.get("sections", []):
            for item in section.get("items", []):
                if item.get("source") == ["docx"]:
                    docx_added += 1
                elif item.get("merge_type") == "same_concept":
                    exact += 1
                else:
                    original += 1
        category_distribution[category["name"]] = {
            "sections": len(category.get("sections", [])),
            "items": original + exact + docx_added,
            "original_only_items": original,
            "exact_merged_original_items": exact,
            "docx_added_items": docx_added,
        }
    return category_distribution


def write_report(stats):
    lines = [
        "# 真实融合结果报告",
        "",
        f"- 原始 JSON 节点数：{stats['formula']['original_json_items']}",
        f"- exact_matches 合并记录数：{stats['formula']['exact_matches_merged']}",
        f"- exact_matches 覆盖原节点数：{stats['formula']['exact_matches_unique_items']}",
        f"- pattern_matches 新增节点数：{stats['formula']['pattern_items_added']}",
        f"- 新章节新增节点数：{stats['formula']['new_section_items_added']}",
        f"- 新增节点总数：{stats['formula']['added_items_total']}",
        f"- 最终节点数：{stats['formula']['final_items']}",
        f"- 计算公式：{stats['formula']['expression']}",
        "",
        "## 模式匹配拆分",
        "",
    ]
    for key, value in stats["pattern_match_split"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 唯一新增章节", ""])
    for section in stats["created_sections"]:
        lines.append(f"- {section['id']} {section['name']}（{section['category']}，{section['level']}）：{section['items']} 个节点")
    lines.extend(["", "## 分类分布", ""])
    for category, row in stats["category_distribution"].items():
        lines.append(
            f"- {category}: {row['sections']} 章，{row['items']} 节点；"
            f"原始-only {row['original_only_items']}，exact 合并 {row['exact_merged_original_items']}，docx 新增 {row['docx_added_items']}"
        )
    lines.extend(["", "## 校验", ""])
    validation = stats["validation"]
    lines.append(f"- 重复章节 ID：{len(validation['duplicate_section_ids'])}")
    lines.append(f"- 重复知识点 ID：{len(validation['duplicate_item_ids'])}")
    lines.append(f"- 悬空引用：{len(validation['dangling_references'])}")
    lines.append(f"- 章节强依赖环节点：{len(validation['section_pre_cycle_nodes'])}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if MERGED_JSON.exists() and not BACKUP_JSON.exists():
        shutil.copy2(MERGED_JSON, BACKUP_JSON)

    kg = deepcopy(load_json(ORIGINAL_JSON))
    mappings = load_json(MAPPINGS_JSON)

    initialize_original_items(kg)
    categories_by_name, sections_by_id, items_by_id, _ = build_indexes(kg)

    exact_merged, exact_unique_items = apply_exact_matches(mappings, items_by_id)
    pattern_added, pattern_counts = apply_pattern_matches(mappings, sections_by_id)
    created_sections_map = create_new_sections(kg, mappings)
    manual_review_rows = write_manual_review(mappings)

    final_categories_by_name, final_sections_by_id, final_items_by_id, _ = build_indexes(kg)

    created_sections = []
    for section in created_sections_map:
        created_sections.append(
            {
                "category": section.pop("_created_category", ""),
                "id": section["id"],
                "name": section["name"],
                "level": section["level"],
                "items": len(section.get("items", [])),
            }
        )

    original_count = 592
    new_section_added = sum(len(section.get("items", [])) for section in created_sections_map)
    added_total = pattern_added + new_section_added
    final_count = len(final_items_by_id)

    kg["meta"]["title"] = "算法竞赛知识图谱融合版"
    kg["meta"]["source_files"] = ["io_v4_4.json", "算法知识图谱aa.docx"]
    kg["meta"]["merge_strategy"] = "以原 JSON 五大类为骨架；exact_matches 合并到原节点；pattern_matches 与新章节建议作为 docx 新节点落入主图谱；manual_review 单独输出审核表。"
    kg["meta"]["final_fusion_statistics"] = {
        "original_json_items": original_count,
        "exact_matches_merged": exact_merged,
        "exact_matches_unique_items": exact_unique_items,
        "pattern_items_added": pattern_added,
        "new_section_items_added": new_section_added,
        "manual_review_items": len(manual_review_rows),
        "final_items": final_count,
    }

    validation = validate_graph(kg)
    stats = {
        "formula": {
            "original_json_items": original_count,
            "exact_matches_merged": exact_merged,
            "exact_matches_unique_items": exact_unique_items,
            "pattern_items_added": pattern_added,
            "new_section_items_added": new_section_added,
            "added_items_total": added_total,
            "final_items": final_count,
            "expression": f"{original_count} 原节点 + {added_total} 新增节点；{exact_merged} 个 exact_matches 合并进原节点不新增 = {final_count}",
        },
        "pattern_match_split": dict(pattern_counts),
        "created_sections": created_sections,
        "manual_review": {
            "items": len(manual_review_rows),
            "json": str(MANUAL_REVIEW_JSON),
            "csv": str(MANUAL_REVIEW_CSV),
            "md": str(MANUAL_REVIEW_MD),
        },
        "category_distribution": collect_counts(kg),
        "validation": validation,
    }

    dump_json(MERGED_JSON, kg)
    dump_json(STATS_JSON, stats)
    write_report(stats)

    print(json.dumps(stats["formula"], ensure_ascii=False, indent=2))
    print("pattern_match_split", dict(pattern_counts))
    print("created_sections", created_sections)
    print("validation", {k: len(v) for k, v in validation.items()})


if __name__ == "__main__":
    main()
