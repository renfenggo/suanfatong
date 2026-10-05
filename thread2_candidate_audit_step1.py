import json
import os
import re

def load_json_file(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def validate_candidate_id(candidate_id, existing_candidate_ids, existing_item_ids):
    """
    验证 candidate_id 是否规范
    格式应为 cand.<domain>.<topic>.<subtopic>
    """
    issues = []
    
    # 检查格式
    if not candidate_id.startswith('cand.'):
        issues.append("ID 不以 'cand.' 开头")
        return False, issues
    
    # 检查是否有足够数量的点分隔符
    parts = candidate_id.split('.')
    if len(parts) < 4:
        issues.append(f"ID 格式不正确，应为 cand.<domain>.<topic>.<subtopic>，实际有 {len(parts)} 个部分")
        return False, issues
    
    # 检查是否包含中文拼音
    if re.search(r'[a-z]*[a-z]*[a-z]*[a-z]*[a-z]*', candidate_id):
        # 这里需要更复杂的逻辑来判断是否是拼音
        pass
    
    # 检查是否与现有候选ID重复
    if candidate_id in existing_candidate_ids:
        issues.append(f"与现有候选ID重复: {candidate_id}")
    
    # 检查是否与现有item ID冲突 (简单检查，实际可能需要更复杂的逻辑)
    if candidate_id.replace('cand.', '') in existing_item_ids:
        issues.append(f"与现有item ID冲突: {candidate_id}")
    
    # 检查是否使用随机ID
    if any(len(part) < 2 for part in parts if part):
        issues.append("ID 包含过短的部分，可能是随机ID")
    
    return len(issues) == 0, issues

def check_field_completeness(candidate):
    """检查候选的字段完整性"""
    required_fields = [
        'candidate_id',
        'name', 
        'en_name',
        'category_suggestion',
        'section_suggestion',
        'level',
        'difficulty',
        'tracks',
        'audience',
        'visibility',
        'learning_path_policy',
        'reason_to_add',
        'global_relevance',
        'direct_pre_suggestion',
        'rel_suggestion',
        'parent_concept_suggestion',
        'merge_check',
        'i18n_seed',
        'content_status',
        'review_status'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in candidate:
            missing_fields.append(field)
        elif candidate[field] is None:
            missing_fields.append(f"{field} (值为null)")
        elif isinstance(candidate[field], list) and len(candidate[field]) == 0 and field not in ['tracks', 'audience', 'direct_pre_suggestion', 'rel_suggestion']:
            missing_fields.append(f"{field} (空列表)")
    
    return len(missing_fields) == 0, missing_fields

def determine_recommended_destination(candidate):
    """
    判断候选的推荐目标
    - knowledge_items: 适合作为知识点
    - problem_patterns: 更像题型模式
    - problem_refs: 更像具体题目映射
    - i18n_only: 只是术语别名，不适合做知识点
    """
    name = candidate.get('name', '').lower()
    en_name = candidate.get('en_name', '').lower()
    category = candidate.get('category_suggestion', '').lower()
    reason = candidate.get('reason_to_add', '').lower()
    
    # 检查是否只是术语别名
    if '术语' in name or 'alias' in en_name or '翻译' in reason or '翻译' in name:
        if len(candidate.get('reason_to_add', '')) < 20:
            return 'i18n_only'
    
    # 检查是否是具体题目
    if '题目' in name or 'problem' in en_name and 'leetcode' in en_name:
        if '具体题目' in reason or '特定题目' in reason:
            return 'problem_refs'
    
    # 检查是否是题型模式
    if '题型' in name or 'pattern' in en_name or '模板' in name:
        if '题型' in category or '模式' in reason:
            return 'problem_patterns'
    
    # 默认作为知识点
    return 'knowledge_items'

def calculate_initial_quality_score(candidate, field_complete, id_valid, id_issues, missing_fields):
    """计算初始质量分数 (0-100)"""
    score = 100
    
    # 字段完整性扣分
    if not field_complete:
        score -= 30  # 字段不完整大幅扣分
        score -= min(20, len(missing_fields) * 2)  # 每个缺失字段扣2分
    
    # ID 有效性扣分
    if not id_valid:
        score -= 20  # ID 不有效扣分
        score -= min(15, len(id_issues) * 3)  # 每个ID问题扣3分
    
    # 内容状态扣分
    content_status = candidate.get('content_status', '')
    if content_status == 'outline':
        score -= 5  # 只有大纲轻微扣分
    elif content_status == 'empty' or content_status == '':
        score -= 15  # 无内容明显扣分
    
    # 重复性检查
    merge_check = candidate.get('merge_check', {})
    if merge_check.get('is_duplicate'):
        if merge_check.get('duplicate_type') == 'exact_name':
            score -= 40  # 完全重名严重扣分
        elif merge_check.get('duplicate_type') == 'similar_name':
            score -= 20  # 名称相似中度扣分
    
    # 确保分数在0-100范围内
    return max(0, min(100, score))

def identify_blocking_issues(candidate, id_valid, id_issues, missing_fields, field_complete):
    """识别阻塞问题"""
    blocking_issues = []
    
    # ID 问题通常是阻塞的
    if not id_valid:
        blocking_issues.extend([f"ID问题: {issue}" for issue in id_issues])
    
    # 关键字段缺失
    critical_fields = ['candidate_id', 'name', 'en_name', 'category_suggestion', 'section_suggestion']
    for field in critical_fields:
        if field in missing_fields or f"{field} (值为null)" in missing_fields:
            blocking_issues.append(f"关键字段缺失: {field}")
    
    # 重复性问题
    merge_check = candidate.get('merge_check', {})
    if merge_check.get('is_duplicate') and merge_check.get('duplicate_type') == 'exact_name':
        blocking_issues.append(f"完全重复: 与 {merge_check.get('matching_item_ids', [])} 重名")
    
    return blocking_issues

def main():
    base_path = r'C:\Users\renfenggo\Documents\trae_projects\suanfatong'
    
    # 读取候选文件
    candidates_file = os.path.join(base_path, 'data', 'candidate_new_knowledge_items_batch1.json')
    candidates = load_json_file(candidates_file)
    
    if not candidates:
        print("❌ 无法读取候选文件")
        return
    
    print(f"✅ 成功读取 {len(candidates)} 个候选")
    
    # 读取主图谱以获取现有item ID (简化版本，实际可能需要从主图谱文件读取)
    # 这里先假设有一些已知的item ID模式
    existing_item_ids = set()
    
    # 模拟现有item ID (实际应该从主图谱文件读取)
    for i in range(1, 65):  # 64个sections
        for j in range(1, 30):  # 假设每个section最多30个items
            existing_item_ids.add(f"{i}.{j}")
    
    # 执行审计
    audit_results = []
    existing_candidate_ids = set()
    
    for candidate in candidates:
        candidate_id = candidate.get('candidate_id', '')
        existing_candidate_ids.add(candidate_id)
        
        # 检查字段完整性
        field_complete, missing_fields = check_field_completeness(candidate)
        
        # 检查ID有效性
        id_valid, id_issues = validate_candidate_id(candidate_id, set(), existing_item_ids)
        
        # 判断推荐目标
        recommended_destination = determine_recommended_destination(candidate)
        
        # 计算质量分数
        initial_quality_score = calculate_initial_quality_score(
            candidate, field_complete, id_valid, id_issues, missing_fields
        )
        
        # 识别阻塞问题
        blocking_issues = identify_blocking_issues(
            candidate, id_valid, id_issues, missing_fields, field_complete
        )
        
        audit_result = {
            "candidate_id": candidate_id,
            "name": candidate.get('name', ''),
            "en_name": candidate.get('en_name', ''),
            "field_complete": field_complete,
            "missing_fields": missing_fields,
            "id_valid": id_valid,
            "id_issues": id_issues,
            "recommended_destination": recommended_destination,
            "initial_quality_score": initial_quality_score,
            "blocking_issues": blocking_issues
        }
        
        audit_results.append(audit_result)
    
    # 保存审计结果
    output_file = os.path.join(base_path, 'data', 'thread2_candidate_quality_audit_step1.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 审计结果已保存到 {output_file}")
    
    # 生成统计报告
    total_candidates = len(audit_results)
    field_complete_count = sum(1 for r in audit_results if r['field_complete'])
    id_valid_count = sum(1 for r in audit_results if r['id_valid'])
    
    destination_distribution = {}
    for result in audit_results:
        dest = result['recommended_destination']
        destination_distribution[dest] = destination_distribution.get(dest, 0) + 1
    
    low_quality_candidates = [r for r in audit_results if r['initial_quality_score'] < 60]
    blocking_issue_candidates = [r for r in audit_results if r['blocking_issues']]
    
    print(f"\n=== 审计统计 ===")
    print(f"候选总数: {total_candidates}")
    print(f"字段完整: {field_complete_count} ({field_complete_count/total_candidates*100:.1f}%)")
    print(f"ID合法: {id_valid_count} ({id_valid_count/total_candidates*100:.1f}%)")
    print(f"\n推荐目标分布:")
    for dest, count in destination_distribution.items():
        print(f"  {dest}: {count} ({count/total_candidates*100:.1f}%)")
    print(f"\n低质量候选 (分数<60): {len(low_quality_candidates)}")
    print(f"有阻塞问题的候选: {len(blocking_issue_candidates)}")
    
    return audit_results, destination_distribution, low_quality_candidates, blocking_issue_candidates

if __name__ == "__main__":
    main()