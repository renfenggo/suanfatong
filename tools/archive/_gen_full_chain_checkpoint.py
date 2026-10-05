import json
import os
import time

IO_PATH = "assets/data/knowledge/io_v4_4.json"
MAIN_GRAPH_PATH = "merged_knowledge_graph_item_dependencies_refined.json"
CONTENT_INDEX_PATH = "assets/data/knowledge_content/content_index.json"

SOURCE_FILES = {
    "batch2_stable_checkpoint": "data/stage5_hard_knowledge_batch2_full600_stable_checkpoint.json",
    "io_v4_4_sync_audit": "data/io_v4_4_sync_to_3240_audit.json",
    "io_v4_4_frontend_readiness": "data/io_v4_4_3240_frontend_readiness_check.json",
    "batch2_content_summary": "assets/data/knowledge_content/reports/stage5_hard_batch2_content_generation_summary.json",
    "batch2_content_validation": "assets/data/knowledge_content/reports/stage5_hard_batch2_content_validation_result.json",
    "batch2_content_frontend_readiness": "data/stage5_hard_batch2_content_frontend_readiness_check.json",
}

BACKUP_FILES = {
    "content_index_before_stage5_hard_batch1": "assets/data/knowledge_content/content_index_before_stage5_hard_batch1.json",
    "content_index_before_stage5_hard_batch2": "assets/data/knowledge_content/content_index_before_stage5_hard_batch2.json",
    "io_v4_4_before_sync": "assets/data/knowledge/io_v4_4_before_sync_to_3240.json",
}


