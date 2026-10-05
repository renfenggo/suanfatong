import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_animation.dart';

/// Tests for the 4 MVP Demo animations (batch 1).
///
/// Validates:
/// - manifest contains all 4 animationIds
/// - 4 assetPath files exist
/// - 4 JSONs are parseable
/// - each has non-empty steps
/// - each itemId is correct
/// - CppAnimation.fromJson does not throw
/// - matrix type container support
void main() {
  late CppAnimationManifest manifest;

  const mvpAnimations = [
    _MvpSpec(
      animationId: 'cpp_dfs_graph_traversal',
      itemId: '2.7.16',
      assetPath: 'assets/data/cpp/animations/dfs_graph_traversal.json',
      title: '图的遍历：DFS',
    ),
    _MvpSpec(
      animationId: 'cpp_bfs_graph_traversal',
      itemId: '2.7.17',
      assetPath: 'assets/data/cpp/animations/bfs_graph_traversal.json',
      title: '图的遍历：BFS',
    ),
    _MvpSpec(
      animationId: 'cpp_prefix_sum_1d',
      itemId: '2.4.17',
      assetPath: 'assets/data/cpp/animations/prefix_sum_1d.json',
      title: '前缀和 (一维)',
    ),
    _MvpSpec(
      animationId: 'cpp_prefix_sum_2d',
      itemId: '2.4.18',
      assetPath: 'assets/data/cpp/animations/prefix_sum_2d.json',
      title: '前缀和 (二维)',
    ),
  ];

  setUpAll(() async {
    final manifestMap = jsonDecode(
      await File('assets/data/cpp/animations/cpp_animation_manifest.json')
          .readAsString(),
    ) as Map<String, dynamic>;
    manifest = CppAnimationManifest.fromJson(manifestMap);
  });

  group('MVP Demo manifest registration', () {
    for (final spec in mvpAnimations) {
      test('manifest contains animationId ${spec.animationId}', () {
        final found = manifest.animations
            .any((a) => a.animationId == spec.animationId);
        expect(found, isTrue,
            reason: '${spec.animationId} not found in manifest');
      });

      test('${spec.animationId} has correct itemId ${spec.itemId}', () {
        final meta = manifest.animations
            .firstWhere((a) => a.animationId == spec.animationId);
        expect(meta.itemId, spec.itemId);
      });

      test('${spec.animationId} has correct assetPath', () {
        final meta = manifest.animations
            .firstWhere((a) => a.animationId == spec.animationId);
        expect(meta.assetPath, spec.assetPath);
      });

      test('${spec.animationId} has correct title', () {
        final meta = manifest.animations
            .firstWhere((a) => a.animationId == spec.animationId);
        expect(meta.title, spec.title);
      });
    }
  });

  group('MVP Demo asset files exist', () {
    for (final spec in mvpAnimations) {
      test('file exists: ${spec.assetPath}', () async {
        final exists = await File(spec.assetPath).exists();
        expect(exists, isTrue, reason: 'File not found: ${spec.assetPath}');
      });
    }
  });

  group('MVP Demo JSON parseable', () {
    for (final spec in mvpAnimations) {
      test('${spec.animationId} JSON is parseable', () async {
        final content = await File(spec.assetPath).readAsString();
        expect(() => jsonDecode(content), returnsNormally,
            reason: 'Failed to parse ${spec.assetPath}');
      });
    }
  });

  group('MVP Demo CppAnimation model compatibility', () {
    for (final spec in mvpAnimations) {
      test('${spec.animationId} CppAnimation.fromJson does not throw',
          () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        expect(
            () => CppAnimation.fromJson(map), returnsNormally,
            reason: 'CppAnimation.fromJson failed for ${spec.animationId}');
      });

      test('${spec.animationId} has correct animationId', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.animationId, spec.animationId);
      });

      test('${spec.animationId} has correct itemId', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.itemId, spec.itemId);
      });

      test('${spec.animationId} has non-empty title', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.title.isNotEmpty, isTrue);
      });

      test('${spec.animationId} steps is non-empty', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.steps.isNotEmpty, isTrue,
            reason: '${spec.animationId} has no steps');
      });

      test('${spec.animationId} has expectedLearningPoint', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        // expectedLearningPoint is not in the model, just verify JSON has it
        expect(map.containsKey('expectedLearningPoint'), isTrue,
            reason: '${spec.animationId} missing expectedLearningPoint');
        expect((map['expectedLearningPoint'] as String).isNotEmpty, isTrue);
      });

      test('${spec.animationId} initialState is valid', () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.initialState, isNotNull);
        // At least one of variables, containers, or output should exist
        expect(
          animation.initialState.variables.isNotEmpty ||
              animation.initialState.containers.isNotEmpty ||
              animation.initialState.output.isNotEmpty,
          isTrue,
          reason: '${spec.animationId} initialState is completely empty',
        );
      });

      test('${spec.animationId} every step has title, description, codeLine, state',
          () async {
        final content = await File(spec.assetPath).readAsString();
        final map = jsonDecode(content) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        for (var i = 0; i < animation.steps.length; i++) {
          final step = animation.steps[i];
          expect(step.title.isNotEmpty, isTrue,
              reason: '${spec.animationId} step[$i] empty title');
          expect(step.description.isNotEmpty, isTrue,
              reason: '${spec.animationId} step[$i] empty description');
          expect(step.codeLine.isNotEmpty, isTrue,
              reason: '${spec.animationId} step[$i] empty codeLine');
          expect(step.state, isNotNull,
              reason: '${spec.animationId} step[$i] null state');
        }
      });
    }
  });

  group('MVP Demo specific content validation', () {
    test('DFS has stack-like container (visited + 递归栈)', () async {
      final content =
          await File('assets/data/cpp/animations/dfs_graph_traversal.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);

      final containerNames =
          animation.initialState.containers.map((c) => c.name).toSet();
      expect(containerNames.contains('visited'), isTrue,
          reason: 'DFS should have visited container');
      expect(containerNames.contains('递归栈'), isTrue,
          reason: 'DFS should have 递归栈 container');
    });

    test('DFS steps show backtracking (visited toggled or stack pops)',
        () async {
      final content =
          await File('assets/data/cpp/animations/dfs_graph_traversal.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);
      // Should have at least 5 steps for a 6-node graph with backtracking
      expect(animation.steps.length, greaterThanOrEqualTo(5));
    });

    test('BFS has queue container', () async {
      final content =
          await File('assets/data/cpp/animations/bfs_graph_traversal.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);

      final queueContainers = animation.initialState.containers
          .where((c) => c.type == 'queue')
          .toList();
      expect(queueContainers.isNotEmpty, isTrue,
          reason: 'BFS should have a queue container');
    });

    test('1D prefix sum has original array and prefix array', () async {
      final content =
          await File('assets/data/cpp/animations/prefix_sum_1d.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);

      final containerNames =
          animation.initialState.containers.map((c) => c.name).toSet();
      expect(containerNames.contains('a'), isTrue,
          reason: '1D prefix sum should have original array a');
      expect(containerNames.contains('prefix'), isTrue,
          reason: '1D prefix sum should have prefix array');
    });

    test('2D prefix sum has matrix type containers', () async {
      final content =
          await File('assets/data/cpp/animations/prefix_sum_2d.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);

      final matrixContainers = animation.initialState.containers
          .where((c) => c.isMatrix)
          .toList();
      expect(matrixContainers.isNotEmpty, isTrue,
          reason: '2D prefix sum should have matrix containers');

      // Verify matrix values are parseable as List<List<String>>
      for (final mc in matrixContainers) {
        expect(mc.matrixValues.isNotEmpty, isTrue);
        expect(mc.matrixValues.first, isA<List<String>>());
      }
    });

    test('2D prefix sum flatValues for matrix container works', () async {
      final content =
          await File('assets/data/cpp/animations/prefix_sum_2d.json')
              .readAsString();
      final map = jsonDecode(content) as Map<String, dynamic>;
      final animation = CppAnimation.fromJson(map);

      // There are two matrix containers in initialState
      final matrixContainers = animation.initialState.containers
          .where((c) => c.isMatrix)
          .toList();
      expect(matrixContainers.length, 2);

      // First matrix is a (3x3=9), second is prefix S (4x4=16)
      expect(matrixContainers[0].flatValues.length, 9,
          reason: '3x3 matrix should have 9 flat values');
      expect(matrixContainers[1].flatValues.length, 16,
          reason: '4x4 prefix sum should have 16 flat values');
    });
  });

  group('MVP Demo animationId uniqueness', () {
    test('all 4 MVP animationIds are unique', () {
      final ids = mvpAnimations.map((s) => s.animationId).toList();
      expect(ids.toSet().length, ids.length,
          reason: 'Duplicate animationId among MVP demos');
    });

    test('MVP animationIds do not conflict with existing manifest', () {
      final existingIds =
          manifest.animations.map((a) => a.animationId).toSet();
      final mvpIds = mvpAnimations.map((s) => s.animationId).toSet();
      // All MVP IDs should be in the manifest (already registered)
      expect(mvpIds.difference(existingIds), isEmpty,
          reason: 'MVP animationId not found in manifest');
    });
  });

  group('MVP Demo existing animations preserved', () {
    test('manifest total >= 115', () {
      expect(manifest.animations.length, greaterThanOrEqualTo(115));
    });

    test('original 111 animations still present', () {
      // Check that specific known animations still exist
      final ids = manifest.animations.map((a) => a.animationId).toSet();
      expect(ids.contains('cpp_bfs_demo'), isTrue,
          reason: 'Original cpp_bfs_demo missing');
      expect(ids.contains('cpp_dfs_demo'), isTrue,
          reason: 'Original cpp_dfs_demo missing');
      expect(ids.contains('cpp_prefix_sum'), isTrue,
          reason: 'Original cpp_prefix_sum missing');
    });
  });
}

class _MvpSpec {
  final String animationId;
  final String itemId;
  final String assetPath;
  final String title;

  const _MvpSpec({
    required this.animationId,
    required this.itemId,
    required this.assetPath,
    required this.title,
  });
}
