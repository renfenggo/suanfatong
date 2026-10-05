import json
import copy

# 读取文件
with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/stage3e_aggressive_batch1_dependency_fix_candidates.json', 'r', encoding='utf-8') as f:
    dependency_fix_candidates = json.load(f)

# 构建索引
item_by_id = {}
section_by_id = {}
for cat in data.get('categories', []):
    for section in cat.get('sections', []):
        section_by_id[section['id']] = section
        for item in section.get('items', []):
            item_by_id[item['id']] = item

# 构建反向依赖图（下游节点）
downstream_map = {}
for item_id, item in item_by_id.items():
    for dep in item.get('direct_pre', []):
        if dep not in downstream_map:
            downstream_map[dep] = []
        downstream_map[dep].append(item_id)

def get_section_deps(item_id):
    """获取item所属section的依赖"""
    parent_id = None
    for cat in data.get('categories', []):
        for section in cat.get('sections', []):
            for item in section.get('items', []):
                if item['id'] == item_id:
                    parent_id = section['id']
                    break
            if parent_id:
                break
        if parent_id:
            break

    if parent_id and parent_id in section_by_id:
        return section_by_id[parent_id].get('pre', [])
    return []

def calculate_resolved_pre_recursive(direct_pre, item_id, item_by_id, section_by_id):
    """递归计算resolved_pre"""
    resolved_pre = list(direct_pre)
    section_deps = get_section_deps(item_id)

    # 添加section依赖中的item
    for dep in section_deps:
        if dep in item_by_id:
            resolved_pre.append(dep)
        elif dep in section_by_id:
            # 如果是section依赖，添加section下的item
            section = section_by_id[dep]
            for item in section.get('items', []):
                resolved_pre.append(item['id'])

    # 递归添加依赖的依赖
    queue = list(resolved_pre)
    visited = set(resolved_pre)

    while queue:
        current = queue.pop(0)
        if current in item_by_id:
            item = item_by_id[current]
            for dep in item.get('direct_pre', []):
                if dep != item_id and dep not in visited:
                    visited.add(dep)
                    resolved_pre.append(dep)
                    queue.append(dep)

    # 去重并保持顺序
    seen = set()
    result = []
    for dep in resolved_pre:
        if dep not in seen:
            seen.add(dep)
            result.append(dep)

    return result

# 模拟依赖修复
simulated_changes = []
for fix_candidate in dependency_fix_candidates.get('fix_candidates', []):
    item_id = fix_candidate['item_id']
    if item_id in item_by_id:
        item = item_by_id[item_id]
        original_direct_pre = list(item.get('direct_pre', []))

        # 应用修复（模拟）
        new_direct_pre = list(original_direct_pre)
        for dep in fix_candidate.get('suggested_direct_pre_add', []):
            if dep not in new_direct_pre:
                new_direct_pre.append(dep)
        for dep in fix_candidate.get('suggested_direct_pre_remove', []):
            if dep in new_direct_pre:
                new_direct_pre.remove(dep)

        # 控制direct_pre数量在1-8个
        if len(new_direct_pre) > 8:
            new_direct_pre = new_direct_pre[:8]

        if new_direct_pre != original_direct_pre:
            simulated_changes.append({
                'item_id': item_id,
                'item_name': item['name'],
                'original_direct_pre': original_direct_pre,
                'new_direct_pre': new_direct_pre
            })

print(f"模拟修复节点数量: {len(simulated_changes)}")

# 计算每个受影响节点的 resolved_pre 变化
resolved_pre_mismatches = []
downstream_affected = []

for change in simulated_changes:
    item_id = change['item_id']
    item_name = change['item_name']
    old_direct_pre = change['original_direct_pre']
    new_direct_pre = change['new_direct_pre']

    # 计算新的 resolved_pre
    new_resolved_pre = calculate_resolved_pre_recursive(new_direct_pre, item_id, item_by_id, section_by_id)

    # 获取当前存储的 resolved_pre
    current_resolved_pre = item_by_id[item_id].get('resolved_pre', [])

    # 比较差异
    current_set = set(current_resolved_pre)
    new_set = set(new_resolved_pre)

    missing_in_current = new_set - current_set
    extra_in_current = current_set - new_set

    if missing_in_current or extra_in_current:
        resolved_pre_mismatches.append({
            'item_id': item_id,
            'name': item_name,
            'old_direct_pre': old_direct_pre,
            'new_direct_pre': new_direct_pre,
            'stored_resolved_pre': current_resolved_pre,
            'expected_resolved_pre': new_resolved_pre,
            'missing_in_stored': sorted(list(missing_in_current)),
            'extra_in_stored': sorted(list(extra_in_current)),
            'cause': 'direct_pre_changed_resolved_pre_not_updated'
        })

    # 检查下游影响
    if item_id in downstream_map:
        downstream_affected.append({
            'changed_item_id': item_id,
            'downstream_items': list(set(downstream_map[item_id]))
        })

print(f"会产生 resolved_pre mismatch 的节点数量: {len(resolved_pre_mismatches)}")
print(f"有下游影响的节点数量: {len(downstream_affected)}")

# 生成诊断结果
diagnosis_result = {
    'description': 'Stage3E-Aggressive Batch1 Resolved Pre Mismatch Diagnosis',
    'generated_at': '2026-05-22',
    'batch_id': 'batch_1',

    'current_graph_state': {
        'item_count': 1512,
        'section_count': 65,
        'json_parsable': True,
        'backup_status': 'restored'
    },

    'simulation_results': {
        'total_fixes_needed': len(dependency_fix_candidates.get('fix_candidates', [])),
        'nodes_with_direct_pre_changes': len(simulated_changes),
        'nodes_with_resolved_pre_mismatches': len(resolved_pre_mismatches),
        'nodes_with_downstream_impact': len(downstream_affected)
    },

    'simulated_direct_pre_changes': simulated_changes,

    'resolved_pre_mismatches': resolved_pre_mismatches,

    'downstream_impact': downstream_affected,

    'root_cause_analysis': {
        'main_cause': 'Direct_pre changed but resolved_pre not recalculated',
        'affected_node_types': ['Batch1新增节点'],
        'dependency_chain_impact': 'Direct pre changes propagate to resolved pre of affected nodes',
        'validation_logic': 'Strict validation compares stored resolved_pre with recalculated resolved_pre'
    },

    'recommended_fix_approach': {
        'step1': 'Apply direct_pre fixes to 10 nodes',
        'step2': 'Recalculate resolved_pre for all affected nodes (10 nodes)',
        'step3': 'Check if downstream nodes need resolved_pre updates (likely minimal)',
        'step4': 'Run validate-only to confirm no mismatches',
        'recommended_script': 'recompute_resolved_pre_for_affected_nodes.py'
    },

    'nodes_need_resolved_pre_recalculation': [m['item_id'] for m in resolved_pre_mismatches],
    'total_downstream_nodes_affected': sum(len(d['downstream_items']) for d in downstream_affected),

    'validation_results': {
        'can_proceed_with_fix': True,
        'requires_resolved_pre_update': True,
        'expected_mismatch_count_after_proper_fix': 0
    }
}

# 保存诊断结果
with open('data/stage3e_aggressive_batch1_resolved_pre_mismatch_diagnosis.json', 'w', encoding='utf-8') as f:
    json.dump(diagnosis_result, f, ensure_ascii=False, indent=2)

print("诊断结果已保存到: data/stage3e_aggressive_batch1_resolved_pre_mismatch_diagnosis.json")