import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/progress_provider.dart';
import '../state/cpp_animation_provider.dart';
import '../state/unified_learning_provider.dart';
import '../models/knowledge_item.dart';
import '../models/knowledge_graph.dart';
import '../models/learning_card.dart';
import '../models/practice_entry.dart';
import '../models/cpp14_template_entry.dart';
import '../services/learning_card_service.dart';
import '../services/practice_entry_service.dart';
import '../services/cpp14_template_service.dart';
import '../widgets/knowledge/learning_card_section.dart';
import '../widgets/knowledge/practice_entry_section.dart';
import '../widgets/knowledge/cpp14_template_entry_section.dart';
import '../widgets/knowledge/animation_entry_section.dart';
import '../widgets/knowledge/knowledge_content_section.dart';
import '../state/knowledge_content_provider.dart';

class KnowledgeItemPage extends ConsumerStatefulWidget {
  final String itemId;

  const KnowledgeItemPage({super.key, required this.itemId});

  @override
  ConsumerState<KnowledgeItemPage> createState() => _KnowledgeItemPageState();
}

class _KnowledgeItemPageState extends ConsumerState<KnowledgeItemPage> {
  final _learningCardService = LearningCardService();
  final _practiceEntryService = PracticeEntryService();
  final _cpp14TemplateService = Cpp14TemplateService();

  Future<LearningCard?> _loadLearningCard(String itemId) async {
    try {
      return await _learningCardService.getCardById(itemId);
    } catch (_) {
      return null;
    }
  }

  Future<PracticeEntry?> _loadPracticeEntry(String itemId) async {
    try {
      return await _practiceEntryService.getEntryByItemId(itemId);
    } catch (_) {
      return null;
    }
  }

  Future<Cpp14TemplateEntry?> _loadCpp14Template(String itemId) async {
    try {
      return await _cpp14TemplateService.getEntryByItemId(itemId);
    } catch (_) {
      return null;
    }
  }

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
    final isLearnableItem =
        isCppItem || _isAlgorithmItem(item, graph) || _isMathItem(item, graph);
    final bfsActions = _getBfsActions(item);

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(item, section),
          const SizedBox(height: 16),
          // 知识讲解区域（knowledge_content 内容包，按需加载，缺失降级隐藏）
          _buildKnowledgeContentSection(item),
          // 学习卡片区域（异步）
          FutureBuilder<LearningCard?>(
            future: _loadLearningCard(item.id),
            builder: (context, snapshot) {
              if (!snapshot.hasData || snapshot.data == null) {
                return const SizedBox.shrink();
              }
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  LearningCardSection(card: snapshot.data!),
                  const SizedBox(height: 12),
                ],
              );
            },
          ),
          // 练习入口区域（异步）
          FutureBuilder<PracticeEntry?>(
            future: _loadPracticeEntry(item.id),
            builder: (context, snapshot) {
              if (!snapshot.hasData || snapshot.data == null) {
                return const SizedBox.shrink();
              }
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  PracticeEntrySection(entry: snapshot.data!),
                  const SizedBox(height: 12),
                ],
              );
            },
          ),
          // C++14 模板入口区域（异步）
          FutureBuilder<Cpp14TemplateEntry?>(
            future: _loadCpp14Template(item.id),
            builder: (context, snapshot) {
              if (!snapshot.hasData || snapshot.data == null) {
                return const SizedBox.shrink();
              }
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Cpp14TemplateEntrySection(entry: snapshot.data!),
                  const SizedBox(height: 12),
                ],
              );
            },
          ),
          // 动画入口区域（复用现有 provider 和路由）
          _buildAnimationEntrySection(context, item),
          if (isLearnableItem) _buildLegacyCppLearnCard(context, item),
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

  /// 知识讲解区域：从 knowledge_content 内容包按需加载当前知识点的
  /// 结构化讲解（3240 节点全覆盖）。加载失败或未收录时隐藏（降级）。
  Widget _buildKnowledgeContentSection(KnowledgeItem item) {
    final contentAsync = ref.watch(knowledgeContentItemProvider(item.id));
    return contentAsync.when(
      data: (content) {
        if (content == null) return const SizedBox.shrink();
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            KnowledgeContentSection(item: content),
            const SizedBox(height: 12),
          ],
        );
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
    );
  }

  /// 动画入口区域（统一入口，复用现有 provider 和路由）
  Widget _buildAnimationEntrySection(BuildContext context, KnowledgeItem item) {
    final animationsAsync = ref.watch(cppAnimationsForItemProvider(item.id));
    return animationsAsync.when(
      data: (animations) {
        if (animations.isEmpty) return const SizedBox.shrink();
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AnimationEntrySection(
              animations: animations,
              onViewAnimation: (animationId) {
                context.push('/cpp_animation', extra: animationId);
              },
            ),
            const SizedBox(height: 12),
          ],
        );
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
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

  Widget _buildLegacyCppLearnCard(BuildContext context, KnowledgeItem item) {
    final unitAsync = ref.watch(unifiedLearningUnitByItemIdProvider(item.id));
    return unitAsync.when(
      data: (unit) {
        if (unit == null) return const SizedBox.shrink();
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildCppLearnCard(context, item),
            const SizedBox(height: 12),
          ],
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
                '学习工具',
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

  bool _isAlgorithmItem(KnowledgeItem item, KnowledgeGraph graph) {
    final section = graph.sectionById(item.parent);
    if (section == null) return false;
    final prefix = section.id.split('.').first;
    return prefix == '2' || prefix == '3';
  }

  bool _isMathItem(KnowledgeItem item, KnowledgeGraph graph) {
    final section = graph.sectionById(item.parent);
    if (section == null) return false;
    final prefix = section.id.split('.').first;
    return prefix == '4' || prefix == '5';
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
