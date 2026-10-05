import 'package:flutter/material.dart';
import '../../../models/learning_path.dart';

/// 跨章节前置知识点面板
///
/// 展示 learning_path_report_data.json 中的 cross_section_prerequisites。
/// 标题为"建议先补的基础"。当无数据时不渲染（由调用方控制）。
class CrossSectionPrerequisitePanel extends StatelessWidget {
  final List<CrossSectionPrerequisite> prerequisites;
  final void Function(String itemId)? onItemTap;

  const CrossSectionPrerequisitePanel({
    super.key,
    required this.prerequisites,
    this.onItemTap,
  });

  @override
  Widget build(BuildContext context) {
    if (prerequisites.isEmpty) return const SizedBox.shrink();

    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: const Color(0xFFE67E22).withValues(alpha: 0.2),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.school,
                  size: 20,
                  color: Color(0xFFE67E22),
                ),
                const SizedBox(width: 8),
                const Text(
                  '建议先补的基础',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFE67E22),
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE67E22).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    '${prerequisites.length} 个',
                    style: const TextStyle(
                      fontSize: 12,
                      color: Color(0xFFE67E22),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            const Text(
              '以下知识点在其他章节，建议先了解',
              style: TextStyle(fontSize: 12, color: Color(0xFF999999)),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: prerequisites.map((pre) {
                return _PrerequisiteChip(
                  prerequisite: pre,
                  onTap: onItemTap != null ? () => onItemTap!(pre.id) : null,
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class _PrerequisiteChip extends StatelessWidget {
  final CrossSectionPrerequisite prerequisite;
  final VoidCallback? onTap;

  const _PrerequisiteChip({required this.prerequisite, this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xFFFFF8F0),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: const Color(0xFFE67E22).withValues(alpha: 0.25),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 4,
                    vertical: 1,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE67E22).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    prerequisite.id,
                    style: const TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFFE67E22),
                    ),
                  ),
                ),
                const SizedBox(width: 6),
                ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 180),
                  child: Text(
                    prerequisite.name,
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w500,
                      color:
                          onTap != null
                              ? const Color(0xFF333333)
                              : const Color(0xFF666666),
                      decoration: onTap != null ? TextDecoration.underline : null,
                      decorationColor: const Color(0xFFE67E22).withValues(alpha: 0.4),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            if (prerequisite.reason.isNotEmpty) ...[
              const SizedBox(height: 2),
              Text(
                prerequisite.reason,
                style: const TextStyle(fontSize: 10, color: Color(0xFFAAAAAA)),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
