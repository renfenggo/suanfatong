# Patterns v0.1 Frontend QA Checklist

## Current Baseline
- ready pattern 数量：83
- frontend cards 数量：83
- 首页推荐 section 数量：6
- beginner / interview / icpc / noi 推荐入口数量：beginner=10, interview=12, icpc=14, noi=10
- item 反向索引覆盖数量：43
- 主图谱是否修改：否

## Data Files Reference
- `patterns_v0_1_frontend_cards.json` - 83 条卡片数据
- `patterns_v0_1_homepage_sections.json` - 6 个首页推荐区
- `patterns_v0_1_recommended_entry_points.json` - 4 个入口路径
- `patterns_v0_1_detail_page_schema.json` - 83 条详情页记录
- `patterns_v0_1_item_to_patterns_map.json` - 43 个知识点反向映射

---

## 1. 首页推荐区展示测试

### 1.1 基本展示
- [ ] 首页正常加载 6 个推荐 section（interview_high_frequency, beginner_must_know, icpc_advanced, graph_modeling, dp_classics, data_structure_maintenance）
- [ ] 每个 section 显示正确的 title 和 subtitle
- [ ] 每个 section 下的 pattern 数量与预期一致

### 1.2 数据完整性
- [ ] 每个 section 都正确显示 pattern 卡片，无空 section
- [ ] 卡片 pattern_id 能正确跳转到详情页
- [ ] section 的 pattern_ids 列表完整，无缺失

### 1.3 异常情况
- [ ] 如果某个 section 的 pattern 全部被过滤掉（如难度筛选），显示合理的空状态
- [ ] section 数据加载失败时有友好的错误提示

---

## 2. 入口路径访问测试

### 2.1 入口可访问性
- [ ] beginner 入口可访问，显示 10 个推荐 pattern
- [ ] interview 入口可访问，显示 12 个推荐 pattern
- [ ] icpc 入口可访问，显示 14 个推荐 pattern
- [ ] noi 入口可访问，显示 10 个推荐 pattern

### 2.2 入口内容展示
- [ ] 每个入口页显示对应的 title 和 description
- [ ] 入口页显示 recommended_pattern_ids 对应的所有 pattern
- [ ] recommended_count 与实际显示数量一致

### 2.3 入口排序
- [ ] beginner 路径默认按 difficulty 从低到高排序（intermediate 在前，advanced 在后）
- [ ] interview 路径优先展示 Interview Patterns 与 Graph/Search Patterns
- [ ] icpc 路径可按 Graph Modeling、DP、Data Structure、Competitive Modeling 分组展示
- [ ] noi 路径作为进阶专题展示

### 2.4 入口异常处理
- [ ] 入口页 pattern 为空时显示合理空状态
- [ ] 入口数据加载失败时有友好的错误提示

---

## 3. Pattern Card 展示测试

### 3.1 基本字段展示
- [ ] 卡片显示正确的 title（中文名称）
- [ ] 卡片显示正确的 subtitle（英文名称）
- [ ] 卡片显示正确的 category（Interview Patterns, Graph/Search Patterns, DP Patterns 等）
- [ ] 卡片显示正确的 difficulty（beginner, intermediate, advanced, expert）
- [ ] 卡片显示正确的 tracks（如 interview, beginner, icpc, university_cp, advanced_graph）

### 3.2 简洁摘要展示
- [ ] 卡片显示 recognition_summary（识别信号摘要）
- [ ] 卡片显示 transform_summary（转化方法摘要）
- [ ] 卡片显示 required_item_count（前置知识数量）
- [ ] 卡片显示 related_item_count（相关知识数量）
- [ ] 卡片不展示长讲义内容（保持简洁）

### 3.3 卡片交互
- [ ] 点击卡片能正确跳转到 pattern 详情页
- [ ] 卡片 hover 或点击时有明显的视觉反馈
- [ ] 卡片在不同列表页（首页、搜索、分类页）样式一致

### 3.4 卡片异常处理
- [ ] 卡片数据缺失字段时显示合理默认值或隐藏该字段
- [ ] 卡片 visibility 为 "core" 和 "advanced" 都正常显示

---

## 4. Pattern Detail 展示测试

### 4.1 标题区展示
- [ ] 详情页显示正确的 title
- [ ] 详情页显示正确的 en_title
- [ ] 详情页显示正确的 category
- [ ] 详情页显示正确的 difficulty
- [ ] 详情页显示正确的 tracks 数组

