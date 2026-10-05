import json

d4 = json.load(open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json","r",encoding="utf-8"))

# Check all batch4 candidates in full
print("=== All batch4 candidate_id -> item_id ===")
for cid, iid in sorted(d4.items()):
    print(f"  {cid} -> {iid}")

# Check if demands and edge_lower_bound are in any batch1-5
print("\n=== Checking specific candidates across all batches ===")
checks = {
    "cand.graph.flow_bounds.demands": None,
    "cand.graph.flow_bounds.edge_lower_bound_transform": None,
    "cand.graph.matching_cover.blossom_algorithm": None,
}

for bf in ["data/stage3e_aggressive_batch1_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch3_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json",
           "data/stage3e_batch5_smaller15_candidate_to_item_id_mapping.json"]:
    d = json.load(open(bf,'r',encoding='utf-8'))
    batch = bf.split("/")[-1].split("_")[0] if "batch5" not in bf else "batch5"
    if isinstance(d, list):
        for m in d:
            cid = m["candidate_id"]
            if cid in checks:
                checks[cid] = {"batch": batch, "item_id": m["item_id"]}
    elif isinstance(d, dict):
        for cid, iid in d.items():
            if cid in checks:
                checks[cid] = {"batch": batch, "item_id": iid}

for cid, info in checks.items():
    print(f"  {cid}: {info}")
