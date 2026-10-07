import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';

/// 桥接进程不可用（未安装/无法启动）。
class BridgeUnavailableException implements Exception {
  const BridgeUnavailableException(this.message);

  final String message;

  @override
  String toString() => 'BridgeUnavailableException: $message';
}

/// 桥接进程意外退出（pending 请求全部以本异常失败）。
class BridgeDisconnectedException implements Exception {
  const BridgeDisconnectedException([this.exitCode]);

  final int? exitCode;

  @override
  String toString() => 'BridgeDisconnectedException: exitCode=$exitCode';
}

/// 远端返回错误信封（{"id":...,"ok":false,"error":{code,message}}）。
class BridgeRemoteException implements Exception {
  const BridgeRemoteException({required this.code, required this.message});

  /// IPC 错误码（error_codes.md）。
  final String code;

  /// 错误描述。
  final String message;

  @override
  String toString() => 'BridgeRemoteException: $code $message';
}

/// 桥接进程句柄抽象（生产为 dart:io Process；测试提供 Fake）。
abstract class BridgeProcess {
  /// stdout 行流（每行一个响应 JSON）。
  Stream<String> get stdoutLines;

  /// stderr 行流（诊断日志）。
  Stream<String> get stderrLines;

  /// 写一行请求 JSON（UTF-8 + 换行 + flush）。
  Future<void> writeLine(String line);

  /// 关闭 stdin（触发桥接进程 EOF 退出）。
  Future<void> close();

  /// 强制终止进程。
  Future<void> kill();
}

/// 桥接进程启动器抽象（生产为 Process.start；测试提供 Fake）。
abstract class BridgeProcessLauncher {
  /// 尝试以指定可执行文件启动桥接进程；失败返回 null（上层转不可用状态）。
  Future<BridgeProcess?> tryStart(String executable);
}

/// 生产实现：dart:io Process。
class ProcessBridgeLauncher implements BridgeProcessLauncher {
  @override
  Future<BridgeProcess?> tryStart(String executable) async {
    if (!File(executable).existsSync()) {
      return null;
    }
    try {
      final process = await Process.start(executable, const <String>[]);
      return _ProcessBridgeProcess(process);
    } on Exception {
      return null;
    }
  }
}

class _ProcessBridgeProcess implements BridgeProcess {
  _ProcessBridgeProcess(this._process);

  final Process _process;

  @override
  Stream<String> get stdoutLines =>
      _process.stdout.transform(utf8.decoder).transform(const LineSplitter());

  @override
  Stream<String> get stderrLines =>
      _process.stderr.transform(utf8.decoder).transform(const LineSplitter());

  @override
  Future<void> writeLine(String line) async {
    _process.stdin.writeln(line);
    await _process.stdin.flush();
  }

  @override
  Future<void> close() => _process.stdin.close();

  @override
  Future<void> kill() async {
    _process.kill();
  }
}

/// DesktopBridge 行协议客户端（Flutter ↔ Winknow 唯一通道，ADR-002）。
///
/// 协议：子进程 stdin 每行一个请求 JSON
/// `{"id":..,"method":"..","params":{..},"trace_id":".."}`；
/// stdout 每行一个响应 `{"id":..,"ok":true,"result":..}` 或
/// `{"id":..,"ok":false,"error":{code,message}}`；日志只走 stderr。
/// 进程懒启动、跨请求复用；进程退出时 pending 请求全部失败。
class DesktopBridgeClient {
  DesktopBridgeClient({
    BridgeProcessLauncher? launcher,
    List<String>? candidateExecutables,
  }) : _launcher = launcher ?? ProcessBridgeLauncher(),
       _candidates = candidateExecutables ?? defaultCandidateExecutables();

  final BridgeProcessLauncher _launcher;
  final List<String> _candidates;

  BridgeProcess? _process;
  Future<BridgeProcess?>? _starting;
  StreamSubscription<String>? _stdoutSub;
  StreamSubscription<String>? _stderrSub;
  final Map<int, Completer<Map<String, dynamic>>> _pending = {};
  int _nextId = 1;
  bool _disposed = false;

