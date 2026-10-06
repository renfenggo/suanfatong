import '../models/knowledge_content_index.dart';
import 'json_asset_repository.dart';

/// 加载 knowledge_content 内容包清单（content_index.json）。
///
/// content_index 只包含分片区间的生产元信息（不含 item_id 映射），
/// item_id -> 分片的显式映射见 item_part_index.json（由
/// tools/publish/build_item_part_index.py 生成）。
class ContentIndexRepository {
  static const _assetPath = 'assets/data/knowledge_content/content_index.json';

  final JsonAssetRepository _jsonRepo;

  ContentIndexRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<KnowledgeContentIndex> loadIndex() async {
    final map = await _jsonRepo.loadMap(_assetPath);
    return KnowledgeContentIndex.fromJson(map);
  }
}
