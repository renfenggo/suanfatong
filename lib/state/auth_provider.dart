/// 登录会话状态与控制器（P1 最小用户闭环）。
///
/// N02（2026-10-08 第二轮复核）：**不再持久化原始密码**——此前密码被
/// 原样写入 SharedPreferences（auth_password）并在重启后读回自动重登，
/// 属明文敏感数据落盘。现在：
/// - 仅保存用户名/显示名（普通偏好，用于界面展示）；
/// - 会话令牌由登录动作经 [CloudSyncService.adoptSession] 注入内存，
///   重启后回到未登录状态、需重新输入密码（报告允许的过渡形态；
///   后续接入可撤销会话凭据 + 操作系统保护存储）；
/// - 构造时清理历史遗留的 auth_password（升级迁移）。
///
/// N03（2026-10-08 第二轮复核）：登录/登出切换队列与进度的账号命名空间
/// （[OfflineEventQueue.switchOwner] + 进度命名空间回调），A 的离线事件
/// 与本地进度不再被下一个登录的 B 账号消费或看到。
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../services/cloud_sync_service.dart';
import '../services/offline_event_queue.dart';
import '../services/platform_api_client.dart';
import '../services/platform_api_models.dart' show AuthToken;

/// SharedPreferences 账号偏好键。
const String kAuthUsernameKey = 'auth_username';
const String kAuthDisplayNameKey = 'auth_display_name';

/// 历史版本持久化原始密码的键（N02：不再写入；构造时清理遗留数据）。
const String kLegacyAuthPasswordKey = 'auth_password';

/// 登录会话状态。
///
/// 重启后 [username]/[displayName] 从偏好恢复（预填展示），
/// [loggedIn] 为 false——需要重新登录才能恢复云同步。
class AuthSession {
  const AuthSession({this.username = '', this.displayName = '', this.loggedIn = false});

  final String username;
  final String displayName;
  final bool loggedIn;
}

/// 登录操作的即时结果（登录页展示错误用；不含令牌细节）。
class AuthLoginResult {
  const AuthLoginResult({required this.success, this.errorMessage});

  final bool success;
  final String? errorMessage;
}

/// 登录会话控制器：登录（即时校验凭证）/ 登出 / 偏好恢复。
class AuthController extends StateNotifier<AuthSession> {
  AuthController({
    required PlatformApiClient client,
    required SharedPreferences prefs,
    required String deviceId,
    required OfflineEventQueue queue,
    required CloudSyncService syncService,
    void Function(String? namespace)? onOwnerChanged,
    void Function()? onSessionCleared,
  }) : _client = client,
       _prefs = prefs,
       _deviceId = deviceId,
       _queue = queue,
       _syncService = syncService,
       _onOwnerChanged = onOwnerChanged,
       _onSessionCleared = onSessionCleared,
       super(const AuthSession()) {
    _restore();
  }

  final PlatformApiClient _client;
  final SharedPreferences _prefs;
  final String _deviceId;
  final OfflineEventQueue _queue;
  final CloudSyncService _syncService;

  /// 账号命名空间变化回调（进度等按账号隔离的存储跟随切换）。
  final void Function(String? namespace)? _onOwnerChanged;

  /// 凭证清除后的回调（容器层失效 CloudSyncService 的 token 缓存）。
  final void Function()? _onSessionCleared;

  void _restore() {
    // N02 升级迁移：清理历史版本遗留的明文密码（尽力而为）。
    _prefs.remove(kLegacyAuthPasswordKey);
    final username = _prefs.getString(kAuthUsernameKey);
    if (username == null || username.isEmpty) {
      return;
    }
    // 重启后不自动恢复登录（无持久化凭证），仅预填用户名/显示名。
    state = AuthSession(
      username: username,
      displayName: _prefs.getString(kAuthDisplayNameKey) ?? username,
      loggedIn: false,
    );
  }

  /// 登录：立即向平台校验凭证；成功后保存账号偏好、切换账号命名空间
  /// 并把会话令牌注入云同步服务（N02：密码不落盘）。
  Future<AuthLoginResult> login({
    required String username,
    required String password,
  }) async {
    if (username.isEmpty || password.isEmpty) {
      return const AuthLoginResult(success: false, errorMessage: '请输入用户名和密码');
    }
    final AuthToken token;
    try {
      token = await _client.login(
        username: username,
        password: password,
        deviceId: _deviceId,
      );
    } on PlatformServerException catch (error) {
      return AuthLoginResult(
        success: false,
        errorMessage: error.statusCode == 401
            ? '用户名或密码错误'
            : '登录失败（${error.envelope.code}）：${error.envelope.message}',
      );
    } on PlatformNetworkException catch (error) {
      return AuthLoginResult(
        success: false,
        errorMessage: error.kind == 'timeout' ? '连接超时，请检查网络后重试' : '网络连接失败，请检查网络',
      );
    }

    _client.accessToken = token.accessToken;
    final displayName = token.user.displayName.isEmpty ? username : token.user.displayName;
    await _prefs.setString(kAuthUsernameKey, username);
    await _prefs.setString(kAuthDisplayNameKey, displayName);

    // N03：队列与进度切换到该账号的命名空间（A 的离线事件不再随 B 上传）。
    await _queue.switchOwner(username);
    _onOwnerChanged?.call(username);

    // N02：会话令牌注入云同步（重启后无此内存会话，需重新登录）。
    _syncService.adoptSession(token);

    state = AuthSession(username: username, displayName: displayName, loggedIn: true);
    return const AuthLoginResult(success: true);
  }

  /// 登出：清除本地账号偏好与客户端令牌，队列/进度切回未登录命名空间，
  /// 会话回到未登录（未上报事件保留在原账号命名空间内，不丢）。
  Future<void> logout() async {
    await _prefs.remove(kAuthUsernameKey);
    await _prefs.remove(kAuthDisplayNameKey);
    _client.accessToken = null;
    await _queue.switchOwner(null);
    _onOwnerChanged?.call(null);
    state = const AuthSession();
    _onSessionCleared?.call();
  }
}
