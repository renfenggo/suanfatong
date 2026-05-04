import '../models/quiz.dart';
import '../models/content_manifest.dart';
import 'json_asset_repository.dart';

class QuizRepository {
  final JsonAssetRepository _jsonRepo;

  QuizRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<List<Quiz>> loadQuizSet(
    ContentManifest manifest,
    String topicId,
    String quizSetId,
  ) async {
    final topic = manifest.findTopic(topicId);
    if (topic == null) {
      throw StateError('Topic "$topicId" not found in manifest');
    }
    final quizSet = topic.findQuizSet(quizSetId);
    if (quizSet == null) {
      throw StateError('QuizSet "$quizSetId" not found in topic "$topicId"');
    }
    final list = await _jsonRepo.loadList(quizSet.assetPath);
    return list.map((e) => Quiz.fromJson(e as Map<String, dynamic>)).toList();
  }
}
