# Stage3E-Aggressive Batch1 Resolved Pre Mismatch 诊断报告

**报告生成时间**: 2026-05-22  
**批次标识**: Stage3E-Aggressive Batch1  
**批次 ID**: batch_1  
**诊断模式**: 纯诊断，不修改主图谱

---

## 执行摘要

### 诊断背景
在执行 Stage3E-Aggressive Batch1 Fix 过程中，validate-only 验证失败，发现 resolved_pre_mismatches 问题。已从备份恢复主图谱到修复前状态，本阶段进行纯诊断分析。

### 诊断结果摘要
- **当前主图谱状态**: ✅ 正常
- **需要修复的节点数**: 10 个
- **产生 resolved_pre mismatch 的节点数**: 10 个  
- **总缺失依赖数**: 38 个
- **需要重算 resolved_pre 的节点**: 10 个
- **下游影响节点数**: 0 个
- **本阶段是否修改主图谱**: ❌ 否

---

## 当前主图谱状态确认

### 基础状态检查
- **item_count**: 1512 ✅
- **section_count**: 65 ✅  
- **JSON 可解析性**: ✅ 正常
- **备份状态**: ✅ 已恢复到修复前状态
- **direct_pre 无环**: ✅ 验证通过
- **悬空引用**: ✅ 0 个

### 硬校验结果
- ✅ item_count 仍为 1512
- ✅ section_count 仍为 65  
- ✅ JSON 可解析
- ✅ item id 不重复
- ✅ direct_pre 无 section id
- ✅ rel 无 section id
- ✅ resolved_pre 无 section id
- ✅ 悬空引用为 0
- ✅ direct_pre 无环

---

## Resolved Pre Mismatch 详细分析

### 实际验证发现的问题

#### Dynamic MST 系列 (6 个节点)

| 节点 ID | 节点名称 | 预期依赖数 | 实际依赖数 | 缺失数 |
|---------|---------|-----------|-----------|-------|
| 2.21.88 | 动态最小生成树：Batch Recomputation | 26 | 22 | 4 |
| 2.21.89 | 动态最小生成树：Certificate Graph | 26 | 22 | 4 |
| 2.21.90 | 动态最小生成树：Divide Conquer Approach | 26 | 22 | 4 |
| 2.21.91 | 动态最小生成树：Edge Deletion | 26 | 22 | 4 |
| 2.21.92 | 动态最小生成树：Edge Insertion | 26 | 22 | 4 |
| 2.21.93 | 动态最小生成树：Sensitivity Analysis | 26 | 22 | 4 |

**系列总计**: 6 个节点，24 个缺失依赖

**原因**: 这些节点的新增依赖 2.21.44 (Dynamic MST: Offline Updates) 带来了额外的 MST 和数据结构前置依赖，但这些依赖没有在 resolved_pre 中反映出来。

#### Global Min-Cut 系列 (3 个节点)

| 节点 ID | 节点名称 | 预期依赖数 | 实际依赖数 | 缺失数 |
|---------|---------|-----------|-----------|-------|
| 2.21.96 | 全局最小割：Random Contraction | 37 | 33 | 4 |
| 2.21.97 | 全局最小割：Recursive Contraction | 37 | 33 | 4 |
| 2.21.98 | 全局最小割：Sparsification | 37 | 33 | 4 |

**系列总计**: 3 个节点，12 个缺失依赖

**原因**: 这些节点的新增依赖 2.21.45 (Global Min-Cut: Gomory Hu Tree) 带来了额外的最小割和流网络前置依赖。

#### Directed MST 系列 (1 个节点)

| 节点 ID | 节点名称 | 预期依赖数 | 实际依赖数 | 缺失数 |
|---------|---------|-----------|-----------|-------|
| 2.21.81 | 有向生成树：Weighted Directed Mst | 24 | 22 | 2 |

**系列总计**: 1 个节点，2 个缺失依赖

**原因**: 该节点的新增依赖 2.21.77 (Maximum Arborescence) 和 2.21.78 (Minimum Arborescence) 带来了额外的 MST 前置依赖。

