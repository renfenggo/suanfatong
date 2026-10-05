# Stage5 当前状态总验收报告

- 审计时间: `2026-06-16`
- 审计类型: 只读审计
- 未修改: 主图谱、前端图谱、内容索引、内容正文、已有报告

## 一、输入文件

- `merged_knowledge_graph_item_dependencies_refined.json`
- `assets/data/knowledge/io_v4_4.json`
- `assets/data/knowledge_content/content_index.json`
- `assets/data/knowledge_content/items/stage5_hard_batch2_part_001.json`
- `docs/stage5_batch2_persistent_segment_tree_section_review.md`
- `data/stage5_batch2_persistent_segment_tree_section_review.json`
- `data/stage5_batch2_persistent_segment_tree_section_fix_report.json`
- `data/checkpoint_category_logic_verification.json`
- `data/stage5_hard_knowledge_batch3_readiness_plan.json`

## 二、一号线程验收结果

- **passed**: True
- **has_content 全部 true**: True
- **7 个目标节点主图谱全部 3.13**: True
- **7 个目标节点前端图谱全部 3.13**: True
- **7 个目标节点内容 part 全部 3.13**: True
- **direct_pre/rel/resolved_pre 完整**: True
- **声明未修改内容正文**: True

## 三、二号线程验收结果

- **passed**: True
- **verification_status**: passed
- **matches_expected**: True
- **stats_fixed**: {'算法': 323, '数据结构': 110, '数学': 167, '合计': 600}
- **stats_match_expected**: True
- **prefix_distribution**: {'2': 323, '3': 110, '4': 167}
- **prefix_match_expected**: True

## 四、三号线程验收结果

- **passed**: True
- **stability_status**: [PASS] 稳定
- **is_stable_3240**: True
- **unique_risky_candidate_count**: 141
- **safe_candidate_count**: 0
- **risk_ratio**: 100%
- **dependency_missing_count**: 141
- **dependency_missing_ratio**: 100.0%
- **remaining_candidate_count**: 141
- **suggestion_reasonable**: True

## 五、全局 3240 稳定性检查

- **passed**: True
- **main_item_count**: 3240
- **frontend_item_count**: 3240
- **main_section_count**: 65
- **frontend_section_count**: 65
- **id_sets_match**: True
- **generated_item_count**: 3240
- **content_covered_count**: 3240
- **batch2_id_count**: 600
- **batch2_content_covered**: True

## 六、Batch2 当前分类统计

### section-prefix 统计

- **算法**: 323
- **数学**: 167
- **数据结构**: 110
- **合计**: 600

### 预期统计

- **算法**: 323
- **数据结构**: 110
- **数学**: 167
- **合计**: 600

说明：item.category 统计与 section-prefix 统计可能不同；checkpoint 使用 section-prefix 统计；当前 checkpoint 正式报告如果尚未重生成，旧报告中的'数据结构 0'仍是过期报告结果。

## 七、Batch3 是否具备启动条件

- **ready**: False
- **reason**: 剩余候选 141 个，建议先补依赖和 section_id，再做 30-50 个候选试点; 依赖缺失比例 100%，建议先补依赖

### 阻塞项

- 剩余候选 141 个，建议先补依赖和 section_id，再做 30-50 个候选试点
- 依赖缺失比例 100%，建议先补依赖

## 八、下一步建议

1. 不建议立即进入 Batch3。
2. 应先补依赖和 section_id，再做 30-50 个候选试点。
3. 如果后续重生成 checkpoint 报告，确保使用修复后的统计口径。

## 九、声明

- 本轮只读审计，未修改主图谱、前端图谱、内容索引、内容正文、已有报告。
- 未进入 Batch3。
- 未生成新节点。
- 未删除节点。
