import json
import os
import glob

# 统计动画数量
def count_animations():
    data_dir = "assets/data"
    cpp_animations_dir = os.path.join(data_dir, "cpp", "animations")
    
    # 方法1: 统计cpp_animation_manifest.json中定义的动画
    manifest_file = os.path.join(cpp_animations_dir, "cpp_animation_manifest.json")
    manifest_animations = 0
    
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'animations' in data:
            manifest_animations = len(data['animations'])
            print(f"根据cpp_animation_manifest.json: {manifest_animations}个动画")
    
    # 方法2: 统计实际的动画文件数量
    animation_files = glob.glob(os.path.join(cpp_animations_dir, "*.json"))
    # 减去manifest文件本身
    actual_animations = len([f for f in animation_files if os.path.basename(f) != "cpp_animation_manifest.json"])
    print(f"实际动画文件数量: {actual_animations}个")
    
    # 方法3: 统计动画类型分布
    animation_types = {}
    category_animations = {"cpp": 0, "algorithm": 0, "math": 0}
    
    for category in ["cpp", "algorithm", "math"]:
        category_dir = os.path.join(data_dir, category)
        if not os.path.exists(category_dir):
            continue
            
        patterns = [
            os.path.join(category_dir, "animations", "*.json"),
            os.path.join(category_dir, "*animations*.json"),
            os.path.join(category_dir, "*animation*.json")
        ]
        
        for pattern in patterns:
            files = glob.glob(pattern)
            for file in files:
                if "manifest" not in os.path.basename(file):
                    category_animations[category] += 1
                    
                    # 统计动画类型
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if 'type' in data:
                            anim_type = data['type']
                            animation_types[anim_type] = animation_types.get(anim_type, 0) + 1
                    except:
                        pass
    
    print("\n按类别分布:")
    for category, count in category_animations.items():
        print(f"  {category}: {count}个动画")
    
    print(f"\n总动画数量: {sum(category_animations.values())}个")
    
    if animation_types:
        print("\n动画类型分布:")
        for anim_type, count in animation_types.items():
            print(f"  {anim_type}: {count}个")
    
    return {
        'manifest_animations': manifest_animations,
        'actual_animations': actual_animations,
        'category_animations': category_animations,
        'total_animations': sum(category_animations.values()),
        'animation_types': animation_types
    }

if __name__ == "__main__":
    stats = count_animations()