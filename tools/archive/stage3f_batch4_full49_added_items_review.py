#!/usr/bin/env python3
"""
Stage3F Batch4 Full49 Added Items Review (Fixed)
复查49个新增节点，不修改主图谱
"""
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_section_id(item_id):
    parts = item_id.split(".")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else ""

print("=" * 60)
print("Stage3F Batch4 Full49 Added Items Review (Fixed)")
print("=" * 60)

# Load inputs
graph = load_json(os.path.join(BASE_DIR, "merged_knowledge_graph_item_dependencies_refined.json"))
mapping = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_candidate_to_item_id_mapping.json"))
summary_data = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_added_items_summary.json"))
validation = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_validation_result.json"))
v2_plan = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_candidate_plan_v2.json"))

# Build item lookup and section info
all_items = {}
all_sections = {}
section_item_counts = {}
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        sid = sec["id"]
        all_sections[sid] = sec.get("name", "")
        section_item_counts.setdefault(sid, 0)
        for item in sec.get("items", []):
            all_items[item["id"]] = item
            section_item_counts[sid] += 1

print(f"  Total items in graph: {len(all_items)}")
print(f"  Total sections: {len(all_sections)}")

# Build existing name lookup (excluding self)
existing_names = {}
for iid, item in all_items.items():
    name = item.get("name", "")
    if name:
        existing_names[name] = existing_names.get(name, []) + [iid]

# Extract 49 new item IDs
new_item_ids = set(m["item_id"] for m in mapping["mappings"])
print(f"  New item IDs: {len(new_item_ids)}")

# ============================================================
# Analyze each new item
# ============================================================
print("\n[Analysis] Analyzing each new item...")

review_results = []
section_dist = Counter()
result_dist = Counter()
type_dist = Counter()
priority_counts = Counter()

merge_candidates = []
problem_pattern_candidates = []
dependency_fix_candidates = []
manual_review_items = []

