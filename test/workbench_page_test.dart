import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/models/runner_models.dart';
import 'package:bfs_learn/pages/workbench_page.dart';
import 'package:bfs_learn/services/desktop_bridge_client.dart';
import 'package:bfs_learn/services/runner_service.dart';
import 'package:bfs_learn/state/runner_provider.dart';

/// 编程工作台页面测试（Fake RunnerService 注入，不触真实桥接）。
void main() {
  _FakeRunnerService fakeService() => _FakeRunnerService();

  Future<void> pumpPage(WidgetTester tester, RunnerService service) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [runnerServiceProvider.overrideWithValue(service)],
        child: const MaterialApp(home: WorkbenchPage()),
      ),
    );
    // 触发 initState 的 microtask 能力探测
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 50));
  }

  testWidgets('初始渲染：默认中文模板 + 运行入口', (tester) async {
    await pumpPage(tester, fakeService());

    final codeField = tester.widget<TextField>(
        find.byKey(const Key('workbench_code_field')));
    expect(codeField.controller!.text, contains('你好，算法通！'));
    expect(find.byKey(const Key('workbench_run_button')), findsOneWidget);
    expect(find.byKey(const Key('workbench_bridge_unavailable')),
        findsNothing, reason: '桥接可用时不应显示降级横幅');
  });

  testWidgets('点击运行：busy 状态后展示运行成功与 stdout', (tester) async {
    final service = fakeService()
      ..executeResult = const RunnerResult(
        requestId: 'wb-1',
        status: RunnerStatus.runOk,
        compileExitCode: 0,
        runExitCode: 0,
        stdout: '你好，算法通！',
        elapsedMs: 152,
        peakMemoryKb: 3072,
        timedOut: false,
        outputTruncated: false,
        artifactsCleaned: true,
      );
    await pumpPage(tester, service);

    await tester.tap(find.byKey(const Key('workbench_run_button')));
    await tester.pump(); // busy 渲染
    await tester.pump(const Duration(milliseconds: 50)); // 结果渲染

    final status = tester
        .widget<Text>(find.byKey(const Key('workbench_status_line')))
        .data!;
    expect(status, contains('运行成功'));
    expect(status, contains('152 ms'));
    expect(status, contains('3072 KB'));

    final stdoutTexts = tester.widgetList<Text>(find.descendant(
        of: find.byKey(const Key('workbench_stdout')),
        matching: find.byType(Text)));
    expect(stdoutTexts.map((t) => t.data ?? '').join('\n'),
        contains('你好，算法通！'));
  });

  testWidgets('编译失败：展示编译诊断区', (tester) async {
    final service = fakeService()
      ..executeResult = const RunnerResult(
        requestId: 'wb-2',
        status: RunnerStatus.compileFailed,
        compileExitCode: 1,
        compileDiagnostics: 'error: expected \';\' before "return"',
        elapsedMs: 300,
        timedOut: false,
        outputTruncated: false,
        artifactsCleaned: true,
      );
    await pumpPage(tester, service);

    await tester.tap(find.byKey(const Key('workbench_run_button')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 50));

    expect(find.byKey(const Key('workbench_diagnostics')), findsOneWidget);
    expect(
        find.textContaining("expected ';'"), findsOneWidget);
    expect(find.byKey(const Key('workbench_stdout')), findsOneWidget);
  });

  testWidgets('执行异常：展示错误条且可再次运行', (tester) async {
    final service = fakeService()
      ..executeError = const BridgeRemoteException(
          code: 'UNAVAILABLE', message: 'runner 未就绪');
    await pumpPage(tester, service);

    await tester.tap(find.byKey(const Key('workbench_run_button')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 50));

    expect(find.byKey(const Key('workbench_error_banner')), findsOneWidget);
    expect(find.byKey(const Key('workbench_error_text')), findsOneWidget);
    final runButton = tester.widget<FilledButton>(
        find.byKey(const Key('workbench_run_button')));
    expect(runButton.onPressed, isNotNull, reason: '异常后按钮应恢复可用');
  });

  testWidgets('stdin 与语言随请求透传', (tester) async {
    final service = fakeService();
    await pumpPage(tester, service);

    await tester.enterText(
        find.byKey(const Key('workbench_stdin_field')), '42');
    await tester.pump();
    await tester.tap(find.byKey(const Key('workbench_run_button')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 50));

    expect(service.lastSource, contains('#include <iostream>'));
    expect(service.lastStdin, '42');
    expect(service.lastLanguage, RunnerLanguage.cpp14);
  });

  testWidgets('桥接不可用：显示降级横幅但仍可编辑', (tester) async {
    final service = _FakeRunnerService(
      capabilitiesError: const BridgeUnavailableException('not found'),
    );
    await pumpPage(tester, service);

    expect(find.byKey(const Key('workbench_bridge_unavailable')),
        findsOneWidget);
    final codeField = tester.widget<TextField>(
        find.byKey(const Key('workbench_code_field')));
    expect(codeField.enabled, isNot(isFalse),
        reason: 'enabled 为 null 表示默认启用（可编辑）');
  });
}

/// 手写 Fake（项目惯例：不引入 mock 库）。
class _FakeRunnerService implements RunnerService {
  _FakeRunnerService({
    RunnerCapabilities? capabilities,
    this.capabilitiesError,
  }) : _capabilities = capabilities ??
            const RunnerCapabilities(
              available: true,
              languages: [RunnerLanguage.cpp14],
            );

  final RunnerCapabilities _capabilities;
  final Exception? capabilitiesError;

  RunnerResult? executeResult;
  Exception? executeError;

  String? lastSource;
  String? lastStdin;
  RunnerLanguage? lastLanguage;

  @override
  Future<RunnerCapabilities> getCapabilities() async {
    if (capabilitiesError != null) {
      throw capabilitiesError!;
    }
    return _capabilities;
  }

  @override
  Future<RunnerResult> execute({
    required String source,
    String? stdin,
    RunnerLanguage language = RunnerLanguage.cpp14,
    ResourceLimits limits = const ResourceLimits(),
  }) async {
    lastSource = source;
    lastStdin = stdin;
    lastLanguage = language;
    if (executeError != null) {
      throw executeError!;
    }
    return executeResult ??
        const RunnerResult(
          requestId: 'wb-default',
          status: RunnerStatus.runOk,
          elapsedMs: 1,
          timedOut: false,
          outputTruncated: false,
          artifactsCleaned: true,
        );
  }
}