### 4.2 识别信号展示
- [ ] 识别信号区域显示 recognition_signals 短 bullet 列表
- [ ] 识别信号标题清晰（如"如何识别"）
- [ ] 识别信号内容简洁明了，每条独立显示

### 4.3 转化方法展示
- [ ] 转化方法区域显示 common_transforms 短 bullet 列表
- [ ] 转化方法标题清晰（如"如何转化"）
- [ ] 转化方法内容简洁明了，每条独立显示

### 4.4 前置知识展示
- [ ] 前置知识区域显示 required_items 列表
- [ ] 每个 required_item 显示为可点击的 chip
- [ ] 点击 required_item 能跳转到对应的知识点详情页
- [ ] required_item 为空时显示"无前置知识"或隐藏该区域

### 4.5 相关知识展示
- [ ] 相关知识区域显示 related_items 列表
- [ ] 每个 related_item 显示为可点击的 chip（视觉上比前置知识弱一些）
- [ ] 点击 related_item 能跳转到对应的知识点详情页
- [ ] related_item 为空时显示"无相关知识"或隐藏该区域

### 4.6 复杂度展示
- [ ] 复杂度区域显示 typical_complexities
- [ ] 复杂度内容清晰易读
- [ ] 复杂度为空时隐藏该区域

### 4.7 例题引用展示
- [ ] 当 example_problem_refs 存在时显示例题引用区域
- [ ] 例题引用显示为链接或引用格式
- [ ] 点击例题引用能跳转到对应题目（如果有外部链接）
- [ ] example_problem_refs 为空时隐藏该区域（不显示空状态）

### 4.8 继续学习展示
- [ ] 继续学习区域显示 next_patterns
- [ ] 每个 next_pattern 显示为可点击的卡片或 chip
- [ ] 点击 next_pattern 能跳转到对应的 pattern 详情页
- [ ] next_patterns 只包含 ready pattern，不包含 A/B 审核项
- [ ] next_patterns 为空时隐藏该区域

### 4.9 详情页异常处理
- [ ] pattern_id 不存在时显示 404 或友好错误提示
- [ ] 详情页数据缺失字段时显示合理默认值或隐藏该字段
- [ ] required_items 或 related_items 引用的知识点不存在时显示"未知知识点"或隐藏该 chip

---

## 5. Knowledge Item 跳转测试

### 5.1 Pattern Detail 到 Knowledge Item 跳转
- [ ] 从 Pattern Detail 点击 required_items 能跳转到知识点详情页
- [ ] 从 Pattern Detail 点击 related_items 能跳转到知识点详情页
- [ ] 跳转时传递正确的 item_id 参数
- [ ] 跳转后 URL 参数正确，支持书签和分享

### 5.2 Knowledge Item Detail 返回功能
- [ ] 知识点详情页有"返回"按钮或浏览器导航能返回到来源 pattern 详情页
- [ ] 返回时保持原来的筛选和滚动位置（如果可能）

---

## 6. Knowledge Item Detail 反向关联测试

### 6.1 "相关题型模式"模块展示
- [ ] 知识点详情页显示"相关题型模式"模块
- [ ] 优先展示 required_by_patterns，最多 6 个
- [ ] 再展示 related_to_patterns，最多 6 个
- [ ] 每个 pattern chip 显示 pattern_id、name、difficulty、category
- [ ] 点击 pattern chip 能跳转到对应的 pattern 详情页

### 6.2 排序逻辑
- [ ] required_by_patterns 按 difficulty 从低到高排序
- [ ] related_to_patterns 保持原顺序或按 difficulty 排序

### 6.3 模块异常处理
- [ ] 如果 item_id 在 patterns_v0_1_item_to_patterns_map.json 中不存在，隐藏"相关题型模式"模块
- [ ] 如果 required_by_patterns 和 related_to_patterns 都为空，隐藏"相关题型模式"模块
- [ ] 不显示空状态的"相关题型模式"模块

### 6.4 只展示 ready pattern
- [ ] "相关题型模式"模块只展示 ready pattern
- [ ] 不展示 A/B 审核项或未审核 pattern

---

## 7. 空数据和异常引用处理测试

### 7.1 空数据处理
- [ ] pattern 列表为空时显示友好的空状态（如图标+文案）
- [ ] pattern 搜索结果为空时显示搜索无结果提示
- [ ] pattern 筛选后结果为空时显示"暂无符合条件的题型模式"
- [ ] knowledge item 没有反向关联 pattern 时不显示空模块

