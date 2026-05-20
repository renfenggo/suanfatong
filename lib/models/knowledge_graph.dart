import 'knowledge_category.dart';
import 'knowledge_section.dart';
import 'knowledge_item.dart';

const _categorySortOrder = ['C++语法', '算法', '数据结构', '算法竞赛数学', 'C++编程/调试技巧'];

class KnowledgeGraph {
  final Map<String, dynamic> meta;
  final List<KnowledgeCategory> categories;

  const KnowledgeGraph({this.meta = const {}, this.categories = const []});

  factory KnowledgeGraph.fromJson(Map<String, dynamic> json) {
    final rawCategories =
        (json['categories'] as List?)
            ?.map((e) => KnowledgeCategory.fromJson(e as Map<String, dynamic>))
            .toList() ??
        const [];
    final sorted = List<KnowledgeCategory>.from(rawCategories);
    sorted.sort((a, b) {
      final ai = _categorySortOrder.indexOf(a.name);
      final bi = _categorySortOrder.indexOf(b.name);
      final av = ai == -1 ? _categorySortOrder.length : ai;
      final bv = bi == -1 ? _categorySortOrder.length : bi;
      return av.compareTo(bv);
    });
    return KnowledgeGraph(
      meta: (json['meta'] as Map<String, dynamic>?) ?? const {},
      categories: sorted,
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
