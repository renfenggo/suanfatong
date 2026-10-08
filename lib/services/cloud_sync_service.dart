/// 云同步编排器（M4-F2）：组合 [PlatformApiClient] 与 [OfflineEventQueue]。
///
/// 一轮同步（[syncOnce]）：flag 门控 → 确保登录（token 缓存 + 过期判断）→
/// 循环 nextBatch → uploadLearningEvents → completeBatch 直到队列清空或
/// 遇错。错误分类：网络失败/可重试服务端错误 → 保留队列停止本轮（稍后
/// 重试）；401 → 清 token 缓存并通知会话过期（队列保留）；其余服务端
/// 错误 → 停止本轮（队列保留）。不引入 UI 依赖与真实后端。
library;

import 'offline_event_queue.dart';
import 'platform_api_client.dart';
import 'platform_api_models.dart';

/// 云同步开关来源抽象（M4-F3 接 platform /v1/feature-flags）。
///
/// N04（2026-10-08 第二轮复核）：实现**不吞异常**——开关查询的网络失败、
/// 401 等错误原样上抛，由 [CloudSyncService.syncOnce] 统一分类
/// （retryLater / loggedOut / failed），不得把基础设施错误伪装成
/// "业务开关关闭"（skippedFlagOff）。
abstract class SyncFlagSource {
  /// cloud_sync 功能开关是否开启。
  ///
  /// 无会话（未登录）时可返回 true 放行到登录步。
  Future<bool> isCloudSyncEnabled();
}

/// 默认实现：全关（ADR-006 回滚 = 关闭 cloud_sync flag）。
class DisabledSyncFlagSource implements SyncFlagSource {
  const DisabledSyncFlagSource();

  @override
  Future<bool> isCloudSyncEnabled() async => false;
}

/// 登录凭证（M4-F3 由登录 UI 提供，本层只消费）。
class CloudSyncCredentials {
  const CloudSyncCredentials({
    required this.username,
    required this.password,
    this.deviceId,
  });

  final String username;
  final String password;
  final String? deviceId;
}

/// 一轮同步的结果分类。
enum CloudSyncOutcome {
  /// 队列清空：全部待上报事件已被服务端确认（accepted 或 duplicated）。
  synced,

  /// flag 关闭：不发上报请求、队列不动（N04：会话确保在 flag 查询之前，
  /// 登录请求可能已发出）。
  skippedFlagOff,

  /// 无可用凭证：未登录、队列不动。
  skippedNoCredentials,

  /// 会话失效（401）：token 缓存已清、onSessionExpired 已通知、队列保留。
  loggedOut,

  /// 网络失败或可重试服务端错误：队列保留，稍后重试。
  retryLater,

  /// 不可重试服务端错误（或服务端未确认本批任何事件）：队列保留，
  /// 需人工介入/诊断。
  failed,
}

/// 一轮同步结果。
class CloudSyncResult {
  const CloudSyncResult({
    required this.outcome,
    this.confirmedCount = 0,
    this.error,
    this.persistError,
  });

  final CloudSyncOutcome outcome;

  /// 本轮被服务端确认并移出队列的事件数。
  final int confirmedCount;

  /// 触发停止的异常（retryLater/loggedOut/failed 时携带）。
  final Object? error;

  /// 本轮 completeBatch 落盘失败（P1：队列行/水位分别记录）。
  ///
  /// 服务端已确认、内存已清理，但本地持久化失败——重启后该批事件会
  /// 按旧存储状态恢复并重复上报（服务端 mutation_id 幂等兜底）。
  /// outcome 仍为 synced（上报本身成功），上层据此观测/告警磁盘问题。
  final OfflinePersistErrors? persistError;
}

/// 云同步编排器。
///
/// token 缓存规则：登录成功后按 `登录时刻 + expires_in_s` 缓存有效期，
/// 剩余不足 [tokenExpiryMargin] 视为过期需重新登录；401 时立即失效。
class CloudSyncService {
  CloudSyncService({
    required PlatformApiClient client,
    required OfflineEventQueue queue,
    required Future<CloudSyncCredentials?> Function() credentialProvider,
    SyncFlagSource? flagSource,
    DateTime Function()? clock,
    this.tokenExpiryMargin = const Duration(seconds: 60),
    this.onSessionExpired,
  }) : _client = client,
       _queue = queue,
       _credentialProvider = credentialProvider,
       _flagSource = flagSource ?? const DisabledSyncFlagSource(),
       _clock = clock ?? DateTime.now;

  /// 判定 token 快过期的提前量。
  final Duration tokenExpiryMargin;

  /// 会话失效回调（401 时同步通知，UI 层据此引导重新登录）。
  final void Function()? onSessionExpired;

  final PlatformApiClient _client;
  final OfflineEventQueue _queue;
  final Future<CloudSyncCredentials?> Function() _credentialProvider;
  final SyncFlagSource _flagSource;
  final DateTime Function() _clock;

  AuthToken? _cachedToken;
  DateTime? _tokenExpiresAt;

  /// 当前缓存的令牌（未登录或已失效为 null；测试/诊断用）。
  AuthToken? get cachedToken => _cachedToken;

