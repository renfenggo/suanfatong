import 'package:flutter/material.dart';
import '../../../models/knowledge_item.dart';
import '../../../models/learning_layer.dart';

/// 分层知识点列表
///
/// 将章节内知识点按 core / standard / advanced / optional 分组展示。
/// core 默认展开，standard 默认展开，advanced 和 optional 默认折叠。
/// 高拥挤章节（由 collapsePolicy 决定）进一步折叠。
class LayeredKnowledgeList extends StatefulWidget {
  final List<KnowledgeItem> items;
  final Map<String, String> itemLayers;
  final SectionCollapsePolicy? collapsePolicy;
  final void Function(KnowledgeItem item)? onItemTap;

  const LayeredKnowledgeList({
    super.key,
    required this.items,
    required this.itemLayers,
    this.collapsePolicy,
    this.onItemTap,
  });

  @override
  State<LayeredKnowledgeList> createState() => _LayeredKnowledgeListState();
}

class _LayeredKnowledgeListState extends State<LayeredKnowledgeList> {
  @override
  Widget build(BuildContext context) {
    final grouped = _groupItemsByLayer(widget.items, widget.itemLayers);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLayerSummary(grouped),
        const SizedBox(height: 8),
        _buildLayerSection(
          context,
          layerName: 'core',
          title: '核心主线',
          icon: Icons.star,
          color: const Color(0xFF3498DB),
          items: grouped['core'] ?? const [],
          initiallyExpanded: true,
        ),
        if ((grouped['standard'] ?? []).isNotEmpty) ...[
          const SizedBox(height: 8),
          _buildLayerSection(
            context,
            layerName: 'standard',
            title: '常用进阶',
            icon: Icons.trending_up,
            color: const Color(0xFF27AE60),
            items: grouped['standard'] ?? const [],
            initiallyExpanded: true,
          ),
        ],
        if ((grouped['advanced'] ?? []).isNotEmpty) ...[
          const SizedBox(height: 8),
          _buildLayerSection(
            context,
            layerName: 'advanced',
            title: '专题扩展',
            icon: Icons.school,
            color: const Color(0xFFE67E22),
            items: grouped['advanced'] ?? const [],
            initiallyExpanded: _isAdvancedExpanded(),
          ),
        ],
        if ((grouped['optional'] ?? []).isNotEmpty) ...[
          const SizedBox(height: 8),
          _buildLayerSection(
            context,
            layerName: 'optional',
            title: '冷门 / 可选',
            icon: Icons.bookmark_border,
            color: const Color(0xFF95A5A6),
            items: grouped['optional'] ?? const [],
            initiallyExpanded: false,
          ),
        ],
      ],
    );
  }

  /// advanced 是否默认展开
  /// 高拥挤章节默认折叠 advanced，其他章节也默认折叠
  bool _isAdvancedExpanded() {
    // advanced 默认折叠，不论章节
    return false;
  }

  Map<String, List<KnowledgeItem>> _groupItemsByLayer(
    List<KnowledgeItem> items,
    Map<String, String> itemLayers,
  ) {
    final result = <String, List<KnowledgeItem>>{
      'core': [],
      'standard': [],
      'advanced': [],
      'optional': [],
    };

    for (final item in items) {
      final layer = itemLayers[item.id] ?? 'standard';
      final normalized = _normalizeLayer(layer);
      result[normalized]?.add(item);
    }

    return result;
  }

  String _normalizeLayer(String layer) {
    final lower = layer.toLowerCase();
    if (lower == 'core') return 'core';
    if (lower == 'standard' || lower == 'normal') return 'standard';
    if (lower == 'advanced' || lower == 'advanced_optional') return 'advanced';
    if (lower == 'optional') return 'optional';
    return 'standard';
  }

  Widget _buildLayerSummary(Map<String, List<KnowledgeItem>> grouped) {
    final coreCount = (grouped['core'] ?? []).length;
    final standardCount = (grouped['standard'] ?? []).length;
    final advancedCount = (grouped['advanced'] ?? []).length;
    final optionalCount = (grouped['optional'] ?? []).length;

    return Wrap(
      spacing: 6,
      runSpacing: 4,
      children: [
        _summaryChip('核心', coreCount, const Color(0xFF3498DB)),
        _summaryChip('进阶', standardCount, const Color(0xFF27AE60)),
        _summaryChip('扩展', advancedCount, const Color(0xFFE67E22)),
        _summaryChip('可选', optionalCount, const Color(0xFF95A5A6)),
      ],
    );
  }

  Widget _summaryChip(String label, int count, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
          const SizedBox(width: 4),
          Text(
            '$count',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLayerSection(
    BuildContext context, {
    required String layerName,
    required String title,
    required IconData icon,
    required Color color,
    required List<KnowledgeItem> items,
    required bool initiallyExpanded,
  }) {
    if (items.isEmpty) return const SizedBox.shrink();

    return ExpansionTile(
      initiallyExpanded: initiallyExpanded,
      tilePadding: const EdgeInsets.symmetric(horizontal: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: BorderSide(color: color.withValues(alpha: 0.15)),
      ),
      collapsedShape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: BorderSide(color: color.withValues(alpha: 0.15)),
      ),
      backgroundColor: color.withValues(alpha: 0.03),
      collapsedBackgroundColor: color.withValues(alpha: 0.03),
      title: Row(
        children: [
          Icon(icon, size: 18, color: color),
          const SizedBox(width: 6),
          Text(
            title,
            style: TextStyle(
              fontSize: 15,
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
      children: items.map((item) => _LayerItemCard(
        item: item,
        color: color,
        onTap: widget.onItemTap != null ? () => widget.onItemTap!(item) : null,
      )).toList(),
    );
  }
}

class _LayerItemCard extends StatelessWidget {
  final KnowledgeItem item;
  final Color color;
  final VoidCallback? onTap;

  const _LayerItemCard({
    required this.item,
    required this.color,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final preCount = item.directPre.length;
    final resolvedCount = item.resolvedPre.length;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      elevation: 0,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              Container(
                width: 36,
                height: 36,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    item.id,
                    style: TextStyle(
                      fontSize: 9,
                      fontWeight: FontWeight.w600,
                      color: color,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.name,
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Row(
                      children: [
                        if (item.pickupGroupName.isNotEmpty) ...[
                          Flexible(
                            child: Text(
                              item.pickupGroupName,
                              style: const TextStyle(
                                fontSize: 11,
                                color: Color(0xFF27AE60),
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          const SizedBox(width: 6),
                        ],
                        if (preCount > 0)
                          Text(
                            '前置 $resolvedCount',
                            style: const TextStyle(
                              fontSize: 11,
                              color: Color(0xFF888888),
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: Colors.grey[400], size: 18),
            ],
          ),
        ),
      ),
    );
  }
}
