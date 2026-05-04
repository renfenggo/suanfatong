import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_graph.dart';

class KnowledgeItemPage extends ConsumerWidget {
  final String itemId;

  const KnowledgeItemPage({super.key, required this.itemId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphAsync = ref.watch(knowledgeGraphProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('知识点详情')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final item = graph.itemById(itemId);
            if (item == null) {
              return _buildNotFound(context);
            }
            return _buildContent(context, item, graph);
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
            '找不到该知识点',
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
    KnowledgeItem item,
    KnowledgeGraph graph,
  ) {
    final section =
        item.parent.isNotEmpty ? graph.sectionById(item.parent) : null;
    final hasBfsContent = _getBfsRoute(item) != null;
    final isCppItem = _isCppSyntaxItem(item, graph);

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(item, section),
          const SizedBox(height: 16),
          if (isCppItem) ...[
            _buildCppLearnCard(context, item),
            const SizedBox(height: 16),
          ],
          if (hasBfsContent) ...[
            _buildActionCard(context, item),
            const SizedBox(height: 16),
          ],
          if (item.alias.isNotEmpty) ...[
            _buildTagSection('别名', item.alias, const Color(0xFF9B59B6)),
            const SizedBox(height: 12),
          ],
          if (item.directPre.isNotEmpty) ...[
            _buildRefSection(
              '直接前置',
              item.directPre,
              graph,
              const Color(0xFFE67E22),
            ),
            const SizedBox(height: 12),
          ],
          if (item.resolvedPre.isNotEmpty) ...[
            _buildRefSection(
              '展开前置',
              item.resolvedPre,
              graph,
              const Color(0xFFE74C3C),
            ),
            const SizedBox(height: 12),
          ],
          if (item.rel.isNotEmpty) ...[
            _buildRefSection('相关知识', item.rel, graph, const Color(0xFF27AE60)),
            const SizedBox(height: 12),
          ],
          _buildInfoRow('pickup_group', item.pickupGroup),
          if (item.pickupGroupName.isNotEmpty)
            _buildInfoRow('pickup_group 名称', item.pickupGroupName),
          if (item.blockId.isNotEmpty) _buildInfoRow('block_id', item.blockId),
          if (item.blockName.isNotEmpty)
            _buildInfoRow('block_name', item.blockName),
        ],
      ),
    );
  }

  Widget _buildHeader(KnowledgeItem item, dynamic section) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: const Color(0xFF3498DB).withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(
                item.id,
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF3498DB),
                ),
              ),
            ),
            const SizedBox(height: 10),
            Text(
              item.name,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            if (section != null) ...[
              const SizedBox(height: 6),
              Row(
                children: [
                  const Icon(
                    Icons.folder_open,
                    size: 16,
                    color: Color(0xFF888888),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    '所属章节：${section.name}（${section.id}）',
                    style: const TextStyle(
                      fontSize: 14,
                      color: Color(0xFF666666),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, KnowledgeItem item) {
    final route = _getBfsRoute(item)!;
    final label = _getBfsLabel(item);

    return Card(
      color: const Color(0xFFE8F5E9),
      child: InkWell(
        onTap: () => Navigator.pushNamed(context, route),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: const Color(0xFF4CAF50).withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.play_circle_filled,
                  color: Color(0xFF4CAF50),
                  size: 26,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF2E7D32),
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '已关联 BFS 学习内容',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF66BB6A),
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward, color: Color(0xFF4CAF50)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTagSection(String label, List<String> tags, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 6),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
        ),
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children:
              tags
                  .map(
                    (tag) => Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: color.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: color.withValues(alpha: 0.3)),
                      ),
                      child: Text(
                        tag,
                        style: TextStyle(fontSize: 13, color: color),
                      ),
                    ),
                  )
                  .toList(),
        ),
      ],
    );
  }

  Widget _buildRefSection(
    String label,
    List<String> ids,
    KnowledgeGraph graph,
    Color color,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 6),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
        ),
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children:
              ids.map((id) {
                final displayName = _resolveId(id, graph);
                return Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: color.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: color.withValues(alpha: 0.3)),
                  ),
                  child: Text(
                    displayName,
                    style: TextStyle(fontSize: 13, color: color),
                  ),
                );
              }).toList(),
        ),
      ],
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(fontSize: 13, color: Color(0xFF888888)),
            ),
          ),
          Expanded(
            child: Text(
              value.isEmpty ? '—' : value,
              style: const TextStyle(fontSize: 13, color: Color(0xFF333333)),
            ),
          ),
        ],
      ),
    );
  }

  String _resolveId(String id, KnowledgeGraph graph) {
    final section = graph.sectionById(id);
    if (section != null) return '${section.name}（$id）';
    final item = graph.itemById(id);
    if (item != null) return '${item.name}（$id）';
    return id;
  }

  String? _getBfsRoute(KnowledgeItem item) {
    return switch (item.pickupGroup) {
      'bfs_basic' => '/lesson',
      'bfs_maze' => '/lesson',
      'bfs_mistakes' => '/mistake',
      'bfs_maze_steps' => '/animation',
      _ => null,
    };
  }

  String _getBfsLabel(KnowledgeItem item) {
    return switch (item.pickupGroup) {
      'bfs_basic' => '去学习 BFS 基础',
      'bfs_maze' => '看 BFS 迷宫应用',
      'bfs_mistakes' => '查看常见错误',
      'bfs_maze_steps' => '看 BFS 动画',
      _ => '去学习',
    };
  }

  bool _isCppSyntaxItem(KnowledgeItem item, KnowledgeGraph graph) {
    final section = graph.sectionById(item.parent);
    if (section == null) return false;
    for (final cat in graph.categories) {
      if (cat.name == 'C++语法') {
        return cat.sections.any((s) => s.id == section.id);
      }
    }
    return false;
  }

  Widget _buildCppLearnCard(BuildContext context, KnowledgeItem item) {
    return Card(
      color: const Color(0xFFE0F2F1),
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(
            context,
            '/cpp_learning_unit',
            arguments: item.id,
          );
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: const Color(0xFF00897B).withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.school,
                  color: Color(0xFF00897B),
                  size: 26,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '开始学习',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF00897B),
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '查看 ${item.name} 的讲解与练习',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF4DB6AC),
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward, color: Color(0xFF00897B)),
            ],
          ),
        ),
      ),
    );
  }
}
