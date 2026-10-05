import json

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

# 应用依赖修复（仅修改 direct_pre，不修改 resolved_pre）
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
            new_direct_pre = new_direct_pre[:8]

        # 更新direct_pre
        if new_direct_pre != original_direct_pre:
            item['direct_pre'] = new_direct_pre
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