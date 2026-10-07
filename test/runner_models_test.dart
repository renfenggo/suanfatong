import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/models/runner_models.dart';

/// Runner 契约模型测试（对齐 contracts/runner/runner.schema.json）。
void main() {
  group('ResourceLimits', () {
    test('toJson 为 snake_case 契约字段名', () {
      final json = const ResourceLimits(
        wallClockMs: 5000,
        cpuMs: 4000,
        memoryMb: 128,
        processCount: 4,
        outputBytes: 32768,
        fileBytes: 2048,
      ).toJson();
      expect(json, const <String, dynamic>{
        'wall_clock_ms': 5000,
        'cpu_ms': 4000,
        'memory_mb': 128,
        'process_count': 4,
        'output_bytes': 32768,
        'file_bytes': 2048,
      });
    });
  });

  group('RunnerLanguage', () {
    test('fromWireName 大小写容错且未知值返回 null', () {
      expect(RunnerLanguage.fromWireName('cpp14'), RunnerLanguage.cpp14);
      expect(RunnerLanguage.fromWireName('CPP17'), RunnerLanguage.cpp17);
      expect(RunnerLanguage.fromWireName(null), isNull);
      expect(RunnerLanguage.fromWireName('python'), isNull);
    });
  });

  group('RunnerStatus', () {
    test('fromWireName 解析大写下划线契约线名', () {
      expect(RunnerStatus.fromWireName('RUN_OK'), RunnerStatus.runOk);
      expect(RunnerStatus.fromWireName('COMPILE_FAILED'),
          RunnerStatus.compileFailed);
      expect(RunnerStatus.fromWireName('RUN_TIMEOUT'), RunnerStatus.runTimeout);
      expect(RunnerStatus.fromWireName('RESOURCE_LIMIT'),
          RunnerStatus.resourceLimit);
      expect(
          RunnerStatus.fromWireName('INTERNAL_ERROR'),
          RunnerStatus
              .internalError); // ignore: avoid_redundant_argument_values
      expect(RunnerStatus.fromWireName('REJECTED'), RunnerStatus.rejected);
    });

    test('未知状态归 unknown，displayName 为中文', () {
      expect(RunnerStatus.fromWireName('SOMETHING_NEW'), RunnerStatus.unknown);
      expect(RunnerStatus.fromWireName(null), RunnerStatus.unknown);
      expect(RunnerStatus.runOk.displayName, '运行成功');
      expect(RunnerStatus.compileFailed.displayName, '编译失败');
      expect(RunnerStatus.runTimeout.displayName, '超时终止');
      expect(RunnerStatus.resourceLimit.displayName, '超出资源限制');
    });
  });

  group('RunnerResult.fromJson', () {
    test('契约样本全字段解析', () {
      // 与 winknow RunnerJson 输出一致的样本（snake_case + 大写状态）
      final json = jsonDecode('''
      {
        "request_id": "wb-1",
        "status": "RUN_OK",
        "compile_exit_code": 0,
        "compile_diagnostics": "",
        "run_exit_code": 0,
        "stdout": "你好，算法通！",
        "stderr": "",
        "elapsed_ms": 152,
        "peak_memory_kb": 3072,
        "timed_out": false,
        "output_truncated": false,
        "artifacts_cleaned": true,
        "trace_id": "t-9"
      }
      ''') as Map<String, dynamic>;

      final result = RunnerResult.fromJson(json);
      expect(result.requestId, 'wb-1');
      expect(result.status, RunnerStatus.runOk);
      expect(result.compileExitCode, 0);
      expect(result.runExitCode, 0);
      expect(result.stdout, '你好，算法通！');
      expect(result.elapsedMs, 152);
      expect(result.peakMemoryKb, 3072);
      expect(result.artifactsCleaned, isTrue);
      expect(result.traceId, 't-9');
    });

    test('缺省字段安全降级（新客户端读旧响应不崩）', () {
      final result = RunnerResult.fromJson(const <String, dynamic>{
        'request_id': 'wb-2',
        'status': 'RUN_TIMEOUT',
      });
      expect(result.status, RunnerStatus.runTimeout);
      expect(result.elapsedMs, 0);
      expect(result.timedOut, isFalse);
      expect(result.artifactsCleaned, isFalse);
      expect(result.stdout, isNull);
      expect(result.peakMemoryKb, isNull);
    });
  });

  group('RunnerCapabilities.fromJson', () {
    test('解析能力快照并过滤未知语言', () {
      final caps = RunnerCapabilities.fromJson(<String, dynamic>{
        'component': 'code_runner',
        'available': true,
        'compiler_path': r'C:\Dev-Cpp\MinGW64\bin\g++.exe',
        'compiler_version': 'g++ (tdm-1) 4.9.2',
        'languages': <dynamic>['cpp14', 'cpp20', 'CPP17'],
      });
      expect(caps.component, 'code_runner');
      expect(caps.available, isTrue);
      expect(caps.compilerVersion, contains('4.9.2'));
      expect(caps.languages,
          const [RunnerLanguage.cpp14, RunnerLanguage.cpp17]);
    });

    test('缺省字段默认不可用', () {
      final caps = RunnerCapabilities.fromJson(const <String, dynamic>{});
      expect(caps.available, isFalse);
      expect(caps.languages, isEmpty);
      expect(caps.component, 'code_runner');
    });
  });
}
