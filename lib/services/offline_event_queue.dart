import 'dart:convert';
import 'dart:io';

import 'package:path_provider/path_provider.dart';

import 'platform_api_models.dart';

/// 离线事件队列持久化抽象（V1：整体读/写 JSON 行列表）。
///
/// 生产实现（文件）构造注入；测试用内存/Fake 实现。
///
/// 契约（P1 离线队列可靠性，2026-10-08）：
/// - load 系列：缺失/损坏降级为空数据，不抛异常；
/// - save 系列：写失败必须抛出异常，由调用方（[OfflineEventQueue]）捕获
///   并装进 [OfflinePersistErrors] 向上层返回失败结果——持久化失败不允许
///   被静默吞掉。
abstract class OfflineEventStore {
  /// 读取全部待上报事件的 JSON 行（按入队顺序）。
  Future<List<String>> loadJsonEntries();

  /// 覆盖保存全部待上报事件（每次入队/清理后调用）。
  ///
  /// 失败时抛出异常（实现方可同时记录内部可观测字段供诊断）。
  Future<void> saveJsonEntries(List<String> entries);

  /// 读取持久化的单调序号水位（R07：未持久化时返回 0）。
  ///
  /// 默认实现为空操作，供不关心水位的实现复用。
  Future<int> loadSeqWatermark() async => 0;

  /// 保存单调序号水位（R07）。
  ///
  /// 水位独立于队列行存储：全部事件确认后队列清空不影响水位，重启后
  /// 新事件继续从已用最大序号递增，不产生重复的 mutation_id/event_id。
  /// 失败时抛出异常。
  Future<void> saveSeqWatermark(int seq) async {}
}

/// 队列行文件与水位文件的写入错误（分别记录，P1）。
///
/// 两类写入失败互不掩盖：队列行写失败时水位仍会尝试写入（反之亦然），
/// 上层据此区分"事件可能未落盘"与"幂等键水位可能回退（重启后有复用
/// 风险，需告警）"。
class OfflinePersistErrors {
  const OfflinePersistErrors({this.queueError, this.seqError});

  /// 队列行文件写失败原因；null 表示写入成功。
  final Object? queueError;

  /// 水位文件写失败原因；null 表示写入成功。
  final Object? seqError;

  bool get isEmpty => queueError == null && seqError == null;

  bool get isNotEmpty => !isEmpty;

  @override
  String toString() =>
      'OfflinePersistErrors(queueError: $queueError, seqError: $seqError)';
}

/// 一次入队的结果（P1：持久化失败如实向上层返回）。
class OfflineEnqueueResult {
  const OfflineEnqueueResult({required this.errors, this.event});

  /// 入队成功并已加入内存队列的事件；null 表示 mutation_id 与待上报
  /// 事件重复被跳过（此时未触发持久化，errors 为空）。
  final LearningEvent? event;

  /// 本次入队触发的持久化写入错误（队列行与水位分别记录）。
  final OfflinePersistErrors errors;
}

/// 内存实现（测试与未接持久化阶段的默认选择）。
class InMemoryOfflineEventStore implements OfflineEventStore {
  final List<String> _entries = <String>[];
  int _seqWatermark = 0;

  @override
  Future<List<String>> loadJsonEntries() async => List<String>.from(_entries);

  @override
  Future<void> saveJsonEntries(List<String> entries) async {
    _entries
      ..clear()
      ..addAll(entries);
  }

  @override
  Future<int> loadSeqWatermark() async => _seqWatermark;

  @override
  Future<void> saveSeqWatermark(int seq) async {
    _seqWatermark = seq;
  }
}

/// 未登录（无 owner）事件使用的命名空间（N03：隔离保留，不自动上传）。
const String kUnownedNamespace = 'unowned';

/// 命名空间安全化：仅保留文件系统/偏好键安全字符，其余替换为 '_'。
///
/// 统一小写：仅大小写差异的用户名归并到同一命名空间，避免 Windows
/// 文件系统大小写不敏感导致两个账号互访对方文件。
String sanitizeNamespace(String namespace) {
  final cleaned = namespace.toLowerCase().replaceAll(
    RegExp(r'[^a-z0-9_\-@.]'),
    '_',
  );
  return cleaned.isEmpty ? kUnownedNamespace : cleaned;
}

