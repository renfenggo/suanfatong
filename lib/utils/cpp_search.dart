import '../models/cpp_learning_unit.dart';
import '../models/knowledge_graph.dart';
import '../models/knowledge_category.dart';
import '../models/knowledge_section.dart';

enum CppSearchSource {
  name,
  alias,
  title,
  learningGoal,
  explanation,
  codeNote,
  commonMistake,
  practice,
}

class CppSearchResult {
  final String itemId;
  final String itemName;
  final String sectionId;
  final String sectionName;
  final bool hasUnit;
  final bool isCppItem;
  final String summary;
  final int score;
  final Set<CppSearchSource> sources;

  const CppSearchResult({
    required this.itemId,
    required this.itemName,
    required this.sectionId,
    required this.sectionName,
    required this.hasUnit,
    required this.isCppItem,
    required this.summary,
    required this.score,
    required this.sources,
  });
}

List<CppSearchResult> searchCppUnits(
  String query,
  KnowledgeGraph graph,
  CppLearningContent content,
) {
  if (query.trim().isEmpty) return [];

  final q = query.trim().toLowerCase();

  KnowledgeCategory? cppCategory;
  for (final cat in graph.categories) {
    if (cat.name == 'C++语法') {
      cppCategory = cat;
      break;
    }
  }
  if (cppCategory == null) return [];

  final unitMap = <String, CppLearningUnit>{};
  for (final unit in content.units) {
    unitMap[unit.itemId] = unit;
  }

  final sectionMap = <String, KnowledgeSection>{};
  for (final section in cppCategory.sections) {
    sectionMap[section.id] = section;
  }

  final results = <String, CppSearchResult>{};

  for (final section in cppCategory.sections) {
    for (final item in section.items) {
      final unit = unitMap[item.id];
      int score = 0;
      final sources = <CppSearchSource>{};

      if (item.name.toLowerCase().contains(q)) {
        score += 10;
        sources.add(CppSearchSource.name);
      }

      for (final a in item.alias) {
        if (a.toLowerCase().contains(q)) {
          score += 9;
          sources.add(CppSearchSource.alias);
          break;
        }
      }

      if (unit != null) {
        if (unit.title.toLowerCase().contains(q)) {
          score += 10;
          sources.add(CppSearchSource.title);
        }
        if (unit.learningGoal.toLowerCase().contains(q)) {
          score += 7;
          sources.add(CppSearchSource.learningGoal);
        }
        if (unit.explanation.toLowerCase().contains(q)) {
          score += 3;
          sources.add(CppSearchSource.explanation);
        }
        for (final note in unit.codeNotes) {
          if (note.toLowerCase().contains(q)) {
            score += 3;
            sources.add(CppSearchSource.codeNote);
            break;
          }
        }
        for (final m in unit.commonMistakes) {
          if (m.title.toLowerCase().contains(q) ||
              m.description.toLowerCase().contains(q)) {
            score += 5;
            sources.add(CppSearchSource.commonMistake);
            break;
          }
        }
        if (unit.practice.prompt.toLowerCase().contains(q)) {
          score += 5;
          sources.add(CppSearchSource.practice);
        }
      }

      if (score > 0) {
        String summary;
        if (unit != null && unit.learningGoal.isNotEmpty) {
          summary = unit.learningGoal;
        } else if (unit != null && unit.explanation.isNotEmpty) {
          summary =
              unit.explanation.length > 60
                  ? '${unit.explanation.substring(0, 60)}...'
                  : unit.explanation;
        } else {
          summary = '';
        }

        results[item.id] = CppSearchResult(
          itemId: item.id,
          itemName: item.name,
          sectionId: section.id,
          sectionName: section.name,
          hasUnit: unit != null,
          isCppItem: true,
          summary: summary,
          score: score,
          sources: sources,
        );
      }
    }
  }

  for (final category in graph.categories) {
    if (category.name == 'C++语法') continue;

    for (final section in category.sections) {
      for (final item in section.items) {
        int score = 0;
        final sources = <CppSearchSource>{};

        if (item.name.toLowerCase().contains(q)) {
          score += 10;
          sources.add(CppSearchSource.name);
        }

        for (final a in item.alias) {
          if (a.toLowerCase().contains(q)) {
            score += 9;
            sources.add(CppSearchSource.alias);
            break;
          }
        }

        if (score > 0 && !results.containsKey(item.id)) {
          results[item.id] = CppSearchResult(
            itemId: item.id,
            itemName: item.name,
            sectionId: section.id,
            sectionName: '${category.name} / ${section.name}',
            hasUnit: false,
            isCppItem: false,
            summary: '',
            score: score,
            sources: sources,
          );
        }
      }
    }
  }

  final list = results.values.toList();
  list.sort((a, b) => b.score.compareTo(a.score));
  return list;
}

const kCppSearchSuggestions = [
  'vector',
  'sort',
  'long long',
  'getline',
  '数组越界',
  'priority_queue',
  '= 与 ==',
  'BFS',
  '队列',
];
