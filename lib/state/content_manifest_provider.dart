import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repositories/json_asset_repository.dart';
import '../repositories/content_manifest_repository.dart';
import '../models/content_manifest.dart';

final jsonAssetRepositoryProvider = Provider((ref) => JsonAssetRepository());

final contentManifestRepositoryProvider = Provider((ref) {
  return ContentManifestRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final contentManifestProvider = FutureProvider<ContentManifest>((ref) {
  return ref.watch(contentManifestRepositoryProvider).loadManifest();
});

class DefaultContentIds {
  final String topicId;
  final String lessonSetId;
  final String quizSetId;
  final String mistakeSetId;
  final String animationScenarioId;

  const DefaultContentIds({
    this.topicId = '',
    required this.lessonSetId,
    required this.quizSetId,
    required this.mistakeSetId,
    required this.animationScenarioId,
  });
}

final defaultContentIdsProvider = FutureProvider<DefaultContentIds>((ref) {
  final manifestAsync = ref.watch(contentManifestProvider);
  return manifestAsync.when(
    data: (manifest) {
      final topic = manifest.defaultTopic;
      return DefaultContentIds(
        topicId: manifest.defaultTopicId,
        lessonSetId:
            topic.lessonSets.isNotEmpty
                ? topic.lessonSets.first.lessonSetId
                : '',
        quizSetId:
            topic.quizSets.isNotEmpty ? topic.quizSets.first.quizSetId : '',
        mistakeSetId:
            topic.mistakeSets.isNotEmpty
                ? topic.mistakeSets.first.mistakeSetId
                : '',
        animationScenarioId:
            topic.animationScenarios.isNotEmpty
                ? topic.animationScenarios.first.scenarioId
                : '',
      );
    },
    loading:
        () => const DefaultContentIds(
          lessonSetId: '',
          quizSetId: '',
          mistakeSetId: '',
          animationScenarioId: '',
        ),
    error:
        (_, __) => const DefaultContentIds(
          lessonSetId: '',
          quizSetId: '',
          mistakeSetId: '',
          animationScenarioId: '',
        ),
  );
});
