import json, os

pre_b1 = json.load(open('assets/data/knowledge_content/content_index_before_stage5_hard_batch1.json', encoding='utf-8'))
current = json.load(open('assets/data/knowledge_content/content_index.json', encoding='utf-8'))

b1_parts = [p for p in current['parts'] if p.get('filename', '').startswith('stage5_hard_batch1_')]
print(f'Batch1 parts found: {len(b1_parts)}')
for p in b1_parts:
    fn = p['filename']
    cnt = p['item_count']
    print(f'  {fn} ({cnt} items)')

pre_b1['parts'].extend(b1_parts)
pre_b1['total_parts'] = len(pre_b1['parts'])
pre_b1['version'] = 'stage5_hard_batch1_v1'
pre_b1['source_item_count'] = 2640
pre_b1['generated_item_count'] = 2640
pre_b1['stage5_hard_batch1'] = current.get('stage5_hard_batch1', {})
pre_b1['generated_at'] = current.get('generated_at', '')

json.dump(pre_b1, open('assets/data/knowledge_content/content_index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

covered = set()
for p in pre_b1['parts']:
    if os.path.exists(p['path']):
        items = json.load(open(p['path'], encoding='utf-8'))
        for it in items:
            covered.add(it['item_id'])
print(f'Clean index covers: {len(covered)} items')
print(f'Total parts: {len(pre_b1["parts"])}')
