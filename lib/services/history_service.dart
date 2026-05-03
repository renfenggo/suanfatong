import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../models/answer_record.dart';

class HistoryService {
  static const _maxPerTopic = 500;

  Future<Directory> _getDir() async {
    final appDir = await getApplicationDocumentsDirectory();
    final dir = Directory('${appDir.path}/history');
    if (!await dir.exists()) {
      await dir.create(recursive: true);
    }
    return dir;
  }

  Future<List<AnswerRecord>> loadHistory(String topic) async {
    try {
      final dir = await _getDir();
      final file = File('${dir.path}/$topic.json');
      if (!await file.exists()) return const [];
      final content = await file.readAsString();
      final List<dynamic> list = json.decode(content);
      return list
          .map((e) => AnswerRecord.fromJson(e as Map<String, dynamic>))
          .toList();
    } catch (_) {
      return const [];
    }
  }

  Future<void> saveHistory(String topic, List<AnswerRecord> records) async {
    try {
      final dir = await _getDir();
      final file = File('${dir.path}/$topic.json');
      final trimmed =
          records.length > _maxPerTopic
              ? records.sublist(records.length - _maxPerTopic)
              : records;
      final jsonStr = json.encode(trimmed.map((r) => r.toJson()).toList());
      await file.writeAsString(jsonStr);
    } catch (_) {}
  }

  Future<void> appendRecord(String topic, AnswerRecord record) async {
    final records = await loadHistory(topic);
    records.add(record);
    await saveHistory(topic, records);
  }

  Future<void> clearTopic(String topic) async {
    try {
      final dir = await _getDir();
      final file = File('${dir.path}/$topic.json');
      if (await file.exists()) await file.delete();
    } catch (_) {}
  }

  Future<void> clearAll() async {
    try {
      final dir = await _getDir();
      if (await dir.exists()) await dir.delete(recursive: true);
    } catch (_) {}
  }

  Future<Map<String, int>> getTopicStats(String topic) async {
    final records = await loadHistory(topic);
    int correct = 0;
    int wrong = 0;
    final uniqueIds = <String>{};
    for (final r in records) {
      uniqueIds.add(r.quizId);
      if (r.correct) {
        correct++;
      } else {
        wrong++;
      }
    }
    return {
      'total': records.length,
      'correct': correct,
      'wrong': wrong,
      'unique': uniqueIds.length,
    };
  }
}
