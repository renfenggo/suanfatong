# Patterns v0.1 Page Implementation Notes

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

## 1. 推荐页面结构

### 1.1 首页结构
```
首页
├── Header (导航栏)
│   ├── Logo
│   ├── 首页链接
│   ├── 题型模式链接
│   ├── 入口路径下拉菜单
│   │   ├── 入门题型路径
│   │   ├── 面试刷题路径
│   │   ├── ICPC 训练路径
│   │   └── NOI 进阶路径
│   └── 搜索框
├── Main Content (主内容区)
│   ├── Section 1: 面试高频题型 (interview_high_frequency)
│   │   ├── Title: "面试高频题型"
│   │   ├── Subtitle: "从补数、窗口、二分答案到常见图搜索，适合刷题面试入口。"
│   │   └── Pattern Cards (8 个卡片横滑)
│   ├── Section 2: 入门必会题型 (beginner_must_know)
│   │   ├── Title: "入门必会题型"
│   │   ├── Subtitle: "优先掌握数组、窗口、哈希、基础搜索和回溯的识别方式。"
│   │   └── Pattern Cards (8 个卡片横滑)
│   ├── Section 3: ICPC 进阶题型 (icpc_advanced)
│   │   ├── Title: "ICPC 进阶题型"
│   │   ├── Subtitle: "面向竞赛训练的建模、离线、DP 和数据结构维护模式。"
│   │   └── Pattern Cards (8 个卡片横滑)
│   ├── Section 4: 图论建模题型 (graph_modeling)
│   │   ├── Title: "图论建模题型"
│   │   ├── Subtitle: "把约束、路径、匹配和选择问题转化为图上的状态与边。"
│   │   └── Pattern Cards (8 个卡片横滑)
│   ├── Section 5: DP 经典题型 (dp_classics)
│   │   ├── Title: "DP 经典题型"
│   │   ├── Subtitle: "覆盖背包、区间、树形、数位、状压和序列 DP 的核心入口。"
│   │   └── Pattern Cards (8 个卡片横滑)
│   └── Section 6: 数据结构维护题型 (data_structure_maintenance)
│       ├── Title: "数据结构维护题型"
│       ├── Subtitle: "面向多次更新/查询，理解如何把操作映射到可维护状态。"
│       └── Pattern Cards (8 个卡片横滑)
└── Footer
```

### 1.2 入口路径页结构
```
入门题型路径页
├── Header (导航栏)
├── Page Header
│   ├── Title: "入门题型路径"
│   ├── Description: "从数组、哈希、滑动窗口、基础搜索开始，建立题型识别感。"
│   └── Pattern Count: "共 10 个题型模式"
├── Main Content
│   ├── Filter Bar (可选)
│   │   ├── Difficulty Filter: [All] [Beginner] [Intermediate] [Advanced] [Expert]
│   │   ├── Category Filter: [All] [Interview Patterns] [Graph/Search Patterns] [DP Patterns]...
│   │   └── Track Filter: [All] [Beginner] [Interview] [ICPC] [NOI]
│   └── Pattern Grid/Grid List
│       └── Pattern Cards (10 个卡片)
│           ├── Card 1: 两数之和模式
│           ├── Card 2: 前缀和 + 哈希表
│           ├── ... (按 difficulty 从低到高排序)
│           └── Card 10: 岛屿问题
└── Footer
```

