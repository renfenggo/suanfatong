# Stage3F Batch2 Added Items Review 模板

## 基本信息

- **批次**: Stage3F Batch2
- **预计新增节点数**: 20
- **预计 item_count**: 1661 → **1681**
- **涉及 sections**:

| Section ID | Section 名称 | 候选数 |
|-----------|-------------|--------|
| 2.10 | 字符串算法 | 6 |
| 4.1 | 整数与数论基础 | 5 |
| 3.8 | 字符串结构 | 3 |
| 4.3 | 计数与组合 | 2 |
| 4.9 | 高级数学与群论 | 2 |
| 2.18 | 综合高级技巧专题 | 2 |

- **主图谱状态**: 未修改（等待 1号线程 Merge）

---

## 一、候选全表

### 1.1 字符串算法系列 (2.10, 6 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 1 | cand.string.z_algorithm.basic | Z算法基础 | yellow |
| 2 | cand.string.z_algorithm.pattern_matching | Z算法模式匹配应用 | yellow |
| 3 | cand.string.ex_kmp.basic | 扩展KMP算法基础 | yellow |
| 4 | cand.string.kmp_automaton.basic | KMP自动机基础 | yellow |
| 5 | cand.string.ac_automaton.applications | AC自动机高级应用 | yellow |
| 6 | cand.string.ac_failure_tree.analysis | AC自动机失败树分析 | yellow |

### 1.2 数论基础系列 (4.1, 5 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 7 | cand.math.prime_testing.miller_rabin | Miller-Rabin素数测试 | yellow |
| 8 | cand.math.prime_factorization.pollard_rho | Pollard Rho分解 | yellow |
| 9 | cand.math.primitive_root.basic | 原根基础 | yellow |
| 10 | cand.math.discrete_log.bsgs | BSGS离散对数 | yellow |
| 11 | cand.math.discrete_log.exbsgs | 扩展BSGS | yellow |

### 1.3 字符串结构系列 (3.8, 3 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 12 | cand.string.lcp_rmq.optimization | LCP RMQ优化 | yellow |
| 13 | cand.string.sam_parent_tree.structure | SAM父树结构 | yellow |
| 14 | cand.string.eertree.construction | 回文树Eertree构建 | yellow |

### 1.4 组合数学系列 (4.3, 2 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 15 | cand.math.combinatorial.lucas | Lucas定理 | yellow |
| 16 | cand.math.combinatorial.catalan | Catalan数 | yellow |

### 1.5 高级数学系列 (4.9, 2 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 17 | cand.math.dirichlet_convolution.basic | 狄利克雷卷积基础 | yellow |
| 18 | cand.math.mobius_inversion.applications | 莫比乌斯反演应用 | yellow |

### 1.6 DP 优化系列 (2.18, 2 个)

| # | candidate_id | 名称 | 动态预审 Risk |
|---|-------------|------|--------------|
| 19 | cand.dp.optimization.monotone_queue | 单调队列优化 | yellow |
| 20 | cand.dp.optimization.monotone_queue_sliding | 滑动窗口DP | yellow |

---

## 二、系列专项复查点

### 2.1 Z算法 / 扩展KMP / KMP自动机 (2.10)

| candidate_id | 动态预审近重复提示 | 复查重点 |
|-------------|-----------------|---------|
| cand.string.z_algorithm.basic | — | Z算法是字符串匹配的独立算法，与KMP功能等价但原理不同。确认与已有"KMP"节点的关系：两者是并列关系而非包含关系。 |
| cand.string.z_algorithm.pattern_matching | — | Z算法的模式匹配应用。作为Z算法的典型应用场景，确认 direct_pre 指向 Z算法基础。 |
| cand.string.ex_kmp.basic | — | 扩展KMP（Z函数）是字符串匹配的另一个经典算法。确认与已有KMP节点的关系。 |
| cand.string.kmp_automaton.basic | 已有"KMP" | KMP自动机是KMP算法的自动机形式化。vs 已有"KMP"节点——如果已有KMP已包含自动机构造，则需标注区分。 |

