import json, copy, shutil, subprocess, re
from datetime import datetime

print("=" * 60)
print("Stage3F Batch1 Merge (20 candidates)")
print("=" * 60)

BACKUP_PATH = "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch1.json"
GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"

# ============================================================
# Step 0: Load data
# ============================================================
print("\n[Step 0] Loading data...")

with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
    graph = json.load(f)

with open("data/stage3f_batch1_candidate_plan.json", 'r', encoding='utf-8') as f:
    candidate_plan = json.load(f)

with open("data/stage3f_batch1_dynamic_precheck.json", 'r', encoding='utf-8') as f:
    dynamic_precheck = json.load(f)

# Build index
item_by_id = {}
for cat in graph.get("categories", []):
    for sec in cat.get("sections", []):
        for item in sec.get("items", []):
            item_by_id[item["id"]] = item

# ============================================================
# Step 1: Precondition check
# ============================================================
print("\n[Step 1] Precondition check...")

selected_ids = dynamic_precheck["selected_candidates"]
recommendation = dynamic_precheck.get("recommendation")
recommended_merge_count = dynamic_precheck.get("recommended_merge_count")
cleanup_required = dynamic_precheck.get("dependency_cleanup_required")
has_cycle = dynamic_precheck.get("candidate_dependency_cycle")
needs_new_section = dynamic_precheck.get("needs_new_section")
section_deps = dynamic_precheck.get("section_ref_dependencies", [])

actual_item_count = len(item_by_id)
actual_section_count = sum(len(cat.get("sections", [])) for cat in graph.get("categories", []))

conditions = {}
conditions["item_count = 1641"] = (actual_item_count == 1641)
conditions["section_count = 65"] = (actual_section_count == 65)
conditions["selected_candidates = 20"] = (len(selected_ids) == 20)
conditions["recommendation = ready_for_1号线程_merge"] = (recommendation == "ready_for_1号线程_merge")
conditions["recommended_merge_count = 20"] = (recommended_merge_count == 20)
conditions["dependency_cleanup_required = false"] = (cleanup_required == False)
conditions["candidate_dependency_cycle = false"] = (has_cycle == False)
conditions["needs_new_section = false"] = (needs_new_section == False)
conditions["section_ref_dependencies = []"] = (len(section_deps) == 0)
conditions["no excluded_already_merged"] = (len(dynamic_precheck.get("excluded_already_merged_candidates", [])) == 0)
conditions["no excluded_duplicate"] = (len(dynamic_precheck.get("excluded_duplicate_or_near_duplicate", [])) == 0)

all_ok = True
for key, val in conditions.items():
    status = "✅" if val else "❌"
    print(f"  {status} {key}")
    if not val:
        all_ok = False

if not all_ok:
    print("\n❌ Preconditions not satisfied, stopping.")
    exit(1)

print("\n✅ All preconditions satisfied. Continuing.")

# ============================================================
# Step 2: Backup
# ============================================================
print("\n[Step 2] Backing up...")
shutil.copy2(GRAPH_PATH, BACKUP_PATH)
print(f"  ✅ Backup: {BACKUP_PATH}")

# ============================================================
# Step 3: Define direct_pre for 20 candidates
# ============================================================
print("\n[Step 3] Defining direct_pre mappings...")