### 1.3 Pattern Detail 页结构
```
Pattern Detail 页
├── Header (导航栏)
├── Breadcrumb
│   ├── 首页
│   ├── 题型模式
│   └── 两数之和模式
├── Main Content
│   ├── Title Section
│   │   ├── Title: "两数之和模式"
│   │   ├── Subtitle: "Two Sum Pattern"
│   │   ├── Category: "Interview Patterns"
│   │   ├── Difficulty: "Intermediate"
│   │   └── Tracks: [Interview] [Beginner]
│   ├── Recognition Section
│   │   ├── Title: "如何识别"
│   │   └── Recognition Signals (Bullet List)
│   │       ├── 题面要求两个元素/两个下标配对
│   │       ├── target - x 的补数可直接查询
│   │       └── ...
│   ├── Transform Section
│   │   ├── Title: "如何转化"
│   │   └── Common Transforms (Bullet List)
│   │       ├── 把 a+b=target 转为补数存在性查询
│   │       ├── 若要求值而非下标，可排序后相向双指针
│   │       └── ...
│   ├── Prerequisites Section
│   │   ├── Title: "前置知识"
│   │   └── Required Items (Clickable Chips)
│   │       ├── [3.2.5 哈希表]
│   │       └── [2.5.1 相向双指针]
│   ├── Related Knowledge Section
│   │   ├── Title: "相关知识"
│   │   └── Related Items (Clickable Chips, 次级样式)
│   │       ├── [2.2.1 冒泡排序]
│   │       └── [2.4.1 前缀和]
│   ├── Complexity Section
│   │   ├── Title: "复杂度"
│   │   └── Typical Complexities
│   │       ├── O(n)
│   │       └── O(n log n) after sorting
│   ├── Examples Section (如果有 example_problem_refs)
│   │   ├── Title: "例题引用"
│   │   └── Example Problem Refs
│   │       └── LeetCode 1
│   └── Continue Learning Section
│       ├── Title: "继续学习"
│       └── Next Patterns (Clickable Chips)
│           ├── [前缀和 + 哈希表]
│           ├── [定长滑动窗口]
│           └── ...
└── Footer
```

### 1.4 Knowledge Item Detail 页结构（新增模块）
```
Knowledge Item Detail 页
├── Header (导航栏)
├── Breadcrumb
│   ├── 首页
│   ├── 知识点
│   └── 哈希表
├── Main Content
│   ├── Title Section
│   │   ├── Item ID: "3.2.5"
│   │   └── Item Name: "哈希表"
│   ├── Content Section (原有内容)
│   │   └── (知识点原有的内容，如定义、示例等)
│   └── Related Patterns Section (新增)
│       ├── Title: "相关题型模式"
│       ├── Description: "掌握本知识点后可学习以下题型模式"
│       ├── Required By Patterns (最多 6 个，按 difficulty 从低到高排序)
│       │   ├── [两数之和模式 Intermediate]
│       │   ├── [前缀和 + 哈希表 Intermediate]
│       │   └── ...
│       └── Related To Patterns (最多 6 个，保持原顺序或按 difficulty 排序)
│           ├── [快慢指针 Intermediate]
│           ├── [单调栈求下一个更大元素 Intermediate]
│           └── ...
└── Footer
```

---

## 2. 数据加载顺序

### 2.1 首页数据加载
1. **初始加载**：加载 `patterns_v0_1_homepage_sections.json`
   - 包含 6 个 section 的基本信息
   - 每个 section 包含 pattern_ids 数组

2. **按需加载**：根据 section 的 pattern_ids 加载对应的 pattern 卡片数据
   - 从 `patterns_v0_1_frontend_cards.json` 中提取对应 pattern_id 的卡片数据
   - 或者直接在客户端根据 pattern_ids 过滤完整的 cards 数组

3. **优化策略**：
   - 首屏只加载第一个 section 的卡片数据
   - 滚动到其他 section 时再加载对应数据（懒加载）
   - 预加载相邻 section 的数据

### 2.2 入口路径页数据加载
1. **初始加载**：加载 `patterns_v0_1_recommended_entry_points.json`
   - 根据入口 ID（beginner/interview/icpc/noi）获取对应的 recommended_pattern_ids

2. **按需加载**：根据 recommended_pattern_ids 加载对应的 pattern 卡片数据
   - 从 `patterns_v0_1_frontend_cards.json` 中提取对应 pattern_id 的卡片数据

3. **排序处理**：
   - beginner 路径：按 difficulty 从低到高排序（intermediate 在前，advanced 在后）
   - interview 路径：优先展示 Interview Patterns 与 Graph/Search Patterns
   - icpc 路径：按 Graph Modeling、DP、Data Structure、Competitive Modeling 分组
   - noi 路径：作为进阶专题展示

4. **筛选优化**：
   - 客户端维护完整的 cards 数组
   - 筛选时在客户端过滤，无需重新请求
   - 支持多条件组合筛选（difficulty、category、track）

