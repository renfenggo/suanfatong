# Stage3E P0-A 三节点微型复核报告

## 执行概况

- **生成者**: GLM5
- **生成时间**: 2026-05-22T23:50:00.000Z
- **主图谱状态**: 未修改
- **复核节点**: 2.21.76, 2.21.106, 2.21.117

## 三个节点的真实名称

### 2.21.76
| 字段 | 值 |
|------|-----|
| name | 有向生成树：Branching Theorem |
| en_name | Directed MST: Branching Theorem |
| direct_pre | 4.5.2, 2.13.10 |
| resolved_pre_count | 22 |
| section | 2.21（高级图论扩展） |
| aliases | ['Directed MST', 'Branching Theorem'] |
| review_status | need_manual_review=True, priority=B |
| 分类草稿 type | implementation_variant（建议改为 theorem_or_property） |

### 2.21.106
| 字段 | 值 |
|------|-----|
| name | 平面图：Dual Shortest Path |
| en_name | Planar Graph: Dual Shortest Path |
| direct_pre | 2.7.1 |
| resolved_pre_count | 19 |
| section | 2.21（高级图论扩展） |
| review_status | need_manual_review=True, priority=B |
| 分类草稿 type | implementation_variant（建议改为 modeling_pattern） |

### 2.21.117
| 字段 | 值 |
|------|-----|
| name | 特殊图：Tournament Graph |
| en_name | Special Graph: Tournament Graph |
| direct_pre | 2.7.1 |
| resolved_pre_count | 19 |
| section | 2.21（高级图论扩展） |
| aliases | 无 |
| review_status | need_manual_review=False, priority=C（Batch2 Review 已降级） |
| 分类草稿 type | unclear（建议改为 core_concept） |

## 2.21.117 ID/Name 一致性检查结果

**结论: 无 ID/Name 不一致问题。**

- 主图谱中 2.21.117 确实是 **特殊图：Tournament Graph**
- candidate_id: `cand.graph.special_graph.tournament_graph`，来自 batch_2
- Virtual Tree 系列从 2.21.118（虚树：Colored Points）开始，ID 无重叠
- 分类草稿中将其误标为 unclear/Grade D，但主图谱 review_status 已标注 priority=C（已复查）
- Tournament Graph（竞赛图）是图论中稳定的特殊图概念，在竞赛中高频出现

## 三个节点是否仍阻塞 Batch5

| 节点 | 原分级 | 复核后 | 是否阻塞 Batch5 | 建议行动 |
|------|--------|--------|----------------|---------|
| 2.21.76 Branching Theorem | P0-A | → P0-B | **否** | keep_with_parent_note |
| 2.21.106 Dual Shortest Path | P0-A | → P0-B | **否** | keep_with_parent_note |
| 2.21.117 Tournament Graph | P0-A | → P0-B | **否** | needs_parent_fix_later |

**三个节点均不应阻塞 Batch5。** 原因：

### 2.21.76 Branching Theorem
- 本质是定理/性质（theorem_or_property），不是实现变体
- 有 22 个 resolved_pre，依赖链完整
- 已有 aliases 标注（'Directed MST', 'Branching Theorem'）
- 父概念 weak 但可接受：保留在 2.21 下，后续补充 parent note

### 2.21.106 Dual Shortest Path
- 本质是建模模式（modeling_pattern），不是实现变体
- 有 19 个 resolved_pre，依赖合理
- 父概念 2.21（高级图论扩展）可暂时接受

### 2.21.117 Tournament Graph
- **主图谱中 ID/name 一致，无映射错误**
- review_status 已标注 need_manual_review=False, priority=C
- Tournament Graph 是图论确切概念，有独立竞赛价值
- 分类草稿误标为 unclear/Grade D，建议后续修正
- 父概念 2.21 可接受，但 2.9（图基础与遍历）更合适

## 处理建议汇总

| 节点 | 建议 |
|------|------|
| 2.21.76 | 降为 P0-B，保留，补充 parent note（2.6.4 或 2.21） |
| 2.21.106 | 降为 P0-B，保留，补充 parent note（2.21） |
| 2.21.117 | 降为 P0-B，保留，后续修复父概念（建议 2.9） |

## 整体复核结论

### 1. 三个节点的真实名称是否确认？
- **2.21.76**: 有向生成树：Branching Theorem ✓
- **2.21.106**: 平面图：Dual Shortest Path ✓
- **2.21.117**: 特殊图：Tournament Graph ✓

### 2. 是否存在 2.21.117 ID/name 不一致？
**否。** 2.21.117 明确是 Tournament Graph。
Virtual Tree Build 在老版本报告中可能指代 2.21.118（虚树：Colored Points）
或虚树系列的概念混淆，但当前主图谱无此问题。

### 3. 三个节点是否仍阻塞 Batch5？
**否。** 三个节点均不阻塞 Batch5。建议：
- 将 2.21.76 从 P0-A 降为 P0-B
- 将 2.21.106 从 P0-A 降为 P0-B
- 将 2.21.117 从 P0-A 降为 P0-B（其 review_status 已是 C 级）

### 4. 是否建议继续 Batch5 smaller_15？
**是，建议立即以 smaller_15 模式继续 Batch5。**

三个 P0-A 节点经复核后均不应阻塞 Batch5：
- 父概念虽然有 weak/missing，但不影响合并
- 依赖关系合理
- 分类草稿中的 Grade D/unclear 是审计分类偏差，非节点本身质量问题

### 5. 是否修改主图谱？
**否。** 本次复核未修改主图谱。

## 建议的 Batch5 启动条件

1. 将 2.21.76 从 P0-A 降为 P0-B（保留，补充 parent note）
2. 将 2.21.106 从 P0-A 降为 P0-B（保留，补充 parent note）
3. 将 2.21.117 从 P0-A 降为 P0-B（保留，后续修复父概念）
4. 更新 dual_risk_triage.json 中的分级（可选）
5. **立即以 smaller_15 启动 Batch5**

---

报告生成时间: 2026-05-22T23:50:00.000Z
生成者: GLM5
任务类型: Stage3E P0-A 三节点微型复核
主图谱修改状态: 否
