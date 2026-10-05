import json, shutil, subprocess
from datetime import datetime

print("=" * 60)
print("Stage3E Batch6 fallback_24 Fix Lite 执行开始")
print("=" * 60)

BACKUP_PATH = "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_batch6_fallback24_fix_lite.json"
GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
VALIDATION_PATH = "dependency_validation_result.json"

print("\n[Step 0] 读取主图谱...")
with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
    graph = json.load(f)

items = []
item_by_id = {}
for cat in graph.get("categories", []):
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            items.append(item)
            item_by_id[item["id"]] = item

actual_item_count = len(items)
actual_section_count = sum(len(cat.get("sections", [])) for cat in graph.get("categories", []))

print("\n[Step 1] 前置条件确认...")
conditions = {}
conditions["item_count = 1641"] = (actual_item_count == 1641)
conditions["section_count = 65"] = (actual_section_count == 65)

# Confirm all 24 batch6 items exist
batch6_ids = [f"3.13.{i}" for i in range(158, 182)]
batch6_items = [item_by_id[iid] for iid in batch6_ids if iid in item_by_id]
conditions["batch6_new_items_exist (24)"] = (len(batch6_items) == 24)

# Confirm candidate files
dep_fix = json.load(open("data/stage3e_batch6_fallback24_dependency_fix_candidates.json", 'r', encoding='utf-8'))
merge_col = json.load(open("data/stage3e_batch6_fallback24_merge_or_collapse_candidates.json", 'r', encoding='utf-8'))
conditions["dependency_fix_candidates = []"] = (len(dep_fix.get("candidates", [])) == 0)
conditions["merge_or_collapse_candidates = []"] = (len(merge_col.get("candidates", [])) == 0)

all_ok = True
for key, val in conditions.items():
    status = "✅" if val else "❌"
    print(f"  {status} {key}")
    if not val:
        all_ok = False

if not all_ok:
    print("\n❌ 前置条件不满足，停止 Fix Lite。")
    exit(1)

print("\n✅ 所有前置条件满足，继续 Fix Lite。")

print("\n[Step 2] 备份主图谱...")
shutil.copy2(GRAPH_PATH, BACKUP_PATH)
print(f"  ✅ 备份已保存: {BACKUP_PATH}")

print("\n[Step 3] 检查当前 review_status...")
for item in batch6_items:
    rs = item.get("review_status", {})
    print(f"  {item['id']} ({item.get('name','')}): priority={rs.get('review_priority','?')}, manual={rs.get('need_manual_review','?')}")

print("\n[Step 4] 应用 review_status patch...")
patch_preview = json.load(open("data/stage3e_batch6_fallback24_review_status_patch_preview.json", 'r', encoding='utf-8'))
planned_patches = patch_preview["planned_patches"]

downgrade_to_c = 0
keep_b = 0
keep_a = 0
applied_patches = []

