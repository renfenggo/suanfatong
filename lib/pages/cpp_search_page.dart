import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/knowledge_graph_provider.dart';
import '../state/cpp_learning_provider.dart';
import '../utils/cpp_search.dart';

class CppSearchPage extends ConsumerStatefulWidget {
  const CppSearchPage({super.key});

  @override
  ConsumerState<CppSearchPage> createState() => _CppSearchPageState();
}

class _CppSearchPageState extends ConsumerState<CppSearchPage> {
  final _controller = TextEditingController();
  String _query = '';

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final graphAsync = ref.watch(knowledgeGraphProvider);
    final contentAsync = ref.watch(cppLearningContentProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('搜索知识点')),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
              child: TextField(
                controller: _controller,
                autofocus: true,
                decoration: InputDecoration(
                  hintText: '搜索知识点、代码、常见错误...',
                  prefixIcon: const Icon(Icons.search),
                  suffixIcon:
                      _query.isNotEmpty
                          ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _controller.clear();
                              setState(() => _query = '');
                            },
                          )
                          : null,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  contentPadding: const EdgeInsets.symmetric(vertical: 12),
                ),
                onChanged: (v) => setState(() => _query = v),
              ),
            ),
            Expanded(
              child: graphAsync.when(
                data: (graph) {
                  return contentAsync.when(
                    data: (content) {
                      if (_query.trim().isEmpty) {
                        return _buildSuggestions();
                      }
                      final results = searchCppUnits(_query, graph, content);
                      if (results.isEmpty) {
                        return _buildEmpty();
                      }
                      return _buildResults(results);
                    },
                    loading:
                        () => const Center(child: CircularProgressIndicator()),
                    error:
                        (e, _) => Center(
                          child: Padding(
                            padding: const EdgeInsets.all(32),
                            child: Text(
                              '加载失败：$e',
                              style: const TextStyle(color: Color(0xFF888888)),
                            ),
                          ),
                        ),
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error:
                    (e, _) => Center(
                      child: Padding(
                        padding: const EdgeInsets.all(32),
                        child: Text(
                          '加载知识图谱失败：$e',
                          style: const TextStyle(color: Color(0xFF888888)),
                        ),
                      ),
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSuggestions() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.trending_up, size: 18, color: Color(0xFF00897B)),
              SizedBox(width: 6),
              Text(
                '常用搜索',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF00897B),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children:
                kCppSearchSuggestions.map((keyword) {
                  return ActionChip(
                    label: Text(keyword),
                    onPressed: () {
                      _controller.text = keyword;
                      setState(() => _query = keyword);
                    },
                  );
                }).toList(),
          ),
          const SizedBox(height: 24),
          const Row(
            children: [
              Icon(Icons.info_outline, size: 18, color: Color(0xFF888888)),
              SizedBox(width: 6),
              Text(
                '可搜索知识点名称、标题、学习目标、讲解、常见错误等',
                style: TextStyle(fontSize: 13, color: Color(0xFF888888)),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildEmpty() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.search_off, size: 56, color: Color(0xFFBDBDBD)),
            const SizedBox(height: 16),
            Text(
              '未找到与「$_query」相关的内容',
              style: const TextStyle(fontSize: 16, color: Color(0xFF888888)),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResults(List<CppSearchResult> results) {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      itemCount: results.length,
      itemBuilder: (context, index) {
        final r = results[index];
        return _SearchResultCard(result: r);
      },
    );
  }
}

class _SearchResultCard extends StatelessWidget {
  final CppSearchResult result;

  const _SearchResultCard({required this.result});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: InkWell(
        onTap: () {
          if (result.isCppItem) {
            Navigator.pushNamed(
              context,
              '/cpp_learning_unit',
              arguments: result.itemId,
            );
          } else {
            Navigator.pushNamed(
              context,
              '/knowledge/item',
              arguments: result.itemId,
            );
          }
        },
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
                      result.itemName,
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (result.hasUnit)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFE8F5E9),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text(
                        '可学习',
                        style: TextStyle(
                          fontSize: 10,
                          color: Color(0xFF4CAF50),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    )
                  else
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF5F5F5),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text(
                        '内容待补充',
                        style: TextStyle(
                          fontSize: 10,
                          color: Color(0xFF9E9E9E),
                        ),
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 4),
              Row(
                children: [
                  Text(
                    result.itemId,
                    style: const TextStyle(
                      fontSize: 12,
                      color: Color(0xFFBDBDBD),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      result.sectionName,
                      style: const TextStyle(
                        fontSize: 12,
                        color: Color(0xFF00897B),
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              if (result.summary.isNotEmpty) ...[
                const SizedBox(height: 6),
                Text(
                  result.summary,
                  style: const TextStyle(
                    fontSize: 13,
                    color: Color(0xFF666666),
                    height: 1.4,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
              const SizedBox(height: 6),
              Wrap(
                spacing: 4,
                runSpacing: 4,
                children:
                    result.sources.map((s) {
                      return Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 6,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: _sourceColor(s).withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          _sourceLabel(s),
                          style: TextStyle(
                            fontSize: 10,
                            color: _sourceColor(s),
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      );
                    }).toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _sourceLabel(CppSearchSource s) {
    return switch (s) {
      CppSearchSource.name => '知识点',
      CppSearchSource.alias => '别名',
      CppSearchSource.title => '标题',
      CppSearchSource.learningGoal => '学习目标',
      CppSearchSource.explanation => '讲解',
      CppSearchSource.codeNote => '代码注释',
      CppSearchSource.commonMistake => '常见错误',
      CppSearchSource.practice => '练习',
    };
  }

  Color _sourceColor(CppSearchSource s) {
    return switch (s) {
      CppSearchSource.name => const Color(0xFF00897B),
      CppSearchSource.alias => const Color(0xFF00897B),
      CppSearchSource.title => const Color(0xFF00897B),
      CppSearchSource.learningGoal => const Color(0xFF1976D2),
      CppSearchSource.explanation => const Color(0xFF888888),
      CppSearchSource.codeNote => const Color(0xFF888888),
      CppSearchSource.commonMistake => const Color(0xFFE67E22),
      CppSearchSource.practice => const Color(0xFF7B1FA2),
    };
  }
}
