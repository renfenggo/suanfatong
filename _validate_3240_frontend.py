import json
import os
import sys
import time
import random
import importlib.util

random.seed(42)

IO_PATH = "assets/data/knowledge/io_v4_4.json"
MAIN_GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"

def main():
    results = {
        "task": "io_v4_4_3240_frontend_readiness_check",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checks": {},
        "spot_checks": {},
        "section_checks": {},
        "field_compatibility": {},
        "flutter_analyze": None,
        "test_results": None,
        "build_results": {},
        "performance": {},
        "conclusions": {},
        "data_modified": False,
        "frontend_code_modified": False,
        "batch3_continued": False,
    }

    # ================================================================
    # 1. JSON Parse Check
    # ================================================================
    print("=" * 60)
    print("1. JSON Parse Check")
    print("=" * 60)
    t0 = time.time()
    try:
        with open(IO_PATH, encoding="utf-8") as f:
            data = json.load(f)
        parse_ok = True
        parse_error = None
    except Exception as e:
        data = None
        parse_ok = False
        parse_error = str(e)
    parse_time = time.time() - t0

    file_size_mb = os.path.getsize(IO_PATH) / (1024 * 1024)
    print(f"  JSON parse: {'OK' if parse_ok else 'FAIL'}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Parse time: {parse_time:.3f}s")

    results["checks"]["json_parse"] = {
        "ok": parse_ok,
        "error": parse_error,
        "file_size_mb": round(file_size_mb, 2),
        "parse_time_s": round(parse_time, 3),
    }
    results["performance"]["file_size_mb"] = round(file_size_mb, 2)
    results["performance"]["parse_time_s"] = round(parse_time, 3)

    if not parse_ok:
        print("FATAL: Cannot parse JSON. Aborting.")
        write_report(results)
        return

    # ================================================================
    # 2. Simulate Dart KnowledgeGraph.fromJson
    # ================================================================
    print("\n" + "=" * 60)
    print("2. Simulate Dart Model Parsing")
    print("=" * 60)

    categories = data.get("categories", [])
    all_sections = []
    all_items = []
    section_count = 0
    item_count = 0
    parse_errors = []

    for ci, cat in enumerate(categories):
        cat_name = cat.get("name", "")
        cat_sections = cat.get("sections", [])
        for si, sec in enumerate(cat_sections):
            sec_id = sec.get("id", "")
            sec_name = sec.get("name", "")
            if not sec_id:
                parse_errors.append(f"Category[{ci}] Section[{si}] missing id")
                continue
            all_sections.append(sec)
            section_count += 1
            sec_items = sec.get("items", [])
            for ii, it in enumerate(sec_items):
                it_id = it.get("id", "")
                it_name = it.get("name", "")
                if not it_id:
                    parse_errors.append(f"Section[{sec_id}] Item[{ii}] missing id")
                    continue
                all_items.append(it)
                item_count += 1

    print(f"  Categories: {len(categories)}")
    print(f"  Sections: {section_count}")
    print(f"  Items: {item_count}")
    print(f"  Parse errors: {len(parse_errors)}")

    results["checks"]["model_simulation"] = {
        "category_count": len(categories),
        "section_count": section_count,
        "item_count": item_count,
        "expected_section_count": 65,
        "expected_item_count": 3240,
        "section_count_ok": section_count == 65,
        "item_count_ok": item_count == 3240,
        "parse_errors": parse_errors[:20],
    }

    # ================================================================
    # 3. Duplicate IDs
    # ================================================================
    print("\n" + "=" * 60)
    print("3. Duplicate IDs Check")
    print("=" * 60)

    all_item_ids = [it["id"] for it in all_items]
    all_section_ids = [sec["id"] for sec in all_sections]
    dup_items = [iid for iid in set(all_item_ids) if all_item_ids.count(iid) > 1]
    dup_sections = [sid for sid in set(all_section_ids) if all_section_ids.count(sid) > 1]
    print(f"  Duplicate item IDs: {len(dup_items)}")
    print(f"  Duplicate section IDs: {len(dup_sections)}")

    results["checks"]["duplicates"] = {
        "duplicate_item_ids": len(dup_items),
        "duplicate_section_ids": len(dup_sections),
        "ok": len(dup_items) == 0 and len(dup_sections) == 0,
    }

    # ================================================================
    # 4. Build lookup maps
    # ================================================================
    item_map = {it["id"]: it for it in all_items}
    section_map = {sec["id"]: sec for sec in all_sections}
    item_id_set = set(all_item_ids)
    section_id_set = set(all_section_ids)

    # ================================================================
    # 5. Classify items by batch
    # ================================================================
    batch1_ids = set()
    batch2_ids = set()
    old_ids = set()

    for it in all_items:
        srcs = it.get("source", [])
        if "stage5_hard_batch1_full500" in srcs:
            batch1_ids.add(it["id"])
        elif "stage5_hard_batch2_full600" in srcs:
            batch2_ids.add(it["id"])
        else:
            old_ids.add(it["id"])

    print(f"\n  Old nodes: {len(old_ids)}")
    print(f"  Batch1 nodes: {len(batch1_ids)}")
    print(f"  Batch2 nodes: {len(batch2_ids)}")

    # ================================================================
    # 6. Dangling refs check
    # ================================================================
    print("\n" + "=" * 60)
    print("4. Dangling References Check")
    print("=" * 60)

    dangling_direct_pre = []
    dangling_resolved_pre = []
    dangling_rel = []
    dangling_parent = []
    direct_pre_section_refs = []

    for it in all_items:
        parent = it.get("parent", "")
        if parent and parent not in section_id_set:
            dangling_parent.append((it["id"], parent))

        for ref in it.get("direct_pre", []):
            if ref in section_id_set:
                direct_pre_section_refs.append((it["id"], ref))
            elif ref not in item_id_set:
                dangling_direct_pre.append((it["id"], ref))

        for ref in it.get("resolved_pre", []):
            if ref not in item_id_set and ref not in section_id_set:
                dangling_resolved_pre.append((it["id"], ref))

        for ref in it.get("rel", []):
            if ref not in item_id_set and ref not in section_id_set:
                dangling_rel.append((it["id"], ref))

    print(f"  Dangling parent refs: {len(dangling_parent)}")
    print(f"  Dangling direct_pre refs: {len(dangling_direct_pre)}")
    print(f"  Dangling resolved_pre refs: {len(dangling_resolved_pre)}")
    print(f"  Dangling rel refs: {len(dangling_rel)}")
    print(f"  direct_pre section refs: {len(direct_pre_section_refs)}")

    results["checks"]["dangling_refs"] = {
        "dangling_parent": len(dangling_parent),
        "dangling_direct_pre": len(dangling_direct_pre),
        "dangling_resolved_pre": len(dangling_resolved_pre),
        "dangling_rel": len(dangling_rel),
        "direct_pre_section_refs": len(direct_pre_section_refs),
        "ok": (len(dangling_parent) == 0 and len(dangling_direct_pre) == 0
               and len(dangling_resolved_pre) == 0 and len(dangling_rel) == 0
               and len(direct_pre_section_refs) == 0),
    }

    # ================================================================
    # 7. Spot check: random 20 old nodes
    # ================================================================
    print("\n" + "=" * 60)
    print("5. Spot Check: Random 20 Old Nodes")
    print("=" * 60)

    old_list = sorted(old_ids)
    sample_old = random.sample(old_list, min(20, len(old_list)))
    old_spot_results = []
    for iid in sample_old:
        it = item_map[iid]
        has_name = bool(it.get("name", ""))
        has_parent = bool(it.get("parent", ""))
        parent_exists = it.get("parent", "") in section_id_set
        old_spot_results.append({
            "id": iid,
            "name_ok": has_name,
            "parent_ok": has_parent and parent_exists,
        })
        print(f"  {iid}: name={'OK' if has_name else 'MISSING'}, parent={'OK' if has_parent and parent_exists else 'FAIL'}")

    all_old_ok = all(r["name_ok"] and r["parent_ok"] for r in old_spot_results)
    print(f"  All 20 old nodes OK: {all_old_ok}")
    results["spot_checks"]["old_nodes_20"] = {
        "sample": old_spot_results,
        "all_ok": all_old_ok,
    }

    # ================================================================
    # 8. Spot check: random 40 Batch2 new nodes
    # ================================================================
    print("\n" + "=" * 60)
    print("6. Spot Check: Random 40 Batch2 New Nodes")
    print("=" * 60)

    batch2_list = sorted(batch2_ids)
    sample_b2 = random.sample(batch2_list, min(40, len(batch2_list)))
    b2_spot_results = []
    for iid in sample_b2:
        it = item_map[iid]
        has_name = bool(it.get("name", ""))
        has_parent = bool(it.get("parent", ""))
        parent_exists = it.get("parent", "") in section_id_set
        has_direct_pre = "direct_pre" in it
        has_resolved_pre = "resolved_pre" in it
        has_rel = "rel" in it
        b2_spot_results.append({
            "id": iid,
            "name_ok": has_name,
            "parent_ok": has_parent and parent_exists,
            "has_direct_pre": has_direct_pre,
            "has_resolved_pre": has_resolved_pre,
            "has_rel": has_rel,
        })
        print(f"  {iid}: name={'OK' if has_name else 'MISSING'}, parent={'OK' if parent_exists else 'FAIL'}, "
              f"direct_pre={'Y' if has_direct_pre else 'N'}, resolved_pre={'Y' if has_resolved_pre else 'N'}, rel={'Y' if has_rel else 'N'}")

    all_b2_ok = all(r["name_ok"] and r["parent_ok"] for r in b2_spot_results)
    print(f"  All 40 Batch2 nodes OK: {all_b2_ok}")
    results["spot_checks"]["batch2_nodes_40"] = {
        "sample": b2_spot_results,
        "all_ok": all_b2_ok,
    }

    # ================================================================
    # 9. Migration nodes verification
    # ================================================================
    print("\n" + "=" * 60)
    print("7. Migration Nodes Verification")
    print("=" * 60)

    new_ids_313 = [f"3.13.{i}" for i in range(386, 400)]
    new_ids_37 = [f"3.7.{i}" for i in range(40, 53)]
    old_ids_21 = [f"2.1.{i}" for i in range(102, 116)] + [f"2.1.{i}" for i in range(117, 130)]

    migration_new = new_ids_313 + new_ids_37
    migration_old = old_ids_21

    new_found = []
    new_missing = []
    for nid in migration_new:
        if nid in item_id_set:
            it = item_map[nid]
            new_found.append({
                "id": nid,
                "name": it.get("name", "")[:50],
                "parent": it.get("parent", ""),
                "parent_ok": it.get("parent", "") in section_id_set,
            })
            print(f"  NEW {nid}: FOUND, parent={it.get('parent', '')}, parent_ok={it.get('parent', '') in section_id_set}")
        else:
            new_missing.append(nid)
            print(f"  NEW {nid}: MISSING!")

    old_found = []
    for oid in migration_old:
        if oid in item_id_set:
            old_found.append(oid)
            print(f"  OLD {oid}: STILL EXISTS (should not)!")
        else:
            print(f"  OLD {oid}: correctly absent")

    print(f"\n  New IDs found: {len(new_found)}/{len(migration_new)}")
    print(f"  New IDs missing: {len(new_missing)}")
    print(f"  Old IDs still present: {len(old_found)}/{len(migration_old)}")

    results["spot_checks"]["migration"] = {
        "new_ids_expected": len(migration_new),
        "new_ids_found": len(new_found),
        "new_ids_missing": new_missing,
        "old_ids_expected_absent": len(migration_old),
        "old_ids_still_present": old_found,
        "ok": len(new_found) == len(migration_new) and len(old_found) == 0,
        "new_id_details": new_found,
    }

    # ================================================================
    # 10. Section node count checks
    # ================================================================
    print("\n" + "=" * 60)
    print("8. Section Node Count Checks")
    print("=" * 60)

    sec_checks = {}
    for target_id, expected in [("2.1", 115), ("3.13", 367), ("3.7", 52)]:
        sec = section_map.get(target_id)
        if sec:
            actual = len(sec.get("items", []))
            ok = actual == expected
        else:
            actual = -1
            ok = False
        sec_checks[target_id] = {"expected": expected, "actual": actual, "ok": ok}
        print(f"  Section {target_id}: expected={expected}, actual={actual}, ok={ok}")

    results["section_checks"] = sec_checks

    # ================================================================
    # 11. Field compatibility with Dart models
    # ================================================================
    print("\n" + "=" * 60)
    print("9. Field Compatibility with Dart Models")
    print("=" * 60)

    dart_item_fields = {
        "id": str, "name": str, "alias": list, "parent": str,
        "direct_pre": list, "resolved_pre": list, "rel": list,
        "block_id": str, "block_name": str, "pickup_group": str,
        "pickup_group_name": str, "pickup_order": int,
        "resource_block_id": str, "resource_block_name": str,
    }

    dart_section_fields = {
        "id": str, "name": str, "level": str, "pre": list, "rel": list,
        "items": list, "learning_blocks": list, "track": str, "track_note": str,
    }

    field_issues = []
    for it in all_items:
        for field, expected_type in dart_item_fields.items():
            if field in it:
                val = it[field]
                if val is not None and not isinstance(val, expected_type):
                    field_issues.append(f"Item {it['id']}: field '{field}' type {type(val).__name__} != {expected_type.__name__}")
                    break

    for sec in all_sections:
        for field, expected_type in dart_section_fields.items():
            if field in sec:
                val = sec[field]
                if val is not None and not isinstance(val, expected_type):
                    field_issues.append(f"Section {sec['id']}: field '{field}' type {type(val).__name__} != {expected_type.__name__}")
                    break

    if len(field_issues) > 20:
        field_issues_display = field_issues[:20]
    else:
        field_issues_display = field_issues

    print(f"  Field type issues: {len(field_issues)}")
    for issue in field_issues_display:
        print(f"    {issue}")

    results["field_compatibility"] = {
        "dart_model": "KnowledgeItem + KnowledgeSection",
        "type_issues_count": len(field_issues),
        "type_issues_sample": field_issues_display,
        "ok": len(field_issues) == 0,
    }

    # ================================================================
    # 12. direct_pre/resolved_pre/rel field deep check
    # ================================================================
    print("\n" + "=" * 60)
    print("10. Dependency Field Deep Check")
    print("=" * 60)

    dep_issues = []
    for it in all_items[:500]:
        for field in ["direct_pre", "resolved_pre", "rel"]:
            val = it.get(field)
            if val is None:
                continue
            if not isinstance(val, list):
                dep_issues.append(f"Item {it['id']}: {field} is not list: {type(val).__name__}")
                continue
            for elem in val:
                if not isinstance(elem, str):
                    dep_issues.append(f"Item {it['id']}: {field} contains non-string: {type(elem).__name__}")
                    break

    print(f"  Dependency field issues (checked first 500 items): {len(dep_issues)}")
    for issue in dep_issues[:10]:
        print(f"    {issue}")

    results["checks"]["dependency_fields"] = {
        "issues_count": len(dep_issues),
        "issues_sample": dep_issues[:10],
        "ok": len(dep_issues) == 0,
    }

    # ================================================================
    # 13. Cycle detection simulation
    # ================================================================
    print("\n" + "=" * 60)
    print("11. Cycle Detection (DFS)")
    print("=" * 60)

    adjacency = {}
    for it in all_items:
        pre_refs = it.get("resolved_pre", [])
        adjacency[it["id"]] = [r for r in pre_refs if r in item_id_set]

    visited = set()
    in_stack = set()
    has_cycle = False
    cycle_example = None

    def dfs_cycle(node):
        global has_cycle, cycle_example
        visited.add(node)
        in_stack.add(node)
        for pre in adjacency.get(node, []):
            if pre in in_stack:
                return True
            if pre not in visited:
                if dfs_cycle(pre):
                    return True
        in_stack.discard(node)
        return False

    for it in all_items:
        if it["id"] not in visited:
            if dfs_cycle(it["id"]):
                has_cycle = True
                cycle_example = list(in_stack)[:5]
                break

    print(f"  Has cycle: {has_cycle}")
    if has_cycle:
        print(f"  Cycle nodes sample: {cycle_example}")

    results["checks"]["cycle_detection"] = {
        "has_cycle": has_cycle,
        "cycle_nodes_sample": cycle_example,
    }

    # ================================================================
    # 14. Performance estimate
    # ================================================================
    print("\n" + "=" * 60)
    print("12. Performance Estimate")
    print("=" * 60)

    # Simulate full traversal
    t1 = time.time()
    for it in all_items:
        _ = it.get("id", "")
        _ = it.get("name", "")
        _ = it.get("parent", "")
        _ = it.get("direct_pre", [])
        _ = it.get("resolved_pre", [])
        _ = it.get("rel", [])
    traversal_time = time.time() - t1

    # Simulate search (linear scan)
    t2 = time.time()
    for _ in range(100):
        target = random.choice(all_item_ids)
        found = item_map.get(target)
    search_time = time.time() - t2

    print(f"  Full traversal (3240 items): {traversal_time:.4f}s")
    print(f"  100 lookups: {search_time:.4f}s")
    print(f"  JSON parse: {parse_time:.3f}s")
    print(f"  File size: {file_size_mb:.2f} MB")

    performance_acceptable = file_size_mb < 10 and parse_time < 5.0

    results["performance"]["full_traversal_s"] = round(traversal_time, 4)
    results["performance"]["lookup_100_s"] = round(search_time, 4)
    results["performance"]["acceptable"] = performance_acceptable

    # ================================================================
    # 15. Conclusions
    # ================================================================
    all_checks_pass = (
        parse_ok
        and section_count == 65
        and item_count == 3240
        and len(dup_items) == 0
        and len(dup_sections) == 0
        and len(dangling_parent) == 0
        and len(dangling_direct_pre) == 0
        and len(dangling_resolved_pre) == 0
        and len(dangling_rel) == 0
        and len(direct_pre_section_refs) == 0
        and all_old_ok
        and all_b2_ok
        and len(new_found) == len(migration_new)
        and len(old_found) == 0
        and not has_cycle
        and performance_acceptable
        and len(field_issues) == 0
    )

    sec_all_ok = all(v["ok"] for v in sec_checks.values())

    results["conclusions"] = {
        "all_checks_pass": all_checks_pass,
        "json_parse_ok": parse_ok,
        "item_count_ok": item_count == 3240,
        "section_count_ok": section_count == 65,
        "old_nodes_accessible": all_old_ok,
        "batch2_nodes_accessible": all_b2_ok,
        "migration_ok": len(new_found) == len(migration_new) and len(old_found) == 0,
        "section_counts_ok": sec_all_ok,
        "no_duplicates": len(dup_items) == 0,
        "no_dangling_refs": len(dangling_resolved_pre) == 0 and len(dangling_rel) == 0,
        "no_cycles": not has_cycle,
        "field_compatible": len(field_issues) == 0,
        "performance_acceptable": performance_acceptable,
        "recommend_proceed_to_batch2_content": all_checks_pass,
        "data_modified": False,
        "frontend_code_modified": False,
        "batch3_continued": False,
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  All checks pass: {all_checks_pass}")
    print(f"  JSON parse: {'OK' if parse_ok else 'FAIL'}")
    print(f"  Item count: {item_count} (expected 3240) {'OK' if item_count == 3240 else 'FAIL'}")
    print(f"  Section count: {section_count} (expected 65) {'OK' if section_count == 65 else 'FAIL'}")
    print(f"  Old nodes (20 sample): {'OK' if all_old_ok else 'FAIL'}")
    print(f"  Batch2 nodes (40 sample): {'OK' if all_b2_ok else 'FAIL'}")
    print(f"  Migration new IDs: {len(new_found)}/{len(migration_new)} found")
    print(f"  Migration old IDs: {len(old_found)}/{len(migration_old)} still present")
    print(f"  Section counts: {'OK' if sec_all_ok else 'FAIL'}")
    print(f"  No duplicates: {'OK' if len(dup_items) == 0 else 'FAIL'}")
    print(f"  No dangling refs: {'OK' if len(dangling_resolved_pre) == 0 else 'FAIL'}")
    print(f"  No cycles: {'OK' if not has_cycle else 'CYCLE DETECTED'}")
    print(f"  Field compatible: {'OK' if len(field_issues) == 0 else 'ISSUES'}")
    print(f"  Performance acceptable: {'OK' if performance_acceptable else 'CONCERN'}")
    print(f"  Recommend proceed to Batch2 content: {all_checks_pass}")
    print(f"  Data modified: NO")
    print(f"  Frontend code modified: NO")
    print(f"  Batch3 continued: NO")

    write_report(results)


def write_report(results):
    json_path = "data/io_v4_4_3240_frontend_readiness_check.json"
    os.makedirs("data", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nJSON report written to {json_path}")


if __name__ == "__main__":
    main()
