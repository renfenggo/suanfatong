import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/progress.dart';
import '../services/progress_service.dart';

final progressServiceProvider = Provider((ref) => ProgressService());

final progressProvider = FutureProvider<Progress>((ref) {
  return ref.watch(progressServiceProvider).loadProgress();
});
