class ContentModule {
  final String moduleId;
  final String title;
  final String subtitle;
  final String iconKey;
  final String colorHex;
  final String route;
  final int order;

  const ContentModule({
    required this.moduleId,
    this.title = '',
    this.subtitle = '',
    this.iconKey = 'menu_book',
    this.colorHex = '#4A90D9',
    this.route = '/',
    this.order = 0,
  });

  factory ContentModule.fromJson(Map<String, dynamic> json) {
    return ContentModule(
      moduleId: json['moduleId'] as String? ?? '',
      title: json['title'] as String? ?? '',
      subtitle: json['subtitle'] as String? ?? '',
      iconKey: json['iconKey'] as String? ?? 'menu_book',
      colorHex: json['colorHex'] as String? ?? '#4A90D9',
      route: json['route'] as String? ?? '/',
      order: json['order'] as int? ?? 0,
    );
  }
}
