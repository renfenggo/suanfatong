# Stage3F 候选池重建规划报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-25T12:10:00.000Z
- **任务**: Stage3F 候选池重建规划
- **主图谱状态**: 未修改

## 1. 当前主图谱状态

| 检查项 | 实际值 |
|--------|--------|
| item_count | 1641 |
| section_count | 65 |
| Stage3E 总新增 | 159 (含 Batch5 smaller_15 + Batch6 fallback_24) |

## 2. Stage3E 停止判断

- **Stage3E 是否应停止**: **是**
- **原因**: 
  - aggressive_batches 中 150 个候选，名称均已存在于主图谱
  - reserve_pool 中 30 个候选，仅 4 个名称不在图谱中（且均为 wait_for_stage3e_result）
  - 唯一绝对安全候选: **dominance_counting**（v2 计划第 25 个因 fallback_24 截断）
  - 继续 aggressive 模式需启用全新区间候选池

### Stage3E 合并汇总

| 批次 | 数量 | item_count |
|------|------|-----------|
| Batch1 (2.21) | 30 | 1482→1512 |
| Batch2 (2.21+3.13) | 30 | 1512→1542 |
| Batch3 (3.13+2.21) | 30 | 1542→1572 |
| Batch4 (2.21) | 30 | 1572→1602 |
| Batch5 smaller_15 | 15 | 1602→1617 |
| Batch6 fallback_24 | 24 | 1617→1641 |
| **总计** | **159** | **1482→1641** |

## 3. Reserve Pool 状态

| 类别 | 数量 | 说明 |
|------|------|------|
| 原始保留 | 30 | stage3f=55, stage3g=20, wait_for_stage3e=10 (去重后30个不同candidate_id) |
| 已合并(Batch1~6) | 11 | candidate_id 已在 mapping 中 |
| 名称已在图谱中 | 15 | 名称与主图谱已有 item 重复 |
| **可用(名称不在图谱)** | **4** | 可带入 Stage3F |

### 可用 Reserve 候选

| candidate_id | name | section | risk |
|-------------|------|---------|------|
| cand.ds.merge_sort_tree.memory_optimization | Merge Sort Tree: Memory Optimization | 3.13 | green |
| cand.ds.merge_sort_tree.offline_inversion | Merge Sort Tree: Offline Inversion | 3.13 | green |
| cand.ds.merge_sort_tree.persistent_variant | Merge Sort Tree: Persistent Variant | 3.13 | green |
| cand.ds.multidimensional.dominance_counting | Multidimensional: Dominance Counting | 3.13 | green |

## 4. 外部候选池状态

### Batch1 (Codex: 图论+数据结构)

| 类别 | 数量 |
|------|------|
| 总计 | 340 |
| 名称已在图谱中 | 284 (284) |
| 别名冲突 | 10 |
| 可用(名称+别名均不重复) | **46** |

**Section 分布**: {'2.21': 25, '3.13': 21}

**Risk 分布**: {'medium': 30, 'low': 16}

### Batch2 (字符串/数学/DP)

| 类别 | 数量 |
|------|------|
| 总计 | 83 |
| 名称已在图谱中 | 4 |
| 可用 | **79** |

**Section 分布**: {'advanced_algorithm': 79}

**Risk 分布**: {'medium': 68, 'low': 11}

> ⚠️ Batch2 的 79 个候选来自全新的"高级算法"区间
> 这需要在 Stage3F 之前完成 section 归属映射

## 5. Stage3F 候选池全景

### 总规模

| 来源 | 数量 |
|------|------|
| Stage3E carry-over (dominance_counting) | 1 |
| Reserve pool (名称可用) | 4 |
| External B1 (Codex, 名称+别名可用) | 46 |
| External B2 (String/Math/DP, 名称可用) | 79 |
| **总计** | **130** |

### Section 分布

| Section | 数量 | 说明 |
|---------|------|------|
| 2.21 | 25 | 高级图论扩展 |
| 3.13 | 26 | 高级数据结构扩展 |
| advanced_algorithm | 79 | 需解析的候选(字符串/数学/DP) |

### Risk 分布

| Risk 等级 | 数量 |
|-----------|------|
| green | 5 |
| low | 27 |
| medium | 98 |

## 6. 第一批建议 (20个)

**建议数量**: 20 个（比 Stage3E 的 30 更稳健）

**选择策略**:
1. 优先 3.13 green/low risk 候选
2. 再选 2.21 green/low risk 候选
3. 最后选 advanced_algorithm medium risk 候选
4. reserve pool + Codex 优先于 Batch2

