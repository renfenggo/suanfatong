import 'package:flutter_test/flutter_test.dart';
import 'package:bfs_learn/models/learning_path.dart';
import 'package:bfs_learn/services/learning_path_service.dart';

void main() {
  group('LearningPath Model Tests', () {
    test('LearningPath should create from JSON correctly', () {
      // 模拟2.8章节的JSON数据
      final json = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': [
          '2.8.207',
          '2.8.217',
          '2.8.204',
          '2.8.206',
          '2.8.203',
          '2.8.213',
          '2.8.214',
          '2.8.216',
          '2.8.202',
          '2.8.205'
        ],
        'beginner_description': '包含10个知识点',
        'intermediate_path': [
          '2.8.218',
          '2.8.208',
          '2.8.266',
          '2.8.286',
          '2.8.291',
          '2.8.296',
          '2.8.256',
          '2.8.7',
          '2.8.12',
          '2.8.67',
          '2.8.68',
          '2.8.69',
          '2.8.70',
          '2.8.102',
          '2.8.121'
        ],
        'intermediate_description': '包含15个知识点',
        'advanced_path': [
          '2.8.157',
          '2.8.147',
          '2.8.198',
          '2.8.187',
          '2.8.196',
          '2.8.189',
          '2.8.160',
          '2.8.158',
          '2.8.159',
          '2.8.134',
          '2.8.188',
          '2.8.161',
          '2.8.186',
          '2.8.36',
          '2.8.1'
        ],
        'advanced_description': '包含15个知识点',
        'cross_section_prerequisites': [
          {
            'id': '1.3.10',
            'name': '变量定义',
            'level': 'L1',
            'reference_count': 40,
            'reason': '重要前置节点'
          }
        ]
      };

      final learningPath = LearningPath.fromJson(json);

      expect(learningPath.sectionId, equals('2.8'));
      expect(learningPath.sectionName, equals('动态规划'));
      expect(learningPath.beginnerPath.length, equals(10));
      expect(learningPath.intermediatePath.length, equals(15));
      expect(learningPath.advancedPath.length, equals(15));
      expect(learningPath.crossSectionPrerequisites.length, equals(1));
    });

    test('CrossSectionPrerequisite should create from JSON correctly', () {
      final json = {
        'id': '1.3.10',
        'name': '变量定义',
        'level': 'L1',
        'reference_count': 40,
        'reason': '重要前置节点'
      };

      final prereq = CrossSectionPrerequisite.fromJson(json);

      expect(prereq.id, equals('1.3.10'));
      expect(prereq.name, equals('变量定义'));
      expect(prereq.level, equals('L1'));
      expect(prereq.referenceCount, equals(40));
      expect(prereq.reason, equals('重要前置节点'));
    });

    test('LearningPath should calculate path statistics correctly', () {
      final json = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207', '2.8.217', '2.8.204'],
        'intermediate_path': ['2.8.218', '2.8.208', '2.8.266', '2.8.286', '2.8.291'],
        'advanced_path': ['2.8.157', '2.8.147'],
        'cross_section_prerequisites': [
          {'id': '1.3.10', 'name': '变量定义', 'reference_count': 40, 'reason': '重要前置节点'}
        ]
      };

      final learningPath = LearningPath.fromJson(json);
      final statistics = learningPath.getPathStatistics();

      expect(statistics['beginner'], equals(3));
      expect(statistics['intermediate'], equals(5));
      expect(statistics['advanced'], equals(2));
      expect(statistics['crossSection'], equals(1));
      expect(statistics['total'], equals(11)); // 3 + 5 + 2 + 1 = 11
    });

    test('LearningPath should detect if has path data', () {
      // 有路径数据的情况
      final jsonWithPath = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207'],
        'cross_section_prerequisites': []
      };
      final pathWithData = LearningPath.fromJson(jsonWithPath);
      expect(pathWithData.hasPathData(), isTrue);

      // 无路径数据的情况
      final jsonWithoutPath = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': [],
        'intermediate_path': [],
        'advanced_path': [],
        'cross_section_prerequisites': []
      };
      final pathWithoutData = LearningPath.fromJson(jsonWithoutPath);
      expect(pathWithoutData.hasPathData(), isFalse);
    });

    test('LearningPath should detect cross section prerequisites', () {
      final jsonWithPrereqs = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207'],
        'cross_section_prerequisites': [
          {'id': '1.3.10', 'name': '变量定义', 'reference_count': 40, 'reason': '重要前置节点'}
        ]
      };
      final pathWithPrereqs = LearningPath.fromJson(jsonWithPrereqs);
      expect(pathWithPrereqs.hasCrossSectionPrerequisites(), isTrue);

      final jsonWithoutPrereqs = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207'],
        'cross_section_prerequisites': []
      };
      final pathWithoutPrereqs = LearningPath.fromJson(jsonWithoutPrereqs);
      expect(pathWithoutPrereqs.hasCrossSectionPrerequisites(), isFalse);
    });

    test('LearningPath should handle missing fields gracefully', () {
      final incompleteJson = {
        'section_id': '2.8',
        'section_name': '动态规划',
      };

      final learningPath = LearningPath.fromJson(incompleteJson);

      expect(learningPath.sectionId, equals('2.8'));
      expect(learningPath.sectionName, equals('动态规划'));
      expect(learningPath.beginnerPath, isEmpty);
      expect(learningPath.intermediatePath, isEmpty);
      expect(learningPath.advancedPath, isEmpty);
      expect(learningPath.crossSectionPrerequisites, isEmpty);
      expect(learningPath.beginnerDescription, isEmpty);
      expect(learningPath.intermediateDescription, isEmpty);
      expect(learningPath.advancedDescription, isEmpty);
    });
  });

  group('LearningPath Validation Tests', () {
    test('Should validate 2.8 section paths contain only 2.8.* nodes', () {
      final json = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207', '2.8.217', '2.8.204'],
        'intermediate_path': ['2.8.218', '2.8.208', '2.8.266'],
        'advanced_path': ['2.8.157', '2.8.147', '2.8.198'],
        'cross_section_prerequisites': []
      };

      final path = LearningPath.fromJson(json);
      final sectionPrefix = '2.8';
      final issues = <String>[];

      // 检查入门路径
      for (final itemId in path.beginnerPath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Beginner path contains cross-section node: $itemId');
        }
      }

      // 检查提高路径
      for (final itemId in path.intermediatePath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Intermediate path contains cross-section node: $itemId');
        }
      }

      // 检查冲刺路径
      for (final itemId in path.advancedPath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Advanced path contains cross-section node: $itemId');
        }
      }

      expect(issues, isEmpty);
    });

    test('Should detect cross-section nodes in paths', () {
      final json = {
        'section_id': '3.13',
        'section_name': '高级数据结构扩展',
        'beginner_path': ['3.13.295', '3.13.251', '3.13.250'],
        'intermediate_path': ['3.13.284', '2.1.95', '3.13.285'], // 2.1.95 是跨章节节点
        'advanced_path': ['3.13.141', '3.13.142', '3.13.143'],
        'cross_section_prerequisites': []
      };

      final path = LearningPath.fromJson(json);
      final sectionPrefix = '3.13';
      final issues = <String>[];

      // 检查入门路径
      for (final itemId in path.beginnerPath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Beginner path contains cross-section node: $itemId');
        }
      }

      // 检查提高路径
      for (final itemId in path.intermediatePath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Intermediate path contains cross-section node: $itemId');
        }
      }

      // 检查冲刺路径
      for (final itemId in path.advancedPath) {
        if (!itemId.startsWith('$sectionPrefix.')) {
          issues.add('Advanced path contains cross-section node: $itemId');
        }
      }

      expect(issues.length, greaterThan(0));
      expect(issues.any((issue) => issue.contains('2.1.95')), isTrue);
    });
  });

  group('Mock LearningPath Service Tests', () {
    // 这些测试模拟service的行为，但不实际加载JSON文件
    test('Should handle missing section gracefully', () async {
      final service = LearningPathService();
      
      // 注意：由于测试环境中无法初始化flutter binding，
      // 这里的测试主要验证service的接口设计
      // 实际的文件加载测试需要在集成测试中进行
      
      // 验证service对象能够创建
      expect(service, isNotNull);
      expect(service.isLoading, isFalse);
      expect(service.loadError, isNull);
    });

    test('Should calculate correct cross-section prerequisite counts', () {
      // 模拟2.8章节（应该有8个跨章节前置）
      final json28 = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': ['2.8.207'],
        'cross_section_prerequisites': List.generate(8, (i) => {
          'id': '1.3.$i',
          'name': '基础知识点$i',
          'level': 'L1',
          'reference_count': 10 - i,
          'reason': '补基础/前置回顾'
        })
      };

      // 模拟3.13章节（应该有8个跨章节前置）
      final json313 = {
        'section_id': '3.13',
        'section_name': '高级数据结构扩展',
        'beginner_path': ['3.13.295'],
        'cross_section_prerequisites': List.generate(8, (i) => {
          'id': '1.3.$i',
          'name': 'C++基础$i',
          'level': 'L1',
          'reference_count': 10 - i,
          'reason': '重要前置节点'
        })
      };

      // 模拟4.1章节（应该有0个跨章节前置）
      final json41 = {
        'section_id': '4.1',
        'section_name': '整数与数论基础',
        'beginner_path': ['4.1.1'],
        'cross_section_prerequisites': []
      };

      final path28 = LearningPath.fromJson(json28);
      final path313 = LearningPath.fromJson(json313);
      final path41 = LearningPath.fromJson(json41);

      expect(path28.crossSectionPrerequisites.length, equals(8));
      expect(path313.crossSectionPrerequisites.length, equals(8));
      expect(path41.crossSectionPrerequisites.length, equals(0));
    });

    test('Should provide correct path statistics', () {
      final json = {
        'section_id': '2.8',
        'section_name': '动态规划',
        'beginner_path': List.generate(10, (i) => '2.8.${200 + i}'),
        'intermediate_path': List.generate(15, (i) => '2.8.${210 + i}'),
        'advanced_path': List.generate(15, (i) => '2.8.${230 + i}'),
        'cross_section_prerequisites': List.generate(8, (i) => {
          'id': '1.3.$i',
          'name': '基础知识点$i',
          'level': 'L1',
          'reference_count': 10 - i,
          'reason': '补基础/前置回顾'
        })
      };

      final path = LearningPath.fromJson(json);
      final statistics = path.getPathStatistics();

      expect(statistics['beginner'], equals(10));
      expect(statistics['intermediate'], equals(15));
      expect(statistics['advanced'], equals(15));
      expect(statistics['crossSection'], equals(8));
      expect(statistics['total'], equals(48)); // 10 + 15 + 15 + 8 = 48
    });
  });

  group('Real Asset Loading Tests', () {
    setUp(() {
      // 初始化Flutter binding用于测试环境
      TestWidgetsFlutterBinding.ensureInitialized();
    });

    test('rootBundle should load data/learning_path_report_data.json', () async {
      final service = LearningPathService();
      
      // 加载真实的学习路径数据
      final paths = await service.loadLearningPaths();
      
      // 应该成功加载
      expect(paths, isNotNull);
      expect(paths.isNotEmpty, isTrue);
    });

    test('LearningPathService.loadLearningPaths() should return 3 sections', () async {
      final service = LearningPathService();
      
      // 加载真实的学习路径数据
      final paths = await service.loadLearningPaths();
      
      // 应该返回3个章节
      expect(paths.length, equals(3));
    });

    test('sectionExists(\'2.8\') should be true', () async {
      final service = LearningPathService();
      
      // 加载学习路径数据
      await service.loadLearningPaths();
      
      // 检查2.8章节是否存在
      final exists = await service.hasLearningPath('2.8');
      expect(exists, isTrue);
    });

    test('sectionExists(\'3.13\') should be true', () async {
      final service = LearningPathService();
      
      // 加载学习路径数据
      await service.loadLearningPaths();
      
      // 检查3.13章节是否存在
      final exists = await service.hasLearningPath('3.13');
      expect(exists, isTrue);
    });

    test('sectionExists(\'4.1\') should be true', () async {
      final service = LearningPathService();
      
      // 加载学习路径数据
      await service.loadLearningPaths();
      
      // 检查4.1章节是否存在
      final exists = await service.hasLearningPath('4.1');
      expect(exists, isTrue);
    });

    test('getBeginnerPath(\'2.8\').length should be 10', () async {
      final service = LearningPathService();
      
      // 获取2.8章节的入门路径
      final beginnerPath = await service.getBeginnerPath('2.8');
      
      // 应该有10个入门知识点
      expect(beginnerPath.length, equals(10));
    });

    test('getIntermediatePath(\'2.8\').length should be 15', () async {
      final service = LearningPathService();
      
      // 获取2.8章节的提高路径
      final intermediatePath = await service.getIntermediatePath('2.8');
      
      // 应该有15个提高知识点
      expect(intermediatePath.length, equals(15));
    });

    test('getAdvancedPath(\'2.8\').length should be 15', () async {
      final service = LearningPathService();
      
      // 获取2.8章节的冲刺路径
      final advancedPath = await service.getAdvancedPath('2.8');
      
      // 应该有15个冲刺知识点
      expect(advancedPath.length, equals(15));
    });

    test('getCrossSectionPrerequisites(\'2.8\').length should be 8', () async {
      final service = LearningPathService();
      
      // 获取2.8章节的跨章节前置
      final prerequisites = await service.getCrossSectionPrerequisites('2.8');
      
      // 应该有8个跨章节前置
      expect(prerequisites.length, equals(8));
    });

    test('getCrossSectionPrerequisites(\'3.13\').length should be 8', () async {
      final service = LearningPathService();
      
      // 获取3.13章节的跨章节前置
      final prerequisites = await service.getCrossSectionPrerequisites('3.13');
      
      // 应该有8个跨章节前置
      expect(prerequisites.length, equals(8));
    });

    test('getCrossSectionPrerequisites(\'4.1\').length should be 0', () async {
      final service = LearningPathService();
      
      // 获取4.1章节的跨章节前置
      final prerequisites = await service.getCrossSectionPrerequisites('4.1');
      
      // 应该有0个跨章节前置
      expect(prerequisites.length, equals(0));
    });

    test('LearningPath sectionId should be correctly injected', () async {
      final service = LearningPathService();
      
      // 获取2.8章节的完整学习路径
      final path = await service.getLearningPathBySectionId('2.8');
      
      // 验证sectionId正确注入
      expect(path, isNotNull);
      expect(path!.sectionId, equals('2.8'));
      expect(path.sectionName, equals('动态规划'));
    });

    test('All three sections should have correct structure', () async {
      final service = LearningPathService();
      
      // 获取所有学习路径
      final paths = await service.loadLearningPaths();
      
      // 验证每个章节都有正确的结构
      paths.forEach((sectionId, path) {
        expect(path.sectionId, equals(sectionId));
        expect(path.sectionName, isNotEmpty);
        expect(path.beginnerPath, isNotEmpty);
        expect(path.intermediatePath, isNotEmpty);
        expect(path.advancedPath, isNotEmpty);
        // validation_status在真实数据中不存在，使用默认值unknown
        expect(path.validationStatus, equals(ValidationStatus.unknown));
      });
    });
  });
}