/// 练习入口 Model
/// 用于表示某个知识点对应的练习题列表
class PracticeProblem {
  /// 题目引用 ID（如 "cses.range_queries.static_range_sum"）
  final String problemRefId;

  /// 平台（如 "CSES"、"LeetCode"）
  final String platform;

  /// 平台题目 ID
  final String problemId;

  /// 题目标题
  final String title;

  /// 外链 URL
  final String url;

  /// 难度（easy / medium / hard）
  final String difficulty;

  /// 角色（intro / standard / classic / challenge）
  final String role;

  /// 备注
  final String note;

  const PracticeProblem({
    required this.problemRefId,
    required this.platform,
    required this.problemId,
    required this.title,
    required this.url,
    required this.difficulty,
    required this.role,
    required this.note,
  });

  factory PracticeProblem.fromJson(Map<String, dynamic> json) {
    return PracticeProblem(
      problemRefId: json['problem_ref_id'] as String? ?? '',
      platform: json['platform'] as String? ?? '',
      problemId: json['problem_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      url: json['url'] as String? ?? '',
      difficulty: json['difficulty'] as String? ?? '',
      role: json['role'] as String? ?? '',
      note: json['note'] as String? ?? '',
    );
  }

  bool get isValid => title.isNotEmpty && url.isNotEmpty;
}

/// 某个知识点的练习入口
class PracticeEntry {
  /// 知识点 ID（如 "2.4.1"）
  final String itemId;

  /// 知识点标题
  final String title;

  /// 章节 ID
  final String sectionId;

  /// 章节名称
  final String sectionName;

  /// 题目列表
  final List<PracticeProblem> problems;

  const PracticeEntry({
    required this.itemId,
    required this.title,
    required this.sectionId,
    required this.sectionName,
    required this.problems,
  });

  factory PracticeEntry.fromJson(Map<String, dynamic> json) {
    final problemsRaw = json['problems'] as List<dynamic>? ?? [];
    return PracticeEntry(
      itemId: json['item_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      sectionId: json['section_id'] as String? ?? '',
      sectionName: json['section_name'] as String? ?? '',
      problems:
          problemsRaw
              .map((e) => PracticeProblem.fromJson(e as Map<String, dynamic>))
              .where((p) => p.isValid)
              .toList(),
    );
  }

  bool get isValid => itemId.isNotEmpty && problems.isNotEmpty;
}
