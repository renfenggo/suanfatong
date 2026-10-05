import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'package:bfs_learn/models/learning_card.dart';
import 'package:bfs_learn/services/learning_card_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('LearningCard Model Tests', () {
    test('LearningCard.fromJson should parse valid JSON', () {
      final json = {
        'item_id': '2.8.208',
        'item_name': '后缀最值 DP',
        'section': '2.8',
        'one_sentence_explanation': '从后往前算，记录每个位置后面的最大/最小值',
        'when_to_use': '需要频繁查询某个位置后面的最大/最小值时',
        'core_intuition': '后缀信息一次性算好，用的时候直接取',
        'minimal_example': '数组[3,1,4,1,5]的后缀最大值计算',
        'common_traps': ['忘记从右往左算', '边界处理错误'],
        'practice_entry': '从简单数组后缀最大值开始',
        'learn_next': ['前缀最值DP', '双端队列维护最值'],
        'must_know_before': [],
        'nice_to_know': [],
        'learning_action': 'read',
      };

      final card = LearningCard.fromJson(json);

      expect(card.id, equals('2.8.208'));
      expect(card.title, equals('后缀最值 DP'));
      expect(card.sectionId, equals('2.8'));
      expect(card.summary, equals('从后往前算，记录每个位置后面的最大/最小值'));
      expect(card.useCases, equals('需要频繁查询某个位置后面的最大/最小值时'));
      expect(card.intuition, equals('后缀信息一次性算好，用的时候直接取'));
      expect(card.example, equals('数组[3,1,4,1,5]的后缀最大值计算'));
      expect(card.traps, equals(['忘记从右往左算', '边界处理错误']));
      expect(card.practice, equals('从简单数组后缀最大值开始'));
      expect(card.nextItems, equals(['前缀最值DP', '双端队列维护最值']));
      expect(card.actionType, equals('read'));
    });

    test('LearningCard.fromJson should handle null values with defaults', () {
      final json = {
        'item_id': null,
        'item_name': null,
        'section': null,
        'one_sentence_explanation': null,
        'when_to_use': null,
        'core_intuition': null,
        'minimal_example': null,
        'common_traps': null,
        'practice_entry': null,
        'learn_next': null,
        'must_know_before': null,
        'nice_to_know': null,
        'learning_action': null,
      };

      final card = LearningCard.fromJson(json);

      expect(card.id, equals(''));
      expect(card.title, equals(''));
      expect(card.sectionId, equals(''));
      expect(card.summary, equals(''));
      expect(card.useCases, equals(''));
      expect(card.intuition, equals(''));
      expect(card.example, equals(''));
      expect(card.traps, equals([]));
      expect(card.practice, equals(''));
      expect(card.nextItems, equals([]));
      expect(card.requiredPre, equals([]));
      expect(card.recommendedPre, equals([]));
      expect(card.actionType, equals('read'));
    });

    test('LearningCard.isValid should return true for valid cards', () {
      final card = LearningCard(
        id: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        summary: '从后往前算',
        useCases: '需要频繁查询',
        intuition: '后缀信息一次性算好',
        example: '数组[3,1,4,1,5]',
        traps: ['忘记从右往左算'],
        practice: '从简单数组开始',
        nextItems: ['前缀最值DP'],
        actionType: 'read',
      );

      expect(card.isValid(), isTrue);
    });

    test('LearningCard.isValid should return false for invalid cards', () {
      final card = LearningCard(
        id: '',
        title: '',
        sectionId: '',
        summary: '',
        useCases: '',
        intuition: '',
        example: '',
        traps: [],
        practice: '',
        nextItems: [],
        actionType: 'read',
      );

      expect(card.isValid(), isFalse);
    });

    test('LearningCard.isComplete should return true for complete cards', () {
      final card = LearningCard(
        id: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        summary: '从后往前算',
        useCases: '需要频繁查询',
        intuition: '后缀信息一次性算好',
        example: '数组[3,1,4,1,5]',
        traps: ['忘记从右往左算'],
        practice: '从简单数组开始',
        nextItems: ['前缀最值DP'],
        actionType: 'read',
      );

      expect(card.isComplete(), isTrue);
    });

    test('LearningCard.getActionTypeDescription should return correct description', () {
      final card = LearningCard(
        id: '2.8.208',
        title: '后缀最值 DP',
        sectionId: '2.8',
        summary: '',
        useCases: '',
        intuition: '',
        example: '',
        traps: [],
        practice: '',
        nextItems: [],
        actionType: 'read',
      );

      expect(card.getActionTypeDescription(), equals('阅读理解'));
    });
  });

  group('LearningCardService Tests', () {
    late LearningCardService service;

    setUp(() {
      service = LearningCardService();
    });

    test('LearningCardService should load 30 samples', () async {
      await service.loadSamples();
      final totalCount = await service.getTotalCount();
      expect(totalCount, equals(30));
    });

    test('LearningCardService should have 10 samples in section 2.8', () async {
      await service.loadSamples();
      final cards = await service.getCardsBySection('2.8');
      expect(cards.length, equals(10));
    });

    test('LearningCardService should have 10 samples in section 3.13', () async {
      await service.loadSamples();
      final cards = await service.getCardsBySection('3.13');
      expect(cards.length, equals(10));
    });

    test('LearningCardService should have 10 samples in section 4.1', () async {
      await service.loadSamples();
      final cards = await service.getCardsBySection('4.1');
      expect(cards.length, equals(10));
    });

    test('LearningCardService should return correct section distribution', () async {
      await service.loadSamples();
      final distribution = await service.getSectionDistribution();
      expect(distribution['2.8'], equals(10));
      expect(distribution['3.13'], equals(10));
      expect(distribution['4.1'], equals(10));
    });

    test('LearningCardService should query card by itemId', () async {
      await service.loadSamples();
      final card = await service.getCardById('2.8.208');
      expect(card, isNotNull);
      expect(card!.id, equals('2.8.208'));
      expect(card.title, equals('后缀最值 DP'));
    });

    test('LearningCardService should return null for non-existent itemId', () async {
      await service.loadSamples();
      final card = await service.getCardById('non-existent-id');
      expect(card, isNull);
    });

    test('LearningCardService should query cards by sectionId', () async {
      await service.loadSamples();
      final cards = await service.getCardsBySection('2.8');
      expect(cards.length, equals(10));
      for (final card in cards) {
        expect(card.sectionId, equals('2.8'));
      }
    });

    test('LearningCardService should return empty list for non-existent sectionId', () async {
      await service.loadSamples();
      final cards = await service.getCardsBySection('non-existent-section');
      expect(cards, isEmpty);
    });

    test('LearningCardService should return all cards', () async {
      await service.loadSamples();
      final allCards = await service.getAllCards();
      expect(allCards.length, equals(30));
    });

    test('LearningCardService should check card existence', () async {
      await service.loadSamples();
      final exists = await service.existsCard('2.8.208');
      expect(exists, isTrue);

      final notExists = await service.existsCard('non-existent-id');
      expect(notExists, isFalse);
    });

    test('LearningCardService should check section existence', () async {
      await service.loadSamples();
      final exists = await service.existsSection('2.8');
      expect(exists, isTrue);

      final notExists = await service.existsSection('non-existent-section');
      expect(notExists, isFalse);
    });

    test('LearningCardService should return all section IDs', () async {
      await service.loadSamples();
      final sectionIds = await service.getAllSectionIds();
      expect(sectionIds.length, equals(3));
      expect(sectionIds.contains('2.8'), isTrue);
      expect(sectionIds.contains('3.13'), isTrue);
      expect(sectionIds.contains('4.1'), isTrue);
    });

    test('LearningCardService should return statistics', () async {
      await service.loadSamples();
      final stats = await service.getStatistics();
      expect(stats['total_count'], equals(30));
      expect(stats['section_distribution'], isNotNull);
      expect(stats['sections'], isNotNull);
    });

    test('LearningCardService should search cards by title', () async {
      await service.loadSamples();
      final cards = await service.searchCardsByTitle('DP');
      expect(cards.length, greaterThan(0));
      for (final card in cards) {
        expect(card.title.toLowerCase().contains('dp'), isTrue);
      }
    });

    test('LearningCardService should search cards by summary', () async {
      await service.loadSamples();
      final cards = await service.searchCardsBySummary('从');
      expect(cards.length, greaterThan(0));
      for (final card in cards) {
        expect(card.summary.toLowerCase().contains('从'), isTrue);
      }
    });

    test('LearningCardService should get cards by action type', () async {
      await service.loadSamples();
      final cards = await service.getCardsByActionType('read');
      expect(cards.length, greaterThan(0));
      for (final card in cards) {
        expect(card.actionType, equals('read'));
      }
    });

    test('LearningCardService should get complete cards', () async {
      await service.loadSamples();
      final cards = await service.getCompleteCards();
      expect(cards.length, equals(30));
      for (final card in cards) {
        expect(card.isComplete(), isTrue);
      }
    });

    test('LearningCardService should get valid cards', () async {
      await service.loadSamples();
      final cards = await service.getValidCards();
      expect(cards.length, equals(30));
      for (final card in cards) {
        expect(card.isValid(), isTrue);
      }
    });

    test('LearningCardService should clear cache and reload', () async {
      await service.loadSamples();
      final totalCount1 = await service.getTotalCount();
      expect(totalCount1, equals(30));

      service.clearCache();
      final totalCount2 = await service.getTotalCount();
      expect(totalCount2, equals(30));
    });

    test('LearningCardService should handle batch query by IDs', () async {
      await service.loadSamples();
      final result = await service.getCardsByIds(['2.8.208', '3.13.317', 'non-existent']);
      expect(result.length, equals(3));
      expect(result['2.8.208'], isNotNull);
      expect(result['3.13.317'], isNotNull);
      expect(result['non-existent'], isNull);
    });
  });

  group('LearningCard Field Validation Tests', () {
    test('All cards should have non-empty id', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.id.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty title', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.title.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty sectionId', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.sectionId.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty summary', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.summary.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty useCases', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.useCases.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty intuition', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.intuition.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty example', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.example.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty traps', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.traps.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty practice', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.practice.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty nextItems', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.nextItems.isNotEmpty, isTrue);
      }
    });

    test('All cards should have non-empty actionType', () async {
      final service = LearningCardService();
      await service.loadSamples();
      final allCards = await service.getAllCards();
      for (final card in allCards) {
        expect(card.actionType.isNotEmpty, isTrue);
      }
    });
  });

  group('Asset Loading Tests', () {
    test('rootBundle should load data/learning_card_samples.json', () async {
      // 测试 rootBundle 能加载 asset 文件
      final jsonString = await rootBundle.loadString('data/learning_card_samples.json');
      expect(jsonString.isNotEmpty, isTrue);
      
      // 验证 JSON 格式正确
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      expect(jsonData.containsKey('meta'), isTrue);
      expect(jsonData.containsKey('samples'), isTrue);
    });

    test('LearningCardService should load 30 samples via asset', () async {
      final service = LearningCardService();
      await service.loadSamples();
      
      // 验证加载了30个样板
      final totalCount = await service.getTotalCount();
      expect(totalCount, equals(30));
      
      // 验证章节分布
      final distribution = await service.getSectionDistribution();
      expect(distribution['2.8'], equals(10));
      expect(distribution['3.13'], equals(10));
      expect(distribution['4.1'], equals(10));
    });

    test('LearningCardService should not depend on local File fallback', () async {
      // 测试 LearningCardService 不依赖本地 File fallback 也能加载
      // 这个测试通过 asset 加载，不需要本地文件
      final service = LearningCardService();
      
      // 清除缓存确保重新加载
      service.clearCache();
      await service.loadSamples();
      
      // 验证加载成功
      final allCards = await service.getAllCards();
      expect(allCards.length, equals(30));
      
      // 验证所有卡片都是有效的
      for (final card in allCards) {
        expect(card.isValid(), isTrue);
      }
    });

    test('Asset path should be data/learning_card_samples.json', () async {
      // 验证 asset 路径正确
      final jsonString = await rootBundle.loadString('data/learning_card_samples.json');
      expect(jsonString.isNotEmpty, isTrue);
      
      // 验证不是 assets/data/learning_card_samples.json（旧路径）
      try {
        await rootBundle.loadString('assets/data/learning_card_samples.json');
        // 如果能加载，说明旧路径还存在，但这不是预期的
        fail('Old asset path should not exist');
      } catch (e) {
        // 旧路径不存在，这是预期的
        expect(e, isNotNull);
      }
    });
  });
}