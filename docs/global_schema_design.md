# Global Schema Design

This stage upgrades the existing 1349-node knowledge graph into a product-ready data model for an algorithm encyclopedia and global training platform.

The design separates knowledge items, problem patterns, problem references, i18n terms, and learning paths. Problem references store metadata only and never copy problem statements.

## Knowledge Item Development Rule

The graph is allowed to include fine-grained modeling situations, implementation variants, and application cases. These nodes are part of the product goal: detailed coverage for an algorithm encyclopedia and training platform.

Future reviews should not reject a node only because it is specific. Instead, classify it as a core concept, modeling pattern, implementation variant, application case, theorem/property, or training signal. Detailed modeling nodes should be attached to a stable parent concept and may also be synced to problem patterns.

See `docs/knowledge_item_development_guidelines.md` for the full development guideline.