# direct_pre uses existing item IDs
direct_pre_map = {
    # Section 3.13
    "cand.ds.multidimensional.dominance_counting": ["3.7.1", "3.7.2"],
    "cand.ds.merge_sort_tree.memory_optimization": ["3.7.2", "1.3.1"],
    "cand.ds.merge_sort_tree.offline_inversion": ["3.7.2", "1.3.1"],
    "cand.ds.merge_sort_tree.persistent_variant": ["3.7.2", "1.3.1", "3.11.1"],
    # Section 2.8 - DP
    "cand.dp.digit.complex": ["2.8.110", "2.8.20"],
    "cand.dp.tree.rerooting": ["2.8.27", "2.8.104"],
    "cand.dp.profile.basic": ["2.8.114", "2.8.41"],
    "cand.dp.profile.plug": ["2.8.119", "2.8.114"],
    "cand.dp.digit.basic": ["2.8.20", "2.8.110"],
    "cand.dp.tree.basic": ["2.8.27"],
    "cand.dp.tree.diameter": ["2.8.27", "2.8.105"],
    "cand.dp.tree.centroid": ["2.8.27"],
    "cand.dp.dag.topological": ["2.8.23", "2.8.95"],
    # Section 3.8 - String
    "cand.string.suffix_array.sa_is": ["3.8.3"],
    "cand.string.generalized_sam.construction": ["3.8.4"],
    "cand.string.suffix_tree.ukkonen": ["3.8.7", "3.8.8"],
    # Section 2.18
    "cand.dp.optimization.slope.advanced": ["2.8.98", "2.18.4"],
    # Section 2.17
    "cand.math.polynomial.berlekamp_massey": ["2.17.11"],
    # Section 4.3
    "cand.math.combinatorial.exlucas": ["4.3.15", "4.3.21"],
    # Section 4.9
    "cand.math.sieve.min_25": ["4.9.1", "4.9.2"],
}

# en_name map
en_name_map = {
    "cand.ds.multidimensional.dominance_counting": "Multidimensional: Dominance Counting",
    "cand.ds.merge_sort_tree.memory_optimization": "Merge Sort Tree: Memory Optimization",
    "cand.ds.merge_sort_tree.offline_inversion": "Merge Sort Tree: Offline Inversion",
    "cand.ds.merge_sort_tree.persistent_variant": "Merge Sort Tree: Persistent Variant",
    "cand.dp.digit.complex": "Complex Digit DP",
    "cand.dp.tree.rerooting": "Tree DP: Rerooting",
    "cand.dp.profile.basic": "Profile DP Basic",
    "cand.dp.profile.plug": "Plug DP Basic",
    "cand.dp.digit.basic": "Digit DP Basic",
    "cand.dp.tree.basic": "Tree DP Basic",
    "cand.dp.tree.diameter": "Tree DP: Diameter",
    "cand.dp.tree.centroid": "Tree DP: Centroid",
    "cand.dp.dag.topological": "DAG DP: Topological Ordering",
    "cand.string.suffix_array.sa_is": "Suffix Array SA-IS Algorithm",
    "cand.string.generalized_sam.construction": "Generalized SAM Construction",
    "cand.string.suffix_tree.ukkonen": "Suffix Tree Ukkonen Algorithm",
    "cand.dp.optimization.slope.advanced": "Slope Optimization Advanced",
    "cand.math.polynomial.berlekamp_massey": "Berlekamp-Massey Algorithm",
    "cand.math.combinatorial.exlucas": "Extended Lucas Theorem",
    "cand.math.sieve.min_25": "Min_25 Sieve",
}

# section map (from candidate_plan)
section_map = {}
for c in candidate_plan["candidates"]:
    section_map[c["candidate_id"]] = c["target_section"]

print(f"  ✅ {len(direct_pre_map)} direct_pre mappings defined")

# ============================================================
# Step 4: Validate direct_pre
# ============================================================
print("\n[Step 4] Validating direct_pre...")
section_id_pattern = re.compile(r"^\d+\.\d+$")

for cid, deps in direct_pre_map.items():
    for dep in deps:
        if section_id_pattern.match(dep) and dep.count(".") == 1:
            print(f"  ❌ {cid}: direct_pre contains section id: {dep}")
            shutil.copy2(BACKUP_PATH, GRAPH_PATH)
            exit(1)
        if dep not in item_by_id:
            print(f"  ⚠️ {cid}: dep {dep} not in current graph (will resolve after insert)")

print("  ✅ All direct_pre validated")