### 2.3 Pattern Detail 页数据加载
1. **初始加载**：根据 URL 中的 pattern_id 加载对应数据
   - 从 `patterns_v0_1_detail_page_schema.json` 中提取对应 pattern_id 的记录
   - 或者通过 API 按 pattern_id 获取单条记录

2. **数据结构**：
   - 包含完整的 pattern 详情信息（title、recognition_signals、common_transforms 等）
   - 包含 required_items、related_items、next_patterns 等引用

3. **按需加载**：
   - required_items 和 related_items 的详细信息按需加载
   - next_patterns 的详细信息按需加载（用户点击时加载）

### 2.4 Knowledge Item Detail 页数据加载
1. **初始加载**：根据 URL 中的 item_id 加载对应数据
   - 从 `knowledge_items` 中加载知识点详情（原有数据）
   - 从 `patterns_v0_1_item_to_patterns_map.json` 中提取对应 item_id 的反向映射

2. **按需加载**：根据 required_by_patterns 和 related_to_patterns 的 pattern_ids 加载对应的 pattern 卡片数据
   - 从 `patterns_v0_1_frontend_cards.json` 中提取对应 pattern_id 的卡片数据
   - 或者从 `patterns_v0_1_detail_page_schema.json` 中提取更详细的信息

3. **排序和限制**：
   - required_by_patterns 按 difficulty 从低到高排序
   - required_by_patterns 最多显示 6 个
   - related_to_patterns 保持原顺序或按 difficulty 排序
   - related_to_patterns 最多显示 6 个

### 2.5 数据加载优化策略
1. **预加载**：
   - 首页预加载前两个 section 的数据
   - 列表页预加载下一页数据
   - 详情页预加载 next_patterns 的数据

2. **缓存策略**：
   - 静态文件（JSON）使用浏览器缓存
   - 动态数据使用内存缓存（如 Redux/MobX）
   - 用户会话期间保持缓存，刷新后重新加载

3. **数据大小优化**：
   - `patterns_v0_1_frontend_cards.json` 只包含卡片展示所需的字段
   - `patterns_v0_1_detail_page_schema.json` 包含完整的详情数据，但按需加载
   - `patterns_v0_1_item_to_patterns_map.json` 只包含反向映射关系

---

## 3. 前端字段映射

### 3.1 Pattern Card 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| pattern_id | 路由和内部标识 | string | 是 | 用于跳转到详情页 |
| title | 卡片标题 | string | 是 | 中文名称 |
| subtitle | 卡片副标题 | string | 是 | 英文名称 |
| category | 分类标签 | string | 是 | Interview Patterns, Graph/Search Patterns, DP Patterns 等 |
| difficulty | 难度标签 | string | 是 | beginner, intermediate, advanced, expert |
| tracks | 学习路径标签 | array | 是 | [beginner, interview, icpc, university_cp, advanced_graph] |
| recognition_summary | 识别摘要 | string | 是 | 简短的识别信号描述 |
| transform_summary | 转化摘要 | string | 是 | 简短的转化方法描述 |
| required_item_count | 前置知识数量 | number | 是 | 显示为"X个前置知识" |
| related_item_count | 相关知识数量 | number | 是 | 显示为"X个相关知识" |
| visibility | 可见性 | string | 是 | core 或 advanced，前端不需要过滤 |

