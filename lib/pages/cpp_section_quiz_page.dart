import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/cpp_learning_provider.dart';
import '../state/progress_provider.dart';
import '../models/cpp_learning_unit.dart';
import '../models/cpp_quiz_entry.dart';
import '../models/knowledge_section.dart';

enum _QuizMode { normal, wrongOnly }

class CppSectionQuizPage extends ConsumerStatefulWidget {
  final String sectionId;

  const CppSectionQuizPage({super.key, required this.sectionId});

  @override
  ConsumerState<CppSectionQuizPage> createState() => _CppSectionQuizPageState();
}

class _CppSectionQuizPageState extends ConsumerState<CppSectionQuizPage> {
  int _currentIndex = 0;
  int? _selectedOption;
  bool _answered = false;
  int _correctCount = 0;
  bool _finished = false;
  List<CppQuizEntry> _quizEntries = [];
  _QuizMode _mode = _QuizMode.normal;
  final Set<String> _newWrongIds = {};
  final Set<String> _correctedIds = {};
  bool _resultSaved = false;

  List<CppQuizEntry> _buildEntries(
    KnowledgeSection section,
    CppLearningContent content,
  ) {
    final itemIds = section.items.map((i) => i.id).toSet();
    final units =
        content.units.where((u) => itemIds.contains(u.itemId)).toList();
    final entries = <CppQuizEntry>[];
    for (final unit in units) {
      for (var i = 0; i < unit.quiz.length; i++) {
        entries.add(
          CppQuizEntry(
            sectionId: section.id,
            itemId: unit.itemId,
            quizIndex: i,
            question: unit.quiz[i],
          ),
        );
      }
    }
    return entries;
  }

  List<CppQuizEntry> _filterWrongOnly(
    List<CppQuizEntry> all,
    Set<String> wrongIds,
  ) {
    return all.where((e) => wrongIds.contains(e.wrongId)).toList();
  }

