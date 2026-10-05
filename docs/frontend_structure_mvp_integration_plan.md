# 前端结构 MVP 总集成方案

## 审计时间

2026-06-16

## 审计范围

- Flutter 前端结构（lib/ 目录下 16 个页面、23 个 model、14 个 repository、19 个 provider）
- 6 个数据源 JSON
- 3240 知识点主图谱

---

## 一、现有前端结构审计

### 1.1 页面清单

| 页面 | 文件 | 状态 | MVP 关联 |
|------|------|------|----------|
| HomePage | home_page.dart | 已有，基础功能 | **需增强** |
| KnowledgeMapPage | knowledge_map_page.dart | 已有，大类→章节列表 | 保持 |
| KnowledgeSectionPage | knowledge_section_page.dart | 已有，平铺所有 items | **需增强** |
| KnowledgeItemPage | knowledge_item_page.dart | 已有，详情+动画+前置 | **需增强** |
| CppLearningUnitPage | cpp_learning_unit_page.dart | 已有 | 保持 |
| CppAnimationPage | cpp_animation_page.dart | 已有 | 保持 |
| CppSearchPage | cpp_search_page.dart | 已有 | 保持 |
| CppSectionQuizPage | cpp_section_quiz_page.dart | 已有 | 保持 |
| CppBasicPathPage | cpp_basic_path_page.dart | 已有 | 保持 |
| ProgressPage | progress_page.dart | 已有 | 保持 |
| SettingsPage | settings_page.dart | 已有 | 保持 |
| LessonPage | lesson_page.dart | 已有（BFS 专用） | 保持 |
| AnimationPage | animation_page.dart | 已有（BFS 专用） | 保持 |
| QuizPage | quiz_page.dart | 已有（BFS 专用） | 保持 |
| MistakePage | mistake_page.dart | 已有（BFS 专用） | 保持 |
| TeacherModePage | teacher_mode_page.dart | 已有（BFS 专用） | 保持 |

### 1.2 数据流

```
io_v4_4.json → KnowledgeGraphRepository → KnowledgeGraphProvider → 各页面
cpp_animation_manifest.json → CppAnimationRepository → CppAnimationProvider → KnowledgeItemPage
progress (SharedPreferences) → ProgressService → ProgressProvider → HomePage/ItemPage
```

### 1.3 关键缺失

| 缺失项 | 说明 |
|--------|------|
| 分层数据加载 | 无 provider 加载 learning_path_layers_frontend_usage_review.json |
| 学习卡片加载 | 无 provider 加载 learning_card_samples.json |
| 学习路径加载 | 无 provider 加载 dependency_to_learning_path.json |
| 题目引用加载 | 无 provider 加载 problem_refs_seed.json |
| KnowledgeItem 无 layer 字段 | model 中无 frontend_display_layer / graph_layer |
| KnowledgeSection 无折叠策略 | model 中无 overcrowded_collapse_policy |
| 首页无推荐入口 | 无"今日学习目标"、"推荐章节"区域 |

---

## 二、首页接入方案

### 2.1 现有结构

```
HomePage
├── _buildHeader()           — 品牌卡片（算法通）
├── _buildContinueLearning() — 继续学习 / 开始学习
├── _SectionLabel('学习入口')
├── _HomeCard('知识地图')
├── _HomeCard('搜索知识点')
├── _HomeCard('学习进度')
└── _HomeCard('设置')
```

### 2.2 MVP 增强方案

