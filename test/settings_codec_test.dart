import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:bfs_learn/utils/settings_codec.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('SettingsCodec.decodeThemeMode（int/string 双轨兼容，M1-3）', () {
    test('int 轨（现行）：0/1/2 -> system/light/dark', () {
      expect(SettingsCodec.decodeThemeMode(0), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode(1), ThemeMode.light);
      expect(SettingsCodec.decodeThemeMode(2), ThemeMode.dark);
    });

    test('string 轨（settings_repository 历史遗留）兼容解码', () {
      expect(SettingsCodec.decodeThemeMode('system'), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode('light'), ThemeMode.light);
      expect(SettingsCodec.decodeThemeMode('dark'), ThemeMode.dark);
    });

    test('异常值兜底为 system', () {
      expect(SettingsCodec.decodeThemeMode(null), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode(-1), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode(99), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode('乱值'), ThemeMode.system);
      expect(SettingsCodec.decodeThemeMode(3.14), ThemeMode.system);
    });

    test('从 SharedPreferences 读取 string 遗留值不抛异常', () async {
      SharedPreferences.setMockInitialValues({'theme_mode': 'dark'});
      final prefs = await SharedPreferences.getInstance();
      expect(SettingsCodec.loadThemeMode(prefs), ThemeMode.dark);
    });
  });

  group('SettingsCodec.decodeLocale', () {
    test('zh_CN -> Locale(zh, CN)', () {
      final locale = SettingsCodec.decodeLocale('zh_CN');
      expect(locale, isNotNull);
      expect(locale!.languageCode, 'zh');
      expect(locale.countryCode, 'CN');
    });

    test('en -> Locale(en)', () {
      final locale = SettingsCodec.decodeLocale('en');
      expect(locale, isNotNull);
      expect(locale!.languageCode, 'en');
      expect(locale.countryCode, isNull);
    });

    test('null / 空串 -> null（跟随系统）', () {
      expect(SettingsCodec.decodeLocale(null), isNull);
      expect(SettingsCodec.decodeLocale(''), isNull);
    });
  });

  group('bootstrapSettings（启动恢复，M1-3）', () {
    test('空偏好 -> 全部默认值', () async {
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      final settings = bootstrapSettings(prefs);
      expect(settings.themeMode, ThemeMode.system);
      expect(settings.locale, isNull);
      expect(settings.fontSize, 16.0);
    });

    test('恢复深色主题 + 英语 + 字号 20', () async {
      SharedPreferences.setMockInitialValues({
        'theme_mode': 2,
        'app_locale': 'en',
        'font_size': 20.0,
      });
      final prefs = await SharedPreferences.getInstance();
      final settings = bootstrapSettings(prefs);
      expect(settings.themeMode, ThemeMode.dark);
      expect(settings.locale, const Locale('en'));
      expect(settings.fontSize, 20.0);
    });

    test('历史 string theme_mode 遗留也能恢复', () async {
      SharedPreferences.setMockInitialValues({'theme_mode': 'light'});
      final prefs = await SharedPreferences.getInstance();
      expect(bootstrapSettings(prefs).themeMode, ThemeMode.light);
    });
  });
}
