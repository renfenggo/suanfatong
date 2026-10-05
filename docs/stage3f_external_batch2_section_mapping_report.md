# Stage3F External Batch2 Section Mapping 报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T12:20:00.000Z
- **任务**: 对 External Batch2 的 83 个候选做 section 映射和风险标注
- **主图谱状态**: 未修改

## 1. 主图谱引用

| Section ID | Section 名称 | 分类 |
|-----------|-------------|------|
| 2.10 | 字符串算法 | 算法 |
| 2.8 | 动态规划 | 算法 |
| 2.17 | 线性代数与插值专题 | 算法 |
| 2.18 | 综合高级技巧专题 | 算法 |
| 2.21 | 高级图论扩展 | 算法 |
| 3.8 | 字符串结构 | 数据结构 |
| 3.13 | 高级数据结构扩展 | 数据结构 |
| 4.1 | 整数与数论基础 | 算法竞赛数学 |
| 4.3 | 计数与组合 | 算法竞赛数学 |
| 4.4 | 离散数学基础 | 算法竞赛数学 |
| 4.5 | 图与树的数学基础 | 算法竞赛数学 |
| 4.9 | 高级数学与群论 | 算法竞赛数学 |

## 2. 映射统计

| 指标 | 数量 |
|------|------|
| Batch2 总候选 | 83 |
| 成功映射 (high confidence) | 78 |
| 成功映射 (medium confidence) | 5 |
| 低 confidence | 0 |
| green 风险 | 11 |
| yellow 风险 | 65 |
| red 风险 (含重复) | 4 |
| 需要新 section | 0 |
| 疑似重复 | 4 |
| **建议进入 Stage3F Batch1** | **76** |

## 3. Section 映射分布

| Section ID | Section 名称 | 候选数 |
|-----------|-------------|--------|
| 2.10 | 字符串算法 | 15 |
| 2.17 | 线性代数与插值专题 | 4 |
| 2.18 | 综合高级技巧专题 | 7 |
| 2.8 | 动态规划 | 23 |
| 3.8 | 字符串结构 | 8 |
| 4.1 | 整数与数论基础 | 10 |
| 4.3 | 计数与组合 | 3 |
| 4.4 | 离散数学基础 | 4 |
| 4.5 | 图与树的数学基础 | 2 |
| 4.9 | 高级数学与群论 | 7 |

## 4. 映射策略说明

### 4.1 字符串算法 (cand.string.*: 23 个)

| 子类别 | 映射到 | confidence | 说明 |
|--------|--------|-----------|------|
| 后缀数组/后缀自动机/后缀树/回文树 | **3.8 字符串结构** | high | 高级字符串结构 |
| KMP/Z算法/扩展KMP/AC自动机 | **2.10 字符串算法** | high | 基础/中级字符串算法 |
| Manacher/Boyer-Moore/Rabin-Karp | **2.10 字符串算法** | high | 字符串匹配算法 |
| 字符串哈希/LCP RMQ | **2.10/3.8** | high | 辅助字符串技术 |
| Lyndon分解/Duval/Runs/Border Tree | **2.10 字符串算法** | high | 高级字符串分析 |

### 4.2 数学专题 (cand.math.*: 31 个)

| 子类别 | 映射到 | confidence | 说明 |
|--------|--------|-----------|------|
| Miller-Rabin/Pollard Rho/原根/BSGS | **4.1 整数与数论基础** | high | 经典数论算法 |
| CRT/扩展CRT/Garner | **4.1 整数与数论基础** | high | 数论与中国剩余定理 |
| 杜教筛/Min_25筛 | **4.9 高级数学与群论** | high | 高级数论技巧 |
| Lucas/扩展Lucas/Catalan | **4.3 计数与组合** | high | 组合数学 |
| 狄利克雷卷积/莫比乌斯反演 | **4.9 高级数学与群论** | high | 数论高级专题 |
| FWT/子集卷积/Lagrange/BM | **2.17 线性代数与插值专题** | high | 多项式与线性代数 |
| 线性递推/生成函数 | **4.4 离散数学基础** | medium | 递推关系 |
| Burnside/Polya | **4.9 高级数学与群论** | high | 群论与计数 |
| 矩阵树定理/GF(2)消元 | **4.5 图与树的数学基础** | high | 图论数学基础 |

### 4.3 DP 高级专题 (cand.dp.*: 29 个)

