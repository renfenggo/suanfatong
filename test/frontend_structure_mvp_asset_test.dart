import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Frontend Structure MVP Asset Loading', () {
    test('rootBundle should load learning card samples', () async {
      final jsonString = await rootBundle.loadString(
        'data/learning_card_samples.json',
      );
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      final samples = jsonData['samples'] as Map<String, dynamic>;

      expect(samples.containsKey('2.8'), isTrue);
      expect(samples.containsKey('3.13'), isTrue);
      expect(samples.containsKey('4.1'), isTrue);
    });

    test('rootBundle should load learning path report data', () async {
      final jsonString = await rootBundle.loadString(
        'data/learning_path_report_data.json',
      );
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;

      expect(jsonData.isNotEmpty, isTrue);
    });

    test('rootBundle should load learning layer review data', () async {
      final jsonString = await rootBundle.loadString(
        'data/learning_path_layers_frontend_usage_review.json',
      );
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;

      expect(jsonData.isNotEmpty, isTrue);
    });

    test('rootBundle should load practice entry MVP index', () async {
      final jsonString = await rootBundle.loadString(
        'data/practice_entry_mvp_index.json',
      );
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      final index = jsonData['index'] as List<dynamic>;

      expect(index.isNotEmpty, isTrue);
    });

    test('rootBundle should load C++14 template MVP index', () async {
      final jsonString = await rootBundle.loadString(
        'data/cpp14_template_mvp_index.json',
      );
      final jsonData = json.decode(jsonString) as Map<String, dynamic>;
      final index = jsonData['index'] as List<dynamic>;
      final dfs = index.cast<Map<String, dynamic>>().firstWhere(
        (entry) => entry['item_id'] == '2.7.16',
      );

      expect(dfs['title'], 'DFS 模板');
      expect(dfs['code_reference'], isA<Map<String, dynamic>>());
    });

    test('rootBundle should load animation manifest and DFS animation', () async {
      final manifestString = await rootBundle.loadString(
        'assets/data/cpp/animations/cpp_animation_manifest.json',
      );
      final manifest = json.decode(manifestString) as Map<String, dynamic>;
      final animations = manifest['animations'] as List<dynamic>;

      final dfs = animations.cast<Map<String, dynamic>>().firstWhere(
        (entry) => entry['itemId'] == '2.7.16',
      );
      expect(dfs['animationId'], 'cpp_dfs_graph_traversal');

      final animationString = await rootBundle.loadString(
        dfs['assetPath'] as String,
      );
      final animation = json.decode(animationString) as Map<String, dynamic>;
      expect(animation['animationId'], 'cpp_dfs_graph_traversal');
      expect(animation['itemId'], '2.7.16');
    });
  });
}
