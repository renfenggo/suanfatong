import 'package:flutter/material.dart';
import '../app/router.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final items = [
      _MenuItem(
        title: 'BFS 知识讲解',
        subtitle: '从零开始理解广度优先搜索',
        icon: Icons.menu_book,
        color: const Color(0xFF4A90D9),
        route: AppRouter.lesson,
      ),
      _MenuItem(
        title: 'BFS 动画演示',
        subtitle: '一步步看 BFS 如何搜索',
        icon: Icons.play_circle_filled,
        color: const Color(0xFF50C878),
        route: AppRouter.animation,
      ),
      _MenuItem(
        title: '选择题训练',
        subtitle: '测试你的 BFS 知识',
        icon: Icons.quiz,
        color: const Color(0xFFFF8C42),
        route: AppRouter.quiz,
      ),
      _MenuItem(
        title: '常见错误',
        subtitle: '学习别人踩过的坑',
        icon: Icons.warning_amber,
        color: const Color(0xFFE74C3C),
        route: AppRouter.mistake,
      ),
      _MenuItem(
        title: '老师演示模式',
        subtitle: '课堂投屏专用',
        icon: Icons.school,
        color: const Color(0xFF9B59B6),
        route: AppRouter.teacherMode,
      ),
      _MenuItem(
        title: '学习进度',
        subtitle: '查看你的学习记录',
        icon: Icons.bar_chart,
        color: const Color(0xFF1ABC9C),
        route: AppRouter.progress,
      ),
      _MenuItem(
        title: '设置',
        subtitle: '字体大小、主题等',
        icon: Icons.settings,
        color: const Color(0xFF95A5A6),
        route: AppRouter.settings,
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('BFS 专题学习')),
      body: SafeArea(
        child: Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 10),
              child: const Text(
                '一层一层扩展，理解队列和最短路',
                style: TextStyle(fontSize: 15, color: Color(0xFF666666)),
              ),
            ),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.only(bottom: 24),
                itemCount: items.length,
                itemBuilder: (context, index) {
                  final item = items[index];
                  return _MenuCard(item: item);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _MenuItem {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final String route;

  const _MenuItem({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.route,
  });
}

class _MenuCard extends StatelessWidget {
  final _MenuItem item;

  const _MenuCard({required this.item});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(context, item.route);
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: item.color.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(item.icon, color: item.color, size: 28),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.title,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      item.subtitle,
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF888888),
                      ),
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: Colors.grey[400]),
            ],
          ),
        ),
      ),
    );
  }
}
