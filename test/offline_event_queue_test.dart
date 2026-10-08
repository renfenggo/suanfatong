import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/offline_event_queue.dart';
import 'package:bfs_learn/services/platform_api_models.dart';

/// 离线事件队列测试（内存/手写 Fake 存储，不发真实网络请求）。
void main() {
  group('OfflineEventQueue.enqueue', () {
    test('生成 mutation_id={device_id}:{ns}:{seq} 与 event_id，occurred_at 为 ISO 时间并持久化', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final event = (await queue.enqueue(
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'kn-1',
      )).event;

      expect(event, isNotNull);
      // N03：默认（未登录）命名空间 unowned，幂等键含命名空间段。
      expect(event!.mutationId, 'dev-1:unowned:1');
      expect(event.eventId, 'dev-1-unowned-e2');
      expect(event.kind, LearningEventKind.knowledgeComplete);
      expect(event.itemId, 'kn-1');
      expect(event.occurredAt, endsWith('Z'), reason: 'UTC ISO 8601');
      expect(queue.pendingCount, 1);
      expect((await store.loadJsonEntries()), hasLength(1), reason: '入队即落盘');

      // 持久化内容为契约线名 JSON 行
      final saved = await store.loadJsonEntries();
      expect(saved, hasLength(1));
      expect(
        jsonDecode(saved.single) as Map<String, dynamic>,
        containsPair('mutation_id', 'dev-1:unowned:1'),
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

      final duplicate = (await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'q-1-other',
        mutationId: 'fixed-key',
      )).event;

      expect(duplicate, isNull);
      expect(queue.pendingCount, 1);
      expect(store.saveCount, savesBefore, reason: '去重入队不应触发持久化');
    });

    test('自动生成的 mutation_id 连续入队互不相同', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');

      final ids = <String>[];
      for (var i = 0; i < 3; i++) {
        final event = (await queue.enqueue(
          kind: LearningEventKind.animationWatch,
          itemId: 'anim-$i',
        )).event;
        ids.add(event!.mutationId);
      }

      expect(ids.toSet().length, 3);
      expect(ids, <String>['dev-1:unowned:1', 'dev-1:unowned:3', 'dev-1:unowned:5']);
    });

    test('显式 occurred_at 与 payload 原样保留', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');

      final event = (await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'q-9',
        mutationId: 'm-explicit',
        occurredAt: '2026-10-07T08:00:00Z',
        payload: <String, dynamic>{'score': 88, 'correct': true},
      )).event;

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
      final first = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a')).event;
      final second = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b')).event;
      final third = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'c')).event;

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
      final event = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a')).event;

      await queue.completeBatch(
        EventUploadResult(accepted: <String>[event!.mutationId]),
      );

      expect(queue.pendingCount, 1, reason: '按 event_id 匹配，mutation_id 字符串不应命中');
    });

    test('清理后同步持久化（存储内容与内存一致，按 event_id 清理）', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final kept = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'keep')).event;
      final removed = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'drop')).event;

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

      final fresh = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'new')).event;

      expect(fresh!.mutationId, 'dev-1:unowned:42');
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
      // N03：未指定命名空间的文件存储默认写 unowned 命名空间的文件。
      final onDisk = jsonDecode(
        await File(
          '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.queueFileNameFor(kUnownedNamespace)}',
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
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.queueFileNameFor(kUnownedNamespace)}',
      ).writeAsString('{"events": [截断');

      expect(await newStore().loadJsonEntries(), isEmpty);
    });

    test('文件为 JSON 对象（非数组）→ 空列表', () async {
      await File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.queueFileNameFor(kUnownedNamespace)}',
      ).writeAsString('{"schema_version":"1.0"}');

      expect(await newStore().loadJsonEntries(), isEmpty);
    });

    test('数组内非字符串项被过滤，字符串行保留（行级坏行由队列跳过）', () async {
      await File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.queueFileNameFor(kUnownedNamespace)}',
      ).writeAsString('["{\\"event_id\\":\\"e-1\\"}", 42, null, "not-a-json{{{"]');

      expect(await newStore().loadJsonEntries(), <String>[
        '{"event_id":"e-1"}',
        'not-a-json{{{',
      ]);
    });

    test('目录不可写（路径被文件占用）→ save 抛异常并记录 lastQueueWriteError（P1 外抛）', () async {
      final blocker = File('${tempDir.path}${Platform.pathSeparator}blocker');
      await blocker.writeAsString('occupied');
      final store = FileOfflineEventStore(
        directoryProvider: () async => Directory(blocker.path),
      );

      await expectLater(
        store.saveJsonEntries(<String>['{"event_id":"e-1"}']),
        throwsA(isA<Exception>()),
        reason: 'P1：写失败不再被吞，向上层如实返回',
      );
      await expectLater(store.saveSeqWatermark(3), throwsA(isA<Exception>()));
      expect(store.lastQueueWriteError, isNotNull);
      expect(store.lastSeqWriteError, isNotNull);

      // load 系列仍降级不抛（损坏/缺失 → 空数据）
      expect(await store.loadJsonEntries(), isEmpty);
      expect(await store.loadSeqWatermark(), 0);
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
      // （R07 独立水位：水位含 eventId 消耗的 seq（历史 :1/:3 与 -e2/-e4），
      // 恢复为 4，续写为 :5；幂等键允许跳号，唯一性不受影响。N03：键含
      // 命名空间段 unowned）
      final fresh = (await restored.enqueue(
        kind: LearningEventKind.animationWatch,
        itemId: 'anim-1',
      )).event;
      expect(fresh!.mutationId, 'dev-1:unowned:5');
    });

    group('R07 序号水位持久化（清空队列重启不复用 ID）', () {
    test('全部确认清空队列并重启后，mutation_id 不与历史重复（audit-device:1 不再复用）', () async {
      final first = OfflineEventQueue(store: newStore(), deviceId: 'audit-device');
      final event = (await first.enqueue(
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'kn-1',
      )).event;
      await first.completeBatch(
        EventUploadResult(accepted: <String>[event!.eventId]),
      );
      expect(first.pendingCount, 0, reason: '队列已清空');
      expect(await newStore().loadJsonEntries(), isEmpty, reason: '队列文件为空');

      // 重启：旧缺陷此处 _seq 回退为 0，新事件复用 audit-device:1 被服务端
      // 按 mutation_id 误判为旧记录；R07 修复后续增为 :3。
      final restarted = OfflineEventQueue(store: newStore(), deviceId: 'audit-device');
      final fresh = (await restarted.enqueue(
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'kn-2',
      )).event;

      expect(fresh!.mutationId, isNot(event.mutationId));
      expect(fresh.mutationId, 'audit-device:unowned:3');
      expect(fresh.eventId, isNot(event.eventId));
    });

    test('清空队列后水位文件仍保留（不随队列清空删除）', () async {
      final store = newStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final event = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a')).event;
      await queue.completeBatch(EventUploadResult(accepted: <String>[event!.eventId]));

      final seqFile = File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.seqFileNameFor(kUnownedNamespace)}',
      );
      expect(await seqFile.exists(), isTrue, reason: '水位独立文件不随清队列删除');
      expect(await newStore().loadSeqWatermark(), 2);
    });

    test('水位文件损坏/非正整数 → 降级 0，由待上报事件回填兜底', () async {
      final seqFile = File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.seqFileNameFor(kUnownedNamespace)}',
      );
      await seqFile.writeAsString('corrupted{{{');
      expect(await newStore().loadSeqWatermark(), 0);

      await seqFile.writeAsString('-7');
      expect(await newStore().loadSeqWatermark(), 0);

      // 兜底路径：水位丢失但事件仍在队列中，回填仍生效
      final store = newStore();
      await store.saveJsonEntries(<String>[
        jsonEncode(const LearningEvent(
          eventId: 'e-old',
          mutationId: 'dev-1:9',
          kind: LearningEventKind.importEvent,
          itemId: 'old',
        ).toJson()),
      ]);
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final fresh = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'new')).event;
      expect(fresh!.mutationId, 'dev-1:unowned:10');
    });

    test('save→load 水位往返一致；未变化不重写', () async {
      final store = newStore();
      expect(await store.loadSeqWatermark(), 0, reason: '文件不存在 → 0');

      await store.saveSeqWatermark(42);
      expect(await newStore().loadSeqWatermark(), 42);

      final seqFile = File(
        '${tempDir.path}${Platform.pathSeparator}${FileOfflineEventStore.seqFileNameFor(kUnownedNamespace)}',
      );
      final modifiedBefore = await seqFile.lastModified();
      await store.saveSeqWatermark(42);
      expect(await seqFile.lastModified(), modifiedBefore, reason: '同值跳过重写');
    });

    test('原子替换：保存后目录无 .tmp 残留', () async {
      final store = newStore();
      await store.saveJsonEntries(<String>['{"event_id":"e-1"}']);
      await store.saveSeqWatermark(7);

      final residue = await tempDir
          .list()
          .map((entity) => entity.uri.pathSegments.last)
          .where((name) => name.endsWith('.tmp'))
          .toList();
      expect(residue, isEmpty);
    });

    test('写失败可观测：lastQueue/SeqWriteError 分别记录并外抛，成功后清除', () async {
      final blocker = File('${tempDir.path}${Platform.pathSeparator}blocker');
      await blocker.writeAsString('occupied');
      final broken = FileOfflineEventStore(
        directoryProvider: () async => Directory(blocker.path),
      );

      await expectLater(
        broken.saveJsonEntries(<String>['{"event_id":"e-1"}']),
        throwsA(isA<Exception>()),
      );
      expect(broken.lastQueueWriteError, isNotNull, reason: '写失败不再静默');
      await expectLater(broken.saveSeqWatermark(3), throwsA(isA<Exception>()));
      expect(broken.lastSeqWriteError, isNotNull);

      final healthy = newStore();
      await healthy.saveJsonEntries(const <String>[]);
      await healthy.saveSeqWatermark(5);
      expect(healthy.lastQueueWriteError, isNull);
      expect(healthy.lastSeqWriteError, isNull);
    });

    test('P1 写失败后重试：目录恢复 → 落盘成功、错误清除、事件不丢（整体覆盖重写）', () async {
      final blocker = File('${tempDir.path}${Platform.pathSeparator}blocker');
      await blocker.writeAsString('occupied');
      var broken = true;
      final store = FileOfflineEventStore(
        directoryProvider: () async => broken ? Directory(blocker.path) : tempDir,
      );
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final failed = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');
      expect(failed.event, isNotNull, reason: '事件已入内存队列');
      expect(failed.errors.queueError, isNotNull);
      expect(failed.errors.seqError, isNotNull, reason: '同一坏目录水位也失败');
      expect(store.lastQueueWriteError, isNotNull);

      broken = false; // 磁盘恢复
      final retried = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b');
      expect(retried.errors.isEmpty, isTrue, reason: '重试成功');
      expect(retried.event, isNotNull);
      expect(store.lastQueueWriteError, isNull, reason: '成功后清除错误记录');
      expect(store.lastSeqWriteError, isNull);

      // 重启恢复：两条事件都在（首次失败后第二次入队整体覆盖重写，不丢 a）
      final restored = OfflineEventQueue(
        store: FileOfflineEventStore(directoryProvider: () async => tempDir),
        deviceId: 'dev-1',
      );
      await restored.load();
      expect(restored.pendingCount, 2);
      expect((await restored.nextBatch()).map((e) => e.itemId).toList(), <String>['a', 'b']);
    });
    });
  });

  group('P1 离线队列可靠性（并发与写入失败上抛）', () {
    test('并发首次入队共享同一初始化 Future：存储只读一次、事件不丢失、ID 不复用', () async {
      // 问题复现（旧实现）：load() 用 _loaded 布尔，A 在 await 读取期间
      // 返回、B 直接通过并 add 事件，A 恢复后 _pending..clear() 吞掉 B 的
      // 事件；且每个并发入口各触发一次读取。
      final store = _FakeStore()
        ..loadDelay = const Duration(milliseconds: 30);
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final results = await Future.wait(<Future<OfflineEnqueueResult>>[
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a'),
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b'),
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'c'),
      ]);

      expect(store.loadCount, 1, reason: '并发操作共享同一个初始化 Future，只读一次存储');
      expect(
        results.map((r) => r.event).whereType<LearningEvent>(),
        hasLength(3),
      );
      expect(queue.pendingCount, 3, reason: '旧实现：初始化 clear 吞掉并发入队事件');
      final mutationIds = results.map((r) => r.event!.mutationId).toSet();
      expect(mutationIds, hasLength(3), reason: '并发入队 ID 不复用');
      for (final result in results) {
        expect(result.errors.isEmpty, isTrue);
      }
      expect(await store.loadJsonEntries(), hasLength(3));
    });

    test('入队与确认交错：按入链顺序串行执行，确认的移除、新的保留、落盘一致', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final first = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a')).event!;
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b');

      await Future.wait(<Future<Object>>[
        queue.completeBatch(EventUploadResult(accepted: <String>[first.eventId])),
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'c'),
      ]);

      expect(queue.pendingCount, 2, reason: 'a 已确认移除，b/c 保留');
      final batch = await queue.nextBatch();
      expect(batch.map((e) => e.itemId).toList(), <String>['b', 'c']);
      // 互斥链保证最后一次持久化包含完整状态（旧实现两处 _persist 并发交错）
      expect(await store.loadJsonEntries(), hasLength(2));
      expect(store._entries.first, contains('"item_id":"b"'));
      expect(store._entries.last, contains('"item_id":"c"'));
    });

    test('队列行写入失败：事件仍有效入内存，errors.queueError 上抛且不被水位失败掩盖', () async {
      final store = _FakeStore()..failNextEntriesSave = 'disk full';
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final result = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');

      expect(result.event, isNotNull, reason: '事件已入内存队列（不因落盘失败丢弃）');
      expect(result.errors.queueError, isNotNull);
      expect(result.errors.seqError, isNull, reason: '水位独立写入成功');
      expect(queue.pendingCount, 1);
    });

    test('水位写入失败：errors.seqError 上抛且不被队列行失败掩盖', () async {
      final store = _FakeStore()..failNextSeqSave = 'file locked';
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final result = await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a');

      expect(result.errors.queueError, isNull, reason: '队列行独立写入成功');
      expect(result.errors.seqError, isNotNull);
      expect(result.event, isNotNull);
    });

    test('completeBatch 写失败上抛失败结果；重启按存储旧状态恢复（重复上报由服务端幂等兜底）', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final confirmed = (await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a')).event!;
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b');
      store.failNextEntriesSave = 'flush failed';

      final errors = await queue.completeBatch(
        EventUploadResult(accepted: <String>[confirmed.eventId]),
      );

      expect(errors.queueError, isNotNull, reason: '清理后的落盘失败如实返回');
      expect(errors.seqError, isNull);
      expect(queue.pendingCount, 1, reason: '内存已清理（服务端已确认）');
      // 存储写入失败 → 重启按旧状态恢复（含已确认的 a：如实反映，
      // 重试上报由服务端 mutation_id 幂等去重兜底，不丢事件）
      final restored = OfflineEventQueue(store: store, deviceId: 'dev-1');
      await restored.load();
      expect(restored.pendingCount, 2);
      expect((await restored.nextBatch()).map((e) => e.itemId).toList(), <String>['a', 'b']);
    });

    test('并发入队全部确认并重启：水位不回退，新事件 ID 续增不复用', () async {
      final store = _FakeStore();
      final queue = OfflineEventQueue(store: store, deviceId: 'dev-1');

      final results = await Future.wait(<Future<OfflineEnqueueResult>>[
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a'),
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b'),
        queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'c'),
      ]);
      final allIds = results.map((r) => r.event!.eventId).toList();
      final completeErrors = await queue.completeBatch(
        EventUploadResult(accepted: allIds),
      );
      expect(completeErrors.isEmpty, isTrue);
      expect(queue.pendingCount, 0, reason: '队列清空');

      // 重启：水位（含 eventId 消耗的 seq，最大 :5 → 水位 6）不回退，
      // 新事件续增为 :7，不与历史 :1/:3/:5 复用（N03：键含 unowned 段）
      final restarted = OfflineEventQueue(store: store, deviceId: 'dev-1');
      final fresh = await restarted.enqueue(kind: LearningEventKind.importEvent, itemId: 'new');
      expect(fresh.event!.mutationId, 'dev-1:unowned:7');
      final historyIds = results.map((r) => r.event!.mutationId).toSet();
      expect(historyIds.contains(fresh.event!.mutationId), isFalse);
    });
  });

  group('N03 账号隔离（switchOwner 与命名空间）', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp('offline_queue_ns_test');
    });

    tearDown(() async {
      if (await tempDir.exists()) {
        await tempDir.delete(recursive: true);
      }
    });

    OfflineEventQueue newQueue(String deviceId) => OfflineEventQueue(
      store: FileOfflineEventStore(
        directoryProvider: () async => tempDir,
        namespace: kUnownedNamespace,
      ),
      deviceId: deviceId,
      storeFactory: (ns) => FileOfflineEventStore(
        directoryProvider: () async => tempDir,
        namespace: ns,
      ),
    );

    test('A 入队 → 切 B：B 看不到 A 的待上报事件；A 的数据留在 A 的文件', () async {
      final queue = newQueue('dev-1');
      final aEvent = (await queue.enqueue(
        kind: LearningEventKind.knowledgeComplete,
        itemId: 'a-item',
      )).event;
      expect(aEvent!.mutationId, 'dev-1:unowned:1');

      await queue.switchOwner('alice');
      final aliceEvent = (await queue.enqueue(
        kind: LearningEventKind.quizSubmit,
        itemId: 'alice-item',
      )).event;
      expect(aliceEvent!.mutationId, 'dev-1:alice:1', reason: '命名空间段切换，幂等键不与 unowned 撞');

      await queue.switchOwner('bob');
      expect(queue.currentNamespace, 'bob');
      expect(queue.pendingCount, 0, reason: 'B 登录后消费的是 B 命名空间的空队列');
      expect(await queue.nextBatch(), isEmpty, reason: 'A 的待上报事件不会混入 B 的上传批次');

      // A 的事件仍在 A 的文件中（隔离保留，不自动归给 B）。
      final aliceStore = FileOfflineEventStore(
        directoryProvider: () async => tempDir,
        namespace: 'alice',
      );
      final aliceEntries = await aliceStore.loadJsonEntries();
      expect(aliceEntries, hasLength(1));
      expect(aliceEntries.single, contains('alice-item'));
    });

    test('A → B → A 切回：A 的待上报事件恢复可见（不丢）', () async {
      final queue = newQueue('dev-1');
      await queue.switchOwner('alice');
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a-1');
      await queue.switchOwner('bob');
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'b-1');

      await queue.switchOwner('alice');
      expect(queue.pendingCount, 1, reason: '切回 A 恢复 A 的队列');
      expect((await queue.nextBatch()).single.itemId, 'a-1');
    });

    test('文件名带命名空间后缀；历史无后缀文件不再被读写', () async {
      // 升级前的全局队列文件（无后缀）：写入后新装配（unowned）不读它。
      await File(
        '${tempDir.path}${Platform.pathSeparator}offline_event_queue.json',
      ).writeAsString('[{"event_id":"legacy"}]');

      final store = FileOfflineEventStore(
        directoryProvider: () async => tempDir,
        namespace: kUnownedNamespace,
      );
      expect(await store.loadJsonEntries(), isEmpty, reason: '历史未归属数据隔离保留，不自动归入 unowned');

      // 写入落在带后缀的文件，不污染历史文件。
      await store.saveJsonEntries(<String>['{"event_id":"fresh"}']);
      final legacy = await File(
        '${tempDir.path}${Platform.pathSeparator}offline_event_queue.json',
      ).readAsString();
      expect(legacy, '[{"event_id":"legacy"}]', reason: '历史文件保持原样');
    });

    test('无工厂（内存装配）switchOwner：清内存待上报列表，旧账号事件不混入新批次', () async {
      final queue = OfflineEventQueue(store: _FakeStore(), deviceId: 'dev-1');
      await queue.enqueue(kind: LearningEventKind.importEvent, itemId: 'a-1');

      await queue.switchOwner('bob');

      expect(queue.pendingCount, 0);
      expect(await queue.nextBatch(), isEmpty);
    });
  });
}

