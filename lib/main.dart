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
  // 跨重启保留待上报事件与幂等键水位）。
  // N03 账号隔离：队列带命名空间工厂——启动为 unowned（未登录），
  // 登录/登出经 switchOwner 换用对应账号的文件（offline_event_queue_{ns}）；
  // 历史无后缀文件（升级前全局队列）不再被读写，未归属数据隔离保留。
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
            store: FileOfflineEventStore(namespace: null),
            deviceId: deviceId,
            storeFactory:
                (namespace) => FileOfflineEventStore(namespace: namespace),
          ),
        ),
      ],
      child: const BfsApp(),
    ),
  );
}
