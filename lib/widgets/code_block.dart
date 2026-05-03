import 'package:flutter/material.dart';

class CodeBlock extends StatelessWidget {
  final String code;
  final String? language;

  const CodeBlock({super.key, required this.code, this.language});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE0E0E0)),
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: SelectableText(
          code,
          style: const TextStyle(
            fontFamily: 'Courier',
            fontSize: 14,
            height: 1.5,
          ),
        ),
      ),
    );
  }
}
