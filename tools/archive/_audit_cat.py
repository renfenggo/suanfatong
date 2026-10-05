import json
from collections import Counter

graph = json.load(open("merged_knowledge_graph_item_dependencies_refined.json", "r", encoding="utf-8"))
b2_map = json.load(open("data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json", "r", encoding="utf-8"))
applied = json.load(open("data/stage5_hard_knowledge_batch2_full600_section_relocation_applied_patch.json", "r", encoding="utf-8"))

old_to_new = {r["old_item_id"]: r["new_item_id"] for r in applied["relocations"]}

# Build graph index
items_by_id = {}
item_section = {}
section_name = {}
for cat in graph["categories"]:
    for sec in cat["sections"]:
        sid = sec["id"]
        section_name[sid] = sec.get("name", sid)
        for it in sec["items"]:
            items_by_id[it["id"]] = it
            item_section[it["id"]] = sid

# Build category → sections mapping
cat_sections = {}
for cat in graph["categories"]:
    cat_name = cat.get("name", cat.get("id", "?"))
    sec_ids = [sec["id"] for sec in cat["sections"]]
    cat_sections[cat_name] = sec_ids
    print(f"Category: {cat_name} → sections: {sec_ids[:5]}...")

# Section → category mapping
sec_to_cat = {}
for cat_name, sids in cat_sections.items():
    for sid in sids:
        sec_to_cat[sid] = cat_name

# Get all Batch2 item IDs (corrected for relocation)
b2_mappings = b2_map["mappings"]
print(f"\nBatch2 mappings: {len(b2_mappings)}")

# Method 1: By original candidate category
orig_cat_dist = Counter()
for m in b2_mappings:
    orig_cat_dist[m.get("category", "?")] += 1
print(f"\nMethod 1 - Original candidate category:")
for cat, cnt in orig_cat_dist.most_common():
    print(f"  {cat}: {cnt}")

# Method 2: By actual section in graph
actual_cat_dist = Counter()
actual_sec_dist = Counter()
unresolved = []
for m in b2_mappings:
    iid = m["item_id"]
    # Apply relocation
    actual_iid = old_to_new.get(iid, iid)
    if actual_iid not in items_by_id:
        unresolved.append(actual_iid)
        continue
    sec = item_section[actual_iid]
    cat = sec_to_cat.get(sec, f"unknown({sec})")
    actual_cat_dist[cat] += 1
    actual_sec_dist[sec] += 1

print(f"\nMethod 2 - Actual section category in graph:")
for cat, cnt in actual_cat_dist.most_common():
    print(f"  {cat}: {cnt}")

print(f"\nSection distribution (top 15):")
for sec, cnt in actual_sec_dist.most_common(15):
    print(f"  {sec} ({section_name.get(sec, '?')}): {cnt}")

print(f"\nUnresolved IDs: {len(unresolved)}")

# Now let's understand: checkpoint says algorithm=433, math=167, data_structure=0
# Check if checkpoint used section prefix mapping
# Section prefix: 1.x = ?, 2.x = ?, 3.x = ?
print(f"\n--- Section prefix analysis ---")
prefix_dist = Counter()
for m in b2_mappings:
    iid = m["item_id"]
    actual_iid = old_to_new.get(iid, iid)
    if actual_iid in items_by_id:
        sec = item_section[actual_iid]
        prefix = sec.split(".")[0]
        prefix_dist[prefix] += 1

print(f"Section prefix distribution:")
for p, cnt in sorted(prefix_dist.items()):
    print(f"  {p}.x: {cnt}")

# Check what the checkpoint script likely did
# If it used "category" from items, let's check
print(f"\n--- Item-level category/track fields ---")
sample = list(items_by_id.values())[0]
print(f"Item fields: {list(sample.keys())}")
print(f"Sample: {json.dumps({k: sample[k] for k in ['id', 'name'] if k in sample}, ensure_ascii=False)[:200]}")

# Check if items have category/track field
has_cat = sum(1 for it in items_by_id.values() if "category" in it)
has_track = sum(1 for it in items_by_id.values() if "track" in it)
print(f"Items with 'category' field: {has_cat}")
print(f"Items with 'track' field: {has_track}")

# Check batch2 items specifically
b2_sample = None
for m in b2_mappings[:1]:
    iid = m["item_id"]
    actual_iid = old_to_new.get(iid, iid)
    if actual_iid in items_by_id:
        b2_sample = items_by_id[actual_iid]
        print(f"\nBatch2 sample item fields: {list(b2_sample.keys())}")
        print(f"Batch2 sample: {json.dumps(b2_sample, ensure_ascii=False)[:300]}")

# What does candidate mapping's "category" look like?
print(f"\nCandidate mapping sample:")
for m in b2_mappings[:3]:
    print(f"  {m['item_id']}: cat={m.get('category','?')} subcat={m.get('subcategory','?')} sec={m.get('section','?')}")

# Check mapping category values
map_cats = Counter(m.get("category", "?") for m in b2_mappings)
print(f"\nMapping category values: {dict(map_cats)}")

# Check mapping section values
map_secs = Counter(m.get("section", "?") for m in b2_mappings)
print(f"\nMapping section values (top 10):")
for sec, cnt in map_secs.most_common(10):
    print(f"  {sec}: {cnt}")

# Cross-check: how many mapping sections start with "3." (data structure)?
ds_by_map = sum(1 for m in b2_mappings if m.get("section", "").startswith("3."))
ds_by_actual = sum(1 for m in b2_mappings if item_section.get(old_to_new.get(m["item_id"], m["item_id"]), "").startswith("3."))
print(f"\nData structure by mapping section prefix 3.x: {ds_by_map}")
print(f"Data structure by actual section prefix 3.x: {ds_by_actual}")

# The checkpoint says algorithm=433, math=167, ds=0
# Let's see if 433 = 255+145+some, or if section-based counting was wrong
# What if checkpoint used section prefix 1=算法 2=算法 3=数据结构 4=数学?
# Then nodes in sections 1.x, 2.x would be "algorithm", nodes in 3.x would be "data_structure", nodes in 4.x would be "math"

# Let's check by section prefix
sec1 = sum(1 for m in b2_mappings if item_section.get(old_to_new.get(m["item_id"], m["item_id"]), "").startswith("1."))
sec2 = sum(1 for m in b2_mappings if item_section.get(old_to_new.get(m["item_id"], m["item_id"]), "").startswith("2."))
sec3 = sum(1 for m in b2_mappings if item_section.get(old_to_new.get(m["item_id"], m["item_id"]), "").startswith("3."))
sec4 = sum(1 for m in b2_mappings if item_section.get(old_to_new.get(m["item_id"], m["item_id"]), "").startswith("4."))
print(f"\nBy actual section prefix: 1.x={sec1} 2.x={sec2} 3.x={sec3} 4.x={sec4}")
print(f"Total: {sec1+sec2+sec3+sec4}")

# What mapping section prefixes look like
map_sec1 = sum(1 for m in b2_mappings if m.get("section", "").startswith("1."))
map_sec2 = sum(1 for m in b2_mappings if m.get("section", "").startswith("2."))
map_sec3 = sum(1 for m in b2_mappings if m.get("section", "").startswith("3."))
map_sec4 = sum(1 for m in b2_mappings if m.get("section", "").startswith("4."))
print(f"\nBy mapping section prefix: 1.x={map_sec1} 2.x={map_sec2} 3.x={map_sec3} 4.x={map_sec4}")
