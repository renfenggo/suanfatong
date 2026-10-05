import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Mojibake prevention', () {
    final mojibakeFragments = [
      '绠楁硶',
      '鐭ヨ瘑',
      '瀛︿範',
      '椤甸潰',
      '鍔犺浇',
      '寮€濮',
      '缁х画',
      '娴忚',
      '鎼滅储',
      '璁剧疆',
      '涓婃',
      '澶辫触',
    ];

    final directories = ['lib/app', 'lib/pages'];

    List<File> collectDartFiles() {
      final files = <File>[];
      for (final dir in directories) {
        final directory = Directory(dir);
        if (directory.existsSync()) {
          files.addAll(
            directory
                .listSync(recursive: true)
                .whereType<File>()
                .where((f) => f.path.endsWith('.dart')),
          );
        }
      }
      return files;
    }

    test('lib/app and lib/pages Dart files contain no mojibake fragments', () {
      final files = collectDartFiles();
      final violations = <String>[];

      for (final file in files) {
        final content = file.readAsStringSync(encoding: utf8);
        for (final fragment in mojibakeFragments) {
          if (content.contains(fragment)) {
            final idx = content.indexOf(fragment);
            final start = idx > 30 ? idx - 30 : 0;
            final end =
                idx + fragment.length + 30 < content.length
                    ? idx + fragment.length + 30
                    : content.length;
            final context = content.substring(start, end);
            violations.add(
              '${file.path}: found mojibake "$fragment" near "...$context..."',
            );
          }
        }
      }

      expect(violations, isEmpty, reason: violations.take(20).join('\n'));
    });

    test('pubspec.yaml has no mojibake and correct description', () {
      final content = File('pubspec.yaml').readAsStringSync(encoding: utf8);
      for (final fragment in mojibakeFragments) {
        expect(content, isNot(contains(fragment)));
      }
      expect(content, contains('算法通离线学习 App'));
    });

    test('android strings.xml is valid XML with correct app_name', () {
      final content = File(
        'android/app/src/main/res/values/strings.xml',
      ).readAsStringSync(encoding: utf8);
      for (final fragment in mojibakeFragments) {
        expect(content, isNot(contains(fragment)));
      }
      expect(content, contains('<string name="app_name">算法通</string>'));
    });

    test('web manifest.json is valid JSON with correct name', () {
      final raw = File('web/manifest.json').readAsStringSync(encoding: utf8);
      for (final fragment in mojibakeFragments) {
        expect(raw, isNot(contains(fragment)));
      }
      final json = jsonDecode(raw) as Map<String, dynamic>;
      expect(json['name'], '算法通');
      expect(json['short_name'], '算法通');
      expect(json['description'], '算法通离线学习 App');
    });

    test('key UI Chinese strings exist in app.dart', () {
      final content = File('lib/app/app.dart').readAsStringSync(encoding: utf8);
      expect(content, contains('算法通'));
    });

    test('key UI Chinese strings exist in home_page.dart', () {
      final content = File(
        'lib/pages/home_page.dart',
      ).readAsStringSync(encoding: utf8);
      expect(content, contains('算法通'));
      expect(content, contains('学习入口'));
      expect(content, contains('知识地图'));
      expect(content, contains('搜索知识点'));
      expect(content, contains('学习进度'));
      expect(content, contains('设置'));
      expect(content, contains('开始学习'));
      expect(content, contains('继续学习'));
    });

    test('key UI Chinese strings exist in app_router.dart', () {
      final content = File(
        'lib/app/app_router.dart',
      ).readAsStringSync(encoding: utf8);
      expect(content, contains('页面未找到'));
    });

    test('key UI Chinese strings exist in cpp_learning_unit_page.dart', () {
      final content = File(
        'lib/pages/cpp_learning_unit_page.dart',
      ).readAsStringSync(encoding: utf8);
      expect(content, contains('学习目标'));
      expect(content, contains('讲解'));
      expect(content, contains('示例代码'));
      expect(content, contains('常见错误'));
      expect(content, contains('练习'));
      expect(content, contains('下一个知识点'));
    });

    test('widget_test.dart asserts correct Chinese title', () {
      final content = File(
        'test/widget_test.dart',
      ).readAsStringSync(encoding: utf8);
      expect(content, contains('算法通'));
      for (final fragment in mojibakeFragments) {
        expect(content, isNot(contains(fragment)));
      }
    });
  });
}
