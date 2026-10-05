import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/learning_layer.dart';
import 'package:bfs_learn/services/learning_layer_service.dart';

void main() {
  group('LearningLayerData Model Tests', () {
    test('LearningLayerData should parse from JSON correctly', () {
      final json = {
        'audit_time': '2026-06-16',
        'total_items': 3240,
        'frontend_layer_totals': {
          'core': 727,
          'standard': 1264,
          'advanced': 933,
          'optional': 316,
        },
        'suspected_misclassified_core': [
          {
            'id': '2.8.202',
            'name': '凸包维护 DP',
            'section_id': '2.8',
            'current_layer': 'core',
            'suggested_frontend_layer': 'advanced',
            'reason': '名称含高级关键词: 凸包',
          },
        ],
        'overcrowded_section_collapse_policy': [
          {
            'section_id': '3.13',
            'section_name': '高级数据结构扩展',
            'category': '数据结构',
            'total': 374,
            'frontend_core': 46,
            'frontend_standard': 117,
            'frontend_advanced': 158,
            'frontend_optional': 53,
            'foldable_ratio': 0.564,
            'default_collapse_policy': '折叠 advanced+optional',
          },
          {
            'section_id': '4.1',
            'section_name': '整数与数论基础',
            'category': '算法竞赛数学',
            'total': 193,
            'frontend_core': 26,
            'frontend_standard': 140,
            'frontend_advanced': 27,
            'frontend_optional': 0,
            'foldable_ratio': 0.14,
            'default_collapse_policy': '不默认折叠',
          },
        ],
      };

      final data = LearningLayerData.fromJson(json);

      expect(data.auditTime, equals('2026-06-16'));
      expect(data.totalItems, equals(3240));
      expect(data.frontendLayerTotals.core, equals(727));
      expect(data.frontendLayerTotals.standard, equals(1264));
      expect(data.frontendLayerTotals.advanced, equals(933));
      expect(data.frontendLayerTotals.optional, equals(316));
    });

    test(
      'frontendLayerOverrideForItem should return override for misclassified items',
      () {
        final json = {
          'suspected_misclassified_core': [
            {
              'id': '2.8.202',
              'name': '凸包维护 DP',
              'section_id': '2.8',
              'current_layer': 'core',
              'suggested_frontend_layer': 'advanced',
              'reason': '名称含高级关键词: 凸包',
            },
          ],
        };

        final data = LearningLayerData.fromJson(json);

        expect(data.frontendLayerOverrideForItem('2.8.202'), equals('advanced'));
        expect(data.frontendLayerOverrideForItem('2.8.999'), isNull);
      },
    );

    test('collapsePolicyForSection should return correct policy', () {
      final json = {
        'overcrowded_section_collapse_policy': [
          {
            'section_id': '3.13',
            'section_name': '高级数据结构扩展',
            'total': 374,
            'foldable_ratio': 0.564,
            'default_collapse_policy': '折叠 advanced+optional',
          },
          {
            'section_id': '4.1',
            'section_name': '整数与数论基础',
            'total': 193,
            'foldable_ratio': 0.14,
            'default_collapse_policy': '不默认折叠',
          },
        ],
      };

      final data = LearningLayerData.fromJson(json);

      final policy313 = data.collapsePolicyForSection('3.13');
      expect(policy313, isNotNull);
      expect(policy313!.sectionName, equals('高级数据结构扩展'));
      expect(policy313.shouldCollapseAdvanced, isTrue);
      expect(policy313.shouldCollapseOptional, isTrue);

      final policy41 = data.collapsePolicyForSection('4.1');
      expect(policy41, isNotNull);
      expect(policy41!.shouldCollapseAdvanced, isFalse);
      expect(policy41.shouldCollapseOptional, isFalse);

      final policy999 = data.collapsePolicyForSection('9.9');
      expect(policy999, isNull);
    });

    test('Should handle empty/malformed JSON gracefully', () {
      final data = LearningLayerData.fromJson({});

      expect(data.auditTime, isEmpty);
      expect(data.totalItems, equals(0));
      expect(data.frontendLayerTotals.core, equals(0));
      expect(data.suspectedMisclassifiedCore, isEmpty);
      expect(data.overcrowdedSectionCollapsePolicy, isEmpty);
      expect(data.frontendLayerOverrideForItem('any'), isNull);
      expect(data.collapsePolicyForSection('any'), isNull);
    });
  });

  group('SectionCollapsePolicy Tests', () {
    test('shouldCollapseAdvanced and shouldCollapseOptional work correctly', () {
      final collapseBoth = SectionCollapsePolicy.fromJson({
        'section_id': '3.13',
        'default_collapse_policy': '折叠 advanced+optional',
      });
      expect(collapseBoth.shouldCollapseAdvanced, isTrue);
      expect(collapseBoth.shouldCollapseOptional, isTrue);

      final collapseOptionalOnly = SectionCollapsePolicy.fromJson({
        'section_id': '2.9',
        'default_collapse_policy': '折叠 optional',
      });
      expect(collapseOptionalOnly.shouldCollapseAdvanced, isFalse);
      expect(collapseOptionalOnly.shouldCollapseOptional, isTrue);

      final noCollapse = SectionCollapsePolicy.fromJson({
        'section_id': '4.1',
        'default_collapse_policy': '不默认折叠',
      });
      expect(noCollapse.shouldCollapseAdvanced, isFalse);
      expect(noCollapse.shouldCollapseOptional, isFalse);
    });
  });

  group('Real Asset Loading Tests', () {
    setUp(() {
      TestWidgetsFlutterBinding.ensureInitialized();
    });

    test('LearningLayerService should load real JSON data', () async {
      final service = LearningLayerService();

      // 加载真实分层数据
      final data = await service.loadLayerData();

      // 应该成功加载
      expect(data.totalItems, equals(3240));
      expect(data.frontendLayerTotals.core, equals(727));
      expect(data.frontendLayerTotals.standard, equals(1264));
      expect(data.frontendLayerTotals.advanced, equals(933));
      expect(data.frontendLayerTotals.optional, equals(316));
    });

    test('getCollapsePolicy for 3.13 should fold advanced+optional', () async {
      final service = LearningLayerService();
      final policy = await service.getCollapsePolicy('3.13');

      expect(policy, isNotNull);
      expect(policy!.shouldCollapseAdvanced, isTrue);
      expect(policy.shouldCollapseOptional, isTrue);
    });

    test('getCollapsePolicy for 4.1 should not fold', () async {
      final service = LearningLayerService();
      final policy = await service.getCollapsePolicy('4.1');

      expect(policy, isNotNull);
      expect(policy!.shouldCollapseAdvanced, isFalse);
      expect(policy.shouldCollapseOptional, isFalse);
    });

    test('getFrontendLayerForItem should return override for 2.8.202', () async {
      final service = LearningLayerService();
      final layer = await service.getFrontendLayerForItem('2.8.202');

      // 2.8.202 在 suspected_misclassified_core 中，应返回 advanced
      expect(layer, equals('advanced'));
    });
  });
}