### 7.2 异常引用处理
- [ ] pattern 引用的知识点不存在时显示"未知知识点"或隐藏该 chip
- [ ] pattern 的 next_patterns 引用不存在时跳过或显示错误状态
- [ ] 知识点反向引用的 pattern 不存在时跳过或显示错误状态
- [ ] 首页 section 引用的 pattern 不存在时跳过或显示错误状态
- [ ] 入口路径引用的 pattern 不存在时跳过或显示错误状态

### 7.3 数据格式异常
- [ ] JSON 数据格式错误时显示友好的错误提示
- [ ] 必填字段缺失时显示合理默认值或隐藏该字段
- [ ] 数组字段为空时不报错，隐藏对应区域
- [ ] 字段类型错误时有容错处理（如将字符串转为数组）

---

## 8. 移动端小屏展示测试

### 8.1 响应式布局
- [ ] Pattern Card 在移动端正常显示，无横向滚动
- [ ] Pattern Card 的 title、subtitle、summary 等文本在移动端不被截断
- [ ] Pattern Card 在移动端保持点击区域足够大（至少 44x44px）
- [ ] Pattern Card 在移动端显示的核心信息优先级正确

### 8.2 Pattern Detail 移动端
- [ ] Pattern Detail 的识别信号和转化方法在移动端保持可读性
- [ ] Pattern Detail 的前置知识和相关知识 chip 在移动端不换行过多
- [ ] Pattern Detail 的复杂度和例题引用在移动端合理布局
- [ ] Pattern Detail 的继续学习模块在移动端可用（横滑或分页）

### 8.3 知识点详情页移动端
- [ ] 知识点详情页的"相关题型模式"模块在移动端可用
- [ ] 知识点详情页的反向关联 pattern chip 在移动端可点击
- [ ] 知识点详情页的主要内容在移动端优先展示

### 8.4 入口路径移动端
- [ ] 入口路径页在移动端正常显示
- [ ] 入口路径的分组和筛选在移动端可用
- [ ] 入口路径的 pattern 列表在移动端可用

### 8.5 移动端性能
- [ ] 移动端页面加载时间合理（< 3 秒）
- [ ] 移动端滚动流畅，无卡顿
- [ ] 移动端图片和动画不影响性能

---

## 9. 多语言字段预留测试

### 9.1 字段预留
- [ ] Pattern Card 的 title 和 subtitle 字段支持多语言扩展（当前为中文+英文）
- [ ] Pattern Detail 的 title、en_title、recognition_signals、common_transforms 字段支持多语言扩展
- [ ] Knowledge Item 的 name 字段支持多语言扩展
- [ ] 所有静态文案（如"如何识别"、"如何转化"、"前置知识"等）使用 i18n_key

### 9.2 国际化实现
- [ ] 前端代码中不硬编码中文文案，使用 i18n 工具
- [ ] 语言切换功能预留接口或实现基础切换
- [ ] 多语言切换时页面内容正确更新
- [ ] 多语言切换时 URL 参数或本地存储正确更新

### 9.3 多语言兼容性
- [ ] 当前中文和英文混合展示时布局合理
- [ ] 英文内容过长时有合理的换行或截断处理
- [ ] 多语言字段缺失时有合理的 fallback 逻辑

---

## 10. A/B 未审核 Pattern 过滤测试

### 10.1 前端不过滤原则
- [ ] 前端读取 patterns_v0_1_frontend_cards.json 时不过滤任何 pattern
- [ ] 前端读取 patterns_v0_1_homepage_sections.json 时不过滤任何 pattern
- [ ] 前端读取 patterns_v0_1_recommended_entry_points.json 时不过滤任何 pattern
- [ ] 前端读取 patterns_v0_1_detail_page_schema.json 时不过滤任何 pattern

### 10.2 A/B 审核项处理
- [ ] A/B 未审核 pattern 不在 patterns_v0_1_ready.json 中，因此不在前端数据源中
- [ ] 如果未来 A/B 审核项进入数据源，前端需要按照 visibility 或 status 字段过滤
- [ ] 普通用户端不展示 A/B 审核项，后台管理页可读取 patterns_v0_1_manual_review.json 展示审核队列

### 10.3 过滤规则验证
- [ ] 验证前端只展示 visibility 为 "core" 和 "advanced" 的 pattern
- [ ] 验证前端不展示 A/B 审核项（如果数据源中存在）
- [ ] 验证 next_patterns 只包含 ready pattern，不包含 A/B 审核项
- [ ] 验证知识点反向关联只展示 ready pattern，不包含 A/B 审核项

