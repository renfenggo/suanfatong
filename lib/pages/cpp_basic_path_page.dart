import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/progress_provider.dart';
import '../state/cpp_animation_provider.dart';
import '../models/knowledge_graph.dart';
import '../models/knowledge_category.dart';
import '../models/knowledge_section.dart';
import '../models/knowledge_item.dart';
import '../models/progress.dart';

enum CppFilter { all, l1, l2, l3, hasPre, startingPoint }

class CppBasicPathPage extends ConsumerStatefulWidget {
  const CppBasicPathPage({super.key});

  @override
  ConsumerState<CppBasicPathPage> createState() => _CppBasicPathPageState();
}

class _CppBasicPathPageState extends ConsumerState<CppBasicPathPage> {
  CppFilter _filter = CppFilter.all;

  @override
  Widget build(BuildContext context) {
    final graphAsync = ref.watch(knowledgeGraphProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('C++基础学习路径')),
      body: SafeArea(
        child: graphAsync.when(
          data: (graph) {
            final category = _findCppCategory(graph);
            if (category == null) {
              return _buildNotFound();
            }
            return _buildContent(context, graph, category);
          },
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

  KnowledgeCategory? _findCppCategory(KnowledgeGraph graph) {
    for (final cat in graph.categories) {
      if (cat.name == 'C++语法') return cat;
    }
    return null;
  }

  Widget _buildNotFound() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.search_off, size: 56, color: Color(0xFF888888)),
          const SizedBox(height: 16),
          const Text(
            '未找到 C++语法分类',
            style: TextStyle(fontSize: 18, color: Color(0xFF888888)),
          ),
        ],
      ),
    );
  }

  List<KnowledgeSection> _applyFilter(List<KnowledgeSection> sections) {
    return switch (_filter) {
      CppFilter.all => sections,
      CppFilter.l1 => sections.where((s) => s.level == 'L1').toList(),
      CppFilter.l2 => sections.where((s) => s.level == 'L2').toList(),
      CppFilter.l3 =>
        sections.where((s) => s.level == 'L3' || s.level == 'L4').toList(),
      CppFilter.hasPre => sections.where((s) => s.pre.isNotEmpty).toList(),
      CppFilter.startingPoint => sections.where((s) => s.pre.isEmpty).toList(),
    };
  }

  Widget _buildContent(
    BuildContext context,
    KnowledgeGraph graph,
    KnowledgeCategory category,
  ) {
    final sections = category.sections;
    final totalItems = sections.fold<int>(0, (sum, s) => sum + s.items.length);
    final l1Count = sections.where((s) => s.level == 'L1').length;
    final l2Count = sections.where((s) => s.level == 'L2').length;
    final l3Count =
        sections.where((s) => s.level == 'L3' || s.level == 'L4').length;

    final completedIds = ref.watch(cppProgressProvider);
    final quizProgress = ref.watch(cppQuizProgressProvider);
    final animManifestAsync = ref.watch(cppAnimationManifestProvider);
    final animationItemIds =
        animManifestAsync.whenOrNull<Set<String>>(
          data: (m) => m.animations.map((a) => a.itemId).toSet(),
        ) ??
        <String>{};
    final completedCount = _countCompleted(sections, completedIds);
    final percent =
        totalItems > 0 ? (completedCount / totalItems * 100).round() : 0;
    final allDone = completedCount >= totalItems && totalItems > 0;

    final nextItem = _findFirstIncomplete(sections, completedIds);

    final filtered = _applyFilter(sections);

    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF00897B), Color(0xFF00796B)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.terminal, color: Colors.white, size: 36),
                const SizedBox(height: 10),
                const Text(
                  'C++基础学习路径',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                const Text(
                  '按前置关系一步步学习',
                  style: TextStyle(fontSize: 14, color: Color(0xFFB2DFDB)),
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  runSpacing: 6,
                  children: [
                    _StatChip(
                      label: '${sections.length} 章节',
                      icon: Icons.folder_open,
                    ),
                    _StatChip(
                      label: '$totalItems 知识点',
                      icon: Icons.lightbulb_outline,
                    ),
                    _StatChip(
                      label: '已完成 $completedCount',
                      icon: Icons.check_circle,
                    ),
                    _StatChip(label: '$percent%', icon: Icons.trending_up),
                    _StatChip(label: 'L1 ×$l1Count', icon: Icons.looks_one),
                    _StatChip(label: 'L2 ×$l2Count', icon: Icons.looks_two),
                    if (l3Count > 0)
                      _StatChip(label: 'L3+ ×$l3Count', icon: Icons.looks_3),
                  ],
                ),
                const SizedBox(height: 12),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: totalItems > 0 ? completedCount / totalItems : 0,
                    backgroundColor: Colors.white.withValues(alpha: 0.3),
                    valueColor: const AlwaysStoppedAnimation<Color>(
                      Colors.white,
                    ),
                    minHeight: 6,
                  ),
                ),
                const SizedBox(height: 10),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed:
                        allDone
                            ? null
                            : () {
                              if (nextItem != null) {
                                Navigator.pushNamed(
                                  context,
                                  '/cpp_learning_unit',
                                  arguments: nextItem.id,
                                );
                              }
                            },
                    icon: Icon(allDone ? Icons.emoji_events : Icons.play_arrow),
                    label: Text(allDone ? '全部完成' : '继续学习'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: const Color(0xFF00897B),
                      disabledBackgroundColor: Colors.white.withValues(
                        alpha: 0.5,
                      ),
                      disabledForegroundColor: const Color(0xFF00897B),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                InkWell(
                  onTap: () {
                    Navigator.pushNamed(context, '/cpp_search');
                  },
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 10,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: Colors.white.withValues(alpha: 0.3),
                      ),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.search, color: Color(0xFFB2DFDB), size: 18),
                        SizedBox(width: 8),
                        Text(
                          '搜索知识点...',
                          style: TextStyle(
                            fontSize: 14,
                            color: Color(0xFFB2DFDB),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(12, 12, 12, 4),
            child: Wrap(
              spacing: 6,
              children:
                  CppFilter.values.map((f) {
                    final selected = f == _filter;
                    return ChoiceChip(
                      label: Text(_filterLabel(f)),
                      selected: selected,
                      onSelected: (_) => setState(() => _filter = f),
                    );
                  }).toList(),
            ),
          ),
        ),
        if (filtered.isEmpty)
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.all(40),
              child: Center(
                child: Text(
                  '没有匹配的章节',
                  style: TextStyle(fontSize: 16, color: Color(0xFF888888)),
                ),
              ),
            ),
          )
        else
          SliverList(
            delegate: SliverChildBuilderDelegate((context, index) {
              return _SectionCard(
                section: filtered[index],
                graph: graph,
                completedIds: completedIds,
                quizProgress: quizProgress,
                animationItemIds: animationItemIds,
              );
            }, childCount: filtered.length),
          ),
        const SliverPadding(padding: EdgeInsets.only(bottom: 24)),
      ],
    );
  }

  int _countCompleted(
    List<KnowledgeSection> sections,
    Set<String> completedIds,
  ) {
    int count = 0;
    for (final section in sections) {
      for (final item in section.items) {
        if (completedIds.contains(item.id)) count++;
      }
    }
    return count;
  }

  KnowledgeItem? _findFirstIncomplete(
    List<KnowledgeSection> sections,
    Set<String> completedIds,
  ) {
    for (final section in sections) {
      for (final item in section.items) {
        if (!completedIds.contains(item.id)) return item;
      }
    }
    return null;
  }

  String _filterLabel(CppFilter f) {
    return switch (f) {
      CppFilter.all => '全部',
      CppFilter.l1 => 'L1',
      CppFilter.l2 => 'L2',
      CppFilter.l3 => 'L3+',
      CppFilter.hasPre => '有前置',
      CppFilter.startingPoint => '起点',
    };
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

class _SectionCard extends StatelessWidget {
  final KnowledgeSection section;
  final KnowledgeGraph graph;
  final Set<String> completedIds;
  final Progress quizProgress;
  final Set<String> animationItemIds;

  const _SectionCard({
    required this.section,
    required this.graph,
    required this.completedIds,
    required this.quizProgress,
    required this.animationItemIds,
  });

  @override
  Widget build(BuildContext context) {
    final isStartingPoint = section.pre.isEmpty;
    final previewItems = section.items.take(3).toList();
    final completedCount = _sectionCompletedCount();
    final totalItems = section.items.length;
    final progress = totalItems > 0 ? completedCount / totalItems : 0.0;

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
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: const Color(0xFF00897B).withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: Text(
                        section.id,
                        style: const TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF00897B),
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
                                  color: const Color(0xFFE0F2F1),
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: Text(
                                  section.level,
                                  style: const TextStyle(
                                    fontSize: 11,
                                    color: Color(0xFF00897B),
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                              const SizedBox(width: 8),
                            ],
                            Text(
                              '$completedCount/$totalItems',
                              style: const TextStyle(
                                fontSize: 13,
                                color: Color(0xFF888888),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: () {
                      Navigator.pushNamed(
                        context,
                        '/cpp_section_quiz',
                        arguments: section.id,
                      );
                    },
                    icon: const Icon(Icons.quiz_outlined),
                    tooltip: '章节小测',
                    color: const Color(0xFF00897B),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(
                      minWidth: 36,
                      minHeight: 36,
                    ),
                  ),
                  Icon(Icons.chevron_right, color: Colors.grey[400]),
                ],
              ),
              const SizedBox(height: 8),
              _buildQuizInfoRow(),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(3),
                      child: LinearProgressIndicator(
                        value: progress,
                        backgroundColor: const Color(0xFFE0E0E0),
                        valueColor: const AlwaysStoppedAnimation<Color>(
                          Color(0xFF00897B),
                        ),
                        minHeight: 4,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  _buildStatusBadge(completedCount, totalItems),
                ],
              ),
              const SizedBox(height: 10),
              if (isStartingPoint)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE8F5E9),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.flag, size: 14, color: Color(0xFF4CAF50)),
                      SizedBox(width: 4),
                      Text(
                        '建议从这里开始',
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFF4CAF50),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                )
              else ...[
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF3E0),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(
                        Icons.lock_outline,
                        size: 14,
                        color: Color(0xFFE67E22),
                      ),
                      const SizedBox(width: 4),
                      Flexible(
                        child: Text(
                          '完成前置后学习（${section.pre.length} 项）',
                          style: const TextStyle(
                            fontSize: 12,
                            color: Color(0xFFE67E22),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 6),
                Wrap(
                  spacing: 4,
                  runSpacing: 4,
                  children:
                      section.pre.map((preId) {
                        final preSection = graph.sectionById(preId);
                        final display =
                            preSection != null
                                ? '${preSection.name}（$preId）'
                                : preId;
                        return Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 6,
                            vertical: 2,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFFF8E1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            display,
                            style: const TextStyle(
                              fontSize: 11,
                              color: Color(0xFF9E9E9E),
                            ),
                          ),
                        );
                      }).toList(),
                ),
              ],
              if (previewItems.isNotEmpty) ...[
                const SizedBox(height: 10),
                const Divider(height: 1),
                const SizedBox(height: 8),
                ...previewItems.map(
                  (item) => _ItemPreview(
                    item: item,
                    graph: graph,
                    completed: completedIds.contains(item.id),
                    hasAnimation: animationItemIds.contains(item.id),
                  ),
                ),
                if (section.items.length > 3)
                  Padding(
                    padding: const EdgeInsets.only(top: 4),
                    child: Text(
                      '还有 ${section.items.length - 3} 个知识点...',
                      style: const TextStyle(
                        fontSize: 12,
                        color: Color(0xFFBDBDBD),
                      ),
                    ),
                  ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  int _sectionCompletedCount() {
    int count = 0;
    for (final item in section.items) {
      if (completedIds.contains(item.id)) count++;
    }
    return count;
  }

  int _sectionWrongCount() {
    int count = 0;
    for (final id in quizProgress.cppWrongQuizIds) {
      if (id.startsWith('${section.id}|')) count++;
    }
    return count;
  }

  Widget _buildQuizInfoRow() {
    final score = quizProgress.cppQuizScores[section.id];
    final wrongCount = _sectionWrongCount();
    final List<Widget> chips = [];

    if (score != null) {
      chips.add(
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
          decoration: BoxDecoration(
            color: const Color(0xFFE0F2F1),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Text(
            '最近小测 $score 分',
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFF00897B),
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      );
    } else {
      chips.add(
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
          decoration: BoxDecoration(
            color: const Color(0xFFF5F5F5),
            borderRadius: BorderRadius.circular(4),
          ),
          child: const Text(
            '未小测',
            style: TextStyle(fontSize: 11, color: Color(0xFF9E9E9E)),
          ),
        ),
      );
    }

    if (wrongCount > 0) {
      chips.add(const SizedBox(width: 6));
      chips.add(
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
          decoration: BoxDecoration(
            color: const Color(0xFFFFF3E0),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Text(
            '错题 $wrongCount 道',
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFFE67E22),
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      );
    }

    return Wrap(spacing: 6, runSpacing: 4, children: chips);
  }

  Widget _buildStatusBadge(int completed, int total) {
    if (completed == 0) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
          color: const Color(0xFFF5F5F5),
          borderRadius: BorderRadius.circular(4),
        ),
        child: const Text(
          '未开始',
          style: TextStyle(fontSize: 11, color: Color(0xFF9E9E9E)),
        ),
      );
    } else if (completed >= total) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
          color: const Color(0xFFE8F5E9),
          borderRadius: BorderRadius.circular(4),
        ),
        child: const Text(
          '已完成',
          style: TextStyle(fontSize: 11, color: Color(0xFF4CAF50)),
        ),
      );
    } else {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
          color: const Color(0xFFE0F2F1),
          borderRadius: BorderRadius.circular(4),
        ),
        child: const Text(
          '继续学习',
          style: TextStyle(
            fontSize: 11,
            color: Color(0xFF00897B),
            fontWeight: FontWeight.w600,
          ),
        ),
      );
    }
  }
}

