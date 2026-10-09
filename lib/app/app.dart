import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../pages/settings_page.dart';
import '../state/cloud_sync_provider.dart';
import 'app_router.dart';
import 'theme.dart';

class BfsApp extends ConsumerStatefulWidget {
  const BfsApp({super.key});

  @override
  ConsumerState<BfsApp> createState() => _BfsAppState();
}

class _BfsAppState extends ConsumerState<BfsApp> {
  @override
  void initState() {
    super.initState();
    // R06-2（GO_LIVE §3.4b）：启动即自动同步调度（默认 5 分钟周期，
    // 兼网络恢复重试语义；未登录轮次 skippedNoCredentials 无副作用）。
    ref.read(cloudSyncSchedulerProvider).start();
  }

  @override
  Widget build(BuildContext context) {
    final themeMode = ref.watch(themeModeProvider);
    final locale = ref.watch(localeProvider);
    return MaterialApp.router(
      title: '算法通',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      locale: locale,
      supportedLocales: AppSupportedLocales.all,
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      routerConfig: appRouter,
      debugShowCheckedModeBanner: false,
    );
  }
}
