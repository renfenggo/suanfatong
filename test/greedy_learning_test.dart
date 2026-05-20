import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';
import 'package:bfs_learn/models/cpp_animation.dart';

const _greedyItemIds = <String>{
  '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5', '2.4.6', '2.4.7', '2.4.8',
  '2.4.9', '2.4.10', '2.4.11', '2.4.12', '2.4.13', '2.4.14', '2.4.15',
  '2.4.16',
};

const _searchKeywords = <String>[
  '贪心', '排序贪心', '区间贪心', '交换论证', '双指针贪心',
  '堆贪心', '栈贪心', '反悔贪心', '贪心反例',
];

Future<Map<String, dynamic>> _readJson(String assetPath) async {
  final file = File(assetPath);
  if (!await file.exists()) {
    throw StateError('Asset file not found: $assetPath');
  }
  final raw = await file.readAsString(encoding: utf8);
  return jsonDecode(raw) as Map<String, dynamic>;
}

void main() {
  group('Greedy learning units', () {
    late List<CppLearningUnit> greedyUnits;
    late Set<String> greedyUnitIds;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final sectionA = CppLearningContent.fromJson(
        await _readJson('assets/data/algorithm/section_2_4_units.json'),
      );
      final sectionB = CppLearningContent.fromJson(
        await _readJson('assets/data/algorithm/section_2_4_b_units.json'),
      );

      greedyUnits = [...sectionA.units, ...sectionB.units];
      greedyUnitIds = greedyUnits.map((u) => u.itemId).toSet();

      final graphMap = await _readJson(
        'assets/data/knowledge/io_v4_4.json',
      );
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('all 16 greedy units are present', () {
      expect(greedyUnitIds, containsAll(_greedyItemIds));
      expect(greedyUnitIds.length, greaterThanOrEqualTo(16));
    });

    test('no duplicate greedy itemId', () {
      expect(greedyUnitIds.length, greedyUnits.length);
    });

    test('every greedy itemId exists in knowledge graph', () {
      final missing = <String>[];
      for (final id in greedyUnitIds) {
        if (graph.itemById(id) == null) {
          missing.add(id);
        }
      }
      expect(missing, isEmpty, reason: 'Missing in KG: ${missing.join(', ')}');
    });

    test('knowledge graph section 2.4 has at least 16 items', () {
      final section = graph.sectionById('2.4');
      expect(section, isNotNull, reason: 'Section 2.4 not found in KG');
      final items = graph.itemsOfSection('2.4');
      expect(items.length, greaterThanOrEqualTo(16));
    });

    test('every greedy unit has non-empty required fields', () {
      final errors = <String>[];
      for (final u in greedyUnits) {
        if (u.itemId.isEmpty) errors.add('[${u.title}] itemId empty');
        if (u.title.isEmpty) errors.add('[${u.itemId}] title empty');
        if (u.explanation.isEmpty && u.learningGoal.isEmpty) {
          errors.add('[${u.itemId}] both explanation and learningGoal empty');
        }
      }
      expect(errors, isEmpty, reason: errors.take(10).join('\n'));
    });

    test('every greedy unit has exampleCode with at most one main', () {
      final errors = <String>[];
      for (final u in greedyUnits) {
        if (u.exampleCode.isEmpty) continue;
        final mainCount = 'int main('.allMatches(u.exampleCode).length;
        if (mainCount > 1) {
          errors.add('${u.itemId} has $mainCount main functions');
        }
      }
      expect(errors, isEmpty, reason: errors.join('\n'));
    });

    test('every greedy unit has at least 2 quiz questions', () {
      final errors = <String>[];
      for (final u in greedyUnits) {
        if (u.quiz.length < 2) {
          errors.add('${u.itemId} has only ${u.quiz.length} quiz');
        }
      }
      expect(errors, isEmpty, reason: errors.join('\n'));
    });

    test('every quiz has exactly 4 options and valid answerIndex', () {
      final errors = <String>[];
      for (final u in greedyUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          if (q.options.length != 4) {
            errors.add(
              '${u.itemId} quiz[$i] has ${q.options.length} options',
            );
          }
          if (q.answerIndex < 0 || q.answerIndex >= 4) {
            errors.add(
              '${u.itemId} quiz[$i] answerIndex=${q.answerIndex} invalid',
            );
          }
        }
      }
      expect(errors, isEmpty, reason: errors.take(10).join('\n'));
    });

    test('every greedy unit has at least 2 commonMistakes', () {
      final errors = <String>[];
      for (final u in greedyUnits) {
        if (u.commonMistakes.length < 2) {
          errors.add(
            '${u.itemId} has only ${u.commonMistakes.length} mistakes',
          );
        }
      }
      expect(errors, isEmpty, reason: errors.join('\n'));
    });

    test('search keywords can find greedy content', () {
      final allText = greedyUnits
          .map((u) =>
              '${u.title} ${u.learningGoal} ${u.explanation} ${u.codeNotes.join(' ')}')
          .join(' ');

      final missing = <String>[];
      for (final kw in _searchKeywords) {
        if (!allText.contains(kw)) {
          missing.add(kw);
        }
      }
      expect(missing, isEmpty, reason: 'Keywords not found: ${missing.join(', ')}');
    });

    test('greedy units have valid parent reference in KG', () {
      final errors = <String>[];
      for (final id in greedyUnitIds) {
        final item = graph.itemById(id);
        if (item != null && item.parent != '2.4') {
          errors.add('$id has parent=${item.parent}, expected 2.4');
        }
      }
      expect(errors, isEmpty, reason: errors.join('\n'));
    });
  });

  group('Greedy animations', () {
    late CppAnimationManifest manifest;

    setUpAll(() async {
      final manifestMap = await _readJson(
        'assets/data/cpp/animations/cpp_animation_manifest.json',
      );
      manifest = CppAnimationManifest.fromJson(manifestMap);
    });

    test('greedy animation entries exist in manifest', () {
      final greedyIds = [
        'algo_greedy_activity_selection',
        'algo_greedy_interval_cover',
        'algo_greedy_huffman',
        'algo_greedy_two_pointer',
        'algo_greedy_stack',
        'algo_greedy_regret',
      ];
      for (final id in greedyIds) {
        final found = manifest.animations.any((a) => a.animationId == id);
        expect(found, isTrue, reason: 'Animation $id not in manifest');
      }
    });

    test('greedy animation asset files exist', () async {
      final greedyAnimations = manifest.animations
          .where((a) => a.animationId.startsWith('algo_greedy_'))
          .toList();

      expect(greedyAnimations.length, greaterThanOrEqualTo(6));

      for (final anim in greedyAnimations) {
        final file = File(anim.assetPath);
        final exists = await file.exists();
        expect(exists, isTrue, reason: '${anim.assetPath} does not exist');
      }
    });

    test('greedy animation asset files are valid JSON', () async {
      final greedyAnimations = manifest.animations
          .where((a) => a.animationId.startsWith('algo_greedy_'))
          .toList();

      for (final anim in greedyAnimations) {
        final raw = await File(anim.assetPath).readAsString(encoding: utf8);
        expect(
          () => jsonDecode(raw),
          returnsNormally,
          reason: '${anim.assetPath} is not valid JSON',
        );
      }
    });

    test('greedy animations have at least 8 steps', () async {
      final greedyAnimations = manifest.animations
          .where((a) => a.animationId.startsWith('algo_greedy_'))
          .toList();

      for (final anim in greedyAnimations) {
        final raw = await File(anim.assetPath).readAsString(encoding: utf8);
        final json = jsonDecode(raw) as Map<String, dynamic>;
        final steps = json['steps'] as List;
        expect(
          steps.length,
          greaterThanOrEqualTo(8),
          reason: '${anim.animationId} has only ${steps.length} steps',
        );
      }
    });
  });

  group('Greedy no mojibake', () {
    test('greedy JSON files contain no mojibake patterns', () async {
      final files = [
        'assets/data/algorithm/section_2_4_units.json',
        'assets/data/algorithm/section_2_4_b_units.json',
      ];
      for (final path in files) {
        final raw = await File(path).readAsString(encoding: utf8);
        expect(raw, isNot(contains('ä')), reason: '$path has mojibake');
        expect(raw, isNot(contains('Ã')), reason: '$path has mojibake');
        expect(raw, isNot(contains('æ')), reason: '$path has mojibake');
      }
    });
  });
}
