# 动画覆盖审计报告 v2 (均衡选择版)

**审计时间**: 2026-09-02 22:19:04
**知识点总数**: 3240
**已有动画数**: 115 (覆盖 112 个 itemId)
**动画覆盖率**: 3.5%

## 1. 动画优先级分布

| 优先级 | 数量 | 已有动画 | 含义 |
|--------|------|----------|------|
| P0 | 1077 | 10 | 强烈建议动画 |
| P1 | 445 | 26 | 适合动画 |
| P2 | 1374 | 74 | 可选动画 |
| NONE | 344 | 2 | 不适合动画 |

## 2. 旧清单问题与改进

### 旧清单问题:
- 旧清单按 ID 顺序选取，2.1 章节占据过多名额
- 未考虑竞赛核心价值和初学者收益的综合评分
- 未做章节均衡限制
- 未标注模板复用潜力和工作量估计

### 新清单改进:
- 按算法类别 must_have 模式匹配核心知识点
- 综合评分: 竞赛核心价值 + 初学者收益 + 动画表达 + 无动画加分 + 复用潜力
- 每章节最多 6 个名额，确保分布均衡
- 标注推荐模板、工作量、复用潜力
- 生成暂缓高优先级清单供后续批次使用

## 3. 第一批动画制作清单 (均衡选择版)

**总数**: 50 个 | **每章节上限**: 6 个

