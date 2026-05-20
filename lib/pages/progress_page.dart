import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/answer_record.dart';
import '../models/progress.dart';
import '../models/quiz.dart';
import '../state/progress_provider.dart';
import '../state/quiz_set_provider.dart';
import '../state/history_provider.dart';
import '../state/content_manifest_provider.dart';
import '../state/knowledge_graph_provider.dart';

class ProgressPage extends ConsumerWidget {
  const ProgressPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progressAsync = ref.watch(progressProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('学习进度')),
      body: SafeArea(
        child: progressAsync.when(
          data: (progress) {
            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildHeader(progress),
                  const SizedBox(height: 16),
                  _buildOverviewCard(context, progress, ref),
                  const SizedBox(height: 12),
                  _buildCppProgressCard(progress),
                  if (_hasBfsProgress(progress)) ...[
                    const SizedBox(height: 12),
                    _buildBfsProgressCard(context, progress, ref),
                  ],
                  const SizedBox(height: 12),
                  _buildRecentLearningCard(progress, ref),
                  _buildHistorySection(context, ref),
                ],
              ),
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (err, _) => Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(
                      Icons.error_outline,
                      size: 56,
                      color: Color(0xFFE74C3C),
                    ),
                    const SizedBox(height: 16),
                    Text('加载失败：$err'),
                  ],
                ),
              ),
        ),
      ),
    );
  }

  bool _hasBfsProgress(Progress progress) {
    return progress.completedLessons.isNotEmpty ||
        progress.completedQuizzes.isNotEmpty ||
        progress.quizScores.isNotEmpty ||
        progress.totalQuizAttempts > 0 ||
        progress.answerRecords.isNotEmpty ||
        progress.answerHistory.isNotEmpty;
  }

  int _totalQuizAttempts(Progress progress) {
    return progress.totalQuizAttempts +
        progress.cppQuizAttempts.values.fold<int>(0, (sum, item) => sum + item);
  }

  Widget _buildHeader(Progress progress) {
    final totalCpp = progress.completedCppItems.length;
    final totalBfs = progress.completedLessons.length;
    final totalQuiz = _totalQuizAttempts(progress);
    final hasBfs = _hasBfsProgress(progress);
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFF2C3E50), Color(0xFF3498DB)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.school, color: Colors.white, size: 36),
          const SizedBox(height: 10),
          const Text(
            '学习进度',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 10,
            runSpacing: 6,
            children: [
              _HeaderChip(label: 'C++ $totalCpp 项', icon: Icons.terminal),
              if (hasBfs)
                _HeaderChip(label: 'BFS $totalBfs 项', icon: Icons.explore),
              _HeaderChip(label: '测验 $totalQuiz 次', icon: Icons.quiz),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildOverviewCard(
    BuildContext context,
    Progress progress,
    WidgetRef ref,
  ) {
    final cppDone = progress.completedCppItems.length;
    final bfsDone = progress.completedLessons.length;
    final bfsQuizzes = progress.completedQuizzes.length;
    final totalWrong = progress.cppWrongQuizIds.length;
    final lastItem = progress.lastKnowledgeItemId;
    final hasBfs = _hasBfsProgress(progress);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.dashboard, color: Color(0xFF2C3E50)),
                SizedBox(width: 8),
                Text(
                  '总览',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                _StatItem(
                  label: 'C++ 已学知识点',
                  value: '$cppDone',
                  color: const Color(0xFF00897B),
                ),
                if (hasBfs)
                  _StatItem(
                    label: 'BFS 已完成课程',
                    value: '$bfsDone',
                    color: const Color(0xFF4A90D9),
                  ),
                if (hasBfs)
                  _StatItem(
                    label: 'BFS 已完成测验',
                    value: '$bfsQuizzes',
                    color: const Color(0xFF9B59B6),
                  ),
                _StatItem(
                  label: 'C++ 错题数',
                  value: '$totalWrong',
                  color: const Color(0xFFE74C3C),
                ),
              ],
            ),
            if (lastItem.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.history, size: 16, color: Color(0xFF888888)),
                  const SizedBox(width: 6),
                  Expanded(
                    child: Text(
                      '最近学习：$lastItem',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF666666),
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildCppProgressCard(Progress progress) {
    final scores = progress.cppQuizScores;
    final attempts = progress.cppQuizAttempts;
    final lastDates = progress.cppQuizLastDates;
    final wrong = progress.cppWrongQuizIds;
    final completed = progress.completedCppItems;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.terminal, color: Color(0xFF00897B)),
                SizedBox(width: 8),
                Text(
                  'C++ 基础',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildStatRow('已完成知识点', '${completed.length} 个'),
            const SizedBox(height: 10),
            _buildStatRow('已测验章节', '${scores.length} 个'),
            const SizedBox(height: 10),
            _buildStatRow('错题数量', '${wrong.length} 道'),
            if (scores.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text(
                '章节测验成绩',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF666666),
                ),
              ),
              const SizedBox(height: 8),
              ...scores.entries.map((entry) {
                final att = attempts[entry.key] ?? 0;
                final lastDate = lastDates[entry.key];
                return Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    children: [
                      SizedBox(
                        width: 48,
                        child: Text(
                          entry.key,
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF00897B),
                          ),
                        ),
                      ),
                      Expanded(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: LinearProgressIndicator(
                            value: (entry.value).clamp(0, 100) / 100,
                            minHeight: 8,
                            backgroundColor: const Color(0xFFE0E0E0),
                            valueColor: AlwaysStoppedAnimation<Color>(
                              entry.value >= 60
                                  ? const Color(0xFF4CAF50)
                                  : const Color(0xFFFF9800),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      SizedBox(
                        width: 150,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              '${entry.value}分 / $att次',
                              style: const TextStyle(
                                fontSize: 12,
                                color: Color(0xFF888888),
                              ),
                            ),
                            Text(
                              lastDate == null || lastDate.isEmpty
                                  ? '做题时间：暂无'
                                  : '做题时间：$lastDate',
                              textAlign: TextAlign.end,
                              style: const TextStyle(
                                fontSize: 10,
                                color: Color(0xFFAAAAAA),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              }),
            ],
            if (wrong.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text(
                '错题列表',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFFE74C3C),
                ),
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                runSpacing: 4,
                children:
                    wrong.take(20).map((id) {
                      return Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 3,
                        ),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFFEBEE),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          id,
                          style: const TextStyle(
                            fontSize: 11,
                            color: Color(0xFFE74C3C),
                          ),
                        ),
                      );
                    }).toList(),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildBfsProgressCard(
    BuildContext context,
    Progress progress,
    WidgetRef ref,
  ) {
    if (!_hasBfsProgress(progress)) {
      return const SizedBox.shrink();
    }

    final quizzesAsync = ref
        .watch(defaultContentIdsProvider)
        .when(
          data: (ids) => ref.watch(quizSetProvider(ids.quizSetId)),
          loading: () => const AsyncValue<List<Quiz>>.data([]),
          error: (_, __) => const AsyncValue<List<Quiz>>.data([]),
        );
    return quizzesAsync.when(
      data: (quizzes) {
        final records = progress.answerRecords;
        final lastDateMap = <String, String>{};
        for (final h in progress.answerHistory.reversed) {
          lastDateMap.putIfAbsent(h.quizId, () => h.date);
        }
        int correct = 0;
        int wrong = 0;
        for (final quiz in quizzes) {
          final record = records[quiz.id];
          if (record != null) {
            if (record == quiz.answerIndex) {
              correct++;
            } else {
              wrong++;
            }
          }
        }
        final tried = records.length;
        final total = quizzes.length;

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.explore, color: Color(0xFF4A90D9)),
                    SizedBox(width: 8),
                    Text(
                      'BFS 专题',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                _buildStatRow('已完成课程', '${progress.completedLessons.length} 个'),
                const SizedBox(height: 10),
                _buildStatRow('已完成测验', '${progress.completedQuizzes.length} 套'),
                const SizedBox(height: 10),
                _buildStatRow(
                  '答题情况',
                  '$tried / $total 题（对 $correct / 错 $wrong）',
                ),
                if (tried > 0) ...[
                  const SizedBox(height: 12),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: LinearProgressIndicator(
                      value: tried / (total > 0 ? total : 1),
                      minHeight: 10,
                      backgroundColor: const Color(0xFFE0E0E0),
                      valueColor: AlwaysStoppedAnimation<Color>(
                        correct >= wrong
                            ? const Color(0xFF4CAF50)
                            : const Color(0xFFFF8C42),
                      ),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '正确率 ${tried > 0 ? (correct * 100 / tried).round() : 0}%',
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color(0xFF888888),
                    ),
                  ),
                ],
                if (wrong > 0) ...[
                  const SizedBox(height: 12),
                  _buildBfsWrongSection(quizzes, records, lastDateMap),
                ],
              ],
            ),
          ),
        );
      },
      loading:
          () => const Card(
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Center(child: CircularProgressIndicator()),
            ),
          ),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  Widget _buildBfsWrongSection(
    List<Quiz> quizzes,
    Map<String, int> records,
    Map<String, String> lastDateMap,
  ) {
    final wrongItems =
        quizzes.where((q) {
          final r = records[q.id];
          return r != null && r != q.answerIndex;
        }).toList();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '做错的题目',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: Color(0xFFE74C3C),
          ),
        ),
        const SizedBox(height: 8),
        ...wrongItems.map((quiz) {
          final date = lastDateMap[quiz.id] ?? '';
          final question =
              quiz.question.length > 20
                  ? '${quiz.question.substring(0, 20)}...'
                  : quiz.question;
          return Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.cancel, size: 16, color: Color(0xFFE74C3C)),
                const SizedBox(width: 6),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${quiz.id}. $question',
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFFE74C3C),
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      if (date.isNotEmpty) ...[
                        const SizedBox(height: 2),
                        Text(
                          '做题时间：$date',
                          style: const TextStyle(
                            fontSize: 10,
                            color: Color(0xFFAAAAAA),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            ),
          );
        }),
      ],
    );
  }

  Widget _buildRecentLearningCard(Progress progress, WidgetRef ref) {
    final graphAsync = ref.watch(knowledgeGraphProvider);
    final lastId = progress.lastKnowledgeItemId;
    if (lastId.isEmpty) return const SizedBox.shrink();

    return graphAsync.when(
      data: (graph) {
        final item = graph.itemById(lastId);
        final name = item != null ? item.name : lastId;
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.history, color: Color(0xFF27AE60)),
                    SizedBox(width: 8),
                    Text(
                      '最近学习',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFF27AE60).withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        lastId,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFF27AE60),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        name,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  Widget _buildHistorySection(BuildContext context, WidgetRef ref) {
    final topicId =
        ref.read(defaultContentIdsProvider).valueOrNull?.topicId ?? 'bfs';
    return FutureBuilder<List<AnswerRecord>>(
      future: ref.read(historyServiceProvider).loadHistory(topicId),
      builder: (context, snapshot) {
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const SizedBox.shrink();
        }
        final history = snapshot.data!.reversed.toList();
        final display = history.take(30).toList();
        return Padding(
          padding: const EdgeInsets.only(top: 12),
          child: _buildHistoryList(display, ref),
        );
      },
    );
  }

  Widget _buildHistoryList(List<AnswerRecord> display, WidgetRef ref) {
    final quizzesAsync = ref
        .watch(defaultContentIdsProvider)
        .when(
          data: (ids) => ref.watch(quizSetProvider(ids.quizSetId)),
          loading: () => const AsyncValue<List<Quiz>>.data([]),
          error: (_, __) => const AsyncValue<List<Quiz>>.data([]),
        );
    return quizzesAsync.when(
      data: (quizzes) {
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.history, color: Color(0xFFFF8C42)),
                    const SizedBox(width: 8),
                    Text(
                      '做题记录（最近 ${display.length} 条）',
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                ...display.map((record) {
                  final quiz =
                      quizzes.where((q) => q.id == record.quizId).firstOrNull;
                  final questionText =
                      quiz != null
                          ? (quiz.question.length > 25
                              ? '${quiz.question.substring(0, 25)}...'
                              : quiz.question)
                          : record.quizId;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(
                          record.correct ? Icons.check_circle : Icons.cancel,
                          size: 18,
                          color:
                              record.correct
                                  ? const Color(0xFF4CAF50)
                                  : const Color(0xFFE74C3C),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                questionText,
                                style: const TextStyle(
                                  fontSize: 13,
                                  height: 1.4,
                                ),
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                              const SizedBox(height: 2),
                              Text(
                                '做题时间：${record.date}',
                                style: const TextStyle(
                                  fontSize: 11,
                                  color: Color(0xFFAAAAAA),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                }),
              ],
            ),
          ),
        );
      },
      loading:
          () => const Card(
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Center(child: CircularProgressIndicator()),
            ),
          ),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  Widget _buildStatRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 15, color: Color(0xFF666666)),
        ),
        Text(
          value,
          style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
        ),
      ],
    );
  }
}

class _HeaderChip extends StatelessWidget {
  final String label;
  final IconData icon;

  const _HeaderChip({required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.2),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: Colors.white, size: 14),
          const SizedBox(width: 4),
          Text(
            label,
            style: const TextStyle(fontSize: 12, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _StatItem({
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            value,
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(fontSize: 12, color: color.withValues(alpha: 0.8)),
          ),
        ],
      ),
    );
  }
}
