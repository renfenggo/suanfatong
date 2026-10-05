import json
import os
import glob
from collections import defaultdict

# 分析需要动画的知识点
def analyze_missing_animations():
    data_dir = "assets/data"
    
    # 1. 读取现有动画清单
    manifest_file = os.path.join(data_dir, "cpp", "animations", "cpp_animation_manifest.json")
    existing_animations = set()
    
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        
        for anim in manifest_data.get('animations', []):
            existing_animations.add(anim.get('itemId', ''))
    
    print(f"现有动画对应的知识点ID: {len(existing_animations)}个")
    
    # 2. 遍历所有知识点，找出没有动画的
    units_without_animation = []
    units_by_category = defaultdict(list)
    
    for category in ["cpp", "algorithm", "math"]:
        pattern = os.path.join(data_dir, category, "*_units.json")
        unit_files = glob.glob(pattern)
        
        for file_path in unit_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                units = data.get('units', [])
                for unit in units:
                    item_id = unit.get('itemId', '')
                    title = unit.get('title', '')
                    
                    if item_id and item_id not in existing_animations:
                        unit_info = {
                            'itemId': item_id,
                            'title': title,
                            'category': category,
                            'learning_goal': unit.get('learningGoal', ''),
                            'common_mistakes': unit.get('commonMistakes', []),
                            'practice': unit.get('practice', {})
                        }
                        units_without_animation.append(unit_info)
                        units_by_category[category].append(unit_info)
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"\n没有动画的知识点总数: {len(units_without_animation)}个")
    
    # 3. 根据知识点特征判断是否适合动画
    def needs_animation_score(unit):
        score = 0
        reasons = []
        
        # 检查常见错误中是否涉及过程性问题
        for mistake in unit.get('common_mistakes', []):
            desc = mistake.get('description', '').lower()
            if any(keyword in desc for keyword in ['过程', '步骤', '顺序', '流程', '逐步', '一层层', '遍历', '扩展', '改变', '变化', '执行', '调用']):
                score += 3
                reasons.append("常见错误涉及过程性问题")
                break
        
        # 检查学习目标中是否涉及过程性操作
        goal = unit.get('learning_goal', '').lower()
        if any(keyword in goal for keyword in ['过程', '步骤', '演示', '理解', '掌握', '操作', '执行', '实现']):
            score += 2
            reasons.append("学习目标涉及理解过程")
        
        # 检查练习提示中是否涉及分步操作
        practice = unit.get('practice', {})
        prompt = practice.get('prompt', '').lower()
        if any(keyword in prompt for keyword in ['逐步', '一步步', '过程', '顺序', '先', '然后', '最后']):
            score += 2
            reasons.append("练习提示涉及分步操作")
        
        # 检查代码注释中是否涉及执行顺序
        example_code = unit.get('exampleCode', '').lower()
        if any(keyword in example_code for keyword in ['循环', '递归', '调用', '队列', '栈', '树', '图']):
            score += 1
            reasons.append("代码涉及复杂数据结构或控制流")
        
        # 检查标题中的关键词
        title = unit.get('title', '').lower()
        high_priority_keywords = ['排序', '查找', '搜索', '遍历', '递归', '回溯', '动态规划', '分治', '贪心', '排序', '算法', '过程', '原理']
        medium_priority_keywords = ['概念', '基础', '思想', '理解', '学习', '掌握']
        
        if any(keyword in title for keyword in high_priority_keywords):
            score += 4
            reasons.append("标题涉及高优先级算法概念")
        elif any(keyword in title for keyword in medium_priority_keywords):
            score += 1
            reasons.append("标题涉及基础概念")
        
        return score, reasons
    
    # 4. 对知识点进行评分和排序
    scored_units = []
    for unit in units_without_animation:
        score, reasons = needs_animation_score(unit)
        if score > 0:
            scored_units.append({
                **unit,
                'animation_score': score,
                'reasons': reasons
            })
    
    # 按分数排序
    scored_units.sort(key=lambda x: x['animation_score'], reverse=True)
    
    # 5. 生成报告
    print("\n" + "=" * 80)
    print("需要动画解析的知识点推荐 (按优先级排序)")
    print("=" * 80)
    
    # 高优先级 (分数 >= 5)
    high_priority = [u for u in scored_units if u['animation_score'] >= 5]
    medium_priority = [u for u in scored_units if 3 <= u['animation_score'] < 5]
    low_priority = [u for u in scored_units if 1 <= u['animation_score'] < 3]
    
    print(f"\n🔴 高优先级 (分数≥5): {len(high_priority)}个")
    for i, unit in enumerate(high_priority[:15], 1):  # 只显示前15个
        print(f"  {i}. [{unit['itemId']}] {unit['title']} ({unit['category']}) - 分数:{unit['animation_score']}")
        print(f"     原因: {', '.join(unit['reasons'])}")
    
    if len(high_priority) > 15:
        print(f"  ... 还有 {len(high_priority) - 15} 个")
    
    print(f"\n🟡 中优先级 (分数3-4): {len(medium_priority)}个")
    for i, unit in enumerate(medium_priority[:10], 1):
        print(f"  {i}. [{unit['itemId']}] {unit['title']} ({unit['category']}) - 分数:{unit['animation_score']}")
        print(f"     原因: {', '.join(unit['reasons'])}")
    
    if len(medium_priority) > 10:
        print(f"  ... 还有 {len(medium_priority) - 10} 个")
    
    print(f"\n🟢 低优先级 (分数1-2): {len(low_priority)}个")
    for i, unit in enumerate(low_priority[:5], 1):
        print(f"  {i}. [{unit['itemId']}] {unit['title']} ({unit['category']}) - 分数:{unit['animation_score']}")
    
    if len(low_priority) > 5:
        print(f"  ... 还有 {len(low_priority) - 5} 个")
    
    # 按类别统计
    print(f"\n📊 各类别需要动画的知识点数:")
    for category in ["cpp", "algorithm", "math"]:
        count = len([u for u in scored_units if u['category'] == category])
        print(f"  {category}: {count}个")
    
    # 生成详细的列表
    high_priority_list = []
    for unit in high_priority:
        high_priority_list.append({
            'itemId': unit['itemId'],
            'title': unit['title'],
            'category': unit['category'],
            'score': unit['animation_score'],
            'reasons': unit['reasons'],
            'learning_goal': unit['learning_goal']
        })
    
    medium_priority_list = []
    for unit in medium_priority:
        medium_priority_list.append({
            'itemId': unit['itemId'],
            'title': unit['title'],
            'category': unit['category'],
            'score': unit['animation_score'],
            'reasons': unit['reasons'],
            'learning_goal': unit['learning_goal']
        })
    
    # 保存到文件
    output_file = "animation_recommendations.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'high_priority': high_priority_list[:30],
            'medium_priority': medium_priority_list[:20],
            'total_high_priority': len(high_priority),
            'total_medium_priority': len(medium_priority),
            'total_needs_animation': len(scored_units)
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细推荐列表已保存到: {output_file}")
    
    return {
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'total_scored': len(scored_units),
        'total_without_animation': len(units_without_animation)
    }

if __name__ == "__main__":
    stats = analyze_missing_animations()