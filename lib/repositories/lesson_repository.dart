import '../models/lesson.dart';
import '../models/content_manifest.dart';
import 'json_asset_repository.dart';

class LessonRepository {
  final JsonAssetRepository _jsonRepo;

  LessonRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<List<Lesson>> loadLessonSet(
    ContentManifest manifest,
    String topicId,
    String lessonSetId,
  ) async {
    final topic = manifest.findTopic(topicId);
    if (topic == null) {
      throw StateError('Topic "$topicId" not found in manifest');
    }
    final lessonSet = topic.findLessonSet(lessonSetId);
    if (lessonSet == null) {
      throw StateError(
        'LessonSet "$lessonSetId" not found in topic "$topicId"',
      );
    }
    final list = await _jsonRepo.loadList(lessonSet.assetPath);
    return list.map((e) => Lesson.fromJson(e as Map<String, dynamic>)).toList();
  }
}
