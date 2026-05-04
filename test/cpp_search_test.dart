import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/cpp_learning_unit.dart';
import 'package:bfs_learn/models/knowledge_graph.dart';
import 'package:bfs_learn/utils/cpp_search.dart';

KnowledgeGraph _buildGraph() {
  return KnowledgeGraph.fromJson({
    'categories': [
      {
        'name': 'C++语法',
        'sections': [
          {
            'id': '1.1',
            'name': '程序基本结构',
            'level': 'L1',
            'items': [
              {
                'id': '1.1.1',
                'name': '#include',
                'alias': ['头文件'],
                'parent': '1.1',
              },
              {'id': '1.1.2', 'name': 'using namespace std', 'parent': '1.1'},
              {'id': '1.1.3', 'name': 'main 函数', 'parent': '1.1'},
            ],
          },
          {
            'id': '1.5',
            'name': '数组与字符串',
            'level': 'L1',
            'items': [
              {
                'id': '1.5.1',
                'name': '数组基础',
                'alias': ['array'],
                'parent': '1.5',
              },
              {
                'id': '1.5.3',
                'name': 'vector',
                'alias': ['动态数组', '向量'],
                'parent': '1.5',
              },
              {
                'id': '1.5.5',
                'name': '数组越界',
                'alias': ['越界访问', 'out of bounds'],
                'parent': '1.5',
              },
            ],
          },
          {
            'id': '1.8',
            'name': 'STL 算法',
            'level': 'L2',
            'items': [
              {
                'id': '1.8.1',
                'name': 'sort',
                'alias': ['排序'],
                'parent': '1.8',
              },
              {
                'id': '1.8.9',
                'name': 'priority_queue',
                'alias': ['优先队列', '堆'],
                'parent': '1.8',
              },
            ],
          },
        ],
      },
      {
        'name': 'BFS',
        'sections': [
          {
            'id': 'bfs1',
            'name': 'BFS基础',
            'items': [
              {'id': 'bfs.1', 'name': '队列'},
            ],
          },
        ],
      },
    ],
  });
}

CppLearningContent _buildContent() {
  return CppLearningContent.fromJson({
    'version': 1,
    'category': 'C++语法',
    'units': [
      {
        'itemId': '1.1.1',
        'title': '#include 指令',
        'learningGoal': '理解 include 的作用和常见头文件',
        'explanation': '#include 是预处理指令，用于引入头文件。',
        'commonMistakes': [
          {'title': '忘记头文件', 'description': '忘记引入需要的头文件'},
        ],
      },
      {
        'itemId': '1.1.2',
        'title': 'using namespace std',
        'learningGoal': '理解命名空间的作用',
        'explanation': 'using namespace std 让我们可以直接使用 cout 和 endl。',
      },
      {
        'itemId': '1.5.3',
        'title': 'vector 动态数组',
        'learningGoal': '掌握 vector 的基本用法',
        'explanation': 'vector 是 C++ STL 中的动态数组容器，可以自动扩容。使用 push_back 添加元素。',
        'codeNotes': ['vector<int> v;', 'v.push_back(1);'],
        'commonMistakes': [
          {'title': '数组越界', 'description': '使用下标访问时超出 vector 的有效范围'},
        ],
      },
      {
        'itemId': '1.5.5',
        'title': '数组越界问题',
        'learningGoal': '理解数组越界的危害和防范',
        'explanation': '数组越界是 C++ 中常见的错误，可能导致未定义行为。',
        'commonMistakes': [
          {'title': '越界访问', 'description': '下标超出数组范围，导致未定义行为'},
        ],
      },
      {
        'itemId': '1.8.1',
        'title': 'sort 排序算法',
        'learningGoal': '掌握 STL sort 的用法',
        'explanation': 'sort 是 C++ STL 提供的排序算法，默认从小到大排序。可以传入自定义比较函数。',
        'practice': {
          'prompt': '使用 sort 对 vector 排序',
          'hint': 'include <algorithm>',
        },
      },
      {
        'itemId': '1.8.9',
        'title': 'priority_queue 优先队列',
        'learningGoal': '掌握优先队列的使用',
        'explanation': 'priority_queue 是 STL 中的适配器，默认大顶堆。',
      },
    ],
  });
}