/// 手写 Fake 存储：记录保存/读取次数，支持预置初始行、延迟读取与写失败注入。
class _FakeStore implements OfflineEventStore {
  _FakeStore([List<String>? initial]) : _entries = List<String>.from(initial ?? const <String>[]);

  List<String> _entries;
  int saveCount = 0;

  /// loadJsonEntries 调用次数（验证共享初始化只读一次）。
  int loadCount = 0;

  /// 读取前让出时长（放大初始化竞态窗口）。
  Duration loadDelay = Duration.zero;

  /// 下一次 saveJsonEntries 抛出（一次性注入，P1 写失败上抛）。
  Object? failNextEntriesSave;

  /// 下一次 saveSeqWatermark 抛出（一次性注入）。
  Object? failNextSeqSave;

  int _seqWatermark = 0;

  @override
  Future<List<String>> loadJsonEntries() async {
    loadCount++;
    if (loadDelay > Duration.zero) {
      await Future<void>.delayed(loadDelay);
    }
    return List<String>.from(_entries);
  }

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    final failure = failNextEntriesSave;
    if (failure != null) {
      failNextEntriesSave = null;
      throw Exception('injected entries save failure: $failure');
    }
    _entries = List<String>.from(entries);
    saveCount++;
  }

  @override
  Future<int> loadSeqWatermark() async => _seqWatermark;

  @override
  Future<void> saveSeqWatermark(int seq) async {
    final failure = failNextSeqSave;
    if (failure != null) {
      failNextSeqSave = null;
      throw Exception('injected seq save failure: $failure');
    }
    _seqWatermark = seq;
  }
}
