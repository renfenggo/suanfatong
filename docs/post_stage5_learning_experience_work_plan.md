# Post-Stage5 Learning Experience Work Plan

## Current Direction

The project should not rush from 3240 knowledge points to 6000. The better path is:

1. Stabilize the current 3240-point graph.
2. Improve learning experience and readability.
3. Run a small Batch3 pilot only after dependencies and sections are ready.
4. Re-evaluate the final target size after quality improves.

Recommended target range:

- Short term: 3600
- Medium term: 4200
- Long-term upper bound: 4800
- Avoid treating 6000 as a hard target unless later evidence shows real need.

## Phase 1: Current State Acceptance

Goal: Freeze a reliable baseline after Threads 1, 2, and 3.

Tasks:

- Run Stage5 current-state acceptance audit.
- Verify Thread 1 persistent segment tree section fixes.
- Verify Thread 2 checkpoint category logic fix.
- Verify Thread 3 Batch3 readiness report.
- Verify global 3240 stability.

Expected outputs:

- `tools/audit_stage5_current_state_acceptance.py`
- `docs/stage5_current_state_acceptance_report.md`
- `data/stage5_current_state_acceptance_report.json`

Exit criteria:

- Main graph item_count = 3240.
- Frontend graph item_count = 3240.
- Main/frontend ID sets match.
- Content coverage = 3240/3240.
- Batch2 content coverage = 600/600.
- Batch2 section-prefix stats = algorithm 323, data structure 110, math 167.
- Batch3 is not started yet.

## Phase 2: Turn The Graph Into Learning Paths

Goal: Convert the 3240-point graph from a knowledge warehouse into a learning system.

Use existing dependency fields:

- `direct_pre`: display as must-learn prerequisites.
- `resolved_pre`: use internally for unlock/path ordering.
- `rel`: display as related or after-learning exploration.

Add or derive learner-facing layers:

- Core path
- Common advanced path
- Topic extension
- Optional/cold topic

Recommended learning card structure:

- One-sentence explanation
- When to use it
- Must-learn prerequisites
- Recommended prerequisites
- Core intuition
- Minimal example
- Common traps
- Practice entry
- What to learn next

Start with three sample chapters:

- `2.8` Dynamic Programming
- `3.13` Advanced Data Structure Extensions
- `4.1` Integer and Number Theory Basics

Do not process all 3240 points at once. Build high-quality samples first.

## Phase 3: Animation Coverage Audit

Goal: Identify which knowledge points deserve dynamic visualization.

Do not animate every node. Prioritize process-based and state-based topics.

Best animation candidates:

- BFS / DFS
- Binary search
- Prefix sum / difference
- Union find
- Heap
- Monotonic stack / queue
- Fenwick tree
- Segment tree
- Lazy propagation
- Dijkstra
- Topological sort
- Kruskal
- Tarjan SCC
- KMP
- Trie
- 0/1 knapsack
- LIS
- Interval DP
- Tree DP
- State compression DP
- Fast exponentiation
- Euclidean algorithm
- Sieve
- Combination recurrence
- Persistent segment tree basics

Recommended outputs:

- `tools/audit_animation_coverage.py`
- `docs/animation_coverage_audit_report.md`
- `data/animation_coverage_audit.json`

Priority labels:

- P0: must-have, high learning value
- P1: useful for advanced learning
- P2: optional

Initial target: 30-50 P0 animations.

## Phase 4: Batch3 Pilot

Goal: Validate the pipeline with a small, high-quality batch.

Do not run a large Batch3 yet.

Prerequisites:

- Thread 3 readiness report is accepted.
- Remaining candidates have dependency and section metadata.
- No negative safe candidate count.
- Risk ratio is valid.
- Candidate pool conflicts are explained.

Recommended pilot size:

- 30-50 nodes

Pilot requirements:

- Select high-value candidates only.
- Fill `section_id`, `category`, `subcategory`.
- Fill `direct_pre`.
- Compute `resolved_pre`.
- Add useful `rel`.
- Generate content package.
- Sync frontend graph.
- Validate graph and content coverage.

## Phase 5: Reconsider Final Scale

Do not treat 6000 as mandatory.

Current count:

- 3240 knowledge points
- 65 sections

Recommended future targets:

- 3600: short-term quality-first target
- 4200: best medium-term target
- 4800: long-term upper bound

Before increasing the target, evaluate:

- Are learning paths understandable?
- Are content cards high quality?
- Are dependencies useful to learners?
- Are animations covering core hard topics?
- Can the frontend handle the graph without overwhelming users?
- Do users actually need more nodes?

## Immediate Next Step

Wait for Thread 1 to finish the Stage5 current-state acceptance audit.

After Thread 1 returns:

1. Independently verify its report.
2. If accepted, freeze the 3240 baseline.
3. Start Phase 2 with learning card/path samples for `2.8`, `3.13`, and `4.1`.

Do not open Thread 4 for expansion until the acceptance audit is complete and the final target is re-evaluated.
