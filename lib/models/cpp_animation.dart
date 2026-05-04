class CppAnimationVariable {
  final String name;
  final String value;
  final String note;

  const CppAnimationVariable({this.name = '', this.value = '', this.note = ''});

  factory CppAnimationVariable.fromJson(Map<String, dynamic> json) {
    return CppAnimationVariable(
      name: json['name'] as String? ?? '',
      value: json['value'] as String? ?? '',
      note: json['note'] as String? ?? '',
    );
  }
}

class CppAnimationContainer {
  final String name;
  final String type;
  final List<String> values;
  final int activeIndex;
  final String note;

  const CppAnimationContainer({
    this.name = '',
    this.type = '',
    this.values = const [],
    this.activeIndex = -1,
    this.note = '',
  });

  factory CppAnimationContainer.fromJson(Map<String, dynamic> json) {
    return CppAnimationContainer(
      name: json['name'] as String? ?? '',
      type: json['type'] as String? ?? '',
      values:
          (json['values'] as List?)?.whereType<String>().toList() ?? const [],
      activeIndex: json['activeIndex'] as int? ?? -1,
      note: json['note'] as String? ?? '',
    );
  }
}

class CppAnimationState {
  final List<CppAnimationVariable> variables;
  final List<CppAnimationContainer> containers;
  final String output;

  const CppAnimationState({
    this.variables = const [],
    this.containers = const [],
    this.output = '',
  });

  factory CppAnimationState.fromJson(Map<String, dynamic> json) {
    return CppAnimationState(
      variables:
          (json['variables'] as List?)
              ?.map(
                (e) => CppAnimationVariable.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          const [],
      containers:
          (json['containers'] as List?)
              ?.map(
                (e) =>
                    CppAnimationContainer.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          const [],
      output: json['output'] as String? ?? '',
    );
  }
}

class CppAnimationStep {
  final int step;
  final String title;
  final String description;
  final String codeLine;
  final List<String> highlights;
  final CppAnimationState state;

  const CppAnimationStep({
    this.step = 0,
    this.title = '',
    this.description = '',
    this.codeLine = '',
    this.highlights = const [],
    required this.state,
  });

  factory CppAnimationStep.fromJson(Map<String, dynamic> json) {
    return CppAnimationStep(
      step: json['step'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      codeLine: json['codeLine'] as String? ?? '',
      highlights:
          (json['highlights'] as List?)?.whereType<String>().toList() ??
          const [],
      state:
          json['state'] != null
              ? CppAnimationState.fromJson(
                json['state'] as Map<String, dynamic>,
              )
              : const CppAnimationState(),
    );
  }
}

class CppAnimation {
  final String animationId;
  final String itemId;
  final String title;
  final String description;
  final CppAnimationState initialState;
  final List<CppAnimationStep> steps;

  const CppAnimation({
    this.animationId = '',
    this.itemId = '',
    this.title = '',
    this.description = '',
    this.initialState = const CppAnimationState(),
    this.steps = const [],
  });

  factory CppAnimation.fromJson(Map<String, dynamic> json) {
    return CppAnimation(
      animationId: json['animationId'] as String? ?? '',
      itemId: json['itemId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      initialState:
          json['initialState'] != null
              ? CppAnimationState.fromJson(
                json['initialState'] as Map<String, dynamic>,
              )
              : const CppAnimationState(),
      steps:
          (json['steps'] as List?)
              ?.map((e) => CppAnimationStep.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }
}

class CppAnimationMeta {
  final String animationId;
  final String itemId;
  final String title;
  final String description;
  final String assetPath;
  final String type;
  final int order;

  const CppAnimationMeta({
    this.animationId = '',
    this.itemId = '',
    this.title = '',
    this.description = '',
    this.assetPath = '',
    this.type = '',
    this.order = 0,
  });

  factory CppAnimationMeta.fromJson(Map<String, dynamic> json) {
    return CppAnimationMeta(
      animationId: json['animationId'] as String? ?? '',
      itemId: json['itemId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      assetPath: json['assetPath'] as String? ?? '',
      type: json['type'] as String? ?? '',
      order: json['order'] as int? ?? 0,
    );
  }
}

class CppAnimationManifest {
  final int version;
  final List<CppAnimationMeta> animations;

  const CppAnimationManifest({this.version = 1, this.animations = const []});

  factory CppAnimationManifest.fromJson(Map<String, dynamic> json) {
    return CppAnimationManifest(
      version: json['version'] as int? ?? 1,
      animations:
          (json['animations'] as List?)
              ?.map((e) => CppAnimationMeta.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );
  }
}
