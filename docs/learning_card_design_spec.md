# 学习卡片设计规格文档

**生成时间**: 2026-06-16T11:00:00+08:00
**设计目的**: 为算法竞赛知识点设计统一的学习卡片结构，让知识点更通俗易懂
**适用范围**: 主图谱所有知识点（当前 item_count = 3240）

## 1. 设计理念

### 1.1 核心目标

**让知识点更易学**：
- 降低理解门槛：用大白话解释复杂概念
- 明确学习路径：清晰的前置和后续关系
- 提供实践指引：具体的学习动作和练习建议
- 避免常见错误：总结易错点和混淆点

### 1.2 设计原则

1. **通俗化**：用最简单的语言解释核心概念
2. **结构化**：统一字段，便于前端展示和用户理解
3. **可操作**：提供具体的学习动作和练习建议
4. **关联化**：明确前置、后续、对比关系
5. **实用性**：聚焦实际应用场景和常见问题

## 2. 学习卡片 Schema 定义

### 2.1 字段列表

| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| `one_sentence_explanation` | string | 是 | 一句话通俗解释 | "动态规划就是把大问题拆成小问题，记住答案避免重复计算" |
| `when_to_use` | string | 是 | 什么时候用 | "当你发现可以用递归解决，但递归会重复计算很多次时" |
| `must_know_before` | array | 是 | 必须前置知识 | ["2.8.1 动态规划基础概念", "2.1 递归思想"] |
| `nice_to_know` | array | 否 | 推荐前置知识 | ["2.3 二分查找", "2.6 贪心算法"] |
| `core_intuition` | string | 是 | 核心直觉/核心思想 | "记住过去，避免重复劳动" |
| `minimal_example` | string | 是 | 最小例子 | "斐波那契数列：f(n) = f(n-1) + f(n-2)，用数组存每个f(i)" |
| `common_traps` | array | 是 | 常见坑/易错点 | ["忘记初始化边界", "状态定义不清晰", "递推顺序错误"] |
| `compare_with` | array | 否 | 易混淆对比 | ["贪心算法（每步最优不一定全局最优）", "分治（分治是分解，DP是记忆）"] |
| `practice_entry` | string | 是 | 练习入口 | "从斐波那契数列开始，然后做背包问题入门题" |
| `learn_next` | array | 是 | 学完继续 | ["背包问题", "区间DP", "状态压缩DP"] |
| `learning_action` | enum | 是 | 学习动作 | "trace" |

### 2.2 学习动作枚举

| 动作 | 描述 | 适用场景 |
|------|------|----------|
| `read` | 阅读理解 | 概念性知识点，需要理解原理 |
| `trace` | 手动推导 | 状态转移、递推过程，需要手动计算几个例子 |
| `code` | 编写代码 | 实现类知识点，需要动手写代码 |
| `prove` | 数学证明 | 定理、公式类知识点，需要理解证明过程 |
| `solve` | 解决问题 | 应用类知识点，需要做练习题 |
| `compare` | 对比理解 | 易混淆知识点，需要对比学习 |

## 3. 字段设计详解

### 3.1 one_sentence_explanation（一句话解释）

**目的**：用最通俗的语言解释核心概念，降低理解门槛。

**设计要点**：
- 长度：建议 50-100 字
- 语言：大白话，避免专业术语
- 重点：抓住本质，不求全面
- 对象：面向初学者

**示例**：
- DP优化：把时间复杂度从O(n²)降到O(n)的方法
- 状态压缩：用二进制数表示集合，节省空间
- 莫比乌斯反演：把复杂计数问题变成简单求和的工具

### 3.2 when_to_use（什么时候用）

**目的**：明确应用场景，帮助用户判断何时使用该知识点。

**设计要点**：
- 具体场景：给出典型问题特征
- 判断标准：如何识别这类问题
- 避免泛泛：不要说"所有问题"

**示例**：
- 状态压缩DP：当状态是集合，集合元素不超过20个时
- 线段树：需要频繁查询和修改区间时
- 莫比乌斯反演：计数问题涉及gcd、约数、质数时

### 3.3 must_know_before（必须前置）

