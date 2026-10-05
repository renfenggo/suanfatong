import 'package:flutter/material.dart';
import '../../models/cpp_animation.dart';

/// 动画入口区域
/// 展示某个知识点对应的动画演示入口
/// 复用现有 /cpp_animation 路由
class AnimationEntrySection extends StatelessWidget {
  final List<CppAnimationMeta> animations;
  final void Function(String animationId)? onViewAnimation;

  const AnimationEntrySection({
    super.key,
    required this.animations,
    this.onViewAnimation,
  });

  @override
  Widget build(BuildContext context) {
    if (animations.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 10),
          child: Row(
            children: [
              Icon(
                Icons.play_circle_outline,
                size: 20,
                color: const Color(0xFF43A047).withValues(alpha: 0.9),
              ),
              const SizedBox(width: 6),
              const Text(
                '动画演示',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF43A047),
                ),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFF43A047).withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  '${animations.length} 个',
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF43A047),
                  ),
                ),
              ),
            ],
          ),
        ),
        ...animations.map((a) => _buildAnimationCard(a)),
      ],
    );
  }

  Widget _buildAnimationCard(CppAnimationMeta animation) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Card(
        elevation: 0,
        color: const Color(0xFFE8F5E9),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(color: const Color(0xFF43A047).withValues(alpha: 0.2)),
        ),
        child: InkWell(
          onTap: onViewAnimation != null ? () => onViewAnimation!(animation.animationId) : null,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            child: Row(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: const Color(0xFF43A047).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: const Icon(
                    Icons.play_arrow,
                    color: Color(0xFF43A047),
                    size: 24,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        animation.title,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF2E7D32),
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        animation.animationId,
                        style: const TextStyle(
                          fontSize: 11,
                          color: Color(0xFF81C784),
                          fontFamily: 'Courier',
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                const Icon(
                  Icons.chevron_right,
                  color: Color(0xFF43A047),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
