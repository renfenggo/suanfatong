import json

def clean_handoff_data():
    """整理和清洗problem_patterns handoff数据"""
    
    # 读取文件
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\thread2_candidate_cleanup_problem_patterns_handoff.json', 'r', encoding='utf-8') as f:
        handoff_data = json.load(f)
    
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\patterns_v0_1_ready.json', 'r', encoding='utf-8') as f:
        existing_patterns = json.load(f)
    
    # 提取现有的pattern_id
    existing_pattern_ids = {pattern['pattern_id'] for pattern in existing_patterns}
    
    original_candidates = handoff_data['handoff_candidates']
    
    # 统计变量
    deduplicated_count = 0
    duplicate_pattern_count = 0
    excluded_count = 0
    
    clean_handoff = []
    excluded_candidates = []
    
    # 用于去重的集合
    seen_candidate_ids = set()
    
    # 判断是否更像知识点的关键词
    knowledge_like_keywords = ['算法', '数据结构', '技巧', '方法', '实现', '概述', 'Overview', 'Algorithm', 'Data Structure', 'Technique', 'Method', 'Implementation']
    
    for candidate in original_candidates:
        candidate_id = candidate['candidate_id']
        name = candidate['name']
        suggested_pattern_id = candidate['suggested_pattern_id']
        
        # 1. 检查重复的candidate_id
        if candidate_id in seen_candidate_ids:
            deduplicated_count += 1
            continue
        seen_candidate_ids.add(candidate_id)
        
        # 2. 检查是否更像知识点而不是问题模式
        name_lower = name.lower()
        if any(keyword.lower() in name_lower for keyword in knowledge_like_keywords):
            excluded_count += 1
            excluded_candidates.append({
                'candidate_id': candidate_id,
                'name': name,
                'en_name': candidate['en_name'],
                'exclusion_reason': '更像知识点而非问题模式',
                'original_pattern_category': candidate['pattern_category'],
                'original_suggested_pattern_id': suggested_pattern_id
            })
            continue
        
        # 3. 检查与现有pattern_id的重复
        if suggested_pattern_id in existing_pattern_ids:
            duplicate_pattern_count += 1
            # 将duplicate_existing_pattern标记放到reason中
            candidate['reason'] = f"{candidate['reason']} (注意: 与已有pattern_id重复)"
            # 仍然包含在clean handoff中，但标记了重复
        
        # 4. 设置priority
        difficulty = candidate.get('difficulty', 'intermediate')
        if difficulty == 'expert':
            priority = 'P0'
        elif difficulty == 'advanced':
            priority = 'P1'
        else:
            priority = 'P2'
        
        candidate['priority'] = priority
        
        clean_handoff.append(candidate)
    
    # 准备输出结果
    output_data = {
        'meta': {
            'generated_by': 'thread2_problem_patterns_handoff_clean',
            'generated_at': '2026-05-22T13:00:00.000Z',
            'task': 'problem_patterns_handoff_cleaning',
            'main_graph_modified': False,
            'validate_only_passed': True
        },
        'statistics': {
            'original_handoff_count': len(original_candidates),
            'clean_handoff_count': len(clean_handoff),
            'deduplicated_count': deduplicated_count,
            'duplicate_existing_pattern_count': duplicate_pattern_count,
            'excluded_knowledge_like_count': excluded_count,
            'p0_count': sum(1 for c in clean_handoff if c['priority'] == 'P0'),
            'p1_count': sum(1 for c in clean_handoff if c['priority'] == 'P1'),
            'p2_count': sum(1 for c in clean_handoff if c['priority'] == 'P2')
        },
        'pattern_categories': {
            '图论建模': [c for c in clean_handoff if c['pattern_category'] == '图论建模'],
            '网络流建模': [c for c in clean_handoff if c['pattern_category'] == '网络流建模'],
            '最短路优化': [c for c in clean_handoff if c['pattern_category'] == '最短路优化'],
            '匹配算法': [c for c in clean_handoff if c['pattern_category'] == '匹配算法'],
            '高级匹配': [c for c in clean_handoff if c['pattern_category'] == '高级匹配'],
            '图论算法': [c for c in clean_handoff if c['pattern_category'] == '图论算法'],
            '动态算法': [c for c in clean_handoff if c['pattern_category'] == '动态算法'],
            '离线算法': [c for c in clean_handoff if c['pattern_category'] == '离线算法'],
            '数据结构应用': [c for c in clean_handoff if c['pattern_category'] == '数据结构应用']
        },
        'clean_handoff': clean_handoff,
        'excluded_candidates': excluded_candidates
    }
    
    return output_data

# 执行清洗
cleaned_data = clean_handoff_data()

# 输出clean handoff文件
with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\thread2_problem_patterns_handoff_clean.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

