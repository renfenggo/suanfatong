class LessonSet {
  final String lessonSetId;
  final String title;
  final String subtitle;
  final String assetPath;
  final int order;
  final String pickupGroup;

  const LessonSet({
    required this.lessonSetId,
    this.title = '',
    this.subtitle = '',
    this.assetPath = '',
    this.order = 0,
    this.pickupGroup = '',
  });

  factory LessonSet.fromJson(Map<String, dynamic> json) {
    return LessonSet(
      lessonSetId: json['lessonSetId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      subtitle: json['subtitle'] as String? ?? '',
      assetPath: json['assetPath'] as String? ?? '',
      order: json['order'] as int? ?? 0,
      pickupGroup: json['pickupGroup'] as String? ?? '',
    );
  }
}