  /// 桥接可执行文件候选路径（按序探测）。
  static List<String> defaultCandidateExecutables() {
    final env = Platform.environment['WINKNOW_BRIDGE_EXE'];
    final exe = Platform.resolvedExecutable.replaceAll('/', r'\');
    final sep = exe.lastIndexOf(r'\');
    final beside = sep < 0 ? exe : '${exe.substring(0, sep)}\\Winknow.DesktopBridge.exe';
    const installed = r'C:\Program Files\Winknow\Winknow.DesktopBridge.exe';
    return <String>[
      if (env != null && env.isNotEmpty) env,
      beside,
      installed,
    ];
  }

  /// 调用桥接方法并等待响应。
  ///
  /// [timeout] 到点抛 [TimeoutException]（连接保留，不杀进程）；
  /// ok=false 抛 [BridgeRemoteException]；进程不可用抛 [BridgeUnavailableException]。
  Future<Map<String, dynamic>> invoke(
    String method,
    Map<String, dynamic>? params, {
    Duration? timeout,
    String? traceId,
  }) async {
    if (_disposed) {
      throw const BridgeUnavailableException('bridge client disposed');
    }
    final process = await _ensureStarted();

    final id = _nextId++;
    final completer = Completer<Map<String, dynamic>>();
    _pending[id] = completer;

    final request = <String, dynamic>{
      'id': id,
      'method': method,
      if (params != null) 'params': params,
      if (traceId != null) 'trace_id': traceId,
    };
    try {
      await process.writeLine(jsonEncode(request));
    } on Exception {
      _pending.remove(id);
      rethrow;
    }

    final future = completer.future;
    try {
      if (timeout == null) {
        return await future;
      }
      return await future.timeout(timeout);
    } on TimeoutException {
      _pending.remove(id);
      rethrow;
    }
  }

  /// 关闭连接（stdin EOF → 桥接自然退出；兜底 kill）。
  Future<void> dispose() async {
    if (_disposed) {
      return;
    }
    _disposed = true;
    await _stdoutSub?.cancel();
    await _stderrSub?.cancel();
    final process = _process;
    if (process != null) {
      await process.close();
      await process.kill();
    }
    _failPending(const BridgeDisconnectedException());
    _process = null;
  }

  Future<BridgeProcess> _ensureStarted() async {
    final existing = _process;
    if (existing != null) {
      return existing;
    }
    final process = await (_starting ??= _start());
    if (process == null) {
      // 理论不可达（_start 失败时已抛出并重置 _starting）；兜底防御。
      _starting = null;
      throw const BridgeUnavailableException('bridge start failed');
    }
    return process;
  }

  Future<BridgeProcess?> _start() async {
    for (final executable in _candidates) {
      final process = await _launcher.tryStart(executable);
      if (process == null) {
        continue;
      }
      _process = process;
      _stdoutSub = process.stdoutLines.listen(_onResponseLine,
          onError: (Object _) => _onProcessGone(null),
          onDone: () => _onProcessGone(null));
      _stderrSub = process.stderrLines.listen(
        (line) => debugPrint('[bridge] $line'),
        onError: (Object _) {},
      );
      return process;
    }
    _starting = null;
    throw BridgeUnavailableException(
      'Winknow.DesktopBridge.exe not found (tried: ${_candidates.join('; ')})',
    );
  }

  void _onResponseLine(String line) {
    if (line.trim().isEmpty) {
      return;
    }
    Map<String, dynamic> response;
    try {
      final decoded = jsonDecode(line);
      if (decoded is! Map<String, dynamic>) {
        return;
      }
      response = decoded;
    } on FormatException {
      return;
    }
    final id = response['id'];
    if (id is! int) {
      return;
    }
    final completer = _pending.remove(id);
    if (completer == null || completer.isCompleted) {
      return;
    }
    if (response['ok'] == true) {
      completer.complete(_asObject(response['result']));
    } else {
      final error = response['error'];
      completer.completeError(BridgeRemoteException(
        code: error is Map<String, dynamic> ? '${error['code']}' : 'UNKNOWN',
        message: error is Map<String, dynamic> ? '${error['message']}' : 'unknown error',
      ));
    }
  }

  static Map<String, dynamic> _asObject(Object? result) {
    if (result is Map<String, dynamic>) {
      return result;
    }
    return <String, dynamic>{};
  }

  void _onProcessGone(int? exitCode) {
    final process = _process;
    if (process == null) {
      return;
    }
    _process = null;
    _starting = null;
    _failPending(BridgeDisconnectedException(exitCode));
  }

  void _failPending(BridgeDisconnectedException error) {
    final pending = List<MapEntry<int, Completer<Map<String, dynamic>>>>.from(
      _pending.entries,
    );
    _pending.clear();
    for (final entry in pending) {
      if (!entry.value.isCompleted) {
        entry.value.completeError(error);
      }
    }
  }
}
