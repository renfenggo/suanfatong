/// 平台 HTTP API 契约模型（contracts/platform_api/openapi.yaml 对齐）。
///
/// 线格式：字段 snake_case；所有错误统一 ErrorEnvelope（schema_version "1.0"）。
/// 容错策略沿用 runner_models.dart：未知字段忽略、缺失字段取默认值、
/// 未知枚举线名不抛异常（枚举只增不改）。
library;

/// 学习事件类型（契约 LearningEvent.kind 枚举）。
enum LearningEventKind {
  knowledgeComplete('knowledge_complete'),
  quizSubmit('quiz_submit'),
  animationWatch('animation_watch'),
  importEvent('import');

  const LearningEventKind(this.wireName);

  /// 契约线名。
  final String wireName;

  /// 解析契约线名；未知值返回 null（兼容性：枚举只增不改）。
  static LearningEventKind? fromWireName(String? wireName) {
    switch (wireName) {
      case 'knowledge_complete':
        return LearningEventKind.knowledgeComplete;
      case 'quiz_submit':
        return LearningEventKind.quizSubmit;
      case 'animation_watch':
        return LearningEventKind.animationWatch;
      case 'import':
        return LearningEventKind.importEvent;
      default:
        return null;
    }
  }
}

/// 用户简要信息（契约 UserBrief）。
class UserBrief {
  const UserBrief({
    this.userId = '',
    this.displayName = '',
    this.role = '',
    this.tenantId = '',
  });

  final String userId;
  final String displayName;
  final String role;
  final String tenantId;

