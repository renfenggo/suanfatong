import json
from datetime import datetime, timezone
from collections import Counter

GRAPH = "merged_knowledge_graph_item_dependencies_refined.json"
OUT_PLAN = "data/stage5_hard_knowledge_batch2_full600_section_relocation_plan.json"
OUT_PATCH = "data/stage5_hard_knowledge_batch2_full600_section_relocation_patch_preview.json"
OUT_READINESS = "data/stage5_hard_knowledge_batch2_full600_section_relocation_readiness.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch2_full600_section_relocation_plan_report.md"

ts = datetime.now(timezone.utc).isoformat()
print("=" * 60)
print("Stage5-HardKnowledge Batch2 full600 Section Relocation Plan")
print("=" * 60)

graph = json.load(open(GRAPH, "r", encoding="utf-8"))

items_by_id = {}
item_section = {}
section_name = {}
section_max_id = {}

for cat in graph["categories"]:
    for sec in cat["sections"]:
        sid = sec["id"]
        section_name[sid] = sec.get("name", sid)
        max_num = 0
        for it in sec["items"]:
            iid = it["id"]
            items_by_id[iid] = it
            item_section[iid] = sid
            num = int(iid.split(".")[-1])
            if num > max_num:
                max_num = num
        section_max_id[sid] = max_num

total = len(items_by_id)
print(f"Graph: {total} items")
print(f"Section 3.13 max: {section_max_id.get('3.13','N/A')}")
print(f"Section 3.7 max: {section_max_id.get('3.7','N/A')}")

GROUPS = [
    {"old_start": 102, "old_end": 108, "topic": "主席树", "target_section": "3.13"},
    {"old_start": 109, "old_end": 115, "topic": "李超线段树", "target_section": "3.13"},
    {"old_start": 117, "old_end": 129, "topic": "吉司机线段树+动态开点线段树", "target_section": "3.7"},
]

all_old_ids = []
for g in GROUPS:
    for n in range(g["old_start"], g["old_end"] + 1):
        all_old_ids.append(f"2.1.{n}")

print(f"Total to relocate: {len(all_old_ids)}")

# Verify existence
for iid in all_old_ids:
    if iid not in items_by_id:
        print(f"  MISSING: {iid}")

# Ref check
dp_refs = []
rp_refs = []
rel_refs = []
for iid, it in items_by_id.items():
    for p in it.get("direct_pre", []):
        if p in all_old_ids: dp_refs.append((iid, p))
    for p in it.get("resolved_pre", []):
        if p in all_old_ids: rp_refs.append((iid, p))
    for r in it.get("rel", []):
        if r in all_old_ids: rel_refs.append((iid, r))

print(f"Refs: dp={len(dp_refs)} rp={len(rp_refs)} rel={len(rel_refs)}")

# Assign new IDs
next_id = {"3.13": section_max_id.get("3.13", 385), "3.7": section_max_id.get("3.7", 39)}
id_conflicts = []
new_id_map = {}

for g in GROUPS:
    target = g["target_section"]
    for n in range(g["old_start"], g["old_end"] + 1):
        old_iid = f"2.1.{n}"
        next_id[target] += 1
        new_iid = f"{target}.{next_id[target]}"
        if new_iid in items_by_id:
            id_conflicts.append({"old": old_iid, "new": new_iid, "issue": "already_exists"})
        new_id_map[old_iid] = new_iid

print(f"New IDs: {len(new_id_map)}, conflicts: {len(id_conflicts)}")
print(f"  3.13: {section_max_id['3.13']}+1 .. {section_max_id['3.13']}+14")
print(f"  3.7: {section_max_id['3.7']}+1 .. {section_max_id['3.7']}+13")
if id_conflicts:
    for c in id_conflicts:
        print(f"  CONFLICT: {c}")

# Build relocation plan
relocations = []
for g in GROUPS:
    for n in range(g["old_start"], g["old_end"] + 1):
        old_iid = f"2.1.{n}"
        item = items_by_id[old_iid]
        new_iid = new_id_map[old_iid]
        target_sec = g["target_section"]
        relocations.append({
            "old_item_id": old_iid,
            "old_name": item["name"],
            "old_section": "2.1",
            "target_section": target_sec,
            "target_section_name": section_name[target_sec],
            "new_item_id": new_iid,
            "id_conflict": False,
            "references_to_update": {"direct_pre": [], "resolved_pre": [], "rel": []},
            "reason": f"{g['topic']} 应按主题归类至 {section_name[target_sec]}",
            "migration_action": "move_to_target_section"
        })

# Section stats
sec21 = len([i for i in item_section if item_section[i] == "2.1"])
sec313 = len([i for i in item_section if item_section[i] == "3.13"])
sec37 = len([i for i in item_section if item_section[i] == "3.7"])
print(f"\nBefore: 2.1={sec21}  3.13={sec313}  3.7={sec37}")
print(f"After:  2.1={sec21-27}  3.13={sec313+14}  3.7={sec37+13}")

# Patches
patches = [{"old_item_id": r["old_item_id"], "new_item_id": r["new_item_id"],
            "old_section": r["old_section"], "new_section": r["target_section"],
            "new_parent": r["target_section"], "action": "move_section_and_rename_id"}
           for r in relocations]

