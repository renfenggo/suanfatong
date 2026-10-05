# Stage3F Batch3 Full40 候选计划与动态预审报告

## 基本信息

| 项目 | 值 |
|------|------|
| **批次** | Stage3F Batch3 Full40 |
| **目标候选数** | 40 |
| **实际入选数** | 40 |
| **生成时间** | 2026-05-25T17:00:00 |
| **主图谱修改** | 否 |

## 当前主图谱状态

| 检查项 | 预期值 | 实际值 | 状态 |
|--------|--------|--------|------|
| item_count | 1677 | 1677 | ✅ |
| section_count | 65 | 65 | ✅ |
| validate-only passed | true | true | ✅ |
| resolved_pre_mismatches | [] | [] | ✅ |
| dangling_refs | [] | [] | ✅ |
| direct_pre_cycle | null | null | ✅ |
| product_metadata_validation.passed | true | true | ✅ |
| report_matches_json | true | true | ✅ |
| passed | true | true | ✅ |

## 候选池分析

| 指标 | 数量 |
|------|------|
| 标准化候选池总数 | 129 |
| Batch1 已使用 | 20 |
| Batch2 已使用 | 20 |
| 排除重复候选 | 0 |
| **剩余可选** | 129 |
| **Batch3 入选** | **40** |

## Batch3 Full40 候选列表

### 按 Source 分布

| Source | 数量 |
|--------|------|
| external_b1 | 11 |
| external_b2 | 29 |

### 按 Section 分布

| Section | Section 名称 | 数量 |
|---------|-------------|------|
| 2.10 | 字符串算法 | 5 |
| 2.17 | 线性代数与插值 | 2 |
| 2.18 | 综合高级技巧 | 4 |
| 2.21 | 高级图论扩展 | 5 |
| 2.8 | 动态规划 | 8 |
| 3.13 | 高级数据结构扩展 | 6 |
| 3.8 | 字符串结构 | 2 |
| 4.1 | 整数与数论基础 | 4 |
| 4.9 | 高级数学与群论 | 4 |

### 按 Risk 分布

| Risk Band | 数量 |
|-----------|------|
| green | 9 |
| yellow | 31 |

### 入选候选详情

