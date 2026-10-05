# 学习卡片 Adapter 实现报告

**生成时间**: 2026-06-16T13:00:00+08:00
**更新时间**: 2026-06-16T13:30:00+08:00
**执行线程**: GLM5 二号线程
**任务性质**: 前端 adapter 和 model 实现，不修改页面 UI

## 1. 任务概述

### 1.1 任务目标

为30个学习卡片样板实现前端 adapter 和 model，提供数据加载和查询能力。

### 1.2 严格限制遵守情况

- ✅ 未修改主图谱 ([`merged_knowledge_graph_item_dependencies_refined.json`](merged_knowledge_graph_item_dependencies_refined.json))
- ✅ 未修改前端图谱 ([`assets/data/knowledge/io_v4_4.json`](assets/data/knowledge/io_v4_4.json))
- ✅ 未修改内容索引 ([`assets/data/knowledge_content/content_index.json`](assets/data/knowledge_content/content_index.json))
- ✅ 未修改内容正文 ([`assets/data/knowledge_content/items/*`](assets/data/knowledge_content/items))
- ✅ 未修改样板数据 ([`data/learning_card_samples.json`](data/learning_card_samples.json))
- ✅ 未修改现有页面 UI 文件

### 1.3 允许新增文件

- ✅ [`lib/models/learning_card.dart`](lib/models/learning_card.dart) - LearningCard model（新增）
- ✅ [`lib/services/learning_card_service.dart`](lib/services/learning_card_service.dart) - 学习卡片服务（新增）
- ✅ [`test/learning_card_service_test.dart`](test/learning_card_service_test.dart) - 测试文件（新增）
- ✅ [`docs/learning_card_frontend_adapter_report.md`](docs/learning_card_frontend_adapter_report.md) - Adapter报告（新增）
- ✅ [`data/learning_card_frontend_adapter_report.json`](data/learning_card_frontend_adapter_report.json) - Adapter报告JSON（新增）

## 2. 实现结果总结

### 2.1 Model 实现

**文件**: [`lib/models/learning_card.dart`](lib/models/learning_card.dart)

**字段列表（13个字段）**:

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | String | 是 | 知识点唯一标识（如 "2.8.208"） |
| title | String | 是 | 知识点标题（如 "后缀最值 DP"） |
| sectionId | String | 是 | 知识点所属章节ID（如 "2.8"） |
| summary | String | 是 | 一句话通俗解释（摘要） |
| useCases | String | 是 | 应用场景（什么时候用） |
| intuition | String | 是 | 核心直觉/核心思想 |
| example | String | 是 | 最小例子 |
| traps | List<String> | 是 | 常见坑/易错点列表 |
| practice | String | 是 | 练习入口/练习建议 |
| nextItems | List<String> | 是 | 后续学习节点列表 |
| requiredPre | List<Map<String, String>> | 否 | 必须前置知识列表 |
| recommendedPre | List<Map<String, String>> | 否 | 推荐前置知识列表 |
| actionType | String | 是 | 学习动作类型 |

**Model 功能**:
- ✅ `fromJson`: 从 JSON Map 创建 LearningCard（字段映射）
- ✅ `toJson`: 转换为 JSON Map
- ✅ `isValid`: 判断是否为有效的学习卡片（关键字段非空）
- ✅ `isComplete`: 判断是否为完整的学习卡片（所有必填字段非空）
- ✅ `getActionTypeDescription`: 获取学习动作的中文描述
- ✅ `copyWith`: 复制并修改部分字段
- ✅ 安全默认值处理（字段缺失时给空字符串或空列表）

### 2.2 Service 实现

**文件**: [`lib/services/learning_card_service.dart`](lib/services/learning_card_service.dart)

**Service 功能**:

