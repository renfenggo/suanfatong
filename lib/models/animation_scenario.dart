class AnimationScenario {
  final String scenarioId;
  final String title;
  final String assetPath;
  final int rows;
  final int cols;
  final int playIntervalMs;
  final String pickupGroup;

  const AnimationScenario({
    required this.scenarioId,
    this.title = '',
    this.assetPath = '',
    this.rows = 5,
    this.cols = 5,
    this.playIntervalMs = 1000,
    this.pickupGroup = '',
  });

  factory AnimationScenario.fromJson(Map<String, dynamic> json) {
    return AnimationScenario(
      scenarioId: json['scenarioId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      assetPath: json['assetPath'] as String? ?? '',
      rows: json['rows'] as int? ?? 5,
      cols: json['cols'] as int? ?? 5,
      playIntervalMs: json['playIntervalMs'] as int? ?? 1000,
      pickupGroup: json['pickupGroup'] as String? ?? '',
    );
  }
}
