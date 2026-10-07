import 'dart:convert';
import 'dart:io';

import 'package:path_provider/path_provider.dart';

import 'platform_api_models.dart';

/// 离线事件队列持久化抽象（V1：整体读/写 JSON 行列表）。
///
/// 生产实现（SharedPreferences/文件，M4-F2 接入）构造注入；测试用内存实现。
abstract class OfflineEventStore {
  /// 读取全部待上报事件的 JSON 行（按入队顺序）。
  Future<List<String>> loadJsonEntries();

  /// 覆盖保存全部待上报事件（每次入队/清理后调用）。
  Future<void> saveJsonEntries(List<String> entries);
}

/// 内存实现（测试与未接持久化阶段的默认选择）。
class InMemoryOfflineEventStore implements OfflineEventStore {
  final List<String> _entries = <String>[];

  @override
  Future<List<String>> loadJsonEntries() async => List<String>.from(_entries);

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    _entries
      ..clear()
      ..addAll(entries);
  }
}

/// 文件实现：单 JSON 文件（字符串数组），ADR-006 V1 队列持久化。
///
/// 位置默认取应用支持目录（path_provider），构造可注入目录解析函数以便测试。
/// 损坏降级：文件不存在/不可解析/非数组 → 空队列（事件 append-only，跳过
/// 坏行由 [OfflineEventQueue.load] 承担），任何文件 IO 异常不外抛。
class FileOfflineEventStore implements OfflineEventStore {
  FileOfflineEventStore({
    Future<Directory> Function()? directoryProvider,
    this.fileName = defaultFileName,
  }) : _directoryProvider =
           directoryProvider ?? getApplicationSupportDirectory;

  /// 队列文件名（应用支持目录下）。
  static const String defaultFileName = 'offline_event_queue.json';

  final Future<Directory> Function() _directoryProvider;
  final String fileName;

  Future<File> _resolveFile() async {
    final directory = await _directoryProvider();
    return File('${directory.path}${Platform.pathSeparator}$fileName');
  }

  @override
  Future<List<String>> loadJsonEntries() async {
    try {
      final file = await _resolveFile();
      if (!await file.exists()) {
        return const <String>[];
      }
      final decoded = jsonDecode(await file.readAsString());
      if (decoded is List<dynamic>) {
        return decoded.whereType<String>().toList();
      }
      return const <String>[];
    } on Exception {
      // 损坏文件降级为空队列，不 crash（ADR-006：事件层可独立回滚）。
      return const <String>[];
    }
  }

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    try {
      final file = await _resolveFile();
      await file.parent.create(recursive: true);
      await file.writeAsString(jsonEncode(entries), flush: true);
    } on Exception {
      // 写失败不外抛：内存队列仍有效，下次入队整体覆盖重写。
    }
  }
}

/// 离线学习事件队列（ADR-006：本地 append-only 事件、mutation_id 幂等、
/// 网络恢复后按序批量上报，单批 ≤ [maxBatchSize] 对齐契约）。
///
/// mutation_id 生成采用 ADR-006 方案 `{device_id}:{local_seq}`，seq 水位随
/// 队列恢复而回填，重启后不产生重复幂等键；上报重试间事件对象不变。
class OfflineEventQueue {
  OfflineEventQueue({required OfflineEventStore store, required this.deviceId})
    : _store = store;

  /// 契约单批上限（POST /v1/learning/events maxItems 200）。
  static const int maxBatchSize = 200;

  final OfflineEventStore _store;
  final String deviceId;

  final List<LearningEvent> _pending = <LearningEvent>[];
  int _seq = 0;
  bool _loaded = false;

  /// 待上报事件数。
  int get pendingCount => _pending.length;

  /// 从持久化恢复队列（懒加载，首个操作前自动完成）。
  Future<void> load() async {
    if (_loaded) {
      return;
    }
    _loaded = true;
    final entries = await _store.loadJsonEntries();
    _pending
      ..clear()
      ..addAll(
        entries.map((String line) => _tryDecodeEvent(line)).whereType<LearningEvent>(),
      );
    // 回填 seq 水位：扫描本机已入队 mutation_id（{deviceId}:{seq}）取最大值，
    // 保证重启后新生成的幂等键不与历史冲突。
    final prefix = '$deviceId:';
    for (final event in _pending) {
      if (event.mutationId.startsWith(prefix)) {
        final seq = int.tryParse(event.mutationId.substring(prefix.length));
        if (seq != null && seq > _seq) {
          _seq = seq;
        }
      }
    }
  }

  /// 入队一个学习事件并立即持久化。
  ///
  /// [mutationId] 缺省时自动生成（`{device_id}:{seq}`）；与队列中待上报事件
  /// 重复时跳过并返回 null（入队去重）。已上报成功移除后同键再次入队不拦，
  /// 最终幂等由服务端 duplicated 兜底。
  Future<LearningEvent?> enqueue({
    required LearningEventKind kind,
    required String itemId,
    String? mutationId,
    String? occurredAt,
    Map<String, dynamic> payload = const <String, dynamic>{},
  }) async {
    await load();
    final effectiveMutationId = mutationId ?? '$deviceId:${_advanceSeq()}';
    for (final event in _pending) {
      if (event.mutationId == effectiveMutationId) {
        return null;
      }
    }
    final event = LearningEvent(
      eventId: '$deviceId-e${_advanceSeq()}',
      mutationId: effectiveMutationId,
      kind: kind,
      itemId: itemId,
      occurredAt: occurredAt ?? DateTime.now().toUtc().toIso8601String(),
      payload: payload,
    );
    _pending.add(event);
    await _persist();
    return event;
  }

  /// 按入队顺序取下一批待上报事件（≤ [maxCount]，钳制到 [1, maxBatchSize]）。
  ///
  /// 只读不出队：上报成功后调 [completeBatch] 按 accepted/duplicated 清理；
  /// 失败则原样保留重试（mutation_id 不变保证服务端幂等去重）。
  Future<List<LearningEvent>> nextBatch({int maxCount = maxBatchSize}) async {
    await load();
    var count = maxCount < 1 ? 1 : maxCount;
    if (count > maxBatchSize) {
      count = maxBatchSize;
    }
    if (count > _pending.length) {
      count = _pending.length;
    }
    return List<LearningEvent>.unmodifiable(_pending.take(count));
  }

  /// 上报成功后清理：响应 accepted/duplicated 回带 event_id（契约 M4-5
  /// 实装语义），两个集合中的事件均视为已确认并移除；响应中未提及的事件
  /// 保留待下次重试。
  Future<void> completeBatch(EventUploadResult result) async {
    await load();
    if (_pending.isEmpty) {
      return;
    }
    final confirmed = result.confirmedEventIds;
    if (confirmed.isEmpty) {
      return;
    }
    _pending.removeWhere((LearningEvent event) => confirmed.contains(event.eventId));
    await _persist();
  }

  int _advanceSeq() => ++_seq;

  Future<void> _persist() async {
    await _store.saveJsonEntries(
      _pending.map((LearningEvent event) => jsonEncode(event.toJson())).toList(),
    );
  }

  /// 持久化行 → 事件（损坏行跳过：事件 append-only，跳过不破坏后续）。
  static LearningEvent? _tryDecodeEvent(String line) {
    try {
      final decoded = jsonDecode(line);
      if (decoded is Map<String, dynamic>) {
        return LearningEvent.fromJson(decoded);
      }
      return null;
    } on FormatException {
      return null;
    }
  }
}
