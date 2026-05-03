import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/lesson.dart';

class LessonService {
  Future<List<Lesson>> loadLessons(String assetPath) async {
    final jsonStr = await rootBundle.loadString(assetPath);
    final List<dynamic> jsonList = json.decode(jsonStr);
    return jsonList
        .map((e) => Lesson.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
