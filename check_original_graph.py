import json

graph = json.load(open('merged_knowledge_graph.json', 'r', encoding='utf-8'))
item_count = sum(len(s["items"]) for c in graph["categories"] for s in c["sections"])
print(f'item_count: {item_count}')