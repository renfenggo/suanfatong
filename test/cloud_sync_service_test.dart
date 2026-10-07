import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/cloud_sync_service.dart';
import 'package:bfs_learn/services/offline_event_queue.dart';
import 'package:bfs_learn/services/platform_api_client.dart';
import 'package:bfs_learn/services/platform_api_models.dart';

/// 云同步编排器测试（Fake 传输层 + 内存队列，不发真实网络请求）。
void main() {
  group('CloudSyncService flag 门控', () {
    test('默认 DisabledSyncFlagSource 全关：不发任何请求、不取凭证、队列不动', () async {
      final fake = _FakeTransport(_unexpectedTransport);
      final queue = _newQueue();
      await _enqueue(queue, 1);
      var credentialCalls = 0;
      final service = CloudSyncService(
        client: _client(fake),
        queue: queue,
        credentialProvider: () async {
          credentialCalls++;
          return _creds();
        },
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.skippedFlagOff);
      expect(fake.requests, isEmpty);
      expect(credentialCalls, 0);
      expect(queue.pendingCount, 1);
    });

    test('flag 显式关闭 → 同样 skippedFlagOff', () async {
      final fake = _FakeTransport(_unexpectedTransport);
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final service = _service(
        fake: fake,
        queue: queue,
        flags: _FakeFlagSource(false),
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.skippedFlagOff);
      expect(queue.pendingCount, 2);
    });
  });

  group('CloudSyncService 成功路径', () {
    test('队列 2 条：登录一次 + 一次上报全 accepted（回带 event_id）→ 清空', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        if (request.url.endsWith('/v1/learning/events')) {
          return _acceptAll(request.body!);
        }
        throw StateError('unexpected ${request.url}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 2);
      expect(queue.pendingCount, 0);

      expect(fake.requests, hasLength(2));
      expect(fake.requests.first.url, 'http://sync.test/v1/auth/login');
      final eventsRequest = fake.requests.last;
      expect(eventsRequest.headers['Authorization'], 'Bearer at-1');
      final body = jsonDecode(eventsRequest.body!) as Map<String, dynamic>;
      expect((body['events'] as List<dynamic>), hasLength(2));
      expect(
        (body['events'] as List<dynamic>).first,
        containsPair('kind', 'knowledge_complete'),
      );
    });

    test('duplicated 回带 event_id 同样确认移除（幂等重放）', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        final ids = _eventIdsOf(request.body!);
        return _jsonResponse(200, jsonEncode(<String, dynamic>{'duplicated': ids}));
      });
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 2);
      expect(queue.pendingCount, 0);
    });

    test('205 条 → 两批上报（200+5）循环清空', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _acceptAll(request.body!);
      });
      final queue = _newQueue();
      await _enqueue(queue, 205);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 205);
      expect(queue.pendingCount, 0);

      final eventsRequests = fake.requests
          .where((r) => r.url.endsWith('/v1/learning/events'))
          .toList();
      expect(eventsRequests, hasLength(2));
      expect(_eventIdsOf(eventsRequests[0].body!), hasLength(200));
      expect(_eventIdsOf(eventsRequests[1].body!), hasLength(5));
    });

    test('部分确认：首批只确认 1 条 → 第二次请求只含剩余事件', () async {
      var round = 0;
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        round++;
        final ids = _eventIdsOf(request.body!);
        if (round == 1) {
          return _jsonResponse(200, jsonEncode(<String, dynamic>{
            'accepted': <String>[ids.first],
          }));
        }
        return _acceptAll(request.body!);
      });
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 2);
      expect(queue.pendingCount, 0);

      final eventsRequests = fake.requests
          .where((r) => r.url.endsWith('/v1/learning/events'))
          .toList();
      expect(eventsRequests, hasLength(2));
      expect(_eventIdsOf(eventsRequests[1].body!), hasLength(1));
    });

    test('队列已空：仍确保登录但不发 events 请求', () async {
      final fake = _FakeTransport((request) async => _loginOk());
      final service = _service(fake: fake, queue: _newQueue());

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 0);
      expect(fake.requests.single.url, 'http://sync.test/v1/auth/login');
    });
  });

  group('CloudSyncService 错误分类', () {
    test('登录阶段网络失败 → retryLater，队列保留、无 events 请求', () async {
      final fake = _FakeTransport((request) async {
        throw const SocketException('connection refused');
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.retryLater);
      expect(result.error, isA<PlatformNetworkException>());
      expect(queue.pendingCount, 1);
      expect(
        fake.requests.where((r) => r.url.endsWith('/v1/learning/events')),
        isEmpty,
      );
    });

    test('上报阶段网络失败 → retryLater，队列保留且 mutation_id 不变（幂等重试前提）', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        throw const SocketException('network down');
      });
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final before = await queue.nextBatch();
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.retryLater);
      expect(result.confirmedCount, 0);
      final after = await queue.nextBatch();
      expect(
        after.map((e) => e.mutationId).toList(),
        before.map((e) => e.mutationId).toList(),
      );
    });

    test('上报 500 retryable=true → retryLater，队列保留', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _jsonResponse(500, '{"code":"INTERNAL_ERROR","message":"暂不可用","retryable":true}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.retryLater);
      expect(queue.pendingCount, 1);
    });

    test('上报 400 retryable=false → failed，队列保留', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _jsonResponse(400, '{"code":"INVALID_REQUEST","message":"参数错误","retryable":false}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.failed);
      expect(result.error, isA<PlatformServerException>());
      expect(queue.pendingCount, 1);
    });

    test('上报 401 → loggedOut：清 token 缓存、通知会话过期、队列保留', () async {
      var expiredNotifications = 0;
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _jsonResponse(401, '{"code":"UNAUTHORIZED","message":"令牌过期","retryable":false}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(
        fake: fake,
        queue: queue,
        onSessionExpired: () => expiredNotifications++,
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.loggedOut);
      expect(expiredNotifications, 1);
      expect(service.cachedToken, isNull);
      expect(queue.pendingCount, 1);
    });

    test('登录 401（凭证错误）→ loggedOut 并通知，队列保留', () async {
      var expiredNotifications = 0;
      final fake = _FakeTransport((request) async {
        return _jsonResponse(401, '{"code":"UNAUTHORIZED","message":"用户名或密码错误","retryable":false}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(
        fake: fake,
        queue: queue,
        onSessionExpired: () => expiredNotifications++,
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.loggedOut);
      expect(expiredNotifications, 1);
      expect(queue.pendingCount, 1);
      expect(
        fake.requests.where((r) => r.url.endsWith('/v1/learning/events')),
        isEmpty,
      );
    });

    test('200 但未确认本批任何事件 → failed 停止（无死循环），队列原样保留', () async {
      var eventsCalls = 0;
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        eventsCalls++;
        return _jsonResponse(200, '{"accepted":[],"duplicated":[]}');
      });
      final queue = _newQueue();
      await _enqueue(queue, 3);
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.failed);
      expect(eventsCalls, 1);
      expect(queue.pendingCount, 3);
    });
  });

  group('CloudSyncService token 缓存与过期', () {
    test('有效期内第二轮同步复用缓存 token：不再登录，events 仍带 Bearer', () async {
      var now = DateTime.utc(2026, 10, 7, 8);
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _acceptAll(request.body!);
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(
        fake: fake,
        queue: queue,
        clock: () => now,
      );

      await service.syncOnce();
      await _enqueue(queue, 1);
      now = now.add(const Duration(minutes: 30));
      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(
        fake.requests.where((r) => r.url.endsWith('/v1/auth/login')).toList(),
        hasLength(1),
        reason: '有效期内不得重复登录',
      );
      final eventsRequests = fake.requests
          .where((r) => r.url.endsWith('/v1/learning/events'))
          .toList();
      expect(eventsRequests.last.headers['Authorization'], 'Bearer at-1');
    });

    test('临近过期（剩余 < 提前量 60s）→ 重新登录换取新 token', () async {
      var now = DateTime.utc(2026, 10, 7, 8);
      var logins = 0;
      var tokenSeq = 0;
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) {
          logins++;
          tokenSeq++;
          return _loginOk(accessToken: 'at-$tokenSeq');
        }
        return _acceptAll(request.body!);
      });
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(
        fake: fake,
        queue: queue,
        clock: () => now,
      );

      await service.syncOnce();
      // expires_in_s=3600、margin 60s：3541s 后视为过期
      now = now.add(const Duration(seconds: 3541));
      await _enqueue(queue, 1);
      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(logins, 2);
      final eventsRequests = fake.requests
          .where((r) => r.url.endsWith('/v1/learning/events'))
          .toList();
      expect(eventsRequests.last.headers['Authorization'], 'Bearer at-2');
    });

    test('无凭证（credentialProvider 返回 null）→ skippedNoCredentials，不发请求', () async {
      final fake = _FakeTransport(_unexpectedTransport);
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = _service(
        fake: fake,
        queue: queue,
        credentialProvider: () async => null,
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.skippedNoCredentials);
      expect(fake.requests, isEmpty);
      expect(queue.pendingCount, 1);
    });
  });
}

