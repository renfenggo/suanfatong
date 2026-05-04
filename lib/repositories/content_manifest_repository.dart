import '../models/content_manifest.dart';
import 'json_asset_repository.dart';

class ContentManifestRepository {
  static const _manifestPath = 'assets/data/content_manifest.json';
  final JsonAssetRepository _jsonRepo;

  ContentManifestRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<ContentManifest> loadManifest() async {
    final map = await _jsonRepo.loadMap(_manifestPath);
    return ContentManifest.fromJson(map);
  }
}
