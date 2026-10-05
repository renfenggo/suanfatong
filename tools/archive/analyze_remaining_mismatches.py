import json

def build_item_map(data):
    """构建 item_id -> item 映射"""
    item_by_id = {}
    for cat in data.get('categories', []):
        for section in cat.get('sections', []):
            for item in section.get('items', []):
                item_by_id[item['id']] = item
    return item_by_id

def analyze_remaining_mismatches():
    """分析剩余的 mismatches"""

    print("读取主图谱...")
    with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    item_by_id = build_item_map(data)

    # 分析 Dynamic MST 节点还缺什么
    print("=== Dynamic MST 节点还缺什么 ===")
    item_2_21_44 = item_by_id.get("2.21.44")
    if item_2_21_44:
        resolved_pre_2_21_44 = set(item_2_21_44.get('resolved_pre', []))
        print(f"2.21.44 的 resolved_pre: {sorted(list(resolved_pre_2_21_44))}")

    dynamic_nodes = ["2.21.88", "2.21.89", "2.21.90", "2.21.91", "2.21.92", "2.21.93"]
    for node_id in dynamic_nodes:
        item = item_by_id.get(node_id)
        if item:
            current_resolved_pre = set(item.get('resolved_pre', []))
            missing = resolved_pre_2_21_44 - current_resolved_pre
            if missing:
                print(f"{node_id} 还缺: {sorted(list(missing))}")
            else:
                print(f"{node_id}: 已包含所有 2.21.44 依赖")

    # 分析 Global Min-Cut 节点还缺什么
    print("\n=== Global Min-Cut 节点还缺什么 ===")
    item_2_21_45 = item_by_id.get("2.21.45")
    if item_2_21_45:
        resolved_pre_2_21_45 = set(item_2_21_45.get('resolved_pre', []))
        print(f"2.21.45 的 resolved_pre: {sorted(list(resolved_pre_2_21_45))}")

    global_nodes = ["2.21.96", "2.21.97", "2.21.98"]
    for node_id in global_nodes:
        item = item_by_id.get(node_id)
        if item:
            current_resolved_pre = set(item.get('resolved_pre', []))
            missing = resolved_pre_2_21_45 - current_resolved_pre
            if missing:
                print(f"{node_id} 还缺: {sorted(list(missing))}")
            else:
                print(f"{node_id}: 已包含所有 2.21.45 依赖")

    # 分析 Directed MST 节点还缺什么
    print("\n=== Directed MST 节点还缺什么 ===")
    item_2_21_77 = item_by_id.get("2.21.77")
    item_2_21_78 = item_by_id.get("2.21.78")

    if item_2_21_77 and item_2_21_78:
        resolved_pre_2_21_77 = set(item_2_21_77.get('resolved_pre', []))
        resolved_pre_2_21_78 = set(item_2_21_78.get('resolved_pre', []))
        combined = resolved_pre_2_21_77 | resolved_pre_2_21_78
        print(f"2.21.77 的 resolved_pre: {sorted(list(resolved_pre_2_21_77))}")
        print(f"2.21.78 的 resolved_pre: {sorted(list(resolved_pre_2_21_78))}")
        print(f"合并: {sorted(list(combined))}")

        item_2_21_81 = item_by_id.get("2.21.81")
        if item_2_21_81:
            current_resolved_pre = set(item_2_21_81.get('resolved_pre', []))
            missing = combined - current_resolved_pre
            if missing:
                print(f"2.21.81 还缺: {sorted(list(missing))}")
            else:
                print(f"2.21.81: 已包含所有 2.21.77/2.21.78 依赖")

if __name__ == "__main__":
    analyze_remaining_mismatches()