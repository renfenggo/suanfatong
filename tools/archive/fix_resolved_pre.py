import json

def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out

def detect_cycle(edges, item_ids):
    color, stack = {}, []

    def dfs(node):
        color[node] = 1
        stack.append(node)
        for dep in edges.get(node, []):
            if dep not in item_ids:
                continue
            if color.get(dep) == 1:
                return stack[stack.index(dep):] + [dep]
            if color.get(dep) != 2:
                cycle = dfs(dep)
                if cycle:
                    return cycle
        stack.pop()
        color[node] = 2
        return None

    for item_id in item_ids:
        if color.get(item_id) is None:
            cycle = dfs(item_id)
            if cycle:
                return cycle
    return None

def level_num(level):
    import re
    m = re.search(r"\d+", str(level or ""))
    return int(m.group()) if m else 3

def break_cycles(edges, item_by_id):
    fixes = []
    item_ids = set(item_by_id)
    while True:
        cycle = detect_cycle(edges, item_ids)
        if not cycle:
            return fixes
        pairs = list(zip(cycle, cycle[1:]))

        def edge_score(pair):
            src, dep = pair
            src_item, dep_item = item_by_id[src], item_by_id[dep]
            src_level, dep_level = level_num(src_item.get("level")), level_num(dep_item.get("level"))
            score = 0
            if src_level <= dep_level:
                score += 30
            if src_item.get("parent") == dep_item.get("parent"):
                score += 10
            if src_item.get("parent", "").startswith("1.") and not dep_item.get("parent", "").startswith("1."):
                score += 100
            if src_level <= 2:
                score += 20
            return score, src

        src, dep = max(pairs, key=edge_score)
        if dep in edges.get(src, []):
            edges[src].remove(dep)
            fixes.append({"removed_from": src, "removed_dependency": dep, "cycle": cycle})
        else:
            raise RuntimeError(f"Cannot break cycle: {cycle}")

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

def build_indexes(graph):
    item_by_id = {}
    all_items = []
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                item_by_id[item["id"]] = item
                all_items.append(item)
    return {
        "item_by_id": item_by_id,
        "items": all_items,
    }

def recompute_resolved_pre(graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    fixes = break_cycles(edges, item_by_id)
    resolved = compute_resolved(edges, set(item_by_id))
    for item in idx["items"]:
        item["direct_pre"] = edges[item["id"]]
        item["resolved_pre"] = resolved[item["id"]]
    return fixes

def main():
    graph_file = "merged_knowledge_graph_item_dependencies_refined.json"
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    
    new_item_ids = set()
    for category in graph["categories"]:
        for section in category["sections"]:
            if section["id"] in ["2.21", "3.13"]:
                for item in section["items"]:
                    if item["id"] not in item_by_id:
                        item_by_id[item["id"]] = item
                    if section["id"] == "2.21" and item["id"].startswith("2.21.124"):
                        new_item_ids.add(item["id"])
                    elif section["id"] == "3.13" and item["id"].startswith("3.13.106"):
                        new_item_ids.add(item["id"])
    
    print(f"✅ 新增节点 ID 集合大小: {len(new_item_ids)}")
    
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    
    cycle_before = detect_cycle(edges, set(item_by_id))
    if cycle_before:
        print(f"⚠️  检测到环: {cycle_before}")
    
    fixes = break_cycles(edges, item_by_id)
    if fixes:
        print(f"✅ 打破了 {len(fixes)} 个环")
        for fix in fixes:
            print(f"   从 {fix['removed_from']} 移除依赖 {fix['removed_dependency']}")
    
    cycle_after = detect_cycle(edges, set(item_by_id))
    if cycle_after:
        print(f"❌ 仍然有环: {cycle_after}")
    
    resolved = compute_resolved(edges, set(item_by_id))
    
    only_update_count = 0
    skip_update_count = 0
    mismatch_count = 0
    
    for item in idx["items"]:
        item_id = item["id"]
        expected_resolved_pre = resolved[item_id]
        current_resolved_pre = item.get("resolved_pre", [])
        
        if item_id in new_item_ids:
            if current_resolved_pre != expected_resolved_pre:
                item["resolved_pre"] = expected_resolved_pre
                only_update_count += 1
                print(f"⚠️  新增节点 {item_id} 的 resolved_pre 不匹配")
                print(f"   期望: {len(expected_resolved_pre)}, 实际: {len(current_resolved_pre)}")
                mismatch_count += 1
        else:
            skip_update_count += 1
    
    print(f"✅ 更新了 {only_update_count} 个新增节点的 resolved_pre")
    print(f"✅ 跳过了 {skip_update_count} 个现有节点的 resolved_pre")
    print(f"⚠️  {mismatch_count} 个新增节点 resolved_pre 不匹配")
    
    validation_baseline = graph.get("meta", {}).get("validation_baseline", {})
    new_item_count = 1572
    validation_baseline["item_count"] = new_item_count
    validation_baseline["section_count"] = 65
    
    if "meta" not in graph:
        graph["meta"] = {}
    if "validation_baseline" not in graph["meta"]:
        graph["meta"]["validation_baseline"] = {}
    graph["meta"]["validation_baseline"] = validation_baseline
    
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 主图谱文件已更新")
    return fixes, mismatch_count

if __name__ == "__main__":
    fixes, mismatch_count = main()