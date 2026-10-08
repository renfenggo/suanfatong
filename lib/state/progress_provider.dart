import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/progress.dart';
import '../services/learning_event_recorder.dart';
import '../services/progress_service.dart';
import 'cloud_sync_provider.dart';

final progressServiceProvider = Provider((ref) => ProgressService());

final progressProvider = FutureProvider<Progress>((ref) {
  return ref.watch(progressServiceProvider).loadProgress();
});

class CppProgressNotifier extends StateNotifier<Set<String>> {
  final ProgressService _service;

  /// 学习事件记录器（P1 最小闭环：单元完成 → 离线队列）；null 时不入队。
  final LearningEventRecorder? _recorder;

  /// 构造期初始加载的共享 Future：写操作先等它完成，防止 _load 的迟到
  /// 赋值覆盖写操作结果（构造 → 未加载完即 markCompleted 的竞态）。
  Future<void>? _loadFuture;

  Progress? _cached;

  CppProgressNotifier(this._service, {LearningEventRecorder? recorder})
    : _recorder = recorder,
      super(const {}) {
    _loadFuture = _load();
  }

  Future<void> _load() async {
    _cached = await _service.loadProgress();
    state = _cached!.completedCppItems;
  }

  Future<void> markCompleted(String itemId) async {
    await _loadFuture;
    _cached ??= await _service.loadProgress();
    if (state.contains(itemId)) return;
    state = {...state, itemId};
    final updated = _cached!.copyWith(completedCppItems: state);
    await _service.saveProgress(updated);
    _cached = updated;
    await _recorder?.recordKnowledgeComplete(itemId);
  }

  bool isCompleted(String itemId) => state.contains(itemId);
}

final cppProgressProvider =
    StateNotifierProvider<CppProgressNotifier, Set<String>>((ref) {
      return CppProgressNotifier(
        ref.watch(progressServiceProvider),
        recorder: ref.watch(learningEventRecorderProvider),
      );
    });

class CppQuizProgressNotifier extends StateNotifier<Progress> {
  final ProgressService _service;

  /// 学习事件记录器（P1 最小闭环：测验提交 → 离线队列）；null 时不入队。
  final LearningEventRecorder? _recorder;

  /// 构造期初始加载的共享 Future（语义同 CppProgressNotifier）。
  Future<void>? _loadFuture;

  CppQuizProgressNotifier(this._service, {LearningEventRecorder? recorder})
    : _recorder = recorder,
      super(const Progress()) {
    _loadFuture = _load();
  }

  Future<void> _load() async {
    final progress = await _service.loadProgress();
    state = progress;
  }

  Future<void> saveCppSectionQuizResult({
    required String sectionId,
    required int score,
    required Set<String> newWrongIds,
    required Set<String> correctedIds,
  }) async {
    await _loadFuture;
    final current = state;
    final updatedScores = Map<String, int>.from(current.cppQuizScores);
    updatedScores[sectionId] = score;

    final updatedAttempts = Map<String, int>.from(current.cppQuizAttempts);
    updatedAttempts[sectionId] = (updatedAttempts[sectionId] ?? 0) + 1;

    final updatedLastDates = Map<String, String>.from(current.cppQuizLastDates);
    final now = DateTime.now();
    updatedLastDates[sectionId] =
        '${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')} '
        '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';

    final updatedWrong = Set<String>.from(current.cppWrongQuizIds);
    updatedWrong.addAll(newWrongIds);
    updatedWrong.removeAll(correctedIds);

    final updated = current.copyWith(
      cppQuizScores: updatedScores,
      cppQuizAttempts: updatedAttempts,
      cppQuizLastDates: updatedLastDates,
      cppWrongQuizIds: updatedWrong,
    );
    await _service.saveProgress(updated);
    state = updated;
    await _recorder?.recordQuizSubmit(sectionId: sectionId, score: score);
  }
}

final cppQuizProgressProvider =
    StateNotifierProvider<CppQuizProgressNotifier, Progress>((ref) {
      return CppQuizProgressNotifier(
        ref.watch(progressServiceProvider),
        recorder: ref.watch(learningEventRecorderProvider),
      );
    });

class LastKnowledgeItemNotifier extends StateNotifier<String> {
  final ProgressService _service;

  /// 构造期初始加载的共享 Future（语义同 CppProgressNotifier）。
  Future<void>? _loadFuture;

  Progress? _cached;

  LastKnowledgeItemNotifier(this._service) : super('') {
    _loadFuture = _load();
  }

  Future<void> _load() async {
    _cached = await _service.loadProgress();
    state = _cached!.lastKnowledgeItemId;
  }

  Future<void> setLastKnowledgeItem(String itemId) async {
    if (itemId.isEmpty) return;
    await _loadFuture;
    _cached ??= await _service.loadProgress();
    state = itemId;
    final updated = _cached!.copyWith(lastKnowledgeItemId: itemId);
    await _service.saveProgress(updated);
    _cached = updated;
  }
}

final lastKnowledgeItemProvider =
    StateNotifierProvider<LastKnowledgeItemNotifier, String>((ref) {
      return LastKnowledgeItemNotifier(ref.watch(progressServiceProvider));
    });