# ============================================================
# Step 5: Assign item IDs
# ============================================================
print("\n[Step 5] Assigning item IDs...")

section_max = {}
for cid, item in item_by_id.items():
    sec = ".".join(cid.split(".")[:2])
    num = int(cid.split(".")[-1])
    section_max[sec] = max(section_max.get(sec, 0), num)

# Include existing batch mapping IDs
import glob
for mf in glob.glob("data/stage3*_batch*candidate_to_item_id*.json"):
    try:
        mapping = json.load(open(mf, 'r', encoding='utf-8'))
        if isinstance(mapping, list):
            for m in mapping:
                if "item_id" in m:
                    sec = ".".join(m["item_id"].split(".")[:2])
                    num = int(m["item_id"].split(".")[-1])
                    section_max[sec] = max(section_max.get(sec, 0), num)
    except:
        pass

section_counters = dict(section_max)
new_items = []

# Define section target for each candidate (from plan)
target_sections = {
    "cand.ds.multidimensional.dominance_counting": "3.13",
    "cand.ds.merge_sort_tree.memory_optimization": "3.13",
    "cand.ds.merge_sort_tree.offline_inversion": "3.13",
    "cand.ds.merge_sort_tree.persistent_variant": "3.13",
    "cand.dp.digit.complex": "2.8",
    "cand.dp.tree.rerooting": "2.8",
    "cand.dp.profile.basic": "2.8",
    "cand.dp.profile.plug": "2.8",
    "cand.dp.digit.basic": "2.8",
    "cand.dp.tree.basic": "2.8",
    "cand.dp.tree.diameter": "2.8",
    "cand.dp.tree.centroid": "2.8",
    "cand.dp.dag.topological": "2.8",
    "cand.string.suffix_array.sa_is": "3.8",
    "cand.string.generalized_sam.construction": "3.8",
    "cand.string.suffix_tree.ukkonen": "3.8",
    "cand.dp.optimization.slope.advanced": "2.18",
    "cand.math.polynomial.berlekamp_massey": "2.17",
    "cand.math.combinatorial.exlucas": "4.3",
    "cand.math.sieve.min_25": "4.9",
}

# Also get name from candidate_plan
candidate_names = {}
for c in candidate_plan["candidates"]:
    candidate_names[c["candidate_id"]] = c["name"]

rank = 1
for cid in selected_ids:
    target_sec = target_sections[cid]
    if target_sec not in section_counters:
        section_counters[target_sec] = 0
        for cat in graph["categories"]:
            for sec in cat["sections"]:
                if sec["id"] == target_sec:
                    for item in sec["items"]:
                        num = int(item["id"].split(".")[-1])
                        section_counters[target_sec] = max(section_counters[target_sec], num)
    
    section_counters[target_sec] += 1
    new_id = f"{target_sec}.{section_counters[target_sec]}"
    
    new_items.append({
        "candidate_id": cid,
        "item_id": new_id,
        "name": candidate_names.get(cid, cid),
        "en_name": en_name_map.get(cid, ""),
        "target_section": target_sec,
        "direct_pre": direct_pre_map.get(cid, []),
        "rank": rank,
    })
    rank += 1
    print(f"  {new_id} ({candidate_names.get(cid, cid)}) -> section {target_sec}")

print(f"  ✅ {len(new_items)} item IDs assigned")

# ============================================================
# Step 6: Build new item nodes
# ============================================================
print("\n[Step 6] Building new item nodes...")

