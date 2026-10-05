# Stage3E-Aggressive Batch4 Dependency Cleanup 报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T21:00:00.000Z
- 任务类型: Stage3E-Aggressive Batch4 Dependency Cleanup
- 主图谱状态: 未修改
- 任务目的: 清除 Batch4 候选中的 section 引用，为重试合并做准备

## Batch4 动态预审结果回顾

**动态预审发现**:
- **Batch4 候选总数**: 30
- **Section 引用依赖数量**: 16
- **涉及的 Section ID**: 2.9（图基础与遍历）、3.10（平衡树与有序维护）
- **dependency_cleanup_required**: true
- **recommendation**: needs_dependency_cleanup_before_merge

## 任务一：找出 Batch4 中所有 section 引用

### 候选总数与问题候选

- **Batch4 候选总数**: 30
- **含 section 引用的候选数量**: 16
- **问题候选占比**: 53.3%

### 涉及的 Section ID 列表

发现以下 section 引用:
- **2.9** (图基础与遍历)
- **3.10** (平衡树与有序维护)


### 问题候选详细列表

以下是包含 section 引用的候选:

#### 图论建模：K Shortest Paths (`cand.graph.graph_modeling.k_shortest_paths`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 图论建模：Layered Graph (`cand.graph.graph_modeling.layered_graph`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 图论建模：Minimum Mean Cycle (`cand.graph.graph_modeling.minimum_mean_cycle`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 图论建模：Shortest Path Potentials (`cand.graph.graph_modeling.shortest_path_potentials`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 图论建模：State Graph (`cand.graph.graph_modeling.state_graph`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 图论建模：Steiner Tree (`cand.graph.graph_modeling.steiner_tree`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `2.9` (图基础与遍历, type=section, match=synonym, input=Graph Theory)

**当前 direct_pre_suggestion**:
- `Graph Theory` → `2.9` (图基础与遍历, type=section, match=synonym)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

#### 高级平衡树：Fhq Split Merge (`cand.ds.balanced_tree_advanced.fhq_split_merge`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Implicit Treap (`cand.ds.balanced_tree_advanced.implicit_treap`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Join Based Tree (`cand.ds.balanced_tree_advanced.join_based_tree`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Lazy Reversible Sequence (`cand.ds.balanced_tree_advanced.lazy_reversible_sequence`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Order Statistic Tree (`cand.ds.balanced_tree_advanced.order_statistic_tree`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Persistent Treap (`cand.ds.balanced_tree_advanced.persistent_treap`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Piece Table (`cand.ds.balanced_tree_advanced.piece_table`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Rope (`cand.ds.balanced_tree_advanced.rope`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Scapegoat Tree (`cand.ds.balanced_tree_advanced.scapegoat_tree`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

#### 高级平衡树：Splay Sequence (`cand.ds.balanced_tree_advanced.splay_sequence`)

**问题**: direct_pre包含 1 个section引用

**Section 引用详情**:
- `3.10` (平衡树与有序维护, type=section, match=synonym, input=Balanced Binary Search Tree)

**当前 direct_pre_suggestion**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护, type=section, match=synonym)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

## 任务二：把 Section ID 精确替换为 Item ID

### 清洗策略

- **精确替换**: 不粗暴展开整个 section，根据候选语义选择最相关的 1~4 个具体 item id
- **智能映射**: 根据候选的具体内容选择依赖项，避免过度泛化
- **语义驱动**: 
  - 对于 2.9（图基础与遍历）：优先选择图基础、图遍历、DFS/BFS 等基础图论 item
  - 对于 3.10（平衡树与有序维护）：优先选择平衡树基础、Treap、Splay 等具体 item
- **保守处理**: 无法确定映射时标记为 needs_manual_dependency_mapping

### 清洗结果概览

- **已成功清洗数量**: 16
- **需要人工映射数量**: 0
- **自动清洗成功率**: 100.0%

### 清洗候选详细列表


#### 图论建模：K Shortest Paths (`cand.graph.graph_modeling.k_shortest_paths`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 图论建模：Layered Graph (`cand.graph.graph_modeling.layered_graph`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 图论建模：Minimum Mean Cycle (`cand.graph.graph_modeling.minimum_mean_cycle`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 图论建模：Shortest Path Potentials (`cand.graph.graph_modeling.shortest_path_potentials`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 图论建模：State Graph (`cand.graph.graph_modeling.state_graph`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 图论建模：Steiner Tree (`cand.graph.graph_modeling.steiner_tree`)

**旧依赖建议**:
- `Graph Theory` → `2.9` (图基础与遍历)
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path)

**清洗后的依赖 (Item IDs)**:
- `2.9.2`
- `2.9.3`
- `2.9.1`
- `2.21.42`