| # | candidate_id | 名称 | Source | Section | Risk | Confidence |
|---|-------------|------|--------|---------|------|-----------|
| 1 | cand.dp.dag.longest_path | DAG最长路DP | external_b2 | 2.8 | yellow | high |
| 2 | cand.dp.state_compression.basic | 状态压缩DP基础 | external_b2 | 2.8 | yellow | high |
| 3 | cand.dp.state_compression.traveling | 旅行商问题DP | external_b2 | 2.8 | yellow | high |
| 4 | cand.dp.subset.basic | 子集DP基础 | external_b2 | 2.8 | yellow | high |
| 5 | cand.dp.subset.enumeration | 子集枚举优化 | external_b2 | 2.8 | yellow | high |
| 6 | cand.dp.automaton.basic | 自动机DP基础 | external_b2 | 2.8 | yellow | high |
| 7 | cand.dp.automaton.matrix | 自动机矩阵DP | external_b2 | 2.8 | yellow | high |
| 8 | cand.dp.probability.basic | 概率DP基础 | external_b2 | 2.8 | yellow | high |
| 9 | cand.string.border_tree.structure | Border树结构 | external_b2 | 2.10 | yellow | high |
| 10 | cand.string.manacher.algorithm | Manacher算法 | external_b2 | 2.10 | yellow | high |
| 11 | cand.string.boyer_moore.algorithm | Boyer-Moore算法 | external_b2 | 2.10 | yellow | high |
| 12 | cand.string.rabin_karp.algorithm | Rabin-Karp算法 | external_b2 | 2.10 | yellow | high |
| 13 | cand.string.string_matching.kmp | KMP算法详解 | external_b2 | 2.10 | yellow | high |
| 14 | cand.string.lyndon_decomposition.basic | Lyndon分解基础 | external_b2 | 3.8 | yellow | high |
| 15 | cand.string.runs_repetitions.basic | Runs重复子串分析 | external_b2 | 3.8 | yellow | high |
| 16 | cand.math.quadratic_residue.legendre_symbol | Legendre符号 | external_b2 | 4.1 | yellow | high |
| 17 | cand.math.quadratic_residue.tonelli_shanks | Tonelli-Shanks算法 | external_b2 | 4.1 | yellow | high |
| 18 | cand.math.crt.extended | 扩展中国剩余定理 | external_b2 | 4.1 | yellow | high |
| 19 | cand.math.crt.garner | Garner算法 | external_b2 | 4.1 | yellow | high |
| 20 | cand.math.euler_function.applications | 欧拉函数应用 | external_b2 | 4.9 | yellow | high |
| 21 | cand.math.sieve.du_jiao | 杜教筛 | external_b2 | 4.9 | yellow | high |
| 22 | cand.math.group_theory.burnside | Burnside引理 | external_b2 | 4.9 | yellow | high |
| 23 | cand.math.group_theory.polya | Polya计数定理 | external_b2 | 4.9 | yellow | high |
| 24 | cand.math.polynomial.fwt | 快速沃尔什变换 | external_b2 | 2.17 | yellow | high |
| 25 | cand.math.polynomial.subset_convolution | 子集卷积 | external_b2 | 2.17 | yellow | high |
| 26 | cand.dp.optimization.slope.basic | 斜率优化基础 | external_b2 | 2.18 | yellow | high |
| 27 | cand.dp.optimization.divide_conquer | 分治DP优化 | external_b2 | 2.18 | yellow | high |
| 28 | cand.dp.optimization.knuth | Knuth优化 | external_b2 | 2.18 | yellow | high |
| 29 | cand.dp.optimization.wqs_binary | WQS二分优化 | external_b2 | 2.18 | yellow | high |
| 30 | cand.graph.scc_dag.dag_reachability | 强连通分量 DAG：Dag Reachability | external_b1 | 2.21 | green | high |
| 31 | cand.graph.dynamic_connectivity.divide_and_conquer_on_time | 动态图连通性：Divide And Conquer On Time | external_b1 | 2.21 | green | high |
| 32 | cand.graph.scc_dag.dominating_components | 强连通分量 DAG：Dominating Components | external_b1 | 2.21 | green | high |
| 33 | cand.graph.dynamic_connectivity.edge_interval_model | 动态图连通性：Edge Interval Model | external_b1 | 2.21 | green | high |
| 34 | cand.graph.scc_dag.minimum_edges_to_strong | 强连通分量 DAG：Minimum Edges To Strong | external_b1 | 2.21 | green | high |
| 35 | cand.ds.bitset_linear_basis.rollback_linear_basis | 位集与线性基：Rollback Linear Basis | external_b1 | 3.13 | green | high |
| 36 | cand.ds.bitset_linear_basis.maximum_xor_query | 位集与线性基：Maximum Xor Query | external_b1 | 3.13 | green | high |
| 37 | cand.ds.bitset_linear_basis.rank_over_gf2 | 位集与线性基：Rank Over Gf2 | external_b1 | 3.13 | green | high |
| 38 | cand.ds.bitset_linear_basis.basis_with_deletion | 位集与线性基：Basis With Deletion | external_b1 | 3.13 | green | high |
| 39 | cand.ds.segment_tree_variants.split | 线段树变体：Split | external_b1 | 3.13 | yellow | high |
| 40 | cand.ds.dsu_advanced.parity | 高级并查集：Parity | external_b1 | 3.13 | yellow | high |

## 严格重复守卫检查

### candidate_id 重复
- **已合并/已使用检查**: 40 个候选已排除
- **排除候选列表**: 已在上方列出

### 名称重复检查

