import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/offline_event_queue.dart';
import 'package:bfs_learn/services/platform_api_models.dart';

/// 离线事件队列测试（内存/手写 Fake 存储，不发真实网络请求）。
void main() {
  group('OfflineEventQueue.enqueue', () {
    test('生成 mutation_id={device_id}:{seq} 与 event_id，occurred_at 为 ISO 时间并持久化', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final event = await queue.enqueue(
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'kn-1',
      );

      expect(event, isNotNull);
      expect(event!.mutationId, 'dev-1:1');
      expect(event.eventId, 'dev-1-e2');
      expect(event.kind, LearningEventKind.knowledgeComplete);
      expect(event.itemId, 'kn-1');
      expect(event.occurredAt, endsWith('Z'), reason: 'UTC ISO 8601');
      expect(queue.pendingCount, 1);

      // 持久化内容为契约线名 JSON 行
      final saved = await store.loadJsonEntries();
      expect(saved, hasLength(1));
      expect(
        jsonDecode(saved.single) as Map<String, dynamic>,
        containsPair('mutation_id', 'dev-1:1'),
      );
      expect(
        jsonDecode(saved.single) as Map<String, dynamic>,
        containsPair('kind', 'knowledge_complete'),
      );
    });

    test('同 mutation_id 重复入队被去重（返回 null，队列与存储不变）', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'q-1',
        mutationId: 'fixed-key',
      );
      final savesBefore = store.saveCount;

      final duplicate = await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'q-1-other',
        mutationId: 'fixed-key',
      );

      expect(duplicate, isNull);
      expect(queue.pendingCount, 1);
      expect(store.saveCount, savesBefore, reason: '去重入队不应触发持久化');
    });

    test('自动生成的 mutation_id 连续入队互不相同', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');

      final ids = <String>[];
      for (var i = 0; i < 3; i++) {
        final event = await queue.enqueue(
          kind: LearningEventKind.animationWatch,
          itemId: 'anim-$i',
        );
        ids.add(event!.mutationId);
      }

      expect(ids.toSet().length, 3);
      expect(ids, <String>['dev-1:1', 'dev-1:3', 'dev-1:5']);
    });

    test('显式 occurred_at 与 payload 原样保留', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');

      final event = await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'q-9',
        mutationId: 'm-explicit',
        occurredAt: '2026-10-07T08:00:00Z',
        payload: <String, dynamic>{'score': 88, 'correct': true},
      );

      expect(event!.occurredAt, '2026-10-07T08:00:00Z');
      expect(event.payload, <String, dynamic>{'score': 88, 'correct': true});
    });
  });

  group('OfflineEventQueue.nextBatch', () {
    test('FIFO：批次顺序与入队顺序一致', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      for (var i = 0; i < 3; i++) {
        await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'item-$i');
      }

      final batch = await queue.nextBatch();

      expect(batch.map((e) => e.itemId).toList(), <String>['item-0', 'item-1', 'item-2']);
    });

    test('批量切分：205 条 → 200 + 5，传入更大的 maxCount 也被钳到契约上限', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      for (var i = 0; i < 205; i++) {
        await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'item-$i');
      }

      final first = await queue.nextBatch(maxCount: 500);
      expect(first, hasLength(200));
      expect(first.first.itemId, 'item-0');

      // 模拟第一批上报全部 accepted（回带 event_id）→ 取下一批
      await queue.completeBatch(
        EventUploadResult(accepted: first.map((e) => e.eventId).toList()),
      );
      final second = await queue.nextBatch();

      expect(second, hasLength(5));
      expect(second.first.itemId, 'item-200');
    });

    test('只读不出队：上报失败后再次取批内容与 mutation_id 完全一致', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      await queue.enqueue(kind: LearningEventKind.knowledgeComplete, itemId: 'kn-1');
      await queue.enqueue(kind: LearningEventKind.knowledgeComplete, itemId: 'kn-2');

      final first = await queue.nextBatch();
      // 模拟上报抛异常 → 不调 completeBatch，直接重试
      final second = await queue.nextBatch();

      expect(
        second.map((e) => e.mutationId).toList(),
        first.map((e) => e.mutationId).toList(),
      );
      expect(queue.pendingCount, 2);
    });

    test('空队列为空批次、maxCount<1 钳制为 1', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');

      expect(await queue.nextBatch(), isEmpty);

      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'only');
      final batch = await queue.nextBatch(maxCount: 0);
      expect(batch, hasLength(1));
    });
  });

  group('OfflineEventQueue.completeBatch', () {
    test('accepted 与 duplicated 回带 event_id，均按 event_id 移除，未提及的保留', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      final first = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');
      final second = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b');
      final third = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'c');

      await queue.completeBatch(EventUploadResult(
        accepted: <String>[first!.eventId],
        duplicated: <String>[second!.eventId],
      ));

      expect(queue.pendingCount, 1);
      final batch = await queue.nextBatch();
      expect(batch.single.itemId, 'c');
      expect(batch.single.eventId, third!.eventId);
    });

    test('语义防护：回带字符串恰好等于某事件 mutation_id 时不再移除（契约回带 event_id）', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      final event = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');

      await queue.completeBatch(
        EventUploadResult(accepted: <String>[event!.mutationId]),
      );

      expect(queue.pendingCount, 1, reason: '按 event_id 匹配，mutation_id 字符串不应命中');
    });

    test('清理后同步持久化（存储内容与内存一致，按 event_id 清理）', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final kept = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'keep');
      final removed = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'drop');

      await queue.completeBatch(
        EventUploadResult(accepted: <String>[removed!.eventId]),
      );

      final saved = await store.loadJsonEntries();
      expect(saved, hasLength(1));
      expect(
        (jsonDecode(saved.single) as Map<String, dynamic>)['event_id'],
        kept!.eventId,
      );
    });

    test('空结果（无 accepted/duplicated）不动队列', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');

      await queue.completeBatch(const EventUploadResult());

      expect(queue.pendingCount, 1);
      expect(store.saveCount, 1, reason: '仅入队触发过一次持久化');
    });
  });

  group('OfflineEventQueue.load', () {
    test('从存储恢复队列与 FIFO 顺序', () async {
      final store = _FakeStore(<String>[
        jsonEncode(const LearningEvent(
          eventId: 'e-1',
          mutationId: 'dev-1:5',
          kind: LearningEventKind.knowledgeComplete,
          itemId: 'kn-1',
          occurredAt: '2026-10-07T08:00:00Z',
        ).toJson()),
        jsonEncode(const LearningEvent(
          eventId: 'e-2',
          mutationId: 'dev-1:7',
          kind: LearningEventKind.quizSubmit,
          itemId: 'q-1',
          occurredAt: '2026-10-07T09:00:00Z',
        ).toJson()),
      ]);
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      expect(queue.pendingCount, 0, reason: 'load 懒加载，首个操作前不读存储');
      await queue.load();

      expect(queue.pendingCount, 2);
      final batch = await queue.nextBatch();
      expect(batch.first.itemId, 'kn-1');
      expect(batch.first.kind, LearningEventKind.knowledgeComplete);
    });

    test('恢复 seq 水位：重启后新生成的 mutation_id 不与历史冲突', () async {
      final store = _FakeStore(<String>[
        jsonEncode(const LearningEvent(
          eventId: 'e-old',
          mutationId: 'dev-1:41',
          kind: LearningEventKind.importEvent,
          itemId: 'old',
        ).toJson()),
      ]);
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final fresh = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'new');

      expect(fresh!.mutationId, 'dev-1:42');
    });

    test('损坏的持久化行被跳过，不破坏其余事件', () async {
      final store = _FakeStore(<String>[
        'not-a-json{{{',
        jsonEncode(const LearningEvent(
          eventId: 'e-ok',
          mutationId: 'dev-1:2',
          kind: LearningEventKind.animationWatch,
          itemId: 'ok',
        ).toJson()),
      ]);
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      await queue.load();

      expect(queue.pendingCount, 1);
      expect((await queue.nextBatch()).single.itemId, 'ok');
    });
  });

  group('FileOfflineEventStore', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp('offline_queue_test');
    });

    tearDown(() async {
      if (await tempDir.exists()) {
        await tempDir.delete(recursive: true);
      }
    });

    FileOfflineEventStore newStore() => FileOfflineEventStore(
      directoryProvider: () async => tempDir,
    );

    test('文件不存在 → 空列表（首次运行）', () async {
      expect(await newStore().loadJsonEntries(), isEmpty);
    });

    test('save→load 往返一致且保序，文件内容为字符串数组', () async {
      final store = newStore();
      final entries = <String>[
        jsonEncode(const LearningEvent(
          eventId: 'e-1',
          mutationId: 'dev-1:1',
          kind: LearningEventKind.knowledgeComplete,
          itemId: 'kn-1',
        ).toJson()),
        jsonEncode(const LearningEvent(
          eventId: 'e-2',
          mutationId: 'dev-1:3',
          kind: LearningEventKind.quizSubmit,
          itemId: 'q-1',
        ).toJson()),
      ];

      await store.saveJsonEntries(entries);

      expect(await store.loadJsonEntries(), entries);
      final onDisk = jsonDecode(
        await File(
          '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.defaultFileName}',
        ).readAsString(),
      );
      expect(onDisk, isA<List<dynamic>>());
      expect((onDisk as List<dynamic>).whereType<String>().toList(), entries);
    });

    test('save 空列表覆盖旧内容（清理后不残留历史行）', () async {
      final store = newStore();
      await store.saveJsonEntries(<String>['{"event_id":"e-1"}']);
      await store.saveJsonEntries(const <String>[]);

      expect(await store.loadJsonEntries(), isEmpty);
    });

    test('文件损坏（非 JSON）→ 降级空列表不抛', () async {
      await File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.defaultFileName}',
      ).writeAsString('{"events": [截断');

      expect(await newStore().loadJsonEntries(), isEmpty);
    });

    test('文件为 JSON 对象（非数组）→ 空列表', () async {
      await File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.defaultFileName}',
      ).writeAsString('{"schema_version":"1.0"}');

      expect(await newStore().loadJsonEntries(), isEmpty);
    });

    test('数组内非字符串项被过滤，字符串行保留（行级坏行由队列跳过）', () async {
      await File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.defaultFileName}',
      ).writeAsString('["{\\"event_id\\":\\"e-1\\"}", 42, null, "not-a-json{{{"]');

      expect(await newStore().loadJsonEntries(), <String>[
        '{"event_id":"e-1"}',
        'not-a-json{{{',
      ]);
    });

    test('目录不可写（路径被文件占用）→ save 不抛异常', () async {
      final blocker = File('${tempDir.path}${Platform.pathSeparator}blocker');
      await blocker.writeAsString('occupied');
      final store = FileOfflineEventStore(
        directoryProvider: () async => Directory(blocker.path),
      );

      await store.saveJsonEntries(<String>['{"event_id":"e-1"}']);
      await store.saveJsonEntries(const <String>[]);

      expect(await store.loadJsonEntries(), isEmpty);
    });

    test('与 OfflineEventQueue 集成：enqueue 落盘 → 新实例恢复队列与 seq 水位', () async {
      final queue = OfflineEventQueue(store: newStore(), deviceId: 'dev-1');
      await queue.enqueue(kind: LearningEventKind.knowledgeComplete, itemId: 'kn-1');
      await queue.enqueue(kind: LearningEventKind.quizSubmit, itemId: 'q-1');

      final restored = OfflineEventQueue(store: newStore(), deviceId: 'dev-1');
      final restoredBatch = await restored.nextBatch();

      expect(restoredBatch, hasLength(2));
      expect(restoredBatch.map((e) => e.itemId).toList(), <String>['kn-1', 'q-1']);

      // 重启后新生成的 mutation_id 不与历史冲突
      // （水位回填只扫 {device_id}:{seq} 形态的 mutation_id：历史用了 :1/:3，
      // eventId 的 -e2/-e4 不参与回填，故续写为 :4）
      final fresh = await restored.enqueue(
        kind: LearningEventKind.animationWatch,
        itemId: 'anim-1',
      );
      expect(fresh!.mutationId, 'dev-1:4');
    });
  });
}

/// 手写 Fake 存储：记录保存次数，支持预置初始行。
class _FakeStore implements OfflineEventStore {
  _FakeStore([List<String>? initial]) : _entries = List<String>.from(initial ?? const <String>[]);

  List<String> _entries;
  int saveCount = 0;

  @override
  Future<List<String>> loadJsonEntries() async => List<String>.from(_entries);

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    _entries = List<String>.from(entries);
    saveCount++;
  }
}
