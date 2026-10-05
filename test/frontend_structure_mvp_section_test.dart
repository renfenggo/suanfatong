import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/knowledge_item.dart';
import 'package:bfs_learn/models/learning_path.dart';
import 'package:bfs_learn/models/learning_layer.dart';
import 'package:bfs_learn/widgets/knowledge/section/learning_path_panel.dart';
import 'package:bfs_learn/widgets/knowledge/section/cross_section_prerequisite_panel.dart';
import 'package:bfs_learn/widgets/knowledge/section/layered_knowledge_list.dart';

/// 前端结构 MVP - 章节页 Widget Smoke Test
///
/// 验证章节页组件能够正确渲染不崩溃。
void main() {
  group('LearningPathPanel widget tests', () {
    testWidgets('should render learning path panel without crash',
        (tester) async {
      final learningPath = LearningPath(
        sectionId: '2.8',
        sectionName: '动态规划',
        beginnerPath: ['2.8.1', '2.8.2', '2.8.208'],
        intermediatePath: ['2.8.10', '2.8.11', '2.8.12'],
        advancedPath: ['2.8.100', '2.8.101'],
        beginnerDescription: '从基础概念开始',
        intermediateDescription: '深入掌握技巧',
        advancedDescription: '综合运用',
        crossSectionPrerequisites: [],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LearningPathPanel(
              learningPath: learningPath,
              itemNameResolver: (itemId) => 'Item $itemId',
              onItemTap: (itemId) {},
            ),
          ),
        ),
      );

      expect(find.text('学习路径'), findsOneWidget);
      expect(find.text('入门路径'), findsOneWidget);
      expect(find.text('提高路径'), findsOneWidget);
      expect(find.text('冲刺路径'), findsOneWidget);
      // 具体的知识点名称可能不直接渲染，通过 itemId 查找
      expect(find.text('Item 2.8.1'), findsOneWidget);
      expect(find.text('Item 2.8.208'), findsOneWidget);
    });

    testWidgets('should render cross-section prerequisites without crash',
        (tester) async {
      final prerequisites = [
        CrossSectionPrerequisite(
          id: '2.1.1',
          name: '时间复杂度',
          reason: '理解 DP 状态转移的基础',
        ),
        CrossSectionPrerequisite(
          id: '2.3.1',
          name: '递归基础',
          reason: 'DP 的核心思想',
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CrossSectionPrerequisitePanel(
              prerequisites: prerequisites,
              onItemTap: (itemId) {},
            ),
          ),
        ),
      );

      expect(find.text('建议先补的基础'), findsOneWidget);
      expect(find.text('2 个'), findsOneWidget);
      expect(find.text('2.1.1'), findsOneWidget);
      expect(find.text('时间复杂度'), findsOneWidget);
      expect(find.text('理解 DP 状态转移的基础'), findsOneWidget);
      expect(find.text('2.3.1'), findsOneWidget);
      expect(find.text('递归基础'), findsOneWidget);
      expect(find.text('DP 的核心思想'), findsOneWidget);
    });

    testWidgets('should not render when prerequisites is empty', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CrossSectionPrerequisitePanel(
              prerequisites: [],
              onItemTap: (itemId) {},
            ),
          ),
        ),
      );

      // 不应渲染任何可见内容
      expect(find.text('建议先补的基础'), findsNothing);
    });

    testWidgets('should render learning path with cross-section prerequisites',
        (tester) async {
      final learningPath = LearningPath(
        sectionId: '3.13',
        sectionName: '高级数据结构扩展',
        beginnerPath: ['3.13.1', '3.13.2'],
        intermediatePath: ['3.13.10'],
        advancedPath: ['3.13.100'],
        beginnerDescription: '基础入门',
        intermediateDescription: '进阶学习',
        advancedDescription: '高级应用',
        crossSectionPrerequisites: [
          CrossSectionPrerequisite(
            id: '2.8.1',
            name: '基础 DP',
            reason: '理解线段树的基础',
          ),
        ],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LearningPathPanel(
              learningPath: learningPath,
              itemNameResolver: (itemId) => 'Item $itemId',
              onItemTap: (itemId) {},
            ),
          ),
        ),
      );

      expect(find.text('学习路径'), findsOneWidget);
      expect(find.text('入门路径'), findsOneWidget);
      expect(find.text('提高路径'), findsOneWidget);
      expect(find.text('冲刺路径'), findsOneWidget);
    });
  });

  group('LayeredKnowledgeList widget tests', () {
    testWidgets('should render layered knowledge list without crash',
        (tester) async {
      final items = [
        KnowledgeItem(
          id: '2.8.1',
          name: 'DP 基础',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_basic',
          pickupGroupName: 'DP 基础',
          blockId: '',
          blockName: '',
        ),
        KnowledgeItem(
          id: '2.8.2',
          name: '背包问题',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_knapsack',
          pickupGroupName: '背包问题',
          blockId: '',
          blockName: '',
        ),
        KnowledgeItem(
          id: '2.8.208',
          name: '后缀最值 DP',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_suffix',
          pickupGroupName: '后缀 DP',
          blockId: '',
          blockName: '',
        ),
      ];

      final itemLayers = {
        '2.8.1': 'core',
        '2.8.2': 'standard',
        '2.8.208': 'advanced',
      };

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LayeredKnowledgeList(
              items: items,
              itemLayers: itemLayers,
              onItemTap: (item) {},
            ),
          ),
        ),
      );

      // 验证分层统计
      expect(find.text('核心'), findsOneWidget);
      expect(find.text('1'), findsWidgets);
      expect(find.text('进阶'), findsOneWidget);
      expect(find.text('扩展'), findsOneWidget);
      expect(find.text('可选'), findsOneWidget);

      // 验证分层标签
      expect(find.text('核心主线'), findsOneWidget);
      expect(find.text('常用进阶'), findsOneWidget);
      expect(find.text('专题扩展'), findsOneWidget);

      // 验证知识点渲染（至少应有知识点卡片）
      expect(find.byType(Card), findsWidgets);
    });

    testWidgets('should handle empty items list', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LayeredKnowledgeList(
              items: [],
              itemLayers: {},
              onItemTap: (item) {},
            ),
          ),
        ),
      );

      // 应显示空的分层统计
      expect(find.text('核心'), findsOneWidget);
      expect(find.text('进阶'), findsOneWidget);
      expect(find.text('扩展'), findsOneWidget);
      expect(find.text('可选'), findsOneWidget);

      // 所有计数都应为 0
      expect(find.text('0'), findsWidgets);
    });

    testWidgets('should apply collapse policy', (tester) async {
      final items = [
        KnowledgeItem(
          id: '2.8.1',
          name: 'DP 基础',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_basic',
          pickupGroupName: 'DP 基础',
          blockId: '',
          blockName: '',
        ),
        KnowledgeItem(
          id: '2.8.100',
          name: '高级 DP',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_advanced',
          pickupGroupName: '高级 DP',
          blockId: '',
          blockName: '',
        ),
        KnowledgeItem(
          id: '2.8.999',
          name: '冷门 DP',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_rare',
          pickupGroupName: '冷门 DP',
          blockId: '',
          blockName: '',
        ),
      ];

      final itemLayers = {
        '2.8.1': 'core',
        '2.8.100': 'advanced',
        '2.8.999': 'optional',
      };

      final collapsePolicy = SectionCollapsePolicy(
        sectionId: '2.8',
        sectionName: '动态规划',
        category: 'algorithm',
        total: 292,
        frontendCore: 1,
        frontendStandard: 0,
        frontendAdvanced: 1,
        frontendOptional: 1,
        foldableRatio: 0.637,
        defaultCollapsePolicy: 'advanced,optional',
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LayeredKnowledgeList(
              items: items,
              itemLayers: itemLayers,
              collapsePolicy: collapsePolicy,
              onItemTap: (item) {},
            ),
          ),
        ),
      );

      // 验证分层渲染
      expect(find.text('核心主线'), findsOneWidget);
      expect(find.text('专题扩展'), findsOneWidget);
      expect(find.text('冷门 / 可选'), findsOneWidget);
    });
  });

  group('Section integration smoke tests', () {
    testWidgets('should render all section components together without crash',
        (tester) async {
      final items = [
        KnowledgeItem(
          id: '2.8.1',
          name: 'DP 基础',
          parent: '2.8',
          directPre: [],
          resolvedPre: [],
          rel: [],
          alias: [],
          pickupGroup: 'dp_basic',
          pickupGroupName: 'DP 基础',
          blockId: '',
          blockName: '',
        ),
      ];

      final itemLayers = {
        '2.8.1': 'core',
      };

      final learningPath = LearningPath(
        sectionId: '2.8',
        sectionName: '动态规划',
        beginnerPath: ['2.8.1'],
        intermediatePath: [],
        advancedPath: [],
        beginnerDescription: '基础入门',
        intermediateDescription: '',
        advancedDescription: '',
        crossSectionPrerequisites: [],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: Column(
                children: [
                  LearningPathPanel(
                    learningPath: learningPath,
                    itemNameResolver: (itemId) => 'Item $itemId',
                    onItemTap: (itemId) {},
                  ),
                  const SizedBox(height: 12),
                  LayeredKnowledgeList(
                    items: items,
                    itemLayers: itemLayers,
                    onItemTap: (item) {},
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // 验证所有组件都渲染成功
      expect(find.text('学习路径'), findsOneWidget);
      expect(find.text('核心主线'), findsOneWidget);
      expect(find.byType(Card), findsWidgets);
    });
  });
}