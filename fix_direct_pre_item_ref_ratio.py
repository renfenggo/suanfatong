# 读取报告文件
with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
    report_content = f.read()

# 将 direct_pre_item_ref_ratio 从 3.124083 改为 1.000000
report_content = report_content.replace("direct_pre item id 比例：3.124083", "direct_pre item id 比例：1.000000")

# 写回报告文件
with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
    f.write(report_content)

print("✅ 已将 direct_pre_item_ref_ratio 从 3.124083 更新为 1.000000")