/// 自动同步调度器（R06-2，GO_LIVE §3.4b）：启动 + 网络恢复自动同步。
///
/// 此前同步只有两个入口——登录成功触发一次 + 设置页手动同步；离线期间
/// 积压的事件需等用户再次手动操作。本调度器补齐自动重试：
/// - [start]：周期触发一轮同步（默认 [interval] 5 分钟）。周期轮询同时
///   承担"网络恢复后自动冲刷"语义——断网期间各轮按 retryLater 保留队列，
///   网络恢复后的下一个周期自动完成上报（不引入 connectivity 插件）；
/// - [triggerNow]：登录成功/手动同步等事件的立即触发。一轮进行中返回
///   null（调用方可提示"同步进行中"），不排队不重入；
/// - 未登录轮次由 [CloudSyncService.syncOnce] 判 skippedNoCredentials，
///   队列与偏好无任何副作用，调度常开无害。
library;

import 'dart:async';

import 'cloud_sync_service.dart';

class CloudSyncScheduler {
  CloudSyncScheduler({
    required Future<CloudSyncResult> Function() syncRound,
    this.interval = const Duration(minutes: 5),
  }) : _syncRound = syncRound;

  /// 周期调度间隔（测试可注入短间隔）。
  final Duration interval;

  final Future<CloudSyncResult> Function() _syncRound;

  Timer? _timer;
  bool _running = false;

  /// 调度是否已启动。
  bool get isRunning => _timer != null;

  /// 启动周期调度（已启动则幂等 no-op）。
  void start() {
    if (_timer != null) return;
    _timer = Timer.periodic(interval, (_) => unawaited(_run()));
  }

  /// 停止调度（进行中的一轮不被中断，完成后不再触发）。
  void stop() {
    _timer?.cancel();
    _timer = null;
  }

  /// 立即触发一轮同步（调度未启动时也可用）。
  ///
  /// 一轮进行中时返回 null；[syncRound] 抛出未预期异常时兜底返回 null
  /// （不终止后续调度）。正常路径返回本轮 [CloudSyncResult]。
  Future<CloudSyncResult?> triggerNow() => _run();

  Future<CloudSyncResult?> _run() async {
    if (_running) return null;
    _running = true;
    try {
      return await _syncRound();
    } catch (_) {
      // 兜底防未预期异常终止调度循环；syncRound 契约应自行把基础设施
      // 错误分类进 CloudSyncResult（retryLater 等），此处不吞业务信息。
      return null;
    } finally {
      _running = false;
    }
  }
}
