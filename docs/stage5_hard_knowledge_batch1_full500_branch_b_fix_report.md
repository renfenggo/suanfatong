# Stage5-HardKnowledge Batch1 full500 Branch B 修复报告

- 修复时间: 2026-05-26T15:55:52
- 分支: B（先合并/折叠 → 再 direct_pre 缩减）

## 修复前状态

- item_count = **2665**
- section_count = 65

## 步骤一：合并/折叠 25 个模板化子节点

| 父主题 (Keeper) | 子节点合并数量 | 子节点 ID 范围 |
|:-------------|:------------:|:-------------|
| 2.8.202 (凸包维护 DP) | 4 | 2.8.209, 2.8.210, 2.8.211, 2.8.212 |
| 2.8.203 (分治转移 DP) | 4 | 2.8.219, 2.8.220, 2.8.221, 2.8.222 |
| 2.8.204 (队列维护 DP) | 4 | 2.8.223, 2.8.224, 2.8.225, 2.8.226 |
| 2.8.205 (线段树维护 DP) | 4 | 2.8.227, 2.8.228, 2.8.229, 2.8.230 |
| 2.8.206 (堆维护 DP) | 4 | 2.8.231, 2.8.232, 2.8.233, 2.8.234 |
| 2.8.207 (前缀最值 DP) | 4 | 2.8.235, 2.8.236, 2.8.237, 2.8.238 |
| 2.8.208 (后缀最值 DP) | 1 | 2.8.239 |

**总合并节点：25**
**保留 keeper：7**
**删除后 item_count：2665 - 25 = 2640**

## 步骤二：direct_pre 缩减

- 缩减节点数：282（方案 282，过滤移除节点后 282）
- 缩减前 direct_pre 总数：10535
- 缩减后 direct_pre 总数：756
- 每个节点 direct_pre 数量：2～6 ✓
- section ID 引用：0 ✓
- 被删除节点引用：0 ✓

## Validate-only 结果

| 检查项 | 结果 |
|:-------|:--:|
| item_count = 2640 | ✅ |
| section_count = 65 | ✅ |
| dangling_refs = [] | ✅ (0) |
| direct_pre_cycle = null | ✅ |
| resolved_pre_mismatches = [] | ✅ (0) |
| section id refs in direct_pre = 0 | ✅ (0) |
| removed node refs in direct_pre = 0 | ✅ (0) |
| duplicates = 0 | ✅ (0) |
| product_metadata OK | ✅ |
| **passed = true** | **✅** |

## 修改状态

| 检查项 | 状态 |
|:-------|:--:|
| 是否修改旧 2165 节点 | **否** — 仅修改 Stage5 新增节点 |
| 是否修改 io_v4_4.json | **否** |
| 是否修改前端代码 | **否** |
| 是否继续 Batch2 | **否** |

## 建议

**建议进入 Fix Lite。**
Branch B 修复全部 11 项验证通过，可统一进入 Review/Fix Lite 阶段。

## 备份文件

`backups/merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch1_full500_branch_b_fix.json`

---
*报告自动生成于 2026-05-26T15:55:52*