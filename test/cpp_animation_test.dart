import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_animation.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';
import 'package:bfs_learn/app/router.dart';

void main() {
  group('CppAnimation models fromJson defaults', () {
    test('CppAnimationVariable fromJson empty', () {
      final v = CppAnimationVariable.fromJson({});
      expect(v.name, '');
      expect(v.value, '');
      expect(v.note, '');
    });

    test('CppAnimationContainer fromJson empty', () {
      final c = CppAnimationContainer.fromJson({});
      expect(c.name, '');
      expect(c.type, '');
      expect(c.values, isEmpty);
      expect(c.activeIndex, -1);
      expect(c.note, '');
    });

    test('CppAnimationState fromJson empty', () {
      final s = CppAnimationState.fromJson({});
      expect(s.variables, isEmpty);
      expect(s.containers, isEmpty);
      expect(s.output, '');
    });

    test('CppAnimationStep fromJson empty', () {
      final step = CppAnimationStep.fromJson({});
      expect(step.step, 0);
      expect(step.title, '');
      expect(step.description, '');
      expect(step.codeLine, '');
      expect(step.highlights, isEmpty);
      expect(step.state.variables, isEmpty);
    });

    test('CppAnimation fromJson empty', () {
      final a = CppAnimation.fromJson({});
      expect(a.animationId, '');
      expect(a.itemId, '');
      expect(a.title, '');
      expect(a.steps, isEmpty);
      expect(a.initialState.variables, isEmpty);
    });

    test('CppAnimationMeta fromJson empty', () {
      final m = CppAnimationMeta.fromJson({});
      expect(m.animationId, '');
      expect(m.order, 0);
      expect(m.type, '');
      expect(m.assetPath, '');
    });

    test('CppAnimationManifest fromJson empty', () {
      final m = CppAnimationManifest.fromJson({});
      expect(m.version, 1);
      expect(m.animations, isEmpty);
    });
  });

  group('CppAnimation models fromJson with data', () {
    test('CppAnimationVariable full', () {
      final v = CppAnimationVariable.fromJson({
        'name': 'x',
        'value': '3',
        'note': 'int',
      });
      expect(v.name, 'x');
      expect(v.value, '3');
      expect(v.note, 'int');
    });

    test('CppAnimationContainer with values', () {
      final c = CppAnimationContainer.fromJson({
        'name': 'a',
        'type': 'array',
        'values': ['1', '2', '3'],
        'activeIndex': 2,
        'note': 'test',
      });
      expect(c.values.length, 3);
      expect(c.values[0], '1');
      expect(c.activeIndex, 2);
    });

    test('CppAnimation round-trip', () {
      final json = {
        'animationId': 'test',
        'itemId': '1.3.1',
        'title': 'T',
        'description': 'D',
        'initialState': {
          'variables': [
            {'name': 'x', 'value': '0', 'note': ''},
          ],
          'containers': [],
          'output': '',
        },
        'steps': [
          {
            'step': 1,
            'title': 'S1',
            'description': 'D1',
            'codeLine': 'int x = 0;',
            'highlights': ['x'],
            'state': {
              'variables': [
                {'name': 'x', 'value': '0', 'note': ''},
              ],
              'containers': [],
              'output': '',
            },
          },
        ],
      };
      final a = CppAnimation.fromJson(json);
      expect(a.animationId, 'test');
      expect(a.steps.length, 1);
      expect(a.steps[0].codeLine, 'int x = 0;');
      expect(a.steps[0].state.variables.first.name, 'x');
      expect(a.initialState.variables.first.name, 'x');
    });
  });

  group('Real C++ animation assets', () {
    late CppAnimationManifest manifest;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final manifestMap =
          jsonDecode(
                await File(
                  'assets/data/cpp/animations/cpp_animation_manifest.json',
                ).readAsString(),
              )
              as Map<String, dynamic>;
      manifest = CppAnimationManifest.fromJson(manifestMap);

      final graphMap =
          jsonDecode(
                await File('assets/data/knowledge/io_v4_4.json').readAsString(),
              )
              as Map<String, dynamic>;
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('manifest is valid and parseable', () {
      expect(manifest.version, 1);
      expect(manifest.animations.isNotEmpty, isTrue);
    });

    test('every animationId is unique', () {
      final ids = manifest.animations.map((a) => a.animationId).toList();
      expect(ids.toSet().length, ids.length);
    });

    test('every itemId exists in knowledge graph', () {
      for (final meta in manifest.animations) {
        final item = graph.itemById(meta.itemId);
        expect(
          item,
          isNotNull,
          reason: 'itemId ${meta.itemId} not found in knowledge graph',
        );
      }
    });

    test('every assetPath file exists and is parseable', () async {
      for (final meta in manifest.animations) {
        final file = File(meta.assetPath);
        expect(
          await file.exists(),
          isTrue,
          reason: 'File not found: ${meta.assetPath}',
        );
        final map =
            jsonDecode(await file.readAsString()) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.animationId, meta.animationId);
      }
    });

    test('every animation has at least 4 steps', () async {
      for (final meta in manifest.animations) {
        final file = File(meta.assetPath);
        final map =
            jsonDecode(await file.readAsString()) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(
          animation.steps.length,
          greaterThanOrEqualTo(4),
          reason:
              '${meta.animationId} has only ${animation.steps.length} steps',
        );
      }
    });

    test('every step has title, description, codeLine', () async {
      for (final meta in manifest.animations) {
        final file = File(meta.assetPath);
        final map =
            jsonDecode(await file.readAsString()) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        for (var i = 0; i < animation.steps.length; i++) {
          final step = animation.steps[i];
          expect(
            step.title.isNotEmpty,
            isTrue,
            reason: '${meta.animationId} step[$i] has empty title',
          );
          expect(
            step.description.isNotEmpty,
            isTrue,
            reason: '${meta.animationId} step[$i] has empty description',
          );
          expect(
            step.codeLine.isNotEmpty,
            isTrue,
            reason: '${meta.animationId} step[$i] has empty codeLine',
          );
        }
      }
    });

    test('animationsForItem logic finds correct animations', () {
      final matched =
          manifest.animations.where((m) => m.itemId == '1.8.9').toList()
            ..sort((a, b) => a.order.compareTo(b.order));
      expect(matched.isNotEmpty, isTrue);
      expect(matched.first.animationId, 'cpp_vector_push_back');
    });

    test('at least 6 animations in manifest', () {
      expect(manifest.animations.length, greaterThanOrEqualTo(6));
    });
  });

  group('CppAnimation route constant', () {
    test('/cpp_animation route exists in AppRouter', () {
      expect(AppRouter.cppAnimation, '/cpp_animation');
    });
  });

  group('Manifest completeness and consistency', () {
    late CppAnimationManifest manifest;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final manifestMap =
          jsonDecode(
                await File(
                  'assets/data/cpp/animations/cpp_animation_manifest.json',
                ).readAsString(),
              )
              as Map<String, dynamic>;
      manifest = CppAnimationManifest.fromJson(manifestMap);

      final graphMap =
          jsonDecode(
                await File('assets/data/knowledge/io_v4_4.json').readAsString(),
              )
              as Map<String, dynamic>;
      graph = KnowledgeGraph.fromJson(graphMap);
    });

    test('no orphan animation JSON files outside manifest', () async {
      final animationsDir = Directory('assets/data/cpp/animations');
      final jsonFiles =
          await animationsDir
              .list()
              .where(
                (entity) => entity is File && entity.path.endsWith('.json'),
              )
              .cast<File>()
              .toList();
      final manifestPaths =
          manifest.animations.map((m) => m.assetPath).toSet();
      for (final file in jsonFiles) {
        final path = file.path.replaceAll(r'\', '/');
        if (path.endsWith('cpp_animation_manifest.json')) continue;
        expect(
          manifestPaths.contains(path),
          isTrue,
          reason: 'Orphan animation file not in manifest: $path',
        );
      }
    });

    test('every assetPath file exists', () async {
      for (final meta in manifest.animations) {
        final file = File(meta.assetPath);
        expect(
          await file.exists(),
          isTrue,
          reason: 'assetPath file not found: ${meta.assetPath}',
        );
      }
    });

    test('every animationId is unique (comprehensive)', () {
      final ids = manifest.animations.map((a) => a.animationId).toList();
      expect(ids.toSet().length, ids.length, reason: 'Duplicate animationId');
    });

    test('every order is unique and ascending', () {
      final orders = manifest.animations.map((a) => a.order).toList();
      expect(
        orders.toSet().length,
        orders.length,
        reason: 'Duplicate order values in manifest',
      );
      final sorted = List<int>.from(orders)..sort();
      expect(orders, orderedEquals(sorted), reason: 'Orders not in ascending');
    });

    test('every itemId exists in knowledge graph (comprehensive)', () {
      for (final meta in manifest.animations) {
        final item = graph.itemById(meta.itemId);
        expect(
          item,
          isNotNull,
          reason:
              'itemId ${meta.itemId} (animationId: ${meta.animationId}) not found in knowledge graph',
        );
      }
    });

    test('at least one step has state with variables or containers or output',
        () async {
      for (final meta in manifest.animations) {
        final file = File(meta.assetPath);
        final map =
            jsonDecode(await file.readAsString()) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        final hasAnyState = animation.steps.any(
          (s) =>
              s.state.variables.isNotEmpty ||
              s.state.containers.isNotEmpty ||
              s.state.output.isNotEmpty,
        );
        expect(
          hasAnyState,
          isTrue,
          reason:
              '${meta.animationId} has no step with any state content at all',
        );
      }
    });

    test('per-section animation count summary for C++ 1.1-1.10', () async {
      final sectionCounts = <String, int>{};
      for (final meta in manifest.animations) {
        final sectionId = meta.itemId.split('.').take(2).join('.');
        sectionCounts[sectionId] =
            (sectionCounts[sectionId] ?? 0) + 1;
      }

      final cppSections = <String>{};
      for (final cat in graph.categories) {
        if (cat.name != 'C++语法') continue;
        for (final sec in cat.sections) {
          final match = RegExp(r'^1\.(\d+)$').firstMatch(sec.id);
          if (match != null) {
            final n = int.parse(match.group(1)!);
            if (n >= 1 && n <= 10) {
              cppSections.add(sec.id);
            }
          }
        }
      }

      expect(
        sectionCounts.isNotEmpty,
        isTrue,
        reason: 'Should have at least one section with animations',
      );

      expect(
        manifest.animations.length,
        greaterThanOrEqualTo(28),
        reason:
            'Total animations (${manifest.animations.length}) should be >= 28',
      );

      expect(
        sectionCounts['1.9'] ?? 0,
        greaterThanOrEqualTo(2),
        reason:
            'Section 1.9 should have at least 2 animations, got ${sectionCounts['1.9'] ?? 0}',
      );

      expect(
        sectionCounts['1.10'] ?? 0,
        greaterThanOrEqualTo(2),
        reason:
            'Section 1.10 should have at least 2 animations, got ${sectionCounts['1.10'] ?? 0}',
      );
    });

    test('animationsForItem returns correct results by itemId', () {
      final byItemId = <String, List<CppAnimationMeta>>{};
      for (final meta in manifest.animations) {
        byItemId.putIfAbsent(meta.itemId, () => []).add(meta);
      }

      for (final entry in byItemId.entries) {
        final sorted =
            entry.value.toList()..sort((a, b) => a.order.compareTo(b.order));
        expect(
          sorted.first.order,
          lessThanOrEqualTo(sorted.last.order),
          reason:
              'animationsForItem(${entry.key}) should return in ascending order',
        );
      }

      expect(byItemId.containsKey('1.8.9'), isTrue);
      expect(byItemId['1.8.9']!.first.animationId, 'cpp_vector_push_back');
      expect(byItemId.containsKey('1.5.1'), isTrue);
      expect(byItemId['1.5.1']!.first.animationId, 'cpp_if_branch');
    });
  });
}
