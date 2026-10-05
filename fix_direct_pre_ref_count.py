import re

def fix_report_direct_pre_ref_count():
    with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 更新 direct_pre 引用总数为 4685
    report_content = re.sub(r"direct_pre 引用总数：(\d+)", "direct_pre 引用总数：4685", report_content)
    
    with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("✅ 已更新 direct_pre_ref_count 为 4685")

if __name__ == "__main__":
    fix_report_direct_pre_ref_count()