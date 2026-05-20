import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';

const _mathAllowlistItemIds = <String>{
  '4.0.1',
  '4.0.2',
  '4.2.8',
  '4.2.9',
  '4.6.9',
  '4.6.10',
};

void main() {
  group('Algorithm learning assets', () {
    late CppLearningManifest manifest;
    late List<CppLearningUnit> allUnits;
    late Set<String> allItemIds;
    late KnowledgeGraph graph;

    Future<Map<String, dynamic>> readJson(String assetPath) async {
      final file = File(assetPath);
      if (!await file.exists()) {
        throw StateError('Asset file not found: $assetPath');
      }
      final raw = await file.readAsString(encoding: utf8);
      return jsonDecode(raw) as Map<String, dynamic>;
    }

    setUpAll(() async {
      final manifestMap = await readJson(
        'assets/data/algorithm/algorithm_learning_manifest.json',
      );
      manifest = CppLearningManifest.fromJson(manifestMap);

      allUnits = [];
      allItemIds = {};

      final baseUnits =
          CppLearningContent.fromJson(await readJson(manifest.baseFile)).units;
      for (final u in baseUnits) {
        if (allItemIds.contains(u.itemId)) {
          throw StateError(
            'Duplicate itemId ${u.itemId} in ${manifest.baseFile}',
          );
        }
        allItemIds.add(u.itemId);
        allUnits.add(u);
      }

      for (final sf in manifest.sectionFiles) {
        final sectionUnits =
            CppLearningContent.fromJson(await readJson(sf)).units;
        for (final u in sectionUnits) {
          if (allItemIds.contains(u.itemId)) {
            throw StateError('Duplicate itemId ${u.itemId} in $sf');
          }
          allItemIds.add(u.itemId);
          allUnits.add(u);
        }
      }

      final graphMap = await readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('manifest is valid and readable', () {
      expect(manifest.version, 1);
      expect(manifest.category, isNotEmpty);
      expect(manifest.baseFile, isNotEmpty);
      expect(manifest.sectionFiles, isNotEmpty);
    });

    test('all section files are valid JSON and parseable', () {
      expect(allUnits.isNotEmpty, isTrue, reason: 'No units loaded at all');
    });

    test('no duplicate itemId across all files', () {
      expect(
        allItemIds.length,
        allUnits.length,
        reason:
            '${allUnits.length} units loaded but only ${allItemIds.length} unique itemIds',
      );
    });

    test('every unit itemId exists in knowledge graph', () {
      final missing = <String>[];
      for (final id in allItemIds) {
        if (graph.itemById(id) == null) {
          missing.add(id);
        }
      }
      expect(
        missing,
        isEmpty,
        reason:
            'These algorithm itemIds not found in knowledge graph: ${missing.join(', ')}',
      );
    });

    test('every unit has non-empty itemId, title, explanation', () {
      final errors = <String>[];
      for (final u in allUnits) {
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

    test('every unit has at least one of exampleCode, practice, or quiz', () {
      final empty = <String>[];
      for (final u in allUnits) {
        final hasContent =
            u.exampleCode.isNotEmpty ||
            u.practice.prompt.isNotEmpty ||
            u.quiz.isNotEmpty;
        if (!hasContent) {
          empty.add(u.itemId);
        }
      }
      expect(
        empty,
        isEmpty,
        reason:
            'These algorithm units have no exampleCode, practice, or quiz: ${empty.join(', ')}',
      );
    });

    test('every quiz has exactly 4 options', () {
      final errors = <String>[];
      for (final u in allUnits) {
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

    test('every quiz answerIndex is valid (0..options.length-1)', () {
      final errors = <String>[];
      for (final u in allUnits) {
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
  });

  group('Math learning assets', () {
    late CppLearningManifest manifest;
    late List<CppLearningUnit> allUnits;
    late Set<String> allItemIds;
    late KnowledgeGraph graph;

    Future<Map<String, dynamic>> readJson(String assetPath) async {
      final file = File(assetPath);
      if (!await file.exists()) {
        throw StateError('Asset file not found: $assetPath');
      }
      final raw = await file.readAsString(encoding: utf8);
      return jsonDecode(raw) as Map<String, dynamic>;
    }

    setUpAll(() async {
      final manifestMap = await readJson(
        'assets/data/math/math_learning_manifest.json',
      );
      manifest = CppLearningManifest.fromJson(manifestMap);

      allUnits = [];
      allItemIds = {};

      final baseUnits =
          CppLearningContent.fromJson(await readJson(manifest.baseFile)).units;
      for (final u in baseUnits) {
        if (allItemIds.contains(u.itemId)) {
          throw StateError(
            'Duplicate itemId ${u.itemId} in ${manifest.baseFile}',
          );
        }
        allItemIds.add(u.itemId);
        allUnits.add(u);
      }

      for (final sf in manifest.sectionFiles) {
        final sectionUnits =
            CppLearningContent.fromJson(await readJson(sf)).units;
        for (final u in sectionUnits) {
          if (allItemIds.contains(u.itemId)) {
            throw StateError('Duplicate itemId ${u.itemId} in $sf');
          }
          allItemIds.add(u.itemId);
          allUnits.add(u);
        }
      }

      final graphMap = await readJson('assets/data/knowledge/io_v4_4.json');
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('manifest is valid and readable', () {
      expect(manifest.version, 1);
      expect(manifest.category, isNotEmpty);
      expect(manifest.baseFile, isNotEmpty);
      expect(manifest.sectionFiles, isNotEmpty);
    });

    test('all section files are valid JSON and parseable', () {
      expect(allUnits.isNotEmpty, isTrue, reason: 'No units loaded at all');
    });

    test('no duplicate itemId across all files', () {
      expect(
        allItemIds.length,
        allUnits.length,
        reason:
            '${allUnits.length} units loaded but only ${allItemIds.length} unique itemIds',
      );
    });

    test('every unit itemId exists in knowledge graph (except allowlisted)', () {
      final missing = <String>[];
      for (final id in allItemIds) {
        if (graph.itemById(id) == null && !_mathAllowlistItemIds.contains(id)) {
          missing.add(id);
        }
      }
      expect(
        missing,
        isEmpty,
        reason:
            'These math itemIds not found in knowledge graph and not in allowlist: '
            '${missing.join(', ')}. '
            'Current allowlist (units not yet in KG): ${_mathAllowlistItemIds.join(', ')}',
      );
    });

    test('allowlisted itemIds are known and documented', () {
      for (final id in _mathAllowlistItemIds) {
        final hasUnit = allItemIds.contains(id);
        expect(
          hasUnit,
          isTrue,
          reason:
              'Allowlisted itemId $id does not exist in math assets. '
              'Remove it from the allowlist if no longer needed.',
        );
      }
    });

    test('every unit has non-empty itemId, title, explanation', () {
      final errors = <String>[];
      for (final u in allUnits) {
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

    test('every unit has at least one of exampleCode, practice, or quiz', () {
      final empty = <String>[];
      for (final u in allUnits) {
        final hasContent =
            u.exampleCode.isNotEmpty ||
            u.practice.prompt.isNotEmpty ||
            u.quiz.isNotEmpty;
        if (!hasContent) {
          empty.add(u.itemId);
        }
      }
      expect(
        empty,
        isEmpty,
        reason:
            'These math units have no exampleCode, practice, or quiz: ${empty.join(', ')}',
      );
    });

    test('every quiz has exactly 4 options', () {
      final errors = <String>[];
      for (final u in allUnits) {
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

    test('every quiz answerIndex is valid (0..options.length-1)', () {
      final errors = <String>[];
      for (final u in allUnits) {
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
  });
}
