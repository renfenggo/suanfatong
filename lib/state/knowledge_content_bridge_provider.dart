import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/knowledge_content_bridge.dart';
import 'content_manifest_provider.dart';
import 'knowledge_graph_provider.dart';

final knowledgeContentBridgeProvider = FutureProvider<KnowledgeContentBridge?>((
  ref,
) {
  final graphAsync = ref.watch(knowledgeGraphProvider);
  final manifestAsync = ref.watch(contentManifestProvider);

  if (!graphAsync.hasValue || !manifestAsync.hasValue) return null;

  return KnowledgeContentBridge(
    graph: graphAsync.value!,
    manifest: manifestAsync.value!,
  );
});
