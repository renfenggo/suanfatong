# Thread2 Stage3E-Aggressive Plan Report

This is a planning-only audit. No candidate was merged and the main graph was not modified.

## Required Summary

| Metric | Count |
|---|---:|
| 外部候选总数 | 340 |
| 已合并数量 | 133 |
| 未合并数量 | 207 |
| 可进入 aggressive pool 数量 | 167 |
| 进入 150 计划数量 | 150 |
| green 数量 | 85 |
| yellow 数量 | 82 |
| red 数量 | 173 |
| problem_patterns 排除数量 | 35 |
| manual_review 排除数量 | 4 |
| high duplicate risk 排除数量 | 1 |
| 依赖问题数量 | 0 |
| 主图谱是否被修改 | 否 |
| validate-only 是否 passed | 是 |

## Batch Plan

| Batch | Count | Risk | 2.21 | 3.13 | Other Sections | Risk Distribution |
|---|---:|---|---:|---:|---|---|
| batch_1 | 30 | lowest | 30 | 0 | 0 | {"green":30} |
| batch_2 | 30 | low | 24 | 6 | 0 | {"green":30} |
| batch_3 | 30 | mid_low | 5 | 25 | 0 | {"green":25,"yellow":5} |
| batch_4 | 30 | medium_controlled | 18 | 12 | 0 | {"yellow":30} |
| batch_5 | 30 | optional_remaining | 0 | 30 | 0 | {"yellow":30} |

## Validate-Only

- passed: true
- item_count: 1482
- section_count: 65
- mode: read-only, no validation file write

## Rules Applied

- Excluded Stage3B / Stage3C / Stage3D merged candidates.
- Excluded high duplicate risk, reject, merge_with_existing, obvious problem_patterns, unmapped direct_pre, and candidates needing new sections.
- Red candidates are not included in any batch.
- Candidate dependency cycle check: no batch introduces candidate-to-candidate dependency edges; all mapped direct_pre targets are existing graph nodes, so each batch is cycle-free by construction.
- Existing sections 2.21 and 3.13 were prioritized in sorting and batch allocation.

## Files

- data/thread2_stage3e_aggressive_candidate_pool.json
- data/thread2_stage3e_aggressive_batches.json
- data/thread2_stage3e_aggressive_risk_review.json
