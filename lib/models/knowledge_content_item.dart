/// 知识内容包（knowledge_content 分片）的单条讲解内容模型。
///
/// 数据来源：assets/data/knowledge_content/items/*.json（33 个分片，
/// 覆盖全部 3240 个图谱节点）。解析按“容错优先”：可选字段缺失时给
/// 空默认值；必需字段（item_id/title/short_explanation）缺失时抛
/// [FormatException]，由仓库层跳过坏记录，不阻塞整个分片。
class KnowledgeContentItem {
  final String itemId;
  final String title;
  final String sectionId;
  final String sectionName;
  final String difficulty;
  final String shortExplanation;
  final String learningGoal;
  final String coreIdea;
  final List<String> stepByStep;
  final List<KnowledgeContentMistake> commonMistakes;
  final KnowledgeContentExample? example;
  final List<KnowledgeContentQuizQuestion> quiz;
  final KnowledgeContentAnimationPlan? animationPlan;
  final List<KnowledgeContentPracticeTask> practiceTasks;
  final KnowledgeContentUnlockCheck? unlockCheck;
  final List<String> qualityFlags;

  const KnowledgeContentItem({
    required this.itemId,
    required this.title,
    this.sectionId = '',
    this.sectionName = '',
    this.difficulty = '',
    this.shortExplanation = '',
    this.learningGoal = '',
    this.coreIdea = '',
    this.stepByStep = const [],
    this.commonMistakes = const [],
    this.example,
    this.quiz = const [],
    this.animationPlan,
    this.practiceTasks = const [],
    this.unlockCheck,
    this.qualityFlags = const [],
  });

  factory KnowledgeContentItem.fromJson(Map<String, dynamic> json) {
    final itemId = json['item_id'] as String? ?? '';
    final title = json['title'] as String? ?? '';
    final shortExplanation = json['short_explanation'] as String? ?? '';
    if (itemId.isEmpty || title.isEmpty || shortExplanation.isEmpty) {
      throw FormatException(
        'knowledge_content item 缺少必需字段: item_id=$itemId title=${title.isEmpty ? "(空)" : title}',
      );
    }
    return KnowledgeContentItem(
      itemId: itemId,
      title: title,
      sectionId: json['section_id'] as String? ?? '',
      sectionName: json['section_name'] as String? ?? '',
      difficulty: json['difficulty'] as String? ?? '',
      shortExplanation: shortExplanation,
      learningGoal: json['learning_goal'] as String? ?? '',
      coreIdea: json['core_idea'] as String? ?? '',
      stepByStep: _toStringList(json['step_by_step']),
      commonMistakes:
          _toObjectList(
            json['common_mistakes'],
          ).map(KnowledgeContentMistake.fromJson).toList(),
      example:
          json['example'] == null
              ? null
              : KnowledgeContentExample.fromJson(json['example']),
      quiz:
          _toObjectList(json['quiz'])
              .map(KnowledgeContentQuizQuestion.fromJson)
              .where((q) => q.question.isNotEmpty)
              .toList(),
      animationPlan:
          json['animation_plan'] == null
              ? null
              : KnowledgeContentAnimationPlan.fromJson(json['animation_plan']),
      practiceTasks:
          _toObjectList(
            json['practice_tasks'],
          ).map(KnowledgeContentPracticeTask.fromJson).toList(),
      unlockCheck:
          json['unlock_check'] == null
              ? null
              : KnowledgeContentUnlockCheck.fromJson(json['unlock_check']),
      qualityFlags: _toStringList(json['quality_flags']),
    );
  }
}

class KnowledgeContentMistake {
  final String mistake;
  final String fix;

  const KnowledgeContentMistake({required this.mistake, required this.fix});

  factory KnowledgeContentMistake.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentMistake(
      mistake: json['mistake'] as String? ?? '',
      fix: json['fix'] as String? ?? '',
    );
  }
}

class KnowledgeContentExample {
  final String description;
  final String explanation;
  final String pseudoOrCode;
  final List<String> notes;

  const KnowledgeContentExample({
    this.description = '',
    this.explanation = '',
    this.pseudoOrCode = '',
    this.notes = const [],
  });

  factory KnowledgeContentExample.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentExample(
      description: json['description'] as String? ?? '',
      explanation: json['explanation'] as String? ?? '',
      pseudoOrCode: json['pseudo_or_code'] as String? ?? '',
      notes: _toStringList(json['notes']),
    );
  }
}

class KnowledgeContentQuizQuestion {
  final String type;
  final String question;
  final List<String> options;
  final String answer;
  final String explanation;

  const KnowledgeContentQuizQuestion({
    this.type = '',
    required this.question,
    this.options = const [],
    this.answer = '',
    this.explanation = '',
  });

  factory KnowledgeContentQuizQuestion.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentQuizQuestion(
      type: json['type'] as String? ?? '',
      question: json['question'] as String? ?? '',
      options: _toStringList(json['options']),
      answer: json['answer'] as String? ?? '',
      explanation: json['explanation'] as String? ?? '',
    );
  }
}

class KnowledgeContentAnimationFrame {
  final String title;
  final String description;
  final List<String> visualElements;
  final String highlight;

  const KnowledgeContentAnimationFrame({
    this.title = '',
    this.description = '',
    this.visualElements = const [],
    this.highlight = '',
  });

  factory KnowledgeContentAnimationFrame.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentAnimationFrame(
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      visualElements: _toStringList(json['visual_elements']),
      highlight: json['highlight'] as String? ?? '',
    );
  }
}

class KnowledgeContentAnimationPlan {
  final bool suitable;
  final String type;
  final List<KnowledgeContentAnimationFrame> frames;

  const KnowledgeContentAnimationPlan({
    this.suitable = false,
    this.type = '',
    this.frames = const [],
  });

  factory KnowledgeContentAnimationPlan.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentAnimationPlan(
      suitable: json['suitable'] as bool? ?? false,
      type: json['type'] as String? ?? '',
      frames:
          _toObjectList(
            json['frames'],
          ).map(KnowledgeContentAnimationFrame.fromJson).toList(),
    );
  }
}

class KnowledgeContentPracticeTask {
  final String taskType;
  final String title;
  final String description;
  final String expectedResult;

  const KnowledgeContentPracticeTask({
    this.taskType = '',
    this.title = '',
    this.description = '',
    this.expectedResult = '',
  });

  factory KnowledgeContentPracticeTask.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentPracticeTask(
      taskType: json['task_type'] as String? ?? '',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      expectedResult: json['expected_result'] as String? ?? '',
    );
  }
}

class KnowledgeContentUnlockCheck {
  final String passCondition;
  final String quickQuestion;
  final String expectedAnswer;

  const KnowledgeContentUnlockCheck({
    this.passCondition = '',
    this.quickQuestion = '',
    this.expectedAnswer = '',
  });

  factory KnowledgeContentUnlockCheck.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentUnlockCheck(
      passCondition: json['pass_condition'] as String? ?? '',
      quickQuestion: json['quick_question'] as String? ?? '',
      expectedAnswer: json['expected_answer'] as String? ?? '',
    );
  }
}

List<String> _toStringList(dynamic value) {
  if (value is List) {
    return value.whereType<String>().toList();
  }
  return const [];
}

List<Map<String, dynamic>> _toObjectList(dynamic value) {
  if (value is List) {
    return value.whereType<Map<String, dynamic>>().toList();
  }
  return const [];
}
