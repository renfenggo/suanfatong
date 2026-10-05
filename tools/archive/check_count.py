import json

with open('merged_knowledge_graph_item_dependencies_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items_count = 0
sections_count = sum([len(cat.get('sections', [])) for cat in data.get('categories', [])])
for cat in data.get('categories', []):
    for section in cat.get('sections', []):
        items_count += len(section.get('items', []))

print(f'Items: {items_count}')
print(f'Sections: {sections_count}')