# 算法通

> 历史包名 `bfs_learn`，产品展示名为「算法通」。

面向信息学竞赛初学者的离线算法学习 App，涵盖 C++ 语法基础、算法、数据结构、竞赛数学等知识点。

## 功能模块

| 模块 | 功能 |
|------|------|
| 知识地图 | 按分类、章节浏览全部知识点（387 项），查看前置依赖关系 |
| 学习单元 | 每个知识点包含学习目标、讲解、示例代码、常见错误、练习、小测 |
| 动画演示 | 93 个算法动画（排序、搜索、图论等），逐步可视化代码执行过程 |
| 章节小测 | 每个章节配套选择题测验，即时反馈 + 解析 |
| 搜索 | 按名称、别名、讲解、常见错误等全文搜索知识点 |
| 学习进度 | 本地持久化学习记录、测验成绩、错题集 |
| BFS 专题 | BFS 知识讲解、迷宫动画、选择题训练、常见错误、教师演示模式 |
| 设置 | 字体大小、深色/浅色主题、多语言切换、清除进度 |

## 知识体系（5 大分类）

| 分类 | 章节数 | 知识点数 | 数据位置 |
|------|--------|----------|----------|
| C++ 语法 | 10 sections (1.x) + 9 sections (5.x) | ~247 units | `assets/data/cpp/` |
| 算法 | 14 sections (2.x + 3.x) | ~40 items | `assets/data/algorithm/` |
| 数据结构 | 含在知识图谱中 | ~54 items | — |
| 算法竞赛数学 | 7 sections (4.x) | ~50 items | `assets/data/math/` |
| C++ 编程/调试技巧 | 9 sections (5.x) | ~102 items | 含在 `assets/data/cpp/` |

知识图谱文件：`assets/data/knowledge/io_v4_4.json`

## 技术栈

- Flutter 3.7+ / Dart
- flutter_riverpod ^2.6.1（状态管理）
- shared_preferences ^2.5.3（本地存储）
- path_provider ^2.1.5
- 本地 JSON 数据，完全离线运行

## 项目结构

```
lib/
├── app/            # MaterialApp、路由、主题
├── models/         # 数据模型（22 个）
├── pages/          # 页面（16 个）
├── repositories/   # 数据仓库层（13 个）
├── services/       # 业务逻辑（5 个）
├── state/          # Riverpod Provider（18 个）
├── utils/          # 搜索等工具
└── widgets/        # 可复用组件（6 个）

assets/data/
├── knowledge/      # 知识图谱 JSON（io_v4_4.json）
├── cpp/            # C++ 学习单元 + 动画数据
│   └── animations/ # 93 个动画 JSON + manifest
├── algorithm/      # 算法学习单元 + manifest
├── math/           # 数学学习单元 + manifest
├── lessons/        # BFS 课程
├── quizzes/        # BFS 题库
└── mistakes/       # BFS 常见错误

test/               # 单元测试 + 资产验证测试
```

## 运行方式

```bash
flutter pub get
flutter run
```

## 测试方式

```bash
flutter test
flutter analyze
```

测试覆盖：模型 fromJson、知识图谱解析与验证、C++/算法/数学资产完整性校验、动画 manifest 一致性、搜索功能、Widget smoke 测试。

## 打包方式

```bash
flutter build apk --release
```

APK 输出路径：`build/app/outputs/flutter-apk/app-release.apk`

注意：当前使用 debug 签名，发布前需配置自己的签名密钥。