| # | ID | 名称 | 章节 | 优先级 | 评分 | 推荐形式 | 模板 | 工作量 | 复用 | 来源 |
|---|----|----|----|--------|------|---------|------|--------|------|------|
| 1 | 2.5.22 | 搜索进阶：双向BFS优化 | 双指针与滑动窗口 | P0 | 92.0 | Flutter | graph_traversal | medium | high | must_have  |
| 2 | 2.5.23 | 搜索进阶：DFS序与回溯 | 双指针与滑动窗口 | P0 | 92.0 | Flutter | backtrack | medium | high | must_have  |
| 3 | 2.7.55 | 双向 BFS的可行性剪枝 (双向 BFS Feasibility Pruning) | 搜索 | P0 | 72.0 | Flutter | backtrack | low | high | must_have  |
| 4 | 3.13.320 | 按秩合并并查集的撤销栈 (按秩合并并查集 Undo Stack) | 高级数据结构扩展 | P0 | 92.0 | Flutter | stack | low | high | must_have  |
| 5 | 2.8.266 | 背包 DP 的单调队列优化 (背包 DP Monotone Queue Optimization) | 动态规划 | P0 | 65.0 | static_steps | queue | low | high | must_have  |
| 6 | 3.13.156 | 线段树变体：Dynamic Segment Tree | 高级数据结构扩展 | P0 | 50.0 | Flutter | segment_tree | high | medium | must_have  |
| 7 | 2.13.18 | Dijkstra (堆优化) | 最短路与生成树 | P0 | 72.0 | Flutter | shortest_path | medium | high | must_have  |
| 8 | 2.13.9 | Kruskal | 最短路与生成树 | P0 | 40.0 | Flutter | mst | medium | medium | must_have  |
| 9 | 2.13.14 | 最小生成树：Prim 算法 (堆优化) | 最短路与生成树 | P0 | 72.0 | Flutter | mst | medium | medium | must_have  |
| 10 | 2.10.17 | 扩展 KMP | 字符串算法 | P0 | 60.0 | HTML | string_match | medium | high | must_have  |
| 11 | 3.6.8 | 字典树 (Trie) | 树结构 | P0 | 40.0 | Flutter | trie | medium | high | must_have  |
| 12 | 3.13.394 | 李超线段树的合并操作 (李超线段树 Merge Operation) | 高级数据结构扩展 | P0 | 70.0 | Flutter | li_chao | high | low | must_have  |
| 13 | 3.7.47 | 动态开点线段树的合并操作 (动态开点线段树 Merge Operation) | 区间维护结构 | P0 | 70.0 | Flutter | dynamic_open | medium | medium | must_have  |
| 14 | 3.2.10 | 单调栈构建笛卡尔树 | 栈与队列 | P0 | 82.0 | Flutter | monotone_stack | medium | high | must_have  |
| 15 | 2.9.135 | 建模方法：前缀和与差分扩展 | 图基础与遍历 | P1 | 92.0 | Flutter | prefix_sum | low | high | must_have  |
| 16 | 2.4.19 | 前缀和 (多维差分) | 前缀、差分、离散化、分块 | P1 | 72.0 | Flutter | difference | low | high | must_have  |
| 17 | 1.8.41 | 拓扑排序 (DFS 着色法) | 结构体与 STL | P0 | 92.0 | Flutter | graph_traversal | medium | high | scored  |
| 18 | 2.2.15 | 排序：归并排序 | 排序与顺序统计 | P1 | 92.0 | Flutter | sorting | medium | high | scored  |
| 19 | 2.2.16 | 排序：快速排序 | 排序与顺序统计 | P1 | 92.0 | Flutter | sorting | medium | high | scored  |
| 20 | 2.2.17 | 排序：堆排序 | 排序与顺序统计 | P0 | 92.0 | Flutter | sorting | medium | high | scored  |
| 21 | 2.2.6 | 堆排序 | 排序与顺序统计 | P0 | 92.0 | Flutter | sorting | medium | high | scored  |
| 22 | 2.4.58 | 分块并查集的询问排序 (分块并查集 Query Ordering) | 前缀、差分、离散化、分块 | P0 | 92.0 | Flutter | sorting | low | high | scored  |
| 23 | 2.7.28 | 搜索进阶：哈希优化BFS | 搜索 | P0 | 92.0 | Flutter | graph_traversal | low | high | scored  |
| 24 | 2.8.223 | 堆维护 DP的转移图稀疏化 (堆维护 DP Transition Graph Sparsification) | 动态规划 | P0 | 92.0 | Flutter | heap | medium | high | scored  |
| 25 | 2.9.177 | BFS 到最短路的权值扩展 (BFS 到最短路 权值扩展) | 图基础与遍历 | P0 | 92.0 | Flutter | graph_traversal | low | high | scored  |
| 26 | 3.13.1 | 归并排序树：Range Count | 高级数据结构扩展 | P1 | 92.0 | Flutter | sorting | medium | high | scored  |
| 27 | 3.13.11 | 归并排序树：Range Kth With Binary Search | 高级数据结构扩展 | P1 | 92.0 | Flutter | sorting | medium | high | scored  |
| 28 | 3.13.21 | 归并排序树：Fractional Cascading | 高级数据结构扩展 | P1 | 92.0 | Flutter | sorting | medium | high | scored  |
| 29 | 3.4.12 | 并查集扩展域 | 并查集 | P0 | 92.0 | Flutter | dsu | low | high | scored  |
| 30 | 3.4.5 | 扩展域并查集 | 并查集 | P0 | 92.0 | Flutter | dsu | low | high | scored  |
| 31 | 3.4.9 | 并查集：按秩合并 | 并查集 | P0 | 92.0 | Flutter | dsu | low | high | scored  |
| 32 | 3.5.17 | 二项堆合并 | 堆 | P0 | 92.0 | Flutter | heap | medium | high | scored  |
| 33 | 5.5.4 | BFS 入队即标记 | 图论实现技巧 | P0 | 92.0 | Flutter | graph_traversal | low | high | scored  |
| 34 | 2.13.1 | BFS 最短路 | 最短路与生成树 | P0 | 72.0 | Flutter | graph_traversal | low | high | scored  |
| 35 | 2.13.5 | 0-1 BFS | 最短路与生成树 | P0 | 72.0 | Flutter | graph_traversal | low | high | scored  |
| 36 | 2.15.18 | 最短路进阶：0-1BFS变体 | 连通分量与特殊图 | P0 | 72.0 | Flutter | graph_traversal | low | high | scored  |
| 37 | 2.2.4 | 归并排序 | 排序与顺序统计 | P1 | 72.0 | Flutter | sorting | medium | high | scored [已有] |
| 38 | 2.2.5 | 快速排序 | 排序与顺序统计 | P1 | 72.0 | Flutter | sorting | medium | high | scored [已有] |
| 39 | 2.21.170 | 高级最短路：Zero One Bfs Modeling | 高级图论扩展 | P0 | 72.0 | Flutter | graph_traversal | low | high | scored  |
| 40 | 2.4.2 | 二维前缀和 | 前缀、差分、离散化、分块 | P1 | 72.0 | Flutter | prefix_sum | low | high | scored  |
| 41 | 2.4.26 | 树上前缀和 | 前缀、差分、离散化、分块 | P1 | 72.0 | Flutter | dp_tree | low | high | scored  |
| 42 | 2.4.36 | DP 优化：前缀和优化 | 前缀、差分、离散化、分块 | P1 | 72.0 | static_steps | dp_table | low | high | scored  |
| 43 | 2.4.38 | 高维前缀和 | 前缀、差分、离散化、分块 | P1 | 72.0 | Flutter | prefix_sum | low | high | scored  |
| 44 | 2.6.23 | 堆维护贪心的可交换性条件 (堆维护贪心 Exchangeability Condition) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 45 | 2.6.24 | 堆维护贪心的单调选择性质 (堆维护贪心 Monotone Choice Property) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 46 | 2.6.55 | 堆维护贪心的反悔机制 (堆维护贪心 Regret Mechanism) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 47 | 2.6.56 | 堆维护贪心的带权变体 (堆维护贪心 Weighted Variant) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 48 | 2.6.57 | 堆维护贪心的多约束变体 (堆维护贪心 Multi-constraint Variant) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 49 | 2.6.58 | 堆维护贪心的最优性证明组件 (堆维护贪心 Optimality Component) | 贪心 | P0 | 72.0 | Flutter | heap | medium | high | scored  |
| 50 | 2.7.16 | 图的遍历：DFS | 搜索 | P0 | 72.0 | Flutter | graph_traversal | low | high | scored [已有] |

