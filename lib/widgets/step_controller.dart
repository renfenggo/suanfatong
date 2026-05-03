import 'package:flutter/material.dart';

class StepController extends StatelessWidget {
  final int currentStep;
  final int totalSteps;
  final bool isPlaying;
  final VoidCallback? onPrevious;
  final VoidCallback? onNext;
  final VoidCallback? onReset;
  final VoidCallback? onPlayPause;

  const StepController({
    super.key,
    required this.currentStep,
    required this.totalSteps,
    this.isPlaying = false,
    this.onPrevious,
    this.onNext,
    this.onReset,
    this.onPlayPause,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          '第 ${currentStep + 1} / $totalSteps 步',
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            IconButton.outlined(
              onPressed: onReset,
              icon: const Icon(Icons.refresh),
              tooltip: '重置',
            ),
            const SizedBox(width: 8),
            IconButton.filledTonal(
              onPressed: currentStep > 0 ? onPrevious : null,
              icon: const Icon(Icons.skip_previous),
              tooltip: '上一步',
            ),
            const SizedBox(width: 8),
            FloatingActionButton.small(
              onPressed: onPlayPause,
              backgroundColor:
                  isPlaying ? const Color(0xFFE74C3C) : const Color(0xFF4CAF50),
              child: Icon(
                isPlaying ? Icons.pause : Icons.play_arrow,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 8),
            IconButton.filledTonal(
              onPressed: currentStep < totalSteps - 1 ? onNext : null,
              icon: const Icon(Icons.skip_next),
              tooltip: '下一步',
            ),
          ],
        ),
      ],
    );
  }
}
