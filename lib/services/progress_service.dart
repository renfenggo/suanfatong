import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/progress.dart';

class ProgressService {
  static const _key = 'bfs_learn_progress';

  Future<Progress> loadProgress() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString(_key);
    if (jsonStr == null) return const Progress();
    return Progress.fromJson(json.decode(jsonStr) as Map<String, dynamic>);
  }

  Future<void> saveProgress(Progress progress) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, json.encode(progress.toJson()));
  }
}