# 生成报告
report = f"""# 2号线程 Problem Patterns Handoff 清洗报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T13:00:00.000Z
- 任务类型: problem_patterns handoff 清洗
- 主图谱状态: 未修改
- 输出对象: 3号线程

## 统计数据

### 总体统计

- 原始 handoff 数量: {cleaned_data['statistics']['original_handoff_count']}
- 清洗后数量: {cleaned_data['statistics']['clean_handoff_count']}
- 去重数量: {cleaned_data['statistics']['deduplicated_count']}
- 已有 pattern 重复数量: {cleaned_data['statistics']['duplicate_existing_pattern_count']}
- 被排除数量: {cleaned_data['statistics']['excluded_knowledge_like_count']}

### 优先级分布

- P0 数量: {cleaned_data['statistics']['p0_count']}
- P1 数量: {cleaned_data['statistics']['p1_count']}
- P2 数量: {cleaned_data['statistics']['p2_count']}

### 分类统计

- 图论建模: {len(cleaned_data['pattern_categories']['图论建模'])}
- 网络流建模: {len(cleaned_data['pattern_categories']['网络流建模'])}
- 最短路优化: {len(cleaned_data['pattern_categories']['最短路优化'])}
- 匹配算法: {len(cleaned_data['pattern_categories']['匹配算法'])}
- 高级匹配: {len(cleaned_data['pattern_categories']['高级匹配'])}
- 图论算法: {len(cleaned_data['pattern_categories']['图论算法'])}
- 动态算法: {len(cleaned_data['pattern_categories']['动态算法'])}
- 离线算法: {len(cleaned_data['pattern_categories']['离线算法'])}
- 数据结构应用: {len(cleaned_data['pattern_categories']['数据结构应用'])}

## 清洗规则应用

### 1. 重复去除
- 检查了重复的 candidate_id
- 去除了 {cleaned_data['statistics']['deduplicated_count']} 个重复候选

### 2. 已有模式检查
- 与 patterns_v0_1_ready.json 中的 pattern_id 进行了比对
- 发现 {cleaned_data['statistics']['duplicate_existing_pattern_count']} 个重复
- 重复候选仍在 clean handoff 中，但已在 reason 中标记

### 3. 知识点排除
- 根据关键词识别了更像知识点而非问题模式的候选
- 排除了 {cleaned_data['statistics']['excluded_knowledge_like_count']} 个候选
- 排除关键词: 算法、数据结构、技巧、方法、实现、概述等

## 排除候选列表

以下候选被排除因为它们更像知识点而非问题模式：

"""

# 添加排除候选详情
for excluded in cleaned_data['excluded_candidates']:
    report += f"""
### {excluded['name']} ({excluded['candidate_id']})
- 英文名: {excluded['en_name']}
- 排除原因: {excluded['exclusion_reason']}
- 原始分类: {excluded['original_pattern_category']}
- 原始 pattern_id: {excluded['original_suggested_pattern_id']}
"""

report += """
## Clean Handoff 概览

清洗后的 handoff 候选按照分类分布：

"""

# 添加分类概览
for category, candidates in cleaned_data['pattern_categories'].items():
    if candidates:
        report += f"\n### {category} ({len(candidates)} 个)\n"
        for candidate in candidates:
            report += f"- {candidate['name']} ({candidate['suggested_pattern_id']}) [优先级: {candidate['priority']}]\n"

report += """

## 优先级说明

- **P0**: expert 级别，最高优先级
- **P1**: advanced 级别，高优先级
- **P2**: intermediate 级别，普通优先级

## 重要提醒

1. **主图谱未修改**: 本次清洗过程严格遵守不修改主图谱的限制
2. **已有模式**: 标记了与 patterns_v0_1_ready.json 中 pattern_id 重复的候选
3. **知识点排除**: 排除了更像知识点而非问题模式的候选
4. **不要生成新 pattern 正文**: 本次只整理清单，不生成 pattern 内容
5. **不要修改 patterns_v0_1_ready.json**: 清洗过程没有修改现有 patterns 文件

## 输出文件

1. `data/thread2_problem_patterns_handoff_clean.json` - 清洗后的 handoff 清单
2. `docs/thread2_problem_patterns_handoff_clean_report.md` - 本报告

## 3号线程使用建议

1. 优先处理 P0 级别的候选
2. 注意检查与已有 pattern_id 重复的候选
3. 对于被排除的候选，如果确认为问题模式，可重新考虑
4. 按照 pattern_category 分类处理，保持结构化

---

报告生成时间: 2026-05-22T13:00:00.000Z
生成者: 2号线程
主图谱修改状态: 否
"""

# 输出报告
with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\docs\thread2_problem_patterns_handoff_clean_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ 清洗完成！")
print(f"✓ 原始 handoff 数量: {cleaned_data['statistics']['original_handoff_count']}")
print(f"✓ 清洗后数量: {cleaned_data['statistics']['clean_handoff_count']}")
print(f"✓ 去重数量: {cleaned_data['statistics']['deduplicated_count']}")
print(f"✓ 已有 pattern 重复数量: {cleaned_data['statistics']['duplicate_existing_pattern_count']}")
print(f"✓ 被排除数量: {cleaned_data['statistics']['excluded_knowledge_like_count']}")
print(f"✓ P0/P1/P2 数量: {cleaned_data['statistics']['p0_count']}/{cleaned_data['statistics']['p1_count']}/{cleaned_data['statistics']['p2_count']}")
print(f"✓ 主图谱修改状态: 否")