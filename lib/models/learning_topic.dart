import 'lesson_set.dart';
import 'quiz_set.dart';
import 'mistake_set.dart';
import 'animation_scenario.dart';

class LearningTopic {
  final String topicId;
  final String title;
  final String subtitle;
  final List<LessonSet> lessonSets;
  final List<QuizSet> quizSets;
  final List<MistakeSet> mistakeSets;
  final List<AnimationScenario> animationScenarios;

  const LearningTopic({
    required this.topicId,
    this.title = '',
    this.subtitle = '',
    this.lessonSets = const [],
    this.quizSets = const [],
    this.mistakeSets = const [],
    this.animationScenarios = const [],
  });

  factory LearningTopic.fromJson(Map<String, dynamic> json) {
    return LearningTopic(
      topicId: json['topicId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      subtitle: json['subtitle'] as String? ?? '',
      lessonSets:
          (json['lessonSets'] as List?)
              ?.map((e) => LessonSet.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      quizSets:
          (json['quizSets'] as List?)
              ?.map(
                (e) => QuizSet.fromJson(
                  e as Map<String, dynamic>,
                  topicId: json['topicId'] as String? ?? '',
                ),
              )
              .toList() ??
          const [],
      mistakeSets:
          (json['mistakeSets'] as List?)
              ?.map((e) => MistakeSet.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      animationScenarios:
          (json['animationScenarios'] as List?)
              ?.map(
                (e) => AnimationScenario.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          const [],
    );
  }

  LessonSet? findLessonSet(String lessonSetId) {
    for (final s in lessonSets) {
      if (s.lessonSetId == lessonSetId) return s;
    }
    return null;
  }

  QuizSet? findQuizSet(String quizSetId) {
    for (final s in quizSets) {
      if (s.quizSetId == quizSetId) return s;
    }
    return null;
  }

  MistakeSet? findMistakeSet(String mistakeSetId) {
    for (final s in mistakeSets) {
      if (s.mistakeSetId == mistakeSetId) return s;
    }
    return null;
  }

  AnimationScenario? findAnimationScenario(String scenarioId) {
    for (final s in animationScenarios) {
      if (s.scenarioId == scenarioId) return s;
    }
    return null;
  }
}
