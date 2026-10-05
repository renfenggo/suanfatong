# Stage3F Batch3 Full40 Added Items Review 模板

## 基本信息

- **批次**: Stage3F Batch3 Full40
- **预计新增节点数**: **40**
- **预计 item_count**: 1677 → **1717**
- **涉及 sections**:

| Section ID | Section 名称 | 候选数 |
|-----------|-------------|--------|
| 2.8 | 动态规划 | 8 |
| 2.10 | 字符串算法 | 5 |
| 2.17 | 线性代数与插值 | 2 |
| 2.18 | 综合高级技巧 | 4 |
| 2.21 | 高级图论扩展 | 5 |
| 3.8 | 字符串结构 | 2 |
| 3.13 | 高级数据结构扩展 | 6 |
| 4.1 | 整数与数论基础 | 4 |
| 4.9 | 高级数学与群论 | 4 |

- **Dependency Cleanup 已完成**: 11 候选依赖已映射为 item id，dependency_cleanup_required = false
- **主图谱状态**: 未修改（等待 1号线程 Merge）

---

## 一、候选全表

### 1.1 DP 高级专题 (2.8, 8 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 1 | cand.dp.dag.longest_path | DAG最长路DP | yellow | external_b2 |
| 2 | cand.dp.state_compression.basic | 状态压缩DP基础 | yellow | external_b2 |
| 3 | cand.dp.state_compression.traveling | 旅行商问题DP | yellow | external_b2 |
| 4 | cand.dp.subset.basic | 子集DP基础 | yellow | external_b2 |
| 5 | cand.dp.subset.enumeration | 子集枚举优化 | yellow | external_b2 |
| 6 | cand.dp.automaton.basic | 自动机DP基础 | yellow | external_b2 |
| 7 | cand.dp.automaton.matrix | 自动机矩阵DP | yellow | external_b2 |
| 8 | cand.dp.probability.basic | 概率DP基础 | yellow | external_b2 |

### 1.2 字符串算法 (2.10, 5 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 9 | cand.string.border_tree.structure | Border树结构 | yellow | external_b2 |
| 10 | cand.string.manacher.algorithm | Manacher算法 | yellow | external_b2 |
| 11 | cand.string.boyer_moore.algorithm | Boyer-Moore算法 | yellow | external_b2 |
| 12 | cand.string.rabin_karp.algorithm | Rabin-Karp算法 | yellow | external_b2 |
| 13 | cand.string.string_matching.kmp | KMP算法详解 | yellow | external_b2 |

### 1.3 数论基础 (4.1, 4 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 14 | cand.math.quadratic_residue.legendre_symbol | Legendre符号 | yellow | external_b2 |
| 15 | cand.math.quadratic_residue.tonelli_shanks | Tonelli-Shanks算法 | yellow | external_b2 |
| 16 | cand.math.crt.extended | 扩展中国剩余定理 | yellow | external_b2 |
| 17 | cand.math.crt.garner | Garner算法 | yellow | external_b2 |

### 1.4 高级数学 (4.9, 4 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 18 | cand.math.euler_function.applications | 欧拉函数应用 | yellow | external_b2 |
| 19 | cand.math.sieve.du_jiao | 杜教筛 | yellow | external_b2 |
| 20 | cand.math.group_theory.burnside | Burnside引理 | yellow | external_b2 |
| 21 | cand.math.group_theory.polya | Polya计数定理 | yellow | external_b2 |

### 1.5 线性代数与插值 (2.17, 2 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 22 | cand.math.polynomial.fwt | 快速沃尔什变换 | yellow | external_b2 |
| 23 | cand.math.polynomial.subset_convolution | 子集卷积 | yellow | external_b2 |

### 1.6 DP 优化技巧 (2.18, 4 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 24 | cand.dp.optimization.slope.basic | 斜率优化基础 | yellow | external_b2 |
| 25 | cand.dp.optimization.divide_conquer | 分治DP优化 | yellow | external_b2 |
| 26 | cand.dp.optimization.knuth | Knuth优化 | yellow | external_b2 |
| 27 | cand.dp.optimization.wqs_binary | WQS二分优化 | yellow | external_b2 |

### 1.7 高级图论扩展 (2.21, 5 个) — Dependency Cleanup

