import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/platform_api_client.dart';
import 'package:bfs_learn/services/platform_api_models.dart';

/// 平台 HTTP API 客户端测试（Fake 传输层，不发真实网络请求）。
void main() {
  group('PlatformApiClient.login', () {
    test('成功：POST /v1/auth/login，body 契约字段，无 device_id 时省略，不带 Authorization', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '''
        {"access_token":"at-1","refresh_token":"rt-1","expires_in_s":3600,
         "user":{"user_id":"u-1","display_name":"张三","role":"student","tenant_id":"t-1"}}
      '''));
      final client = PlatformApiClient(transport: fake, baseUrl: 'http://api.test');

      final token = await client.login(username: 'zhang', password: 'pw');

      expect(fake.requests, hasLength(1));
      final request = fake.requests.single;
      expect(request.method, 'POST');
      expect(request.url, 'http://api.test/v1/auth/login');
      expect(request.headers.containsKey('Authorization'), isFalse);
      final body = jsonDecode(request.body!) as Map<String, dynamic>;
      expect(body, <String, dynamic>{'username': 'zhang', 'password': 'pw'});

      expect(token.accessToken, 'at-1');
      expect(token.refreshToken, 'rt-1');
      expect(token.expiresInS, 3600);
      expect(token.user.userId, 'u-1');
      expect(token.user.role, 'student');
    });

    test('携带 device_id 时写入 body', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '{"access_token":"at"}'));
      final client = PlatformApiClient(transport: fake);

      await client.login(username: 'u', password: 'p', deviceId: 'dev-1');

      final body = jsonDecode(fake.requests.single.body!) as Map<String, dynamic>;
      expect(body, containsPair('device_id', 'dev-1'));
    });

    test('401 错误信封透传为 PlatformServerException', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(401, '''
        {"schema_version":"1.0","code":"UNAUTHORIZED","message":"用户名或密码错误",
         "retryable":false,"trace_id":"t-9","request_id":"r-9","details":{"field":"password"}}
      '''));
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.login(username: 'u', password: 'bad'),
        throwsA(
          isA<PlatformServerException>()
              .having((e) => e.statusCode, 'statusCode', 401)
              .having((e) => e.envelope.code, 'code', 'UNAUTHORIZED')
              .having((e) => e.envelope.message, 'message', '用户名或密码错误')
              .having((e) => e.envelope.retryable, 'retryable', isFalse)
              .having((e) => e.envelope.traceId, 'traceId', 't-9')
              .having((e) => e.envelope.requestId, 'requestId', 'r-9')
              .having((e) => e.envelope.details, 'details',
                  containsPair('field', 'password')),
        ),
      );
    });
  });

  group('PlatformApiClient.uploadLearningEvents', () {
    test('成功：body 为 {events:[契约线名事件]}，解析 accepted/duplicated', () async {
      final fake = _FakeTransport(
        (request) async => _jsonResponse(200, '{"accepted":["m-1"],"duplicated":["m-2"]}'),
      );
      final client = PlatformApiClient(transport: fake);

      final result = await client.uploadLearningEvents(const <LearningEvent>[
        LearningEvent(
          eventId: 'e-1',
          mutationId: 'm-1',
          kind: LearningEventKind.knowledgeComplete,
          itemId: 'kn-1',
          occurredAt: '2026-10-07T08:00:00Z',
          payload: <String, dynamic>{'layer': 1},
        ),
        LearningEvent(
          eventId: 'e-2',
          mutationId: 'm-2',
          kind: LearningEventKind.quizSubmit,
          itemId: 'q-1',
        ),
      ]);

      final request = fake.requests.single;
      expect(request.method, 'POST');
      expect(request.url, 'http://localhost:8000/v1/learning/events');
      final body = jsonDecode(request.body!) as Map<String, dynamic>;
      final events = body['events'] as List<dynamic>;
      expect(events, hasLength(2));
      expect(events.first, <String, dynamic>{
        'event_id': 'e-1',
        'mutation_id': 'm-1',
        'kind': 'knowledge_complete',
        'item_id': 'kn-1',
        'occurred_at': '2026-10-07T08:00:00Z',
        'payload': <String, dynamic>{'layer': 1},
      });

      expect(result.accepted, <String>['m-1']);
      expect(result.duplicated, <String>['m-2']);
    });

    test('Bearer 令牌注入 Authorization 头', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '{"accepted":[]}'));
      final client = PlatformApiClient(transport: fake)
        ..accessToken = 'at-secret';

      await client.uploadLearningEvents(const <LearningEvent>[
        LearningEvent(
          eventId: 'e',
          mutationId: 'm',
          kind: LearningEventKind.importEvent,
          itemId: 'i',
        ),
      ]);

      expect(fake.requests.single.headers['Authorization'], 'Bearer at-secret');
    });

    test('未登录（token 为 null/空串）时不携带 Authorization', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '{"accepted":[]}'));
      final client = PlatformApiClient(transport: fake)..accessToken = '';

      await client.uploadLearningEvents(const <LearningEvent>[
        LearningEvent(
          eventId: 'e',
          mutationId: 'm',
          kind: LearningEventKind.importEvent,
          itemId: 'i',
        ),
      ]);

      expect(fake.requests.single.headers.containsKey('Authorization'), isFalse);
    });

    test('500 + 合法错误信封 → 透传信封（retryable=true）', () async {
      final fake = _FakeTransport(
        (request) async => _jsonResponse(500, '''
          {"schema_version":"1.0","code":"INTERNAL_ERROR","message":"服务暂不可用","retryable":true}
        '''),
      );
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.uploadLearningEvents(const <LearningEvent>[]),
        throwsA(
          isA<PlatformServerException>()
              .having((e) => e.statusCode, 'statusCode', 500)
              .having((e) => e.envelope.code, 'code', 'INTERNAL_ERROR')
              .having((e) => e.envelope.retryable, 'retryable', isTrue),
        ),
      );
    });

    test('503 + 非 JSON body → 合成 HTTP_ERROR 信封（5xx 可重试）', () async {
      final fake = _FakeTransport((request) async => _plainResponse(503, 'oops'));
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.uploadLearningEvents(const <LearningEvent>[]),
        throwsA(
          isA<PlatformServerException>()
              .having((e) => e.statusCode, 'statusCode', 503)
              .having((e) => e.envelope.code, 'code', 'HTTP_ERROR')
              .having((e) => e.envelope.retryable, 'retryable', isTrue)
              .having((e) => e.envelope.message, 'message', contains('oops')),
        ),
      );
    });

    test('400 + 非 JSON body → 合成信封 4xx 不可重试', () async {
      final fake = _FakeTransport((request) async => _plainResponse(400, 'bad request'));
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.uploadLearningEvents(const <LearningEvent>[]),
        throwsA(
          isA<PlatformServerException>().having(
            (e) => e.envelope.retryable,
            'retryable',
            isFalse,
          ),
        ),
      );
    });
  });

  group('PlatformApiClient.fetchLearningState', () {
    test('成功：GET /v1/learning/state + Bearer，解析 LearningState', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '''
        {"version":7,"completed_item_ids":["kn-1","kn-2"],"counters":{"quiz_submit":12}}
      '''));
      final client = PlatformApiClient(transport: fake)..accessToken = 'at-1';

      final state = await client.fetchLearningState();

      final request = fake.requests.single;
      expect(request.method, 'GET');
      expect(request.url, 'http://localhost:8000/v1/learning/state');
      expect(request.headers['Authorization'], 'Bearer at-1');
      expect(request.body, isNull);

      expect(state.version, 7);
      expect(state.completedItemIds, <String>['kn-1', 'kn-2']);
      expect(state.counters, <String, dynamic>{'quiz_submit': 12});
    });

    test('404 + 合法信封 → 信封优先于状态码合成', () async {
      final fake = _FakeTransport(
        (request) async => _jsonResponse(404, '''
          {"code":"NOT_FOUND","message":"状态不存在","retryable":false}
        '''),
      );
      final client = PlatformApiClient(transport: fake)..accessToken = 'at-1';

      await expectLater(
        client.fetchLearningState(),
        throwsA(
          isA<PlatformServerException>()
              .having((e) => e.statusCode, 'statusCode', 404)
              .having((e) => e.envelope.code, 'code', 'NOT_FOUND')
              .having((e) => e.envelope.retryable, 'retryable', isFalse),
        ),
      );
    });
  });

  group('PlatformApiClient.fetchFeatureFlags', () {
    test('成功：GET /v1/feature-flags + Bearer，解析 flags 布尔映射', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(
        200,
        '{"flags":{"cloud_sync":true,"ai":false,"telemetry":true}}',
      ));
      final client = PlatformApiClient(transport: fake)..accessToken = 'at-1';

      final flags = await client.fetchFeatureFlags();

      final request = fake.requests.single;
      expect(request.method, 'GET');
      expect(request.url, 'http://localhost:8000/v1/feature-flags');
      expect(request.headers['Authorization'], 'Bearer at-1');
      expect(flags, <String, bool>{'cloud_sync': true, 'ai': false, 'telemetry': true});
    });

    test('非布尔值容错为 false；缺失 flags 对象 → 空映射', () async {
      final fake = _FakeTransport(
        (request) async => _jsonResponse(200, '{"flags":{"cloud_sync":"yes","ai":1}}'),
      );
      final client = PlatformApiClient(transport: fake)..accessToken = 'at-1';
      expect(await client.fetchFeatureFlags(), <String, bool>{'cloud_sync': false, 'ai': false});

      final fakeNoFlags = _FakeTransport((request) async => _jsonResponse(200, '{"other":1}'));
      final clientNoFlags = PlatformApiClient(transport: fakeNoFlags)..accessToken = 'at-1';
      expect(await clientNoFlags.fetchFeatureFlags(), isEmpty);
    });

    test('401 → PlatformServerException（信封透传）', () async {
      final fake = _FakeTransport(
        (request) async => _jsonResponse(
          401,
          '{"code":"UNAUTHORIZED","message":"令牌无效","retryable":false}',
        ),
      );
      final client = PlatformApiClient(transport: fake)..accessToken = 'stale';

      await expectLater(
        client.fetchFeatureFlags(),
        throwsA(
          isA<PlatformServerException>().having((e) => e.statusCode, 'statusCode', 401),
        ),
      );
    });
  });

  group('PlatformApiClient 异常映射', () {
    test('网络异常（SocketException）→ PlatformNetworkException', () async {
      final fake = _FakeTransport((request) async {
        throw const SocketException('connection refused');
      });
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.fetchLearningState(),
        throwsA(
          isA<PlatformNetworkException>()
              .having((e) => e.kind, 'kind', 'network')
              .having((e) => e.message, 'message', contains('connection refused')),
        ),
      );
    });

    test('超时 → PlatformNetworkException(kind=timeout)，超时长度可注入', () async {
      final client = PlatformApiClient(
        transport: _NeverTransport(),
        stateTimeout: const Duration(milliseconds: 30),
      );

      await expectLater(
        client.fetchLearningState(),
        throwsA(
          isA<PlatformNetworkException>().having((e) => e.kind, 'kind', 'timeout'),
        ),
      );
    });

    test('200 + 非 JSON 响应体 → 合成 INVALID_RESPONSE 信封', () async {
      final fake = _FakeTransport((request) async => _plainResponse(200, '<html>gateway</html>'));
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.fetchLearningState(),
        throwsA(
          isA<PlatformServerException>()
              .having((e) => e.statusCode, 'statusCode', 200)
              .having((e) => e.envelope.code, 'code', 'INVALID_RESPONSE'),
        ),
      );
    });

    test('200 + JSON 非对象（数组）→ 同样合成 INVALID_RESPONSE', () async {
      final fake = _FakeTransport((request) async => _jsonResponse(200, '[1,2]'));
      final client = PlatformApiClient(transport: fake);

      await expectLater(
        client.login(username: 'u', password: 'p'),
        throwsA(
          isA<PlatformServerException>().having(
            (e) => e.envelope.code,
            'code',
            'INVALID_RESPONSE',
          ),
        ),
      );
    });
  });

  test('baseUrl 尾斜杠归一化，不产生双斜杠 URL', () async {
    final fake = _FakeTransport((request) async => _jsonResponse(200, '{"status":"ok"}'));
    final client = PlatformApiClient(transport: fake, baseUrl: 'http://api.test/');

    await client.login(username: 'u', password: 'p');

    expect(fake.requests.single.url, 'http://api.test/v1/auth/login');
  });
}

PlatformHttpResponse _jsonResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: body);

/// 模拟非 JSON 响应体（如网关 HTML 错误页）。
PlatformHttpResponse _plainResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: body);

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

/// 永不返回的传输层（超时测试）。
class _NeverTransport implements PlatformHttpTransport {
  @override
  Future<PlatformHttpResponse> send(PlatformHttpRequest request) =>
      Completer<PlatformHttpResponse>().future;
}
