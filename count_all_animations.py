import json
import os
import glob
from pathlib import Path

# 全面统计动画数量
def count_all_animations():
    data_dir = "assets/data"
    
    # 1. 统计cpp/animations中的动画
    cpp_animations_dir = os.path.join(data_dir, "cpp", "animations")
    cpp_animations = 0
    
    manifest_file = os.path.join(cpp_animations_dir, "cpp_animation_manifest.json")
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        cpp_animations = len(manifest_data.get('animations', []))
    
    # 2. 统计其他可能的动画文件
    other_animations = []
    
    # 检查assets/data/下的json文件，看是否有动画
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json') and 'animation' not in file and 'manifest' not in file:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 判断是否为动画文件（有steps或animationId等特征）
                    is_animation = False
                    if isinstance(data, list) and len(data) > 0:
                        first_item = data[0]
                        if 'step' in first_item or 'animationId' in first_item or 'frames' in first_item:
                            is_animation = True
                    
                    if is_animation:
                        rel_path = os.path.relpath(file_path, data_dir)
                        other_animations.append(rel_path)
                except:
                    pass
    
    # 3. 检查content_manifest.json中定义的动画场景
    content_manifest = os.path.join(data_dir, "content_manifest.json")
    content_animations = 0
    if os.path.exists(content_manifest):
        with open(content_manifest, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        for topic in content_data.get('topics', []):
            content_animations += len(topic.get('animationScenarios', []))
    
    # 生成报告
    print("=" * 60)
    print("动画数量统计报告")
    print("=" * 60)
    
    print(f"\n1. C++语法动画 (cpp/animations/): {cpp_animations}个")
    
    print(f"\n2. 其他动画文件: {len(other_animations)}个")
    for anim in other_animations:
        print(f"   - {anim}")
    
    print(f"\n3. content_manifest中定义的动画场景: {content_animations}个")
    
    total = cpp_animations + len(other_animations) + content_animations
    print(f"\n总动画数量: {total}个")
    
    return {
        'cpp_animations': cpp_animations,
        'other_animations': other_animations,
        'content_animations': content_animations,
        'total_animations': total
    }

if __name__ == "__main__":
    stats = count_all_animations()