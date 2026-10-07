/// Runner 契约模型（contracts/runner/runner.schema.json 对齐）。
///
/// 线格式：字段 snake_case；语言 `cpp14`/`cpp17`；状态为大写下划线
/// （`RUN_OK` 等，见 winknow RunnerJson.UpperSnakeCaseNamingPolicy）。
library;

/// 资源限制（契约 $defs/ResourceLimits，全部字段必填且带范围）。
class ResourceLimits {
  const ResourceLimits({
    this.wallClockMs = 10000,
    this.cpuMs = 8000,
    this.memoryMb = 256,
    this.processCount = 8,
    this.outputBytes = 65536,
    this.fileBytes = 1024,
  });

  /// 墙钟超时（毫秒，契约范围 [100, 60000]）。
  final int wallClockMs;

  /// CPU 时间上限（毫秒，契约范围 [100, 60000]）。
  final int cpuMs;

  /// 内存上限（MB，契约范围 [16, 512]）。
  final int memoryMb;

  /// 进程数上限（含子进程，契约范围 [1, 8]）。
  final int processCount;

  /// 输出字节上限（stdout+stderr 合计，契约范围 [1024, 1048576]）。
  final int outputBytes;

  /// 单文件写入字节上限（契约范围 [1024, 10485760]）。
  final int fileBytes;

  Map<String, dynamic> toJson() => <String, dynamic>{
    'wall_clock_ms': wallClockMs,
    'cpu_ms': cpuMs,
    'memory_mb': memoryMb,
    'process_count': processCount,
    'output_bytes': outputBytes,
    'file_bytes': fileBytes,
  };
}

/// 源语言（契约线名 cpp14/cpp17）。
enum RunnerLanguage {
  cpp14('cpp14'),
  cpp17('cpp17');

  const RunnerLanguage(this.wireName);

  /// 契约线名。
  final String wireName;

  /// 解析契约线名；未知值返回 null（兼容性：枚举只增不改）。
  static RunnerLanguage? fromWireName(String? wireName) {
    switch (wireName?.toLowerCase()) {
      case 'cpp14':
        return RunnerLanguage.cpp14;
      case 'cpp17':
        return RunnerLanguage.cpp17;
      default:
        return null;
    }
  }
}

/// 执行状态（契约 $defs/RunnerStatus；兼容性：枚举只增不改）。
enum RunnerStatus {
  compiledOk,
  compileFailed,
  runOk,
  runFailed,
  runTimeout,
  resourceLimit,
  internalError,
  rejected,
  unknown;

  /// 解析契约状态线名（大写下划线，如 RUN_OK）；未知值归 unknown。
  static RunnerStatus fromWireName(String? wireName) {
    switch (wireName?.toUpperCase()) {
      case 'COMPILED_OK':
        return RunnerStatus.compiledOk;
      case 'COMPILE_FAILED':
        return RunnerStatus.compileFailed;
      case 'RUN_OK':
        return RunnerStatus.runOk;
      case 'RUN_FAILED':
        return RunnerStatus.runFailed;
      case 'RUN_TIMEOUT':
        return RunnerStatus.runTimeout;
      case 'RESOURCE_LIMIT':
        return RunnerStatus.resourceLimit;
      case 'INTERNAL_ERROR':
        return RunnerStatus.internalError;
      case 'REJECTED':
        return RunnerStatus.rejected;
      default:
        return RunnerStatus.unknown;
    }
  }

  /// 中文显示名（工作台状态行）。
  String get displayName {
    switch (this) {
      case RunnerStatus.compiledOk:
        return '编译成功';
      case RunnerStatus.compileFailed:
        return '编译失败';
      case RunnerStatus.runOk:
        return '运行成功';
      case RunnerStatus.runFailed:
        return '运行失败';
      case RunnerStatus.runTimeout:
        return '超时终止';
      case RunnerStatus.resourceLimit:
        return '超出资源限制';
      case RunnerStatus.internalError:
        return '运行器内部错误';
      case RunnerStatus.rejected:
        return '请求被拒绝';
      case RunnerStatus.unknown:
        return '未知状态';
    }
  }
}

