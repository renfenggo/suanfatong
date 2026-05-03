class BfsStep {
  final int step;
  final String description;
  final int layer;
  final Set<String> visited;
  final List<String> queue;
  final String? current;
  final Set<String> walls;
  final Set<String> path;
  final String start;
  final String end;

  const BfsStep({
    required this.step,
    required this.description,
    this.layer = 0,
    this.visited = const {},
    this.queue = const [],
    this.current,
    this.walls = const {},
    this.path = const {},
    this.start = '0,0',
    this.end = '4,4',
  });

  factory BfsStep.fromJson(Map<String, dynamic> json) {
    return BfsStep(
      step: json['step'] as int,
      description: json['description'] as String,
      layer: json['layer'] as int? ?? 0,
      visited: (json['visited'] as List?)?.cast<String>().toSet() ?? {},
      queue: (json['queue'] as List?)?.cast<String>() ?? [],
      current: json['current'] as String?,
      walls: (json['walls'] as List?)?.cast<String>().toSet() ?? {},
      path: (json['path'] as List?)?.cast<String>().toSet() ?? {},
      start: json['start'] as String? ?? '0,0',
      end: json['end'] as String? ?? '4,4',
    );
  }
}
