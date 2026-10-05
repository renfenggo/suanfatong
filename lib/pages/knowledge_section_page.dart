import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/learning_structure_provider.dart';
import '../models/knowledge_section.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_graph.dart';
import '../widgets/knowledge/section/learning_path_panel.dart';
import '../widgets/knowledge/section/cross_section_prerequisite_panel.dart';
import '../widgets/knowledge/section/layered_knowledge_list.dart';

class KnowledgeSectionPage extends ConsumerWidget {
  final String sectionId;

  const KnowledgeSectionPage({super.key, required this.sectionId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphAsync = ref.watch(knowledgeGraphProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('章节详情')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final section = graph.sectionById(sectionId);
            if (section == null) {
              return _buildNotFound(context);
            }
            return _buildContent(context, ref, section, graph);
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Text(
                    '加载失败：$e',
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Color(0xFF888888)),
                  ),
                ),
              ),
        ),
      ),
    );
  }

  Widget _buildNotFound(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.search_off, size: 56, color: Color(0xFF888888)),
          const SizedBox(height: 16),
          const Text(
            '找不到该章节',
            style: TextStyle(fontSize: 18, color: Color(0xFF888888)),
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('返回'),
          ),
        ],
      ),
    );
  }

  Widget _buildContent(
    BuildContext context,
    WidgetRef ref,
    KnowledgeSection section,
    KnowledgeGraph graph,
  ) {
    // 监听学习路径和分层数据
    final learningPathAsync = ref.watch(
      sectionLearningPathProvider(sectionId),
    );
    final collapsePolicyAsync = ref.watch(
      sectionCollapsePolicyProvider(sectionId),
    );

    // 收集所有 itemId 用于查询分层
    final allItemIds = section.items.map((e) => e.id).toList();
    final itemLayersAsync = ref.watch(itemFrontendLayersProvider(allItemIds));

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(section),
          const SizedBox(height: 16),
          if (section.pre.isNotEmpty) ...[
            _buildTagRow('前置章节', section.pre, const Color(0xFFE67E22)),
            const SizedBox(height: 12),
          ],
          if (section.rel.isNotEmpty) ...[
            _buildTagRow('相关章节', section.rel, const Color(0xFF27AE60)),
            const SizedBox(height: 12),
          ],

          // 学习路径区域（仅有数据时显示，优雅降级）
          learningPathAsync.when(
            data: (learningPath) {
              if (learningPath == null || !learningPath.hasPathData()) {
                return const SizedBox.shrink();
              }
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 跨章节前置区域（仅有数据时显示）
                  if (learningPath.hasCrossSectionPrerequisites()) ...[
                    CrossSectionPrerequisitePanel(
                      prerequisites: learningPath.crossSectionPrerequisites,
                      onItemTap: (itemId) {
                        Navigator.pushNamed(
                          context,
                          '/knowledge/item',
                          arguments: itemId,
                        );
                      },
                    ),
                    const SizedBox(height: 12),
                  ],
                  // 学习路径面板
                  LearningPathPanel(
                    learningPath: learningPath,
                    itemNameResolver: (itemId) {
                      final item = graph.itemById(itemId);
                      return item?.name;
                    },
                    onItemTap: (itemId) {
                      Navigator.pushNamed(
                        context,
                        '/knowledge/item',
                        arguments: itemId,
                      );
                    },
                  ),
                  const SizedBox(height: 12),
                ],
              );
            },
            loading: () => const SizedBox.shrink(),
            error: (_, __) => const SizedBox.shrink(),
          ),

          const Divider(height: 24),
          Text(
            '知识点（${section.items.length}）',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),

          // 分层知识点列表（替代原来的平铺列表）
          itemLayersAsync.when(
            data: (itemLayers) {
              final collapsePolicy = collapsePolicyAsync.maybeWhen(
                data: (p) => p,
                orElse: () => null,
              );
              return LayeredKnowledgeList(
                items: section.items,
                itemLayers: itemLayers,
                collapsePolicy: collapsePolicy,
                onItemTap: (item) {
                  Navigator.pushNamed(
                    context,
                    '/knowledge/item',
                    arguments: item.id,
                  );
                },
              );
            },
            loading: () => _buildFallbackList(section),
            error: (_, __) => _buildFallbackList(section),
          ),
        ],
      ),
    );
  }

  /// 降级方案：不分层，直接平铺（与原有 UI 一致）
  Widget _buildFallbackList(KnowledgeSection section) {
    return Column(
      children: section.items.map((item) => _ItemCard(item: item)).toList(),
    );
  }

  Widget _buildHeader(KnowledgeSection section) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 3,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFF3498DB).withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    section.id,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF3498DB),
                    ),
                  ),
                ),
                if (section.level.isNotEmpty) ...[
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 3,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE8F0FE),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      section.level,
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF3498DB),
                      ),
                    ),
                  ),
                ],
              ],
            ),
            const SizedBox(height: 10),
            Text(
              section.name,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            Text(
              '${section.items.length} 个知识点',
              style: const TextStyle(fontSize: 14, color: Color(0xFF666666)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTagRow(String label, List<String> ids, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
          const SizedBox(height: 4),
          Wrap(
            spacing: 6,
            runSpacing: 4,
            children:
                ids
                    .map(
                      (id) => Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 3,
                        ),
                        decoration: BoxDecoration(
                          color: color.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(
                            color: color.withValues(alpha: 0.3),
                          ),
                        ),
                        child: Text(
                          id,
                          style: TextStyle(fontSize: 12, color: color),
                        ),
                      ),
                    )
                    .toList(),
          ),
        ],
      ),
    );
  }
}

class _ItemCard extends StatelessWidget {
  final KnowledgeItem item;

  const _ItemCard({required this.item});

  @override
  Widget build(BuildContext context) {
    final preCount = item.directPre.length;
    final resolvedCount = item.resolvedPre.length;

    return Card(
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(context, '/knowledge/item', arguments: item.id);
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: const Color(0xFFF0F4FF),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Center(
                  child: Text(
                    item.id,
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF3498DB),
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.name,
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 3),
                    Row(
                      children: [
                        if (item.pickupGroupName.isNotEmpty) ...[
                          Flexible(
                            child: Text(
                              item.pickupGroupName,
                              style: const TextStyle(
                                fontSize: 12,
                                color: Color(0xFF27AE60),
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          const SizedBox(width: 8),
                        ],
                        if (preCount > 0)
                          Text(
                            '前置 $resolvedCount',
                            style: const TextStyle(
                              fontSize: 12,
                              color: Color(0xFF888888),
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: Colors.grey[400], size: 20),
            ],
          ),
        ),
      ),
    );
  }
}
