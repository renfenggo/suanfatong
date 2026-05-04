import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cpp_animation.dart';
import '../repositories/cpp_animation_repository.dart';
import 'content_manifest_provider.dart';

final cppAnimationRepositoryProvider = Provider((ref) {
  return CppAnimationRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final cppAnimationManifestProvider = FutureProvider<CppAnimationManifest>((
  ref,
) {
  return ref.watch(cppAnimationRepositoryProvider).loadManifest();
});

final cppAnimationProvider = FutureProvider.family<CppAnimation, String>((
  ref,
  animationId,
) {
  return ref.watch(cppAnimationRepositoryProvider).loadAnimation(animationId);
});

final cppAnimationsForItemProvider =
    FutureProvider.family<List<CppAnimationMeta>, String>((ref, itemId) {
      return ref
          .watch(cppAnimationRepositoryProvider)
          .animationsForItem(itemId);
    });
