import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../state/progress_provider.dart';

final fontSizeProvider = StateProvider<double>((ref) => 16.0);
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.system);
final localeProvider = StateProvider<Locale?>((ref) => null);

class _LocaleItem {
  final String name;
  final String nativeName;
  final Locale locale;
  const _LocaleItem(this.name, this.nativeName, this.locale);
}

class AppSupportedLocales {
  static const all = [
    Locale('zh', 'CN'),
    Locale('zh', 'TW'),
    Locale('en'),
    Locale('ja'),
    Locale('ko'),
    Locale('fr'),
    Locale('de'),
    Locale('es'),
    Locale('it'),
    Locale('pt'),
    Locale('ru'),
    Locale('ar'),
    Locale('th'),
    Locale('vi'),
    Locale('id'),
    Locale('ms'),
    Locale('tr'),
    Locale('pl'),
    Locale('nl'),
    Locale('hi'),
  ];
}

const _locales = [
  _LocaleItem('中文（简体）', '简体中文', Locale('zh', 'CN')),
  _LocaleItem('中文（繁體）', '繁體中文', Locale('zh', 'TW')),
  _LocaleItem('English', 'English', Locale('en')),
  _LocaleItem('日本語', '日本語', Locale('ja')),
  _LocaleItem('한국어', '한국어', Locale('ko')),
  _LocaleItem('Français', 'Français', Locale('fr')),
  _LocaleItem('Deutsch', 'Deutsch', Locale('de')),
  _LocaleItem('Español', 'Español', Locale('es')),
  _LocaleItem('Italiano', 'Italiano', Locale('it')),
  _LocaleItem('Português', 'Português', Locale('pt')),
  _LocaleItem('Русский', 'Русский', Locale('ru')),
  _LocaleItem('العربية', 'العربية', Locale('ar')),
  _LocaleItem('ไทย', 'ไทย', Locale('th')),
  _LocaleItem('Tiếng Việt', 'Tiếng Việt', Locale('vi')),
  _LocaleItem('Bahasa Indonesia', 'Indonesia', Locale('id')),
  _LocaleItem('Bahasa Melayu', 'Melayu', Locale('ms')),
  _LocaleItem('Türkçe', 'Türkçe', Locale('tr')),
  _LocaleItem('Polski', 'Polski', Locale('pl')),
  _LocaleItem('Nederlands', 'Nederlands', Locale('nl')),
  _LocaleItem('हिन्दी', 'हिन्दी', Locale('hi')),
];

class SettingsPage extends ConsumerStatefulWidget {
  const SettingsPage({super.key});

  @override
  ConsumerState<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends ConsumerState<SettingsPage> {
  double _fontSize = 16.0;
  ThemeMode _themeMode = ThemeMode.system;
  Locale? _selectedLocale;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    final savedLang = prefs.getString('app_locale');
    setState(() {
      _fontSize = prefs.getDouble('font_size') ?? 16.0;
      _themeMode = ThemeMode.values[prefs.getInt('theme_mode') ?? 0];
      if (savedLang != null) {
        final parts = savedLang.split('_');
        _selectedLocale =
            parts.length > 1 ? Locale(parts[0], parts[1]) : Locale(parts[0]);
      }
      _loading = false;
    });
    ref.read(fontSizeProvider.notifier).state = _fontSize;
    ref.read(themeModeProvider.notifier).state = _themeMode;
    ref.read(localeProvider.notifier).state = _selectedLocale;
  }

  Future<void> _setFontSize(double size) async {
    setState(() => _fontSize = size);
    ref.read(fontSizeProvider.notifier).state = size;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('font_size', size);
  }

  Future<void> _setThemeMode(ThemeMode mode) async {
    setState(() => _themeMode = mode);
    ref.read(themeModeProvider.notifier).state = mode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('theme_mode', mode.index);
  }

  Future<void> _setLocale(Locale? locale) async {
    setState(() => _selectedLocale = locale);
    ref.read(localeProvider.notifier).state = locale;
    final prefs = await SharedPreferences.getInstance();
    if (locale != null) {
      final key =
          locale.countryCode != null
              ? '${locale.languageCode}_${locale.countryCode}'
              : locale.languageCode;
      await prefs.setString('app_locale', key);
    } else {
      await prefs.remove('app_locale');
    }
  }