### 章节分布

- 3.13 3.13 高级数据结构扩展: 6 个
- 2.4 2.4 前缀、差分、离散化、分块: 6 个
- 2.2 2.2 排序与顺序统计: 6 个
- 2.6 2.6 贪心: 6 个
- 2.13 2.13 最短路与生成树: 5 个
- 2.7 2.7 搜索: 3 个
- 3.4 3.4 并查集: 3 个
- 2.5 2.5 双指针与滑动窗口: 2 个
- 2.8 2.8 动态规划: 2 个
- 2.9 2.9 图基础与遍历: 2 个
- 2.10 2.10 字符串算法: 1 个
- 3.6 3.6 树结构: 1 个
- 3.7 3.7 区间维护结构: 1 个
- 3.2 3.2 栈与队列: 1 个
- 1.8 1.8 结构体与 STL: 1 个
- 3.5 3.5 堆: 1 个
- 5.5 5.5 图论实现技巧: 1 个
- 2.15 2.15 连通分量与特殊图: 1 个
- 2.21 2.21 高级图论扩展: 1 个

### 动画形式分布

- Flutter 原生动画 JSON: 47 个
- 静态图 + 步骤: 2 个
- HTML/WebView: 1 个

### 工作量分布

- medium: 27 个
- low: 21 个
- high: 2 个

## 4. 暂缓高优先级清单 (P0 未入选)

**暂缓总数**: 1040 个 (仅列前 30)

