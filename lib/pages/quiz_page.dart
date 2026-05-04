import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/answer_record.dart';
import '../models/progress.dart';
import '../models/quiz.dart';
import '../state/quiz_set_provider.dart';
import '../state/progress_provider.dart';
import '../state/history_provider.dart';
import '../state/content_manifest_provider.dart';

enum QuizFilter { all, untried, wrong }

class QuizPage extends ConsumerStatefulWidget {
  const QuizPage({super.key});

  @override
  ConsumerState<QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends ConsumerState<QuizPage> {
  int _currentIndex = 0;
  int? _selectedIndex;
  bool _answered = false;
  List<Quiz> _quizzes = [];
  List<Quiz> _filteredQuizzes = [];
  bool _finished = false;
  int _sessionCorrect = 0;
  int _sessionTotal = 0;
  Map<String, int> _localRecords = {};
  QuizFilter _filter = QuizFilter.all;

  @override
  Widget build(BuildContext context) {
    final quizzesAsync = ref
        .watch(defaultContentIdsProvider)
        .when(
          data: (ids) => ref.watch(quizSetProvider(ids.quizSetId)),
          loading: () => const AsyncValue<List<Quiz>>.data([]),
          error: (_, __) => const AsyncValue<List<Quiz>>.data([]),
        );

    return Scaffold(
      appBar: AppBar(title: const Text('选择题训练')),
      body: SafeArea(
        child: quizzesAsync.when(
          data: (quizzes) {
            if (_quizzes.isEmpty) {
              _quizzes = quizzes;
              _loadLocalRecords();
              _applyFilter();
            }
            if (_filteredQuizzes.isEmpty) {
              return _buildEmptyFilter(context);
            }
            if (_finished) {
              return _buildResult(context);
            }
            return _buildQuiz(context);
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (err, _) => Center(
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
                      const Text(
                        '加载题目失败',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFE74C3C),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        err.toString(),
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
        ),
      ),
    );
  }

  void _loadLocalRecords() {
    final progress = ref.read(progressProvider).valueOrNull;
    if (progress != null) {
      _localRecords = Map<String, int>.from(progress.answerRecords);
    }
  }

  void _applyFilter() {
    switch (_filter) {
      case QuizFilter.all:
        _filteredQuizzes = List.of(_quizzes);
        break;
      case QuizFilter.untried:
        _filteredQuizzes =
            _quizzes.where((q) => !_localRecords.containsKey(q.id)).toList();
        break;
      case QuizFilter.wrong:
        _filteredQuizzes =
            _quizzes.where((q) {
              final record = _localRecords[q.id];
              return record != null && record != q.answerIndex;
            }).toList();
        break;
    }
    _currentIndex = 0;
    _selectedIndex = null;
    _answered = false;
    _finished = false;
    _sessionCorrect = 0;
    _sessionTotal = 0;
  }

  Widget _buildEmptyFilter(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.check_circle_outline,
              size: 64,
              color: Color(0xFF4CAF50),
            ),
            const SizedBox(height: 16),
            const Text(
              '暂无符合条件的题目',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(
              _filter == QuizFilter.untried
                  ? '所有题目都已做过，试试筛选「全部」'
                  : '没有做错的题，太棒了！',
              style: const TextStyle(fontSize: 14, color: Color(0xFF888888)),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _filter = QuizFilter.all;
                  _applyFilter();
                });
              },
              child: const Text('显示全部题目'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuiz(BuildContext context) {
    final quiz = _filteredQuizzes[_currentIndex];
    final previousRecord = _localRecords[quiz.id];
    final isCorrect = _selectedIndex == quiz.answerIndex;

    return Column(
      children: [
        _buildTopBar(),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildProgressIndicator(),
                if (previousRecord != null && !_answered) ...[
                  const SizedBox(height: 8),
                  _buildPreviousRecordBadge(previousRecord, quiz),
                ],
                const SizedBox(height: 16),
                _buildQuestionCard(quiz),
                const SizedBox(height: 12),
                ..._buildOptions(quiz),
                if (_answered) ...[
                  const SizedBox(height: 12),
                  _buildFeedback(isCorrect, quiz),
                ],
              ],
            ),
          ),
        ),
        _buildBottomNav(),
      ],
    );
  }

  Widget _buildTopBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: Row(
        children: [
          const Spacer(),
          TextButton.icon(
            onPressed: _showFilterDialog,
            icon: Icon(_filterIcon(), size: 18),
            label: Text(_filterLabel(), style: const TextStyle(fontSize: 13)),
          ),
        ],
      ),
    );
  }

  IconData _filterIcon() {
    switch (_filter) {
      case QuizFilter.all:
        return Icons.list;
      case QuizFilter.untried:
        return Icons.fiber_new;
      case QuizFilter.wrong:
        return Icons.error_outline;
    }
  }

  String _filterLabel() {
    switch (_filter) {
      case QuizFilter.all:
        return '全部';
      case QuizFilter.untried:
        return '未做过';
      case QuizFilter.wrong:
        return '做错的';
    }
  }

  void _showFilterDialog() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder:
          (ctx) => SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '筛选题目',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  _buildFilterOption(
                    ctx,
                    QuizFilter.all,
                    '全部题目',
                    '显示所有 20 道题',
                    Icons.list,
                  ),
                  _buildFilterOption(
                    ctx,
                    QuizFilter.untried,
                    '只做没做过的',
                    '${_quizzes.where((q) => !_localRecords.containsKey(q.id)).length} 道未做过',
                    Icons.fiber_new,
                  ),
                  _buildFilterOption(
                    ctx,
                    QuizFilter.wrong,
                    '只做做错的',
                    '${_quizzes.where((q) {
                      final r = _localRecords[q.id];
                      return r != null && r != q.answerIndex;
                    }).length} 道做错',
                    Icons.error_outline,
                  ),
                ],
              ),
            ),
          ),
    );
  }

  Widget _buildFilterOption(
    BuildContext ctx,
    QuizFilter filter,
    String title,
    String subtitle,
    IconData icon,
  ) {
    final selected = _filter == filter;
    return ListTile(
      leading: Icon(icon, color: selected ? const Color(0xFF4A90D9) : null),
      title: Text(
        title,
        style: TextStyle(
          fontWeight: selected ? FontWeight.bold : FontWeight.normal,
        ),
      ),
      subtitle: Text(subtitle, style: const TextStyle(fontSize: 12)),
      trailing:
          selected ? const Icon(Icons.check, color: Color(0xFF4A90D9)) : null,
      onTap: () {
        Navigator.pop(ctx);
        setState(() {
          _filter = filter;
          _applyFilter();
        });
      },
    );
  }

  Widget _buildPreviousRecordBadge(int previousRecord, Quiz quiz) {
    final wasCorrect = previousRecord == quiz.answerIndex;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: wasCorrect ? const Color(0xFFE8F5E9) : const Color(0xFFFFEBEE),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(
            wasCorrect ? Icons.check_circle : Icons.cancel,
            size: 16,
            color:
                wasCorrect ? const Color(0xFF4CAF50) : const Color(0xFFE74C3C),
          ),
          const SizedBox(width: 6),
          Text(
            wasCorrect ? '上次答对了，再巩固一下' : '上次答错了，这次加油',
            style: TextStyle(
              fontSize: 13,
              color:
                  wasCorrect
                      ? const Color(0xFF2E7D32)
                      : const Color(0xFFC62828),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProgressIndicator() {
    final total = _filteredQuizzes.length;
    final current = _currentIndex + 1;
    final progress = current / total;
    final answered =
        _filteredQuizzes.where((q) => _localRecords.containsKey(q.id)).length;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '第 $current / $total 题',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            Text(
              '本次：$_sessionCorrect/$_sessionTotal',
              style: const TextStyle(
                fontSize: 14,
                color: Color(0xFF4A90D9),
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: LinearProgressIndicator(
            value: progress,
            minHeight: 6,
            backgroundColor: const Color(0xFFE0E0E0),
            valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF4A90D9)),
          ),
        ),
        if (answered > 0)
          Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(
              '已累计作答 $answered/${_quizzes.length} 题',
              style: const TextStyle(fontSize: 12, color: Color(0xFF888888)),
            ),
          ),
      ],
    );
  }

  Widget _buildQuestionCard(Quiz quiz) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Text(
          quiz.question,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            height: 1.6,
          ),
        ),
      ),
    );
  }

  List<Widget> _buildOptions(Quiz quiz) {
    return List.generate(quiz.options.length, (index) {
      final isThis = _selectedIndex == index;
      final isAnswer = index == quiz.answerIndex;

      Color bgColor = const Color(0xFFF8F8F8);
      Color borderColor = const Color(0xFFE0E0E0);
      Color textColor = Colors.black87;
      IconData? trailingIcon;

      if (_answered) {
        if (isAnswer) {
          bgColor = const Color(0xFFE8F5E9);
          borderColor = const Color(0xFF4CAF50);
          textColor = const Color(0xFF2E7D32);
          trailingIcon = Icons.check_circle;
        } else if (isThis && !isAnswer) {
          bgColor = const Color(0xFFFFEBEE);
          borderColor = const Color(0xFFE74C3C);
          textColor = const Color(0xFFC62828);
          trailingIcon = Icons.cancel;
        }
      } else if (isThis) {
        bgColor = const Color(0xFFE3F2FD);
        borderColor = const Color(0xFF4A90D9);
        textColor = const Color(0xFF4A90D9);
      }

      return Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: InkWell(
          onTap: _answered ? null : () => _onOptionTap(index),
          borderRadius: BorderRadius.circular(12),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            decoration: BoxDecoration(
              color: bgColor,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: borderColor, width: 1.5),
            ),
            child: Row(
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color:
                        _answered
                            ? (isAnswer
                                ? const Color(0xFF4CAF50)
                                : (isThis
                                    ? const Color(0xFFE74C3C)
                                    : const Color(0xFFBDBDBD)))
                            : (isThis
                                ? const Color(0xFF4A90D9)
                                : const Color(0xFFBDBDBD)),
                  ),
                  child: Center(
                    child:
                        trailingIcon != null
                            ? Icon(trailingIcon, color: Colors.white, size: 18)
                            : Text(
                              String.fromCharCode(65 + index),
                              style: TextStyle(
                                color:
                                    _answered && !isAnswer && !isThis
                                        ? const Color(0xFF757575)
                                        : Colors.white,
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    quiz.options[index],
                    style: TextStyle(
                      fontSize: 16,
                      color: textColor,
                      height: 1.4,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    });
  }

  Widget _buildFeedback(bool isCorrect, Quiz quiz) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isCorrect ? const Color(0xFFE8F5E9) : const Color(0xFFFFEBEE),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isCorrect ? const Color(0xFFA5D6A7) : const Color(0xFFEF9A9A),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                isCorrect ? Icons.check_circle : Icons.cancel,
                color:
                    isCorrect
                        ? const Color(0xFF4CAF50)
                        : const Color(0xFFE74C3C),
              ),
              const SizedBox(width: 8),
              Text(
                isCorrect ? '回答正确！' : '回答错误',
                style: TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                  color:
                      isCorrect
                          ? const Color(0xFF2E7D32)
                          : const Color(0xFFC62828),
                ),
              ),
            ],
          ),
          if (!isCorrect) ...[
            const SizedBox(height: 8),
            Text(
              '正确答案：${String.fromCharCode(65 + quiz.answerIndex)}. ${quiz.options[quiz.answerIndex]}',
              style: const TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.w600,
                color: Color(0xFF2E7D32),
              ),
            ),
          ],
          if (quiz.explanation.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              quiz.explanation,
              style: TextStyle(
                fontSize: 14,
                height: 1.6,
                color:
                    isCorrect
                        ? const Color(0xFF388E3C)
                        : const Color(0xFFB71C1C),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildBottomNav() {
    final hasPrev = _currentIndex > 0;
    final hasNext = _currentIndex < _filteredQuizzes.length - 1;

    return Container(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Color(0xFFE0E0E0))),
      ),
      child: Row(
        children: [
          Expanded(
            child: OutlinedButton(
              onPressed: hasPrev ? () => _goTo(_currentIndex - 1) : null,
              style: OutlinedButton.styleFrom(
                minimumSize: const Size.fromHeight(46),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text('上一题'),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: ElevatedButton(
              onPressed:
                  !_answered
                      ? null
                      : () {
                        if (hasNext) {
                          _goTo(_currentIndex + 1);
                        } else {
                          _saveAndFinish();
                        }
                      },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4A90D9),
                foregroundColor: Colors.white,
                disabledBackgroundColor: const Color(0xFFBDBDBD),
                minimumSize: const Size.fromHeight(46),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Text(hasNext ? '下一题' : '查看成绩'),
            ),
          ),
        ],
      ),
    );
  }

  void _goTo(int index) {
    setState(() {
      _currentIndex = index;
      _selectedIndex = null;
      _answered = false;
    });
  }

  void _onOptionTap(int index) {
    if (_answered) return;
    final quiz = _filteredQuizzes[_currentIndex];
    final isCorrect = index == quiz.answerIndex;
    final now = DateTime.now();
    final dateStr =
        '${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')} ${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';
    setState(() {
      _selectedIndex = index;
      _answered = true;
      _sessionTotal++;
      if (isCorrect) _sessionCorrect++;
    });
    _localRecords[quiz.id] = index;
    final topicId =
        ref.read(defaultContentIdsProvider).valueOrNull?.topicId ?? 'bfs';
    final record = AnswerRecord(
      topic: topicId,
      quizId: quiz.id,
      selectedIndex: index,
      correct: isCorrect,
      date: dateStr,
    );
    ref.read(historyServiceProvider).appendRecord(topicId, record);
    _persistRecords();
  }

  void _saveAndFinish() {
    _persistRecords();
    setState(() => _finished = true);
  }

  void _persistRecords() {
    final progressSvc = ref.read(progressServiceProvider);
    progressSvc
        .loadProgress()
        .then((progress) {
          final updated = progress.copyWith(
            answerRecords: _localRecords,
            totalQuizAttempts: progress.totalQuizAttempts,
          );
          progressSvc
              .saveProgress(updated)
              .then((_) {
                ref.invalidate(progressProvider);
              })
              .catchError((_) {});
        })
        .catchError((_) {
          final fallback = const Progress().copyWith(
            answerRecords: _localRecords,
          );
          progressSvc
              .saveProgress(fallback)
              .then((_) {
                ref.invalidate(progressProvider);
              })
              .catchError((_) {});
        });
  }

  Widget _buildResult(BuildContext context) {
    final total = _sessionTotal;
    if (total == 0) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              '没有作答任何题目',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 24),
            ElevatedButton(onPressed: _restart, child: const Text('重新开始')),
          ],
        ),
      );
    }
    final percent = (_sessionCorrect * 100 / total).round();
    final isGood = percent >= 80;
    final isOk = percent >= 60;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color:
                    isGood
                        ? const Color(0xFFE8F5E9)
                        : (isOk
                            ? const Color(0xFFFFF8E1)
                            : const Color(0xFFFFEBEE)),
              ),
              child: Center(
                child: FittedBox(
                  child: Text(
                    '$percent',
                    style: TextStyle(
                      fontSize: 42,
                      fontWeight: FontWeight.bold,
                      color:
                          isGood
                              ? const Color(0xFF4CAF50)
                              : (isOk
                                  ? const Color(0xFFFFA000)
                                  : const Color(0xFFE74C3C)),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              '本轮答对 $_sessionCorrect / $total 题',
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              isGood
                  ? '太棒了！你已经掌握了 BFS 基础知识！'
                  : (isOk ? '不错！再巩固一下就更好了！' : '继续加油！多看看知识点再来挑战吧！'),
              style: TextStyle(
                fontSize: 16,
                color:
                    isGood
                        ? const Color(0xFF4CAF50)
                        : (isOk
                            ? const Color(0xFFFFA000)
                            : const Color(0xFFE74C3C)),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: _restart,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4A90D9),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  '再来一次',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600),
                ),
              ),
            ),
            const SizedBox(height: 12),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('返回首页', style: TextStyle(fontSize: 16)),
            ),
          ],
        ),
      ),
    );
  }

  void _restart() {
    setState(() {
      _applyFilter();
    });
  }
}
