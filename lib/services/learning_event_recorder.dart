/// 学习事件记录器：把学习行为写入离线事件队列，云同步稍后统一上报。
///
/// 挂接点（P1 最小用户闭环）：
/// - C++ 单元完成（CppProgressNotifier.markCompleted）→ knowledge_complete；
/// - C++ 章节测验提交（CppQuizProgressNotifier.saveCppSectionQuizResult）
///   → quiz_submit（payload 携带 score）。
///
/// 持久化失败可观测：入队结果中的 [OfflinePersistErrors] 记录在
/// [lastPersistErrors]（事件本身已入内存队列，下次入队整体覆盖重写，
/// 事件不丢失；磁盘故障需人工诊断，不阻断学习主流程）。
library;

import 'offline_event_queue.dart';
import 'platform_api_models.dart';

class LearningEventRecorder {
  LearningEventRecorder({required OfflineEventQueue queue}) : _queue = queue;

  final OfflineEventQueue _queue;

  /// 最近一次入队触发的持久化写入错误（null/空 = 成功）；诊断用。
  OfflinePersistErrors? lastPersistErrors;

  /// 记录知识点/单元完成事件。
  Future<void> recordKnowledgeComplete(String itemId) async {
    final result = await _queue.enqueue(
      kind: LearningEventKind.knowledgeComplete,
      itemId: itemId,
    );
    lastPersistErrors = result.errors;
  }

  /// 记录测验提交事件（payload 携带得分）。
  Future<void> recordQuizSubmit({required String sectionId, required int score}) async {
    final result = await _queue.enqueue(
      kind: LearningEventKind.quizSubmit,
      itemId: sectionId,
      payload: <String, dynamic>{'score': score},
    );
    lastPersistErrors = result.errors;
  }
}
