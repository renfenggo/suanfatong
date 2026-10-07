import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/runner_models.dart';
import '../state/runner_provider.dart';

/// M3-8 最小编程工作台：编辑 C++ 源码，经 DesktopBridge 行协议
/// 编译并安全运行，展示 stdout/stderr/编译诊断与执行状态。
///
/// 依赖注入：测试经 `runnerServiceProvider.overrideWithValue(...)` 注入 Fake。
class WorkbenchPage extends ConsumerStatefulWidget {
  const WorkbenchPage({super.key});

  @override
  ConsumerState<WorkbenchPage> createState() => _WorkbenchPageState();
}

/// 默认模板（中文注释的 hello world）。
const String kWorkbenchDefaultSource = '''
#include <iostream>
using namespace std;

int main() {
    cout << "你好，算法通！" << endl;
    return 0;
}
''';

class _WorkbenchPageState extends ConsumerState<WorkbenchPage> {
  late final TextEditingController _codeController;
  late final TextEditingController _stdinController;
  RunnerLanguage _language = RunnerLanguage.cpp14;
  List<RunnerLanguage> _languages = const [RunnerLanguage.cpp14];
  bool _bridgeAvailable = true;
  bool _busy = false;
  RunnerResult? _result;
  String? _error;

  @override
  void initState() {
    super.initState();
    _codeController = TextEditingController(text: kWorkbenchDefaultSource);
    _stdinController = TextEditingController();
    Future.microtask(_loadCapabilities);
  }

  @override
  void dispose() {
    _codeController.dispose();
    _stdinController.dispose();
    super.dispose();
  }

  Future<void> _loadCapabilities() async {
    try {
      final caps = await ref.read(runnerServiceProvider).getCapabilities();
      if (!mounted) {
        return;
      }
      setState(() {
        _bridgeAvailable = caps.available || caps.languages.isNotEmpty;
        if (caps.languages.isNotEmpty) {
          _languages = caps.languages;
          if (!_languages.contains(_language)) {
            _language = _languages.first;
          }
        }
      });
    } on Exception {
      // 桥接不可用（未安装/无法启动/超时）：降级提示，仍允许编辑代码。
      if (mounted) {
        setState(() => _bridgeAvailable = false);
      }
    }
  }

