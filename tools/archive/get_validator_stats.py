import json

def get_validator_stats():
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    direct_pre_nonempty = 0
    direct_pre_ref_count = 0
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if item.get("direct_pre"):
                    direct_pre_nonempty += 1
                    direct_pre_ref_count += len(item.get("direct_pre", []))
    
    print(f"📊 Validator 统计:")
    print(f"   direct_pre_nonempty: {direct_pre_nonempty}")
    print(f"   direct_pre_ref_count: {direct_pre_ref_count}")
    print(f"   direct_pre_item_ref_ratio: {direct_pre_ref_count / direct_pre_nonempty:.6f}")

if __name__ == "__main__":
    get_validator_stats()