**目的**：明确硬前置依赖，不学这些就无法理解当前知识点。

**数据来源**：
- 主图谱 `direct_pre` 字段
- 人工判断核心前置

**设计要点**：
- 数量：建议 2-5 个
- 优先级：只列出最核心的前置
- 可点击：前端应支持跳转到前置节点

### 3.4 nice_to_know（推荐前置）

**目的**：列出相关前置，学了能更好理解，但不是必须。

**数据来源**：
- 主图谱 `rel` 字段
- 相关但非硬前置的节点

**设计要点**：
- 数量：建议 2-5 个
- 可选性：明确标注为"推荐"
- 价值说明：为什么推荐学这些

### 3.5 core_intuition（核心直觉）

**目的**：用一句话抓住本质，帮助用户快速理解核心思想。

**设计要点**：
- 简洁：一句话，10-30 字
- 直观：用比喻、类比、口诀
- 记忆点：便于记忆和回忆

**示例**：
- DP：记住过去，避免重复
- 状态压缩：二进制表示集合
- 莫比乌斯反演：复杂计数变简单求和

### 3.6 minimal_example（最小例子）

**目的**：用最简单的例子说明核心概念，降低理解门槛。

**设计要点**：
- 简单：最简单的有意义的例子
- 具体：具体数值、具体过程
- 完整：包含输入、过程、输出
- 可推导：用户可以手动推导

**示例**：
- DP：斐波那契数列 f(5) 的计算过程
- 状态压缩：用 3 位二进制表示 {1,2,3} 的子集
- 莫比乌斯反演：求 [1,6] 中与 6 互质的数个数

### 3.7 common_traps（常见坑）

**目的**：总结易错点，帮助用户避免常见错误。

**设计要点**：
- 数量：建议 3-5 个
- 具体：具体的错误场景
- 原因：为什么会错
- 解决：如何避免

**示例**：
- DP：
  - 忘记初始化边界条件
  - 状态定义不清晰
  - 递推顺序错误（应该先算依赖的）
  - 空间优化时覆盖了还需要用的值

### 3.8 compare_with（易混淆对比）

**目的**：列出易混淆的知识点，帮助用户区分。

**设计要点**：
- 对象：确实容易混淆的知识点
- 区别：明确指出关键区别
- 场景：各自适用场景

**示例**：
- DP vs 贪心：
  - 贪心：每步最优，但不保证全局最优
  - DP：考虑所有可能，保证全局最优
  - 场景：贪心适合局部最优能推导全局最优的问题

### 3.9 practice_entry（练习入口）

**目的**：提供练习建议，帮助用户开始实践。

**设计要点**：
- 具体：具体的题目或练习路径
- 难度：从简单到复杂
- 数量：建议 3-5 道题
- 平台：推荐具体平台（如洛谷、Codeforces）

**示例**：
- DP入门：
  - 斐波那契数列（洛谷 P1255）
  - 数字三角形（洛谷 P1216）
  - 背包问题入门（洛谷 P1048）

### 3.10 learn_next（学完继续）

**目的**：明确后续学习路径，帮助用户规划学习。

**数据来源**：
- 反向依赖查找（哪些节点依赖当前节点）
- 相关进阶节点

**设计要点**：
- 数量：建议 3-5 个
- 进阶性：确实是后续进阶内容
- 路径：建议学习顺序

### 3.11 learning_action（学习动作）

**目的**：建议具体的学习方式，帮助用户有效学习。

**推断逻辑**：
- 包含"证明"、"定理" → `prove`
- 包含"实现"、"代码"、"模板" → `code`
- 包含"例题"、"应用" → `solve`
- 包含"对比"、"区别" → `compare`
- 包含"推导"、"过程" → `trace`
- 其他 → `read`

**设计要点**：
- 具体建议：不只是动作名称，还要给出具体建议
- 可操作性：用户能立即执行
- 效果说明：为什么这样学效果好

## 4. 前端展示建议

### 4.1 卡片布局

建议采用**渐进式展开**布局：

