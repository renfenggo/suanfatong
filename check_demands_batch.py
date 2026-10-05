import json

checks = {
    "cand.graph.flow_bounds.demands": None,
    "cand.graph.flow_bounds.edge_lower_bound_transform": None,
}

for bf in ["data/stage3e_aggressive_batch1_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch3_candidate_to_item_id_mapping.json",
           "data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json",
           "data/stage3e_batch5_smaller15_candidate_to_item_id_mapping.json"]:
    d = json.load(open(bf,'r',encoding='utf-8'))
    print(f"\n=== {bf} ===")
    if isinstance(d, list):
        for m in d:
            cid = m["candidate_id"]
            if cid in checks:
                print(f"  FOUND: {cid} -> {m['item_id']}")
    elif isinstance(d, dict):
        for cid, iid in d.items():
            if cid in checks:
                print(f"  FOUND: {cid} -> {iid}")
