import json

# 读取文件
with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/stage3e_aggressive_batch1_review_status_patch_preview.json', 'r', encoding='utf-8') as f:
    review_status_patch = json.load(f)

# 构建item查找索引
item_by_id = {}
for cat in data.get('categories', []):
    for section in cat.get('sections', []):
        for item in section.get('items', []):
            item_by_id[item['id']] = item

# 应用review_status patch
applied_review_patches = []
for patch in review_status_patch.get('patches', []):
    item_id = patch['item_id']
    if item_id in item_by_id:
        item = item_by_id[item_id]
        new_priority = patch['new_review_priority']
        new_need_manual_review = patch['new_need_manual_review']

        # 保存旧值
        old_priority = item.get('review_priority', 'B')
        old_need_manual_review = item.get('need_manual_review', True)

        # 应用patch
        if 'review_priority' in item:
            item['review_priority'] = new_priority

        if 'need_manual_review' in item:
            item['need_manual_review'] = new_need_manual_review

        # 记录变更
        if old_priority != new_priority or old_need_manual_review != new_need_manual_review:
            applied_review_patches.append({
                'item_id': item_id,
                'item_name': item['name'],
                'old_priority': old_priority,
                'new_priority': new_priority,
                'old_need_manual_review': old_need_manual_review,
                'new_need_manual_review': new_need_manual_review,
                'patch_type': patch['patch_type'],
                'reason': patch['reason']
            })

# 保存结果
with open('merged_knowledge_graph_item_dependencies_refined.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 输出修复摘要
print(f"Total review status patches: {len(review_status_patch.get('patches', []))}")
print(f"Applied review patches: {len(applied_review_patches)}")
print(f"Review status patches applied successfully!")

# 保存应用的补丁到现有的文件
with open('data/stage3e_aggressive_batch1_fix_applied_patch.json', 'r', encoding='utf-8') as f:
    applied_patch_data = json.load(f)

applied_patch_data['applied_review_patches'] = applied_review_patches

with open('data/stage3e_aggressive_batch1_fix_applied_patch.json', 'w', encoding='utf-8') as f:
    json.dump(applied_patch_data, f, ensure_ascii=False, indent=2)

print("Applied patch file updated with review status patches!")