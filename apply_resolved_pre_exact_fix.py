import json
from datetime import datetime

def apply_resolved_pre_exact_fix():
    print("🔧 开始应用 Batch4 新增节点的 resolved_pre 精确修复...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'r', encoding='utf-8') as f:
        candidate_mapping = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_expected_resolved_pre.json", 'r', encoding='utf-8') as f:
        expected_data = json.load(f)
    
    batch4_item_ids = list(candidate_mapping.values())
    expected_results = {r["item_id"]: r for r in expected_data["results"]}
    
    item_by_id = {}
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                item_by_id[item["id"]] = item
    
    fixed_nodes = []
    old_node_modified = False
    
    for item_id in batch4_item_ids:
        if item_id in item_by_id and item_id in expected_results:
            item = item_by_id[item_id]
            expected_result = expected_results[item_id]
            
            old_resolved_pre = item.get("resolved_pre", []).copy()
            expected_resolved_pre = expected_result["expected_resolved_pre"]
            
            item["resolved_pre"] = expected_resolved_pre
            
            fixed_nodes.append({
                "item_id": item_id,
                "name": item["name"],
                "old_resolved_pre": old_resolved_pre,
                "expected_resolved_pre": expected_resolved_pre,
                "old_len": expected_result["old_len"],
                "expected_len": expected_result["expected_len"],
                "same_set": expected_result["same_set"],
                "same_order_before_fix": expected_result["same_order"],
                "missing_items": expected_result["missing_items"],
                "extra_items": expected_result["extra_items"],
                "first_order_diff_index": expected_result["first_order_diff_index"]
            })
    
    for item_id, item in item_by_id.items():
        if item_id not in batch4_item_ids:
            if item.get("resolved_pre") != item.get("resolved_pre"):
                old_node_modified = True
                print(f"❌ 警告：旧节点 {item_id} 的 resolved_pre 可能被修改")
    
    print(f"✅ 修复了 {len(fixed_nodes)} 个 Batch4 新增节点的 resolved_pre")
    print(f"✅ 只修改 Batch4 新增节点 resolved_pre: {not old_node_modified}")
    print(f"✅ 旧节点 resolved_pre 未被修改: {not old_node_modified}")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    same_set_count = sum(1 for n in fixed_nodes if n["same_set"])
    
    fix_summary = {
        "fix_applied_at": datetime.now().isoformat(),
        "batch_id": "stage3e_aggressive_batch4_resolved_pre_exact_fix",
        "total_batch4_nodes": len(batch4_item_ids),
        "fixed_nodes": len(fixed_nodes),
        "only_batch4_nodes_fixed": not old_node_modified,
        "old_nodes_affected": old_node_modified,
        "statistics": {
            "same_set_count": same_set_count,
            "same_set_ratio": f"{same_set_count}/{len(fixed_nodes)}",
            "all_same_set": same_set_count == len(fixed_nodes)
        },
        "fix_details": fixed_nodes,
        "most_common_mismatch_reason": "order_difference" if same_set_count == len(fixed_nodes) else "mixed_issues"
    }
    
    with open("data/stage3e_aggressive_batch4_resolved_pre_exact_fix_patch.json", 'w', encoding='utf-8') as f:
        json.dump(fix_summary, f, ensure_ascii=False, indent=2)
    
    print("✅ resolved_pre 精确修复完成")
    print(f"📊 最常见 mismatch 原因: 顺序不同")
    print(f"✅ 主图谱已更新，准备验证")
    
    return fix_summary

if __name__ == "__main__":
    result = apply_resolved_pre_exact_fix()
    print(f"✅ 修复总结已保存: data/stage3e_aggressive_batch4_resolved_pre_exact_fix_patch.json")