```
HomePage（增强后）
├── _buildHeader()                    — 保持
├── _buildContinueLearning()          — 保持，增强为显示最近 3 个知识点
├── _SectionLabel('推荐入口')          — 新增
│   ├── _HomeCard('C++ 基础')         — 跳转 1.1~1.10 章节（core_ratio ≥ 0.8）
│   ├── _HomeCard('算法入门')          — 跳转 2.3/2.5/2.7 章节（core_ratio ≥ 0.5）
│   └── _HomeCard('数据结构基础')      — 跳转 3.1/3.2/3.5 章节（core_ratio ≥ 0.5）
├── _SectionLabel('今日学习目标')       — 新增占位
│   └── _HomeCard('设置今日目标')       — 占位，暂不实现逻辑
├── _SectionLabel('学习入口')          — 保持
│   ├── _HomeCard('知识地图')
│   ├── _HomeCard('搜索知识点')
│   ├── _HomeCard('学习进度')
│   └── _HomeCard('设置')
```

### 2.3 数据来源

| 区域 | 数据来源 | 状态 |
|------|----------|------|
| 继续学习 | progress_provider（已有） | **可直接用** |
| 推荐入口 | recommended_homepage_entry_sections（learning_path_layers_frontend_usage_review.json） | 需新增 provider |
| 今日学习目标 | 无 | **占位，不实现** |

### 2.4 推荐入口章节

来自 `recommended_homepage_entry_sections`，按 core_ratio 排序：

**high 优先级（core_ratio ≥ 0.8）：**
- 1.1 程序基本结构 (1.0)
- 1.2 输入输出 (1.0)
- 1.4 运算符 (1.0)
- 1.9 预处理与代码组织 (0.929)
- 1.8 结构体与 STL (0.889)
- 1.10 常见易错点 (0.867)
- 3.1 线性结构 (0.833)
- 1.5 控制结构 (0.818)
- 1.3 数据类型与变量 (0.8)

**medium 优先级（core_ratio 0.5~0.8）：**
- 3.2 栈与队列 (0.706)
- 1.7 函数递归引用指针 (0.705)
- 3.5 堆 (0.692)
- 2.5 双指针与滑动窗口 (0.652)
- 2.3 二分与答案搜索 (0.621)
- 2.7 搜索 (core_ratio=0.564, foldable_ratio=0.021)
- 4.5 图与树的数学基础 (0.543)
- 4.6 概率与期望 (0.541)

---

## 三、章节页接入方案

### 3.1 现有结构

```
KnowledgeSectionPage
├── _buildHeader(section)        — 章节名 + level 标签
├── _buildTagRow('前置章节')      — section.pre
├── _buildTagRow('相关章节')      — section.rel
└── section.items.map(_ItemCard) — 平铺所有 items，无分层
```

### 3.2 MVP 增强方案

```
KnowledgeSectionPage（增强后）
├── _buildHeader(section)              — 保持，增加分层统计标签
├── _buildLayerSummary()               — 新增：core/standard/advanced/optional 计数
├── _buildTagRow('前置章节')            — 保持
├── _buildTagRow('相关章节')            — 保持
├── _buildLearningPathEntry()          — 新增：学习路径入口（如有）
├── _SectionLabel('核心主线 (core)')    — 默认展开
│   └── core items
├── _SectionLabel('常用进阶 (standard)') — 默认显示
│   └── standard items
├── _SectionLabel('专题扩展 (advanced)') — 默认折叠
│   └── advanced items（ExpansionTile）
└── _SectionLabel('冷门/可选 (optional)') — 深度折叠
    └── optional items（ExpansionTile）
```

### 3.3 高拥挤章节折叠策略

来自 `overcrowded_section_collapse_policy`：

| 章节 | 章节总数 | core | standard | advanced | optional | 可折叠比例 | 默认策略 |
|------|----------|------|----------|----------|----------|------------|----------|
| 2.8 动态规划 | 292 | 2 | 104 | 171 | 15 | 0.637 | 折叠 advanced+optional |
| 3.13 高级数据结构扩展 | 374 | 46 | 117 | 158 | 53 | 0.564 | 折叠 advanced+optional |
| 2.21 高级图论扩展 | 186 | 0 | 13 | 129 | 44 | 0.930 | 折叠 advanced+optional |
| 2.10 字符串算法 | 81 | 12 | 11 | 33 | 25 | 0.716 | 折叠 advanced+optional |
| 2.9 图基础与遍历 | 204 | 35 | 90 | 74 | 5 | 0.387 | 折叠 optional |
| 4.1 整数与数论基础 | 193 | 26 | 140 | 27 | 0 | 0.140 | 不默认折叠 |
| 2.7 搜索 | 94 | 53 | 39 | 2 | 0 | 0.021 | 不默认折叠 |

