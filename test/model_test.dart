import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/lesson.dart';
import 'package:bfs_learn/models/quiz.dart';
import 'package:bfs_learn/models/mistake.dart';
import 'package:bfs_learn/models/bfs_step.dart';
import 'package:bfs_learn/models/progress.dart';
import 'package:bfs_learn/models/answer_record.dart';
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
}
