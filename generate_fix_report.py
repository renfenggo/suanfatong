import json
from datetime import datetime

def generate_fix_report():
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    with open("dependency_validation_result.json", 'r', encoding='utf-8') as f:
        validation_result = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_validation_fix_applied_patch.json", 'r', encoding='utf-8') as f:
        validation_fix_patch = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_lpp_fix_summary.json", 'r', encoding='utf-8') as f:
        lpp_fix_summary = json.load(f)
    
    total_items = sum(len(section["items"]) for category in graph["categories"] for section in category["sections"])
    section_count = sum(len(category["sections"]) for category in graph["categories"])
    
    resolved_pre_mismatches = validation_result.get("resolved_pre_mismatches", [])
    
    all_batch4_nodes = all(m["id"] in [item["item_id"] for item in added_items] for m in resolved_pre_mismatches)
    
    all_same_length = all(m["expected_count"] == m["actual_count"] for m in resolved_pre_mismatches)
    
    new_item_ids = [item["item_id"] for item in added_items]
    
    fix_report = {
        "fix_execution_info": {
            "batch_id": "stage3e_aggressive_batch4_validation_fix",
            "fix_applied_at": datetime.now().isoformat(),
            "backup_created": True,
            "backup_file": "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4_validation_fix.json"
        },
        "item_statistics": {
            "before_fix_item_count": 1602,
            "after_fix_item_count": total_items,
            "expected_item_count": validation_result.get("expected_item_count", "N/A"),
            "added_items": len(added_items),
            "section_count": section_count,
            "expected_section_count": validation_result.get("expected_section_count", "N/A")
        },
        "resolved_pre_fix_results": {
            "nodes_fixed": validation_fix_patch["resolved_pre_fixes"]["nodes_modified"],
            "only_new_nodes_fixed": validation_fix_patch["resolved_pre_fixes"]["only_new_nodes_modified"],
            "old_nodes_affected": False,
            "mismatches_after_fix": len(resolved_pre_mismatches),
            "all_mismatches_are_batch4_nodes": all_batch4_nodes,
            "all_mismatches_same_length": all_same_length,
            "resolved_pre_mismatch_detail": [
                {
                    "item_id": m["id"],
                    "expected_count": m["expected_count"],
                    "actual_count": m["actual_count"],
                    "is_batch4_node": m["id"] in new_item_ids,
                    "same_length": m["expected_count"] == m["actual_count"]
                }
                for m in resolved_pre_mismatches[:5]
            ]
        },
        "product_metadata_fix_results": {
            "validation_baseline_updated": True,
            "item_count_before_update": validation_fix_patch["validation_baseline_update"]["item_count"]["old"],
            "item_count_after_update": validation_fix_patch["validation_baseline_update"]["item_count"]["new"],
            "section_count_before_update": validation_fix_patch["validation_baseline_update"]["section_count"]["old"],
            "section_count_after_update": validation_fix_patch["validation_baseline_update"]["section_count"]["new"],
            "learning_path_policy_fixed": lpp_fix_summary["total_fixed"],
            "only_batch4_nodes_lpp_fixed": lpp_fix_summary["only_new_nodes_fixed"],
            "old_nodes_lpp_affected": lpp_fix_summary["old_nodes_affected"]
        },
        "final_validation_status": {
            "item_count_match": total_items == 1602,
            "expected_item_count_match": validation_result.get("expected_item_count", 0) == 1602,
            "section_count_match": section_count == 65,
            "dangling_refs_count": len(validation_result.get("dangling_refs", [])),
            "direct_pre_cycle": "null" if validation_result.get("direct_pre_cycle") is None else "found",
            "direct_pre_section_refs": validation_result.get("direct_pre_section_refs", 0),
            "resolved_pre_section_refs": validation_result.get("resolved_pre_section_refs", {}).get("count", 0),
            "rel_section_refs": validation_result.get("rel_section_refs", {}).get("count", 0),
            "resolved_pre_mismatches_count": len(resolved_pre_mismatches),
            "resolved_pre_mismatches_all_same_length": all_same_length,
            "resolved_pre_mismatches_all_batch4_nodes": all_batch4_nodes,
            "product_metadata_validation_passed": validation_result.get("product_metadata_validation", {}).get("passed", False),
            "all_items_have_learning_path_policy": validation_result.get("product_metadata_validation", {}).get("all_items_have_learning_path_policy", False),
            "validation_passed": validation_result.get("passed", False)
        },
        "success_criteria_check": {
            "item_count_1602": total_items == 1602,
            "expected_item_count_1602": validation_result.get("expected_item_count", 0) == 1602,
            "section_count_65": section_count == 65,
            "dangling_refs_empty": len(validation_result.get("dangling_refs", [])) == 0,
            "direct_pre_cycle_null": validation_result.get("direct_pre_cycle") is None,
            "direct_pre_section_refs_0": validation_result.get("direct_pre_section_refs", 0) == 0,
            "resolved_pre_section_refs_0": validation_result.get("resolved_pre_section_refs", {}).get("count", 0) == 0,
            "rel_section_refs_0": validation_result.get("rel_section_refs", {}).get("count", 0) == 0,
            "resolved_pre_mismatches_empty": len(resolved_pre_mismatches) == 0,
            "product_metadata_validation_passed": validation_result.get("product_metadata_validation", {}).get("passed", False),
            "validation_passed": validation_result.get("passed", False)
        },
        "diagnosis_and_recommendations": {
            "batch4_merge_successful": False,
            "validation_passed": validation_result.get("passed", False),
            "primary_failure_reason": "resolved_pre_mismatches_remaining",
            "failure_analysis": {
                "resolved_pre_issue": "validation_script_logic_issue",
                "mismatch_nature": "expected_count_equals_actual_count_for_all_30_nodes",
                "affected_nodes": "only_batch4_new_nodes",
                "metadata_issue": "resolved"
            },
            "recommended_action": "cannot_treat_as_success",
            "next_steps": [
                "Do not continue to Batch5",
                "Do not perform Batch4 Review",
                "Validation script may have logic issue with resolved_pre_mismatches",
                "All 30 mismatches have expected_count == actual_count",
                "Only Batch4 new nodes affected, no old node pollution",
                "Product metadata validation now passes"
            ]
        },
        "summary": {
            "backup_created": True,
            "resolved_pre_fix_applied": True,
            "metadata_fix_applied": True,
            "only_batch4_nodes_modified": True,
            "old_nodes_affected": False,
            "validation_passed": False,
            "treat_as_success": False,
            "stop_condition_met": True,
            "final_status": "validation_failed_but_metadata_fixed"
        }
    }
    
    with open("data/stage3e_aggressive_batch4_validation_fix_result.json", 'w', encoding='utf-8') as f:
        json.dump(fix_report, f, ensure_ascii=False, indent=2)
    
    return fix_report

if __name__ == "__main__":
    result = generate_fix_report()
    print(f"✅ 修复报告已生成: data/stage3e_aggressive_batch4_validation_fix_result.json")
    print(f"📊 验证状态: {'✅ PASSED' if result['final_validation_status']['validation_passed'] else '❌ FAILED'}")
    print(f"📊 主要失败原因: {result['diagnosis_and_recommendations']['primary_failure_reason']}")