  Future<void> _clearProgress() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder:
          (ctx) => AlertDialog(
            title: const Text('确认清除'),
            content: const Text('确定要清除所有学习进度吗？此操作不可恢复。'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx, false),
                child: const Text('取消'),
              ),
              TextButton(
                onPressed: () => Navigator.pop(ctx, true),
                child: const Text(
                  '确定清除',
                  style: TextStyle(color: Color(0xFFE74C3C)),
                ),
              ),
            ],
          ),
    );
    if (confirmed == true) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('bfs_learn_progress');
      ref.invalidate(progressProvider);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('学习进度已清除'),
            backgroundColor: Color(0xFF4CAF50),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Scaffold(
        appBar: AppBar(title: const Text('设置')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('设置')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildSectionHeader('显示设置'),
            const SizedBox(height: 8),
            _buildFontSizeCard(),
            const SizedBox(height: 16),
            _buildThemeCard(),
            const SizedBox(height: 24),
            _buildSectionHeader('语言 / Language'),
            const SizedBox(height: 8),
            _buildLocaleCard(),
            const SizedBox(height: 24),
            _buildSectionHeader('数据管理'),
            const SizedBox(height: 8),
            _buildClearCard(),
            const SizedBox(height: 24),
            _buildSectionHeader('关于'),
            const SizedBox(height: 8),
            _buildAboutCard(),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: Color(0xFF888888),
        ),
      ),
    );
  }

  Widget _buildFontSizeCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.text_fields, color: Color(0xFF4A90D9)),
                SizedBox(width: 8),
                Text(
                  '字体大小',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                const Text('小', style: TextStyle(fontSize: 12)),
                Expanded(
                  child: Slider(
                    value: _fontSize,
                    min: 12,
                    max: 24,
                    divisions: 6,
                    label: _fontSize.round().toString(),
                    onChanged: _setFontSize,
                  ),
                ),
                const Text('大', style: TextStyle(fontSize: 18)),
              ],
            ),
            Center(
              child: Text(
                '当前：${_fontSize.round()} px',
                style: const TextStyle(fontSize: 13, color: Color(0xFF888888)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildThemeCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.dark_mode, color: Color(0xFF9B59B6)),
                SizedBox(width: 8),
                Text(
                  '主题模式',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 12),
            SegmentedButton<ThemeMode>(
              segments: const [
                ButtonSegment(
                  value: ThemeMode.system,
                  label: Text('跟随系统'),
                  icon: Icon(Icons.brightness_auto),
                ),
                ButtonSegment(
                  value: ThemeMode.light,
                  label: Text('浅色'),
                  icon: Icon(Icons.light_mode),
                ),
                ButtonSegment(
                  value: ThemeMode.dark,
                  label: Text('深色'),
                  icon: Icon(Icons.dark_mode),
                ),
              ],
              selected: {_themeMode},
              onSelectionChanged: (modes) => _setThemeMode(modes.first),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLocaleCard() {
    final currentName =
        _selectedLocale == null
            ? '跟随系统'
            : _locales
                .firstWhere(
                  (l) => l.locale == _selectedLocale,
                  orElse: () => _locales[0],
                )
                .name;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.language, color: Color(0xFF50C878)),
                SizedBox(width: 8),
                Text(
                  '界面语言',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 4),
            const Text(
              '切换 App 显示语言，上架 App Store 必备',
              style: TextStyle(fontSize: 12, color: Color(0xFF888888)),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: DropdownButton<String>(
                value:
                    _selectedLocale == null
                        ? '__system__'
                        : (_selectedLocale!.countryCode != null
                            ? '${_selectedLocale!.languageCode}_${_selectedLocale!.countryCode}'
                            : _selectedLocale!.languageCode),
                isExpanded: true,
                underline: Container(height: 1, color: const Color(0xFFE0E0E0)),
                style: const TextStyle(fontSize: 15, color: Color(0xFF333333)),
                items: [
                  DropdownMenuItem(
                    value: '__system__',
                    child: Text(currentName),
                  ),
                  ..._locales.map((item) {
                    final key =
                        item.locale.countryCode != null
                            ? '${item.locale.languageCode}_${item.locale.countryCode}'
                            : item.locale.languageCode;
                    return DropdownMenuItem(
                      value: key,
                      child: Text('${item.nativeName}  (${item.name})'),
                    );
                  }),
                ],
                onChanged: (value) {
                  if (value == null || value == '__system__') {
                    _setLocale(null);
                  } else {
                    final parts = value.split('_');
                    _setLocale(
                      parts.length > 1
                          ? Locale(parts[0], parts[1])
                          : Locale(parts[0]),
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildClearCard() {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.delete_outline, color: Color(0xFFE74C3C)),
        title: const Text(
          '清除学习进度',
          style: TextStyle(fontWeight: FontWeight.w600),
        ),
        subtitle: const Text('删除所有答题记录和学习数据'),
        trailing: const Icon(Icons.chevron_right),
        onTap: _clearProgress,
      ),
    );
  }

  Widget _buildAboutCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.info_outline, color: Color(0xFF4A90D9)),
                SizedBox(width: 8),
                Text(
                  '关于',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _buildInfoRow('应用名称', 'BFS 专题学习'),
            const SizedBox(height: 8),
            _buildInfoRow('版本', '1.0.0'),
            const SizedBox(height: 8),
            _buildInfoRow('说明', '信奥 BFS 专题离线学习 App'),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(color: Color(0xFF666666))),
        Text(value, style: const TextStyle(fontWeight: FontWeight.w500)),
      ],
    );
  }
}
