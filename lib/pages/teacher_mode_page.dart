import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/bfs_step.dart';
import '../widgets/bfs_grid.dart';

class TeacherModePage extends StatefulWidget {
  const TeacherModePage({super.key});

  @override
  State<TeacherModePage> createState() => _TeacherModePageState();
}

class _TeacherModePageState extends State<TeacherModePage> {
  List<BfsStep> _steps = [];
  int _currentIndex = 0;
  bool _isPlaying = false;
  Timer? _timer;
  String? _error;
  bool _landscapeHintShown = false;

  @override
  void initState() {
    super.initState();
    _loadSteps();
    WidgetsBinding.instance.addPostFrameCallback((_) => _showLandscapeHint());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _showLandscapeHint() {
    if (_landscapeHintShown) return;
    final size = MediaQuery.of(context).size;
    if (size.width < size.height) {
      _landscapeHintShown = true;
      showDialog(
        context: context,
        builder:
            (ctx) => AlertDialog(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              title: const Row(
                children: [
                  Icon(
                    Icons.screen_rotation,
                    color: Color(0xFF4A90D9),
                    size: 28,
                  ),
                  SizedBox(width: 10),
                  Text('建议横屏使用'),
                ],
              ),
              content: const Text(
                '老师演示模式建议将设备横屏放置，可以获得更好的投屏效果。\n\n竖屏也可以正常使用，但横屏布局更适合课堂讲解。',
                style: TextStyle(fontSize: 15, height: 1.6),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('我知道了'),
                ),
              ],
            ),
      );
    }
  }

  Future<void> _loadSteps() async {
    try {
      final jsonStr = await rootBundle.loadString('assets/data/bfs_steps.json');
      final List<dynamic> jsonList = json.decode(jsonStr);
      final steps =
          jsonList
              .map((e) => BfsStep.fromJson(e as Map<String, dynamic>))
              .toList();
      setState(() {
        _steps = steps;
        _currentIndex = 0;
      });
    } catch (e) {
      setState(() => _error = e.toString());
    }
  }

  BfsStep get _current =>
      _steps.isNotEmpty
          ? _steps[_currentIndex]
          : const BfsStep(step: 0, description: '');

  void _onPrevious() {
    if (_currentIndex > 0) setState(() => _currentIndex--);
  }

  void _onNext() {
    if (_currentIndex < _steps.length - 1) {
      setState(() => _currentIndex++);
    } else {
      _stopPlaying();
    }
  }

  void _onReset() {
    _stopPlaying();
    setState(() => _currentIndex = 0);
  }

  void _togglePlayPause() {
    if (_isPlaying) {
      _stopPlaying();
    } else {
      _startPlaying();
    }
  }

  void _startPlaying() {
    if (_currentIndex >= _steps.length - 1) {
      setState(() => _currentIndex = 0);
    }
    setState(() => _isPlaying = true);
    _timer = Timer.periodic(const Duration(milliseconds: 1500), (_) {
      if (_currentIndex < _steps.length - 1) {
        setState(() => _currentIndex++);
      } else {
        _stopPlaying();
      }
    });
  }

  void _stopPlaying() {
    _timer?.cancel();
    _timer = null;
    setState(() => _isPlaying = false);
  }

