import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/bfs_step.dart';
import '../models/animation_scenario.dart';
import '../repositories/animation_repository.dart';
import 'content_manifest_provider.dart';

final animationRepositoryProvider = Provider((ref) {
  return AnimationRepository(jsonRepo: ref.watch(jsonAssetRepositoryProvider));
});

final animationScenarioProvider = FutureProvider.family<List<BfsStep>, String>((
  ref,
  scenarioId,
) {
  final manifestAsync = ref.watch(contentManifestProvider);
  return manifestAsync.when(
    data: (manifest) {
      final repo = ref.read(animationRepositoryProvider);
      return repo.loadAnimationScenario(
        manifest,
        manifest.defaultTopicId,
        scenarioId,
      );
    },
    loading: () => Future.value(const []),
    error: (_, __) => Future.value(const []),
  );
});

final animationScenarioConfigProvider =
    FutureProvider.family<AnimationScenario?, String>((ref, scenarioId) {
      final manifestAsync = ref.watch(contentManifestProvider);
      return manifestAsync.when(
        data: (manifest) {
          final topic = manifest.defaultTopic;
          return topic.findAnimationScenario(scenarioId);
        },
        loading: () => null,
        error: (_, __) => null,
      );
    });