/// 文件实现：单 JSON 文件（字符串数组），ADR-006 V1 队列持久化。
///
/// 位置默认取应用支持目录（path_provider），构造可注入目录解析函数以便测试。
/// 损坏降级：文件不存在/不可解析/非数组 → 空队列（事件 append-only，跳过
/// 坏行由 [OfflineEventQueue] 承担），load 系列 IO 异常不外抛。
///
/// R07（审查 2026-10-07）：
/// - 写入原子替换（先写 `<file>.tmp` 再 rename），中途失败不破坏旧文件；
/// - 序号水位存独立文件，不随队列清空而删除。
///
/// P1 可靠性（2026-10-08）：
/// - save 系列写失败分别记录于 [lastQueueWriteError] / [lastSeqWriteError]
///   （成功后清除，供诊断观测），并原样外抛——由 [OfflineEventQueue] 捕获
///   装进 [OfflinePersistErrors] 向上层返回失败结果。
///
/// N03（2026-10-08 第二轮复核）：文件名带账号命名空间后缀
/// （`offline_event_queue_{ns}.json`），按登录账号隔离待上报事件与水位；
/// 历史无后缀文件（升级前的全局队列）不再被读写——未归属数据隔离
/// 保留在磁盘，不自动归给下一个登录用户。
class FileOfflineEventStore implements OfflineEventStore {
  FileOfflineEventStore({
    Future<Directory> Function()? directoryProvider,
    String? fileName,
    String? seqFileName,
    String? namespace,
  }) : fileName =
         fileName ??
         queueFileNameFor(namespace ?? kUnownedNamespace),
       seqFileName = seqFileName ?? seqFileNameFor(namespace ?? kUnownedNamespace),
       _directoryProvider = directoryProvider ?? getApplicationSupportDirectory;

  /// 队列文件名（应用支持目录下，带命名空间后缀）。
  static const String defaultFileName = 'offline_event_queue.json';

  /// 序号水位文件名（R07：独立于队列文件，清空队列不删除）。
  static const String defaultSeqFileName = 'offline_event_seq.json';

  /// 命名空间 → 队列文件名。
  static String queueFileNameFor(String namespace) =>
      'offline_event_queue_${sanitizeNamespace(namespace)}.json';

  /// 命名空间 → 水位文件名。
  static String seqFileNameFor(String namespace) =>
      'offline_event_seq_${sanitizeNamespace(namespace)}.json';

  final Future<Directory> Function() _directoryProvider;
  final String fileName;
  final String seqFileName;

  /// 最近一次队列行文件写失败的原因（成功后清除）；null 表示写入成功。
  Object? lastQueueWriteError;

  /// 最近一次水位文件写失败的原因（成功后清除）；null 表示写入成功。
  Object? lastSeqWriteError;

  int _savedSeq = -1;

  Future<File> _resolveFile(String name) async {
    final directory = await _directoryProvider();
    return File('${directory.path}${Platform.pathSeparator}$name');
  }

  /// 原子替换写入：先写临时文件再 rename 覆盖目标。
  Future<void> _writeAtomically(File file, String contents) async {
    final tmp = File('${file.path}.tmp');
    await file.parent.create(recursive: true);
    await tmp.writeAsString(contents, flush: true);
    await tmp.rename(file.path);
  }

  @override
  Future<List<String>> loadJsonEntries() async {
    try {
      final file = await _resolveFile(fileName);
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
      await _writeAtomically(await _resolveFile(fileName), jsonEncode(entries));
      lastQueueWriteError = null;
    } on Exception catch (error) {
      lastQueueWriteError = error;
      // P1：失败如实外抛，由队列层装进失败结果向上层返回（内存队列仍
      // 有效，下次入队整体覆盖重写，事件不丢失）。
      rethrow;
    }
  }

  @override
  Future<int> loadSeqWatermark() async {
    try {
      final file = await _resolveFile(seqFileName);
      if (!await file.exists()) {
        return 0;
      }
      final decoded = jsonDecode(await file.readAsString());
      return decoded is int && decoded > 0 ? decoded : 0;
    } on Exception {
      // 损坏/不可读 → 0；由待上报事件回填兜底（见 OfflineEventQueue）。
      return 0;
    }
  }

  @override
  Future<void> saveSeqWatermark(int seq) async {
    if (seq == _savedSeq) {
      return; // 未变化不重写（completeBatch 清理后的重复保存）。
    }
    try {
      await _writeAtomically(await _resolveFile(seqFileName), '$seq');
      _savedSeq = seq;
      lastSeqWriteError = null;
    } on Exception catch (error) {
      lastSeqWriteError = error;
      rethrow;
    }
  }
}

