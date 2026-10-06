import '../models/knowledge_content_item.dart';
import 'json_asset_repository.dart';

/// 知识内容包仓库：按 item_id 从 33 个分片中按需加载讲解内容。
///
/// 设计约束（M1-4 / ADR-004）：
/// - 不把 33 个分片一次性全解码到内存；每次只加载 item 所在的一个分片。
/// - item_id -> 分片映射来自 item_part_index.json（离线生成，见
///   tools/publish/build_item_part_index.py）；分片顺序与图谱展平顺序
///   不一致，禁止用 content_index 的 start_index/end_index 区间推算。
/// - LRU 分片缓存（默认 4 个分片，约 2.5MB），同一分片内多个知识点
///   只解码一次。
/// - 失败降级：索引缺失、分片缺失、JSON 损坏、item 未命中、坏记录，
///   一律返回 null（UI 隐藏讲解区），不向调用方抛异常。
class KnowledgeContentRepository {
  static const _indexPath =
      'assets/data/knowledge_content/item_part_index.json';
  static const _itemsDir = 'assets/data/knowledge_content/items/';
  static const defaultMaxCachedParts = 4;

  final JsonAssetRepository _jsonRepo;
  final int maxCachedParts;

  Map<String, String>? _itemToPart;
  Future<Map<String, String>>? _indexFuture;

  final _partCache = <String, Map<String, KnowledgeContentItem>>{};
  final _partInFlight = <String, Future<Map<String, KnowledgeContentItem>>>{};
  final _lruOrder = <String>[];

  KnowledgeContentRepository({
    required JsonAssetRepository jsonRepo,
    this.maxCachedParts = defaultMaxCachedParts,
  }) : _jsonRepo = jsonRepo;

  /// 加载 item 的讲解内容；任何失败都降级返回 null。
  Future<KnowledgeContentItem?> loadItem(String itemId) async {
    if (itemId.isEmpty) return null;
    try {
      final index = await _loadIndex();
      final partFile = index[itemId];
      if (partFile == null) return null;
      final partItems = await _loadPart(partFile);
      return partItems[itemId];
    } catch (_) {
      return null;
    }
  }

  /// item 所在分片文件名（不含目录）；未收录返回 null。
  Future<String?> partForItem(String itemId) async {
    if (itemId.isEmpty) return null;
    try {
      final index = await _loadIndex();
      return index[itemId];
    } catch (_) {
      return null;
    }
  }

  /// 索引收录的 item 总数（测试/诊断用）；加载失败返回 0。
  Future<int> indexedItemCount() async {
    try {
      return (await _loadIndex()).length;
    } catch (_) {
      return 0;
    }
  }

  /// 当前缓存的分片数（测试/诊断用）。
  int get cachedPartCount => _partCache.length;

  Future<Map<String, String>> _loadIndex() {
    return _indexFuture ??= _loadIndexUncached();
  }

  Future<Map<String, String>> _loadIndexUncached() async {
    if (_itemToPart != null) return _itemToPart!;
    final map = await _jsonRepo.loadMap(_indexPath);
    final rawItems = map['items'];
    if (rawItems is! Map) {
      throw const FormatException('item_part_index 缺少 items 映射');
    }
    final result = <String, String>{};
    rawItems.forEach((key, value) {
      if (key is String && value is String && key.isNotEmpty) {
        result[key] = value;
      }
    });
    if (result.isEmpty) {
      throw const FormatException('item_part_index 映射为空');
    }
    return _itemToPart = result;
  }

  Future<Map<String, KnowledgeContentItem>> _loadPart(String partFile) {
    final cached = _partCache[partFile];
    if (cached != null) {
      _touchLru(partFile);
      return Future.value(cached);
    }
    return _partInFlight[partFile] ??= _loadPartUncached(partFile);
  }

  Future<Map<String, KnowledgeContentItem>> _loadPartUncached(
    String partFile,
  ) async {
    try {
      final list = await _jsonRepo.loadList('$_itemsDir$partFile');
      final items = <String, KnowledgeContentItem>{};
      for (final entry in list) {
        if (entry is! Map) continue;
        // 坏记录跳过，不阻塞整个分片。
        try {
          final item = KnowledgeContentItem.fromJson(
            entry.cast<String, dynamic>(),
          );
          items[item.itemId] = item;
        } on FormatException {
          continue;
        }
      }
      _partCache[partFile] = items;
      _touchLru(partFile);
      _evictIfNeeded();
      return items;
    } finally {
      _partInFlight.remove(partFile);
    }
  }

  void _touchLru(String partFile) {
    _lruOrder.remove(partFile);
    _lruOrder.add(partFile);
  }

  void _evictIfNeeded() {
    while (_lruOrder.length > maxCachedParts) {
      final oldest = _lruOrder.removeAt(0);
      _partCache.remove(oldest);
    }
  }
}
