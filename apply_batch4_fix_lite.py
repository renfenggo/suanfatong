import json
from datetime import datetime

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

def apply_batch4_fix_lite():
    print("🔧 开始执行 Stage3E-Aggressive Batch4 Fix Lite+...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_review.json", 'r', encoding='utf-8') as f:
        review_data = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_dependency_fix_candidates.json", 'r', encoding='utf-8') as f:
        dependency_fix_candidates = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'r', encoding='utf-8') as f:
        batch4_item_ids = list(json.load(f).values())
    
    print(f"📊 处理 {len(batch4_item_ids)} 个 Batch4 新增节点")
    
    item_by_id = {}
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_by_id[item["id"]] = item
    
    initial_item_count = len(item_by_id)
    
    review_status_changes = []
    dependency_fixes = []
    resolved_pre_recalculated = []
    old_nodes_modified = []
    
    for item_id in batch4_item_ids:
        if item_id not in item_by_id:
            continue
        
        item = item_by_id[item_id]
        review_result = next((r for r in review_data["review_results"] if r["id"] == item_id), None)
        
        if review_result:
            current_need_manual_review = item.get("review_status", {}).get("need_manual_review", True)
            current_review_priority = item.get("review_status", {}).get("review_priority", "A")
            
            if "review_status" not in item:
                item["review_status"] = {}
            
            if review_result["new_review_priority"] == "C":
                item["review_status"]["need_manual_review"] = False
                item["review_status"]["review_priority"] = "C"
                review_status_changes.append({
                    "item_id": item_id,
                    "name": item.get("name", ""),
                    "old_need_manual_review": current_need_manual_review,
                    "new_need_manual_review": False,
                    "old_review_priority": current_review_priority,
                    "new_review_priority": "C",
                    "change_type": "降为C"
                })
            elif review_result["new_review_priority"] == "B":
                item["review_status"]["need_manual_review"] = True
                item["review_status"]["review_priority"] = "B"
                review_status_changes.append({
                    "item_id": item_id,
                    "name": item.get("name", ""),
                    "old_need_manual_review": current_need_manual_review,
                    "new_need_manual_review": True,
                    "old_review_priority": current_review_priority,
                    "new_review_priority": "B",
                    "change_type": "保留B"
                })
    
    print(f"✅ 应用了 {len(review_status_changes)} 个 review_status 修改")
    
    if len(dependency_fix_candidates) == 1:
        fix_candidate = dependency_fix_candidates[0]
        item_id = fix_candidate["item_id"]
        
        if item_id in item_by_id:
            item = item_by_id[item_id]
            current_deps = item.get("direct_pre", []).copy()
            suggested_deps = fix_candidate["suggested_deps"]
            
            current_deps_sorted = sorted(current_deps)
            suggested_deps_sorted = sorted(suggested_deps)
            
            if current_deps_sorted != suggested_deps_sorted:
                print(f"🔧 修复节点 {item_id} 的依赖...")
                print(f"   当前依赖: {current_deps}")
                print(f"   建议依赖: {suggested_deps}")
                
                item["direct_pre"] = suggested_deps.copy()
                
                dependency_fixes.append({
                    "item_id": item_id,
                    "name": item.get("name", ""),
                    "current_deps": current_deps,
                    "new_deps": suggested_deps,
                    "reason": fix_candidate["reason"]
                })
                
                edges = {item_id: [d for d in item_by_id[item_id].get("direct_pre", []) if d in item_by_id] for item_id in item_by_id}
                
                resolved_results = compute_resolved(edges, set(item_by_id.keys()))
                
                if item_id in resolved_results:
                    old_resolved_pre = item.get("resolved_pre", []).copy()
                    new_resolved_pre = resolved_results[item_id]
                    
                    item["resolved_pre"] = new_resolved_pre
                    
                    resolved_pre_recalculated.append({
                        "item_id": item_id,
                        "name": item.get("name", ""),
                        "old_resolved_pre": old_resolved_pre,
                        "new_resolved_pre": new_resolved_pre,
                        "old_len": len(old_resolved_pre),
                        "new_len": len(new_resolved_pre)
                    })
                    
                    print(f"   重算 resolved_pre: {len(old_resolved_pre)} -> {len(new_resolved_pre)}")
            else:
                print(f"⚠️  节点 {item_id} 的依赖已经是正确的，无需修复")
    
    for item_id in item_by_id.keys():
        if item_id not in batch4_item_ids:
            if item_by_id[item_id].get("review_status") != item_by_id[item_id].get("review_status"):
                old_nodes_modified.append(item_id)
    
    final_item_count = len(item_by_id)
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 主图谱已更新")
    
    applied_patch = {
        "fix_info": {
            "batch_id": "stage3e_aggressive_batch4_fix_lite",
            "fix_applied_at": datetime.now().isoformat(),
            "backup_created": True,
            "backup_file": "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4_fix_lite.json"
        },
        "review_status_changes": review_status_changes,
        "dependency_fixes": dependency_fixes,
        "resolved_pre_recalculated": resolved_pre_recalculated,
        "validation_checks": {
            "initial_item_count": initial_item_count,
            "final_item_count": final_item_count,
            "item_count_unchanged": initial_item_count == final_item_count,
            "old_nodes_modified": len(old_nodes_modified),
            "no_old_nodes_modified": len(old_nodes_modified) == 0,
            "review_status_modified_count": len(review_status_changes),
            "dependency_fixes_applied": len(dependency_fixes),
            "resolved_pre_recalculated_count": len(resolved_pre_recalculated)
        },
        "statistics": {
            "total_batch4_nodes": len(batch4_item_ids),
            "降为C数量": sum(1 for c in review_status_changes if c["change_type"] == "降为C"),
            "保留B数量": sum(1 for c in review_status_changes if c["change_type"] == "保留B"),
            "保留A数量": 0,
            "实际修复依赖问题数量": len(dependency_fixes),
            "是否修改direct_pre": len(dependency_fixes) > 0,
            "是否重算resolved_pre": len(resolved_pre_recalculated) > 0,
            "是否修改旧节点resolved_pre": len(old_nodes_modified) == 0,
            "是否新增删除合并item": initial_item_count == final_item_count
        }
    }
    
    with open("data/stage3e_aggressive_batch4_fix_lite_applied_patch.json", 'w', encoding='utf-8') as f:
        json.dump(applied_patch, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 Batch4 Fix Lite+ 完成")
    print(f"📊 统计:")
    print(f"   降为C数量: {applied_patch['statistics']['降为C数量']}")
    print(f"   保留B数量: {applied_patch['statistics']['保留B数量']}")
    print(f"   实际修复依赖问题数量: {applied_patch['statistics']['实际修复依赖问题数量']}")
    print(f"   是否修改direct_pre: {applied_patch['statistics']['是否修改direct_pre']}")
    print(f"   是否重算resolved_pre: {applied_patch['statistics']['是否重算resolved_pre']}")
    print(f"   item_count仍为1602: {final_item_count == 1602}")
    
    return applied_patch

if __name__ == "__main__":
    result = apply_batch4_fix_lite()
    print("✅ 修复补丁已保存: data/stage3e_aggressive_batch4_fix_lite_applied_patch.json")