---

## 11. 数据加载和性能测试

### 11.1 数据加载顺序
- [ ] 首页优先加载 patterns_v0_1_homepage_sections.json
- [ ] 列表页优先加载 patterns_v0_1_frontend_cards.json
- [ ] 详情页按需加载 patterns_v0_1_detail_page_schema.json 中的单条记录
- [ ] 知识点详情页按需加载 patterns_v0_1_item_to_patterns_map.json 中的单条记录

### 11.2 数据缓存
- [ ] 首页数据缓存合理，避免重复请求
- [ ] 列表页数据缓存合理，筛选时不重新加载完整数据
- [ ] 详情页数据缓存合理，返回时保持缓存
- [ ] 知识点详情页反向关联数据缓存合理

### 11.3 性能指标
- [ ] 首页加载时间 < 2 秒
- [ ] 列表页加载时间 < 1.5 秒
- [ ] 详情页加载时间 < 1 秒
- [ ] 知识点详情页加载时间 < 1 秒
- [ ] 页面切换流畅，无明显卡顿

---

## 12. 浏览器兼容性测试

### 12.1 主流浏览器测试
- [ ] Chrome 最新版本正常显示和交互
- [ ] Firefox 最新版本正常显示和交互
- [ ] Safari 最新版本正常显示和交互
- [ ] Edge 最新版本正常显示和交互

### 12.2 移动浏览器测试
- [ ] iOS Safari 正常显示和交互
- [ ] Android Chrome 正常显示和交互
- [ ] 微信内置浏览器正常显示和交互

### 12.3 兼容性问题
- [ ] CSS Grid 和 Flexbox 兼容性
- [ ] ES6+ 语法兼容性
- [ ] JSON 解析兼容性
- [ ] URL 参数解析兼容性

---

## 13. 无障碍访问测试

### 13.1 语义化 HTML
- [ ] 页面使用语义化标签（header, main, nav, section, article 等）
- [ ] 图片有 alt 属性
- [ ] 链接和按钮有清晰的文案

### 13.2 键盘导航
- [ ] 所有交互元素可用 Tab 键访问
- [ ] Enter 键可触发按钮和链接
- [ ] 焦点顺序合理
- [ ] 焦点状态明显

### 13.3 屏幕阅读器
- [ ] 标题层级正确（h1, h2, h3 等）
- [ ] 表单元素有 label
- [ ] 列表使用 ul/ol/li
- [ ] 重要内容不被隐藏或跳过

---

## 14. 错误监控和日志测试

### 14.1 错误捕获
- [ ] JavaScript 运行时错误被捕获和上报
- [ ] 网络请求错误被捕获和上报
- [ ] 数据解析错误被捕获和上报
- [ ] 用户操作错误被捕获和上报

### 14.2 日志记录
- [ ] 页面加载日志记录
- [ ] 用户点击日志记录
- [ ] 筛选和搜索日志记录
- [ ] 异常情况日志记录

---

## 15. 主图谱未修改验证

### 15.1 数据源验证
- [ ] 确认 patterns_v0_1_frontend_cards.json 源自 patterns_v0_1_ready.json
- [ ] 确认 patterns_v0_1_homepage_sections.json 源自 patterns_v0_1_ready.json
- [ ] 确认 patterns_v0_1_recommended_entry_points.json 源自 patterns_v0_1_ready.json
- [ ] 确认 patterns_v0_1_detail_page_schema.json 源自 patterns_v0_1_ready.json
- [ ] 确认 patterns_v0_1_item_to_patterns_map.json 源自 patterns_v0_1_ready.json

### 15.2 数据完整性
- [ ] 所有前端数据文件都包含 generated_at 字段
- [ ] 所有前端数据文件都包含 source 字段，指向 patterns_v0_1_ready.json
- [ ] 主图谱文件未被修改或移动

---

## Summary

本 QA Checklist 覆盖了 Patterns v0.1 前端实现的所有关键功能点：
1. 首页推荐区展示
2. 入口路径访问
3. Pattern Card 展示
4. Pattern Detail 展示
5. Knowledge Item 跳转
6. Knowledge Item 反向关联
7. 空数据和异常引用处理
8. 移动端小屏展示
9. 多语言字段预留
10. A/B 未审核 Pattern 过滤
11. 数据加载和性能
12. 浏览器兼容性
13. 无障碍访问
14. 错误监控和日志
15. 主图谱未修改验证

所有测试点完成后，Patterns v0.1 前端实现可以进入正式发布阶段。