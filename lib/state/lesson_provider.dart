import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/lesson.dart';
import '../services/lesson_service.dart';

final lessonServiceProvider = Provider((ref) => LessonService());

final lessonsProvider = FutureProvider.family<List<Lesson>, String>((
  ref,
  assetPath,
) {
  return ref.watch(lessonServiceProvider).loadLessons(assetPath);
});
