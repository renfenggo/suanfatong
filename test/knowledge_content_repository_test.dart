import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/knowledge_content_index.dart';
import 'package:bfs_learn/models/knowledge_content_item.dart';
import 'package:bfs_learn/repositories/content_index_repository.dart';
import 'package:bfs_learn/repositories/json_asset_repository.dart';
import 'package:bfs_learn/repositories/knowledge_content_repository.dart';
import 'package:bfs_learn/widgets/knowledge/knowledge_content_section.dart';

/// fake 资产仓库：按 path 返回预置内容，用于降级路径测试。
class _FakeJsonAssetRepository implements JsonAssetRepository {
  final Map<String, dynamic> assets;
  final Set<String> requestedPaths = {};

  _FakeJsonAssetRepository(this.assets);

  @override
  Future<Map<String, dynamic>> loadMap(String assetPath) async {
    requestedPaths.add(assetPath);
    final value = assets[assetPath];
    if (value is! Map) {
      throw FormatException('asset not found: $assetPath');
    }
    return value.cast<String, dynamic>();
  }

  @override
  Future<List<dynamic>> loadList(String assetPath) async {
    requestedPaths.add(assetPath);
    final value = assets[assetPath];
    if (value is! List) {
      throw FormatException('asset not found: $assetPath');
    }
    return value;
  }
}

/// 总是抛异常的仓库。
class _ThrowingJsonAssetRepository implements JsonAssetRepository {
  @override
  Future<Map<String, dynamic>> loadMap(String assetPath) async {
    throw Exception('boom: $assetPath');
  }

