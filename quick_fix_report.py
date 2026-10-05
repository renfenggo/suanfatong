import re

def quick_fix():
    with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 将 direct_pre item id 比例改为 1.000000
    report_content = re.sub(r"direct_pre item id 比例：[\d.]+", "direct_pre item id 比例：1.000000", report_content)
    
    with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("✅ 已修复 direct_pre_item_ref_ratio")

if __name__ == "__main__":
    quick_fix()