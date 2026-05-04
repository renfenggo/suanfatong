import 'knowledge_category.dart';
import 'knowledge_section.dart';
import 'knowledge_item.dart';

class KnowledgeGraph {
  final Map<String, dynamic> meta;
  final List<KnowledgeCategory> categories;

  const KnowledgeGraph({this.meta = const {}, this.categories = const []});

  factory KnowledgeGraph.fromJson(Map<String, dynamic> json) {
    return KnowledgeGraph(
      meta: (json['meta'] as Map<String, dynamic>?) ?? const {},
      categories:
          (json['categories'] as List?)
              ?.map(
                (e) => KnowledgeCategory.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          const [],
    );
  }

  List<KnowledgeSection> get allSections {
    final result = <KnowledgeSection>[];
    for (final cat in categories) {
      result.addAll(cat.sections);
    }
    return result;
  }

  List<KnowledgeItem> get allItems {
    final result = <KnowledgeItem>[];
    for (final section in allSections) {
      result.addAll(section.items);
    }
    return result;
  }

  KnowledgeSection? sectionById(String id) {
    for (final section in allSections) {
      if (section.id == id) return section;
    }
    return null;
  }

  KnowledgeItem? itemById(String id) {
    for (final item in allItems) {
      if (item.id == id) return item;
    }
    return null;
  }

  List<KnowledgeItem> itemsByPickupGroup(String group) {
    return allItems.where((item) => item.pickupGroup == group).toList();
  }

  List<KnowledgeItem> itemsOfSection(String sectionId) {
    final section = sectionById(sectionId);
    return section?.items.toList() ?? const [];
  }
}
