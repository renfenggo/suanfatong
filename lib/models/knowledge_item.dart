class KnowledgeItem {
  final String id;
  final String name;
  final List<String> alias;
  final String parent;
  final List<String> directPre;
  final List<String> resolvedPre;
  final List<String> rel;
  final String blockId;
  final String blockName;
  final String pickupGroup;
  final String pickupGroupName;
  final int pickupOrder;
  final String resourceBlockId;
  final String resourceBlockName;

  const KnowledgeItem({
    required this.id,
    required this.name,
    this.alias = const [],
    this.parent = '',
    this.directPre = const [],
    this.resolvedPre = const [],
    this.rel = const [],
    this.blockId = '',
    this.blockName = '',
    this.pickupGroup = '',
    this.pickupGroupName = '',
    this.pickupOrder = 0,
    this.resourceBlockId = '',
    this.resourceBlockName = '',
  });

  factory KnowledgeItem.fromJson(Map<String, dynamic> json) {
    return KnowledgeItem(
      id: json['id'] as String? ?? '',
      name: json['name'] as String? ?? '',
      alias: _toStringList(json['alias']),
      parent: json['parent'] as String? ?? '',
      directPre: _toStringList(json['direct_pre']),
      resolvedPre: _toStringList(json['resolved_pre']),
      rel: _toStringList(json['rel']),
      blockId: json['block_id'] as String? ?? '',
      blockName: json['block_name'] as String? ?? '',
      pickupGroup: json['pickup_group'] as String? ?? '',
      pickupGroupName: json['pickup_group_name'] as String? ?? '',
      pickupOrder: json['pickup_order'] as int? ?? 0,
      resourceBlockId: json['resource_block_id'] as String? ?? '',
      resourceBlockName: json['resource_block_name'] as String? ?? '',
    );
  }
}

List<String> _toStringList(dynamic value) {
  if (value is List) {
    return value.whereType<String>().toList();
  }
  return const [];
}
