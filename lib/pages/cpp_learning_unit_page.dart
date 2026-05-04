import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/cpp_learning_provider.dart';
import '../state/progress_provider.dart';
import '../state/cpp_animation_provider.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_graph.dart';
import '../models/knowledge_category.dart';
import '../models/cpp_learning_unit.dart';

class CppLearningUnitPage extends ConsumerStatefulWidget {
  final String itemId;

  const CppLearningUnitPage({super.key, required this.itemId});

  @override
  ConsumerState<CppLearningUnitPage> createState() =>
      _CppLearningUnitPageState();
}

class _CppLearningUnitPageState extends ConsumerState<CppLearningUnitPage> {
  int _currentQuizIndex = 0;
  int? _selectedOption;
  bool _answered = false;

  @override
  Widget build(BuildContext context) {
    final graphAsync = ref.watch(knowledgeGraphProvider);
    final unitAsync = ref.watch(cppLearningUnitByItemIdProvider(widget.itemId));

    return Scaffold(
      appBar: AppBar(title: const Text('C++ 学习')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final item = graph.itemById(widget.itemId);
            if (item == null) return _buildItemNotFound();
            return unitAsync.when(
              data: (unit) {
                if (unit == null) {
                  return _buildNoContent(item);
                }
                return _buildContent(context, item, unit, graph);
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (_, __) => _buildNoContent(item),
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Text(
                    '加载失败：$e',
                    style: const TextStyle(color: Color(0xFF888888)),
                  ),
                ),
              ),
        ),
      ),
    );
  }

  Widget _buildItemNotFound() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.search_off, size: 56, color: Color(0xFF888888)),
          const SizedBox(height: 16),
          const Text('知识点不存在', style: TextStyle(fontSize: 18)),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('返回'),
          ),
        ],
      ),
    );
  }

  Widget _buildNoContent(KnowledgeItem item) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            item.name,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(
            'ID: ${item.id}',
            style: const TextStyle(fontSize: 13, color: Color(0xFF888888)),
          ),
          const SizedBox(height: 24),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFFFFF8E1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.edit_note, size: 40, color: Color(0xFF9E9E9E)),
                SizedBox(height: 12),
                Text(
                  '该知识点内容正在补充中',
                  style: TextStyle(fontSize: 16, color: Color(0xFF666666)),
                ),
                SizedBox(height: 8),
                Text(
                  '敬请期待！你可以先浏览其他知识点。',
                  style: TextStyle(fontSize: 14, color: Color(0xFF888888)),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContent(
    BuildContext context,
    KnowledgeItem item,
    CppLearningUnit unit,
    KnowledgeGraph graph,
  ) {
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(item, unit),
          const SizedBox(height: 16),
          _buildAnimationEntry(),
          const SizedBox(height: 14),
          if (unit.learningGoal.isNotEmpty) ...[
            _buildSection('学习目标', unit.learningGoal, const Color(0xFF00897B)),
            const SizedBox(height: 14),
          ],
          _buildSection('讲解', unit.explanation, const Color(0xFF333333)),
          const SizedBox(height: 14),
          if (unit.exampleCode.isNotEmpty) ...[
            _buildCodeSection(unit),
            const SizedBox(height: 14),
          ],
          if (unit.codeNotes.isNotEmpty) ...[
            _buildCodeNotes(unit.codeNotes),
            const SizedBox(height: 14),
          ],
          if (unit.commonMistakes.isNotEmpty) ...[
            _buildMistakes(unit.commonMistakes),
            const SizedBox(height: 14),
          ],
          if (unit.practice.prompt.isNotEmpty) ...[
            _buildPractice(unit.practice),
            const SizedBox(height: 14),
          ],
          if (unit.quiz.isNotEmpty) ...[
            _buildQuiz(unit.quiz),
            const SizedBox(height: 14),
          ],
          _buildCompleteButton(),
          const SizedBox(height: 16),
          _buildNextItem(context, item, graph),
        ],
      ),
    );
  }

  Widget _buildAnimationEntry() {
    final animationsAsync = ref.watch(
      cppAnimationsForItemProvider(widget.itemId),
    );
    return animationsAsync.when(
      data: (animations) {
        if (animations.isEmpty) return const SizedBox.shrink();
        final first = animations.first;
        return Card(
          color: const Color(0xFFE0F2F1),
          child: InkWell(
            onTap: () {
              Navigator.pushNamed(
                context,
                '/cpp_animation',
                arguments: first.animationId,
              );
            },
            borderRadius: BorderRadius.circular(16),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: const Color(0xFF00897B).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(
                      Icons.play_circle_fill,
                      color: Color(0xFF00897B),
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '看动画演示',
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF00897B),
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          first.title,
                          style: const TextStyle(
                            fontSize: 12,
                            color: Color(0xFF666666),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right, color: Color(0xFF00897B)),
                ],
              ),
            ),
          ),
        );
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  Widget _buildHeader(KnowledgeItem item, CppLearningUnit unit) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 3,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFF00897B).withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    item.id,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF00897B),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  item.parent,
                  style: const TextStyle(
                    fontSize: 13,
                    color: Color(0xFF888888),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              unit.title.isNotEmpty ? unit.title : item.name,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSection(String label, String content, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFFF5F5F5),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            content,
            style: const TextStyle(fontSize: 15, height: 1.8),
          ),
        ),
      ],
    );
  }

  Widget _buildCodeSection(CppLearningUnit unit) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '示例代码',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00897B),
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: const Color(0xFF1E1E1E),
            borderRadius: BorderRadius.circular(12),
          ),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Text(
              unit.exampleCode,
              style: const TextStyle(
                fontFamily: 'monospace',
                fontSize: 14,
                color: Color(0xFFD4D4D4),
                height: 1.5,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildCodeNotes(List<String> notes) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '代码说明',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00897B),
            ),
          ),
        ),
        ...notes.map(
          (note) => Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '• ',
                  style: TextStyle(
                    fontSize: 15,
                    color: Color(0xFF00897B),
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Expanded(
                  child: Text(
                    note,
                    style: const TextStyle(fontSize: 14, height: 1.5),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMistakes(List<CppCommonMistake> mistakes) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '常见错误',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFFE74C3C),
            ),
          ),
        ),
        ...mistakes.map(
          (m) => Container(
            width: double.infinity,
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFFFFEBEE),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: const Color(0xFFFFCDD2)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  m.title,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFFE74C3C),
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  m.description,
                  style: const TextStyle(fontSize: 14, height: 1.6),
                ),
                const SizedBox(height: 6),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE8F5E9),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '✓ ',
                        style: TextStyle(
                          color: Color(0xFF4CAF50),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Expanded(
                        child: Text(
                          m.fix,
                          style: const TextStyle(
                            fontSize: 14,
                            color: Color(0xFF2E7D32),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPractice(CppPractice practice) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '动手练习',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFFE67E22),
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFFFFF3E0),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                practice.prompt,
                style: const TextStyle(fontSize: 15, height: 1.7),
              ),
              const SizedBox(height: 10),
              ExpansionTile(
                tilePadding: EdgeInsets.zero,
                childrenPadding: const EdgeInsets.only(top: 8),
                title: const Text(
                  '查看提示',
                  style: TextStyle(fontSize: 14, color: Color(0xFFE67E22)),
                ),
                children: [
                  Text(
                    practice.hint,
                    style: const TextStyle(fontSize: 14, height: 1.6),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildQuiz(List<CppQuizQuestion> quiz) {
    if (_currentQuizIndex >= quiz.length) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: const Color(0xFFE8F5E9),
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Column(
          children: [
            Icon(Icons.check_circle, color: Color(0xFF4CAF50), size: 40),
            SizedBox(height: 8),
            Text(
              '小测完成！',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4CAF50),
              ),
            ),
          ],
        ),
      );
    }

    final q = quiz[_currentQuizIndex];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '小测（${_currentQuizIndex + 1}/${quiz.length}）',
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF3498DB),
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFFE3F2FD),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                q.question,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 14),
              ...List.generate(q.options.length, (i) {
                final isCorrect = i == q.answerIndex;
                final isSelected = i == _selectedOption;
                Color bg = Colors.white;
                Color border = const Color(0xFFBDBDBD);
                Color text = const Color(0xFF333333);

                if (_answered && isSelected && isCorrect) {
                  bg = const Color(0xFFC8E6C9);
                  border = const Color(0xFF4CAF50);
                  text = const Color(0xFF2E7D32);
                } else if (_answered && isSelected && !isCorrect) {
                  bg = const Color(0xFFFFCDD2);
                  border = const Color(0xFFE74C3C);
                  text = const Color(0xFFC62828);
                } else if (_answered && isCorrect) {
                  bg = const Color(0xFFC8E6C9);
                  border = const Color(0xFF4CAF50);
                  text = const Color(0xFF2E7D32);
                }

                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    onTap:
                        _answered
                            ? null
                            : () => setState(() {
                              _selectedOption = i;
                              _answered = true;
                            }),
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: bg,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: border),
                      ),
                      child: Text(
                        '${String.fromCharCode(65 + i)}. ${q.options[i]}',
                        style: TextStyle(fontSize: 15, color: text),
                      ),
                    ),
                  ),
                );
              }),
              if (_answered) ...[
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF5F5F5),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    q.explanation,
                    style: const TextStyle(fontSize: 14, height: 1.6),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      setState(() {
                        _currentQuizIndex++;
                        _selectedOption = null;
                        _answered = false;
                      });
                    },
                    child: Text(
                      _currentQuizIndex < quiz.length - 1 ? '下一题' : '完成',
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCompleteButton() {
    final completed = ref.watch(cppProgressProvider).contains(widget.itemId);
    if (completed) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFFE8F5E9),
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.check_circle, color: Color(0xFF4CAF50)),
            SizedBox(width: 8),
            Text(
              '已完成',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: Color(0xFF4CAF50),
              ),
            ),
          ],
        ),
      );
    }

    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed:
            () => ref
                .read(cppProgressProvider.notifier)
                .markCompleted(widget.itemId),
        icon: const Icon(Icons.check),
        label: const Text('标记已学完'),
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 14),
          backgroundColor: const Color(0xFF00897B),
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
    );
  }

  Widget _buildNextItem(
    BuildContext context,
    KnowledgeItem item,
    KnowledgeGraph graph,
  ) {
    final completedItems = ref.watch(cppProgressProvider);
    final nextItem = _findNextItem(item, graph, completedItems);

    if (nextItem == null) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFFF5F5F5),
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Text(
          '恭喜！已到达当前可学的最后一个知识点',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 14, color: Color(0xFF888888)),
        ),
      );
    }

    final nextSection = graph.sectionById(nextItem.parent);
    final isSameSection = nextItem.parent == item.parent;
    final subtitle =
        isSameSection
            ? '下一个知识点'
            : '下一章节：${nextSection?.name ?? nextItem.parent}';

    return Card(
      color: const Color(0xFFE0F2F1),
      child: InkWell(
        onTap: () {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => CppLearningUnitPage(itemId: nextItem.id),
              settings: RouteSettings(
                name: '/cpp_learning_unit',
                arguments: nextItem.id,
              ),
            ),
          );
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              const Icon(Icons.arrow_forward, color: Color(0xFF00897B)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 12,
                        color: Color(0xFF00897B),
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      nextItem.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF00897B),
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: Color(0xFF00897B)),
            ],
          ),
        ),
      ),
    );
  }

  KnowledgeItem? _findNextItem(
    KnowledgeItem current,
    KnowledgeGraph graph,
    Set<String> completed,
  ) {
    final section = graph.sectionById(current.parent);
    if (section != null) {
      final items = section.items;
      final idx = items.indexWhere((i) => i.id == current.id);
      if (idx >= 0 && idx < items.length - 1) {
        return items[idx + 1];
      }
    }

    KnowledgeCategory? cppCategory;
    for (final cat in graph.categories) {
      if (cat.name == 'C++语法') {
        cppCategory = cat;
        break;
      }
    }
    if (cppCategory == null) return null;

    final allDone = {...completed, current.id};
    final currentSectionIdx = cppCategory.sections.indexWhere(
      (s) => s.id == current.parent,
    );

    for (
      int si = currentSectionIdx + 1;
      si < cppCategory.sections.length;
      si++
    ) {
      for (final candidate in cppCategory.sections[si].items) {
        if (allDone.containsAll(candidate.resolvedPre)) {
          return candidate;
        }
      }
    }

    return null;
  }
}