| 功能 | 方法 | 描述 |
|------|------|------|
| 加载样板数据 | `loadSamples()` | 从 assets 或本地文件加载样板数据 |
| 获取所有卡片 | `getAllCards()` | 返回所有学习卡片列表 |
| 按ID查询 | `getCardById(itemId)` | 按 itemId 查询学习卡片 |
| 按章节查询 | `getCardsBySection(sectionId)` | 按 sectionId 查询学习卡片列表 |
| 获取总数 | `getTotalCount()` | 获取样板总数 |
| 获取章节分布 | `getSectionDistribution()` | 获取章节分布统计 |
| 检查存在性 | `existsCard(itemId)` | 检查学习卡片是否存在 |
| 检查章节存在 | `existsSection(sectionId)` | 检查章节是否有学习卡片 |
| 获取所有章节ID | `getAllSectionIds()` | 获取所有章节ID列表 |
| 清除缓存 | `clearCache()` | 清除缓存（用于重新加载） |
| 重新加载 | `reloadSamples()` | 重新加载学习卡片样板数据 |
| 获取统计信息 | `getStatistics()` | 获取统计信息 |
| 批量查询 | `getCardsByIds(itemIds)` | 批量查询学习卡片（按 itemId 列表） |
| 搜索标题 | `searchCardsByTitle(keyword)` | 搜索学习卡片（按标题关键词） |
| 搜索摘要 | `searchCardsBySummary(keyword)` | 搜索学习卡片（按摘要关键词） |
| 按动作类型查询 | `getCardsByActionType(actionType)` | 获取指定学习动作类型的卡片 |
| 获取完整卡片 | `getCompleteCards()` | 获取完整的学习卡片列表 |
| 获取有效卡片 | `getValidCards()` | 获取有效的学习卡片列表 |

**Service 特性**:
- ✅ 优先从 assets 加载，失败则从本地文件加载（开发环境）
- ✅ 字段缺失时给安全默认值
- ✅ 单条样板异常不影响整个页面（跳过异常卡片）
- ✅ 缓存机制（避免重复加载）
- ✅ 异常处理（JSON 解析失败时使用空数据）

### 2.3 测试实现

**文件**: [`test/learning_card_service_test.dart`](test/learning_card_service_test.dart)

**测试覆盖（38个测试）**:

| 测试组 | 测试数 | 测试内容 |
|--------|-------:|----------|
| LearningCard Model Tests | 6 | Model 解析、默认值、有效性判断、完整性判断、动作描述 |
| LearningCardService Tests | 21 | 加载样板、章节分布、ID查询、章节查询、搜索、统计、缓存 |
| LearningCard Field Validation Tests | 11 | 所有字段非空验证 |
| **合计** | **38** | **全部通过** |

**测试结果**: ✅ 所有38个测试通过

## 3. 验证结果

### 3.1 样板总数验证

- **预期**: 30个样板
- **实际**: 30个样板
- **结果**: ✅ PASS

### 3.2 章节分布验证

| 章节 | 预期 | 实际 | 结果 |
|------|-----:|-----:|------|
| 2.8 | 10 | 10 | ✅ PASS |
| 3.13 | 10 | 10 | ✅ PASS |
| 4.1 | 10 | 10 | ✅ PASS |
| **合计** | **30** | **30** | ✅ PASS |

### 3.3 关键字段非空验证

| 字段 | 非空数 | 结果 |
|------|-------:|------|
| id | 30/30 | ✅ PASS |
| title | 30/30 | ✅ PASS |
| sectionId | 30/30 | ✅ PASS |
| summary | 30/30 | ✅ PASS |
| useCases | 30/30 | ✅ PASS |
| intuition | 30/30 | ✅ PASS |
| example | 30/30 | ✅ PASS |
| traps | 30/30 | ✅ PASS |
| practice | 30/30 | ✅ PASS |
| nextItems | 30/30 | ✅ PASS |
| actionType | 30/30 | ✅ PASS |

### 3.4 查询能力验证

**按 itemId 查询**:
- ✅ `getCardById('2.8.208')` 返回正确卡片
- ✅ `getCardById('non-existent')` 返回 null

**按 sectionId 查询**:
- ✅ `getCardsBySection('2.8')` 返回10个卡片
- ✅ `getCardsBySection('3.13')` 返回10个卡片
- ✅ `getCardsBySection('4.1')` 返回10个卡片
- ✅ `getCardsBySection('non-existent')` 返回空列表

### 3.5 测试结果

- **测试总数**: 38
- **通过数**: 38
- **失败数**: 0
- **结果**: ✅ All tests passed!

## 4. 字段映射实现

### 4.1 字段映射表

