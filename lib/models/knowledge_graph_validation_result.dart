class KnowledgeGraphValidationResult {
  final List<String> duplicateSectionIds;
  final List<String> duplicateItemIds;
  final List<String> missingParents;
  final List<String> missingRefs;
  final bool hasCycle;
  final List<String> cycleNodes;

  const KnowledgeGraphValidationResult({
    this.duplicateSectionIds = const [],
    this.duplicateItemIds = const [],
    this.missingParents = const [],
    this.missingRefs = const [],
    this.hasCycle = false,
    this.cycleNodes = const [],
  });

  bool get isValid =>
      duplicateSectionIds.isEmpty &&
      duplicateItemIds.isEmpty &&
      missingParents.isEmpty &&
      !hasCycle;
}
