import json
# Check if these items actually exist in the graph
g = json.load(open("merged_knowledge_graph_item_dependencies_refined.json","r",encoding="utf-8"))

item_ids_in_graph = set()
for cat in g["categories"]:
    for s in cat["sections"]:
        for item in s["items"]:
            item_ids_in_graph.add(item["id"])

# batch4 dict has candidate_id -> item_id mapping
d = json.load(open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json","r",encoding="utf-8"))

conflicts = ["cand.graph.matching_cover.stable_marriage",
             "cand.graph.matching_cover.minimum_path_cover",
             "cand.graph.matching_cover.dilworth_theorem",
             "cand.graph.flow_bounds.demands",
             "cand.graph.flow_bounds.edge_lower_bound_transform",
             "cand.graph.matching_cover.konig_theorem",
             "cand.graph.matching_cover.weighted_general_matching",
             "cand.graph.flow_bounds.minimum_flow"]

for c in conflicts:
    if c in d:
        item_id = d[c]
        in_graph = item_id in item_ids_in_graph
        print(f"{c}: item_id={item_id}, in_graph={in_graph}")
