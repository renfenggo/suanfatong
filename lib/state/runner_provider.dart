import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../services/desktop_bridge_client.dart';
import '../services/runner_service.dart';

/// DesktopBridge 客户端（全局单例：懒启动、跨请求复用进程）。
final desktopBridgeClientProvider = Provider<DesktopBridgeClient>((ref) {
  final client = DesktopBridgeClient();
  ref.onDispose(() => client.dispose());
  return client;
});

/// Runner 服务（经 DesktopBridge 行协议）。
final runnerServiceProvider = Provider<RunnerService>((ref) {
  return BridgeRunnerService(ref.watch(desktopBridgeClientProvider));
});
