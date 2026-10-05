import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'app/app.dart';
import 'pages/settings_page.dart';
import 'utils/settings_codec.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 启动时恢复主题/语言/字号（M1-3：此前只有进入设置页才恢复）
  final prefs = await SharedPreferences.getInstance();
  final settings = bootstrapSettings(prefs);

  runApp(
    ProviderScope(
      overrides: [
        themeModeProvider.overrideWith((ref) => settings.themeMode),
        localeProvider.overrideWith((ref) => settings.locale),
        fontSizeProvider.overrideWith((ref) => settings.fontSize),
      ],
      child: const BfsApp(),
    ),
  );
}
