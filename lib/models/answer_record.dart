class AnswerRecord {
  final String topic;
  final String quizId;
  final int selectedIndex;
  final bool correct;
  final String date;

  const AnswerRecord({
    this.topic = 'bfs',
    required this.quizId,
    required this.selectedIndex,
    required this.correct,
    required this.date,
  });

  Map<String, dynamic> toJson() {
    return {
      'topic': topic,
      'quizId': quizId,
      'selectedIndex': selectedIndex,
      'correct': correct,
      'date': date,
    };
  }

  factory AnswerRecord.fromJson(Map<String, dynamic> json) {
    return AnswerRecord(
      topic: json['topic'] as String? ?? 'bfs',
      quizId: json['quizId'] as String? ?? '',
      selectedIndex: json['selectedIndex'] as int? ?? 0,
      correct: json['correct'] as bool? ?? false,
      date: json['date'] as String? ?? '',
    );
  }
}
