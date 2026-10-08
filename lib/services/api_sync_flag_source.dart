/// 基于 platform /v1/feature-flags 的云同步开关源。
///
/// N04（2026-10-08 第二轮复核）修正：
/// - CloudSyncService.syncOnce 已改为**先确保会话（[_ensureLoggedIn]，
///   含过期重登/无效判定）、后查 flag**，本源的查询一定发生在有效会话上；
/// - 异常**不吞**：401 / 网络失败 / 服务端错误原样上抛，由
///   CloudSyncService 统一分类（401 → loggedOut 清 token，网络 →
///   retryLater，其余按 retryable 分类）。此前"一切异常 → false"会把
///   失效 token 的 401 伪装成"业务开关关闭"，syncOnce 永远
///   skippedFlagOff 无法自愈。
///
/// 无 token（未登录）：返回 true 放行到登录步。
library;

import 'cloud_sync_service.dart';
import 'platform_api_client.dart';

class ApiSyncFlagSource implements SyncFlagSource {
  ApiSyncFlagSource({required PlatformApiClient client}) : _client = client;

  final PlatformApiClient _client;

  @override
  Future<bool> isCloudSyncEnabled() async {
    final token = _client.accessToken;
    if (token == null || token.isEmpty) {
      return true; // 未登录：放行到登录步（见库注释）。
    }
    final flags = await _client.fetchFeatureFlags();
    return flags['cloud_sync'] ?? false;
  }
}
