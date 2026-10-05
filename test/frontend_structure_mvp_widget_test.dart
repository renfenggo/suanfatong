import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/learning_card.dart';
import 'package:bfs_learn/models/practice_entry.dart';
import 'package:bfs_learn/models/cpp14_template_entry.dart';
import 'package:bfs_learn/models/cpp_animation.dart';
import 'package:bfs_learn/widgets/knowledge/learning_card_section.dart';
import 'package:bfs_learn/widgets/knowledge/practice_entry_section.dart';
import 'package:bfs_learn/widgets/knowledge/cpp14_template_entry_section.dart';
import 'package:bfs_learn/widgets/knowledge/animation_entry_section.dart';

/// 前端结构 MVP - Widget Smoke Test
///
/// 验证前端结构 MVP 的核心组件能够正确渲染不崩溃。
void main() {
  group('LearningCardSection widget tests', () {
    testWidgets('should render learning card without crash', (tester) async {
      final card = LearningCard(
        id: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        summary: '从后往前算，记录每个位置后面的最大/最小值',
        useCases: '需要频繁查询某个位置后面的最大/最小值时',
        intuition: '后缀信息一次性算好，用的时候直接取',
        example: '数组[3,1,4,1,5]的后缀最大值计算',
        traps: ['忘记从右往左算', '边界处理错误'],
        practice: '从简单数组后缀最大值开始',
        nextItems: ['前缀最值DP', '双端队列维护最值'],
        actionType: 'read',
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LearningCardSection(card: card),
          ),
        ),
      );

      expect(find.text('学习卡片'), findsOneWidget);
      expect(find.text('一句话解释'), findsOneWidget);
      expect(find.text('核心直觉'), findsOneWidget);
      expect(find.text('什么时候用'), findsOneWidget);
      expect(find.text('最小例子'), findsOneWidget);
      expect(find.text('常见坑'), findsOneWidget);
      expect(find.text('学完继续'), findsOneWidget);
    });

    testWidgets('should handle card with minimal fields', (tester) async {
      final card = LearningCard(
        id: '2.8.209',
        title: '最小卡片',
        sectionId: '2.8',
        summary: '测试最小卡片',
        useCases: '',
        intuition: '',
        example: '',
        traps: [],
        practice: '',
        nextItems: [],
        actionType: 'read',
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LearningCardSection(card: card),
          ),
        ),
      );

      expect(find.text('学习卡片'), findsOneWidget);
      expect(find.text('一句话解释'), findsOneWidget);
      // 不应渲染可选字段
      expect(find.text('核心直觉'), findsNothing);
      expect(find.text('常见坑'), findsNothing);
    });
  });

  group('PracticeEntrySection widget tests', () {
    testWidgets('should render practice entry without crash', (tester) async {
      final entry = PracticeEntry(
        itemId: '2.4.1',
        title: '二分答案',
        sectionId: '2.4',
        sectionName: '二分与答案搜索',
        problems: [
          PracticeProblem(
            problemRefId: 'cses.range_queries.static_range_sum',
            platform: 'CSES',
            problemId: '1628',
            title: 'Binary Search',
            url: 'https://cses.fi/problemset/task/1628',
            difficulty: 'Easy',
            role: 'intro',
            note: '',
          ),
          PracticeProblem(
            problemRefId: 'leetcode.find_first_and_last',
            platform: 'LeetCode',
            problemId: '34',
            title: 'First and Last Position',
            url: 'https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/',
            difficulty: 'Medium',
            role: 'standard',
            note: '',
          ),
        ],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PracticeEntrySection(entry: entry),
          ),
        ),
      );

      expect(find.text('练习入口'), findsOneWidget);
      expect(find.text('2 题'), findsOneWidget);
      expect(find.text('Binary Search'), findsOneWidget);
      expect(find.text('First and Last Position'), findsOneWidget);
      expect(find.text('CSES'), findsOneWidget);
      expect(find.text('LeetCode'), findsOneWidget);
      expect(find.text('简单'), findsOneWidget);
      expect(find.text('中等'), findsOneWidget);
    });

    testWidgets('should not render when problems is empty', (tester) async {
      final entry = PracticeEntry(
        itemId: 'empty',
        title: '空练习',
        sectionId: '2.4',
        sectionName: '二分与答案搜索',
        problems: [],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PracticeEntrySection(entry: entry),
          ),
        ),
      );

      expect(find.byType(PracticeEntrySection), findsOneWidget);
      // 不应渲染任何可见内容
      expect(find.text('练习入口'), findsNothing);
    });
  });

  group('Cpp14TemplateEntrySection widget tests', () {
    testWidgets('should render template entry without crash', (tester) async {
      final entry = Cpp14TemplateEntry(
        itemId: '2.7.16',
        title: 'BFS 模板',
        sectionId: '2.7',
        sectionName: '搜索',
        templateType: 'graph_algorithm',
        complexity: 'O(V+E)',
        difficulty: '入门',
        templateInfo: Cpp14TemplateInfo(
          keyConcepts: ['队列', '访问标记', '距离计算'],
          templateFunctions: ['bfs()', 'main()'],
          commonVariants: [],
          usageScenario: '图的最短路径搜索',
        ),
        sourceFile: 'templates/bfs_standard.cpp',
        practiceProblems: [],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Cpp14TemplateEntrySection(entry: entry),
          ),
        ),
      );

      expect(find.text('C++14 模板'), findsOneWidget);
      expect(find.text('BFS 模板'), findsOneWidget);
      expect(find.text('图的最短路径搜索'), findsOneWidget);
      expect(find.text('队列'), findsOneWidget);
      expect(find.text('访问标记'), findsOneWidget);
      expect(find.text('距离计算'), findsOneWidget);
      // hasSource 计算：sourceFile.isNotEmpty => true
      // 组件内部通过 entry.sourceFile.isNotEmpty 判断
    });

    testWidgets('should handle entry without source', (tester) async {
      final entry = Cpp14TemplateEntry(
        itemId: 'no-source',
        title: '无源模板',
        sectionId: '2.7',
        sectionName: '搜索',
        templateType: 'test',
        complexity: '',
        difficulty: '',
        templateInfo: Cpp14TemplateInfo(
          keyConcepts: [],
          templateFunctions: [],
          commonVariants: [],
          usageScenario: '',
        ),
        sourceFile: '',
        practiceProblems: [],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Cpp14TemplateEntrySection(entry: entry),
          ),
        ),
      );

      expect(find.text('C++14 模板'), findsOneWidget);
      expect(find.text('无源模板'), findsOneWidget);
      // hasSource 计算：sourceFile.isNotEmpty => false
      // 组件内部通过 entry.sourceFile.isNotEmpty 判断，不显示"可查看"
    });
  });

  group('AnimationEntrySection widget tests', () {
    testWidgets('should render animation entry without crash', (tester) async {
      final animations = [
        CppAnimationMeta(
          animationId: 'bfs_demo',
          itemId: '2.7.1',
          order: 1,
          type: 'graph',
          title: 'BFS 演示',
          assetPath: 'assets/data/cpp/animations/bfs_demo.json',
        ),
        CppAnimationMeta(
          animationId: 'dfs_demo',
          itemId: '2.7.2',
          order: 1,
          type: 'graph',
          title: 'DFS 演示',
          assetPath: 'assets/data/cpp/animations/dfs_demo.json',
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AnimationEntrySection(animations: animations),
          ),
        ),
      );

      expect(find.text('动画演示'), findsOneWidget);
      expect(find.text('2 个'), findsOneWidget);
      expect(find.text('BFS 演示'), findsOneWidget);
      expect(find.text('DFS 演示'), findsOneWidget);
    });

    testWidgets('should not render when animations is empty', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AnimationEntrySection(animations: []),
          ),
        ),
      );

      expect(find.byType(AnimationEntrySection), findsOneWidget);
      // 不应渲染任何可见内容
      expect(find.text('动画演示'), findsNothing);
    });
  });

  group('Component integration smoke tests', () {
    testWidgets('should render all components together without crash',
        (tester) async {
      final card = LearningCard(
        id: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        summary: '从后往前算，记录每个位置后面的最大/最小值',
        useCases: '需要频繁查询某个位置后面的最大/最小值时',
        intuition: '后缀信息一次性算好，用的时候直接取',
        example: '数组[3,1,4,1,5]的后缀最大值计算',
        traps: ['忘记从右往左算'],
        practice: '从简单数组后缀最大值开始',
        nextItems: ['前缀最值DP'],
        actionType: 'read',
      );

      final practiceEntry = PracticeEntry(
        itemId: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        sectionName: '动态规划',
        problems: [
          PracticeProblem(
            problemRefId: 'cses.range_queries.static_range_sum',
            platform: 'CSES',
            problemId: '1628',
            title: 'Binary Search',
            url: 'https://cses.fi/problemset/task/1628',
            difficulty: 'Easy',
            role: 'intro',
            note: '',
          ),
        ],
      );

      final templateEntry = Cpp14TemplateEntry(
        itemId: '2.8.208',
        title: '后缀最值 DP 模板',
        sectionId: '2.8',
        sectionName: '动态规划',
        templateType: 'dp',
        complexity: 'O(n)',
        difficulty: '入门',
        templateInfo: Cpp14TemplateInfo(
          keyConcepts: ['逆向遍历', '状态更新'],
          templateFunctions: ['suffix_max()', 'main()'],
          commonVariants: [],
          usageScenario: '计算数组后缀最值',
        ),
        sourceFile: 'templates/suffix_max.cpp',
        practiceProblems: [],
      );

      final animations = [
        CppAnimationMeta(
          animationId: 'suffix_max_demo',
          itemId: '2.8.208',
          order: 1,
          type: 'dp',
          title: '后缀最值演示',
          assetPath: 'assets/data/cpp/animations/suffix_max_demo.json',
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: Column(
                children: [
                  LearningCardSection(card: card),
                  const SizedBox(height: 12),
                  PracticeEntrySection(entry: practiceEntry),
                  const SizedBox(height: 12),
                  Cpp14TemplateEntrySection(entry: templateEntry),
                  const SizedBox(height: 12),
                  AnimationEntrySection(animations: animations),
                ],
              ),
            ),
          ),
        ),
      );

      // 验证所有组件都渲染成功
      expect(find.text('学习卡片'), findsOneWidget);
      expect(find.text('练习入口'), findsWidgets);
      expect(find.text('C++14 模板'), findsOneWidget);
      expect(find.text('动画演示'), findsOneWidget);
    });
  });
}