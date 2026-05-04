import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../models/knowledge_graph.dart';
import '../models/knowledge_category.dart';
import '../models/knowledge_section.dart';

class KnowledgeMapPage extends ConsumerWidget {
  const KnowledgeMapPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphAsync = ref.watch(knowledgeGraphProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('知识地图')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) => _buildContent(context, graph),
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(
                        Icons.error_outline,
                        size: 56,
                        color: Color(0xFFE74C3C),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        '加载知识图谱失败',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFE74C3C),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        e.toString(),
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 14,
                          color: Color(0xFF888888),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
        ),
      ),
    );
  }

  Widget _buildContent(BuildContext context, KnowledgeGraph graph) {
    final sectionCount = graph.allSections.length;
    final itemCount = graph.allItems.length;
    final categoryCount = graph.categories.length;

    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF3498DB), Color(0xFF2980B9)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.account_tree, color: Colors.white, size: 36),
                const SizedBox(height: 10),
                const Text(
                  '知识地图',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                const Text(
                  '按分类和章节浏览知识点',
                  style: TextStyle(fontSize: 14, color: Color(0xFFD4E6F9)),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    _StatChip(
                      label: '$categoryCount 个分类',
                      icon: Icons.category,
                    ),
                    const SizedBox(width: 10),
                    _StatChip(
                      label: '$sectionCount 个章节',
                      icon: Icons.folder_open,
                    ),
                    const SizedBox(width: 10),
                    _StatChip(
                      label: '$itemCount 个知识点',
                      icon: Icons.lightbulb_outline,
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
        SliverList(
          delegate: SliverChildBuilderDelegate((context, index) {
            final category = graph.categories[index];
            return _CategorySection(category: category, graph: graph);
          }, childCount: graph.categories.length),
        ),
        const SliverPadding(padding: EdgeInsets.only(bottom: 24)),
      ],
    );
  }
}

class _StatChip extends StatelessWidget {
  final String label;
  final IconData icon;

  const _StatChip({required this.label, required this.icon});

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

class _CategorySection extends StatelessWidget {
  final KnowledgeCategory category;
  final KnowledgeGraph graph;

  const _CategorySection({required this.category, required this.graph});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 8),
          child: Text(
            category.name,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Color(0xFF333333),
            ),
          ),
        ),
        ...category.sections.map((section) => _SectionCard(section: section)),
      ],
    );
  }
}

class _SectionCard extends StatelessWidget {
  final KnowledgeSection section;

  const _SectionCard({required this.section});

  @override
  Widget build(BuildContext context) {
    final itemCount = section.items.length;
    final preCount = section.pre.length;

    return Card(
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(
            context,
            '/knowledge/section',
            arguments: section.id,
          );
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: const Color(0xFF3498DB).withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Center(
                  child: Text(
                    section.id,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF3498DB),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      section.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        if (section.level.isNotEmpty) ...[
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 6,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: const Color(0xFFE8F0FE),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              section.level,
                              style: const TextStyle(
                                fontSize: 11,
                                color: Color(0xFF3498DB),
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                        ],
                        Text(
                          '$itemCount 个知识点',
                          style: const TextStyle(
                            fontSize: 13,
                            color: Color(0xFF888888),
                          ),
                        ),
                        if (preCount > 0) ...[
                          const SizedBox(width: 8),
                          Text(
                            '需前置 $preCount 项',
                            style: const TextStyle(
                              fontSize: 13,
                              color: Color(0xFFE67E22),
                            ),
                          ),
                        ],
                      ],
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