  @override
  Widget build(BuildContext context) {
    final graphAsync = ref.watch(knowledgeGraphProvider);
    final contentAsync = ref.watch(cppLearningContentProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('章节小测')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final section = graph.sectionById(widget.sectionId);
            if (section == null) return _buildSectionNotFound();
            return contentAsync.when(
              data: (content) {
                final allEntries = _buildEntries(section, content);
                if (allEntries.isEmpty) return _buildEmptyState(section);

                if (_quizEntries.isEmpty) {
                  final quizProgress = ref.read(cppQuizProgressProvider);
                  final sectionWrong = _sectionWrongCount(
                    section.id,
                    quizProgress.cppWrongQuizIds,
                  );

                  if (sectionWrong > 0 && _mode == _QuizMode.normal) {
                    return _buildModeChoice(section, allEntries, sectionWrong);
                  }

                  _quizEntries = allEntries;
                  if (_mode == _QuizMode.wrongOnly) {
                    _quizEntries = _filterWrongOnly(
                      allEntries,
                      quizProgress.cppWrongQuizIds,
                    );
                    if (_quizEntries.isEmpty) {
                      return _buildEmptyState(section);
                    }
                  }
                }

                if (_finished) return _buildResult(section);
                return _buildQuizBody(section);
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error:
                  (e, _) => Center(
                    child: Padding(
                      padding: const EdgeInsets.all(32),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.error_outline,
                            size: 56,
                            color: Color(0xFFE74C3C),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            '加载失败',
                            style: const TextStyle(
                              fontSize: 18,
                              color: Color(0xFFE74C3C),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            e.toString(),
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              fontSize: 14,
                              color: Color(0xFF888888),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Text(
                    '加载知识图谱失败：$e',
                    style: const TextStyle(color: Color(0xFF888888)),
                  ),
                ),
              ),
        ),
      ),
    );
  }

  int _sectionWrongCount(String sectionId, Set<String> wrongIds) {
    int count = 0;
    for (final id in wrongIds) {
      if (id.startsWith('$sectionId|')) count++;
    }
    return count;
  }

  Widget _buildModeChoice(
    KnowledgeSection section,
    List<CppQuizEntry> allEntries,
    int wrongCount,
  ) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.quiz_outlined, size: 64, color: Color(0xFF00897B)),
            const SizedBox(height: 20),
            Text(
              section.name,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              '该章节有 $wrongCount 道错题',
              style: const TextStyle(fontSize: 16, color: Color(0xFFE67E22)),
            ),
            const SizedBox(height: 28),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed:
                    () => setState(() {
                      _mode = _QuizMode.normal;
                      _quizEntries = allEntries;
                    }),
                icon: const Icon(Icons.play_arrow),
                label: const Text('开始章节小测'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed:
                    () => setState(() {
                      _mode = _QuizMode.wrongOnly;
                    }),
                icon: const Icon(Icons.error_outline),
                label: Text('只练错题（$wrongCount 题）'),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionNotFound() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.search_off, size: 56, color: Color(0xFF888888)),
          const SizedBox(height: 16),
          const Text('章节不存在', style: TextStyle(fontSize: 18)),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('返回'),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState(KnowledgeSection section) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.quiz_outlined, size: 64, color: Color(0xFFBDBDBD)),
            const SizedBox(height: 20),
            Text(
              section.name,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              _mode == _QuizMode.wrongOnly ? '没有错题，继续保持！' : '该章节暂无小测题目',
              style: const TextStyle(fontSize: 16, color: Color(0xFF888888)),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back),
              label: const Text('返回路径页'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuizBody(KnowledgeSection section) {
    final entry = _quizEntries[_currentIndex];
    final total = _quizEntries.length;

    return Column(
      children: [
        _buildProgressBar(section, total),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildQuestionCard(entry.question),
                const SizedBox(height: 16),
                if (_answered) ...[
                  _buildExplanation(entry.question),
                  const SizedBox(height: 16),
                  _buildNextButton(total),
                ],
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildProgressBar(KnowledgeSection section, int total) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
      decoration: const BoxDecoration(
        color: Color(0xFFE0F2F1),
        border: Border(bottom: BorderSide(color: Color(0xFFB2DFDB), width: 1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  section.name,
                  style: const TextStyle(
                    fontSize: 13,
                    color: Color(0xFF00897B),
                    fontWeight: FontWeight.w600,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              if (_mode == _QuizMode.wrongOnly)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 6,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF3E0),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: const Text(
                    '错题模式',
                    style: TextStyle(
                      fontSize: 11,
                      color: Color(0xFFE67E22),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: (_currentIndex + 1) / total,
                    backgroundColor: const Color(0xFFB2DFDB),
                    valueColor: const AlwaysStoppedAnimation<Color>(
                      Color(0xFF00897B),
                    ),
                    minHeight: 6,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Text(
                '${_currentIndex + 1}/$total',
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF00897B),
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              const Icon(
                Icons.check_circle_outline,
                size: 16,
                color: Color(0xFF4CAF50),
              ),
              const SizedBox(width: 4),
              Text(
                '正确 $_correctCount',
                style: const TextStyle(fontSize: 12, color: Color(0xFF4CAF50)),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionCard(CppQuizQuestion q) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFFE3F2FD),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            q.question,
            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 18),
          ...List.generate(q.options.length, (i) {
            final isCorrect = i == q.answerIndex;
            final isSelected = i == _selectedOption;

            Color bg = Colors.white;
            Color border = const Color(0xFFBDBDBD);
            Color textColor = const Color(0xFF333333);
            IconData? trailingIcon;

            if (_answered && isSelected && isCorrect) {
              bg = const Color(0xFFC8E6C9);
              border = const Color(0xFF4CAF50);
              textColor = const Color(0xFF2E7D32);
              trailingIcon = Icons.check_circle;
            } else if (_answered && isSelected && !isCorrect) {
              bg = const Color(0xFFFFCDD2);
              border = const Color(0xFFE74C3C);
              textColor = const Color(0xFFC62828);
              trailingIcon = Icons.cancel;
            } else if (_answered && isCorrect) {
              bg = const Color(0xFFC8E6C9);
              border = const Color(0xFF4CAF50);
              textColor = const Color(0xFF2E7D32);
              trailingIcon = Icons.check_circle;
            }

            return Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: InkWell(
                onTap: _answered ? null : () => _onOptionSelected(i, isCorrect),
                borderRadius: BorderRadius.circular(12),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: BoxDecoration(
                    color: bg,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: border, width: 1.5),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Text(
                          '${String.fromCharCode(65 + i)}. ${q.options[i]}',
                          style: TextStyle(fontSize: 15, color: textColor),
                        ),
                      ),
                      if (trailingIcon != null)
                        Icon(trailingIcon, color: textColor, size: 20),
                    ],
                  ),
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  void _onOptionSelected(int index, bool isCorrect) {
    final entry = _quizEntries[_currentIndex];
    final wrongId = entry.wrongId;

    setState(() {
      _selectedOption = index;
      _answered = true;
      if (isCorrect) {
        _correctCount++;
        _correctedIds.add(wrongId);
      } else {
        _newWrongIds.add(wrongId);
      }
    });
  }

  Widget _buildExplanation(CppQuizQuestion q) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.lightbulb_outline,
                size: 18,
                color: Color(0xFFE67E22),
              ),
              const SizedBox(width: 6),
              const Text(
                '解析',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFFE67E22),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            q.explanation.isNotEmpty ? q.explanation : '暂无解析',
            style: const TextStyle(fontSize: 14, height: 1.7),
          ),
        ],
      ),
    );
  }

  Widget _buildNextButton(int total) {
    final isLast = _currentIndex >= total - 1;
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: () {
          setState(() {
            if (isLast) {
              _finished = true;
              _saveResult();
            } else {
              _currentIndex++;
              _selectedOption = null;
              _answered = false;
            }
          });
        },
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        child: Text(
          isLast ? '查看成绩' : '下一题',
          style: const TextStyle(fontSize: 16),
        ),
      ),
    );
  }

  void _saveResult() {
    if (_resultSaved) return;
    _resultSaved = true;
    final total = _quizEntries.length;
    final score = total > 0 ? (_correctCount / total * 100).round() : 0;
    ref
        .read(cppQuizProgressProvider.notifier)
        .saveCppSectionQuizResult(
          sectionId: widget.sectionId,
          score: score,
          newWrongIds: _newWrongIds,
          correctedIds: _correctedIds,
        );
  }

  Widget _buildResult(KnowledgeSection section) {
    final total = _quizEntries.length;
    final correct = _correctCount;
    final score = total > 0 ? (correct / total * 100).round() : 0;
    final isGood = correct >= total * 0.6;

    final quizProgress = ref.watch(cppQuizProgressProvider);
    final attempts = quizProgress.cppQuizAttempts[section.id] ?? 1;
    final sectionWrong = _sectionWrongCount(
      section.id,
      quizProgress.cppWrongQuizIds,
    );

    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color:
                    isGood ? const Color(0xFFE8F5E9) : const Color(0xFFFFF3E0),
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Icon(
                  isGood ? Icons.emoji_events : Icons.refresh,
                  size: 50,
                  color:
                      isGood
                          ? const Color(0xFF4CAF50)
                          : const Color(0xFFE67E22),
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              '小测完成！',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              section.name,
              style: const TextStyle(fontSize: 15, color: Color(0xFF888888)),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 28),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color:
                    isGood ? const Color(0xFFE8F5E9) : const Color(0xFFFFF3E0),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _ResultStat(
                        label: '得分',
                        value: '$correct/$total',
                        color:
                            isGood
                                ? const Color(0xFF4CAF50)
                                : const Color(0xFFE67E22),
                      ),
                      _ResultStat(
                        label: '百分制',
                        value: '$score',
                        color:
                            isGood
                                ? const Color(0xFF4CAF50)
                                : const Color(0xFFE67E22),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _ResultStat(
                        label: '累计小测',
                        value: '$attempts 次',
                        color: const Color(0xFF00897B),
                      ),
                      _ResultStat(
                        label: '剩余错题',
                        value: '$sectionWrong 道',
                        color:
                            sectionWrong > 0
                                ? const Color(0xFFE67E22)
                                : const Color(0xFF4CAF50),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    isGood ? '表现不错，继续保持！' : '还需加油，建议复习后重试。',
                    style: TextStyle(
                      fontSize: 15,
                      color:
                          isGood
                              ? const Color(0xFF2E7D32)
                              : const Color(0xFFE67E22),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            if (_newWrongIds.isNotEmpty)
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: () {
                    setState(() {
                      _currentIndex = 0;
                      _selectedOption = null;
                      _answered = false;
                      _correctCount = 0;
                      _finished = false;
                      _newWrongIds.clear();
                      _correctedIds.clear();
                      _resultSaved = false;
                      _mode = _QuizMode.wrongOnly;
                      _quizEntries = _filterWrongOnly(
                        _quizEntries,
                        ref.read(cppQuizProgressProvider).cppWrongQuizIds,
                      );
                    });
                  },
                  icon: const Icon(Icons.error_outline),
                  label: Text('只练本次错题（${_newWrongIds.length} 题）'),
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            if (_newWrongIds.isNotEmpty) const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back),
                label: const Text('返回路径页'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ResultStat extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _ResultStat({
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(fontSize: 13, color: Color(0xFF888888)),
        ),
      ],
    );
  }
}
