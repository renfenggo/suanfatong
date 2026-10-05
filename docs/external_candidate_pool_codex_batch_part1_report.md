# External Candidate Pool Codex Batch Part 1 Report

## Raw 文件读取结果
- Raw file exists: True
- Legal JSON array extracted: True
- Raw candidates extracted: 26
- Repaired candidates: 0
- Discarded candidates: 0
- Missing older candidate files: data/candidate_new_knowledge_items_batch1_round3.json

## Candidate Summary
- cleaned candidate count: 26
- added candidate count: 314
- combined candidate total: 340
- advanced graph count: 170
- advanced data structure count: 170

## Merge Action Distribution
- add_new: 226
- add_as_subtopic: 104
- merge_with_existing: 1
- reject: 0
- manual_review: 9
- move_to_problem_patterns: 0

## Duplicate Risk Distribution
- none: 0
- low: 226
- medium: 113
- high: 1

## Dependency Review
- empty direct_pre_name_suggestion count: 0
- has section id dependency: False
- dangling dependency count: 0
- has candidate dependency cycle: False

## I18n Review
- i18n seed covers all candidates: True

## Highest Duplicate Risk Candidates
- `cand.graph.virtual_tree.construction` Virtual Tree Construction -> merge_with_existing (exact name/en_name appears in existing graph)

## Next Stage Recommendation
- Recommended for next merge review: 330
- Prefer reviewing `add_as_subtopic` entries before `add_new`, because many advanced topics should attach under existing fundamentals.
- Keep this pool external until duplicate and dependency names are mapped to formal item ids.

## Main Graph Safety
- Main graph categories / sections / items modified: false
- Main graph item_count before validation: 1349
- validate-only status: passed
- validate-only item_count: 1349
