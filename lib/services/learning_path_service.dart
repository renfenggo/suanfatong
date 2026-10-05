import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/learning_path.dart';

/// 章节学习路径服务
///
/// 负责加载和管理章节学习路径数据，提供查询和安全降级功能
class LearningPathService {
  // JSON数据路径
  static const String _dataPath = 'data/learning_path_report_data.json';

  // 缓存学习路径数据
  Map<String, LearningPath>? _learningPathsCache;

  // 加载状态
  bool _isLoading = false;
  String? _loadError;

  /// 获取加载状态
  bool get isLoading => _isLoading;

  /// 获取加载错误信息
  String? get loadError => _loadError;

  /// 加载学习路径数据
  ///
  /// 返回所有可用的学习路径，如果加载失败则返回空Map
  Future<Map<String, LearningPath>> loadLearningPaths() async {
    // 如果已经加载，直接返回缓存
    if (_learningPathsCache != null) {
      return _learningPathsCache!;
    }

    _isLoading = true;
    _loadError = null;

    try {
      // 加载JSON数据
      final jsonStr = await rootBundle.loadString(_dataPath);
      final Map<String, dynamic> jsonData = json.decode(jsonStr);

      // 解析学习路径数据
      _learningPathsCache = _parseLearningPaths(jsonData);
      _isLoading = false;

      return _learningPathsCache!;
    } catch (e) {
      _isLoading = false;
      _loadError = 'Failed to load learning paths: $e';

      // 返回空Map进行安全降级
      return {};
    }
  }

  /// 解析学习路径数据
  Map<String, LearningPath> _parseLearningPaths(Map<String, dynamic> jsonData) {
    final Map<String, LearningPath> paths = {};

    // 尝试从不同的字段结构中解析学习路径
    // 优先使用真实的 sample_paths 字段
    if (jsonData.containsKey('sample_paths')) {
      final samplePaths = jsonData['sample_paths'] as Map<String, dynamic>;
      samplePaths.forEach((sectionId, pathData) {
        try {
          final learningPath = LearningPath.fromJson(
            pathData as Map<String, dynamic>,
            sectionId: sectionId, // 注入外层的sectionId作为参数
          );
          paths[sectionId] = learningPath;
        } catch (e) {
          _loadError = 'Failed to parse learning path for $sectionId: $e';
        }
      });
    }
    // 兼容旧的 sample_learning_paths 字段
    else if (jsonData.containsKey('sample_learning_paths')) {
      final samplePaths =
          jsonData['sample_learning_paths'] as Map<String, dynamic>;
      samplePaths.forEach((sectionId, pathData) {
        try {
          final learningPath = LearningPath.fromJson(
            pathData as Map<String, dynamic>,
            sectionId: sectionId, // 注入外层的sectionId作为参数
          );
          paths[sectionId] = learningPath;
        } catch (e) {
          _loadError = 'Failed to parse learning path for $sectionId: $e';
        }
      });
    }

    return paths;
  }

  /// 按章节ID查询学习路径
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回对应的学习路径，如果不存在则返回null
  Future<LearningPath?> getLearningPathBySectionId(String sectionId) async {
    final paths = await loadLearningPaths();
    return paths[sectionId];
  }

  /// 判断某章节是否有学习路径数据
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回true表示有路径数据，false表示没有
  Future<bool> hasLearningPath(String sectionId) async {
    final path = await getLearningPathBySectionId(sectionId);
    return path != null && path.hasPathData();
  }

  /// 获取入门路径
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回入门路径的知识点ID列表，如果不存在则返回空列表
  Future<List<String>> getBeginnerPath(String sectionId) async {
    final path = await getLearningPathBySectionId(sectionId);
    return path?.beginnerPath ?? [];
  }

  /// 获取提高路径
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回提高路径的知识点ID列表，如果不存在则返回空列表
  Future<List<String>> getIntermediatePath(String sectionId) async {
    final path = await getLearningPathBySectionId(sectionId);
    return path?.intermediatePath ?? [];
  }

  /// 获取冲刺路径
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回冲刺路径的知识点ID列表，如果不存在则返回空列表
  Future<List<String>> getAdvancedPath(String sectionId) async {
    final path = await getLearningPathBySectionId(sectionId);
    return path?.advancedPath ?? [];
  }

