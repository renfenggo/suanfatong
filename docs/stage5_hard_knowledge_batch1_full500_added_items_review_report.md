# Stage5-HardKnowledge Batch1 full500 新增节点 Review 报告

**生成时间**: 2026-05-26T07:13:51.655064+00:00

## 1. Review 总节点数

**500** (必须为 500)

## 2. approve 数量

**200**

## 3. 建议降为 C 数量

**200**

## 4. 建议保留 B 数量

**294**

## 5. 建议保留 A 数量

**6**

## 6. needs_dependency_fix 数量

**268**

- direct_pre >= 100 的项目: 38
- direct_pre >= 15 的项目: 300

## 7. needs_merge_or_collapse 数量

**32**

- 模板化名称: 32

## 8. delete_duplicate 数量

**0**

## 9. manual_review 数量

**0**

## 10. direct_pre 过长问题

| 指标 | 值 |
|------|-----|
| direct_pre >= 100 | 38 |
| direct_pre >= 15 | 300 |
| 最大值 | 234 |

### 严重过长 (>100 条) 示例

- 2.8.236: 前缀最值 DP的在线转移 (前缀最值 DP Online Transition)... (234 条)
- 2.8.238: 前缀最值 DP的分段决策 (前缀最值 DP Segmented Decision)... (234 条)
- 2.8.206: 堆维护 DP的边界压缩 (堆维护 DP Boundary Compression)... (234 条)
- 2.8.219: 分治转移 DP的可合并状态 (分治转移 DP Mergeable States)... (234 条)
- 2.8.208: 后缀最值 DP的边界压缩 (后缀最值 DP Boundary Compression)... (234 条)

**问题**: 234 条 direct_pre 实际将整个 section 2.8 的所有节点加入了前置，需要修复为 2-4 个核心前置。

## 11. 是否发现重复或近重复

与旧节点高相似度 (>=0.85): 0
新节点间高相似度 (>=0.85): 0

## 12. 是否建议进入 Fix Lite

**是** — 268 个需依赖修复，32 个需合并/折叠

## 13. 是否建议先执行 Duplicate Prune

**否**

## 14. 是否建议继续 Batch2

**暂缓** — 先完成 Fix Lite 和 Duplicate Prune 后再评估。

## 15. 是否修改主图谱

**否**

## 16. 风险分布详情

| 风险类型 | 数量 |
|---------|------|
| direct_pre_long | 262 |
| direct_pre_too_long | 38 |
| template_name | 32 |
| low_learning_value_as_standalone | 32 |

---
*本报告自动生成*
