import json

g = json.load(open("merged_knowledge_graph_item_dependencies_refined.json", encoding="utf-8"))

batch1, batch2, stage3g = [], [], []
for cat in g["categories"]:
    for sec in cat["sections"]:
        for it in sec["items"]:
            srcs = it.get("source", [])
            if "stage5_hard_batch1_full500" in srcs:
                batch1.append(it)
            elif "stage5_hard_batch2_full600" in srcs:
                batch2.append(it)
            elif any("stage3g" in s for s in srcs):
                stage3g.append(it)

print(f"Batch1={len(batch1)}, Batch2={len(batch2)}, stage3g={len(stage3g)}")

# Chronological: stage3g (oldest) -> batch1 -> batch2 (newest)
# Last 1200: stage3g tail (125) + batch1 (475) + batch2 (600) = 1200
tail_s3g = stage3g[-125:] if len(stage3g) >= 125 else stage3g
combined = tail_s3g + batch1 + batch2
print(f"Showing last 1200: stage3g tail {len(tail_s3g)} + batch1 {len(batch1)} + batch2 {len(batch2)} = {len(combined)}\n")

for i, it in enumerate(combined):
    iid = it["id"]
    name = it["name"][:68]
    sec = it.get("parent", "?")
    tier = it.get("source_tier", "")
    diff = it.get("difficulty", 0)
    if "stage5_hard_batch2_full600" in it.get("source", []):
        src = "B2"
    elif "stage5_hard_batch1_full500" in it.get("source", []):
        src = "B1"
    else:
        src = "S3G"
    print(f"{i+1:4d}. [{iid}] ({sec}) {name} | {src} {tier} diff={diff}")
