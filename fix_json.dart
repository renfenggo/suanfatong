// ignore_for_file: avoid_print
import 'dart:io';
import 'dart:convert';

void main() async {
  final files = [
    'assets/data/cpp/section_5_5_units.json',
    'assets/data/cpp/section_5_6_units.json',
    'assets/data/cpp/section_5_7_units.json',
    'assets/data/cpp/section_5_8_units.json',
    'assets/data/cpp/section_5_9_units.json',
  ];
  for (final f in files) {
    var content = await File(f).readAsString();
    final lines = content.split('\n');
    final fixed = <String>[];
    for (int i = 0; i < lines.length; i++) {
      var line = lines[i].trimRight();
      if (line.endsWith('}]}')) {
        line = line.substring(0, line.length - 1);
      }
      fixed.add(line);
    }
    await File(f).writeAsString(fixed.join('\n'));
    try {
      jsonDecode(await File(f).readAsString());
      print('OK: $f');
    } catch (e) {
      print('STILL ERROR: $f => $e');
    }
  }
}
