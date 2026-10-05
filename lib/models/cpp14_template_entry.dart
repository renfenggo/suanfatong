class Cpp14TemplatePracticeProblem {
  final String problemType;
  final String platform;
  final String problemId;
  final String title;

  const Cpp14TemplatePracticeProblem({
    required this.problemType,
    required this.platform,
    required this.problemId,
    required this.title,
  });

  factory Cpp14TemplatePracticeProblem.fromJson(Map<String, dynamic> json) {
    return Cpp14TemplatePracticeProblem(
      problemType: json['problem_type'] as String? ?? '',
      platform: json['platform'] as String? ?? '',
      problemId: json['problem_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
    );
  }
}

class Cpp14TemplateInfo {
  final List<String> keyConcepts;
  final List<String> templateFunctions;
  final List<String> commonVariants;
  final String usageScenario;

  const Cpp14TemplateInfo({
    required this.keyConcepts,
    required this.templateFunctions,
    required this.commonVariants,
    required this.usageScenario,
  });

  factory Cpp14TemplateInfo.fromJson(Map<String, dynamic> json) {
    return Cpp14TemplateInfo(
      keyConcepts: parseStringList(json['key_concepts']),
      templateFunctions: parseStringList(json['template_functions']),
      commonVariants: parseStringList(json['common_variants']),
      usageScenario: json['usage_scenario'] as String? ?? '',
    );
  }

  static List<String> parseStringList(dynamic value) {
    if (value is List) return value.map((e) => e.toString()).toList();
    return [];
  }
}

class Cpp14CodeReference {
  final String templateSignature;
  final List<String> requiredIncludes;
  final List<String> dataStructures;

  const Cpp14CodeReference({
    this.templateSignature = '',
    this.requiredIncludes = const [],
    this.dataStructures = const [],
  });

  factory Cpp14CodeReference.fromJson(Map<String, dynamic> json) {
    return Cpp14CodeReference(
      templateSignature: json['template_signature'] as String? ?? '',
      requiredIncludes: Cpp14TemplateInfo.parseStringList(
        json['required_includes'],
      ),
      dataStructures: Cpp14TemplateInfo.parseStringList(
        json['data_structures'],
      ),
    );
  }
}

class Cpp14TemplateEntry {
  final String itemId;
  final String title;
  final String sectionId;
  final String sectionName;
  final String templateType;
  final String difficulty;
  final String complexity;
  final String sourceFile;
  final Cpp14TemplateInfo templateInfo;
  final Cpp14CodeReference codeReference;
  final List<Cpp14TemplatePracticeProblem> practiceProblems;

  const Cpp14TemplateEntry({
    required this.itemId,
    required this.title,
    required this.sectionId,
    required this.sectionName,
    required this.templateType,
    required this.difficulty,
    required this.complexity,
    required this.sourceFile,
    required this.templateInfo,
    this.codeReference = const Cpp14CodeReference(),
    required this.practiceProblems,
  });

  factory Cpp14TemplateEntry.fromJson(Map<String, dynamic> json) {
    final problemsRaw = json['practice_problems'] as List<dynamic>? ?? [];
    return Cpp14TemplateEntry(
      itemId: json['item_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      sectionId: json['section_id'] as String? ?? '',
      sectionName: json['section_name'] as String? ?? '',
      templateType: json['template_type'] as String? ?? '',
      difficulty: json['difficulty'] as String? ?? '',
      complexity: json['complexity'] as String? ?? '',
      sourceFile: json['source_file'] as String? ?? '',
      templateInfo: Cpp14TemplateInfo.fromJson(
        (json['template_info'] as Map<String, dynamic>?) ?? {},
      ),
      codeReference: Cpp14CodeReference.fromJson(
        (json['code_reference'] as Map<String, dynamic>?) ?? {},
      ),
      practiceProblems:
          problemsRaw
              .map(
                (e) => Cpp14TemplatePracticeProblem.fromJson(
                  e as Map<String, dynamic>,
                ),
              )
              .toList(),
    );
  }

  bool get isValid => itemId.isNotEmpty && title.isNotEmpty;

  bool get hasSource => sourceFile.isNotEmpty;

  String get templateCode {
    if (itemId == '2.7.16') {
      return '''#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> adj;
vector<int> visited;

void dfs(int u) {
    visited[u] = 1;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    adj.assign(n + 1, {});
    visited.assign(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(1);
    return 0;
}''';
    }

    final includes =
        codeReference.requiredIncludes.isEmpty
            ? '#include <bits/stdc++.h>'
            : codeReference.requiredIncludes
                .map((name) => '#include <$name>')
                .join('\n');
    final structures = codeReference.dataStructures.join(';\n');
    final signature =
        codeReference.templateSignature.isNotEmpty
            ? codeReference.templateSignature
            : '// Template body to be filled';

    return [
      includes,
      'using namespace std;',
      if (structures.isNotEmpty) '$structures;',
      '',
      signature,
    ].join('\n');
  }
}
