import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/app/app_router.dart';
import 'package:bfs_learn/app/desktop_shell.dart';

/// M1-6 桌面适配验证（指导书 03 任务 7）：
/// 至少验证 Windows 1366x768 / 1920x1080 / 高 DPI / 窗口缩放 / 键盘导航基本可用。
///
/// 说明：pumpWidget/pump 成功即代表该尺寸下无 RenderFlex 溢出
/// （测试框架会把溢出错误上报为用例失败）。
void main() {
  setUp(() {
    // Shell 预建全部分支根页面（含设置页），测试环境需 mock 平台通道
    SharedPreferences.setMockInitialValues({});
    PackageInfo.setMockInitialValues(
      appName: '算法通',
      packageName: 'com.winknow.suanfatong',
      version: '1.0.0',
      buildNumber: '1',
      buildSignature: '',
    );
  });

  Widget host(GoRouter router) =>
      ProviderScope(child: MaterialApp.router(routerConfig: router));

  /// 按逻辑分辨率 + 设备像素比模拟桌面窗口。
  void setWindow(WidgetTester tester, Size logical, double dpr) {
    tester.view.physicalSize = logical * dpr;
    tester.view.devicePixelRatio = dpr;
    addTearDown(() {
      tester.view.resetPhysicalSize();
      tester.view.resetDevicePixelRatio();
    });
  }

  NavigationRail railOf(WidgetTester tester) =>
      tester.widget<NavigationRail>(find.byType(NavigationRail));

  testWidgets('1366x768 @1.0：扩展导航栏布局完整渲染', (tester) async {
    setWindow(tester, const Size(1366, 768), 1.0);
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 300));

    expect(find.byType(DesktopShell), findsOneWidget);
    final rail = railOf(tester);
    expect(rail.destinations.length, 9);
    expect(rail.extended, isTrue, reason: '1366 逻辑宽度 >= 1000 应为扩展栏');
    // 扩展栏应直接展示全部 9 个导航区文字标签
    for (final label in [
      '首页',
      '知识图谱',
      '学习中心',
      '题目训练',
      '编程工作台',
      'AI 助手',
      '课堂',
      '学习记录',
      '设置',
    ]) {
      expect(find.text(label), findsWidgets);
    }
  });

  testWidgets('1920x1080 @1.0：全高清下扩展栏与内容区正常', (tester) async {
    setWindow(tester, const Size(1920, 1080), 1.0);
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 300));

    final rail = railOf(tester);
    expect(rail.extended, isTrue);
    expect(rail.selectedIndex, 0);
    // 导航栏贴左、内容区占据剩余宽度：rail 右边界应小于屏幕宽度
    final railRect = tester.getRect(find.byType(NavigationRail));
    expect(railRect.left, 0);
    expect(railRect.right, lessThan(1920));
  });

  testWidgets('高 DPI：1.25 缩放逻辑 1536x864 扩展栏、2.0 缩放逻辑 960x540 收起栏', (
    tester,
  ) async {
    // Windows 常见 125% 缩放：物理 1920x1080 @1.25 → 逻辑 1536x864
    setWindow(tester, const Size(1536, 864), 1.25);
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 300));
    expect(railOf(tester).extended, isTrue, reason: '1536 >= 1000 应为扩展栏');

    // 200% 高 DPI 缩放：同一物理屏 → 逻辑 960x540，低于断点应收起
    tester.view.physicalSize = const Size(1920, 1080);
    tester.view.devicePixelRatio = 2.0;
    await tester.pump(const Duration(milliseconds: 200));
    final rail = railOf(tester);
    expect(rail.extended, isFalse, reason: '960 < 1000 应收起为窄栏');
    expect(rail.labelType, NavigationRailLabelType.selected);
  });

  testWidgets('窗口缩放：宽窄拖拽时导航栏在扩展/收起间切换', (tester) async {
    setWindow(tester, const Size(1280, 800), 1.0);
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 300));
    expect(railOf(tester).extended, isTrue);

    // 用户把窗口拖窄到 <1000
    tester.view.physicalSize = const Size(900, 700);
    tester.view.devicePixelRatio = 1.0;
    await tester.pump(const Duration(milliseconds: 200));
    expect(railOf(tester).extended, isFalse);

    // 再拉宽恢复扩展栏，导航状态不丢
    tester.view.physicalSize = const Size(1600, 900);
    tester.view.devicePixelRatio = 1.0;
    await tester.pump(const Duration(milliseconds: 200));
    final rail = railOf(tester);
    expect(rail.extended, isTrue);
    expect(rail.selectedIndex, 0);
    expect(find.byType(DesktopShell), findsOneWidget);
  });

  testWidgets('键盘导航：Tab 遍历焦点保留在 Shell 内且 Enter 不异常', (tester) async {
    setWindow(tester, const Size(1366, 768), 1.0);
    await tester.pumpWidget(host(buildAppRouter()));
    await tester.pump(const Duration(milliseconds: 300));

    for (var i = 0; i < 6; i++) {
      await tester.sendKeyEvent(LogicalKeyboardKey.tab);
      await tester.pump(const Duration(milliseconds: 50));
    }
    final focus = tester.binding.focusManager.primaryFocus;
    expect(focus, isNotNull, reason: 'Tab 之后应存在主焦点节点');
    expect(
      focus!.context?.findAncestorWidgetOfExactType<DesktopShell>(),
      isNotNull,
      reason: '焦点应保留在桌面 Shell 内（导航栏/内容区），不丢焦',
    );

    // 激活当前焦点（若落在导航项上则切换分支），流程不抛异常
    await tester.sendKeyEvent(LogicalKeyboardKey.enter);
    await tester.pump(const Duration(milliseconds: 200));
    expect(find.byType(DesktopShell), findsOneWidget);
    expect(railOf(tester).destinations.length, 9);
  });
}
