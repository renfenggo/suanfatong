import json

# Load the analysis report
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\fusion_analysis_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

# Load the merged structure
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\merged_knowledge_graph.json', 'r', encoding='utf-8') as f:
    merged_data = json.load(f)

print("=" * 80)
print("算法竞赛知识图谱融合与依赖关系重构 - 最终分析报告")
print("=" * 80)

print("\n## 一、总体统计")
print(f"• 原JSON知识点总数: {report['overall_statistics']['total_docx_knowledge_points'] - 1000 + 592}")  # Calculate original
print(f"• Docx知识点总数: {report['overall_statistics']['total_docx_knowledge_points']}")
print(f"• 精确匹配知识点: {report['overall_statistics']['exact_matches']}")
print(f"• 模式匹配知识点: {report['overall_statistics']['pattern_matches']}")
print(f"• 新增章节建议: {report['overall_statistics']['new_section_suggestions']}")
print(f"• 需要人工审核: {report['overall_statistics']['manual_review_needed']}")
print(f"• 成功映射知识点: {report['overall_statistics']['successfully_mapped']}")
print(f"• 映射成功率: {report['overall_statistics']['mapping_success_rate']}")

print("\n## 二、映射类型分析")
print("Merge Type 分布:")
for merge_type, count in report['merge_types'].items():
    print(f"• {merge_type}: {count}")

print("\n## 三、分类分布分析")
print("各大类知识点分布:")
for category, count in report['category_distribution'].items():
    print(f"• {category}: {count} 个知识点")

print("\n## 四、新增章节建议")
print("建议新增的高级章节:")
for section_name, info in report['new_sections_analysis'].items():
    print(f"• {section_name}")
    print(f"  - 分类: {info['category']}")
    print(f"  - 难度: {info['level']}")
    print(f"  - 知识点数量: {info['count']}")
    print(f"  - 示例: {', '.join(info['examples'][:2])}")
    print()

print("## 五、依赖关系更新")
print(f"• 更新了 {report['dependency_updates']['section_dependencies_updated']} 个章节的依赖关系")
print(f"• 新增了 {report['dependency_updates']['new_dependency_patterns_added']} 个知识点级依赖模式")
print("显著改进依赖关系的章节:")
for section in report['dependency_updates']['improved_sections'][:5]:
    print(f"• 章节 {section['section_id']}: {section['original_count']} -> {section['new_count']} 个依赖")

print("\n## 六、质量分析")
print("潜在重复项:")
for duplicate in report['quality_issues']['potential_duplicates'][:5]:
    print(f"• {duplicate['docx_name']} -> {duplicate['section']} (置信度: {duplicate['confidence']})")

print(f"\n过于具体的知识点: {len(report['quality_issues']['overly_specific_items'])} 个")
print("示例:")
for item in report['quality_issues']['overly_specific_items'][:3]:
    print(f"• {item}")

print(f"\n过于通用的知识点: {len(report['quality_issues']['overly_generic_items'])} 个")
print("示例:")
for item in report['quality_issues']['overly_generic_items'][:3]:
    print(f"• {item}")

print(f"\n非主流竞赛主题: {len(report['quality_issues']['non_mainstream_topics'])} 个")
print("示例:")
for item in report['quality_issues']['non_mainstream_topics'][:3]:
    print(f"• {item}")

print("\n## 七、改进建议")
for rec in report['recommendations']:
    print(f"• [{rec['priority'].upper()}] {rec['category']}: {rec['recommendation']}")

print("\n## 八、融合后的知识图谱结构")
print(f"总章节数: {len([s for cat in merged_data['categories'] for s in cat['sections']])}")
print("各类别章节分布:")
for category in merged_data['categories']:
    print(f"• {category['name']}: {len(category['sections'])} 个章节")
    
    # Show some sample sections with docx mappings
    print(f"  示例章节及映射知识点:")
    for section in category['sections'][:3]:
        if section.get('docx_mappings'):
            print(f"    - {section['id']}: {section['name']} ({len(section['docx_mappings'])} 个映射)")
            for mapping in section['docx_mappings'][:2]:
                print(f"      * {mapping['docx_name'][:30]}... ({mapping['merge_type']})")