### 3.2 Pattern Detail 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| pattern_id | 路由和内部标识 | string | 是 | 用于跳转和埋点 |
| title | 详情页标题 | string | 是 | 中文名称 |
| en_title | 详情页英文标题 | string | 是 | 英文名称 |
| category | 分类标签 | string | 是 | Interview Patterns, Graph/Search Patterns, DP Patterns 等 |
| difficulty | 难度标签 | string | 是 | beginner, intermediate, advanced, expert |
| tracks | 学习路径标签 | array | 是 | [beginner, interview, icpc, university_cp, advanced_graph] |
| recognition_signals | 识别信号列表 | array | 是 | 每个元素是一个短字符串，显示为 bullet |
| common_transforms | 转化方法列表 | array | 是 | 每个元素是一个短字符串，显示为 bullet |
| required_items | 前置知识列表 | array | 是 | 知识点 ID 数组，每个 ID 对应一个可点击的 chip |
| related_items | 相关知识列表 | array | 是 | 知识点 ID 数组，每个 ID 对应一个可点击的 chip（次级样式） |
| typical_complexities | 复杂度列表 | array | 否 | 时间和空间复杂度，为空时隐藏该区域 |
| example_problem_refs | 例题引用列表 | array | 否 | 例题引用，为空时隐藏该区域 |
| next_patterns | 继续学习列表 | array | 否 | Pattern ID 数组，每个 ID 对应一个可点击的 chip |
| frontend_notes | 前端实现提示 | string | 否 | 开发者备注，不展示给用户 |

### 3.3 Homepage Section 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| section_id | Section 标识 | string | 是 | 内部标识 |
| title | Section 标题 | string | 是 | 如"面试高频题型" |
| subtitle | Section 描述 | string | 是 | 如"从补数、窗口、二分答案到常见图搜索，适合刷题面试入口。" |
| pattern_ids | Pattern ID 列表 | array | 是 | 该 section 包含的 pattern_id 数组 |

### 3.4 Recommended Entry Point 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| entry_id | 入口标识 | string | 是 | beginner/interview/icpc/noi |
| title | 入口标题 | string | 是 | 如"入门题型路径" |
| description | 入口描述 | string | 是 | 如"从数组、哈希、滑动窗口、基础搜索开始，建立题型识别感。" |
| recommended_pattern_ids | 推荐 Pattern ID 列表 | array | 是 | 该入口包含的 pattern_id 数组 |
| recommended_count | 推荐数量 | number | 是 | 显示为"共 X 个题型模式" |

### 3.5 Item to Patterns Map 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| item_id | 知识点 ID | string | 是 | 知识点唯一标识 |
| item_name | 知识点名称 | string | 是 | 知识点中文名称 |
| required_by_patterns | 被依赖的 Pattern 列表 | array | 否 | Pattern 数组，每个元素包含 pattern_id, name, en_name, category |
| related_to_patterns | 相关的 Pattern 列表 | array | 否 | Pattern 数组，每个元素包含 pattern_id, name, en_name, category |

### 3.6 Knowledge Item Chip 字段映射

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| item_id | 芯片内部标识 | string | 是 | 用于跳转到知识点详情页 |
| item_name | 芯片显示文本 | string | 是 | 知识点名称，如"哈希表" |

### 3.7 Pattern Chip 字段映射（用于 Knowledge Item Detail 页）

| 数据字段 | 前端展示 | 类型 | 必填 | 备注 |
|---------|---------|------|------|------|
| pattern_id | 芯片内部标识 | string | 是 | 用于跳转到 pattern 详情页 |
| name | 芯片显示文本 | string | 是 | Pattern 中文名称，如"两数之和模式" |
| difficulty | 难度标签 | string | 是 | beginner/intermediate/advanced/expert |
| category | 分类标签 | string | 是 | Interview Patterns, Graph/Search Patterns, DP Patterns 等 |

---

## 4. 推荐筛选逻辑

### 4.1 首页 Section 展示逻辑
1. **默认展示**：按 `patterns_v0_1_homepage_sections.json` 中的 sections 顺序展示
2. **Section 内排序**：按 `pattern_ids` 数组中的顺序展示
3. **过滤逻辑**：如果用户设置了筛选条件，按以下逻辑过滤
   - 如果 section 中所有 pattern 都被过滤掉，隐藏该 section
   - 如果 section 中部分 pattern 被过滤掉，只展示未过滤的 pattern

### 4.2 入口路径页筛选逻辑
1. **默认排序**：
   - beginner：按 difficulty 从低到高排序（intermediate 在前，advanced 在后）
   - interview：优先展示 Interview Patterns 与 Graph/Search Patterns，其他类别按 difficulty 排序
   - icpc：按 Graph Modeling、DP、Data Structure、Competitive Modeling 分组，每组内按 difficulty 排序
   - noi：按 difficulty 从低到高排序

