# Stage3F Batch1 Added Items Review 模板

## 基本信息

- **批次**: Stage3F Batch1
- **预计新增节点数**: 20
- **预计 item_count**: 1641 → **1661**
- **涉及 sections**:

| Section ID | Section 名称 | 候选数 |
|-----------|-------------|--------|
| 2.8 | 动态规划 | 9 |
| 3.13 | 高级数据结构扩展 | 4 |
| 3.8 | 字符串结构 | 3 |
| 2.18 | 综合高级技巧专题 | 1 |
| 2.17 | 线性代数与插值专题 | 1 |
| 4.3 | 计数与组合 | 1 |
| 4.9 | 高级数学与群论 | 1 |

- **主图谱状态**: 未修改（等待 1号线程 Merge）

---

## 一、候选全表

### 1.1 动态规划系列 (2.8, 9 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 1 | cand.dp.digit.complex | 复杂数位DP | green | external_b2 |
| 2 | cand.dp.tree.rerooting | 换根DP | green | external_b2 |
| 3 | cand.dp.profile.basic | 轮廓DP基础 | green | external_b2 |
| 4 | cand.dp.profile.plug | 插头DP基础 | green | external_b2 |
| 5 | cand.dp.digit.basic | 数位DP基础 | yellow | external_b2 |
| 6 | cand.dp.tree.basic | 树DP基础 | yellow | external_b2 |
| 7 | cand.dp.tree.diameter | 树的直径DP | yellow | external_b2 |
| 8 | cand.dp.tree.centroid | 树的重心DP | yellow | external_b2 |
| 9 | cand.dp.dag.topological | 拓扑排序DP | yellow | external_b2 |

### 1.2 数据结构系列 (3.13, 4 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 10 | cand.ds.multidimensional.dominance_counting | Multidimensional: Dominance Counting | green | carry_over |
| 11 | cand.ds.merge_sort_tree.memory_optimization | Merge Sort Tree: Memory Optimization | green | reserve_pool |
| 12 | cand.ds.merge_sort_tree.offline_inversion | Merge Sort Tree: Offline Inversion | green | reserve_pool |
| 13 | cand.ds.merge_sort_tree.persistent_variant | Merge Sort Tree: Persistent Variant | green | reserve_pool |

### 1.3 字符串结构系列 (3.8, 3 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 14 | cand.string.suffix_array.sa_is | 后缀数组SA-IS算法 | green | external_b2 |
| 15 | cand.string.generalized_sam.construction | 广义SAM构建 | green | external_b2 |
| 16 | cand.string.suffix_tree.ukkonen | 后缀树Ukkonen算法 | green | external_b2 |

### 1.4 DP 优化系列 (2.18, 1 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 17 | cand.dp.optimization.slope.advanced | 斜率优化高级 | green | external_b2 |

### 1.5 线性代数系列 (2.17, 1 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 18 | cand.math.polynomial.berlekamp_massey | Berlekamp-Massey算法 | green | external_b2 |

### 1.6 组合数学系列 (4.3, 1 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 19 | cand.math.combinatorial.exlucas | 扩展Lucas定理 | green | external_b2 |

### 1.7 高级数学系列 (4.9, 1 个)

| # | candidate_id | 名称 | 动态预审 Risk | 来源 |
|---|-------------|------|--------------|------|
| 20 | cand.math.sieve.min_25 | Min_25筛 | green | external_b2 |

---

## 二、系列专项复查点

### 2.1 数位DP / 树DP / 轮廓DP / 插头DP (2.8)

| candidate_id | 动态预审近重复提示 | 复查重点 |
|-------------|-----------------|---------|
| cand.dp.digit.basic | 已有"数位DP" | 数位DP基础 vs 已有数位DP —— 是基础/进阶关系还是完全重复？如果是对数位DP的详细介绍而非简单变体，可保留。标注区分度说明。 |
| cand.dp.digit.complex | — | 复杂数位DP作为数位DP的高级扩展，与基础的区分度是否明确？ |
| cand.dp.tree.basic | — | 树DP基础与已有树形DP（如有）的关系。如果是第2个介绍层级，需说明区分。 |
| cand.dp.tree.diameter | 已有"树的直径" | 树的直径DP vs 树的直径 —— 树的直径可能是静态定义，DP版是求解方法。需确认已有节点是否包含DP解法。 |
| cand.dp.tree.centroid | 已有"树的重心" | 树的重心DP vs 树的重心 —— 同上。确认已有节点是否包含重心DP求解。 |
| cand.dp.tree.rerooting | — | 换根DP是树DP经典技巧，在竞赛中有独立教育价值。确认与已有树DP节点的依赖关系。 |
| cand.dp.profile.basic | — | 轮廓DP基础是状态压缩DP的扩展，2.8中是否有类似节点？需检查是否与已有状压DP节点重叠。 |
| cand.dp.profile.plug | — | 插头DP是轮廓DP的经典应用，同上检查重叠。 |
| cand.dp.dag.topological | 已有"拓扑排序" | 拓扑排序DP vs 拓扑排序 —— 拓扑排序本身是DAG排序算法，DP是DAG上的递推求解。区分明确。 |

### 2.2 Merge Sort Tree 变体 (3.13)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.ds.merge_sort_tree.memory_optimization | Merge Sort Tree 的内存优化变体。与已有 3.13.179 (2d Dominance) 的关系：是同一数据结构的不同方面，还是完全独立的方法？ |
| cand.ds.merge_sort_tree.offline_inversion | 离线求逆序数应用。Merge Sort Tree 的典型应用场景。 |
| cand.ds.merge_sort_tree.persistent_variant | 可持久化变体。与 3.13.9 (Persistent Array) 的关系？是否属于可持久化系列的自然扩展？ |

