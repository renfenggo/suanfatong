import json
from datetime import datetime

def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out

def build_indexes(graph):
    item_by_id, section_by_id = {}, {}
    category_by_item, section_by_item = {}, {}
    section_name_by_item, all_items = {}, []
    duplicate_item_ids = []
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            section_by_id[section["id"]] = section
            for item in section.get("items", []):
                if item["id"] in item_by_id:
                    duplicate_item_ids.append(item["id"])
                item_by_id[item["id"]] = item
                category_by_item[item["id"]] = category["name"]
                section_by_item[item["id"]] = section["id"]
                section_name_by_item[item["id"]] = section["name"]
                all_items.append(item)
    return {
        "item_by_id": item_by_id,
        "section_by_id": section_by_id,
        "category_by_item": category_by_item,
        "section_by_item": section_by_item,
        "section_name_by_item": section_name_by_item,
        "items": all_items,
        "duplicate_item_ids": duplicate_item_ids,
    }

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

def debug_batch4_expected_resolved_pre():
    print("🔍 使用 validator 同源逻辑生成 Batch4 新增节点的 expected_resolved_pre...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_candidate_to_item_id_mapping.json", 'r', encoding='utf-8') as f:
        candidate_mapping = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    batch4_item_ids = list(candidate_mapping.values())
    
    print(f"📊 Batch4 新增节点数: {len(batch4_item_ids)}")
    
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    expected = compute_resolved(edges, set(item_by_id))
    
    results = []
    
    for item_id in batch4_item_ids:
        if item_id in item_by_id:
            old_resolved_pre = item_by_id[item_id].get("resolved_pre", [])
            expected_resolved_pre = expected[item_id]
            
            old_len = len(old_resolved_pre)
            expected_len = len(expected_resolved_pre)
            
            old_set = set(old_resolved_pre)
            expected_set = set(expected_resolved_pre)
            
            same_set = old_set == expected_set
            same_order = old_resolved_pre == expected_resolved_pre
            
            missing_items = list(expected_set - old_set) if not same_set else []
            extra_items = list(old_set - expected_set) if not same_set else []
            
            first_order_diff_index = -1
            if not same_order and len(old_resolved_pre) == len(expected_resolved_pre):
                for i, (old, new) in enumerate(zip(old_resolved_pre, expected_resolved_pre)):
                    if old != new:
                        first_order_diff_index = i
                        break
            
            result = {
                "item_id": item_id,
                "name": item_by_id[item_id]["name"],
                "old_resolved_pre": old_resolved_pre,
                "expected_resolved_pre": expected_resolved_pre,
                "old_len": old_len,
                "expected_len": expected_len,
                "same_set": same_set,
                "same_order": same_order,
                "missing_items": missing_items,
                "extra_items": extra_items,
                "first_order_diff_index": first_order_diff_index
            }
            
            results.append(result)
            
            print(f"📝 {item_id}: old_len={old_len}, expected_len={expected_len}, same_set={same_set}, same_order={same_order}")
    
    same_set_count = sum(1 for r in results if r["same_set"])
    same_order_count = sum(1 for r in results if r["same_order"])
    
    print(f"📊 统计: same_set={same_set_count}/{len(results)}, same_order={same_order_count}/{len(results)}")
    
    summary = {
        "batch_id": "stage3e_aggressive_batch4_resolved_pre_exact_fix",
        "generated_at": datetime.now().isoformat(),
        "batch4_node_count": len(batch4_item_ids),
        "results": results,
        "statistics": {
            "total_nodes": len(results),
            "same_set_count": same_set_count,
            "same_order_count": same_order_count,
            "needs_fix_count": len(results) - same_order_count
        }
    }
    
    with open("data/stage3e_aggressive_batch4_expected_resolved_pre.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ expected_resolved_pre 已生成并保存到 data/stage3e_aggressive_batch4_expected_resolved_pre.json")
    
    return summary

if __name__ == "__main__":
    debug_batch4_expected_resolved_pre()