| # | candidate_id | 名称 | Risk | Source | cleaned_direct_pre |
|---|-------------|------|------|--------|-------------------|
| 28 | cand.graph.scc_dag.dag_reachability | 强连通分量 DAG：Dag Reachability | green | external_b1 | 2.15.1, 2.9.7 |
| 29 | cand.graph.dynamic_connectivity.divide_and_conquer_on_time | 动态图连通性：Divide And Conquer On Time | green | external_b1 | 2.1.34, 3.4.1 |
| 30 | cand.graph.scc_dag.dominating_components | 强连通分量 DAG：Dominating Components | green | external_b1 | 2.15.1, 2.15.10 |
| 31 | cand.graph.dynamic_connectivity.edge_interval_model | 动态图连通性：Edge Interval Model | yellow | external_b1 | 2.21.27, 3.4.1 |
| 32 | cand.graph.scc_dag.minimum_edges_to_strong | 强连通分量 DAG：Minimum Edges To Strong | yellow | external_b1 | 2.15.1, 2.15.10 |

### 1.8 高级数据结构扩展 (3.13, 6 个) — Dependency Cleanup

| # | candidate_id | 名称 | Risk | Source | cleaned_direct_pre |
|---|-------------|------|------|--------|-------------------|
| 33 | cand.ds.bitset_linear_basis.rollback_linear_basis | 位集与线性基：Rollback Linear Basis | green | external_b1 | 2.18.3, 3.13.49 |
| 34 | cand.ds.bitset_linear_basis.maximum_xor_query | 位集与线性基：Maximum Xor Query | green | external_b1 | 2.18.3, 2.17.6 |
| 35 | cand.ds.bitset_linear_basis.rank_over_gf2 | 位集与线性基：Rank Over Gf2 | green | external_b1 | 2.18.3, 2.17.8 |
| 36 | cand.ds.bitset_linear_basis.basis_with_deletion | 位集与线性基：Basis With Deletion | green | external_b1 | 2.18.3, 3.13.49 |
| 37 | cand.ds.segment_tree_variants.split | 线段树变体：Split | yellow | external_b1 | 3.7.2 |
| 38 | cand.ds.dsu_advanced.parity | 高级并查集：Parity | yellow | external_b1 | 3.4.1, 3.4.4 |

### 1.9 字符串结构 (3.8, 2 个)

| # | candidate_id | 名称 | Risk | Source |
|---|-------------|------|------|--------|
| 39 | cand.string.lyndon_decomposition.basic | Lyndon分解基础 | yellow | external_b2 |
| 40 | cand.string.runs_repetitions.basic | Runs重复子串分析 | yellow | external_b2 |

---

## 二、系列专项复查点

### 2.1 DP 高级专题 (2.8)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 1 | DAG最长路DP | vs 已有 2.8.14 "DAG 上 DP"：是否已有节点覆盖最长路内容 |
| 2 | 状态压缩DP基础 | vs 已有"状态压缩"相关节点：检查是否为重复 |
| 3 | 旅行商问题DP | 典型TSP问题DP，建议 application_case，注意 direct_pre 应指向状态压缩 |
| 4 | 子集DP基础 | direct_pre 应指向基础 DP 概念节点 |
| 5 | 子集枚举优化 | 与子集DP基础的区分：基础 vs 优化技巧，建议明确层次关系 |
| 6 | 自动机DP基础 | direct_pre 应指向自动机/字符串匹配相关节点 |
| 7 | 自动机矩阵DP | 与自动机DP基础的区别：矩阵加速版本，建议 direct_pre 指向自动机DP基础 |
| 8 | 概率DP基础 | 确认图谱中概率DP相关节点，建议降 C |

### 2.2 字符串算法 (2.10) — 近重复高风险

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 9 | ★ Border树结构 | **近重复高风险**：vs 已有 2.10.16 "KMP 的失配树"——Border树可能与失配树同一概念 |
| 10 | Manacher算法 | 独立算法，图谱中尚无专门 Manacher 节点 |
| 11 | Boyer-Moore算法 | 经典字符串匹配算法，图谱中尚无 |
| 12 | Rabin-Karp算法 | 滚动哈希匹配，图谱中尚无 |
| 13 | ★★ KMP算法详解 | **极高重复风险**：vs 已有 2.10.2 "KMP"——"详解"版本是否与基础KMP重叠严重 |