**实现建议：**
- 总数 ≥ 60 且可折叠比例 > 0.5：默认折叠 advanced+optional
- 总数 ≥ 60 且可折叠比例 0.3~0.5：默认折叠 optional
- 其他：不默认折叠

### 3.4 章节学习路径入口

来自 `dependency_to_learning_path.json`，当前仅覆盖 3 个章节（2.8/3.13/4.1）。

**MVP 策略：**
- 仅在 2.8/3.13/4.1 章节页显示"学习路径"入口按钮
- 点击后跳转到学习路径页面（新页面，展示该章节的推荐学习顺序）
- 其他章节暂不显示学习路径入口

### 3.5 数据来源

| 区域 | 数据来源 | 状态 |
|------|----------|------|
| 分层标签 | learning_path_layers_frontend_usage_review.json → suspected_misclassified_core + frontend_layer_totals | 需新增 provider |
| 折叠策略 | overcrowded_section_collapse_policy | 同上 |
| 学习路径 | dependency_to_learning_path.json | 需新增 provider + 页面 |

---

## 四、知识点页接入方案

### 4.1 现有结构

```
KnowledgeItemPage
├── _buildHeader(item, section)       — ID + 章节名 + 名称
├── _buildCppLearnCard()              — "开始学习"入口（C++/算法/数学项）
├── _buildCppAnimationCard()          — 动画入口（C++ 项，从 manifest 查找）
├── _buildBfsActionsGroup()           — BFS 专用学习工具
├── _buildTagSection('别名')          — alias
├── _buildClickableRefSection('直接前置') — directPre
├── _buildClickableRefSection('展开前置') — resolvedPre
├── _buildClickableRefSection('相关知识') — rel
├── _buildInfoRow('pickup_group')     — 元数据
└── _buildInfoRow('block_id')         — 元数据
```

### 4.2 MVP 增强方案

```
KnowledgeItemPage（增强后）
├── _buildHeader(item, section)           — 保持，增加 frontend_display_layer 标签
├── _buildLearningCard()                  — 新增：学习卡片区域
│   ├── one_sentence_explanation          — 一句话解释
│   ├── core_intuition                   — 核心直觉
│   ├── when_to_use                      — 什么时候用
│   └── minimal_example                  — 最小例子
├── _buildCppLearnCard()                  — 保持
├── _buildCppAnimationCard()              — 保持
├── _buildPrerequisiteSection()           — 增强：区分 must_know / nice_to_know
│   ├── "必须掌握" (must_know_before)    — 高亮显示
│   └── "推荐了解" (nice_to_know)        — 淡色显示
├── _buildLearnNextSection()              — 新增：学完继续
│   └── learn_next 列表（可点击跳转）
├── _buildPracticeEntry()                 — 新增：练习入口
│   └── practice_entry 文字 + 题目链接
├── _buildBfsActionsGroup()               — 保持
├── _buildTagSection('别名')              — 保持
├── _buildClickableRefSection('直接前置') — 保持
├── _buildClickableRefSection('展开前置') — 保持
├── _buildClickableRefSection('相关知识') — 保持
├── _buildCommonTraps()                   — 新增：常见坑
├── _buildCompareWith()                   — 新增：易混淆对比
└── _buildInfoRow(...)                    — 保持
```

### 4.3 学习卡片

来自 `learning_card_samples.json`，当前仅 30 个样板（2.8/3.13/4.1 章节）。