2. **多条件筛选**：
   - 支持 difficulty、category、track 多条件组合筛选
   - 筛选条件之间是 AND 关系
   - 筛选结果实时更新，无需重新加载数据

3. **筛选实现**：
   ```javascript
   const filteredPatterns = patterns.filter(pattern => {
     const matchDifficulty = selectedDifficulty === 'all' || pattern.difficulty === selectedDifficulty;
     const matchCategory = selectedCategory === 'all' || pattern.category === selectedCategory;
     const matchTrack = selectedTrack === 'all' || pattern.tracks.includes(selectedTrack);
     return matchDifficulty && matchCategory && matchTrack;
   });
   ```

### 4.3 列表页筛选逻辑
1. **默认展示**：按 `patterns_v0_1_frontend_cards.json` 中的顺序展示
2. **支持筛选**：category、track、difficulty 三个筛选器
3. **默认展示**：homepage_sections 的内容
4. **排序选项**：
   - 默认排序（按 pattern_id 或其他字段）
   - Difficulty 升序/降序
   - Title A-Z / Z-A

### 4.4 搜索逻辑
1. **全文搜索**：支持搜索 title、subtitle、category、recognition_summary、transform_summary
2. **模糊搜索**：支持部分匹配和大小写不敏感
3. **搜索结果排序**：按相关度排序（title 匹配优先，其他字段次之）
4. **空结果处理**：显示"暂无符合条件的题型模式"和搜索建议

---

## 5. 后续接 problem_refs 时如何扩展

### 5.1 数据结构扩展

#### 5.1.1 Pattern Detail 扩展
```json
{
  "pattern_id": "pat.two_sum",
  "title": "两数之和模式",
  "en_title": "Two Sum Pattern",
  "category": "Interview Patterns",
  "difficulty": "intermediate",
  "tracks": ["interview", "beginner"],
  "recognition_signals": ["..."],
  "common_transforms": ["..."],
  "required_items": ["3.2.5", "2.5.1"],
  "related_items": ["2.2.1", "2.4.1"],
  "typical_complexities": ["O(n)", "O(n log n) after sorting"],
  "example_problem_refs": ["LeetCode 1"],
  "problem_refs": [
    {
      "problem_id": "lc.1",
      "source": "leetcode",
      "title": "Two Sum",
      "url": "https://leetcode.com/problems/two-sum/",
      "difficulty": "easy",
      "tags": ["array", "hash-table"]
    },
    {
      "problem_id": "platform.123",
      "source": "platform",
      "title": "两数之和",
      "url": "/problems/123",
      "difficulty": "easy",
      "tags": ["array", "hash-table"]
    }
  ],
  "next_patterns": ["pat.prefix_sum_hashmap", "pat.sliding_window_fixed_size"]
}
```

#### 5.1.2 Pattern Card 扩展
```json
{
  "pattern_id": "pat.two_sum",
  "title": "两数之和模式",
  "subtitle": "Two Sum Pattern",
  "category": "Interview Patterns",
  "difficulty": "intermediate",
  "tracks": ["interview", "beginner"],
  "recognition_summary": "题面要求两个元素/两个下标配对；target - x 的补数可直接查询。",
  "transform_summary": "把 a+b=target 转为补数存在性查询；若要求值而非下标，可排序后相向双指针。",
  "required_item_count": 2,
  "related_item_count": 2,
  "problem_count": 15,
  "visibility": "core"
}
```

### 5.2 前端界面扩展

#### 5.2.1 Pattern Detail 页扩展
1. **增加"相关题目"模块**：
   ```
   相关题目
   ├── 总数: "共 15 道"
   └── 题目列表
       ├── [LeetCode 1 Two Sum Easy]
       ├── [Platform 123 两数之和 Easy]
       └── ...
   ```

2. **增加题目筛选**：
   - 按来源筛选（LeetCode、Platform、Codeforces 等）
   - 按难度筛选（Easy、Medium、Hard）
   - 按标签筛选（Array、Hash-Table、DP 等）

3. **增加题目排序**：
   - 默认排序（按推荐度或难度）
   - 难度升序/降序
   - 来源分组

