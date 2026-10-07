import 'dart:async';
import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';

import 'package:bfs_learn/services/desktop_bridge_client.dart';

/// DesktopBridge 行协议客户端测试（Fake 进程，不触真实文件系统）。
void main() {
  group('DesktopBridgeClient', () {
    test('请求行为契约 JSON：id/method/params/trace_id，且 id 自增', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      final future = client.invoke('runner.get_capabilities',
          const <String, dynamic>{'x': 1},
          traceId: 't-1');
      await Future<void>.delayed(Duration.zero);
      await Future<void>.delayed(Duration.zero);

      expect(fake.writtenLines, hasLength(1));
      final request = jsonDecode(fake.writtenLines.single)
          as Map<String, dynamic>;
      expect(request['id'], 1);
      expect(request['method'], 'runner.get_capabilities');
      expect(request['params'], <String, dynamic>{'x': 1});
      expect(request['trace_id'], 't-1');

      fake.respond('{"id":1,"ok":true,"result":{"available":true}}');
      final result = await future;
      expect(result['available'], isTrue);

      // 第二次请求复用进程且 id 递增
      final second = client.invoke('runner.execute', null);
      await Future<void>.delayed(Duration.zero);
      await Future<void>.delayed(Duration.zero);
      expect(fake.writtenLines, hasLength(2));
      expect((jsonDecode(fake.writtenLines[1])
          as Map<String, dynamic>)['id'], 2);
      expect(fake.startCount, 1, reason: '进程必须跨请求复用');
      fake.respond('{"id":2,"ok":true,"result":{"status":"RUN_OK"}}');
      expect((await second)['status'], 'RUN_OK');

      await client.dispose();
    });

    test('并发请求乱序响应按 id 关联', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      final first = client.invoke('m.a', null);
      final second = client.invoke('m.b', null);
      await Future<void>.delayed(Duration.zero);

      // 先回第二个请求的响应
      fake.respond('{"id":2,"ok":true,"result":{"who":"b"}}');
      fake.respond('{"id":1,"ok":true,"result":{"who":"a"}}');

      expect((await first)['who'], 'a');
      expect((await second)['who'], 'b');
      await client.dispose();
    });

    test('ok=false 抛 BridgeRemoteException 携带错误码', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      final future = client.invoke('runner.execute', null);
      await Future<void>.delayed(Duration.zero);
      fake.respond(
          '{"id":1,"ok":false,"error":{"code":"UNAVAILABLE","message":"runner 未就绪"}}');

      await expectLater(future,
          throwsA(isA<BridgeRemoteException>().having((e) => e.code, 'code',
              'UNAVAILABLE').having((e) => e.message, 'message', 'runner 未就绪')));
      await client.dispose();
    });

    test('候选路径全部失败抛 BridgeUnavailableException', () async {
      final client = DesktopBridgeClient(
        launcher: _NeverStartLauncher(),
        candidateExecutables: const <String>[r'C:\no\a.exe', r'C:\no\b.exe'],
      );
      await expectLater(
        client.invoke('system.get_status', null),
        throwsA(isA<BridgeUnavailableException>()),
      );
    });

    test('超时抛 TimeoutException 且连接保留可继续用', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      // 不回响应 → 超时
      await expectLater(
        client.invoke('slow.method', null, timeout: const Duration(milliseconds: 20)),
        throwsA(isA<TimeoutException>()),
      );

      // 同一进程后续请求仍可用
      final next = client.invoke('fast.method', null);
      await Future<void>.delayed(Duration.zero);
      expect(fake.startCount, 1, reason: '超时不杀进程');
      fake.respond('{"id":2,"ok":true,"result":{"ok":1}}');
      expect((await next)['ok'], 1);
      await client.dispose();
    });

    test('进程退出后 pending 请求以 BridgeDisconnectedException 失败', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      final pending = client.invoke('runner.execute', null);
      await Future<void>.delayed(Duration.zero);

      fake.terminate(); // stdout 关闭（进程退出）
      await expectLater(
          pending, throwsA(isA<BridgeDisconnectedException>()));
      await client.dispose();
    });

    test('dispose 后调用抛 BridgeUnavailableException', () async {
      final fake = _FakeProcess();
      final client = DesktopBridgeClient(launcher: _FakeLauncher(fake));

      // 先完成一次调用让进程启动（dispose 只清理已启动的连接）
      final first = client.invoke('any', null);
      await Future<void>.delayed(Duration.zero);
      fake.respond('{"id":1,"ok":true,"result":{}}');
      await first;

      await client.dispose();
      expect(fake.closed, isTrue, reason: 'dispose 应关闭 stdin 触发桥接 EOF');
      await expectLater(
        client.invoke('any', null),
        throwsA(isA<BridgeUnavailableException>()),
      );
    });
  });
}

/// Fake 桥接进程：记录写出的请求行，测试手动注入响应行。
class _FakeProcess implements BridgeProcess {
  final StreamController<String> _stdout =
      StreamController<String>.broadcast();
  final StreamController<String> _stderr =
      StreamController<String>.broadcast();
  final List<String> writtenLines = <String>[];
  int startCount = 0;
  bool closed = false;
  bool killed = false;

  void respond(String line) => _stdout.add(line);

  /// 模拟进程退出（stdout 流关闭）。
  void terminate() {
    _stdout.close();
    _stderr.close();
  }

  @override
  Stream<String> get stdoutLines => _stdout.stream;

  @override
  Stream<String> get stderrLines => _stderr.stream;

  @override
  Future<void> writeLine(String line) async {
    writtenLines.add(line);
  }

  @override
  Future<void> close() async {
    closed = true;
  }

  @override
  Future<void> kill() async {
    killed = true;
  }
}

class _FakeLauncher implements BridgeProcessLauncher {
  _FakeLauncher(this.process);

  final _FakeProcess process;

  @override
  Future<BridgeProcess?> tryStart(String executable) async {
    process.startCount++;
    return process;
  }
}

class _NeverStartLauncher implements BridgeProcessLauncher {
  @override
  Future<BridgeProcess?> tryStart(String executable) async => null;
}
