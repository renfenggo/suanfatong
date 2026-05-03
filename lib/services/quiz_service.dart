import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/quiz.dart';

class QuizService {
  Future<List<Quiz>> loadQuizzes(String assetPath) async {
    final jsonStr = await rootBundle.loadString(assetPath);
    final List<dynamic> jsonList = json.decode(jsonStr);
    return jsonList
        .map((e) => Quiz.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
