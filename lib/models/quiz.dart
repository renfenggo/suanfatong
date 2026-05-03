class Quiz {
  final String id;
  final String question;
  final List<String> options;
  final int answerIndex;
  final String explanation;

  const Quiz({
    required this.id,
    required this.question,
    required this.options,
    required this.answerIndex,
    this.explanation = '',
  });

  factory Quiz.fromJson(Map<String, dynamic> json) {
    return Quiz(
      id: json['id'] as String? ?? '',
      question: json['question'] as String? ?? '',
      options:
          (json['options'] as List?)?.map((e) => e.toString()).toList() ??
          const [],
      answerIndex: json['answerIndex'] as int? ?? 0,
      explanation: json['explanation'] as String? ?? '',
    );
  }
}
