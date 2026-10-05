# Stage3F 标准化候选池与 Batch1 候选计划报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T12:30:00.000Z
- **任务**: 构建 Stage3F 标准化候选池 + 生成 Batch1 候选计划
- **主图谱状态**: 未修改 (item_count=1641, section_count=65)

## 1. 标准化候选池

### 总览

| 指标 | 数量 |
|------|------|
| **候选池总计** | **129** |
| **eligible** | **129** |
| excluded (duplicate/alias) | 298 |
| excluded (high_risk) | 0 |

### 按来源分布

| 来源 | 数量 | 说明 |
|------|------|------|
| carry_over (Stage3E) | 1 | dominance_counting (3.13, green) |
| reserve_pool | 3 | Merge Sort Tree 变体 (3.13, green) |
| external_b1 (Codex) | 46 | 图论+数据结构 (2.21+3.13) |
| external_b2 (String/Math/DP) | 79 | 字符串/数学/DP 全系列 |

### 按 Section 分布

| Section | 名称 | 数量 |
|---------|------|------|
| 2.10 | 字符串算法 | 15 |
| 2.17 | 线性代数 | 3 |
| 2.18 | 综合高级技巧 | 7 |
| 2.21 | 高级图论扩展 | 25 |
| 2.8 | 动态规划 | 23 |
| 3.13 | 高级数据结构扩展 | 25 |
| 3.8 | 字符串结构 | 8 |
| 4.1 | 整数与数论基础 | 9 |
| 4.3 | 计数与组合 | 3 |
| 4.4 | 离散数学基础 | 2 |
| 4.5 | 图与树的数学基础 | 2 |
| 4.9 | 高级数学与群论 | 7 |

### 按风险分布

| Risk | 数量 |
|------|------|
| green | 31 |
| medium | 3 |
| yellow | 95 |

## 2. Stage3F Batch1 候选计划 (20 个)

### 选择策略

1. **Carry-over 优先**: dominance_counting (green, 3.13)
2. **Reserve pool**: Merge Sort Tree 3 变体 (green, 3.13)
3. **B2薄弱区 (green优先)**: 优先补充 **2.8 DP**, **2.10 字符串**, **3.8 字符串结构**, **4.1 数论**
4. **B2 yellow**: 继续补充薄弱区候选
5. **B1 补充**: 最后补充图论/数据结构

### 候选列表

| # | 来源 | Section | 名称 | Risk | Confidence |
|---|------|---------|------|------|-----------|
| 1 | carry_over | 3.13 | Multidimensional: Dominance Counting | green | high |
| 2 | reserve_pool | 3.13 | Merge Sort Tree: Memory Optimization | green | high |
| 3 | reserve_pool | 3.13 | Merge Sort Tree: Offline Inversion | green | high |
| 4 | reserve_pool | 3.13 | Merge Sort Tree: Persistent Variant | green | high |
| 5 | external_b2 | 2.8 | 复杂数位DP | green | high |
| 6 | external_b2 | 2.8 | 换根DP | green | high |
| 7 | external_b2 | 2.8 | 轮廓DP基础 | green | high |
| 8 | external_b2 | 2.8 | 插头DP基础 | green | high |
| 9 | external_b2 | 3.8 | 后缀数组SA-IS算法 | green | high |
| 10 | external_b2 | 3.8 | 广义SAM构建 | green | high |
| 11 | external_b2 | 3.8 | 后缀树Ukkonen算法 | green | high |
| 12 | external_b2 | 2.18 | 斜率优化高级 | green | high |
| 13 | external_b2 | 2.17 | Berlekamp-Massey算法 | green | high |
| 14 | external_b2 | 4.3 | 扩展Lucas定理 | green | high |
| 15 | external_b2 | 4.9 | Min_25筛 | green | high |
| 16 | external_b2 | 2.8 | 数位DP基础 | yellow | high |
| 17 | external_b2 | 2.8 | 树DP基础 | yellow | high |
| 18 | external_b2 | 2.8 | 树的直径DP | yellow | high |
| 19 | external_b2 | 2.8 | 树的重心DP | yellow | high |
| 20 | external_b2 | 2.8 | 拓扑排序DP | yellow | high |

### Section 分布

| Section | 数量 |
|---------|------|
| 2.17 线性代数 | 1 |
| 2.18 综合高级技巧 | 1 |
| 2.8 动态规划 | 9 |
| 3.13 高级数据结构扩展 | 4 |
| 3.8 字符串结构 | 3 |
| 4.3 计数与组合 | 1 |
| 4.9 高级数学与群论 | 1 |

## 3. 推荐结论

| 问题 | 回答 |
|------|------|
| 标准候选池总数 | 129 |
| eligible 数量 | 129 |
| excluded_duplicate 数量 | 298 |
| 建议下一步做动态预审 | **是** |
| **是否修改主图谱** | **否** |
| **是否生成正式 Batch1** | **否** (只是计划) |

## 4. 下一步

1. ✅ 标准化候选池已构建 (129 个候选)
2. ✅ Batch1 候选计划已准备 (20 个)
3. 🔲 执行 Stage3F Batch1 动态预审 (严格重复守卫)
4. 🔲 1号线程执行 Stage3F Batch1 Merge
5. 🔲 2号线程执行 Stage3F Batch1 Review

---

*本计划不修改主图谱，不生成正式合并批次。*
