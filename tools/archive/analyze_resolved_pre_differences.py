import json
import copy

def build_item_map(data):
    """构建 item_id -> item 映射"""
    item_by_id = {}
    section_by_id = {}

    for cat in data.get('categories', []):
        for section in cat.get('sections', []):
            section_by_id[section['id']] = section
            for item in section.get('items', []):
                item_by_id[item['id']] = item

    return item_by_id, section_by_id

def analyze_missing_dependencies(item_by_id, section_by_id):
    """分析缺失的依赖"""

    # 2.21.44 的 resolved_pre
    item_2_21_44 = item_by_id.get("2.21.44")
    if item_2_21_44:
        resolved_pre_2_21_44 = set(item_2_21_44.get('resolved_pre', []))
        print(f"2.21.44 的 resolved_pre 数量: {len(resolved_pre_2_21_44)}")
    else:
        resolved_pre_2_21_44 = set()
        print("2.21.44 不存在")

    # 分析 Dynamic MST 系列
    print("\n=== Dynamic MST 系列 ===")
    dynamic_mst_nodes = ["2.21.88", "2.21.89", "2.21.90", "2.21.91", "2.21.92", "2.21.93"]

    for node_id in dynamic_mst_nodes:
        item = item_by_id.get(node_id)
        if item:
            current_resolved_pre = set(item.get('resolved_pre', []))
            direct_pre = item.get('direct_pre', [])

            print(f"\n{node_id} ({item['name']}):")
            print(f"  direct_pre: {direct_pre}")
            print(f"  当前 resolved_pre 数量: {len(current_resolved_pre)}")

            # 找出缺失的来自 2.21.44 的依赖
            missing_from_2_21_44 = resolved_pre_2_21_44 - current_resolved_pre
            if missing_from_2_21_44:
                print(f"  缺失的 2.21.44 依赖: {sorted(list(missing_from_2_21_44))}")
            else:
                print(f"  不缺失 2.21.44 的依赖")

    # 分析 Global Min-Cut 系列
    print("\n=== Global Min-Cut 系列 ===")
    item_2_21_45 = item_by_id.get("2.21.45")
    if item_2_21_45:
        resolved_pre_2_21_45 = set(item_2_21_45.get('resolved_pre', []))
        print(f"2.21.45 的 resolved_pre 数量: {len(resolved_pre_2_21_45)}")
    else:
        resolved_pre_2_21_45 = set()
        print("2.21.45 不存在")

    global_min_cut_nodes = ["2.21.96", "2.21.97", "2.21.98"]

    for node_id in global_min_cut_nodes:
        item = item_by_id.get(node_id)
        if item:
            current_resolved_pre = set(item.get('resolved_pre', []))
            direct_pre = item.get('direct_pre', [])

            print(f"\n{node_id} ({item['name']}):")
            print(f"  direct_pre: {direct_pre}")
            print(f"  当前 resolved_pre 数量: {len(current_resolved_pre)}")

            # 找出缺失的来自 2.21.45 的依赖
            missing_from_2_21_45 = resolved_pre_2_21_45 - current_resolved_pre
            if missing_from_2_21_45:
                print(f"  缺失的 2.21.45 依赖: {sorted(list(missing_from_2_21_45))}")
            else:
                print(f"  不缺失 2.21.45 的依赖")

    # 分析 Directed MST 系列
    print("\n=== Directed MST 系列 ===")
    item_2_21_77 = item_by_id.get("2.21.77")
    item_2_21_78 = item_by_id.get("2.21.78")

    if item_2_21_77 and item_2_21_78:
        resolved_pre_2_21_77 = set(item_2_21_77.get('resolved_pre', []))
        resolved_pre_2_21_78 = set(item_2_21_78.get('resolved_pre', []))
        combined_resolved_pre = resolved_pre_2_21_77 | resolved_pre_2_21_78
        print(f"2.21.77 的 resolved_pre 数量: {len(resolved_pre_2_21_77)}")
        print(f"2.21.78 的 resolved_pre 数量: {len(resolved_pre_2_21_78)}")
        print(f"合并后的 resolved_pre 数量: {len(combined_resolved_pre)}")
    else:
        combined_resolved_pre = set()
        print("2.21.77 或 2.21.78 不存在")

    directed_mst_nodes = ["2.21.81"]

    for node_id in directed_mst_nodes:
        item = item_by_id.get(node_id)
        if item:
            current_resolved_pre = set(item.get('resolved_pre', []))
            direct_pre = item.get('direct_pre', [])

            print(f"\n{node_id} ({item['name']}):")
            print(f"  direct_pre: {direct_pre}")
            print(f"  当前 resolved_pre 数量: {len(current_resolved_pre)}")

            # 找出缺失的来自 2.21.77 和 2.21.78 的依赖
            missing_from_directed = combined_resolved_pre - current_resolved_pre
            if missing_from_directed:
                print(f"  缺失的 2.21.77/2.21.78 依赖: {sorted(list(missing_from_directed))}")
            else:
                print(f"  不缺失 2.21.77/2.21.78 的依赖")

def main():
    print("分析 Stage3E-Batch1 Resolved Pre 差异...")

    # 读取主图谱
    print("读取主图谱...")
    with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 构建映射
    print("构建映射...")
    item_by_id, section_by_id = build_item_map(data)

    # 分析差异
    analyze_missing_dependencies(item_by_id, section_by_id)

if __name__ == "__main__":
    main()