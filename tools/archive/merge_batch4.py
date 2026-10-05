import json
import copy
import re

def compute_resolved(edges, node_set):
    memo = {}
    
    def dfs(node):
        if node in memo:
            return memo[node]
        
        if node not in node_set:
            return []
        
        if node not in edges:
            memo[node] = []
            return []
        
        resolved = []
        for dep in edges[node]:
            if dep in node_set and dep != node:
                resolved.extend(dfs(dep))
        
        resolved.extend(edges[node])
        
        seen = set()
        unique_resolved = []
        for dep in resolved:
            if dep not in seen and dep != node:
                seen.add(dep)
                unique_resolved.append(dep)
        
        memo[node] = unique_resolved
        return unique_resolved
    
    result = {}
    for node in node_set:
        result[node] = dfs(node)
    
    return result

def merge_batch4():
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/thread2_stage3e_aggressive_batch4_cleaned_dependency_plan.json", 'r', encoding='utf-8') as f:
        cleaned_plan = json.load(f)
    
    with open("data/external_candidate_pool_codex_batch_part1_combined.json", 'r', encoding='utf-8') as f:
        all_candidates = json.load(f)
    
    candidate_by_id = {c["candidate_id"]: c for c in all_candidates}
    
    candidate_to_item_id = {}
    added_items_summary = []
    items_by_section = {}
    
    section_2_21_counter = 129
    section_3_13_counter = 131
    
    cleaned_candidate_map = {c["candidate_id"]: c for c in cleaned_plan["cleaned_candidates"]}
    
    for cleaned_candidate in cleaned_plan["cleaned_candidates"]:
        candidate_id = cleaned_candidate["candidate_id"]
        candidate = candidate_by_id.get(candidate_id)
        
        if not candidate:
            print(f"⚠️  候选 {candidate_id} 不在原始候选池中，跳过")
            continue
        
        section_id = cleaned_candidate.get("target_section_id")
        
        if "graph" in candidate_id or "graph_modeling" in candidate_id:
            section_id = "2.21"
            new_item_id = f"2.21.{section_2_21_counter}"
            section_2_21_counter += 1
        else:
            section_id = "3.13"
            new_item_id = f"3.13.{section_3_13_counter}"
            section_3_13_counter += 1
        
        candidate_to_item_id[candidate_id] = new_item_id
        
        direct_pre = cleaned_candidate.get("cleaned_direct_pre_item_ids", [])
        used_cleaned_dependency = candidate_id in cleaned_candidate_map
        
        item = {
            "id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate.get("en_name", candidate["name"]),
            "aliases": candidate.get("aliases", []),
            "global_aliases": candidate.get("global_aliases", []),
            "level": candidate.get("level", "expert"),
            "direct_pre": direct_pre,
            "resolved_pre": [],
            "rel": [],
            "tracks": candidate.get("tracks", ["icpc", "ioi", "noi"]),
            "audience": candidate.get("audience", ["university_icpc", "high_school_oi"]),
            "visibility": candidate.get("visibility", "expert"),
            "learning_path_policy": {
                "unlock_mode": candidate.get("learning_path_policy", {}).get("unlock_mode", "expert_branch"),
                "path_order": candidate.get("learning_path_policy", {}).get("path_order", 999),
                "optional": False
            },
            "localization_status": "ready",
            "content_status": "draft",
            "platform_tags": candidate.get("platform_tags", []),
            "review_status": {
                "need_manual_review": True,
                "review_priority": "A" if "graph_modeling" in candidate_id else "B"
            }
        }
        
        added_items_summary.append({
            "candidate_id": candidate_id,
            "item_id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate.get("en_name", candidate["name"]),
            "section_id": section_id,
            "direct_pre": direct_pre,
            "used_cleaned_dependency": used_cleaned_dependency,
            "risk_band": candidate.get("risk_band", "green"),
            "review_priority": item["review_status"]["review_priority"]
        })
        
        if section_id not in items_by_section:
            items_by_section[section_id] = []
        items_by_section[section_id].append(item)
    
    for category in graph["categories"]:
        for section in category["sections"]:
            if section["id"] in items_by_section:
                section["items"].extend(items_by_section[section["id"]])
    
    old_item_ids = set()
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if item["id"] not in [summary["item_id"] for summary in added_items_summary]:
                    old_item_ids.add(item["id"])
    
    new_item_ids = set([summary["item_id"] for summary in added_items_summary])
    
    item_by_id = {}
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_by_id[item["id"]] = item
    
    edges = {}
    for item_id, item in item_by_id.items():
        direct_pre = item.get("direct_pre", [])
        edges[item_id] = []
        for dep in direct_pre:
            if dep in item_by_id and dep != item_id:
                edges[item_id].append(dep)
    
    resolved_results = compute_resolved(edges, set(item_by_id.keys()))
    
    only_update_count = 0
    skip_count = 0
    
    for item_id in new_item_ids:
        if item_id in resolved_results:
            item_by_id[item_id]["resolved_pre"] = resolved_results[item_id]
            only_update_count += 1
    
    for item_id in old_item_ids:
        skip_count += 1
    
    print(f"完整 item_by_id 大小: {len(item_by_id)} (旧节点: {len(old_item_ids)}, 新增节点: {len(new_item_ids)})")
    print(f"只更新了 {only_update_count} 个新增节点的 resolved_pre")
    print(f"跳过了 {skip_count} 个现有节点的 resolved_pre")
    
    new_nodes_dependencies = 0
    for item_id in new_item_ids:
        for dep in item_by_id[item_id]["direct_pre"]:
            if dep in new_item_ids:
                new_nodes_dependencies += 1
    
    print(f"新增节点之间的依赖关系数量: {new_nodes_dependencies}")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(candidate_to_item_id, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'w', encoding='utf-8') as f:
        json.dump(added_items_summary, f, ensure_ascii=False, indent=2)
    
    return graph, added_items_summary, new_nodes_dependencies

if __name__ == "__main__":
    graph, added_items_summary, new_nodes_dependencies = merge_batch4()
    print(f"✅ Batch4 合并完成")
    print(f"✅ 新增了 {len(added_items_summary)} 个节点")
    print(f"✅ 合并后主图谱已更新")