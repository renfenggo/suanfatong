import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/lesson.dart';
import '../repositories/lesson_repository.dart';
import 'content_manifest_provider.dart';

final lessonRepositoryProvider = Provider((ref) {
  return LessonRepository(jsonRepo: ref.watch(jsonAssetRepositoryProvider));
});

final lessonSetProvider = FutureProvider.family<List<Lesson>, String>((
  ref,
  lessonSetId,
) {
  final manifestAsync = ref.watch(contentManifestProvider);
  return manifestAsync.when(
    data: (manifest) {
      final repo = ref.read(lessonRepositoryProvider);
      return repo.loadLessonSet(manifest, manifest.defaultTopicId, lessonSetId);
    },
    loading: () => Future.value(const []),
    error: (_, __) => Future.value(const []),
  );
});
