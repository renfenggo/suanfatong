import 'package:flutter/material.dart';

class BfsGrid extends StatelessWidget {
  final int rows;
  final int cols;
  final Set<String> visited;
  final List<String> queue;
  final String? current;
  final Set<String> walls;
  final Set<String> path;
  final String start;
  final String end;

  const BfsGrid({
    super.key,
    this.rows = 5,
    this.cols = 5,
    this.visited = const {},
    this.queue = const [],
    this.current,
    this.walls = const {},
    this.path = const {},
    this.start = '0,0',
    this.end = '4,4',
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final maxWidth = constraints.maxWidth;
        final gridSize =
            maxWidth.isFinite
                ? maxWidth
                : (MediaQuery.of(context).size.width - 32);

        return SizedBox(
          width: gridSize,
          height: gridSize,
          child: GridView.builder(
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: cols,
              mainAxisSpacing: 3,
              crossAxisSpacing: 3,
            ),
            itemCount: rows * cols,
            itemBuilder: (context, index) {
              final row = index ~/ cols;
              final col = index % cols;
              final key = '$row,$col';
              return _buildCell(key, row, col);
            },
          ),
        );
      },
    );
  }

  Widget _buildCell(String key, int row, int col) {
    final isWall = walls.contains(key);
    final isStart = key == start;
    final isEnd = key == end;
    final isCurrent = key == current;
    final isOnPath = path.contains(key);
    final isVisited = visited.contains(key);
    final isInQueue = queue.contains(key);

    Color bgColor;
    Color textColor;
    String label = '';
    double fontSize = 11;

    if (isWall) {
      bgColor = const Color(0xFF37474F);
      textColor = Colors.white;
      label = '#';
      fontSize = 16;
    } else if (isOnPath && path.isNotEmpty) {
      bgColor = const Color(0xFFFF9800);
      textColor = Colors.white;
      label = '★';
      fontSize = 16;
      if (isStart) label = 'S★';
      if (isEnd) label = 'E★';
    } else if (isStart) {
      bgColor = const Color(0xFF4CAF50);
      textColor = Colors.white;
      label = 'S';
      fontSize = 18;
    } else if (isEnd) {
      bgColor = const Color(0xFFF44336);
      textColor = Colors.white;
      label = 'E';
      fontSize = 18;
    } else if (isCurrent) {
      bgColor = const Color(0xFFE91E63);
      textColor = Colors.white;
      label = '$row,$col';
    } else if (isVisited) {
      bgColor = const Color(0xFF42A5F5);
      textColor = Colors.white;
      label = '$row,$col';
    } else if (isInQueue) {
      bgColor = const Color(0xFFFFEB3B);
      textColor = const Color(0xFF5D4037);
      label = '$row,$col';
    } else {
      bgColor = Colors.white;
      textColor = const Color(0xFF9E9E9E);
      label = '$row,$col';
    }

    return Container(
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(
          color:
              isCurrent
                  ? const Color(0xFFC2185B)
                  : (isOnPath && path.isNotEmpty
                      ? const Color(0xFFE65100)
                      : const Color(0xFFBDBDBD)),
          width: isCurrent || (isOnPath && path.isNotEmpty) ? 2.5 : 1,
        ),
        boxShadow:
            isCurrent
                ? [
                  BoxShadow(
                    color: const Color(0xFFE91E63).withValues(alpha: 0.4),
                    blurRadius: 6,
                    spreadRadius: 1,
                  ),
                ]
                : null,
      ),
      child: Center(
        child: Text(
          label,
          style: TextStyle(
            fontSize: fontSize,
            fontWeight:
                isCurrent || isStart || isEnd || isOnPath
                    ? FontWeight.bold
                    : FontWeight.normal,
            color: textColor,
          ),
        ),
      ),
    );
  }
}
