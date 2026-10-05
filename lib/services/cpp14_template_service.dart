import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/cpp14_template_entry.dart';

/// C++14 模板入口服务
/// 负责从 data/cpp14_template_mvp_index.json 加载模板入口数据
class Cpp14TemplateService {
  static const String _dataPath = 'data/cpp14_template_mvp_index.json';

  Map<String, Cpp14TemplateEntry>? _entriesById;
  List<Cpp14TemplateEntry>? _allEntries;

  /// 加载模板入口数据
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
          final entry = Cpp14TemplateEntry.fromJson(
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

  /// 按 itemId 查询模板入口，未找到返回 null
  Future<Cpp14TemplateEntry?> getEntryByItemId(String itemId) async {
    await load();
    return _entriesById?[itemId];
  }

  /// 获取所有模板入口
  Future<List<Cpp14TemplateEntry>> getAllEntries() async {
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