**过度拆分风险**: 低（各变体聚焦不同维度：内存/应用/可持久化）
**建议**: 全部降为 C，implementation_variant 或 application_case

### 2.3 Dominance Counting (3.13)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.ds.multidimensional.dominance_counting | Dominance Counting 是多维偏序计数问题的统称。建议检查：(1)是否更适合作为 problem_pattern（计数模式）而非独立知识节点？(2)与 CDQ 分治（3.13.181）的关系：CDQ 是解法，Dominance Counting 是问题定义？(3)如果保留为独立节点，建议 item_type = modeling_pattern。 |

### 2.4 后缀数组 SA-IS / 广义 SAM / 后缀树 Ukkonen (3.8)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.string.suffix_array.sa_is | SA-IS 是后缀数组的线性时间构造算法。已有"后缀数组"节点（可能在 2.10？），SA-IS 是构造算法的具体实现变体。确认 (1) 已有后缀数组节点是否包含 SA-IS；(2) SA-IS 作为具体实现变体的教育价值。 |
| cand.string.generalized_sam.construction | 广义 SAM 构建是多串场景下 SAM 的扩展。已有 SAM 节点（可能在 3.8？），广义 SAM 是重要扩展。确认与 SAM 的依赖关系清晰。 |
| cand.string.suffix_tree.ukkonen | Ukkonen 算法是后缀树的线性时间在线构建算法。后缀树是高级字符串结构，Ukkonen 算法是其经典构建方法。 |

### 2.5 斜率优化高级 (2.18)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.dp.optimization.slope.advanced | 斜率优化高级。2.18 是综合高级技巧专题。确认与 2.8 动态规划的区别：2.18 聚焦优化技巧本身，而 2.8 聚焦 DP 问题分类。 |

### 2.6 Berlekamp-Massey 算法 (2.17)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.math.polynomial.berlekamp_massey | BM 算法是线性递推的最小多项式求解算法。在 2.17 线性代数中是合理的。item_type 建议为 theorem_or_property 或 implementation_variant。 |

### 2.7 扩展 Lucas 定理 (4.3)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.math.combinatorial.exlucas | 扩展 Lucas 定理 vs 已有 Lucas —— 已有"Lucas"节点，扩展版处理模数为非素数的情况。区分明确，需确保 direct_pre 包含 Lucas 节点。 |

### 2.8 Min_25 筛 (4.9)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.math.sieve.min_25 | Min_25 筛是高级数论筛法，4.9 高级数学与群论是合理位置。确认：(1) 与已有杜教筛(如在4.9中)的依赖关系；(2) 竞赛中出现频率虽高但实现复杂度大，需确认 visibility 设置为 expert。 |

---

## 三、过度拆分风险判断

| 系列 | 数量 | 风险 | 建议 |
|------|------|------|------|
| 数位DP（基础+复杂） | 2 | 🟢 low | 基础+进阶，层次分明，无过度拆分 |
| 树DP（基础+直径+重心+换根） | 4 | 🟡 medium | 4个变体覆盖不同场景，建议保留3~4个（检查树DP基础是否与已有节点重叠） |
| 轮廓DP（基础+插头） | 2 | 🟢 low | 基础+应用，层次清楚 |
| Merge Sort Tree 变体 | 3 | 🟢 low | 内存/应用/可持久化，维度不同 |
| 字符串结构（SA-IS+SAM+后缀树） | 3 | 🟢 low | 三个独立的高级字符串结构，无重叠 |
| DP 优化/线性代数/组合/高级数学 | 各1 | 🟢 low | 独立主题，无问题 |

---

## 四、预期质量参考

| 等级 | 预期数量 | 说明 |
|------|---------|------|
| A | 0~2 | 极少数可能有 independent core value |
| B | 3~6 | 核心概念或需要专家复核的候选 |
| C | 14~17 | 明确的 implementation_variant，可降级 |
| theorem_or_property | 1~3 | Berlekamp-Massey / Dominance Counting 可能更适合此类型 |

---

## 五、Review 输出文件建议

| 文件 | 说明 |
|------|------|
| **data/stage3f_batch1_added_items_review.json** | 逐节点 Review 结论（approve / C / B） |
| **docs/stage3f_batch1_added_items_review_report.md** | Review 完整报告 |
| **data/stage3f_batch1_review_status_patch_preview.json** | review_status 补丁预览（B→C 降级 + 清除 need_manual_review） |
| **data/stage3f_batch1_dependency_fix_candidates.json** | 依赖修复候选（预期空，所有 direct_pre 均为 item id） |
| **data/stage3f_batch1_problem_pattern_sync_candidates.json** | 建议同步到 problem_patterns 的候选（预期 1~3 个：Dominance Counting / BM / Min_25） |
| **data/stage3f_batch1_merge_or_collapse_candidates.json** | 建议合并/折叠的候选（预期 0~1 个） |

---

## 六、Review 操作步骤

1. 等待 1号线程完成 Merge
2. 确认 item_count = 1661，section_count = 65
3. 读取 `stage3f_batch1_candidate_to_item_id_mapping.json`（待生成）
4. 读取 `stage3f_batch1_added_items_summary.json`（待生成）
5. 逐个复查 20 个新增节点，使用上方检查维度
6. 生成 6 个输出文件
7. 运行 validate-only 确认主图谱状态

---

*本模板不修改主图谱，不执行 Review。等待 Merge 成功后基于真实 item_id 执行。*
