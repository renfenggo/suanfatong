import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/progress.dart';
import 'offline_event_queue.dart' show sanitizeNamespace, kUnownedNamespace;

/// 本地学习进度存取（SharedPreferences 单键 JSON）。
///
/// N03（2026-10-08 第二轮复核）：进度键带账号命名空间后缀
/// （`bfs_learn_progress_{ns}`），按登录账号隔离——换账号登录后加载的是
/// 该账号自己的进度，A 的完成记录不会出现在 B 的界面上。未登录使用
/// unowned 命名空间。历史无后缀键 `bfs_learn_progress` 不再被读写
/// （升级前的全局进度隔离保留在磁盘）。
class ProgressService {
  ProgressService({String? namespace})
    : _key = progressKeyFor(namespace ?? kUnownedNamespace);

  final String _key;

  /// 命名空间 → 进度偏好键。
  static String progressKeyFor(String namespace) =>
      'bfs_learn_progress_${sanitizeNamespace(namespace)}';

  Future<Progress> loadProgress() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString(_key);
    if (jsonStr == null) return const Progress();
    return Progress.fromJson(json.decode(jsonStr) as Map<String, dynamic>);
  }

  Future<void> saveProgress(Progress progress) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, json.encode(progress.toJson()));
  }

  /// 清除当前命名空间的进度键（只影响当前账号，不动其他账号数据）。
  Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
  }
}
