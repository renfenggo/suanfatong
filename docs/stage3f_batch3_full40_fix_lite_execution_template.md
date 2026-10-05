# Stage3F Batch3 full_40 Fix Lite 执行模板

## 基本信息

- **批次**: Stage3F Batch3 full_40
- **当前状态**: Merge 已完成，item_count=1717, section_count=65, validate-only=passed
- **本模板用途**: 等待 2号线程 Review 返回后执行 Fix Lite（仅修改 review_status）
- **执行者**: 1号线程 / GLM5
- **依据**: v2 文件（candidate_plan_v2 + dynamic_precheck_v2 + dependency_cleanup_plan）
- **主图谱**: 未修改（本模板不执行任何修改）

---

## 一、等待 2号 Review 输出的文件列表

在执行 Fix Lite 之前，必须确认以下 5 个 Review 输出文件已就绪：

| # | 文件路径 | 说明 | 关键字段 |
|---|---------|------|---------|
| 1 | `data/stage3f_batch3_full40_added_items_review.json` | 逐节点 Review 结论 | item_id, verdict (approve/C/B/A), suggested_priority |
| 2 | `data/stage3f_batch3_full40_review_status_patch_preview.json` | review_status 补丁预览 | item_id, old_review_priority, new_review_priority, old_need_manual_review, new_need_manual_review |
| 3 | `data/stage3f_batch3_full40_dependency_fix_candidates.json` | 依赖修复候选 | candidate_id, item_id, issue_type, suggested_direct_pre |
| 4 | `data/stage3f_batch3_full40_problem_pattern_sync_candidates.json` | problem_pattern 同步候选 | candidate_id, item_id, pattern_type, action |
| 5 | `data/stage3f_batch3_full40_merge_or_collapse_candidates.json` | 建议合并/折叠的候选 | candidate_id, item_id, target_item_id, action |

**前置条件检查（执行 Fix Lite 前必须全部满足）**：

| 检查项 | 期望值 | 实际值（由执行时填写） |
|--------|:------:|:--------------------:|
| item_count | 1717 | |
| section_count | 65 | |
| validate-only passed | true | |
| resolved_pre_mismatches | [] | |
| dangling_refs | [] | |
| direct_pre_cycle | null | |
| product_metadata_validation.passed | true | |
| report_matches_json | true | |
| passed | true | |
| 2号 Review 5 个输出文件全部存在 | true | |

---

## 二、三分支决策树

执行 Fix Lite 时，根据 2号 Review 的输出内容选择分支：

```
读取 2号 Review 输出文件
│
├── dependency_fix_candidates 是否非空？
│   ├── 是 → 分支 C（暂停，不自动修改 direct_pre）
│   └── 否 → 继续
│
├── merge_or_collapse_candidates 是否非空？
│   ├── 是 → 分支 B（暂停，先执行 Duplicate Resolution Plan）
│   └── 否 → 继续
│
└── 全部为空 → 分支 A（执行标准 Fix Lite）
```

### 分支 A：dependency_fix_candidates 为空，merge_or_collapse_candidates 为空

标准 Fix Lite 流程（只修改 review_status）：

```
Step 1: 备份主图谱
  -> backups/merged_knowledge_graph_item_dependencies_refined_before_stage3f_batch3_full40_fix_lite.json

Step 2: 读取 data/stage3f_batch3_full40_review_status_patch_preview.json
  -> 验证 patches 列表
  -> 验证每条的 item_id 属于 Stage3F Batch3 新增 40 个节点
  -> 验证 old_review_priority 和 old_need_manual_review 与当前图谱一致

Step 3: 逐个应用 patch（仅修改 review_status）
  -> 修改 review_status.review_priority: B → C 或 B → B（keep-B）
  -> 修改 review_status.need_manual_review: true → false（clear manual review）
  -> 绝对不修改 direct_pre / resolved_pre / rel
  -> 绝对不修改旧节点

Step 4: 写入主图谱

Step 5: 运行 validate-only
  -> python refine_item_dependencies.py --validate-only --input merged_knowledge_graph_item_dependencies_refined.json --report item_dependency_refinement_report.md --low-conf low_confidence_dependency_review.json --validation dependency_validation_result.json --strict

Step 6: 验证结果
  -> item_count = 1717
  -> section_count = 65
  -> dangling_refs = []
  -> direct_pre_cycle = null
  -> resolved_pre_mismatches = []
  -> product_metadata_validation.passed = true
  -> report_matches_json = true
  -> passed = true

Step 7: 输出结果文件
  -> data/stage3f_batch3_full40_fix_lite_applied_patch.json（已应用的 patch 记录）
  -> data/stage3f_batch3_full40_fix_lite_validation_result.json（验证结果）
  -> docs/stage3f_batch3_full40_fix_lite_report.md（Fix Lite 报告）
```

