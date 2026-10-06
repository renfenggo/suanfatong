import 'package:flutter/material.dart';
import '../../models/knowledge_content_item.dart';

/// 知识讲解区域：展示 knowledge_content 内容包（3240 节点全覆盖）中
/// 当前知识点的结构化讲解：简介 / 学习目标 / 核心思想 / 步骤 /
/// 常见错误 / 示例 / 自测题 / 练习任务 / 掌握检查。
///
/// 内容缺失时由调用方隐藏本区域（内容包加载失败降级策略）。
class KnowledgeContentSection extends StatelessWidget {
  final KnowledgeContentItem item;

  const KnowledgeContentSection({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    final ex = item.example;
    final check = item.unlockCheck;

    return Card(
      elevation: 0,
      color: const Color(0xFFE3F2FD),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: const Color(0xFF1976D2).withValues(alpha: 0.3)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeader(),
            const SizedBox(height: 14),
            if (item.shortExplanation.isNotEmpty) ...[
              _buildField(
                icon: Icons.lightbulb_outline,
                label: '内容简介',
                content: item.shortExplanation,
                color: const Color(0xFF0D47A1),
              ),
              const SizedBox(height: 12),
            ],
            if (item.learningGoal.isNotEmpty) ...[
              _buildField(
                icon: Icons.flag_outlined,
                label: '学习目标',
                content: item.learningGoal,
                color: const Color(0xFF00695C),
              ),
              const SizedBox(height: 12),
            ],
            if (item.coreIdea.isNotEmpty) ...[
              _buildField(
                icon: Icons.psychology_outlined,
                label: '核心思想',
                content: item.coreIdea,
                color: const Color(0xFF6A1B9A),
              ),
              const SizedBox(height: 12),
            ],
            if (item.stepByStep.isNotEmpty) ...[
              _buildStepList(),
              const SizedBox(height: 12),
            ],
            if (item.commonMistakes.isNotEmpty) ...[
              _buildMistakes(),
              const SizedBox(height: 12),
            ],
            if (ex != null && _exampleHasContent(ex)) ...[
              _buildExample(ex),
              const SizedBox(height: 12),
            ],
            if (item.quiz.isNotEmpty) ...[
              _buildQuiz(),
              const SizedBox(height: 12),
            ],
            if (item.practiceTasks.isNotEmpty) ...[
              _buildPracticeTasks(),
              const SizedBox(height: 12),
            ],
            if (check != null && check.quickQuestion.isNotEmpty) ...[
              _buildUnlockCheck(check),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Row(
      children: [
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: const Color(0xFF1976D2).withValues(alpha: 0.15),
            borderRadius: BorderRadius.circular(10),
          ),
          child: const Icon(
            Icons.menu_book_outlined,
            color: Color(0xFF1976D2),
            size: 22,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '知识讲解',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF1976D2),
                ),
              ),
              if (item.sectionName.isNotEmpty)
                Text(
                  '${item.sectionName} · ${item.title}',
                  style: const TextStyle(
                    fontSize: 12,
                    color: Color(0xFF5C8AB8),
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildField({
    required IconData icon,
    required String label,
    required String content,
    required Color color,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 16, color: color),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        Text(
          content,
          style: const TextStyle(
            fontSize: 14,
            height: 1.5,
            color: Color(0xFF333333),
          ),
        ),
      ],
    );
  }

  Widget _buildStepList() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(
              Icons.format_list_numbered,
              size: 16,
              color: Color(0xFF1565C0),
            ),
            const SizedBox(width: 6),
            const Text(
              '学习步骤',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFF1565C0),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ...item.stepByStep.asMap().entries.map(
          (entry) => Padding(
            padding: const EdgeInsets.only(left: 8, bottom: 4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(
                  width: 20,
                  child: Text(
                    '${entry.key + 1}.',
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF1565C0),
                    ),
                  ),
                ),
                Expanded(
                  child: Text(
                    entry.value,
                    style: const TextStyle(
                      fontSize: 13,
                      height: 1.4,
                      color: Color(0xFF333333),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMistakes() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Row(
          children: [
            Icon(
              Icons.warning_amber_rounded,
              size: 16,
              color: Color(0xFFE65100),
            ),
            SizedBox(width: 6),
            Text(
              '常见错误与纠正',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFFE65100),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ...item.commonMistakes
            .where((m) => m.mistake.isNotEmpty)
            .map(
              (m) => Padding(
                padding: const EdgeInsets.only(left: 8, bottom: 6),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '× ${m.mistake}',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFFBF360C),
                      ),
                    ),
                    if (m.fix.isNotEmpty)
                      Text(
                        '✓ ${m.fix}',
                        style: const TextStyle(
                          fontSize: 13,
                          color: Color(0xFF2E7D32),
                        ),
                      ),
                  ],
                ),
              ),
            ),
      ],
    );
  }

  bool _exampleHasContent(KnowledgeContentExample ex) {
    return ex.description.isNotEmpty ||
        ex.explanation.isNotEmpty ||
        ex.pseudoOrCode.isNotEmpty;
  }

  Widget _buildExample(KnowledgeContentExample ex) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Row(
          children: [
            Icon(Icons.code, size: 16, color: Color(0xFF2E7D32)),
            SizedBox(width: 6),
            Text(
              '示例',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFF2E7D32),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        if (ex.description.isNotEmpty)
          Text(
            ex.description,
            style: const TextStyle(fontSize: 13, color: Color(0xFF333333)),
          ),
        if (ex.pseudoOrCode.isNotEmpty) ...[
          const SizedBox(height: 6),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: const Color(0xFF263238).withValues(alpha: 0.92),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              ex.pseudoOrCode,
              style: const TextStyle(
                fontSize: 12,
                height: 1.5,
                color: Color(0xFFECEFF1),
                fontFamily: 'monospace',
              ),
            ),
          ),
        ],
        if (ex.explanation.isNotEmpty) ...[
          const SizedBox(height: 6),
          Text(
            ex.explanation,
            style: const TextStyle(fontSize: 13, color: Color(0xFF333333)),
          ),
        ],
        if (ex.notes.isNotEmpty) ...[
          const SizedBox(height: 4),
          ...ex.notes.map(
            (n) => Text(
              '· $n',
              style: const TextStyle(fontSize: 12, color: Color(0xFF666666)),
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildQuiz() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Row(
          children: [
            Icon(Icons.quiz_outlined, size: 16, color: Color(0xFFEF6C00)),
            SizedBox(width: 6),
            Text(
              '随堂自测',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFFEF6C00),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ...item.quiz.asMap().entries.map((entry) {
          final q = entry.value;
          return Padding(
            padding: const EdgeInsets.only(left: 8, bottom: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Q${entry.key + 1} ${q.question}',
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF333333),
                  ),
                ),
                if (q.options.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(left: 12, top: 2),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children:
                          q.options
                              .map(
                                (o) => Text(
                                  '· $o',
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: Color(0xFF555555),
                                  ),
                                ),
                              )
                              .toList(),
                    ),
                  ),
                if (q.answer.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 2),
                    child: Text(
                      '答案：${q.answer}',
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF2E7D32),
                      ),
                    ),
                  ),
              ],
            ),
          );
        }),
      ],
    );
  }

  Widget _buildPracticeTasks() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Row(
          children: [
            Icon(Icons.fitness_center, size: 16, color: Color(0xFF6A1B9A)),
            SizedBox(width: 6),
            Text(
              '练习任务',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFF6A1B9A),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ...item.practiceTasks
            .where((t) => t.title.isNotEmpty)
            .map(
              (t) => Padding(
                padding: const EdgeInsets.only(left: 8, bottom: 6),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '· ${t.title}',
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF333333),
                      ),
                    ),
                    if (t.description.isNotEmpty)
                      Text(
                        t.description,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFF555555),
                        ),
                      ),
                  ],
                ),
              ),
            ),
      ],
    );
  }

  Widget _buildUnlockCheck(KnowledgeContentUnlockCheck check) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF1976D2).withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: const Color(0xFF1976D2).withValues(alpha: 0.25),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.verified_outlined, size: 16, color: Color(0xFF1976D2)),
              SizedBox(width: 6),
              Text(
                '掌握检查',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF1976D2),
                ),
              ),
            ],
          ),
          if (check.quickQuestion.isNotEmpty) ...[
            const SizedBox(height: 6),
            Text(
              check.quickQuestion,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFF333333),
              ),
            ),
          ],
          if (check.expectedAnswer.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 2),
              child: Text(
                '参考：${check.expectedAnswer}',
                style: const TextStyle(fontSize: 12, color: Color(0xFF555555)),
              ),
            ),
          if (check.passCondition.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 2),
              child: Text(
                '通过标准：${check.passCondition}',
                style: const TextStyle(fontSize: 12, color: Color(0xFF666666)),
              ),
            ),
        ],
      ),
    );
  }
}