/// 离线学习事件队列（ADR-006：本地 append-only 事件、mutation_id 幂等、
/// 网络恢复后按序批量上报，单批 ≤ [maxBatchSize] 对齐契约）。
///
/// mutation_id 生成采用 ADR-006 方案 `{device_id}:{local_seq}`；R07（审查
/// 2026-10-07）：seq 水位独立持久化（[OfflineEventStore.saveSeqWatermark]），
/// 全部事件确认、队列清空并重启后水位不回退，新事件必产新幂等键。
///
/// P1 可靠性（2026-10-08）：
/// - 并发调用共享同一个初始化 Future（[_ensureLoaded]）：首次操作期间
///   并发到达的其他操作等待同一恢复完成，不再出现"恢复中 clear 吞掉
///   并发入队事件"的竞态；
/// - 队列修改（enqueue/completeBatch）经 [_serialized] 互斥链按入链顺序
///   串行执行，修改与持久化不交错，落盘内容与内存最终一致；
/// - 持久化写失败通过 [OfflinePersistErrors] / [OfflineEnqueueResult]
///   如实向上层返回（队列行与水位分别记录），事件不丢（内存仍有效，
///   下次操作整体覆盖重写）。
///
/// N03（2026-10-08 第二轮复核）账号隔离：
/// - 队列绑定账号命名空间 [currentNamespace]（登录用户名归一化；未登录
///   = [kUnownedNamespace]）。切换账号经 [switchOwner] 换用对应命名空间
///   的存储并重新加载——A 退出、B 登录后消费的是 B 命名空间的文件，
///   A 的待上报事件留在 A 的文件中，不会上传到 B 的服务端账号；
/// - mutation_id/event_id 含命名空间段（`{deviceId}:{ns}:{seq}` /
///   `{deviceId}-{ns}-e{seq}`）：各命名空间水位独立，跨账号也不产生
///   重复幂等键（服务端 mutation_id 为全局唯一约束）；
/// - 未登录期间的学习事件入 unowned 命名空间，登录后不自动代上传
///   （隔离保留，避免归给下一个登录用户）。
class OfflineEventQueue {
  OfflineEventQueue({
    required OfflineEventStore store,
    required this.deviceId,
    String? namespace,
    OfflineEventStore Function(String namespace)? storeFactory,
  }) : _store = store,
       _namespace = sanitizeNamespace(namespace ?? kUnownedNamespace),
       _storeFactory = storeFactory;

  /// 契约单批上限（POST /v1/learning/events maxItems 200）。
  static const int maxBatchSize = 200;

  OfflineEventStore _store;
  String _namespace;

  /// 命名空间 → 新存储的工厂（[switchOwner] 换仓用）；null 时仅切换
  /// 内存标签并清空内存待上报列表（测试内存装配的隔离语义）。
  final OfflineEventStore Function(String namespace)? _storeFactory;

  final String deviceId;

  /// 当前账号命名空间（事件上传前的 owner 校验基准）。
  String get currentNamespace => _namespace;

  final List<LearningEvent> _pending = <LearningEvent>[];
  int _seq = 0;

  /// 共享初始化 Future：并发调用（enqueue/nextBatch/completeBatch/load）
  /// 只触发一次存储读取，全部等待同一恢复完成。
  Future<void>? _init;

  /// 操作互斥链尾：修改类操作按调用顺序串行执行。
  Future<void> _tail = Future<void>.value();

  /// 待上报事件数。
  int get pendingCount => _pending.length;

  Future<void> _ensureLoaded() => _init ??= _loadFromStore();

  Future<void> _loadFromStore() async {
    final entries = await _store.loadJsonEntries();
    _pending
      ..clear()
      ..addAll(
        entries.map((String line) => _tryDecodeEvent(line)).whereType<LearningEvent>(),
      );
    // 回填 seq 水位（兜底路径）：扫描本机已入队 mutation_id 取最大序号。
    // R07：独立水位文件优先（清空队列后重启仍不回退），事件回填仅在
    // 水位文件缺失/损坏时提供兜底保护。
    // N03：mutation_id 含命名空间段（`{deviceId}:{ns}:{seq}`），取尾段
    // 数字；兼容旧格式 `{deviceId}:{seq}`。
    final prefix = '$deviceId:';
    for (final event in _pending) {
      if (event.mutationId.startsWith(prefix)) {
        var seqPart = event.mutationId.substring(prefix.length);
        final lastColon = seqPart.lastIndexOf(':');
        if (lastColon >= 0) {
          seqPart = seqPart.substring(lastColon + 1);
        }
        final seq = int.tryParse(seqPart);
        if (seq != null && seq > _seq) {
          _seq = seq;
        }
      }
    }
    final storedWatermark = await _store.loadSeqWatermark();
    if (storedWatermark > _seq) {
      _seq = storedWatermark;
    }
  }

  /// 从持久化恢复队列（懒加载；与并发操作共享同一初始化 Future）。
  Future<void> load() => _ensureLoaded();

