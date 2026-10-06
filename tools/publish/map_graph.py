# -*- coding: utf-8 -*-
"""图谱 publish mapper + validator（ADR-004）。

职责：
1. map：refined（Draft 源，global schema）-> io_v4_4（Publish 产物，App schema）
   的字段映射集中在此一处；业务代码/生产脚本禁止自行猜字段。
2. validate：节点数守恒 / ID 唯一 / 引用存在 / 依赖无环；不过不得发布。
3. verify：mapper 输出与现有 Publish 产物语义 diff（深度相等，键顺序无关）。

映射规则（由 tools/archive/inspect_*.py 侦查固化，全部经过 3240 节点验证）：
- item 全局丢弃字段：subcategory/quality_score/candidate_id/source_tier/
  category/need_manual_review（Draft 管线评审元数据，不入 Publish）
- stage5 批次（refined 有 source_tier 标记者）额外丢弃：
  review_status/platform_tags/difficulty/review_priority
- 补全：merge_type 缺 -> stage5 批次 "new_knowledge"，否则 "stage3g_full400"；
  parent 缺 -> id 去掉最后一段；alias 缺 -> aliases 非空取之，否则 [name]；
  aliases/source/docx_ids 缺 -> []；level 缺 -> graph_overrides.level_overrides；
  pickup_group/block_id 缺 -> ""；pickup_order 缺 -> 0
- meta：丢弃 stage5_hard_batch1_* 过程键；按 overrides.meta_patch 增/改
- section：仅保留 id/name/level/pre/rel/items
- level 例外（475 条 stage5_hard_batch1 评估值）与 meta sync 信息：
  Publish 独有、Draft 无源，显式固化于 graph_overrides.json

用法：
  python tools/publish/map_graph.py --verify   # 验收：与现 io_v4_4 语义 diff
  python tools/publish/map_graph.py --write    # 发布：重写 io_v4_4.json
"""
import argparse
import json
import sys

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
PUBLISH = r"assets/data/knowledge/io_v4_4.json"
OVERRIDES = r"tools/publish/graph_overrides.json"

META_DROP_PREFIX = "stage5_hard_batch1_"

ITEM_DROP_FIELDS = {
    "subcategory", "quality_score", "candidate_id", "source_tier",
    "category", "need_manual_review",
}
STAGE5_DROP_FIELDS = {
    "review_status", "platform_tags", "difficulty", "review_priority",
}
STAGE5_MARK = "source_tier"

SECTION_KEEP_FIELDS = ["id", "name", "level", "pre", "rel", "items"]

