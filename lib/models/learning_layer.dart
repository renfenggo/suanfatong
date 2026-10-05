/// 知识点前端分层模型
///
/// 表示知识点的 core / standard / advanced / optional 分层信息，
/// 以及章节级别的折叠策略。
///
/// 数据来源：data/learning_path_layers_frontend_usage_review.json
/// 注意：本模型为只读消费，不写回主图谱。
class LearningLayerData {
  /// 审计时间
  final String auditTime;

  /// 总知识点数
  final int totalItems;

  /// 前端分层统计
  final FrontendLayerTotals frontendLayerTotals;

  /// 疑似误分 core 节点（包含 id -> suggested_frontend_layer 映射）
  final List<MisclassifiedCoreItem> suspectedMisclassifiedCore;

  /// 高拥挤章节折叠策略
  final List<SectionCollapsePolicy> overcrowdedSectionCollapsePolicy;

  /// 前端分层展示建议
  final Map<String, LayerDisplaySuggestion> frontendDisplayLayerSuggestions;

  const LearningLayerData({
    this.auditTime = '',
    this.totalItems = 0,
    this.frontendLayerTotals = const FrontendLayerTotals(),
    this.suspectedMisclassifiedCore = const [],
    this.overcrowdedSectionCollapsePolicy = const [],
    this.frontendDisplayLayerSuggestions = const {},
  });

  factory LearningLayerData.fromJson(Map<String, dynamic> json) {
    return LearningLayerData(
      auditTime: json['audit_time'] as String? ?? '',
      totalItems: json['total_items'] as int? ?? 0,
      frontendLayerTotals: FrontendLayerTotals.fromJson(
        json['frontend_layer_totals'] as Map<String, dynamic>? ?? {},
      ),
      suspectedMisclassifiedCore: _parseMisclassifiedList(
        json['suspected_misclassified_core'],
      ),
      overcrowdedSectionCollapsePolicy: _parseCollapsePolicyList(
        json['overcrowded_section_collapse_policy'],
      ),
      frontendDisplayLayerSuggestions: _parseDisplaySuggestions(
        json['frontend_display_layer_suggestions'],
      ),
    );
  }

  /// 获取指定章节的折叠策略，无数据时返回 null
  SectionCollapsePolicy? collapsePolicyForSection(String sectionId) {
    for (final policy in overcrowdedSectionCollapsePolicy) {
      if (policy.sectionId == sectionId) return policy;
    }
    return null;
  }

  /// 获取指定 itemId 的前端分层覆盖（来自误分列表）
  /// 返回 "advanced" 等覆盖值，如果不在误分列表中则返回 null
  String? frontendLayerOverrideForItem(String itemId) {
    for (final item in suspectedMisclassifiedCore) {
      if (item.id == itemId) return item.suggestedFrontendLayer;
    }
    return null;
  }
}

/// 前端分层统计
class FrontendLayerTotals {
  final int core;
  final int standard;
  final int advanced;
  final int optional;

  const FrontendLayerTotals({
    this.core = 0,
    this.standard = 0,
    this.advanced = 0,
    this.optional = 0,
  });

  factory FrontendLayerTotals.fromJson(Map<String, dynamic> json) {
    return FrontendLayerTotals(
      core: json['core'] as int? ?? 0,
      standard: json['standard'] as int? ?? 0,
      advanced: json['advanced'] as int? ?? 0,
      optional: json['optional'] as int? ?? 0,
    );
  }
}

/// 疑似误分 core 节点
class MisclassifiedCoreItem {
  final String id;
  final String name;
  final String sectionId;
  final String currentLayer;
  final String suggestedFrontendLayer;
  final String reason;

  const MisclassifiedCoreItem({
    required this.id,
    this.name = '',
    this.sectionId = '',
    this.currentLayer = '',
    this.suggestedFrontendLayer = '',
    this.reason = '',
  });

  factory MisclassifiedCoreItem.fromJson(Map<String, dynamic> json) {
    return MisclassifiedCoreItem(
      id: json['id'] as String? ?? '',
      name: json['name'] as String? ?? '',
      sectionId: json['section_id'] as String? ?? '',
      currentLayer: json['current_layer'] as String? ?? '',
      suggestedFrontendLayer:
          json['suggested_frontend_layer'] as String? ?? '',
      reason: json['reason'] as String? ?? '',
    );
  }
}

/// 章节折叠策略
class SectionCollapsePolicy {
  final String sectionId;
  final String sectionName;
  final String category;
  final int total;
  final int frontendCore;
  final int frontendStandard;
  final int frontendAdvanced;
  final int frontendOptional;
  final double foldableRatio;
  final String defaultCollapsePolicy;

  const SectionCollapsePolicy({
    required this.sectionId,
    this.sectionName = '',
    this.category = '',
    this.total = 0,
    this.frontendCore = 0,
    this.frontendStandard = 0,
    this.frontendAdvanced = 0,
    this.frontendOptional = 0,
    this.foldableRatio = 0,
    this.defaultCollapsePolicy = '',
  });

  factory SectionCollapsePolicy.fromJson(Map<String, dynamic> json) {
    return SectionCollapsePolicy(
      sectionId: json['section_id'] as String? ?? '',
      sectionName: json['section_name'] as String? ?? '',
      category: json['category'] as String? ?? '',
      total: json['total'] as int? ?? 0,
      frontendCore: json['frontend_core'] as int? ?? 0,
      frontendStandard: json['frontend_standard'] as int? ?? 0,
      frontendAdvanced: json['frontend_advanced'] as int? ?? 0,
      frontendOptional: json['frontend_optional'] as int? ?? 0,
      foldableRatio: (json['foldable_ratio'] as num?)?.toDouble() ?? 0,
      defaultCollapsePolicy:
          json['default_collapse_policy'] as String? ?? '',
    );
  }

  /// 是否应默认折叠 advanced
  bool get shouldCollapseAdvanced =>
      defaultCollapsePolicy.contains('advanced');

  /// 是否应默认折叠 optional
  bool get shouldCollapseOptional =>
      defaultCollapsePolicy.contains('optional');
}

/// 前端分层展示建议
class LayerDisplaySuggestion {
  final String display;
  final String description;
  final String uiBehavior;
  final String colorSuggestion;

  const LayerDisplaySuggestion({
    this.display = '',
    this.description = '',
    this.uiBehavior = '',
    this.colorSuggestion = '',
  });

  factory LayerDisplaySuggestion.fromJson(Map<String, dynamic> json) {
    return LayerDisplaySuggestion(
      display: json['display'] as String? ?? '',
      description: json['description'] as String? ?? '',
      uiBehavior: json['ui_behavior'] as String? ?? '',
      colorSuggestion: json['color_suggestion'] as String? ?? '',
    );
  }
}

// ===== 辅助解析函数 =====

List<MisclassifiedCoreItem> _parseMisclassifiedList(dynamic value) {
  if (value is List) {
    return value
        .map((e) => MisclassifiedCoreItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }
  return const [];
}

List<SectionCollapsePolicy> _parseCollapsePolicyList(dynamic value) {
  if (value is List) {
    return value
        .map((e) => SectionCollapsePolicy.fromJson(e as Map<String, dynamic>))
        .toList();
  }
  return const [];
}

Map<String, LayerDisplaySuggestion> _parseDisplaySuggestions(dynamic value) {
  if (value is Map) {
    final result = <String, LayerDisplaySuggestion>{};
    value.forEach((key, val) {
      if (val is Map<String, dynamic>) {
        result[key.toString()] = LayerDisplaySuggestion.fromJson(val);
      }
    });
    return result;
  }
  return const {};
}
