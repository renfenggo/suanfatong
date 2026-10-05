import json

def fix_unlock_modes():
    print("🔧 修复新增节点的 unlock_mode...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = [item["item_id"] for item in added_items]
    
    fixed_count = 0
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if item["id"] in new_item_ids:
                    if item.get("learning_path_policy", {}).get("unlock_mode") != "expert_branch":
                        item["learning_path_policy"]["unlock_mode"] = "expert_branch"
                        fixed_count += 1
    
    print(f"✅ 修复了 {fixed_count} 个节点的 unlock_mode")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    print("✅ 主图谱已更新")

if __name__ == "__main__":
    fix_unlock_modes()