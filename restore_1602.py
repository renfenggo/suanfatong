import json, copy

# Read current refined graph (1617 items - corrupted)
refined = json.load(open("merged_knowledge_graph_item_dependencies_refined.json","r",encoding="utf-8"))

# Read original graph (1602 items - clean)
original = json.load(open("merged_knowledge_graph.json","r",encoding="utf-8"))

# Find section 3.13 in refined and remove items 3.13.143 to 3.13.157
removed_count = 0
for cat in refined["categories"]:
    for sec in cat["sections"]:
        if sec["id"] == "3.13":
            original_len = len(sec["items"])
            sec["items"] = [item for item in sec["items"] if not any(
                item["id"] == f"3.13.{i}" for i in range(143, 158)
            )]
            removed_count = original_len - len(sec["items"])
            print(f"Section 3.13: removed {removed_count} items ({original_len} -> {len(sec['items'])})")
            break

# Update validation_baseline
if "meta" not in refined:
    refined["meta"] = {}
refined["meta"]["validation_baseline"] = {"item_count": 1602, "section_count": 65}

# Verify total items
items = []
for cat in refined["categories"]:
    for sec in cat["sections"]:
        for item in sec["items"]:
            items.append(item)
print(f"Total items after cleanup: {len(items)}")

# Save
with open("merged_knowledge_graph_item_dependencies_refined.json","w",encoding="utf-8") as f:
    json.dump(refined, f, ensure_ascii=False, indent=2)
print("Saved cleaned refined graph.")