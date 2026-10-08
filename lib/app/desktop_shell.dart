import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// 桌面 Shell 统一导航区定义（M1 指导书 9 区）
class ShellDestination {
  final String label;
  final IconData icon;
  final IconData selectedIcon;
  final String location;

  const ShellDestination({
    required this.label,
    required this.icon,
    required this.selectedIcon,
    required this.location,
  });
}

const List<ShellDestination> shellDestinations = [
  ShellDestination(
    label: '首页',
    icon: Icons.home_outlined,
    selectedIcon: Icons.home,
    location: '/',
  ),
  ShellDestination(
    label: '知识图谱',
    icon: Icons.hub_outlined,
    selectedIcon: Icons.hub,
    location: '/knowledge',
  ),
  ShellDestination(
    label: '学习中心',
    icon: Icons.school_outlined,
    selectedIcon: Icons.school,
    location: '/cpp_basic',
  ),
  ShellDestination(
    label: '题目训练',
    icon: Icons.edit_note_outlined,
    selectedIcon: Icons.edit_note,
    location: '/cpp_search',
  ),
  ShellDestination(
    label: '编程工作台',
    icon: Icons.terminal_outlined,
    selectedIcon: Icons.terminal,
    location: '/workbench',
  ),
  ShellDestination(
    label: 'AI 助手',
    icon: Icons.smart_toy_outlined,
    selectedIcon: Icons.smart_toy,
    location: '/ai_assistant',
  ),
  ShellDestination(
    label: '课堂',
    icon: Icons.cast_for_education_outlined,
    selectedIcon: Icons.cast_for_education,
    location: '/classroom',
  ),
  ShellDestination(
    label: '学习记录',
    icon: Icons.insights_outlined,
    selectedIcon: Icons.insights,
    location: '/progress',
  ),
  ShellDestination(
    label: '设置',
    icon: Icons.settings_outlined,
    selectedIcon: Icons.settings,
    location: '/settings',
  ),
];

/// 桌面统一壳：左侧 NavigationRail + 右侧内容区。
/// 每个导航区对应 StatefulShellRoute 的一个分支，切换时保留各分支导航状态。
class DesktopShell extends StatelessWidget {
  final StatefulNavigationShell navigationShell;

  const DesktopShell({super.key, required this.navigationShell});

  @override
  Widget build(BuildContext context) {
    final isWide = MediaQuery.sizeOf(context).width >= 1000;
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            extended: isWide,
            labelType:
                isWide
                    ? NavigationRailLabelType.none
                    : NavigationRailLabelType.selected,
            selectedIndex: navigationShell.currentIndex,
            onDestinationSelected:
                (index) => navigationShell.goBranch(
                  index,
                  // 再次点击当前导航区时回到该区根页面
                  initialLocation: index == navigationShell.currentIndex,
                ),
            destinations: [
              for (final destination in shellDestinations)
                NavigationRailDestination(
                  icon: Icon(destination.icon),
                  selectedIcon: Icon(destination.selectedIcon),
                  label: Text(destination.label),
                ),
            ],
          ),
          VerticalDivider(thickness: 1, width: 1, color: scheme.outlineVariant),
          Expanded(child: navigationShell),
        ],
      ),
    );
  }
}

/// 后续里程碑接入前的占位页（编程工作台 / AI 助手 / 课堂）。
class ShellPlaceholderPage extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;

  const ShellPlaceholderPage({
    super.key,
    required this.title,
    required this.description,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 64, color: scheme.outline),
            const SizedBox(height: 16),
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text(description, style: TextStyle(color: scheme.outline)),
            const SizedBox(height: 8),
            Text(
              '该模块正在开发中，暂未开放',
              style: TextStyle(color: scheme.outline, fontSize: 13),
            ),
          ],
        ),
      ),
    );
  }
}