/// 执行结果（契约 $defs/RunnerResult）。
class RunnerResult {
  const RunnerResult({
    required this.requestId,
    required this.status,
    required this.elapsedMs,
    required this.timedOut,
    required this.outputTruncated,
    required this.artifactsCleaned,
    this.compileExitCode,
    this.compileDiagnostics,
    this.runExitCode,
    this.stdout,
    this.stderr,
    this.peakMemoryKb,
    this.traceId,
  });

  /// 请求标识（回带）。
  final String requestId;

  /// 执行状态。
  final RunnerStatus status;

  /// 编译退出码（未到编译阶段为 null）。
  final int? compileExitCode;

  /// 编译诊断输出（≤ 64KB，超出截断）。
  final String? compileDiagnostics;

  /// 运行退出码（未到运行阶段为 null）。
  final int? runExitCode;

  /// 标准输出（≤ 1MB，超出截断）。
  final String? stdout;

  /// 标准错误（≤ 256KB，超出截断）。
  final String? stderr;

  /// 端到端耗时（毫秒）。
  final int elapsedMs;

  /// 峰值内存（KB，来自 Job Object 记账）。
  final int? peakMemoryKb;

  /// 是否发生超时终止。
  final bool timedOut;

  /// 输出是否被截断。
  final bool outputTruncated;

  /// 工作目录与产物是否已清理。
  final bool artifactsCleaned;

  /// 可选链路追踪 ID（回带）。
  final String? traceId;

  /// 解析契约 JSON（snake_case）。
  factory RunnerResult.fromJson(Map<String, dynamic> json) {
    return RunnerResult(
      requestId: json['request_id'] as String? ?? '',
      status: RunnerStatus.fromWireName(json['status'] as String?),
      compileExitCode: json['compile_exit_code'] as int?,
      compileDiagnostics: json['compile_diagnostics'] as String?,
      runExitCode: json['run_exit_code'] as int?,
      stdout: json['stdout'] as String?,
      stderr: json['stderr'] as String?,
      elapsedMs: json['elapsed_ms'] as int? ?? 0,
      peakMemoryKb: json['peak_memory_kb'] as int?,
      timedOut: json['timed_out'] as bool? ?? false,
      outputTruncated: json['output_truncated'] as bool? ?? false,
      artifactsCleaned: json['artifacts_cleaned'] as bool? ?? false,
      traceId: json['trace_id'] as String?,
    );
  }
}

/// Runner 能力快照（IPC runner.get_capabilities 响应结果）。
class RunnerCapabilities {
  const RunnerCapabilities({
    required this.available,
    this.component = 'code_runner',
    this.compilerPath,
    this.compilerVersion,
    this.languages = const [],
  });

  /// 组件名（恒 code_runner）。
  final String component;

  /// 工具链是否可用（g++ 探测成功）。
  final bool available;

  /// 编译器完整路径（不可用为 null）。
  final String? compilerPath;

  /// 编译器版本描述（不可用为 null）。
  final String? compilerVersion;

  /// 支持的语言列表（cpp14/cpp17 子集）。
  final List<RunnerLanguage> languages;

  /// 解析契约 JSON（snake_case）。
  factory RunnerCapabilities.fromJson(Map<String, dynamic> json) {
    return RunnerCapabilities(
      component: json['component'] as String? ?? 'code_runner',
      available: json['available'] as bool? ?? false,
      compilerPath: json['compiler_path'] as String?,
      compilerVersion: json['compiler_version'] as String?,
      languages:
          (json['languages'] as List<dynamic>? ?? const <dynamic>[])
              .map((dynamic e) => RunnerLanguage.fromWireName(e as String?))
              .whereType<RunnerLanguage>()
              .toList(),
    );
  }
}
