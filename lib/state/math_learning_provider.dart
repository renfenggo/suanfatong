import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cpp_learning_unit.dart';
import '../repositories/math_learning_repository.dart';
import 'content_manifest_provider.dart';

final mathLearningRepositoryProvider = Provider((ref) {
  return MathLearningRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final mathLearningContentProvider = FutureProvider<CppLearningContent>((ref) {
  return ref.watch(mathLearningRepositoryProvider).loadContent();
});

final mathLearningUnitByItemIdProvider =
    FutureProvider.family<CppLearningUnit?, String>((ref, itemId) {
      final contentAsync = ref.watch(mathLearningContentProvider);
      return contentAsync.when(
        data: (content) => content.unitByItemId(itemId),
        loading: () => null,
        error: (_, __) => null,
      );
    });
