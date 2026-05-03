import 'package:flutter/material.dart';
import '../pages/home_page.dart';
import '../pages/lesson_page.dart';
import '../pages/animation_page.dart';
import '../pages/quiz_page.dart';
import '../pages/mistake_page.dart';
import '../pages/teacher_mode_page.dart';
import '../pages/progress_page.dart';
import '../pages/settings_page.dart';

class AppRouter {
  static const String home = '/';
  static const String lesson = '/lesson';
  static const String animation = '/animation';
  static const String quiz = '/quiz';
  static const String mistake = '/mistake';
  static const String teacherMode = '/teacher';
  static const String progress = '/progress';
  static const String settings = '/settings';

  static final Map<String, WidgetBuilder> routes = {
    home: (context) => const HomePage(),
    lesson: (context) => const LessonPage(),
    animation: (context) => const AnimationPage(),
    quiz: (context) => const QuizPage(),
    mistake: (context) => const MistakePage(),
    teacherMode: (context) => const TeacherModePage(),
    progress: (context) => const ProgressPage(),
    settings: (context) => const SettingsPage(),
  };
}
