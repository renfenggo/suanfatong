import json

# 验证JSON格式
try:
    with open("assets/data/cpp/animations/cpp_animation_manifest.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("✅ JSON格式验证通过")
    print(f"动画总数: {len(data['animations'])}")
    
    # 查找新添加的动画
    new_animations = [
        "cpp_merge_sort", "cpp_recursion_basic", "cpp_topological_sort",
        "cpp_dfs_backtrack", "cpp_priority_queue_heap", "cpp_greedy_activity_selection_proof"
    ]
    
    print("\n新添加的动画:")
    for anim_id in new_animations:
        found = any(anim['animationId'] == anim_id for anim in data['animations'])
        status = "✅" if found else "❌"
        print(f"  {status} {anim_id}")
    
except json.JSONDecodeError as e:
    print(f"❌ JSON格式错误: {e}")
except Exception as e:
    print(f"❌ 验证失败: {e}")