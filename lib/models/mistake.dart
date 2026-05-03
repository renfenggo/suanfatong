class Mistake {
  final int id;
  final String title;
  final String wrongCode;
  final String why;
  final String correct;
  final String tip;

  const Mistake({
    required this.id,
    required this.title,
    required this.wrongCode,
    required this.why,
    required this.correct,
    required this.tip,
  });

  factory Mistake.fromJson(Map<String, dynamic> json) {
    return Mistake(
      id: json['id'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      wrongCode: json['wrongCode'] as String? ?? '',
      why: json['why'] as String? ?? '',
      correct: json['correct'] as String? ?? '',
      tip: json['tip'] as String? ?? '',
    );
  }
}