**MVP 策略：**
- 有卡片的节点：显示学习卡片区域
- 无卡片的节点：不显示（非空判断，优雅降级）
- 卡片字段优先级：
  1. one_sentence_explanation（必须）
  2. core_intuition（必须）
  3. when_to_use（推荐）
  4. minimal_example（推荐）
  5. common_traps / compare_with（可选）

### 4.4 动画入口

来自 `cpp_animation_manifest.json`，当前 115 个动画。

**现有逻辑已完善：**
- `cppAnimationsForItemProvider(item.id)` 查询该知识点关联动画
- 有动画时显示"动画演示（N）"卡片
- 点击跳转 CppAnimationPage

**MVP 无需修改。**

### 4.5 练习入口

来自 `problem_refs_seed.json`，当前 20 条题目引用。

**MVP 策略：**
- 仅显示有 linked_items 匹配当前 itemId 的题目
- 显示题目名 + 平台标签（如 CSES）
- 点击跳转外部 URL（launchUrl）
- 无匹配时不显示

### 4.6 C++14 模板入口

统一模板索引尚未完成，等待 5 号线程输出 `cpp14_template_mvp_index.json` 后再接入。**本轮结构 MVP 暂不接入。**

### 4.7 数据来源

| 区域 | 数据来源 | 状态 |
|------|----------|------|
| 学习卡片 | learning_card_samples.json | 需新增 provider，仅 30 个样板 |
| 前置知识增强 | learning_card_samples.json → must_know_before / nice_to_know | 需新增 provider |
| 学完继续 | learning_card_samples.json → learn_next | 需新增 provider |
| 练习入口 | problem_refs_seed.json | 需新增 provider |
| 动画入口 | cpp_animation_manifest.json（已有） | **可直接用** |
| C++14 模板 | 等待 cpp14_template_mvp_index.json | **本轮不接入** |

---

## 五、数据来源映射

### 5.1 完整映射表

| 数据文件 | 字段/区域 | 消费页面 | 可直接用 | 说明 |
|----------|-----------|----------|----------|------|
| learning_path_layers_frontend_usage_review.json | frontend_layer_totals | 章节页 | 是 | 分层统计 |
| learning_path_layers_frontend_usage_review.json | suspected_misclassified_core | 章节页 | 是 | 误分节点映射 |
| learning_path_layers_frontend_usage_review.json | overcrowded_section_collapse_policy | 章节页 | 是 | 折叠策略 |
| learning_path_layers_frontend_usage_review.json | recommended_homepage_entry_sections | 首页 | 是 | 推荐入口 |
| learning_path_layers_frontend_usage_review.json | frontend_display_layer_suggestions | 全局 | 是 | UI 规范 |
| learning_card_samples.json | samples.{section} | 知识点页 | **样板** | 仅 30 个，3 章节 |
| dependency_to_learning_path.json | sections.{section_id}.learning_path | 章节页 | **样板** | 仅 3 个章节 |
| learning_path_report_data.json | dependency_distribution | 不直接消费 | 参考 | 统计报告 |
| cpp_animation_manifest.json | animations[] | 知识点页 | **可直接用** | 115 个动画 |
| problem_refs_seed.json | [] | 知识点页 | **样板** | 仅 20 条 |

### 5.2 数据可用性分级

**A 级 — 可直接用（全量数据）：**
- learning_path_layers_frontend_usage_review.json（3240 节点全覆盖）
- cpp_animation_manifest.json（115 个动画）

**B 级 — 样板可用（部分数据，需优雅降级）：**
- learning_card_samples.json（30 个样板，覆盖 2.8/3.13/4.1）
- dependency_to_learning_path.json（3 个章节）
- problem_refs_seed.json（20 条题目引用）

**C 级 — 参考用（不直接消费）：**
- learning_path_report_data.json（统计报告）

---

## 六、风险分析

### 6.1 可直接用的数据

| 数据 | 风险 | 缓解 |
|------|------|------|
| 分层结果 | 111 个疑似误分 core 节点 | 使用 frontend_display_layer 而非 graph_layer |
| 动画 manifest | 部分动画 JSON 文件可能不完整 | 已有 provider 做空值处理 |

