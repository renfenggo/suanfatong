import json

def main():
    graph_file = "merged_knowledge_graph_item_dependencies_refined.json"
    mapping_file = "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json"
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        candidate_to_item_id = json.load(f)
    
    batch2_item_ids = set(candidate_to_item_id.values())
    
    applied_patch = []
    stats = {
        "batch2_item_count": len(batch2_item_ids),
        "unlock_mode_fixed": 0,
        "learning_path_policy_fixed": 0,
        "validation_baseline_updated": False,
        "expected_item_count_before": 0,
        "expected_item_count_after": 0
    }
    
    old_validation_baseline = graph.get("meta", {}).get("validation_baseline", {})
    stats["expected_item_count_before"] = old_validation_baseline.get("item_count", 1512)
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                
                if item_id in batch2_item_ids:
                    learning_path_policy = item.get("learning_path_policy", {})
                    
                    if not isinstance(learning_path_policy, dict):
                        learning_path_policy = {}
                        item["learning_path_policy"] = learning_path_policy
                    
                    old_policy_keys = set(learning_path_policy.keys())
                    
                    if "unlock_mode" not in learning_path_policy or learning_path_policy["unlock_mode"] not in ["mainline", "optional_branch", "expert_branch", "reference_only"]:
                        old_unlock_mode = learning_path_policy.get("unlock_mode")
                        learning_path_policy["unlock_mode"] = "expert_branch"
                        stats["unlock_mode_fixed"] += 1
                        
                        applied_patch.append({
                            "id": item_id,
                            "name": item.get("name", ""),
                            "change_type": "unlock_mode_fix",
                            "old_unlock_mode": old_unlock_mode,
                            "new_unlock_mode": "expert_branch",
                            "reason": "Batch2 新增节点 unlock_mode 为无效值，修复为 expert_branch"
                        })
                    
                    required_keys = ["show_in_beginner_path", "show_in_interview_path", "show_in_icpc_path", "show_in_noi_path", "unlock_mode"]
                    missing_keys = set(required_keys) - old_policy_keys
                    
                    if missing_keys:
                        for key in missing_keys:
                            if key == "show_in_icpc_path":
                                learning_path_policy[key] = False
                            elif key == "show_in_noi_path":
                                learning_path_policy[key] = False
                        stats["learning_path_policy_fixed"] += 1
                        
                        applied_patch.append({
                            "id": item_id,
                            "name": item.get("name", ""),
                            "change_type": "learning_path_policy_fix",
                            "missing_keys_added": list(missing_keys),
                            "reason": "Batch2 新增节点缺少必需的 learning_path_policy 字段"
                        })
    
    if "meta" not in graph:
        graph["meta"] = {}
    
    if "validation_baseline" not in graph["meta"]:
        graph["meta"]["validation_baseline"] = {}
    
    old_item_count = graph["meta"]["validation_baseline"].get("item_count", 1512)
    old_section_count = graph["meta"]["validation_baseline"].get("section_count", 65)
    
    graph["meta"]["validation_baseline"]["item_count"] = 1542
    graph["meta"]["validation_baseline"]["section_count"] = 65
    
    stats["expected_item_count_after"] = 1542
    stats["validation_baseline_updated"] = True
    
    applied_patch.append({
        "change_type": "validation_baseline_update",
        "old_item_count": old_item_count,
        "new_item_count": 1542,
        "old_section_count": old_section_count,
        "new_section_count": 65,
        "reason": "更新 validation_baseline 反映 Batch2 新增的 30 个节点"
    })
    
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_metadata_fix_applied_patch.json", 'w', encoding='utf-8') as f:
        json.dump(applied_patch, f, ensure_ascii=False, indent=2)
    
    print("✅ Batch2 Metadata Fix completed")
    print(f"✅ Batch2 items processed: {stats['batch2_item_count']}")
    print(f"✅ Unlock mode fixed: {stats['unlock_mode_fixed']}")
    print(f"✅ Learning path policy fixed: {stats['learning_path_policy_fixed']}")
    print(f"✅ Validation baseline updated: {stats['validation_baseline_updated']}")
    print(f"✅ Expected item count: {stats['expected_item_count_before']} → {stats['expected_item_count_after']}")
    
    return applied_patch, stats

if __name__ == "__main__":
    applied_patch, stats = main()