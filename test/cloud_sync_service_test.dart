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
    test('默认 DisabledSyncFlagSource 全关：不上报、队列不动（N04：会话先于 flag）', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        throw StateError('unexpected ${request.url}');
      });
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

      // N04：先确保会话再查 flag——登录在 flag 判定之前，不再以"零请求"
      // 作为关闭语义，关闭只保证不上报、队列不动。
      expect(result.outcome, CloudSyncOutcome.skippedFlagOff);
      expect(credentialCalls, 1, reason: 'N04：凭证获取先于 flag 查询');
      expect(
        fake.requests.where((r) => r.url.endsWith('/v1/learning/events')),
        isEmpty,
      );
      expect(queue.pendingCount, 1);
    });

    test('flag 显式关闭 → 同样 skippedFlagOff', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        throw StateError('unexpected ${request.url}');
      });
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

    test('N04：flag 查询网络失败 → retryLater（不伪装成开关关闭）', () async {
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = CloudSyncService(
        client: _client(_FakeTransport((request) async => _loginOk())),
        queue: queue,
        credentialProvider: () async => _creds(),
        flagSource: _ThrowingFlagSource(
          // 模拟 ApiSyncFlagSource 契约：传输层网络错误包装为
          // PlatformNetworkException 上抛（不吞）。
          const PlatformNetworkException('flags endpoint unreachable'),
        ),
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.retryLater);
      expect(result.error, isA<PlatformNetworkException>());
      expect(queue.pendingCount, 1);
    });

    test('N04：flag 查询 401 → loggedOut 并通知会话过期（过期 token 自愈入口）', () async {
      var expiredNotifications = 0;
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = CloudSyncService(
        client: _client(_FakeTransport((request) async => _loginOk())),
        queue: queue,
        credentialProvider: () async => _creds(),
        flagSource: _ThrowingFlagSource(
          PlatformServerException(
            statusCode: 401,
            envelope: ErrorEnvelope(
              code: 'UNAUTHORIZED',
              message: '令牌过期',
              retryable: false,
            ),
          ),
        ),
        onSessionExpired: () => expiredNotifications++,
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.loggedOut);
      expect(expiredNotifications, 1);
      expect(service.cachedToken, isNull);
      expect(queue.pendingCount, 1);
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

    test('completeBatch 落盘失败：outcome 仍 synced（上报本身成功），persistError 如实透传（P1）', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _acceptAll(request.body!);
      });
      final store = _FailingEntriesStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      await queue.enqueue(kind: LearningEventKind.knowledgeComplete, itemId: 'kn-1');
      final service = _service(fake: fake, queue: queue);

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced, reason: '服务端已确认，上报成功');
      expect(result.confirmedCount, 1);
      expect(result.persistError, isNotNull, reason: '本地落盘失败向上层返回');
      expect(result.persistError!.queueError, isNotNull);
      expect(result.persistError!.seqError, isNull, reason: '水位写入独立成功');
      expect(queue.pendingCount, 0, reason: '内存已清理');
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

  group('CloudSyncService 登录后 flag 复查（两段式）', () {
    test('无 token 初查放行 → 登录 → 复查 OFF → skippedFlagOff，不发 events', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        throw StateError('unexpected ${request.url}');
      });
      final client = _client(fake);
      final queue = _newQueue();
      await _enqueue(queue, 2);
      final service = CloudSyncService(
        client: client,
        queue: queue,
        credentialProvider: () async => _creds(),
        // 两段式语义：无 token（登录前）放行 true；有 token（登录后复查）OFF。
        flagSource: _TokenAwareFlagSource(
          client: client,
          unauthenticated: true,
          authenticated: false,
        ),
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.skippedFlagOff);
      expect(fake.requests.single.url, 'http://sync.test/v1/auth/login');
      expect(
        fake.requests.where((r) => r.url.endsWith('/v1/learning/events')),
        isEmpty,
        reason: '复查 OFF 后不得发任何上报请求',
      );
      expect(queue.pendingCount, 2, reason: '队列保留');
    });

    test('两段均放行 → 正常上报（回归：复查不影响成功路径）', () async {
      final fake = _FakeTransport((request) async {
        if (request.url.endsWith('/v1/auth/login')) return _loginOk();
        return _acceptAll(request.body!);
      });
      final client = _client(fake);
      final queue = _newQueue();
      await _enqueue(queue, 1);
      final service = CloudSyncService(
        client: client,
        queue: queue,
        credentialProvider: () async => _creds(),
        flagSource: _TokenAwareFlagSource(
          client: client,
          unauthenticated: true,
          authenticated: true,
        ),
      );

      final result = await service.syncOnce();

      expect(result.outcome, CloudSyncOutcome.synced);
      expect(result.confirmedCount, 1);
      expect(queue.pendingCount, 0);
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

/// 抛异常的 Fake flag 源（N04：实现不吞异常，由 syncOnce 统一分类）。
class _ThrowingFlagSource implements SyncFlagSource {
  _ThrowingFlagSource(this.error);

  final Object error;

  @override
  Future<bool> isCloudSyncEnabled() async => throw error;
}

/// 按 token 有无区分判定的 Fake（模拟 ApiSyncFlagSource 两段式语义）。
class _TokenAwareFlagSource implements SyncFlagSource {
  _TokenAwareFlagSource({
    required this.client,
    required this.unauthenticated,
    required this.authenticated,
  });

  final PlatformApiClient client;
  final bool unauthenticated;
  final bool authenticated;

  @override
  Future<bool> isCloudSyncEnabled() async {
    final token = client.accessToken;
    return token == null || token.isEmpty ? unauthenticated : authenticated;
  }
}

/// 队列行持久化恒失败的存储（P1 落盘失败透传验收；水位写入正常）。
class _FailingEntriesStore implements OfflineEventStore {
  final List<String> _entries = <String>[];
  int _seqWatermark = 0;

  @override
  Future<List<String>> loadJsonEntries() async => List<String>.from(_entries);

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    throw Exception('injected: disk full');
  }

  @override
  Future<int> loadSeqWatermark() async => _seqWatermark;

  @override
  Future<void> saveSeqWatermark(int seq) async {
    _seqWatermark = seq;
  }
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
