import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/mistake.dart';
import '../repositories/mistake_repository.dart';
import 'content_manifest_provider.dart';

final mistakeRepositoryProvider = Provider((ref) {
  return MistakeRepository(jsonRepo: ref.watch(jsonAssetRepositoryProvider));
});

final mistakeSetProvider = FutureProvider.family<List<Mistake>, String>((
  ref,
  mistakeSetId,
) {
  final manifestAsync = ref.watch(contentManifestProvider);
  return manifestAsync.when(
    data: (manifest) {
      final repo = ref.read(mistakeRepositoryProvider);
      return repo.loadMistakeSet(
        manifest,
        manifest.defaultTopicId,
        mistakeSetId,
      );
    },
    loading: () => Future.value(const []),
    error: (_, __) => Future.value(const []),
  );
});
