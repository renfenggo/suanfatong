import json

with open('C:\\Users\\renfenggo\\Documents\\trae_projects\\suanfatong\\io_v4_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('JSON Structure Analysis:')
print('=' * 50)
print(f'Total categories: {len(data["categories"])}')
print()

total_sections = 0
total_items = 0

for cat in data['categories']:
    cat_sections = len(cat['sections'])
    cat_items = sum(len(s['items']) for s in cat['sections'])
    total_sections += cat_sections
    total_items += cat_items
    
    print(f'{cat["name"]}:')
    print(f'  Sections: {cat_sections}')
    print(f'  Items: {cat_items}')
    
    # Show section details
    print(f'  Sections list:')
    for s in cat['sections']:
        print(f'    - {s["id"]}: {s["name"]} ({s["level"]}) - {len(s["items"])} items')
    print()

print('=' * 50)
print(f'Total sections: {total_sections}')
print(f'Total items: {total_items}')