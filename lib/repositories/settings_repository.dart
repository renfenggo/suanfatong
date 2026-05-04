import 'package:shared_preferences/shared_preferences.dart';

class SettingsRepository {
  static const _keyFontSize = 'font_size';
  static const _keyThemeMode = 'theme_mode';
  static const _keyLocale = 'app_locale';

  Future<double> loadFontSize() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getDouble(_keyFontSize) ?? 16.0;
  }

  Future<void> saveFontSize(double size) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_keyFontSize, size);
  }

  Future<String> loadThemeMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyThemeMode) ?? 'system';
  }

  Future<void> saveThemeMode(String mode) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyThemeMode, mode);
  }

  Future<String?> loadLocale() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyLocale);
  }

  Future<void> saveLocale(String? localeKey) async {
    final prefs = await SharedPreferences.getInstance();
    if (localeKey != null) {
      await prefs.setString(_keyLocale, localeKey);
    } else {
      await prefs.remove(_keyLocale);
    }
  }
}
