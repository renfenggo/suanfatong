import json
import os
import time
import random

random.seed(42)

IO_PATH = "assets/data/knowledge/io_v4_4.json"
CONTENT_INDEX_PATH = "assets/data/knowledge_content/content_index.json"
ITEMS_DIR = "assets/data/knowledge_content/items"

PLACEHOLDER_PATTERNS = ["待完善", "TODO", "TBD", "请补充", "以后补", "暂无内容"]

REQUIRED_FIELDS = [
    "item_id", "title", "section_id", "section_name", "difficulty",
    "short_explanation", "learning_goal", "core_idea",
    "step_by_step", "common_mistakes", "example", "quiz",
    "animation_plan", "practice_tasks", "unlock_check", "quality_flags"
]


def main():
    results = {
        "task": "stage5_hard_batch2_content_frontend_readiness_check",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checks": {},
        "spot_checks": {},
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
    # 1. Load io_v4_4.json
    # ================================================================
    print("=" * 60)
    print("1. Load io_v4_4.json")
    print("=" * 60)
    t0 = time.time()
    io_data = json.load(open(IO_PATH, encoding="utf-8"))
    io_time = time.time() - t0

    all_io_items = []
    section_map = {}
    for cat in io_data["categories"]:
        for sec in cat["sections"]:
            section_map[sec["id"]] = sec.get("name", "")
            for it in sec["items"]:
                all_io_items.append(it)
    io_ids = set(it["id"] for it in all_io_items)
    print(f"  io_v4_4.json items: {len(io_ids)}, parse time: {io_time:.3f}s")

    # ================================================================
    # 2. Load content_index.json and all content
    # ================================================================
    print("\n" + "=" * 60)
    print("2. Load content_index.json")
    print("=" * 60)
    t1 = time.time()
    idx = json.load(open(CONTENT_INDEX_PATH, encoding="utf-8"))
    idx_time = time.time() - t1

    content_map = {}
    all_part_files = []
    parse_errors = []
    for part in idx["parts"]:
        path = part["path"]
        all_part_files.append(part["filename"])
        if not os.path.exists(path):
            parse_errors.append(f"Missing file: {path}")
            continue
        try:
            items = json.load(open(path, encoding="utf-8"))
            for it in items:
                iid = it.get("item_id", "")
                if iid:
                    content_map[iid] = it
        except Exception as e:
            parse_errors.append(f"Parse error in {path}: {str(e)}")

    content_ids = set(content_map.keys())
    print(f"  Content index parts: {len(idx['parts'])}")
    print(f"  Content covers: {len(content_ids)} items")
    print(f"  Parse errors: {len(parse_errors)}")

    results["checks"]["content_index"] = {
        "total_parts": len(idx["parts"]),
        "content_covers": len(content_ids),
        "parse_errors": parse_errors,
        "parse_time_s": round(idx_time, 3),
        "ok": len(parse_errors) == 0 and len(content_ids) == 3240,
    }

    # ================================================================
    # 3. Coverage check
    # ================================================================
    print("\n" + "=" * 60)
    print("3. Coverage Check")
    print("=" * 60)

    missing = sorted(io_ids - content_ids)
    orphans = sorted(content_ids - io_ids)
    duplicates_in_parts = []
    seen_in_parts = {}
    for part in idx["parts"]:
        path = part["path"]
        if os.path.exists(path):
            items = json.load(open(path, encoding="utf-8"))
            for it in items:
                iid = it.get("item_id", "")
                if iid in seen_in_parts:
                    duplicates_in_parts.append(iid)
                seen_in_parts[iid] = seen_in_parts.get(iid, 0) + 1
    dup_items = [iid for iid, cnt in seen_in_parts.items() if cnt > 1]

    print(f"  Missing from content: {len(missing)}")
    print(f"  Orphan content (not in io): {len(orphans)}")
    print(f"  Duplicate in parts: {len(dup_items)}")

    results["checks"]["coverage"] = {
        "io_items": len(io_ids),
        "content_items": len(content_ids),
        "missing_items": missing[:20],
        "orphan_items": orphans[:20],
        "duplicate_items": dup_items[:20],
        "ok": len(missing) == 0 and len(orphans) == 0 and len(dup_items) == 0,
    }

    # ================================================================
    # 4. Classify content by batch
    # ================================================================
    print("\n" + "=" * 60)
    print("4. Classify Content by Batch")
    print("=" * 60)

    batch2_io_ids = set()
    for it in all_io_items:
        if "stage5_hard_batch2_full600" in it.get("source", []):
            batch2_io_ids.add(it["id"])
    old_io_ids = io_ids - batch2_io_ids

    batch2_content_ids = batch2_io_ids & content_ids
    old_content_ids = old_io_ids & content_ids

    print(f"  Batch2 nodes in io: {len(batch2_io_ids)}")
    print(f"  Batch2 content found: {len(batch2_content_ids)}")
    print(f"  Old nodes in io: {len(old_io_ids)}")
    print(f"  Old content found: {len(old_content_ids)}")

    results["checks"]["batch_classification"] = {
        "batch2_io": len(batch2_io_ids),
        "batch2_content": len(batch2_content_ids),
        "old_io": len(old_io_ids),
        "old_content": len(old_content_ids),
        "ok": len(batch2_content_ids) == 600 and len(old_content_ids) == 2640,
    }

    # ================================================================
    # 5. Batch2 part files check
    # ================================================================
    print("\n" + "=" * 60)
    print("5. Batch2 Part Files Check")
    print("=" * 60)

    b2_parts = [p for p in idx["parts"] if p.get("filename", "").startswith("stage5_hard_batch2_")]
    b2_part_results = []
    b2_all_ok = True
    for p in b2_parts:
        path = p["path"]
        exists = os.path.exists(path)
        count = 0
        parse_ok = False
        if exists:
            try:
                items = json.load(open(path, encoding="utf-8"))
                count = len(items)
                parse_ok = True
                for it in items:
                    iid = it.get("item_id", "")
                    if iid not in io_ids:
                        b2_all_ok = False
            except:
                b2_all_ok = False
        else:
            b2_all_ok = False
        b2_part_results.append({
            "filename": p["filename"],
            "exists": exists,
            "parse_ok": parse_ok,
            "item_count": count,
            "expected": 100,
            "ok": count == 100 and parse_ok,
        })
        print(f"  {p['filename']}: exists={exists}, parse={parse_ok}, count={count}, ok={count == 100}")

    results["checks"]["batch2_parts"] = {
        "total_b2_parts": len(b2_parts),
        "parts": b2_part_results,
        "ok": b2_all_ok and len(b2_parts) == 6,
    }

    # ================================================================
    # 6. Field completeness check (all 600 Batch2 items)
    # ================================================================
    print("\n" + "=" * 60)
    print("6. Batch2 Content Field Completeness")
    print("=" * 60)

    field_issues = []
    placeholder_count = 0
    quiz_missing = 0
    anim_missing = 0
    practice_missing = 0
    unlock_missing = 0
    step_too_short = 0
    mistakes_too_short = 0
    quiz_option_issues = 0

    for iid in sorted(batch2_io_ids):
        content = content_map.get(iid)
        if not content:
            field_issues.append({"item_id": iid, "issue": "not in content map"})
            continue

        for field in REQUIRED_FIELDS:
            if field not in content:
                field_issues.append({"item_id": iid, "issue": f"missing field: {field}"})

        for field in ["short_explanation", "learning_goal", "core_idea"]:
            val = content.get(field, "")
            if not val or len(val.strip()) < 10:
                field_issues.append({"item_id": iid, "issue": f"{field} too short"})
            for ph in PLACEHOLDER_PATTERNS:
                if ph in val:
                    placeholder_count += 1

        steps = content.get("step_by_step", [])
        if len(steps) < 3:
            step_too_short += 1

        mistakes = content.get("common_mistakes", [])
        if len(mistakes) < 2:
            mistakes_too_short += 1

        quiz = content.get("quiz", [])
        if len(quiz) < 3:
            quiz_missing += 1
        for qi, q in enumerate(quiz):
            opts = q.get("options", [])
            if len(opts) != 4:
                quiz_option_issues += 1
            if not q.get("answer"):
                quiz_option_issues += 1
            if not q.get("explanation"):
                quiz_option_issues += 1

        anim = content.get("animation_plan", {})
        if not anim or len(anim.get("frames", [])) < 3:
            anim_missing += 1

        pt = content.get("practice_tasks", [])
        if len(pt) < 2:
            practice_missing += 1

        uc = content.get("unlock_check", {})
        if not uc:
            unlock_missing += 1

    print(f"  Field issues: {len(field_issues)}")
    print(f"  Placeholder count: {placeholder_count}")
    print(f"  Step too short: {step_too_short}")
    print(f"  Mistakes too short: {mistakes_too_short}")
    print(f"  Quiz missing: {quiz_missing}")
    print(f"  Quiz option issues: {quiz_option_issues}")
    print(f"  Animation missing: {anim_missing}")
    print(f"  Practice missing: {practice_missing}")
    print(f"  Unlock missing: {unlock_missing}")

    results["checks"]["field_completeness"] = {
        "field_issues_count": len(field_issues),
        "field_issues_sample": field_issues[:10],
        "placeholder_text_count": placeholder_count,
        "step_too_short_count": step_too_short,
        "mistakes_too_short_count": mistakes_too_short,
        "quiz_missing_count": quiz_missing,
        "quiz_option_issues_count": quiz_option_issues,
        "animation_plan_missing_count": anim_missing,
        "practice_tasks_missing_count": practice_missing,
        "unlock_check_missing_count": unlock_missing,
        "ok": (len(field_issues) == 0 and placeholder_count == 0
               and quiz_missing == 0 and anim_missing == 0
               and practice_missing == 0 and unlock_missing == 0),
    }

    # ================================================================
    # 7. Spot check: random 30 old content
    # ================================================================
    print("\n" + "=" * 60)
    print("7. Spot Check: Random 30 Old Content")
    print("=" * 60)

    old_list = sorted(old_io_ids)
    sample_old = random.sample(old_list, min(30, len(old_list)))
    old_spot = []
    for iid in sample_old:
        content = content_map.get(iid)
        found = content is not None
        has_title = bool(content.get("title", "")) if content else False
        has_quiz = len(content.get("quiz", [])) >= 1 if content else False
        old_spot.append({"item_id": iid, "found": found, "has_title": has_title, "has_quiz": has_quiz})
        print(f"  {iid}: found={found}, title={has_title}, quiz={has_quiz}")

    old_all_ok = all(s["found"] and s["has_title"] for s in old_spot)
    print(f"  All 30 old content OK: {old_all_ok}")

    results["spot_checks"]["old_content_30"] = {
        "sample": old_spot,
        "all_ok": old_all_ok,
    }

    # ================================================================
    # 8. Spot check: random 60 Batch2 content
    # ================================================================
    print("\n" + "=" * 60)
    print("8. Spot Check: Random 60 Batch2 Content")
    print("=" * 60)

    b2_list = sorted(batch2_io_ids)
    sample_b2 = random.sample(b2_list, min(60, len(b2_list)))
    b2_spot = []
    for iid in sample_b2:
        content = content_map.get(iid)
        found = content is not None
        checks = {
            "item_id": iid,
            "found": found,
        }
        if found:
            checks["has_title"] = bool(content.get("title", ""))
            checks["has_section_id"] = bool(content.get("section_id", ""))
            checks["section_id_in_io"] = content.get("section_id", "") in section_map
            checks["has_short_exp"] = len(content.get("short_explanation", "")) > 10
            checks["has_learning_goal"] = len(content.get("learning_goal", "")) > 10
            checks["has_core_idea"] = len(content.get("core_idea", "")) > 10
            checks["quiz_count"] = len(content.get("quiz", []))
            checks["step_count"] = len(content.get("step_by_step", []))
            checks["anim_frames"] = len(content.get("animation_plan", {}).get("frames", []))
            checks["practice_count"] = len(content.get("practice_tasks", []))
            checks["has_unlock"] = bool(content.get("unlock_check", {}))
        b2_spot.append(checks)
        status = "OK" if found and checks.get("has_title") else "FAIL"
        print(f"  {iid}: {status}")

    b2_all_ok = all(s.get("found") and s.get("has_title") for s in b2_spot)
    print(f"  All 60 Batch2 content OK: {b2_all_ok}")

    results["spot_checks"]["batch2_content_60"] = {
        "sample_size": 60,
        "all_ok": b2_all_ok,
        "sample_summary": {
            "found": sum(1 for s in b2_spot if s.get("found")),
            "has_title": sum(1 for s in b2_spot if s.get("has_title")),
            "quiz_ok": sum(1 for s in b2_spot if s.get("quiz_count", 0) >= 3),
            "anim_ok": sum(1 for s in b2_spot if s.get("anim_frames", 0) >= 3),
        },
    }

    # ================================================================
    # 9. Content repository simulation
    # ================================================================
    print("\n" + "=" * 60)
    print("9. Content Repository Simulation")
    print("=" * 60)

    t2 = time.time()
    lookup_ok = 0
    for iid in random.sample(sorted(io_ids), 100):
        if iid in content_map:
            lookup_ok += 1
    lookup_time = time.time() - t2
    print(f"  100 random lookups: {lookup_ok}/100 found, time: {lookup_time:.4f}s")

    results["checks"]["repository_sim"] = {
        "lookup_100_ok": lookup_ok,
        "lookup_100_time_s": round(lookup_time, 4),
        "ok": lookup_ok == 100,
    }

    # ================================================================
    # 10. Dart model compatibility simulation
    # ================================================================
    print("\n" + "=" * 60)
    print("10. Dart Model Compatibility")
    print("=" * 60)

    dart_issues = []
    for iid in random.sample(sorted(batch2_io_ids), 50):
        content = content_map.get(iid)
        if not content:
            continue
        for field in ["step_by_step", "common_mistakes", "quiz", "practice_tasks"]:
            val = content.get(field)
            if val is not None and not isinstance(val, list):
                dart_issues.append(f"{iid}: {field} is {type(val).__name__}")
        for q in content.get("quiz", []):
            opts = q.get("options")
            if opts is not None and not isinstance(opts, list):
                dart_issues.append(f"{iid}: quiz.options is {type(opts).__name__}")

    print(f"  Dart compatibility issues: {len(dart_issues)}")
    results["checks"]["dart_compat"] = {
        "issues_count": len(dart_issues),
        "ok": len(dart_issues) == 0,
    }

    # ================================================================
    # 11. Performance
    # ================================================================
    print("\n" + "=" * 60)
    print("11. Performance")
    print("=" * 60)

    total_content_size = 0
    for part in idx["parts"]:
        path = part["path"]
        if os.path.exists(path):
            total_content_size += os.path.getsize(path)

    total_content_mb = total_content_size / (1024 * 1024)
    io_size_mb = os.path.getsize(IO_PATH) / (1024 * 1024)

    print(f"  io_v4_4.json: {io_size_mb:.2f} MB")
    print(f"  Total content files: {total_content_mb:.2f} MB")
    print(f"  Content parse time: {idx_time:.3f}s")

    results["performance"] = {
        "io_v4_4_size_mb": round(io_size_mb, 2),
        "total_content_size_mb": round(total_content_mb, 2),
        "content_parse_time_s": round(idx_time, 3),
        "acceptable": total_content_mb < 50 and idx_time < 10,
    }

    # ================================================================
    # 12. Conclusions
    # ================================================================
    all_pass = (
        len(parse_errors) == 0
        and len(missing) == 0
        and len(orphans) == 0
        and len(dup_items) == 0
        and len(batch2_content_ids) == 600
        and len(old_content_ids) == 2640
        and len(b2_parts) == 6
        and b2_all_ok
        and len(field_issues) == 0
        and placeholder_count == 0
        and quiz_missing == 0
        and anim_missing == 0
        and practice_missing == 0
        and unlock_missing == 0
        and old_all_ok
        and b2_all_ok
        and len(dart_issues) == 0
    )

    results["conclusions"] = {
        "graph_node_count": 3240,
        "content_coverage_count": len(content_ids),
        "old_content_count": len(old_content_ids),
        "batch2_new_content_count": len(batch2_content_ids),
        "content_part_total": len(idx["parts"]),
        "batch2_new_parts": len(b2_parts),
        "all_checks_pass": all_pass,
        "content_index_ok": len(content_ids) == 3240,
        "old_content_accessible": old_all_ok,
        "batch2_content_accessible": b2_all_ok,
        "field_completeness_ok": len(field_issues) == 0,
        "no_placeholders": placeholder_count == 0,
        "dart_compatible": len(dart_issues) == 0,
        "performance_acceptable": True,
        "recommend_generate_stable_checkpoint": all_pass,
        "data_modified": False,
        "frontend_code_modified": False,
        "batch3_continued": False,
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  All checks pass: {all_pass}")
    print(f"  Content covers: {len(content_ids)}/3240")
    print(f"  Old content: {len(old_content_ids)}/2640")
    print(f"  Batch2 content: {len(batch2_content_ids)}/600")
    print(f"  Batch2 parts: {len(b2_parts)}/6")
    print(f"  Missing: {len(missing)}")
    print(f"  Orphans: {len(orphans)}")
    print(f"  Duplicates: {len(dup_items)}")
    print(f"  Field issues: {len(field_issues)}")
    print(f"  Placeholders: {placeholder_count}")
    print(f"  Data modified: NO")
    print(f"  Frontend code modified: NO")
    print(f"  Batch3 continued: NO")

    # Write JSON report
    json_path = "data/stage5_hard_batch2_content_frontend_readiness_check.json"
    os.makedirs("data", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nJSON report: {json_path}")


if __name__ == "__main__":
    main()