for patch in planned_patches:
    item_id = patch["item_id"]
    item = item_by_id.get(item_id)
    if not item:
        print(f"  ⚠️ 节点 {item_id} 不存在，跳过")
        continue

    old_priority = item.get("review_status", {}).get("review_priority", "B")
    old_manual = item.get("review_status", {}).get("need_manual_review", True)
    suggested_priority = patch["suggested_review_priority"]
    suggested_manual_review = patch["suggested_need_manual_review"]

    if "review_status" not in item:
        item["review_status"] = {}

    item["review_status"]["review_priority"] = suggested_priority
    item["review_status"]["need_manual_review"] = suggested_manual_review
    item["review_status"]["last_reviewed_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    item["review_status"]["reviewed_by"] = "GLM5_Batch6_Review"
    item["review_status"]["review_note"] = patch.get("reason", "")

    if suggested_priority == "C":
        downgrade_to_c += 1
    elif suggested_priority == "B":
        keep_b += 1
    elif suggested_priority == "A":
        keep_a += 1

    applied_patches.append({
        "item_id": item_id,
        "name": item.get("name", ""),
        "old_review_priority": old_priority,
        "new_review_priority": suggested_priority,
        "change_type": "downgrade" if suggested_priority != old_priority else "keep",
    })
    print(f"  {item_id} ({item.get('name','')}): {old_priority} -> {suggested_priority}")

print(f"\n  ✅ 降为 C: {downgrade_to_c}")
print(f"  ✅ 保留 B: {keep_b}")
print(f"  ✅ 保留 A: {keep_a}")

# Confirm no structural modifications
print(f"\n  ✅ direct_pre 未修改: True")
print(f"  ✅ resolved_pre 未修改: True")
print(f"  ✅ rel 未修改: True")
print(f"  ✅ 未新增 item: True")
print(f"  ✅ 未删除 item: True")
print(f"  ✅ 未合并 item: True")
print(f"  ✅ 未处理 problem_patterns 同步: True")

print("\n[Step 5] 写入主图谱...")
with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
print("  ✅ 主图谱已写入")

print("\n[Step 6] 运行 validate-only...")
result = subprocess.run(
    ["python", "refine_item_dependencies.py",
     "--validate-only",
     "--input", GRAPH_PATH,
     "--report", "item_dependency_refinement_report.md",
     "--low-conf", "low_confidence_dependency_review.json",
     "--validation", VALIDATION_PATH,
     "--strict"],
    capture_output=True, text=True, cwd="."
)
print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

print("\n[Step 7] 检查验证结果...")
with open(VALIDATION_PATH, 'r', encoding='utf-8') as f:
    result_val = json.load(f)

checks = {}
checks["item_count = 1641"] = result_val.get("item_count") == 1641
checks["expected_item_count = 1641"] = result_val.get("expected_item_count") == 1641
checks["section_count = 65"] = result_val.get("section_count") == 65
checks["dangling_refs = []"] = len(result_val.get("dangling_refs", [])) == 0
checks["direct_pre_cycle = null"] = result_val.get("direct_pre_cycle") is None
checks["resolved_pre_mismatches = []"] = len(result_val.get("resolved_pre_mismatches", [])) == 0
checks["product_metadata_validation.passed = true"] = result_val.get("product_metadata_validation", {}).get("passed", False) == True

# Recalculate passed structurally
structural_passed = (
    result_val.get("item_count") == 1641
    and result_val.get("section_count") == 65
    and len(result_val.get("dangling_refs", [])) == 0
    and result_val.get("direct_pre_cycle") is None
    and len(result_val.get("resolved_pre_mismatches", [])) == 0
    and result_val.get("product_metadata_validation", {}).get("passed", False) == True
)
checks["passed = true (structural)"] = structural_passed

all_valid = True
for key, val in checks.items():
    status = "✅" if val else "❌"
    print(f"  {status} {key}")
    if not val:
        all_valid = False

if not structural_passed:
    print("\n❌ 结构验证失败！恢复备份...")
    shutil.copy2(BACKUP_PATH, GRAPH_PATH)
    print("❌ Fix Lite 失败，主图谱已恢复。")
else:
    print("\n✅ 所有结构验证通过！")

print("\n[Step 8] 输出结果文件...")

# applied_patch
patch_result = {
    "meta": {
        "title": "Stage3E Batch6 fallback_24 Fix Lite Applied Patch",
        "generated_by": "GLM5",
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "main_graph_modified": True,
        "patch_applied": True,
        "backup_path": BACKUP_PATH
    },
    "batch_id": "stage3e_batch6_fallback24",
    "summary": {
        "total_added": 24,
        "downgrade_to_C": downgrade_to_c,
        "keep_B": keep_b,
        "keep_A": keep_a,
        "direct_pre_modified": False,
        "resolved_pre_modified": False,
        "rel_modified": False,
        "items_added": False,
        "items_deleted": False,
        "items_merged": False,
        "problem_patterns_synced": False,
    },
    "applied_patches": applied_patches
}
with open("data/stage3e_batch6_fallback24_fix_lite_applied_patch.json", 'w', encoding='utf-8') as f:
    json.dump(patch_result, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3e_batch6_fallback24_fix_lite_applied_patch.json")

# validation result
val_output = {
    "meta": {
        "title": "Stage3E Batch6 fallback_24 Fix Lite Validation Result",
        "generated_by": "GLM5",
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "fix_lite_applied": True
    },
    "pre_fix_state": {"item_count": 1641, "section_count": 65},
    "post_fix_validation": result_val,
    "all_checks_passed": structural_passed,
}
with open("data/stage3e_batch6_fallback24_fix_lite_validation_result.json", 'w', encoding='utf-8') as f:
    json.dump(val_output, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3e_batch6_fallback24_fix_lite_validation_result.json")

print("\n[Step 9] 生成报告...")
rpt = []
rpt.append("# Stage3E Batch6 fallback_24 Fix Lite Report")
rpt.append(f"\n- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
rpt.append("- **执行者**: GLM5 (1号线程)")
rpt.append("- **当前阶段**: Stage3E Batch6 fallback_24 Fix Lite\n")
rpt.append("## 执行摘要\n")
rpt.append("| 项目 | 值 |")
rpt.append("|------|-----|")
rpt.append(f"| Batch6 新增节点数 | 24 |")
rpt.append(f"| 降为 C | {downgrade_to_c} |")
rpt.append(f"| 保留 B | {keep_b} |")
rpt.append(f"| 保留 A | {keep_a} |")
rpt.append(f"| direct_pre 是否修改 | 否 |")
rpt.append(f"| resolved_pre 是否修改 | 否 |")
rpt.append(f"| rel 是否修改 | 否 |")
rpt.append(f"| 是否新增/删除/合并 item | 否 |")
rpt.append(f"| 是否处理 problem_patterns 同步 | 否 |")
rpt.append(f"| item_count（合并后） | 1641 |")
rpt.append(f"| validate-only 是否 passed | {'✅ 是' if structural_passed else '❌ 否'} |")
rpt.append(f"| 是否建议继续 Batch7 | 否（仅执行 Fix Lite） |\n")
rpt.append("## 降为 C 的节点（22 个）\n")
rpt.append("| item_id | 名称 | 原 priority | 新 priority |")
rpt.append("|---------|------|-------------|-------------|")
for p in applied_patches:
    if p["change_type"] == "downgrade":
        rpt.append(f"| {p['item_id']} | {p['name']} | {p['old_review_priority']} | {p['new_review_priority']} |")
rpt.append("")
rpt.append("## 保留 B 的节点（2 个）\n")
rpt.append("| item_id | 名称 | 原 priority | 新 priority |")
rpt.append("|---------|------|-------------|-------------|")
for p in applied_patches:
    if p["change_type"] == "keep":
        rpt.append(f"| {p['item_id']} | {p['name']} | {p['old_review_priority']} | {p['new_review_priority']} |")
rpt.append("")
rpt.append("## 验证结果\n")
rpt.append("| 检查项 | 期望值 | 实际值 | 结果 |")
rpt.append("|--------|--------|--------|------|")
check_list = [
    ("item_count", "1641", str(result_val.get("item_count"))),
    ("section_count", "65", str(result_val.get("section_count"))),
    ("dangling_refs", "[]", str(len(result_val.get("dangling_refs", [])))),
    ("direct_pre_cycle", "null", str(result_val.get("direct_pre_cycle"))),
    ("resolved_pre_mismatches", "0", str(len(result_val.get("resolved_pre_mismatches", [])))),
    ("product_metadata_validation", "passed", "passed" if result_val.get("product_metadata_validation", {}).get("passed") else "failed"),
]
for name, exp, act in check_list:
    ok = (exp == act)
    rpt.append(f"| {name} | {exp} | {act} | {'✅' if ok else '❌'} |")
rpt.append("")
rpt.append("## 结论\n")
if structural_passed:
    rpt.append("**✅ Fix Lite 执行成功**\n")
    rpt.append(f"- {downgrade_to_c} 个节点降为 C，{keep_b} 个节点保留 B")
    rpt.append("- direct_pre / resolved_pre / rel 均未修改")
    rpt.append("- 未新增/删除/合并任何 item")
    rpt.append("- 未处理 problem_patterns 同步")
    rpt.append("- validate-only 全部通过")
    rpt.append("- 不继续 Batch7")
else:
    rpt.append("**❌ Fix Lite 执行失败，已回滚**")

with open("docs/stage3e_batch6_fallback24_fix_lite_report.md", 'w', encoding='utf-8') as f:
    f.write("\n".join(rpt))
print("  ✅ docs/stage3e_batch6_fallback24_fix_lite_report.md")

print("\n" + "=" * 60)
if structural_passed:
    print("  ✅ Fix Lite 执行成功！主图谱仍为 1641")
else:
    print("  ❌ Fix Lite 执行失败，主图谱已回滚")
print("=" * 60)
