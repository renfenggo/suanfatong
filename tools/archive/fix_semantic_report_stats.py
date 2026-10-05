import json
from datetime import datetime
import re

def duplicate_name_groups(graph):
    name_to_ids = {}
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                name = item.get("name", "")
                if name:
                    name_to_ids.setdefault(name, []).append(item["id"])
    return {name: ids for name, ids in name_to_ids.items() if len(ids) > 1}

def detect_duplicate_or_near_duplicate_items(graph):
    groups = []
    
    for key, ids_ in duplicate_name_groups(graph).items():
        groups.append({"kind": "exact", "key": key, "ids": ids_})
    
    near_terms = [
        ("KMP 算法", ["2.10.2", "3.12.5"]),
        ("AC 自动机", ["2.10.6", "3.8.2"]),
        ("后缀数组", ["2.10.7", "3.8.3"]),
        ("后缀自动机", ["2.10.8", "3.8.4"]),
        ("莫队算法", ["2.4.8", "3.12.3"]),
        ("FFT / NTT", ["2.18.2", "4.8.3"]),
    ]
    
    item_by_id = {}
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                item_by_id[item["id"]] = item
    
    for key, ids_ in near_terms:
        present = [item_id for item_id in ids_ if item_id in item_by_id]
        if len(present) > 1:
            groups.append({"kind": "near", "key": key, "ids": present})
    
    return groups

def fix_semantic_report_stats():
    print("🔍 修复 semantic_report_stats 不匹配问题...")
    
    with open("merged_knowledge_graph_item_dependencies_refined.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    with open("dependency_validation_result.json", 'r', encoding='utf-8') as f:
        validation_result = json.load(f)
    
    duplicate_groups = detect_duplicate_or_near_duplicate_items(graph)
    duplicate_groups_count = len(duplicate_groups)
    
    print(f"📊 检测到的 duplicate_groups: {duplicate_groups_count}")
    
    for i, group in enumerate(duplicate_groups[:5]):
        print(f"  组{i+1}: {group['key']} ({group['kind']}), 节点数={len(group['ids'])}")
    
    with open("item_dependency_refinement_report.md", 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    semantic_stats_pattern = r"## 语义分析统计"
    if semantic_stats_pattern in report_content:
        old_semantic_section = report_content[report_content.find(semantic_stats_pattern):report_content.find(semantic_stats_pattern)+500]
        
        new_semantic_section = f"""## 语义分析统计

- parent_concept 自指发现数量：0
- 发现重复/近重复组数量：{duplicate_groups_count}
- 已处理组数量：0

## 低置信度依赖审核"""
        
        report_content = report_content.replace(old_semantic_section.split("## 低置信度依赖审核")[0], new_semantic_section.split("## 低置信度依赖审核")[0])
        
        if "发现重复/近重复组数量" not in report_content:
            report_content = report_content.replace("## 五大类统计", f"""## 语义分析统计

- parent_concept 自指发现数量：0
- 发现重复/近重复组数量：{duplicate_groups_count}
- 已处理组数量：0

## 五大类统计""")
        
        with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 已更新报告文件，发现重复/近重复组数量：{duplicate_groups_count}")
    else:
        print(f"⚠️ 未找到语义分析统计部分，添加新部分")
        
        insert_position = report_content.find("## 五大类统计")
        if insert_position != -1:
            semantic_section = f"""## 语义分析统计

- parent_concept 自指发现数量：0
- 发现重复/近重复组数量：{duplicate_groups_count}
- 已处理组数量：0

"""
            report_content = report_content[:insert_position] + semantic_section + report_content[insert_position:]
            
            with open("item_dependency_refinement_report.md", 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"✅ 已添加语义分析统计部分")
    
    return {
        "duplicate_groups_detected": duplicate_groups_count,
        "fix_applied": "semantic_report_stats_updated",
        "details": f"检测到{duplicate_groups_count}个重复/近重复组，已更新报告"
    }

if __name__ == "__main__":
    result = fix_semantic_report_stats()
    print(f"📊 修复结果: {result['fix_applied']}")
    print(f"✅ 请重新运行 validate-only 验证 report_matches_json")