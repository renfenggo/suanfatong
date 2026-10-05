import json

def check_learning_path_policy_details():
    print("🔍 详细检查 learning_path_policy...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = set([item["item_id"] for item in added_items])
    
    missing_lpp = []
    incomplete_lpp = []
    invalid_unlock_mode = []
    missing_optional_field = []
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                
                if "learning_path_policy" not in item or not item["learning_path_policy"]:
                    missing_lpp.append(item_id)
                else:
                    lpp = item["learning_path_policy"]
                    
                    if "unlock_mode" not in lpp or not lpp["unlock_mode"]:
                        incomplete_lpp.append({
                            "item_id": item_id,
                            "missing_field": "unlock_mode"
                        })
                    
                    if "optional" not in lpp:
                        incomplete_lpp.append({
                            "item_id": item_id,
                            "missing_field": "optional"
                        })
                    
                    if "path_order" not in lpp:
                        incomplete_lpp.append({
                            "item_id": item_id,
                            "missing_field": "path_order"
                        })
    
    print(f"❌ 完全缺少 learning_path_policy 的节点: {len(missing_lpp)}")
    if missing_lpp:
        print("示例:", missing_lpp[:5])
    
    print(f"❌ learning_path_policy 缺少字段的节点: {len(incomplete_lpp)}")
    if incomplete_lpp:
        print("示例:", incomplete_lpp[:5])
    
    print(f"📊 总节点数: 1602")
    print(f"📊 新增节点数: {len(new_item_ids)}")
    
    return {
        "missing_lpp_count": len(missing_lpp),
        "incomplete_lpp_count": len(incomplete_lpp),
        "missing_lpp_nodes": missing_lpp[:10],
        "incomplete_lpp_nodes": incomplete_lpp[:10],
        "all_good": len(missing_lpp) == 0 and len(incomplete_lpp) == 0
    }

if __name__ == "__main__":
    check_learning_path_policy_details()