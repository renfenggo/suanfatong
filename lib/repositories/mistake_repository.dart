import '../models/mistake.dart';
import '../models/content_manifest.dart';
import 'json_asset_repository.dart';

class MistakeRepository {
  final JsonAssetRepository _jsonRepo;

  MistakeRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<List<Mistake>> loadMistakeSet(
    ContentManifest manifest,
    String topicId,
    String mistakeSetId,
  ) async {
    final topic = manifest.findTopic(topicId);
    if (topic == null) {
      throw StateError('Topic "$topicId" not found in manifest');
    }
    final mistakeSet = topic.findMistakeSet(mistakeSetId);
    if (mistakeSet == null) {
      throw StateError(
        'MistakeSet "$mistakeSetId" not found in topic "$topicId"',
      );
    }
    final list = await _jsonRepo.loadList(mistakeSet.assetPath);
    return list
        .map((e) => Mistake.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
