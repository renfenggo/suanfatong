import json
g = json.load(open("merged_knowledge_graph_item_dependencies_refined.json","r",encoding="utf-8"))
items = set()
for cat in g["categories"]:
    for s in cat["sections"]:
        for i in s["items"]:
            items.add(i["id"])
checks = ["2.7.1","2.7.2","2.7.5","2.8.25","2.8.28","3.4.1","3.4.4","3.7.2","3.7.3","3.2.3","2.15.1","2.21.1"]
for cid in checks:
    print(f"{cid}: {'EXIST' if cid in items else 'MISSING'}")