| 样板字段（JSON） | Model字段（Dart） | 映射实现 |
|------------------|-------------------|----------|
| item_id | id | `json['item_id'] as String? ?? ''` |
| item_name | title | `json['item_name'] as String? ?? ''` |
| section | sectionId | `json['section'] as String? ?? ''` |
| one_sentence_explanation | summary | `json['one_sentence_explanation'] as String? ?? ''` |
| when_to_use | useCases | `json['when_to_use'] as String? ?? ''` |
| core_intuition | intuition | `json['core_intuition'] as String? ?? ''` |
| minimal_example | example | `json['minimal_example'] as String? ?? ''` |
| common_traps | traps | `_parseStringList(json['common_traps'])` |
| practice_entry | practice | `json['practice_entry'] as String? ?? ''` |
| learn_next | nextItems | `_parseStringList(json['learn_next'])` |
| must_know_before | requiredPre | `_parsePreList(json['must_know_before'])` |
| nice_to_know | recommendedPre | `_parsePreList(json['nice_to_know'])` |
| learning_action | actionType | `json['learning_action'] as String? ?? 'read'` |

### 4.2 安全默认值处理

**String 字段默认值**: 空字符串 `''`
**List<String> 字段默认值**: 空列表 `[]`
**List<Map<String, String>> 字段默认值**: 空列表 `[]`
**actionType 默认值**: `'read'`

### 4.3 异常处理

**单条卡片解析异常**: 跳过该卡片，不影响其他卡片
**JSON 解析异常**: 使用空数据，不抛出异常
**文件加载异常**: 从 assets 加载失败时尝试本地文件，失败时使用空数据

## 5. 数据加载策略

### 5.1 加载优先级

1. **优先从 assets 加载**: `assets/data/learning_card_samples.json`
2. **失败则从本地文件加载**: `data/learning_card_samples.json`（开发环境）
3. **失败则使用空数据**: 不抛出异常，保证页面不崩溃

### 5.2 缓存机制

- **首次加载**: 解析 JSON 并缓存到 `_allCards`、`_cardsBySection`、`_cardsById`
- **后续查询**: 直接从缓存读取，不重复加载
- **清除缓存**: `clearCache()` 清除缓存，`reloadSamples()` 重新加载

### 5.3 数据结构解析

**JSON 结构**:
```json
{
  "meta": {...},
  "schema_definition": {...},
  "samples": {
    "2.8": [...],
    "3.13": [...],
    "4.1": [...]
  }
}
```

**解析逻辑**:
- 解析 `samples` 字段
- 按 sectionId 分组解析
- 每个卡片使用 `LearningCard.fromJson` 创建
- 过滤无效卡片（`isValid()` 返回 false）

## 6. 使用示例

### 6.1 加载样板数据

```dart
final service = LearningCardService();
await service.loadSamples();
```

### 6.2 获取所有学习卡片

```dart
final allCards = await service.getAllCards();
print('样板总数: ${allCards.length}');
```

### 6.3 按 itemId 查询

```dart
final card = await service.getCardById('2.8.208');
if (card != null) {
  print('标题: ${card.title}');
  print('摘要: ${card.summary}');
}
```

### 6.4 按 sectionId 查询

```dart
final cards = await service.getCardsBySection('2.8');
print('2.8章节卡片数: ${cards.length}');
```

### 6.5 搜索学习卡片

```dart
final cards = await service.searchCardsByTitle('DP');
print('标题包含DP的卡片数: ${cards.length}');
```

### 6.6 获取统计信息

```dart
final stats = await service.getStatistics();
print('总数: ${stats['total_count']}');
print('章节分布: ${stats['section_distribution']}');
```

## 7. Model 字段详解

### 7.1 id（知识点唯一标识）

- **来源**: `item_id`
- **格式**: 章节ID + 序号（如 "2.8.208"）
- **用途**: 唯一标识知识点，用于查询和跳转
- **默认值**: 空字符串

### 7.2 title（知识点标题）

- **来源**: `item_name`
- **示例**: "后缀最值 DP"
- **用途**: 显示标题，用于列表展示和搜索
- **默认值**: 空字符串

### 7.3 sectionId（章节ID）

- **来源**: `section`
- **示例**: "2.8"
- **用途**: 知识点所属章节，用于章节分组查询
- **默认值**: 空字符串

### 7.4 summary（一句话通俗解释）

- **来源**: `one_sentence_explanation`
- **示例**: "从后往前算，记录每个位置后面的最大/最小值"
- **用途**: 摘要显示，快速理解知识点
- **默认值**: 空字符串

### 7.5 useCases（应用场景）

