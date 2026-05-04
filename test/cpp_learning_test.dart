import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';

void main() {
  group('CppLearningUnit', () {
    test('fromJson with all fields', () {
      final json = {
        'itemId': '1.1.1',
        'title': '#include',
        'learningGoal': '理解 include',
        'explanation': '讲解内容',
        'exampleCode': '#include <iostream>',
        'codeNotes': ['第一行', '第二行'],
        'commonMistakes': [
          {'title': '忘写', 'description': '忘了', 'fix': '加上'},
        ],
        'practice': {'prompt': '写一个程序', 'hint': '提示', 'expectedIdea': '答案'},
        'quiz': [
          {
            'question': 'Q?',
            'options': ['A', 'B', 'C', 'D'],
            'answerIndex': 0,
            'explanation': '因为',
          },
        ],
      };

      final unit = CppLearningUnit.fromJson(json);
      expect(unit.itemId, '1.1.1');
      expect(unit.title, '#include');
      expect(unit.learningGoal, '理解 include');
      expect(unit.explanation, '讲解内容');
      expect(unit.exampleCode, '#include <iostream>');
      expect(unit.codeNotes.length, 2);
      expect(unit.commonMistakes.length, 1);
      expect(unit.commonMistakes.first.title, '忘写');
      expect(unit.practice.prompt, '写一个程序');
      expect(unit.quiz.length, 1);
      expect(unit.quiz.first.options.length, 4);
      expect(unit.quiz.first.answerIndex, 0);
    });

    test('fromJson missing fields gives defaults', () {
      final unit = CppLearningUnit.fromJson({});
      expect(unit.itemId, '');
      expect(unit.title, '');
      expect(unit.learningGoal, '');
      expect(unit.explanation, '');
      expect(unit.exampleCode, '');
      expect(unit.codeNotes, isEmpty);
      expect(unit.commonMistakes, isEmpty);
      expect(unit.practice.prompt, '');
      expect(unit.quiz, isEmpty);
    });

    test('CppCommonMistake fromJson missing fields', () {
      final m = CppCommonMistake.fromJson({});
      expect(m.title, '');
      expect(m.description, '');
      expect(m.fix, '');
    });

    test('CppPractice fromJson missing fields', () {
      final p = CppPractice.fromJson({});
      expect(p.prompt, '');
      expect(p.hint, '');
      expect(p.expectedIdea, '');
    });

    test('CppQuizQuestion fromJson missing fields', () {
      final q = CppQuizQuestion.fromJson({});
      expect(q.question, '');
      expect(q.options, isEmpty);
      expect(q.answerIndex, 0);
      expect(q.explanation, '');
    });
  });

  group('CppLearningContent', () {
    test('unitByItemId finds matching unit', () {
      final content = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.1.1', 'title': 'A'},
          {'itemId': '1.1.2', 'title': 'B'},
        ],
      });

      final found = content.unitByItemId('1.1.2');
      expect(found, isNotNull);
      expect(found!.title, 'B');
    });

    test('unitByItemId returns null for unknown id', () {
      final content = CppLearningContent.fromJson({
        'units': [
          {'itemId': '1.1.1', 'title': 'A'},
        ],
      });

      expect(content.unitByItemId('9.9.9'), isNull);
    });
  });

  group('Cpp learning data validation', () {
    KnowledgeGraph buildCppGraph() {
      return KnowledgeGraph.fromJson({
        'categories': [
          {
            'name': 'C++语法',
            'sections': [
              {
                'id': '1.1',
                'name': '程序基本结构',
                'level': 'L1',
                'items': [
                  {'id': '1.1.1', 'name': '#include', 'parent': '1.1'},
                  {
                    'id': '1.1.2',
                    'name': 'using namespace std',
                    'parent': '1.1',
                  },
                  {'id': '1.1.3', 'name': 'main 函数', 'parent': '1.1'},
                  {'id': '1.1.4', 'name': '语句与分号', 'parent': '1.1'},
                  {'id': '1.1.5', 'name': '代码块与大括号', 'parent': '1.1'},
                  {'id': '1.1.6', 'name': '注释', 'parent': '1.1'},
                  {'id': '1.1.7', 'name': 'return 0', 'parent': '1.1'},
                  {'id': '1.1.8', 'name': '头文件基础', 'parent': '1.1'},
                  {'id': '1.1.9', 'name': '编译与运行基础', 'parent': '1.1'},
                ],
              },
            ],
          },
        ],
      });
    }

    CppLearningContent buildSampleContent() {
      return CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {
            'itemId': '1.1.1',
            'title': '#include 指令',
            'quiz': [
              {
                'question': 'Q1',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 1,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.2',
            'title': 'using namespace std',
            'quiz': [
              {
                'question': 'Q2',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 0,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.3',
            'title': 'main 函数',
            'quiz': [
              {
                'question': 'Q3',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 2,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.4',
            'title': '语句与分号',
            'quiz': [
              {
                'question': 'Q4',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 1,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.5',
            'title': '代码块与大括号',
            'quiz': [
              {
                'question': 'Q5',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 1,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.6',
            'title': '注释',
            'quiz': [
              {
                'question': 'Q6',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 1,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.7',
            'title': 'return 0',
            'quiz': [
              {
                'question': 'Q7',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 2,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.8',
            'title': '头文件基础',
            'quiz': [
              {
                'question': 'Q8',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 2,
                'explanation': 'E',
              },
            ],
          },
          {
            'itemId': '1.1.9',
            'title': '编译与运行基础',
            'quiz': [
              {
                'question': 'Q9',
                'options': ['A', 'B', 'C', 'D'],
                'answerIndex': 2,
                'explanation': 'E',
              },
            ],
          },
        ],
      });
    }

    test('all unit itemIds exist in knowledge graph', () {
      final graph = buildCppGraph();
      final content = buildSampleContent();

      for (final unit in content.units) {
        final found = graph.itemById(unit.itemId);
        expect(
          found,
          isNotNull,
          reason: 'itemId ${unit.itemId} not found in knowledge graph',
        );
      }
    });

    test('all quiz options have 4 choices', () {
      final content = buildSampleContent();
      for (final unit in content.units) {
        for (final q in unit.quiz) {
          expect(
            q.options.length,
            4,
            reason:
                'Quiz in unit ${unit.itemId} has ${q.options.length} options',
          );
        }
      }
    });

    test('all quiz answerIndex in 0~3 range', () {
      final content = buildSampleContent();
      for (final unit in content.units) {
        for (final q in unit.quiz) {
          expect(
            q.answerIndex,
            greaterThanOrEqualTo(0),
            reason: 'unit ${unit.itemId} answerIndex < 0',
          );
          expect(
            q.answerIndex,
            lessThan(4),
            reason: 'unit ${unit.itemId} answerIndex >= 4 (only 4 options)',
          );
        }
      }
    });

    test('at least one unit can be found by itemId', () {
      final content = buildSampleContent();
      expect(content.unitByItemId('1.1.1'), isNotNull);
      expect(content.unitByItemId('1.1.3'), isNotNull);
    });
  });

  group('CppLearningManifest', () {
    test('fromJson with all fields', () {
      final json = {
        'version': 2,
        'category': 'C++语法',
        'baseFile': 'assets/data/cpp/cpp_learning_units.json',
        'sectionFiles': [
          'assets/data/cpp/section_1_2_units.json',
          'assets/data/cpp/section_1_3_units.json',
        ],
      };

      final manifest = CppLearningManifest.fromJson(json);
      expect(manifest.version, 2);
      expect(manifest.category, 'C++语法');
      expect(manifest.baseFile, 'assets/data/cpp/cpp_learning_units.json');
      expect(manifest.sectionFiles.length, 2);
      expect(
        manifest.sectionFiles[0],
        'assets/data/cpp/section_1_2_units.json',
      );
      expect(
        manifest.sectionFiles[1],
        'assets/data/cpp/section_1_3_units.json',
      );
    });

    test('fromJson missing fields gives defaults', () {
      final manifest = CppLearningManifest.fromJson({});
      expect(manifest.version, 1);
      expect(manifest.category, '');
      expect(manifest.baseFile, '');
      expect(manifest.sectionFiles, isEmpty);
    });
  });

  void addUnitsWithDuplicateCheck(
    List<CppLearningUnit> targetUnits,
    List<CppLearningUnit> sourceUnits,
    Set<String> seenItemIds,
  ) {
    for (final unit in sourceUnits) {
      if (seenItemIds.contains(unit.itemId)) {
        throw StateError('Duplicate C++ learning unit itemId: ${unit.itemId}');
      }
      seenItemIds.add(unit.itemId);
      targetUnits.add(unit);
    }
  }

  group('Repository merge logic with mock data', () {
    test('merge base and section files without duplicates', () {
      final baseContent = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.1.1', 'title': 'Base 1.1.1'},
          {'itemId': '1.1.2', 'title': 'Base 1.1.2'},
        ],
      });

      final sectionContent1 = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.2.1', 'title': 'Section 1.2.1'},
          {'itemId': '1.2.2', 'title': 'Section 1.2.2'},
        ],
      });

      final sectionContent2 = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.3.1', 'title': 'Section 1.3.1'},
        ],
      });

      final allUnits = <CppLearningUnit>[];
      final seenItemIds = <String>{};

      addUnitsWithDuplicateCheck(allUnits, baseContent.units, seenItemIds);
      addUnitsWithDuplicateCheck(allUnits, sectionContent1.units, seenItemIds);
      addUnitsWithDuplicateCheck(allUnits, sectionContent2.units, seenItemIds);

      expect(allUnits.length, 5);
      expect(allUnits[0].itemId, '1.1.1');
      expect(allUnits[1].itemId, '1.1.2');
      expect(allUnits[2].itemId, '1.2.1');
      expect(allUnits[3].itemId, '1.2.2');
      expect(allUnits[4].itemId, '1.3.1');
    });

    test('merge throws on duplicate itemId', () {
      final content1 = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.1.1', 'title': 'First'},
        ],
      });

      final content2 = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {'itemId': '1.1.1', 'title': 'Duplicate'},
        ],
      });

      final allUnits = <CppLearningUnit>[];
      final seenItemIds = <String>{};

      addUnitsWithDuplicateCheck(allUnits, content1.units, seenItemIds);

      expect(
        () => addUnitsWithDuplicateCheck(allUnits, content2.units, seenItemIds),
        throwsA(isA<StateError>()),
      );
    });
  });

  group('Code validation tests', () {
    test('each exampleCode has only one main function', () {
      final content = CppLearningContent.fromJson({
        'version': 1,
        'category': 'C++语法',
        'units': [
          {
            'itemId': '1.1.1',
            'title': 'Test',
            'exampleCode':
                '#include <iostream>\nint main() {\n    return 0;\n}',
          },
          {
            'itemId': '1.1.2',
            'title': 'Test2',
            'exampleCode':
                '#include <iostream>\nint main() {\n    return 0;\n}',
          },
          {
            'itemId': '1.1.3',
            'title': 'NoMain',
            'exampleCode': '#include <iostream>\nvoid foo() {}',
          },
        ],
      });

      for (final unit in content.units) {
        final mainCount = 'int main'.allMatches(unit.exampleCode).length;
        expect(
          mainCount <= 1,
          isTrue,
          reason:
              'Unit ${unit.itemId} has $mainCount main functions (max 1 allowed)',
        );
      }
    });
  });

  group('Real C++ learning assets', () {
    late CppLearningManifest manifest;
    late List<CppLearningUnit> allUnits;
    late Set<String> allItemIds;
    late KnowledgeGraph graph;
    late Set<String> cppSyntaxItemIds;

    Future<Map<String, dynamic>> readJson(String assetPath) async {
      final file = File(assetPath);
      if (!await file.exists()) {
        throw StateError('Asset file not found: $assetPath');
      }
      final raw = await file.readAsString(encoding: utf8);
      return jsonDecode(raw) as Map<String, dynamic>;
    }

    List<CppLearningUnit> loadUnitsFromMap(Map<String, dynamic> map) {
      final content = CppLearningContent.fromJson(map);
      return content.units;
    }

    bool isCppSyntaxSection(String sectionId) {
      final match = RegExp(r'^1\.(\d+)$').firstMatch(sectionId);
      if (match == null) return false;
      final n = int.parse(match.group(1)!);
      return n >= 1 && n <= 10;
    }

    setUpAll(() async {
      final manifestMap = await readJson(
        'assets/data/cpp/cpp_learning_manifest.json',
      );
      manifest = CppLearningManifest.fromJson(manifestMap);

      allUnits = [];
      allItemIds = {};

      final baseUnits = loadUnitsFromMap(await readJson(manifest.baseFile));
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
        final sectionUnits = loadUnitsFromMap(await readJson(sf));
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

      cppSyntaxItemIds = {};
      for (final cat in graph.categories) {
        if (cat.name != 'C++语法') continue;
        for (final sec in cat.sections) {
          if (!isCppSyntaxSection(sec.id)) continue;
          for (final item in sec.items) {
            cppSyntaxItemIds.add(item.id);
          }
        }
      }
    });

    test('manifest is valid and readable', () {
      expect(manifest.version, 1);
      expect(manifest.category, 'C++语法');
      expect(manifest.baseFile, isNotEmpty);
      expect(manifest.sectionFiles, isNotEmpty);
    });

    test('all section files are valid JSON and parseable', () {
      expect(allUnits.isNotEmpty, isTrue, reason: 'No units loaded at all');
    });

    test(
      'units total count matches C++ syntax 1.1~1.10 items in knowledge graph',
      () {
        final expectedCount = cppSyntaxItemIds.length;
        expect(
          allUnits.length,
          expectedCount,
          reason:
              'Expected $expectedCount units (from knowledge graph C++语法 1.1~1.10), '
              'but got ${allUnits.length}',
        );
      },
    );

    test('no duplicate itemId across all files', () {
      expect(
        allItemIds.length,
        allUnits.length,
        reason:
            '${allUnits.length} units loaded but only ${allItemIds.length} unique itemIds '
            '— duplicates exist',
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
            'These itemIds are not found in knowledge graph: ${missing.join(', ')}',
      );
    });

    test('every C++ syntax 1.1~1.10 knowledge item has a corresponding unit', () {
      final missing = <String>[];
      for (final id in cppSyntaxItemIds) {
        if (!allItemIds.contains(id)) {
          missing.add(id);
        }
      }
      expect(
        missing,
        isEmpty,
        reason:
            'These knowledge graph items (C++语法 1.1~1.10) have no learning unit: '
            '${missing.join(', ')}',
      );
    });

    test('every unit has non-empty required fields', () {
      final errors = <String>[];
      for (final u in allUnits) {
        if (u.itemId.isEmpty) {
          errors.add('[${u.title}] itemId is empty');
        }
        if (u.title.isEmpty) {
          errors.add('[${u.itemId}] title is empty');
        }
        if (u.learningGoal.isEmpty) {
          errors.add('[${u.itemId}] learningGoal is empty');
        }
        if (u.explanation.isEmpty) {
          errors.add('[${u.itemId}] explanation is empty');
        }
        if (u.exampleCode.isEmpty) {
          errors.add('[${u.itemId}] exampleCode is empty');
        }
        if (u.practice.prompt.isEmpty) {
          errors.add('[${u.itemId}] practice.prompt is empty');
        }
        if (u.practice.expectedIdea.isEmpty) {
          errors.add('[${u.itemId}] practice.expectedIdea is empty');
        }
      }
      expect(
        errors,
        isEmpty,
        reason:
            'Required field violations found (${errors.length}):\n'
            '${errors.take(20).join('\n')}'
            '${errors.length > 20 ? '\n... and ${errors.length - 20} more' : ''}',
      );
    });

    test('every unit has at least 1 quiz', () {
      final noQuiz = <String>[];
      for (final u in allUnits) {
        if (u.quiz.isEmpty) {
          noQuiz.add(u.itemId);
        }
      }
      expect(
        noQuiz,
        isEmpty,
        reason: 'These units have no quiz: ${noQuiz.join(', ')}',
      );
    });

    test('every quiz has exactly 4 options', () {
      final errors = <String>[];
      for (final u in allUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          if (q.options.length != 4) {
            errors.add(
              '${u.itemId} quiz[$i] has ${q.options.length} options (expected 4)',
            );
          }
        }
      }
      expect(
        errors,
        isEmpty,
        reason:
            'Quiz option count violations (${errors.length}):\n'
            '${errors.take(20).join('\n')}'
            '${errors.length > 20 ? '\n... and ${errors.length - 20} more' : ''}',
      );
    });

    test('every quiz answerIndex is in range 0~3', () {
      final errors = <String>[];
      for (final u in allUnits) {
        for (var i = 0; i < u.quiz.length; i++) {
          final q = u.quiz[i];
          if (q.answerIndex < 0 || q.answerIndex > 3) {
            errors.add(
              '${u.itemId} quiz[$i] answerIndex=${q.answerIndex} (must be 0~3)',
            );
          }
        }
      }
      expect(
        errors,
        isEmpty,
        reason:
            'Quiz answerIndex violations (${errors.length}):\n'
            '${errors.take(20).join('\n')}'
            '${errors.length > 20 ? '\n... and ${errors.length - 20} more' : ''}',
      );
    });

    test('each exampleCode has at most 1 main function', () {
      final errors = <String>[];
      final mainPattern = RegExp(r'int\s+main\s*\(');
      for (final u in allUnits) {
        final count = mainPattern.allMatches(u.exampleCode).length;
        if (count > 1) {
          errors.add(
            '${u.itemId} has $count main functions in exampleCode (max 1)',
          );
        }
      }
      expect(
        errors,
        isEmpty,
        reason:
            'Multiple main() violations (${errors.length}):\n'
            '${errors.join('\n')}',
      );
    });
  });
}
