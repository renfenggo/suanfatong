import '../models/bfs_step.dart';
import '../models/content_manifest.dart';
import 'json_asset_repository.dart';

class AnimationRepository {
  final JsonAssetRepository _jsonRepo;

  AnimationRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<List<BfsStep>> loadAnimationScenario(
    ContentManifest manifest,
    String topicId,
    String scenarioId,
  ) async {
    final topic = manifest.findTopic(topicId);
    if (topic == null) {
      throw StateError('Topic "$topicId" not found in manifest');
    }
    final scenario = topic.findAnimationScenario(scenarioId);
    if (scenario == null) {
      throw StateError(
        'AnimationScenario "$scenarioId" not found in topic "$topicId"',
      );
    }
    final list = await _jsonRepo.loadList(scenario.assetPath);
    return list
        .map((e) => BfsStep.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
