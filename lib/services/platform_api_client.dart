import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'platform_api_models.dart';

/// 网络层失败（连接拒绝/DNS 解析失败/超时等本地错误）。
///
/// 队列/同步层可安全按“稍后重试”处理；超时类带 kind='timeout'。
class PlatformNetworkException implements Exception {
  const PlatformNetworkException(this.message, {this.kind = 'network'});

  final String message;

  /// 失败类别（network/timeout）。
  final String kind;

  @override
  String toString() => 'PlatformNetworkException($kind): $message';
}

/// 服务端返回错误（HTTP 非 2xx，或 2xx 但响应体不可解析）。
///
/// 错误统一携带 ErrorEnvelope：响应体可解析时透传，否则按状态码合成兜底信封。
class PlatformServerException implements Exception {
  const PlatformServerException({required this.statusCode, required this.envelope});

  final int statusCode;
  final ErrorEnvelope envelope;

  @override
  String toString() =>
      'PlatformServerException: HTTP $statusCode ${envelope.code} ${envelope.message}';
}

/// 平台 HTTP 请求（经传输层发出；body 为 JSON 字符串）。
class PlatformHttpRequest {
  const PlatformHttpRequest({
    required this.method,
    required this.url,
    this.headers = const <String, String>{},
    this.body,
  });

  final String method;
  final String url;
  final Map<String, String> headers;
  final String? body;
}

/// 平台 HTTP 响应。
class PlatformHttpResponse {
  const PlatformHttpResponse({required this.statusCode, required this.body});

  final int statusCode;
  final String body;
}

/// HTTP 传输抽象（生产 dart:io HttpClient；测试提供 Fake，不发真实网络请求）。
abstract class PlatformHttpTransport {
  Future<PlatformHttpResponse> send(PlatformHttpRequest request);
}

/// 生产实现：dart:io HttpClient（无新依赖，Content-Type 由本层补齐）。
class IoPlatformHttpTransport implements PlatformHttpTransport {
  IoPlatformHttpTransport({Duration? connectionTimeout})
    : _http = HttpClient()..connectionTimeout = connectionTimeout;

  final HttpClient _http;

  @override
  Future<PlatformHttpResponse> send(PlatformHttpRequest request) async {
    final httpRequest = await _http.openUrl(request.method, Uri.parse(request.url));
    httpRequest.followRedirects = false;
    for (final header in request.headers.entries) {
      httpRequest.headers.set(header.key, header.value);
    }
    if (request.body != null) {
      httpRequest.headers.contentType = ContentType.json;
      httpRequest.write(request.body);
    }
    final response = await httpRequest.close();
    final body = await response.transform(utf8.decoder).join();
    return PlatformHttpResponse(statusCode: response.statusCode, body: body);
  }

  /// 释放底层连接（应用退出时调用）。
  void dispose() {
    _http.close(force: true);
  }
}

/// 平台 HTTP API 客户端（contracts/platform_api/openapi.yaml 对齐）。
///
/// 三端点：POST /v1/auth/login、POST /v1/learning/events、GET /v1/learning/state。
/// Bearer 令牌经 [accessToken] 注入；超时语义 login/state 10s、events 15s。
/// 错误统一映射：网络层异常 → [PlatformNetworkException]；
/// 非 2xx 或响应体不可解析 → [PlatformServerException]（携带 ErrorEnvelope）。
class PlatformApiClient {
  PlatformApiClient({
    PlatformHttpTransport? transport,
    String baseUrl = defaultBaseUrl,
    Duration? loginTimeout,
    Duration? eventsTimeout,
    Duration? stateTimeout,
  }) : _transport = transport ?? IoPlatformHttpTransport(),
       _baseUrl = baseUrl.endsWith('/')
           ? baseUrl.substring(0, baseUrl.length - 1)
           : baseUrl,
       _loginTimeout = loginTimeout ?? const Duration(seconds: 10),
       _eventsTimeout = eventsTimeout ?? const Duration(seconds: 15),
       _stateTimeout = stateTimeout ?? const Duration(seconds: 10);

  /// dev 默认地址（契约 servers 第一项）。
  static const String defaultBaseUrl = 'http://localhost:8000';

