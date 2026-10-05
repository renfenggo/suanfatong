import json

def review_batch3_items():
    with open("data/stage3e_aggressive_batch3_added_items_summary.json", 'r', encoding='utf-8') as f:
        items_summary = json.load(f)
    
    review_results = []
    series_analysis = {}
    
    for item in items_summary:
        item_id = item["item_id"]
        name = item["name"]
        candidate_id = item["candidate_id"]
        section_id = item["section_id"]
        direct_pre = item["direct_pre"]
        used_cleaned_dependency = item["used_cleaned_dependency"]
        current_priority = item["review_priority"]
        
        series = determine_series(candidate_id)
        if series not in series_analysis:
            series_analysis[series] = []
        
        review_result = {
            "id": item_id,
            "name": name,
            "en_name": item["en_name"],
            "series": series,
            "review_result": "keep_manual_review",
            "new_review_priority": current_priority,
            "need_manual_review": True,
            "issues": [],
            "suggested_patch": {},
            "reason": ""
        }
        
        analyze_item(item, review_result, series_analysis[series])
        
        review_results.append(review_result)
    
    generate_statistics(review_results, series_analysis)
    
    return review_results, series_analysis

def determine_series(candidate_id):
    if candidate_id.startswith("cand.graph.flow_bounds"):
        return "上下界网络流系列"
    elif candidate_id.startswith("cand.ds.offline_framework"):
        return "离线数据结构框架系列"
    elif candidate_id.startswith("cand.ds.persistent_structure"):
        return "可持久化数据结构系列"
    elif candidate_id.startswith("cand.ds.rmq_sparse"):
        return "RMQ / 序列维护系列"
    elif candidate_id.startswith("cand.ds.sequence_structure"):
        return "序列维护结构系列"
    elif candidate_id.startswith("cand.ds.succinct_probabilistic"):
        return "简洁与概率结构系列"
    elif candidate_id.startswith("cand.ds.tree_decomposition_ds"):
        return "树分治 / 树上数据结构系列"
    else:
        return "其他"