  Future<void> _run() async {
    if (_busy) {
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
      _result = null;
    });
    try {
      final result = await ref
          .read(runnerServiceProvider)
          .execute(
            source: _codeController.text,
            stdin: _stdinController.text,
            language: _language,
          );
      if (mounted) {
        setState(() => _result = result);
      }
    } on Exception catch (e) {
      if (mounted) {
        setState(() => _error = e.toString());
      }
    } finally {
      if (mounted) {
        setState(() => _busy = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('编程工作台')),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final wide = constraints.maxWidth >= 1000;
            final editor = _buildEditor();
            final output = _buildOutput();
            if (wide) {
              return Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(child: editor),
                  const VerticalDivider(width: 1),
                  Expanded(child: output),
                ],
              );
            }
            return Column(
              children: [
                Expanded(flex: 5, child: editor),
                const Divider(height: 1),
                Expanded(flex: 4, child: output),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildEditor() {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            children: [
              DropdownButton<RunnerLanguage>(
                key: const Key('workbench_language_dropdown'),
                value: _language,
                items: [
                  for (final lang in _languages)
                    DropdownMenuItem(value: lang, child: Text(lang.wireName)),
                ],
                onChanged:
                    _busy
                        ? null
                        : (lang) {
                          if (lang != null) {
                            setState(() => _language = lang);
                          }
                        },
              ),
              const SizedBox(width: 12),
              FilledButton.icon(
                key: const Key('workbench_run_button'),
                onPressed: _busy ? null : _run,
                icon:
                    _busy
                        ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                        : const Icon(Icons.play_arrow),
                label: Text(_busy ? '运行中…' : '运行'),
              ),
              const Spacer(),
              Text(
                '通过本地沙箱运行器执行（受限令牌 + Job Object）',
                style: theme.textTheme.bodySmall?.copyWith(
                  color: theme.colorScheme.outline,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          if (!_bridgeAvailable) _buildUnavailableBanner(),
          Expanded(
            child: TextField(
              key: const Key('workbench_code_field'),
              controller: _codeController,
              maxLines: null,
              expands: true,
              textAlignVertical: TextAlignVertical.top,
              style: TextStyle(
                fontFamily: 'monospace',
                fontFamilyFallback: const ['Consolas', 'Courier New'],
                fontSize: 14,
              ),
              decoration: const InputDecoration(
                hintText: '在此编写 C++ 代码…',
                border: OutlineInputBorder(),
                isDense: true,
              ),
            ),
          ),
          const SizedBox(height: 8),
          TextField(
            key: const Key('workbench_stdin_field'),
            controller: _stdinController,
            maxLines: 3,
            style: const TextStyle(fontFamily: 'monospace', fontSize: 13),
            decoration: const InputDecoration(
              labelText: '标准输入（可选）',
              border: OutlineInputBorder(),
              isDense: true,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildUnavailableBanner() {
    return Container(
      key: const Key('workbench_bridge_unavailable'),
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.orange.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.orange.shade200),
      ),
      child: const Row(
        children: [
          Icon(Icons.warning_amber_rounded, color: Colors.orange),
          SizedBox(width: 8),
          Expanded(
            child: Text(
              '未连接 Winknow 桥接，暂无法编译运行；可继续编辑代码。'
              '（安装 Winknow 或设置 WINKNOW_BRIDGE_EXE 后重试）',
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOutput() {
    final theme = Theme.of(context);
    final result = _result;
    final compileDiag =
        (result?.status == RunnerStatus.compileFailed)
            ? result?.compileDiagnostics
            : null;
    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _buildStatusLine(result, theme),
          if (_error != null)
            Container(
              key: const Key('workbench_error_banner'),
              margin: const EdgeInsets.only(top: 8),
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: theme.colorScheme.errorContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                _error!,
                key: const Key('workbench_error_text'),
                style: TextStyle(color: theme.colorScheme.onErrorContainer),
              ),
            ),
          const SizedBox(height: 8),
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _buildOutputSection(
                    key: const Key('workbench_stdout'),
                    title: '标准输出 stdout',
                    text: result?.stdout,
                    mono: true,
                  ),
                  if (result?.stderr?.isNotEmpty == true)
                    _buildOutputSection(
                      key: const Key('workbench_stderr'),
                      title: '标准错误 stderr',
                      text: result?.stderr,
                      mono: true,
                    ),
                  if (compileDiag?.isNotEmpty == true)
                    _buildOutputSection(
                      key: const Key('workbench_diagnostics'),
                      title: '编译诊断',
                      text: compileDiag,
                      mono: false,
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusLine(RunnerResult? result, ThemeData theme) {
    if (result == null) {
      return Text(
        _busy ? '正在提交…' : '点击「运行」编译并执行代码',
        style: theme.textTheme.bodySmall,
      );
    }
    final parts = <String>[
      '状态：${result.status.displayName}',
      '耗时：${result.elapsedMs} ms',
      if (result.peakMemoryKb != null) '峰值内存：${result.peakMemoryKb} KB',
      if (result.runExitCode != null) '退出码：${result.runExitCode}',
      if (result.compileExitCode != null)
        '编译退出码：${result.compileExitCode}',
      if (result.outputTruncated) '输出已截断',
    ];
    return Text(
      parts.join('　|　'),
      key: const Key('workbench_status_line'),
      style: theme.textTheme.bodySmall?.copyWith(
        fontWeight: FontWeight.w600,
        color: switch (result.status) {
          RunnerStatus.runOk => Colors.green.shade700,
          RunnerStatus.compiledOk => Colors.green.shade700,
          RunnerStatus.compileFailed => theme.colorScheme.error,
          RunnerStatus.runFailed => theme.colorScheme.error,
          RunnerStatus.runTimeout => Colors.orange.shade800,
          RunnerStatus.resourceLimit => Colors.orange.shade800,
          _ => theme.colorScheme.onSurface,
        },
      ),
    );
  }

  Widget _buildOutputSection({
    required Key key,
    required String title,
    required String? text,
    required bool mono,
  }) {
    final theme = Theme.of(context);
    return Container(
      key: key,
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            title,
            style: theme.textTheme.labelSmall?.copyWith(
              color: theme.colorScheme.outline,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            text ?? '',
            style: mono
                ? const TextStyle(fontFamily: 'monospace', fontSize: 13)
                : const TextStyle(fontSize: 13),
          ),
        ],
      ),
    );
  }
}
