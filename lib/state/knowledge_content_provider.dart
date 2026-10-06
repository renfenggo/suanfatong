import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/knowledge_content_index.dart';
import '../models/knowledge_content_item.dart';
import '../repositories/content_index_repository.dart';
import '../repositories/knowledge_content_repository.dart';
import 'content_manifest_provider.dart' show jsonAssetRepositoryProvider;

final contentIndexRepositoryProvider = Provider<ContentIndexRepository>((ref) {
  return ContentIndexRepository(
    jsonRepo: ref.watch(jsonAssetRepositoryProvider),
  );
});

final knowledgeContentRepositoryProvider = Provider<KnowledgeContentRepository>(
  (ref) {
    return KnowledgeContentRepository(
      jsonRepo: ref.watch(jsonAssetRepositoryProvider),
    );
  },
);

/// knowledge_content 内容包清单（生产元信息，33 分片 / 3240 节点）。
final contentIndexProvider = FutureProvider<KnowledgeContentIndex>((ref) {
  return ref.watch(contentIndexRepositoryProvider).loadIndex();
});

/// 按 item_id 加载讲解内容；失败降级为 null（UI 隐藏讲解区）。
final knowledgeContentItemProvider =
    FutureProvider.family<KnowledgeContentItem?, String>((ref, itemId) {
      return ref.watch(knowledgeContentRepositoryProvider).loadItem(itemId);
    });
