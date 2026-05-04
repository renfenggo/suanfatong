class QuizSet {
  final String quizSetId;
  final String title;
  final String assetPath;
  final int totalQuestions;
  final String topicId;
  final String pickupGroup;

  const QuizSet({
    required this.quizSetId,
    this.title = '',
    this.assetPath = '',
    this.totalQuestions = 0,
    this.topicId = '',
    this.pickupGroup = '',
  });

  factory QuizSet.fromJson(Map<String, dynamic> json, {String topicId = ''}) {
    return QuizSet(
      quizSetId: json['quizSetId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      assetPath: json['assetPath'] as String? ?? '',
      totalQuestions: json['totalQuestions'] as int? ?? 0,
      topicId: json['topicId'] as String? ?? topicId,
      pickupGroup: json['pickupGroup'] as String? ?? '',
    );
  }
}
