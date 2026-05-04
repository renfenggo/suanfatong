import '../models/cpp_learning_unit.dart';
import 'json_asset_repository.dart';

class CppLearningRepository {
  final JsonAssetRepository _jsonRepo;
  static const _manifestPath = 'assets/data/cpp/cpp_learning_manifest.json';

  CppLearningRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<CppLearningContent> loadContent() async {
    final manifestMap = await _jsonRepo.loadMap(_manifestPath);
    final manifest = CppLearningManifest.fromJson(manifestMap);

    final allUnits = <CppLearningUnit>[];
    final seenItemIds = <String>{};

    final baseContent = await _loadSingleFile(manifest.baseFile);
    _addUnitsWithDuplicateCheck(
      allUnits,
      baseContent.units,
      seenItemIds,
      manifest.baseFile,
    );

    for (final sectionFile in manifest.sectionFiles) {
      final sectionContent = await _loadSingleFile(sectionFile);
      _addUnitsWithDuplicateCheck(
        allUnits,
        sectionContent.units,
        seenItemIds,
        sectionFile,
      );
    }

    return CppLearningContent(
      version: manifest.version,
      category: manifest.category,
      units: allUnits,
    );
  }

  Future<CppLearningContent> _loadSingleFile(String filePath) async {
    final map = await _jsonRepo.loadMap(filePath);
    return CppLearningContent.fromJson(map);
  }

  void _addUnitsWithDuplicateCheck(
    List<CppLearningUnit> targetUnits,
    List<CppLearningUnit> sourceUnits,
    Set<String> seenItemIds,
    String sourceFile,
  ) {
    for (final unit in sourceUnits) {
      if (seenItemIds.contains(unit.itemId)) {
        throw StateError(
          'Duplicate C++ learning unit itemId: ${unit.itemId} found in $sourceFile',
        );
      }
      seenItemIds.add(unit.itemId);
      targetUnits.add(unit);
    }
  }
}
