import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/practice_entry.dart';

/// 练习入口服务
/// 负责从 data/practice_entry_mvp_index.json 加载练习入口数据
class PracticeEntryService {
  static const String _dataPath = 'data/practice_entry_mvp_index.json';

  Map<String, PracticeEntry>? _entriesById;
  List<PracticeEntry>? _allEntries;

  /// 加载练习入口数据
  Future<void> load() async {
    if (_entriesById != null) return;
    try {
      final jsonString = await rootBundle.loadString(_dataPath);
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      final indexRaw = jsonData['index'] as List<dynamic>? ?? [];

      _entriesById = {};
      _allEntries = [];

      for (final entryData in indexRaw) {
        try {
          final entry = PracticeEntry.fromJson(
            entryData as Map<String, dynamic>,
          );
          if (entry.isValid) {
            _entriesById![entry.itemId] = entry;
            _allEntries!.add(entry);
          }
        } catch (_) {
          continue;
        }
      }
    } catch (_) {
      _entriesById = {};
      _allEntries = [];
    }
  }

  /// 按 itemId 查询练习入口，未找到返回 null
  Future<PracticeEntry?> getEntryByItemId(String itemId) async {
    await load();
    return _entriesById?[itemId];
  }

  /// 获取所有练习入口
  Future<List<PracticeEntry>> getAllEntries() async {
    await load();
    return _allEntries ?? [];
  }

  /// 检查是否存在
  Future<bool> exists(String itemId) async {
    final entry = await getEntryByItemId(itemId);
    return entry != null;
  }

  /// 清除缓存
  void clearCache() {
    _entriesById = null;
    _allEntries = null;
  }
}
