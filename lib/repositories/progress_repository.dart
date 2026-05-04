import '../services/progress_service.dart';
import '../models/progress.dart';

class ProgressRepository {
  final ProgressService _service;

  ProgressRepository({required ProgressService service}) : _service = service;

  Future<Progress> loadProgress() => _service.loadProgress();

  Future<void> saveProgress(Progress progress) =>
      _service.saveProgress(progress);
}