PlatformApiClient _client(_FakeTransport fake) =>
    PlatformApiClient(transport: fake, baseUrl: 'http://sync.test');

OfflineEventQueue _newQueue() =>
    OfflineEventQueue(store: InMemoryOfflineEventStore(), deviceId: 'dev-1');

Future<void> _enqueue(OfflineEventQueue queue, int count) async {
  for (var i = 0; i < count; i++) {
    await queue.enqueue(kind: LearningEventKind.knowledgeComplete, itemId: 'kn-$i');
  }
}

CloudSyncCredentials _creds() => const CloudSyncCredentials(
  username: 'zhang',
  password: 'pw',
  deviceId: 'dev-1',
);

CloudSyncService _service({
  required _FakeTransport fake,
  required OfflineEventQueue queue,
  _FakeFlagSource? flags,
  Future<CloudSyncCredentials?> Function()? credentialProvider,
  DateTime Function()? clock,
  void Function()? onSessionExpired,
}) {
  return CloudSyncService(
    client: _client(fake),
    queue: queue,
    credentialProvider: credentialProvider ?? (() async => _creds()),
    flagSource: flags ?? _FakeFlagSource(true),
    clock: clock,
    onSessionExpired: onSessionExpired,
  );
}

Future<PlatformHttpResponse> _unexpectedTransport(PlatformHttpRequest request) async {
  throw StateError('unexpected request ${request.url}');
}

