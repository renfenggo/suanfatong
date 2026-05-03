class Lesson {
  final String id;
  final String title;
  final String subtitle;
  final String content;
  final String example;
  final String code;
  final String tip;
  final int order;

  const Lesson({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.content,
    this.example = '',
    this.code = '',
    this.tip = '',
    this.order = 0,
  });

  factory Lesson.fromJson(Map<String, dynamic> json) {
    return Lesson(
      id: json['id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      subtitle: json['subtitle'] as String? ?? '',
      content: json['content'] as String? ?? '',
      example: json['example'] as String? ?? '',
      code: json['code'] as String? ?? '',
      tip: json['tip'] as String? ?? '',
      order: json['order'] as int? ?? 0,
    );
  }
}