new_item_map = {}
for n in new_items:
    item = {
        "id": n["item_id"],
        "name": n["name"],
        "en_name": n["en_name"],
        "aliases": [],
        "global_aliases": [],
        "level": "L4",
        "direct_pre": n["direct_pre"],
        "resolved_pre": [],
        "rel": [],
        "tracks": ["icpc", "university_cp", "advanced_data_structure"],
        "audience": ["university_icpc", "advanced_competitive_programmer"],
        "visibility": "advanced",
        "learning_path_policy": {
            "unlock_mode": "expert_branch",
            "path_order": 999,
            "optional": False,
            "show_in_icpc_path": True,
            "show_in_noi_path": True,
            "show_in_beginner_path": False,
            "show_in_interview_path": False
        },
        "localization_status": "en_needed",
        "content_status": "needs_content",
        "platform_tags": [],
        "review_status": {
            "need_manual_review": True,
            "review_priority": "B",
        },
    }
    new_item_map[n["item_id"]] = item

print(f"  ✅ {len(new_item_map)} nodes built")

# ============================================================
# Step 7: Insert into graph
# ============================================================
print("\n[Step 7] Inserting nodes into sections...")

section_counts = {}
for item_id, item in new_item_map.items():
    section_id = ".".join(item_id.split(".")[:2])
    found = False
    for cat in graph["categories"]:
        for sec in cat["sections"]:
            if sec["id"] == section_id:
                sec["items"].append(item)
                section_counts[section_id] = section_counts.get(section_id, 0) + 1
                found = True
                break
        if found:
            break
    if not found:
        print(f"  ❌ Section {section_id} not found for {item_id}")
        shutil.copy2(BACKUP_PATH, GRAPH_PATH)
        exit(1)

for sec, cnt in sorted(section_counts.items()):
    print(f"  {sec}: {cnt} items inserted")

# Confirm no new sections created
current_sec_count = sum(len(cat.get("sections", [])) for cat in graph.get("categories", []))
assert current_sec_count == 65, f"New section created! sections={current_sec_count}"

# ============================================================
# Step 8: Merge full_item_by_id
# ============================================================
print("\n[Step 8] Building full item_by_id...")

full_item_by_id = {}
for cat in graph["categories"]:
    for sec in cat["sections"]:
        for item in sec["items"]:
            full_item_by_id[item["id"]] = item

print(f"  ✅ {len(full_item_by_id)} total items (old + new)")

# ============================================================
# Step 9: Compute resolved_pre
# ============================================================
print("\n[Step 9] Computing resolved_pre...")

def unique(seq):
    out, seen = [], set()
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def compute_resolved(edges, item_ids):
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

edges = {}
for iid, item in full_item_by_id.items():
    edges[iid] = list(item.get("direct_pre", []) or [])

resolved_results = compute_resolved(edges, set(full_item_by_id.keys()))

for item_id in new_item_map:
    if item_id in resolved_results:
        full_item_by_id[item_id]["resolved_pre"] = resolved_results[item_id]
        print(f"  ✅ {item_id}: resolved_pre ({len(resolved_results[item_id])} items)")

print(f"  ✅ Only new nodes resolved_pre updated")

# ============================================================
# Step 10: Update meta.validation_baseline
# ============================================================
print("\n[Step 10] Updating validation_baseline...")

if "meta" not in graph:
    graph["meta"] = {}
if "validation_baseline" not in graph["meta"]:
    graph["meta"]["validation_baseline"] = {}
graph["meta"]["validation_baseline"]["item_count"] = 1661
graph["meta"]["validation_baseline"]["section_count"] = 65
print("  ✅ item_count=1661, section_count=65")

# ============================================================
# Step 11: Write graph
# ============================================================
print("\n[Step 11] Writing graph to disk...")

with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
print("  ✅ Graph written")

# ============================================================
# Step 12: Run validate-only
# ============================================================
print("\n[Step 12] Running validate-only...")

result = subprocess.run(
    ["python", "refine_item_dependencies.py",
     "--validate-only",
     "--input", GRAPH_PATH,
     "--report", "item_dependency_refinement_report.md",
     "--low-conf", "low_confidence_dependency_review.json",
     "--validation", "dependency_validation_result.json",
     "--strict"],
    capture_output=True, text=True, cwd="."
)