```
┌─────────────────────────────────────┐
│ 知识点名称                           │
├─────────────────────────────────────┤
│ 一句话解释（默认展开）                │
│                                     │
│ 核心直觉（默认展开）                  │
│                                     │
│ [展开详情]                           │
└─────────────────────────────────────┘

点击展开后：
┌─────────────────────────────────────┐
│ 知识点名称                           │
├─────────────────────────────────────┤
│ 一句话解释                           │
│                                     │
│ 核心直觉                             │
│                                     │
│ 什么时候用                           │
│                                     │
│ 最小例子                             │
│                                     │
│ 必须前置 [可点击跳转]                │
│                                     │
│ 常见坑                               │
│                                     │
│ 练习入口                             │
│                                     │
│ 学完继续 [可点击跳转]                │
│                                     │
│ 学习动作：trace                      │
│                                     │
│ [更多：推荐前置、易混淆对比]          │
└─────────────────────────────────────┘
```

### 4.2 字段优先级

**第一优先级（默认展开）**：
- one_sentence_explanation
- core_intuition

**第二优先级（点击展开）**：
- when_to_use
- minimal_example
- must_know_before
- common_traps
- practice_entry
- learn_next
- learning_action

**第三优先级（更多详情）**：
- nice_to_know
- compare_with

### 4.3 交互设计

1. **前置跳转**：点击前置节点名称，跳转到对应学习卡片
2. **后续跳转**：点击后续节点名称，跳转到对应学习卡片
3. **练习跳转**：点击练习题目，跳转到题目页面（外部链接）
4. **学习动作提示**：显示具体建议，如"建议手动推导3个例子"

### 4.4 视觉设计

1. **颜色区分**：
   - 必须前置：红色标记
   - 推荐前置：蓝色标记
   - 常见坑：黄色警告
   - 学习动作：绿色提示

2. **图标使用**：
   - 学习动作：用图标表示（如 trace 用笔图标）
   - 常见坑：用警告图标
   - 前置：用箭头图标

3. **排版**：
   - 一句话解释：大字体，突出显示
   - 核心直觉：中等字体，加粗
   - 其他字段：正常字体

## 5. 数据来源与生成

### 5.1 数据来源

| 字段 | 数据来源 | 生成方式 |
|------|----------|----------|
| must_know_before | direct_pre | 自动提取 + 人工筛选 |
| nice_to_know | rel | 自动提取 + 人工筛选 |
| learn_next | 反向依赖 | 需要反向依赖查找 |
| learning_action | 节点名称 | 自动推断 + 人工确认 |
| 其他字段 | 无 | 需要人工填写 |

### 5.2 生成策略

**当前阶段**：只生成样板，不批量生成

**批量生成建议**：
1. **分阶段**：先生成核心节点（review_priority = A/B）
2. **分章节**：按章节逐步生成
3. **人工审核**：每个字段需要人工审核确认
4. **渐进完善**：先生成基础字段，后续补充详细字段

### 5.3 自动化程度

| 字段 | 自动化程度 | 备注 |
|------|-----------|------|
| must_know_before | 高 | 可从 direct_pre 自动提取 |
| nice_to_know | 中 | 可从 rel 自动提取，需人工筛选 |
| learn_next | 低 | 需要反向依赖查找 |
| learning_action | 中 | 可自动推断，需人工确认 |
| 其他字段 | 低 | 需要人工填写 |

## 6. 实施建议

### 6.1 短期目标（1-2周）

1. 完成样板审核：审核当前30个样板，确认字段设计合理性
2. 完善样板内容：为30个样板填写完整内容
3. 前端原型设计：设计学习卡片前端原型
4. 用户测试：邀请用户测试样板卡片

### 6.2 中期目标（1-2月）

1. 扩大样板范围：增加到100个样板节点
2. 优化字段设计：根据用户反馈调整字段
3. 前端实现：实现学习卡片前端展示
4. 部署测试：部署到测试环境

### 6.3 长期目标（3-6月）

1. 批量生成：为核心节点批量生成学习卡片
2. 覆盖扩展：逐步覆盖更多章节和节点
3. 持续优化：根据用户反馈持续优化
4. 数据维护：建立学习卡片数据维护机制

## 7. 风险与挑战

