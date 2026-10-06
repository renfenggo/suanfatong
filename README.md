# 算法通

> 历史包名 `bfs_learn`，产品展示名为「算法通」。

面向信息学竞赛初学者的离线算法学习 App（Windows 桌面优先），涵盖 C++ 语法基础、算法、数据结构、竞赛数学等知识点。当前处于 Winknow + suanfatong 融合平台 M1（Flutter 桌面 Shell）阶段。

## 功能模块

| 模块 | 功能 |
|------|------|
| 知识图谱 | 按分类、章节浏览全部 **3240 个知识点**（5 大分类 / 65 章节），查看前置依赖关系 |
| 知识点内容 | 每个知识点九区块内容：简介、学习目标、核心思想、学习步骤、常见错误、示例、随堂自测、练习任务、掌握检查（33 分片内容包按需加载） |
| 学习单元 | C++ 语法/算法/数学学习单元：讲解、示例代码、常见错误、练习、小测 |
| 动画演示 | **115 个算法动画**（排序、搜索、图论等），逐步可视化代码执行过程 |
| 章节小测 | 每个章节配套选择题测验，即时反馈 + 解析 |
| 搜索 | 按名称、别名、讲解、常见错误等全文搜索知识点 |
| 学习进度 | 本地持久化学习记录、测验成绩、错题集 |
| BFS 专题 | BFS 知识讲解、迷宫动画、选择题训练、常见错误、教师演示模式 |
| 设置 | 字体大小、深色/浅色主题、多语言切换（启动恢复）、清除进度 |
| 桌面 Shell | 左侧 NavigationRail 九导航区（首页/知识图谱/学习中心/题目训练/编程工作台/AI 助手/课堂/学习记录/设置），宽窄窗口自适应，go_router 声明式路由 + 深链 |

## 知识体系（5 大分类，共 3240 知识点）

| 分类 | 数据位置 |
|------|----------|
| C++ 语法（1.x + 5.x） | `assets/data/cpp/` |
| 算法（2.x + 3.x） | `assets/data/algorithm/` |
| 算法竞赛数学（4.x） | `assets/data/math/` |
| 数据结构 | 含在知识图谱中 |

- 知识图谱（唯一 SoT）：`assets/data/knowledge/io_v4_4.json`（5 分类 / 65 章节 / 3240 items）
- 图谱生产管线映射工具：`tools/publish/map_graph.py`（双 schema 映射 + validator，`--verify` 语义 diff=0）
- 知识点内容包：`assets/data/knowledge_content/`（`content_index.json` 33 分片 + `item_part_index.json` 显式 item→分片映射，3240 条全覆盖，按需加载 + LRU 缓存 + 全链路降级）

## 技术栈

- Flutter 3.29 / Dart ^3.7.0
- flutter_riverpod ^2.6.1（状态管理）
- go_router ^14.8.1（声明式路由 + StatefulShellRoute 桌面壳）
- shared_preferences ^2.5.3（本地存储）
- 本地 JSON 数据，完全离线运行

## 项目结构

```
lib/
├── app/            # 桌面 Shell（NavigationRail 9 区）、go_router 路由、主题
├── models/         # 数据模型（29 个）
├── pages/          # 页面（16 个）
├── repositories/   # 数据仓库层（15 个，含知识图谱/内容包仓库）
├── services/       # 业务逻辑（10 个）
├── state/          # Riverpod Provider（19 个）
├── utils/          # 搜索等工具
└── widgets/        # 可复用组件（14 个，含 knowledge 知识内容组件 5 个）

assets/data/
├── knowledge/         # 知识图谱 JSON（io_v4_4.json，唯一 SoT）
├── knowledge_content/ # 知识点内容包（content_index 33 分片 + item_part_index）
├── cpp/               # C++ 学习单元 + 动画数据
│   └── animations/    # 115 个动画 JSON + manifest
├── algorithm/         # 算法学习单元 + manifest
├── math/              # 数学学习单元 + manifest
├── lessons/           # BFS 课程
├── quizzes/           # BFS 题库
└── mistakes/          # BFS 常见错误

tools/publish/      # 离线生产管线（图谱映射、内容分片索引生成）
test/               # 单元测试 + Widget 测试 + 资产验证测试（468 用例）
```

## 运行方式

```bash
flutter pub get
flutter run -d windows
```

## 测试方式

```bash
flutter test
flutter analyze
```

测试覆盖（468 用例）：模型 fromJson、知识图谱解析与验证、内容包索引/按需加载/降级、C++/算法/数学资产完整性校验、动画 manifest 一致性、搜索功能、go_router 路由与深链、桌面适配（1366x768 / 1920x1080 / 高 DPI / 窗口缩放 / 键盘导航）、Widget smoke 测试。

## 打包方式

```bash
flutter build windows --release
```

Windows 打包需要 Visual Studio C++ 工具链；若构建报开发者模式相关错误，需在系统设置中开启「开发者模式」（当前环境下该步骤受 BLK-001 阻塞）。

```bash
flutter build apk --release   # Android 端（历史支持）
```

注意：APK 当前使用 debug 签名，发布前需配置自己的签名密钥。