### 2.3 数论基础 (4.1)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 14 | Legendre符号 | 二次剩余的基础符号，item_type = theorem_or_property |
| 15 | Tonelli-Shanks算法 | 二次剩余求解算法，direct_pre 应指向 Legendre符号 |
| 16 | 扩展中国剩余定理 | vs 已有 CRT 节点：确认是否有独立节点 |
| 17 | Garner算法 | Garner vs 扩展CRT：两个算法解同一问题（CRT），但适用场景不同 |

### 2.4 高级数学 (4.9)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 18 | 欧拉函数应用 | vs 已有"欧拉函数"节点：确认属于应用扩展而非重复 |
| 19 | 杜教筛 | 高级数论筛法，确认与已有"筛法"节点的关系 |
| 20 | Burnside引理 | 群论在组合计数中的应用，图谱中尚无 |
| 21 | Polya计数定理 | Burnside引理的扩展，direct_pre 应指向 Burnside |

### 2.5 线性代数与插值 (2.17)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 22 | 快速沃尔什变换(FWT) | 独立变换算法，图谱中尚无，建议 core_concept |
| 23 | 子集卷积 | FWT的应用扩展，direct_pre 指向 FWT |

### 2.6 DP 优化技巧 (2.18)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 24 | ★ 斜率优化基础 | **近重复风险**：vs Batch1 已有 2.18.9 "斜率优化高级"——基础应与高级互补 |
| 25 | 分治DP优化 | 独立优化技巧，确认图谱中尚无 |
| 26 | Knuth优化 | 四边形不等式优化，确认图谱中尚无 |
| 27 | WQS二分优化 | 带权二分优化技巧，确认图谱中尚无 |

### 2.7 高级图论扩展 (2.21) — Dependency Cleanup 验证

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 28 | SCC DAG: Dag Reachability | cleaned_direct_pre=2.15.1+2.9.7 rel=2.21.32 ✓ |
| 29 | 动态连通性: Divide And Conquer On Time | cleaned_direct_pre=2.1.34+3.4.1 rel=2.21.36 ✓ |
| 30 | SCC DAG: Dominating Components | cleaned_direct_pre=2.15.1+2.15.10 rel=2.21.32 ✓ |
| 31 | 动态连通性: Edge Interval Model | cleaned_direct_pre=2.21.27+3.4.1 rel=2.21.36 ✓ |
| 32 | SCC DAG: Minimum Edges To Strong | cleaned_direct_pre=2.15.1+2.15.10 rel=2.21.32+2.21.49 ✓ |

**系列过度拆分风险**: SCC DAG 3 个节点（28/30/32）+ 动态连通性 2 个节点（29/31）— 5 个节点在 2.21 是否过多？每个是否有正交的教育目标？

### 2.8 高级数据结构扩展 (3.13) — Dependency Cleanup 验证

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 33 | 线性基: Rollback Linear Basis | cleaned_direct_pre=2.18.3+3.13.49 rel=3.13.25 ✓ |
| 34 | 线性基: Maximum Xor Query | cleaned_direct_pre=2.18.3+2.17.6 rel=3.13.39 ✓ |
| 35 | 线性基: Rank Over Gf2 | cleaned_direct_pre=2.18.3+2.17.8 ✓ |
| 36 | 线性基: Basis With Deletion | cleaned_direct_pre=2.18.3+3.13.49 ✓ |
| 37 | 线段树变体: Split | cleaned_direct_pre=3.7.2 rel=3.7.22 — **需检查 vs 3.7.22 "线段树分裂" 是否重复** |
| 38 | 高级并查集: Parity | cleaned_direct_pre=3.4.1+3.4.4 — 与带权并查集边界清晰 |

**系列过度拆分风险**: 线性基 4 个节点（33/34/35/36）是否过度拆分？每个方向正交（回滚/异或查询/秩/删除）有一定独立价值但需确认。

### 2.9 字符串结构 (3.8)

| ID | candidate | 复查重点 |
|----|-----------|---------|
| 39 | Lyndon分解基础 | 独立字符串主题，图谱中尚无 |
| 40 | Runs重复子串分析 | 高级字符串分析，确认 direct_pre 应指向相关字符串节点 |

---

## 三、Dependency Cleanup 验证

| 检查项 | 预期 | 状态 |
|--------|------|------|
| 11 候选的 cleaned_direct_pre 均为有效 item id | ✅ | 待 Merge 后确认 |
| 不含 section id 引用 | ✅ | 待确认 |
| 无 dangling refs | ✅ | 待确认 |
| 无依赖环形成 | ✅ | 待确认 |

