import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/history_service.dart';

final historyServiceProvider = Provider((ref) => HistoryService());
