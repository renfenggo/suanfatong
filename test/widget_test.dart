import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:bfs_learn/app/app.dart';

void main() {
  testWidgets('App renders home page title', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: BfsApp()));
    await tester.pumpAndSettle();

    expect(find.text('BFS 专题学习'), findsOneWidget);
    expect(find.text('BFS 知识讲解'), findsOneWidget);
  });
}
