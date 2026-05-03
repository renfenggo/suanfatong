import 'answer_record.dart';

class Progress {
  final Set<String> completedLessons;
  final Set<String> completedQuizzes;
  final Map<String, int> quizScores;
  final int totalQuizAttempts;
  final Map<String, int> answerRecords;
  final List<AnswerRecord> answerHistory;

  const Progress({
    this.completedLessons = const {},
    this.completedQuizzes = const {},
    this.quizScores = const {},
    this.totalQuizAttempts = 0,
    this.answerRecords = const {},
    this.answerHistory = const [],
  });

  Progress copyWith({
    Set<String>? completedLessons,
    Set<String>? completedQuizzes,
    Map<String, int>? quizScores,
    int? totalQuizAttempts,
    Map<String, int>? answerRecords,
    List<AnswerRecord>? answerHistory,
  }) {
    return Progress(
      completedLessons: completedLessons ?? this.completedLessons,
      completedQuizzes: completedQuizzes ?? this.completedQuizzes,
      quizScores: quizScores ?? this.quizScores,
      totalQuizAttempts: totalQuizAttempts ?? this.totalQuizAttempts,
      answerRecords: answerRecords ?? this.answerRecords,
      answerHistory: answerHistory ?? this.answerHistory,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'completedLessons': completedLessons.toList(),
      'completedQuizzes': completedQuizzes.toList(),
      'quizScores': quizScores,
      'totalQuizAttempts': totalQuizAttempts,
      'answerRecords': answerRecords,
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
    );
  }
}
