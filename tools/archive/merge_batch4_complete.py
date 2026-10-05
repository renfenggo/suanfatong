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

def is_item_id(item_id):
    return bool(re.match(r'^\d+\.\d+(\.\d+)*$', item_id))

def is_section_id(section_id):
    return bool(re.match(r'^\d+$', section_id))

def check_all_item_ids(dependencies):
    for dep in dependencies:
        if not is_item_id(dep):
            return False, dep
    return True, None

def merge_batch4():
    print("📖 读取数据文件...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/thread2_stage3e_aggressive_batch4_cleaned_dependency_plan.json", 'r', encoding='utf-8') as f:
        cleaned_plan = json.load(f)
    
    with open("data/external_candidate_pool_codex_batch_part1_combined.json", 'r', encoding='utf-8') as f:
        all_candidates = json.load(f)
    
    with open("data/thread2_stage3e_aggressive_batches.json", 'r', encoding='utf-8') as f:
        batches_data = json.load(f)
    
    candidate_by_id = {c["candidate_id"]: c for c in all_candidates}
    
    batch_4_info = None
    for batch in batches_data["batches"]:
        if batch["batch_id"] == "batch_4":
            batch_4_info = batch
            break
    
    if not batch_4_info:
        print("❌ 无法找到 batch_4 信息")
        return None
    
    print(f"✅ 找到 batch_4，共 {batch_4_info['count']} 个候选")
    print(f"📊 分布：2.21 ({batch_4_info['section_distribution']['2.21']}), 3.13 ({batch_4_info['section_distribution']['3.13']})")
    
    candidate_to_item_id = {}
    added_items_summary = []
    items_by_section = {}
    
    section_2_21_counter = 129
    section_3_13_counter = 131
    
    cleaned_candidate_map = {c["candidate_id"]: c for c in cleaned_plan["cleaned_candidates"]}
    
    print(f"🔧 清洗候选数：{len(cleaned_candidate_map)}")
    
    for candidate in batch_4_info["candidates"]:
        candidate_id = candidate["candidate_id"]
        full_candidate = candidate_by_id.get(candidate_id)
        
        if not full_candidate:
            print(f"⚠️  候选 {candidate_id} 不在原始候选池中，跳过")
            continue
        
        section_id = candidate["target_section"]["id"]
        target_section_name = candidate["target_section"]["name"]
        
        if section_id == "2.21":
            new_item_id = f"2.21.{section_2_21_counter}"
            section_2_21_counter += 1
        else:
            new_item_id = f"3.13.{section_3_13_counter}"
            section_3_13_counter += 1
        
        candidate_to_item_id[candidate_id] = new_item_id
        
        if candidate_id in cleaned_candidate_map:
            cleaned_info = cleaned_candidate_map[candidate_id]
            direct_pre = cleaned_info.get("cleaned_direct_pre_item_ids", [])
            used_cleaned_dependency = True
            
            check_result, invalid_dep = check_all_item_ids(direct_pre)
            if not check_result:
                print(f"❌ 清洗后的 {candidate_id} 包含非 item id 的依赖: {invalid_dep}")
                print("❌ 停止合并并恢复备份")
                return None
        else:
            direct_pre = [dep["id"] for dep in candidate["direct_pre"] if dep["type"] == "item"]
            used_cleaned_dependency = False
            
            check_result, invalid_dep = check_all_item_ids(direct_pre)
            if not check_result:
                print(f"❌ {candidate_id} 包含非 item id 的依赖: {invalid_dep}")
                print("❌ 停止合并并恢复备份")
                return None
            
            unique_direct_pre = []
            seen = set()
            for dep in direct_pre:
                if dep not in seen:
                    seen.add(dep)
                    unique_direct_pre.append(dep)
            direct_pre = unique_direct_pre
        
        item = {
            "id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate["en_name"],
            "aliases": full_candidate.get("aliases", []),
            "global_aliases": full_candidate.get("global_aliases", []),
            "level": full_candidate.get("level", "expert"),
            "direct_pre": direct_pre,
            "resolved_pre": [],
            "rel": [],
            "tracks": full_candidate.get("tracks", ["icpc", "ioi", "noi"]),
            "audience": full_candidate.get("audience", ["university_icpc", "high_school_oi"]),
            "visibility": full_candidate.get("visibility", "expert"),
            "learning_path_policy": {
                "unlock_mode": full_candidate.get("learning_path_policy", {}).get("unlock_mode", "expert_branch"),
                "path_order": full_candidate.get("learning_path_policy", {}).get("path_order", 999),
                "optional": False
            },
            "localization_status": "ready",
            "content_status": "draft",
            "platform_tags": full_candidate.get("platform_tags", []),
            "review_status": {
                "need_manual_review": True,
                "review_priority": "A" if "graph_modeling" in candidate_id or "flow_bounds" in candidate_id or "matching_cover" in candidate_id else "B"
            }
        }
        
        added_items_summary.append({
            "candidate_id": candidate_id,
            "item_id": new_item_id,
            "name": candidate["name"],
            "en_name": candidate["en_name"],
            "section_id": section_id,
            "section_name": target_section_name,
            "direct_pre": direct_pre,
            "used_cleaned_dependency": used_cleaned_dependency,
            "risk_band": candidate.get("risk_band", "yellow"),
            "review_priority": item["review_status"]["review_priority"],
            "rank_in_batch": candidate["rank_in_batch"]
        })
        
        if section_id not in items_by_section:
            items_by_section[section_id] = []
        items_by_section[section_id].append(item)
    
    if len(added_items_summary) != 30:
        print(f"❌ 预期合并30个候选，实际准备 {len(added_items_summary)} 个")
        print("❌ 停止合并并恢复备份")
        return None
    
    print(f"✅ 所有30个候选检查通过，开始插入图谱...")
    
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
    
    print(f"📝 基于 {len(item_by_id)} 个节点（旧节点: {len(old_item_ids)}, 新增节点: {len(new_item_ids)}）计算 resolved_pre...")
    
    resolved_results = compute_resolved(edges, set(item_by_id.keys()))
    
    only_update_count = 0
    skip_count = 0
    
    for item_id in new_item_ids:
        if item_id in resolved_results:
            item_by_id[item_id]["resolved_pre"] = resolved_results[item_id]
            only_update_count += 1
    
    for item_id in old_item_ids:
        skip_count += 1
    
    print(f"✅ 只更新了 {only_update_count} 个新增节点的 resolved_pre")
    print(f"✅ 跳过了 {skip_count} 个现有节点的 resolved_pre")
    
    new_nodes_dependencies = 0
    for item_id in new_item_ids:
        for dep in item_by_id[item_id]["direct_pre"]:
            if dep in new_item_ids:
                new_nodes_dependencies += 1
    
    print(f"📊 新增节点之间的依赖关系数量: {new_nodes_dependencies}")
    
    section_distribution = {}
    for summary in added_items_summary:
        section_id = summary["section_id"]
        if section_id not in section_distribution:
            section_distribution[section_id] = 0
        section_distribution[section_id] += 1
    
    print(f"📊 新增节点分布:")
    for section_id, count in section_distribution.items():
        print(f"   {section_id}: {count}")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(candidate_to_item_id, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'w', encoding='utf-8') as f:
        json.dump(added_items_summary, f, ensure_ascii=False, indent=2)
    
    return graph, added_items_summary, new_nodes_dependencies, section_distribution

if __name__ == "__main__":
    result = merge_batch4()
    if result:
        graph, added_items_summary, new_nodes_dependencies, section_distribution = result
        print(f"✅ Batch4 合并完成")
        print(f"✅ 新增了 {len(added_items_summary)} 个节点")
        print(f"✅ 主图谱已更新，准备验证")
    else:
        print(f"❌ Batch4 合并失败，已停止")
        print(f"🔄 请手动恢复备份")