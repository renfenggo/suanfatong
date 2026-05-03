import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/mistake_provider.dart';
import '../widgets/code_block.dart';

class MistakePage extends ConsumerWidget {
  const MistakePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final mistakesAsync = ref.watch(
      mistakesProvider('assets/data/mistakes/bfs_mistakes.json'),
    );

    return Scaffold(
      appBar: AppBar(title: const Text('常见错误')),
      body: SafeArea(
        child: mistakesAsync.when(
          data:
              (mistakes) => ListView.builder(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                itemCount: mistakes.length,
                itemBuilder: (context, index) {
                  return _MistakeTile(mistake: mistakes[index], index: index);
                },
              ),
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
}

class _MistakeTile extends StatelessWidget {
  final dynamic mistake;
  final int index;

  const _MistakeTile({required this.mistake, required this.index});

  @override
  Widget build(BuildContext context) {
    final colors = [
      const Color(0xFFE74C3C),
      const Color(0xFFFF6B35),
      const Color(0xFFE91E63),
      const Color(0xFFD32F2F),
      const Color(0xFFFF5722),
      const Color(0xFFC62828),
      const Color(0xFFE53935),
      const Color(0xFFFF7043),
    ];
    final accentColor = colors[index % colors.length];

    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: ExpansionTile(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: BorderSide(color: accentColor.withValues(alpha: 0.3)),
        ),
        collapsedShape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: BorderSide(color: accentColor.withValues(alpha: 0.2)),
        ),
        backgroundColor: Colors.white,
        collapsedBackgroundColor: accentColor.withValues(alpha: 0.03),
        tilePadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
        childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
        leading: Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: accentColor.withValues(alpha: 0.15),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              '${mistake.id}',
              style: TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.bold,
                color: accentColor,
              ),
            ),
          ),
        ),
        title: Text(
          mistake.title,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            color: accentColor,
          ),
        ),
        subtitle: Text(
          mistake.why.length > 40
              ? '${mistake.why.substring(0, 40)}...'
              : mistake.why,
          style: const TextStyle(
            fontSize: 13,
            color: Color(0xFF888888),
            height: 1.3,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        children: [
          _buildSection(
            '错误代码',
            mistake.wrongCode,
            const Color(0xFFFFEBEE),
            const Color(0xFFC62828),
          ),
          const SizedBox(height: 10),
          _buildWhySection(mistake.why),
          const SizedBox(height: 10),
          _buildSection(
            '正确做法',
            mistake.correct,
            const Color(0xFFE8F5E9),
            const Color(0xFF2E7D32),
          ),
          const SizedBox(height: 10),
          _buildTipSection(mistake.tip),
        ],
      ),
    );
  }

  Widget _buildSection(
    String title,
    String content,
    Color bgColor,
    Color borderColor,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: borderColor,
          ),
        ),
        const SizedBox(height: 6),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: bgColor,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: borderColor.withValues(alpha: 0.3)),
          ),
          child: CodeBlock(code: content),
        ),
      ],
    );
  }

  Widget _buildWhySection(String text) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF3E0),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: const Color(0xFFFFB74D).withValues(alpha: 0.5),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('❌ ', style: TextStyle(fontSize: 16)),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 14,
                height: 1.6,
                color: Color(0xFF5D4037),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTipSection(String text) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFE3F2FD),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: const Color(0xFF90CAF9).withValues(alpha: 0.5),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('💡 ', style: TextStyle(fontSize: 16)),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 14,
                height: 1.6,
                color: Color(0xFF1565C0),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
