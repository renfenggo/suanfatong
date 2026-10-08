/// 基于 platform /v1/feature-flags 的云同步开关源（两段式）。
///
/// 平台 flags 端点需要认证，而 CloudSyncService 的同步流程是"先查 flag
/// 后登录"，两者存在次序矛盾。两段式化解：
///
/// - 无 token（未登录）：返回 true 放行，让流程走到登录步；未登录且无
///   存储凭证时自然落入 skippedNoCredentials（无需先登录才能查 flag）；
/// - 有 token：GET /v1/feature-flags 权威判定 cloud_sync；CloudSyncService
///   在登录成功后复查一次，OFF → skippedFlagOff，不发任何 events。
///
/// 异常保守策略：401（token 失效）/ 网络失败 / 其他服务端错误 → false
/// （跳过本轮、队列保留，下轮由 CloudSyncService 自行换发 token）。
/// 本源不修改客户端任何状态（token 清理由 CloudSyncService 统一负责）。
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
    try {
      final flags = await _client.fetchFeatureFlags();
      return flags['cloud_sync'] ?? false;
    } on Exception {
      return false; // 保守：无法判定视为关闭，本轮跳过、队列保留。
    }
  }
}
