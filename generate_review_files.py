import json

def generate_review_files():
    with open("data/stage3e_aggressive_batch3_review_statistics.json", 'r', encoding='utf-8') as f:
        statistics = json.load(f)
    
    with open("data/stage3e_aggressive_batch3_added_items_review.json", 'r', encoding='utf-8') as f:
        review_results = json.load(f)
    
    review_status_patch = []
    dependency_fix_candidates = []
    problem_pattern_sync_candidates = []
    merge_or_collapse_candidates = []
    
    for result in review_results:
        item_id = result["id"]
        review_result_val = result["review_result"]
        new_priority = result["new_review_priority"]
        need_manual = result["need_manual_review"]
        
        patch_entry = {
            "item_id": item_id,
            "current_need_manual_review": True,
            "new_need_manual_review": need_manual,
            "current_review_priority": "A" if review_result_val in ["keep_manual_review", "needs_merge_or_collapse"] else "B",
            "new_review_priority": new_priority,
            "action": review_result_val,
            "reason": result["reason"],
            "issues": result["issues"],
            "suggested_patch": result["suggested_patch"]
        }
        
        review_status_patch.append(patch_entry)
        
        if review_result_val == "needs_dependency_fix":
            dependency_fix_candidates.append({
                "item_id": item_id,
                "name": result["name"],
                "series": result["series"],
                "issues": result["issues"],
                "suggested_patch": result["suggested_patch"]
            })
        
        if review_result_val == "move_to_problem_patterns":
            problem_pattern_sync_candidates.append({
                "item_id": item_id,
                "name": result["name"],
                "series": result["series"],
                "reason": result["reason"]
            })
        
        if review_result_val == "needs_merge_or_collapse":
            merge_or_collapse_candidates.append({
                "item_id": item_id,
                "name": result["name"],
                "series": result["series"],
                "reason": result["reason"],
                "suggested_patch": result["suggested_patch"]
            })
    
    with open("data/stage3e_aggressive_batch3_review_status_patch_preview.json", 'w', encoding='utf-8') as f:
        json.dump(review_status_patch, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_dependency_fix_candidates.json", 'w', encoding='utf-8') as f:
        json.dump({
            "total_candidates": len(dependency_fix_candidates),
            "candidates": dependency_fix_candidates
        }, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_problem_pattern_sync_candidates.json", 'w', encoding='utf-8') as f:
        json.dump({
            "total_candidates": len(problem_pattern_sync_candidates),
            "candidates": problem_pattern_sync_candidates
        }, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_merge_or_collapse_candidates.json", 'w', encoding='utf-8') as f:
        json.dump({
            "total_candidates": len(merge_or_collapse_candidates),
            "candidates": merge_or_collapse_candidates
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成了 review_status_patch 预览文件")
    print(f"✅ 生成了 dependency_fix_candidates 文件: {len(dependency_fix_candidates)} 个")
    print(f"✅ 生成了 problem_pattern_sync_candidates 文件: {len(problem_pattern_sync_candidates)} 个")
    print(f"✅ 生成了 merge_or_collapse_candidates 文件: {len(merge_or_collapse_candidates)} 个")

if __name__ == "__main__":
    generate_review_files()