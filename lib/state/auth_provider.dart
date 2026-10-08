/// 登录会话状态与控制器（P1 最小用户闭环）。
///
/// V1 桌面简化：登录成功后把用户名/密码存入 SharedPreferences（供重启后
/// CloudSyncService 自动恢复登录），不引入独立 token 存储。登出清凭证。
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../services/platform_api_client.dart';
import '../services/platform_api_models.dart';

/// SharedPreferences 凭证键。
const String kAuthUsernameKey = 'auth_username';
const String kAuthPasswordKey = 'auth_password';
const String kAuthDisplayNameKey = 'auth_display_name';

/// 登录会话状态（由本地存储恢复或登录成功后更新）。
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

/// 登录会话控制器：登录（即时校验凭证）/ 登出 / 从本地存储恢复。
class AuthController extends StateNotifier<AuthSession> {
  AuthController({
    required PlatformApiClient client,
    required SharedPreferences prefs,
    required String deviceId,
    void Function()? onSessionCleared,
  }) : _client = client,
       _prefs = prefs,
       _deviceId = deviceId,
       _onSessionCleared = onSessionCleared,
       super(const AuthSession()) {
    _restore();
  }

  static const String _usernameKey = kAuthUsernameKey;
  static const String _passwordKey = kAuthPasswordKey;
  static const String _displayNameKey = kAuthDisplayNameKey;

  final PlatformApiClient _client;
  final SharedPreferences _prefs;
  final String _deviceId;

  /// 凭证清除后的回调（容器层失效 CloudSyncService 的 token 缓存）。
  final void Function()? _onSessionCleared;

  void _restore() {
    final username = _prefs.getString(_usernameKey);
    if (username == null || username.isEmpty) {
      return;
    }
    state = AuthSession(
      username: username,
      displayName: _prefs.getString(_displayNameKey) ?? username,
      loggedIn: true,
    );
  }

  /// 登录：立即向平台校验凭证；成功后持久化凭证并写入客户端令牌。
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
    await _prefs.setString(_usernameKey, username);
    await _prefs.setString(_passwordKey, password);
    await _prefs.setString(_displayNameKey, displayName);
    state = AuthSession(username: username, displayName: displayName, loggedIn: true);
    return const AuthLoginResult(success: true);
  }

  /// 登出：清除本地凭证与客户端令牌，会话回到未登录。
  Future<void> logout() async {
    await _prefs.remove(_usernameKey);
    await _prefs.remove(_passwordKey);
    await _prefs.remove(_displayNameKey);
    _client.accessToken = null;
    state = const AuthSession();
    _onSessionCleared?.call();
  }
}
