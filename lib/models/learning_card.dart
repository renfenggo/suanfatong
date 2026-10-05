/// 学习卡片 Model
/// 用于表示一个知识点的学习卡片，包含通俗易懂的教学内容
class LearningCard {
  /// 知识点唯一标识（如 "2.8.208"）
  final String id;

  /// 知识点标题（如 "后缀最值 DP"）
  final String title;

  /// 知识点所属章节ID（如 "2.8"）
  final String sectionId;

  /// 一句话通俗解释（摘要）
  final String summary;

  /// 应用场景（什么时候用）
  final String useCases;

  /// 核心直觉/核心思想
  final String intuition;

  /// 最小例子
  final String example;

  /// 常见坑/易错点列表
  final List<String> traps;

  /// 练习入口/练习建议
  final String practice;

  /// 后续学习节点列表
  final List<String> nextItems;

  /// 必须前置知识列表（每个元素包含 id 和 name）
  final List<Map<String, String>> requiredPre;

  /// 推荐前置知识列表（每个元素包含 id 和 name）
  final List<Map<String, String>> recommendedPre;

  /// 学习动作类型（read / trace / code / prove / solve / compare）
  final String actionType;

  /// 构造函数
  LearningCard({
    required this.id,
    required this.title,
    required this.sectionId,
    required this.summary,
    required this.useCases,
    required this.intuition,
    required this.example,
    required this.traps,
    required this.practice,
    required this.nextItems,
    this.requiredPre = const [],
    this.recommendedPre = const [],
    required this.actionType,
  });

  /// 从 JSON Map 创建 LearningCard
  /// 字段映射：
  /// - item_id -> id
  /// - item_name -> title
  /// - section -> sectionId
  /// - one_sentence_explanation -> summary
  /// - when_to_use -> useCases
  /// - core_intuition -> intuition
  /// - minimal_example -> example
  /// - common_traps -> traps
  /// - practice_entry -> practice
  /// - learn_next -> nextItems
  /// - must_know_before -> requiredPre
  /// - nice_to_know -> recommendedPre
  /// - learning_action -> actionType
  factory LearningCard.fromJson(Map<String, dynamic> json) {
    return LearningCard(
      id: json['item_id'] as String? ?? '',
      title: json['item_name'] as String? ?? '',
      sectionId: json['section'] as String? ?? '',
      summary: json['one_sentence_explanation'] as String? ?? '',
      useCases: json['when_to_use'] as String? ?? '',
      intuition: json['core_intuition'] as String? ?? '',
      example: json['minimal_example'] as String? ?? '',
      traps: _parseStringList(json['common_traps']),
      practice: json['practice_entry'] as String? ?? '',
      nextItems: _parseStringList(json['learn_next']),
      requiredPre: _parsePreList(json['must_know_before']),
      recommendedPre: _parsePreList(json['nice_to_know']),
      actionType: json['learning_action'] as String? ?? 'read',
    );
  }

  /// 解析 String List，处理 null 和类型错误
  static List<String> _parseStringList(dynamic value) {
    if (value == null) return [];
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return [];
  }

  /// 解析前置知识 List，每个元素是 `Map<String, String>`
  static List<Map<String, String>> _parsePreList(dynamic value) {
    if (value == null) return [];
    if (value is List) {
      return value.map((e) {
        if (e is Map) {
          return Map<String, String>.from(e);
        }
        return <String, String>{};
      }).toList();
    }
    return [];
  }

  /// 转换为 JSON Map
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'sectionId': sectionId,
      'summary': summary,
      'useCases': useCases,
      'intuition': intuition,
      'example': example,
      'traps': traps,
      'practice': practice,
      'nextItems': nextItems,
      'requiredPre': requiredPre,
      'recommendedPre': recommendedPre,
      'actionType': actionType,
    };
  }

  /// 判断是否为有效的学习卡片（关键字段非空）
  bool isValid() {
    return id.isNotEmpty && title.isNotEmpty && sectionId.isNotEmpty;
  }

  /// 判断是否为完整的学习卡片（所有必填字段非空）
  bool isComplete() {
    return isValid() &&
        summary.isNotEmpty &&
        useCases.isNotEmpty &&
        intuition.isNotEmpty &&
        example.isNotEmpty &&
        traps.isNotEmpty &&
        practice.isNotEmpty &&
        nextItems.isNotEmpty &&
        actionType.isNotEmpty;
  }

  /// 获取学习动作的中文描述
  String getActionTypeDescription() {
    switch (actionType) {
      case 'read':
        return '阅读理解';
      case 'trace':
        return '手动推导';
      case 'code':
        return '编写代码';
      case 'prove':
        return '数学证明';
      case 'solve':
        return '解决问题';
      case 'compare':
        return '对比理解';
      default:
        return '阅读理解';
    }
  }

  /// 复制并修改部分字段
  LearningCard copyWith({
    String? id,
    String? title,
    String? sectionId,
    String? summary,
    String? useCases,
    String? intuition,
    String? example,
    List<String>? traps,
    String? practice,
    List<String>? nextItems,
    List<Map<String, String>>? requiredPre,
    List<Map<String, String>>? recommendedPre,
    String? actionType,
  }) {
    return LearningCard(
      id: id ?? this.id,
      title: title ?? this.title,
      sectionId: sectionId ?? this.sectionId,
      summary: summary ?? this.summary,
      useCases: useCases ?? this.useCases,
      intuition: intuition ?? this.intuition,
      example: example ?? this.example,
      traps: traps ?? this.traps,
      practice: practice ?? this.practice,
      nextItems: nextItems ?? this.nextItems,
      requiredPre: requiredPre ?? this.requiredPre,
      recommendedPre: recommendedPre ?? this.recommendedPre,
      actionType: actionType ?? this.actionType,
    );
  }

  @override
  String toString() {
    return 'LearningCard(id: $id, title: $title, sectionId: $sectionId, actionType: $actionType)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is LearningCard && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
