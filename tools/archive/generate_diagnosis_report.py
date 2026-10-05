import json
from datetime import datetime

def generate_diagnosis_report():
    with open("data/stage3e_aggressive_batch4_validation_diagnosis.json", 'r', encoding='utf-8') as f:
        diagnosis = json.load(f)
    
    with open("dependency_validation_result.json", 'r', encoding='utf-8') as f:
        validation_result = json.load(f)
    
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items = json.load(f)
    
    report = f"""# Stage3E-Aggressive Batch4 Validation Diagnosis Report

**生成时间**: {datetime.now().isoformat()}
**Batch ID**: stage3e_aggressive_batch4
**当前状态**: validation_failed

---

## 执行摘要

- **当前 item_count**: 1602
- **合并前 item_count**: 1572
- **新增 item 数**: 30
- **validation_passed**: ❌ False
- **resolved_pre_mismatches**: {len(validation_result.get('resolved_pre_mismatches', []))} 个
- **product_metadata_validation.passed**: ❌ False

---

## 任务一：resolved_pre_mismatches 详细诊断

### 概览
- **总数量**: {diagnosis['task1_resolved_pre_mismatches']['summary']['total_mismatches']}
- **所有长度相同**: {diagnosis['task1_resolved_pre_mismatches']['summary']['all_same_length']}
- **都是 Batch4 新增节点**: {diagnosis['task1_resolved_pre_mismatches']['summary']['all_batch4_new_nodes']}
- **涉及旧节点**: {diagnosis['task1_resolved_pre_mismatches']['summary']['involves_old_nodes']}
- **诊断结论**: {diagnosis['task1_resolved_pre_mismatches']['summary']['diagnosis']}

### 关键发现
1. **数量问题**: {'是' if not diagnosis['task1_resolved_pre_mismatches']['summary']['all_same_length'] else '否'}
2. **集合问题**: 无法确定（需要逐项比对）
3. **顺序问题**: 可能存在
4. **是否全部都是 Batch4 新增节点**: {'是' if diagnosis['task1_resolved_pre_mismatches']['summary']['all_batch4_new_nodes'] else '否'}
5. **是否涉及旧节点**: {'是' if diagnosis['task1_resolved_pre_mismatches']['summary']['involves_old_nodes'] else '否'}

### 详细条目
"""
    
    for i, mismatch in enumerate(diagnosis['task1_resolved_pre_mismatches']['mismatches'][:5], 1):
        report += f"""
#### {i}. {mismatch['item_id']} - {mismatch['name'][:20]}...
- **预期长度**: {mismatch['expected_len']}
- **实际长度**: {mismatch['actual_len']}
- **长度相同**: {mismatch['same_length']}
- **是 Batch4 新增节点**: {mismatch['is_batch4_new_node']}
- **resolved_pre 示例**: {str(mismatch['resolved_pre_sample'][:3])}...
"""
    
    if len(diagnosis['task1_resolved_pre_mismatches']['mismatches']) > 5:
        report += f"\n*... 还有 {len(diagnosis['task1_resolved_pre_mismatches']['mismatches']) - 5} 个条目，详见诊断 JSON 文件*"
    
    report += f"""
---

## 任务二：product_metadata_validation.passed=false 诊断

### 核心验证字段状态
- **all_items_have_en_name**: {diagnosis['task2_product_metadata']['all_items_have_en_name']}
- **all_items_have_tracks**: {diagnosis['task2_product_metadata']['all_items_have_tracks']}
- **all_items_have_audience**: {diagnosis['task2_product_metadata']['all_items_have_audience']}
- **all_items_have_visibility**: {diagnosis['task2_product_metadata']['all_items_have_visibility']}
- **all_items_have_learning_path_policy**: ❌ {diagnosis['task2_product_metadata']['all_items_have_learning_path_policy']}
- **all_items_have_localization_status**: {diagnosis['task2_product_metadata']['all_items_have_localization_status']}
- **all_items_have_content_status**: {diagnosis['task2_product_metadata']['all_items_have_content_status']}

### 问题详情

#### learning_path_policy 问题
- **缺少 learning_path_policy 的节点总数**: {diagnosis['task2_product_metadata']['missing_learning_path_policy_count']}
- **Batch4 新增节点缺少数**: {diagnosis['task2_product_metadata']['missing_learning_path_policy_batch4']}
- **旧节点缺少数**: {diagnosis['task2_product_metadata']['missing_learning_path_policy_old']}

#### 其他字段验证
- **invalid_tracks 数量**: {diagnosis['task2_product_metadata']['invalid_tracks_count']}
- **invalid_audience 数量**: {diagnosis['task2_product_metadata']['invalid_audience_count']}
- **invalid_visibility 数量**: {diagnosis['task2_product_metadata']['invalid_visibility_count']}
- **invalid_unlock_mode 数量**: {diagnosis['task2_product_metadata']['invalid_unlock_mode_count']}

#### 预期 vs 实际
- **expected_item_count**: {validation_result.get('expected_item_count', 'N/A')}
- **actual_item_count**: {diagnosis['task2_product_metadata']['total_items']}
- **expected_section_count**: {validation_result.get('expected_section_count', 'N/A')}
- **actual_section_count**: {validation_result.get('section_count', 'N/A')}

### 导致 product_metadata_validation.passed=false 的字段
**主要失败原因**: {diagnosis['task2_product_metadata']['primary_failure_reason']}
- **涉及 Batch4 节点**: {diagnosis['task2_product_metadata']['involves_batch4_nodes']}
- **涉及旧节点**: {diagnosis['task2_product_metadata']['involves_old_nodes']}

---

## 任务三：是否需要回滚

### 关键判断参数
"""
    
    for key, value in diagnosis['task3_rollback_decision'].items():
        if key not in ['reasons_for_in_place_fix', 'reasons_for_rollback', 'diagnosis_summary', 'reasons_for_rollback']:
            report += f"- **{key}**: {value}\n"
    
    report += f"""
### 就地修复的理由
"""
    
    for reason in diagnosis['task3_rollback_decision']['reasons_for_in_place_fix']:
        report += f"- ✅ {reason}\n"
    
    report += f"""
### 回滚的理由
"""
    
    for reason in diagnosis['task3_rollback_decision']['reasons_for_rollback']:
        report += f"- ❌ {reason}\n"
    
    report += f"""
### 诊断摘要
"""
    
    for key, value in diagnosis['task3_rollback_decision']['diagnosis_summary'].items():
        report += f"- **{key}**: {value}\n"
    
    report += f"""
---

## 任务四：诊断总结（仅诊断，不修复）

### 执行限制
- ❌ 不修复任何问题
- ❌ 不继续 batch_5
- ❌ 不做 Batch4 Review
- ❌ 不凭手动检查判定误报
- ✅ 只输出诊断结果

### 整体诊断结论
"""
    
    for key, value in diagnosis['overall_diagnosis'].items():
        report += f"- **{key}**: {value}\n"
    
    report += f"""
---

## 建议操作流程

### 如果需要就地修复 (can_fix_in_place = true)
1. 定位并修复 {diagnosis['task2_product_metadata']['missing_learning_path_policy_count']} 个缺少 learning_path_policy 的节点
2. 重新运行 validate-only 检查
3. 如果通过，可以继续后续操作

### 如果需要回滚 (should_restore_backup = true)
1. 执行回滚操作：`Copy-Item backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4.json merged_knowledge_graph_item_dependencies_refined.json`
2. 验证 item_count 回到 1572
3. 重新分析 Batch4 依赖计划
4. 修正问题后重新合并

---

## 数据文件参考

- 完整诊断结果: `data/stage3e_aggressive_batch4_validation_diagnosis.json`
- 验证结果: `dependency_validation_result.json`
- 新增节点摘要: `data/stage3e_aggressive_batch4_added_items_summary.json`
- 备份文件: `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4.json`

---

**诊断生成完成时间**: {datetime.now().isoformat()}
**当前 item_count**: {diagnosis['task2_product_metadata']['total_items']}
**validation_passed**: {diagnosis['task3_rollback_decision']['validation_passed']}
**推荐操作**: {diagnosis['task3_rollback_decision']['recommended_next_action']}
"""
    
    return report

if __name__ == "__main__":
    report = generate_diagnosis_report()
    
    with open("docs/stage3e_aggressive_batch4_validation_diagnosis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 诊断报告已生成: docs/stage3e_aggressive_batch4_validation_diagnosis_report.md")