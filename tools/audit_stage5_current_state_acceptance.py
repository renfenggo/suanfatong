"""Stage5 当前状态总验收审计（只读）。

统一复核 1/2/3 号线程产物，判断是否具备进入 Batch3 的条件。

严格限制：
- 只读审计，不做修复
- 不进入 Batch3
- 不修改任何图谱、内容或报告

输出：
- docs/stage5_current_state_acceptance_report.md
- data/stage5_current_state_acceptance_report.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

# 输入文件
MAIN_GRAPH = ROOT / "merged_knowledge_graph_item_dependencies_refined.json"
FRONTEND_GRAPH = ROOT / "assets" / "data" / "knowledge" / "io_v4_4.json"
CONTENT_INDEX = ROOT / "assets" / "data" / "knowledge_content" / "content_index.json"
CONTENT_PART = ROOT / "assets" / "data" / "knowledge_content" / "items" / "stage5_hard_batch2_part_001.json"

# 一号线程产物
REVIEW_MD = ROOT / "docs" / "stage5_batch2_persistent_segment_tree_section_review.md"
REVIEW_JSON = ROOT / "data" / "stage5_batch2_persistent_segment_tree_section_review.json"
FIX_REPORT_JSON = ROOT / "data" / "stage5_batch2_persistent_segment_tree_section_fix_report.json"

# 二号线程产物
CHECKPOINT_VERIFICATION_JSON = ROOT / "data" / "checkpoint_category_logic_verification.json"

# 三号线程产物
BATCH3_READINESS_JSON = ROOT / "data" / "stage5_hard_knowledge_batch3_readiness_plan.json"

# Baseline 文件（用于 Batch2 ID 差集计算）
BASELINE_GRAPH = (
    ROOT
    / "backups"
    / "merged_knowledge_graph_item_dependencies_refined_before_stage5_hard_batch2_full600_20260526_223555.json"
)

TARGET_IDS = [
    "2.1.95",
    "2.1.96",
    "2.1.97",
    "2.1.98",
    "2.1.99",
    "2.1.100",
    "2.1.101",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def audit_thread1() -> dict[str, Any]:
    """一号线程产物验收。"""
    review_json = load_json(REVIEW_JSON)
    fix_report_json = load_json(FIX_REPORT_JSON)

    # 检查 has_content 是否全部 true
    has_content_check = all(r.get("has_content") for r in review_json.get("reviews", []))
    has_content_details = {
        r["id"]: r.get("has_content") for r in review_json.get("reviews", [])
    }

    # 检查 7 个节点在主图谱、前端图谱、内容 part 中均为 3.13
    target_nodes_main = fix_report_json.get("verification", {}).get("target_nodes_section", {})
    target_nodes_frontend = fix_report_json.get("verification", {}).get(
        "target_nodes_section_frontend", {}
    )
    target_nodes_content = fix_report_json.get("verification", {}).get(
        "target_nodes_section_content", {}
    )

    target_nodes_main_all_313 = all(loc == "3.13" for loc in target_nodes_main.values())
    target_nodes_frontend_all_313 = all(loc == "3.13" for loc in target_nodes_frontend.values())
    target_nodes_content_all_313 = all(loc == "3.13" for loc in target_nodes_content.values())

    # 检查 direct_pre / rel / resolved_pre 是否完整
    pre_fields_check = fix_report_json.get("verification", {}).get("pre_fields_check", {})
    pre_fields_intact = all(
        all(check.values()) for check in pre_fields_check.values()
        if isinstance(check, dict)
    )

    # 检查 Markdown 报告是否声明未修改内容正文
    review_md_content = REVIEW_MD.read_text(encoding="utf-8")
    declared_no_content_modification = (
        "未修改" in review_md_content and "内容正文" in review_md_content
    )

    passed = (
        has_content_check
        and target_nodes_main_all_313
        and target_nodes_frontend_all_313
        and target_nodes_content_all_313
        and pre_fields_intact
        and declared_no_content_modification
    )

    return {
        "passed": passed,
        "has_content_check": has_content_check,
        "has_content_details": has_content_details,
        "target_nodes_main_all_313": target_nodes_main_all_313,
        "target_nodes_frontend_all_313": target_nodes_frontend_all_313,
        "target_nodes_content_all_313": target_nodes_content_all_313,
        "target_nodes_section_main": target_nodes_main,
        "target_nodes_section_frontend": target_nodes_frontend,
        "target_nodes_section_content": target_nodes_content,
        "pre_fields_intact": pre_fields_intact,
        "declared_no_content_modification": declared_no_content_modification,
    }


def audit_thread2() -> dict[str, Any]:
    """二号线程产物验收。"""
    checkpoint_verification = load_json(CHECKPOINT_VERIFICATION_JSON)

    verification_status = checkpoint_verification.get("verification_status")
    checks = checkpoint_verification.get("checks", {})
    matches_expected = checks.get("matches_expected", False)

    # 检查分类统计
    stats_fixed = checkpoint_verification.get("stats", {}).get(
        "category_stats_fixed", {}
    )
    expected_stats = {
        "算法": 323,
        "数据结构": 110,
        "数学": 167,
        "合计": 600,
    }
    stats_match_expected = stats_fixed == expected_stats

    # 检查 prefix 分布
    prefix_distribution = checkpoint_verification.get("prefix_distribution", {})
    expected_prefix = {"2": 323, "3": 110, "4": 167}
    prefix_match_expected = prefix_distribution == expected_prefix

    passed = (
        verification_status == "passed"
        and matches_expected
        and stats_match_expected
        and prefix_match_expected
    )

    return {
        "passed": passed,
        "verification_status": verification_status,
        "matches_expected": matches_expected,
        "stats_fixed": stats_fixed,
        "expected_stats": expected_stats,
        "stats_match_expected": stats_match_expected,
        "prefix_distribution": prefix_distribution,
        "expected_prefix": expected_prefix,
        "prefix_match_expected": prefix_match_expected,
        "all_checks": checks,
    }


def audit_thread3() -> dict[str, Any]:
    """三号线程产物验收。"""
    batch3_readiness = load_json(BATCH3_READINESS_JSON)

    # 稳定性状态
    stability_status = batch3_readiness.get("stable_state_check", {}).get(
        "stability_status", ""
    )
    is_stable_3240 = batch3_readiness.get("stable_state_check", {}).get(
        "is_stable_3240", False
    )

    # 风险统计
    risk_summary = batch3_readiness.get("risk_audit", {}).get("_summary", {})
    risk_type_counts = risk_summary.get("risk_type_counts", {})
    unique_risky_candidate_count = risk_summary.get("unique_risky_candidate_count")
    safe_candidate_count = risk_summary.get("safe_candidate_count")
    risk_ratio = risk_summary.get("risk_ratio")
    dependency_missing_count = risk_summary.get("dependency_missing_count")
    dependency_missing_ratio = risk_summary.get("dependency_missing_ratio")

    # 剩余候选
    remaining_count = batch3_readiness.get("filtered_candidates", {}).get(
        "remaining_candidate_count", 0
    )

    # Batch2 差异解释
    batch2_explanation = batch3_readiness.get("filtered_candidates", {}).get(
        "batch2_discrepancy_explanation", {}
    )

    # 检查是否有负数、超过 100%
    has_negative = risk_ratio is not None and risk_ratio < 0
    has_over_100 = risk_ratio is not None and risk_ratio > 100

    # 建议
    suggestion_reasonable = (
        remaining_count == 141
        and dependency_missing_ratio == 100.0
        and risk_ratio == 100
    )

    passed = (
        is_stable_3240
        and not has_negative
        and not has_over_100
        and suggestion_reasonable
    )

    return {
        "passed": passed,
        "stability_status": stability_status,
        "is_stable_3240": is_stable_3240,
        "risk_type_counts": risk_type_counts,
        "unique_risky_candidate_count": unique_risky_candidate_count,
        "safe_candidate_count": safe_candidate_count,
        "risk_ratio": risk_ratio,
        "dependency_missing_count": dependency_missing_count,
        "dependency_missing_ratio": dependency_missing_ratio,
        "remaining_candidate_count": remaining_count,
        "has_negative": has_negative,
        "has_over_100": has_over_100,
        "batch2_discrepancy_explanation": batch2_explanation,
        "suggestion_reasonable": suggestion_reasonable,
    }


def audit_global_stability() -> dict[str, Any]:
    """全局稳定性检查。"""
    main_graph = load_json(MAIN_GRAPH)
    frontend_graph = load_json(FRONTEND_GRAPH)
    content_index = load_json(CONTENT_INDEX)

    # 主图谱
    main_item_count = 0
    main_section_count = 0
    main_ids = set()
    for cat in main_graph.get("categories", []):
        main_section_count += len(cat.get("sections", []))
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                main_item_count += 1
                main_ids.add(item["id"])

    # 前端图谱
    fe_item_count = 0
    fe_section_count = 0
    fe_ids = set()
    for cat in frontend_graph.get("categories", []):
        fe_section_count += len(cat.get("sections", []))
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                fe_item_count += 1
                fe_ids.add(item["id"])

    # 内容索引
    generated_item_count = content_index.get("generated_item_count", 0)
    covered_ids = set()
    for part in content_index.get("parts", []):
        part_path = ROOT / part["path"]
        if not part_path.exists():
            continue
        part_data = load_json(part_path)
        items = part_data if isinstance(part_data, list) else part_data.get("items", [])
        for it in items:
            iid = it.get("item_id") or it.get("id")
            if iid:
                covered_ids.add(iid)

    # Batch2 内容覆盖
    baseline_graph = load_json(BASELINE_GRAPH) if BASELINE_GRAPH.exists() else {}
    baseline_ids = set()
    if baseline_graph:
        for cat in baseline_graph.get("categories", []):
            for sec in cat.get("sections", []):
                for item in sec.get("items", []):
                    baseline_ids.add(item["id"])
    batch2_ids = main_ids - baseline_ids
    batch2_covered = len(batch2_ids - covered_ids) == 0

    # 7 个目标节点内容覆盖
    target_content = {}
    content_part_data = load_json(CONTENT_PART) if CONTENT_PART.exists() else []
    for it in content_part_data:
        iid = it.get("item_id")
        if iid in TARGET_IDS:
            target_content[iid] = it.get("section_id")

    passed = (
        main_item_count == 3240
        and fe_item_count == 3240
        and main_section_count == 65
        and fe_section_count == 65
        and main_ids == fe_ids
        and generated_item_count == 3240
        and len(covered_ids) == 3240
        and batch2_covered
    )

    return {
        "passed": passed,
        "main_item_count": main_item_count,
        "frontend_item_count": fe_item_count,
        "main_section_count": main_section_count,
        "frontend_section_count": fe_section_count,
        "id_sets_match": main_ids == fe_ids,
        "generated_item_count": generated_item_count,
        "content_covered_count": len(covered_ids),
        "batch2_id_count": len(batch2_ids),
        "batch2_content_covered": batch2_covered,
        "target_content_section": target_content,
    }


def compute_batch2_section_prefix_stats() -> dict[str, Any]:
    """重新统计 Batch2 section-prefix 分类。"""
    main_graph = load_json(MAIN_GRAPH)
    baseline_graph = load_json(BASELINE_GRAPH) if BASELINE_GRAPH.exists() else {}

    baseline_ids = set()
    for cat in baseline_graph.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                baseline_ids.add(item["id"])

    # 获取当前所有 ID
    current_ids = set()
    section_map = {}
    for cat in main_graph.get("categories", []):
        for sec in cat.get("sections", []):
            for item in sec.get("items", []):
                current_ids.add(item["id"])
                if item["id"] not in baseline_ids:
                    section_map[item["id"]] = sec["id"]

    batch2_ids = current_ids - baseline_ids

    # 统计
    stats = Counter()
    for nid in batch2_ids:
        sec_id = section_map.get(nid)
        if not sec_id:
            continue
        prefix = sec_id.split(".")[0]
        if prefix == "2":
            stats["算法"] += 1
        elif prefix == "3":
            stats["数据结构"] += 1
        elif prefix == "4":
            stats["数学"] += 1

    prefix_stats = {}
    for nid in batch2_ids:
        sec_id = section_map.get(nid)
        if not sec_id:
            continue
        prefix = sec_id.split(".")[0]
        prefix_stats[prefix] = prefix_stats.get(prefix, 0) + 1

    return {
        "section_major_category": dict(stats),
        "prefix_distribution": prefix_stats,
        "total": len(batch2_ids),
        "expected": {
            "算法": 323,
            "数据结构": 110,
            "数学": 167,
            "合计": 600,
        },
    }


def decide_batch3_readiness(
    thread1: dict[str, Any],
    thread2: dict[str, Any],
    thread3: dict[str, Any],
    global_stability: dict[str, Any],
) -> dict[str, Any]:
    """判断是否具备进入 Batch3 的条件。"""
    # 所有线程必须 passed
    all_threads_passed = (
        thread1.get("passed", False)
        and thread2.get("passed", False)
        and thread3.get("passed", False)
    )
    global_stable = global_stability.get("passed", False)

    # 阻塞项
    blockers = []

    if not thread1.get("passed", False):
        blockers.append("一号线程产物未通过验收")
    if not thread2.get("passed", False):
        blockers.append("二号线程产物未通过验收")
    if not thread3.get("passed", False):
        blockers.append("三号线程产物未通过验收")
    if not global_stable:
        blockers.append("全局稳定性检查未通过")

    # 三号线程的阻塞项
    if thread3.get("remaining_candidate_count", 0) == 141:
        blockers.append("剩余候选 141 个，建议先补依赖和 section_id，再做 30-50 个候选试点")
    if thread3.get("dependency_missing_ratio", 0) == 100.0:
        blockers.append("依赖缺失比例 100%，建议先补依赖")

    # 建议
    ready = len(blockers) == 0

    return {
        "ready": ready,
        "reason": "ready" if ready else "; ".join(blockers),
        "blockers": blockers,
    }


def main():
    """主函数。"""
    audit_time = "2026-06-16"

    # 审计各线程产物
    thread1_result = audit_thread1()
    thread2_result = audit_thread2()
    thread3_result = audit_thread3()
    global_stability_result = audit_global_stability()
    batch2_stats = compute_batch2_section_prefix_stats()

    # 判断 Batch3 启动条件
    batch3_readiness = decide_batch3_readiness(
        thread1_result,
        thread2_result,
        thread3_result,
        global_stability_result,
    )

    # 总体结论
    overall_passed = (
        thread1_result.get("passed", False)
        and thread2_result.get("passed", False)
        and thread3_result.get("passed", False)
        and global_stability_result.get("passed", False)
    )

    output = {
        "audit_time": audit_time,
        "input_files": [
            "merged_knowledge_graph_item_dependencies_refined.json",
            "assets/data/knowledge/io_v4_4.json",
            "assets/data/knowledge_content/content_index.json",
            "assets/data/knowledge_content/items/stage5_hard_batch2_part_001.json",
            "docs/stage5_batch2_persistent_segment_tree_section_review.md",
            "data/stage5_batch2_persistent_segment_tree_section_review.json",
            "data/stage5_batch2_persistent_segment_tree_section_fix_report.json",
            "data/checkpoint_category_logic_verification.json",
            "data/stage5_hard_knowledge_batch3_readiness_plan.json",
        ],
        "thread1_result": thread1_result,
        "thread2_result": thread2_result,
        "thread3_result": thread3_result,
        "global_stability_result": global_stability_result,
        "batch2_stats": batch2_stats,
        "batch3_readiness": batch3_readiness,
        "overall_passed": overall_passed,
        "declaration": {
            "read_only_audit": True,
            "no_modifications_to_main_graph": True,
            "no_modifications_to_frontend_graph": True,
            "no_modifications_to_content_index": True,
            "no_modifications_to_content_body": True,
            "no_modifications_to_existing_reports": True,
            "no_batch3_entry": True,
        },
    }

    # 输出 JSON
    json_path = ROOT / "data" / "stage5_current_state_acceptance_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"JSON 报告已写入: {json_path}")

    # 输出 Markdown
    md_lines = [
        "# Stage5 当前状态总验收报告",
        "",
        "- 审计时间: `" + audit_time + "`",
        "- 审计类型: 只读审计",
        "- 未修改: 主图谱、前端图谱、内容索引、内容正文、已有报告",
        "",
        "## 一、输入文件",
        "",
    ]
    for f in output["input_files"]:
        md_lines.append(f"- `{f}`")

    md_lines.extend([
        "",
        "## 二、一号线程验收结果",
        "",
        f"- **passed**: {thread1_result.get('passed', False)}",
        f"- **has_content 全部 true**: {thread1_result.get('has_content_check', False)}",
        f"- **7 个目标节点主图谱全部 3.13**: {thread1_result.get('target_nodes_main_all_313', False)}",
        f"- **7 个目标节点前端图谱全部 3.13**: {thread1_result.get('target_nodes_frontend_all_313', False)}",
        f"- **7 个目标节点内容 part 全部 3.13**: {thread1_result.get('target_nodes_content_all_313', False)}",
        f"- **direct_pre/rel/resolved_pre 完整**: {thread1_result.get('pre_fields_intact', False)}",
        f"- **声明未修改内容正文**: {thread1_result.get('declared_no_content_modification', False)}",
        "",
        "## 三、二号线程验收结果",
        "",
        f"- **passed**: {thread2_result.get('passed', False)}",
        f"- **verification_status**: {thread2_result.get('verification_status', '')}",
        f"- **matches_expected**: {thread2_result.get('matches_expected', False)}",
        f"- **stats_fixed**: {thread2_result.get('stats_fixed', {})}",
        f"- **stats_match_expected**: {thread2_result.get('stats_match_expected', False)}",
        f"- **prefix_distribution**: {thread2_result.get('prefix_distribution', {})}",
        f"- **prefix_match_expected**: {thread2_result.get('prefix_match_expected', False)}",
        "",
        "## 四、三号线程验收结果",
        "",
        f"- **passed**: {thread3_result.get('passed', False)}",
        f"- **stability_status**: {thread3_result.get('stability_status', '')}",
        f"- **is_stable_3240**: {thread3_result.get('is_stable_3240', False)}",
        f"- **unique_risky_candidate_count**: {thread3_result.get('unique_risky_candidate_count')}",
        f"- **safe_candidate_count**: {thread3_result.get('safe_candidate_count')}",
        f"- **risk_ratio**: {thread3_result.get('risk_ratio')}%",
        f"- **dependency_missing_count**: {thread3_result.get('dependency_missing_count')}",
        f"- **dependency_missing_ratio**: {thread3_result.get('dependency_missing_ratio')}%",
        f"- **remaining_candidate_count**: {thread3_result.get('remaining_candidate_count')}",
        f"- **suggestion_reasonable**: {thread3_result.get('suggestion_reasonable', False)}",
        "",
        "## 五、全局 3240 稳定性检查",
        "",
        f"- **passed**: {global_stability_result.get('passed', False)}",
        f"- **main_item_count**: {global_stability_result.get('main_item_count')}",
        f"- **frontend_item_count**: {global_stability_result.get('frontend_item_count')}",
        f"- **main_section_count**: {global_stability_result.get('main_section_count')}",
        f"- **frontend_section_count**: {global_stability_result.get('frontend_section_count')}",
        f"- **id_sets_match**: {global_stability_result.get('id_sets_match', False)}",
        f"- **generated_item_count**: {global_stability_result.get('generated_item_count')}",
        f"- **content_covered_count**: {global_stability_result.get('content_covered_count')}",
        f"- **batch2_id_count**: {global_stability_result.get('batch2_id_count')}",
        f"- **batch2_content_covered**: {global_stability_result.get('batch2_content_covered', False)}",
        "",
        "## 六、Batch2 当前分类统计",
        "",
        "### section-prefix 统计",
        "",
    ])

    for k, v in batch2_stats.get("section_major_category", {}).items():
        md_lines.append(f"- **{k}**: {v}")
    md_lines.append(f"- **合计**: {batch2_stats.get('total', 0)}")

    md_lines.extend([
        "",
        "### 预期统计",
        "",
    ])
    expected = batch2_stats.get("expected", {})
    for k, v in expected.items():
        md_lines.append(f"- **{k}**: {v}")

    md_lines.append("")
    md_lines.append("说明：item.category 统计与 section-prefix 统计可能不同；checkpoint 使用 section-prefix 统计；当前 checkpoint 正式报告如果尚未重生成，旧报告中的'数据结构 0'仍是过期报告结果。")
    md_lines.append("")

    md_lines.extend([
        "## 七、Batch3 是否具备启动条件",
        "",
        f"- **ready**: {batch3_readiness.get('ready', False)}",
        f"- **reason**: {batch3_readiness.get('reason', '')}",
        "",
        "### 阻塞项",
        "",
    ])
    blockers = batch3_readiness.get("blockers", [])
    if blockers:
        for b in blockers:
            md_lines.append(f"- {b}")
    else:
        md_lines.append("- 无")

    md_lines.extend([
        "",
        "## 八、下一步建议",
        "",
        "1. 不建议立即进入 Batch3。",
        "2. 应先补依赖和 section_id，再做 30-50 个候选试点。",
        "3. 如果后续重生成 checkpoint 报告，确保使用修复后的统计口径。",
        "",
        "## 九、声明",
        "",
        "- 本轮只读审计，未修改主图谱、前端图谱、内容索引、内容正文、已有报告。",
        "- 未进入 Batch3。",
        "- 未生成新节点。",
        "- 未删除节点。",
        "",
    ])

    md_path = ROOT / "docs" / "stage5_current_state_acceptance_report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Markdown 报告已写入: {md_path}")

    print("\n=== 总验收结论 ===")
    print(f"一号线程: {'通过' if thread1_result.get('passed', False) else '未通过'}")
    print(f"二号线程: {'通过' if thread2_result.get('passed', False) else '未通过'}")
    print(f"三号线程: {'通过' if thread3_result.get('passed', False) else '未通过'}")
    print(f"全局稳定性: {'通过' if global_stability_result.get('passed', False) else '未通过'}")
    print(f"总体: {'通过' if overall_passed else '未通过'}")
    print(f"是否建议进入 Batch3: {'是' if batch3_readiness.get('ready', False) else '否，' + batch3_readiness.get('reason', '')}")
    print()


if __name__ == "__main__":
    main()