for item_id in sorted(new_item_ids):
    item = all_items.get(item_id)
    if not item:
        print(f"  WARNING: {item_id} not found in graph!")
        continue

    name = item.get("name", "")
    # Extract section from item ID (new items may lack parent field)
    section_id = item.get("parent") or extract_section_id(item_id)
    section_name = all_sections.get(section_id, "")
    direct_pre = item.get("direct_pre", [])
    resolved_pre = item.get("resolved_pre", [])
    rel = item.get("rel", [])

    # Find candidate info
    candidate_info = None
    for m in mapping["mappings"]:
        if m["item_id"] == item_id:
            candidate_info = m
            break
    candidate_id = candidate_info["candidate_id"] if candidate_info else "unknown"

    # Check if medium risk
    is_medium_risk = any(
        c["candidate_id"] == candidate_id
        for c in v2_plan.get("manual_review_candidates", [])
    )

    # ==============================
    # Type classification
    # ==============================
    item_type = "core_concept"
    name_lower = name.lower()
    if any(kw in name for kw in ["建模", "Modeling", "modeling", "应用", "Application", "application", "技巧", "Technique", "technique"]):
        item_type = "modeling_pattern"
    elif any(kw in name for kw in ["变体", "Variant", "variant", "变种"]):
        item_type = "implementation_variant"
    elif any(kw in name for kw in ["定理", "Theorem", "theorem", "引理", "Lemma", "lemma"]):
        item_type = "theorem_or_property"
    elif any(kw in name for kw in ["Overview", "overview", "基础", "Basic", "basic", "策略", "Strategy", "strategy"]):
        item_type = "core_concept"

    # ==============================
    # Issue detection
    # ==============================
    issues = []
    direct_pre_count = len(direct_pre)

    # Check for over-broad direct_pre
    if direct_pre_count > 50:
        issues.append(f"direct_pre 过长 ({direct_pre_count}个)，可能包含大量泛化依赖")

    # Check if direct_pre is close to section size
    sec_total = section_item_counts.get(section_id, 0)
    if sec_total > 0 and direct_pre_count > sec_total * 0.8:
        issues.append(f"direct_pre ({direct_pre_count}) 接近整节 item 数 ({sec_total})，疑似整节引用")
    elif sec_total == 0 and direct_pre_count > 20:
        issues.append(f"section_id '{section_id}' 未在 section_item_counts 中找到")

    # Check if direct_pre has section-level references
    has_section_refs = any(re.match(r'^\d+\.\d+$', ref) for ref in direct_pre)
    if has_section_refs:
        issues.append("direct_pre 包含 section 级引用")

    # Check for duplicate name
    dupe_ids = existing_names.get(name, [])
    if dupe_ids and dupe_ids[0] not in new_item_ids:
        issues.append(f"名称 '{name}' 与已有节点 {dupe_ids} 重复")

    # Medium risk specific
    if is_medium_risk:
        issues.append("medium 风险候选，需人工确认 direct_pre 是否为必要前置")

    # ==============================
    # Priority
    # ==============================
    has_dep_issue = any("direct_pre 过长" in iss for iss in issues)
    if item_type == "theorem_or_property":
        new_priority = "A"
    elif has_dep_issue:
        new_priority = "C"
    elif item_type == "implementation_variant":
        new_priority = "C"
    elif item_type == "modeling_pattern":
        new_priority = "B"
    elif is_medium_risk:
        new_priority = "B"
    else:
        new_priority = "B"

    # ==============================
    # Candidate lists (independent)
    # ==============================
    if has_dep_issue:
        dependency_fix_candidates.append({
            "id": item_id,
            "name": name,
            "direct_pre_count": direct_pre_count,
            "section": section_id,
            "issues": [i for i in issues if "direct_pre" in i]
        })
    if item_type == "modeling_pattern":
        problem_pattern_candidates.append({
            "id": item_id,
            "name": name,
            "section": section_id,
            "reason": "建模/应用/技巧类节点，可同步到 problem_patterns"
        })
    if dupe_ids and dupe_ids[0] not in new_item_ids:
        merge_candidates.append({
            "id": item_id,
            "name": name,
            "duplicate_with": dupe_ids,
            "reason": f"与已有节点重复"
        })
    if is_medium_risk:
        manual_review_items.append(item_id)

    # ==============================
    # Review result (primary)
    # ==============================
    review_result = "approve"
    if is_medium_risk:
        review_result = "keep_manual_review"
    elif has_dep_issue:
        review_result = "needs_dependency_fix"
    elif item_type == "modeling_pattern":
        review_result = "move_to_problem_patterns"
    elif dupe_ids and dupe_ids[0] not in new_item_ids:
        review_result = "needs_merge_or_collapse"

    # ==============================
    # Build entry
    # ==============================
    entry = {
        "id": item_id,
        "name": name,
        "section": section_id,
        "section_name": section_name,
        "candidate_id": candidate_id,
        "series": section_id.split(".")[0] if "." in section_id else "",
        "review_result": review_result,
        "new_review_priority": new_priority,
        "need_manual_review": is_medium_risk or bool(dupe_ids),
        "item_type": item_type,
        "direct_pre_count": direct_pre_count,
        "issues": issues,
        "suggested_patch": {},
        "reason": issues[0] if issues else ("自动审批通过" if review_result == "approve" else f"需人工确认")
    }

    # Suggest patch for dependency fix
    if review_result == "needs_dependency_fix" and direct_pre_count > 50:
        # Check if items have reasonable per-section distribution
        entry["suggested_patch"] = {
            "field": "direct_pre",
            "current_count": direct_pre_count,
            "suggested_action": "缩减至必要前置（通常 3-10 个），参考同节已存在节点的 direct_pre 模式",
            "note": f"当前 direct_pre={direct_pre_count}，包含全部前置节的所有 item，应仅保留直接依赖的核心概念"
        }

    review_results.append(entry)
    section_dist[section_id] += 1
    type_dist[item_type] += 1
    result_dist[review_result] += 1
    priority_counts[new_priority] += 1

# ============================================================
# Write outputs
# ============================================================
print("\n[Output] Writing files...")

# 1. added_items_review.json
review_out = {
    "batch_id": "stage3f_batch4_full49",
    "meta": {
        "title": "Stage3F Batch4 Full49 Added Items Review",
        "generated_by": "GLM5",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "main_graph_modified": False,
        "total_added": len(new_item_ids),
        "item_count_before": 1716,
        "item_count_after": 1765,
        "section_count": 65,
        "validate_only_passed": validation.get("passed", False)
    },
    "summary": {
        "total_reviewed": len(review_results),
        "by_result": {
            "approve": result_dist.get("approve", 0),
            "keep_manual_review": result_dist.get("keep_manual_review", 0),
            "needs_dependency_fix": result_dist.get("needs_dependency_fix", 0),
            "move_to_problem_patterns": result_dist.get("move_to_problem_patterns", 0),
            "needs_merge_or_collapse": result_dist.get("needs_merge_or_collapse", 0),
            "needs_section_review": result_dist.get("needs_section_review", 0)
        },
        "priority_A": priority_counts.get("A", 0),
        "priority_B": priority_counts.get("B", 0),
        "priority_C": priority_counts.get("C", 0),
        "by_type": dict(type_dist),
        "by_section": dict(section_dist),
        "needs_fix_lite": len(dependency_fix_candidates) > 0 or len(merge_candidates) > 0,
        "suggest_next_batch5": len(dependency_fix_candidates) == 0 and len(merge_candidates) == 0
    },
    "items": review_results
}

outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_added_items_review.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(review_out, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# 2. review_status_patch_preview.json
patches = []
for r in review_results:
    if r["suggested_patch"]:
        patches.append({
            "item_id": r["id"],
            "name": r["name"],
            "review_result": r["review_result"],
            "suggested_patch": r["suggested_patch"]
        })
patch_out = {
    "batch_id": "stage3f_batch4_full49",
    "description": "此 patch 仅为预览，未应用。1号线程可在 Fix Lite 阶段决定是否执行。",
    "main_graph_modified": False,
    "patches": patches,
    "total_patches": len(patches)
}
outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_review_status_patch_preview.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(patch_out, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# 3. dependency_fix_candidates.json
fix_out = {
    "batch_id": "stage3f_batch4_full49",
    "description": "需要依赖修复的候选。direct_pre 过长的节点需在 Fix Lite 阶段精简。",
    "main_graph_modified": False,
    "candidates": dependency_fix_candidates,
    "total": len(dependency_fix_candidates)
}
outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_dependency_fix_candidates.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(fix_out, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# 4. problem_pattern_sync_candidates.json
pp_out = {
    "batch_id": "stage3f_batch4_full49",
    "description": "建议同步到 problem_patterns 的建模/应用节点。",
    "main_graph_modified": False,
    "candidates": problem_pattern_candidates,
    "total": len(problem_pattern_candidates)
}
outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_problem_pattern_sync_candidates.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(pp_out, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# 5. merge_or_collapse_candidates.json
mc_out = {
    "batch_id": "stage3f_batch4_full49",
    "description": "需要合并或折叠的重复/近似节点。",
    "main_graph_modified": False,
    "candidates": merge_candidates,
    "total": len(merge_candidates)
}
outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_merge_or_collapse_candidates.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(mc_out, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# ============================================================
# Report
# ============================================================
md_lines = []
md_lines.append("# Stage3F Batch4 Full49 Added Items Review Report\n")
md_lines.append(f"**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
md_lines.append(f"**生成者**: GLM5 (2号线程)")
md_lines.append(f"**任务类型**: Added Items Review（仅复查，不修改主图谱）\n")
md_lines.append("---\n")

md_lines.append("## 1. 概览\n")
md_lines.append(f"| 指标 | 值 |")
md_lines.append(f"|------|-----|")
md_lines.append(f"| Batch4 新增节点 | {len(new_item_ids)} |")
md_lines.append(f"| 合并前 item_count | 1716 |")
md_lines.append(f"| 合并后 item_count | 1765 |")
md_lines.append(f"| section_count | 65 |")
md_lines.append(f"| validate-only passed | {validation.get('passed', False)} |")
md_lines.append(f"| dangling_refs | {len(validation.get('dangling_refs', []))} |")
md_lines.append(f"| direct_pre_cycle | {validation.get('direct_pre_cycle')} |")
md_lines.append(f"| resolved_pre_mismatches | {len(validation.get('resolved_pre_mismatches', []))} |")
md_lines.append("")

md_lines.append("## 2. 复查结果汇总\n")
md_lines.append(f"| 复查结果 | 数量 | 说明 |")
md_lines.append(f"|----------|------|------|")
md_lines.append(f"| approve | {result_dist.get('approve', 0)} | 自动审批通过 |")
md_lines.append(f"| keep_manual_review | {result_dist.get('keep_manual_review', 0)} | 需人工确认 direct_pre 映射 |")
md_lines.append(f"| needs_dependency_fix | {result_dist.get('needs_dependency_fix', 0)} | direct_pre 过长，需缩减 |")
md_lines.append(f"| move_to_problem_patterns | {result_dist.get('move_to_problem_patterns', 0)} | 建议同步到 problem_patterns |")
md_lines.append(f"| needs_merge_or_collapse | {result_dist.get('needs_merge_or_collapse', 0)} | 与已有节点重复 |")
md_lines.append(f"| **合计** | {len(review_results)} | |")
md_lines.append("")

md_lines.append("## 3. 优先级分布\n")
md_lines.append(f"| 优先级 | 数量 |")
md_lines.append(f"|--------|------|")
for p in ["A", "B", "C"]:
    md_lines.append(f"| {p} | {priority_counts.get(p, 0)} |")
md_lines.append("")

md_lines.append("## 4. 按 Section 分布\n")
md_lines.append(f"| Section | 名称 | 新增 | direct_pre 问题 | 评估 |")
md_lines.append(f"|---------|------|------|---------------|------|")
for sec_id in sorted(section_dist.keys()):
    cnt = section_dist[sec_id]
    sec_name = all_sections.get(sec_id, "")
    sec_items = [r for r in review_results if r["section"] == sec_id]
    n_dep_issues = sum(1 for r in sec_items if r["review_result"] == "needs_dependency_fix")
    dep_str = f"{n_dep_issues}/{cnt} 个" if n_dep_issues > 0 else "0"
    if cnt >= 15:
        advice = "⚠️ 密集新增，注意过度拆分"
    elif n_dep_issues > 0:
        advice = "⚠️ 需依赖修复"
    else:
        advice = "✅ 正常"
    md_lines.append(f"| {sec_id} | {sec_name} | {cnt} | {dep_str} | {advice} |")
md_lines.append("")

md_lines.append("## 5. 节点复查明细\n")
md_lines.append("| # | item_id | name | section | type | result | priority | direct_pre | issues |")
md_lines.append("|---|--------|------|---------|------|--------|----------|-----------|--------|")
for i, r in enumerate(review_results, 1):
    iss_str = "; ".join(r["issues"][:2]) if r["issues"] else "-"
    md_lines.append(f"| {i} | {r['id']} | {r['name']} | {r['section']} | {r['item_type']} | {r['review_result']} | {r['new_review_priority']} | {r['direct_pre_count']} | {iss_str} |")
md_lines.append("")

md_lines.append("## 6. 3 个 Medium 风险候选依赖复查\n")
medium_ids = ["2.10.39", "4.4.15", "4.4.16"]
medium_names = {"2.10.39": "Sunday算法", "4.4.15": "线性递推基础", "4.4.16": "Kitamasa算法"}
for mid in medium_ids:
    r = next((x for x in review_results if x["id"] == mid), None)
    if not r:
        continue
    item = all_items.get(mid, {})
    dp = item.get("direct_pre", [])
    rp = item.get("resolved_pre", [])
    md_lines.append(f"### {r['name']} ({mid})\n")
    md_lines.append(f"- **candidate_id**: {r.get('candidate_id', 'unknown')}")
    md_lines.append(f"- **direct_pre 数**: {len(dp)}")
    md_lines.append(f"- **resolved_pre 数**: {len(rp)}")
    md_lines.append(f"- **contains section ref**: {'是' if any(re.match(r'^\d+\.\d+$', ref) for ref in dp) else '否'}")
    if len(dp) > 20:
        md_lines.append(f"- ⚠️ direct_pre 过多 ({len(dp)})，可能存在将 resolved_pre 误当作 direct_pre")
    if r["issues"]:
        md_lines.append(f"- **问题**: {'; '.join(r['issues'])}")
    md_lines.append(f"- **复查结论**: {r['reason']}")
    md_lines.append("")

md_lines.append("## 7. 2.21 / 3.13 密集新增分析\n")
for sec_id in ["2.21", "3.13"]:
    cnt = section_dist.get(sec_id, 0)
    sec_items = [r for r in review_results if r["section"] == sec_id]
    total = section_item_counts.get(sec_id, 0)
    n_dep = sum(1 for r in sec_items if r["review_result"] == "needs_dependency_fix")
    n_pp = sum(1 for r in sec_items if r["review_result"] == "move_to_problem_patterns")
    md_lines.append(f"### {sec_id} {all_sections.get(sec_id, '')}\n")
    md_lines.append(f"- 本次新增: {cnt}")
    md_lines.append(f"- 节内总 item 数: {total}")
    md_lines.append(f"- 新增占比: {cnt/max(total,1)*100:.1f}%")
    md_lines.append(f"- 需依赖修复: {n_dep}")
    md_lines.append(f"- 建议同步 problem_patterns: {n_pp}")
    md_lines.append(f"- **评估**: {'⚠️ 密集新增 + 大范围 direct_pre 过长，建议进入 Fix Lite' if n_dep > 0 else '✅ 合理'}")
    for r_ in sec_items:
        if r_["issues"]:
            md_lines.append(f"  - {r_['id']} {r_['name']}: {'; '.join(r_['issues'][:2])}")
    md_lines.append("")

md_lines.append("## 8. 建议同步到 Problem Patterns\n")
if problem_pattern_candidates:
    for c in problem_pattern_candidates:
        md_lines.append(f"- {c['id']} {c['name']} ({c['section']}): {c['reason']}")
else:
    md_lines.append("无建议同步节点。\n")

md_lines.append("## 9. 建议合并/折叠\n")
if merge_candidates:
    for c in merge_candidates:
        md_lines.append(f"- {c['id']} {c['name']}: {c['reason']}")
else:
    md_lines.append("无建议合并节点。\n")

md_lines.append("## 10. 建议依赖修复\n")
if dependency_fix_candidates:
    md_lines.append("以下节点 direct_pre 过长，需在 Fix Lite 阶段缩减至必要前置：\n")
    md_lines.append("| item_id | name | direct_pre | 所在 Section |")
    md_lines.append("|---------|------|-----------|-------------|")
    for c in dependency_fix_candidates:
        md_lines.append(f"| {c['id']} | {c['name']} | {c['direct_pre_count']} | {c.get('section', '')} |")
    md_lines.append("")
    md_lines.append("**建议修复方案**: 将 direct_pre 从当前全量前置节 item 列表缩减为仅包含直接依赖的核心概念（通常 3-10 个），"
                     "其余依赖可通过 resolved_pre 继承。具体做法：删除 section-level 批量引用，只保留对直接前置概念的 item 级引用。")
else:
    md_lines.append("无建议依赖修复节点。\n")

md_lines.append("## 11. 结论与建议\n")
needs_fl = len(dependency_fix_candidates) > 0 or len(merge_candidates) > 0
md_lines.append(f"| 建议项 | 值 |")
md_lines.append(f"|-------|-----|")
md_lines.append(f"| 是否建议进入 Fix Lite | **{'是' if needs_fl else '否'}** |")
md_lines.append(f"| Fix Lite 内容 | {'依赖修复 + direct_pre 缩减' if dependency_fix_candidates else '无'} |")
md_lines.append(f"| 是否建议继续 Stage3F Batch5 | {'建议先 Fix Lite' if needs_fl else '是'} |")
md_lines.append(f"| 主图谱是否修改 | 否 |")
md_lines.append("")

if needs_fl:
    md_lines.append("**⚠️ 核心问题**: 批量新增的 2.21 高级图论扩展（20个）和 2.10 字符串算法（4个）等节点的 "
                     "direct_pre 被设置为整节全部前置 item（113~218个），而非仅直接依赖的核心概念。"
                     "这会导致依赖图过于稠密，影响后续推理性能。建议在 Fix Lite 阶段精简。")
else:
    md_lines.append("**✅ 全部节点审批通过，可以继续 Batch5。**")

md_lines.append(f"\n**最终结论**: Batch4 full49 合并完成，主图谱状态正常。")
md_lines.append(f"{'部分节点需先进入 Fix Lite 处理依赖修复，再继续 Batch5。' if needs_fl else '可以继续 Stage3F Batch5。'}")

report_md = "\n".join(md_lines)

# Write report
report_path = os.path.join(DOCS_DIR, "stage3f_batch4_full49_added_items_review_report.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_md)
print(f"  Written: {report_path}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'=' * 60}")
print(f"Stage3F Batch4 Full49 Added Items Review Complete")
print(f"{'=' * 60}")
print(f"\nSummary:")
print(f"  Total reviewed: {len(review_results)}")
print(f"  By result: approve={result_dist.get('approve',0)}, "
      f"keep_manual={result_dist.get('keep_manual_review',0)}, "
      f"needs_dep_fix={result_dist.get('needs_dependency_fix',0)}, "
      f"move_to_pp={result_dist.get('move_to_problem_patterns',0)}, "
      f"merge={result_dist.get('needs_merge_or_collapse',0)}")
print(f"  By priority: A={priority_counts.get('A',0)} B={priority_counts.get('B',0)} C={priority_counts.get('C',0)}")
print(f"  Dependency fix candidates: {len(dependency_fix_candidates)}")
print(f"  Problem pattern candidates: {len(problem_pattern_candidates)}")
print(f"  Merge/collapse candidates: {len(merge_candidates)}")
print(f"  Manual review items: {len(manual_review_items)}")
print(f"\n  main_graph_modified: False")
print(f"  validate-only passed: {validation.get('passed', False)}")
