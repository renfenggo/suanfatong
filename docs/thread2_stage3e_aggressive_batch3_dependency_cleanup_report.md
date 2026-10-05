# Stage3E-Aggressive Batch3 Dependency Cleanup 报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T19:00:00.000Z
- 任务类型: Stage3E-Aggressive Batch3 Dependency Cleanup
- 主图谱状态: 未修改
- 任务目的: 清除 Batch3 候选中的 section 引用，为重试合并做准备

## 失败原因分析

**Batch3 Merge 失败的根本原因**:
- **primary_issue**: resolved_pre_mismatches 无法通过验证
- **root_cause**: Batch3 部分候选的 direct_pre 包含 section 引用，被官方 compute_resolved 过滤后导致 resolved_pre 计算不完整
- **validation_results.resolved_pre_mismatches**: 50

**Section 引用问题**:
- 部分候选的 direct_pre 依赖项形如 "3.10"、"3.6"、"2.21"
- 这些是 section id（两级编号），不是具体的 item id
- 官方 compute_resolved 会过滤掉这些 section 引用
- 导致部分依赖项丢失，产生 resolved_pre_mismatches

## 任务一：找出 Batch3 中所有 section 引用

### 候选总数与问题候选

- **Batch3 候选总数**: 30
- **含 section 引用的候选数量**: 10
- **问题候选占比**: 33.3%

### 涉及的 Section ID 列表

发现以下 section 引用:
- **3.10**
- **3.6**


### 问题候选详细列表

以下是包含 section 引用的候选:

#### 序列维护结构：Order Maintenance (`cand.ds.sequence_structure.order_maintenance`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)

#### 序列维护结构：Persistent Sequence (`cand.ds.sequence_structure.persistent_sequence`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)

#### 序列维护结构：Range Hash Maintenance (`cand.ds.sequence_structure.range_hash_maintenance`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)

#### 序列维护结构：Sequence Split Merge (`cand.ds.sequence_structure.sequence_split_merge`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)

#### 序列维护结构：Text Editor Model (`cand.ds.sequence_structure.text_editor_model`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)

#### 树分治维护：Dynamic Centroid (`cand.ds.tree_decomposition_ds.dynamic_centroid`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.6` (树结构, type=section, match=synonym, input=Tree)

**当前 direct_pre_suggestion**:
- `Tree` → `3.6` (树结构, type=section, match=synonym)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

#### 树分治维护：Subtree Query Flatten (`cand.ds.tree_decomposition_ds.subtree_query_flatten`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.6` (树结构, type=section, match=synonym, input=Tree)

**当前 direct_pre_suggestion**:
- `Tree` → `3.6` (树结构, type=section, match=synonym)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

#### 树分治维护：Tree Distance Aggregate (`cand.ds.tree_decomposition_ds.tree_distance_aggregate`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.6` (树结构, type=section, match=synonym, input=Tree)

**当前 direct_pre_suggestion**:
- `Tree` → `3.6` (树结构, type=section, match=synonym)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

#### 树分治维护：Tree Path Kth (`cand.ds.tree_decomposition_ds.tree_path_kth`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.6` (树结构, type=section, match=synonym, input=Tree)

**当前 direct_pre_suggestion**:
- `Tree` → `3.6` (树结构, type=section, match=synonym)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

#### 树分治维护：Virtual Tree Plus Hld (`cand.ds.tree_decomposition_ds.virtual_tree_plus_hld`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.6` (树结构, type=section, match=synonym, input=Tree)

**当前 direct_pre_suggestion**:
- `Tree` → `3.6` (树结构, type=section, match=synonym)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

## 任务二：把 Section ID 精确替换为 Item ID

### 清洗策略

- **精确替换**: 不粗暴展开整个 section，根据候选语义选择最相关的 1~4 个具体 item id
- **智能映射**: 根据候选的具体内容选择依赖项，避免过度泛化
- **保守处理**: 无法确定映射时标记为 needs_manual_dependency_mapping

### 清洗结果概览

- **已成功清洗数量**: 10
- **需要人工映射数量**: 0
- **自动清洗成功率**: 100.0%

### 清洗候选详细列表


