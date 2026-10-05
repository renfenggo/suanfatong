import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/learning_layer.dart';

/// 知识点分层服务
///
/// 负责加载 learning_path_layers_frontend_usage_review.json，
/// 并为每个知识点计算前端分层（core / standard / advanced / optional）。
///
/// 分层规则（只读消费，不写回主图谱）：
/// 1. 如果 itemId 在 suspected_misclassified_core 中，使用 suggested_frontend_layer
/// 2. 否则使用主图谱 io_v4_4.json 中的 visibility 字段
/// 3. 如果都没有，默认为 standard
class LearningLayerService {
  static const String _reviewDataPath =
      'data/learning_path_layers_frontend_usage_review.json';
  static const String _graphDataPath = 'assets/data/knowledge/io_v4_4.json';

  LearningLayerData? _layerDataCache;
  Map<String, String>? _graphVisibilityCache;
  bool _isLoading = false;
  String? _loadError;

  bool get isLoading => _isLoading;
  String? get loadError => _loadError;

  /// 加载分层数据
  Future<LearningLayerData> loadLayerData() async {
    if (_layerDataCache != null) return _layerDataCache!;

    _isLoading = true;
    _loadError = null;

    try {
      final jsonStr = await rootBundle.loadString(_reviewDataPath);
      final Map<String, dynamic> jsonData = json.decode(jsonStr);
      _layerDataCache = LearningLayerData.fromJson(jsonData);
      _isLoading = false;
      return _layerDataCache!;
    } catch (e) {
      _isLoading = false;
      _loadError = 'Failed to load layer data: $e';
      return const LearningLayerData();
    }
  }

  /// 加载主图谱中的 visibility 字段（只读，不修改原文件）
  Future<Map<String, String>> _loadGraphVisibility() async {
    if (_graphVisibilityCache != null) return _graphVisibilityCache!;

    try {
      final jsonStr = await rootBundle.loadString(_graphDataPath);
      final Map<String, dynamic> jsonData = json.decode(jsonStr);
      final result = <String, String>{};

      final categories = jsonData['categories'] as List? ?? [];
      for (final cat in categories) {
        final sections =
            (cat as Map<String, dynamic>)['sections'] as List? ?? [];
        for (final section in sections) {
          final items =
              (section as Map<String, dynamic>)['items'] as List? ?? [];
          for (final item in items) {
            final itemMap = item as Map<String, dynamic>;
            final id = itemMap['id'] as String? ?? '';
            final visibility = itemMap['visibility'] as String? ?? '';
            if (id.isNotEmpty && visibility.isNotEmpty) {
              result[id] = visibility;
            }
          }
        }
      }

      _graphVisibilityCache = result;
      return result;
    } catch (e) {
      _loadError = 'Failed to load graph visibility: $e';
      return {};
    }
  }

  /// 获取指定 itemId 的前端分层
  ///
  /// 优先级：
  /// 1. suspected_misclassified_core 中的 suggested_frontend_layer
  /// 2. 主图谱的 visibility 字段
  /// 3. 默认 standard
  Future<String> getFrontendLayerForItem(String itemId) async {
    final layerData = await loadLayerData();
    final override = layerData.frontendLayerOverrideForItem(itemId);
    if (override != null && override.isNotEmpty) return override;

    final visibility = await _loadGraphVisibility();
    final graphLayer = visibility[itemId];
    if (graphLayer != null && graphLayer.isNotEmpty) return graphLayer;

    return 'standard';
  }

  /// 批量获取多个 itemId 的前端分层
  Future<Map<String, String>> getFrontendLayersForItems(
    List<String> itemIds,
  ) async {
    final layerData = await loadLayerData();
    final visibility = await _loadGraphVisibility();
    final result = <String, String>{};

    for (final itemId in itemIds) {
      final override = layerData.frontendLayerOverrideForItem(itemId);
      if (override != null && override.isNotEmpty) {
        result[itemId] = override;
      } else {
        final graphLayer = visibility[itemId];
        result[itemId] =
            (graphLayer != null && graphLayer.isNotEmpty)
                ? graphLayer
                : 'standard';
      }
    }

    return result;
  }

  /// 获取指定章节的折叠策略
  Future<SectionCollapsePolicy?> getCollapsePolicy(String sectionId) async {
    final layerData = await loadLayerData();
    return layerData.collapsePolicyForSection(sectionId);
  }

  /// 清除缓存
  void clearCache() {
    _layerDataCache = null;
    _graphVisibilityCache = null;
    _loadError = null;
    _isLoading = false;
  }
}
