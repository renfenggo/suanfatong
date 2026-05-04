import '../services/history_service.dart';
import '../models/answer_record.dart';

class AnswerHistoryRepository {
  final HistoryService _service;

  AnswerHistoryRepository({required HistoryService service})
    : _service = service;

  Future<List<AnswerRecord>> loadHistory(String topic) =>
      _service.loadHistory(topic);

  Future<void> appendRecord(String topic, AnswerRecord record) =>
      _service.appendRecord(topic, record);

  Future<void> clearTopic(String topic) => _service.clearTopic(topic);

  Future<void> clearAll() => _service.clearAll();

  Future<Map<String, int>> getTopicStats(String topic) =>
      _service.getTopicStats(topic);
}
