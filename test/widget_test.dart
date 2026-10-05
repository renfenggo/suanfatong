import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:bfs_learn/app/app.dart';

void main() {
  setUp(() {
    // 桌面 Shell（StatefulShellRoute.indexedStack）会预建全部分支根页面，
    // 包括设置页（读取 SharedPreferences 与 PackageInfo），测试环境需 mock。
    SharedPreferences.setMockInitialValues({});
    PackageInfo.setMockInitialValues(
      appName: '算法通',
      packageName: 'com.winknow.suanfatong',
      version: '1.0.0',
      buildNumber: '1',
      buildSignature: '',
    );
  });

  testWidgets('App renders home page title', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: BfsApp()));
    await tester.pump(const Duration(milliseconds: 500));

    expect(find.text('算法通'), findsWidgets);
  });
}