  @override
  Future<List<dynamic>> loadList(String assetPath) async {
    throw Exception('boom: $assetPath');
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ContentIndexRepository（真实 content_index.json）', () {
    late ContentIndexRepository repo;

    setUp(() {
      repo = ContentIndexRepository(jsonRepo: JsonAssetRepository());
    });

    test('解析生产元信息：33 分片 / 3240 节点 / 全部 passed', () async {
      final index = await repo.loadIndex();
      expect(index.version, isNotEmpty);
      expect(index.totalParts, 33);
      expect(index.generatedItemCount, 3240);
      expect(index.parts.length, 33);
      // 分片终态方言：stage4 批次为 passed，stage5_hard 批次为 generated
      expect(
        index.parts.every(
          (p) => p.status == 'passed' || p.status == 'generated',
        ),
        isTrue,
      );
      expect(index.parts.every((p) => p.filename.isNotEmpty), isTrue);
      expect(index.parts.fold<int>(0, (sum, p) => sum + p.itemCount), 3240);
    });

    test('item_part_index 覆盖全部 3240 个图谱节点 id', () async {
      final graphStr = await rootBundle.loadString(
        'assets/data/knowledge/io_v4_4.json',
      );
      final graph = json.decode(graphStr) as Map<String, dynamic>;
      final graphIds = <String>{};
      for (final cat in graph['categories'] as List) {
        for (final section in (cat as Map)['sections'] as List) {
          for (final item in (section as Map)['items'] as List) {
            graphIds.add((item as Map)['id'] as String);
          }
        }
      }
      expect(graphIds.length, 3240);

      final indexStr = await rootBundle.loadString(
        'assets/data/knowledge_content/item_part_index.json',
      );
      final index = json.decode(indexStr) as Map<String, dynamic>;
      final items = index['items'] as Map<String, dynamic>;
      expect(items.length, 3240);
      expect(items.keys.toSet(), graphIds);
      expect(
        items.values.every((v) => v is String && v.endsWith('.json')),
        isTrue,
      );
    });
  });

  group('KnowledgeContentRepository（真实资产按需加载）', () {
    late KnowledgeContentRepository repo;

    setUp(() {
      repo = KnowledgeContentRepository(jsonRepo: JsonAssetRepository());
    });

    test('索引首个分片的首个 item 可加载且字段完整', () async {
      final first = await repo.loadItem('2.1.1');
      expect(first, isNotNull);
      expect(first!.itemId, '2.1.1');
      expect(first.title, isNotEmpty);
      expect(first.shortExplanation, isNotEmpty);
      expect(first.learningGoal, isNotEmpty);
      expect(first.stepByStep, isNotEmpty);
      expect(first.quiz, isNotEmpty);
      expect(first.quiz.first.options, isNotEmpty);
    });

    test('首个图谱节点（C++语法起点）也可加载', () async {
      final item = await repo.loadItem('1.1.1');
      expect(item, isNotNull);
      expect(item!.itemId, '1.1.1');
    });

    test('未收录 / 空白 item_id 降级返回 null', () async {
      expect(await repo.loadItem('9.9.9'), isNull);
      expect(await repo.loadItem(''), isNull);
    });

    test('同分片缓存：两个 item 只缓存一个分片', () async {
      // 2.1.1 与 2.1.2 同在 stage4_batch1_part_001
      final a = await repo.loadItem('2.1.1');
      final b = await repo.loadItem('2.1.2');
      expect(a, isNotNull);
      expect(b, isNotNull);
      expect(repo.cachedPartCount, 1);
    });

    test('LRU 淘汰：maxCachedParts=1 时跨分片加载只留最新', () async {
      final small = KnowledgeContentRepository(
        jsonRepo: JsonAssetRepository(),
        maxCachedParts: 1,
      );
      final a = await small.loadItem('2.1.1'); // stage4_batch1_part_001
      final b = await small.loadItem('1.1.1'); // 不同分片
      expect(a, isNotNull);
      expect(b, isNotNull);
      expect(small.cachedPartCount, 1);
      expect(await small.partForItem('2.1.1'), isNotNull);
    });

    test('partForItem 与 indexedItemCount', () async {
      expect(await repo.partForItem('2.1.1'), 'stage4_batch1_part_001.json');
      expect(await repo.partForItem('9.9.9'), isNull);
      expect(await repo.indexedItemCount(), 3240);
    });
  });

  group('KnowledgeContentRepository（降级路径）', () {
    test('索引缺失返回 null', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _FakeJsonAssetRepository({}),
      );
      expect(await repo.loadItem('2.1.1'), isNull);
      expect(await repo.indexedItemCount(), 0);
    });

    test('索引结构损坏（items 非 Map）返回 null', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _FakeJsonAssetRepository({
          'assets/data/knowledge_content/item_part_index.json': {
            'version': 1,
            'items': <dynamic>[1, 2, 3],
          },
        }),
      );
      expect(await repo.loadItem('2.1.1'), isNull);
    });

    test('分片文件缺失返回 null', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _FakeJsonAssetRepository({
          'assets/data/knowledge_content/item_part_index.json': {
            'version': 1,
            'items': {'2.1.1': 'missing_part.json'},
          },
        }),
      );
      expect(await repo.loadItem('2.1.1'), isNull);
    });

    test('坏 JSON（分片为非对象数组）返回 null', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _FakeJsonAssetRepository({
          'assets/data/knowledge_content/item_part_index.json': {
            'version': 1,
            'items': {'2.1.1': 'bad_part.json'},
          },
          'assets/data/knowledge_content/items/bad_part.json': <dynamic>[
            1,
            2,
            3,
          ],
        }),
      );
      expect(await repo.loadItem('2.1.1'), isNull);
    });

    test('坏记录跳过：缺必需字段的条目不阻塞同分片好记录', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _FakeJsonAssetRepository({
          'assets/data/knowledge_content/item_part_index.json': {
            'version': 1,
            'items': {'good.1.1': 'mix_part.json', 'bad.1.1': 'mix_part.json'},
          },
          'assets/data/knowledge_content/items/mix_part.json': [
            {'item_id': 'good.1.1', 'title': '好记录', 'short_explanation': 'OK'},
            // 缺 title/short_explanation 的坏记录
            {'item_id': 'bad.1.1'},
          ],
        }),
      );
      final good = await repo.loadItem('good.1.1');
      expect(good, isNotNull);
      expect(good!.title, '好记录');
      expect(await repo.loadItem('bad.1.1'), isNull);
    });

    test('底层仓库抛异常时全部降级为 null', () async {
      final repo = KnowledgeContentRepository(
        jsonRepo: _ThrowingJsonAssetRepository(),
      );
      expect(await repo.loadItem('2.1.1'), isNull);
      expect(await repo.partForItem('2.1.1'), isNull);
      expect(await repo.indexedItemCount(), 0);
    });
  });

  group('KnowledgeContentItem 模型 schema', () {
    test('缺少必需字段抛 FormatException', () {
      expect(
        () => KnowledgeContentItem.fromJson({'item_id': 'x'}),
        throwsFormatException,
      );
      expect(
        () => KnowledgeContentItem.fromJson({'item_id': 'x', 'title': 't'}),
        throwsFormatException,
      );
    });

    test('完整解析：quiz/动画计划/练习任务/掌握检查', () {
      final item = KnowledgeContentItem.fromJson({
        'item_id': 'x.1.1',
        'title': '测试知识点',
        'short_explanation': '简介',
        'learning_goal': '目标',
        'core_idea': '思想',
        'step_by_step': ['第一步', '第二步'],
        'common_mistakes': [
          {'mistake': '错', 'fix': '对'},
        ],
        'example': {
          'description': '例子',
          'pseudo_or_code': 'int main() {}',
          'notes': ['注'],
        },
        'quiz': [
          {
            'type': 'single_choice',
            'question': '问',
            'options': ['A', 'B'],
            'answer': 'A',
          },
          {'type': 'single_choice'}, // 空问题被过滤
        ],
        'animation_plan': {
          'suitable': true,
          'type': 'algorithm_process',
          'frames': [
            {
              'title': '帧',
              'visual_elements': ['a'],
            },
          ],
        },
        'practice_tasks': [
          {'task_type': 'explain', 'title': '解释'},
        ],
        'unlock_check': {'quick_question': '会了吗'},
      });
      expect(item.itemId, 'x.1.1');
      expect(item.stepByStep.length, 2);
      expect(item.commonMistakes.single.fix, '对');
      expect(item.example!.pseudoOrCode, 'int main() {}');
      expect(item.quiz.length, 1); // 空问题被过滤
      expect(item.animationPlan!.frames.single.title, '帧');
      expect(item.practiceTasks.single.taskType, 'explain');
      expect(item.unlockCheck!.quickQuestion, '会了吗');
    });

    test('KnowledgeContentIndex.fromJson 容错', () {
      final index = KnowledgeContentIndex.fromJson({});
      expect(index.version, '');
      expect(index.parts, isEmpty);
      final full = KnowledgeContentIndex.fromJson({
        'version': 'v1',
        'total_parts': 2,
        'parts': [
          {'filename': 'a.json', 'item_count': 100, 'status': 'passed'},
          'not-a-map',
        ],
      });
      expect(full.parts.length, 1);
      expect(full.parts.single.itemCount, 100);
    });
  });

  group('KnowledgeContentSection widget', () {
    testWidgets('渲染关键区块文案', (tester) async {
      final item = KnowledgeContentItem.fromJson({
        'item_id': '2.1.1',
        'title': '枚举',
        'section_name': '基础算法思想',
        'short_explanation': '一句话简介',
        'learning_goal': '学完能解释',
        'core_idea': '核心是流程',
        'step_by_step': ['先读题'],
        'common_mistakes': [
          {'mistake': '只记名字', 'fix': '先确认条件'},
        ],
        'example': {'description': '小例子', 'pseudo_or_code': 'step 1'},
        'quiz': [
          {
            'question': '第一步做什么？',
            'options': ['读题', '写码'],
            'answer': '读题',
          },
        ],
        'practice_tasks': [
          {'task_type': 'explain', 'title': '用自己的话解释'},
        ],
        'unlock_check': {'quick_question': '何时使用枚举？'},
      });
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: KnowledgeContentSection(item: item),
            ),
          ),
        ),
      );
      expect(find.text('知识讲解'), findsOneWidget);
      expect(find.text('内容简介'), findsOneWidget);
      expect(find.text('学习目标'), findsOneWidget);
      expect(find.text('核心思想'), findsOneWidget);
      expect(find.text('学习步骤'), findsOneWidget);
      expect(find.text('常见错误与纠正'), findsOneWidget);
      expect(find.text('随堂自测'), findsOneWidget);
      expect(find.text('练习任务'), findsOneWidget);
      expect(find.text('掌握检查'), findsOneWidget);
      expect(find.text('一句话简介'), findsOneWidget);
      expect(find.textContaining('Q1 第一步做什么？'), findsOneWidget);
      expect(find.textContaining('答案：读题'), findsOneWidget);
    });
  });
}
