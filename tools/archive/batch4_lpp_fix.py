import json
from datetime import datetime

def batch4_learning_path_policy_fix():
    print("🔧 修复 Batch4 新增节点的 learning_path_policy...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = set([item["item_id"] for item in added_items])
    
    required_fields = {
        "show_in_beginner_path", 
        "show_in_interview_path", 
        "show_in_icpc_path",
        "show_in_noi_path", 
        "unlock_mode"
    }
    
    fixed_items = []
    old_node_modified = False
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                
                if item_id in new_item_ids:
                    old_lpp = item.get("learning_path_policy", {}).copy()
                    
                    if "learning_path_policy" not in item or not item["learning_path_policy"]:
                        item["learning_path_policy"] = {}
                    
                    current_fields = set(item["learning_path_policy"].keys())
                    missing_fields = required_fields - current_fields
                    
                    if missing_fields:
                        for field in missing_fields:
                            if field == "show_in_beginner_path":
                                item["learning_path_policy"][field] = False
                            elif field == "show_in_interview_path":
                                item["learning_path_policy"][field] = False
                            elif field == "show_in_icpc_path":
                                item["learning_path_policy"][field] = True
                            elif field == "show_in_noi_path":
                                item["learning_path_policy"][field] = True
                            elif field == "unlock_mode":
                                item["learning_path_policy"][field] = "expert_branch"
                        
                        fixed_items.append({
                            "item_id": item_id,
                            "name": item["name"],
                            "old_lpp": old_lpp,
                            "new_lpp": item["learning_path_policy"],
                            "missing_fields": list(missing_fields)
                        })
                else:
                    if "learning_path_policy" not in item or not item["learning_path_policy"]:
                        old_node_modified = True
                        print(f"❌ 旧节点 {item_id} 缺少 learning_path_policy")
    
    print(f"✅ 修复了 {len(fixed_items)} 个 Batch4 新增节点的 learning_path_policy")
    print(f"✅ 旧节点未受影响: {not old_node_modified}")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    fix_summary = {
        "fix_applied_at": datetime.now().isoformat(),
        "batch_id": "stage3e_aggressive_batch4_learning_path_policy_fix",
        "required_fields": list(required_fields),
        "fixed_items": fixed_items,
        "total_fixed": len(fixed_items),
        "only_new_nodes_fixed": not old_node_modified,
        "old_nodes_affected": old_node_modified
    }
    
    with open("data/stage3e_aggressive_batch4_lpp_fix_summary.json", 'w', encoding='utf-8') as f:
        json.dump(fix_summary, f, ensure_ascii=False, indent=2)
    
    print("✅ learning_path_policy 修复完成")
    
    return fix_summary

if __name__ == "__main__":
    batch4_learning_path_policy_fix()