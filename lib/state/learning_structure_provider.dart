import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/learning_path_service.dart';
import '../services/learning_layer_service.dart';
import '../models/learning_path.dart';
import '../models/learning_layer.dart';

/// 学习路径服务 provider
final learningPathServiceProvider = Provider<LearningPathService>((ref) {
  return LearningPathService();
});

/// 分层服务 provider
final learningLayerServiceProvider = Provider<LearningLayerService>((ref) {
  return LearningLayerService();
});

/// 指定章节的学习路径 provider
final sectionLearningPathProvider =
    FutureProvider.family<LearningPath?, String>((ref, sectionId) {
      final service = ref.watch(learningPathServiceProvider);
      return service.getLearningPathBySectionId(sectionId);
    });

/// 指定章节的折叠策略 provider
final sectionCollapsePolicyProvider =
    FutureProvider.family<SectionCollapsePolicy?, String>((ref, sectionId) {
      final service = ref.watch(learningLayerServiceProvider);
      return service.getCollapsePolicy(sectionId);
    });

/// 批量获取多个 itemId 的前端分层 provider
final itemFrontendLayersProvider =
    FutureProvider.family<Map<String, String>, List<String>>((
      ref,
      itemIds,
    ) {
      final service = ref.watch(learningLayerServiceProvider);
      return service.getFrontendLayersForItems(itemIds);
    });
