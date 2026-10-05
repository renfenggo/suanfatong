# Patterns v0.1 Frontend Usage Spec

## Current Baseline

- ready pattern 数量：83
- frontend cards 数量：83
- item 反向索引覆盖数量：43
- 首页推荐 section 数量：6
- beginner / interview / icpc / noi 推荐入口数量：beginner=10, interview=12, icpc=14, noi=10
- 暂不进入 Batch2：A/B 人工审核项未确认前，不生成第二批 pattern。
- 主图谱是否修改：否

## File Usage

### patterns_v0_1_frontend_cards.json

用于题型模式首页、列表页、搜索结果页和推荐横滑卡片。每张卡片只展示短摘要：标题、副标题、category、difficulty、tracks、识别摘要、转化摘要和 prerequisite 数量。不要在卡片里展示长讲义，也不要直接展示完整题目内容。

### patterns_v0_1_learning_path_map.json

用于 beginner_path、interview_path、icpc_path、noi_path 四个路径入口。路径页可以先展示 pattern_count，再按 category 或 difficulty 分组渲染 patterns。当前路径只包含 v0.1 ready patterns，不包含 A/B 未审核项。

### patterns_v0_1_item_to_patterns_map.json

用于知识点详情页的“相关题型模式”模块。打开某个 knowledge item 时，用 item_id 查找 required_by_patterns 和 related_to_patterns：required_by_patterns 更适合显示为“掌握本知识点后可学习”，related_to_patterns 可显示为“相关题型”。

## Knowledge Item Detail Page

在知识点详情页，建议放一个紧凑模块：

- 优先展示 required_by_patterns，最多 6 个，按 difficulty 从低到高排序。
- 再展示 related_to_patterns，最多 6 个，作为延伸阅读。
- 每个 pattern chip 使用 pattern_id 跳转题型详情页，展示 name、difficulty、category。
- 如果 item_to_patterns_map 中没有该 item_id，则隐藏模块，不显示空态。

## Pattern Detail Page

题型详情页使用 patterns_v0_1_detail_page_schema.json 中的 records 或按 pattern_id 从 ready 数据组装。建议页面结构：

1. 标题区：title、en_title、category、difficulty、tracks。
2. 如何识别：recognition_signals，用短 bullet 展示。
3. 如何转化：common_transforms，用短 bullet 展示。
4. 前置知识：required_items，展示为可点击知识点 chip。
5. 相关知识：related_items，展示为次级 chip。
6. 复杂度：typical_complexities。
7. 例题引用：example_problem_refs，有则展示，无则隐藏。
8. 继续学习：next_patterns，仅引用 ready pattern。

## Path Display

- beginner：适合首页新手入口，默认按 intermediate 在前、advanced 在后排序。
- interview：适合刷题/面试入口，可以优先展示 Interview Patterns 与 Graph/Search Patterns。
- icpc：适合训练平台专题入口，可按 Graph Modeling、DP、Data Structure、Competitive Modeling 分组。
- noi：当前数量较少，作为进阶专题入口展示，不扩充 Batch2 数据。

## Difficulty Display

使用 patterns_v0_1_index_by_difficulty.json 驱动难度筛选。v0.1 ready 中 beginner 难度为 0，但 beginner track 有 20 条，所以 UI 文案应区分“入门路径”和“beginner 难度”。

## A/B Review Handling

A/B 未审核 pattern 当前不进入前台 ready 列表。后台管理页可读取 patterns_v0_1_manual_review.json 展示审核队列，但普通用户端不展示，避免层级或归属尚未确认的 pattern 进入学习路径。

## Frontend Page Recommendations

- 列表页用 category、track、difficulty 三个筛选器，默认展示 homepage_sections。
- 详情页 required_items 与 related_items 均跳转知识点详情页，不复制知识点正文。
- item 详情页反向关联 pattern 时，只展示 ready pattern，避免 A/B 审核项混入。
- 所有路由和收藏使用 pattern_id，展示文案可后续接 i18n_key。

## Guardrails

- 本阶段不生成 Batch2。
- 不修改主图谱。
- 不修改 knowledge_items。
- 不修改 patterns_v0_1_ready.json。
