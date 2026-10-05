import re

def check_report_content():
    with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    patterns = {
        "item_count": r"总 item 节点数：(\d+)",
        "section_count": r"section 数：(\d+)",
        "direct_pre_nonempty": r"direct_pre 非空节点数：(\d+)",
        "rel_nonempty": r"rel 非空节点数：(\d+)",
        "direct_pre_ref_count": r"direct_pre 引用总数：(\d+)",
        "direct_pre_section_ref_count": r"direct_pre section id 引用数：(\d+)",
        "dangling_count": r"悬空引用数量：(\d+)",
        "self_in_resolved_count": r"self in resolved_pre 数量：(\d+)",
    }
    
    out = {}
    for key, pat in patterns.items():
        m = re.search(pat, report_content)
        if m:
            out[key] = int(m.group(1))
        else:
            print(f"❌ 未找到模式: {pat}")
    
    m = re.search(r"direct_pre item id 比例：([0-9.]+)", report_content)
    if m:
        out["direct_pre_item_ref_ratio"] = float(m.group(1))
    else:
        print("❌ 未找到 direct_pre_item_ref_ratio 模式")
    
    print("📊 报告文件统计:")
    for key, value in out.items():
        print(f"   {key}: {value}")
    
    return out

if __name__ == "__main__":
    check_report_content()