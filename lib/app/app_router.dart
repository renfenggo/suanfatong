import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../pages/animation_page.dart';
import '../pages/cpp_animation_page.dart';
import '../pages/cpp_basic_path_page.dart';
import '../pages/cpp_learning_unit_page.dart';
import '../pages/cpp_search_page.dart';
import '../pages/cpp_section_quiz_page.dart';
import '../pages/home_page.dart';
import '../pages/knowledge_item_page.dart';
import '../pages/knowledge_map_page.dart';
import '../pages/knowledge_section_page.dart';
import '../pages/lesson_page.dart';
import '../pages/login_page.dart';
import '../pages/mistake_page.dart';
import '../pages/progress_page.dart';
import '../pages/quiz_page.dart';
import '../pages/settings_page.dart';
import '../pages/teacher_mode_page.dart';
import '../pages/workbench_page.dart';
import 'desktop_shell.dart';

/// 统一路由路径常量（与迁移前 Navigator 1.0 路径保持兼容）
class AppRouter {
  static const String home = '/';
  static const String lesson = '/lesson';
  static const String animation = '/animation';
  static const String quiz = '/quiz';
  static const String mistake = '/mistake';
  static const String teacherMode = '/teacher';
  static const String teacherModeAlias = '/teacher_mode';
  static const String progress = '/progress';
  static const String settings = '/settings';
  static const String login = '/login';
  static const String knowledge = '/knowledge';
  static const String knowledgeSection = '/knowledge/section';
  static const String knowledgeItem = '/knowledge/item';
  static const String cppBasic = '/cpp_basic';
  static const String cppLearningUnit = '/cpp_learning_unit';
  static const String cppSectionQuiz = '/cpp_section_quiz';
  static const String cppSearch = '/cpp_search';
  static const String cppAnimation = '/cpp_animation';

  // M1 新增桌面 Shell 导航区
  static const String workbench = '/workbench';
  static const String aiAssistant = '/ai_assistant';
  static const String classroom = '/classroom';

  // 深链路径
  static const String knowledgeItemDeepLink = '/knowledge/item/:item_id';
}

String _stringExtra(GoRouterState state) => state.extra as String? ?? '';

/// 构建 App 全局路由（go_router，ADR-005）。
///
/// 结构：StatefulShellRoute.indexedStack + DesktopShell（NavigationRail 9 区），
/// 各分支保留导航状态；旧 16 路径全部原样保留；新增 /knowledge/item/:item_id
/// 深链；未匹配路径进入统一 AppErrorPage。
GoRouter buildAppRouter({String initialLocation = AppRouter.home}) {
  return GoRouter(
    initialLocation: initialLocation,
    errorBuilder:
        (context, state) =>
            AppErrorPage(location: state.uri.toString(), error: state.error),
    routes: [
      StatefulShellRoute.indexedStack(
        builder:
            (context, state, navigationShell) =>
                DesktopShell(navigationShell: navigationShell),
        branches: [
          // 0 首页
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.home,
                builder: (context, state) => const HomePage(),
              ),
            ],
          ),
          // 1 知识图谱
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.knowledge,
                builder: (context, state) => const KnowledgeMapPage(),
              ),
              GoRoute(
                path: AppRouter.knowledgeSection,
                builder:
                    (context, state) =>
                        KnowledgeSectionPage(sectionId: _stringExtra(state)),
              ),
              GoRoute(
                path: AppRouter.knowledgeItem,
                builder:
                    (context, state) =>
                        KnowledgeItemPage(itemId: _stringExtra(state)),
              ),
              GoRoute(
                path: AppRouter.knowledgeItemDeepLink,
                builder:
                    (context, state) => KnowledgeItemPage(
                      itemId: state.pathParameters['item_id'] ?? '',
                    ),
              ),
            ],
          ),
          // 2 学习中心（C++ 基础路径 + 旧学习单元流程）
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.cppBasic,
                builder: (context, state) => const CppBasicPathPage(),
              ),
              GoRoute(
                path: AppRouter.cppLearningUnit,
                builder:
                    (context, state) =>
                        CppLearningUnitPage(itemId: _stringExtra(state)),
              ),
              GoRoute(
                path: AppRouter.cppSectionQuiz,
                builder:
                    (context, state) =>
                        CppSectionQuizPage(sectionId: _stringExtra(state)),
              ),
              GoRoute(
                path: AppRouter.lesson,
                builder: (context, state) => const LessonPage(),
              ),
              GoRoute(
                path: AppRouter.animation,
                builder: (context, state) => const AnimationPage(),
              ),
              GoRoute(
                path: AppRouter.quiz,
                builder: (context, state) => const QuizPage(),
              ),
              GoRoute(
                path: AppRouter.teacherMode,
                builder: (context, state) => const TeacherModePage(),
              ),
            ],
          ),
          // 3 题目训练
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.cppSearch,
                builder: (context, state) => const CppSearchPage(),
              ),
              GoRoute(
                path: AppRouter.cppAnimation,
                builder:
                    (context, state) =>
                        CppAnimationPage(animationId: _stringExtra(state)),
              ),
            ],
          ),
          // 4 编程工作台（M3-8：经 DesktopBridge 行协议接入 CodeRunner）
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.workbench,
                builder: (context, state) => const WorkbenchPage(),
              ),
            ],
          ),
          // 5 AI 助手（占位，M5 接入 AI Gateway）
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.aiAssistant,
                builder:
                    (context, state) => const ShellPlaceholderPage(
                      title: 'AI 助手',
                      description: 'AI 答疑与讲解（开发中，暂未开放）',
                      icon: Icons.smart_toy,
                    ),
              ),
            ],
          ),
          // 6 课堂（占位，M2 接入 Winknow DesktopBridge）
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.classroom,
                builder:
                    (context, state) => const ShellPlaceholderPage(
                      title: '课堂',
                      description: 'Winknow 课堂管控（开发中，暂未开放）',
                      icon: Icons.cast_for_education,
                    ),
              ),
            ],
          ),
          // 7 学习记录
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.progress,
                builder: (context, state) => const ProgressPage(),
              ),
              GoRoute(
                path: AppRouter.mistake,
                builder: (context, state) => const MistakePage(),
              ),
            ],
          ),
          // 8 设置
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: AppRouter.settings,
                builder: (context, state) => const SettingsPage(),
              ),
            ],
          ),
        ],
      ),
      // 顶层：登录页（不带桌面 Shell 导航的独立页）
      GoRoute(
        path: AppRouter.login,
        builder: (context, state) => const LoginPage(),
      ),
      // 旧别名：/teacher_mode -> /teacher
      GoRoute(
        path: AppRouter.teacherModeAlias,
        redirect: (context, state) => AppRouter.teacherMode,
      ),
    ],
  );
}

/// 全局路由实例（App 启动使用；测试请用 buildAppRouter 另建实例）
final GoRouter appRouter = buildAppRouter();

/// 统一路由错误页（替代旧手写 404）
class AppErrorPage extends StatelessWidget {
  final String location;
  final Object? error;

  const AppErrorPage({super.key, required this.location, this.error});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: const Text('页面未找到')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.travel_explore, size: 64, color: scheme.outline),
            const SizedBox(height: 16),
            Text('页面未找到', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text('路径：$location', style: TextStyle(color: scheme.outline)),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () => context.go(AppRouter.home),
              icon: const Icon(Icons.home),
              label: const Text('返回首页'),
            ),
          ],
        ),
      ),
    );
  }
}
