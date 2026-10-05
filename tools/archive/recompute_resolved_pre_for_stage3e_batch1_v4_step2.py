import json

def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out

def compute_resolved(edges, item_ids):
    memo, visiting = {}, set()

    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))
                out.append(dep)
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])
        return memo[node]

    return {item_id: resolve(item_id) for item_id in item_ids}

def main():
    input_file = "merged_knowledge_graph_item_dependencies_refined.json"
    patch_file = "data/stage3e_batch1_resolved_pre_fix_v4_step2_applied_patch.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    items = []
    for category in graph["categories"]:
        for section in category["sections"]:
            items.extend(section.get("items", []))
    
    item_by_id = {item["id"]: item for item in items}
    item_ids = set(item_by_id.keys())
    
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in items}
    
    target_nodes = [
        "2.21.88", "2.21.89", "2.21.90", "2.21.91", "2.21.92", "2.21.93",
        "2.21.96", "2.21.97", "2.21.98",
        "2.21.81"
    ]
    
    applied_patch = []
    
    for item_id in target_nodes:
        if item_id not in item_by_id:
            print(f"Warning: {item_id} not found in graph")
            continue
        
        item = item_by_id[item_id]
        old_resolved_pre = item.get("resolved_pre", []) or []
        
        new_resolved_pre = compute_resolved(edges, item_ids)[item_id]
        
        if old_resolved_pre == new_resolved_pre:
            print(f"{item_id}: No change needed")
            continue
        
        patch_entry = {
            "item_id": item_id,
            "name": item.get("name", ""),
            "old_resolved_pre": old_resolved_pre,
            "new_resolved_pre": new_resolved_pre,
            "old_len": len(old_resolved_pre),
            "new_len": len(new_resolved_pre),
            "method": "official_compute_resolved_logic"
        }
        
        applied_patch.append(patch_entry)
        item["resolved_pre"] = new_resolved_pre
        
        print(f"{item_id}: {len(old_resolved_pre)} -> {len(new_resolved_pre)}")
    
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open(patch_file, 'w', encoding='utf-8') as f:
        json.dump(applied_patch, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal nodes fixed: {len(applied_patch)}")
    print(f"Patch saved to: {patch_file}")
    print(f"Graph updated: {input_file}")

if __name__ == "__main__":
    main()