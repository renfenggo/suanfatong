import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/bfs_step.dart';
import '../widgets/bfs_grid.dart';
import '../widgets/step_controller.dart';

class AnimationPage extends StatefulWidget {
  const AnimationPage({super.key});

  @override
  State<AnimationPage> createState() => _AnimationPageState();
}

class _AnimationPageState extends State<AnimationPage> {
  List<BfsStep> _steps = [];
  int _currentIndex = 0;
  bool _isPlaying = false;
  Timer? _timer;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadSteps();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
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
    if (_currentIndex > 0) {
      setState(() => _currentIndex--);
    }
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
    _timer = Timer.periodic(const Duration(milliseconds: 1200), (_) {
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
    return Scaffold(
      appBar: AppBar(title: const Text('BFS 动画演示')),
      body: SafeArea(child: _buildBody()),
    );
  }

  Widget _buildBody() {
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.error_outline,
                size: 56,
                color: Color(0xFFE74C3C),
              ),
              const SizedBox(height: 16),
              const Text(
                '加载动画数据失败',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFE74C3C),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                _error!,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 14, color: Color(0xFF888888)),
              ),
            ],
          ),
        ),
      );
    }

    if (_steps.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    final step = _current;

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      child: Column(
        children: [
          _buildInfoBar(step),
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
          _buildLegend(),
          const SizedBox(height: 12),
          _buildQueueDisplay(step),
          const SizedBox(height: 16),
          StepController(
            currentStep: _currentIndex,
            totalSteps: _steps.length,
            isPlaying: _isPlaying,
            onPrevious: _onPrevious,
            onNext: _onNext,
            onReset: _onReset,
            onPlayPause: _togglePlayPause,
          ),
          const SizedBox(height: 16),
          _buildDescription(step),
        ],
      ),
    );
  }

  Widget _buildInfoBar(BfsStep step) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: const Color(0xFFE3F2FD),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildInfoItem('当前层', '${step.layer}'),
          Container(width: 1, height: 20, color: const Color(0xFFBBDEFB)),
          _buildInfoItem('已访问', '${step.visited.length}'),
          Container(width: 1, height: 20, color: const Color(0xFFBBDEFB)),
          _buildInfoItem('队列', '${step.queue.length}'),
        ],
      ),
    );
  }

  Widget _buildInfoItem(String label, String value) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Color(0xFF666666)),
        ),
        Text(
          value,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1565C0),
          ),
        ),
      ],
    );
  }

  Widget _buildLegend() {
    return Wrap(
      spacing: 12,
      runSpacing: 4,
      alignment: WrapAlignment.center,
      children: [
        _legendItem(const Color(0xFF4CAF50), 'S 起点'),
        _legendItem(const Color(0xFFF44336), 'E 终点'),
        _legendItem(const Color(0xFF37474F), '# 墙'),
        _legendItem(const Color(0xFFE91E63), '当前'),
        _legendItem(const Color(0xFF42A5F5), '已访问'),
        _legendItem(const Color(0xFFFFEB3B), '队列中'),
        _legendItem(const Color(0xFFFF9800), '最短路'),
      ],
    );
  }

  Widget _legendItem(Color color, String text) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 14,
          height: 14,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(3),
          ),
        ),
        const SizedBox(width: 4),
        Text(
          text,
          style: const TextStyle(fontSize: 11, color: Color(0xFF666666)),
        ),
      ],
    );
  }

  Widget _buildQueueDisplay(BfsStep step) {
    final queue = step.queue;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
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
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Color(0xFF5D4037),
            ),
          ),
          const SizedBox(height: 6),
          if (queue.isEmpty)
            const Text(
              '（空）',
              style: TextStyle(fontSize: 13, color: Color(0xFF9E9E9E)),
            )
          else
            Wrap(
              spacing: 6,
              runSpacing: 4,
              children:
                  queue.map((q) {
                    final isHead = q == queue.first;
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 3,
                      ),
                      decoration: BoxDecoration(
                        color:
                            isHead
                                ? const Color(0xFFFF9800)
                                : const Color(0xFFFFE082),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        '($q)${isHead ? ' ← 队首' : ''}',
                        style: TextStyle(
                          fontSize: 12,
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

  Widget _buildDescription(BfsStep step) {
    final isFinal = step.path.isNotEmpty;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isFinal ? const Color(0xFFE8F5E9) : const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isFinal ? const Color(0xFFA5D6A7) : const Color(0xFFE0E0E0),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            isFinal ? Icons.celebration : Icons.lightbulb_outline,
            color: isFinal ? const Color(0xFF4CAF50) : const Color(0xFF4A90D9),
            size: 22,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              step.description,
              style: TextStyle(
                fontSize: 15,
                height: 1.6,
                color:
                    isFinal ? const Color(0xFF2E7D32) : const Color(0xFF333333),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
