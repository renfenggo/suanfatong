# Stage5-HardKnowledge Batch1 full500 Post-Branch-B 复查报告

**生成时间**: 2026-05-26T08:02:01.543574+00:00

## 1. 当前 item_count

**2640**

## 2. 剩余 Stage5 Batch1 节点数量

**475** (2665 - 25 = 2640，其中旧节点 2165 + batch1剩余 475)

## 3. 已删除节点数量

**25**

## 4. Keeper 节点数量

**7**

| item_id | 父主题 |
|---------|--------|
| 2.8.202 | 凸包维护 DP |
| 2.8.203 | 分治转移 DP |
| 2.8.204 | 队列维护 DP |
| 2.8.205 | 线段树维护 DP |
| 2.8.206 | 堆维护 DP |
| 2.8.207 | 前缀最值 DP |
| 2.8.208 | 后缀最值 DP |

## 5. direct_pre 过长问题是否已解决

**是**

## 6. merge_or_collapse 问题是否已解决

**是** — 32 个模板节点已处理为 7 个 keeper

## 7. needs_dependency_fix 剩余数量

**0**

## 8. needs_merge_or_collapse 剩余数量

**0**

## 9. Fix Lite 补丁数量

**475** (只更新 review_status/priority 轻量字段)

## 10. C / B / A 分布建议

| Priority | 数量 | 说明 |
|----------|------|------|
| C | 468 | approve 节点，直接降为 C |
| B | 7 | 7 个 keeper + 少量需关注节点 |
| A | 0 | 需人工复查 |

## 11. 是否建议 1号执行 Fix Lite

**是** — readiness=ready_for_1号线程_fix_lite_stage5_hard_batch1_full500_post_branch_b

## 12. 是否建议继续 Batch2

**否** — 必须暂缓，待 Fix Lite 完成后评估

## 13. 是否修改主图谱

**否**

## 14. 验证检查汇总

| 检查项 | 结果 |
|--------|------|
| item_count_2640 | ✅ |
| section_count_65 | ✅ |
| validation_passed | ✅ |
| removed_25 | ✅ |
| removed_not_in_graph | ✅ |
| no_dangling_to_removed | ✅ |
| no_pre_234 | ✅ |
| no_section_refs | ✅ |
| remaining_475 | ✅ |
| keepers_7 | ✅ |
| dep_fix_remaining_0 | ✅ |
| old_items_preserved | ✅ |

## 15. Readiness

```json
{
  "baseline_item_count": 2640,
  "remaining_stage5_batch1_nodes": 475,
  "deleted_or_merged_nodes": 25,
  "dependency_fix_remaining": 0,
  "merge_or_collapse_remaining": 0,
  "recommendation": "ready_for_1号线程_fix_lite_stage5_hard_batch1_full500_post_branch_b"
}
```

---
*本报告自动生成*
