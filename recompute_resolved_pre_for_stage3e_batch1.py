import json
from collections import deque

# 需要修复的 10 个节点
TARGET_NODES = [
    "2.21.88",  # Dynamic MST: Batch Recomputation
    "2.21.89",  # Dynamic MST: Certificate Graph
    "2.21.90",  # Dynamic MST: Divide Conquer Approach
    "2.21.91",  # Dynamic MST: Edge Deletion
    "2.21.92",  # Dynamic MST: Edge Insertion
    "2.21.93",  # Dynamic MST: Sensitivity Analysis
    "2.21.96",  # Global Min-Cut: Random Contraction
    "2.21.97",  # Global Min-Cut: Recursive Contraction
    "2.21.98",  # Global Min-Cut: Sparsification
    "2.21.81"   # Weighted Directed Mst
]

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

def get_section_deps(item_id, item_by_id, section_by_id):
    """获取 item 所属 section 的依赖"""
    parent_id = None
    for item in item_by_id.values():
        if item['id'] == item_id:
            parent_id = item.get('parent')
            break

    if parent_id and parent_id in section_by_id:
        return section_by_id[parent_id].get('pre', [])
    return []

def get_section_items_for_deps(section_deps, section_by_id):
    """将 section 依赖转换为 item 依赖"""
    result = []
    for dep in section_deps:
        if dep in section_by_id:
            section = section_by_id[dep]
            for item in section.get('items', []):
                result.append(item['id'])
        else:
            # 如果是 item id 直接添加
            result.append(dep)
    return result

def calculate_resolved_pre(item_id, item_by_id, section_by_id):
    """计算 resolved_pre"""
    item = item_by_id[item_id]
    direct_pre = item.get('direct_pre', [])

    resolved_pre = set()

    # 添加 direct_pre
    for dep in direct_pre:
        if dep in item_by_id:  # 确保 dep 是有效的 item
            resolved_pre.add(dep)

    # 添加 section 依赖中的 item
    section_deps = get_section_deps(item_id, item_by_id, section_by_id)
    section_items = get_section_items_for_deps(section_deps, section_by_id)
    for item_id_from_section in section_items:
        if item_id_from_section in item_by_id:
            resolved_pre.add(item_id_from_section)

    # 递归添加依赖的依赖 (BFS 遍历)
    queue = deque(direct_pre)

    while queue:
        current = queue.popleft()
        if current in item_by_id:
            current_item = item_by_id[current]
            for dep in current_item.get('direct_pre', []):
                if dep != item_id and dep in item_by_id:  # 确保不是自己且是有效 item
                    if dep not in resolved_pre:
                        resolved_pre.add(dep)
                        queue.append(dep)

    # 转换为列表并排序 (按图谱中 item id 的自然顺序)
    result = sorted(list(resolved_pre))

    return result

def main():
    print("开始修复 Stage3E-Batch1 Resolved Pre Mismatches...")

    # 读取主图谱
    print("读取主图谱...")
    with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 构建映射
    print("构建映射...")
    item_by_id, section_by_id = build_item_map(data)

    # 检查目标节点是否存在
    print(f"检查 {len(TARGET_NODES)} 个目标节点...")
    for node_id in TARGET_NODES:
        if node_id not in item_by_id:
            print(f"警告: 节点 {node_id} 不在图谱中")

    # 修复节点
    print(f"\n开始修复 {len(TARGET_NODES)} 个节点的 resolved_pre...")
    applied_patches = []

    for node_id in TARGET_NODES:
        if node_id not in item_by_id:
            print(f"跳过 {node_id} (不存在)")
            continue

        item = item_by_id[node_id]
        old_resolved_pre = list(item.get('resolved_pre', []))

        # 重新计算 resolved_pre
        new_resolved_pre = calculate_resolved_pre(node_id, item_by_id, section_by_id)

        # 检查变化
        if old_resolved_pre != new_resolved_pre:
            item['resolved_pre'] = new_resolved_pre

            # 计算差异
            old_set = set(old_resolved_pre)
            new_set = set(new_resolved_pre)
            added = sorted(list(new_set - old_set))
            removed = sorted(list(old_set - new_set))

            applied_patches.append({
                'item_id': node_id,
                'item_name': item['name'],
                'old_resolved_pre_count': len(old_resolved_pre),
                'new_resolved_pre_count': len(new_resolved_pre),
                'added_dependencies': added,
                'removed_dependencies': removed,
                'old_resolved_pre': old_resolved_pre,
                'new_resolved_pre': new_resolved_pre
            })

            print(f"✓ {node_id}: {len(old_resolved_pre)} -> {len(new_resolved_pre)} (新增 {len(added)}, 删除 {len(removed)})")
        else:
            print(f"○ {node_id}: 无变化")

    # 保存结果
    print(f"\n保存修复结果...")
    with open('merged_knowledge_graph_item_dependencies_refined.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 保存应用补丁
    print("保存应用补丁...")
    applied_patch_data = {
        'description': 'Stage3E-Aggressive Batch1 Resolved Pre Fix Applied Patches',
        'generated_at': '2026-05-22',
        'batch_id': 'batch_1',
        'target_nodes': TARGET_NODES,
        'total_nodes_processed': len(TARGET_NODES),
        'nodes_fixed': len(applied_patches),
        'applied_patches': applied_patches
    }

    with open('data/stage3e_aggressive_batch1_resolved_pre_fix_applied_patch.json', 'w', encoding='utf-8') as f:
        json.dump(applied_patch_data, f, ensure_ascii=False, indent=2)

    print(f"\n修复完成:")
    print(f"- 处理节点数: {len(TARGET_NODES)}")
    print(f"- 修复节点数: {len(applied_patches)}")
    print(f"- 新增依赖总数: {sum(len(p['added_dependencies']) for p in applied_patches)}")
    print(f"- 删除依赖总数: {sum(len(p['removed_dependencies']) for p in applied_patches)}")
    print(f"\n应用补丁已保存到: data/stage3e_aggressive_batch1_resolved_pre_fix_applied_patch.json")

    return applied_patches

if __name__ == "__main__":
    main()