import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/mistake.dart';
import '../services/mistake_service.dart';

final mistakeServiceProvider = Provider((ref) => MistakeService());

final mistakesProvider = FutureProvider.family<List<Mistake>, String>((
  ref,
  assetPath,
) {
  return ref.watch(mistakeServiceProvider).loadMistakes(assetPath);
});
