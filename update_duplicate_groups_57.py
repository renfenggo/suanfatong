import json

# 读取报告文件
with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
    report_content = f.read()

# 将 duplicate_groups_found 从 42 改为 57
report_content = report_content.replace("发现重复/近重复组数量：42", "发现重复/近重复组数量：57")

# 写回报告文件
with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
    f.write(report_content)

print("✅ 已将 duplicate_groups_found 从 42 更新为 57")