#### 5.2.2 Pattern Card 扩展
1. **增加题目数量**：
   - 在卡片上显示 `problem_count`，如"15 道相关题目"

2. **增加题目预览**：
   - 卡片上显示 1-2 个热门题目的小图标或链接

#### 5.2.3 搜索扩展
1. **增加题目搜索**：
   - 搜索框支持搜索题目标题、来源、标签
   - 搜索结果显示题目和对应的 pattern

2. **增加反向搜索**：
   - 从题目搜索到 pattern
   - 从题目详情页跳转到 pattern 详情页

### 5.3 API 扩展

#### 5.3.1 获取 Pattern 的题目列表
```
GET /api/patterns/{pattern_id}/problems
Response:
{
  "pattern_id": "pat.two_sum",
  "problem_count": 15,
  "problems": [...]
}
```

#### 5.3.2 获取题目对应的 Pattern 列表
```
GET /api/problems/{problem_id}/patterns
Response:
{
  "problem_id": "lc.1",
  "pattern_count": 1,
  "patterns": [
    {
      "pattern_id": "pat.two_sum",
      "title": "两数之和模式",
      "difficulty": "intermediate",
      "category": "Interview Patterns"
    }
  ]
}
```

### 5.4 数据加载扩展
1. **懒加载**：
   - Pattern Detail 页默认不加载题目列表
   - 用户展开"相关题目"模块时再加载

2. **分页加载**：
   - 如果题目数量较多（> 20），支持分页加载
   - 每页加载 10-20 道题目

3. **缓存优化**：
   - 题目列表缓存到内存中
   - 用户在同一个 pattern 详情页内多次展开不重复加载

### 5.5 用户交互扩展
1. **题目跳转**：
   - 点击题目跳转到题目详情页（如果是平台内部题目）
   - 点击题目跳转到外部链接（如果是 LeetCode 等）

2. **题目收藏**：
   - 支持收藏题目
   - 收藏的题目显示在"我的收藏"页面
   - 收藏的题目可以关联到对应的 pattern

3. **题目练习记录**：
   - 记录用户完成的题目
   - 在 pattern 详情页显示用户完成进度（如"已完成 5/15 道"）
   - 在知识图谱中展示用户的学习进度

---

## 6. 主图谱是否被修改，必须为否

### 6.1 数据源验证
1. **patterns_v0_1_ready.json**：
   - 这是主图谱文件，本阶段**未被修改**
   - 所有前端数据文件都从这个文件派生
   - 前端实现不应该直接修改这个文件

2. **前端数据文件**：
   - `patterns_v0_1_frontend_cards.json`：从 ready 文件提取卡片所需字段
   - `patterns_v0_1_homepage_sections.json`：从 ready 文件筛选并分组
   - `patterns_v0_1_recommended_entry_points.json`：从 ready 文件筛选并排序
   - `patterns_v0_1_detail_page_schema.json`：从 ready 文件提取完整详情
   - `patterns_v0_1_item_to_patterns_map.json`：从 ready 文件构建反向索引

### 6.2 字段验证
1. **pattern_id**：
   - 所有前端数据文件中的 pattern_id 都来自 ready 文件
   - 没有新增或修改 pattern_id

2. **title、en_title**：
   - 所有前端数据文件中的标题都来自 ready 文件
   - 没有修改标题文本

3. **category、difficulty、tracks**：
   - 所有前端数据文件中的分类、难度、路径都来自 ready 文件
   - 没有修改这些字段的值

4. **required_items、related_items**：
   - 所有前端数据文件中的知识点引用都来自 ready 文件
   - 没有修改这些引用关系

### 6.3 文件元信息验证
所有前端数据文件都包含以下元信息：
```json
{
  "generated_at": "2026-05-22",
  "source": "patterns_v0_1_ready.json",
  "pattern_count": 83
}
```
这些信息表明：
- 数据生成时间为 2026-05-22
- 数据源为 patterns_v0_1_ready.json
- pattern 数量为 83（与 ready 文件一致）

