class MistakeSet {
  final String mistakeSetId;
  final String title;
  final String assetPath;
  final String pickupGroup;

  const MistakeSet({
    required this.mistakeSetId,
    this.title = '',
    this.assetPath = '',
    this.pickupGroup = '',
  });

  factory MistakeSet.fromJson(Map<String, dynamic> json) {
    return MistakeSet(
      mistakeSetId: json['mistakeSetId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      assetPath: json['assetPath'] as String? ?? '',
      pickupGroup: json['pickupGroup'] as String? ?? '',
    );
  }
}