| ID | 名称 | 章节 | 评分 | 暂缓原因 |
|----|----|----|------|---------|
| 3.13.244 | 按秩合并并查集的集合语义 (按秩合并并查集 Set Semantics) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.251 | 可持久化堆版本合并 (可持久化堆版本合并) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.279 | 可撤销并查集的合并约束 (可撤销并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.280 | 种类并查集的合并约束 (种类并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.281 | 带权并查集的合并约束 (带权并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.282 | 可持久化并查集的合并约束 (可持久化并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.283 | 按秩合并并查集的合并约束 (按秩合并并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.284 | 路径压缩并查集的合并约束 (路径压缩并查集 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.285 | 并查集维护二分性的合并约束 (并查集维护二分性 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.286 | 并查集维护距离的合并约束 (并查集维护距离 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.287 | 并查集维护势能的合并约束 (并查集维护势能 Merge Constraint) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.319 | 按秩合并并查集的权值关系 (按秩合并并查集 Weighted Relation) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.321 | 按秩合并并查集的离线动态连通性 (按秩合并并查集 Offline Dynamic Connectivity) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.322 | 按秩合并并查集的矛盾判定 (按秩合并并查集 Contradiction Detection) | 高级数据结构扩展 | 92.0 | 章节 3.13 名额已满 |
| 3.13.232 | 单调栈的弹出条件 (单调栈 Pop Condition) | 高级数据结构扩展 | 82.0 | 章节 3.13 名额已满 |
| 2.4.57 | 分块并查集的块大小选择 (分块并查集 Block Size Selection) | 前缀、差分、离散化、分块 | 72.0 | 章节 2.4 名额已满 |
| 2.4.63 | 分块并查集的增删贡献维护 (分块并查集 Add Remove Contribution) | 前缀、差分、离散化、分块 | 72.0 | 章节 2.4 名额已满 |
| 2.4.75 | 分块并查集的修改时间维 (分块并查集 Modification Time Dimension) | 前缀、差分、离散化、分块 | 72.0 | 章节 2.4 名额已满 |
| 2.4.76 | 分块并查集的回滚状态 (分块并查集 Rollback State) | 前缀、差分、离散化、分块 | 72.0 | 章节 2.4 名额已满 |
| 2.4.77 | 分块并查集的复杂度平衡 (分块并查集 Complexity Balancing) | 前缀、差分、离散化、分块 | 72.0 | 章节 2.4 名额已满 |
| 2.7.17 | 图的遍历：BFS | 搜索 | 72.0 | 评分低于第一批阈值, 已有动画 |
| 2.7.18 | BFS 求无权图最短路 | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.19 | DFS 求连通分量 | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.20 | 树的直径 (两次 BFS/DFS) | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.21 | DFS 序与欧拉序 | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.22 | 匈牙利算法 DFS 与 BFS 版本 | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.33 | 双向 BFS的状态图模型 (双向 BFS State Graph Model) | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.34 | 双向 BFS的路径恢复 (双向 BFS Path Reconstruction) | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.35 | 多源 BFS的状态图模型 (多源 BFS State Graph Model) | 搜索 | 72.0 | 评分低于第一批阈值 |
| 2.7.36 | 多源 BFS的路径恢复 (多源 BFS Path Reconstruction) | 搜索 | 72.0 | 评分低于第一批阈值 |

## 5. 推荐动画模板复用

### backtrack (2 个)
- 2.5.23 搜索进阶：DFS序与回溯
- 2.7.55 双向 BFS的可行性剪枝 (双向 BFS Feasibility Pruning)

### difference (1 个)
- 2.4.19 前缀和 (多维差分)

### dp_table (1 个)
- 2.4.36 DP 优化：前缀和优化

### dp_tree (1 个)
- 2.4.26 树上前缀和

### dsu (3 个)
- 3.4.12 并查集扩展域
- 3.4.5 扩展域并查集
- 3.4.9 并查集：按秩合并

### dynamic_open (1 个)
- 3.7.47 动态开点线段树的合并操作 (动态开点线段树 Merge Operation)

### graph_traversal (10 个)
- 2.5.22 搜索进阶：双向BFS优化
- 1.8.41 拓扑排序 (DFS 着色法)
- 2.7.28 搜索进阶：哈希优化BFS
- 2.9.177 BFS 到最短路的权值扩展 (BFS 到最短路 权值扩展)
- 5.5.4 BFS 入队即标记
- 2.13.1 BFS 最短路
- 2.13.5 0-1 BFS
- 2.15.18 最短路进阶：0-1BFS变体
- 2.21.170 高级最短路：Zero One Bfs Modeling
- 2.7.16 图的遍历：DFS

### heap (8 个)
- 2.8.223 堆维护 DP的转移图稀疏化 (堆维护 DP Transition Graph Sparsification)
- 3.5.17 二项堆合并
- 2.6.23 堆维护贪心的可交换性条件 (堆维护贪心 Exchangeability Condition)
- 2.6.24 堆维护贪心的单调选择性质 (堆维护贪心 Monotone Choice Property)
- 2.6.55 堆维护贪心的反悔机制 (堆维护贪心 Regret Mechanism)
- 2.6.56 堆维护贪心的带权变体 (堆维护贪心 Weighted Variant)
- 2.6.57 堆维护贪心的多约束变体 (堆维护贪心 Multi-constraint Variant)
- 2.6.58 堆维护贪心的最优性证明组件 (堆维护贪心 Optimality Component)

### li_chao (1 个)
- 3.13.394 李超线段树的合并操作 (李超线段树 Merge Operation)

### monotone_stack (1 个)
- 3.2.10 单调栈构建笛卡尔树

### mst (2 个)
- 2.13.9 Kruskal
- 2.13.14 最小生成树：Prim 算法 (堆优化)

### prefix_sum (3 个)
- 2.9.135 建模方法：前缀和与差分扩展
- 2.4.2 二维前缀和
- 2.4.38 高维前缀和

### queue (1 个)
- 2.8.266 背包 DP 的单调队列优化 (背包 DP Monotone Queue Optimization)

### segment_tree (1 个)
- 3.13.156 线段树变体：Dynamic Segment Tree

### shortest_path (1 个)
- 2.13.18 Dijkstra (堆优化)

### sorting (10 个)
- 2.2.15 排序：归并排序
- 2.2.16 排序：快速排序
- 2.2.17 排序：堆排序
- 2.2.6 堆排序
- 2.4.58 分块并查集的询问排序 (分块并查集 Query Ordering)
- 3.13.1 归并排序树：Range Count
- 3.13.11 归并排序树：Range Kth With Binary Search
- 3.13.21 归并排序树：Fractional Cascading
- 2.2.4 归并排序
- 2.2.5 快速排序

### stack (1 个)
- 3.13.320 按秩合并并查集的撤销栈 (按秩合并并查集 Undo Stack)

### string_match (1 个)
- 2.10.17 扩展 KMP

### trie (1 个)
- 3.6.8 字典树 (Trie)

## 6. 章节动画价值排名 (前 15)

| # | 章节 | 总数 | P0 | P1 | 价值分 | 已有动画 | 覆盖率 | 建议 |
|---|------|------|----|----|--------|---------|--------|------|
| 1 | 3.13 3.13 高级数据结构扩展 | 374 | 246 | 49 | 908 | 0 | 0.0% | 强烈建议重点动画化 |
| 2 | 2.8 2.8 动态规划 | 292 | 87 | 52 | 507 | 2 | 0.7% | 强烈建议重点动画化 |
| 3 | 4.1 4.1 整数与数论基础 | 193 | 67 | 6 | 262 | 8 | 4.1% | 强烈建议重点动画化 |
| 4 | 2.21 2.21 高级图论扩展 | 186 | 41 | 9 | 257 | 0 | 0.0% | 强烈建议重点动画化 |
| 5 | 4.3 4.3 计数与组合 | 158 | 55 | 10 | 253 | 11 | 7.0% | 强烈建议重点动画化 |
| 6 | 2.1 2.1 基础算法思想 | 108 | 43 | 40 | 234 | 1 | 0.9% | 强烈建议重点动画化 |
| 7 | 2.9 2.9 图基础与遍历 | 204 | 17 | 18 | 231 | 0 | 0.0% | 强烈建议重点动画化 |
| 8 | 2.10 2.10 字符串算法 | 81 | 58 | 0 | 197 | 0 | 0.0% | 强烈建议重点动画化 |
| 9 | 2.20 2.20 交互题与构造题技巧 | 187 | 20 | 22 | 190 | 0 | 0.0% | 强烈建议重点动画化 |
| 10 | 2.4 2.4 前缀、差分、离散化、分块 | 82 | 29 | 35 | 172 | 8 | 9.8% | 强烈建议重点动画化 |
| 11 | 2.7 2.7 搜索 | 94 | 37 | 16 | 170 | 8 | 8.5% | 强烈建议重点动画化 |
| 12 | 3.7 3.7 区间维护结构 | 52 | 50 | 0 | 152 | 0 | 0.0% | 强烈建议重点动画化 |
| 13 | 2.6 2.6 贪心 | 70 | 6 | 51 | 131 | 1 | 1.4% | 建议动画化 |
| 14 | 4.7 4.7 几何基础 | 63 | 23 | 2 | 107 | 8 | 12.7% | 强烈建议重点动画化 |
| 15 | 1.6 1.6 数组与字符串 | 50 | 27 | 1 | 105 | 3 | 6.0% | 强烈建议重点动画化 |

## 7. 重要声明

**本次审计严格遵循只读原则，未修改以下任何文件:**
- 主图谱 (merged_knowledge_graph_item_dependencies_refined.json)
- 前端图谱 (assets/data/knowledge/io_v4_4.json)
- 内容索引 (assets/data/knowledge_content/content_index.json)
- 内容正文文件 (assets/data/knowledge_content/items/*)
- Flutter 代码 (lib/*, test/*, pubspec.yaml)
- 动画数据文件 (assets/data/cpp/animations/*)

**生成/更新的文件:**
- tools/audit_animation_coverage.py (本脚本)
- docs/animation_coverage_audit_report.md (本报告)
- data/animation_coverage_audit.json (数据报告)
- docs/animation_first_batch_selection_review.md (清单审查报告)
- data/animation_first_batch_selection_review.json (清单审查数据)
