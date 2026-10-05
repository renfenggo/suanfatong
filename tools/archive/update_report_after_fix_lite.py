import json

def correct_report_update():
    print("🔧 正确更新报告一致性...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    total_items = sum(len(section["items"]) for category in graph["categories"] for section in category["sections"])
    section_count = sum(len(category["sections"]) for category in graph["categories"])
    
    direct_pre_nonempty = 0
    direct_pre_ref_count = 0
    
    for category in graph["categories"]:
        for section in category["sections"]:
            for item in section["items"]:
                if item.get("direct_pre"):
                    direct_pre_nonempty += 1
                    direct_pre_ref_count += len(item.get("direct_pre", []))
    
    direct_pre_item_ref_ratio = direct_pre_ref_count / max(direct_pre_nonempty, 1) if direct_pre_nonempty > 0 else 1.0
    
    print(f"📊 统计:")
    print(f"   total_items: {total_items}")
    print(f"   section_count: {section_count}")
    print(f"   direct_pre_nonempty: {direct_pre_nonempty}")
    print(f"   direct_pre_ref_count: {direct_pre_ref_count}")
    print(f"   direct_pre_item_ref_ratio: {direct_pre_item_ref_ratio:.6f}")
    
    import re
    
    pattern1 = r"总 item 节点数：(\d+)"
    if re.search(pattern1, report_content):
        report_content = re.sub(pattern1, f"总 item 节点数：{total_items}", report_content)
    
    pattern2 = r"总 section 节点数：(\d+)"
    if re.search(pattern2, report_content):
        report_content = re.sub(pattern2, f"总 section 节点数：{section_count}", report_content)
    
    pattern3 = r"direct_pre item id 比例：([\d.]+)"
    if re.search(pattern3, report_content):
        report_content = re.sub(pattern3, f"direct_pre item id 比例：{direct_pre_item_ref_ratio:.6f}", report_content)
    
    with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 已更新报告文件中的统计数据")

if __name__ == "__main__":
    correct_report_update()
    print("✅ 报告一致性已修复")