  /// 获取跨章节前置
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回跨章节前置知识点列表，如果不存在则返回空列表
  Future<List<CrossSectionPrerequisite>> getCrossSectionPrerequisites(
    String sectionId,
  ) async {
    final path = await getLearningPathBySectionId(sectionId);
    return path?.crossSectionPrerequisites ?? [];
  }

  /// 获取所有可用章节的学习路径统计
  ///
  /// 返回Map，key为章节ID，value为该章节的路径统计信息
  Future<Map<String, Map<String, int>>> getAllPathStatistics() async {
    final paths = await loadLearningPaths();
    final Map<String, Map<String, int>> statistics = {};

    paths.forEach((sectionId, path) {
      statistics[sectionId] = path.getPathStatistics();
    });

    return statistics;
  }

  /// 获取路径描述
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// [pathType] 路径类型: 'beginner', 'intermediate', 'advanced'
  /// 返回对应的路径描述，如果不存在则返回空字符串
  Future<String> getPathDescription(String sectionId, String pathType) async {
    final path = await getLearningPathBySectionId(sectionId);
    if (path == null) return '';

    switch (pathType.toLowerCase()) {
      case 'beginner':
        return path.beginnerDescription;
      case 'intermediate':
        return path.intermediateDescription;
      case 'advanced':
        return path.advancedDescription;
      default:
        return '';
    }
  }

  /// 检查章节ID是否在当前数据中
  ///
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回true表示数据中存在该章节，false表示不存在
  Future<bool> sectionExists(String sectionId) async {
    final paths = await loadLearningPaths();
    return paths.containsKey(sectionId);
  }

  /// 获取所有可用章节ID列表
  ///
  /// 返回所有有学习路径数据的章节ID列表
  Future<List<String>> getAvailableSectionIds() async {
    final paths = await loadLearningPaths();
    return paths.keys.toList();
  }

  /// 清除缓存，强制重新加载数据
  void clearCache() {
    _learningPathsCache = null;
    _loadError = null;
    _isLoading = false;
  }

  /// 验证路径数据的完整性
  ///
  /// 检查路径是否包含正确的章节内节点，无跨章节混入
  /// [sectionId] 章节ID，如 "2.8"
  /// 返回验证结果，包含是否通过和详细信息
  Future<Map<String, dynamic>> validatePathIntegrity(String sectionId) async {
    final path = await getLearningPathBySectionId(sectionId);

    if (path == null) {
      return {
        'valid': false,
        'error': 'Section not found',
        'sectionId': sectionId,
      };
    }

    final sectionPrefix = sectionId.split('.')[0];
    final issues = <String>[];

    // 检查入门路径
    for (final itemId in path.beginnerPath) {
      if (!itemId.startsWith('$sectionPrefix.')) {
        issues.add('Beginner path contains cross-section node: $itemId');
      }
    }

    // 检查提高路径
    for (final itemId in path.intermediatePath) {
      if (!itemId.startsWith('$sectionPrefix.')) {
        issues.add('Intermediate path contains cross-section node: $itemId');
      }
    }

    // 检查冲刺路径
    for (final itemId in path.advancedPath) {
      if (!itemId.startsWith('$sectionPrefix.')) {
        issues.add('Advanced path contains cross-section node: $itemId');
      }
    }

    return {
      'valid': issues.isEmpty,
      'sectionId': sectionId,
      'sectionName': path.sectionName,
      'issues': issues,
      'statistics': path.getPathStatistics(),
    };
  }

  /// 获取验证摘要信息
  ///
  /// 返回所有章节的验证状态摘要
  Future<Map<String, dynamic>> getValidationSummary() async {
    final paths = await loadLearningPaths();
    final Map<String, dynamic> summary = {
      'totalSections': paths.length,
      'validSections': 0,
      'invalidSections': 0,
      'sectionDetails': <String, Map<String, dynamic>>{},
    };

    for (final sectionId in paths.keys) {
      final validation = await validatePathIntegrity(sectionId);
      if (validation['valid'] as bool) {
        summary['validSections'] = (summary['validSections'] as int) + 1;
      } else {
        summary['invalidSections'] = (summary['invalidSections'] as int) + 1;
      }
      (summary['sectionDetails'] as Map<String, dynamic>)[sectionId] =
          validation;
    }

    return summary;
  }
}
