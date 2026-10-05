import json

def check_all_nodes_lpp():
    print("🔍 检查所有节点的 learning_path_policy...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    new_item_ids = set([item["item_id"] for item in added_items])
    
    missing_lpp_old = []
    missing_lpp_new = []
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if "learning_path_policy" not in item:
                    if item["id"] in new_item_ids:
                        missing_lpp_new.append(item["id"])
                    else:
                        missing_lpp_old.append(item["id"])
    
    print(f"❌ 旧节点缺少 learning_path_policy: {len(missing_lpp_old)}")
    if missing_lpp_old:
        print("   示例:", missing_lpp_old[:5])
    
    print(f"❌ 新节点缺少 learning_path_policy: {len(missing_lpp_new)}")
    if missing_lpp_new:
        print("   示例:", missing_lpp_new[:5])
    
    print(f"📊 总节点数: {sum(len(s['items']) for c in graph['categories'] for s in c['sections'])}")
    print(f"📊 新增节点数: {len(new_item_ids)}")
    
    all_good = len(missing_lpp_new) == 0
    print(f"{'✅' if all_good else '❌'} 新增节点检查结果: {'所有新增节点都有 learning_path_policy' if all_good else '存在新增节点缺少 learning_path_policy'}")
    
    return len(missing_lpp_old), len(missing_lpp_new)

if __name__ == "__main__":
    old_missing, new_missing = check_all_nodes_lpp()