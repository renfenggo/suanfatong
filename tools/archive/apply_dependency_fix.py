import json
import copy

# 读取文件
with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/stage3e_aggressive_batch1_dependency_fix_candidates.json', 'r', encoding='utf-8') as f:
    dependency_fix_candidates = json.load(f)

# 构建item查找索引
item_by_id = {}
for cat in data.get('categories', []):
    for section in cat.get('sections', []):
        for item in section.get('items', []):
            item_by_id[item['id']] = item

# 获取section依赖
section_by_id = {}
for cat in data.get('categories', []):
    for section in cat.get('sections', []):
        section_by_id[section['id']] = section

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

def calculate_resolved_pre(direct_pre, item_id):
    """计算resolved_pre"""
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

# 应用依赖修复
applied_patches = []
for fix_candidate in dependency_fix_candidates.get('fix_candidates', []):
    item_id = fix_candidate['item_id']
    if item_id in item_by_id:
        item = item_by_id[item_id]
        original_direct_pre = list(item.get('direct_pre', []))

        # 应用修复
        new_direct_pre = list(original_direct_pre)
        for dep in fix_candidate.get('suggested_direct_pre_add', []):
            if dep not in new_direct_pre:
                new_direct_pre.append(dep)
        for dep in fix_candidate.get('suggested_direct_pre_remove', []):
            if dep in new_direct_pre:
                new_direct_pre.remove(dep)

        # 控制direct_pre数量在1-8个
        if len(new_direct_pre) > 8:
            # 保留前8个
            new_direct_pre = new_direct_pre[:8]

        # 更新direct_pre
        if new_direct_pre != original_direct_pre:
            item['direct_pre'] = new_direct_pre
            # 重新计算resolved_pre
            item['resolved_pre'] = calculate_resolved_pre(new_direct_pre, item_id)
            applied_patches.append({
                'item_id': item_id,
                'item_name': item['name'],
                'original_direct_pre': original_direct_pre,
                'new_direct_pre': new_direct_pre,
                'change_type': fix_candidate.get('fix_type', 'unknown')
            })

# 保存结果
with open('merged_knowledge_graph_item_dependencies_refined.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 输出修复摘要
print(f"Total items needing fix: {len(dependency_fix_candidates.get('fix_candidates', []))}")
print(f"Applied patches: {len(applied_patches)}")
print(f"Dependency fixes applied successfully!")

# 保存应用的补丁
with open('data/stage3e_aggressive_batch1_fix_applied_patch.json', 'w', encoding='utf-8') as f:
    json.dump({
        'description': 'Stage3E-Aggressive Batch1 Applied Dependency Fix Patches',
        'generated_at': '2026-05-22',
        'batch_id': 'batch_1',
        'total_fixes_needed': len(dependency_fix_candidates.get('fix_candidates', [])),
        'total_fixes_applied': len(applied_patches),
        'applied_patches': applied_patches
    }, f, ensure_ascii=False, indent=2)

print("Applied patch file saved to: data/stage3e_aggressive_batch1_fix_applied_patch.json")