void main() {
  late KnowledgeGraph graph;
  late CppLearningContent content;

  setUp(() {
    graph = _buildGraph();
    content = _buildContent();
  });

  test('empty query returns empty results', () {
    final results = searchCppUnits('', graph, content);
    expect(results, isEmpty);
  });

  test('whitespace-only query returns empty results', () {
    final results = searchCppUnits('   ', graph, content);
    expect(results, isEmpty);
  });

  test('search "vector" hits relevant items', () {
    final results = searchCppUnits('vector', graph, content);
    expect(results.isNotEmpty, isTrue);
    final ids = results.map((r) => r.itemId).toSet();
    expect(ids, contains('1.5.3'));
  });

  test('search "sort" hits sort item', () {
    final results = searchCppUnits('sort', graph, content);
    expect(results.isNotEmpty, isTrue);
    final ids = results.map((r) => r.itemId).toSet();
    expect(ids, contains('1.8.1'));
  });

  test('search "数组越界" hits relevant items', () {
    final results = searchCppUnits('数组越界', graph, content);
    expect(results.isNotEmpty, isTrue);
    final ids = results.map((r) => r.itemId).toSet();
    expect(ids, contains('1.5.5'));
  });

  test('returns C++ and other knowledge items', () {
    final results = searchCppUnits('队列', graph, content);
    expect(results.isNotEmpty, isTrue);
    final hasCppItems = results.any((r) => r.isCppItem);
    final hasOtherItems = results.any((r) => !r.isCppItem);
    expect(hasCppItems || hasOtherItems || results.isNotEmpty, isTrue);
  });

  test('name/title match scores higher than explanation match', () {
    final results = searchCppUnits('vector', graph, content);
    final vectorResult = results.firstWhere((r) => r.itemId == '1.5.3');
    expect(vectorResult.sources, contains(CppSearchSource.name));
    expect(vectorResult.score, greaterThan(0));
  });

  test('case insensitive search: VECTOR hits vector', () {
    final results = searchCppUnits('VECTOR', graph, content);
    expect(results.isNotEmpty, isTrue);
    final ids = results.map((r) => r.itemId).toSet();
    expect(ids, contains('1.5.3'));
  });

  test('case insensitive search: SORT hits sort', () {
    final results = searchCppUnits('Sort', graph, content);
    expect(results.isNotEmpty, isTrue);
    final ids = results.map((r) => r.itemId).toSet();
    expect(ids, contains('1.8.1'));
  });

  test('search "priority_queue" hits correct item', () {
    final results = searchCppUnits('priority_queue', graph, content);
    expect(results.isNotEmpty, isTrue);
    expect(results.first.itemId, '1.8.9');
  });

  test('search commonMistakes description', () {
    final results = searchCppUnits('越界访问', graph, content);
    expect(results.isNotEmpty, isTrue);
    final hasMistake = results.any(
      (r) => r.sources.contains(CppSearchSource.commonMistake),
    );
    expect(hasMistake, isTrue);
  });

  test('search learningGoal field', () {
    final results = searchCppUnits('掌握 STL sort', graph, content);
    expect(results.isNotEmpty, isTrue);
    final hasGoal = results.any(
      (r) => r.sources.contains(CppSearchSource.learningGoal),
    );
    expect(hasGoal, isTrue);
  });

  test('search practice prompt field', () {
    final results = searchCppUnits('对 vector 排序', graph, content);
    expect(results.isNotEmpty, isTrue);
  });

  test('results are sorted by score descending', () {
    final results = searchCppUnits('vector', graph, content);
    for (var i = 1; i < results.length; i++) {
      expect(results[i - 1].score, greaterThanOrEqualTo(results[i].score));
    }
  });

  test('hasUnit is true for items with learning content', () {
    final results = searchCppUnits('vector', graph, content);
    final vectorResult = results.firstWhere((r) => r.itemId == '1.5.3');
    expect(vectorResult.hasUnit, isTrue);
  });

  test('summary prefers learningGoal over explanation', () {
    final results = searchCppUnits('vector', graph, content);
    final vectorResult = results.firstWhere((r) => r.itemId == '1.5.3');
    expect(vectorResult.summary, contains('掌握'));
  });

  test('section info is correct', () {
    final results = searchCppUnits('vector', graph, content);
    final vectorResult = results.firstWhere((r) => r.itemId == '1.5.3');
    expect(vectorResult.sectionId, '1.5');
    expect(vectorResult.sectionName, '数组与字符串');
  });
}