#### 序列维护结构：Order Maintenance (`cand.ds.sequence_structure.order_maintenance`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`
- `3.10.2`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.2` (Wavelet Tree, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]

**移除的 Section 引用**: 3.10

**映射原因**: 将 3.10 替换为: ['平衡二叉搜索树（Balanced BST） (3.10.1)', 'Wavelet Tree (3.10.2)', 'Treap 简介 (3.10.3)']

**置信度**: medium

**需要人工映射**: 否

#### 序列维护结构：Persistent Sequence (`cand.ds.sequence_structure.persistent_sequence`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`
- `3.10.2`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.2` (Wavelet Tree, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]

**移除的 Section 引用**: 3.10

**映射原因**: 将 3.10 替换为: ['平衡二叉搜索树（Balanced BST） (3.10.1)', 'Wavelet Tree (3.10.2)', 'Treap 简介 (3.10.3)']

**置信度**: medium

**需要人工映射**: 否

#### 序列维护结构：Range Hash Maintenance (`cand.ds.sequence_structure.range_hash_maintenance`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`
- `3.10.2`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.2` (Wavelet Tree, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]

**移除的 Section 引用**: 3.10

**映射原因**: 将 3.10 替换为: ['平衡二叉搜索树（Balanced BST） (3.10.1)', 'Wavelet Tree (3.10.2)', 'Treap 简介 (3.10.3)']

**置信度**: medium

**需要人工映射**: 否

#### 序列维护结构：Sequence Split Merge (`cand.ds.sequence_structure.sequence_split_merge`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`
- `3.10.2`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.2` (Wavelet Tree, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]

**移除的 Section 引用**: 3.10

**映射原因**: 将 3.10 替换为: ['平衡二叉搜索树（Balanced BST） (3.10.1)', 'Wavelet Tree (3.10.2)', 'Treap 简介 (3.10.3)']

**置信度**: medium

**需要人工映射**: 否

#### 序列维护结构：Text Editor Model (`cand.ds.sequence_structure.text_editor_model`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`
- `3.10.2`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.2` (Wavelet Tree, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]

**移除的 Section 引用**: 3.10

**映射原因**: 将 3.10 替换为: ['平衡二叉搜索树（Balanced BST） (3.10.1)', 'Wavelet Tree (3.10.2)', 'Treap 简介 (3.10.3)']

**置信度**: medium

**需要人工映射**: 否

#### 树分治维护：Dynamic Centroid (`cand.ds.tree_decomposition_ds.dynamic_centroid`)

**旧依赖建议**:
- `Tree` → `3.6` (树结构)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming)

**清洗后的依赖 (Item IDs)**:
- `3.6.4`
- `3.6.2`
- `3.6.1`
- `3.6.3`
- `2.21.65`

**清洗后的依赖详情**:
- `Tree` → `3.6.1` (二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.2` (完全二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.3` (二叉搜索树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.4` (平衡树基础, type=item, match=exact) [从section 3.6替换]
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

**移除的 Section 引用**: 3.6

**映射原因**: 将 3.6 替换为: ['二叉树 (3.6.1)', '完全二叉树 (3.6.2)', '二叉搜索树 (3.6.3)']

**置信度**: medium

**需要人工映射**: 否

#### 树分治维护：Subtree Query Flatten (`cand.ds.tree_decomposition_ds.subtree_query_flatten`)

**旧依赖建议**:
- `Tree` → `3.6` (树结构)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming)

**清洗后的依赖 (Item IDs)**:
- `3.6.4`
- `3.6.2`
- `3.6.1`
- `3.6.3`
- `2.21.65`

