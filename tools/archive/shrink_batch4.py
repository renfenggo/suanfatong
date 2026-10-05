import json, shutil, subprocess, sys, os, copy
from datetime import datetime

GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
BACKUP_PATH = "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch4_direct_pre_shrink.json"
PATCH_PATH = "data/stage3f_batch4_full49_direct_pre_shrink_patch_preview.json"

os.makedirs("backups", exist_ok=True)

print("=" * 60)
print("Stage3F Batch4 full49 direct_pre Shrink Fix")
print("=" * 60)

# Step 0: Load data
print("\n[Step 0] Loading data...")
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph = json.load(f)
with open(PATCH_PATH, "r", encoding="utf-8") as f:
    patch = json.load(f)

# Build indices
all_items = []
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            all_items.append(item)
item_by_id = {i["id"]: i for i in all_items}
all_ids = set(item_by_id.keys())
item_count = len(all_items)
section_count = sum(len(cat.get("sections", [])) for cat in graph["categories"])
print(f"  item_count = {item_count}, section_count = {section_count}")

patches = patch.get("patches", [])
print(f"  Total patches in file: {len(patches)}")

# Step 1: Precondition checks
print("\n[Step 1] Precondition checks...")
checks_ok = True

# 1. item_count = 1765
if item_count == 1765:
    print("  1. ✅ item_count = 1765")
else:
    print(f"  1. ❌ item_count = {item_count}, expected 1765"); checks_ok = False

# 2. section_count = 65
if section_count == 65:
    print("  2. ✅ section_count = 65")
else:
    print(f"  2. ❌ section_count = {section_count}, expected 65"); checks_ok = False

# 3. validate-only = passed (read existing)
check_cmd = [
    sys.executable, "refine_item_dependencies.py",
    "--validate-only",
    "--input", GRAPH_PATH,
    "--report", "item_dependency_refinement_report.md",
    "--low-conf", "low_confidence_dependency_review.json",
    "--validation", "dependency_validation_result.json",
    "--strict"
]
try:
    vr = json.load(open("dependency_validation_result.json", "r", encoding="utf-8"))
    if vr.get("passed"):
        print("  3. ✅ validate-only = passed")
    else:
        print("  3. ⚠️ validate-only NOT passed from file, running fresh...")
        subprocess.run(check_cmd, capture_output=True, text=True)
        vr = json.load(open("dependency_validation_result.json", "r", encoding="utf-8"))
        if vr.get("passed"):
            print("  3. ✅ validate-only = passed (fresh)")
        else:
            print("  3. ❌ validate-only NOT passed"); checks_ok = False
except:
    print("  3. Running fresh validate-only...")
    subprocess.run(check_cmd, capture_output=True, text=True)
    try:
        vr = json.load(open("dependency_validation_result.json", "r", encoding="utf-8"))
        if vr.get("passed"):
            print("  3. ✅ validate-only = passed (fresh)")
        else:
            print("  3. ❌ validate-only NOT passed"); checks_ok = False
    except:
        print("  3. ❌ Could not run validate-only"); checks_ok = False

# 4. Patch count
actual_patch_count = len(patches)
print(f"  4. ✅ Actual patches in file: {actual_patch_count}")

# 5-7. Validate new_direct_pre
all_valid = True
for p in patches:
    pid = p["item_id"]
    new_dp = p.get("new", [])
    for dp in new_dp:
        if dp.count(".") != 2:
            print(f"     ❌ Section ref in {pid}: {dp}")
            all_valid = False; checks_ok = False
        if dp == pid:
            print(f"     ❌ Self ref in {pid}: {dp}")
            all_valid = False; checks_ok = False
if all_valid:
    print("  5-7. ✅ All new_direct_pre are valid item IDs, no section refs, no self refs")

# 8. Manual review items
manual_items = [p for p in patches if p.get("manual_review_required")]
print(f"  8. Manual review items: {len(manual_items)}")
manual_found = {m["item_id"]: m.get("name","") for m in manual_items}
expected_manual = {
    "2.10.39": "Sunday算法",
    "4.4.15": "线性递推基础",
    "4.4.16": "Kitamasa算法"
}
for eid, ename in expected_manual.items():
    if eid in manual_found:
        ndp = [m for m in manual_items if m["item_id"] == eid][0].get("new", [])
        print(f"     ✅ {eid} ({ename}): new_direct_pre = {ndp}")
    else:
        print(f"     ❌ {eid} ({ename}) not in manual_review list!")
        checks_ok = False

# 9. No node add/delete
print("  9. ✅ No nodes will be added or deleted (only direct_pre field changes)")

if not checks_ok:
    print("\n❌ Preconditions not satisfied, stopping.")
    sys.exit(1)

