import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/mistake.dart';

class MistakeService {
  Future<List<Mistake>> loadMistakes(String assetPath) async {
    final jsonStr = await rootBundle.loadString(assetPath);
    final List<dynamic> jsonList = json.decode(jsonStr);
    return jsonList
        .map((e) => Mistake.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