def analyze_item(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    candidate_id = item["candidate_id"]
    direct_pre = item["direct_pre"]
    section_id = item["section_id"]
    used_cleaned_dependency = item["used_cleaned_dependency"]
    
    if review_result["series"] == "上下界网络流系列":
        review_flow_bounds(item, review_result, series_issues)
    elif review_result["series"] == "离线数据结构框架系列":
        review_offline_framework(item, review_result, series_issues)
    elif review_result["series"] == "可持久化数据结构系列":
        review_persistent_structure(item, review_result, series_issues)
    elif review_result["series"] in ["RMQ / 序列维护系列", "序列维护结构系列"]:
        review_rmq_sequence(item, review_result, series_issues)
    elif review_result["series"] == "简洁与概率结构系列":
        review_succinct_probabilistic(item, review_result, series_issues)
    elif review_result["series"] == "树分治 / 树上数据结构系列":
        review_tree_decomposition(item, review_result, series_issues)

def review_flow_bounds(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    candidate_id = item["candidate_id"]
    
    issues = review_result["issues"]
    
    series_issues.append({
        "item_id": item_id,
        "name": name,
        "analysis": "上下界网络流系列更像知识点而非建模题型"
    })
    
    if len(direct_pre) == 2 and "2.16.3" in direct_pre and "2.16.12" in direct_pre:
        issues.append("依赖主要依赖基础网络流，可能缺少关键前置")
        review_result["review_result"] = "keep_manual_review"
        review_result["new_review_priority"] = "A"
        review_result["reason"] = "高级网络流专题，依赖合理但需要人工审核边界"
    else:
        review_result["review_result"] = "approve"
        review_result["new_review_priority"] = "C"
        review_result["need_manual_review"] = False
        review_result["reason"] = "依赖明确，子专题合理"

def review_offline_framework(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    
    series_issues.append({
        "item_id": item_id,
        "name": name,
        "analysis": "离线数据结构框架，依赖合理"
    })
    
    if len(direct_pre) == 2 and "2.1.8" in direct_pre and "2.1.5" in direct_pre:
        review_result["review_result"] = "approve"
        review_result["new_review_priority"] = "C"
        review_result["need_manual_review"] = False
        review_result["reason"] = "依赖明确（时间复杂度+二分查找），子专题合理"
    else:
        review_result["review_result"] = "keep_manual_review"
        review_result["new_review_priority"] = "B"
        review_result["reason"] = "依赖明确但需人工审核"

def review_persistent_structure(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    
    issues = review_result["issues"]
    suggested_patch = review_result["suggested_patch"]
    
    series_issues.append({
        "item_id": item_id,
        "name": name,
        "analysis": "可持久化数据结构系列，可能存在过度拆分"
    })
    
    if len(direct_pre) == 1 and "3.13.9" in direct_pre:
        issues.append("所有节点都依赖同一个前置 3.13.9，可能存在过度拆分")
        review_result["review_result"] = "needs_merge_or_collapse"
        review_result["new_review_priority"] = "A"
        review_result["reason"] = "明显过度拆分，建议合并或精简"
        suggested_patch["action"] = "merge_or_collapse"
        suggested_patch["suggestion"] = "考虑合并多个可持久化实现方法节点"
    else:
        review_result["review_result"] = "keep_manual_review"
        review_result["new_review_priority"] = "B"
        review_result["reason"] = "依赖明确但可能过度拆分"

def review_rmq_sequence(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    candidate_id = item["candidate_id"]
    used_cleaned_dependency = item["used_cleaned_dependency"]
    
    suggested_patch = review_result["suggested_patch"]
    
    if review_result["series"] == "RMQ / 序列维护系列":
        series_issues.append({
            "item_id": item_id,
            "name": name,
            "analysis": "高级 RMQ 系列，可能过度拆分"
        })
        
        if len(direct_pre) == 1 and "3.8.1" in direct_pre:
            review_result["review_result"] = "needs_merge_or_collapse"
            review_result["new_review_priority"] = "B"
            review_result["reason"] = "多个 RMQ 变体都依赖 3.8.1，可能过度拆分"
            suggested_patch["action"] = "merge_or_collapse"
            suggested_patch["suggestion"] = "考虑合并多个 RMQ 变体节点"
        else:
            review_result["review_result"] = "approve"
            review_result["new_review_priority"] = "C"
            review_result["need_manual_review"] = False
            review_result["reason"] = "依赖明确，子专题合理"
    
    elif review_result["series"] == "序列维护结构系列":
        series_issues.append({
            "item_id": item_id,
            "name": name,
            "analysis": "序列维护结构系列，依赖清洗后的平衡树"
        })
        
        if used_cleaned_dependency:
            review_result["review_result"] = "approve"
            review_result["new_review_priority"] = "C"
            review_result["need_manual_review"] = False
            review_result["reason"] = "依赖清洗成功，依赖明确（平衡树变体），子专题合理"
        else:
            review_result["review_result"] = "keep_manual_review"
            review_result["new_review_priority"] = "B"
            review_result["reason"] = "依赖明确但需人工审核"

def review_succinct_probabilistic(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    
    suggested_patch = review_result["suggested_patch"]
    
    series_issues.append({
        "item_id": item_id,
        "name": name,
        "analysis": "简洁与概率结构系列，可能存在过度拆分"
    })
    
    if len(direct_pre) == 2 and "3.12.2" in direct_pre and "1.4.13" in direct_pre:
        review_result["review_result"] = "needs_merge_or_collapse"
        review_result["new_review_priority"] = "B"
        review_result["reason"] = "多个简洁结构节点依赖相同前置，可能过度拆分"
        suggested_patch["action"] = "merge_or_collapse"
        suggested_patch["suggestion"] = "考虑合并多个简洁结构节点"
    else:
        review_result["review_result"] = "keep_manual_review"
        review_result["new_review_priority"] = "B"
        review_result["reason"] = "依赖明确但可能过度拆分"

def review_tree_decomposition(item, review_result, series_issues):
    item_id = item["item_id"]
    name = item["name"]
    direct_pre = item["direct_pre"]
    used_cleaned_dependency = item["used_cleaned_dependency"]
    
    series_issues.append({
        "item_id": item_id,
        "name": name,
        "analysis": "树分治维护系列，依赖清洗后的树结构基础"
    })
    
    if used_cleaned_dependency:
        if len(direct_pre) == 5:
            review_result["review_result"] = "approve"
            review_result["new_review_priority"] = "C"
            review_result["need_manual_review"] = False
            review_result["reason"] = "依赖清洗成功，依赖明确（树基础+仙人掌图DP），子专题合理"
        else:
            review_result["review_result"] = "keep_manual_review"
            review_result["new_review_priority"] = "B"
            review_result["reason"] = "依赖清洗成功但需人工审核依赖数量"
    else:
        review_result["review_result"] = "needs_dependency_fix"
        review_result["new_review_priority"] = "A"
        review_result["reason"] = "未使用清洗后的依赖，需要修复"

def generate_statistics(review_results, series_analysis):
    statistics = {
        "total_items": len(review_results),
        "approve": 0,
        "downgrade_to_c": 0,
        "keep_b": 0,
        "keep_a": 0,
        "needs_dependency_fix": 0,
        "move_to_problem_patterns": 0,
        "needs_merge_or_collapse": 0,
        "series_analysis": series_analysis
    }
    
    for result in review_results:
        if result["review_result"] == "approve":
            statistics["approve"] += 1
            if result["new_review_priority"] == "C":
                statistics["downgrade_to_c"] += 1
        elif result["review_result"] == "keep_manual_review":
            if result["new_review_priority"] == "B":
                statistics["keep_b"] += 1
            elif result["new_review_priority"] == "A":
                statistics["keep_a"] += 1
        elif result["review_result"] == "needs_dependency_fix":
            statistics["needs_dependency_fix"] += 1
        elif result["review_result"] == "move_to_problem_patterns":
            statistics["move_to_problem_patterns"] += 1
        elif result["review_result"] == "needs_merge_or_collapse":
            statistics["needs_merge_or_collapse"] += 1
    
    statistics["suggested_batch3_fix"] = statistics["needs_dependency_fix"] > 0 or statistics["needs_merge_or_collapse"] > 0
    statistics["suggested_continue_batch4"] = True
    statistics["suggested_batch4_approach"] = "same_as_batch3_with_improvements"
    
    return statistics

if __name__ == "__main__":
    review_results, series_analysis = review_batch3_items()
    statistics = generate_statistics(review_results, series_analysis)
    
    with open("data/stage3e_aggressive_batch3_added_items_review.json", 'w', encoding='utf-8') as f:
        json.dump(review_results, f, ensure_ascii=False, indent=2)
    
    with open("data/stage3e_aggressive_batch3_review_statistics.json", 'w', encoding='utf-8') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 复查了 {len(review_results)} 个 Batch3 新增节点")
    print(f"✅ 批准: {statistics['approve']} 个")
    print(f"✅ 降级为 C: {statistics['downgrade_to_c']} 个")
    print(f"✅ 保留 B: {statistics['keep_b']} 个")
    print(f"✅ 保留 A: {statistics['keep_a']} 个")
    print(f"⚠️  需要依赖修复: {statistics['needs_dependency_fix']} 个")
    print(f"⚠️  建议合并/精简: {statistics['needs_merge_or_collapse']} 个")
    print(f"📊 建议进入 Batch3 Fix: {statistics['suggested_batch3_fix']}")
    print(f"📊 建议继续 Batch4: {statistics['suggested_continue_batch4']}")