import 'dart:convert';
import 'dart:io';
import 'package:flutter/services.dart';
import '../models/learning_card.dart';

/// 学习卡片服务
/// 负责加载和管理学习卡片样板数据
class LearningCardService {
  /// 所有学习卡片缓存
  List<LearningCard>? _allCards;

  /// 按 sectionId 分组的学习卡片缓存
  Map<String, List<LearningCard>>? _cardsBySection;

  /// 按 id 索引的学习卡片缓存
  Map<String, LearningCard>? _cardsById;

  /// 样板数据文件路径（Flutter assets）
  static const String _assetsDataPath = 'data/learning_card_samples.json';

  /// 样板数据文件路径（本地开发环境 fallback）
  static const String _localDataPath = 'data/learning_card_samples.json';

  /// 加载学习卡片样板数据
  /// 优先从 assets 加载，失败则从本地文件加载
  Future<void> loadSamples() async {
    try {
      // 尝试从 assets 加载
      final jsonString = await rootBundle.loadString(_assetsDataPath);
      _parseAndCache(jsonString);
    } catch (e) {
      // assets 加载失败，尝试从本地文件加载（开发环境）
      try {
        final file = File(_localDataPath);
        if (await file.exists()) {
          final jsonString = await file.readAsString();
          _parseAndCache(jsonString);
        } else {
          // 文件不存在，使用空数据
          _allCards = [];
          _cardsBySection = {};
          _cardsById = {};
        }
      } catch (e) {
        // 本地文件加载失败，使用空数据
        _allCards = [];
        _cardsBySection = {};
        _cardsById = {};
      }
    }
  }

  /// 解析 JSON 字符串并缓存数据
  void _parseAndCache(String jsonString) {
    try {
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      final samples = jsonData['samples'] as Map<String, dynamic>?;

      if (samples == null) {
        _allCards = [];
        _cardsBySection = {};
        _cardsById = {};
        return;
      }

      // 解析所有学习卡片
      _allCards = [];
      _cardsBySection = {};
      _cardsById = {};

      for (final sectionId in samples.keys) {
        final sectionCards = samples[sectionId] as List<dynamic>?;
        if (sectionCards == null) continue;

        final cards = <LearningCard>[];
        for (final cardData in sectionCards) {
          try {
            final card = LearningCard.fromJson(cardData as Map<String, dynamic>);
            if (card.isValid()) {
              cards.add(card);
              _cardsById![card.id] = card;
            }
          } catch (e) {
            // 单条卡片解析失败，跳过，不影响其他卡片
            continue;
          }
        }

        _cardsBySection![sectionId] = cards;
        _allCards!.addAll(cards);
      }
    } catch (e) {
      // JSON 解析失败，使用空数据
      _allCards = [];
      _cardsBySection = {};
      _cardsById = {};
    }
  }

  /// 获取所有学习卡片
  /// 如果未加载，会自动加载
  Future<List<LearningCard>> getAllCards() async {
    if (_allCards == null) {
      await loadSamples();
    }
    return _allCards ?? [];
  }

  /// 按 itemId 查询学习卡片
  /// 返回 null 表示未找到
  Future<LearningCard?> getCardById(String itemId) async {
    if (_cardsById == null) {
      await loadSamples();
    }
    return _cardsById?[itemId];
  }

  /// 按 sectionId 查询学习卡片列表
  /// 返回空列表表示该章节无卡片
  Future<List<LearningCard>> getCardsBySection(String sectionId) async {
    if (_cardsBySection == null) {
      await loadSamples();
    }
    return _cardsBySection?[sectionId] ?? [];
  }

  /// 获取样板总数
  Future<int> getTotalCount() async {
    final cards = await getAllCards();
    return cards.length;
  }

  /// 获取章节分布统计
  Future<Map<String, int>> getSectionDistribution() async {
    if (_cardsBySection == null) {
      await loadSamples();
    }

    final distribution = <String, int>{};
    for (final sectionId in _cardsBySection?.keys ?? <String>[]) {
      distribution[sectionId] = _cardsBySection?[sectionId]?.length ?? 0;
    }
    return distribution;
  }

  /// 检查学习卡片是否存在
  Future<bool> existsCard(String itemId) async {
    final card = await getCardById(itemId);
    return card != null;
  }

  /// 检查章节是否有学习卡片
  Future<bool> existsSection(String sectionId) async {
    final cards = await getCardsBySection(sectionId);
    return cards.isNotEmpty;
  }

  /// 获取所有章节ID列表
  Future<List<String>> getAllSectionIds() async {
    if (_cardsBySection == null) {
      await loadSamples();
    }
    return _cardsBySection?.keys.toList() ?? [];
  }

  /// 清除缓存（用于重新加载数据）
  void clearCache() {
    _allCards = null;
    _cardsBySection = null;
    _cardsById = null;
  }

  /// 重新加载学习卡片样板数据
  Future<void> reloadSamples() async {
    clearCache();
    await loadSamples();
  }

  /// 获取统计信息
  Future<Map<String, dynamic>> getStatistics() async {
    final totalCount = await getTotalCount();
    final sectionDistribution = await getSectionDistribution();

    return {
      'total_count': totalCount,
      'section_distribution': sectionDistribution,
      'sections': sectionDistribution.keys.toList(),
    };
  }

  /// 批量查询学习卡片（按 itemId 列表）
  /// 返回 Map，key 为 itemId，value 为 LearningCard（未找到的为 null）
  Future<Map<String, LearningCard?>> getCardsByIds(List<String> itemIds) async {
    final result = <String, LearningCard?>{};
    for (final itemId in itemIds) {
      result[itemId] = await getCardById(itemId);
    }
    return result;
  }

  /// 搜索学习卡片（按标题关键词）
  /// 返回标题包含关键词的学习卡片列表
  Future<List<LearningCard>> searchCardsByTitle(String keyword) async {
    final allCards = await getAllCards();
    if (keyword.isEmpty) return allCards;

    return allCards.where((card) {
      return card.title.toLowerCase().contains(keyword.toLowerCase());
    }).toList();
  }

  /// 搜索学习卡片（按摘要关键词）
  /// 返回摘要包含关键词的学习卡片列表
  Future<List<LearningCard>> searchCardsBySummary(String keyword) async {
    final allCards = await getAllCards();
    if (keyword.isEmpty) return allCards;

    return allCards.where((card) {
      return card.summary.toLowerCase().contains(keyword.toLowerCase());
    }).toList();
  }

  /// 搜索学习卡片（按学习动作类型）
  /// 返回指定学习动作类型的学习卡片列表
  Future<List<LearningCard>> getCardsByActionType(String actionType) async {
    final allCards = await getAllCards();
    return allCards.where((card) {
      return card.actionType == actionType;
    }).toList();
  }

  /// 获取完整的学习卡片列表（所有必填字段非空）
  Future<List<LearningCard>> getCompleteCards() async {
    final allCards = await getAllCards();
    return allCards.where((card) => card.isComplete()).toList();
  }

  /// 获取有效的学习卡片列表（关键字段非空）
  Future<List<LearningCard>> getValidCards() async {
    final allCards = await getAllCards();
    return allCards.where((card) => card.isValid()).toList();
  }
}