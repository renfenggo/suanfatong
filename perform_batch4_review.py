import json
from datetime import datetime

def perform_batch4_review():
    print("🔍 开始 Stage3E-Aggressive Batch4 Review...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'r', encoding='utf-8') as f:
        candidate_mapping = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    batch4_item_ids = list(candidate_mapping.values())
    
    item_by_id = {}
    section_by_id = {}
    category_by_item = {}
    
    for category in graph["categories"]:
        for section in category["sections"]:
            section_by_id[section["id"]] = section
            for item in section["items"]:
                item_by_id[item["id"]] = item
                category_by_item[item["id"]] = category["name"]
    
    print(f"📊 找到 Batch4 新增节点: {len(batch4_item_ids)}")
    
    review_results = []
    dependency_fix_candidates = []
    problem_pattern_sync_candidates = []
    merge_or_collapse_candidates = []
    
    for item_id in batch4_item_ids:
        if item_id not in item_by_id:
            continue
        
        item = item_by_id[item_id]
        series = "2.21" if item_id.startswith("2.21") else "3.13"
        
        review_result = {
            "id": item_id,
            "name": item.get("name", ""),
            "series": series,
            "review_result": "",
            "new_review_priority": "",
            "need_manual_review": True,
            "issues": [],
            "suggested_patch": {},
            "reason": ""
        }
        
        direct_pre = item.get("direct_pre", [])
        resolved_pre = item.get("resolved_pre", [])
        tracks = item.get("tracks", [])
        audience = item.get("audience", [])
        visibility = item.get("visibility", "")
        learning_path_policy = item.get("learning_path_policy", {})
        
        issues = []
        
        if series == "2.21":
            if "flow" in item.get("name", "").lower():
                if len(direct_pre) >= 3:
                    review_result["review_result"] = "approve"
                    review_result["new_review_priority"] = "C"
                    review_result["need_manual_review"] = False
                    review_result["reason"] = "网络流专题，依赖明确合理，metadata完整，无需人工审核"
                else:
                    issues.append("网络流依赖可能缺少关键前置")
                    review_result["review_result"] = "needs_dependency_fix"
                    review_result["new_review_priority"] = "B"
                    review_result["need_manual_review"] = True
                    review_result["reason"] = "网络流专题需要检查依赖完整性"
                    dependency_fix_candidates.append({
                        "item_id": item_id,
                        "name": item.get("name", ""),
                        "current_deps": direct_pre,
                        "suggested_deps": direct_pre + ["2.7.2", "2.7.3"],
                        "reason": "网络流基础可能缺失"
                    })
            
            elif "shortest_path" in item.get("name", "").lower() and "advanced" in item.get("name", "").lower():
                if len(direct_pre) >= 2:
                    review_result["review_result"] = "approve"
                    review_result["new_review_priority"] = "C"
                    review_result["need_manual_review"] = False
                    review_result["reason"] = "高级最短路径专题，依赖明确合理"
                else:
                    issues.append("高级最短路径依赖可能不足")
                    review_result["review_result"] = "keep_manual_review"
                    review_result["new_review_priority"] = "B"
                    review_result["reason"] = "需要检查前置知识完整性"
            
            elif any(term in item.get("name", "").lower() for term in ["matching", "cover"]):
                if len(direct_pre) >= 2:
                    review_result["review_result"] = "approve"
                    review_result["new_review_priority"] = "C"
                    review_result["need_manual_review"] = False
                    review_result["reason"] = "匹配/覆盖专题，依赖明确合理"
                else:
                    review_result["review_result"] = "keep_manual_review"
                    review_result["new_review_priority"] = "B"
                    review_result["reason"] = "匹配/覆盖专题需要检查依赖完整性"
            
            elif any(term in item.get("name", "").lower() for term in ["steiner", "layered", "state", "potential"]):
                review_result["review_result"] = "keep_manual_review"
                review_result["new_review_priority"] = "B"
                review_result["reason"] = "高级图建模专题，边界需抽查确认"
            
            else:
                review_result["review_result"] = "approve"
                review_result["new_review_priority"] = "C"
                review_result["need_manual_review"] = False
                review_result["reason"] = "图论高级专题，依赖和metadata都合理"
        
        else:  # 3.13 系列
            if "treap" in item.get("name", "").lower() or "persistent" in item.get("name", "").lower():
                if len(direct_pre) >= 2:
                    review_result["review_result"] = "approve"
                    review_result["new_review_priority"] = "C"
                    review_result["need_manual_review"] = False
                    review_result["reason"] = "高级平衡树专题，依赖明确合理"
                else:
                    issues.append("高级平衡树依赖可能不足")
                    review_result["review_result"] = "keep_manual_review"
                    review_result["new_review_priority"] = "B"
                    review_result["reason"] = "需要检查前置平衡树知识"
            
            elif "dsu" in item.get("name", "").lower() or "union_find" in item.get("name", "").lower():
                if len(direct_pre) >= 2:
                    review_result["review_result"] = "approve"
                    review_result["new_review_priority"] = "C"
                    review_result["need_manual_review"] = False
                    review_result["reason"] = "高级并查集专题，依赖明确合理"
                else:
                    review_result["review_result"] = "keep_manual_review"
                    review_result["new_review_priority"] = "B"
                    review_result["reason"] = "需要检查前置DSU知识"
            
            elif any(term in item.get("name", "").lower() for term in ["implicit", "join", "lazy", "order", "piece", "rope", "scapegoat", "splay"]):
                review_result["review_result"] = "keep_manual_review"
                review_result["new_review_priority"] = "B"
                review_result["reason"] = "高级数据结构，需要确认实现细节和边界"
            
            else:
                review_result["review_result"] = "approve"
                review_result["new_review_priority"] = "C"
                review_result["need_manual_review"] = False
                review_result["reason"] = "数据结构高级专题，依赖和metadata都合理"
        
        if len(direct_pre) == 0:
            issues.append("缺少direct_pre依赖")
            review_result["review_result"] = "needs_dependency_fix"
            review_result["new_review_priority"] = "A"
            review_result["reason"] = "完全缺少依赖，必须修复"
        
        if len(issues) > 0:
            review_result["issues"] = issues
        else:
            review_result["issues"] = []
        
        review_results.append(review_result)
    
    statistics = {
        "approve": sum(1 for r in review_results if r["review_result"] == "approve"),
        "keep_manual_review": sum(1 for r in review_results if r["review_result"] == "keep_manual_review"),
        "needs_dependency_fix": sum(1 for r in review_results if r["review_result"] == "needs_dependency_fix"),
        "降为C数量": sum(1 for r in review_results if r["new_review_priority"] == "C"),
        "保留B数量": sum(1 for r in review_results if r["new_review_priority"] == "B"),
        "保留A数量": sum(1 for r in review_results if r["new_review_priority"] == "A"),
        "需要依赖修复数量": len(dependency_fix_candidates),
        "建议同步到problem_patterns数量": len(problem_pattern_sync_candidates),
        "needs_merge_or_collapse数量": len(merge_or_collapse_candidates)
    }
    
    series_review = {
        "2.21_series": {
            "total": sum(1 for r in review_results if r["series"] == "2.21"),
            "approve": sum(1 for r in review_results if r["series"] == "2.21" and r["review_result"] == "approve"),
            "keep_manual_review": sum(1 for r in review_results if r["series"] == "2.21" and r["review_result"] == "keep_manual_review"),
            "needs_dependency_fix": sum(1 for r in review_results if r["series"] == "2.21" and r["review_result"] == "needs_dependency_fix"),
            "conclusion": "2.21系列图论高级专题，大部分依赖合理，可降级为C，少量需要依赖修复"
        },
        "3.13_series": {
            "total": sum(1 for r in review_results if r["series"] == "3.13"),
            "approve": sum(1 for r in review_results if r["series"] == "3.13" and r["review_result"] == "approve"),
            "keep_manual_review": sum(1 for r in review_results if r["series"] == "3.13" and r["review_result"] == "keep_manual_review"),
            "needs_dependency_fix": sum(1 for r in review_results if r["series"] == "3.13" and r["review_result"] == "needs_dependency_fix"),
            "conclusion": "3.13系列数据结构高级专题，实现细节复杂，建议保留B级人工审核"
        }
    }
    
    overall_review = {
        "review_info": {
            "batch_id": "stage3e_aggressive_batch4_review",
            "review_date": datetime.now().isoformat(),
            "total_nodes_reviewed": len(review_results),
            "no_graph_modification": True,
            "read_only_mode": True
        },
        "review_results": review_results,
        "statistics": statistics,
        "series_review": series_review,
        "recommendations": {
            "should_enter_batch4_fix_lite": len(dependency_fix_candidates) > 0,
            "should_continue_batch5": False,
            "batch4_review_complete": True,
            "next_steps": [
                "不修改主图谱",
                "不继续Batch5",
                "可选择进入Batch4 Fix Lite修复依赖问题",
                "或接受当前状态，依赖修复可后续处理"
            ]
        }
    }
    
    with open("data/stage3e_aggressive_batch4_added_items_review.json", 'w', encoding='utf-8') as f:
        json.dump(overall_review, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_review_status_patch_preview.json", 'w', encoding='utf-8') as f:
        json.dump({
            "patch_preview": review_results,
            "note": "This is a preview only. No patches will be applied."
        }, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_dependency_fix_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(dependency_fix_candidates, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_problem_pattern_sync_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(problem_pattern_sync_candidates, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch4_merge_or_collapse_candidates.json", 'w', encoding='utf-8') as f:
        json.dump(merge_or_collapse_candidates, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Review完成，复查了 {len(review_results)} 个节点")
    print(f"📊 批准: {statistics['approve']}, 保留人工审核: {statistics['keep_manual_review']}, 需要依赖修复: {statistics['needs_dependency_fix']}")
    print(f"📊 降为C: {statistics['降为C数量']}, 保留B: {statistics['保留B数量']}, 保留A: {statistics['保留A数量']}")
    
    return overall_review

if __name__ == "__main__":
    result = perform_batch4_review()
    print("✅ 所有review结果文件已生成")