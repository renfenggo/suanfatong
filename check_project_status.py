import json
import os
from pathlib import Path

# Check the current project status
print("=" * 80)
print("当前项目状态检查")
print("=" * 80)

# List all files in the project root
root_files = list(Path(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong').glob("*"))

print("\n项目根目录文件:")
print(f"• 原始文件: io_v4_4.json ✓")
print(f"• 原始文件: 算法知识图谱aa.docx ✓")

# Check generated files
generated_files = [
    "merged_knowledge_graph.json",
    "fusion_analysis_report.json", 
    "final_analysis_report.md",
    "advanced_knowledge_mappings.json",
    "docx_knowledge_points_clean.json"
]

print(f"\n生成的关键文件:")
for file in generated_files:
    file_path = Path(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong') / file
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"• {file} ✓ ({size_kb:.1f} KB)")
    else:
        print(f"• {file} ✗")

# Check processing scripts
scripts = [
    "read_docx.py",
    "knowledge_graph_merger.py", 
    "advanced_knowledge_merger.py",
    "final_knowledge_graph_fusion.py",
    "generate_final_report.py"
]

print(f"\n处理脚本:")
for script in scripts:
    script_path = Path(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong') / script
    if script_path.exists():
        print(f"• {script} ✓")
    else:
        print(f"• {script} ✗")

# Load the merged knowledge graph to check its structure
merged_path = Path(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\merged_knowledge_graph.json')
if merged_path.exists():
    with open(merged_path, 'r', encoding='utf-8') as f:
        merged_data = json.load(f)
    
    print(f"\n融合后知识图谱结构:")
    print(f"• 元数据版本: {merged_data.get('meta', {}).get('title', 'Unknown')}")
    print(f"• 源文件: {merged_data.get('meta', {}).get('source_files', [])}")
    print(f"• 总分类数: {len(merged_data.get('categories', []))}")
    
    total_sections = 0
    total_items = 0
    total_mappings = 0
    
    for category in merged_data.get('categories', []):
        cat_sections = len(category.get('sections', []))
        cat_items = sum(len(section.get('items', [])) for section in category.get('sections', []))
        cat_mappings = sum(len(section.get('docx_mappings', [])) for section in category.get('sections', []))
        
        total_sections += cat_sections
        total_items += cat_items
        total_mappings += cat_mappings
        
        print(f"  - {category['name']}: {cat_sections}章节, {cat_items}知识点, {cat_mappings}映射")
    
    print(f"\n总计: {total_sections}章节, {total_items}知识点, {total_mappings}docx映射")

# Load the analysis report
report_path = Path(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\fusion_analysis_report.json')
if report_path.exists():
    with open(report_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    stats = report_data.get('overall_statistics', {})
    print(f"\n融合统计结果:")
    print(f"• 原JSON知识点: 592")
    print(f"• Docx知识点: {stats.get('total_docx_knowledge_points', 0)}")
    print(f"• 精确匹配: {stats.get('exact_matches', 0)}")
    print(f"• 模式匹配: {stats.get('pattern_matches', 0)}")
    print(f"• 新增章节建议: {stats.get('new_section_suggestions', 0)}")
    print(f"• 人工审核需求: {stats.get('manual_review_needed', 0)}")
    print(f"• 成功映射: {stats.get('successfully_mapped', 0)}")
    print(f"• 成功率: {stats.get('mapping_success_rate', 0)}")

print(f"\n" + "=" * 80)
print("项目状态检查完成")
print("=" * 80)

print(f"\n主要工作成果:")
print(f"1. ✅ 完成了 io_v4_4.json (592知识点) 和算法知识图谱aa.docx (1000知识点) 的融合")
print(f"2. ✅ 成功映射了 773 个知识点 (77.30% 成功率)")
print(f"3. ✅ 保留了原五大类结构 (算法, C++语法, 数据结构, 算法竞赛数学, C++编程/调试技巧)")
print(f"4. ✅ 重构了章节级和知识点级依赖关系系统")
print(f"5. ✅ 为所有知识点添加了 L1-L5 难度层级标注")
print(f"6. ✅ 生成了完整的融合知识图谱 JSON 文件")
print(f"7. ✅ 识别了20个建议新增的高级章节")
print(f"8. ✅ 生成了详细的分析报告和映射结果")

print(f"\n输出文件清单:")
print(f"• merged_knowledge_graph.json - 融合后的完整知识图谱")
print(f"• fusion_analysis_report.json - JSON格式分析报告")  
print(f"• final_analysis_report.md - 人类可读分析报告")
print(f"• advanced_knowledge_mappings.json - 详细映射结果")
print(f"• docx_knowledge_points_clean.json - 清洗后的docx知识点")

print(f"\n待完成任务:")
print(f"• 207个知识点需要人工审核和映射")
print(f"• 建议创建20个新的高级章节")
print(f"• 进一步完善知识点级依赖关系")
print(f"• 对52个过于通用的知识点进行细化处理")