import 'learning_topic.dart';
import 'content_module.dart';

class ContentManifest {
  final int version;
  final String defaultTopicId;
  final List<LearningTopic> topics;
  final List<ContentModule> modules;

  const ContentManifest({
    this.version = 1,
    this.defaultTopicId = 'bfs',
    this.topics = const [],
    this.modules = const [],
  });

  factory ContentManifest.fromJson(Map<String, dynamic> json) {
    return ContentManifest(
      version: json['version'] as int? ?? 1,
      defaultTopicId: json['defaultTopicId'] as String? ?? 'bfs',
      topics:
          (json['topics'] as List?)
              ?.map((e) => LearningTopic.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      modules:
          (json['modules'] as List?)
              ?.map((e) => ContentModule.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }

  LearningTopic? findTopic(String topicId) {
    for (final t in topics) {
      if (t.topicId == topicId) return t;
    }
    return null;
  }

  LearningTopic get defaultTopic {
    return findTopic(defaultTopicId) ??
        (topics.isNotEmpty ? topics.first : const LearningTopic(topicId: ''));
  }
}
