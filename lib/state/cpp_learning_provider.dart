import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cpp_learning_unit.dart';
import '../repositories/cpp_learning_repository.dart';
import 'content_manifest_provider.dart';

final cppLearningRepositoryProvider = Provider((ref) {
  return CppLearningRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final cppLearningContentProvider = FutureProvider<CppLearningContent>((ref) {
  return ref.watch(cppLearningRepositoryProvider).loadContent();
});

final cppLearningUnitByItemIdProvider =
    FutureProvider.family<CppLearningUnit?, String>((ref, itemId) {
      final contentAsync = ref.watch(cppLearningContentProvider);
      return contentAsync.when(
        data: (content) => content.unitByItemId(itemId),
        loading: () => null,
        error: (_, __) => null,
      );
    });
