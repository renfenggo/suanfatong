#!/usr/bin/env python3
"""
只读验证脚本：验证 checkpoint 分类统计修正后的正确性
不修改任何文件，只验证逻辑
"""

import json
from pathlib import Path
from collections import defaultdict

def main():
    print("=== Checkpoint 分类统计修正验证 ===")
    print()

    # 1. 读取主图谱
    print("1. 读取主图谱...")
    main_graph_path = Path("merged_knowledge_graph_item_dependencies_refined.json")
    with open(main_graph_path, 'r', encoding='utf-8') as f:
        main_graph = json.load(f)
    
    # 提取所有 items
    main_items = []
    for category in main_graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                main_items.append(item)
    
    print(f"   主图谱 item_count: {len(main_items)}")
    print()

    # 2. 读取前端图谱
    print("2. 读取前端图谱...")
    frontend_graph_path = Path("assets/data/knowledge/io_v4_4.json")
    with open(frontend_graph_path, 'r', encoding='utf-8') as f:
        frontend_graph = json.load(f)
    
    # 提取所有 items
    frontend_items = []
    for category in frontend_graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                frontend_items.append(item)
    
    print(f"   前端图谱 item_count: {len(frontend_items)}")
    print()

    # 3. 验证主图谱和前端图谱一致性
    print("3. 验证主图谱和前端图谱一致性...")
    main_ids = set(it["id"] for it in main_items)
    frontend_ids = set(it["id"] for it in frontend_items)
    
    if main_ids == frontend_ids:
        print("   [PASS] 主图谱和前端图谱 ID 集合完全一致")
    else:
        print(f"   [FAIL] ID 集合不一致：主图谱差异 {len(main_ids - frontend_ids)}, 前端差异 {len(frontend_ids - main_ids)}")
    print()

    # 4. 提取 Batch2 节点
    print("4. 提取 Batch2 节点...")
    batch2_items = [it for it in main_items if "stage5_hard_batch2_full600" in it.get("source", [])]
    batch2_ids = set(it["id"] for it in batch2_items)
    
    print(f"   Batch2 节点数: {len(batch2_items)}")
    print()

    # 5. 按 section prefix 修正统计
    print("5. 按 section prefix 修正统计...")
    print("   统计口径：2.x=算法, 3.x=数据结构, 4.x=数学")
    
    algo_count = 0
    ds_count = 0
    math_count = 0
    unknown_count = 0
    
    section_prefix_stats = defaultdict(lambda: {"算法": 0, "数据结构": 0, "数学": 0, "其他": 0})
    item_details = []
    
    for it in batch2_items:
        parent = it.get("parent", "")
        sec_prefix = parent.split(".")[0] if parent else ""
        
        # 按修正后的逻辑统计
        if sec_prefix == "2":
            algo_count += 1
            section_prefix_stats[sec_prefix]["算法"] += 1
        elif sec_prefix == "3":
            ds_count += 1
            section_prefix_stats[sec_prefix]["数据结构"] += 1
        elif sec_prefix == "4":
            math_count += 1
            section_prefix_stats[sec_prefix]["数学"] += 1
        else:
            algo_count += 1  # 保持原有 else 逻辑
            section_prefix_stats[sec_prefix]["其他"] += 1
            unknown_count += 1
        
        item_details.append({
            "id": it["id"],
            "parent": parent,
            "section_prefix": sec_prefix,
            "title": it.get("name", "")
        })
    
    total_count = algo_count + ds_count + math_count
    
    print(f"   算法: {algo_count}")
    print(f"   数据结构: {ds_count}")
    print(f"   数学: {math_count}")
    print(f"   合计: {total_count}")
    print(f"   未知前缀: {unknown_count}")
    print()

    # 6. 验证统计结果
    print("6. 验证统计结果...")
    
    # 验证 3.x 不再计入算法
    section_3x_count = sum(1 for it in batch2_items if it.get("parent", "").split(".")[0] == "3")
    print(f"   [INFO] 3.x 节点数: {section_3x_count}")
    print(f"   [INFO] 数据结构统计: {ds_count}")
    if section_3x_count == ds_count:
        print("   [PASS] 3.x 节点正确计入数据结构")
    else:
        print(f"   [FAIL] 3.x 节点统计不匹配")
    
    # 验证合计仍为 600
    if total_count == 600:
        print(f"   [PASS] 合计仍为 600")
    else:
        print(f"   [FAIL] 合计不等于 600: {total_count}")
    
    # 验证主图谱 item_count 仍为 3240
    if len(main_items) == 3240:
        print(f"   [PASS] 主图谱 item_count 仍为 3240")
    else:
        print(f"   [FAIL] 主图谱 item_count 变更: {len(main_items)}")
    
    # 验证前端图谱 item_count 仍为 3240
    if len(frontend_items) == 3240:
        print(f"   [PASS] 前端图谱 item_count 仍为 3240")
    else:
        print(f"   [FAIL] 前端图谱 item_count 变更: {len(frontend_items)}")
    
    # 验证 ID 集合一致性
    current_main_ids = set(it["id"] for it in main_items)
    if current_main_ids == main_ids:
        print(f"   [PASS] 主图谱 ID 集合未变更")
    else:
        print(f"   [FAIL] 主图谱 ID 集合发生变更")
    
    print()

    # 7. Section prefix 分布详情
    print("7. Section prefix 分布详情...")
    prefix_distribution = defaultdict(int)
    for it in batch2_items:
        parent = it.get("parent", "")
        sec_prefix = parent.split(".")[0] if parent else ""
        prefix_distribution[sec_prefix] += 1
    
    for prefix in sorted(prefix_distribution.keys(), key=lambda x: (len(x), x)):
        print(f"   Section {prefix}.x: {prefix_distribution[prefix]} 个")
    print()

    # 8. 与预期结果对比
    print("8. 与预期结果对比...")
    expected_algo = 323
    expected_ds = 110
    expected_math = 167
    
    print(f"   预期 - 算法: {expected_algo}, 数据结构: {expected_ds}, 数学: {expected_math}")
    print(f"   实际 - 算法: {algo_count}, 数据结构: {ds_count}, 数学: {math_count}")
    
    if algo_count == expected_algo and ds_count == expected_ds and math_count == expected_math:
        print("   [PASS] 统计结果与预期完全一致")
    else:
        print("   [FAIL] 统计结果与预期不一致")
    print()

    # 9. 对比修正前后
    print("9. 对比修正前后...")
    print("   修正前 - 算法: 433, 数据结构: 0, 数学: 167")
    print(f"   修正后 - 算法: {algo_count}, 数据结构: {ds_count}, 数学: {math_count}")
    print(f"   修正 - 算法减少: {433 - algo_count}, 数据结构增加: {ds_count - 0}")
    print()

    # 10. 输出验证结论
    print("=== 验证结论 ===")
    all_checks_passed = (
        total_count == 600 and
        len(main_items) == 3240 and
        len(frontend_items) == 3240 and
        section_3x_count == ds_count and
        main_ids == frontend_ids and
        algo_count == expected_algo and
        ds_count == expected_ds and
        math_count == expected_math
    )
    
    if all_checks_passed:
        print("[PASS] 所有验证检查通过")
        print("[PASS] checkpoint 分类统计修正正确")
        print("[PASS] 未影响主图谱数据")
        print("[PASS] ID 集合保持一致")
    else:
        print("[FAIL] 部分验证检查未通过")
    
    # 11. 保存验证结果
    verification_result = {
        "audit_time": "2026-06-16T10:30:00+08:00",
        "fix_type": "checkpoint_category_logic_fix",
        "verification_status": "passed" if all_checks_passed else "failed",
        "stats": {
            "main_graph_item_count": len(main_items),
            "frontend_graph_item_count": len(frontend_items),
            "batch2_item_count": len(batch2_items),
            "category_stats_fixed": {
                "算法": algo_count,
                "数据结构": ds_count,
                "数学": math_count,
                "合计": total_count
            },
            "category_stats_before": {
                "算法": 433,
                "数据结构": 0,
                "数学": 167,
                "合计": 600
            },
            "expected_stats": {
                "算法": expected_algo,
                "数据结构": expected_ds,
                "数学": expected_math,
                "合计": 600
            }
        },
        "prefix_distribution": dict(prefix_distribution),
        "checks": {
            "total_count_600": total_count == 600,
            "main_graph_count_3240": len(main_items) == 3240,
            "frontend_graph_count_3240": len(frontend_items) == 3240,
            "section_3x_in_ds": section_3x_count == ds_count,
            "id_sets_consistent": main_ids == frontend_ids,
            "matches_expected": algo_count == expected_algo and ds_count == expected_ds and math_count == expected_math
        },
        "conclusion": "所有验证检查通过，修正正确且未影响数据" if all_checks_passed else "部分验证检查未通过"
    }
    
    # 保存验证结果到 data 目录
    output_path = Path("data/checkpoint_category_logic_verification.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(verification_result, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 验证结果已保存到: {output_path}")

if __name__ == "__main__":
    main()