### 7.1 内容质量风险

**风险**：自动生成内容质量不高，不够通俗或准确

**应对**：
- 人工审核每个字段
- 建立内容质量标准
- 用户反馈机制

### 7.2 工作量挑战

**挑战**：3240个节点，每个节点11个字段，工作量巨大

**应对**：
- 分阶段实施
- 优先核心节点
- 建立众包机制
- 开发辅助工具

### 7.3 前端展示挑战

**挑战**：字段多，如何有效展示不显冗余

**应对**：
- 渐进式展开设计
- 字段优先级排序
- 用户可自定义显示字段

### 7.4 数据维护挑战

**挑战**：学习卡片内容需要持续更新和维护

**应对**：
- 建立维护机制
- 版本管理
- 用户贡献机制

## 8. 总结

### 8.1 设计成果

1. ✅ 设计了11个字段的学习卡片 schema
2. ✅ 生成了30个样板节点（每个章节10个）
3. ✅ 提供了前端展示建议
4. ✅ 明确了数据来源和生成策略
5. ✅ 提供了实施建议和风险应对

### 8.2 核心价值

**让知识点更易学**：
- 降低理解门槛：通俗解释 + 最小例子
- 明确学习路径：前置 + 后续 + 练习
- 提供实践指引：学习动作 + 常见坑
- 避免常见错误：常见坑 + 易混淆对比

### 8.3 下一步建议

1. 审核样板：审核30个样板，确认字段设计合理性
2. 完善内容：为样板填写完整内容
3. 前端设计：设计学习卡片前端原型
4. 用户测试：邀请用户测试样板卡片
5. 扩大范围：根据反馈扩大样板范围

---

**结论**: 学习卡片设计合理，字段全面，可有效提升知识点学习体验。建议分阶段实施，优先核心节点，逐步扩大覆盖范围。

## 9. 前端接入准备（新增）

**更新时间**: 2026-06-16T12:00:00+08:00
**审计结论**: 样板数据完全适合前端接入，建议实现adapter层

### 9.1 前端接入审计结果

**审计时间**: 2026-06-16T12:00:00+08:00
**审计工具**: [`tools/audit_learning_card_frontend_readiness.py`](tools/audit_learning_card_frontend_readiness.py)

**审计结果**:
- 样板总数: 30 ✅ PASS
- 通过率: 100.0% ✅ PASS
- 可直接使用: 是 ✅ PASS
- 建议adapter层: 是 ✅ PASS

**详细检查结果**:
- 结构检查: 全部通过（样板总数、章节分布、基本字段）
- 字段检查: 全部通过（7个教学字段无空值）
- 类型检查: 全部通过（list字段类型正确）
- 主图谱校验: 全部通过（item_id存在、名称匹配、章节匹配）

### 9.2 前端字段映射建议

**字段映射表**:

| 样板字段 | 前端字段 | 类型 | 映射原因 |
|----------|----------|------|----------|
| item_id | id | string | 前端统一使用id作为唯一标识 |
| item_name | title | string | 前端统一使用title作为显示标题 |
| section | section_id | string | 前端需要区分章节ID和章节名称 |
| one_sentence_explanation | summary | string | 一句话解释适合作为摘要显示 |
| when_to_use | use_cases | string | 应用场景更适合命名为use_cases |
| core_intuition | intuition | string | 核心直觉简洁命名 |
| minimal_example | example | string | 最小例子统一命名为example |
| common_traps | traps | array | 常见坑简洁命名 |
| practice_entry | practice | string | 练习入口简洁命名 |
| learn_next | next_items | array | 后续学习节点列表 |
| must_know_before | required_pre | array | 必须前置知识 |
| nice_to_know | recommended_pre | array | 推荐前置知识 |
| learning_action | action_type | string | 学习动作类型 |

### 9.3 前端Adapter层设计建议

**建议位置**: `lib/models/learning_card_adapter.dart`

**建议Model定义**:

