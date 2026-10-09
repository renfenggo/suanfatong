import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/models/progress.dart';
import 'package:bfs_learn/services/learning_state_synchronizer.dart';
import 'package:bfs_learn/services/platform_api_client.dart';
import 'package:bfs_learn/services/platform_api_models.dart';
import 'package:bfs_learn/services/progress_service.dart';

/// R06-1（GO_LIVE §3.4b）：服务端状态拉取合成测试——换设备进度恢复。
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues(<String, Object>{});
  });

  ProgressService serviceFor(String ns) => ProgressService(namespace: ns);

  test('换设备恢复：本地为空，服务端完成项并集落盘', () async {
    await serviceFor('alice').saveProgress(
      const Progress().copyWith(completedCppItems: {'item-1'}),
    );
    final synchronizer = LearningStateSynchronizer(
      client: _StaticStateClient(
        const LearningState(version: 7, completedItemIds: ['item-1', 'item-2']),
      ),
      progressService: serviceFor('alice'),
    );

    final merged = await synchronizer.pullAndMerge();

    expect(merged.completedCppItems, {'item-1', 'item-2'});
    // 落盘可恢复（新设备/清缓存后从盘上读回合成结果）。
    final reloaded = await serviceFor('alice').loadProgress();
    expect(reloaded.completedCppItems, {'item-1', 'item-2'});
  });

  test('服务端是本地子集：不写盘，返回本地当前值', () async {
    final service = serviceFor('bob');
    await service.saveProgress(
      const Progress().copyWith(completedCppItems: {'a', 'b'}),
    );
    final synchronizer = LearningStateSynchronizer(
      client: _StaticStateClient(const LearningState(completedItemIds: ['a'])),
      progressService: service,
    );

    final merged = await synchronizer.pullAndMerge();

    expect(merged.completedCppItems, {'a', 'b'});
    expect((await service.loadProgress()).completedCppItems, {'a', 'b'});
  });

  test('合成只动 completedCppItems：本地明细字段原样保留', () async {
    final service = serviceFor('carol');
    await service.saveProgress(
      const Progress(
        completedCppItems: {'a'},
        cppQuizScores: {'sec-1': 90},
        cppQuizAttempts: {'sec-1': 2},
        cppWrongQuizIds: {'q3'},
        lastKnowledgeItemId: 'a',
      ),
    );
    final synchronizer = LearningStateSynchronizer(
      client: _StaticStateClient(
        // counters（quiz_total 等）不回写本地：服务端权威观测口径，
        // 本地保留明细，互不覆盖。
        const LearningState(
          completedItemIds: ['b'],
          counters: <String, dynamic>{'quiz_total': 99, 'quiz_correct': 98},
        ),
      ),
      progressService: service,
    );

    final merged = await synchronizer.pullAndMerge();

    expect(merged.completedCppItems, {'a', 'b'});
    expect(merged.cppQuizScores, {'sec-1': 90});
    expect(merged.cppQuizAttempts, {'sec-1': 2});
    expect(merged.cppWrongQuizIds, {'q3'});
    expect(merged.lastKnowledgeItemId, 'a');
  });

  test('服务端空状态：返回本地，无新增', () async {
    final service = serviceFor('dave');
    await service.saveProgress(
      const Progress().copyWith(completedCppItems: {'x'}),
    );
    final synchronizer = LearningStateSynchronizer(
      client: _StaticStateClient(const LearningState(version: 1)),
      progressService: service,
    );

    final merged = await synchronizer.pullAndMerge();

    expect(merged.completedCppItems, {'x'});
  });

  test('拉取失败异常上抛（不吞、不落盘）', () async {
    final service = serviceFor('erin');
    await service.saveProgress(
      const Progress().copyWith(completedCppItems: {'a'}),
    );
    final synchronizer = LearningStateSynchronizer(
      client: _ThrowingStateClient(
        const PlatformNetworkException('state endpoint unreachable'),
      ),
      progressService: service,
    );

    await expectLater(
      synchronizer.pullAndMerge(),
      throwsA(isA<PlatformNetworkException>()),
    );
    // 失败不污染本地进度。
    expect((await service.loadProgress()).completedCppItems, {'a'});
  });
}

class _StaticStateClient extends PlatformApiClient {
  _StaticStateClient(this.state);

  final LearningState state;

  @override
  Future<LearningState> fetchLearningState() async => state;
}

class _ThrowingStateClient extends PlatformApiClient {
  _ThrowingStateClient(this.error);

  final Object error;

  @override
  Future<LearningState> fetchLearningState() async => throw error;
}
