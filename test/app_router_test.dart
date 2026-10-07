import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/app/app_router.dart';
import 'package:bfs_learn/app/desktop_shell.dart';
import 'package:bfs_learn/pages/home_page.dart';
import 'package:bfs_learn/pages/knowledge_item_page.dart';
import 'package:bfs_learn/pages/progress_page.dart';
import 'package:bfs_learn/pages/teacher_mode_page.dart';
import 'package:bfs_learn/pages/workbench_page.dart';

void main() {
  setUp(() {
    // Shell 预建全部分支根页面（含设置页），测试环境需 mock 平台通道
    SharedPreferences.setMockInitialValues({});
    PackageInfo.setMockInitialValues(
      appName: '算法通',
      packageName: 'com.winknow.suanfatong',
      version: '1.0.0',
      buildNumber: '1',
      buildSignature: '',
    );
  });

  Widget host(GoRouter router) =>
      ProviderScope(child: MaterialApp.router(routerConfig: router));

  test('路由常量与旧路径保持兼容（ADR-005）', () {
    expect(AppRouter.home, '/');
    expect(AppRouter.lesson, '/lesson');
    expect(AppRouter.quiz, '/quiz');
    expect(AppRouter.mistake, '/mistake');
    expect(AppRouter.teacherMode, '/teacher');
    expect(AppRouter.teacherModeAlias, '/teacher_mode');
    expect(AppRouter.progress, '/progress');
    expect(AppRouter.settings, '/settings');
    expect(AppRouter.knowledge, '/knowledge');
    expect(AppRouter.knowledgeSection, '/knowledge/section');
    expect(AppRouter.knowledgeItem, '/knowledge/item');
    expect(AppRouter.cppBasic, '/cpp_basic');
    expect(AppRouter.cppLearningUnit, '/cpp_learning_unit');
    expect(AppRouter.cppSectionQuiz, '/cpp_section_quiz');
    expect(AppRouter.cppSearch, '/cpp_search');
    expect(AppRouter.cppAnimation, '/cpp_animation');
    // M1 新增导航区
    expect(AppRouter.workbench, '/workbench');
    expect(AppRouter.aiAssistant, '/ai_assistant');
    expect(AppRouter.classroom, '/classroom');
    // Shell 9 区
    expect(shellDestinations.length, 9);
    expect(
      shellDestinations.map((d) => d.location).toList(),
      containsAll(const [
        '/',
        '/knowledge',
        '/cpp_basic',
        '/cpp_search',
        '/workbench',
        '/ai_assistant',
        '/classroom',
        '/progress',
        '/settings',
      ]),
    );
  });

  testWidgets('初始路由进入首页，桌面 Shell 渲染 9 个导航区', (tester) async {
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 200));

    expect(find.byType(DesktopShell), findsOneWidget);
    final rail = tester.widget<NavigationRail>(find.byType(NavigationRail));
    expect(rail.destinations.length, 9);
    expect(rail.selectedIndex, 0);
    expect(find.byType(HomePage), findsOneWidget);
  });

  testWidgets('深链 /knowledge/item/:item_id 打开知识点页', (tester) async {
    await tester.pumpWidget(
      host(buildAppRouter(initialLocation: '/knowledge/item/1.1.1')),
    );
    await tester.pump(const Duration(milliseconds: 200));

    expect(find.byType(KnowledgeItemPage), findsOneWidget);
  });

  testWidgets('旧别名 /teacher_mode 重定向到 /teacher', (tester) async {
    final router = buildAppRouter(initialLocation: AppRouter.teacherModeAlias);
    await tester.pumpWidget(host(router));
    await tester.pump(const Duration(milliseconds: 200));

    expect(
      router.routerDelegate.currentConfiguration.uri.path,
      AppRouter.teacherMode,
    );
    expect(find.byType(TeacherModePage), findsOneWidget);
  });

  testWidgets('未知路径进入统一 ErrorPage', (tester) async {
    final router = buildAppRouter();
    await tester.pumpWidget(host(router));
    await tester.pump(const Duration(milliseconds: 200));

    router.go('/definitely-not-a-route');
    // 注：预建分支可能含持续动画（加载指示器），不能用 pumpAndSettle
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 100));

    expect(find.byType(AppErrorPage), findsOneWidget);
    expect(find.text('页面未找到'), findsWidgets);
    expect(find.text('返回首页'), findsOneWidget);
  });

  testWidgets('编程工作台为实页，AI 助手 / 课堂仍为占位', (tester) async {
    final router = buildAppRouter(initialLocation: AppRouter.workbench);
    await tester.pumpWidget(host(router));
    await tester.pump(const Duration(milliseconds: 100));
    // M3-8：workbench 已接入 WorkbenchPage（经 DesktopBridge 行协议）
    expect(find.byType(WorkbenchPage), findsOneWidget);
    expect(find.byType(ShellPlaceholderPage), findsNothing);

    router.go(AppRouter.aiAssistant);
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.byType(ShellPlaceholderPage), findsOneWidget);

    router.go(AppRouter.classroom);
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.byType(ShellPlaceholderPage), findsOneWidget);
  });

  testWidgets('NavigationRail 点击切换到学习记录', (tester) async {
    final router = buildAppRouter();
    await tester.pumpWidget(host(router));
    await tester.pump(const Duration(milliseconds: 200));

    await tester.tap(find.byIcon(Icons.insights_outlined));
    await tester.pump(const Duration(milliseconds: 300));

    expect(
      router.routerDelegate.currentConfiguration.uri.path,
      AppRouter.progress,
    );
    expect(find.byType(ProgressPage), findsOneWidget);
  });
}