```dart
class LearningCard {
  final String id;              // 必填
  final String title;           // 必填
  final String sectionId;       // 必填
  final String summary;         // 必填
  final String useCases;        // 必填
  final String intuition;       // 必填
  final String example;         // 必填
  final List<String> traps;     // 必填
  final String practice;        // 必填
  final List<String> nextItems; // 必填
  final List<Map<String, String>> requiredPre;     // 可选
  final List<Map<String, String>> recommendedPre;  // 可选
  final String actionType;      // 必填
  
  LearningCard({
    required this.id,
    required this.title,
    required this.sectionId,
    required this.summary,
    required this.useCases,
    required this.intuition,
    required this.example,
    required this.traps,
    required this.practice,
    required this.nextItems,
    this.requiredPre,
    this.recommendedPre,
    required this.actionType,
  });
}
```

**建议Adapter函数**:

```dart
LearningCard adaptLearningCard(Map<String, dynamic> data) {
  return LearningCard(
    id: data['item_id'] as String,
    title: data['item_name'] as String,
    sectionId: data['section'] as String,
    summary: data['one_sentence_explanation'] as String,
    useCases: data['when_to_use'] as String,
    intuition: data['core_intuition'] as String,
    example: data['minimal_example'] as String,
    traps: (data['common_traps'] as List).cast<String>(),
    practice: data['practice_entry'] as String,
    nextItems: (data['learn_next'] as List).cast<String>(),
    requiredPre: (data['must_know_before'] as List?)?.map((e) => Map<String, String>.from(e)).toList(),
    recommendedPre: (data['nice_to_know'] as List?)?.map((e) => Map<String, String>.from(e)).toList(),
    actionType: data['learning_action'] as String,
  );
}
```

### 9.4 前端接入方案建议

**是否建议前端直接读取当前文件**:
- ✅ 可以直接读取，但建议实现adapter层
- 理由：样板数据结构完整，字段齐全，但字段名与前端习惯不一致

**是否建议实现adapter层**:
- ✅ 强烈建议实现adapter层
- 理由：
  1. 字段名不一致（item_id vs id）
  2. 统一model定义
  3. 便于后续变更
  4. 数据验证和清洗
  5. 解耦数据源和前端

**是否建议生成专门的前端样板数据文件**:
- ❌ 本轮不建议生成前端文件
- 理由：
  1. 避免误导为正式数据
  2. 建议先用adapter层读取现有样板JSON
  3. 待MVP验证后再决定是否生成独立前端文件

### 9.5 前端接入步骤建议

**第一步**: 实现adapter层
- 创建 `lib/models/learning_card_adapter.dart`
- 定义 `LearningCard` model
- 实现 `adaptLearningCard` 和 `adaptLearningCardList` 函数

**第二步**: 加载样板数据
- 从 [`data/learning_card_samples.json`](data/learning_card_samples.json) 加载样板数据
- 使用adapter函数转换为LearningCard model列表

**第三步**: MVP展示
- 实现学习卡片展示UI
- 使用30个样板数据进行展示
- 验证字段映射和数据展示效果

**第四步**: 用户测试
- 邀请用户测试MVP展示
- 收集用户反馈
- 根据反馈调整字段和展示

**第五步**: 决定后续方案
- 根据MVP测试结果决定是否扩大样板范围
- 根据反馈决定是否生成独立前端文件
- 根据需求决定是否批量生成更多学习卡片

### 9.6 相关文件

**审计报告**:
- [`data/learning_card_frontend_readiness.json`](data/learning_card_frontend_readiness.json) - 审计报告JSON
- [`docs/learning_card_frontend_readiness_report.md`](docs/learning_card_frontend_readiness_report.md) - 审计报告Markdown

**样板数据**:
- [`data/learning_card_samples.json`](data/learning_card_samples.json) - 30个样板节点数据（已填充内容）

**填充报告**:
- [`data/learning_card_filled_samples_review.json`](data/learning_card_filled_samples_review.json) - 填充复核报告JSON
- [`docs/learning_card_filled_samples_review.md`](docs/learning_card_filled_samples_review.md) - 填充复核报告Markdown

---

**前端接入结论**: 学习卡片样板数据完全适合前端接入，建议实现adapter层进行字段映射，本轮不生成独立前端文件，先用30个样板跑通MVP展示。