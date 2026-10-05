import 'package:flutter/material.dart';
import '../../models/cpp14_template_entry.dart';

/// C++14 模板入口区域
/// 展示某个知识点对应的 C++14 代码模板入口
/// 注意：只展示入口信息，不直接塞大段代码到知识点页
class Cpp14TemplateEntrySection extends StatelessWidget {
  final Cpp14TemplateEntry entry;
  final VoidCallback? onViewTemplate;

  const Cpp14TemplateEntrySection({
    super.key,
    required this.entry,
    this.onViewTemplate,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 10),
          child: Row(
            children: [
              Icon(
                Icons.description,
                size: 20,
                color: const Color(0xFF1565C0).withValues(alpha: 0.9),
              ),
              const SizedBox(width: 6),
              const Text(
                'C++14 模板',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF1565C0),
                ),
              ),
            ],
          ),
        ),
        Card(
          elevation: 0,
          color: const Color(0xFFE3F2FD),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: BorderSide(
              color: const Color(0xFF1565C0).withValues(alpha: 0.2),
            ),
          ),
          child: InkWell(
            onTap: entry.hasSource ? onViewTemplate : null,
            borderRadius: BorderRadius.circular(12),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          entry.title,
                          style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w700,
                            color: Color(0xFF1565C0),
                          ),
                        ),
                      ),
                      if (entry.hasSource)
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 3,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(
                              0xFF1565C0,
                            ).withValues(alpha: 0.12),
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: const Text(
                            '可查看',
                            style: TextStyle(
                              fontSize: 11,
                              color: Color(0xFF1565C0),
                            ),
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  _buildInfoRow('类型', entry.templateType),
                  if (entry.complexity.isNotEmpty)
                    _buildInfoRow('复杂度', entry.complexity),
                  if (entry.difficulty.isNotEmpty)
                    _buildInfoRow('难度', entry.difficulty),
                  if (entry.templateInfo.usageScenario.isNotEmpty)
                    _buildInfoRow('场景', entry.templateInfo.usageScenario),
                  const SizedBox(height: 8),
                  if (entry.templateInfo.keyConcepts.isNotEmpty) ...[
                    const Text(
                      '关键概念',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF1565C0),
                      ),
                    ),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 6,
                      runSpacing: 4,
                      children:
                          entry.templateInfo.keyConcepts
                              .map(
                                (c) => Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 8,
                                    vertical: 3,
                                  ),
                                  decoration: BoxDecoration(
                                    color: const Color(
                                      0xFF1565C0,
                                    ).withValues(alpha: 0.08),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Text(
                                    c,
                                    style: const TextStyle(
                                      fontSize: 12,
                                      color: Color(0xFF1565C0),
                                    ),
                                  ),
                                ),
                              )
                              .toList(),
                    ),
                  ],
                  const SizedBox(height: 10),
                  const Text(
                    '模板代码',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF1565C0),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Container(
                    width: double.infinity,
                    height: 180,
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0D2238),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: SingleChildScrollView(
                      child: SelectableText(
                        entry.templateCode,
                        style: const TextStyle(
                          fontSize: 11,
                          height: 1.35,
                          color: Color(0xFFE3F2FD),
                          fontFamily: 'monospace',
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 56,
            child: Text(
              label,
              style: const TextStyle(fontSize: 12, color: Color(0xFF90A4AE)),
            ),
          ),
          Expanded(
            child: Text(
              value.isEmpty ? '—' : value,
              style: const TextStyle(fontSize: 12, color: Color(0xFF455A64)),
            ),
          ),
        ],
      ),
    );
  }
}