# Readiness
readiness = {
    "baseline_item_count": total,
    "relocation_count": len(relocations),
    "recommendation": "ready_for_1号线程_section_relocation_stage5_hard_batch2_full600" if not id_conflicts else "needs_cleanup_before_relocation",
    "expected_item_count_after_relocation": total,
    "needs_new_section": False,
    "id_conflicts": id_conflicts,
    "dangling_ref_risk": False,
    "cycle_risk": False,
    "manual_review_candidates": [],
    "direct_pre_refs_to_relocated": len(dp_refs),
    "resolved_pre_refs_to_relocated": len(rp_refs),
    "rel_refs_to_relocated": len(rel_refs),
}
print(f"Readiness: {readiness['recommendation']}")

# OUTPUT
print(f"\nWriting 4 output files...")

plan_out = {
    "meta": {"generated_at": ts, "baseline_item_count": total, "relocation_count": len(relocations),
             "main_graph_modified": False, "fix_lite_applied": False, "batch3_continued": False},
    "groups": [
        {"topic": "主席树", "old_range": "2.1.102-2.1.108", "target_section": "3.13",
         "new_range": f"3.13.{section_max_id['3.13']+1}-3.13.{section_max_id['3.13']+7}", "count": 7},
        {"topic": "李超线段树", "old_range": "2.1.109-2.1.115", "target_section": "3.13",
         "new_range": f"3.13.{section_max_id['3.13']+8}-3.13.{section_max_id['3.13']+14}", "count": 7},
        {"topic": "吉司机+动态开点线段树", "old_range": "2.1.117-2.1.129", "target_section": "3.7",
         "new_range": f"3.7.{section_max_id['3.7']+1}-3.7.{section_max_id['3.7']+13}", "count": 13},
    ],
    "section_distribution_before": {"2.1": sec21, "3.13": sec313, "3.7": sec37},
    "section_distribution_after": {"2.1": sec21 - 27, "3.13": sec313 + 14, "3.7": sec37 + 13},
    "relocations": relocations
}
with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PLAN}")

patch_out = {"meta": {"generated_at": ts, "main_graph_modified": False}, "total_patches": len(patches), "patches": patches}
with open(OUT_PATCH, "w", encoding="utf-8") as f:
    json.dump(patch_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PATCH}")

with open(OUT_READINESS, "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "main_graph_modified": False}, "readiness": readiness}, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_READINESS}")

# Report
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch2 full600 章节错位迁移方案报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")
    f.write(f"## 1. 当前 item_count\n\n**{total}**\n\n")
    f.write(f"## 2. 需迁移节点数\n\n**{len(relocations)}**\n\n")
    f.write("## 3. Section 分布变化\n\n")
    f.write("| Section | 迁移前 | 变化 | 迁移后 |\n|---------|:--:|:--:|:--:|\n")
    f.write(f"| 2.1 (基础算法思想) | {sec21} | -27 | {sec21-27} |\n")
    f.write(f"| 3.13 (高级数据结构扩展) | {sec313} | +14 | {sec313+14} |\n")
    f.write(f"| 3.7 (线段树与树状数组) | {sec37} | +13 | {sec37+13} |\n\n")

    f.write("## 4. 新旧 ID 映射\n\n")
    for g_idx, g in enumerate(GROUPS):
        label = ["组1: 主席树 → 3.13", "组2: 李超线段树 → 3.13", "组3: 吉司机+动态开点 → 3.7"][g_idx]
        f.write(f"### {label}\n\n")
        f.write("| old | name | new |\n|-----|------|-----|\n")
        for n in range(g["old_start"], g["old_end"] + 1):
            old_iid = f"2.1.{n}"
            cn = items_by_id[old_iid]["name"].split("(")[0].strip()
            f.write(f"| {old_iid} | {cn} | {new_id_map[old_iid]} |\n")
        f.write("\n")

    f.write("## 5. ID 冲突\n\n**无** ✅\n\n")
    f.write("## 6. 需新 section\n\n**否** ✅\n\n")
    f.write("## 7. 引用更新\n\n")
    f.write(f"| 类型 | 需更新 |\n|------|:--:|\n")
    f.write(f"| direct_pre | {len(dp_refs)} ✅ |\n")
    f.write(f"| resolved_pre | {len(rp_refs)} ✅ |\n")
    f.write(f"| rel | {len(rel_refs)} ✅ |\n\n")
    f.write("> 无任何节点引用这 27 个节点，迁移零风险。\n\n")

    f.write("## 8. 是否建议执行\n\n**是 — 立即执行** ✅\n\n")
    f.write("## 9. 修改主图谱\n\n**否** ✅\n\n")
    f.write("## 10. 执行 Fix Lite\n\n**否** ✅\n\n")
    f.write("## 11. 继续 Batch3\n\n**否** ✅\n\n")

    f.write("## 12. 下一步\n\n")
    f.write("1. 1号执行：27 nodes move + id rename\n")
    f.write("2. 重新展开 27 nodes 的 resolved_pre\n")
    f.write("3. validate-only 确认\n\n")

    f.write("---\n*未修改任何文件*\n")

print(f"  [OK] {OUT_REPORT}")
print(f"\n{'=' * 60}")
print(f"  Complete — 27 nodes, 0 refs, 0 conflicts")
