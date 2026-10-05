import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/cpp_animation.dart';
import '../state/cpp_animation_provider.dart';

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
              const Icon(Icons.error_outline, size: 56, color: Color(0xFF888888)),
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
            if (animation.steps.isEmpty) return _buildNoSteps(animation);
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
                      const Text(
                        '加载动画失败',
                        style: TextStyle(fontSize: 18, color: Color(0xFFE74C3C)),
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
            const Icon(Icons.movie_outlined, size: 56, color: Color(0xFF888888)),
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
            padding: const EdgeInsets.fromLTRB(16, 10, 16, 16),
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
              fontSize: 17,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00695C),
            ),
          ),
          if (animation.description.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              animation.description,
              style: const TextStyle(fontSize: 13, color: Color(0xFF455A64)),
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
                    minHeight: 5,
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Text(
                '$current/$total',
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFF00695C),
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
                fontWeight: FontWeight.w700,
                color: Color(0xFF00695C),
              ),
            ),
            const SizedBox(height: 6),
            Text(step.description, style: const TextStyle(fontSize: 14, height: 1.6)),
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
        const _SectionTitle(icon: Icons.code, label: '当前代码'),
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
    if (!hasVariables && !hasContainers && !hasOutput) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionTitle(icon: Icons.account_tree_outlined, label: '运行状态'),
        if (hasVariables) _buildVariables(state.variables),
        if (hasVariables && hasContainers) const SizedBox(height: 10),
        if (hasContainers)
          Column(
            children:
                state.containers
                    .map(
                      (c) => Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: _buildContainerCard(c),
                      ),
                    )
                    .toList(),
          ),
        if (hasOutput) _buildOutput(state.output),
      ],
    );
  }

  Widget _buildVariables(List<CppAnimationVariable> variables) {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: variables.map((v) => _buildVariableCard(v)).toList(),
    );
  }

  Widget _buildVariableCard(CppAnimationVariable v) {
    return Container(
      constraints: const BoxConstraints(minWidth: 112, maxWidth: 190),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
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
              color: Color(0xFF607D8B),
              fontWeight: FontWeight.w700,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 3),
          Text(
            v.value,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Color(0xFF00695C),
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          if (v.note.isNotEmpty) ...[
            const SizedBox(height: 3),
            Text(
              v.note,
              style: const TextStyle(fontSize: 10, color: Color(0xFF78909C)),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildContainerCard(CppAnimationContainer c) {
    if (c.type == 'graph' && _hasGraphNodeData(c)) return _buildGraphContainerCard(c);
    if (c.isMatrix || c.type == 'grid' || c.type == 'int[][]') {
      return _buildMatrixContainerCard(c);
    }
    return _buildLinearContainerCard(c);
  }

  bool _hasGraphNodeData(CppAnimationContainer c) {
    return c.values.any((value) => value is Map && value.containsKey('id'));
  }

  Widget _buildLinearContainerCard(CppAnimationContainer c) {
    final values = c.flatValues;
    final isStack = c.type == 'stack' || c.name.contains('栈');
    final isQueue = c.type == 'queue' || c.name.contains('队列') || c.name == 'q';

    return _ContainerShell(
      name: c.name,
      type: c.type,
      note: c.note,
      child:
          values.isEmpty
              ? const Text('空', style: TextStyle(color: Color(0xFF78909C)))
              : Wrap(
                spacing: 6,
                runSpacing: 8,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  if (isQueue) const _DirectionLabel('队首'),
                  for (var i = 0; i < values.length; i++)
                    _ValueCell(
                      value: values[i],
                      index: i,
                      active: i == c.activeIndex,
                      compact: values.length > 10,
                      showIndex: !isStack && !isQueue,
                    ),
                  if (isQueue) const _DirectionLabel('队尾'),
                  if (isStack) const _DirectionLabel('栈顶在右'),
                ],
              ),
    );
  }

  Widget _buildMatrixContainerCard(CppAnimationContainer c) {
    final rows = c.matrixValues.isNotEmpty ? c.matrixValues : _rowsFromFlat(c.flatValues);
    return _ContainerShell(
      name: c.name,
      type: c.type,
      note: c.note,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            for (var r = 0; r < rows.length; r++)
              Padding(
                padding: const EdgeInsets.only(bottom: 5),
                child: Row(
                  children: [
                    for (var col = 0; col < rows[r].length; col++)
                      Padding(
                        padding: const EdgeInsets.only(right: 5),
                        child: _ValueCell(
                          value: rows[r][col],
                          index: col,
                          active: _matrixFlatIndex(rows, r, col) == c.activeIndex,
                          compact: true,
                          showIndex: false,
                        ),
                      ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  List<List<String>> _rowsFromFlat(List<String> values) {
    if (values.isEmpty) return const [];
    final width = values.length <= 4 ? values.length : 4;
    final rows = <List<String>>[];
    for (var i = 0; i < values.length; i += width) {
      rows.add(values.sublist(i, (i + width).clamp(0, values.length)));
    }
    return rows;
  }

  int _matrixFlatIndex(List<List<String>> rows, int r, int c) {
    var index = 0;
    for (var i = 0; i < r; i++) {
      index += rows[i].length;
    }
    return index + c;
  }

  Widget _buildGraphContainerCard(CppAnimationContainer c) {
    final nodeStates = <String, String>{};
    for (final value in c.values) {
      if (value is Map) {
        final id = value['id']?.toString();
        final status = value['status']?.toString() ?? 'unvisited';
        if (id != null && id.isNotEmpty) nodeStates[id] = status;
      }
    }

    const positions = <String, Offset>{
      '0': Offset(0.50, 0.12),
      '1': Offset(0.28, 0.45),
      '2': Offset(0.72, 0.45),
      '3': Offset(0.14, 0.80),
      '4': Offset(0.42, 0.80),
      '5': Offset(0.86, 0.80),
    };

    return _ContainerShell(
      name: c.name,
      type: c.type,
      note: c.note,
      trailing: const Text(
        '灰=未访问 蓝=已访问 红=当前',
        style: TextStyle(fontSize: 10, color: Color(0xFF607D8B)),
      ),
      child: SizedBox(
        height: 168,
        child: LayoutBuilder(
          builder: (context, constraints) {
            return Stack(
              children: [
                Positioned.fill(
                  child: CustomPaint(
                    painter: _DfsGraphPainter(
                      positions: positions,
                      nodeStates: nodeStates,
                    ),
                  ),
                ),
                for (final entry in positions.entries)
                  Positioned(
                    left: entry.value.dx * constraints.maxWidth - 18,
                    top: entry.value.dy * constraints.maxHeight - 18,
                    child: _GraphNode(
                      label: entry.key,
                      status: nodeStates[entry.key] ?? 'unvisited',
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildOutput(String output) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 2),
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
            const Text('输出', style: TextStyle(fontSize: 10, color: Color(0xFF78909C))),
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

class _SectionTitle extends StatelessWidget {
  final IconData icon;
  final String label;

  const _SectionTitle({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 2, bottom: 6),
      child: Row(
        children: [
          Icon(icon, size: 16, color: const Color(0xFF607D8B)),
          const SizedBox(width: 5),
          Text(
            label,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w700,
              color: Color(0xFF607D8B),
            ),
          ),
        ],
      ),
    );
  }
}

class _ContainerShell extends StatelessWidget {
  final String name;
  final String type;
  final String note;
  final Widget child;
  final Widget? trailing;

  const _ContainerShell({
    required this.name,
    required this.type,
    required this.note,
    required this.child,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF7FBFF),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFBBDEFB)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  name,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: Color(0xFF1565C0),
                  ),
                ),
              ),
              if (trailing != null) trailing!,
              if (trailing == null)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: const Color(0xFFBBDEFB),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    type,
                    style: const TextStyle(fontSize: 10, color: Color(0xFF1565C0)),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 9),
          child,
          if (note.isNotEmpty) ...[
            const SizedBox(height: 7),
            Text(note, style: const TextStyle(fontSize: 11, color: Color(0xFF455A64))),
          ],
        ],
      ),
    );
  }
}

class _ValueCell extends StatelessWidget {
  final String value;
  final int index;
  final bool active;
  final bool compact;
  final bool showIndex;

  const _ValueCell({
    required this.value,
    required this.index,
    required this.active,
    required this.compact,
    required this.showIndex,
  });

  @override
  Widget build(BuildContext context) {
    final width = compact ? 44.0 : 54.0;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (showIndex)
          Text(
            '$index',
            style: const TextStyle(fontSize: 10, color: Color(0xFF90A4AE)),
          ),
        Container(
          constraints: BoxConstraints(minWidth: width, maxWidth: compact ? 68 : 92),
          height: 34,
          padding: const EdgeInsets.symmetric(horizontal: 5),
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: active ? const Color(0xFFFFCDD2) : Colors.white,
            borderRadius: BorderRadius.circular(6),
            border: Border.all(
              color: active ? const Color(0xFFE53935) : const Color(0xFFB0BEC5),
              width: active ? 2 : 1,
            ),
          ),
          child: Text(
            value,
            style: TextStyle(
              fontSize: compact ? 12 : 13,
              fontWeight: active ? FontWeight.bold : FontWeight.w500,
              color: active ? const Color(0xFFC62828) : const Color(0xFF263238),
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }
}

class _DirectionLabel extends StatelessWidget {
  final String label;

  const _DirectionLabel(this.label);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 4),
      decoration: BoxDecoration(
        color: const Color(0xFFE0F2F1),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        label,
        style: const TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w700,
          color: Color(0xFF00695C),
        ),
      ),
    );
  }
}

class _GraphNode extends StatelessWidget {
  final String label;
  final String status;

  const _GraphNode({required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    final isActive = status == 'active';
    final isVisited = status == 'visited' || isActive;
    final bg =
        isActive
            ? const Color(0xFFFFCDD2)
            : isVisited
            ? const Color(0xFFBBDEFB)
            : Colors.white;
    final border =
        isActive
            ? const Color(0xFFE53935)
            : isVisited
            ? const Color(0xFF1976D2)
            : const Color(0xFFB0BEC5);

    return Container(
      width: 36,
      height: 36,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: bg,
        shape: BoxShape.circle,
        border: Border.all(color: border, width: isActive ? 3 : 2),
        boxShadow:
            isActive
                ? [
                  BoxShadow(
                    color: const Color(0xFFE53935).withValues(alpha: 0.24),
                    blurRadius: 10,
                    spreadRadius: 1,
                  ),
                ]
                : null,
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 15,
          fontWeight: FontWeight.bold,
          color: isActive ? const Color(0xFFC62828) : const Color(0xFF263238),
        ),
      ),
    );
  }
}

class _DfsGraphPainter extends CustomPainter {
  final Map<String, Offset> positions;
  final Map<String, String> nodeStates;

  const _DfsGraphPainter({required this.positions, required this.nodeStates});

  static const _edges = <(String, String)>[
    ('0', '1'),
    ('0', '2'),
    ('1', '3'),
    ('1', '4'),
    ('2', '5'),
  ];

  @override
  void paint(Canvas canvas, Size size) {
    for (final edge in _edges) {
      final a = positions[edge.$1];
      final b = positions[edge.$2];
      if (a == null || b == null) continue;

      final aStatus = nodeStates[edge.$1] ?? 'unvisited';
      final bStatus = nodeStates[edge.$2] ?? 'unvisited';
      final activeEdge = aStatus == 'active' || bStatus == 'active';
      final visitedEdge =
          aStatus != 'unvisited' && bStatus != 'unvisited' && !activeEdge;

      final paint =
          Paint()
            ..color =
                activeEdge
                    ? const Color(0xFFE53935)
                    : visitedEdge
                    ? const Color(0xFF1976D2)
                    : const Color(0xFFB0BEC5)
            ..strokeWidth = activeEdge ? 3 : 2
            ..style = PaintingStyle.stroke;

      canvas.drawLine(
        Offset(a.dx * size.width, a.dy * size.height),
        Offset(b.dx * size.width, b.dy * size.height),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _DfsGraphPainter oldDelegate) {
    return oldDelegate.nodeStates != nodeStates ||
        oldDelegate.positions != positions;
  }
}
