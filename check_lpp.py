import json

def check_learning_path_policies():
    print("🔍 检查新增节点的 learning_path_policy...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = [item["item_id"] for item in added_items]
    
    missing_lpp = []
    wrong_unlock_mode = []
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if item["id"] in new_item_ids:
                    if "learning_path_policy" not in item:
                        missing_lpp.append(item["id"])
                    elif item["learning_path_policy"].get("unlock_mode") != "expert_branch":
                        wrong_unlock_mode.append({
                            "id": item["id"],
                            "actual_mode": item["learning_path_policy"].get("unlock_mode")
                        })
    
    print(f"❌ 缺少 learning_path_policy 的节点: {len(missing_lpp)}")
    if missing_lpp:
        for item_id in missing_lpp:
            print(f"   - {item_id}")
    
    print(f"❌ unlock_mode 不为 expert_branch 的节点: {len(wrong_unlock_mode)}")
    if wrong_unlock_mode:
        for item in wrong_unlock_mode:
            print(f"   - {item['id']}: {item['actual_mode']}")
    
    all_good = len(missing_lpp) == 0 and len(wrong_unlock_mode) == 0
    print(f"{'✅' if all_good else '❌'} 检查结果: {'所有新增节点配置正确' if all_good else '存在配置问题'}")
    
    return all_good

if __name__ == "__main__":
    check_learning_path_policies()