  @override
  Widget build(BuildContext context) {
    final isLandscape =
        MediaQuery.of(context).size.width > MediaQuery.of(context).size.height;

    return Scaffold(
      appBar: AppBar(
        title: const Text('老师演示模式'),
        actions: [
          IconButton(
            icon: const Icon(Icons.screen_rotation),
            onPressed: _showLandscapeHint,
            tooltip: '横屏提示',
          ),
        ],
      ),
      body: SafeArea(
        child:
            _error != null
                ? _buildError()
                : _steps.isEmpty
                ? const Center(child: CircularProgressIndicator())
                : isLandscape
                ? _buildLandscapeLayout()
                : _buildPortraitLayout(),
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.error_outline, size: 56, color: Color(0xFFE74C3C)),
          const SizedBox(height: 16),
          Text(_error!, textAlign: TextAlign.center),
        ],
      ),
    );
  }

  Widget _buildLandscapeLayout() {
    final step = _current;
    return Column(
      children: [
        Expanded(
          child: Row(
            children: [
              Expanded(
                flex: 5,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Center(
                    child: BfsGrid(
                      rows: 5,
                      cols: 5,
                      visited: step.visited,
                      queue: step.queue,
                      current: step.current,
                      walls: step.walls,
                      path: step.path,
                      start: step.start,
                      end: step.end,
                    ),
                  ),
                ),
              ),
              Expanded(
                flex: 5,
                child: SingleChildScrollView(
                  padding: const EdgeInsets.fromLTRB(0, 16, 16, 16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildTeacherInfoBar(step),
                      const SizedBox(height: 12),
                      _buildTeacherLegend(),
                      const SizedBox(height: 12),
                      _buildTeacherQueue(step),
                      const SizedBox(height: 12),
                      _buildTeacherDescription(step),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
        _buildTeacherControls(),
      ],
    );
  }

  Widget _buildPortraitLayout() {
    final step = _current;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          _buildTeacherInfoBar(step),
          const SizedBox(height: 12),
          BfsGrid(
            rows: 5,
            cols: 5,
            visited: step.visited,
            queue: step.queue,
            current: step.current,
            walls: step.walls,
            path: step.path,
            start: step.start,
            end: step.end,
          ),
          const SizedBox(height: 12),
          _buildTeacherLegend(),
          const SizedBox(height: 12),
          _buildTeacherQueue(step),
          const SizedBox(height: 12),
          _buildTeacherDescription(step),
          const SizedBox(height: 16),
          _buildTeacherControls(),
        ],
      ),
    );
  }

  Widget _buildTeacherInfoBar(BfsStep step) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF1565C0),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildTeacherInfoItem('当前层', '${step.layer}', 22),
          Container(width: 1, height: 30, color: Colors.white24),
          _buildTeacherInfoItem('已访问', '${step.visited.length}', 22),
          Container(width: 1, height: 30, color: Colors.white24),
          _buildTeacherInfoItem('队列', '${step.queue.length}', 22),
          Container(width: 1, height: 30, color: Colors.white24),
          _buildTeacherInfoItem('步数', '${step.step}', 22),
        ],
      ),
    );
  }

  Widget _buildTeacherInfoItem(String label, String value, double fontSize) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: fontSize,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Color(0xFFBBDEFB)),
        ),
      ],
    );
  }

  Widget _buildTeacherLegend() {
    return Wrap(
      spacing: 16,
      runSpacing: 6,
      children: [
        _teacherLegendItem(const Color(0xFF4CAF50), 'S 起点', 14),
        _teacherLegendItem(const Color(0xFFF44336), 'E 终点', 14),
        _teacherLegendItem(const Color(0xFF37474F), '# 墙壁', 14),
        _teacherLegendItem(const Color(0xFFE91E63), '当前处理', 14),
        _teacherLegendItem(const Color(0xFF42A5F5), '已访问', 14),
        _teacherLegendItem(const Color(0xFFFFEB3B), '队列中', 14),
        _teacherLegendItem(const Color(0xFFFF9800), '最短路径', 14),
      ],
    );
  }

  Widget _teacherLegendItem(Color color, String text, double fontSize) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 18,
          height: 18,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(4),
          ),
        ),
        const SizedBox(width: 5),
        Text(
          text,
          style: TextStyle(fontSize: fontSize, fontWeight: FontWeight.w500),
        ),
      ],
    );
  }

  Widget _buildTeacherQueue(BfsStep step) {
    final queue = step.queue;
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFDE7),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFFFE082)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '队列内容：',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF5D4037),
            ),
          ),
          const SizedBox(height: 8),
          if (queue.isEmpty)
            const Text(
              '（空）',
              style: TextStyle(fontSize: 15, color: Color(0xFF9E9E9E)),
            )
          else
            Wrap(
              spacing: 8,
              runSpacing: 6,
              children:
                  queue.map((q) {
                    final isHead = q == queue.first;
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 5,
                      ),
                      decoration: BoxDecoration(
                        color:
                            isHead
                                ? const Color(0xFFFF9800)
                                : const Color(0xFFFFE082),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '($q)${isHead ? ' ← 队首' : ''}',
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight:
                              isHead ? FontWeight.bold : FontWeight.normal,
                          color:
                              isHead ? Colors.white : const Color(0xFF5D4037),
                        ),
                      ),
                    );
                  }).toList(),
            ),
        ],
      ),
    );
  }

  Widget _buildTeacherDescription(BfsStep step) {
    final isFinal = step.path.isNotEmpty;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isFinal ? const Color(0xFFE8F5E9) : const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isFinal ? const Color(0xFF66BB6A) : const Color(0xFFE0E0E0),
          width: 2,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            isFinal ? Icons.celebration : Icons.lightbulb,
            color: isFinal ? const Color(0xFF4CAF50) : const Color(0xFF4A90D9),
            size: 26,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              step.description,
              style: TextStyle(
                fontSize: 17,
                height: 1.7,
                fontWeight: FontWeight.w500,
                color:
                    isFinal ? const Color(0xFF2E7D32) : const Color(0xFF333333),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTeacherControls() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFFFAFAFA),
        border: Border(top: BorderSide(color: const Color(0xFFE0E0E0))),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            '第 ${_currentIndex + 1} / ${_steps.length} 步',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(width: 24),
          IconButton.outlined(
            onPressed: _onReset,
            icon: const Icon(Icons.refresh, size: 28),
            tooltip: '重置',
          ),
          const SizedBox(width: 8),
          IconButton.filledTonal(
            onPressed: _currentIndex > 0 ? _onPrevious : null,
            icon: const Icon(Icons.skip_previous, size: 28),
            tooltip: '上一步',
          ),
          const SizedBox(width: 8),
          FloatingActionButton(
            onPressed: _togglePlayPause,
            backgroundColor:
                _isPlaying ? const Color(0xFFE74C3C) : const Color(0xFF4CAF50),
            child: Icon(
              _isPlaying ? Icons.pause : Icons.play_arrow,
              size: 32,
              color: Colors.white,
            ),
          ),
          const SizedBox(width: 8),
          IconButton.filledTonal(
            onPressed: _currentIndex < _steps.length - 1 ? _onNext : null,
            icon: const Icon(Icons.skip_next, size: 28),
            tooltip: '下一步',
          ),
        ],
      ),
    );
  }
}