  final PlatformHttpTransport _transport;
  final String _baseUrl;
  final Duration _loginTimeout;
  final Duration _eventsTimeout;
  final Duration _stateTimeout;

  /// 当前 Bearer 令牌（login 成功后由调用方赋值；空则不携带 Authorization 头）。
  String? accessToken;

  /// 登录换取会话令牌（不携带 Authorization）。
  Future<AuthToken> login({
    required String username,
    required String password,
    String? deviceId,
  }) async {
    final response = await _send(
      method: 'POST',
      path: '/v1/auth/login',
      body: jsonEncode(<String, dynamic>{
        'username': username,
        'password': password,
        if (deviceId != null && deviceId.isNotEmpty) 'device_id': deviceId,
      }),
      timeout: _loginTimeout,
      authenticated: false,
    );
    return AuthToken.fromJson(_decodeObjectOrThrow(response.statusCode, response.body));
  }

  /// 批量上报学习事件（1-200 条，服务端按 mutation_id 幂等去重；
  /// 响应 accepted/duplicated 回带 event_id）。
  Future<EventUploadResult> uploadLearningEvents(List<LearningEvent> events) async {
    final response = await _send(
      method: 'POST',
      path: '/v1/learning/events',
      body: jsonEncode(<String, dynamic>{
        'events': events.map((LearningEvent event) => event.toJson()).toList(),
      }),
      timeout: _eventsTimeout,
      authenticated: true,
    );
    return EventUploadResult.fromJson(
      _decodeObjectOrThrow(response.statusCode, response.body),
    );
  }

  /// 拉取服务端合成的学习状态（权威）。
  Future<LearningState> fetchLearningState() async {
    final response = await _send(
      method: 'GET',
      path: '/v1/learning/state',
      timeout: _stateTimeout,
      authenticated: true,
    );
    return LearningState.fromJson(
      _decodeObjectOrThrow(response.statusCode, response.body),
    );
  }

  Future<PlatformHttpResponse> _send({
    required String method,
    required String path,
    required Duration timeout,
    required bool authenticated,
    String? body,
  }) async {
    final token = accessToken;
    final request = PlatformHttpRequest(
      method: method,
      url: '$_baseUrl$path',
      headers: <String, String>{
        if (authenticated && token != null && token.isNotEmpty)
          'Authorization': 'Bearer $token',
      },
      body: body,
    );

    final PlatformHttpResponse response;
    try {
      response = await _transport.send(request).timeout(timeout);
    } on TimeoutException {
      throw PlatformNetworkException(
        'request timeout: $method $path',
        kind: 'timeout',
      );
    } on Exception catch (error) {
      throw PlatformNetworkException('$method $path failed: $error');
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw PlatformServerException(
        statusCode: response.statusCode,
        envelope: _envelopeFromResponse(response),
      );
    }
    return response;
  }

  /// 解析响应体为 JSON 对象；不可解析时合成 INVALID_RESPONSE 信封抛出。
  Map<String, dynamic> _decodeObjectOrThrow(int statusCode, String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map<String, dynamic>) {
        return decoded;
      }
    } on FormatException {
      // 落入下方合成信封分支。
    }
    throw PlatformServerException(
      statusCode: statusCode,
      envelope: ErrorEnvelope(
        code: 'INVALID_RESPONSE',
        message: '响应体不是合法的 JSON 对象: ${_truncate(body)}',
        details: <String, dynamic>{'status_code': statusCode},
      ),
    );
  }

  /// 非 2xx 响应转 ErrorEnvelope：body 可解析且含字符串 code 时透传，
  /// 否则按状态码合成兜底信封（5xx 视为可重试）。
  ErrorEnvelope _envelopeFromResponse(PlatformHttpResponse response) {
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map<String, dynamic> && decoded['code'] is String) {
        return ErrorEnvelope.fromJson(decoded);
      }
    } on FormatException {
      // 落入下方合成信封分支。
    }
    return ErrorEnvelope(
      code: 'HTTP_ERROR',
      message: 'HTTP ${response.statusCode}: ${_truncate(response.body)}',
      retryable: response.statusCode >= 500,
      details: <String, dynamic>{'status_code': response.statusCode},
    );
  }

  static String _truncate(String text) =>
      text.length <= 256 ? text : '${text.substring(0, 256)}…';
}
