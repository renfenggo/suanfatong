import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/platform_api_models.dart';

/// 平台 API 契约模型测试（openapi.yaml 对齐 + 容错策略）。
void main() {
  group('LearningEventKind', () {
    test('四个契约线名解析', () {
      expect(
        LearningEventKind.fromWireName('knowledge_complete'),
        LearningEventKind.knowledgeComplete,
      );
      expect(
        LearningEventKind.fromWireName('quiz_submit'),
        LearningEventKind.quizSubmit,
      );
      expect(
        LearningEventKind.fromWireName('animation_watch'),
        LearningEventKind.animationWatch,
      );
      expect(LearningEventKind.fromWireName('import'), LearningEventKind.importEvent);
    });

    test('未知线名返回 null（枚举只增不改）', () {
      expect(LearningEventKind.fromWireName('future_kind'), isNull);
      expect(LearningEventKind.fromWireName(null), isNull);
      expect(LearningEventKind.fromWireName(''), isNull);
    });

    test('wireName 输出与契约一致', () {
      expect(LearningEventKind.knowledgeComplete.wireName, 'knowledge_complete');
      expect(LearningEventKind.quizSubmit.wireName, 'quiz_submit');
      expect(LearningEventKind.animationWatch.wireName, 'animation_watch');
      expect(LearningEventKind.importEvent.wireName, 'import');
    });
  });

  group('UserBrief', () {
    test('完整解析 snake_case 字段', () {
      final user = UserBrief.fromJson(const <String, dynamic>{
        'user_id': 'u-1',
        'display_name': '张三',
        'role': 'student',
        'tenant_id': 't-1',
      });
      expect(user.userId, 'u-1');
      expect(user.displayName, '张三');
      expect(user.role, 'student');
      expect(user.tenantId, 't-1');
    });

    test('字段缺失容错为空串，未知字段忽略', () {
      final user = UserBrief.fromJson(const <String, dynamic>{
        'user_id': 'u-1',
        'extra': <String, dynamic>{'ignored': true},
      });
      expect(user.userId, 'u-1');
      expect(user.displayName, '');
      expect(user.role, '');
      expect(user.tenantId, '');
    });

    test('toJson 回写线格式', () {
      const user = UserBrief(userId: 'u-1', displayName: '张三', role: 'teacher', tenantId: 't-1');
      expect(user.toJson(), const <String, dynamic>{
        'user_id': 'u-1',
        'display_name': '张三',
        'role': 'teacher',
        'tenant_id': 't-1',
      });
    });
  });

  group('AuthToken', () {
    test('完整解析（含嵌套 UserBrief）', () {
      final token = AuthToken.fromJson(const <String, dynamic>{
        'access_token': 'at-xxx',
        'refresh_token': 'rt-yyy',
        'expires_in_s': 3600,
        'user': <String, dynamic>{
          'user_id': 'u-1',
          'display_name': '张三',
          'role': 'student',
          'tenant_id': 't-1',
        },
      });
      expect(token.accessToken, 'at-xxx');
      expect(token.refreshToken, 'rt-yyy');
      expect(token.expiresInS, 3600);
      expect(token.user.userId, 'u-1');
      expect(token.user.role, 'student');
    });

    test('字段缺失容错为默认值', () {
      final token = AuthToken.fromJson(const <String, dynamic>{});
      expect(token.accessToken, '');
      expect(token.refreshToken, '');
      expect(token.expiresInS, 0);
      expect(token.user, const UserBrief());
    });

    test('user 非对象时容错为空 UserBrief', () {
      final token = AuthToken.fromJson(const <String, dynamic>{
        'access_token': 'at',
        'user': 'corrupted',
      });
      expect(token.accessToken, 'at');
      expect(token.user.userId, '');
    });

    test('toJson 往返一致', () {
      final token = AuthToken.fromJson(const <String, dynamic>{
        'access_token': 'at-xxx',
        'refresh_token': 'rt-yyy',
        'expires_in_s': 7200,
        'user': <String, dynamic>{'user_id': 'u-9'},
      });
      expect(AuthToken.fromJson(token.toJson()).toJson(), token.toJson());
    });
  });

  group('LearningEvent', () {
    test('完整解析 + payload 透传', () {
      final event = LearningEvent.fromJson(const <String, dynamic>{
        'event_id': 'e-1',
        'mutation_id': 'dev-1:3',
        'kind': 'quiz_submit',
        'item_id': 'quiz-bfs-1',
        'occurred_at': '2026-10-07T08:00:00Z',
        'payload': <String, dynamic>{'score': 90, 'correct': true},
      });
      expect(event.eventId, 'e-1');
      expect(event.mutationId, 'dev-1:3');
      expect(event.kind, LearningEventKind.quizSubmit);
      expect(event.itemId, 'quiz-bfs-1');
      expect(event.occurredAt, '2026-10-07T08:00:00Z');
      expect(event.payload, const <String, dynamic>{'score': 90, 'correct': true});
    });

    test('缺失字段容错：payload 空对象、occurred_at 空串、kind 未知归 import', () {
      final event = LearningEvent.fromJson(const <String, dynamic>{
        'event_id': 'e-1',
        'mutation_id': 'm-1',
        'kind': 'future_kind',
        'item_id': 'item-1',
      });
      expect(event.kind, LearningEventKind.importEvent);
      expect(event.payload, isEmpty);
      expect(event.occurredAt, '');
    });

    test('payload 非对象时容错为空对象', () {
      final event = LearningEvent.fromJson(const <String, dynamic>{
        'event_id': 'e',
        'mutation_id': 'm',
        'kind': 'import',
        'item_id': 'i',
        'payload': <dynamic>[1, 2],
      });
      expect(event.payload, isEmpty);
    });

    test('toJson 输出契约线名（枚举序列化）', () {
      const event = LearningEvent(
        eventId: 'e-1',
        mutationId: 'dev-1:3',
        kind: LearningEventKind.animationWatch,
        itemId: 'anim-1',
        occurredAt: '2026-10-07T08:00:00Z',
        payload: <String, dynamic>{'seconds': 42},
      );
      expect(event.toJson(), const <String, dynamic>{
        'event_id': 'e-1',
        'mutation_id': 'dev-1:3',
        'kind': 'animation_watch',
        'item_id': 'anim-1',
        'occurred_at': '2026-10-07T08:00:00Z',
        'payload': <String, dynamic>{'seconds': 42},
      });
    });

    test('toJson/fromJson 往返一致（队列持久化依赖）', () {
      const event = LearningEvent(
        eventId: 'e-2',
        mutationId: 'dev-1:9',
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'kn-bfs',
        occurredAt: '2026-10-07T09:30:00.123Z',
        payload: <String, dynamic>{'layer': 2},
      );
      expect(LearningEvent.fromJson(event.toJson()).toJson(), event.toJson());
    });
  });

  group('LearningState', () {
    test('完整解析（version/完成项/计数器）', () {
      final state = LearningState.fromJson(const <String, dynamic>{
        'version': 7,
        'completed_item_ids': <String>['kn-1', 'kn-2'],
        'counters': <String, dynamic>{
          'quiz_submit': 12,
          'knowledge_complete': 34,
        },
      });
      expect(state.version, 7);
      expect(state.completedItemIds, <String>['kn-1', 'kn-2']);
      expect(state.counters, const <String, dynamic>{
        'quiz_submit': 12,
        'knowledge_complete': 34,
      });
    });

    test('缺失字段容错为默认值，非字符串项过滤', () {
      final state = LearningState.fromJson(const <String, dynamic>{
        'completed_item_ids': <dynamic>['kn-1', 42, null],
        'counters': 'corrupted',
      });
      expect(state.version, 0);
      expect(state.completedItemIds, <String>['kn-1']);
      expect(state.counters, isEmpty);
    });

    test('toJson 往返一致', () {
      const state = LearningState(
        version: 3,
        completedItemIds: <String>['a', 'b'],
        counters: <String, dynamic>{'k': 1},
      );
      expect(LearningState.fromJson(state.toJson()).toJson(), state.toJson());
    });
  });

  group('ErrorEnvelope', () {
    test('完整解析（含 trace_id/request_id/details）', () {
      final envelope = ErrorEnvelope.fromJson(const <String, dynamic>{
        'schema_version': '1.0',
        'code': 'UNAUTHORIZED',
        'message': '令牌无效',
        'retryable': false,
        'trace_id': 'trace-1',
        'request_id': 'req-1',
        'details': <String, dynamic>{'reason': 'expired'},
      });
      expect(envelope.schemaVersion, '1.0');
      expect(envelope.code, 'UNAUTHORIZED');
      expect(envelope.message, '令牌无效');
      expect(envelope.retryable, isFalse);
      expect(envelope.traceId, 'trace-1');
      expect(envelope.requestId, 'req-1');
      expect(envelope.details, const <String, dynamic>{'reason': 'expired'});
    });

    test('最小信封（仅契约必填三字段），schema_version 缺省补 1.0', () {
      final envelope = ErrorEnvelope.fromJson(const <String, dynamic>{
        'code': 'RATE_LIMITED',
        'message': '请求过频',
        'retryable': true,
      });
      expect(envelope.schemaVersion, '1.0');
      expect(envelope.retryable, isTrue);
      expect(envelope.traceId, isNull);
      expect(envelope.requestId, isNull);
      expect(envelope.details, isEmpty);
    });

    test('必填字段缺失容错（code→UNKNOWN、retryable→false）', () {
      final envelope = ErrorEnvelope.fromJson(const <String, dynamic>{
        'message': '半截信封',
      });
      expect(envelope.code, 'UNKNOWN');
      expect(envelope.retryable, isFalse);
      expect(envelope.message, '半截信封');
    });

    test('toJson 保留可选字段并保持线名', () {
      const envelope = ErrorEnvelope(
        code: 'INTERNAL',
        message: '内部错误',
        retryable: true,
        traceId: 't-1',
        requestId: 'r-1',
      );
      expect(envelope.toJson(), const <String, dynamic>{
        'schema_version': '1.0',
        'code': 'INTERNAL',
        'message': '内部错误',
        'retryable': true,
        'trace_id': 't-1',
        'request_id': 'r-1',
        'details': <String, dynamic>{},
      });
    });
  });

  group('EventUploadResult', () {
    test('解析 accepted/duplicated，非字符串项过滤', () {
      final result = EventUploadResult.fromJson(const <String, dynamic>{
        'accepted': <dynamic>['dev-1:1', 'dev-1:2', 3],
        'duplicated': <dynamic>['dev-1:3', null],
      });
      expect(result.accepted, <String>['dev-1:1', 'dev-1:2']);
      expect(result.duplicated, <String>['dev-1:3']);
    });

    test('字段缺失容错为空列表', () {
      final result = EventUploadResult.fromJson(const <String, dynamic>{});
      expect(result.accepted, isEmpty);
      expect(result.duplicated, isEmpty);
      expect(result.confirmedMutationIds, isEmpty);
    });

    test('confirmedMutationIds 为 accepted 与 duplicated 并集', () {
      const result = EventUploadResult(
        accepted: <String>['m-1', 'm-2'],
        duplicated: <String>['m-2', 'm-3'],
      );
      expect(result.confirmedMutationIds, <String>{'m-1', 'm-2', 'm-3'});
    });
  });
}
