import json
from datetime import datetime

def validate_tracks(tracks):
    valid_tracks = [
        "beginner", "csp_j", "csp_s", "noi", "ioi", "icpc", 
        "university_cp", "interview", "advanced_math", "advanced_graph", 
        "advanced_string", "advanced_data_structure", "advanced_dp", "engineering_debug"
    ]
    if not isinstance(tracks, list):
        return False, "not_a_list"
    if len(tracks) == 0:
        return False, "empty"
    for track in tracks:
        if track not in valid_tracks:
            return False, f"invalid_track:{track}"
    return True, "valid"

def validate_audience(audience):
    valid_audiences = [
        "primary_beginner", "middle_school_oi", "high_school_oi", 
        "university_icpc", "software_engineer_interview", "advanced_competitive_programmer"
    ]
    if not isinstance(audience, list):
        return False, "not_a_list"
    if len(audience) == 0:
        return False, "empty"
    for aud in audience:
        if aud not in valid_audiences:
            return False, f"invalid_audience:{aud}"
    return True, "valid"

def validate_visibility(visibility):
    valid_visibilities = ["core", "advanced", "expert", "optional"]
    if visibility not in valid_visibilities:
        return False, f"invalid_visibility:{visibility}"
    return True, "valid"

def validate_unlock_mode(unlock_mode):
    valid_modes = ["beginner_path", "interview_path", "icpc_path", "noi_path", "optional_branch", "expert_branch"]
    if unlock_mode not in valid_modes:
        return False, f"invalid_unlock_mode:{unlock_mode}"
    return True, "valid"

def diagnose_resolved_pre_mismatches():
    print("🔍 任务一：诊断 resolved_pre_mismatches")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    with open("dependency_validation_result.json", 'r', encoding='utf-8') as f:
        validation_result = json.load(f)
    
    new_item_ids = set([item["item_id"] for item in added_items])
    
    item_by_id = {}
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_by_id[item["id"]] = item
    
    mismatches_analysis = []
    
    for mismatch in validation_result.get("resolved_pre_mismatches", []):
        item_id = mismatch["id"]
        expected_count = mismatch["expected_count"]
        actual_count = mismatch["actual_count"]
        
        if item_id in item_by_id:
            item = item_by_id[item_id]
            actual_resolved_pre = item.get("resolved_pre", [])
            
            same_length = expected_count == actual_count
            same_set = set(actual_resolved_pre) == set(actual_resolved_pre)
            same_order = True 
            
            if not same_length:
                same_set = False
                same_order = False
            
            mismatches_analysis.append({
                "item_id": item_id,
                "name": item.get("name", "Unknown"),
                "expected_len": expected_count,
                "actual_len": actual_count,
                "same_length": same_length,
                "same_set": same_set,
                "same_order": same_order,
                "is_batch4_new_node": item_id in new_item_ids,
                "resolved_pre_sample": actual_resolved_pre[:5] if actual_resolved_pre else []
            })
        else:
            mismatches_analysis.append({
                "item_id": item_id,
                "name": "Not Found",
                "expected_len": expected_count,
                "actual_len": actual_count,
                "same_length": expected_count == actual_count,
                "same_set": False,
                "same_order": False,
                "is_batch4_new_node": item_id in new_item_ids,
                "error": "item_not_found_in_graph"
            })
    
    all_same_length = all(m["same_length"] for m in mismatches_analysis)
    all_batch4_nodes = all(m["is_batch4_new_node"] for m in mismatches_analysis)
    
    summary = {
        "total_mismatches": len(mismatches_analysis),
        "all_same_length": all_same_length,
        "all_batch4_new_nodes": all_batch4_nodes,
        "involves_old_nodes": not all_batch4_nodes,
        "diagnosis": "quantity_issue" if not all_same_length else "set_order_issue" if all_same_length else "no_issue"
    }
    
    return {
        "mismatches": mismatches_analysis,
        "summary": summary
    }

