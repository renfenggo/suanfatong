#!/usr/bin/env python3
"""
探索图谱文件结构并修复读取逻辑
"""
import json
from pathlib import Path

project_root = Path(r"c:\Users\renfenggo\Documents\trae_projects\suanfatong")

def explore_json_structure(file_path, max_depth=3, current_depth=0):
    """递归探索 JSON 结构"""
    if current_depth > max_depth:
        return {"type": "max_depth_reached"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"error": str(e)}
    
    def explore(obj, depth=0):
        if depth > max_depth:
            return "..."
        
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key in ["items", "sections", "knowledge_items"]:
                    # 对于重要字段，显示更多信息
                    if isinstance(value, list):
                        result[key] = f"list with {len(value)} items"
                        if len(value) > 0:
                            result[key + "_sample"] = explore(value[0], depth + 1)
                    else:
                        result[key] = explore(value, depth + 1)
                elif depth < 2:  # 只在前两层显示所有字段
                    result[key] = explore(value, depth + 1)
            return result
        elif isinstance(obj, list):
            if len(obj) == 0:
                return "empty list"
            return f"list[{len(obj)}]"
        else:
            return str(type(obj).__name__)
    
    return explore(data)

def find_all_items(data, path=""):
    """递归查找所有 items 字段"""
    items_found = []
    
    def _find(obj, current_path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{current_path}.{key}" if current_path else key
                if key == "items" and isinstance(value, list):
                    items_found.append({
                        "path": new_path,
                        "count": len(value),
                        "sample": value[0] if len(value) > 0 else None
                    })
                _find(value, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _find(item, f"{current_path}[{i}]")
    
    _find(data, path)
    return items_found

# 探索主图谱结构
main_graph_path = project_root / "merged_knowledge_graph_item_dependencies_refined.json"
print("=" * 60)
print("探索主图谱结构")
print("=" * 60)

with open(main_graph_path, 'r', encoding='utf-8') as f:
    main_data = json.load(f)

print("\n顶层字段:")
for key in main_data.keys():
    print(f"  - {key}")

# 查找所有 items 字段
print("\n查找所有 items 字段:")
all_items = find_all_items(main_data)
for i, item_info in enumerate(all_items, 1):
    print(f"\n{i}. 路径: {item_info['path']}")
    print(f"   数量: {item_info['count']}")
    if item_info['sample']:
        print(f"   样例字段: {list(item_info['sample'].keys())[:5]}")

# 尝试找到正确的 items
print("\n" + "=" * 60)
print("尝试获取正确的 items 数据")
print("=" * 60)

# 方法1：直接在顶层查找
if "items" in main_data:
    print(f"方法1: 顶层 items - {len(main_data['items'])} 个")
else:
    print("方法1: 顶层没有 items 字段")

# 方法2：在 categories 中查找
if "categories" in main_data:
    categories = main_data["categories"]
    total_items = 0
    if isinstance(categories, list):
        for i, cat_data in enumerate(categories):
            if isinstance(cat_data, dict) and "sections" in cat_data:
                sections = cat_data["sections"]
                for j, section_data in enumerate(sections):
                    if isinstance(section_data, dict) and "items" in section_data:
                        section_items = section_data["items"]
                        total_items += len(section_items)
                        cat_name = cat_data.get("name", f"cat_{i}")
                        sec_name = section_data.get("name", f"sec_{j}")
                        print(f"方法2: categories[{i}].sections[{j}].items ({cat_name}/{sec_name}) - {len(section_items)} 个")
    elif isinstance(categories, dict):
        for cat_name, cat_data in categories.items():
            if isinstance(cat_data, dict) and "sections" in cat_data:
                sections = cat_data["sections"]
                if isinstance(sections, list):
                    for j, section_data in enumerate(sections):
                        if isinstance(section_data, dict) and "items" in section_data:
                            section_items = section_data["items"]
                            total_items += len(section_items)
                            sec_name = section_data.get("name", f"sec_{j}")
                            print(f"方法2: categories.{cat_name}.sections[{j}].items ({sec_name}) - {len(section_items)} 个")
    print(f"方法2: 总计 {total_items} 个")

# 方法3：在 knowledge_graph 中查找
if "knowledge_graph" in main_data:
    kg = main_data["knowledge_graph"]
    if isinstance(kg, dict) and "items" in kg:
        print(f"方法3: knowledge_graph.items - {len(kg['items'])} 个")

# 方法4：在 graph_data 中查找
if "graph_data" in main_data:
    gd = main_data["graph_data"]
    if isinstance(gd, dict) and "items" in gd:
        print(f"方法4: graph_data.items - {len(gd['items'])} 个")

# 探索前端图谱结构
frontend_graph_path = project_root / "assets" / "data" / "knowledge" / "io_v4_4.json"
print("\n" + "=" * 60)
print("探索前端图谱结构")
print("=" * 60)

with open(frontend_graph_path, 'r', encoding='utf-8') as f:
    frontend_data = json.load(f)

print("\n顶层字段:")
for key in frontend_data.keys():
    print(f"  - {key}")

# 查找所有 items 字段
print("\n查找所有 items 字段:")
all_items_frontend = find_all_items(frontend_data)
for i, item_info in enumerate(all_items_frontend, 1):
    print(f"\n{i}. 路径: {item_info['path']}")
    print(f"   数量: {item_info['count']}")
    if item_info['sample']:
        print(f"   样例字段: {list(item_info['sample'].keys())[:5]}")