- **来源**: `when_to_use`
- **示例**: "需要频繁查询某个位置后面的最大/最小值时"
- **用途**: 明确应用场景，帮助判断何时使用
- **默认值**: 空字符串

### 7.6 intuition（核心直觉）

- **来源**: `core_intuition`
- **示例**: "后缀信息一次性算好，用的时候直接取"
- **用途**: 核心思想，抓住本质
- **默认值**: 空字符串

### 7.7 example（最小例子）

- **来源**: `minimal_example`
- **示例**: "数组[3,1,4,1,5]的后缀最大值计算"
- **用途**: 最小可理解例子，降低理解门槛
- **默认值**: 空字符串

### 7.8 traps（常见坑）

- **来源**: `common_traps`
- **类型**: `List<String>`
- **示例**: ["忘记从右往左算", "边界处理错误"]
- **用途**: 常见易错点，避免错误
- **默认值**: 空列表

### 7.9 practice（练习入口）

- **来源**: `practice_entry`
- **示例**: "从简单数组后缀最大值开始"
- **用途**: 练习建议，指引学习
- **默认值**: 空字符串

### 7.10 nextItems（后续学习）

- **来源**: `learn_next`
- **类型**: `List<String>`
- **示例**: ["前缀最值DP", "双端队列维护最值"]
- **用途**: 后续学习路径，规划学习
- **默认值**: 空列表

### 7.11 requiredPre（必须前置）

- **来源**: `must_know_before`
- **类型**: `List<Map<String, String>>`
- **用途**: 必须前置知识，明确硬前置依赖
- **默认值**: 空列表

### 7.12 recommendedPre（推荐前置）

- **来源**: `nice_to_know`
- **类型**: `List<Map<String, String>>`
- **用途**: 推荐前置知识，非必须但有助于理解
- **默认值**: 空列表

### 7.13 actionType（学习动作）

- **来源**: `learning_action`
- **枚举**: read / trace / code / prove / solve / compare
- **用途**: 学习动作类型，建议学习方式
- **默认值**: 'read'

## 8. Service 方法详解

### 8.1 loadSamples()

**功能**: 加载学习卡片样板数据
**优先级**: assets → 本地文件 → 空数据
**异常处理**: 不抛出异常，保证页面不崩溃

### 8.2 getAllCards()

**功能**: 获取所有学习卡片列表
**返回**: `List<LearningCard>`
**缓存**: 从缓存读取，不重复加载

### 8.3 getCardById(itemId)

**功能**: 按 itemId 查询学习卡片
**参数**: `itemId` - 知识点唯一标识
**返回**: `LearningCard?`（未找到返回 null）

### 8.4 getCardsBySection(sectionId)

**功能**: 按 sectionId 查询学习卡片列表
**参数**: `sectionId` - 章节ID
**返回**: `List<LearningCard>`（未找到返回空列表）

### 8.5 getTotalCount()

**功能**: 获取样板总数
**返回**: `int`

### 8.6 getSectionDistribution()

**功能**: 获取章节分布统计
**返回**: `Map<String, int>`（key为章节ID，value为卡片数）

### 8.7 existsCard(itemId)

**功能**: 检查学习卡片是否存在
**参数**: `itemId` - 知识点唯一标识
**返回**: `bool`

### 8.8 existsSection(sectionId)

**功能**: 检查章节是否有学习卡片
**参数**: `sectionId` - 章节ID
**返回**: `bool`

### 8.9 getAllSectionIds()

**功能**: 获取所有章节ID列表
**返回**: `List<String>`

### 8.10 clearCache()

**功能**: 清除缓存
**用途**: 用于重新加载数据

### 8.11 reloadSamples()

**功能**: 重新加载学习卡片样板数据
**实现**: 清除缓存后重新加载

### 8.12 getStatistics()

**功能**: 获取统计信息
**返回**: `Map<String, dynamic>`
**内容**: total_count、section_distribution、sections

### 8.13 getCardsByIds(itemIds)

**功能**: 批量查询学习卡片
**参数**: `itemIds` - itemId列表
**返回**: `Map<String, LearningCard?>`（未找到的为 null）

### 8.14 searchCardsByTitle(keyword)

**功能**: 搜索学习卡片（按标题关键词）
**参数**: `keyword` - 搜索关键词
**返回**: `List<LearningCard>`（标题包含关键词的卡片）