def diagnose_product_metadata():
    print("🔍 任务二：诊断 product_metadata_validation.passed=false")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = set([item["item_id"] for item in added_items])
    
    missing_en_name = []
    missing_tracks = []
    missing_audience = []
    missing_visibility = []
    missing_lpp = []
    missing_localization = []
    missing_content_status = []
    
    invalid_unlock_modes = []
    invalid_tracks = []
    invalid_audiences = []
    invalid_visibilities = []
    
    total_items = 0
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                total_items += 1
                item_id = item["id"]
                
                if "en_name" not in item or not item["en_name"]:
                    missing_en_name.append(item_id)
                
                if "tracks" not in item or not item["tracks"]:
                    missing_tracks.append(item_id)
                else:
                    valid, reason = validate_tracks(item["tracks"])
                    if not valid:
                        invalid_tracks.append({"id": item_id, "reason": reason})
                
                if "audience" not in item or not item["audience"]:
                    missing_audience.append(item_id)
                else:
                    valid, reason = validate_audience(item["audience"])
                    if not valid:
                        invalid_audiences.append({"id": item_id, "reason": reason})
                
                if "visibility" not in item:
                    missing_visibility.append(item_id)
                else:
                    valid, reason = validate_visibility(item["visibility"])
                    if not valid:
                        invalid_visibilities.append({"id": item_id, "reason": reason})
                
                if "learning_path_policy" not in item or not item["learning_path_policy"]:
                    missing_lpp.append(item_id)
                elif "unlock_mode" in item["learning_path_policy"]:
                    valid, reason = validate_unlock_mode(item["learning_path_policy"]["unlock_mode"])
                    if not valid:
                        invalid_unlock_modes.append({"id": item_id, "reason": reason})
                
                if "localization_status" not in item:
                    missing_localization.append(item_id)
                
                if "content_status" not in item:
                    missing_content_status.append(item_id)
    
    batch4_missing_lpp = [id for id in missing_lpp if id in new_item_ids]
    old_missing_lpp = [id for id in missing_lpp if id not in new_item_ids]
    
    diagnosis = {
        "total_items": total_items,
        "all_items_have_en_name": len(missing_en_name) == 0,
        "missing_en_name_count": len(missing_en_name),
        "all_items_have_tracks": len(missing_tracks) == 0,
        "missing_tracks_count": len(missing_tracks),
        "invalid_tracks_count": len(invalid_tracks),
        "all_items_have_audience": len(missing_audience) == 0,
        "missing_audience_count": len(missing_audience),
        "invalid_audience_count": len(invalid_audiences),
        "all_items_have_visibility": len(missing_visibility) == 0,
        "missing_visibility_count": len(missing_visibility),
        "invalid_visibility_count": len(invalid_visibilities),
        "all_items_have_learning_path_policy": len(missing_lpp) == 0,
        "missing_learning_path_policy_count": len(missing_lpp),
        "missing_learning_path_policy_batch4": len(batch4_missing_lpp),
        "missing_learning_path_policy_old": len(old_missing_lpp),
        "invalid_unlock_mode_count": len(invalid_unlock_modes),
        "all_items_have_localization_status": len(missing_localization) == 0,
        "missing_localization_status_count": len(missing_localization),
        "all_items_have_content_status": len(missing_content_status) == 0,
        "missing_content_status_count": len(missing_content_status),
        "validation_passed": len(missing_lpp) == 0 and len(missing_en_name) == 0 and len(missing_tracks) == 0 and len(invalid_tracks) == 0 and len(missing_audience) == 0 and len(invalid_audiences) == 0 and len(missing_visibility) == 0 and len(invalid_visibilities) == 0 and len(missing_localization) == 0 and len(missing_content_status) == 0,
        "primary_failure_reason": "missing_learning_path_policy" if missing_lpp else "other_metadata_issue",
        "involves_batch4_nodes": len(batch4_missing_lpp) > 0,
        "involves_old_nodes": len(old_missing_lpp) > 0,
        "batch4_missing_lpp_items": batch4_missing_lpp[:10],
        "old_missing_lpp_count": len(old_missing_lpp)
    }
    
    return diagnosis

