import json
import copy

def apply_batch3_fix_lite():
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch3_review_status_patch_preview.json", 'r', encoding='utf-8') as f:
        patch_preview = json.load(f)
    
    with open("data/stage3e_aggressive_batch3_merge_or_collapse_candidates.json", 'r', encoding='utf-8') as f:
        merge_candidates_data = json.load(f)
    
    graph_original = copy.deepcopy(graph)
    applied_patch = []
    
    item_by_id = {}
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_by_id[item["id"]] = item
    
    for patch in patch_preview:
        item_id = patch["item_id"]
        if item_id not in item_by_id:
            print(f"⚠️  节点 {item_id} 不在图谱中，跳过")
            continue
        
        item = item_by_id[item_id]
        original_status = {
            "item_id": item_id,
            "original_need_manual_review": item.get("need_manual_review", True),
            "original_review_priority": item.get("review_priority", "B")
        }
        
        if "review_status" not in item:
            item["review_status"] = {}
        
        review_status = item["review_status"]
        
        review_status["need_manual_review"] = patch["new_need_manual_review"]
        review_status["review_priority"] = patch["new_review_priority"]
        
        if patch["action"] == "needs_merge_or_collapse":
            review_status["merge_or_collapse_review"] = True
            review_status["merge_or_collapse_reason"] = "Batch3 Review suggested possible over-splitting; keep as item for now, review later."
        
        applied_patch.append({
            "item_id": item_id,
            "original_status": original_status,
            "new_status": {
                "need_manual_review": patch["new_need_manual_review"],
                "review_priority": patch["new_review_priority"],
                "merge_or_collapse_review": review_status.get("merge_or_collapse_review", False),
                "merge_or_collapse_reason": review_status.get("merge_or_collapse_reason", "")
            },
            "action": patch["action"],
            "reason": patch["reason"]
        })
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_fix_lite_applied_patch.json", 'w', encoding='utf-8') as f:
        json.dump({
            "total_patches_applied": len(applied_patch),
            "patches": applied_patch,
            "backup_file": "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch3_fix_lite.json"
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 应用了 {len(applied_patch)} 个 review_status patches")
    print(f"✅ 备份文件已创建")
    
    return graph, applied_patch

def generate_merge_or_collapse_plan():
    with open("data/stage3e_aggressive_batch3_merge_or_collapse_candidates.json", 'r', encoding='utf-8') as f:
        merge_candidates_data = json.load(f)
    
    with open("data/stage3e_aggressive_batch3_added_items_summary.json", 'r', encoding='utf-8') as f:
        items_summary = json.load(f)
    
    item_summary_by_id = {}
    for item in items_summary:
        item_summary_by_id[item["item_id"]] = item
    
    merge_or_collapse_plan = []
    
    for candidate in merge_candidates_data["candidates"]:
        item_id = candidate["item_id"]
        item_summary = item_summary_by_id.get(item_id, {})
        series = candidate["series"]
        reason = candidate["reason"]
        suggested_patch = candidate.get("suggested_patch", {})
        
        suggested_action = "keep_for_now"
        suggested_merge_group = ""
        
        if "可持久化数据结构" in series:
            suggested_merge_group = "persistent_structure_methods"
            suggested_action = "merge_later"
            risk = "medium"
        elif "RMQ" in series:
            suggested_merge_group = "advanced_rmq_variants"
            suggested_action = "merge_later"
            risk = "medium"
        elif "简洁与概率结构" in series:
            suggested_merge_group = "succinct_probabilistic_structures"
            suggested_action = "collapse_later"
            risk = "low"
        else:
            suggested_action = "keep_for_now"
            risk = "low"
        
        merge_or_collapse_plan.append({
            "item_id": item_id,
            "name": candidate["name"],
            "series": series,
            "suggested_action": suggested_action,
            "suggested_merge_group": suggested_merge_group,
            "reason": reason,
            "risk": risk,
            "final_action_now": "keep_as_independent_item_with_B_review"
        })
    
    with open("data/stage3e_aggressive_batch3_merge_or_collapse_plan.json", 'w', encoding='utf-8') as f:
        json.dump({
            "total_candidates": len(merge_or_collapse_plan),
            "by_action": {
                "keep_for_now": len([p for p in merge_or_collapse_plan if p["suggested_action"] == "keep_for_now"]),
                "merge_later": len([p for p in merge_or_collapse_plan if p["suggested_action"] == "merge_later"]),
                "collapse_later": len([p for p in merge_or_collapse_plan if p["suggested_action"] == "collapse_later"])
            },
            "by_series": {
                "可持久化数据结构系列": len([p for p in merge_or_collapse_plan if "可持久化" in p["series"]]),
                "RMQ / 序列维护系列": len([p for p in merge_or_collapse_plan if "RMQ" in p["series"]]),
                "简洁与概率结构系列": len([p for p in merge_or_collapse_plan if "简洁" in p["series"]])
            },
            "plan": merge_or_collapse_plan
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成了 merge_or_collapse_plan，包含 {len(merge_or_collapse_plan)} 个候选")
    
    return merge_or_collapse_plan

if __name__ == "__main__":
    graph, applied_patch = apply_batch3_fix_lite()
    merge_or_collapse_plan = generate_merge_or_collapse_plan()
    
    print(f"✅ Batch3 Fix Lite 执行完成")
    print(f"✅ 应用了 {len(applied_patch)} 个 patches")
    print(f"✅ 生成了 {len(merge_or_collapse_plan)} 个合并/精简建议")