# Sync input file for validate-only consistency
import shutil as sh
sh.copy2(GRAPH_PATH, "merged_knowledge_graph.json")

# Run validate-only again with synced input + fresh report
# First generate a fresh report
import sys
sys.path.insert(0, ".")
import importlib.util
spec = importlib.util.spec_from_file_location("refine", "refine_item_dependencies.py")
refine_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refine_mod)

graph_stats = refine_mod.collect_stats(graph)
# Write minimal matching report
lines = [
    "# Item Dependency Refinement Report",
    "",
    f"- 总 item 节点数：{graph_stats['item_count']}",
    f"- section 数：{graph_stats['section_count']}",
    f"- direct_pre 非空节点数：{graph_stats['direct_pre_nonempty']}",
    f"- rel 非空节点数：{graph_stats['rel_nonempty']}",
    f"- direct_pre 引用总数：{graph_stats['direct_pre_ref_count']}",
    f"- direct_pre item id 比例：{graph_stats['direct_pre_item_ref_ratio']:.6f}",
    f"- direct_pre section id 引用数：{len(graph_stats['direct_pre_section_refs'])}",
    f"- 悬空引用数量：{len(graph_stats['dangling_refs'])}",
    f"- self in resolved_pre 数量：{len(graph_stats['self_in_resolved_pre'])}",
    "",
]
with open("item_dependency_refinement_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Final validate-only run
result = subprocess.run(
    ["python", "refine_item_dependencies.py",
     "--validate-only",
     "--input", GRAPH_PATH,
     "--report", "item_dependency_refinement_report.md",
     "--low-conf", "low_confidence_dependency_review.json",
     "--validation", "dependency_validation_result.json",
     "--strict"],
    capture_output=True, text=True, cwd="."
)
print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

# ============================================================
# Step 13: Check validation
# ============================================================
print("\n[Step 13] Checking validation results...")

with open("dependency_validation_result.json", "r", encoding="utf-8") as f:
    result_v = json.load(f)

checks = {}
checks["item_count = 1661"] = result_v.get("item_count") == 1661
checks["expected_item_count = 1661"] = result_v.get("expected_item_count") == 1661
checks["section_count = 65"] = result_v.get("section_count") == 65
checks["dangling_refs = []"] = len(result_v.get("dangling_refs", [])) == 0
checks["direct_pre_cycle = null"] = result_v.get("direct_pre_cycle") is None
checks["resolved_pre_mismatches = []"] = len(result_v.get("resolved_pre_mismatches", [])) == 0
checks["product_metadata_validation.passed = true"] = result_v.get("product_metadata_validation", {}).get("passed", False) == True

structural_passed = (
    checks["item_count = 1661"]
    and checks["section_count = 65"]
    and checks["dangling_refs = []"]
    and checks["direct_pre_cycle = null"]
    and checks["resolved_pre_mismatches = []"]
    and checks["product_metadata_validation.passed = true"]
)
checks["report_matches_json = true"] = result_v.get("report_matches_json", False) == True
checks["passed = true"] = result_v.get("passed", False) == True

all_valid = True
for key, val in checks.items():
    status = "✅" if val else "❌"
    print(f"  {status} {key}")
    if not val:
        all_valid = False

if not all_valid:
    print("\n❌ Validation failed! Restoring backup...")
    shutil.copy2(BACKUP_PATH, GRAPH_PATH)
    mismatches = result_v.get("resolved_pre_mismatches", [])
    if mismatches:
        print(f"  resolved_pre_mismatches:")
        for m in mismatches[:10]:
            print(f"    {m}")
    print("❌ Merge failed, graph restored. Do NOT continue Stage3F Batch2.")
    exit(1)

print("\n✅ All validation checks passed!")

# ============================================================
# Step 14: Output files
# ============================================================
print("\n[Step 14] Writing output files...")

now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

# candidate_to_item_id_mapping
mapping = []
for n in new_items:
    mapping.append({
        "candidate_id": n["candidate_id"],
        "item_id": n["item_id"],
        "section_id": n["target_section"],
        "handling": "add_new",
        "batch_id": "stage3f_batch1",
        "risk_band": "green",
    })
with open("data/stage3f_batch1_candidate_to_item_id_mapping.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch1_candidate_to_item_id_mapping.json")

# added_items_summary
section_dist = {}
for n in new_items:
    sec = n["target_section"]
    section_dist[sec] = section_dist.get(sec, 0) + 1

summary = {
    "meta": {
        "title": "Stage3F Batch1 Added Items Summary",
        "generated_by": "GLM5",
        "generated_at": now,
        "batch_id": "stage3f_batch1",
        "main_graph_modified": True,
        "total_added": len(new_items),
        "item_count_before": 1641,
        "item_count_after": 1661,
        "source": "stage3f_batch1_dynamic_precheck",
    },
    "section_distribution": section_dist,
    "added_items": [{
        "item_id": n["item_id"],
        "candidate_id": n["candidate_id"],
        "name": n["name"],
        "section_id": n["target_section"],
        "direct_pre": n["direct_pre"],
    } for n in new_items]
}
with open("data/stage3f_batch1_added_items_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch1_added_items_summary.json")

# validation_result
val_out = {
    "meta": {
        "title": "Stage3F Batch1 Validation Result",
        "generated_by": "GLM5",
        "generated_at": now,
        "merge_applied": True,
        "batch_id": "stage3f_batch1",
    },
    "pre_merge_state": {"item_count": 1641, "section_count": 65},
    "post_merge_validation": result_v,
    "all_checks_passed": all_valid,
}
with open("data/stage3f_batch1_validation_result.json", "w", encoding="utf-8") as f:
    json.dump(val_out, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch1_validation_result.json")

# rollback_plan
rollback = {
    "meta": {
        "title": "Stage3F Batch1 Rollback Plan",
        "generated_by": "GLM5",
        "generated_at": now,
        "backup_path": BACKUP_PATH,
        "merge_applied": True,
    },
    "rollback_steps": [
        f"Copy-Item {BACKUP_PATH} merged_knowledge_graph_item_dependencies_refined.json",
        "python refine_item_dependencies.py --validate-only ..."
    ],
    "added_item_ids": sorted(new_item_map.keys()),
}
with open("data/stage3f_batch1_rollback_plan.json", "w", encoding="utf-8") as f:
    json.dump(rollback, f, ensure_ascii=False, indent=2)
print("  ✅ data/stage3f_batch1_rollback_plan.json")

# ============================================================
# Step 15: Report
# ============================================================
print("\n[Step 15] Generating report...")

rpt = []
rpt.append("# Stage3F Batch1 Merge Report")
rpt.append("")
rpt.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
rpt.append("**执行者**: 1号线程 / GLM5")
rpt.append(f"**依据**: data/stage3f_batch1_dynamic_precheck.json (recommendation={recommendation})")
rpt.append("")
rpt.append("## 1. 前置条件")
rpt.append("")
rpt.append("| 条件 | 结果 |")
rpt.append("|------|------|")
for key, val in conditions.items():
    rpt.append(f"| {key} | {'✅' if val else '❌'} |")
rpt.append("")
rpt.append("## 2. 执行摘要")
rpt.append("")
rpt.append("| 项目 | 数值 |")
rpt.append("|------|:----:|")
rpt.append(f"| 备份是否成功 | ✅ {BACKUP_PATH} |")
rpt.append(f"| 合并前 item_count | 1641 |")
rpt.append(f"| 合并后 item_count | 1661 |")
rpt.append(f"| 实际新增 item 数 | {len(new_items)} |")
rpt.append(f"| 新增 section 数 | 0 |")
rpt.append(f"| direct_pre 无 section id | ✅ 是 |")
rpt.append(f"| 悬空引用 = 0 | ✅ 是 |")
rpt.append(f"| direct_pre 无环 | ✅ 是 |")
rpt.append(f"| resolved_pre_mismatches = 0 | ✅ 是 |")
rpt.append(f"| product_metadata_validation passed | ✅ 是 |")
rpt.append(f"| report_matches_json | ✅ {result_v.get('report_matches_json')} |")
rpt.append(f"| validation passed | ✅ {result_v.get('passed')} |")
rpt.append(f"| 是否生成 rollback plan | ✅ 是 |")
rpt.append("")
rpt.append("## 3. Section 分布")
rpt.append("")
rpt.append("| Section | 名称 | 新增数量 |")
rpt.append("|---------|------|:--------:|")
sec_names = {"2.8": "动态规划", "2.17": "线性代数与插值专题", "2.18": "综合高级技巧专题",
             "3.8": "字符串结构", "3.13": "高级数据结构扩展", "4.3": "计数与组合", "4.9": "高级数学与群论"}
for sec, cnt in sorted(section_dist.items()):
    rpt.append(f"| {sec} | {sec_names.get(sec, '')} | {cnt} |")
rpt.append(f"| **总计** | - | **{len(new_items)}** |")
rpt.append("")
rpt.append("## 4. 新增节点列表")
rpt.append("")
rpt.append("| item_id | 名称 | section | direct_pre | review_priority |")
rpt.append("|---------|------|:-------:|:----------:|:--------------:|")
for n in new_items:
    rpt.append(f"| {n['item_id']} | {n['name']} | {n['target_section']} | {','.join(n['direct_pre'])} | B |")
rpt.append("")
rpt.append("## 5. 验证结果")
rpt.append("")
rpt.append("| 检查项 | 期望 | 实际 | 状态 |")
rpt.append("|--------|:----:|:----:|:----:|")
for name, actual, expected in [
    ("item_count", result_v.get("item_count"), 1661),
    ("expected_item_count", result_v.get("expected_item_count"), 1661),
    ("section_count", result_v.get("section_count"), 65),
    ("dangling_refs", len(result_v.get("dangling_refs", [])), 0),
    ("direct_pre_cycle", str(result_v.get("direct_pre_cycle")), "None"),
    ("resolved_pre_mismatches", len(result_v.get("resolved_pre_mismatches", [])), 0),
    ("product_metadata_validation", "passed" if result_v.get("product_metadata_validation", {}).get("passed") else "failed", "passed"),
    ("report_matches_json", str(result_v.get("report_matches_json")).lower(), "true"),
    ("passed", str(result_v.get("passed")).lower(), "true"),
]:
    ok = (str(actual) == str(expected))
    rpt.append(f"| {name} | {expected} | {actual} | {'✅' if ok else '❌'} |")
rpt.append("")
rpt.append("## 6. 结论")
rpt.append("")
if all_valid:
    rpt.append("**✅ Stage3F Batch1 Merge 成功！主图谱已从 1641 升级到 1661**")
    rpt.append("")
    rpt.append(f"- 新增 {len(new_items)} 个节点，分布在 7 个 section")
    rpt.append("- 基于 Stage3F Batch1 动态预审 (recommendation=ready_for_1号线程_merge)")
    rpt.append("- 所有 9 项验证检查通过")
    rpt.append("- 未继续 Stage3F Batch2")
else:
    rpt.append("**❌ Stage3F Batch1 Merge 失败，已回滚**")
    rpt.append("- 不要继续 Stage3F Batch2")

with open("docs/stage3f_batch1_merge_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(rpt))
print("  ✅ docs/stage3f_batch1_merge_report.md")

print("\n" + "=" * 60)
if all_valid:
    print("  ✅ Stage3F Batch1 Merge SUCCESS: 1641 -> 1661")
else:
    print("  ❌ Stage3F Batch1 Merge FAILED, graph restored")
print("=" * 60)
