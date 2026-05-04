import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/answer_record.dart';
import '../models/progress.dart';
import '../models/quiz.dart';
import '../state/progress_provider.dart';
import '../state/quiz_set_provider.dart';
import '../state/history_provider.dart';
import '../state/content_manifest_provider.dart';

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
                  _buildHeader(),
                  const SizedBox(height: 20),
                  _buildAnswerOverview(context, progress, ref),
                  const SizedBox(height: 16),
                  _buildStatsCard(progress),
                  if (progress.answerRecords.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _buildAnswerDetailCard(context, progress, ref),
                  ],
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

  Widget _buildHeader() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFF4A90D9), Color(0xFF357ABD)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.school, color: Colors.white, size: 36),
          SizedBox(height: 10),
          Text(
            'BFS 学习进度',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          SizedBox(height: 4),
          Text(
            '坚持学习，每天进步一点点！',
            style: TextStyle(fontSize: 14, color: Color(0xFFD4E6F9)),
          ),
        ],
      ),
    );
  }

  Widget _buildAnswerOverview(
    BuildContext context,
    Progress progress,
    WidgetRef ref,
  ) {
    final quizzesAsync = ref
        .watch(defaultContentIdsProvider)
        .when(
          data: (ids) => ref.watch(quizSetProvider(ids.quizSetId)),
          loading: () => const AsyncValue<List<Quiz>>.data([]),
          error: (_, __) => const AsyncValue<List<Quiz>>.data([]),
        );
    return quizzesAsync.when(
      data: (quizzes) {
        final total = quizzes.length;
        final tried = progress.answerRecords.length;
        int correct = 0;
        int wrong = 0;
        for (final quiz in quizzes) {
          final record = progress.answerRecords[quiz.id];
          if (record != null) {
            if (record == quiz.answerIndex) {
              correct++;
            } else {
              wrong++;
            }
          }
        }
        final untried = total - tried;

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.quiz, color: Color(0xFFFF8C42)),
                    SizedBox(width: 8),
                    Text(
                      '答题概况',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    _buildStatCircle('$total', '总题数', const Color(0xFF4A90D9)),
                    const SizedBox(width: 12),
                    _buildStatCircle(
                      '$correct',
                      '已做对',
                      const Color(0xFF4CAF50),
                    ),
                    const SizedBox(width: 12),
                    _buildStatCircle('$wrong', '做错了', const Color(0xFFE74C3C)),
                    const SizedBox(width: 12),
                    _buildStatCircle(
                      '$untried',
                      '未做过',
                      const Color(0xFFBDBDBD),
                    ),
                  ],
                ),
                if (tried > 0) ...[
                  const SizedBox(height: 16),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: LinearProgressIndicator(
                      value: tried / total,
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
                    '完成进度：$tried / $total 题（正确率 ${tried > 0 ? (correct * 100 / tried).round() : 0}%）',
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color(0xFF888888),
                    ),
                  ),
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

  Widget _buildStatCircle(String value, String label, Color color) {
    return Expanded(
      child: Column(
        children: [
          Container(
            width: 52,
            height: 52,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: color.withValues(alpha: 0.12),
            ),
            child: Center(
              child: FittedBox(
                child: Text(
                  value,
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 6),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatsCard(Progress progress) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.bar_chart, color: Color(0xFF1ABC9C)),
                SizedBox(width: 8),
                Text(
                  '学习统计',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildStatRow('已完成测验', '${progress.completedQuizzes.length} 套'),
            const SizedBox(height: 12),
            _buildStatRow('已学知识点', '${progress.completedLessons.length} 个'),
          ],
        ),
      ),
    );
  }

  Widget _buildAnswerDetailCard(
    BuildContext context,
    Progress progress,
    WidgetRef ref,
  ) {
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
        final correctIds = <String>[];
        final wrongIds = <String>[];
        for (final quiz in quizzes) {
          final record = records[quiz.id];
          if (record != null) {
            if (record == quiz.answerIndex) {
              correctIds.add(quiz.id);
            } else {
              wrongIds.add(quiz.id);
            }
          }
        }

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.list_alt, color: Color(0xFF9B59B6)),
                    SizedBox(width: 8),
                    Text(
                      '答题明细',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                if (wrongIds.isNotEmpty) ...[
                  _buildDetailSection(
                    '做错的题目',
                    wrongIds,
                    quizzes,
                    const Color(0xFFE74C3C),
                  ),
                  const SizedBox(height: 12),
                ],
                if (correctIds.isNotEmpty) ...[
                  _buildDetailSection(
                    '做对的题目',
                    correctIds,
                    quizzes,
                    const Color(0xFF4CAF50),
                  ),
                  const SizedBox(height: 12),
                ],
                Text(
                  '共 ${records.length} / ${quizzes.length} 题已作答',
                  style: const TextStyle(
                    fontSize: 13,
                    color: Color(0xFF888888),
                  ),
                ),
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

  Widget _buildDetailSection(
    String title,
    List<String> ids,
    List<Quiz> quizzes,
    Color color,
  ) {
    final items =
        ids.map((id) => quizzes.firstWhere((q) => q.id == id)).toList();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children:
              items.map((quiz) {
                return Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: color.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: color.withValues(alpha: 0.3)),
                  ),
                  child: Text(
                    '${quiz.id}. ${quiz.question.length > 15 ? '${quiz.question.substring(0, 15)}...' : quiz.question}',
                    style: TextStyle(fontSize: 12, color: color),
                  ),
                );
              }).toList(),
        ),
      ],
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
        final display = history.take(50).toList();
        return Padding(
          padding: const EdgeInsets.only(top: 16),
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
                          child: Text(
                            questionText,
                            style: const TextStyle(fontSize: 13, height: 1.4),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          record.date,
                          style: const TextStyle(
                            fontSize: 11,
                            color: Color(0xFFAAAAAA),
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