### 6.4 版本控制验证
1. **Git 验证**：
   - patterns_v0_1_ready.json 的 commit hash 与之前一致
   - 前端数据文件的 commit hash 为新提交
   - 前端数据文件的 diff 显示没有修改 ready 文件

2. **文件大小验证**：
   - patterns_v0_1_ready.json 的文件大小与之前一致
   - 前端数据文件的文件大小为新增大小

### 6.5 功能验证
1. **前端功能**：
   - 前端只展示 ready pattern，不展示 A/B 审核项
   - 前端不修改任何 pattern 数据
   - 前端不修改任何 knowledge_items 数据

2. **后端功能**：
   - 后端只读取 ready 文件并生成前端数据文件
   - 后端不修改 ready 文件
   - 后端不修改 knowledge_items 文件

### 6.6 总结
- ✅ 主图谱未被修改
- ✅ 所有前端数据文件都从 ready 文件派生
- ✅ 前端实现不修改任何原始数据
- ✅ 后端生成脚本不修改任何原始数据
- ✅ 版本控制和文件大小验证通过
- ✅ 功能验证通过

---

## 7. 其他实现建议

### 7.1 路由设计
1. **Pattern 列表页**：`/patterns`
2. **Pattern 详情页**：`/patterns/:patternId`
3. **入口路径页**：`/paths/:entryId`（如 `/paths/beginner`）
4. **Knowledge Item 详情页**：`/knowledge/:itemId`

### 7.2 状态管理
1. **全局状态**：
   - 当前用户信息
   - 当前语言设置
   - 用户收藏列表
   - 用户学习进度

2. **页面级状态**：
   - 当前筛选条件
   - 当前排序方式
   - 当前搜索关键词
   - 当前分页信息

### 7.3 错误处理
1. **404 处理**：
   - Pattern ID 不存在时显示 404 页面
   - Knowledge Item ID 不存在时显示 404 页面
   - Entry ID 不存在时显示 404 页面

2. **加载失败处理**：
   - 数据加载失败时显示错误提示
   - 提供重试按钮
   - 记录错误日志

### 7.4 性能优化
1. **代码分割**：
   - 按路由进行代码分割
   - 按页面组件进行代码分割

2. **图片优化**：
   - 使用 WebP 格式
   - 使用懒加载
   - 使用响应式图片

3. **字体优化**：
   - 使用系统字体
   - 避免加载外部字体
   - 使用 font-display: swap

### 7.5 SEO 优化
1. **Meta 标签**：
   - 每个页面都有正确的 title、description、keywords
   - 使用 Open Graph 标签

2. **结构化数据**：
   - 使用 JSON-LD 格式
   - 标记 Pattern 和 Knowledge Item

3. **URL 优化**：
   - 使用语义化 URL
   - 包含关键词（如 `two-sum-pattern`）

### 7.6 埋点和分析
1. **页面访问**：
   - 记录每个页面的访问次数
   - 记录用户的访问路径

2. **用户行为**：
   - 记录用户点击的 pattern
   - 记录用户的筛选和搜索行为
   - 记录用户的学习进度

3. **性能监控**：
   - 记录页面加载时间
   - 记录 API 响应时间
   - 记录错误率和异常

---

## Summary

本实现文档提供了 Patterns v0.1 前端实现的详细指导：
1. 推荐页面结构（首页、入口路径页、Pattern Detail 页、Knowledge Item Detail 页）
2. 数据加载顺序（首页、入口路径页、Pattern Detail 页、Knowledge Item Detail 页）
3. 前端字段映射（Pattern Card、Pattern Detail、Homepage Section、Recommended Entry Point、Item to Patterns Map）
4. 推荐筛选逻辑（首页 Section 展示、入口路径页筛选、列表页筛选、搜索）
5. 后续接 problem_refs 时如何扩展（数据结构扩展、前端界面扩展、API 扩展、数据加载扩展、用户交互扩展）
6. 主图谱是否被修改，必须为否（数据源验证、字段验证、文件元信息验证、版本控制验证、功能验证）

遵循本文档的指导，前端团队可以高效地实现 Patterns v0.1 的所有功能，并确保数据完整性和系统稳定性。