### 分支 B：merge_or_collapse_candidates 非空

**处理策略：暂停普通 Fix Lite，先执行 Duplicate Prune**

```
1. 输出警告：merge_or_collapse_candidates 非空，需要先走 Duplicate Resolution Plan
2. 暂停 Review Status 降级
3. 调用 docs/stage3f_batch3_full40_duplicate_prune_template.md 执行
4. 按 Duplicate Prune 流程完成后再返回 Fix Lite
5. 删除后 item_count 会减少，需要重新计算 validation_baseline
```

**Duplicate Prune 完成后再执行 Fix Lite（针对剩余节点）**：

```
1. 删除节点后重新备份
2. 更新 validation_baseline
3. 只处理剩余新增节点的 review_status
4. 排除已删除节点
5. 运行 validate-only 并验证
```

### 分支 C：dependency_fix_candidates 非空

**处理策略：暂停，不自动修改 direct_pre**

```
1. 输出警告：dependency_fix_candidates 非空，需要人工介入
2. 只应用 review_status patch（如果 2号 Review 确认可以单独执行）
3. 将 dependency_fix_candidates 记录到 Fix Lite 报告的风险部分
4. 标记 dependency_fix 为 pending，等待人工决策后再执行
5. 不自动修改任何 direct_pre / resolved_pre / rel
```

### problem_pattern_sync_candidates 特殊处理（所有分支通用）

**处理策略：只记录不处理**

```
1. 将 problem_pattern_sync_candidates 记录到 Fix Lite 报告的"已知问题"部分
2. 标记 sync_to_patterns 为需要人工后续处理
3. 不自动创建或修改任何 problem_pattern
4. 不影响 Fix Lite 主流程
```

---

## 三、review_status patch 应用规则

### 3.1 允许的修改

| 字段 | 允许修改 | 说明 |
|------|:-------:|------|
| review_status.review_priority | ✅ 是 | B→C 或 B→B（keep-B）或 A→B，以下发 patch 为准 |
| review_status.need_manual_review | ✅ 是 | true→false（清除人工复查标记） |
| review_status.review_status_reason | ✅ 是 | 可添加降级说明（可选） |

### 3.2 不允许的修改

| 字段 | 允许修改 | 说明 |
|------|:-------:|------|
| direct_pre | ❌ 否 | 绝对不允许修改 |
| resolved_pre | ❌ 否 | 绝对不允许修改 |
| rel | ❌ 否 | 绝对不允许修改 |
| id | ❌ 否 | 不允许修改 |
| name / en_name | ❌ 否 | 不允许修改 |
| level | ❌ 否 | 不允许修改 |
| tracks | ❌ 否 | 不允许修改 |
| learning_path_policy | ❌ 否 | 不允许修改 |
| 旧节点任何字段 | ❌ 否 | 不允许修改任何旧节点 |

### 3.3 新增节点白名单（仅允许修改这 40 个节点的 review_status）

