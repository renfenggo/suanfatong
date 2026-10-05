import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';

const _dpSectionItemIds = <String>{
  '2.8.1',
  '2.8.2',
  '2.8.3',
  '2.8.36',
  '2.8.5',
  '2.8.6',
  '2.8.7',
  '2.8.12',
  '2.8.13',
  '2.8.19',
  '2.8.20',
  '2.8.21',
  '2.8.23',
  '2.8.26',
};

Future<Map<String, dynamic>> _readJson(String assetPath) async {
  final file = File(assetPath);
  if (!await file.exists()) {
    throw StateError('Asset file not found: $assetPath');
  }
  final raw = await file.readAsString(encoding: utf8);
  return jsonDecode(raw) as Map<String, dynamic>;
}

void main() {
  group('DP learning assets', () {
    late List<CppLearningUnit> dpUnits;
    late Set<String> dpItemIds;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final manifestMap = await _readJson(
        'assets/data/algorithm/algorithm_learning_manifest.json',
      );
      final manifest = CppLearningManifest.fromJson(manifestMap);

      final allUnits = <CppLearningUnit>[];
      final allItemIds = <String>{};

      final baseUnits =
          CppLearningContent.fromJson(await _readJson(manifest.baseFile)).units;
      for (final u in baseUnits) {
        allItemIds.add(u.itemId);
        allUnits.add(u);
      }

      for (final sf in manifest.sectionFiles) {
        final sectionUnits =
            CppLearningContent.fromJson(await _readJson(sf)).units;
        for (final u in sectionUnits) {
          allItemIds.add(u.itemId);
          allUnits.add(u);
        }
      }

      dpUnits =
          allUnits.where((u) => _dpSectionItemIds.contains(u.itemId)).toList();
      dpItemIds = dpUnits.map((u) => u.itemId).toSet();

      final graphMap = await _readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('all DP items have learning content', () {
      final missing = <String>[];
      for (final id in _dpSectionItemIds) {
        if (!dpItemIds.contains(id)) {
          missing.add(id);
        }
      }
      expect(
        missing,
        isEmpty,
        reason:
            'These DP items are in the knowledge graph but have no learning content: ${missing.join(', ')}',
      );
    });

    test('every DP learning unit itemId exists in knowledge graph', () {
      final missing = <String>[];
      for (final id in dpItemIds) {
        if (graph.itemById(id) == null) {
          missing.add(id);
        }
      }
      expect(
        missing,
        isEmpty,
        reason:
            'These DP itemIds not found in knowledge graph: ${missing.join(', ')}',
      );
    });

    test('every DP unit has non-empty itemId, title, explanation', () {
      final errors = <String>[];
      for (final u in dpUnits) {
        if (u.itemId.isEmpty) errors.add('[${u.title}] itemId is empty');
        if (u.title.isEmpty) errors.add('[${u.itemId}] title is empty');
        if (u.explanation.isEmpty && u.learningGoal.isEmpty) {
          errors.add(
            '[${u.itemId}] both explanation and learningGoal are empty',
          );
        }
      }
      expect(errors, isEmpty, reason: errors.take(20).join('\n'));
    });

    test('every DP unit has exampleCode', () {
      final empty = <String>[];
      for (final u in dpUnits) {
        if (u.exampleCode.isEmpty) {
          empty.add(u.itemId);
        }
      }
      expect(
        empty,
        isEmpty,
        reason: 'These DP units have no exampleCode: ${empty.join(', ')}',
      );
    });

    test('exampleCode does not contain multiple main functions', () {
      final errors = <String>[];
      for (final u in dpUnits) {
        if (u.exampleCode.isEmpty) continue;
        final mainCount = 'int main()'.allMatches(u.exampleCode).length;
        if (mainCount > 1) {
          errors.add('${u.itemId} has $mainCount main functions');
        }
      }
      expect(errors, isEmpty, reason: errors.join('\n'));
    });

    test('every DP unit has at least 2 quiz questions', () {
      final few = <String>[];
      for (final u in dpUnits) {
        if (u.quiz.length < 2) {
          few.add('${u.itemId} (${u.quiz.length} quizzes)');
        }
      }
      expect(
        few,
        isEmpty,
        reason:
            'These DP units have fewer than 2 quiz questions: ${few.join(', ')}',
      );
    });

    test('every quiz has exactly 4 options', () {
      final errors = <String>[];
      for (final u in dpUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          if (q.options.isNotEmpty && q.options.length != 4) {
            errors.add(
              '${u.itemId} quiz[$i] has ${q.options.length} options (expected 4)',
            );
          }
        }
      }
      expect(errors, isEmpty, reason: errors.take(20).join('\n'));
    });

    test('every quiz answerIndex is valid (0..3)', () {
      final errors = <String>[];
      for (final u in dpUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          if (q.options.isNotEmpty &&
              (q.answerIndex < 0 || q.answerIndex >= q.options.length)) {
            errors.add(
              '${u.itemId} quiz[$i] answerIndex=${q.answerIndex} out of range',
            );
          }
        }
      }
      expect(errors, isEmpty, reason: errors.take(20).join('\n'));
    });

    test('every DP unit has commonMistakes', () {
      final empty = <String>[];
      for (final u in dpUnits) {
        if (u.commonMistakes.isEmpty) {
          empty.add(u.itemId);
        }
      }
      expect(
        empty,
        isEmpty,
        reason: 'These DP units have no commonMistakes: ${empty.join(', ')}',
      );
    });

    test('every DP unit has practice', () {
      final empty = <String>[];
      for (final u in dpUnits) {
        if (u.practice.prompt.isEmpty) {
          empty.add(u.itemId);
        }
      }
      expect(
        empty,
        isEmpty,
        reason: 'These DP units have no practice prompt: ${empty.join(', ')}',
      );
    });
  });

  group('DP knowledge graph nodes', () {
    late KnowledgeGraph graph;

    setUpAll(() async {
      final graphMap = await _readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('section 2.8 has all expected curated DP items', () {
      final expectedIds = [
        '2.8.1',
        '2.8.2',
        '2.8.3',
        '2.8.36',
        '2.8.5',
        '2.8.6',
        '2.8.7',
        '2.8.12',
        '2.8.13',
        '2.8.19',
        '2.8.20',
        '2.8.21',
        '2.8.23',
        '2.8.26',
      ];
      for (final id in expectedIds) {
        final item = graph.itemById(id);
        expect(
          item,
          isNotNull,
          reason: 'Missing DP item $id in knowledge graph',
        );
      }
    });

    test('section 2.8 has all expected DP items', () {
      final expectedIds = ['2.8.1', '2.8.2', '2.8.3'];
      for (final id in expectedIds) {
        final item = graph.itemById(id);
        expect(
          item,
          isNotNull,
          reason: 'Missing DP item $id in knowledge graph',
        );
      }
    });

    test('DP item names contain expected keywords', () {
      final dpBasics = graph.itemById('2.8.1');
      expect(dpBasics, isNotNull);
      expect(dpBasics!.name, contains('DP'));

      final knapsack = graph.itemById('2.8.7');
      expect(knapsack, isNotNull);
      expect(knapsack!.name, contains('背包'));

      final interval = graph.itemById('2.8.12');
      expect(interval, isNotNull);
      expect(interval!.name, contains('区间'));

      final tree = graph.itemById('2.8.13');
      expect(tree, isNotNull);
      expect(tree!.name, contains('树形'));

      final bitmask = graph.itemById('2.8.20');
      expect(bitmask, isNotNull);
      expect(bitmask!.name, anyOf(contains('状态压缩'), contains('状压')));

      final digit = graph.itemById('2.8.21');
      expect(digit, isNotNull);
      expect(digit!.name, contains('数位'));

      final counting = graph.itemById('2.8.19');
      expect(counting, isNotNull);
      expect(counting!.name, contains('计数'));

      final prob = graph.itemById('2.8.23');
      expect(prob, isNotNull);
      expect(prob!.name, anyOf(contains('期望'), contains('概率')));
    });

    test('DP items have correct parent section', () {
      for (final id in _dpSectionItemIds) {
        final item = graph.itemById(id);
        expect(item, isNotNull);
        expect(item!.parent, equals('2.8'));
      }
    });

    test('DP items have valid direct_pre references', () {
      final allItemIds = graph.allItems.map((i) => i.id).toSet();
      for (final id in _dpSectionItemIds) {
        final item = graph.itemById(id);
        if (item != null && item.directPre.isNotEmpty) {
          for (final pre in item.directPre) {
            expect(
              allItemIds.contains(pre),
              isTrue,
              reason:
                  '$id has direct_pre "$pre" which does not exist in knowledge graph',
            );
          }
        }
      }
    });

    test('DP items are searchable by name or alias', () {
      final notSearchable = <String>[];
      for (final id in _dpSectionItemIds) {
        final item = graph.itemById(id);
        if (item != null) {
          final haystack = [item.name, ...item.alias].join(' ');
          if (!RegExp(
            r'DP|状态|转移|记忆化|背包|区间|树形|状压|状态压缩|数位|计数|期望|概率|动态规划',
          ).hasMatch(haystack)) {
            notSearchable.add(id);
          }
        }
      }
      expect(
        notSearchable,
        isEmpty,
        reason:
            'These DP items have neither searchable names nor aliases: '
            '${notSearchable.join(', ')}',
      );
    });
  });

  group('DP animation assets', () {
    late List<Map<String, dynamic>> animations;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final manifestMap = await _readJson(
        'assets/data/cpp/animations/cpp_animation_manifest.json',
      );
      final manifestList = manifestMap['animations'] as List<dynamic>;
      animations = manifestList.cast<Map<String, dynamic>>();

      final graphMap = await _readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('DP animations exist in manifest', () {
      final dpAnimationIds = [
        'cpp_dp_fib',
        'cpp_knapsack_01',
        'cpp_dp_house_robber',
        'cpp_dp_interval_stone',
        'cpp_dp_bitmask_tsp',
      ];
      final manifestIds =
          animations.map((a) => a['animationId'] as String).toSet();
      for (final id in dpAnimationIds) {
        expect(
          manifestIds.contains(id),
          isTrue,
          reason: 'DP animation $id not found in manifest',
        );
      }
    });

    test('DP animation assetPaths point to existing files', () async {
      final dpKeywords = [
        'dp',
        'knapsack',
        'house_robber',
        'interval_stone',
        'bitmask_tsp',
      ];
      final dpAnims = animations.where(
        (a) => dpKeywords.any((k) => (a['assetPath'] as String).contains(k)),
      );

      for (final anim in dpAnims) {
        final path = anim['assetPath'] as String;
        final file = File(path);
        final exists = await file.exists();
        expect(exists, isTrue, reason: 'Animation file not found: $path');
      }
    });

    test('DP animation itemIds exist in knowledge graph', () {
      final dpKeywords = [
        'dp',
        'knapsack',
        'house_robber',
        'interval_stone',
        'bitmask_tsp',
      ];
      final dpAnims = animations.where(
        (a) => dpKeywords.any((k) => (a['assetPath'] as String).contains(k)),
      );

      for (final anim in dpAnims) {
        final itemId = anim['itemId'] as String;
        final item = graph.itemById(itemId);
        expect(
          item,
          isNotNull,
          reason:
              'DP animation "${anim['animationId']}" references itemId "$itemId" which does not exist in knowledge graph',
        );
      }
    });

    test('DP animation JSON files are valid', () async {
      final dpKeywords = [
        'dp',
        'knapsack',
        'house_robber',
        'interval_stone',
        'bitmask_tsp',
      ];
      final dpAnims = animations.where(
        (a) => dpKeywords.any((k) => (a['assetPath'] as String).contains(k)),
      );

      for (final anim in dpAnims) {
        final path = anim['assetPath'] as String;
        final raw = await File(path).readAsString(encoding: utf8);
        expect(
          () => jsonDecode(raw),
          returnsNormally,
          reason: 'Animation file $path is not valid JSON',
        );
      }
    });
  });

  group('DP content searchability', () {
    late KnowledgeGraph graph;

    setUpAll(() async {
      final graphMap = await _readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    void assertSearchHits(String keyword, String description) {
      final hits = graph.allItems.where(
        (item) =>
            item.name.contains(keyword) ||
            item.alias.any((a) => a.contains(keyword)),
      );
      expect(
        hits.isNotEmpty,
        isTrue,
        reason: 'Search "$keyword" ($description) should find DP content',
      );
    }

    test('search DP finds content', () {
      assertSearchHits('DP', 'DP keyword');
    });

    test('search 动态规划 finds content', () {
      final hits = graph.allSections.where((s) => s.name.contains('动态规划'));
      expect(hits.isNotEmpty, isTrue, reason: 'Should find 动态规划 section');
    });

    test('search 背包 finds content', () {
      assertSearchHits('背包', 'knapsack keyword');
    });

    test('search 区间 finds content', () {
      assertSearchHits('区间', 'interval keyword');
    });

    test('search 状态压缩 finds content', () {
      assertSearchHits('状态压缩', 'bitmask keyword');
    });

    test('search 数位 finds content', () {
      assertSearchHits('数位', 'digit DP keyword');
    });

    test('search 计数 finds content', () {
      assertSearchHits('计数', 'counting DP keyword');
    });

    test('search 概率 finds content', () {
      assertSearchHits('概率', 'probability DP keyword');
    });
  });

  group('DP content UTF-8 quality', () {
    late List<CppLearningUnit> dpUnits;

    setUpAll(() async {
      final manifestMap = await _readJson(
        'assets/data/algorithm/algorithm_learning_manifest.json',
      );
      final manifest = CppLearningManifest.fromJson(manifestMap);

      final allUnits = <CppLearningUnit>[];
      final baseUnits =
          CppLearningContent.fromJson(await _readJson(manifest.baseFile)).units;
      allUnits.addAll(baseUnits);

      for (final sf in manifest.sectionFiles) {
        final sectionUnits =
            CppLearningContent.fromJson(await _readJson(sf)).units;
        allUnits.addAll(sectionUnits);
      }

      dpUnits =
          allUnits.where((u) => _dpSectionItemIds.contains(u.itemId)).toList();
    });

    test('no mojibake in DP titles', () {
      for (final u in dpUnits) {
        expect(
          u.title.contains('???'),
          isFalse,
          reason: '${u.itemId} title may have mojibake: ${u.title}',
        );
      }
    });

    test('no English placeholder text in DP content', () {
      final placeholders = ['TODO', 'PLACEHOLDER', 'FIXME', 'TBD', 'xxx'];
      for (final u in dpUnits) {
        for (final p in placeholders) {
          expect(
            u.title.toUpperCase(),
            isNot(contains(p)),
            reason: '${u.itemId} title contains placeholder "$p"',
          );
        }
      }
    });
  });
}
