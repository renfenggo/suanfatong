import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/cpp_animation_provider.dart';
import '../models/cpp_animation.dart';

class CppAnimationPage extends ConsumerStatefulWidget {
  final String animationId;

  const CppAnimationPage({super.key, required this.animationId});

  @override
  ConsumerState<CppAnimationPage> createState() => _CppAnimationPageState();
}

class _CppAnimationPageState extends ConsumerState<CppAnimationPage> {
  int _currentStep = 0;

  @override
  Widget build(BuildContext context) {
    if (widget.animationId.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('动画演示')),
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.error_outline,
                size: 56,
                color: Color(0xFF888888),
              ),
              const SizedBox(height: 16),
              const Text('未指定动画', style: TextStyle(fontSize: 18)),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('返回'),
              ),
            ],
          ),
        ),
      );
    }

    final animationAsync = ref.watch(cppAnimationProvider(widget.animationId));

    return Scaffold(
      appBar: AppBar(title: const Text('动画演示')),
      body: SafeArea(
        child: animationAsync.when(
          data: (animation) {
            if (animation.steps.isEmpty) {
              return _buildNoSteps(animation);
            }
            return _buildAnimation(animation);
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error:
              (e, _) => Center(
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
                      Text(
                        '加载动画失败',
                        style: const TextStyle(
                          fontSize: 18,
                          color: Color(0xFFE74C3C),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        e.toString(),
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 14,
                          color: Color(0xFF888888),
                        ),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('返回'),
                      ),
                    ],
                  ),
                ),
              ),
        ),
      ),
    );
  }

  Widget _buildNoSteps(CppAnimation animation) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.movie_outlined,
              size: 56,
              color: Color(0xFF888888),
            ),
            const SizedBox(height: 16),
            Text(
              animation.title,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              '该动画暂无步骤',
              style: TextStyle(fontSize: 16, color: Color(0xFF888888)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAnimation(CppAnimation animation) {
    final step = animation.steps[_currentStep];
    final total = animation.steps.length;
    final isFirst = _currentStep == 0;
    final isLast = _currentStep == total - 1;

    return Column(
      children: [
        _buildHeader(animation, _currentStep + 1, total),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildStepInfo(step),
                const SizedBox(height: 12),
                _buildCodeLine(step),
                const SizedBox(height: 12),
                _buildState(step.state),
                const SizedBox(height: 16),
                _buildControls(isFirst, isLast, total),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildHeader(CppAnimation animation, int current, int total) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 10),
      decoration: const BoxDecoration(
        color: Color(0xFFE0F2F1),
        border: Border(bottom: BorderSide(color: Color(0xFFB2DFDB))),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            animation.title,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00897B),
            ),
          ),
          if (animation.description.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              animation.description,
              style: const TextStyle(fontSize: 13, color: Color(0xFF666666)),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(3),
                  child: LinearProgressIndicator(
                    value: current / total,
                    backgroundColor: const Color(0xFFB2DFDB),
                    valueColor: const AlwaysStoppedAnimation<Color>(
                      Color(0xFF00897B),
                    ),
                    minHeight: 4,
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Text(
                '$current/$total',
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF00897B),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStepInfo(CppAnimationStep step) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              step.title,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: Color(0xFF00897B),
              ),
            ),
            const SizedBox(height: 6),
            Text(
              step.description,
              style: const TextStyle(fontSize: 14, height: 1.6),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCodeLine(CppAnimationStep step) {
    if (step.codeLine.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 6),
          child: Text(
            '代码',
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Color(0xFF888888),
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFF1E1E1E),
            borderRadius: BorderRadius.circular(10),
          ),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Text(
              step.codeLine,
              style: const TextStyle(
                fontFamily: 'monospace',
                fontSize: 14,
                color: Color(0xFFD4D4D4),
                height: 1.5,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildState(CppAnimationState state) {
    final hasVariables = state.variables.isNotEmpty;
    final hasContainers = state.containers.isNotEmpty;
    final hasOutput = state.output.isNotEmpty;

    if (!hasVariables && !hasContainers && !hasOutput) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4, bottom: 8),
          child: Text(
            '运行状态',
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Color(0xFF888888),
            ),
          ),
        ),
        if (hasVariables)
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children:
                state.variables.map((v) => _buildVariableCard(v)).toList(),
          ),
        if (hasVariables && hasContainers) const SizedBox(height: 8),
        if (hasContainers)
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children:
                state.containers.map((c) => _buildContainerCard(c)).toList(),
          ),
        if (hasOutput) ...[
          const SizedBox(height: 8),
          _buildOutput(state.output),
        ],
      ],
    );
  }

  Widget _buildVariableCard(CppAnimationVariable v) {
    return Container(
      constraints: const BoxConstraints(maxWidth: 180),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE0E0E0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            v.name,
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFF888888),
              fontWeight: FontWeight.w600,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 2),
          Text(
            v.value,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00897B),
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          if (v.note.isNotEmpty) ...[
            const SizedBox(height: 2),
            Text(
              v.note,
              style: const TextStyle(fontSize: 10, color: Color(0xFF9E9E9E)),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildContainerCard(CppAnimationContainer c) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFFE3F2FD),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFBBDEFB)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Flexible(
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Flexible(
                  child: Text(
                    c.name,
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF1976D2),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(width: 6),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 4,
                    vertical: 1,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFBBDEFB),
                    borderRadius: BorderRadius.circular(3),
                  ),
                  child: Text(
                    c.type,
                    style: const TextStyle(
                      fontSize: 9,
                      color: Color(0xFF1565C0),
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 6),
          Wrap(
            spacing: 4,
            runSpacing: 4,
            children: [
              for (var i = 0; i < c.values.length; i++)
                Container(
                  constraints: const BoxConstraints(minWidth: 36, maxWidth: 80),
                  height: 30,
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color:
                        i == c.activeIndex
                            ? const Color(0xFFFFCDD2)
                            : Colors.white,
                    borderRadius: BorderRadius.circular(4),
                    border: Border.all(
                      color:
                          i == c.activeIndex
                              ? const Color(0xFFE74C3C)
                              : const Color(0xFFBDBDBD),
                      width: i == c.activeIndex ? 2 : 1,
                    ),
                  ),
                  child: Text(
                    c.values[i],
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight:
                          i == c.activeIndex
                              ? FontWeight.bold
                              : FontWeight.normal,
                      color:
                          i == c.activeIndex
                              ? const Color(0xFFC62828)
                              : const Color(0xFF333333),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
            ],
          ),
          if (c.note.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              c.note,
              style: const TextStyle(fontSize: 10, color: Color(0xFF666666)),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildOutput(String output) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF263238),
        borderRadius: BorderRadius.circular(8),
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '输出',
              style: TextStyle(fontSize: 10, color: Color(0xFF78909C)),
            ),
            const SizedBox(height: 4),
            Text(
              output,
              style: const TextStyle(
                fontFamily: 'monospace',
                fontSize: 14,
                color: Color(0xFFA5D6A7),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildControls(bool isFirst, bool isLast, int total) {
    return Row(
      children: [
        Expanded(
          child: OutlinedButton.icon(
            onPressed: isFirst ? null : () => setState(() => _currentStep--),
            icon: const Icon(Icons.arrow_back),
            label: const Text('上一步'),
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child:
              isLast
                  ? ElevatedButton.icon(
                    onPressed: () => setState(() => _currentStep = 0),
                    icon: const Icon(Icons.refresh),
                    label: const Text('重置'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF00897B),
                      foregroundColor: Colors.white,
                    ),
                  )
                  : ElevatedButton.icon(
                    onPressed: () => setState(() => _currentStep++),
                    icon: const Icon(Icons.arrow_forward),
                    label: const Text('下一步'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF00897B),
                      foregroundColor: Colors.white,
                    ),
                  ),
        ),
      ],
    );
  }
}
