/// 服务端学习状态拉取合成（R06-1，GO_LIVE §3.4b）：换设备进度恢复。
///
/// 此前 fetchLearningState 只在测试中覆盖，未接入 App——换设备登录后
/// 本地进度为空、服务端已完成项不回补。本服务把服务端合成状态与本地
/// 进度做单调并集并落盘，作为每轮云同步的收尾步骤（上报队列 → 拉取
/// 合成）。
library;

import '../models/progress.dart';
import 'platform_api_client.dart';
import 'progress_service.dart';

/// 拉取合成器：GET /v1/learning/state → 与本地 Progress 合成。
///
/// 合成规则（ADR-006 服务端合成语义对齐）：
/// - `completedCppItems` = 本地 ∪ 服务端 `completed_item_ids`（服务端由
///   knowledge_complete 事件单调并集合成，天然只增不减，并集安全）；
/// - 计数类（`counters`：quiz_total/quiz_correct 等）**不回写本地**——
///   服务端计数是权威观测口径，本地保留自己的明细（cppQuizScores/
///   cppQuizAttempts 等），两者互不覆盖；
/// - 其余本地字段原样保留。
///
/// 拉取失败（网络/401 等）异常原样上抛，由调用方分类处理，不吞
/// （N04 同款契约：基础设施错误不得伪装成业务结果）。
class LearningStateSynchronizer {
  LearningStateSynchronizer({
    required PlatformApiClient client,
    required ProgressService progressService,
  }) : _client = client,
       _progress = progressService;

  final PlatformApiClient _client;
  final ProgressService _progress;

  /// 拉取服务端状态并与本地进度合成，返回合成后的进度。
  ///
  /// 服务端完成项未新增时不写盘（返回本地当前值）。
  Future<Progress> pullAndMerge() async {
    final state = await _client.fetchLearningState();
    final local = await _progress.loadProgress();
    final mergedIds = local.completedCppItems.union(
      state.completedItemIds.toSet(),
    );
    if (mergedIds.length == local.completedCppItems.length) {
      return local;
    }
    final merged = local.copyWith(completedCppItems: mergedIds);
    await _progress.saveProgress(merged);
    return merged;
  }
}
