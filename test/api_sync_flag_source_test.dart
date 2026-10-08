import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/api_sync_flag_source.dart';
import 'package:bfs_learn/services/platform_api_client.dart';

/// ApiSyncFlagSource 两段式判定测试（Fake 传输层）。
void main() {
  test('无 token：放行 true，不发任何请求', () async {
    final fake = _FakeTransport((request) async {
      throw StateError('unexpected ${request.url}');
    });
    final client = PlatformApiClient(transport: fake, baseUrl: 'http://flags.test');
    final source = ApiSyncFlagSource(client: client);

    expect(await source.isCloudSyncEnabled(), isTrue);
    expect(fake.requests, isEmpty);
  });

  test('空 token 同样放行；有 token 时 GET /v1/feature-flags 权威判定', () async {
    final fake = _FakeTransport(
      (request) async => _jsonResponse(200, '{"flags":{"cloud_sync":true}}'),
    );
    final client = PlatformApiClient(transport: fake, baseUrl: 'http://flags.test')
      ..accessToken = '';
    final source = ApiSyncFlagSource(client: client);

    expect(await source.isCloudSyncEnabled(), isTrue, reason: '空 token 视为未登录');
    expect(fake.requests, isEmpty);

    client.accessToken = 'at-1';
    expect(await source.isCloudSyncEnabled(), isTrue);
    final request = fake.requests.single;
    expect(request.url, 'http://flags.test/v1/feature-flags');
    expect(request.headers['Authorization'], 'Bearer at-1');
  });

  test('有 token 且 cloud_sync=false → false', () async {
    final fake = _FakeTransport(
      (request) async => _jsonResponse(200, '{"flags":{"cloud_sync":false,"ai":true}}'),
    );
    final client = PlatformApiClient(transport: fake)..accessToken = 'at-1';

    expect(await ApiSyncFlagSource(client: client).isCloudSyncEnabled(), isFalse);
  });

  test('N04：401（token 失效）→ 异常上抛（由 syncOnce 分类 loggedOut），且不清客户端 token', () async {
    final fake = _FakeTransport(
      (request) async => _jsonResponse(
        401,
        '{"code":"UNAUTHORIZED","message":"令牌无效","retryable":false}',
      ),
    );
    final client = PlatformApiClient(transport: fake)..accessToken = 'stale';
    final source = ApiSyncFlagSource(client: client);

    // N04：开关源不吞 401——伪装成 false 会让 syncOnce 永远
    // skippedFlagOff，到不了会话失效/重登路径。
    await expectLater(
      source.isCloudSyncEnabled(),
      throwsA(
        isA<PlatformServerException>()
            .having((e) => e.statusCode, 'statusCode', 401),
      ),
    );
    expect(client.accessToken, 'stale', reason: 'token 生命周期归 CloudSyncService 管');
  });

  test('N04：网络失败 / 5xx → 异常上抛（由 syncOnce 分类 retryLater/failed）', () async {
    final down = _FakeTransport((request) async {
      throw const SocketException('network down');
    });
    final clientDown = PlatformApiClient(transport: down)..accessToken = 'at-1';
    await expectLater(
      ApiSyncFlagSource(client: clientDown).isCloudSyncEnabled(),
      throwsA(isA<PlatformNetworkException>()),
      reason: '网络失败不再伪装成开关关闭',
    );

    final broken = _FakeTransport(
      (request) async => _jsonResponse(500, '{"code":"INTERNAL_ERROR","retryable":true}'),
    );
    final clientBroken = PlatformApiClient(transport: broken)..accessToken = 'at-1';
    await expectLater(
      ApiSyncFlagSource(client: clientBroken).isCloudSyncEnabled(),
      throwsA(isA<PlatformServerException>()),
      reason: '服务端错误如实上抛',
    );
  });
}

PlatformHttpResponse _jsonResponse(int status, String body) =>
    PlatformHttpResponse(statusCode: status, body: jsonEncode(jsonDecode(body)));

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
