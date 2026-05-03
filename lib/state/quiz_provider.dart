import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/quiz.dart';
import '../services/quiz_service.dart';

final quizServiceProvider = Provider((ref) => QuizService());

final quizzesProvider = FutureProvider.family<List<Quiz>, String>((
  ref,
  assetPath,
) {
  return ref.watch(quizServiceProvider).loadQuizzes(assetPath);
});
