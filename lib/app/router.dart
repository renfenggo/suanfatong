import 'package:flutter/material.dart';
import '../pages/home_page.dart';
import '../pages/lesson_page.dart';
import '../pages/animation_page.dart';
import '../pages/quiz_page.dart';
import '../pages/mistake_page.dart';
import '../pages/teacher_mode_page.dart';
import '../pages/progress_page.dart';
import '../pages/settings_page.dart';
import '../pages/knowledge_map_page.dart';
import '../pages/knowledge_section_page.dart';
import '../pages/knowledge_item_page.dart';
import '../pages/cpp_basic_path_page.dart';
import '../pages/cpp_learning_unit_page.dart';
import '../pages/cpp_section_quiz_page.dart';
import '../pages/cpp_search_page.dart';
import '../pages/cpp_animation_page.dart';

class AppRouter {
  static const String home = '/';
  static const String lesson = '/lesson';
  static const String animation = '/animation';
  static const String quiz = '/quiz';
  static const String mistake = '/mistake';
  static const String teacherMode = '/teacher';
  static const String progress = '/progress';
  static const String settings = '/settings';
  static const String knowledge = '/knowledge';
  static const String knowledgeSection = '/knowledge/section';
  static const String knowledgeItem = '/knowledge/item';
  static const String cppBasic = '/cpp_basic';
  static const String cppLearningUnit = '/cpp_learning_unit';
  static const String cppSectionQuiz = '/cpp_section_quiz';
  static const String cppSearch = '/cpp_search';
  static const String cppAnimation = '/cpp_animation';

  static Route<dynamic> onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(
          builder: (_) => const HomePage(),
          settings: settings,
        );
      case '/lesson':
        return MaterialPageRoute(
          builder: (_) => const LessonPage(),
          settings: settings,
        );
      case '/animation':
        return MaterialPageRoute(
          builder: (_) => const AnimationPage(),
          settings: settings,
        );
      case '/quiz':
        return MaterialPageRoute(
          builder: (_) => const QuizPage(),
          settings: settings,
        );
      case '/mistake':
        return MaterialPageRoute(
          builder: (_) => const MistakePage(),
          settings: settings,
        );
      case '/teacher':
      case '/teacher_mode':
        return MaterialPageRoute(
          builder: (_) => const TeacherModePage(),
          settings: settings,
        );
      case '/progress':
        return MaterialPageRoute(
          builder: (_) => const ProgressPage(),
          settings: settings,
        );
      case '/settings':
        return MaterialPageRoute(
          builder: (_) => const SettingsPage(),
          settings: settings,
        );
      case '/knowledge':
        return MaterialPageRoute(
          builder: (_) => const KnowledgeMapPage(),
          settings: settings,
        );
      case '/knowledge/section':
        final sectionId = settings.arguments as String? ?? '';
        return MaterialPageRoute(
          builder: (_) => KnowledgeSectionPage(sectionId: sectionId),
          settings: settings,
        );
      case '/knowledge/item':
        final itemId = settings.arguments as String? ?? '';
        return MaterialPageRoute(
          builder: (_) => KnowledgeItemPage(itemId: itemId),
          settings: settings,
        );
      case '/cpp_basic':
        return MaterialPageRoute(
          builder: (_) => const CppBasicPathPage(),
          settings: settings,
        );
      case '/cpp_learning_unit':
        final itemId = settings.arguments as String? ?? '';
        return MaterialPageRoute(
          builder: (_) => CppLearningUnitPage(itemId: itemId),
          settings: settings,
        );
      case '/cpp_section_quiz':
        final sectionId = settings.arguments as String? ?? '';
        return MaterialPageRoute(
          builder: (_) => CppSectionQuizPage(sectionId: sectionId),
          settings: settings,
        );
      case '/cpp_search':
        return MaterialPageRoute(
          builder: (_) => const CppSearchPage(),
          settings: settings,
        );
      case '/cpp_animation':
        final animationId = settings.arguments as String? ?? '';
        return MaterialPageRoute(
          builder: (_) => CppAnimationPage(animationId: animationId),
          settings: settings,
        );
      default:
        return MaterialPageRoute(
          builder:
              (_) => Scaffold(
                appBar: AppBar(title: const Text('页面未找到')),
                body: const Center(child: Text('404')),
              ),
        );
    }
  }
}
