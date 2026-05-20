import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/cpp_animation.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';

const _dfsItemIds = <String>{
  '2.7.1',
  '2.7.2',
  '2.7.3',
  '2.7.4',
  '2.7.5',
  '2.7.6',
  '2.7.7',
  '2.7.8',
};

const _dfsKeywords = ['DFS', '深度优先', '回溯', '剪枝', '记忆化搜索', '递归', '网格'];

void main() {
  group('DFS 学习单元 JSON 解析与验证', () {
    late List<CppLearningUnit> dfsUnits;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final raw = await File(
        'assets/data/algorithm/section_2_7_units.json',
      ).readAsString(encoding: utf8);
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final content = CppLearningContent.fromJson(map);
      dfsUnits = content.units;

      final graphRaw = await File(
        'assets/data/knowledge/io_v4_4.json',
      ).readAsString(encoding: utf8);
      graph = KnowledgeGraph.fromJson(
        jsonDecode(graphRaw) as Map<String, dynamic>,
      );
    });

    test('section 2.7 包含 8 个学习单元', () {
      expect(dfsUnits.length, 8);
    });

    test('所有 DFS itemId 正确', () {
      final ids = dfsUnits.map((u) => u.itemId).toSet();
      for (final id in _dfsItemIds) {
        expect(ids.contains(id), isTrue, reason: 'Missing itemId: $id');
      }
    });

    test('每个 DFS 学习单元都有标题和学习目标', () {
      for (final u in dfsUnits) {
        expect(u.itemId, isNotEmpty);
        expect(u.title, isNotEmpty, reason: '${u.itemId} title is empty');
        expect(
          u.learningGoal,
          isNotEmpty,
          reason: '${u.itemId} learningGoal is empty',
        );
        expect(
          u.explanation,
          isNotEmpty,
          reason: '${u.itemId} explanation is empty',
        );
      }
    });

    test('每个 DFS 学习单元都有 exampleCode', () {
      for (final u in dfsUnits) {
        expect(
          u.exampleCode,
          isNotEmpty,
          reason: '${u.itemId} has no exampleCode',
        );
      }
    });

    test('exampleCode 不包含多个 main 函数', () {
      for (final u in dfsUnits) {
        final mainCount = 'int main('.allMatches(u.exampleCode).length;
        expect(
          mainCount,
          equals(1),
          reason:
              '${u.itemId} has $mainCount main() functions (expected 1)',
        );
      }
    });

    test('每个 DFS 学习单元至少有 2 个 quiz', () {
      for (final u in dfsUnits) {
        expect(
          u.quiz.length,
          greaterThanOrEqualTo(2),
          reason: '${u.itemId} has only ${u.quiz.length} quiz (expected >= 2)',
        );
      }
    });

    test('每个 quiz 有 4 个选项', () {
      for (final u in dfsUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          expect(
            q.options.length,
            equals(4),
            reason:
                '${u.itemId} quiz[$i] has ${q.options.length} options (expected 4)',
          );
        }
      }
    });

    test('每个 quiz 的 answerIndex 合法', () {
      for (final u in dfsUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          expect(
            q.answerIndex,
            greaterThanOrEqualTo(0),
            reason: '${u.itemId} quiz[$i] answerIndex < 0',
          );
          expect(
            q.answerIndex,
            lessThan(q.options.length),
            reason:
                '${u.itemId} quiz[$i] answerIndex=${q.answerIndex} >= ${q.options.length}',
          );
        }
      }
    });

    test('每个 DFS 学习单元有 commonMistakes', () {
      for (final u in dfsUnits) {
        expect(
          u.commonMistakes.isNotEmpty,
          isTrue,
          reason: '${u.itemId} has no commonMistakes',
        );
      }
    });

    test('每个 DFS 学习单元有 practice', () {
      for (final u in dfsUnits) {
        expect(
          u.practice.prompt,
          isNotEmpty,
          reason: '${u.itemId} has no practice prompt',
        );
      }
    });

    test('每个 DFS itemId 存在于知识图谱中', () {
      for (final id in _dfsItemIds) {
        final item = graph.itemById(id);
        expect(
          item,
          isNotNull,
          reason: 'itemId $id not found in knowledge graph',
        );
      }
    });

    test('知识图谱中 DFS 节点都有学习内容', () {
      final unitIds = dfsUnits.map((u) => u.itemId).toSet();
      for (final id in _dfsItemIds) {
        expect(
          unitIds.contains(id),
          isTrue,
          reason: 'Knowledge graph has $id but no learning unit for it',
        );
      }
    });

    test('DFS 依赖关系正确', () {
      final dfsBasic = graph.itemById('2.7.2');
      expect(dfsBasic, isNotNull);
      expect(
        dfsBasic!.directPre,
        contains('2.7.1'),
        reason: 'DFS基础 should depend on 递归基础',
      );

      final gridDfs = graph.itemById('2.7.3');
      expect(gridDfs, isNotNull);
      expect(
        gridDfs!.directPre,
        contains('2.7.2'),
        reason: '网格DFS should depend on DFS基础',
      );

      final treeDfs = graph.itemById('2.7.4');
      expect(treeDfs, isNotNull);
      expect(
        treeDfs!.directPre,
        contains('2.7.2'),
        reason: '树与图DFS should depend on DFS基础',
      );

      final backtrack = graph.itemById('2.7.6');
      expect(backtrack, isNotNull);
      expect(
        backtrack!.directPre,
        contains('2.7.2'),
        reason: '回溯枚举 should depend on DFS基础',
      );

      final pruning = graph.itemById('2.7.7');
      expect(pruning, isNotNull);
      expect(
        pruning!.directPre,
        contains('2.7.6'),
        reason: '剪枝优化 should depend on 回溯枚举',
      );

      final memo = graph.itemById('2.7.8');
      expect(memo, isNotNull);
      expect(
        memo!.directPre,
        contains('2.7.2'),
        reason: '记忆化搜索 should depend on DFS基础',
      );
    });
  });

  group('DFS 动画验证', () {
    late CppAnimationManifest manifest;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final manifestRaw = await File(
        'assets/data/cpp/animations/cpp_animation_manifest.json',
      ).readAsString();
      manifest = CppAnimationManifest.fromJson(
        jsonDecode(manifestRaw) as Map<String, dynamic>,
      );

      final graphRaw = await File(
        'assets/data/knowledge/io_v4_4.json',
      ).readAsString();
      graph = KnowledgeGraph.fromJson(
        jsonDecode(graphRaw) as Map<String, dynamic>,
      );
    });

    test('DFS 相关动画的 assetPath 都存在', () async {
      final dfsAnimations = manifest.animations
          .where((m) => _dfsItemIds.contains(m.itemId))
          .toList();
      expect(dfsAnimations.isNotEmpty, isTrue);

      for (final meta in dfsAnimations) {
        final file = File(meta.assetPath);
        expect(
          await file.exists(),
          isTrue,
          reason: 'DFS animation file not found: ${meta.assetPath}',
        );
      }
    });

    test('DFS 相关动画的 itemId 都存在于知识图谱', () {
      final dfsAnimations = manifest.animations
          .where((m) => _dfsItemIds.contains(m.itemId))
          .toList();
      for (final meta in dfsAnimations) {
        final item = graph.itemById(meta.itemId);
        expect(
          item,
          isNotNull,
          reason:
              'Animation ${meta.animationId} has itemId ${meta.itemId} not in KG',
        );
      }
    });

    test('DFS 相关动画可正确解析', () async {
      final dfsAnimations = manifest.animations
          .where((m) => _dfsItemIds.contains(m.itemId))
          .toList();
      for (final meta in dfsAnimations) {
        final raw = await File(meta.assetPath).readAsString();
        final map = jsonDecode(raw) as Map<String, dynamic>;
        final animation = CppAnimation.fromJson(map);
        expect(animation.animationId, meta.animationId);
        expect(animation.steps.length, greaterThanOrEqualTo(4));
      }
    });

    test('新增的 DFS 动画已注册在 manifest 中', () {
      final animationIds = manifest.animations.map((a) => a.animationId).toSet();
      expect(
        animationIds.contains('cpp_dfs_grid_island'),
        isTrue,
        reason: 'cpp_dfs_grid_island not in manifest',
      );
      expect(
        animationIds.contains('cpp_backtrack_permutation'),
        isTrue,
        reason: 'cpp_backtrack_permutation not in manifest',
      );
      expect(
        animationIds.contains('cpp_memoization_fib'),
        isTrue,
        reason: 'cpp_memoization_fib not in manifest',
      );
    });

    test('无孤儿动画文件', () async {
      final animationsDir = Directory('assets/data/cpp/animations');
      final jsonFiles =
          await animationsDir
              .list()
              .where(
                (entity) => entity is File && entity.path.endsWith('.json'),
              )
              .cast<File>()
              .toList();
      final manifestPaths = manifest.animations.map((m) => m.assetPath).toSet();
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
  });

  group('DFS 搜索关键词测试', () {
    late List<CppLearningUnit> dfsUnits;
    late KnowledgeGraph graph;

    setUpAll(() async {
      final raw = await File(
        'assets/data/algorithm/section_2_7_units.json',
      ).readAsString(encoding: utf8);
      final map = jsonDecode(raw) as Map<String, dynamic>;
      dfsUnits = CppLearningContent.fromJson(map).units;

      final graphRaw = await File(
        'assets/data/knowledge/io_v4_4.json',
      ).readAsString(encoding: utf8);
      graph = KnowledgeGraph.fromJson(
        jsonDecode(graphRaw) as Map<String, dynamic>,
      );
    });

    test('搜索 "DFS" 能找到对应内容', () {
      final matched = dfsUnits.where(
        (u) =>
            u.title.contains('DFS') ||
            u.explanation.contains('DFS') ||
            u.learningGoal.contains('DFS'),
      );
      expect(matched.isNotEmpty, isTrue);
    });

    test('搜索 "深度优先" 能找到对应内容', () {
      final matched = dfsUnits.where(
        (u) =>
            u.title.contains('深度优先') ||
            u.explanation.contains('深度优先'),
      );
      expect(matched.isNotEmpty, isTrue);
    });

    test('搜索 "回溯" 能找到对应内容', () {
      final matched = dfsUnits.where(
        (u) =>
            u.title.contains('回溯') ||
            u.explanation.contains('回溯'),
      );
      expect(matched.isNotEmpty, isTrue);
    });

    test('搜索 "剪枝" 能找到对应内容', () {
      final matched = dfsUnits.where(
        (u) =>
            u.title.contains('剪枝') ||
            u.explanation.contains('剪枝'),
      );
      expect(matched.isNotEmpty, isTrue);
    });

    test('搜索 "记忆化搜索" 能找到对应内容', () {
      final matched = dfsUnits.where(
        (u) =>
            u.title.contains('记忆化') ||
            u.explanation.contains('记忆化'),
      );
      expect(matched.isNotEmpty, isTrue);
    });

    test('知识图谱中 DFS 关键词能找到对应节点', () {
      for (final keyword in _dfsKeywords) {
        final found = <String>[];
        for (final cat in graph.categories) {
          for (final sec in cat.sections) {
            for (final item in sec.items) {
              if (item.name.contains(keyword) ||
                  item.alias.any((a) => a.contains(keyword))) {
                found.add(item.id);
              }
            }
          }
        }
        expect(
          found.isNotEmpty,
          isTrue,
          reason: 'Keyword "$keyword" not found in knowledge graph',
        );
      }
    });
  });

  group('DFS 学习单元中文编码测试', () {
    test('所有 DFS 学习单元无乱码', () async {
      final raw = await File(
        'assets/data/algorithm/section_2_7_units.json',
      ).readAsString(encoding: utf8);

      expect(raw.contains(RegExp(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')), isFalse);

      final map = jsonDecode(raw) as Map<String, dynamic>;
      expect(map, isNotNull);
      expect(map['sectionName'], '搜索与回溯');
    });
  });
}
