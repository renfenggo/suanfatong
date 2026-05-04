# BFS 专题学习 App

信奥 BFS（广度优先搜索）专题离线学习应用，面向小学四年级及以上信息学竞赛初学者。

## 功能列表

| 模块 | 功能 |
|------|------|
| 知识讲解 | 10 课 BFS 知识（基础 5 课 + 迷宫应用 5 课），含代码示例和学习提示 |
| 选择题训练 | 20 道 BFS 选择题，即时反馈 + 解释说明，自动计分 |
| 动画演示 | 5×5 迷宫 BFS 19 步逐帧动画，支持播放/暂停/单步/重置 |
| 常见错误 | 8 个高频 BFS 编程错误，展示错误代码、原因、正确做法 |
| 教师模式 | 横屏大字演示，适合教室投屏教学 |
| 学习进度 | 本地持久化答题记录和成绩统计 |
| 设置 | 字体大小调节、深色/浅色主题、清除学习进度 |

## 技术栈

- Flutter 3.29.3 (Dart 3.7.2)
- flutter_riverpod ^2.6.1（状态管理）
- shared_preferences ^2.5.3（本地存储）
- 本地 JSON 数据（课程、题库、动画步骤、常见错误）

## 目录结构

```
lib/
├── app/            # MaterialApp、路由、主题
├── models/         # 数据模型（ContentManifest, Lesson, Quiz, BfsStep, Mistake 等）
├── pages/          # 页面（首页、课程、动画、答题、错题、进度、设置、教师模式）
├── repositories/   # 数据仓库层（JSON 加载、内容 manifest 解析）
├── services/       # 业务逻辑（答题历史、进度持久化）
├── state/          # Riverpod Provider（含 defaultContentIdsProvider 统一内容 ID）
└── widgets/        # 可复用组件（BfsGrid, CodeBlock, StepController 等）

assets/data/
├── content_manifest.json  # 内容清单（定义 topic、lessonSet、quizSet、动画场景等）
├── lessons/               # 课程 JSON（bfs_basic.json, bfs_maze.json）
├── quizzes/               # 题库 JSON（bfs_quiz.json）
├── mistakes/              # 常见错误 JSON（bfs_mistakes.json）
└── bfs_steps.json         # 动画步骤数据

test/               # 单元测试和 Widget 测试
```

## 内容系统架构

应用通过 `content_manifest.json` 驱动内容加载，实现内容与 UI 解耦：

```
content_manifest.json
  └── topics[]                # 学习专题（如 BFS）
        ├── lessonSets[]      # 课程集
        ├── quizSets[]        # 题库集
        ├── mistakeSets[]     # 常见错误集
        └── animationScenarios[]  # 动画场景
  └── modules[]               # 首页功能模块（标题、图标、路由、排序）
```

- `defaultContentIdsProvider`：从 manifest 的默认 topic 中提取第一个 lessonSet / quizSet / mistakeSet / animationScenario 的 ID，供各页面使用，无需硬编码
- 新增专题时只需在 manifest 中添加 topic 和对应的 JSON 数据文件，无需修改 Dart 代码

## 运行方式

```bash
flutter pub get
flutter run
```

## 测试方式

```bash
flutter test
```

当前包含 17 个测试：模型 fromJson 测试、JSON 数据验证测试、Widget smoke 测试。

## 打包方式

```bash
flutter build apk --release
```

APK 输出路径：`build/app/outputs/flutter-apk/app-release.apk`

注意：当前使用 debug 签名。发布前需要配置自己的签名密钥。

## 数据文件说明

| 文件 | 内容 |
|------|------|
| `assets/data/content_manifest.json` | 内容清单（topic 定义、模块路由、默认 ID） |
| `assets/data/lessons/bfs_basic.json` | 5 课 BFS 基础知识 |
| `assets/data/lessons/bfs_maze.json` | 5 课迷宫 BFS 应用 |
| `assets/data/quizzes/bfs_quiz.json` | 20 道 BFS 选择题 |
| `assets/data/mistakes/bfs_mistakes.json` | 8 个常见 BFS 编程错误 |
| `assets/data/bfs_steps.json` | 19 步 BFS 网格动画数据 |

## 后续计划

- 增加 DFS 专题学习模块
- 增加更多题库（中级/高级难度）
- 增加错题本功能
- 增加 BFS 代码编辑器（在线编写和测试 BFS 代码）
- 增加学习成就系统
