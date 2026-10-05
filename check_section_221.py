import json

g = json.load(open("merged_knowledge_graph_item_dependencies_refined.json","r",encoding="utf-8"))

# Show section 2.15 items
print("=== Section 2.15 items ===")
for cat in g["categories"]:
    for s in cat["sections"]:
        if s["id"] == "2.15":
            for item in s["items"]:
                print(f"  {item['id']}: {item.get('name','')}")

# Show section 2.21 items with their names
print("\n=== Section 2.21 items ===")
for cat in g["categories"]:
    for s in cat["sections"]:
        if s["id"] == "2.21":
            for item in s["items"]:
                iid = item["id"]
                num = int(iid.split(".")[-1])
                if num >= 120:
                    print(f"  {iid}: {item.get('name','')}")
