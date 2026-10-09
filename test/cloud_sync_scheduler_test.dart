import 'dart:async';

import 'package:fake_async/fake_async.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/cloud_sync_scheduler.dart';
import 'package:bfs_learn/services/cloud_sync_service.dart';

/// R06-2（GO_LIVE §3.4b）：自动同步调度器测试。
void main() {
  const synced = CloudSyncResult(
    outcome: CloudSyncOutcome.synced,
    confirmedCount: 2,
  );

  CloudSyncScheduler schedulerWith(
    Future<CloudSyncResult> Function() round, {
    Duration interval = const Duration(minutes: 5),
  }) {
    return CloudSyncScheduler(syncRound: round, interval: interval);
  }

  test('triggerNow 返回本轮结果；未启动也可用', () async {
    var rounds = 0;
    final scheduler = schedulerWith(() async {
      rounds++;
      return synced;
    });

    final result = await scheduler.triggerNow();

    expect(scheduler.isRunning, isFalse);
    expect(rounds, 1);
    expect(result?.outcome, CloudSyncOutcome.synced);
    expect(result?.confirmedCount, 2);
  });

  test('一轮进行中：重入返回 null，不排队', () async {
    final gate = Completer<void>();
    final scheduler = schedulerWith(() async {
      await gate.future;
      return synced;
    });

    final first = scheduler.triggerNow();
    final second = await scheduler.triggerNow();

    expect(second, isNull, reason: '进行中的轮次被跳过');
    gate.complete();
    expect((await first)?.outcome, CloudSyncOutcome.synced);

    // 首轮结束后可再次触发。
    final third = await scheduler.triggerNow();
    expect(third?.outcome, CloudSyncOutcome.synced);
  });

  test('syncRound 抛未预期异常：兜底 null，后续调度不受影响', () async {
    var calls = 0;
    final scheduler = schedulerWith(() async {
      calls++;
      if (calls == 1) throw StateError('unexpected');
      return synced;
    });

    final failed = await scheduler.triggerNow();
    final recovered = await scheduler.triggerNow();

    expect(failed, isNull);
    expect(recovered?.outcome, CloudSyncOutcome.synced);
  });

  test('start 周期触发（含网络恢复重试语义）；stop 后不再触发', () {
    fakeAsync((async) {
      var rounds = 0;
      final scheduler = schedulerWith(
        () async {
          rounds++;
          return synced;
        },
        interval: const Duration(minutes: 5),
      );

      scheduler.start();
      expect(scheduler.isRunning, isTrue);

      // 15 分钟 = 3 个周期触发。
      async.elapse(const Duration(minutes: 15));
      expect(rounds, 3, reason: '断网期间每轮照常发起（retryLater 由 syncRound 返回）');

      scheduler.stop();
      expect(scheduler.isRunning, isFalse);
      async.elapse(const Duration(minutes: 30));
      expect(rounds, 3, reason: 'stop 后不再触发');
    });
  });

  test('start 幂等：重复 start 不叠加触发频率', () {
    fakeAsync((async) {
      var rounds = 0;
      final scheduler = schedulerWith(
        () async {
          rounds++;
          return synced;
        },
        interval: const Duration(minutes: 5),
      );

      scheduler.start();
      scheduler.start();

      async.elapse(const Duration(minutes: 10));
      expect(rounds, 2, reason: '重复 start 保持单 Timer，每周期只触发一次');
    });
  });

  test('周期触发与 triggerNow 共享防重入：同刻只跑一轮', () {
    fakeAsync((async) {
      var rounds = 0;
      final gate = Completer<void>();
      final scheduler = schedulerWith(
        () async {
          rounds++;
          await gate.future;
          return synced;
        },
        interval: const Duration(minutes: 5),
      );
      scheduler.start();

      // 手动触发第 1 轮（挂起在 gate 未完成）。
      unawaited(scheduler.triggerNow());
      // 5 分钟周期 tick 到达：第 1 轮仍在进行 → 跳过不重入。
      async.elapse(const Duration(minutes: 5));
      expect(rounds, 1, reason: '进行中的手动轮与周期 tick 合并为一轮');

      // 放行第 1 轮后，下个周期恢复正常触发。
      gate.complete();
      async.elapse(const Duration(minutes: 5));
      expect(rounds, 2);
    });
  });
}
