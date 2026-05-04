import 'knowledge_section.dart';

class KnowledgeCategory {
  final String name;
  final List<KnowledgeSection> sections;

  const KnowledgeCategory({required this.name, this.sections = const []});

  factory KnowledgeCategory.fromJson(Map<String, dynamic> json) {
    return KnowledgeCategory(
      name: json['name'] as String? ?? '',
      sections:
          (json['sections'] as List?)
              ?.map((e) => KnowledgeSection.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }
}
