import '../models/knowledge_graph.dart';
import '../models/knowledge_graph_validation_result.dart';
import 'json_asset_repository.dart';

class KnowledgeGraphRepository {
  final JsonAssetRepository _jsonRepo;
  static const _assetPath = 'assets/data/knowledge/io_v4_4.json';

  KnowledgeGraphRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<KnowledgeGraph> loadGraph() async {
    final map = await _jsonRepo.loadMap(_assetPath);
    return KnowledgeGraph.fromJson(map);
  }

  KnowledgeGraphValidationResult validateGraph(KnowledgeGraph graph) {
    final duplicateSectionIds = <String>[];
    final duplicateItemIds = <String>[];
    final missingParents = <String>[];
    final missingRefs = <String>[];

    final sectionIdSet = <String>{};
    final itemIdSet = <String>{};

    for (final section in graph.allSections) {
      if (!sectionIdSet.add(section.id)) {
        duplicateSectionIds.add(section.id);
      }
    }

    final allSectionIds = sectionIdSet;

    for (final item in graph.allItems) {
      if (!itemIdSet.add(item.id)) {
        duplicateItemIds.add(item.id);
      }
    }

    final allItemIds = itemIdSet;

    for (final item in graph.allItems) {
      if (item.parent.isNotEmpty && !allSectionIds.contains(item.parent)) {
        missingParents.add(item.id);
      }

      for (final ref in item.resolvedPre) {
        if (!allItemIds.contains(ref) && !allSectionIds.contains(ref)) {
          missingRefs.add('${item.id} -> $ref');
        }
      }
    }

    final cycleResult = _detectCycles(graph);

    return KnowledgeGraphValidationResult(
      duplicateSectionIds: duplicateSectionIds,
      duplicateItemIds: duplicateItemIds,
      missingParents: missingParents,
      missingRefs: missingRefs,
      hasCycle: cycleResult.hasCycle,
      cycleNodes: cycleResult.cycleNodes,
    );
  }

  _CycleResult _detectCycles(KnowledgeGraph graph) {
    final allItems = graph.allItems;
    final itemIdSet = allItems.map((e) => e.id).toSet();

    final adjacency = <String, List<String>>{};
    for (final item in allItems) {
      adjacency[item.id] =
          item.resolvedPre.where((pre) => itemIdSet.contains(pre)).toList();
    }

    final visited = <String>{};
    final inStack = <String>{};
    final cycleNodes = <String>[];

    bool dfs(String nodeId) {
      visited.add(nodeId);
      inStack.add(nodeId);

      for (final pre in adjacency[nodeId] ?? const []) {
        if (!visited.contains(pre)) {
          if (dfs(pre)) return true;
        } else if (inStack.contains(pre)) {
          cycleNodes.add(pre);
          return true;
        }
      }

      inStack.remove(nodeId);
      return false;
    }

    for (final item in allItems) {
      if (!visited.contains(item.id)) {
        if (dfs(item.id)) {
          return _CycleResult(hasCycle: true, cycleNodes: cycleNodes);
        }
      }
    }

    return _CycleResult(hasCycle: false, cycleNodes: const []);
  }
}

class _CycleResult {
  final bool hasCycle;
  final List<String> cycleNodes;

  const _CycleResult({required this.hasCycle, required this.cycleNodes});
}