### 6.2 只能做样板的数据

| 数据 | 风险 | 缓解 |
|------|------|------|
| 学习卡片（30 个） | 大部分知识点无卡片 | UI 必须优雅降级，无卡片时不显示区域 |
| 学习路径（3 章节） | 大部分章节无路径 | 仅在 2.8/3.13/4.1 显示入口 |
| 题目引用（20 条） | 覆盖率极低 | 仅在有匹配时显示，不作为核心功能 |

### 6.3 不要现在做的功能

| 功能 | 原因 |
|------|------|
| 推荐 MVP（个性化推荐） | 数据不足，算法未设计 |
| 今日学习目标逻辑 | 需要用户模型，当前无数据 |
| C++14 模板入口 | 统一模板索引尚未完成，等待 5 号线程输出 cpp14_template_mvp_index.json |
| 学习路径全量生成 | 仅 3 个章节有路径，需扩展工具 |
| 分层结果写回图谱 | 111 个误分节点待审核 |
| 知识点完成度追踪 | 需要更完善的进度模型 |

### 6.4 可能需要后续修改的 Flutter 文件

| 文件 | 修改类型 | 优先级 |
|------|----------|--------|
| lib/models/knowledge_item.dart | 新增 frontendDisplayLayer 字段 | high |
| lib/models/knowledge_section.dart | 新增 collapsePolicy 字段 | medium |
| lib/pages/home_page.dart | 新增推荐入口区域 | high |
| lib/pages/knowledge_section_page.dart | 分层展示 + 折叠 | high |
| lib/pages/knowledge_item_page.dart | 学习卡片 + 学完继续 + 练习入口 | high |
| lib/state/knowledge_graph_provider.dart | 新增分层数据 provider | high |
| lib/repositories/ | 新增 learning_card / problem_refs repository | medium |
| lib/app/router.dart | 新增学习路径页面路由 | low |

---

## 七、实施建议

### 7.1 分阶段实施

**Phase 1：数据层（优先）**
1. 新增 `LearningLayerRepository` 加载 learning_path_layers_frontend_usage_review.json
2. 新增 `LearningLayerProvider` 提供分层查询
3. KnowledgeItem model 增加 frontendDisplayLayer 字段
4. KnowledgeSection model 增加 collapsePolicy 字段

**Phase 2：章节页增强**
1. 章节页按 core/standard/advanced/optional 分组显示
2. advanced/optional 默认折叠（ExpansionTile）
3. 高拥挤章节应用折叠策略
4. 2.8/3.13/4.1 章节显示学习路径入口

**Phase 3：首页增强**
1. 新增"推荐入口"区域
2. 推荐入口跳转对应章节页

**Phase 4：知识点页增强**
1. 新增学习卡片区域（有卡片时显示）
2. 新增学完继续区域
3. 新增练习入口（有匹配题目时显示）
4. 前置知识区分 must_know / nice_to_know

### 7.2 不建议现在做的

- 推荐 MVP
- 今日学习目标逻辑
- C++14 模板入口（等待 5 号线程输出 cpp14_template_mvp_index.json）
- 全量学习路径生成
- 分层结果写回图谱

---

## 八、结论

| 项目 | 结论 |
|------|------|
| 是否建议开始结构 MVP | **是**，数据层和页面层改动明确，风险可控 |
| 是否建议开始推荐 MVP | **否**，缺少用户行为数据和推荐算法 |
| 首页接入 | 新增推荐入口区域（3 个分类卡片），今日目标占位 |
| 章节页接入 | 分层展示 + 折叠策略 + 学习路径入口（3 章节） |
| 知识点页接入 | 学习卡片 + 学完继续 + 练习入口，均需优雅降级 |

---

## 九、声明

本轮为只读审计，未修改主图谱、前端图谱、内容索引、内容正文、Flutter 代码。