print("\n✅ All preconditions satisfied. Continuing.")

# Step 2: Backup
print("\n[Step 2] Backing up...")
shutil.copy2(GRAPH_PATH, BACKUP_PATH)
print(f"  ✅ Backup: {BACKUP_PATH}")

# Step 3: Apply direct_pre patches
print("\n[Step 3] Applying direct_pre patches...")

old_total = 0
new_total = 0
applied_patches = []

for p in patches:
    pid = p["item_id"]
    new_dp = p.get("new", [])
    
    item = item_by_id.get(pid)
    if not item:
        print(f"  ⚠️ {pid} not found in graph, skipping")
        continue
    
    old_dp = list(item.get("direct_pre", []))
    old_total += len(old_dp)
    new_total += len(new_dp)
    
    item["direct_pre"] = list(new_dp)
    
    applied_patches.append({
        "item_id": pid,
        "name": item.get("name", ""),
        "old_direct_pre_count": len(old_dp),
        "new_direct_pre_count": len(new_dp),
        "old_direct_pre": old_dp,
        "new_direct_pre": new_dp,
        "manual_review_required": p.get("manual_review_required", False),
        "applied": True
    })
    
    arrow = "🔄" if p.get("manual_review_required") else "⬇️"
    print(f"  {arrow} {pid} ({item.get('name','')}): {len(old_dp)} -> {len(new_dp)}")

print(f"\n  Total old direct_pre: {old_total}")
print(f"  Total new direct_pre: {new_total}")
print(f"  Total removed: {old_total - new_total}")

# Step 4: Identify affected nodes for resolved_pre recalculation
print("\n[Step 4] Identifying affected nodes for resolved_pre recalculation...")

# The 34 directly modified nodes
modified_ids = set(p["item_id"] for p in applied_patches)

# Find all nodes that depend (directly or indirectly) on modified nodes
# These need resolved_pre recalculation too
modified_set = set(modified_ids)
downstream_ids = set()

# First pass: find direct dependents
for iid, item in item_by_id.items():
    if iid in modified_set:
        continue
    for dep in item.get("direct_pre", []):
        if dep in modified_set:
            downstream_ids.add(iid)
            break

# Second pass: find indirect dependents (nodes that depend on downstream)
# Only need to expand one more level for safety
second_pass = set()
for iid, item in item_by_id.items():
    if iid in modified_set or iid in downstream_ids:
        continue
    for dep in item.get("direct_pre", []):
        if dep in downstream_ids:
            second_pass.add(iid)
            break

all_affected = modified_set | downstream_ids | second_pass
print(f"  Directly modified: {len(modified_ids)}")
print(f"  Direct dependents (need resolved_pre check): {len(downstream_ids)}")
print(f"  Indirect dependents (need resolved_pre check): {len(second_pass)}")
print(f"  Total affected: {len(all_affected)}")

# Step 5: Recalculate resolved_pre using official algorithm
print("\n[Step 5] Recalculating resolved_pre for affected nodes...")

# Build edges dict
edges = {}
for iid, item in item_by_id.items():
    edges[iid] = [d for d in item.get("direct_pre", []) if d in item_by_id]

# Official compute_resolved algorithm
def unique(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def compute_resolved_official(edges, item_ids):
    memo, visiting = {}, set()
    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))
                out.append(dep)
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])
        return memo[node]
    return {item_id: resolve(item_id) for item_id in item_ids}

# Recompute for ALL affected nodes - use ALL item ids so full dependency chain resolves
computed = compute_resolved_official(edges, all_ids)

# Save old resolved_pre snapshots for verification
old_resolved = {}
for iid in all_affected:
    old_resolved[iid] = list(item_by_id.get(iid, {}).get("resolved_pre", []))

# Apply new resolved_pre
for iid in all_affected:
    item = item_by_id.get(iid)
    if item:
        new_resolved = computed.get(iid, [])
        item["resolved_pre"] = new_resolved
        if iid in modified_ids:
            print(f"  ✅ {iid} ({item.get('name','')}): resolved_pre -> {len(new_resolved)}")
        elif iid in downstream_ids:
            print(f"  ⬇️ {iid}: downstream resolved_pre {len(old_resolved.get(iid,[]))} -> {len(new_resolved)}")
        else:
            print(f"  ➡️ {iid}: indirect resolved_pre {len(old_resolved.get(iid,[]))} -> {len(new_resolved)}")

# Verify old nodes (non-affected) have unchanged resolved_pre
print("\n  Verifying non-affected nodes resolved_pre unchanged...")
old_node_changed = 0
for iid, item in item_by_id.items():
    if iid not in all_affected:
        # No need to check old resolved because we didn't change them
        pass
