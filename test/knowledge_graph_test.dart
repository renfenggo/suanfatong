import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';
import 'package:bfs_learn/models/knowledge_item.dart';
import 'package:bfs_learn/models/knowledge_content_bridge.dart';
import 'package:bfs_learn/models/content_manifest.dart';
import 'package:bfs_learn/models/learning_topic.dart';
import 'package:bfs_learn/models/lesson_set.dart';
import 'package:bfs_learn/models/quiz_set.dart';
import 'package:bfs_learn/models/mistake_set.dart';
import 'package:bfs_learn/repositories/knowledge_graph_repository.dart';
import 'package:bfs_learn/repositories/json_asset_repository.dart';

KnowledgeGraph _buildGraph(List<Map<String, dynamic>> categories) {
  return KnowledgeGraph.fromJson({
    'meta': {'title': 'test'},
    'categories': categories,
  });
}

void main() {
  group('KnowledgeGraph parsing', () {
    test('parses minimal JSON', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'level': 'L1',
              'pre': [],
              'rel': [],
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'alias': [],
                  'parent': '2.1',
                  'direct_pre': [],
                  'resolved_pre': [],
                  'rel': [],
                  'pickup_group': 'basic_algorithm',
                  'pickup_group_name': '基础算法',
                  'pickup_order': 1,
                },
              ],
            },
          ],
        },
      ]);

      expect(graph.categories.length, 1);
      expect(graph.allSections.length, 1);
      expect(graph.allItems.length, 1);
      expect(graph.allItems.first.name, '枚举');
    });

    test('parses empty categories gracefully', () {
      final graph = KnowledgeGraph.fromJson({});
      expect(graph.categories, isEmpty);
      expect(graph.allSections, isEmpty);
      expect(graph.allItems, isEmpty);
    });

    test('missing string fields default to empty', () {
      final item = KnowledgeItem.fromJson({});
      expect(item.id, '');
      expect(item.name, '');
      expect(item.parent, '');
      expect(item.pickupOrder, 0);
    });

    test('non-list alias/pre/rel fields default to empty list', () {
      final item = KnowledgeItem.fromJson({
        'id': 'x',
        'name': 'test',
        'alias': 'not-a-list',
        'direct_pre': 42,
        'resolved_pre': null,
        'rel': [1, 2, 3],
      });
      expect(item.alias, isEmpty);
      expect(item.directPre, isEmpty);
      expect(item.resolvedPre, isEmpty);
      expect(item.rel, isEmpty);
    });
  });

  group('KnowledgeGraph lookups', () {
    late KnowledgeGraph graph;

    setUp(() {
      graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'level': 'L1',
              'pre': [],
              'rel': [],
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '2.1',
                  'pickup_group': 'basic_algorithm',
                  'pickup_order': 1,
                },
                {
                  'id': '2.1.2',
                  'name': '模拟',
                  'parent': '2.1',
                  'pickup_group': 'basic_algorithm',
                  'pickup_order': 2,
                },
              ],
            },
            {
              'id': '2.2',
              'name': '排序',
              'level': 'L1',
              'pre': ['2.1'],
              'items': [
                {
                  'id': '2.2.1',
                  'name': '冒泡排序',
                  'parent': '2.2',
                  'pickup_group': 'basic_comparison_sort',
                  'pickup_order': 1,
                },
              ],
            },
          ],
        },
      ]);
    });

    test('sectionById finds existing section', () {
      final section = graph.sectionById('2.1');
      expect(section, isNotNull);
      expect(section!.name, '基础算法');
    });

    test('sectionById returns null for missing', () {
      expect(graph.sectionById('9.9'), isNull);
    });

    test('itemById finds existing item', () {
      final item = graph.itemById('2.1.1');
      expect(item, isNotNull);
      expect(item!.name, '枚举');
    });

    test('itemById returns null for missing', () {
      expect(graph.itemById('9.9.9'), isNull);
    });

    test('itemsByPickupGroup returns correct items', () {
      final items = graph.itemsByPickupGroup('basic_algorithm');
      expect(items.length, 2);
      expect(items.map((i) => i.id), containsAll(['2.1.1', '2.1.2']));
    });

    test('itemsByPickupGroup returns empty for unknown group', () {
      expect(graph.itemsByPickupGroup('nonexistent'), isEmpty);
    });

    test('itemsOfSection returns items belonging to section', () {
      final items = graph.itemsOfSection('2.1');
      expect(items.length, 2);
    });

    test('itemsOfSection returns empty for unknown section', () {
      expect(graph.itemsOfSection('9.9'), isEmpty);
    });
  });

  group('KnowledgeGraphValidation', () {
    late KnowledgeGraphRepository repo;

    setUp(() {
      repo = KnowledgeGraphRepository(jsonRepo: JsonAssetRepository());
    });

    test('valid graph passes validation', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '2.1',
                  'resolved_pre': [],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.isValid, isTrue);
      expect(result.duplicateSectionIds, isEmpty);
      expect(result.duplicateItemIds, isEmpty);
      expect(result.missingParents, isEmpty);
      expect(result.hasCycle, isFalse);
    });

    test('missing parent is detected', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '9.9',
                  'resolved_pre': [],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.missingParents, isNotEmpty);
      expect(result.missingParents, contains('2.1.1'));
    });

    test('duplicate item id is detected', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '2.1',
                  'resolved_pre': [],
                },
                {
                  'id': '2.1.1',
                  'name': '枚举2',
                  'parent': '2.1',
                  'resolved_pre': [],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.duplicateItemIds, contains('2.1.1'));
    });

    test('duplicate section id is detected', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {'id': '2.1', 'name': '基础算法', 'items': []},
            {'id': '2.1', 'name': '重复', 'items': []},
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.duplicateSectionIds, contains('2.1'));
    });

    test('simple cycle is detected', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': 'a',
                  'name': 'A',
                  'parent': '2.1',
                  'resolved_pre': ['b'],
                },
                {
                  'id': 'b',
                  'name': 'B',
                  'parent': '2.1',
                  'resolved_pre': ['a'],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.hasCycle, isTrue);
      expect(result.cycleNodes, isNotEmpty);
    });

    test('external refs do not cause failure', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '2.1',
                  'resolved_pre': ['external_ref'],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.missingRefs, isNotEmpty);
      expect(result.isValid, isTrue);
    });

    test('three-node cycle is detected', () {
      final graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': 'a',
                  'name': 'A',
                  'parent': '2.1',
                  'resolved_pre': ['b'],
                },
                {
                  'id': 'b',
                  'name': 'B',
                  'parent': '2.1',
                  'resolved_pre': ['c'],
                },
                {
                  'id': 'c',
                  'name': 'C',
                  'parent': '2.1',
                  'resolved_pre': ['a'],
                },
              ],
            },
          ],
        },
      ]);

      final result = repo.validateGraph(graph);
      expect(result.hasCycle, isTrue);
    });
  });

  group('KnowledgeContentBridge', () {
    late KnowledgeGraph graph;
    late ContentManifest manifest;
    late KnowledgeContentBridge bridge;

    setUp(() {
      graph = _buildGraph([
        {
          'name': '算法',
          'sections': [
            {
              'id': '2.1',
              'name': '基础算法',
              'items': [
                {
                  'id': '2.1.1',
                  'name': '枚举',
                  'parent': '2.1',
                  'pickup_group': 'bfs_basic',
                  'pickup_order': 1,
                },
                {
                  'id': '2.1.2',
                  'name': '模拟',
                  'parent': '2.1',
                  'pickup_group': 'bfs_basic',
                  'pickup_order': 2,
                },
              ],
            },
            {
              'id': '2.2',
              'name': '排序',
              'items': [
                {
                  'id': '2.2.1',
                  'name': '冒泡排序',
                  'parent': '2.2',
                  'pickup_group': 'bfs_maze',
                  'pickup_order': 1,
                },
              ],
            },
          ],
        },
      ]);

      manifest = ContentManifest(
        defaultTopicId: 'bfs',
        topics: [
          LearningTopic(
            topicId: 'bfs',
            lessonSets: [
              LessonSet(
                lessonSetId: 'bfs_basic',
                assetPath: 'assets/data/lessons/bfs_basic.json',
                pickupGroup: 'bfs_basic',
              ),
              LessonSet(
                lessonSetId: 'bfs_maze',
                assetPath: 'assets/data/lessons/bfs_maze.json',
                pickupGroup: 'bfs_maze',
              ),
            ],
            quizSets: [
              QuizSet(
                quizSetId: 'bfs_basic',
                assetPath: 'assets/data/quizzes/bfs_quiz.json',
                pickupGroup: 'bfs_basic',
              ),
            ],
            mistakeSets: [
              MistakeSet(
                mistakeSetId: 'bfs_mistakes',
                assetPath: 'assets/data/mistakes/bfs_mistakes.json',
                pickupGroup: 'bfs_mistakes',
              ),
            ],
          ),
        ],
      );

      bridge = KnowledgeContentBridge(graph: graph, manifest: manifest);
    });

    test('itemsForPickupGroup returns correct items', () {
      final items = bridge.itemsForPickupGroup('bfs_basic');
      expect(items.length, 2);
      expect(items.map((i) => i.id), containsAll(['2.1.1', '2.1.2']));
    });

    test('itemsForLessonSet returns items via pickupGroup', () {
      final items = bridge.itemsForLessonSet('bfs_basic');
      expect(items.length, 2);
    });

    test('itemsForQuizSet returns items via pickupGroup', () {
      final items = bridge.itemsForQuizSet('bfs_basic');
      expect(items.length, 2);
    });

    test('lessonSetIdForItem resolves back to lessonSet', () {
      final item = graph.itemById('2.1.1')!;
      expect(bridge.lessonSetIdForItem(item), 'bfs_basic');
    });

    test('quizSetIdForItem resolves back to quizSet', () {
      final item = graph.itemById('2.1.1')!;
      expect(bridge.quizSetIdForItem(item), 'bfs_basic');
    });

    test('mistakeSetIdForItem returns null when no matching pickupGroup', () {
      final item = graph.itemById('2.1.1')!;
      expect(bridge.mistakeSetIdForItem(item), isNull);
    });

    test('lessonSetIdForItem returns null when pickupGroup is empty', () {
      final item = KnowledgeItem(id: 'x', name: 'test');
      expect(bridge.lessonSetIdForItem(item), isNull);
    });

    test('itemsForLessonSet returns empty for unknown lessonSet', () {
      expect(bridge.itemsForLessonSet('nonexistent'), isEmpty);
    });
  });

  group('C++ basic path', () {
    test('KnowledgeGraph has C++语法 category', () {
      final graph = _buildGraph([
        {
          'name': 'C++语法',
          'sections': [
            {
              'id': '1.1',
              'name': '程序基本结构',
              'level': 'L1',
              'pre': [],
              'items': [
                {
                  'id': '1.1.1',
                  'name': 'include',
                  'parent': '1.1',
                  'resolved_pre': [],
                },
              ],
            },
            {
              'id': '1.2',
              'name': '输入输出',
              'level': 'L1',
              'pre': ['1.1'],
              'items': [
                {
                  'id': '1.2.1',
                  'name': 'cin',
                  'parent': '1.2',
                  'resolved_pre': ['1.1'],
                },
              ],
            },
          ],
        },
      ]);

      final cpp = graph.categories.where((c) => c.name == 'C++语法').toList();
      expect(cpp.length, 1);
      expect(cpp.first.sections.length, 2);
      expect(cpp.first.sections.first.name, '程序基本结构');
    });

    test('C++语法 sections have items', () {
      final graph = _buildGraph([
        {
          'name': 'C++语法',
          'sections': [
            {
              'id': '1.1',
              'name': '程序基本结构',
              'level': 'L1',
              'pre': [],
              'items': [
                {
                  'id': '1.1.1',
                  'name': 'include',
                  'parent': '1.1',
                  'resolved_pre': [],
                },
                {
                  'id': '1.1.2',
                  'name': 'main',
                  'parent': '1.1',
                  'resolved_pre': [],
                },
              ],
            },
          ],
        },
      ]);

      final cpp = graph.categories.first;
      expect(cpp.sections.first.items.length, 2);
    });

    test('C++语法 section order from JSON preserved', () {
      final graph = _buildGraph([
        {
          'name': 'C++语法',
          'sections': [
            {'id': '1.3', 'name': '变量', 'level': 'L1', 'items': []},
            {'id': '1.1', 'name': '程序基本结构', 'level': 'L1', 'items': []},
            {'id': '1.2', 'name': '输入输出', 'level': 'L1', 'items': []},
          ],
        },
      ]);

      final sections = graph.categories.first.sections;
      expect(sections[0].id, '1.3');
      expect(sections[1].id, '1.1');
      expect(sections[2].id, '1.2');
    });

    test('content_manifest cpp_basic module has route /cpp_basic', () {
      final manifest = ContentManifest.fromJson({
        'modules': [
          {
            'moduleId': 'cpp_basic',
            'title': 'C++基础',
            'iconKey': 'terminal',
            'colorHex': '#00897B',
            'route': '/cpp_basic',
            'order': 3,
          },
        ],
      });
      final module = manifest.modules.first;
      expect(module.moduleId, 'cpp_basic');
      expect(module.route, '/cpp_basic');
    });
  });
}
