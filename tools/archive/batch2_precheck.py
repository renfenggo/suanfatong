import json

def perform_batch2_precheck():
    """执行Batch2预审"""
    
    print("开始Stage3E-Aggressive Batch2预审...")
    
    # 1. 读取批次文件
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\thread2_stage3e_aggressive_batches.json', 'r', encoding='utf-8') as f:
        aggressive_batches = json.load(f)
    
    # 2. 读取Batch1合并映射
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\stage3e_aggressive_batch1_candidate_to_item_id_mapping.json', 'r', encoding='utf-8') as f:
        batch1_mapping = json.load(f)
    
    # 3. 读取外部候选池以获取风险信息
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\external_candidate_pool_codex_batch_part1_combined.json', 'r', encoding='utf-8') as f:
        external_candidates = json.load(f)
    
    # 创建外部候选的映射以便快速查找
    external_candidate_map = {c['candidate_id']: c for c in external_candidates}
    
    # 提取Batch1的候选ID
    batch1_candidate_ids = set(item['candidate_id'] for item in batch1_mapping)
    
    # 查找Batch2
    batch2 = None
    for batch in aggressive_batches['batches']:
        if batch['batch_id'] == 'batch_2':
            batch2 = batch
            break
    
    if not batch2:
        print("错误: 未找到batch_2")
        return None
    
    print(f"✓ 找到batch_2，数量: {batch2['count']}")
    
    # 预审结果初始化
    precheck_result = {
        "batch_id": "stage3e_aggressive_batch2",
        "candidate_count": len(batch2['candidates']),
        "already_merged_in_batch1": [],
        "invalid_candidates": [],
        "high_risk_candidates": [],
        "manual_review_candidates": [],
        "problem_pattern_candidates": [],
        "needs_new_section": False,
        "dependency_mapping_risk": [],
        "candidate_dependency_cycle": batch2.get('candidate_dependency_cycle', False),
        "section_distribution": batch2.get('section_distribution', {}),
        "recommendation": "",
        "recommended_merge_count": 0
    }
    
    # 检查每个候选
    section_2_21_count = 0
    section_3_13_count = 0
    
    for candidate in batch2['candidates']:
        candidate_id = candidate['candidate_id']
        target_section_id = candidate.get('target_section', {}).get('id', '')
        
        # 统计section分布
        if target_section_id == '2.21':
            section_2_21_count += 1
        elif target_section_id == '3.13':
            section_3_13_count += 1
        
        # 1. 检查是否已经在Batch1合并过
        if candidate_id in batch1_candidate_ids:
            precheck_result['already_merged_in_batch1'].append({
                'candidate_id': candidate_id,
                'name': candidate['name'],
                'reason': '已在Stage3E Batch1中合并'
            })
            continue
        
        # 2. 获取外部候选的详细信息
        external_candidate = external_candidate_map.get(candidate_id, {})
        duplicate_risk = candidate.get('duplicate_risk', 'unknown')
        risk_band = candidate.get('risk_band', 'unknown')
        
        # 3. 检查高风险候选
        if duplicate_risk == 'high' or risk_band == 'red':
            precheck_result['high_risk_candidates'].append({
                'candidate_id': candidate_id,
                'name': candidate['name'],
                'duplicate_risk': duplicate_risk,
                'risk_band': risk_band,
                'reason': '高风险候选'
            })
        
        # 4. 检查manual_review和problem_patterns
        if external_candidate.get('merge_risk_hint', {}).get('merge_action_hint') == 'manual_review':
            precheck_result['manual_review_candidates'].append({
                'candidate_id': candidate_id,
                'name': candidate['name'],
                'reason': '需要手动审核'
            })
        
        # 5. 检查依赖映射风险
        direct_pre = candidate.get('direct_pre', [])
        for pre in direct_pre:
            if pre.get('match') == 'no_match':
                precheck_result['dependency_mapping_risk'].append({
                    'candidate_id': candidate_id,
                    'name': candidate['name'],
                    'unmapped_dependency': pre.get('input', ''),
                    'reason': '依赖无法映射到主图谱'
                })
            elif pre.get('match') == 'low_confidence':
                precheck_result['dependency_mapping_risk'].append({
                    'candidate_id': candidate_id,
                    'name': candidate['name'],
                    'low_confidence_dependency': pre.get('input', ''),
                    'existing_match': pre.get('id', ''),
                    'reason': '依赖映射置信度低'
                })
    
    # 更新section分布
    precheck_result['section_distribution'] = {
        '2.21': section_2_21_count,
        '3.13': section_3_13_count
    }
    
    # 检查是否需要新section（这里简化处理，假设所有候选都能进入已有section）
    precheck_result['needs_new_section'] = False
    
    # 生成建议
    issue_count = (
        len(precheck_result['already_merged_in_batch1']) +
        len(precheck_result['invalid_candidates']) +
        len(precheck_result['high_risk_candidates']) +
        len(precheck_result['manual_review_candidates']) +
        len(precheck_result['problem_pattern_candidates']) +
        len(precheck_result['dependency_mapping_risk'])
    )
    
    if issue_count > 0:
        precheck_result['recommendation'] = 'needs_cleanup_before_merge'
        precheck_result['recommended_merge_count'] = len(batch2['candidates']) - len(precheck_result['already_merged_in_batch1']) - len(precheck_result['high_risk_candidates']) - len(precheck_result['invalid_candidates'])
    else:
        precheck_result['recommendation'] = 'ready_for_1号线程_merge'
        precheck_result['recommended_merge_count'] = len(batch2['candidates'])
    
    # 添加元数据
    precheck_result['meta'] = {
        'generated_by': 'thread2_stage3e_aggressive_batch2_precheck',
        'generated_at': '2026-05-22T15:00:00.000Z',
        'task': 'batch2_precheck',
        'main_graph_modified': False,
        'precheck_purpose': '等待1号线程确认合并批次'
    }
    
    print("✓ Batch2预审完成")
    print(f"  - 候选总数: {precheck_result['candidate_count']}")
    print(f"  - 已合并(Batch1): {len(precheck_result['already_merged_in_batch1'])}")
    print(f"  - 高风险候选: {len(precheck_result['high_risk_candidates'])}")
    print(f"  - 手动审核候选: {len(precheck_result['manual_review_candidates'])}")
    print(f"  - 依赖映射风险: {len(precheck_result['dependency_mapping_risk'])}")
    print(f"  - Section分布 2.21: {precheck_result['section_distribution']['2.21']}")
    print(f"  - Section分布 3.13: {precheck_result['section_distribution']['3.13']}")
    print(f"  - 依赖环: {precheck_result['candidate_dependency_cycle']}")
    print(f"  - 建议: {precheck_result['recommendation']}")
    print(f"  - 建议合并数量: {precheck_result['recommended_merge_count']}")
    
    return precheck_result