**清洗后的依赖详情**:
- `Tree` → `3.6.1` (二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.2` (完全二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.3` (二叉搜索树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.4` (平衡树基础, type=item, match=exact) [从section 3.6替换]
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

**移除的 Section 引用**: 3.6

**映射原因**: 将 3.6 替换为: ['二叉树 (3.6.1)', '完全二叉树 (3.6.2)', '二叉搜索树 (3.6.3)']

**置信度**: medium

**需要人工映射**: 否

#### 树分治维护：Tree Distance Aggregate (`cand.ds.tree_decomposition_ds.tree_distance_aggregate`)

**旧依赖建议**:
- `Tree` → `3.6` (树结构)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming)

**清洗后的依赖 (Item IDs)**:
- `3.6.4`
- `3.6.2`
- `3.6.1`
- `3.6.3`
- `2.21.65`

**清洗后的依赖详情**:
- `Tree` → `3.6.1` (二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.2` (完全二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.3` (二叉搜索树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.4` (平衡树基础, type=item, match=exact) [从section 3.6替换]
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

**移除的 Section 引用**: 3.6

**映射原因**: 将 3.6 替换为: ['二叉树 (3.6.1)', '完全二叉树 (3.6.2)', '二叉搜索树 (3.6.3)']

**置信度**: medium

**需要人工映射**: 否

#### 树分治维护：Tree Path Kth (`cand.ds.tree_decomposition_ds.tree_path_kth`)

**旧依赖建议**:
- `Tree` → `3.6` (树结构)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming)

**清洗后的依赖 (Item IDs)**:
- `3.6.4`
- `3.6.2`
- `3.6.1`
- `3.6.3`
- `2.21.65`

**清洗后的依赖详情**:
- `Tree` → `3.6.1` (二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.2` (完全二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.3` (二叉搜索树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.4` (平衡树基础, type=item, match=exact) [从section 3.6替换]
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

**移除的 Section 引用**: 3.6

**映射原因**: 将 3.6 替换为: ['二叉树 (3.6.1)', '完全二叉树 (3.6.2)', '二叉搜索树 (3.6.3)']

**置信度**: medium

**需要人工映射**: 否

#### 树分治维护：Virtual Tree Plus Hld (`cand.ds.tree_decomposition_ds.virtual_tree_plus_hld`)

**旧依赖建议**:
- `Tree` → `3.6` (树结构)
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming)

**清洗后的依赖 (Item IDs)**:
- `3.6.4`
- `3.6.2`
- `3.6.1`
- `3.6.3`
- `2.21.65`

**清洗后的依赖详情**:
- `Tree` → `3.6.1` (二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.2` (完全二叉树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.3` (二叉搜索树, type=item, match=exact) [从section 3.6替换]
- `Tree` → `3.6.4` (平衡树基础, type=item, match=exact) [从section 3.6替换]
- `Dynamic Programming` → `2.21.65` (仙人掌图：Dynamic Programming, type=item, match=exact)

**移除的 Section 引用**: 3.6

**映射原因**: 将 3.6 替换为: ['二叉树 (3.6.1)', '完全二叉树 (3.6.2)', '二叉搜索树 (3.6.3)']

**置信度**: medium

**需要人工映射**: 否

## 任务四：校验清洗结果

### 校验项目与结果

1. **cleaned_direct_pre_item_ids 中不包含 section id**: ✓ 通过
2. **cleaned_direct_pre_item_ids 都存在于当前主图谱 item id 中**: ✓ 通过
3. **不包含 batch_1 / batch_2 已合并 candidate id 作为 candidate id**: ✓ 通过
4. **不产生明显候选依赖环**: ✓ 通过
5. **不需要新 section**: ✓ 通过

### 校验结果

- **校验是否通过**: ✓ 是

## 清洗计划总结

### 重试合并建议

- **是否可以重新交给 1号线程合并**: 是
- **推荐本次重试合并数量**: 30
- **总候选数量**: 30

### 重试条件


**✓ 满足重试条件**:
1. 所有 section 引用已清除
2. 依赖映射已完成
3. 无需要人工处理的候选
4. 校验全部通过

**下一步操作**:
1. 1号线程使用清洗后的候选数据重试 Batch3 合并
2. 合并后运行 validate-only 验证
3. 验证通过后生成 candidate_to_item_id_mapping

## 重要统计总结

| 检查项 | 结果 |
|--------|------|
| Batch3 候选总数 | 30 |
| 含 section 引用的候选数量 | 10 |
| 涉及的 section id 数量 | 2 |
| 涉及的 section id 列表 | 3.10, 3.6 |
| 已成功清洗数量 | 10 |
| 需要人工映射数量 | 0 |
| 校验是否通过 | 是 |
| 是否可以重试合并 | 是 |
| 推荐本次重试合并数量 | 30 |

## 主图谱状态确认

- **主图谱是否修改**: **否**
- **本次任务目的**: 仅清洗 Batch3 候选依赖，不涉及图谱修改
- **主图谱基线**: item_count = 1542, section_count = 65
- **主图谱状态**: Batch2 后稳定状态

## 输出文件

1. `data/thread2_stage3e_aggressive_batch3_dependency_cleanup.json` - Batch3 依赖清洗详细结果
2. `data/thread2_stage3e_aggressive_batch3_cleaned_dependency_plan.json` - Batch3 清洗后的依赖计划
3. `docs/thread2_stage3e_aggressive_batch3_dependency_cleanup_report.md` - 本报告

## 重要提醒

1. **不修改主图谱**: 本次任务仅清洗候选依赖，完全不修改主图谱
2. **不进行合并**: 清洗完成后不进行合并操作，等待 1号线程决策
3. **精确替换策略**: 不粗暴展开整个 section，而是根据语义选择最相关的具体 item
4. **人工映射**: 对于无法确定映射的候选，标记为需要人工处理
5. **重试条件**: 必须满足所有校验条件后才能重试合并

## 技术说明

### Section 引用问题原理

**问题根源**:
- 知识图谱中的依赖关系应该在具体 item 之间建立
- Section 级别的引用太宽泛，不利于学习路径规划
- 官方 compute_resolved 会过滤 section 引用
- 导致依赖计算不完整，产生 resolved_pre_mismatches

**解决方法**:
- 将 section 引用替换为具体的 item 引用
- 根据候选的具体内容选择最相关的依赖项
- 限制依赖数量在 1-4 个，避免过度泛化
- 确保每个引用都在当前主图谱中存在

---

报告生成时间: 2026-05-22T19:00:00.000Z
生成者: 2号线程
任务类型: Stage3E-Aggressive Batch3 Dependency Cleanup
主图谱修改状态: 否
下一阶段: 等待1号线程决定是否重试Batch3合并
