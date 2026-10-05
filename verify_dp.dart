import 'dart:convert';
import 'dart:io';

void main() {
  final f = File('assets/data/algorithm/section_2_8_units.json');
  final json = jsonDecode(f.readAsStringSync()) as Map;
  final units = json['units'] as List;
  print('Total units: ${units.length}');
  for (var u in units) {
    final m = u as Map;
    final id = m['itemId'] as String;
    final title = m['title'] as String;
    final expl = (m['explanation'] as String);
    final isTemplate = expl.contains('请参考相关教材和资料学习此内容');
    final marker = isTemplate ? '❌' : '✅';
    print('  $marker $id: $title');
  }
}
