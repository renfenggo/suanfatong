// ignore_for_file: avoid_print
import 'dart:io';
import 'dart:convert';

void main() async {
  final files = [
    'assets/data/cpp/cpp_learning_units.json',
    'assets/data/cpp/section_1_2_units.json',
    'assets/data/cpp/section_1_3_units.json',
    'assets/data/cpp/section_1_4_units.json',
    'assets/data/cpp/section_1_5_units.json',
    'assets/data/cpp/section_1_6_units.json',
    'assets/data/cpp/section_1_7_units.json',
    'assets/data/cpp/section_1_8_units.json',
    'assets/data/cpp/section_1_9_units.json',
    'assets/data/cpp/section_1_10_units.json',
    'assets/data/cpp/section_5_1_units.json',
    'assets/data/cpp/section_5_2_units.json',
    'assets/data/cpp/section_5_3_units.json',
    'assets/data/cpp/section_5_4_units.json',
    'assets/data/cpp/section_5_5_units.json',
    'assets/data/cpp/section_5_6_units.json',
    'assets/data/cpp/section_5_7_units.json',
    'assets/data/cpp/section_5_8_units.json',
    'assets/data/cpp/section_5_9_units.json',
    'assets/data/algorithm/algorithm_learning_units.json',
    'assets/data/algorithm/section_2_2_units.json',
    'assets/data/algorithm/section_2_3_units.json',
    'assets/data/algorithm/section_2_7_units.json',
    'assets/data/algorithm/section_3_1_units.json',
    'assets/data/algorithm/section_3_2_units.json',
    'assets/data/algorithm/section_3_3_units.json',
    'assets/data/algorithm/section_3_4_units.json',
    'assets/data/algorithm/section_3_5_units.json',
    'assets/data/algorithm/section_3_6_units.json',
    'assets/data/algorithm/section_3_7_12_units.json',
    'assets/data/algorithm/section_3_7_units.json',
    'assets/data/algorithm/section_3_8_units.json',
    'assets/data/algorithm/section_3_9_units.json',
    'assets/data/algorithm/section_3_10_units.json',
    'assets/data/algorithm/section_3_11_units.json',
    'assets/data/algorithm/section_3_12_units.json',
    'assets/data/knowledge/io_v4_4.json',
  ];
  for (final f in files) {
    try {
      final raw = await File(f).readAsString();
      jsonDecode(raw);
      print('OK: $f');
    } catch (e) {
      print('ERROR: $f => $e');
    }
  }
}
