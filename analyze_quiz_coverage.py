import json
import os
import glob
from pathlib import Path

# 统计函数
def analyze_units_files():
    data_dir = "assets/data"
    
    total_units = 0
    total_quizzes = 0
    units_with_quizzes = 0
    units_without_quizzes = []
    category_stats = {}
    
    # 遍历所有知识点文件
    for category in ["cpp", "algorithm", "math"]:
        category_dir = os.path.join(data_dir, category)
        if not os.path.exists(category_dir):
            continue
            
        pattern = os.path.join(category_dir, "*_units.json")
        unit_files = glob.glob(pattern)
        
        category_units = 0
        category_quizzes = 0
        category_with_quizzes = 0
        
        for file_path in unit_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 根据文件结构获取units
                if 'units' in data:
                    units = data['units']
                elif 'unit' in data:
                    units = data['unit']
                else:
                    continue
                
                for unit in units:
                    total_units += 1
                    category_units += 1
                    
                    quiz_count = 0
                    if 'quiz' in unit and unit['quiz']:
                        quiz_count = len(unit['quiz'])
                        total_quizzes += quiz_count
                        category_quizzes += quiz_count
                        units_with_quizzes += 1
                        category_with_quizzes += 1
                    else:
                        units_without_quizzes.append({
                            'itemId': unit.get('itemId', 'unknown'),
                            'title': unit.get('title', 'unknown'),
                            'category': category,
                            'file': os.path.basename(file_path)
                        })
                
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        category_stats[category] = {
            'total_units': category_units,
            'total_quizzes': category_quizzes,
            'units_with_quizzes': category_with_quizzes,
            'coverage': category_with_quizzes / category_units if category_units > 0 else 0
        }
    
    # 生成报告
    print("=" * 60)
    print("知识点选择题覆盖统计报告")
    print("=" * 60)
    print(f"总知识点数: {total_units}")
    print(f"总选择题数: {total_quizzes}")
    print(f"有选择题的知识点数: {units_with_quizzes}")
    print(f"无选择题的知识点数: {len(units_without_quizzes)}")
    print(f"总体覆盖率: {units_with_quizzes/total_units*100:.1f}%")
    print()
    
    print("分类统计:")
    for category, stats in category_stats.items():
        print(f"  {category}:")
        print(f"    知识点: {stats['total_units']}")
        print(f"    选择题: {stats['total_quizzes']}")
        print(f"    覆盖率: {stats['coverage']*100:.1f}%")
    print()
    
    print("缺少选择题的知识点（前20个）:")
    for i, unit in enumerate(units_without_quizzes[:20], 1):
        print(f"  {i}. [{unit['itemId']}] {unit['title']} ({unit['category']}/{unit['file']})")
    
    if len(units_without_quizzes) > 20:
        print(f"  ... 还有 {len(units_without_quizzes) - 20} 个")
    
    return {
        'total_units': total_units,
        'total_quizzes': total_quizzes,
        'units_with_quizzes': units_with_quizzes,
        'units_without_quizzes': units_without_quizzes,
        'category_stats': category_stats
    }

if __name__ == "__main__":
    stats = analyze_units_files()