### 2.2 AC自动机高级应用 / 失败树分析 (2.10)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.string.ac_automaton.applications | AC自动机的高级应用（多模式串匹配的各种扩展场景）。确认与已有AC自动机节点的依赖关系：属于高级应用而非重复基础。direct_pre 应指向已有AC自动机节点。 |
| cand.string.ac_failure_tree.analysis | AC自动机的失败（fail）树结构分析。失败树是AC自动机的重要理论结构，构建后缀链接的树形关系。确认其独立教育价值。 |

### 2.3 Miller-Rabin / Pollard Rho / 原根 / BSGS (4.1)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.math.prime_testing.miller_rabin | Miller-Rabin概率性素数测试。是数论基础中的核心算法。建议保留 B 级（核心概念），确认与已有素数判定节点的关系。 |
| cand.math.prime_factorization.pollard_rho | Pollard Rho 大数分解算法。与Miller-Rabin配合使用。确认两者 direct_pre 关系清晰。 |
| cand.math.primitive_root.basic | 原根是数论中模运算的重要概念。属于定理性概念。 |
| cand.math.discrete_log.bsgs | BSGS（Baby Step Giant Step）离散对数求解算法。是数论核心算法。 |
| cand.math.discrete_log.exbsgs | 扩展BSGS，处理模数不互质的情况。与BSGS的区分是功能和适用条件不同，而非重复。确认 direct_pre 指向 BSGS。 |

### 2.4 LCP RMQ / SAM父树 / Eertree (3.8)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.string.lcp_rmq.optimization | LCP（最长公共前缀）的RMQ优化。是后缀数组的配套技术。确认与已有后缀数组（3.8.3）的依赖关系。 |
| cand.string.sam_parent_tree.structure | SAM（后缀自动机）的父（Parent）树结构。是SAM的重要理论结构。确认与已有SAM节点（3.8.4）的依赖关系。 |
| cand.string.eertree.construction | 回文树（Eertree/Palindromic Tree）的构建算法。是3.8字符串结构中独立的高级结构。确认与已有字符串结构节点无重复。 |

### 2.5 Lucas定理 / Catalan数 (4.3)

| candidate_id | 动态预审近重复提示 | 复查重点 |
|-------------|-----------------|---------|
| cand.math.combinatorial.lucas | 已有"Lucas"、"扩展Lucas定理"（Batch1） | **近重复高风险**。已有"Lucas"节点（名称简写）和Batch1新增"扩展Lucas定理"(4.3.32)。需确认：(1)已有"Lucas"节点是否已包含Lucas定理全部内容；(2)新增vs已有的边界划分——推荐删除此候选或明确为"Lucas定理基础"并与已有节点标注区分。 |
| cand.math.combinatorial.catalan | — | Catalan数是组合数学的重要数列。确认与已有组合计数节点的关系：是否已有节点包含了Catalan数的介绍。 |

### 2.6 狄利克雷卷积 / 莫比乌斯反演 (4.9)

| candidate_id | 复查重点 |
|-------------|---------|
| cand.math.dirichlet_convolution.basic | 狄利克雷卷积是数论函数的基本运算。建议 item_type = theorem_or_property。 |
| cand.math.mobius_inversion.applications | 莫比乌斯反演应用。更适合 modeling_pattern 或 problem_pattern 类型。建议同步 problem_patterns 库。 |

### 2.7 单调队列优化 / 滑动窗口DP (2.18)

| candidate_id | 动态预审近重复提示 | 复查重点 |
|-------------|-----------------|---------|
| cand.dp.optimization.monotone_queue | 已有"单调队列"、"单调队列优化DP"、"单调队列优化多重背包" | **近重复高风险**。已有多个相关节点。需确认：(1) 已有"单调队列优化DP"是否已覆盖此主题；(2) 如果覆盖则建议合并/折叠，不新增。 |
| cand.dp.optimization.monotone_queue_sliding | 已有"滑动窗口" | 滑动窗口DP是滑动窗口的DP优化版本。确认与已有"滑动窗口"节点的区分。 |

---

## 三、过度拆分风险判断

