import json, os

io = json.load(open('assets/data/knowledge/io_v4_4.json', encoding='utf-8'))
all_ids = set()
for cat in io['categories']:
    for sec in cat['sections']:
        for it in sec['items']:
            all_ids.add(it['id'])
print(f'io_v4_4.json items: {len(all_ids)}')

idx = json.load(open('assets/data/knowledge_content/content_index.json', encoding='utf-8'))
covered = set()
for p in idx['parts']:
    if os.path.exists(p['path']):
        items = json.load(open(p['path'], encoding='utf-8'))
        for it in items:
            covered.add(it['item_id'])
print(f'Content covers: {len(covered)}')
print(f'Missing: {len(all_ids - covered)}')
print(f'Total parts: {len(idx["parts"])}')

b2_parts = [p for p in idx['parts'] if p.get('filename', '').startswith('stage5_hard_batch2_')]
print(f'Batch2 parts: {len(b2_parts)}')
for p in b2_parts:
    fn = p['filename']
    cnt = p['item_count']
    print(f'  {fn}: {cnt} items')

report = json.load(open('assets/data/knowledge_content/reports/stage5_hard_batch2_content_validation_result.json', encoding='utf-8'))
print(f'Validation passed: {report["validation_passed"]}')
print(f'missing_items: {len(report["missing_items"])}')
print(f'duplicate_items: {len(report["duplicate_items"])}')
print(f'incomplete_items: {report["incomplete_items_count"]}')
print(f'final_content_count: {report["final_content_count"]}')
print(f'placeholder_text_count: {report["placeholder_text_count"]}')
print(f'quiz_missing_count: {report["quiz_missing_count"]}')
print(f'animation_plan_missing_count: {report["animation_plan_missing_count"]}')
