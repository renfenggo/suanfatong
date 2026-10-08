import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../app/app_router.dart';
import '../services/cloud_sync_service.dart';
import '../state/cloud_sync_provider.dart';
import '../state/progress_provider.dart';
import '../utils/settings_codec.dart';

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
  String _version = '';
  bool _syncing = false;
  String? _lastSyncSummary;
  int _pendingCount = 0;

  @override
  void initState() {
    super.initState();
    _loadSettings();
    _refreshPendingCount();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    final info = await PackageInfo.fromPlatform();
    setState(() {
      _fontSize = SettingsCodec.loadFontSize(prefs);
      _themeMode = SettingsCodec.loadThemeMode(prefs);
      _selectedLocale = SettingsCodec.loadLocale(prefs);
      _version = '${info.version} (${info.buildNumber})';
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

  Future<void> _refreshPendingCount() async {
    final queue = ref.read(offlineEventQueueProvider);
    await queue.load();
    if (mounted) {
      setState(() => _pendingCount = queue.pendingCount);
    }
  }

  Future<void> _syncNow() async {
    if (_syncing) return;
    setState(() {
      _syncing = true;
      _lastSyncSummary = null;
    });
    final result = await ref.read(cloudSyncServiceProvider).syncOnce();
    if (!mounted) return;
    setState(() {
      _syncing = false;
      _lastSyncSummary = _describeSyncResult(result);
    });
    await _refreshPendingCount();
  }

  String _describeSyncResult(CloudSyncResult result) {
    switch (result.outcome) {
      case CloudSyncOutcome.synced:
        final persist = result.persistError;
        if (persist != null && persist.isNotEmpty) {
          return '已同步 ${result.confirmedCount} 条（警告：本地落盘失败，重启后可能重复上报，服务端幂等去重）';
        }
        return '已同步 ${result.confirmedCount} 条';
      case CloudSyncOutcome.skippedFlagOff:
        return '云端同步未开启（cloud_sync 开关关闭）';
      case CloudSyncOutcome.skippedNoCredentials:
        return '未登录，请先登录';
      case CloudSyncOutcome.loggedOut:
        return '登录已过期，请重新登录';
      case CloudSyncOutcome.retryLater:
        return '网络暂不可用，已保留待上报记录，稍后重试';
      case CloudSyncOutcome.failed:
        return '同步失败：${result.error ?? '未知错误'}';
    }
  }

  Future<void> _logout() async {
    await ref.read(authControllerProvider.notifier).logout();
    if (!mounted) return;
    await _refreshPendingCount();
    if (!mounted) return;
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('已退出登录（本地学习数据保留）')));
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
      // N03：进度键带账号命名空间，只清当前账号的进度。
      await ref.read(progressServiceProvider).clear();
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
            _buildSectionHeader('云同步'),
            const SizedBox(height: 8),
            _buildCloudSyncCard(),
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
        subtitle: const Text('删除当前账号的答题记录和学习数据'),
        trailing: const Icon(Icons.chevron_right),
        onTap: _clearProgress,
      ),
    );
  }

  Widget _buildCloudSyncCard() {
    final session = ref.watch(authControllerProvider);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.cloud_sync, color: Color(0xFF4A90D9)),
                const SizedBox(width: 8),
                const Text(
                  '云同步',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
                const Spacer(),
                session.loggedIn
                    ? TextButton.icon(
                      key: const Key('sync_logout'),
                      onPressed: _logout,
                      icon: const Icon(Icons.logout, size: 18),
                      label: const Text('退出登录'),
                    )
                    : FilledButton.tonalIcon(
                      key: const Key('sync_go_login'),
                      onPressed: () => context.go(AppRouter.login),
                      icon: const Icon(Icons.login, size: 18),
                      label: const Text('去登录'),
                    ),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              session.loggedIn
                  ? '已登录：${session.displayName}'
                  : session.username.isNotEmpty
                  ? '上次登录：${session.displayName}——登录已过期，请重新登录'
                  : '未登录——登录后学习记录自动同步',
              style: const TextStyle(fontSize: 13, color: Color(0xFF888888)),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '待上报：$_pendingCount 条',
                        style: const TextStyle(fontSize: 13),
                      ),
                      if (_lastSyncSummary != null) ...[
                        const SizedBox(height: 4),
                        Text(
                          _lastSyncSummary!,
                          key: const Key('sync_last_result'),
                          style: const TextStyle(
                            fontSize: 13,
                            color: Color(0xFF888888),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                FilledButton.icon(
                  key: const Key('sync_now'),
                  onPressed: _syncing ? null : _syncNow,
                  icon:
                      _syncing
                          ? const SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                          : const Icon(Icons.sync),
                  label: Text(_syncing ? '同步中…' : '立即同步'),
                ),
              ],
            ),
          ],
        ),
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
            _buildInfoRow('应用名称', '算法通'),
            const SizedBox(height: 8),
            _buildInfoRow('版本', _version.isEmpty ? '加载中…' : _version),
            const SizedBox(height: 8),
            _buildInfoRow('说明', '算法比赛学习应用'),
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