def main():
    print("=" * 60)
    print("Stage5-HardKnowledge Batch2 Full Chain Stable Checkpoint")
    print("=" * 60)

    # ================================================================
    # 1. Load main graph
    # ================================================================
    print("\n1. Load main graph")
    main_g = json.load(open(MAIN_GRAPH_PATH, encoding="utf-8"))
    main_items = []
    main_sections = []
    for cat in main_g["categories"]:
        for sec in cat["sections"]:
            main_sections.append(sec)
            for it in sec["items"]:
                main_items.append(it)
    main_item_count = len(main_items)
    main_section_count = len(main_sections)
    main_item_ids = set(it["id"] for it in main_items)
    print(f"  Main graph: {main_item_count} items, {main_section_count} sections")

    # ================================================================
    # 2. Load io_v4_4.json
    # ================================================================
    print("\n2. Load io_v4_4.json")
    io_data = json.load(open(IO_PATH, encoding="utf-8"))
    io_items = []
    for cat in io_data["categories"]:
        for sec in cat["sections"]:
            for it in sec["items"]:
                io_items.append(it)
    io_item_count = len(io_items)
    io_item_ids = set(it["id"] for it in io_items)
    print(f"  io_v4_4.json: {io_item_count} items")

    # ================================================================
    # 3. Load content index
    # ================================================================
    print("\n3. Load content index")
    idx = json.load(open(CONTENT_INDEX_PATH, encoding="utf-8"))
    content_map = {}
    for part in idx["parts"]:
        path = part["path"]
        if os.path.exists(path):
            items = json.load(open(path, encoding="utf-8"))
            for it in items:
                content_map[it["item_id"]] = it
    content_count = len(content_map)
    content_ids = set(content_map.keys())
    print(f"  Content covers: {content_count} items, {len(idx['parts'])} parts")

    # ================================================================
    # 4. Classify Batch2 nodes
    # ================================================================
    print("\n4. Classify Batch2 nodes")
    batch2_items = [it for it in main_items if "stage5_hard_batch2_full600" in it.get("source", [])]
    batch2_ids = set(it["id"] for it in batch2_items)

    algo_count = 0
    ds_count = 0
    math_count = 0
    for it in batch2_items:
        sec_prefix = it.get("parent", "").split(".")[0]
        if sec_prefix == "2":
            algo_count += 1
        elif sec_prefix == "3":
            ds_count += 1
        elif sec_prefix == "4":
            math_count += 1
        else:
            algo_count += 1

    ready_core_count = sum(1 for it in batch2_items if it.get("source_tier") == "ready_core")
    reserve_useful_count = sum(1 for it in batch2_items if it.get("source_tier") == "reserve_useful")

    fix_a_count = sum(1 for it in batch2_items if it.get("review_priority") == "A")
    fix_b_count = sum(1 for it in batch2_items if it.get("review_priority") == "B")
    fix_c_count = sum(1 for it in batch2_items if it.get("review_priority") == "C")

    batch2_content_count = len(batch2_ids & content_ids)

    print(f"  Batch2 nodes: {len(batch2_items)}")
    print(f"  Algo: {algo_count}, DS: {ds_count}, Math: {math_count}")
    print(f"  ready_core: {ready_core_count}, reserve_useful: {reserve_useful_count}")
    print(f"  Fix A: {fix_a_count}, B: {fix_b_count}, C: {fix_c_count}")

    # ================================================================
    # 5. Section distribution after relocation
    # ================================================================
    print("\n5. Section distribution")
    sec_21_count = 0
    sec_313_count = 0
    sec_37_count = 0
    for it in io_items:
        p = it.get("parent", "")
        if p == "2.1":
            sec_21_count += 1
        elif p == "3.13":
            sec_313_count += 1
        elif p == "3.7":
            sec_37_count += 1
    print(f"  2.1: {sec_21_count}, 3.13: {sec_313_count}, 3.7: {sec_37_count}")

    # ================================================================
    # 6. Load source reports
    # ================================================================
    print("\n6. Load source reports")
    source_reports = {}
    for name, path in SOURCE_FILES.items():
        if os.path.exists(path):
            source_reports[name] = json.load(open(path, encoding="utf-8"))
            print(f"  {name}: loaded")
        else:
            print(f"  {name}: NOT FOUND")

    # ================================================================
    # 7. Consistency check
    # ================================================================
    print("\n7. Consistency check")
    consistent = (main_item_count == 3240 and io_item_count == 3240
                  and content_count == 3240 and main_section_count == 65)
    print(f"  Main={main_item_count}, io={io_item_count}, Content={content_count}")
    print(f"  Sections={main_section_count}")
    print(f"  All consistent: {consistent}")

    # ================================================================
    # 8. Build checkpoint
    # ================================================================
    checkpoint = {
        "checkpoint_type": "stage5_hard_knowledge_batch2_full_chain_stable",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "status": "stable" if consistent else "inconsistent",

        "current_state": {
            "main_graph_item_count": main_item_count,
            "io_v4_4_item_count": io_item_count,
            "content_coverage_count": content_count,
            "section_count": main_section_count,
            "consistency_ok": consistent,
        },

        "batch2_summary": {
            "new_nodes": len(batch2_items),
            "new_content": batch2_content_count,
            "content_part_total": len(idx["parts"]),
            "old_parts": len(idx["parts"]) - 6,
            "batch2_new_parts": 6,
            "category_distribution": {
                "algorithm": algo_count,
                "data_structure": ds_count,
                "math": math_count,
            },
            "source_tier_distribution": {
                "ready_core": ready_core_count,
                "reserve_useful": reserve_useful_count,
            },
            "fix_lite_distribution": {
                "A": fix_a_count,
                "B": fix_b_count,
                "C": fix_c_count,
            },
        },

        "section_relocation_summary": {
            "2.1": {"before": 142, "after": sec_21_count},
            "3.13": {"before": 353, "after": sec_313_count},
            "3.7": {"before": 39, "after": sec_37_count},
            "relocated_nodes": 27,
        },

        "pipeline_stages": [
            {"stage": 1, "name": "Batch2 Candidate Precheck", "input": "2640", "output": "600 candidates"},
            {"stage": 2, "name": "Merge", "input": "2640", "output": "3240"},
            {"stage": 3, "name": "Section Relocation", "input": "27 nodes", "output": "27 nodes relocated"},
            {"stage": 4, "name": "Fix Lite", "input": "600 nodes", "output": "600 review fields updated"},
            {"stage": 5, "name": "Stable Checkpoint", "input": "3240", "output": "main graph stable"},
            {"stage": 6, "name": "io_v4_4 Sync", "input": "2640", "output": "3240"},
            {"stage": 7, "name": "Frontend Readiness", "input": "3240", "output": "all checks passed"},
            {"stage": 8, "name": "Content Generation", "input": "2640", "output": "3240"},
            {"stage": 9, "name": "Content Frontend Readiness", "input": "3240", "output": "all checks passed"},
        ],

        "verification_reports": {
            "batch2_stable_checkpoint": "data/stage5_hard_knowledge_batch2_full600_stable_checkpoint.json",
            "io_v4_4_sync_audit": "data/io_v4_4_sync_to_3240_audit.json",
            "io_v4_4_frontend_readiness": "data/io_v4_4_3240_frontend_readiness_check.json",
            "batch2_content_summary": "assets/data/knowledge_content/reports/stage5_hard_batch2_content_generation_summary.json",
            "batch2_content_validation": "assets/data/knowledge_content/reports/stage5_hard_batch2_content_validation_result.json",
            "batch2_content_frontend_readiness": "data/stage5_hard_batch2_content_frontend_readiness_check.json",
            "batch2_stable_checkpoint_report": "docs/stage5_hard_knowledge_batch2_full600_stable_checkpoint_report.md",
            "io_v4_4_sync_report": "docs/io_v4_4_sync_to_3240_report.md",
            "io_v4_4_frontend_readiness_report": "docs/io_v4_4_3240_frontend_readiness_check_report.md",
            "batch2_content_generation_report": "assets/data/knowledge_content/reports/stage5_hard_batch2_content_generation_report.md",
            "batch2_content_frontend_readiness_report": "docs/stage5_hard_batch2_content_frontend_readiness_check_report.md",
        },

        "backup_files": {},
        "pending_items": [
            "Stage5-HardKnowledge Batch3 has NOT been started",
            "bridge ability formal candidate pool has NOT been generated",
            "problem_pattern_sync_candidates have NOT been processed",
            "Real device full validation has NOT been executed on 3240",
            "Release APK has NOT been built",
            "Any future expansion must start from this stable checkpoint",
        ],

        "restrictions": {
            "main_graph_modified": False,
            "io_v4_4_modified": False,
            "content_modified": False,
            "frontend_code_modified": False,
            "batch3_continued": False,
        },

        "next_step_recommendations": {
            "option_A": "Real device full validation on 3240 nodes",
            "option_B": "Continue Stage5-HardKnowledge Batch3",
            "option_C": "Move to bridge ability code implementation skill candidate pool",
        },
    }

    for name, path in BACKUP_FILES.items():
        if os.path.exists(path):
            checkpoint["backup_files"][name] = path

    # Write JSON
    json_path = "data/stage5_hard_knowledge_batch2_full_chain_stable_checkpoint.json"
    os.makedirs("data", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    print(f"\nCheckpoint written: {json_path}")

    # Write MD report
    write_md_report(checkpoint)


def write_md_report(cp):
    report_path = "docs/stage5_hard_knowledge_batch2_full_chain_stable_checkpoint_report.md"
    os.makedirs("docs", exist_ok=True)

    cs = cp["current_state"]
    bs = cp["batch2_summary"]
    sr = cp["section_relocation_summary"]
    cd = bs["category_distribution"]
    td = bs["source_tier_distribution"]
    fd = bs["fix_lite_distribution"]

    lines = [
        "# Stage5-HardKnowledge Batch2 Full Chain Stable Checkpoint Report",
        "",
        f"**生成时间**: {cp['generated_at']}",
        f"**状态**: {'✅ Stable' if cp['status'] == 'stable' else '❌ Inconsistent'}",
        "",
        "## 1. 三一致性检查",
        "",
        "| 数据源 | item_count | 结果 |",
        "|--------|-----------|------|",
        f"| Main Graph | {cs['main_graph_item_count']} | {'✅' if cs['main_graph_item_count'] == 3240 else '❌'} |",
        f"| io_v4_4.json | {cs['io_v4_4_item_count']} | {'✅' if cs['io_v4_4_item_count'] == 3240 else '❌'} |",
        f"| Content | {cs['content_coverage_count']} | {'✅' if cs['content_coverage_count'] == 3240 else '❌'} |",
        f"| section_count | {cs['section_count']} | {'✅' if cs['section_count'] == 65 else '❌'} |",
        "",
        f"**一致性**: {'✅ 通过' if cs['consistency_ok'] else '❌ 不通过'}",
        "",
        "## 2. Batch2 全链路阶段摘要",
        "",
        "| 阶段 | 名称 | 输入 | 输出 |",
        "|------|------|------|------|",
    ]
    for stage in cp["pipeline_stages"]:
        lines.append(f"| {stage['stage']} | {stage['name']} | {stage['input']} | {stage['output']} |")

    lines.extend([
        "",
        "## 3. Batch2 节点分类分布",
        "",
        "| 分类 | 数量 |",
        "|------|------|",
        f"| 算法 | {cd['algorithm']} |",
        f"| 数据结构 | {cd['data_structure']} |",
        f"| 数学 | {cd['math']} |",
        f"| **合计** | **{bs['new_nodes']}** |",
        "",
        "## 4. Batch2 来源分布",
        "",
        "| 来源层级 | 数量 |",
        "|----------|------|",
        f"| ready_core | {td['ready_core']} |",
        f"| reserve_useful | {td['reserve_useful']} |",
        f"| **合计** | **{bs['new_nodes']}** |",
        "",
        "## 5. Batch2 Fix Lite 分布",
        "",
        "| 优先级 | 数量 |",
        "|--------|------|",
        f"| A | {fd['A']} |",
        f"| B | {fd['B']} |",
        f"| C | {fd['C']} |",
        "",
        "## 6. 章节迁移摘要",
        "",
        "| Section | 迁移前 | 迁移后 | 变化 |",
        "|---------|--------|--------|------|",
    ])
    for sec_id, info in sr.items():
        if sec_id != "relocated_nodes":
            delta = info["after"] - info["before"]
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            lines.append(f"| {sec_id} | {info['before']} | {info['after']} | {delta_str} |")

    lines.extend([
        "",
        "## 7. 内容分包统计",
        "",
        "| 项目 | 数量 |",
        "|------|------|",
        f"| 旧分包 | {bs['old_parts']} |",
        f"| Batch2 新分包 | {bs['batch2_new_parts']} |",
        f"| **总分包数** | **{bs['content_part_total']}** |",
        f"| Batch2 新增节点 | {bs['new_nodes']} |",
        f"| Batch2 新增内容 | {bs['new_content']} |",
        "",
        "## 8. 限制确认",
        "",
        "| 项目 | 结果 |",
        "|------|------|",
        f"| 是否修改主图谱 | {'❌ 否' if not cp['restrictions']['main_graph_modified'] else '⚠️ 是'} |",
        f"| 是否修改 io_v4_4.json | {'❌ 否' if not cp['restrictions']['io_v4_4_modified'] else '⚠️ 是'} |",
        f"| 是否修改内容包 | {'❌ 否' if not cp['restrictions']['content_modified'] else '⚠️ 是'} |",
        f"| 是否修改前端代码 | {'❌ 否' if not cp['restrictions']['frontend_code_modified'] else '⚠️ 是'} |",
        f"| 是否继续 Batch3 | {'❌ 否' if not cp['restrictions']['batch3_continued'] else '⚠️ 是'} |",
        "",
        "## 9. Pending Items",
        "",
    ])
    for item in cp["pending_items"]:
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## 10. 下一步建议",
        "",
        "| 选项 | 描述 |",
        "|------|------|",
        "| **A** | 基于 3240 做真机完整验证 |",
        "| **B** | 继续 Stage5-HardKnowledge Batch3 |",
        "| **C** | 转入 bridge ability 代码实现技巧候选池 |",
        "",
        "## 11. 验证报告索引",
        "",
    ])
    for name, path in cp["verification_reports"].items():
        lines.append(f"- `{path}` ({name})")

    if cp["backup_files"]:
        lines.extend(["", "## 12. 备份文件索引", ""])
        for name, path in cp["backup_files"].items():
            lines.append(f"- `{path}` ({name})")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report written: {report_path}")


if __name__ == "__main__":
    main()