# canonical 键序（语义 diff 与键序无关；仅保证输出确定性）
ITEM_KEY_ORDER = [
    "id", "name", "direct_pre", "resolved_pre", "rel", "level", "aliases",
    "en_name", "global_aliases", "tracks", "audience", "visibility",
    "learning_path_policy", "localization_status", "content_status",
    "review_status", "platform_tags", "alias", "parent", "source",
    "docx_ids", "merge_type", "exact_match_reason", "mapping_reason",
    "parent_concept", "mapping_score", "review_note", "review_priority",
    "difficulty", "block_id", "block_name", "pickup_group",
    "pickup_group_name", "pickup_order", "resource_block_id",
    "resource_block_name", "source_candidate_id", "reason_to_add",
    "global_relevance", "i18n_seed", "stage3b_fix", "stage3c_fix",
    "stage3d_whitelist_rank", "stage3d_fix", "stage3e_batch",
    "stage3e_risk_band", "stage3e_rank_in_batch", "unlock_mode",
    "stage3e_candidate_id", "relocated_from",
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def map_meta(meta, overrides):
    out = {}
    for k, v in meta.items():
        if k.startswith(META_DROP_PREFIX):
            continue
        out[k] = v
    patch = overrides.get("meta_patch", {})
    for k, v in patch.get("add", {}).items():
        out[k] = v
    for k, v in patch.get("set", {}).items():
        out[k] = v
    return out


def map_section(section):
    out = {}
    for k in SECTION_KEEP_FIELDS:
        if k in section:
            out[k] = section[k]
    return out


def map_item(item, level_overrides, pickup_overrides):
    is_stage5 = STAGE5_MARK in item
    out = dict(item)
    for f in ITEM_DROP_FIELDS:
        out.pop(f, None)
    if is_stage5:
        for f in STAGE5_DROP_FIELDS:
            out.pop(f, None)

    iid = out["id"]
    if "merge_type" not in out:
        out["merge_type"] = "new_knowledge" if is_stage5 else "stage3g_full400"
    if "parent" not in out:
        out["parent"] = iid.rsplit(".", 1)[0] if "." in iid else ""
    if "alias" not in out:
        aliases = out.get("aliases") or []
        out["alias"] = aliases if aliases else [out["name"]]
    if "aliases" not in out:
        out["aliases"] = []
    if "source" not in out:
        out["source"] = []
    if "docx_ids" not in out:
        out["docx_ids"] = []
    if "level" not in out:
        if iid not in level_overrides:
            raise SystemExit(f"[MAP FAIL] {iid} 缺 level 且无 overrides 条目")
        out["level"] = level_overrides[iid]
    # pickup 三件套为稀疏字段（仅 ~605 个 item 持有），只按显式补丁补全
    for f, v in pickup_overrides.get(iid, {}).items():
        if f not in out:
            out[f] = v

    unknown = set(out) - set(ITEM_KEY_ORDER)
    if unknown:
        raise SystemExit(
            f"[MAP FAIL] {iid} 存在未知字段（白名单外）: {sorted(unknown)}"
        )
    return {k: out[k] for k in ITEM_KEY_ORDER if k in out}


def map_graph(refined, overrides):
    level_overrides = overrides.get("level_overrides", {})
    pickup_overrides = overrides.get("pickup_overrides", {})
    categories = []
    for cat in refined["categories"]:
        sections = [map_section(s) for s in cat.get("sections", [])]
        for s in sections:
            s["items"] = [
                map_item(i, level_overrides, pickup_overrides)
                for i in s.get("items", [])
            ]
        categories.append({"name": cat["name"], "sections": sections})
    return {
        "meta": map_meta(refined.get("meta", {}), overrides),
        "categories": categories,
    }


def validate(doc, expected_count=None):
    errors = []
    sections = {}
    items = {}
    for cat in doc["categories"]:
        for s in cat["sections"]:
            if s["id"] in sections:
                errors.append(f"section id 重复: {s['id']}")
            sections[s["id"]] = s
            for i in s["items"]:
                if i["id"] in items:
                    errors.append(f"item id 重复: {i['id']}")
                items[i["id"]] = i

    if expected_count is not None and len(items) != expected_count:
        errors.append(f"节点数不守恒: {len(items)} != {expected_count}")

    known = set(sections) | set(items)
    for iid, i in items.items():
        if i["parent"] and i["parent"] not in sections:
            errors.append(f"{iid} parent 不存在: {i['parent']}")
        for ref in i["direct_pre"] + i["resolved_pre"] + i["rel"]:
            if ref not in known:
                errors.append(f"{iid} 引用不存在: {ref}")

    # 依赖无环（DFS）
    adjacency = {
        iid: [r for r in i["resolved_pre"] if r in items]
        for iid, i in items.items()
    }
    visited, in_stack = set(), set()

    def dfs(node):
        visited.add(node)
        in_stack.add(node)
        for nxt in adjacency[node]:
            if nxt not in visited:
                if dfs(nxt):
                    return True
            elif nxt in in_stack:
                errors.append(f"依赖环: {node} -> {nxt}")
                return True
        in_stack.remove(node)
        return False

    for iid in items:
        if iid not in visited and dfs(iid):
            break

    return errors


def semantic_diff(a, b, path="$", limit=10):
    """深度语义 diff（键顺序无关），返回差异清单（截断到 limit）。"""
    diffs = []

    def walk(x, y, p):
        if len(diffs) >= limit:
            return
        if type(x) is not type(y):
            diffs.append(f"{p}: 类型 {type(x).__name__} != {type(y).__name__}")
            return
        if isinstance(x, dict):
            for k in x.keys() - y.keys():
                diffs.append(f"{p}.{k}: 仅左侧存在")
            for k in y.keys() - x.keys():
                diffs.append(f"{p}.{k}: 仅右侧存在")
            for k in x.keys() & y.keys():
                walk(x[k], y[k], f"{p}.{k}")
        elif isinstance(x, list):
            if len(x) != len(y):
                diffs.append(f"{p}: 长度 {len(x)} != {len(y)}")
            for idx, (xe, ye) in enumerate(zip(x, y)):
                walk(xe, ye, f"{p}[{idx}]")
        elif x != y:
            diffs.append(f"{p}: {x!r} != {y!r}")

    walk(a, b, path)
    return diffs


def dump(doc, path):
    text = json.dumps(doc, ensure_ascii=False, indent=2)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text + "\r\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true",
                        help="与现有 Publish 产物语义 diff（验收模式）")
    parser.add_argument("--write", action="store_true",
                        help="重写 Publish 产物 io_v4_4.json")
    args = parser.parse_args()

    refined = load(REFINED)
    overrides = load(OVERRIDES)
    mapped = map_graph(refined, overrides)

    src_count = sum(
        len(s.get("items", []))
        for c in refined["categories"] for s in c.get("sections", [])
    )
    errors = validate(mapped, expected_count=src_count)
    if errors:
        print(f"[VALIDATE FAIL] {len(errors)} 处错误：")
        for e in errors[:20]:
            print("  -", e)
        sys.exit(1)
    out_count = sum(
        len(s["items"]) for c in mapped["categories"] for s in c["sections"]
    )
    print(f"[VALIDATE OK] 节点 {out_count} 守恒 / ID 唯一 / 引用完整 / 无环")

    if args.verify:
        publish = load(PUBLISH)
        diffs = semantic_diff(mapped, publish, limit=20)
        if diffs:
            print(f"[VERIFY FAIL] 与现 io_v4_4 语义差异 {len(diffs)}+ 处：")
            for d in diffs:
                print("  -", d)
            sys.exit(1)
        print("[VERIFY OK] mapper 输出与现 io_v4_4 语义 diff = 0")
        return

    if args.write:
        dump(mapped, PUBLISH)
        print(f"[WRITE OK] -> {PUBLISH}")
        return

    print("[DRY RUN] 未指定 --verify/--write，仅校验。")


if __name__ == "__main__":
    main()
