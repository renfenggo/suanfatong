# Stage 3E-Aggressive Batch1 Added Items Review Report

**报告生成时间**: 2026-05-22  
**批次标识**: Stage3E-Aggressive Batch1  
**批次 ID**: batch_1

---

## 执行摘要

### 复查范围
- **新增节点总数**: 30 个
- **复查覆盖率**: 100% (30/30)
- **所有节点位于**: 2.21 高级图论扩展章节

### 复查结果统计
- **approve（通过）**: 19 个 (63.3%)
- **降为 C 级**: 22 个 (73.3%)
- **保留 B 级**: 7 个 (23.3%)
- **保留 A 级**: 1 个 (3.3%)
- **需要依赖修复**: 9 个 (30.0%)
- **建议同步/转入 problem_patterns**: 4 个 (13.3%)
- **needs_merge_or_collapse**: 0 个 (0.0%)

### 分系列复查结论

#### Maximum Closure 系列 (6 个节点)
- **节点**: 2.21.70-75
- **通过**: 2 个 (2.21.71, 2.21.72)
- **降级 C**: 6 个
- **保留 B**: 0 个
- **保留 A**: 0 个
- **需要依赖修复**: 0 个
- **建议转入 problem_patterns**: 4 个
- **结论**: Maximum Closure 系列中，Binary Decision Model、Open Pit Mining Model、Prerequisite Graph、Task Selection 更像 problem_patterns（应用模型），核心概念 Maximum Weight Closure 和 Minimum Cut Transform 属于算法层，可安全降级。

#### Directed MST 系列 (6 个节点)
- **节点**: 2.21.76-81
- **通过**: 5 个
- **降级 C**: 5 个
- **保留 B**: 1 个
- **保留 A**: 0 个
- **需要依赖修复**: 1 个
- **建议转入 problem_patterns**: 0 个
- **结论**: Directed MST 系列概念区分度较好，Maximum/Minimum Arborescence 有明确区分，Rooted Arborescence 和 Super Root Model 也是不同维度。Weighted Directed Mst 存在概念重叠风险，需要人工确认。

#### Dominator Tree 系列 (6 个节点)
- **节点**: 2.21.82-87
- **通过**: 6 个
- **降级 C**: 4 个
- **保留 B**: 2 个
- **保留 A**: 0 个
- **需要依赖修复**: 0 个
- **建议转入 problem_patterns**: 0 个
- **结论**: Dominator Tree 系列概念清晰，Bridge Relation、Dag Dominator、Dominance Frontier、Path Dominator Query 可安全降级。Online Query 和 Dominator Tree Dp 是高级应用技巧，保留 B 类人工抽查。

#### Dynamic MST 系列 (6 个节点)
- **节点**: 2.21.88-93
- **通过**: 0 个 (全部需要依赖修复)
- **降级 C**: 0 个
- **保留 B**: 6 个
- **保留 A**: 0 个
- **需要依赖修复**: 6 个
- **建议转入 problem_patterns**: 0 个
- **结论**: Dynamic MST 系列全部节点缺少对 2.21.44（Dynamic MST: Offline Updates）的依赖，需要补充依赖后继续人工审查。Edge Insertion 和 Divide Conquer Approach 降为 B。

#### Global Min-Cut 系列 (6 个节点)
- **节点**: 2.21.94-99
- **通过**: 3 个
- **降级 C**: 2 个
- **保留 B**: 4 个
- **保留 A**: 0 个
- **需要依赖修复**: 3 个
- **建议转入 problem_patterns**: 0 个
- **结论**: Global Min-Cut 系列中，Random Contraction、Recursive Contraction、Sparsification 缺少对 2.21.45（Global Min-Cut: Gomory Hu Tree）的依赖，需要补充依赖。Cut Tree Query 降为 B 人工抽查。

---

## 详细问题分析

### 1. 依赖关系问题 (9 个节点)

#### Dynamic MST 系列依赖缺失
- **影响节点**: 2.21.88-93 (全部 6 个节点)
- **问题**: 所有 Dynamic MST 子专题节点缺少对 2.21.44（Dynamic MST: Offline Updates）的依赖
- **当前依赖**: [2.13.10, 3.4.1]
- **建议修复**: 增加 2.21.44 到 direct_pre
- **严重程度**: 高
- **修复优先级**: Batch1 Fix

#### Global Min-Cut 系列依赖缺失
- **影响节点**: 2.21.96-98 (Random Contraction, Recursive Contraction, Sparsification)
- **问题**: 这些算法节点缺少对 2.21.45（Global Min-Cut: Gomory Hu Tree）的依赖
- **当前依赖**: [2.21.67, 2.16.12]
- **建议修复**: 增加 2.21.45 到 direct_pre
- **严重程度**: 高
- **修复优先级**: Batch1 Fix

#### Directed MST 系列概念不明确
- **影响节点**: 2.21.81 (Weighted Directed Mst)
- **问题**: Weighted Directed Mst 与 Maximum/Minimum Arborescence 语义可能重叠
- **建议修复**: 增加 2.21.77 和 2.21.78 到 direct_pre，人工确认概念区分
- **严重程度**: 高
- **修复优先级**: Batch1 Fix

### 2. Problem Pattern 识别 (4 个节点)

#### Maximum Closure 应用模型
- **影响节点**: 2.21.70, 2.21.73-75 (4 个节点)
- **识别为 problem_pattern 的原因**:
  - Binary Decision Model: 二进制决策问题建模
  - Open Pit Mining Model: 开矿问题经典应用
  - Prerequisite Graph: 前置依赖选择问题
  - Task Selection: 任务选择问题
