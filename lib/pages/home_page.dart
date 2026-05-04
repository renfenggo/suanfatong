import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/content_manifest_provider.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  static IconData _resolveIcon(String key) {
    return switch (key) {
      'menu_book' => Icons.menu_book,
      'play_circle' => Icons.play_circle_filled,
      'quiz' => Icons.quiz,
      'warning' => Icons.warning_amber,
      'school' => Icons.school,
      'bar_chart' => Icons.bar_chart,
      'settings' => Icons.settings,
      'account_tree' => Icons.account_tree,
      'terminal' => Icons.terminal,
      _ => Icons.circle,
    };
  }

  static Color _resolveColor(String hex) {
    final code = hex.replaceFirst('#', '');
    return Color(int.parse('FF$code', radix: 16));
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final manifestAsync = ref.watch(contentManifestProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('BFS 专题学习')),
      body: SafeArea(
        child: manifestAsync.when(
          data: (manifest) {
            final modules = List.of(manifest.modules)
              ..sort((a, b) => a.order.compareTo(b.order));
            return Column(
              children: [
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.fromLTRB(20, 20, 20, 10),
                  child: Text(
                    manifest.defaultTopic.subtitle,
                    style: const TextStyle(
                      fontSize: 15,
                      color: Color(0xFF666666),
                    ),
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.only(bottom: 24),
                    itemCount: modules.length,
                    itemBuilder: (context, index) {
                      final m = modules[index];
                      return _MenuCard(
                        title: m.title,
                        subtitle: m.subtitle,
                        icon: _resolveIcon(m.iconKey),
                        color: _resolveColor(m.colorHex),
                        route: m.route,
                      );
                    },
                  ),
                ),
              ],
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, _) => Center(child: Text('加载失败: $e')),
        ),
      ),
    );
  }
}

class _MenuCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final String route;

  const _MenuCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.route,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(context, route);
        },
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF888888),
                      ),
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: Colors.grey[400]),
            ],
          ),
        ),
      ),
    );
  }
}
