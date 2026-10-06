/// content_index.json 的模型：knowledge_content 内容包的生产元信息。
class KnowledgeContentIndex {
  final String version;
  final String sourceFile;
  final int sourceItemCount;
  final int generatedItemCount;
  final int totalParts;
  final List<KnowledgeContentPart> parts;

  const KnowledgeContentIndex({
    this.version = '',
    this.sourceFile = '',
    this.sourceItemCount = 0,
    this.generatedItemCount = 0,
    this.totalParts = 0,
    this.parts = const [],
  });

  factory KnowledgeContentIndex.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentIndex(
      version: json['version'] as String? ?? '',
      sourceFile: json['source_file'] as String? ?? '',
      sourceItemCount: json['source_item_count'] as int? ?? 0,
      generatedItemCount: json['generated_item_count'] as int? ?? 0,
      totalParts: json['total_parts'] as int? ?? 0,
      parts:
          (json['parts'] as List?)
              ?.whereType<Map<String, dynamic>>()
              .map(KnowledgeContentPart.fromJson)
              .toList() ??
          const [],
    );
  }
}

class KnowledgeContentPart {
  final String filename;
  final String path;
  final int batch;
  final int part;
  final int globalPart;
  final int startIndex;
  final int endIndex;
  final int itemCount;
  final String status;

  const KnowledgeContentPart({
    this.filename = '',
    this.path = '',
    this.batch = 0,
    this.part = 0,
    this.globalPart = 0,
    this.startIndex = 0,
    this.endIndex = 0,
    this.itemCount = 0,
    this.status = '',
  });

  factory KnowledgeContentPart.fromJson(Map<String, dynamic> json) {
    return KnowledgeContentPart(
      filename: json['filename'] as String? ?? '',
      path: json['path'] as String? ?? '',
      batch: _toInt(json['batch']),
      part: _toInt(json['part']),
      globalPart: _toInt(json['global_part']),
      startIndex: _toInt(json['start_index']),
      endIndex: _toInt(json['end_index']),
      itemCount: _toInt(json['item_count']),
      status: json['status'] as String? ?? '',
    );
  }
}

/// int 字段容错解码：分片元数据存在 int/String 混用方言
/// （stage5_hard 批次的 batch 为字符串批次名，不可数值化时记 0）。
int _toInt(dynamic value) {
  if (value is int) return value;
  if (value is num) return value.toInt();
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}
