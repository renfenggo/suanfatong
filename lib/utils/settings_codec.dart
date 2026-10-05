import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// 设置持久化键与编解码。
///
/// 历史问题：`settings_repository.dart`（已删除）曾用 string 写入 `theme_mode`
/// ('system'/'light'/'dark')，而设置页用 int 写入（ThemeMode.index）。
/// 本类统一为 int 轨，读取时兼容历史 string 值，避免 `getInt` 对 string 抛异常。
class SettingsCodec {
  static const String keyFontSize = 'font_size';
  static const String keyThemeMode = 'theme_mode';
  static const String keyLocale = 'app_locale';

  /// 兼容解码 theme_mode：int（现行）优先，string（历史遗留）兜底。
  static ThemeMode decodeThemeMode(Object? raw) {
    if (raw is int && raw >= 0 && raw < ThemeMode.values.length) {
      return ThemeMode.values[raw];
    }
    switch (raw) {
      case 'light':
        return ThemeMode.light;
      case 'dark':
        return ThemeMode.dark;
      default:
        return ThemeMode.system;
    }
  }

  static ThemeMode loadThemeMode(SharedPreferences prefs) =>
      decodeThemeMode(prefs.get(keyThemeMode));

  /// 解码 app_locale：'zh_CN' -> Locale('zh', 'CN')；'en' -> Locale('en')。
  static Locale? decodeLocale(String? raw) {
    if (raw == null || raw.isEmpty) return null;
    final parts = raw.split('_');
    return parts.length > 1 ? Locale(parts[0], parts[1]) : Locale(parts[0]);
  }

  static Locale? loadLocale(SharedPreferences prefs) =>
      decodeLocale(prefs.getString(keyLocale));

  static double loadFontSize(SharedPreferences prefs) =>
      prefs.getDouble(keyFontSize) ?? 16.0;
}

/// 启动时一次性恢复的设置快照。
class BootstrappedSettings {
  final ThemeMode themeMode;
  final Locale? locale;
  final double fontSize;

  const BootstrappedSettings({
    required this.themeMode,
    required this.locale,
    required this.fontSize,
  });
}

/// 从持久化中恢复启动设置（main.dart 调用）。
BootstrappedSettings bootstrapSettings(SharedPreferences prefs) {
  return BootstrappedSettings(
    themeMode: SettingsCodec.loadThemeMode(prefs),
    locale: SettingsCodec.loadLocale(prefs),
    fontSize: SettingsCodec.loadFontSize(prefs),
  );
}
