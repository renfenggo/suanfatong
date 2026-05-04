import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/lesson.dart';
import 'package:bfs_learn/models/quiz.dart';
import 'package:bfs_learn/models/mistake.dart';
import 'package:bfs_learn/models/bfs_step.dart';
import 'package:bfs_learn/models/progress.dart';
import 'package:bfs_learn/models/answer_record.dart';
import 'package:bfs_learn/models/content_manifest.dart';
import 'package:bfs_learn/models/learning_topic.dart';
import 'package:bfs_learn/models/lesson_set.dart';
import 'package:bfs_learn/models/quiz_set.dart';
import 'package:bfs_learn/models/mistake_set.dart';
import 'package:bfs_learn/models/animation_scenario.dart';
import 'package:bfs_learn/models/content_module.dart';
import 'package:bfs_learn/models/cpp_quiz_entry.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'dart:convert';

void main() {
  group('Lesson model', () {
    test('fromJson with all fields', () {
      final json = {
        'id': 'test1',
        'title': '测试标题',
        'subtitle': '测试副标题',
        'content': '测试内容',
        'example': '示例',
        'code': 'code',
        'tip': '提示',
        'order': 3,
      };
      final lesson = Lesson.fromJson(json);
      expect(lesson.id, 'test1');
      expect(lesson.title, '测试标题');
      expect(lesson.order, 3);
    });

    test('fromJson with missing optional fields', () {
      final json = {
        'id': 'test2',
        'title': 'T',
        'subtitle': 'S',
        'content': 'C',
      };
      final lesson = Lesson.fromJson(json);
      expect(lesson.example, '');
      expect(lesson.code, '');
      expect(lesson.tip, '');
      expect(lesson.order, 0);
    });

    test('fromJson with null fields', () {
      final json = <String, dynamic>{};
      final lesson = Lesson.fromJson(json);
      expect(lesson.id, '');
      expect(lesson.title, '');
    });
  });

  group('Quiz model', () {
    test('fromJson with valid data', () {
      final json = {
        'id': 'q1',
        'question': 'BFS 用什么数据结构？',
        'options': ['栈', '队列', '堆', '链表'],
        'answerIndex': 1,
        'explanation': 'BFS 使用队列',
      };
      final quiz = Quiz.fromJson(json);
      expect(quiz.id, 'q1');
      expect(quiz.options.length, 4);
      expect(quiz.answerIndex, 1);
    });

    test('fromJson with missing fields', () {
      final json = <String, dynamic>{};
      final quiz = Quiz.fromJson(json);
      expect(quiz.id, '');
      expect(quiz.options, isEmpty);
      expect(quiz.answerIndex, 0);
    });
  });

  group('Mistake model', () {
    test('fromJson with valid data', () {
      final json = {
        'id': 1,
        'title': '忘记标记已访问',
        'wrongCode': 'no vis check',
        'why': '会导致重复访问',
        'correct': '入队时标记 vis',
        'tip': '一定要标记',
      };
      final mistake = Mistake.fromJson(json);
      expect(mistake.id, 1);
      expect(mistake.title, '忘记标记已访问');
    });

    test('fromJson with null fields', () {
      final json = <String, dynamic>{};
      final mistake = Mistake.fromJson(json);
      expect(mistake.id, 0);
      expect(mistake.title, '');
    });
  });

  group('BfsStep model', () {
    test('fromJson with full data', () {
      final json = {
        'step': 0,
        'description': '初始状态',
        'layer': 0,
        'visited': ['0,0'],
        'queue': ['0,0'],
        'current': '0,0',
        'walls': ['1,1', '2,2'],
        'path': [],
        'start': '0,0',
        'end': '4,4',
      };
      final step = BfsStep.fromJson(json);
      expect(step.step, 0);
      expect(step.visited, contains('0,0'));
      expect(step.walls.length, 2);
    });

    test('fromJson with minimal data', () {
      final json = {'step': 1, 'description': 'test'};
      final step = BfsStep.fromJson(json);
      expect(step.layer, 0);
      expect(step.visited, isEmpty);
      expect(step.queue, isEmpty);
      expect(step.start, '0,0');
    });
  });

  group('Progress model', () {
    test('default constructor', () {
      const progress = Progress();
      expect(progress.completedLessons, isEmpty);
      expect(progress.quizScores, isEmpty);
      expect(progress.totalQuizAttempts, 0);
    });

    test('toJson and fromJson round-trip', () {
      final progress = Progress(
        completedLessons: {'lesson1', 'lesson2'},
        completedQuizzes: {'quiz1'},
        quizScores: {'bfs_basic': 18},
        totalQuizAttempts: 3,
        answerRecords: {'q1': 0, 'q2': 2},
      );
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(restored.completedLessons, containsAll(['lesson1', 'lesson2']));
      expect(restored.completedQuizzes, contains('quiz1'));
      expect(restored.quizScores['bfs_basic'], 18);
      expect(restored.totalQuizAttempts, 3);
      expect(restored.answerRecords['q1'], 0);
      expect(restored.answerRecords['q2'], 2);
    });

    test('fromJson with null json', () {
      final progress = Progress.fromJson(<String, dynamic>{});
      expect(progress.completedLessons, isEmpty);
      expect(progress.totalQuizAttempts, 0);
      expect(progress.answerRecords, isEmpty);
    });

    test('copyWith preserves values', () {
      const progress = Progress(totalQuizAttempts: 5);
      final updated = progress.copyWith(totalQuizAttempts: 6);
      expect(updated.totalQuizAttempts, 6);
    });

    test('answerRecords tracks quiz answers', () {
      final progress = Progress(answerRecords: {'q1': 1, 'q2': 0, 'q3': 2});
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(restored.answerRecords.length, 3);
      expect(restored.answerRecords['q2'], 0);
    });

    test('answerHistory with dates', () {
      final history = [
        AnswerRecord(
          topic: 'bfs',
          quizId: 'q1',
          selectedIndex: 0,
          correct: true,
          date: '2026-05-03 14:30',
        ),
        AnswerRecord(
          topic: 'dfs',
          quizId: 'q2',
          selectedIndex: 2,
          correct: false,
          date: '2026-05-03 14:31',
        ),
      ];
      expect(history[0].topic, 'bfs');
      expect(history[1].topic, 'dfs');
      expect(history[0].correct, true);
      expect(history[0].date, '2026-05-03 14:30');
      final r = AnswerRecord.fromJson(history[1].toJson());
      expect(r.quizId, 'q2');
      expect(r.correct, false);
    });
  });

  group('JSON data validation', () {
    test('bfs_basic.json has 5 lessons', () {
      final jsonStr = '''
[
  {"id":"b1","title":"T1","subtitle":"S","content":"C","order":1},
  {"id":"b2","title":"T2","subtitle":"S","content":"C","order":2},
  {"id":"b3","title":"T3","subtitle":"S","content":"C","order":3},
  {"id":"b4","title":"T4","subtitle":"S","content":"C","order":4},
  {"id":"b5","title":"T5","subtitle":"S","content":"C","order":5}
]''';
      final list = json.decode(jsonStr) as List;
      expect(list.length, 5);
      for (final item in list) {
        final lesson = Lesson.fromJson(item as Map<String, dynamic>);
        expect(lesson.id, isNotEmpty);
        expect(lesson.title, isNotEmpty);
      }
    });

    test('quiz options always 4 and answerIndex in range', () {
      final quizJson = '''
[
  {"id":"q1","question":"Q1","options":["A","B","C","D"],"answerIndex":0,"explanation":"E"},
  {"id":"q2","question":"Q2","options":["A","B","C","D"],"answerIndex":3,"explanation":"E"},
  {"id":"q3","question":"Q3","options":["A","B","C","D"],"answerIndex":2,"explanation":""}
]''';
      final list = json.decode(quizJson) as List;
      for (final item in list) {
        final quiz = Quiz.fromJson(item as Map<String, dynamic>);
        expect(quiz.options.length, 4);
        expect(quiz.answerIndex, inInclusiveRange(0, 3));
      }
    });

    test('BFS steps queue is FIFO', () {
      final stepsJson = '''
[
  {"step":0,"description":"init","visited":[],"queue":[]},
  {"step":1,"description":"enqueue start","visited":["0,0"],"queue":["0,0"]},
  {"step":2,"description":"expand","visited":["0,0","0,1","1,0"],"queue":["0,1","1,0"]}
]''';
      final list = json.decode(stepsJson) as List;
      for (final item in list) {
        final step = BfsStep.fromJson(item as Map<String, dynamic>);
        for (final v in step.visited) {
          expect(v, isNotEmpty);
        }
      }
    });
  });

  group('Content manifest models', () {
    test('ContentManifest fromJson with default values', () {
      final manifest = ContentManifest.fromJson({});
      expect(manifest.version, 1);
      expect(manifest.defaultTopicId, 'bfs');
      expect(manifest.topics, isEmpty);
      expect(manifest.modules, isEmpty);
    });

    test('ContentManifest finds topic by id', () {
      final manifest = ContentManifest.fromJson({
        'defaultTopicId': 'bfs',
        'topics': [
          {'topicId': 'bfs', 'title': 'BFS'},
          {'topicId': 'dfs', 'title': 'DFS'},
        ],
      });
      expect(manifest.findTopic('bfs')!.title, 'BFS');
      expect(manifest.findTopic('dfs')!.title, 'DFS');
      expect(manifest.findTopic('dp'), isNull);
      expect(manifest.defaultTopic.topicId, 'bfs');
    });

    test('LessonSet fromJson with defaults', () {
      final ls = LessonSet.fromJson({'lessonSetId': 'test'});
      expect(ls.lessonSetId, 'test');
      expect(ls.title, '');
      expect(ls.assetPath, '');
      expect(ls.order, 0);
    });

    test('QuizSet fromJson inherits topicId', () {
      final qs = QuizSet.fromJson({
        'quizSetId': 'bfs_basic',
        'assetPath': 'assets/data/quizzes/bfs_quiz.json',
        'totalQuestions': 20,
      }, topicId: 'bfs');
      expect(qs.quizSetId, 'bfs_basic');
      expect(qs.topicId, 'bfs');
      expect(qs.totalQuestions, 20);
    });

    test('MistakeSet fromJson', () {
      final ms = MistakeSet.fromJson({'mistakeSetId': 'm1'});
      expect(ms.mistakeSetId, 'm1');
      expect(ms.assetPath, '');
    });

    test('AnimationScenario fromJson with defaults', () {
      final as_ = AnimationScenario.fromJson({'scenarioId': 's1'});
      expect(as_.scenarioId, 's1');
      expect(as_.rows, 5);
      expect(as_.cols, 5);
      expect(as_.playIntervalMs, 1000);
    });

    test('ContentModule fromJson', () {
      final cm = ContentModule.fromJson({
        'moduleId': 'lesson',
        'title': 'Test',
        'iconKey': 'menu_book',
        'colorHex': '#4A90D9',
        'route': '/lesson',
        'order': 1,
      });
      expect(cm.moduleId, 'lesson');
      expect(cm.iconKey, 'menu_book');
      expect(cm.route, '/lesson');
    });

    test('LearningTopic findXxx methods', () {
      final topic = LearningTopic.fromJson({
        'topicId': 'bfs',
        'lessonSets': [
          {'lessonSetId': 'basic', 'assetPath': 'a.json', 'order': 1},
        ],
        'quizSets': [
          {'quizSetId': 'q1', 'assetPath': 'b.json'},
        ],
        'animationScenarios': [
          {'scenarioId': 's1', 'assetPath': 'c.json', 'rows': 6},
        ],
      });
      expect(topic.findLessonSet('basic')!.assetPath, 'a.json');
      expect(topic.findLessonSet('missing'), isNull);
      expect(topic.findQuizSet('q1')!.assetPath, 'b.json');
      expect(topic.findAnimationScenario('s1')!.rows, 6);
    });

    test('AnswerRecord round-trip with topic', () {
      final r = AnswerRecord(
        topic: 'dfs',
        quizId: 'q1',
        selectedIndex: 2,
        correct: true,
        date: '2026-05-03 15:00',
      );
      final json = r.toJson();
      final restored = AnswerRecord.fromJson(json);
      expect(restored.topic, 'dfs');
      expect(restored.quizId, 'q1');
      expect(restored.selectedIndex, 2);
      expect(restored.correct, true);
      expect(restored.date, '2026-05-03 15:00');
    });

    test('Progress old data compat without answerHistory', () {
      final jsonStr = '{"completedLessons":["l1"],"answerRecords":{"q1":0}}';
      final p = Progress.fromJson(json.decode(jsonStr) as Map<String, dynamic>);
      expect(p.completedLessons.length, 1);
      expect(p.answerRecords['q1'], 0);
      expect(p.answerHistory, isEmpty);
    });

    test('completedCppItems defaults to empty', () {
      const progress = Progress();
      expect(progress.completedCppItems, isEmpty);
    });

    test('fromJson old data without completedCppItemIds returns empty', () {
      final jsonStr = '{"completedLessons":["l1"]}';
      final p = Progress.fromJson(json.decode(jsonStr) as Map<String, dynamic>);
      expect(p.completedCppItems, isEmpty);
    });

    test('toJson/fromJson round-trip preserves completedCppItems', () {
      final progress = Progress(
        completedCppItems: {'cpp_var', 'cpp_loop', 'cpp_func'},
      );
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(
        restored.completedCppItems,
        containsAll(['cpp_var', 'cpp_loop', 'cpp_func']),
      );
      expect(restored.completedCppItems.length, 3);
    });

    test('copyWith updates completedCppItems', () {
      const progress = Progress(completedCppItems: {'cpp_var'});
      final updated = progress.copyWith(
        completedCppItems: {'cpp_var', 'cpp_loop'},
      );
      expect(updated.completedCppItems, containsAll(['cpp_var', 'cpp_loop']));
      expect(progress.completedCppItems.length, 1);
    });

    test('duplicate itemId in completedCppItems via Set semantics', () {
      final set = <String>{'cpp_var'};
      set.add('cpp_var');
      final progress = Progress(completedCppItems: set);
      expect(progress.completedCppItems.length, 1);
      expect(progress.completedCppItems, contains('cpp_var'));
    });

    test('completedCppItems does not affect other fields', () {
      final progress = Progress(
        completedLessons: {'l1'},
        completedQuizzes: {'q1'},
        quizScores: {'bfs': 10},
        completedCppItems: {'cpp_var'},
      );
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(restored.completedLessons, contains('l1'));
      expect(restored.completedQuizzes, contains('q1'));
      expect(restored.quizScores['bfs'], 10);
      expect(restored.completedCppItems, contains('cpp_var'));
    });
  });

  group('Progress cppQuizScores/cppQuizAttempts/cppWrongQuizIds', () {
    test('new fields default to empty', () {
      const progress = Progress();
      expect(progress.cppQuizScores, isEmpty);
      expect(progress.cppQuizAttempts, isEmpty);
      expect(progress.cppWrongQuizIds, isEmpty);
    });

    test('fromJson old data without new fields returns empty', () {
      final jsonStr = '{"completedLessons":["l1"]}';
      final p = Progress.fromJson(json.decode(jsonStr) as Map<String, dynamic>);
      expect(p.cppQuizScores, isEmpty);
      expect(p.cppQuizAttempts, isEmpty);
      expect(p.cppWrongQuizIds, isEmpty);
    });

    test('toJson/fromJson round-trip preserves new fields', () {
      final progress = Progress(
        cppQuizScores: {'1.1': 80, '1.2': 60},
        cppQuizAttempts: {'1.1': 3, '1.2': 1},
        cppWrongQuizIds: {'1.1|1.1.3|0', '1.2|1.2.1|1'},
      );
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(restored.cppQuizScores['1.1'], 80);
      expect(restored.cppQuizScores['1.2'], 60);
      expect(restored.cppQuizAttempts['1.1'], 3);
      expect(restored.cppQuizAttempts['1.2'], 1);
      expect(restored.cppWrongQuizIds, contains('1.1|1.1.3|0'));
      expect(restored.cppWrongQuizIds, contains('1.2|1.2.1|1'));
      expect(restored.cppWrongQuizIds.length, 2);
    });

    test('copyWith updates new fields', () {
      const progress = Progress();
      final updated = progress.copyWith(
        cppQuizScores: {'1.1': 100},
        cppQuizAttempts: {'1.1': 2},
        cppWrongQuizIds: {'1.1|1.1.1|0'},
      );
      expect(updated.cppQuizScores['1.1'], 100);
      expect(updated.cppQuizAttempts['1.1'], 2);
      expect(updated.cppWrongQuizIds, contains('1.1|1.1.1|0'));
      expect(progress.cppQuizScores, isEmpty);
    });

    test('new fields do not affect existing fields', () {
      final progress = Progress(
        completedLessons: {'l1'},
        completedCppItems: {'cpp_var'},
        cppQuizScores: {'1.1': 80},
      );
      final json = progress.toJson();
      final restored = Progress.fromJson(json);
      expect(restored.completedLessons, contains('l1'));
      expect(restored.completedCppItems, contains('cpp_var'));
      expect(restored.cppQuizScores['1.1'], 80);
    });
  });

  group('CppQuizEntry wrongId format', () {
    test('wrongId format is sectionId|itemId|quizIndex', () {
      final question = CppQuizQuestion(
        question: 'Q?',
        options: ['A', 'B', 'C', 'D'],
        answerIndex: 0,
        explanation: 'E',
      );
      final entry = CppQuizEntry(
        sectionId: '1.8',
        itemId: '1.8.9',
        quizIndex: 0,
        question: question,
      );
      expect(entry.wrongId, '1.8|1.8.9|0');
    });

    test('wrongId is stable across entries', () {
      final q1 = CppQuizQuestion(question: 'Q1');
      final q2 = CppQuizQuestion(question: 'Q2');
      final e1 = CppQuizEntry(
        sectionId: '1.1',
        itemId: '1.1.1',
        quizIndex: 0,
        question: q1,
      );
      final e2 = CppQuizEntry(
        sectionId: '1.1',
        itemId: '1.1.1',
        quizIndex: 0,
        question: q2,
      );
      expect(e1.wrongId, e2.wrongId);
    });

    test('different quizIndex produces different wrongId', () {
      final q = CppQuizQuestion(question: 'Q');
      final e1 = CppQuizEntry(
        sectionId: '1.1',
        itemId: '1.1.1',
        quizIndex: 0,
        question: q,
      );
      final e2 = CppQuizEntry(
        sectionId: '1.1',
        itemId: '1.1.1',
        quizIndex: 1,
        question: q,
      );
      expect(e1.wrongId, isNot(equals(e2.wrongId)));
    });
  });

  group('Cpp quiz save result logic', () {
    Progress simulateSave(
      Progress current, {
      required String sectionId,
      required int score,
      required Set<String> newWrongIds,
      required Set<String> correctedIds,
    }) {
      final updatedScores = Map<String, int>.from(current.cppQuizScores);
      updatedScores[sectionId] = score;

      final updatedAttempts = Map<String, int>.from(current.cppQuizAttempts);
      updatedAttempts[sectionId] = (updatedAttempts[sectionId] ?? 0) + 1;

      final updatedWrong = Set<String>.from(current.cppWrongQuizIds);
      updatedWrong.addAll(newWrongIds);
      updatedWrong.removeAll(correctedIds);

      return current.copyWith(
        cppQuizScores: updatedScores,
        cppQuizAttempts: updatedAttempts,
        cppWrongQuizIds: updatedWrong,
      );
    }

    test('first quiz saves score and wrong ids', () {
      const current = Progress();
      final updated = simulateSave(
        current,
        sectionId: '1.1',
        score: 67,
        newWrongIds: {'1.1|1.1.3|0', '1.1|1.1.5|1'},
        correctedIds: {},
      );
      expect(updated.cppQuizScores['1.1'], 67);
      expect(updated.cppQuizAttempts['1.1'], 1);
      expect(updated.cppWrongQuizIds.length, 2);
      expect(updated.cppWrongQuizIds, contains('1.1|1.1.3|0'));
    });

    test('second quiz updates score and increments attempts', () {
      var current = const Progress();
      current = simulateSave(
        current,
        sectionId: '1.1',
        score: 50,
        newWrongIds: {'1.1|1.1.3|0'},
        correctedIds: {},
      );
      current = simulateSave(
        current,
        sectionId: '1.1',
        score: 100,
        newWrongIds: {},
        correctedIds: {'1.1|1.1.3|0'},
      );
      expect(current.cppQuizScores['1.1'], 100);
      expect(current.cppQuizAttempts['1.1'], 2);
      expect(current.cppWrongQuizIds, isEmpty);
    });

    test('answering wrong adds to wrong set, answering correct removes', () {
      var current = const Progress();
      current = simulateSave(
        current,
        sectionId: '1.1',
        score: 50,
        newWrongIds: {'1.1|1.1.1|0', '1.1|1.1.2|0'},
        correctedIds: {},
      );
      expect(current.cppWrongQuizIds.length, 2);

      current = simulateSave(
        current,
        sectionId: '1.1',
        score: 100,
        newWrongIds: {},
        correctedIds: {'1.1|1.1.1|0'},
      );
      expect(current.cppWrongQuizIds.length, 1);
      expect(current.cppWrongQuizIds, contains('1.1|1.1.2|0'));
    });

    test('does not affect completedCppItems', () {
      final current = Progress(completedCppItems: {'cpp_var', 'cpp_loop'});
      final updated = simulateSave(
        current,
        sectionId: '1.1',
        score: 80,
        newWrongIds: {'1.1|1.1.3|0'},
        correctedIds: {},
      );
      expect(updated.completedCppItems, containsAll(['cpp_var', 'cpp_loop']));
      expect(updated.completedCppItems.length, 2);
    });

    test('does not affect BFS quiz scores', () {
      final current = Progress(quizScores: {'bfs': 18}, totalQuizAttempts: 5);
      final updated = simulateSave(
        current,
        sectionId: '1.1',
        score: 90,
        newWrongIds: {},
        correctedIds: {},
      );
      expect(updated.quizScores['bfs'], 18);
      expect(updated.totalQuizAttempts, 5);
    });
  });
}
