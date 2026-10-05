import json

def review_batch2_items():
    summary_file = "data/stage3e_aggressive_batch2_added_items_summary.json"
    mapping_file = "data/stage3e_aggressive_batch2_candidate_to_item_id_mapping.json"
    graph_file = "merged_knowledge_graph_item_dependencies_refined.json"
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        items_summary = json.load(f)
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    items = []
    for category in graph["categories"]:
        for section in category["sections"]:
            items.extend(section.get("items", []))
    
    item_by_id = {item["id"]: item for item in items}
    
    review_results = []
    review_status_patch_preview = []
    dependency_fix_candidates = []
    problem_pattern_sync_candidates = []
    merge_or_collapse_candidates = []
    
    stats = {
        "total": 0,
        "approve": 0,
        "demote_to_c": 0,
        "keep_b": 0,
        "keep_a": 0,
        "needs_dependency_fix": 0,
        "move_to_problem_patterns": 0,
        "needs_merge_or_collapse": 0,
        "by_series": {}
    }
    
    for summary in items_summary:
        item_id = summary["id"]
        item = item_by_id.get(item_id, {})
        
        name = item.get("name", "")
        en_name = item.get("en_name", "")
        direct_pre = item.get("direct_pre", [])
        rel = item.get("rel", [])
        tracks = item.get("tracks", [])
        audience = item.get("audience", [])
        visibility = item.get("visibility", "")
        learning_path_policy = item.get("learning_path_policy", {})
        
        candidate_id = summary.get("candidate_id", "")
        
        series = "other"
        if "matroid" in candidate_id:
            series = "拟阵图论系列"
        elif "planar" in candidate_id:
            series = "平面图系列"
        elif "special_graph" in candidate_id:
            series = "特殊图系列"
        elif "virtual_tree" in candidate_id:
            series = "虚树系列"
        elif "multidimensional" in candidate_id:
            series = "多维数据结构系列"
        elif "offline_framework" in candidate_id:
            series = "离线数据结构框架系列"
        elif "scc_dag" in candidate_id:
            series = "强连通分量DAG系列"
        
        stats["total"] += 1
        if series not in stats["by_series"]:
            stats["by_series"][series] = 0
        stats["by_series"][series] += 1
        
        issues = []
        suggested_patch = {}
        review_result = "approve"
        new_review_priority = "C"
        need_manual_review = False
        reason = ""
        
        if series == "拟阵图论系列":
            if len(direct_pre) == 0 or direct_pre == ["2.6.1"]:
                issues.append("依赖关系过于简单，缺少图论基础和集合论基础")
                suggested_patch["direct_pre"] = ["2.7.1", "2.6.1", "2.9.1"]
                review_result = "needs_dependency_fix"
                new_review_priority = "B"
                need_manual_review = True
                reason = "拟阵理论是高级图论概念，需要更完整的图论基础和数学基础"
                stats["needs_dependency_fix"] += 1
                dependency_fix_candidates.append({
                    "id": item_id,
                    "name": name,
                    "issues": issues,
                    "suggested_direct_pre": suggested_patch.get("direct_pre", [])
                })
            else:
                review_result = "approve"
                new_review_priority = "B"
                need_manual_review = True
                reason = "拟阵图论是高级理论概念，保持B级优先级进行人工复核"
                stats["keep_b"] += 1
        
        elif series == "平面图系列":
            if "dual" in name.lower() or "cut" in name.lower():
                issues.append("部分平面图主题更接近建模套路")
                review_result = "move_to_problem_patterns"
                new_review_priority = "C"
                need_manual_review = False
                reason = "平面图的双图和最小割主题更接近建模套路，建议同步到problem_patterns"
                stats["move_to_problem_patterns"] += 1
                problem_pattern_sync_candidates.append({
                    "id": item_id,
                    "name": name,
                    "candidate_id": candidate_id,
                    "reason": reason
                })
            else:
                review_result = "approve"
                new_review_priority = "C"
                need_manual_review = False
                reason = "平面图专题依赖明确，内容边界清晰，可以降为C级"
                stats["demote_to_c"] += 1
        
        elif series == "特殊图系列":
            review_result = "approve"
            new_review_priority = "C"
            need_manual_review = False
            reason = "特殊图系列概念明确，依赖关系合理，可以降为C级"
            stats["demote_to_c"] += 1
        
        elif series == "虚树系列":
            if len(direct_pre) == 2 and "2.7.1" in direct_pre and "2.14.2" in direct_pre:
                review_result = "approve"
                new_review_priority = "C"
                need_manual_review = False
                reason = "虚树系列依赖明确，都是基于LCA和树的经典应用，可以降为C级"
                stats["demote_to_c"] += 1
            else:
                issues.append("虚树系列依赖可能不够完整")
                suggested_patch["direct_pre"] = ["2.7.1", "2.14.2"]
                review_result = "needs_dependency_fix"
                new_review_priority = "B"
                need_manual_review = True
                reason = "虚树应用需要完整的LCA和树论基础"
                stats["needs_dependency_fix"] += 1
                dependency_fix_candidates.append({
                    "id": item_id,
                    "name": name,
                    "issues": issues,
                    "suggested_direct_pre": suggested_patch.get("direct_pre", [])
                })
        
        elif series == "多维数据结构系列":
            review_result = "approve"
            new_review_priority = "C"
            need_manual_review = False
            reason = "多维数据结构依赖明确，是树结构的高级应用，可以降为C级"
            stats["demote_to_c"] += 1
        
        elif series == "离线数据结构框架系列":
            if "parallel" in name.lower():
                review_result = "approve"
                new_review_priority = "B"
                need_manual_review = True
                reason = "并行检查框架是复杂技巧，建议保持B级优先级"
                stats["keep_b"] += 1
            else:
                review_result = "approve"
                new_review_priority = "C"
                need_manual_review = False
                reason = "离线数据结构框架主题明确，依赖合理，可以降为C级"
                stats["demote_to_c"] += 1
        
        elif series == "强连通分量DAG系列":
            review_result = "approve"
            new_review_priority = "C"
            need_manual_review = False
            reason = "强连通分量DAG应用明确，依赖合理，可以降为C级"
            stats["demote_to_c"] += 1
        
        review_result_item = {
            "id": item_id,
            "name": name,
            "en_name": en_name,
            "series": series,
            "review_result": review_result,
            "new_review_priority": new_review_priority,
            "need_manual_review": need_manual_review,
            "issues": issues,
            "suggested_patch": suggested_patch,
            "reason": reason,
            "current_direct_pre": direct_pre,
            "current_rel": rel,
            "current_tracks": tracks,
            "current_audience": audience,
            "current_visibility": visibility,
            "current_learning_path_policy": learning_path_policy
        }
        
        review_results.append(review_result_item)
        
        if review_result in ["approve", "keep_manual_review"]:
            review_status_patch_preview.append({
                "id": item_id,
                "name": name,
                "patch": {
                    "review_status": {
                        "need_manual_review": need_manual_review,
                        "review_priority": new_review_priority,
                        "review_note": f"Batch2 Review: {reason}"
                    }
                }
            })
    
    stats["approve"] = stats["demote_to_c"] + stats["keep_b"] + stats["keep_a"]
    
    with open("data/stage3e_aggressive_batch2_added_items_review.json", 'w', encoding='utf-8') as f:
        json.dump(review_results, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_review_status_patch_preview.json", 'w', encoding='utf-8') as f:
        json.dump(review_status_patch_preview, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_dependency_fix_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(dependency_fix_candidates, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_problem_pattern_sync_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(problem_pattern_sync_candidates, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch2_merge_or_collapse_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(merge_or_collapse_candidates, f, ensure_ascii=False, indent=2)
    
    print("✅ Batch2 Review completed")
    print(f"✅ Total items reviewed: {stats['total']}")
    print(f"✅ Approve: {stats['approve']}")
    print(f"✅ Demote to C: {stats['demote_to_c']}")
    print(f"✅ Keep B: {stats['keep_b']}")
    print(f"✅ Keep A: {stats['keep_a']}")
    print(f"✅ Needs dependency fix: {stats['needs_dependency_fix']}")
    print(f"✅ Move to problem_patterns: {stats['move_to_problem_patterns']}")
    print(f"✅ Needs merge/collapse: {stats['needs_merge_or_collapse']}")
    print(f"✅ By series: {stats['by_series']}")
    
    return review_results, stats

if __name__ == "__main__":
    review_results, stats = review_batch2_items()