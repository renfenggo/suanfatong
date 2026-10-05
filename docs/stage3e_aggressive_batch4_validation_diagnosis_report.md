# Stage3E-Aggressive Batch4 Validation Diagnosis Report

**生成时间**: 2026-05-23T10:09:09.033373
**Batch ID**: stage3e_aggressive_batch4
**当前状态**: validation_failed

---

## 执行摘要

- **当前 item_count**: 1602
- **合并前 item_count**: 1572
- **新增 item 数**: 30
- **validation_passed**: ❌ False
- **resolved_pre_mismatches**: 30 个
- **product_metadata_validation.passed**: ❌ False

---

## 任务一：resolved_pre_mismatches 详细诊断

### 概览
- **总数量**: 30
- **所有长度相同**: True
- **都是 Batch4 新增节点**: True
- **涉及旧节点**: False
- **诊断结论**: set_order_issue

### 关键发现
1. **数量问题**: 否
2. **集合问题**: 无法确定（需要逐项比对）
3. **顺序问题**: 可能存在
4. **是否全部都是 Batch4 新增节点**: 是
5. **是否涉及旧节点**: 否

### 详细条目

#### 1. 2.21.141 - 匹配与覆盖：Matroid Matchi...
- **预期长度**: 28
- **实际长度**: 28
- **长度相同**: True
- **是 Batch4 新增节点**: True
- **resolved_pre 示例**: ['1.3.10', '1.4.3', '1.4.4']...

#### 2. 2.21.136 - 图论建模：State Graph...
- **预期长度**: 30
- **实际长度**: 30
- **长度相同**: True
- **是 Batch4 新增节点**: True
- **resolved_pre 示例**: ['1.3.10', '1.4.3', '1.4.4']...

#### 3. 3.13.132 - 高级平衡树：Implicit Treap...
- **预期长度**: 27
- **实际长度**: 27
- **长度相同**: True
- **是 Batch4 新增节点**: True
- **resolved_pre 示例**: ['3.6.1', '3.6.3', '1.1.3']...

#### 4. 3.13.137 - 高级平衡树：Piece Table...
- **预期长度**: 27
- **实际长度**: 27
- **长度相同**: True
- **是 Batch4 新增节点**: True
- **resolved_pre 示例**: ['3.6.1', '3.6.3', '1.1.3']...

#### 5. 3.13.133 - 高级平衡树：Join Based Tre...
- **预期长度**: 27
- **实际长度**: 27
- **长度相同**: True
- **是 Batch4 新增节点**: True
- **resolved_pre 示例**: ['3.6.1', '3.6.3', '1.1.3']...

*... 还有 25 个条目，详见诊断 JSON 文件*
---

## 任务二：product_metadata_validation.passed=false 诊断

### 核心验证字段状态
- **all_items_have_en_name**: True
- **all_items_have_tracks**: True
- **all_items_have_audience**: True
- **all_items_have_visibility**: True
- **all_items_have_learning_path_policy**: ❌ True
- **all_items_have_localization_status**: True
- **all_items_have_content_status**: True

### 问题详情

#### learning_path_policy 问题
- **缺少 learning_path_policy 的节点总数**: 0
- **Batch4 新增节点缺少数**: 0
- **旧节点缺少数**: 0

#### 其他字段验证
- **invalid_tracks 数量**: 0
- **invalid_audience 数量**: 0
- **invalid_visibility 数量**: 0
- **invalid_unlock_mode 数量**: 366

#### 预期 vs 实际
- **expected_item_count**: 1572
- **actual_item_count**: 1602
- **expected_section_count**: 65
- **actual_section_count**: 65

### 导致 product_metadata_validation.passed=false 的字段
**主要失败原因**: other_metadata_issue
- **涉及 Batch4 节点**: False
- **涉及旧节点**: False

---

## 任务三：是否需要回滚

### 关键判断参数
- **current_item_count**: 1602
- **validation_passed**: False
- **should_treat_as_success**: False
- **can_fix_in_place**: True
- **should_restore_backup**: False
- **recommended_next_action**: fix_in_place_and_revalidate

### 就地修复的理由
- ✅ resolved_pre_mismatches 只是数量相同的情况，可能是验证脚本逻辑问题
- ✅ resolved_pre_mismatches 只涉及 Batch4 新增节点，未污染旧节点

### 回滚的理由

### 诊断摘要
- **resolved_pre_issue**: length_equal_only_new_nodes
- **product_metadata_issue**: mixed_or_old_nodes
- **overall_risk**: low

---

## 任务四：诊断总结（仅诊断，不修复）

### 执行限制
- ❌ 不修复任何问题
- ❌ 不继续 batch_5
- ❌ 不做 Batch4 Review
- ❌ 不凭手动检查判定误报
- ✅ 只输出诊断结果

### 整体诊断结论
- **can_proceed**: False
- **requires_rollback**: False
- **can_be_fixed_in_place**: True
- **recommended_action**: fix_in_place_and_revalidate

---

## 建议操作流程

### 如果需要就地修复 (can_fix_in_place = true)
1. 定位并修复 0 个缺少 learning_path_policy 的节点
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

**诊断生成完成时间**: 2026-05-23T10:09:09.033373
**当前 item_count**: 1602
**validation_passed**: False
**推荐操作**: fix_in_place_and_revalidate
