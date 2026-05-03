import 'package:flutter/material.dart';

class QuizCard extends StatelessWidget {
  final String question;
  final List<String> options;
  final int? selectedIndex;
  final ValueChanged<int>? onOptionSelected;

  const QuizCard({
    super.key,
    required this.question,
    required this.options,
    this.selectedIndex,
    this.onOptionSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              question,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 12),
            ...List.generate(options.length, (index) {
              final isSelected = selectedIndex == index;
              return Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: InkWell(
                  onTap: () => onOptionSelected?.call(index),
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color:
                          isSelected
                              ? Theme.of(context).colorScheme.primaryContainer
                              : const Color(0xFFF8F8F8),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color:
                            isSelected
                                ? Theme.of(context).colorScheme.primary
                                : const Color(0xFFE0E0E0),
                      ),
                    ),
                    child: Text(
                      '${String.fromCharCode(65 + index)}. ${options[index]}',
                      style: TextStyle(
                        fontSize: 15,
                        color:
                            isSelected
                                ? Theme.of(context).colorScheme.primary
                                : Colors.black87,
                      ),
                    ),
                  ),
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}
