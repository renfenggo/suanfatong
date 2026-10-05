import json
from collections import Counter

graph = json.load(open("merged_knowledge_graph_item_dependencies_refined.json", "r", encoding="utf-8"))
b2_map = json.load(open("data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json", "r", encoding="utf-8"))
applied = json.load(open("data/stage5_hard_knowledge_batch2_full600_section_relocation_applied_patch.json", "r", encoding="utf-8"))

old_to_new = {r["old_item_id"]: r["new_item_id"] for r in applied["relocations"]}

items_by_id = {}
item_section = {}
for cat in graph["categories"]:
    for sec in cat["sections"]:
        for it in sec["items"]:
            items_by_id[it["id"]] = it
            item_section[it["id"]] = sec["id"]

b2_ids = set()
b2_cat_field = Counter()
b2_sec_vs_cat = Counter()

for m in b2_map["mappings"]:
    iid = old_to_new.get(m["item_id"], m["item_id"])
    if iid not in items_by_id:
        continue
    it = items_by_id[iid]
    sec = item_section[iid]
    cat_field = it.get("category", "NONE")
    sec_prefix = sec.split(".")[0]
    
    b2_ids.add(iid)
    b2_cat_field[cat_field] += 1
    b2_sec_vs_cat[(sec_prefix, cat_field)] += 1

print(f"Batch2 item 'category' field distribution:")
for cat, cnt in b2_cat_field.most_common():
    print(f"  {cat}: {cnt}")

print(f"\nSection prefix vs item category field:")
for (prefix, cat), cnt in sorted(b2_sec_vs_cat.items()):
    print(f"  sec {prefix}.x → category='{cat}': {cnt}")

# The real graph category (by section)
sec_to_graph_cat = {}
for cat in graph["categories"]:
    cat_name = cat.get("name", "?")
    for sec in cat["sections"]:
        sec_to_graph_cat[sec["id"]] = cat_name

b2_graph_cat = Counter()
for iid in b2_ids:
    sec = item_section[iid]
    graph_cat = sec_to_graph_cat.get(sec, "?")
    b2_graph_cat[graph_cat] += 1

print(f"\nGraph category (by section parent):")
for cat, cnt in b2_graph_cat.most_common():
    print(f"  {cat}: {cnt}")

# Cross-check: items in section 3.x with wrong category
print(f"\n--- Items in 3.x with category != '数据结构' ---")
wrong = 0
for iid in b2_ids:
    sec = item_section[iid]
    if sec.startswith("3."):
        cat_field = items_by_id[iid].get("category", "NONE")
        if cat_field != "数据结构":
            wrong += 1
            if wrong <= 5:
                name = items_by_id[iid]["name"].split("(")[0].strip()[:40]
                print(f"  {iid}: category='{cat_field}' name={name}")
print(f"  Total wrong: {wrong} / {sum(1 for i in b2_ids if item_section[i].startswith('3.'))}")

# Items in 2.x with category = '数据结构'
print(f"\n--- Items in 2.x with category = '数据结构' ---")
ds_in_2x = 0
for iid in b2_ids:
    sec = item_section[iid]
    if sec.startswith("2."):
        cat_field = items_by_id[iid].get("category", "NONE")
        if cat_field == "数据结构":
            ds_in_2x += 1
            if ds_in_2x <= 5:
                name = items_by_id[iid]["name"].split("(")[0].strip()[:40]
                print(f"  {iid}: category='{cat_field}' name={name}")
print(f"  Total: {ds_in_2x} / {sum(1 for i in b2_ids if item_section[i].startswith('2.'))}")

# Summary
print(f"\n{'='*60}")
print(f"ROOT CAUSE ANALYSIS:")
print(f"  Checkpoint counted by item.category field")
print(f"  item.category says: {dict(b2_cat_field)}")
print(f"  Graph says (by section): {dict(b2_graph_cat)}")
print(f"  Difference: {wrong} items in 3.x have wrong category field")
print(f"  Plus {ds_in_2x} items in 2.x marked as 数据结构")
print(f"  Checkpoint total: algorithm={b2_cat_field.get('算法',0)} math={b2_cat_field.get('数学',0)} ds={b2_cat_field.get('数据结构',0)}")
