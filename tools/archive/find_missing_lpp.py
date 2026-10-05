import json

def find_missing_lpp():
    print("🔍 详细检查所有节点的 learning_path_policy...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    missing_lpp = []
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if "learning_path_policy" not in item:
                    missing_lpp.append({
                        "id": item["id"],
                        "name": item["name"],
                        "section": section["id"]
                    })
    
    print(f"❌ 总共缺少 learning_path_policy 的节点数: {len(missing_lpp)}")
    
    if missing_lpp:
        print("缺少 learning_path_policy 的节点:")
        for item in missing_lpp[:10]:
            print(f"  - {item['id']}: {item['name']} (section: {item['section']})")
        if len(missing_lpp) > 10:
            print(f"  ... 还有 {len(missing_lpp) - 10} 个")
    
    return missing_lpp

if __name__ == "__main__":
    missing = find_missing_lpp()