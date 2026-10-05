import 'package:flutter/material.dart';
import '../../../models/learning_path.dart';

/// 学习路径面板
///
/// 展示章节的三条学习路径（入门 / 提高 / 冲刺），
/// 每条路径展示知识点数量和标题列表。
class LearningPathPanel extends StatelessWidget {
  final LearningPath learningPath;
  final String? Function(String itemId)? itemNameResolver;
  final void Function(String itemId)? onItemTap;

  const LearningPathPanel({
    super.key,
    required this.learningPath,
    this.itemNameResolver,
    this.onItemTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: const Color(0xFF3498DB).withValues(alpha: 0.2)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.route, size: 20, color: Color(0xFF3498DB)),
                const SizedBox(width: 8),
                const Text(
                  '学习路径',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF3498DB),
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFF3498DB).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    '${learningPath.getTotalPathCount()} 个',
                    style: const TextStyle(
                      fontSize: 12,
                      color: Color(0xFF3498DB),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _buildPathSection(
              context,
              title: '入门路径',
              icon: Icons.looks_one,
              color: const Color(0xFF27AE60),
              items: learningPath.beginnerPath,
              description: learningPath.beginnerDescription,
            ),
            const SizedBox(height: 8),
            _buildPathSection(
              context,
              title: '提高路径',
              icon: Icons.looks_two,
              color: const Color(0xFFE67E22),
              items: learningPath.intermediatePath,
              description: learningPath.intermediateDescription,
            ),
            const SizedBox(height: 8),
            _buildPathSection(
              context,
              title: '冲刺路径',
              icon: Icons.looks_3,
              color: const Color(0xFFE74C3C),
              items: learningPath.advancedPath,
              description: learningPath.advancedDescription,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPathSection(
    BuildContext context, {
    required String title,
    required IconData icon,
    required Color color,
    required List<String> items,
    required String description,
  }) {
    if (items.isEmpty) return const SizedBox.shrink();

    return ExpansionTile(
      initiallyExpanded: title == '入门路径',
      tilePadding: const EdgeInsets.symmetric(horizontal: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: BorderSide(color: color.withValues(alpha: 0.15)),
      ),
      collapsedShape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: BorderSide(color: color.withValues(alpha: 0.15)),
      ),
      backgroundColor: color.withValues(alpha: 0.04),
      collapsedBackgroundColor: color.withValues(alpha: 0.04),
      title: Row(
        children: [
          Icon(icon, size: 18, color: color),
          const SizedBox(width: 6),
          Text(
            title,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
          const SizedBox(width: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              '${items.length}',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ),
        ],
      ),
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(8, 0, 8, 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: items.map((itemId) {
              final name = itemNameResolver?.call(itemId) ?? itemId;
              return _PathItemTile(
                itemId: itemId,
                name: name,
                color: color,
                onTap: onItemTap != null ? () => onItemTap!(itemId) : null,
              );
            }).toList(),
          ),
        ),
      ],
    );
  }
}

class _PathItemTile extends StatelessWidget {
  final String itemId;
  final String name;
  final Color color;
  final VoidCallback? onTap;

  const _PathItemTile({
    required this.itemId,
    required this.name,
    required this.color,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(6),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 8),
        child: Row(
          children: [
            Container(
              width: 6,
              height: 6,
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.6),
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
              decoration: BoxDecoration(
                color: const Color(0xFFF0F4FF),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                itemId,
                style: const TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF3498DB),
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                name,
                style: TextStyle(
                  fontSize: 13,
                  color: onTap != null ? const Color(0xFF333333) : const Color(0xFF666666),
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            if (onTap != null)
              Icon(Icons.chevron_right, size: 16, color: Colors.grey[400]),
          ],
        ),
      ),
    );
  }
}