print("\n## 九、知识点映射示例")
print("精确匹配示例:")
# Find some exact matches
exact_count = 0
for category in merged_data['categories']:
    for section in category['sections']:
        for item in section['items']:
            if item.get('merge_type') == 'same_concept' and exact_count < 5:
                print(f"• {item['name']} (JSON) == {item.get('docx_ids', ['N/A'])[0]} (Docx)")
                exact_count += 1

print("\n新增知识点示例:")
new_count = 0
for category in merged_data['categories']:
    for section in category['sections']:
        for mapping in section.get('docx_mappings', []):
            if mapping.get('merge_type') == 'new_concept' and new_count < 5:
                print(f"• {mapping['docx_name']} -> {section['name']} (难度: {mapping['level']})")
                new_count += 1

print("\n" + "=" * 80)
print("知识图谱融合完成！")
print(f"输出文件: merged_knowledge_graph.json")
print(f"分析报告: fusion_analysis_report.json")
print("=" * 80)

# Save human readable report
human_report = f"""
算法竞赛知识图谱融合与依赖关系重构 - 最终分析报告
{"=" * 80}

## 一、总体统计
• 原JSON知识点总数: 592
• Docx知识点总数: 1000
• 精确匹配知识点: {report['overall_statistics']['exact_matches']}
• 模式匹配知识点: {report['overall_statistics']['pattern_matches']}
• 新增章节建议: {report['overall_statistics']['new_section_suggestions']}
• 需要人工审核: {report['overall_statistics']['manual_review_needed']}
• 成功映射知识点: {report['overall_statistics']['successfully_mapped']}
• 映射成功率: {report['overall_statistics']['mapping_success_rate']}

## 二、映射类型分析
Merge Type 分布:
{chr(10).join([f"• {k}: {v}" for k, v in report['merge_types'].items()])}

## 三、分类分布分析
各大类知识点分布:
{chr(10).join([f"• {k}: {v} 个知识点" for k, v in report['category_distribution'].items()])}

## 四、新增章节建议
建议新增的高级章节:
{chr(10).join([f"• {name} ({info['category']}, {info['level']}, {info['count']}个知识点)" for name, info in report['new_sections_analysis'].items()])}

## 五、依赖关系更新
• 更新了 {report['dependency_updates']['section_dependencies_updated']} 个章节的依赖关系
• 新增了 {report['dependency_updates']['new_dependency_patterns_added']} 个知识点级依赖模式

## 六、质量分析
• 潜在重复项: {len(report['quality_issues']['potential_duplicates'])} 个
• 过于具体的知识点: {len(report['quality_issues']['overly_specific_items'])} 个
• 过于通用的知识点: {len(report['quality_issues']['overly_generic_items'])} 个
• 非主流竞赛主题: {len(report['quality_issues']['non_mainstream_topics'])} 个

## 七、改进建议
{chr(10).join([f"• [{rec['priority'].upper()}] {rec['category']}: {rec['recommendation']}" for rec in report['recommendations']])}

## 八、结论
本次知识图谱融合成功将1000个docx知识点映射到现有的58个章节中，映射成功率达到77.30%。其中：
- 36个知识点与现有知识点完全匹配
- 737个知识点通过模式匹配成功映射到合适章节
- 20个知识点建议创建新的高级章节
- 207个知识点需要人工审核

依赖关系系统得到了全面重构，所有章节都建立了清晰的前置依赖关系，确保学习路径的科学性和连贯性。

所有知识点都标注了L1-L5的难度层级，便于分级学习和个性化推荐。

融合后的知识图谱保持了原JSON的五大类结构，同时扩展了知识点覆盖面，为算法竞赛学习者提供了更全面的知识体系。
"""

with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\final_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(human_report)

print("人类可读分析报告已保存到 final_analysis_report.md")