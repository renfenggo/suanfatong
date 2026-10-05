import json
from datetime import datetime

def generate_rollback_plan():
    with open("data/stage3e_aggressive_batch4_added_items_summary.json", 'r', encoding='utf-8') as f:
        added_items_summary = json.load(f)
    
    new_item_ids = [summary["item_id"] for summary in added_items_summary]
    candidate_to_item_id = {}
    
    for summary in added_items_summary:
        candidate_to_item_id[summary["candidate_id"]] = summary["item_id"]
    
    rollback_plan = {
        "batch_id": "stage3e_aggressive_batch4",
        "generated_at": datetime.now().isoformat(),
        "reason": "Batch4 合并后的安全回滚计划",
        "backup_location": "backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4.json",
        "target_location": "merged_knowledge_graph_item_dependencies_refined.json",
        "items_to_remove": new_item_ids,
        "items_count": len(new_item_ids),
        "section_distribution": {
            "2.21": len([s for s in added_items_summary if s["section_id"] == "2.21"]),
            "3.13": len([s for s in added_items_summary if s["section_id"] == "3.13"])
        },
        "candidate_to_item_mapping": candidate_to_item_id,
        "restoration_commands": {
            "powershell": [
                f"# 恢复备份文件",
                f"Copy-Item backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_aggressive_batch4.json merged_knowledge_graph_item_dependencies_refined.json",
                f"",
                f"# 验证恢复结果",
                f"python check_count.py"
            ],
            "verification": [
                "# 验证项：",
                f"# 1. item_count 应为 1572",
                f"# 2. section_count 应为 65", 
                f"# 3. 删除所有 Batch4 新增的节点"
            ]
        },
        "expected_final_state": {
            "item_count": 1572,
            "section_count": 65,
            "removed_item_count": len(new_item_ids)
        },
        "manual_verification_steps": [
            "检查备份文件是否存在",
            "确认备份文件的创建时间",
            "执行恢复命令",
            "验证 item_count 是否回到 1572",
            "验证新增的 30 个节点是否已被移除",
            "运行完整的验证脚本"
        ],
        "risks": [
            "确保备份文件完整且未被修改",
            "确保在恢复过程中没有其他进程正在修改主图谱文件",
            "确保有足够的磁盘空间执行操作"
        ]
    }
    
    return rollback_plan

if __name__ == "__main__":
    rollback_plan = generate_rollback_plan()
    
    with open("data/stage3e_aggressive_batch4_rollback_plan.json", 'w', encoding='utf-8') as f:
        json.dump(rollback_plan, f, ensure_ascii=False, indent=2)
    
    print("✅ 回滚计划已生成")
    print(f"📝 计划文件: data/stage3e_aggressive_batch4_rollback_plan.json")
    print(f"🔄 需要移除的节点数: {rollback_plan['items_count']}")
    print(f"📊 恢复后预期节点数: {rollback_plan['expected_final_state']['item_count']}")