class _ItemPreview extends StatelessWidget {
  final KnowledgeItem item;
  final KnowledgeGraph graph;
  final bool completed;
  final bool hasAnimation;

  const _ItemPreview({
    required this.item,
    required this.graph,
    required this.completed,
    required this.hasAnimation,
  });

  @override
  Widget build(BuildContext context) {
    final hasPre = item.resolvedPre.isNotEmpty;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Icon(
            completed
                ? Icons.check_circle
                : (hasPre ? Icons.link : Icons.check_circle_outline),
            size: 14,
            color:
                completed
                    ? const Color(0xFF4CAF50)
                    : (hasPre
                        ? const Color(0xFFBDBDBD)
                        : const Color(0xFF4CAF50)),
          ),
          const SizedBox(width: 6),
          Expanded(
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    item.name,
                    style: TextStyle(
                      fontSize: 13,
                      color:
                          completed
                              ? const Color(0xFF4CAF50)
                              : const Color(0xFF555555),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (hasAnimation) ...[
                  const SizedBox(width: 4),
                  const Icon(
                    Icons.play_circle_filled,
                    size: 13,
                    color: Color(0xFF00897B),
                  ),
                ],
              ],
            ),
          ),
          Flexible(
            child: Text(
              completed
                  ? '已完成'
                  : (hasPre ? '前置 ${item.resolvedPre.length}' : '可学习'),
              style: TextStyle(
                fontSize: 11,
                color:
                    completed
                        ? const Color(0xFF4CAF50)
                        : (hasPre
                            ? const Color(0xFFBDBDBD)
                            : const Color(0xFF4CAF50)),
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}