PlatformHttpResponse _jsonResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: body);

PlatformHttpResponse _loginOk({String accessToken = 'at-1'}) => _jsonResponse(
  200,
  jsonEncode(<String, dynamic>{
    'access_token': accessToken,
    'refresh_token': 'rt-1',
    'expires_in_s': 3600,
    'user': <String, dynamic>{'user_id': 'u-1', 'display_name': '张三'},
  }),
);

/// 按请求 body 回 accepted 全量 event_id（模拟 platform M4-5 实装语义）。
PlatformHttpResponse _acceptAll(String body) {
  return _jsonResponse(
    200,
    jsonEncode(<String, dynamic>{'accepted': _eventIdsOf(body)}),
  );
}

List<String> _eventIdsOf(String? body) {
  final decoded = jsonDecode(body ?? '{}') as Map<String, dynamic>;
  return (decoded['events'] as List<dynamic>? ?? const <dynamic>[])
      .map((e) => (e as Map<String, dynamic>)['event_id'] as String)
      .toList();
}

/// Fake flag 源：固定开关值。
class _FakeFlagSource implements SyncFlagSource {
  _FakeFlagSource(this.enabled);

  final bool enabled;

  @override
  Future<bool> isCloudSyncEnabled() async => enabled;
}

/// Fake 传输层：记录请求，按注入的 handler 返回/抛出。
class _FakeTransport implements PlatformHttpTransport {
  _FakeTransport(Future<PlatformHttpResponse> Function(PlatformHttpRequest) handler)
    : _handler = handler;

  final Future<PlatformHttpResponse> Function(PlatformHttpRequest) _handler;
  final List<PlatformHttpRequest> requests = <PlatformHttpRequest>[];

  @override
  Future<PlatformHttpResponse> send(PlatformHttpRequest request) async {
    requests.add(request);
    return _handler(request);
  }
}
