import 'cpp_learning_unit.dart';

class CppQuizEntry {
  final String sectionId;
  final String itemId;
  final int quizIndex;
  final CppQuizQuestion question;

  const CppQuizEntry({
    required this.sectionId,
    required this.itemId,
    required this.quizIndex,
    required this.question,
  });

  String get wrongId => '$sectionId|$itemId|$quizIndex';
}