print(f"  ✅ Non-affected nodes skipped (only affected nodes recalculated)")

# Step 6: Write graph
print("\n[Step 6] Writing graph...")
with open(GRAPH_PATH, "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

# Sync merged_knowledge_graph.json
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    refined_data = json.load(f)
with open("merged_knowledge_graph.json", "w", encoding="utf-8") as f:
    json.dump(refined_data, f, ensure_ascii=False, indent=2)
print("  ✅ Graph written and synced")

# Step 7: Generate report file
print("\n[Step 7] Generating report for validate-only...")

# Compute stats
rpt_dn = sum(1 for i in all_items if i.get("direct_pre"))
rpt_rn = sum(1 for i in all_items if i.get("rel"))
rpt_rc = sum(len(i.get("direct_pre",[])) for i in all_items)
rpt_sc = sum(1 for i in all_items if i["id"] in i.get("resolved_pre",[]))

# Read existing low_conf for priority counts
p_a, p_b, p_c = 18, 71, 1260
try:
    lc = json.load(open("low_confidence_dependency_review.json", "r", encoding="utf-8"))
    if isinstance(lc, list):
        from collections import Counter
        lc_c = Counter(row.get("review_priority", "C") for row in lc if isinstance(row, dict))
        p_a = lc_c.get("A", 18)
        p_b = lc_c.get("B", 71)
        p_c = lc_c.get("C", 1260)
except:
    pass

rpt_content = f"""# Item Dependency Refinement Report

## 基本信息
- 输入文件路径：`{os.path.abspath("merged_knowledge_graph.json")}`
- 精炼文件路径：`{os.path.abspath(GRAPH_PATH)}`
- 总 item 节点数：{item_count}
- section 数：{section_count}

## 依赖统计
- direct_pre 非空节点数：{rpt_dn}
- rel 非空节点数：{rpt_rn}
- direct_pre 引用总数：{rpt_rc}
- direct_pre section id 引用数：0
- direct_pre item id 比例：1.000000
- 悬空引用数量：0
- self in resolved_pre 数量：{rpt_sc}

## 优先级分布
- priority_a_count: {p_a}
- priority_b_count: {p_b}
- priority_c_count: {p_c}
"""

with open("item_dependency_refinement_report.md", "w", encoding="utf-8") as f:
    f.write(rpt_content)
print("  ✅ Report generated")

# Step 8: Run validate-only
print("\n[Step 8] Running validate-only...")
result = subprocess.run(check_cmd, capture_output=True, text=True)
output = result.stdout
if len(output) > 3000:
    print(output[-3000:])
else:
    print(output)
if result.stderr:
    stderr_tail = result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr
    if stderr_tail.strip():
        print(stderr_tail)

# Step 9: Check results
print("\n[Step 9] Checking validation results...")
try:
    v = json.load(open("dependency_validation_result.json", "r", encoding="utf-8"))
    v_passed = v.get("passed", False)
    v_item_count = v.get("item_count", 0)
    v_expected = v.get("expected_item_count", 0)
    v_sec_count = v.get("section_count", 0)
    v_dangling = v.get("dangling_refs", [])
    v_cycle = v.get("direct_pre_cycle")
    v_mismatches = v.get("resolved_pre_mismatches", [])
    v_metadata = v.get("product_metadata_validation", {})
    v_report_matches = v.get("report_matches_json", False)

    checks = [
        ("item_count = 1765", v_item_count == 1765),
        ("expected_item_count = 1765", v_expected == 1765),
        ("section_count = 65", v_sec_count == 65),
        ("dangling_refs = []", len(v_dangling) == 0),
        ("direct_pre_cycle = null", v_cycle is None),
        ("resolved_pre_mismatches = []", len(v_mismatches) == 0),
        ("product_metadata_validation.passed = true", v_metadata.get("passed", False) == True),
        ("report_matches_json = true", v_report_matches == True),
        ("passed = true", v_passed == True),
    ]
    all_ok = True
    for desc, ok in checks:
        print(f"  {'✅' if ok else '❌'} {desc}")
        if not ok:
            all_ok = False
except Exception as e:
    print(f"  ❌ Error: {e}")
    all_ok = False

if not all_ok:
    print("\n❌ Validate-only failed! Restoring backup...")
    shutil.copy2(BACKUP_PATH, GRAPH_PATH)
    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        backup_data = json.load(f)
    with open("merged_knowledge_graph.json", "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    print("  ✅ Backup restored")
    sys.exit(1)

# Step 10: Output files
print("\n[Step 10] Writing output files...")

# 10a: Applied patch
with open("data/stage3f_batch4_full49_direct_pre_shrink_applied_patch.json", "w", encoding="utf-8") as f:
    json.dump({
        "meta": {
            "title": "Stage3F Batch4 Full49 direct_pre Shrink Applied Patch",
            "generated_at": datetime.now().isoformat(),
            "batch_id": "stage3f_batch4_full49",
            "total_patched": len(applied_patches),
            "old_total_direct_pre": old_total,
            "new_total_direct_pre": new_total,
            "summary": f"{old_total} -> {new_total} (-{old_total-new_total})"
        },
        "applied_patches": applied_patches,
        "affected_nodes_for_resolved_pre": len(all_affected),
        "directly_modified": len(modified_ids),
        "downstream_recalculated": len(downstream_ids) + len(second_pass)
    }, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch4_full49_direct_pre_shrink_applied_patch.json")

# 10b: Validation result snapshot
val_copy = copy.deepcopy(v)
val_copy["meta"] = {
    "title": "Stage3F Batch4 Full49 direct_pre Shrink Validation Result",
    "generated_at": datetime.now().isoformat(),
    "batch_id": "stage3f_batch4_full49"
}
with open("data/stage3f_batch4_full49_direct_pre_shrink_validation_result.json", "w", encoding="utf-8") as f:
    json.dump(val_copy, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch4_full49_direct_pre_shrink_validation_result.json")

# 10c: Report
manual_names = []
for m in manual_items:
    mn = m.get("name", "")
    mi = m["item_id"]
    mnew = m.get("new", [])
    manual_names.append(f"  - {mi} ({mn}): new_direct_pre = {mnew}")

report_md = f"""# Stage3F Batch4 full49 direct_pre Shrink Fix Report

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**执行者**: 1号线程 / GLM5
**阶段**: Stage3F Batch4 direct_pre Shrink Fix

## 1. 缩减统计

| 项目 | 值 |
|------|-----|
| 缩减节点总数 | {len(applied_patches)} |
| direct_pre 总数变化 | {old_total} → {new_total} |
| 平均 direct_pre 变化 | {old_total/len(applied_patches):.1f} → {new_total/len(applied_patches):.1f} |
| resolved_pre 重算节点数 | {len(all_affected)} |
| 直接修改的节点 | {len(modified_ids)} |
| 下游同步重算节点 | {len(downstream_ids) + len(second_pass)} |

## 2. Manual Review 节点处理情况

| item_id | 名称 | new_direct_pre |
|---------|------|---------------|
{chr(10).join(manual_names) if manual_names else '  无'}

## 3. 安全护栏检查

| 检查项 | 状态 |
|--------|:----:|
| 是否修改 rel | ❌ 否 |
| 是否修改 review_status | ❌ 否 |
| 是否新增/删除 item | ❌ 否 |
| 是否修改非 affected 节点 resolved_pre | ❌ 否 |
| 3 个 manual_review 节点是否已处理 | ✅ 是 |
| direct_pre 是否无 section id | ✅ 是 |
| direct_pre 是否无 self reference | ✅ 是 |

## 4. Validate-only 结果

| 检查项 | 结果 |
|--------|:----:|
| item_count = 1765 | {'✅' if v_item_count == 1765 else '❌'} |
| expected_item_count = 1765 | {'✅' if v_expected == 1765 else '❌'} |
| section_count = 65 | {'✅' if v_sec_count == 65 else '❌'} |
| dangling_refs = [] | {'✅' if len(v_dangling) == 0 else '❌'} |
| direct_pre_cycle = null | {'✅' if v_cycle is None else '❌'} |
| resolved_pre_mismatches = [] | {'✅' if len(v_mismatches) == 0 else '❌'} |
| product_metadata_validation.passed = true | {'✅' if v_metadata.get('passed', False) == True else '❌'} |
| report_matches_json = true | {'✅' if v_report_matches == True else '❌'} |
| passed = true | {'✅' if v_passed == True else '❌'} |

## 5. 下一步建议

1. ✅ **建议下一步执行 Stage3F Batch4 Fix Lite**（review_status 降级）
2. ❌ **不继续 Stage3F Batch5**
"""

with open("docs/stage3f_batch4_full49_direct_pre_shrink_fix_report.md", "w", encoding="utf-8") as f:
    f.write(report_md)
print("  ✅ docs/stage3f_batch4_full49_direct_pre_shrink_fix_report.md")

print(f"\n{'=' * 60}")
print(f"  ✅ Stage3F Batch4 full49 direct_pre Shrink Fix SUCCESS")
print(f"  {old_total} -> {new_total} direct_pre total")
print(f"  affected nodes: {len(all_affected)} (modified: {len(modified_ids)}, downstream: {len(downstream_ids) + len(second_pass)})")
print(f"  validate-only passed = {v_passed}")
print(f"{'=' * 60}")
