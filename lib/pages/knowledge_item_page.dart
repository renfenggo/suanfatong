import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/progress_provider.dart';
import '../state/cpp_animation_provider.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_graph.dart';

class KnowledgeItemPage extends ConsumerStatefulWidget {
  final String itemId;

  const KnowledgeItemPage({super.key, required this.itemId});

  @override
  ConsumerState<KnowledgeItemPage> createState() => _KnowledgeItemPageState();
}

class _KnowledgeItemPageState extends ConsumerState<KnowledgeItemPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref
          .read(lastKnowledgeItemProvider.notifier)
          .setLastKnowledgeItem(widget.itemId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final graphAsync = ref.watch(knowledgeGraphProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('知识点详情')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final item = graph.itemById(widget.itemId);
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
    final isCppItem = _isCppSyntaxItem(item, graph);
    final bfsActions = _getBfsActions(item);

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(item, section),
          const SizedBox(height: 16),
          if (isCppItem) ...[
            _buildCppLearnCard(context, item),
            const SizedBox(height: 12),
            _buildCppAnimationCard(context, item),
            const SizedBox(height: 12),
          ],
          if (bfsActions.isNotEmpty) ...[
            _buildBfsActionsGroup(context, bfsActions),
            const SizedBox(height: 12),
          ],
          if (item.alias.isNotEmpty) ...[
            _buildTagSection('别名', item.alias, const Color(0xFF9B59B6)),
            const SizedBox(height: 12),
          ],
          if (item.directPre.isNotEmpty) ...[
            _buildClickableRefSection(
              '直接前置',
              item.directPre,
              graph,
              const Color(0xFFE67E22),
            ),
            const SizedBox(height: 12),
          ],
          if (item.resolvedPre.isNotEmpty) ...[
            _buildClickableRefSection(
              '展开前置',
              item.resolvedPre,
              graph,
              const Color(0xFFE74C3C),
            ),
            const SizedBox(height: 12),
          ],
          if (item.rel.isNotEmpty) ...[
            _buildClickableRefSection(
              '相关知识',
              item.rel,
              graph,
              const Color(0xFF27AE60),
            ),
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
            Wrap(
              spacing: 8,
              runSpacing: 4,
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
                    item.id,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF3498DB),
                    ),
                  ),
                ),
                if (section != null)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 3,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF00897B).withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      section.name,
                      style: const TextStyle(
                        fontSize: 12,
                        color: Color(0xFF00897B),
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              item.name,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
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
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
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

  Widget _buildCppAnimationCard(BuildContext context, KnowledgeItem item) {
    final animationsAsync = ref.watch(cppAnimationsForItemProvider(item.id));
    return animationsAsync.when(
      data: (animations) {
        if (animations.isEmpty) return const SizedBox.shrink();
        final first = animations.first;
        return Card(
          color: const Color(0xFFE8F5E9),
          child: InkWell(
            onTap: () {
              Navigator.pushNamed(
                context,
                '/cpp_animation',
                arguments: first.animationId,
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
                          '动画演示（${animations.length}）',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF2E7D32),
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          first.title,
                          style: const TextStyle(
                            fontSize: 13,
                            color: Color(0xFF66BB6A),
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
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
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  List<_BfsAction> _getBfsActions(KnowledgeItem item) {
    final actions = <_BfsAction>[];
    final group = item.pickupGroup;
    const bfsGroups = {
      'bfs_basic',
      'bfs_maze',
      'bfs_maze_steps',
      'bfs_mistakes',
    };

    if (!bfsGroups.contains(group)) {
      return actions;
    }

    if (group == 'bfs_basic' || group == 'bfs_maze') {
      actions.add(
        _BfsAction(
          icon: Icons.school,
          title: '知识讲解',
          subtitle: '系统学习核心概念',
          route: '/lesson',
          color: const Color(0xFF1976D2),
        ),
      );
    }

    if (group == 'bfs_maze_steps') {
      actions.add(
        _BfsAction(
          icon: Icons.animation,
          title: '动画演示',
          subtitle: '可视化算法执行过程',
          route: '/animation',
          color: const Color(0xFF4CAF50),
        ),
      );
    }

    actions.add(
      _BfsAction(
        icon: Icons.quiz,
        title: '选择题训练',
        subtitle: '检验学习成果',
        route: '/quiz',
        color: const Color(0xFFFF9800),
      ),
    );

    if (group == 'bfs_mistakes') {
      actions.add(
        _BfsAction(
          icon: Icons.warning,
          title: '常见错误',
          subtitle: '避开典型陷阱',
          route: '/mistake',
          color: const Color(0xFFE74C3C),
        ),
      );
    }

    actions.add(
      _BfsAction(
        icon: Icons.cast_for_education,
        title: '老师演示模式',
        subtitle: '适合课堂投屏讲解',
        route: '/teacher',
        color: const Color(0xFF9C27B0),
      ),
    );

    return actions;
  }

  Widget _buildBfsActionsGroup(BuildContext context, List<_BfsAction> actions) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 10),
          child: Row(
            children: [
              Icon(
                Icons.psychology,
                size: 20,
                color: const Color(0xFF1976D2).withValues(alpha: 0.8),
              ),
              const SizedBox(width: 6),
              const Text(
                'BFS 学习工具',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF1976D2),
                ),
              ),
            ],
          ),
        ),
        ...actions.map(
          (action) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: _buildBfsActionItem(context, action),
          ),
        ),
      ],
    );
  }

  Widget _buildBfsActionItem(BuildContext context, _BfsAction action) {
    return Card(
      color: action.color.withValues(alpha: 0.06),
      child: InkWell(
        onTap: () => Navigator.pushNamed(context, action.route),
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          child: Row(
            children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: action.color.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(action.icon, color: action.color, size: 22),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      action.title,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                        color: action.color,
                      ),
                    ),
                    const SizedBox(height: 1),
                    Text(
                      action.subtitle,
                      style: TextStyle(
                        fontSize: 12,
                        color: action.color.withValues(alpha: 0.7),
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.chevron_right,
                color: action.color.withValues(alpha: 0.6),
              ),
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

  Widget _buildClickableRefSection(
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
                final exists = graph.itemById(id) != null;
                return ActionChip(
                  label: Text(
                    displayName,
                    style: TextStyle(fontSize: 13, color: color),
                  ),
                  backgroundColor: color.withValues(alpha: 0.08),
                  side: BorderSide(color: color.withValues(alpha: 0.3)),
                  onPressed:
                      exists
                          ? () {
                            Navigator.pushNamed(
                              context,
                              '/knowledge/item',
                              arguments: id,
                            );
                          }
                          : null,
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
}

class _BfsAction {
  final IconData icon;
  final String title;
  final String subtitle;
  final String route;
  final Color color;

  const _BfsAction({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.route,
    required this.color,
  });
}
