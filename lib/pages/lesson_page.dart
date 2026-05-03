import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/lesson_provider.dart';
import '../widgets/code_block.dart';

class LessonPage extends ConsumerWidget {
  const LessonPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lessonsAsync = ref.watch(
      lessonsProvider('assets/data/lessons/bfs_basic.json'),
    );

    return Scaffold(
      appBar: AppBar(title: const Text('BFS 知识讲解')),
      body: SafeArea(
        child: lessonsAsync.when(
          data: (lessons) {
            final sorted = List.of(lessons)
              ..sort((a, b) => a.order.compareTo(b.order));
            if (sorted.isEmpty) {
              return const Center(
                child: Text(
                  '暂无课程内容',
                  style: TextStyle(fontSize: 16, color: Color(0xFF888888)),
                ),
              );
            }
            return ListView.builder(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 32),
              itemCount: sorted.length,
              itemBuilder: (context, index) {
                return _LessonSection(lesson: sorted[index], index: index);
              },
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => _ErrorWidget(error: err),
        ),
      ),
    );
  }
}

class _LessonSection extends StatelessWidget {
  final dynamic lesson;
  final int index;

  const _LessonSection({required this.lesson, required this.index});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeader(context),
            const SizedBox(height: 14),
            _buildContent(context),
            if (lesson.example.isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildExample(context),
            ],
            if (lesson.code.isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildCode(context),
            ],
            if (lesson.tip.isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildTip(context),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: const Color(0xFF4A90D9),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              '${index + 1}',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                lesson.title,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                lesson.subtitle,
                style: const TextStyle(fontSize: 14, color: Color(0xFF666666)),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildContent(BuildContext context) {
    return Text(
      lesson.content,
      style: const TextStyle(
        fontSize: 16,
        height: 1.8,
        color: Color(0xFF333333),
      ),
    );
  }

  Widget _buildExample(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFE8F5E9),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFA5D6A7)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFF4CAF50),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text(
                  '小例子',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Text(
            lesson.example,
            style: const TextStyle(
              fontSize: 15,
              height: 1.7,
              color: Color(0xFF2E7D32),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCode(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: const Color(0xFF42A5F5),
                borderRadius: BorderRadius.circular(6),
              ),
              child: const Text(
                '代码',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),
        CodeBlock(code: lesson.code),
      ],
    );
  }

  Widget _buildTip(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF8E1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFFFE082)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(
            Icons.lightbulb_outline,
            color: Color(0xFFFFA000),
            size: 22,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              lesson.tip,
              style: const TextStyle(
                fontSize: 15,
                height: 1.6,
                color: Color(0xFF5D4037),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ErrorWidget extends StatelessWidget {
  final Object error;

  const _ErrorWidget({required this.error});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 56, color: Color(0xFFE74C3C)),
            const SizedBox(height: 16),
            const Text(
              '加载课程失败',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Color(0xFFE74C3C),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              error.toString(),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 14, color: Color(0xFF888888)),
            ),
          ],
        ),
      ),
    );
  }
}