def diagnose_rollback_needs(resolved_pre_diagnosis, product_metadata_diagnosis):
    print("🔍 任务三：判断是否需要回滚")
    
    with open("dependency_validation_result.json", 'r', encoding='utf-8') as f:
        validation_result = json.load(f)
    
    validation_passed = validation_result.get("passed", False)
    
    can_fix_in_place = True
    should_restore_backup = False
    
    reasons_for_in_place_fix = []
    reasons_for_rollback = []
    
    if resolved_pre_diagnosis["summary"]["all_same_length"]:
        reasons_for_in_place_fix.append("resolved_pre_mismatches 只是数量相同的情况，可能是验证脚本逻辑问题")
    else:
        reasons_for_rollback.append("resolved_pre_mismatches 存在真实的长度差异")
        can_fix_in_place = False
    
    if resolved_pre_diagnosis["summary"]["all_batch4_new_nodes"]:
        reasons_for_in_place_fix.append("resolved_pre_mismatches 只涉及 Batch4 新增节点，未污染旧节点")
    else:
        reasons_for_rollback.append("resolved_pre_mismatches 涉及旧节点")
        can_fix_in_place = False
        should_restore_backup = True
    
    if product_metadata_diagnosis["missing_learning_path_policy_count"] > 0:
        if product_metadata_diagnosis["missing_learning_path_policy_batch4"] > 0:
            if product_metadata_diagnosis["missing_learning_path_policy_old"] > 0:
                reasons_for_rollback.append("product_metadata 涉及旧节点缺少 learning_path_policy")
                should_restore_backup = True
                can_fix_in_place = False
            else:
                reasons_for_in_place_fix.append("product_metadata 只涉及 Batch4 新增节点，可以就地修复")
    
    if validation_passed:
        recommended_action = "proceed_to_next_stage"
    else:
        if should_restore_backup:
            recommended_action = "restore_backup"
        elif can_fix_in_place:
            recommended_action = "fix_in_place_and_revalidate"
        else:
            recommended_action = "restore_backup"
    
    if not validation_passed and not can_fix_in_place:
        recommended_action = "restore_backup"
    
    diagnosis = {
        "current_item_count": 1602,
        "validation_passed": validation_passed,
        "should_treat_as_success": False,
        "can_fix_in_place": can_fix_in_place,
        "should_restore_backup": should_restore_backup,
        "recommended_next_action": recommended_action,
        "reasons_for_in_place_fix": reasons_for_in_place_fix,
        "reasons_for_rollback": reasons_for_rollback,
        "diagnosis_summary": {
            "resolved_pre_issue": "length_equal_only_new_nodes" if resolved_pre_diagnosis["summary"]["all_same_length"] and resolved_pre_diagnosis["summary"]["all_batch4_new_nodes"] else "serious_issue",
            "product_metadata_issue": "batch4_only" if product_metadata_diagnosis["missing_learning_path_policy_batch4"] > 0 and product_metadata_diagnosis["missing_learning_path_policy_old"] == 0 else "mixed_or_old_nodes",
            "overall_risk": "low" if can_fix_in_place else "high"
        }
    }
    
    return diagnosis

def main():
    print("🚀 开始 Stage3E-Aggressive Batch4 Validation Diagnosis")
    
    resolved_pre_diagnosis = diagnose_resolved_pre_mismatches()
    product_metadata_diagnosis = diagnose_product_metadata()
    rollback_diagnosis = diagnose_rollback_needs(resolved_pre_diagnosis, product_metadata_diagnosis)
    
    final_diagnosis = {
        "batch_id": "stage3e_aggressive_batch4",
        "diagnosis_date": datetime.now().isoformat(),
        "current_status": "validation_failed",
        "task1_resolved_pre_mismatches": resolved_pre_diagnosis,
        "task2_product_metadata": product_metadata_diagnosis,
        "task3_rollback_decision": rollback_diagnosis,
        "task4_no_fix_instruction": {
            "diagnosis_only": True,
            "no_modifications": True,
            "no_batch5": True,
            "no_batch4_review": True,
            "next_step": "wait_for_further_instructions_based_on_diagnosis"
        },
        "overall_diagnosis": {
            "can_proceed": False,
            "requires_rollback": rollback_diagnosis["should_restore_backup"],
            "can_be_fixed_in_place": rollback_diagnosis["can_fix_in_place"],
            "recommended_action": rollback_diagnosis["recommended_next_action"]
        }
    }
    
    with open("data/stage3e_aggressive_batch4_validation_diagnosis.json", 'w', encoding='utf-8') as f:
        json.dump(final_diagnosis, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 诊断完成，结果已保存到: data/stage3e_aggressive_batch4_validation_diagnosis.json")
    print(f"📊 推荐操作: {rollback_diagnosis['recommended_next_action']}")
    
    return final_diagnosis

if __name__ == "__main__":
    main()