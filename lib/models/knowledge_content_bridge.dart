import 'knowledge_graph.dart';
import 'knowledge_item.dart';
import 'content_manifest.dart';

class KnowledgeContentBridge {
  final KnowledgeGraph graph;
  final ContentManifest manifest;

  const KnowledgeContentBridge({required this.graph, required this.manifest});

  List<KnowledgeItem> itemsForPickupGroup(String pickupGroup) {
    return graph.itemsByPickupGroup(pickupGroup);
  }

  List<KnowledgeItem> itemsForLessonSet(String lessonSetId) {
    final topic = manifest.defaultTopic;
    final ls = topic.findLessonSet(lessonSetId);
    if (ls == null || ls.pickupGroup.isEmpty) return const [];
    return graph.itemsByPickupGroup(ls.pickupGroup);
  }

  List<KnowledgeItem> itemsForQuizSet(String quizSetId) {
    final topic = manifest.defaultTopic;
    final qs = topic.findQuizSet(quizSetId);
    if (qs == null || qs.pickupGroup.isEmpty) return const [];
    return graph.itemsByPickupGroup(qs.pickupGroup);
  }

  List<KnowledgeItem> itemsForMistakeSet(String mistakeSetId) {
    final topic = manifest.defaultTopic;
    final ms = topic.findMistakeSet(mistakeSetId);
    if (ms == null || ms.pickupGroup.isEmpty) return const [];
    return graph.itemsByPickupGroup(ms.pickupGroup);
  }

  String? lessonSetIdForItem(KnowledgeItem item) {
    if (item.pickupGroup.isEmpty) return null;
    final topic = manifest.defaultTopic;
    for (final ls in topic.lessonSets) {
      if (ls.pickupGroup == item.pickupGroup) return ls.lessonSetId;
    }
    return null;
  }

  String? quizSetIdForItem(KnowledgeItem item) {
    if (item.pickupGroup.isEmpty) return null;
    final topic = manifest.defaultTopic;
    for (final qs in topic.quizSets) {
      if (qs.pickupGroup == item.pickupGroup) return qs.quizSetId;
    }
    return null;
  }

  String? mistakeSetIdForItem(KnowledgeItem item) {
    if (item.pickupGroup.isEmpty) return null;
    final topic = manifest.defaultTopic;
    for (final ms in topic.mistakeSets) {
      if (ms.pickupGroup == item.pickupGroup) return ms.mistakeSetId;
    }
    return null;
  }
}
