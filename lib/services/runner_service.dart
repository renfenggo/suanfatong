import 'dart:async';

import '../models/runner_models.dart';
import 'desktop_bridge_client.dart';

/// Runner 服务抽象（工作台只依赖本接口；测试注入 Fake）。
abstract class RunnerService {
  /// 获取运行器能力快照（runner.get_capabilities，5s 超时）。
  Future<RunnerCapabilities> getCapabilities();

  /// 提交源码编译并运行（runner.execute）。
  Future<RunnerResult> execute({
    required String source,
    String? stdin,
    RunnerLanguage language = RunnerLanguage.cpp14,
    ResourceLimits limits = const ResourceLimits(),
  });
}

/// DesktopBridge 行协议实现（IPC method_registry.md：get_capabilities 5s / execute 90s，
/// 客户端留余量取 100s 覆盖桥接与管道开销）。
class BridgeRunnerService implements RunnerService {
  BridgeRunnerService(this._bridge);

  final DesktopBridgeClient _bridge;

  static const Duration _capabilitiesTimeout = Duration(seconds: 5);
  static const Duration _executeTimeout = Duration(seconds: 100);

  @override
  Future<RunnerCapabilities> getCapabilities() async {
    final result = await _bridge.invoke(
      'runner.get_capabilities',
      const <String, dynamic>{},
      timeout: _capabilitiesTimeout,
    );
    return RunnerCapabilities.fromJson(result);
  }

  @override
  Future<RunnerResult> execute({
    required String source,
    String? stdin,
    RunnerLanguage language = RunnerLanguage.cpp14,
    ResourceLimits limits = const ResourceLimits(),
  }) async {
    final requestId =
        'wb-${DateTime.now().millisecondsSinceEpoch}-${identityHashCode(this)}';
    final params = <String, dynamic>{
      'request_id': requestId,
      'language': language.wireName,
      'source': source,
      if (stdin != null && stdin.isNotEmpty) 'stdin': stdin,
      'limits': limits.toJson(),
    };
    final result = await _bridge.invoke(
      'runner.execute',
      params,
      timeout: _executeTimeout,
    );
    return RunnerResult.fromJson(result);
  }
}