| 系列 | 数量 | 风险 | 建议 |
|------|------|------|------|
| Z算法（基础+应用） | 2 | 🟢 low | 基础+应用，层次分明 |
| AC自动机（高级应用+失败树） | 2 | 🟢 low | 两个独立的高级扩展方向 |
| 数论（Miller-Rabin/Pollard Rho/原根/BSGS/扩展BSGS） | 5 | 🟡 medium | 5个独立主题，每个有独立教育价值，但需确认与已有数论节点的边界 |
| 字符串结构（LCP RMQ/SAM父树/Eertree） | 3 | 🟢 low | 三个独立不同的主题 |
| Lucas定理 / Catalan数 | 2 | 🟡 medium | Lucas有近重复风险 |
| 高级数学（狄利克雷卷积/莫反） | 2 | 🟢 low | 独立主题 |
| DP优化（单调队列/滑动窗口） | 2 | 🟡 medium | 单调队列有近重复风险 |

---

## 四、重点近重复风险处理方案

| 候选 | 已有节点 | 风险 | 处理预案 |
|------|---------|------|---------|
| **Lucas定理 (4.3)** | "Lucas" + "扩展Lucas定理" | 🔴 **high** | 如果已有"Lucas"已完整覆盖Lucas定理，则标记 needs_merge_or_collapse；如果只是简写，则保留并标注区分 |
| **单调队列优化 (2.18)** | "单调队列优化DP" | 🔴 **high** | 需确认已有节点范围。如果已有节点已含全部单调队列优化内容，则建议不新增 |
| KMP自动机基础 (2.10) | "KMP" | 🟡 medium | KMP自动机是KMP的形式化变体，可保留但需标注实现变体类型 |
| 滑动窗口DP (2.18) | "滑动窗口" | 🟡 medium | DP版本 vs 数据结构/算法版本，可区分 |
| Lucas定理 (4.3) | "扩展Lucas定理"(Batch1新增) | 🟡 medium | Lucas定理处理模素数，扩展Lucas处理模非素数，功能不同，区分明确 |

---

## 五、预期质量参考

| 等级 | 预期数量 | 说明 |
|------|---------|------|
| A | 0 | 极少有 independent core value |
| B | 2~5 | Miller-Rabin, Pollard Rho, BSGS 等数论核心算法可能保留 B |
| C | 15~18 | 明确的 implementation_variant / application_case，可降级 |
| theorem_or_property | 2~3 | 原根、Lucas定理、Catalan数、狄利克雷卷积 |

---

## 六、Review 输出文件建议

| 文件 | 说明 |
|------|------|
| **data/stage3f_batch2_added_items_review.json** | 逐节点 Review 结论（approve / C / B） |
| **docs/stage3f_batch2_added_items_review_report.md** | Review 完整报告 |
| **data/stage3f_batch2_review_status_patch_preview.json** | review_status 补丁预览（B→C 降级 + 清除 need_manual_review） |
| **data/stage3f_batch2_dependency_fix_candidates.json** | 依赖修复候选（预期空，所有 direct_pre 均为 item id） |
| **data/stage3f_batch2_problem_pattern_sync_candidates.json** | 建议同步到 problem_patterns 的候选（预期 1~2 个：莫比乌斯反演应用可能更适合） |
| **data/stage3f_batch2_merge_or_collapse_candidates.json** | 建议合并/折叠的候选（预期 1~2 个：Lucas定理 / 单调队列优化） |

---

## 七、Review 操作步骤

1. 等待 1号线程完成 Merge
2. 确认 item_count = 1681，section_count = 65
3. 读取 `stage3f_batch2_candidate_to_item_id_mapping.json`（待生成）
4. 读取 `stage3f_batch2_added_items_summary.json`（待生成）
5. 逐个复查 20 个新增节点，使用上方检查维度
6. 重点关注近重复风险：Lucas定理(4.3) 和 单调队列优化(2.18)
7. 生成 6 个输出文件
8. 运行 validate-only 确认主图谱状态

---

*本模板不修改主图谱，不执行 Review。等待 Merge 成功后基于真实 item_id 执行。*
