/// 章节学习路径模型
/// 
/// 表示一个章节的推荐学习路径，包括入门、提高、冲刺三个阶段
/// 以及需要学习的跨章节前置知识点
class LearningPath {
  final String sectionId;
  final String sectionName;
  final List<String> beginnerPath;
  final String beginnerDescription;
  final List<String> intermediatePath;
  final String intermediateDescription;
  final List<String> advancedPath;
  final String advancedDescription;
  final List<CrossSectionPrerequisite> crossSectionPrerequisites;
  final ValidationStatus validationStatus;

  const LearningPath({
    required this.sectionId,
    required this.sectionName,
    this.beginnerPath = const [],
    this.beginnerDescription = '',
    this.intermediatePath = const [],
    this.intermediateDescription = '',
    this.advancedPath = const [],
    this.advancedDescription = '',
    this.crossSectionPrerequisites = const [],
    this.validationStatus = ValidationStatus.unknown,
  });

  /// 从JSON创建LearningPath实例
  /// 
  /// [json] 包含路径数据的JSON对象
  /// [sectionId] 可选的章节ID，如果不提供则从json中读取
  factory LearningPath.fromJson(Map<String, dynamic> json, {String? sectionId}) {
    return LearningPath(
      sectionId: sectionId ?? 
                  (json['section_id'] as String? ?? json['section_name'] as String? ?? ''),
      sectionName: json['section_name'] as String? ?? '',
      beginnerPath: _toStringList(json['beginner_path']),
      beginnerDescription: json['beginner_description'] as String? ?? '',
      intermediatePath: _toStringList(json['intermediate_path']),
      intermediateDescription: json['intermediate_description'] as String? ?? '',
      advancedPath: _toStringList(json['advanced_path']),
      advancedDescription: json['advanced_description'] as String? ?? '',
      crossSectionPrerequisites: _toCrossSectionList(json['cross_section_prerequisites']),
    );
  }

  /// 检查章节是否有学习路径数据
  bool hasPathData() {
    return beginnerPath.isNotEmpty || 
           intermediatePath.isNotEmpty || 
           advancedPath.isNotEmpty;
  }

  /// 检查是否有跨章节前置
  bool hasCrossSectionPrerequisites() {
    return crossSectionPrerequisites.isNotEmpty;
  }

  /// 获取总路径知识点数量
  int getTotalPathCount() {
    return beginnerPath.length + intermediatePath.length + advancedPath.length;
  }

  /// 获取路径统计信息
  Map<String, int> getPathStatistics() {
    return {
      'beginner': beginnerPath.length,
      'intermediate': intermediatePath.length,
      'advanced': advancedPath.length,
      'crossSection': crossSectionPrerequisites.length,
      'total': beginnerPath.length + intermediatePath.length + advancedPath.length + crossSectionPrerequisites.length,
    };
  }

  /// 转换为JSON
  Map<String, dynamic> toJson() {
    return {
      'section_id': sectionId,
      'section_name': sectionName,
      'beginner_path': beginnerPath,
      'beginner_description': beginnerDescription,
      'intermediate_path': intermediatePath,
      'intermediate_description': intermediateDescription,
      'advanced_path': advancedPath,
      'advanced_description': advancedDescription,
      'cross_section_prerequisites': crossSectionPrerequisites
          .map((e) => e.toJson())
          .toList(),
      'validation_status': validationStatus.toString(),
    };
  }
}

/// 跨章节前置知识点
class CrossSectionPrerequisite {
  final String id;
  final String name;
  final String level;
  final int referenceCount;
  final String reason;

  const CrossSectionPrerequisite({
    required this.id,
    required this.name,
    this.level = '',
    this.referenceCount = 0,
    this.reason = '',
  });

  factory CrossSectionPrerequisite.fromJson(Map<String, dynamic> json) {
    return CrossSectionPrerequisite(
      id: json['id'] as String? ?? '',
      name: json['name'] as String? ?? '',
      level: json['level'] as String? ?? '',
      referenceCount: json['reference_count'] as int? ?? 0,
      reason: json['reason'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'level': level,
      'reference_count': referenceCount,
      'reason': reason,
    };
  }
}

/// 验证状态枚举
enum ValidationStatus {
  /// 未知状态
  unknown,
  /// 验证通过
  valid,
  /// 验证失败
  invalid,
}

/// 辅助函数：将动态值转换为字符串列表
List<String> _toStringList(dynamic value) {
  if (value is List) {
    return value.map((e) => e.toString()).toList();
  }
  return [];
}

/// 辅助函数：将动态值转换为跨章节前置列表
List<CrossSectionPrerequisite> _toCrossSectionList(dynamic value) {
  if (value is List) {
    return value
        .map((e) => CrossSectionPrerequisite.fromJson(e as Map<String, dynamic>))
        .toList();
  }
  return [];
}