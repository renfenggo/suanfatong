import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/quiz.dart';
import '../repositories/quiz_repository.dart';
import 'content_manifest_provider.dart';

final quizRepositoryProvider = Provider((ref) {
  return QuizRepository(jsonRepo: ref.watch(jsonAssetRepositoryProvider));
});

final quizSetProvider = FutureProvider.family<List<Quiz>, String>((
  ref,
  quizSetId,
) {
  final manifestAsync = ref.watch(contentManifestProvider);
  return manifestAsync.when(
    data: (manifest) {
      final repo = ref.read(quizRepositoryProvider);
      return repo.loadQuizSet(manifest, manifest.defaultTopicId, quizSetId);
    },
    loading: () => Future.value(const []),
    error: (_, __) => Future.value(const []),
  );
});
