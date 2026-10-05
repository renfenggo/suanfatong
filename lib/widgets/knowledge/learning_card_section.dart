import 'package:flutter/material.dart';
import '../../models/learning_card.dart';

/// 学习卡片区域
/// 展示某个知识点的结构化学习内容
class LearningCardSection extends StatelessWidget {
  final LearningCard card;
  final VoidCallback? onNextItemTap;

  const LearningCardSection({
    super.key,
    required this.card,
    this.onNextItemTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: const Color(0xFFFFF8E1),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: const Color(0xFFFFC107).withValues(alpha: 0.3)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeader(),
            const SizedBox(height: 14),
            if (card.summary.isNotEmpty) ...[
              _buildField(
                icon: Icons.lightbulb_outline,
                label: '一句话解释',
                content: card.summary,
                color: const Color(0xFFFFA000),
              ),
              const SizedBox(height: 12),
            ],
            if (card.intuition.isNotEmpty) ...[
              _buildField(
                icon: Icons.psychology_outlined,
                label: '核心直觉',
                content: card.intuition,
                color: const Color(0xFF8E24AA),
              ),
              const SizedBox(height: 12),
            ],
            if (card.useCases.isNotEmpty) ...[
              _buildField(
                icon: Icons.help_outline,
                label: '什么时候用',
                content: card.useCases,
                color: const Color(0xFF1976D2),
              ),
              const SizedBox(height: 12),
            ],
            if (card.example.isNotEmpty) ...[
              _buildField(
                icon: Icons.code,
                label: '最小例子',
                content: card.example,
                color: const Color(0xFF388E3C),
              ),
              const SizedBox(height: 12),
            ],
            if (card.traps.isNotEmpty) ...[
              _buildTraps(card.traps),
              const SizedBox(height: 12),
            ],
            if (card.practice.isNotEmpty) ...[
              _buildField(
                icon: Icons.fitness_center,
                label: '练习入口',
                content: card.practice,
                color: const Color(0xFFE64A19),
              ),
              const SizedBox(height: 12),
            ],
            if (card.nextItems.isNotEmpty) ...[
              _buildNextItems(card.nextItems),
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
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: const Color(0xFFFFC107).withValues(alpha: 0.2),
            borderRadius: BorderRadius.circular(10),
          ),
          child: const Icon(
            Icons.menu_book,
            color: Color(0xFFFFA000),
            size: 22,
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            '学习卡片',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: const Color(0xFFFFA000),
            ),
          ),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
          decoration: BoxDecoration(
            color: const Color(0xFF7E57C2).withValues(alpha: 0.12),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Text(
            card.getActionTypeDescription(),
            style: const TextStyle(fontSize: 11, color: Color(0xFF7E57C2)),
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
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 18, color: color),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: color,
                ),
              ),
              const SizedBox(height: 3),
              Text(
                content,
                style: const TextStyle(
                  fontSize: 14,
                  color: Color(0xFF424242),
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTraps(List<String> traps) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Icon(
          Icons.warning_amber,
          size: 18,
          color: Color(0xFFE53935),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '常见坑',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFFE53935),
                ),
              ),
              const SizedBox(height: 6),
              Wrap(
                spacing: 6,
                runSpacing: 4,
                children:
                    traps
                        .map(
                          (trap) => Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 3,
                            ),
                            decoration: BoxDecoration(
                              color: const Color(0xFFE53935).withValues(
                                alpha: 0.08,
                              ),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              trap,
                              style: const TextStyle(
                                fontSize: 12,
                                color: Color(0xFFE53935),
                              ),
                            ),
                          ),
                        )
                        .toList(),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildNextItems(List<String> nextItems) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Icon(
          Icons.arrow_forward,
          size: 18,
          color: Color(0xFF00897B),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '学完继续',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF00897B),
                ),
              ),
              const SizedBox(height: 6),
              Wrap(
                spacing: 6,
                runSpacing: 4,
                children:
                    nextItems
                        .map(
                          (item) => Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 3,
                            ),
                            decoration: BoxDecoration(
                              color: const Color(0xFF00897B).withValues(
                                alpha: 0.08,
                              ),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              item,
                              style: const TextStyle(
                                fontSize: 12,
                                color: Color(0xFF00897B),
                              ),
                            ),
                          ),
                        )
                        .toList(),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