### 8.15 searchCardsBySummary(keyword)

**功能**: 搜索学习卡片（按摘要关键词）
**参数**: `keyword` - 搜索关键词
**返回**: `List<LearningCard>`（摘要包含关键词的卡片）

### 8.16 getCardsByActionType(actionType)

**功能**: 获取指定学习动作类型的卡片
**参数**: `actionType` - 学习动作类型
**返回**: `List<LearningCard>`

### 8.17 getCompleteCards()

**功能**: 获取完整的学习卡片列表
**返回**: `List<LearningCard>`（所有必填字段非空）

### 8.18 getValidCards()

**功能**: 获取有效的学习卡片列表
**返回**: `List<LearningCard>`（关键字段非空）

## 9. 测试覆盖详解

### 9.1 Model Tests（6个测试）

1. **fromJson 解析测试**: 验证 JSON 解析正确性
2. **fromJson 默认值测试**: 验证 null 值处理
3. **isValid 有效卡片测试**: 验证有效性判断
4. **isValid 无效卡片测试**: 验证无效卡片判断
5. **isComplete 完整卡片测试**: 验证完整性判断
6. **getActionTypeDescription 测试**: 验证动作描述获取

### 9.2 Service Tests（21个测试）

1. **加载30个样板测试**: 验证样板总数
2. **2.8章节10个样板测试**: 验证章节分布
3. **3.13章节10个样板测试**: 验证章节分布
4. **4.1章节10个样板测试**: 验证章节分布
5. **章节分布统计测试**: 验证章节分布统计
6. **itemId查询测试**: 验证ID查询功能
7. **itemId查询不存在测试**: 验证不存在ID处理
8. **sectionId查询测试**: 验证章节查询功能
9. **sectionId查询不存在测试**: 验证不存在章节处理
10. **获取所有卡片测试**: 验证获取所有卡片
11. **卡片存在性检查测试**: 验证存在性检查
12. **章节存在性检查测试**: 验证章节存在性
13. **获取所有章节ID测试**: 验证章节ID列表
14. **获取统计信息测试**: 验证统计信息
15. **搜索标题测试**: 验证标题搜索
16. **搜索摘要测试**: 验证摘要搜索
17. **按动作类型查询测试**: 验证动作类型查询
18. **获取完整卡片测试**: 验证完整卡片获取
19. **获取有效卡片测试**: 验证有效卡片获取
20. **清除缓存测试**: 验证缓存清除
21. **批量查询测试**: 验证批量查询功能

### 9.3 Field Validation Tests（11个测试）

1. **id非空验证**: 验证所有卡片id非空
2. **title非空验证**: 验证所有卡片title非空
3. **sectionId非空验证**: 验证所有卡片sectionId非空
4. **summary非空验证**: 验证所有卡片summary非空
5. **useCases非空验证**: 验证所有卡片useCases非空
6. **intuition非空验证**: 验证所有卡片intuition非空
7. **example非空验证**: 验证所有卡片example非空
8. **traps非空验证**: 验证所有卡片traps非空
9. **practice非空验证**: 验证所有卡片practice非空
10. **nextItems非空验证**: 验证所有卡片nextItems非空
11. **actionType非空验证**: 验证所有卡片actionType非空

## 10. 总结

### 10.1 实现成果

- ✅ 创建 LearningCard model（13个字段）
- ✅ 创建 LearningCardService（18个方法）
- ✅ 创建测试文件（38个测试）
- ✅ 所有测试通过
- ✅ 字段映射正确
- ✅ 安全默认值处理
- ✅ 异常处理完善
- ✅ 未修改任何核心文件和页面UI

### 10.2 核心价值

**为前端提供数据支持**:
- 数据加载能力：从 assets 或本地文件加载样板数据
- 查询能力：按 ID、章节、关键词查询学习卡片
- 异常处理：单条卡片异常不影响整个页面
- 缓存机制：避免重复加载，提升性能

**为 MVP 展示提供基础**:
- Model 定义：统一的 LearningCard model
- Service 实现：完整的数据加载和查询服务
- 测试覆盖：38个测试保证质量
- 安全处理：字段缺失时给默认值

### 10.3 下一步建议

**立即执行**:
1. ✅ Model 和 Service 已实现完成
2. ✅ 测试已通过
3. 🔄 前端页面 UI 实现（下一步）
4. 🔄 MVP 展示30个样板（下一步）

