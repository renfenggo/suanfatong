import 'answer_record.dart';

class Progress {
  final Set<String> completedLessons;
  final Set<String> completedQuizzes;
  final Map<String, int> quizScores;
  final int totalQuizAttempts;
  final Map<String, int> answerRecords;
  final List<AnswerRecord> answerHistory;
  final Set<String> completedCppItems;
  final Map<String, int> cppQuizScores;
  final Map<String, int> cppQuizAttempts;
  final Set<String> cppWrongQuizIds;

  const Progress({
    this.completedLessons = const {},
    this.completedQuizzes = const {},
    this.quizScores = const {},
    this.totalQuizAttempts = 0,
    this.answerRecords = const {},
    this.answerHistory = const [],
    this.completedCppItems = const {},
    this.cppQuizScores = const {},
    this.cppQuizAttempts = const {},
    this.cppWrongQuizIds = const {},
  });

  Progress copyWith({
    Set<String>? completedLessons,
    Set<String>? completedQuizzes,
    Map<String, int>? quizScores,
    int? totalQuizAttempts,
    Map<String, int>? answerRecords,
    List<AnswerRecord>? answerHistory,
    Set<String>? completedCppItems,
    Map<String, int>? cppQuizScores,
    Map<String, int>? cppQuizAttempts,
    Set<String>? cppWrongQuizIds,
  }) {
    return Progress(
      completedLessons: completedLessons ?? this.completedLessons,
      completedQuizzes: completedQuizzes ?? this.completedQuizzes,
      quizScores: quizScores ?? this.quizScores,
      totalQuizAttempts: totalQuizAttempts ?? this.totalQuizAttempts,
      answerRecords: answerRecords ?? this.answerRecords,
      answerHistory: answerHistory ?? this.answerHistory,
      completedCppItems: completedCppItems ?? this.completedCppItems,
      cppQuizScores: cppQuizScores ?? this.cppQuizScores,
      cppQuizAttempts: cppQuizAttempts ?? this.cppQuizAttempts,
      cppWrongQuizIds: cppWrongQuizIds ?? this.cppWrongQuizIds,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'completedLessons': completedLessons.toList(),
      'completedQuizzes': completedQuizzes.toList(),
      'quizScores': quizScores,
      'totalQuizAttempts': totalQuizAttempts,
      'answerRecords': answerRecords,
      'completedCppItems': completedCppItems.toList(),
      'cppQuizScores': cppQuizScores,
      'cppQuizAttempts': cppQuizAttempts,
      'cppWrongQuizIds': cppWrongQuizIds.toList(),
    };
  }

  factory Progress.fromJson(Map<String, dynamic> json) {
    return Progress(
      completedLessons:
          (json['completedLessons'] as List?)?.cast<String>().toSet() ?? {},
      completedQuizzes:
          (json['completedQuizzes'] as List?)?.cast<String>().toSet() ?? {},
      quizScores: Map<String, int>.from(json['quizScores'] as Map? ?? {}),
      totalQuizAttempts: json['totalQuizAttempts'] as int? ?? 0,
      answerRecords: Map<String, int>.from(json['answerRecords'] as Map? ?? {}),
      completedCppItems:
          (json['completedCppItems'] as List?)?.cast<String>().toSet() ?? {},
      cppQuizScores: Map<String, int>.from(json['cppQuizScores'] as Map? ?? {}),
      cppQuizAttempts: Map<String, int>.from(
        json['cppQuizAttempts'] as Map? ?? {},
      ),
      cppWrongQuizIds:
          (json['cppWrongQuizIds'] as List?)?.cast<String>().toSet() ?? {},
    );
  }
}