| Section | item_id | 名称 | risk_band | 清洗候选 |
|:-------:|:-------:|------|:---------:|:--------:|
| 2.8 | 2.8.143 | DAG最长路DP | yellow | - |
| 2.8 | 2.8.144 | 状态压缩DP基础 | yellow | - |
| 2.8 | 2.8.145 | 旅行商问题DP | yellow | - |
| 2.8 | 2.8.146 | 子集DP基础 | yellow | - |
| 2.8 | 2.8.147 | 子集枚举优化 | yellow | - |
| 2.8 | 2.8.148 | 自动机DP基础 | yellow | - |
| 2.8 | 2.8.149 | 自动机矩阵DP | yellow | - |
| 2.8 | 2.8.150 | 概率DP基础 | yellow | - |
| 2.10 | 2.10.35 | Border树结构 | yellow | - |
| 2.10 | 2.10.36 | Manacher算法 | yellow | - |
| 2.10 | 2.10.37 | Boyer-Moore算法 | yellow | - |
| 2.10 | 2.10.38 | Rabin-Karp算法 | yellow | - |
| 2.10 | 2.10.39 | KMP算法详解 | yellow | - |
| 3.8 | 3.8.15 | Lyndon分解基础 | yellow | - |
| 3.8 | 3.8.16 | Runs重复子串分析 | yellow | - |
| 4.1 | 4.1.35 | Legendre符号 | yellow | - |
| 4.1 | 4.1.36 | Tonelli-Shanks算法 | yellow | - |
| 4.1 | 4.1.37 | 扩展中国剩余定理 | yellow | - |
| 4.1 | 4.1.38 | Garner算法 | yellow | - |
| 4.9 | 4.9.6 | 欧拉函数应用 | yellow | - |
| 4.9 | 4.9.7 | 杜教筛 | yellow | - |
| 4.9 | 4.9.8 | Burnside引理 | yellow | - |
| 4.9 | 4.9.9 | Polya计数定理 | yellow | - |
| 2.17 | 2.17.21 | 快速沃尔什变换 | yellow | - |
| 2.17 | 2.17.22 | 子集卷积 | yellow | - |
| 2.18 | 2.18.12 | 斜率优化基础 | yellow | - |
| 2.18 | 2.18.13 | 分治DP优化 | yellow | - |
| 2.18 | 2.18.14 | Knuth优化 | yellow | - |
| 2.18 | 2.18.15 | WQS二分优化 | yellow | - |
| 2.21 | 2.21.147 | 强连通分量 DAG：Dag Reachability | green | ✅ 清洗 |
| 2.21 | 2.21.148 | 动态图连通性：Divide And Conquer On Time | green | ✅ 清洗 |
| 2.21 | 2.21.149 | 强连通分量 DAG：Dominating Components | green | ✅ 清洗 |
| 2.21 | 2.21.150 | 动态图连通性：Edge Interval Model | green | ✅ 清洗 |
| 2.21 | 2.21.151 | 强连通分量 DAG：Minimum Edges To Strong | green | ✅ 清洗 |
| 3.13 | 3.13.186 | 位集与线性基：Rollback Linear Basis | green | ✅ 清洗 |
| 3.13 | 3.13.187 | 位集与线性基：Maximum Xor Query | green | ✅ 清洗 |
| 3.13 | 3.13.188 | 位集与线性基：Rank Over Gf2 | green | ✅ 清洗 |
| 3.13 | 3.13.189 | 位集与线性基：Basis With Deletion | green | ✅ 清洗 |
| 3.13 | 3.13.190 | 线段树变体：Split | yellow | ✅ 清洗 |
| 3.13 | 3.13.191 | 高级并查集：Parity | yellow | ✅ 清洗 |

---

## 四、Fix Lite 执行前验证清单

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | item_count = 1717 | 从当前图谱读取 items 总数 |
| 2 | section_count = 65 | 从当前图谱读取 sections 总数 |
| 3 | validate-only passed | 运行 --validate-only 并检查结果 |
| 4 | 2号 Review 5 个文件全部存在 | 检查文件系统 |
| 5 | patch 只覆盖 40 个新增节点 | 验证每条的 item_id 在白名单中 |
| 6 | patch 不修改旧节点 | 验证没有旧节点 id 出现在 patches 中 |
| 7 | patch 不修改 direct_pre / resolved_pre / rel | 验证 patch 中无这些字段 |
| 8 | 当前分支选择正确 | 按三分支决策树判断 |

---

## 五、Fix Lite 成功标准

| 检查项 | 期望值 |
|--------|:------:|
| item_count | 1717（除非先执行了 Duplicate Prune） |
| section_count | 65 |
| dangling_refs | [] |
| direct_pre_cycle | null |
| resolved_pre_mismatches | [] |
| product_metadata_validation.passed | true |
| report_matches_json | true |
| passed | true |

---

## 六、失败恢复

如果 validate-only 失败：

```
1. 立即恢复备份
   -> shutil.copy2(backup_path, merged_knowledge_graph_item_dependencies_refined.json)
2. 如果执行过 Duplicate Prune，恢复 prune 前的备份
3. 输出失败原因分析
4. 不要继续 Stage3F Batch4
```

---

## 七、Fix Lite 输出文件

| # | 文件路径 | 内容 |
|---|---------|------|
| 1 | data/stage3f_batch3_full40_fix_lite_applied_patch.json | 已应用的 review_status patch 记录 |
| 2 | data/stage3f_batch3_full40_fix_lite_validation_result.json | validate-only 结果快照 |
| 3 | docs/stage3f_batch3_full40_fix_lite_report.md | Fix Lite 执行报告 |
| 4 | data/stage3f_batch3_full40_fix_lite_risk_checklist.json | 风险清单（执行时逐项确认） |

---

## 八、注意事项

1. **只修改 review_status**，不修改其他字段
2. **不继续 Stage3F Batch4**
3. **如果 merge_or_collapse_candidates 非空**，先走 Duplicate Resolution Plan，不要执行 Fix Lite
4. **如果 dependency_fix_candidates 非空**，不自动修 direct_pre，等人工确认
5. **problem_pattern_sync_candidates** 只记录不处理
6. **validate-only 失败必须恢复备份**
