import 'dart:convert';
import 'package:flutter/services.dart';

class JsonAssetRepository {
  Future<Map<String, dynamic>> loadMap(String assetPath) async {
    final jsonStr = await rootBundle.loadString(assetPath);
    return json.decode(jsonStr) as Map<String, dynamic>;
  }

  Future<List<dynamic>> loadList(String assetPath) async {
    final jsonStr = await rootBundle.loadString(assetPath);
    return json.decode(jsonStr) as List<dynamic>;
  }
}