**第一批建议候选**:
  1. [3.13] Multidimensional: Dominance Counting — (green, stage3e_v2_remaining)
  2. [3.13] Merge Sort Tree: Memory Optimization — (green, )
  3. [3.13] Merge Sort Tree: Offline Inversion — (green, )
  4. [3.13] Merge Sort Tree: Persistent Variant — (green, )
  5. [3.13] Multidimensional: Dominance Counting — (green, )
  6. [3.13] 位集与线性基：Rollback Linear Basis — (low, external_batch1_codex)
  7. [3.13] 位集与线性基：Maximum Xor Query — (low, external_batch1_codex)
  8. [3.13] 位集与线性基：Rank Over Gf2 — (low, external_batch1_codex)
  9. [3.13] 位集与线性基：Basis With Deletion — (low, external_batch1_codex)
  10. [2.21] 强连通分量 DAG：Dag Reachability — (low, external_batch1_codex)
  11. [2.21] 动态图连通性：Divide And Conquer On Time — (low, external_batch1_codex)
  12. [2.21] 强连通分量 DAG：Dominating Components — (low, external_batch1_codex)
  13. [2.21] 动态图连通性：Edge Interval Model — (low, external_batch1_codex)
  14. [2.21] 强连通分量 DAG：Minimum Edges To Strong — (low, external_batch1_codex)
  15. [2.21] 全局最小割：Minimum Cut Modeling — (low, external_batch1_codex)
  16. [2.21] 强连通分量 DAG：Scc Dp — (low, external_batch1_codex)
  17. [2.21] 动态图连通性：Dynamic Bridge — (low, external_batch1_codex)
  18. [2.21] 强连通分量 DAG：Component Topo Order — (low, external_batch1_codex)
  19. [2.21] 动态图连通性：Dynamic Biconnectivity — (low, external_batch1_codex)
  20. [2.21] 动态图连通性：Connectivity Snapshots — (low, external_batch1_codex)

## 7. Stage3F 模式建议

### 是否继续 aggressive 模式

**是，继续 aggressive 模式但调整策略**

### aggressive 模式调整

| 项目 | Stage3E | Stage3F 建议 |
|------|---------|-------------|
| 单批容量 | 30 | **20**（逐步推进） |
| 候选来源 | aggressive_batches.json | 外部候选池(Codex/String/Math/DP) |
| section 覆盖 | 2.21 + 3.13 | 2.21 + 3.13 + **高级算法/高级字符串/高级数学/高级DP** |
| 重复守卫 | v1漏检→v2修复→严格精确匹配 | 延续 Batch7 严格守卫 |
| 预审脚本 | medium20→full30→fallback_24 | 需要新的 section 路由和候选池标准化 |

### 需在 Stage3F 开始前完成

1. **External Batch2 (String/Math/DP) section 映射**
   - 79 个候选分布在不同算法子领域
   - 需要分析每个 candidate 的 target_section 归属
   - 可能需要新增 section 或映射到已有 section

2. **候选池标准化**
   - 统一 external_pool 格式 → 主图谱 section 映射
   - 包含 direct_pre_name_suggestion 依赖映射
   - 包含 i18n_seed 别名检查

3. **严格守卫升级**
   - 在 v2 检查（candidate_id + name + en_name）基础上
   - 增加 aliases 检查（避免 Batch6 v1 漏检复现）

## 8. 推荐结论

| 问题 | 回答 |
|------|------|
| Stage3E 是否应停止 | **是** |
| Stage3F 是否需要重新生成候选池 | **是** |
| dominance_counting 是否进入 Stage3F | **是** |
| Stage3F 第一批建议数量 | **20 个** |
| 是否继续 aggressive 模式 | **是**（降低至 20/批） |
| 主图谱是否修改 | **否** |

## 9. 下一步

1. ✅ 确认 Stage3E 正式完成（共 +159 节点，1641）
2. 🔲 将 dominance_counting 加入 Stage3F 候选手册
3. 🔲 解析 External Batch2 (79 个) section 归属
4. 🔲 生成 External Pool → 主图谱 section 完整映射表
5. 🔲 构建 Stage3F 标准化候选池
6. 🔲 生成 Stage3F Batch1 候选计划 (20 个)
7. 🔲 执行 Batch1 动态预审（严格重复守卫）

---

*本规划不修改主图谱，仅输出候选池重建方案。*