- **建议**: 保留 item，但标记为应用模型，适合同步到 problem_patterns
- **注意**: Task Selection 与 Prerequisite Graph 语义相似，建议人工确认是否需要合并

### 3. 概念拆分合理性 (5 个系列)

#### 概念拆分评价
- **Maximum Closure 系列**: 合理拆分，核心概念与应用模型区分清楚
- **Directed MST 系列**: 合理拆分，但 Weighted Directed Mst 存在重叠风险
- **Dominator Tree 系列**: 合理拆分，理论概念与应用技巧区分清楚
- **Dynamic MST 系列**: 合理拆分，但依赖关系不完整
- **Global Min-Cut 系列**: 合理拆分，但部分算法缺少主概念依赖

---

## Batch2 建议与后续行动

### 是否建议进入 Batch1 Fix
- **建议**: ✅ 是
- **理由**: 
  - 9 个节点需要依赖修复（高优先级）
  - 依赖修复后可以进一步降级部分 B 类节点
  - 问题明确，修复成本低

### 是否建议继续 batch_2
- **建议**: ⚠️ 建议先完成 Batch1 Fix
- **理由**:
  - Batch1 中发现了系统性的依赖缺失问题
  - Dynamic MST 和 Global Min-Cut 系列的依赖模式需要在 batch_2 中延续
  - 建议在依赖修复模式稳定后再继续 batch_2

### batch_2 推荐合并数量
- **预计 batch_2 节点数量**: 根据候选文件估算约 30-40 个
- **推荐合并数量**: 建议先进行依赖审查后再确定
- **优先级调整**:
  - 确保所有子专题节点都依赖对应的主概念节点
  - 区分算法概念和应用模型（problem_pattern）
  - 对于系列内节点，确保概念区分度

---

## 复查方法论

### 降级规则应用
1. **降为 C (22 个节点)**:
   - 依赖明确、子专题合理、metadata 完整
   - 属于算法层或理论概念
   - 与现有节点无重复或过度拆分

2. **保留 B (7 个节点)**:
   - 依赖明确但系列边界需抽查
   - 高级复杂专题、拆分边界不清、可能重复
   - 需要依赖修复后进一步审查

3. **保留 A (1 个节点)**:
   - 目前没有节点需要保留 A 类
   - 原 A 类节点均已降级为 B 或 C

### 重点判断验证
1. ✅ **Maximum Closure 系列中建模题型识别**: Binary Decision Model、Open Pit Mining Model、Prerequisite Graph、Task Selection 已识别为 problem_pattern
2. ✅ **Directed MST 系列重叠检查**: Weighted Directed Mst 存在重叠风险，已标记需要依赖修复
3. ✅ **Dominator Tree 系列应用检查**: Online Query 和 Path Dominator Query 分别处理，Path Dominator Query 降为 C
4. ✅ **Dynamic MST 系列主概念依赖检查**: 发现所有节点缺少对 2.21.44 的依赖，已标记需要修复
5. ✅ **Global Min-Cut 系列主概念依赖检查**: 发现 Random Contraction 等算法缺少对 2.21.45 的依赖，已标记需要修复

---

## 输出文件清单

### 本次复查生成的文件
1. **data/stage3e_aggressive_batch1_added_items_review.json**: 30 个节点的详细复查结果
2. **data/stage3e_aggressive_batch1_review_status_patch_preview.json**: review_priority 和 need_manual_review 的 patch 预览
3. **data/stage3e_aggressive_batch1_dependency_fix_candidates.json**: 需要依赖修复的 9 个节点
4. **data/stage3e_aggressive_batch1_problem_pattern_sync_candidates.json**: 建议同步到 problem_patterns 的 4 个节点
5. **docs/stage3e_aggressive_batch1_added_items_review_report.md**: 本复查报告

### 依赖修复总结
- **需要修复的节点**: 9 个
- **需要添加的依赖关系**: 10 个
- **高严重程度问题**: 9 个
- **主要修复方向**:
  - Dynamic MST 系列增加对 2.21.44 的依赖
  - Global Min-Cut 系列增加对 2.21.45 的依赖
  - Directed MST 系列细化概念层级

---

## 风险提示

### 保留人工审查的节点 (8 个)
1. **2.21.81** Weighted Directed Mst: 概念重叠风险
2. **2.21.85** Dominator Tree Dp: 高级应用技巧边界需确认
3. **2.21.86** Online Query: 高级查询技巧边界需确认
4. **2.21.88-93** Dynamic MST 全系列: 需要依赖修复后重新审查
5. **2.21.94** Cut Tree Query: 高级查询技巧边界需确认
6. **2.21.96-98** Global Min-Cut 算法: 需要依赖修复后重新审查

### 需要人工确认的问题
1. Task Selection 与 Prerequisite Graph 是否需要合并
2. Weighted Directed Mst 与 Maximum/Minimum Arborescence 的概念区分
3. Online Query 和 Path Dominator Query 是否应作为应用子专题

---

## 下一步行动建议

### 立即行动 (Batch1 Fix)
1. 应用依赖修复 patch（9 个节点，10 个依赖关系）
2. 重新运行 validate-only 验证
3. 检查修复后的依赖合理性

### 短期行动 (审查跟进)
1. 对 8 个保留人工审查的节点进行人工确认
2. 确认 4 个 problem_pattern 标记的合理性
3. 评估 Task Selection 与 Prerequisite Graph 的合并可能性

### 中期行动 (batch_2 准备)
1. 总结 Batch1 的依赖模式经验
2. 在 batch_2 中预先检查主概念依赖
3. 区分算法概念和应用模型的分类标准

---

**报告结束**