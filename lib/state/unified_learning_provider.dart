import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cpp_learning_unit.dart';
import 'cpp_learning_provider.dart';
import 'algorithm_learning_provider.dart';
import 'math_learning_provider.dart';

final unifiedLearningUnitByItemIdProvider =
    FutureProvider.family<CppLearningUnit?, String>((ref, itemId) {
      final sectionPrefix = itemId.split('.').first;

      if (sectionPrefix == '1' || sectionPrefix == '5') {
        return ref.watch(cppLearningUnitByItemIdProvider(itemId)).value;
      }

      if (sectionPrefix == '2' || sectionPrefix == '3') {
        return ref.watch(algorithmLearningUnitByItemIdProvider(itemId)).value;
      }

      if (sectionPrefix == '4') {
        return ref.watch(mathLearningUnitByItemIdProvider(itemId)).value;
      }

      return null;
    });
