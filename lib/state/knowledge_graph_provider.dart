import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/knowledge_graph.dart';
import '../models/knowledge_graph_validation_result.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_section.dart';
import '../repositories/knowledge_graph_repository.dart';
import 'content_manifest_provider.dart';

final knowledgeGraphRepositoryProvider = Provider((ref) {
  return KnowledgeGraphRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final knowledgeGraphProvider = FutureProvider<KnowledgeGraph>((ref) {
  return ref.watch(knowledgeGraphRepositoryProvider).loadGraph();
});

final knowledgeGraphValidationProvider =
    FutureProvider<KnowledgeGraphValidationResult>((ref) {
      final graphAsync = ref.watch(knowledgeGraphProvider);
      return graphAsync.when(
        data: (graph) {
          final repo = ref.read(knowledgeGraphRepositoryProvider);
          return repo.validateGraph(graph);
        },
        loading: () => const KnowledgeGraphValidationResult(),
        error: (_, __) => const KnowledgeGraphValidationResult(),
      );
    });

final knowledgeItemProvider = FutureProvider.family<KnowledgeItem?, String>((
  ref,
  itemId,
) {
  final graphAsync = ref.watch(knowledgeGraphProvider);
  return graphAsync.when(
    data: (graph) => graph.itemById(itemId),
    loading: () => null,
    error: (_, __) => null,
  );
});

final knowledgeSectionProvider =
    FutureProvider.family<KnowledgeSection?, String>((ref, sectionId) {
      final graphAsync = ref.watch(knowledgeGraphProvider);
      return graphAsync.when(
        data: (graph) => graph.sectionById(sectionId),
        loading: () => null,
        error: (_, __) => null,
      );
    });

final pickupGroupItemsProvider =
    FutureProvider.family<List<KnowledgeItem>, String>((ref, pickupGroup) {
      final graphAsync = ref.watch(knowledgeGraphProvider);
      return graphAsync.when(
        data: (graph) => graph.itemsByPickupGroup(pickupGroup),
        loading: () => const [],
        error: (_, __) => const [],
      );
    });
