import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Frontend Structure MVP page source integration', () {
    test('knowledge item page includes all MVP entry sections', () async {
      final source = await File(
        'lib/pages/knowledge_item_page.dart',
      ).readAsString();

      expect(source, contains('LearningCardSection'));
      expect(source, contains('PracticeEntrySection'));
      expect(source, contains('Cpp14TemplateEntrySection'));
      expect(source, contains('AnimationEntrySection'));
      expect(source, contains('LearningCardService'));
      expect(source, contains('PracticeEntryService'));
      expect(source, contains('Cpp14TemplateService'));
      expect(source, contains('cppAnimationsForItemProvider'));
    });

    test('knowledge section page includes all MVP section widgets', () async {
      final source = await File(
        'lib/pages/knowledge_section_page.dart',
      ).readAsString();

      expect(source, contains('LearningPathPanel'));
      expect(source, contains('CrossSectionPrerequisitePanel'));
      expect(source, contains('LayeredKnowledgeList'));
      expect(source, contains('sectionLearningPathProvider'));
      expect(source, contains('sectionCollapsePolicyProvider'));
      expect(source, contains('itemFrontendLayersProvider'));
    });
  });
}