| 子类别 | 映射到 | confidence | 说明 |
|--------|--------|-----------|------|
| 数位DP/树DP/DAG DP | **2.8 动态规划** | high | 基础DP类别 |
| 状态压缩DP/子集DP | **2.8 动态规划** | high | 状态压缩类别 |
| 轮廓DP/插头DP | **2.8 动态规划** | high | 复杂DP类别 |
| 自动机DP/概率DP/博弈DP | **2.8 动态规划** | high | 特殊DP类别 |
| 单调队列/斜率优化/分治DP | **2.18 综合高级技巧专题** | high | DP优化技巧 |
| Knuth优化/WQS二分 | **2.18 综合高级技巧专题** | high | 高级DP优化 |
| 矩阵DP/矩阵快速幂 | **2.8 动态规划** | high | 矩阵加速DP |

## 5. 重复候选明细

| candidate_id | name | 重复原因 |
|-------------|------|---------|
| cand.math.crt.basic | 中国剩余定理 | 名称"中国剩余定理"已存在于主图谱 |
| cand.math.polynomial.lagrange | 拉格朗日插值 | 名称"拉格朗日插值"已存在于主图谱 |
| cand.math.generating_function.ordinary | 普通生成函数 | 名称"普通生成函数"已存在于主图谱 |
| cand.math.generating_function.exponential | 指数生成函数 | 名称"指数生成函数"已存在于主图谱 |

## 6. 建议进入 Stage3F Batch1 的候选 (前20)

| # | candidate_id | name | section | risk |
|---|-------------|------|---------|------|
| 1 | cand.string.z_algorithm.basic | Z算法基础 | 2.10 | yellow |
| 2 | cand.string.z_algorithm.pattern_matching | Z算法模式匹配应用 | 2.10 | yellow |
| 3 | cand.string.ex_kmp.basic | 扩展KMP算法基础 | 2.10 | yellow |
| 4 | cand.string.kmp_automaton.basic | KMP自动机基础 | 2.10 | yellow |
| 5 | cand.string.ac_automaton.applications | AC自动机高级应用 | 2.10 | yellow |
| 6 | cand.string.ac_failure_tree.analysis | AC自动机失败树分析 | 2.10 | yellow |
| 7 | cand.string.suffix_array.sa_is | 后缀数组SA-IS算法 | 3.8 | green |
| 8 | cand.string.lcp_rmq.optimization | LCP RMQ优化 | 3.8 | yellow |
| 9 | cand.string.generalized_sam.construction | 广义SAM构建 | 3.8 | green |
| 10 | cand.string.sam_parent_tree.structure | SAM父树结构 | 3.8 | yellow |
| 11 | cand.string.eertree.construction | 回文树Eertree构建 | 3.8 | yellow |
| 12 | cand.string.suffix_tree.ukkonen | 后缀树Ukkonen算法 | 3.8 | green |
| 13 | cand.string.lyndon_decomposition.basic | Lyndon分解基础 | 3.8 | yellow |
| 14 | cand.string.runs_repetitions.basic | Runs重复子串分析 | 3.8 | yellow |
| 15 | cand.string.border_tree.structure | Border树结构 | 2.10 | yellow |
| 16 | cand.string.manacher.algorithm | Manacher算法 | 2.10 | yellow |
| 17 | cand.string.boyer_moore.algorithm | Boyer-Moore算法 | 2.10 | yellow |
| 18 | cand.string.rabin_karp.algorithm | Rabin-Karp算法 | 2.10 | yellow |
| 19 | cand.string.string_matching.kmp | KMP算法详解 | 2.10 | yellow |
| 20 | cand.string.string_matching.sunday | Sunday算法 | 2.10 | yellow |

## 7. 关键结论

| 问题 | 回答 |
|------|------|
| External B2 总候选数量 | 83 |
| 成功映射数量 | 83 / 83 |
| high confidence 数量 | 78 |
| medium confidence 数量 | 5 |
| low confidence 数量 | 0 |
| green 数量 | 11 |
| yellow 数量 | 65 |
| red 数量 | 4 |
| 需要新 section 的候选数量 | 0 |
| 疑似重复候选数量 | 4 |
| 建议进入 Stage3F Batch1 的候选数量 | 76 |
| **是否修改主图谱** | **否** |
| **是否生成正式 Stage3F Batch1** | **否** |

## 8. 下一步建议

1. ✅ External Batch2 Section Mapping 完成（83 个候选）
2. 🔲 从 suggested_for_batch1 中筛选前 20 个（优先 high confidence + green/yellow）
3. 🔲 构建 Stage3F Batch1 候选计划
4. 🔲 执行 Batch1 动态预审
5. 🔲 执行 Batch1 Merge
6. 🔲 执行 Batch1 Review

---

*本映射不修改主图谱，不生成正式批次。*