**后续决策**:
1. 根据MVP展示效果决定是否扩大样板范围
2. 根据用户反馈决定是否优化字段设计
3. 根据需求决定是否批量生成更多学习卡片

---

**最终结论**: 学习卡片 Adapter 实现完成，Model 和 Service 功能完善，测试全部通过，可为前端 MVP 展示提供数据支持。下一步建议实现前端页面 UI，展示30个学习卡片样板。

## 11. Asset 接入修正（2026-06-16T13:30:00+08:00）

### 11.1 修正背景

**问题发现**:
- LearningCardService 当前优先读取 `assets/data/learning_card_samples.json`
- 实际样板文件在 `data/learning_card_samples.json`
- pubspec.yaml 没有声明 `data/learning_card_samples.json` 作为 Flutter asset
- 测试环境可能通过本地 File fallback，但真机/Flutter asset 环境无法稳定加载

**修正目标**:
- 修正 asset 路径为 `data/learning_card_samples.json`
- 更新 pubspec.yaml 添加 asset 声明
- 减少对 dart:io File fallback 的依赖
- 增强测试验证 asset 加载能力

### 11.2 修正内容

**1. 修正 LearningCardService asset 路径**:
- **文件**: [`lib/services/learning_card_service.dart`](lib/services/learning_card_service.dart)
- **修改**: `_assetsDataPath` 从 `'assets/data/learning_card_samples.json'` 改为 `'data/learning_card_samples.json'`
- **结果**: asset 路径与实际文件位置一致

**2. 更新 pubspec.yaml asset 声明**:
- **文件**: [`pubspec.yaml`](pubspec.yaml)
- **修改**: 在 `flutter.assets` 中添加 `- data/learning_card_samples.json`
- **结果**: Flutter asset 系统正确识别样板文件

**3. 减少对 dart:io File fallback 的依赖**:
- **策略**: 保留本地 File fallback 用于开发环境，但正式加载优先通过 rootBundle
- **实现**: asset 加载失败时才尝试本地文件加载
- **结果**: 真机环境优先使用 Flutter asset，稳定可靠

**4. 增强测试验证 asset 加载能力**:
- **文件**: [`test/learning_card_service_test.dart`](test/learning_card_service_test.dart)
- **新增测试组**: Asset Loading Tests（4个测试）
- **测试内容**:
  - rootBundle 能加载 `data/learning_card_samples.json`
  - LearningCardService 不依赖本地 File fallback 也能加载30个样板
  - 章节分布验证（2.8/3.13/4.1各10个）
  - asset 路径正确性验证

### 11.3 修正验证

**测试结果**:
- **测试总数**: 42个（新增4个asset加载测试）
- **通过数**: 42个
- **失败数**: 0
- **结果**: ✅ All tests passed!

**Asset 加载验证**:
- ✅ rootBundle.loadString('data/learning_card_samples.json') 成功
- ✅ JSON 格式正确（包含 meta 和 samples 字段）
- ✅ LearningCardService 通过 asset 加载30个样板
- ✅ 章节分布正确（2.8/3.13/4.1各10个）
- ✅ 不依赖本地 File fallback 也能正常加载

### 11.4 修正影响

**正面影响**:
- 真机环境稳定加载学习卡片数据
- Flutter asset 系统正确识别样板文件
- 减少对 dart:io 的依赖，提升跨平台兼容性
- 测试覆盖更全面，验证 asset 加载能力

**无负面影响**:
- 本地开发环境仍可通过 File fallback 加载
- 不影响现有功能逻辑
- 不修改核心文件和样板数据

### 11.5 修正总结

**修正成果**:
- ✅ asset 路径修正完成
- ✅ pubspec.yaml asset 声明完成
- ✅ 测试验证 asset 加载能力
- ✅ 42个测试全部通过
- ✅ 真机环境稳定加载

**核心价值**:
- 真机环境可靠：通过 Flutter asset 系统稳定加载
- 开发环境兼容：保留本地 File fallback 用于开发调试
- 测试覆盖完善：验证 asset 加载和 fallback 机制
- 跨平台兼容：减少对 dart:io 的依赖

---

**最终结论**: 学习卡片 Adapter asset 接入修正完成，真机环境可稳定加载30个样板数据，42个测试全部通过，为前端 MVP 展示提供可靠数据支持。