| 检查维度 | 结果 |
|---------|------|
| name 精确重复 | 0 排除 |
| en_name 重复 | 0 排除 |
| aliases 冲突 | 0 排除 |

### 近重复提示
- **DAG最长路DP** (cand.dp.dag.longest_path): 图谱中相似节点 ['dag']
- **状态压缩DP基础** (cand.dp.state_compression.basic): 图谱中相似节点 ['状态压缩']
- **子集枚举优化** (cand.dp.subset.enumeration): 图谱中相似节点 ['枚举', '子集枚举']
- **概率DP基础** (cand.dp.probability.basic): 图谱中相似节点 ['概率dp']
- **Manacher算法** (cand.string.manacher.algorithm): 图谱中相似节点 ['manacher']
- **Boyer-Moore算法** (cand.string.boyer_moore.algorithm): 图谱中相似节点 ['re']
- **KMP算法详解** (cand.string.string_matching.kmp): 图谱中相似节点 ['kmp']
- **Legendre符号** (cand.math.quadratic_residue.legendre_symbol): 图谱中相似节点 ['re']
- **扩展中国剩余定理** (cand.math.crt.extended): 图谱中相似节点 ['中国剩余定理', '扩展中国剩余定理 (excrt)']
- **欧拉函数应用** (cand.math.euler_function.applications): 图谱中相似节点 ['欧拉函数']
- **Burnside引理** (cand.math.group_theory.burnside): 图谱中相似节点 ['burnside']
- **分治DP优化** (cand.dp.optimization.divide_conquer): 图谱中相似节点 ['分治', 'dp优化']
- **强连通分量 DAG：Dag Reachability** (cand.graph.scc_dag.dag_reachability): 图谱中相似节点 ['连通分量', 'dag', 're']
- **动态图连通性：Divide And Conquer On Time** (cand.graph.dynamic_connectivity.divide_and_conquer_on_time): 图谱中相似节点 ['连通性']
- **强连通分量 DAG：Dominating Components** (cand.graph.scc_dag.dominating_components): 图谱中相似节点 ['连通分量', 'dag']
- **动态图连通性：Edge Interval Model** (cand.graph.dynamic_connectivity.edge_interval_model): 图谱中相似节点 ['int', '连通性']
- **强连通分量 DAG：Minimum Edges To Strong** (cand.graph.scc_dag.minimum_edges_to_strong): 图谱中相似节点 ['连通分量', 'dag']
- **位集与线性基：Rollback Linear Basis** (cand.ds.bitset_linear_basis.rollback_linear_basis): 图谱中相似节点 ['线性基']
- **位集与线性基：Maximum Xor Query** (cand.ds.bitset_linear_basis.maximum_xor_query): 图谱中相似节点 ['线性基']
- **位集与线性基：Rank Over Gf2** (cand.ds.bitset_linear_basis.rank_over_gf2): 图谱中相似节点 ['线性基']
- **位集与线性基：Basis With Deletion** (cand.ds.bitset_linear_basis.basis_with_deletion): 图谱中相似节点 ['线性基']
- **线段树变体：Split** (cand.ds.segment_tree_variants.split): 图谱中相似节点 ['线段树', '线段']

## 风险分析

| 检查项 | 结果 |
|--------|------|
| high_risk 候选 | 0 |
| manual_review 候选 | 0 |
| 需要新 section | 否 |
| 候选依赖环 | 否 |
| dependency_cleanup 需要 | 是 |
| dependency_mapping_risk | 11 个 |

## 综合建议

| 项目 | 建议 |
|------|------|
| 推荐操作 | **ready_for_1号线程_merge_full40** |
| 推荐合并数 | **40** |
| 是否需要 dependency cleanup | 是 - 2.21/3.13 候选可能需检查依赖 |
| 主图谱是否修改 | **否** |
| 是否生成正式 Batch3 | 否（等待 1号合并） |

---

*本报告仅做静态计划和动态预审。不合并。不修改主图谱。*
