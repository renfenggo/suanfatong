import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/progress_provider.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphAsync = ref.watch(knowledgeGraphProvider);
    final lastItemId = ref.watch(lastKnowledgeItemProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('算法通')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            return ListView(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 32),
              children: [
                _buildHeader(),
                const SizedBox(height: 20),
                _buildContinueLearning(context, graph, lastItemId),
                const SizedBox(height: 16),
                _SectionLabel(label: '学习入口'),
                const SizedBox(height: 8),
                _HomeCard(
                  title: 'C++ 基础',
                  subtitle: '按知识图谱循序渐进学习语法',
                  icon: Icons.terminal,
                  color: const Color(0xFF00897B),
                  onTap: () => Navigator.pushNamed(context, '/cpp_basic'),
                ),
                const SizedBox(height: 10),
                _HomeCard(
                  title: '知识地图',
                  subtitle: '浏览所有算法与编程知识点',
                  icon: Icons.account_tree,
                  color: const Color(0xFF3498DB),
                  onTap: () => Navigator.pushNamed(context, '/knowledge'),
                ),
                const SizedBox(height: 10),
                _HomeCard(
                  title: '搜索知识点',
                  subtitle: '快速找到你想学的内容',
                  icon: Icons.search,
                  color: const Color(0xFF8E44AD),
                  onTap: () => Navigator.pushNamed(context, '/cpp_search'),
                ),
                const SizedBox(height: 20),
                _SectionLabel(label: '更多'),
                const SizedBox(height: 8),
                _HomeCard(
                  title: '学习进度',
                  subtitle: '查看你的学习记录',
                  icon: Icons.bar_chart,
                  color: const Color(0xFF1ABC9C),
                  onTap: () => Navigator.pushNamed(context, '/progress'),
                ),
                const SizedBox(height: 10),
                _HomeCard(
                  title: '设置',
                  subtitle: '字体大小、主题等',
                  icon: Icons.settings,
                  color: const Color(0xFF95A5A6),
                  onTap: () => Navigator.pushNamed(context, '/settings'),
                ),
              ],
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Text(
                    '加载失败: $e',
                    style: const TextStyle(color: Color(0xFF888888)),
                  ),
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
          colors: [Color(0xFF2C3E50), Color(0xFF3498DB)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.auto_stories, color: Colors.white, size: 36),
          const SizedBox(height: 10),
          const Text(
            '算法通',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            '围绕知识点，一步步掌握算法与编程',
            style: TextStyle(fontSize: 14, color: Color(0xFFBDC3C7)),
          ),
        ],
      ),
    );
  }

  Widget _buildContinueLearning(
    BuildContext context,
    dynamic graph,
    String lastItemId,
  ) {
    if (lastItemId.isEmpty) {
      return _HomeCard(
        title: '开始学习',
        subtitle: '从 C++ 基础第一个知识点开始',
        icon: Icons.play_circle_filled,
        color: const Color(0xFF27AE60),
        onTap:
            () => Navigator.pushNamed(
              context,
              '/cpp_learning_unit',
              arguments: '1.1.1',
            ),
      );
    }

    final item = graph.itemById(lastItemId);
    final displayName = item != null ? item.name : lastItemId;
    final isCppItem = item != null && _isCppItem(item, graph);

    return _HomeCard(
      title: '继续学习',
      subtitle: '上次学到：$displayName',
      icon: Icons.play_circle_filled,
      color: const Color(0xFF27AE60),
      onTap:
          () => Navigator.pushNamed(
            context,
            isCppItem ? '/cpp_learning_unit' : '/knowledge/item',
            arguments: lastItemId,
          ),
    );
  }

  bool _isCppItem(dynamic item, dynamic graph) {
    final section = graph.sectionById(item.parent);
    if (section == null) return false;
    for (final cat in graph.categories) {
      if (cat.name == 'C++语法') {
        return cat.sections.any((s) => s.id == section.id);
      }
    }
    return false;
  }
}

class _SectionLabel extends StatelessWidget {
  final String label;
  const _SectionLabel({required this.label});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 4),
      child: Text(
        label,
        style: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: Color(0xFF888888),
        ),
      ),
    );
  }
}

class _HomeCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  const _HomeCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(icon, color: color, size: 26),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF888888),
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: Colors.grey[400]),
            ],
          ),
        ),
      ),
    );
  }
}
