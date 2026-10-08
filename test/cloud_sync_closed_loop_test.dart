import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/services/cloud_sync_service.dart';
import 'package:bfs_learn/services/offline_event_queue.dart';
import 'package:bfs_learn/services/platform_api_client.dart';
import 'package:bfs_learn/state/auth_provider.dart';
import 'package:bfs_learn/state/cloud_sync_provider.dart';
import 'package:bfs_learn/state/progress_provider.dart';

/// P1 最小用户闭环验收：登录 → 学习（事件入队）→ 重启（新容器，prefs 与
/// 队列存储延续）→ 同步上报成功；flag 关闭与登出场景。
///
/// 全程 Fake 传输层 + 内存队列，不发真实网络请求。
void main() {
  late _FakePlatformTransport transport;
  late SharedPreferences prefs;
  late InMemoryOfflineEventStore store;

  setUp(() async {
    SharedPreferences.setMockInitialValues(<String, Object>{});
    prefs = await SharedPreferences.getInstance();
    store = InMemoryOfflineEventStore();
    transport = _FakePlatformTransport();
  });

  ProviderContainer newContainer() {
    final container = ProviderContainer(
      overrides: [
        sharedPreferencesProvider.overrideWithValue(prefs),
        platformApiClientProvider.overrideWithValue(
          PlatformApiClient(transport: transport, baseUrl: 'http://loop.test'),
        ),
        // N03：贴近生产装配——按命名空间换仓。共享内存存储模拟 zhang 的
        // 队列文件（重启延续），其余命名空间给独立空存储。
        offlineEventQueueProvider.overrideWithValue(
          OfflineEventQueue(
            store: InMemoryOfflineEventStore(),
            deviceId: 'dev-1',
            storeFactory: (ns) =>
                ns == 'zhang' ? store : InMemoryOfflineEventStore(),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);
    return container;
  }

  test('登录 → 学习入队 → 重启 → 同步：事件上报成功且进度保留', () async {
    final app = newContainer();

    // 1. 登录（实际页面路径：登录页提交 → AuthController.login）
    final login = await app
        .read(authControllerProvider.notifier)
        .login(username: 'zhang', password: 'pw');
    expect(login.success, isTrue, reason: '登录成功');
    expect(app.read(authControllerProvider).loggedIn, isTrue);

    // 2. 学习：C++ 单元完成 + 章节测验 → 两条事件入离线队列
    await app.read(cppProgressProvider.notifier).markCompleted('cpp-01');
    await app
        .read(cppQuizProgressProvider.notifier)
        .saveCppSectionQuizResult(
          sectionId: 'cpp-sec-1',
          score: 90,
          newWrongIds: const <String>{},
          correctedIds: const <String>{},
        );
    final queue1 = app.read(offlineEventQueueProvider);
    await queue1.load();
    expect(queue1.pendingCount, 2, reason: '学习事件已入队');

    // 3. 重启：新容器（内存会话丢弃；prefs 与队列存储延续——生产为文件）
    final restarted = newContainer();
    // N02：密码不再落盘，重启后回到未登录（仅预填用户名，需重新登录）。
    final restoredSession = restarted.read(authControllerProvider);
    expect(restoredSession.loggedIn, isFalse, reason: 'N02：无持久化凭证，重启后需重新登录');
    expect(restoredSession.username, 'zhang', reason: '用户名预填展示');
    expect(prefs.getString(kLegacyAuthPasswordKey), isNull, reason: 'N02：明文密码不落盘');

    // 4. 重启后未登录直接同步：skippedNoCredentials（N04：先确保会话再查
    // flag——flag 端点此时不应被查询）
    final blocked = await restarted.read(cloudSyncServiceProvider).syncOnce();
    expect(blocked.outcome, CloudSyncOutcome.skippedNoCredentials);
    expect(
      transport.requests.where((r) => r.url.endsWith('/v1/feature-flags')),
      isEmpty,
      reason: 'N04：无会话时先短路，不查认证后的 flag 端点',
    );

    // 5. 重新登录 → 同步：队列全部上报确认
    final relogin = await restarted
        .read(authControllerProvider.notifier)
        .login(username: 'zhang', password: 'pw');
    expect(relogin.success, isTrue, reason: '重新登录成功');
    final result = await restarted.read(cloudSyncServiceProvider).syncOnce();

    expect(result.outcome, CloudSyncOutcome.synced);
    expect(result.confirmedCount, 2);
    final queue2 = restarted.read(offlineEventQueueProvider);
    await queue2.load();
    expect(queue2.pendingCount, 0, reason: '重启后队列按持久化存储恢复并清空');

    // 服务端收到的事件内容（唯一一次 events 请求）
    final eventsRequests = transport.requests
        .where((r) => r.url.endsWith('/v1/learning/events'))
        .toList();
    expect(eventsRequests, hasLength(1));
    final events = (jsonDecode(eventsRequests.single.body!)
        as Map<String, dynamic>)['events'] as List<dynamic>;
    expect(events, hasLength(2));
    expect(
      events.map((e) => (e as Map<String, dynamic>)['kind']).toSet(),
      <String>{'knowledge_complete', 'quiz_submit'},
    );
    final quiz = events
        .map((e) => e as Map<String, dynamic>)
        .firstWhere((e) => e['kind'] == 'quiz_submit');
    expect(quiz['item_id'], 'cpp-sec-1');
    expect((quiz['payload'] as Map<String, dynamic>)['score'], 90);

    // 登录请求恰好两次：重启前手动一次 + 重启后手动重登一次
    expect(
      transport.requests.where((r) => r.url.endsWith('/v1/auth/login')).length,
      2,
    );

    // 6. 重启后本地进度保留（学习主线不断；zhang 命名空间）
    final progress = await restarted.read(progressProvider.future);
    expect(progress.completedCppItems, contains('cpp-01'));
  });

  test('flag 关闭（登录后复查 OFF）→ 不上报，事件保留待开启后同步', () async {
    transport.cloudSyncEnabled = false;
    final app = newContainer();

    final login = await app
        .read(authControllerProvider.notifier)
        .login(username: 'zhang', password: 'pw');
    expect(login.success, isTrue);

    await app.read(cppProgressProvider.notifier).markCompleted('cpp-01');
    final result = await app.read(cloudSyncServiceProvider).syncOnce();

    expect(result.outcome, CloudSyncOutcome.skippedFlagOff);
    expect(
      transport.requests.where((r) => r.url.endsWith('/v1/learning/events')),
      isEmpty,
    );
    final queue = app.read(offlineEventQueueProvider);
    await queue.load();
    expect(queue.pendingCount, 1, reason: '事件保留，等 flag 开启后上报');

    // flag 开启后再同步 → 上报成功（事件不丢失）
    transport.cloudSyncEnabled = true;
    final retry = await app.read(cloudSyncServiceProvider).syncOnce();
    expect(retry.outcome, CloudSyncOutcome.synced);
    expect(retry.confirmedCount, 1);
  });

  test('登出：凭证清除，后续同步 skippedNoCredentials，事件隔离保留', () async {
    final app = newContainer();
    await app
        .read(authControllerProvider.notifier)
        .login(username: 'zhang', password: 'pw');
    await app.read(cppProgressProvider.notifier).markCompleted('cpp-01');

    await app.read(authControllerProvider.notifier).logout();

    expect(app.read(authControllerProvider).loggedIn, isFalse);
    expect(prefs.getString(kAuthUsernameKey), isNull);
    final queue = app.read(offlineEventQueueProvider);
    await queue.load();
    // N03：登出切回未登录命名空间——zhang 的待上报事件不随 unowned 消费；
    // 本测试装配无 storeFactory（内存隔离语义），数据保留在存储中不丢。
    expect(queue.pendingCount, 0, reason: '登出后不消费任何账号的待上报事件');
    expect(await store.loadJsonEntries(), hasLength(1), reason: '学习事件隔离保留，不丢');

    final result = await app.read(cloudSyncServiceProvider).syncOnce();
    expect(result.outcome, CloudSyncOutcome.skippedNoCredentials);
  });

  test('登录失败（401）：状态未登录、凭证不落盘、错误信息可展示', () async {
    transport.loginFails = true;
    final app = newContainer();

    final result = await app
        .read(authControllerProvider.notifier)
        .login(username: 'zhang', password: 'bad');

    expect(result.success, isFalse);
    expect(result.errorMessage, '用户名或密码错误');
    expect(app.read(authControllerProvider).loggedIn, isFalse);
    expect(prefs.getString(kAuthUsernameKey), isNull);
  });
}

/// 有状态 Fake 平台服务：login / feature-flags / learning events 三端点。
class _FakePlatformTransport implements PlatformHttpTransport {
  bool cloudSyncEnabled = true;
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
      return _jsonResponse(
        200,
        jsonEncode(<String, dynamic>{
          'flags': <String, bool>{'cloud_sync': cloudSyncEnabled},
        }),
      );
    }
    if (request.url.endsWith('/v1/learning/events')) {
      final events = (jsonDecode(request.body!) as Map<String, dynamic>)['events']
          as List<dynamic>;
      return _jsonResponse(
        200,
        jsonEncode(<String, dynamic>{
          'accepted': events
              .map((e) => (e as Map<String, dynamic>)['event_id'])
              .toList(),
        }),
      );
    }
    throw StateError('unexpected ${request.url}');
  }
}

PlatformHttpResponse _jsonResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: body);
