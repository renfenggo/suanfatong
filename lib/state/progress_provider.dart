import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/progress.dart';
import '../services/progress_service.dart';

final progressServiceProvider = Provider((ref) => ProgressService());

final progressProvider = FutureProvider<Progress>((ref) {
  return ref.watch(progressServiceProvider).loadProgress();
});

class CppProgressNotifier extends StateNotifier<Set<String>> {
  final ProgressService _service;
  Progress? _cached;

  CppProgressNotifier(this._service) : super(const {}) {
    _load();
  }

  Future<void> _load() async {
    _cached = await _service.loadProgress();
    state = _cached!.completedCppItems;
  }

  Future<void> markCompleted(String itemId) async {
    _cached ??= await _service.loadProgress();
    if (state.contains(itemId)) return;
    state = {...state, itemId};
    final updated = _cached!.copyWith(completedCppItems: state);
    await _service.saveProgress(updated);
    _cached = updated;
  }

  bool isCompleted(String itemId) => state.contains(itemId);
}

final cppProgressProvider =
    StateNotifierProvider<CppProgressNotifier, Set<String>>((ref) {
      return CppProgressNotifier(ref.watch(progressServiceProvider));
    });

class CppQuizProgressNotifier extends StateNotifier<Progress> {
  final ProgressService _service;

  CppQuizProgressNotifier(this._service) : super(const Progress()) {
    _load();
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
    final current = state;
    final updatedScores = Map<String, int>.from(current.cppQuizScores);
    updatedScores[sectionId] = score;

    final updatedAttempts = Map<String, int>.from(current.cppQuizAttempts);
    updatedAttempts[sectionId] = (updatedAttempts[sectionId] ?? 0) + 1;

    final updatedWrong = Set<String>.from(current.cppWrongQuizIds);
    updatedWrong.addAll(newWrongIds);
    updatedWrong.removeAll(correctedIds);

    final updated = current.copyWith(
      cppQuizScores: updatedScores,
      cppQuizAttempts: updatedAttempts,
      cppWrongQuizIds: updatedWrong,
    );
    await _service.saveProgress(updated);
    state = updated;
  }
}

final cppQuizProgressProvider =
    StateNotifierProvider<CppQuizProgressNotifier, Progress>((ref) {
      return CppQuizProgressNotifier(ref.watch(progressServiceProvider));
    });