  /// N03：切换账号命名空间（登录/登出时由 AuthController 调用）。
  ///
  /// - 命名空间归一化后与当前一致 → no-op；
  /// - 提供了 [storeFactory]（生产文件装配）：构造新命名空间的存储并
  ///   重新加载该命名空间的待上报事件与水位（A 的事件留在 A 的文件）；
  /// - 未提供工厂（测试内存装配）：清空内存待上报列表（旧账号事件
  ///   不再可见，不会混入新账号上传批次），水位保留防幂等键回退。
  Future<void> switchOwner(String? namespace) {
    final target = sanitizeNamespace(namespace ?? kUnownedNamespace);
    return _serialized(() async {
      await _ensureLoaded();
      if (target == _namespace) {
        return;
      }
      _namespace = target;
      final factory = _storeFactory;
      if (factory != null) {
        _store = factory(target);
        _init = null;
        _pending.clear();
        _seq = 0;
        await _ensureLoaded();
      } else {
        _pending.clear();
      }
    });
  }

  /// 入队一个学习事件并立即持久化。
  ///
  /// [mutationId] 缺省时自动生成（`{device_id}:{seq}`）；与队列中待上报事件
  /// 重复时跳过并返回 `event == null`（入队去重）。已上报成功移除后同键
  /// 再次入队不拦，最终幂等由服务端 duplicated 兜底。
  ///
  /// 持久化失败不吞：结果对象的 [OfflineEnqueueResult.errors] 分别携带
  /// 队列行与水位写入错误（事件本身已入内存队列且返回给调用方）。
  Future<OfflineEnqueueResult> enqueue({
    required LearningEventKind kind,
    required String itemId,
    String? mutationId,
    String? occurredAt,
    Map<String, dynamic> payload = const <String, dynamic>{},
  }) {
    return _serialized(() async {
      await _ensureLoaded();
      final effectiveMutationId = mutationId ?? '$deviceId:$_namespace:${_advanceSeq()}';
      for (final event in _pending) {
        if (event.mutationId == effectiveMutationId) {
          return OfflineEnqueueResult(
            event: null,
            errors: const OfflinePersistErrors(),
          );
        }
      }
      final event = LearningEvent(
        eventId: '$deviceId-$_namespace-e${_advanceSeq()}',
        mutationId: effectiveMutationId,
        kind: kind,
        itemId: itemId,
        occurredAt: occurredAt ?? DateTime.now().toUtc().toIso8601String(),
        payload: payload,
      );
      _pending.add(event);
      return OfflineEnqueueResult(event: event, errors: await _persist());
    });
  }

  /// 按入队顺序取下一批待上报事件（≤ [maxCount]，钳制到 [1, maxBatchSize]）。
  ///
  /// 只读不出队：上报成功后调 [completeBatch] 按 accepted/duplicated 清理；
  /// 失败则原样保留重试（mutation_id 不变保证服务端幂等去重）。
  Future<List<LearningEvent>> nextBatch({int maxCount = maxBatchSize}) async {
    await _ensureLoaded();
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
  ///
  /// 返回本次清理触发的持久化写入错误：服务端已确认、但本地落盘失败时，
  /// 重启后会按旧状态恢复并重复上报（由服务端 mutation_id 幂等去重兜底），
  /// 上层应观测该结果。
  Future<OfflinePersistErrors> completeBatch(EventUploadResult result) {
    return _serialized(() async {
      await _ensureLoaded();
      if (_pending.isEmpty) {
        return const OfflinePersistErrors();
      }
      final confirmed = result.confirmedEventIds;
      if (confirmed.isEmpty) {
        return const OfflinePersistErrors();
      }
      _pending.removeWhere((LearningEvent event) => confirmed.contains(event.eventId));
      return _persist();
    });
  }

  /// 修改互斥链：队列修改与持久化按调用入链顺序串行执行；
  /// 前一个操作的失败不阻断后续操作（链尾吞掉错误）。
  Future<T> _serialized<T>(Future<T> Function() action) {
    final run = _tail.then((_) => action());
    _tail = run.then<void>((_) {}, onError: (Object _) {});
    return run;
  }

  int _advanceSeq() => ++_seq;

  Future<OfflinePersistErrors> _persist() async {
    Object? queueError;
    Object? seqError;
    try {
      await _store.saveJsonEntries(
        _pending.map((LearningEvent event) => jsonEncode(event.toJson())).toList(),
      );
    } on Exception catch (error) {
      queueError = error;
    }
    // R07：水位独立持久化，不随队列清空而丢失（幂等键永不复用）；
    // P1：水位写入独立尝试，不被队列行失败掩盖（分别记录）。
    try {
      await _store.saveSeqWatermark(_seq);
    } on Exception catch (error) {
      seqError = error;
    }
    return OfflinePersistErrors(queueError: queueError, seqError: seqError);
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
