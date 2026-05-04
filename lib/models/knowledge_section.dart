import 'knowledge_item.dart';

class KnowledgeSection {
  final String id;
  final String name;
  final String level;
  final List<String> pre;
  final List<String> rel;
  final List<KnowledgeItem> items;
  final List<Map<String, dynamic>> learningBlocks;
  final String track;
  final String trackNote;

  const KnowledgeSection({
    required this.id,
    required this.name,
    this.level = '',
    this.pre = const [],
    this.rel = const [],
    this.items = const [],
    this.learningBlocks = const [],
    this.track = '',
    this.trackNote = '',
  });

  factory KnowledgeSection.fromJson(Map<String, dynamic> json) {
    return KnowledgeSection(
      id: json['id'] as String? ?? '',
      name: json['name'] as String? ?? '',
      level: json['level'] as String? ?? '',
      pre: _toStringList(json['pre']),
      rel: _toStringList(json['rel']),
      items:
          (json['items'] as List?)
              ?.map((e) => KnowledgeItem.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      learningBlocks:
          (json['learning_blocks'] as List?)
              ?.cast<Map<String, dynamic>>()
              .toList() ??
          const [],
      track: json['track'] as String? ?? '',
      trackNote: json['track_note'] as String? ?? '',
    );
  }
}

List<String> _toStringList(dynamic value) {
  if (value is List) {
    return value.whereType<String>().toList();
  }
  return const [];
}