---

## 根因分析

### 主要原因
**Direct_pre 已更新，但 resolved_pre 未重新计算**

在依赖修复过程中，以下操作已执行：
1. ✅ 为 10 个节点添加了新的 direct_pre 依赖
2. ❌ 但没有同步更新这些节点的 resolved_pre

### 依赖链影响

新增的直接前置节点各自有完整的前置依赖链：

- **2.21.44** (Dynamic MST: Offline Updates) → 带来 4 个额外前置依赖
- **2.21.45** (Global Min-Cut: Gomory Hu Tree) → 带来 4 个额外前置依赖  
- **2.21.77** (Maximum Arborescence) + **2.21.78** (Minimum Arborescence) → 共带来 2 个额外前置依赖

这些额外依赖需要递归传播到依赖它们的节点中。

### 验证逻辑
Strict validation 会：
1. 从更新后的 direct_pre 递归计算 expected_resolved_pre
2. 与存储的 stored_resolved_pre 进行对比
3. 发现不一致时报告 mismatch

---

## 修复方案建议

### 推荐修复流程

#### 步骤 1：创建专门的重算脚本
建议创建 `recompute_resolved_pre_for_stage3e_batch1.py` 脚本，专门处理这 10 个节点的 resolved_pre 更新。

#### 步骤 2：仅重算受影响的节点
只需为以下 10 个节点重新计算 resolved_pre：
```
2.21.81, 2.21.88, 2.21.89, 2.21.90, 2.21.91, 2.21.92, 2.21.93, 2.21.96, 2.21.97, 2.21.98
```

#### 步骤 3：不处理下游节点
分析显示这 10 个节点没有下游依赖项，因此不需要更新其他节点。

#### 步骤 4：验证修复效果
运行 validate-only 确认：
```powershell
python refine_item_dependencies.py --validate-only --input merged_knowledge_graph_item_dependencies_refined.json --report item_dependency_refinement_report.md --low-conf low_confidence_dependency_review.json --validation dependency_validation_result.json --strict
```

---

## 下游影响分析

### 影响节点列表
- **受影响节点数**: 0 个
- **原因**: 这 10 个节点是 Batch1 新增节点，还没有其他节点依赖它们

### 传播链分析
```
受影响节点 → 下游节点 → 更下游节点...
2.21.81    → 无       → 无
2.21.88    → 无       → 无  
2.21.89    → 无       → 无
2.21.90    → 无       → 无
2.21.91    → 无       → 无
2.21.92    → 无       → 无
2.21.93    → 无       → 无
2.21.96    → 无       → 无
2.21.97    → 无       → 无
2.21.98    → 无       → 无
```

### 结论
✅ 不需要更新任何下游节点

---

## 统计总结

### 修复范围统计
- **总节点数**: 1512
- **受影响节点数**: 10
- **影响比例**: 0.66%
- **平均每节点缺失依赖**: 3.8 个

### 按系列分类统计
- **Dynamic MST 系列**: 6 个节点，24 个缺失依赖
- **Global Min-Cut 系列**: 3 个节点，12 个缺失依赖
- **Directed MST 系列**: 1 个节点，2 个缺失依赖

### 修复复杂度评估
- **复杂度**: 低
- **预计修复时间**: 几秒
- **需要人工干预**: 否
- **风险等级**: 低
- **对现有图谱影响**: 无

---

## 下一步行动建议

### 立即行动
1. ✅ **本诊断阶段完成**: 已生成诊断报告 JSON 和 MD
2. ⏭️ **创建重算脚本**: 创建 recompute_resolved_pre_for_stage3e_batch1.py
3. ⏭️ **应用修复**: 运行脚本修复 10 个节点的 resolved_pre
4. ⏭️ **验证修复**: 运行 validate-only 确认修复成功

### 短期行动
1. 如果验证通过，Stage3E-Aggressive Batch1 Fix 视为完成
2. 生成最终的 fix_report.md
3. 继续 Stage3E 的后续批次（如需要）