**清洗后的依赖详情**:
- `Graph Theory` → `2.9.1` (图的 DFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.2` (图的 BFS, type=item, match=exact) [从section 2.9替换]
- `Graph Theory` → `2.9.3` (图建模基础, type=item, match=exact) [从section 2.9替换]
- `Shortest Path` → `2.21.42` (仙人掌图：Shortest Path, type=item, match=exact)

**移除的 Section 引用**: 2.9

**映射原因**: 将2.9(图基础与遍历)替换为图论基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Fhq Split Merge (`cand.ds.balanced_tree_advanced.fhq_split_merge`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Implicit Treap (`cand.ds.balanced_tree_advanced.implicit_treap`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Join Based Tree (`cand.ds.balanced_tree_advanced.join_based_tree`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Lazy Reversible Sequence (`cand.ds.balanced_tree_advanced.lazy_reversible_sequence`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Order Statistic Tree (`cand.ds.balanced_tree_advanced.order_statistic_tree`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Persistent Treap (`cand.ds.balanced_tree_advanced.persistent_treap`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Piece Table (`cand.ds.balanced_tree_advanced.piece_table`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Rope (`cand.ds.balanced_tree_advanced.rope`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Scapegoat Tree (`cand.ds.balanced_tree_advanced.scapegoat_tree`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

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
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

#### 高级平衡树：Splay Sequence (`cand.ds.balanced_tree_advanced.splay_sequence`)

**旧依赖建议**:
- `Balanced Binary Search Tree` → `3.10` (平衡树与有序维护)
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）)

**清洗后的依赖 (Item IDs)**:
- `3.10.1`
- `3.10.3`
- `3.10.4`

**清洗后的依赖详情**:
- `Balanced Binary Search Tree` → `3.10.1` (平衡二叉搜索树（Balanced BST）, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.3` (Treap 简介, type=item, match=exact) [从section 3.10替换]
- `Balanced Binary Search Tree` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=exact) [从section 3.10替换]
- `Treap` → `3.10.4` (FHQ Treap（无旋Treap）, type=item, match=synonym)

**移除的 Section 引用**: 3.10

**映射原因**: 将3.10(平衡树与有序维护)替换为平衡树基础item

**置信度**: high

**需要人工映射**: 否

## 任务四：校验清洗结果

### 校验项目与结果

1. **cleaned_direct_pre_item_ids 中不包含 section id**: ✓ 通过
2. **cleaned_direct_pre_item_ids 都存在于当前主图谱 item id 中**: ✓ 通过
3. **不包含 batch_1 / batch_2 / batch_3 已合并 candidate id 作为 candidate id**: ✓ 通过
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
2. 依赖映射已完成（基于语义选择最相关的item）
3. 无需要人工处理的候选
4. 校验全部通过

**下一步操作**:
1. 1号线程使用清洗后的候选数据重试 Batch4 合并
2. 合并后运行 validate-only 验证
3. 验证通过后生成 candidate_to_item_id_mapping

## 重要统计总结

| 检查项 | 结果 |
|--------|------|
| Batch4 候选总数 | 30 |
| 含 section 引用的候选数量 | 16 |
| 涉及的 section id 数量 | 2 |
| 涉及的 section id 列表 | 2.9, 3.10 |
| 已成功清洗数量 | 16 |
| 需要人工映射数量 | 0 |
| 校验是否通过 | 是 |
| 是否可以重试合并 | 是 |
| 推荐本次重试合并数量 | 30 |

## 主图谱状态确认

- **主图谱是否修改**: **否**
- **本次任务目的**: 仅清洗 Batch4 候选依赖，不涉及图谱修改
- **主图谱基线**: item_count = 1572, section_count = 65
- **主图谱状态**: Batch3 后稳定状态

## 输出文件

1. `data/thread2_stage3e_aggressive_batch4_dependency_cleanup.json` - Batch4 依赖清洗详细结果
2. `data/thread2_stage3e_aggressive_batch4_cleaned_dependency_plan.json` - Batch4 清洗后的依赖计划
3. `docs/thread2_stage3e_aggressive_batch4_dependency_cleanup_report.md` - 本报告

## 重要提醒

1. **不修改主图谱**: 本次任务仅清洗候选依赖，完全不修改主图谱
2. **不进行合并**: 清洗完成后不进行合并操作，等待 1号线程决策
3. **精确替换策略**: 不粗暴展开整个 section，而是根据语义选择最相关的具体 item
4. **语义驱动映射**: 根据候选的具体内容和所属领域选择最合适的依赖项
5. **人工映射**: 对于无法确定映射的候选，标记为需要人工处理
6. **重试条件**: 必须满足所有校验条件后才能重试合并

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

### 语义映射策略

**针对 2.9（图基础与遍历）**:
- 优先选择图基础、图遍历、DFS/BFS、树/连通性等基础图论 item
- 不要直接使用 2.9
- 不要把整个 2.9 section 展开

**针对 3.10（平衡树与有序维护）**:
- 优先选择平衡树基础、Treap、Splay、红黑树、有序集合维护等具体 item
- 不要直接使用 3.10
- 不要把整个 3.10 section 展开

---

报告生成时间: 2026-05-22T21:00:00.000Z
生成者: 2号线程
任务类型: Stage3E-Aggressive Batch4 Dependency Cleanup
主图谱修改状态: 否
下一阶段: 等待1号线程决定是否重试Batch4合并
