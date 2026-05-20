import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cpp_learning_unit.dart';
import '../repositories/algorithm_learning_repository.dart';
import 'content_manifest_provider.dart';

final algorithmLearningRepositoryProvider = Provider((ref) {
  return AlgorithmLearningRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final algorithmLearningContentProvider = FutureProvider<CppLearningContent>((
  ref,
) {
  return ref.watch(algorithmLearningRepositoryProvider).loadContent();
});

final algorithmLearningUnitByItemIdProvider =
    FutureProvider.family<CppLearningUnit?, String>((ref, itemId) {
      final contentAsync = ref.watch(algorithmLearningContentProvider);
      return contentAsync.when(
        data: (content) => content.unitByItemId(itemId),
        loading: () => null,
        error: (_, __) => null,
      );
    });