---

## 四、过度拆分风险判断

| 系列 | 数量 | 风险 | 建议 |
|------|------|------|------|
| DP 高级专题 (2.8) | 8 | 🟡 medium | DAG最长路DP/Automaton DP/子集DP 三个子领域，每个有正交价值，但整体8个是否过多 |
| 字符串算法 (2.10) | 5 | 🟡 medium | KMP详解风险高，可能需排除 |
| 数论基础 (4.1) | 4 | 🟢 low | 独立主题（二次剩余/CRT/Garner） |
| 高级数学 (4.9) | 4 | 🟢 low | 独立主题（欧拉/筛法/群论） |
| DP 优化 (2.18) | 4 | 🟢 low | 4种不同优化技巧，正交 |
| **高级图论 (2.21)** | **5** | **🟡 medium** | **SCC DAG 3个 + 动态连通 2个 — 每个有正交价值但需确认不重复** |
| **高级数据结构 (3.13)** | **6** | **🟡 medium** | **线性基 4个 — 方向正交但需确认不过度拆分** |
| 字符串结构 (3.8) | 2 | 🟢 low | 独立主题 |
| 线性代数 (2.17) | 2 | 🟢 low | FWT + 子集卷积，有依赖关系 |

---

## 五、重点近重复风险处理方案

| 候选 | 已有节点 | 风险 | 处理预案 |
|------|---------|------|---------|
| **KMP算法详解** (2.10) | 2.10.2 "KMP" | 🔴 **high** | 如果内容重叠严重 -> needs_merge_or_collapse |
| **Border树结构** (2.10) | 2.10.16 "KMP 的失配树" | 🔴 **high** | 如果与失配树同概念 -> needs_merge_or_collapse |
| **斜率优化基础** (2.18) | 2.18.9 "斜率优化高级" | 🟡 medium | 基础vs高级互补，大概率可保留 |
| **线段树变体: Split** (3.13) | 3.7.22 "线段树分裂" | 🟡 medium | 变体细分 vs 已有基础，需确认边界 |

---

## 六、预期质量参考

| 等级 | 预期数量 | 说明 |
|------|---------|------|
| A | 0 | 极少有 independent core value |
| B | 2~4 | 杜教筛/WQS/Manacher 等独立算法可能保留 B |
| C | 30~34 | 明确变体/应用型，可降级 |
| needs_merge_or_collapse | 2~3 | KMP详解、Border树结构 等高风险重复 |
| move_to_problem_patterns | 1~2 | 欧拉函数应用可能更适合 patterns |

---

## 七、Review 输出文件建议

| 文件 | 说明 |
|------|------|
| data/stage3f_batch3_full40_added_items_review.json | 逐节点 Review 结论（40 个） |
| docs/stage3f_batch3_full40_added_items_review_report.md | Review 完整报告 |
| data/stage3f_batch3_full40_review_status_patch_preview.json | review_status 补丁预览 |
| data/stage3f_batch3_full40_dependency_fix_candidates.json | 依赖修复候选（预期 0） |
| data/stage3f_batch3_full40_problem_pattern_sync_candidates.json | 建议同步到 problem_patterns 的候选 |
| data/stage3f_batch3_full40_merge_or_collapse_candidates.json | 建议合并/折叠的候选 |

---

## 八、Review 操作步骤

1. 等待 1号线程完成 Merge（预计 1677→1717）
2. 确认 item_count = 1717，section_count = 65
3. 读取 `stage3f_batch3_full40_candidate_to_item_id_mapping.json`（待生成）
4. 读取 `stage3f_batch3_full40_added_items_summary.json`（待生成）
5. 逐个复查 40 个新增节点，使用上方检查维度
6. **重点复查**：
   - Dependency Cleanup 11 候选的 cleaned_direct_pre 是否与 Merge 后一致
   - KMP详解 vs 已有 KMP
   - Border树 vs 失配树
   - 斜率优化基础 vs 高级
   - 线性基 4 个节点是否过度拆分
   - SCC DAG 3 个节点是否过度拆分
7. 生成 6 个输出文件
8. 运行 validate-only 确认主图谱状态

---

*本模板不修改主图谱，不执行 Review。等待 Merge 成功后基于真实 item_id 执行。*
