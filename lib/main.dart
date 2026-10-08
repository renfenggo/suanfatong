import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'app/app.dart';
import 'pages/settings_page.dart';
import 'services/offline_event_queue.dart';
import 'state/cloud_sync_provider.dart';
import 'utils/settings_codec.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 启动时恢复主题/语言/字号（M1-3：此前只有进入设置页才恢复）
  final prefs = await SharedPreferences.getInstance();
  final settings = bootstrapSettings(prefs);

  // P1 最小用户闭环：初始化稳定设备号，云同步队列落盘（文件持久化，
  // 跨重启保留待上报事件与幂等键水位）
  final deviceId = await ensureDeviceId(prefs);

  runApp(
    ProviderScope(
      overrides: [
        themeModeProvider.overrideWith((ref) => settings.themeMode),
        localeProvider.overrideWith((ref) => settings.locale),
        fontSizeProvider.overrideWith((ref) => settings.fontSize),
        sharedPreferencesProvider.overrideWithValue(prefs),
        offlineEventQueueProvider.overrideWith(
          (ref) => OfflineEventQueue(
            store: FileOfflineEventStore(),
            deviceId: deviceId,
          ),
        ),
      ],
      child: const BfsApp(),
    ),
  );
}