  /// N02（2026-10-08 第二轮复核）：登录页成功登录后注入会话令牌。
  ///
  /// 客户端不再持久化原始密码，重启后无存储凭证可自动重登——会话由
  /// 登录动作直接注入（token 缓存 + 有效期 + 客户端令牌）；过期后由
  /// [_ensureLoggedIn] 判定无效并落入 skippedNoCredentials（引导重新
  /// 登录），不再静默用保存的密码重登。
  void adoptSession(AuthToken token) {
    _cachedToken = token;
    _tokenExpiresAt = _clock().add(Duration(seconds: token.expiresInS));
    _client.accessToken = token.accessToken;
  }

  /// 执行一轮同步（幂等：可由定时器/网络恢复事件反复触发）。
  ///
  /// N04（2026-10-08 第二轮复核）顺序修正：**先确保会话、后查认证后的
  /// flag**。此前"先查 flag 后登录"令失效 token 的 flags 401 被开关源
  /// 吞成 false，syncOnce 永远 skippedFlagOff，到不了有效期检查与重登；
  /// 现在过期 token 在 [_ensureLoggedIn] 中被替换/判无效，flag 查询
  /// 一定发生在有效会话上，且查询异常按错误类别如实分类（网络 →
  /// retryLater，401 → loggedOut，其余服务端错误 → retryLater/failed），
  /// 不再伪装成业务开关关闭。
  Future<CloudSyncResult> syncOnce() async {
    try {
      final loggedIn = await _ensureLoggedIn();
      if (!loggedIn) {
        return const CloudSyncResult(outcome: CloudSyncOutcome.skippedNoCredentials);
      }
    } on PlatformNetworkException catch (error) {
      return CloudSyncResult(
        outcome: CloudSyncOutcome.retryLater,
        error: error,
      );
    } on PlatformServerException catch (error) {
      return _handleServerError(error, confirmedCount: 0);
    }

    // 登录后的权威 flag 判定（ApiSyncFlagSource 持有效 token 查询；
    // 异常不吞，见 SyncFlagSource 契约。静态源重复判定同一值，无副作用）。
    try {
      if (!await _flagSource.isCloudSyncEnabled()) {
        return const CloudSyncResult(outcome: CloudSyncOutcome.skippedFlagOff);
      }
    } on PlatformNetworkException catch (error) {
      return CloudSyncResult(
        outcome: CloudSyncOutcome.retryLater,
        error: error,
      );
    } on PlatformServerException catch (error) {
      return _handleServerError(error, confirmedCount: 0);
    }

    var confirmedCount = 0;
    OfflinePersistErrors? persistError;
    while (true) {
      final batch = await _queue.nextBatch();
      if (batch.isEmpty) {
        return CloudSyncResult(
          outcome: CloudSyncOutcome.synced,
          confirmedCount: confirmedCount,
          persistError: persistError,
        );
      }
      final pendingBefore = _queue.pendingCount;
      try {
        final result = await _client.uploadLearningEvents(batch);
        final persistErrors = await _queue.completeBatch(result);
        if (persistErrors.isNotEmpty) {
          persistError = persistErrors;
        }
      } on PlatformNetworkException catch (error) {
        return CloudSyncResult(
          outcome: CloudSyncOutcome.retryLater,
          confirmedCount: confirmedCount,
          error: error,
        );
      } on PlatformServerException catch (error) {
        return _handleServerError(error, confirmedCount: confirmedCount);
      }
      final removed = pendingBefore - _queue.pendingCount;
      confirmedCount += removed;
      if (removed == 0) {
        // 200 但本批无任何事件被确认：停止以防死循环，队列原样保留。
        return CloudSyncResult(
          outcome: CloudSyncOutcome.failed,
          confirmedCount: confirmedCount,
          error: StateError('服务端 200 但未确认本批任何事件（${batch.length} 条）'),
        );
      }
    }
  }

  /// 确保已登录：缓存 token 未过期则复用，否则取凭证重新登录。
  Future<bool> _ensureLoggedIn() async {
    final now = _clock();
    final token = _cachedToken;
    final expiresAt = _tokenExpiresAt;
    if (token != null &&
        expiresAt != null &&
        now.isBefore(expiresAt.subtract(tokenExpiryMargin))) {
      _client.accessToken = token.accessToken;
      return true;
    }
    _invalidateToken();

    final credentials = await _credentialProvider();
    if (credentials == null) {
      return false;
    }
    final fresh = await _client.login(
      username: credentials.username,
      password: credentials.password,
      deviceId: credentials.deviceId,
    );
    _cachedToken = fresh;
    _tokenExpiresAt = _clock().add(Duration(seconds: fresh.expiresInS));
    _client.accessToken = fresh.accessToken;
    return true;
  }

  /// 服务端错误统一分类：401 → 会话失效；retryable → 稍后重试；其余 → 失败。
  /// 三类均保留队列（事件不丢，等下轮或人工介入）。
  CloudSyncResult _handleServerError(
    PlatformServerException error, {
    required int confirmedCount,
  }) {
    if (error.statusCode == 401) {
      _invalidateToken();
      onSessionExpired?.call();
      return CloudSyncResult(
        outcome: CloudSyncOutcome.loggedOut,
        confirmedCount: confirmedCount,
        error: error,
      );
    }
    return CloudSyncResult(
      outcome: error.envelope.retryable
          ? CloudSyncOutcome.retryLater
          : CloudSyncOutcome.failed,
      confirmedCount: confirmedCount,
      error: error,
    );
  }

  void _invalidateToken() {
    _cachedToken = null;
    _tokenExpiresAt = null;
    _client.accessToken = null;
  }
}
