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
    graph_file = "merged_knowledge_graph_item_dependencies_refined.json"
    dependency_fix_file = "data/stage3e_aggressive_batch2_dependency_fix_candidates.json"
    problem_pattern_file = "data/stage3e_aggressive_batch2_problem_pattern_sync_candidates.json"
    review_status_file = "data/stage3e_aggressive_batch2_review_status_patch_preview.json"
    mapping_file = "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json"
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open(dependency_fix_file, 'r', encoding='utf-8') as f:
        dependency_fix_candidates = json.load(f)
    
    with open(problem_pattern_file, 'r', encoding='utf-8') as f:
        problem_pattern_candidates = json.load(f)
    
    with open(review_status_file, 'r', encoding='utf-8') as f:
        review_status_patches = json.load(f)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        candidate_to_item_id = json.load(f)
    
    items = []
    for category in graph["categories"]:
        for section in category["sections"]:
            items.extend(section.get("items", []))
    
    item_by_id = {item["id"]: item for item in items}
    
    applied_patch = []
    stats = {
        "dependency_fix_count": 0,
        "duplicate_direct_pre_removed": 0,
        "key_pre_requisites_added": 0,
        "review_status_patch_count": 0,
        "problem_pattern_sync_count": len(problem_pattern_candidates)
    }
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                
                dependency_fix = next((fix for fix in dependency_fix_candidates if fix["id"] == item_id), None)
                if dependency_fix:
                    old_direct_pre = list(item.get("direct_pre", []))
                    new_direct_pre = dependency_fix["suggested_direct_pre"]
                    
                    item["direct_pre"] = new_direct_pre
                    
                    stats["dependency_fix_count"] += 1
                    stats["key_pre_requisites_added"] += len(new_direct_pre) - len(old_direct_pre)
                    
                    applied_patch.append({
                        "id": item_id,
                        "name": item.get("name", ""),
                        "change_type": "dependency_fix",
                        "old_direct_pre": old_direct_pre,
                        "new_direct_pre": new_direct_pre,
                        "reason": dependency_fix.get("issues", ["依赖修复"])
                    })
                
                review_patch = next((patch for patch in review_status_patches if patch["id"] == item_id), None)
                if review_patch:
                    old_review_status = item.get("review_status", {}).copy()
                    
                    item["review_status"] = review_patch["patch"]["review_status"]
                    
                    stats["review_status_patch_count"] += 1
                    
                    applied_patch.append({
                        "id": item_id,
                        "name": item.get("name", ""),
                        "change_type": "review_status_patch",
                        "old_review_status": old_review_status,
                        "new_review_status": review_patch["patch"]["review_status"],
                        "review_note": review_patch["patch"]["review_status"].get("review_note", "")
                    })
    
    items = []
    for category in graph["categories"]:
        for section in category["sections"]:
            items.extend(section.get("items", []))
    
    item_by_id = {item["id"]: item for item in items}
    item_ids = set(item_by_id.keys())
    
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in items}
    
    resolved = compute_resolved(edges, item_ids)
    
    affected_items = set()
    for patch in applied_patch:
        if patch["change_type"] in ["dependency_fix"]:
            affected_items.add(patch["id"])
            item_by_id[patch["id"]]["resolved_pre"] = resolved[patch["id"]]
    
    for item_id, resolved_pre in resolved.items():
        if item_id in item_by_id:
            item_by_id[item_id]["resolved_pre"] = resolved_pre
    
    problem_pattern_sync_ready = []
    for candidate in problem_pattern_candidates:
        item_id = candidate["id"]
        item = item_by_id.get(item_id, {})
        
        if item:
            sync_entry = {
                "source_item_id": item_id,
                "source_item_name": item.get("name", ""),
                "suggested_pattern_id": f"planar.{item_id.split('.')[-1]}",
                "name": item.get("name", "").replace("平面图：", "").replace("特殊图：", ""),
                "en_name": item.get("en_name", "").replace("Planar Graph: ", "").replace("Special Graph: ", ""),
                "reason": candidate.get("reason", ""),
                "required_items": item.get("direct_pre", []),
                "tracks": item.get("tracks", []),
                "difficulty": "expert"
            }
            problem_pattern_sync_ready.append(sync_entry)
    
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_fix_applied_patch.json", 'w', encoding='utf-8') as f:
        json.dump(applied_patch, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_problem_pattern_sync_ready.json", 'w', encoding='utf-8') as f:
        json.dump(problem_pattern_sync_ready, f, ensure_ascii=False, indent=2)
    
    print("✅ Batch2 Fix completed")
    print(f"✅ Dependency fixes: {stats['dependency_fix_count']}")
    print(f"✅ Key prerequisites added: {stats['key_pre_requisites_added']}")
    print(f"✅ Review status patches: {stats['review_status_patch_count']}")
    print(f"✅ Problem pattern sync candidates: {stats['problem_pattern_sync_count']}")
    print(f"✅ Used official compute_resolved logic")
    
    return applied_patch, stats, problem_pattern_sync_ready

if __name__ == "__main__":
    applied_patch, stats, problem_pattern_sync_ready = main()