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

def is_item_id(id_str):
    return '.' in id_str and any(c.isdigit() for c in id_str)

def main():
    graph_file = "merged_knowledge_graph_item_dependencies_refined.json"
    batches_file = "data/thread2_stage3e_aggressive_batches.json"
    cleaned_plan_file = "data/thread2_stage3e_aggressive_batch3_cleaned_dependency_plan.json"
    mapping_file1 = "data/stage3e_aggressive_batch1_candidate_to_item_id_mapping.json"
    mapping_file2 = "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json"
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open(batches_file, 'r', encoding='utf-8') as f:
        batches_data = json.load(f)
    
    with open(cleaned_plan_file, 'r', encoding='utf-8') as f:
        cleaned_plan = json.load(f)
    
    with open(mapping_file1, 'r', encoding='utf-8') as f:
        batch1_mapping = json.load(f)
    
    with open(mapping_file2, 'r', encoding='utf-8') as f:
        batch2_mapping = json.load(f)
    
    batch3_batch = None
    for batch in batches_data["batches"]:
        if batch["batch_id"] == "batch_3":
            batch3_batch = batch
            break
    
    if not batch3_batch:
        print("❌ 未找到 batch_3 数据")
        return
    
    print(f"✅ 找到 batch_3，数量: {batch3_batch['count']}")
    print(f"✅ 使用清洗后的依赖计划，清洗候选数: {cleaned_plan['bad_section_ref_candidate_count']}")
    
    all_item_ids = set()
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                all_item_ids.add(item["id"])
    
    batch1_item_ids = {item["item_id"] for item in batch1_mapping} if isinstance(batch1_mapping, list) else set(batch1_mapping.values())
    batch2_item_ids = set(batch2_mapping.values()) if isinstance(batch2_mapping, dict) else {item["item_id"] for item in batch2_mapping}
    all_item_ids.update(batch1_item_ids)
    all_item_ids.update(batch2_item_ids)
    
    cleaned_dependency_map = {}
    for cleaned in cleaned_plan.get("cleaned_candidates", []):
        cleaned_dependency_map[cleaned["candidate_id"]] = cleaned["cleaned_direct_pre_item_ids"]
    
    candidate_to_item_id = {}
    added_items_summary = []
    section_counters = {"2.21": 124, "3.13": 106}
    
    for candidate in batch3_batch["candidates"]:
        candidate_id = candidate["candidate_id"]
        target_section_id = candidate["target_section"]["id"]
        
        new_item_id = f"{target_section_id}.{section_counters[target_section_id]}"
        section_counters[target_section_id] += 1
        
        candidate_to_item_id[candidate_id] = new_item_id
        
        if candidate_id in cleaned_dependency_map:
            direct_pre_list = cleaned_dependency_map[candidate_id]
            print(f"✅ 使用清洗后的依赖: {candidate_id} -> {direct_pre_list}")
        else:
            direct_pre_list = []
            for dep in candidate.get("direct_pre", []):
                dep_id = dep["id"]
                dep_type = dep.get("type", "")
                
                if dep_type == "item" and dep_id in all_item_ids and is_item_id(dep_id):
                    if dep_id not in direct_pre_list:
                        direct_pre_list.append(dep_id)
                elif dep_type == "section":
                    pass
                else:
                    if dep_id in all_item_ids and is_item_id(dep_id) and dep_id not in direct_pre_list:
                        direct_pre_list.append(dep_id)
        
        review_priority = "B"
        if candidate.get("risk_band") == "yellow":
            review_priority = "A"
        
        added_items_summary.append({
            "candidate_id": candidate_id,
            "item_id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate["en_name"],
            "section_id": target_section_id,
            "direct_pre": direct_pre_list,
            "used_cleaned_dependency": candidate_id in cleaned_dependency_map,
            "risk_band": candidate.get("risk_band", "green"),
            "review_priority": review_priority
        })
    
    with open("data/stage3e_aggressive_batch3_candidate_to_item_id_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(candidate_to_item_id, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_added_items_summary.json", 'w', encoding='utf-8') as f:
        json.dump(added_items_summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成了 candidate_to_item_id_mapping 和 added_items_summary")
    print(f"✅ Batch3 新增节点分布: 2.21={section_counters['2.21']-124}, 3.13={section_counters['3.13']-106}")
    
    items_by_section = {"2.21": [], "3.13": []}
    
    for candidate in batch3_batch["candidates"]:
        candidate_id = candidate["candidate_id"]
        new_item_id = candidate_to_item_id[candidate_id]
        target_section_id = candidate["target_section"]["id"]
        
        if candidate_id in cleaned_dependency_map:
            direct_pre_list = cleaned_dependency_map[candidate_id]
        else:
            direct_pre_list = []
            for dep in candidate.get("direct_pre", []):
                dep_id = dep["id"]
                dep_type = dep.get("type", "")
                
                if dep_type == "item" and dep_id in all_item_ids and is_item_id(dep_id):
                    if dep_id not in direct_pre_list:
                        direct_pre_list.append(dep_id)
                elif dep_type == "section":
                    pass
                else:
                    if dep_id in all_item_ids and is_item_id(dep_id) and dep_id not in direct_pre_list:
                        direct_pre_list.append(dep_id)
        
        review_priority = "B"
        if candidate.get("risk_band") == "yellow":
            review_priority = "A"
        
        new_item = {
            "id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate["en_name"],
            "aliases": [],
            "global_aliases": [],
            "level": "advanced",
            "direct_pre": direct_pre_list,
            "resolved_pre": [],
            "rel": [],
            "tracks": ["advanced_data_structure", "advanced_graph"],
            "audience": ["advanced_competitive_programmer"],
            "visibility": "expert",
            "unlock_mode": "expert_branch",
            "learning_path_policy": {
                "show_in_beginner_path": False,
                "show_in_interview_path": False,
                "show_in_icpc_path": False,
                "show_in_noi_path": False,
                "unlock_mode": "expert_branch"
            },
            "localization_status": {
                "has_i18n_terms": False,
                "primary_language": "zh-Hans",
                "translation_confidence": "medium",
                "needs_native_review": True
            },
            "content_status": {
                "content_quality": "draft",
                "has_examples": False,
                "has_practice_problems": False
            },
            "platform_tags": [],
            "review_status": {
                "need_manual_review": True,
                "review_priority": review_priority,
                "reviewed_at": None,
                "reviewed_by": None
            }
        }
        
        items_by_section[target_section_id].append(new_item)
    
    for category in graph["categories"]:
        for section in category["sections"]:
            if section["id"] in items_by_section:
                section["items"].extend(items_by_section[section["id"]])
                print(f"✅ 向 section {section['id']} 添加了 {len(items_by_section[section['id']])} 个节点")
    
    all_edges = {}
    updated_all_item_ids = set()
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                updated_all_item_ids.add(item_id)
                direct_pre = item.get("direct_pre", [])
                all_edges[item_id] = []
                for dep in direct_pre:
                    if dep in updated_all_item_ids and dep != item_id:
                        all_edges[item_id].append(dep)
    
    resolved_results = compute_resolved(all_edges, updated_all_item_ids)
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_id = item["id"]
                if item_id in resolved_results:
                    item["resolved_pre"] = resolved_results[item_id]
    
    print("✅ 使用官方 compute_resolved 逻辑生成了 resolved_pre")
    
    validation_baseline = graph.get("meta", {}).get("validation_baseline", {})
    new_item_count = 1542 + 30
    validation_baseline["item_count"] = new_item_count
    validation_baseline["section_count"] = 65
    
    if "meta" not in graph:
        graph["meta"] = {}
    if "validation_baseline" not in graph["meta"]:
        graph["meta"]["validation_baseline"] = {}
    graph["meta"]["validation_baseline"] = validation_baseline
    
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 主图谱文件已更新，item_count 应为 {new_item_count}")
    
    return candidate_to_item_id, added_items_summary

if __name__ == "__main__":
    candidate_to_item_id, added_items_summary = main()