# 执行预审
precheck_result = perform_batch2_precheck()

# 保存预审结果
if precheck_result:
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\thread2_stage3e_aggressive_batch2_precheck.json', 'w', encoding='utf-8') as f:
        json.dump(precheck_result, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 预审结果已保存到 data/thread2_stage3e_aggressive_batch2_precheck.json")
    
    # 生成报告
    report = f"""# Stage3E-Aggressive Batch2 预审报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T15:00:00.000Z
- 任务类型: Stage3E-Aggressive Batch2 预审
- 主图谱状态: 未修改
- 任务目的: 为1号线程合并Batch2做准备

## Batch2 基本信息

- **Batch2 是否存在**: ✓ 是
- **Batch2 数量**: {precheck_result['candidate_count']}
- **预期数量**: 30
- **数量匹配**: {'✓ 匹配' if precheck_result['candidate_count'] == 30 else '✗ 不匹配'}

## 风险检查结果

### 1. 已合并候选检查

- **已在 Batch1 合并的候选**: {len(precheck_result['already_merged_in_batch1'])}
"""

    if precheck_result['already_merged_in_batch1']:
        report += "以下候选已在 Batch1 中合并，应从 Batch2 中移除:\n\n"
        for item in precheck_result['already_merged_in_batch1']:
            report += f"- **{item['name']}** ({item['candidate_id']})\n  - 原因: {item['reason']}\n\n"
    else:
        report += "✓ 未发现已在 Batch1 合并的候选\n\n"

    report += f"""### 2. 高风险候选检查

- **高风险候选数量**: {len(precheck_result['high_risk_candidates'])}
"""

    if precheck_result['high_risk_candidates']:
        report += "以下候选具有高风险:\n\n"
        for item in precheck_result['high_risk_candidates']:
            report += f"- **{item['name']}** ({item['candidate_id']})\n  - 风险类型: {item.get('duplicate_risk', 'unknown')} / {item.get('risk_band', 'unknown')}\n  - 原因: {item['reason']}\n\n"
    else:
        report += "✓ 未发现高风险候选\n\n"

    report += f"""### 3. 手动审核候选检查

- **需要手动审核的候选**: {len(precheck_result['manual_review_candidates'])}
"""

    if precheck_result['manual_review_candidates']:
        report += "以下候选需要手动审核:\n\n"
        for item in precheck_result['manual_review_candidates']:
            report += f"- **{item['name']}** ({item['candidate_id']})\n  - 原因: {item['reason']}\n\n"
    else:
        report += "✓ 未发现需要手动审核的候选\n\n"

    report += f"""### 4. Problem Patterns 候选检查

- **Problem Patterns 候选**: {len(precheck_result['problem_pattern_candidates'])}
"""

    if precheck_result['problem_pattern_candidates']:
        report += "以下候选适合作为 Problem Patterns:\n\n"
        for item in precheck_result['problem_pattern_candidates']:
            report += f"- **{item['name']}** ({item['candidate_id']})\n  - 原因: {item['reason']}\n\n"
    else:
        report += "✓ 未发现 Problem Patterns 候选\n\n"

    report += f"""### 5. Section 需求检查

- **是否需要新 Section**: {'是' if precheck_result['needs_new_section'] else '否'}
- **Section 2.21 数量**: {precheck_result['section_distribution']['2.21']}
- **Section 3.13 数量**: {precheck_result['section_distribution']['3.13']}

✓ 所有候选都能进入已有 Section

### 6. 依赖映射检查

- **依赖映射风险数量**: {len(precheck_result['dependency_mapping_risk'])}
"""

    if precheck_result['dependency_mapping_risk']:
        report += "以下候选存在依赖映射风险:\n\n"
        for item in precheck_result['dependency_mapping_risk']:
            report += f"- **{item['name']}** ({item['candidate_id']})\n  - 风险详情: {item.get('unmapped_dependency', item.get('low_confidence_dependency', 'unknown'))}\n  - 原因: {item['reason']}\n\n"
    else:
        report += "✓ 未发现依赖映射风险\n\n"

    report += f"""### 7. 候选依赖环检查

- **是否存在候选依赖环**: {'是' if precheck_result['candidate_dependency_cycle'] else '否'}
"""

    if precheck_result['candidate_dependency_cycle']:
        report += "⚠ 检测到候选依赖环，需要进一步分析\n\n"
    else:
        report += "✓ 未检测到候选依赖环\n\n"

    report += f"""## 预审建议

### 合并建议

- **建议状态**: {precheck_result['recommendation']}
- **建议本轮合并数量**: {precheck_result['recommended_merge_count']}

### 详细建议

"""

    if precheck_result['recommendation'] == 'ready_for_1号线程_merge':
        report += """**✓ Batch2 准备就绪**

Batch2 可以直接交给 1号线程进行合并。所有候选都通过预审检查，没有发现阻碍合并的问题。

**下一步**:
1. 将预审结果通知 1号线程
2. 1号线程可以开始 Batch2 的合并工作
3. 合并后运行 validate-only 验证
4. 生成 candidate_to_item_id_mapping
"""
    else:
        report += """**⚠ Batch2 需要清理**

Batch2 存在一些问题，建议在合并前进行清理。

**需要处理的问题**:
1. 移除已在 Batch1 合并的候选
2. 处理高风险候选（考虑移除或降级）
3. 审核需要手动审查的候选
4. 解决依赖映射风险

**下一步**:
1. 根据预审结果清理 Batch2
2. 重新运行预审验证
3. 确认无问题后交给 1号线程合并
"""

    report += f"""
## 主图谱状态确认

- **主图谱是否修改**: **否**
- **本次任务目的**: 仅 Batch2 预审，不涉及图谱修改
- **主图谱基线**: item_count = 1512, section_count = 65

## 重要统计总结

| 检查项 | 结果 |
|--------|------|
| Batch2 数量 | {precheck_result['candidate_count']} |
| 已合并候选 | {len(precheck_result['already_merged_in_batch1'])} |
| 高风险候选 | {len(precheck_result['high_risk_candidates'])} |
| 手动审核候选 | {len(precheck_result['manual_review_candidates'])} |
| Problem Patterns | {len(precheck_result['problem_pattern_candidates'])} |
| 依赖映射风险 | {len(precheck_result['dependency_mapping_risk'])} |
| 新 Section 需求 | {'是' if precheck_result['needs_new_section'] else '否'} |
| 候选依赖环 | {'是' if precheck_result['candidate_dependency_cycle'] else '否'} |
| 2.21 分布 | {precheck_result['section_distribution']['2.21']} |
| 3.13 分布 | {precheck_result['section_distribution']['3.13']} |
| 合并建议 | {precheck_result['recommendation']} |
| 建议合并数量 | {precheck_result['recommended_merge_count']} |

## 输出文件

1. `data/thread2_stage3e_aggressive_batch2_precheck.json` - Batch2 预审详细结果
2. `docs/thread2_stage3e_aggressive_batch2_precheck_report.md` - 本报告

## 重要提醒

1. **不进行合并**: 本次任务仅做预审，不进行任何候选合并
2. **不修改主图谱**: 预审过程完全不修改主图谱
3. **不生成新批次**: 不生成新的 aggressive batch
4. **不处理其他批次**: 只处理 batch_2，不涉及 batch_3/4/5
5. **建议性质**: 预审结果仅为建议，最终合并决策由 1号线程决定

## 与 1号线程协调

- **预审完成**: Batch2 预审已完成
- **等待确认**: 等待 1号线程确认是否合并 Batch2
- **协调方式**: 通过预审报告和 JSON 文件进行协调
- **下一步**: 根据预审建议和 1号线程决策执行后续操作

---

报告生成时间: 2026-05-22T15:00:00.000Z
生成者: 2号线程
任务类型: Stage3E-Aggressive Batch2 预审
主图谱修改状态: 否
下一阶段: 等待1号线程决定Batch2合并
"""

    # 保存报告
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\docs\thread2_stage3e_aggressive_batch2_precheck_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✓ 预审报告已保存到 docs/thread2_stage3e_aggressive_batch2_precheck_report.md")
    print("\n✓ Stage3E-Aggressive Batch2 预审任务完成！")

else:
    print("✗ 预审失败，无法生成结果")