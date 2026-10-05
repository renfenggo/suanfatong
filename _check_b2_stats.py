import json
g = json.load(open("merged_knowledge_graph_item_dependencies_refined.json", encoding="utf-8"))
b2 = [it for cat in g["categories"] for sec in cat["sections"] for it in sec["items"] if "stage5_hard_batch2_full600" in it.get("source", [])]
print(f"Batch2 count: {len(b2)}")
it = b2[0]
print(f"source_tier: {it.get('source_tier')}")
print(f"review_priority: {it.get('review_priority')}")
print(f"review_status: {it.get('review_status')}")

tiers = {}
prios = {}
cats = {}
for x in b2:
    t = x.get("source_tier", "unknown")
    tiers[t] = tiers.get(t, 0) + 1
    p = x.get("review_priority", "unknown")
    prios[p] = prios.get(p, 0) + 1
    sec_prefix = x.get("parent", "").split(".")[0]
    if sec_prefix in ("2", "3"):
        c = "algorithm"
    elif sec_prefix == "4":
        c = "math"
    else:
        c = "other"
    cats[c] = cats.get(c, 0) + 1

print(f"tiers: {tiers}")
print(f"prios: {prios}")
print(f"cats: {cats}")
