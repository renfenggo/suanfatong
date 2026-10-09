/// 云同步装配层（P1 最小用户闭环）：client / 队列 / 登录 / 编排器 provider。
///
/// 生产（main.dart）覆写两项：[sharedPreferencesProvider]（启动时已取得的
/// 实例）与 [offlineEventQueueProvider]（FileOfflineEventStore + 持久
/// deviceId）。默认值面向测试：内存队列 + 'local' 设备号，无需平台插件。
///
/// 平台地址解析优先级：环境变量 WINKNOW_PLATFORM_BASE_URL > 默认 dev 地址
/// （http://localhost:8000，契约 servers 第一项）。
library;

import 'dart:io';
import 'dart:math';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../services/api_sync_flag_source.dart';
import '../services/cloud_sync_scheduler.dart';
import '../services/cloud_sync_service.dart';
import '../services/learning_event_recorder.dart';
import '../services/learning_state_synchronizer.dart';
import '../services/offline_event_queue.dart';
import '../services/platform_api_client.dart';
import 'auth_provider.dart';
import 'progress_provider.dart'
    show cppProgressProvider, progressNamespaceProvider, progressServiceProvider;

/// SharedPreferences 实例（main 启动注入；测试用 overrideWithValue）。
final sharedPreferencesProvider = Provider<SharedPreferences>(
  (ref) => throw UnimplementedError('main() 启动时注入'),
);

/// 平台 HTTP 客户端（全局单例：登录/上报/flag 共用同一令牌）。
final platformApiClientProvider = Provider<PlatformApiClient>((ref) {
  return PlatformApiClient(baseUrl: resolvePlatformBaseUrl());
});

/// 离线事件队列（默认内存实现面向测试；生产覆写为文件持久化 + 命名空间
/// 工厂——N03 账号隔离：switchOwner 时换用对应账号的文件存储）。
final offlineEventQueueProvider = Provider<OfflineEventQueue>((ref) {
  return OfflineEventQueue(
    store: InMemoryOfflineEventStore(),
    deviceId: 'local',
  );
});

/// 学习事件记录器（学习行为 → 离线队列）。
final learningEventRecorderProvider = Provider<LearningEventRecorder>((ref) {
  return LearningEventRecorder(queue: ref.watch(offlineEventQueueProvider));
});

/// 云同步编排器（N02：无持久化凭证——重启后需经登录页重新建立会话，
/// 会话令牌由 AuthController 登录成功后 adoptSession 注入）。
final cloudSyncServiceProvider = Provider<CloudSyncService>((ref) {
  return CloudSyncService(
    client: ref.watch(platformApiClientProvider),
    queue: ref.watch(offlineEventQueueProvider),
    credentialProvider: () async => null,
    flagSource: ApiSyncFlagSource(client: ref.watch(platformApiClientProvider)),
  );
});

/// R06-1：服务端状态拉取合成器（换设备进度恢复）。
///
/// 依赖 progressServiceProvider（跟随当前账号命名空间重建）——账号切换
/// 后合成写入新账号的进度键，不会串账号。
final learningStateSynchronizerProvider =
    Provider<LearningStateSynchronizer>((ref) {
      return LearningStateSynchronizer(
        client: ref.watch(platformApiClientProvider),
        progressService: ref.watch(progressServiceProvider),
      );
    });

/// 完整同步轮（R06-1/R06-2 统一入口）：上报离线队列 → 成功后拉取服务端
/// 状态合成本地进度 → 刷新完成项 Notifier。
///
/// 手动同步（设置页）/登录成功/自动调度共用同一打包，保证任何入口触发
/// 的同步都含状态合成。合成是次要动作：上报已成功（outcome=synced）时
/// 合成失败（网络抖动等）不降级本轮结果，下个调度周期重试；刷新总是
/// 执行（合成落盘后 Notifier 需重建重载）。
Future<CloudSyncResult> runSyncRound(Ref ref) async {
  final result = await ref.read(cloudSyncServiceProvider).syncOnce();
  if (result.outcome == CloudSyncOutcome.synced) {
    try {
      await ref.read(learningStateSynchronizerProvider).pullAndMerge();
    } catch (_) {
      // 见上：合成失败不吞上报成功的事实，也不伪装进结果。
    }
    ref.invalidate(cppProgressProvider);
  }
  return result;
}

/// R06-2：自动同步调度器（默认 5 分钟周期轮询，兼网络恢复重试语义）。
///
/// App 启动即 start（见 BfsApp）；未登录轮次 skippedNoCredentials 无副作用。
final cloudSyncSchedulerProvider = Provider<CloudSyncScheduler>((ref) {
  final scheduler = CloudSyncScheduler(syncRound: () => runSyncRound(ref));
  ref.onDispose(scheduler.stop);
  return scheduler;
});

/// 登录会话控制器。
final authControllerProvider = StateNotifierProvider<AuthController, AuthSession>((
  ref,
) {
  return AuthController(
    client: ref.watch(platformApiClientProvider),
    prefs: ref.watch(sharedPreferencesProvider),
    deviceId: ref.watch(offlineEventQueueProvider).deviceId,
    queue: ref.watch(offlineEventQueueProvider),
    syncService: ref.watch(cloudSyncServiceProvider),
    onOwnerChanged: (namespace) =>
        ref.read(progressNamespaceProvider.notifier).state = namespace,
    onSessionCleared: () => ref.invalidate(cloudSyncServiceProvider),
  );
});

/// 读取（缺失则生成并持久化）稳定设备标识。
///
/// 同时用作离线队列 mutation_id 前缀与登录 device_id；跨重启稳定，
/// 保证幂等键不因设备号变化而语义漂移。
Future<String> ensureDeviceId(SharedPreferences prefs) async {
  const key = 'device_id';
  var id = prefs.getString(key);
  if (id == null || id.isEmpty) {
    final random = Random().nextInt(0x7FFFFFFF).toRadixString(36);
    id = 'dev-${DateTime.now().millisecondsSinceEpoch.toRadixString(36)}-$random';
    await prefs.setString(key, id);
  }
  return id;
}

/// 平台地址解析：环境变量优先，否则默认 dev 地址。
String resolvePlatformBaseUrl() {
  final fromEnv = Platform.environment['WINKNOW_PLATFORM_BASE_URL'];
  if (fromEnv != null && fromEnv.isNotEmpty) {
    return fromEnv;
  }
  return PlatformApiClient.defaultBaseUrl;
}
