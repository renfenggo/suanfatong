import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:bfs_learn/app/app.dart';

void main() {
  testWidgets('App renders home page title', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: BfsApp()));
    await tester.pump(const Duration(milliseconds: 500));

    expect(find.text('算法通'), findsWidgets);
  });
}
