class CppCommonMistake {
  final String title;
  final String description;
  final String fix;

  const CppCommonMistake({
    this.title = '',
    this.description = '',
    this.fix = '',
  });

  factory CppCommonMistake.fromJson(Map<String, dynamic> json) {
    return CppCommonMistake(
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      fix: json['fix'] as String? ?? '',
    );
  }
}

class CppPractice {
  final String prompt;
  final String hint;
  final String expectedIdea;

  const CppPractice({this.prompt = '', this.hint = '', this.expectedIdea = ''});

  factory CppPractice.fromJson(Map<String, dynamic> json) {
    return CppPractice(
      prompt: json['prompt'] as String? ?? '',
      hint: json['hint'] as String? ?? '',
      expectedIdea: json['expectedIdea'] as String? ?? '',
    );
  }
}

class CppQuizQuestion {
  final String question;
  final List<String> options;
  final int answerIndex;
  final String explanation;

  const CppQuizQuestion({
    this.question = '',
    this.options = const [],
    this.answerIndex = 0,
    this.explanation = '',
  });

  factory CppQuizQuestion.fromJson(Map<String, dynamic> json) {
    final opts = json['options'];
    return CppQuizQuestion(
      question: json['question'] as String? ?? '',
      options:
          opts is List ? opts.whereType<String>().toList() : const <String>[],
      answerIndex: json['answerIndex'] as int? ?? 0,
      explanation: json['explanation'] as String? ?? '',
    );
  }
}

class CppLearningUnit {
  final String itemId;
  final String title;
  final String learningGoal;
  final String explanation;
  final String exampleCode;
  final List<String> codeNotes;
  final List<CppCommonMistake> commonMistakes;
  final CppPractice practice;
  final List<CppQuizQuestion> quiz;

  const CppLearningUnit({
    required this.itemId,
    this.title = '',
    this.learningGoal = '',
    this.explanation = '',
    this.exampleCode = '',
    this.codeNotes = const [],
    this.commonMistakes = const [],
    this.practice = const CppPractice(),
    this.quiz = const [],
  });

  factory CppLearningUnit.fromJson(Map<String, dynamic> json) {
    return CppLearningUnit(
      itemId: json['itemId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      learningGoal: json['learningGoal'] as String? ?? '',
      explanation: json['explanation'] as String? ?? '',
      exampleCode: json['exampleCode'] as String? ?? '',
      codeNotes:
          (json['codeNotes'] as List?)?.whereType<String>().toList() ??
          const [],
      commonMistakes:
          (json['commonMistakes'] as List?)
              ?.map((e) => CppCommonMistake.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      practice:
          json['practice'] != null
              ? CppPractice.fromJson(json['practice'] as Map<String, dynamic>)
              : const CppPractice(),
      quiz:
          (json['quiz'] as List?)
              ?.map((e) => CppQuizQuestion.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }
}

class CppLearningContent {
  final int version;
  final String category;
  final List<CppLearningUnit> units;

  const CppLearningContent({
    this.version = 1,
    this.category = '',
    this.units = const [],
  });

  factory CppLearningContent.fromJson(Map<String, dynamic> json) {
    return CppLearningContent(
      version: json['version'] as int? ?? 1,
      category: json['category'] as String? ?? '',
      units:
          (json['units'] as List?)
              ?.map((e) => CppLearningUnit.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }

  CppLearningUnit? unitByItemId(String itemId) {
    for (final u in units) {
      if (u.itemId == itemId) return u;
    }
    return null;
  }
}

class CppLearningManifest {
  final int version;
  final String category;
  final String baseFile;
  final List<String> sectionFiles;

  const CppLearningManifest({
    this.version = 1,
    this.category = '',
    this.baseFile = '',
    this.sectionFiles = const [],
  });

  factory CppLearningManifest.fromJson(Map<String, dynamic> json) {
    return CppLearningManifest(
      version: json['version'] as int? ?? 1,
      category: json['category'] as String? ?? '',
      baseFile: json['baseFile'] as String? ?? '',
      sectionFiles:
          (json['sectionFiles'] as List?)?.map((e) => e as String).toList() ??
          const [],
    );
  }
}