  /// 解析契约 JSON（snake_case）。
  factory UserBrief.fromJson(Map<String, dynamic> json) {
    return UserBrief(
      userId: json['user_id'] as String? ?? '',
      displayName: json['display_name'] as String? ?? '',
      role: json['role'] as String? ?? '',
      tenantId: json['tenant_id'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'user_id': userId,
    'display_name': displayName,
    'role': role,
    'tenant_id': tenantId,
  };
}

/// 登录会话令牌（契约 AuthToken，POST /v1/auth/login 200 响应）。
class AuthToken {
  const AuthToken({
    this.accessToken = '',
    this.refreshToken = '',
    this.expiresInS = 0,
    this.user = const UserBrief(),
  });

  final String accessToken;
  final String refreshToken;

  /// 有效期（秒）。
  final int expiresInS;
  final UserBrief user;

  /// 解析契约 JSON（snake_case；user 非对象时容错为空 UserBrief）。
  factory AuthToken.fromJson(Map<String, dynamic> json) {
    return AuthToken(
      accessToken: json['access_token'] as String? ?? '',
      refreshToken: json['refresh_token'] as String? ?? '',
      expiresInS: json['expires_in_s'] as int? ?? 0,
      user: json['user'] is Map<String, dynamic>
          ? UserBrief.fromJson(json['user'] as Map<String, dynamic>)
          : const UserBrief(),
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'access_token': accessToken,
    'refresh_token': refreshToken,
    'expires_in_s': expiresInS,
    'user': user.toJson(),
  };
}

/// 学习事实事件（契约 LearningEvent，append-only，mutation_id 幂等键）。
class LearningEvent {
  const LearningEvent({
    required this.eventId,
    required this.mutationId,
    required this.kind,
    required this.itemId,
    this.occurredAt = '',
    this.payload = const <String, dynamic>{},
  });

  final String eventId;

  /// 幂等键（重试间不变；服务端按此去重）。
  final String mutationId;
  final LearningEventKind kind;
  final String itemId;

  /// 发生时间（契约 date-time；线格式原样透传，不做时区换算）。
  final String occurredAt;

  /// 事件附加数据（契约 additionalProperties: true）。
  final Map<String, dynamic> payload;

  /// 解析契约 JSON（snake_case）。
  factory LearningEvent.fromJson(Map<String, dynamic> json) {
    return LearningEvent(
      eventId: json['event_id'] as String? ?? '',
      mutationId: json['mutation_id'] as String? ?? '',
      // 未知线名容错为 import（fromJson 仅用于本地持久化回读，
      // 客户端生成事件时恒为已知线名，该分支理论不可达）。
      kind:
          LearningEventKind.fromWireName(json['kind'] as String?) ??
          LearningEventKind.importEvent,
      itemId: json['item_id'] as String? ?? '',
      occurredAt: json['occurred_at'] as String? ?? '',
      payload: _asObject(json['payload']),
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'event_id': eventId,
    'mutation_id': mutationId,
    'kind': kind.wireName,
    'item_id': itemId,
    'occurred_at': occurredAt,
    'payload': payload,
  };
}

/// 服务端合成的学习状态（契约 LearningState，GET /v1/learning/state）。
class LearningState {
  const LearningState({
    this.version = 0,
    this.completedItemIds = const <String>[],
    this.counters = const <String, dynamic>{},
  });

  /// optimistic lock 版本（配置类字段用）。
  final int version;
  final List<String> completedItemIds;
  final Map<String, dynamic> counters;

  /// 解析契约 JSON（snake_case；数组/对象字段容错并过滤非字符串项）。
  factory LearningState.fromJson(Map<String, dynamic> json) {
    return LearningState(
      version: json['version'] as int? ?? 0,
      completedItemIds:
          (json['completed_item_ids'] as List<dynamic>? ?? const <dynamic>[])
              .whereType<String>()
              .toList(),
      counters: _asObject(json['counters']),
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'version': version,
    'completed_item_ids': completedItemIds,
    'counters': counters,
  };
}

/// 统一错误信封（契约 ErrorEnvelope，schema_version 恒 "1.0"）。
class ErrorEnvelope {
  const ErrorEnvelope({
    required this.code,
    required this.message,
    this.retryable = false,
    this.schemaVersion = '1.0',
    this.traceId,
    this.requestId,
    this.details = const <String, dynamic>{},
  });

  final String schemaVersion;

  /// 错误码（契约 pattern ^[A-Z][A-Z0-9_]{2,63}$）。
  final String code;
  final String message;
  final bool retryable;
  final String? traceId;
  final String? requestId;
  final Map<String, dynamic> details;

  /// 解析契约 JSON（必填 code/message/retryable 缺失时取容错默认）。
  factory ErrorEnvelope.fromJson(Map<String, dynamic> json) {
    return ErrorEnvelope(
      schemaVersion: json['schema_version'] as String? ?? '1.0',
      code: json['code'] as String? ?? 'UNKNOWN',
      message: json['message'] as String? ?? '',
      retryable: json['retryable'] as bool? ?? false,
      traceId: json['trace_id'] as String?,
      requestId: json['request_id'] as String?,
      details: _asObject(json['details']),
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'schema_version': schemaVersion,
    'code': code,
    'message': message,
    'retryable': retryable,
    if (traceId != null) 'trace_id': traceId,
    if (requestId != null) 'request_id': requestId,
    'details': details,
  };
}

/// 批量上报结果（POST /v1/learning/events 200 响应）。
///
/// accepted/duplicated 回带的是 **event_id**（M4-5 实装语义，2026-10-07
/// 契约澄清）：accepted=上报成功的 event_id；duplicated=服务端按
/// mutation_id 幂等去重命中的 event_id（此前已接收，同样视为已确认）。
class EventUploadResult {
  const EventUploadResult({
    this.accepted = const <String>[],
    this.duplicated = const <String>[],
  });

  final List<String> accepted;
  final List<String> duplicated;

  factory EventUploadResult.fromJson(Map<String, dynamic> json) {
    return EventUploadResult(
      accepted:
          (json['accepted'] as List<dynamic>? ?? const <dynamic>[])
              .whereType<String>()
              .toList(),
      duplicated:
          (json['duplicated'] as List<dynamic>? ?? const <dynamic>[])
              .whereType<String>()
              .toList(),
    );
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'accepted': accepted,
    'duplicated': duplicated,
  };

  /// accepted 与 duplicated 的 event_id 并集（均为服务端已确认）。
  Set<String> get confirmedEventIds => <String>{...accepted, ...duplicated};
}

Map<String, dynamic> _asObject(Object? value) {
  if (value is Map<String, dynamic>) {
    return value;
  }
  return const <String, dynamic>{};
}
