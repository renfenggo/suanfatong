import '../models/cpp_animation.dart';
import '../repositories/json_asset_repository.dart';

class CppAnimationRepository {
  final JsonAssetRepository _jsonRepo;
  static const _manifestPath =
      'assets/data/cpp/animations/cpp_animation_manifest.json';

  CppAnimationRepository({required JsonAssetRepository jsonRepo})
    : _jsonRepo = jsonRepo;

  Future<CppAnimationManifest> loadManifest() async {
    final map = await _jsonRepo.loadMap(_manifestPath);
    return CppAnimationManifest.fromJson(map);
  }

  Future<CppAnimation> loadAnimation(String animationId) async {
    final manifest = await loadManifest();
    for (final meta in manifest.animations) {
      if (meta.animationId == animationId) {
        final map = await _jsonRepo.loadMap(meta.assetPath);
        return CppAnimation.fromJson(map);
      }
    }
    throw StateError('Animation not found: $animationId');
  }

  Future<List<CppAnimationMeta>> animationsForItem(String itemId) async {
    final manifest = await loadManifest();
    final matched =
        manifest.animations.where((m) => m.itemId == itemId).toList()
          ..sort((a, b) => a.order.compareTo(b.order));
    return matched;
  }
}
