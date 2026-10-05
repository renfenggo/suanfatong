# Knowledge Item Development Guidelines

## Purpose

This project is an algorithm encyclopedia and global training platform. The knowledge graph should not only store core algorithms and data structures, but also describe common modeling situations, implementation variants, theorem variants, and training-oriented transformations in detail.

Detailed modeling coverage is a product goal, not a quality problem. Future expansion reviews must distinguish between "bad over-splitting" and "valuable fine-grained modeling coverage".

## Item Types

Every newly added knowledge node should be reviewed with an explicit conceptual type.

Recommended `item_type` values:

- `core_concept`: stable algorithm, data structure, theorem, or foundational concept.
- `modeling_pattern`: a recurring problem-modeling situation or transformation.
- `implementation_variant`: a concrete implementation method, optimization, or data-structure variant.
- `application_case`: a named application scenario of a core concept.
- `theorem_or_property`: theorem, lemma, invariant, or structural property.
- `training_signal`: a recognizable signal that helps learners map problems to methods.

If the schema does not yet contain `item_type`, reviewers should still use this classification in audit reports and action plans.

## Fine-Grained Modeling Rule

Fine-grained nodes are allowed when they help learners recognize different cases under the same family.

Examples that may be valid as fine-grained nodes:

- Maximum Closure: Project Selection, Open Pit Mining Model, Task Selection.
- Graph Modeling: Layered Graph, State Graph, Time Expanded Graph, K Shortest Paths.
- Flow with Lower Bounds: Node Demand, Minimum Flow, Project Selection.
- Virtual Tree: Multi-Key Query, Subtree Aggregation, Distance Compression.
- Persistent Data Structure: Fat Node Method, Path Copying Method, Rollback vs Persistence.

These nodes should not be rejected only because they are specific. They should be placed under the correct parent concept and marked as modeling/application/implementation nodes.

## Layering Rule

Fine-grained nodes must be layered under a stable parent concept.

Recommended fields or review metadata:

- `parent_concept_id`: the core item this node belongs to.
- `item_type`: conceptual role of the node.
- `modeling_family`: modeling family name, such as `maximum_closure`, `layered_graph_modeling`, or `virtual_tree_queries`.
- `training_value`: why this node helps problem recognition or solution transfer.
- `show_in_learning_path`: whether it should appear in the main progressive learning path.
- `show_in_encyclopedia`: whether it should appear in encyclopedia browsing.
- `sync_to_problem_patterns`: whether it should also appear in problem pattern training.

Default recommendation:

- Core concepts: show in encyclopedia and learning path.
- Modeling patterns: show in encyclopedia under the parent concept, and sync to problem patterns.
- Implementation variants: show in encyclopedia; include in learning path only for advanced tracks.
- Application cases: show under the parent concept; usually do not block progression.
- Training signals: prefer problem patterns unless they are widely accepted named concepts.

## Review Standards

Do not judge all nodes by the same "independent algorithm concept" standard.

Use these decisions:

- `keep_as_core_item`: independent core concept.
- `keep_as_modeling_item`: valid fine-grained modeling case.
- `keep_as_implementation_variant`: valid implementation variant.
- `keep_as_application_case`: valid application scenario under a parent concept.
- `sync_to_problem_patterns`: keep in graph and also expose in pattern training.
- `collapse_to_parent`: too small to stand alone; keep as subtopic or alias.
- `merge_with_existing`: duplicate or near-duplicate of an existing item.
- `reject_later`: unstable, unclear, or low educational value.

## Dependency Rule

Fine-grained modeling nodes should not all depend only on a broad basic item. They should normally depend on:

- the direct parent concept;
- the core algorithm or data structure used by the modeling situation;
- one or two important prerequisite concepts needed to understand the transformation.

Example:

- Project Selection should depend on the relevant network-flow/min-cut or maximum-closure concept.
- Layered Graph should depend on shortest path or graph search basics, plus the parent graph-modeling concept.
- Fat Node Method should depend on persistent data structure and the underlying structure being made persistent.

If many sibling nodes have identical `direct_pre`, this is not automatically wrong, but it should trigger a parent-concept review:

- If the siblings are genuinely different recognizable modeling cases, keep them as modeling items.
- If the siblings are only wording variants, collapse them to aliases or subtopics.

## Problem Patterns Relationship

`knowledge_item` and `problem_patterns` are not mutually exclusive.

A modeling node can be:

- kept as a knowledge item for encyclopedia navigation;
- linked under its parent concept;
- also synced to `problem_patterns` for training, recognition signals, and example problem mapping.

Prefer "sync to problem_patterns" over "move out of knowledge graph" when the node has clear educational value and belongs to a known modeling family.

## Batch Expansion Guidance

For future Stage3F/Batch5-style expansion:

1. Continue adding fine-grained modeling cases when they improve coverage.
2. Require every fine-grained node to declare or imply a parent concept.
3. Avoid adding many sibling nodes without a family-level summary item.
4. Use smaller batches when a batch contains mostly modeling/application variants.
5. Review with two separate questions:
   - Is this valid as a detailed modeling/application/implementation node?
   - Should it appear in the main learning path, or only under encyclopedia/problem-pattern views?

## Product Principle

The goal is not to keep the graph small. The goal is to make the graph detailed, navigable, and teachable.

Fine granularity is good when it helps learners recognize more problem situations. Fine granularity is bad only when it creates duplicate names, unclear parentage, weak dependencies, or noisy learning-path progression.
