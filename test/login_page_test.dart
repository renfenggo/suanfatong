import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/app/app_router.dart';
import 'package:bfs_learn/services/offline_event_queue.dart';
import 'package:bfs_learn/services/platform_api_client.dart';
import 'package:bfs_learn/state/auth_provider.dart';
import 'package:bfs_learn/state/cloud_sync_provider.dart';

/// 登录页 widget 测试（Fake 传输层，覆盖成功跳转与 401 错误展示）。
void main() {
  late _FakeTransport transport;
  late SharedPreferences prefs;

  setUp(() async {
    PackageInfo.setMockInitialValues(
      appName: '算法通',
      packageName: 'com.example.bfs_learn',
      version: '1.0.0',
      buildNumber: '1',
      buildSignature: '',
    );
    SharedPreferences.setMockInitialValues(<String, Object>{});
    prefs = await SharedPreferences.getInstance();
    transport = _FakeTransport();
  });

  Future<void> pumpApp(WidgetTester tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          sharedPreferencesProvider.overrideWithValue(prefs),
          platformApiClientProvider.overrideWithValue(
            PlatformApiClient(transport: transport, baseUrl: 'http://login.test'),
          ),
          offlineEventQueueProvider.overrideWithValue(
            OfflineEventQueue(store: InMemoryOfflineEventStore(), deviceId: 'dev-1'),
          ),
        ],
        child: MaterialApp.router(
          routerConfig: buildAppRouter(initialLocation: AppRouter.login),
        ),
      ),
    );
    await tester.pumpAndSettle();
  }

  testWidgets('登录成功：跳转设置页并持久化凭证', (tester) async {
    await pumpApp(tester);

    await tester.enterText(find.byKey(const Key('login_username')), 'zhang');
    await tester.enterText(find.byKey(const Key('login_password')), 'pw');
    await tester.tap(find.byKey(const Key('login_submit')));
    await tester.pumpAndSettle();

    expect(find.text('设置'), findsWidgets, reason: '已跳转设置页');
    await tester.scrollUntilVisible(find.text('退出登录'), 300);
    await tester.pumpAndSettle();
    expect(find.text('退出登录'), findsOneWidget, reason: '登录后云同步区显示退出登录入口');
    expect(prefs.getString(kAuthUsernameKey), 'zhang');

    // 让SnackBar 过期定时器走完，避免测试收尾的 pending timer 报错
    await tester.pump(const Duration(seconds: 4));
    await tester.pumpAndSettle();
  });

  testWidgets('登录失败（401）：展示错误信息，停留登录页', (tester) async {
    transport.loginFails = true;
    await pumpApp(tester);

    await tester.enterText(find.byKey(const Key('login_username')), 'zhang');
    await tester.enterText(find.byKey(const Key('login_password')), 'bad');
    await tester.tap(find.byKey(const Key('login_submit')));
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('login_error')), findsOneWidget);
    expect(find.text('用户名或密码错误'), findsOneWidget);
    expect(find.text('云同步'), findsNothing, reason: '未跳转设置页');
    expect(prefs.getString(kAuthUsernameKey), isNull);
  });

  testWidgets('空凭证提交：前端校验提示，不发请求', (tester) async {
    await pumpApp(tester);

    await tester.tap(find.byKey(const Key('login_submit')));
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('login_error')), findsOneWidget);
    expect(transport.requests, isEmpty);
  });
}

/// Fake 平台服务（登录页场景：login / feature-flags）。
class _FakeTransport implements PlatformHttpTransport {
  bool loginFails = false;
  int logins = 0;

  final List<PlatformHttpRequest> requests = <PlatformHttpRequest>[];

  @override
  Future<PlatformHttpResponse> send(PlatformHttpRequest request) async {
    requests.add(request);
    if (request.url.endsWith('/v1/auth/login')) {
      if (loginFails) {
        return _jsonResponse(
          401,
          '{"code":"UNAUTHORIZED","message":"用户名或密码错误","retryable":false}',
        );
      }
      logins++;
      return _jsonResponse(
        200,
        jsonEncode(<String, dynamic>{
          'access_token': 'at-$logins',
          'refresh_token': 'rt-1',
          'expires_in_s': 3600,
          'user': <String, dynamic>{
            'user_id': 'u-1',
            'display_name': '张三',
            'role': 'student',
          },
        }),
      );
    }
    if (request.url.endsWith('/v1/feature-flags')) {
      return _jsonResponse(200, '{"flags":{"cloud_sync":true}}');
    }
    if (request.url.endsWith('/v1/learning/events')) {
      return _jsonResponse(200, '{"accepted":[]}');
    }
    throw StateError('unexpected ${request.url}');
  }
}

PlatformHttpResponse _jsonResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: body);