### 不建议立即继续
- 不建议立即开始 batch_2，建议先完成 Batch1 的验证和收尾工作

---

## 技术细节

### 依赖传播示例

以 2.21.88 (Dynamic MST: Batch Recomputation) 为例：

#### 修复后的 direct_pre
```
["2.13.10", "3.4.1", "2.21.44"]
```

#### 新增的依赖 2.21.44 的 direct_pre
```
["2.13.8", "2.13.9", "3.4.1"]
```

#### 2.21.44 的 resolved_pre 包含
```
["4.1.1", "1.3.10", "1.1.3", "1.2.1", "1.3.6", "4.7.1", "4.5.1", 
 "1.4.3", "1.4.4", "1.5.6", "1.6.1", "1.8.1", "3.9.2", "2.9.3", 
 "4.5.6", "4.5.7", "2.13.8", "3.4.1", "2.13.9"]
```

#### 2.21.88 的 expected_resolved_pre 应该包含
- 原有依赖的递归展开
- 加上 2.21.44 的递归展开
- 总共 26 个节点（当前只有 22 个，缺失 4 个）

### 重算逻辑要求
重新计算 resolved_pre 时必须：
1. 使用官方的递归展开逻辑
2. 包含 section 依赖
3. 递归处理所有前置依赖的前置依赖
4. 去重并保持顺序
5. 不包含自身 ID

---

## 风险评估

### 当前风险等级
**🟢 低风险**

### 风险因素
- **修复范围**: 仅限 10 个新增节点
- **下游影响**: 无
- **现有图谱影响**: 无
- **回滚能力**: 已有备份

### 潜在风险
- 如果重算逻辑不正确，可能导致新的 mismatch
- 如果遗漏某个节点，validate-only 仍会失败

### 风险缓解
- ✅ 已有完整备份
- ✅ 可以验证每个节点的修复效果
- ✅ validate-only 会发现任何问题

---

## 结论

### 诊断结果
✅ **问题根因已明确**: Direct_pre 更新后 resolved_pre 未同步更新

### 修复可行性
✅ **高度可行**: 问题范围明确，修复方案简单

### 修复预期
✅ **修复成功率高**: 预期一次修复即可通过验证

### 后续影响
✅ **影响可控**: 仅限 10 个节点，无下游传播

---

## 附录：需要重算 Resolved Pre 的完整节点列表

### Dynamic MST 系列
1. **2.21.88** - 动态最小生成树：Batch Recomputation
2. **2.21.89** - 动态最小生成树：Certificate Graph  
3. **2.21.90** - 动态最小生成树：Divide Conquer Approach
4. **2.21.91** - 动态最小生成树：Edge Deletion
5. **2.21.92** - 动态最小生成树：Edge Insertion
6. **2.21.93** - 动态最小生成树：Sensitivity Analysis

### Global Min-Cut 系列
7. **2.21.96** - 全局最小割：Random Contraction
8. **2.21.97** - 全局最小割：Recursive Contraction
9. **2.21.98** - 全局最小割：Sparsification

### Directed MST 系列
10. **2.21.81** - 有向生成树：Weighted Directed Mst

---

## 诊断方法说明

### 使用的诊断方法
1. ✅ 确认当前主图谱基础状态
2. ✅ 分析实际的 validate-only 报告
3. ✅ 按系列分类分析问题
4. ✅ 确定根因和修复范围
5. ✅ 评估下游影响
6. ✅ 提供具体修复建议

### 诊断限制
- ❌ 未修改主图谱（按要求）
- ❌ 未应用任何修复补丁
- ❌ 未运行任何修改操作
- ✅ 仅生成诊断报告和建议

---

**报告结束**

**状态**: ✅ 诊断完成，问题根因明确，修复方案已提供，建议下一步创建并运行重算脚本。

**重要说明**: 本阶段为纯诊断阶段，未对主图谱进行任何修改。下一阶段可以安全地应用修复。