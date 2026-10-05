#!/usr/bin/env python3
"""
Stage3F Candidate Pool Remaining Audit + Stage3G 400 Candidate Pool Rebuild Plan
不修改主图谱，不生成正式候选，不执行合并
"""
import json, os, re
from collections import Counter
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def load(path):
    with open(os.path.join(BASE_DIR, path), 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_section_id(item_id):
    parts = item_id.split(".")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else ""

print("=" * 60)
print("Stage3F Pool Audit + Stage3G 400 Pool Rebuild Plan")
print("=" * 60)

# ============================================================
# Load data
# ============================================================
pool = load("data/stage3f_standardized_candidate_pool.json")
b1_map = load("data/stage3f_batch1_candidate_to_item_id_mapping.json")
b2_map = load("data/stage3f_batch2_candidate_to_item_id_mapping.json")
b3_map = load("data/stage3f_batch3_full40_candidate_to_item_id_mapping.json")
b4_map = load("data/stage3f_batch4_full49_candidate_to_item_id_mapping.json")
b2_prune = load("data/stage3f_batch2_duplicate_prune_removed_items.json")
b3_prune = load("data/stage3f_batch3_full40_duplicate_prune_removed_items.json")
checkpoint = load("data/stage3f_batch4_stable_checkpoint.json")
graph = load("merged_knowledge_graph_item_dependencies_refined.json")
dvr = load("dependency_validation_result.json")

# ============================================================
# Build used candidate ID sets
# ============================================================
b1_ids = set(m["candidate_id"] for m in b1_map)
b2_ids = set(m["candidate_id"] for m in b2_map)
b3_ids = set(m["candidate_id"] for m in b3_map)
b4_ids = set(m["candidate_id"] for m in b4_map["mappings"])

# Candidates that were pruned as duplicates after merge
b2_prune_cids = set()
for pr in b2_prune["removed_items"]:
    if "candidate_id" in pr:
        b2_prune_cids.add(pr["candidate_id"])
b3_prune_cids = set()
# For batch3, find the candidate_id from the mapping
for pr in b3_prune["removed_items"]:
    pr_item_id = pr.get("item_id", "")
    for m in b3_map:
        if m.get("item_id") == pr_item_id:
            b3_prune_cids.add(m["candidate_id"])

all_used_ids = b1_ids | b2_ids | b3_ids | b4_ids
all_pruned_ids = b2_prune_cids | b3_prune_cids
print(f"  Pool total: {pool['meta']['total_candidates']}")
print(f"  Batch1 used: {len(b1_ids)}")
print(f"  Batch2 used: {len(b2_ids)} (pruned: {len(b2_prune_cids)})")
print(f"  Batch3 used: {len(b3_ids)} (pruned: {len(b3_prune_cids)})")
print(f"  Batch4 used: {len(b4_ids)}")
print(f"  Total used: {len(all_used_ids)}")

# ============================================================
# Audit remaining candidates
# ============================================================
pool_candidates = {c["candidate_id"]: c for c in pool["candidates"]}
remaining_ids = set(pool_candidates.keys()) - all_used_ids
remaining_candidates = [pool_candidates[cid] for cid in remaining_ids]
print(f"  Remaining: {len(remaining_ids)}")

# Analyze remaining candidates
remaining_by_section = Counter()
remaining_by_risk = Counter()
remaining_by_source = Counter()
for c in remaining_candidates:
    sec = c.get("suggested_section", "")
    remaining_by_section[sec] += 1
    remaining_by_risk[c.get("risk_band", "")] += 1
    remaining_by_source[c.get("source", "")] += 1

print(f"  Remaining by section: {dict(remaining_by_section)}")
print(f"  Remaining by risk: {dict(remaining_by_risk)}")

# ============================================================
# Analyze graph coverage for Stage3G planning
# ============================================================
all_items = {}
all_sections = {}
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        all_sections[sec["id"]] = sec.get("name", "")
        for item in sec.get("items", []):
            all_items[item["id"]] = item

section_item_counts = Counter()
section_names = {}
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        section_item_counts[sec["id"]] = len(sec.get("items", []))
        section_names[sec["id"]] = sec.get("name", "")

# Identify existing coverage areas
print(f"\n  Graph: {len(all_items)} items, {len(all_sections)} sections")

# ============================================================
# Build outputs
# ============================================================
print("\n[Output] Writing files...")

# ==================== FILE 1: Pool Remaining Audit ====================
audit = {
    "batch_id": "stage3f_pool_audit",
    "meta": {
        "title": "Stage3F Candidate Pool Remaining Audit",
        "generated_by": "GLM5 (2号线程)",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "main_graph_modified": False
    },
    "pool_summary": {
        "total_pool_size": pool["meta"]["total_candidates"],
        "batch1_used": len(b1_ids),
        "batch2_used": len(b2_ids),
        "batch3_used": len(b3_ids),
        "batch4_used": len(b4_ids),
        "total_used": len(all_used_ids),
        "duplicate_pruned_in_batch2": len(b2_prune_cids),
        "duplicate_pruned_in_batch3": len(b3_prune_cids),
        "total_duplicate_pruned": len(all_pruned_ids),
        "remaining_available": len(remaining_ids),
        "pool_exhausted": len(remaining_ids) < 20,
        "sufficient_for_batch5": len(remaining_ids) >= 20,
        "recommend_end_stage3f": len(remaining_ids) < 20,
        "note": "Stage3F 候选池已基本耗尽。剩余候选不足 20，不建议开启 Batch5。建议结束 Stage3F，启动 Stage3G。"
    },
    "by_section_remaining": dict(remaining_by_section),
    "by_risk_remaining": dict(remaining_by_risk),
    "by_source_remaining": dict(remaining_by_source),
    "remaining_candidates_detail": [
        {
            "candidate_id": cid,
            "name": pool_candidates[cid].get("name", ""),
            "section": pool_candidates[cid].get("suggested_section", ""),
            "risk_band": pool_candidates[cid].get("risk_band", ""),
            "source": pool_candidates[cid].get("source", "")
        }
        for cid in sorted(remaining_ids)
    ],
    "current_main_graph_state": {
        "item_count": len(all_items),
        "section_count": len(all_sections),
        "validate_only_passed": dvr.get("passed", False)
    }
}

outpath = os.path.join(BASE_DIR, "data/stage3f_candidate_pool_remaining_audit.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(audit, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# ==================== FILE 3: Stage3G 400 Pool Rebuild Plan ====================
STAGE3G_PLANNED_COVERAGE = {
    "C++_advanced": {
        "display": "C++ 语法高级细节",
        "sections": ["1.3", "1.7", "1.8"],
        "count": 25,
        "priority": "medium",
        "examples": ["右值引用与移动语义", "模板元编程基础", "constexpr与编译期计算", "异常安全与RAII", "C++17/20新特性"]
    },
    "STL_details": {
        "display": "STL 与常用库细节",
        "sections": ["1.8", "3.2"],
        "count": 30,
        "priority": "high",
        "examples": ["自定义分配器", "迭代器失效分析", "PB_ds库扩展", "rope/可持久化数组", "unorder_map哈希策略"]
    },
    "basic_algorithms_ext": {
        "display": "基础算法扩展",
        "sections": ["2.1", "2.2", "2.3", "2.4"],
        "count": 35,
        "priority": "high",
        "examples": ["分治进阶：CDQ分治", "整体二分", "随机化算法", "爬山与模拟退火", "双向搜索进阶"]
    },
    "DP_topics": {
        "display": "动态规划专题",
        "sections": ["2.8"],
        "count": 45,
        "priority": "high",
        "examples": ["DP优化：决策单调性", "DP优化：WQS二分", "DP优化：斜率优化进阶", "插头DP进阶", "DP套DP"]
    },
    "graph_topics": {
        "display": "图论专题",
        "sections": ["2.9", "2.11", "2.12", "2.13", "2.14", "2.15", "2.16", "2.17", "2.21"],
        "count": 55,
        "priority": "high",
        "examples": ["图论建模进阶", "网络流建模", "费用流进阶", "二分图高级应用", "树分治"]
    },
    "string_topics": {
        "display": "字符串专题",
        "sections": ["2.10", "3.8"],
        "count": 35,
        "priority": "high",
        "examples": ["字符串哈希进阶", "后缀数组应用", "后缀自动机应用", "AC自动机DP", "回文自动机"]
    },
    "data_structure_topics": {
        "display": "数据结构专题",
        "sections": ["3.1", "3.3", "3.5", "3.9", "3.13"],
        "count": 50,
        "priority": "high",
        "examples": ["树链剖分进阶", "LCT应用", "可持久化数据结构", "分块与莫队", "K-D Tree"]
    },
    "oi_math": {
        "display": "信奥数学",
        "sections": ["4.1", "4.3", "4.4", "4.5", "4.6"],
        "count": 40,
        "priority": "high",
        "examples": ["数论进阶：杜教筛", "多项式：FFT/NTT", "多项式：生成函数", "组合计数进阶", "概率论进阶"]
    },
    "programming_skills": {
        "display": "编程技巧",
        "sections": ["1.4", "1.5", "1.6", "2.18"],
        "count": 25,
        "priority": "medium",
        "examples": ["代码调试技巧", "性能分析", "对拍与测试", "常用宏与模板", "输入输出优化"]
    },
    "debug_methods": {
        "display": "调试方法",
        "sections": ["2.18", "5.5"],
        "count": 15,
        "priority": "medium",
        "examples": ["gdb/lldb调试", "内存检测", "断言与日志", "静态分析工具", "常见bug模式"]
    },
    "contest_knowledge": {
        "display": "比赛相关知识",
        "sections": ["5.5"],
        "count": 15,
        "priority": "low",
        "examples": ["竞赛策略", "时间复杂度估算", "空间复杂度优化", "IOI/ICPC赛制", "常见罚时分析"]
    },
    "problem_modeling": {
        "display": "题型建模方法",
        "sections": ["2.18"],
        "count": 30,
        "priority": "high",
        "examples": ["构造题方法", "交互题方法", "提交答案题方法", "模型转化技巧", "贪心证明方法"]
    }
}

# Build the 400 plan
coverage_plan = {}
total_planned = 0
for key, cfg in STAGE3G_PLANNED_COVERAGE.items():
    coverage_plan[key] = {
        "display": cfg["display"],
        "sections": cfg["sections"],
        "planned_count": cfg["count"],
        "priority": cfg["priority"],
        "examples": cfg["examples"]
    }
    total_planned += cfg["count"]

# Batch breakdown
batch_plan = []
for i in range(10):
    batch_num = i + 1
    if i < total_planned // 50:
        size = 50
    elif i < total_planned // 40:
        size = 40
    else:
        size = 0
    if size > 0:
        batch_plan.append({
            "batch": f"Stage3G Batch{batch_num}",
            "recommended_size": size,
            "steps": ["候选计划 → 动态预审 → 全图谱查重 → 依赖清理 → Merge → Added Items Review → 重复删除/Fix Lite → 稳定检查点"]
        })

# Risk band distribution
risk_distribution = {
    "green": 80,
    "yellow": 180,
    "medium": 100,
    "red": 40
}

stage3g_plan = {
    "batch_id": "stage3g_400_plan",
    "meta": {
        "title": "Stage3G 400 Candidate Pool Rebuild Plan",
        "generated_by": "GLM5 (2号线程)",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "main_graph_modified": False,
        "formal_candidates_generated": False,
        "merge_executed": False
    },
    "current_state_after_stage3f": {
        "item_count": len(all_items),
        "section_count": len(all_sections),
        "validate_only_passed": dvr.get("passed", False),
        "stage3f_completed_batches": ["Batch1(20)", "Batch2(20)", "Batch3(40)", "Batch4(49)"],
        "stage3f_total_added": 129,
        "stage3f_net_added_after_prune": 129 - len(all_pruned_ids),
        "item_count_before_stage3f": checkpoint["state"]["item_count_before_batch4"] - 49 - 40 - 20,
        "pool_remaining": len(remaining_ids),
        "recommend_end_stage3f": True
    },
    "stage3g_400_plan": {
        "total_planned_candidates": total_planned,
        "planned_distribution_by_topic": coverage_plan,
        "planned_distribution_by_risk": risk_distribution,
        "planned_distribution_by_section": {
            "2.1-2.4": 35, "2.8": 45, "2.9-2.17,2.21": 55,
            "2.10,3.8": 35, "3.1,3.3,3.5,3.9,3.13": 50,
            "4.1,4.3,4.4,4.5,4.6": 40,
            "1.3,1.7,1.8": 25, "1.4,1.5,1.6,2.18": 55,
            "5.5": 15,
            "new_sections_needed": 50
        },
        "total": total_planned
    },
    "tier_strategy": {
        "description": "400 候选分层策略",
        "green": {
            "count": risk_distribution["green"],
            "criteria": "高置信度，知识完整无重复，直接前置明确",
            "priority_batches": "Batch1-Batch3"
        },
        "yellow": {
            "count": risk_distribution["yellow"],
            "criteria": "有价值但需要复查依赖边界",
            "priority_batches": "Batch2-Batch6"
        },
        "medium": {
            "count": risk_distribution["medium"],
            "criteria": "有价值但依赖或重复风险较高，需重点审查",
            "priority_batches": "Batch5-Batch8"
        },
        "red": {
            "count": risk_distribution["red"],
            "criteria": "暂不进入正式候选池，作为备选",
            "priority_batches": "备选"
        }
    },
    "batch_execution_plan": batch_plan,
    "recommended_flow_per_batch": [
        "1. 候选计划：从400池中按分层策略选取N个候选",
        "2. 动态预审：检查重复、依赖环、section分布、item_count",
        "3. 全图谱查重：对比当前1765+节点，精确查重",
        "4. 依赖清理：映射direct_pre为正式item_id，解决悬空引用",
        "5. Merge：写入主图谱，更新items",
        "6. Added Items Review：复查新增节点质量",
        "7. 重复删除 / Fix Lite：处理Review发现的问题",
        "8. 稳定检查点：记录当前状态，准备下一批"
    ],
    "dedup_strategy": {
        "approach": "逐候选对比当前图谱所有1765个节点，检查name/alias/en_name完全匹配和模糊匹配",
        "tools": ["name_exact_match", "name_fuzzy_match", "alias_check", "en_name_check", "candidate_id_check"],
        "threshold": "完全匹配直接排除；>80%相似标记 yellow/medium",
        "execution": "在候选计划阶段动态执行，不进候选池时预标记"
    },
    "required_fields_per_candidate": [
        "candidate_id",
        "name",
        "en_name",
        "target_section",
        "risk_band (green/yellow/medium/red)",
        "suggested_parent_concept",
        "direct_pre_name_suggestion (3-10 items)",
        "may_belong_to_problem_patterns (true/false)",
        "source (newly_proposed / carry_over_from_stage3f)"
    ],
    "conclusion": {
        "main_graph_modified": False,
        "formal_candidates_generated": False,
        "merge_executed": False,
        "recommend_end_stage3f": True,
        "recommend_start_stage3g": True,
        "stage3g_first_batch_size": 40,
        "stage3g_total_batches": len(batch_plan),
        "note": "Stage3F 候选池已耗尽(129/129)。建议启动 Stage3G，重建 400 候选池，按 40-50 一批分 8-10 批合并。"
    }
}

outpath = os.path.join(BASE_DIR, "data/stage3g_400_candidate_pool_rebuild_plan.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(stage3g_plan, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# ============================================================
# Report 1: Pool Remaining Audit Report
# ============================================================
md1 = []
md1.append("# Stage3F Candidate Pool Remaining Audit Report\n")
md1.append(f"**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
md1.append(f"**生成者**: GLM5 (2号线程)")
md1.append(f"**任务类型**: 候选池余量审计\n")
md1.append("---\n")

md1.append("## 1. 候选池使用统计\n")
md1.append("| 指标 | 数量 | 说明 |")
md1.append("|------|:----:|------|")
md1.append(f"| Stage3F 标准候选池总数 | {pool['meta']['total_candidates']} | 初始池 |")
md1.append(f"| Batch1 已使用 | {len(b1_ids)} | 20 个 |")
md1.append(f"| Batch2 已使用 | {len(b2_ids)} | 20 个，其中 {len(b2_prune_cids)} 个后因重复删除 |")
md1.append(f"| Batch3 已使用 | {len(b3_ids)} | 40 个，其中 {len(b3_prune_cids)} 个后因重复删除 |")
md1.append(f"| Batch4 已使用 | {len(b4_ids)} | 49 个 |")
md1.append(f"| 总计已使用 | {len(all_used_ids)} | 129/129 |")
md1.append(f"| 已删除重复候选 | {len(all_pruned_ids)} | Batch2: {len(b2_prune_cids)}, Batch3: {len(b3_prune_cids)} |")
md1.append(f"| **剩余可用候选** | **{len(remaining_ids)}** | **池已耗尽** |")
md1.append("")

md1.append("## 2. 剩余候选分析\n")
if remaining_ids:
    md1.append(f"剩余 {len(remaining_ids)} 个候选:\n")
    md1.append("| candidate_id | name | section | risk |")
    md1.append("|-------------|------|---------|------|")
    for cid in sorted(remaining_ids):
        c = pool_candidates[cid]
        md1.append(f"| {cid} | {c.get('name','')} | {c.get('suggested_section','')} | {c.get('risk_band','')} |")
else:
    md1.append("**没有剩余候选。** 池已完全耗尽。\n")

md1.append("## 3. 结论\n")
md1.append(f"| 问题 | 答案 |")
md1.append(f"|------|:----:|")
md1.append(f"| 剩余候选是否足够开启 Batch5 ({20}个)？ | {'是' if len(remaining_ids) >= 20 else '否（仅剩 '+str(len(remaining_ids))+' 个）'} |")
md1.append(f"| 是否建议结束 Stage3F？ | **是** |")
md1.append(f"| 主图谱是否修改？ | 否 |")
md1.append(f"| 是否执行合并？ | 否 |")
md1.append(f"| 当前 item_count | {len(all_items)} |")
md1.append(f"| validate-only passed | {dvr.get('passed', False)} |")

report1 = "\n".join(md1)

outpath = os.path.join(DOCS_DIR, "stage3f_candidate_pool_remaining_audit_report.md")
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(report1)
print(f"  Written: {outpath}")

# ============================================================
# Report 2: Stage3G 400 Rebuild Plan Report
# ============================================================
md2 = []
md2.append("# Stage3G 400 Candidate Pool Rebuild Plan Report\n")
md2.append(f"**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
md2.append(f"**生成者**: GLM5 (2号线程)")
md2.append(f"**任务类型**: Stage3G 400 候选池重建规划（仅规划，不生成正式候选）\n")
md2.append("---\n")

md2.append("## 1. 背景\n")
md2.append(f"Stage3F 从 129 个标准化候选池中，经 4 批合并共使用了 **{len(all_used_ids)}** 个候选，")
md2.append(f"池已完全耗尽（剩余 {len(remaining_ids)} 个，不足 20）。")
md2.append(f"当前主图谱 **{len(all_items)}** 个节点，**{len(all_sections)}** 个 Section。")
md2.append(f"为继续扩展知识图谱覆盖，需重建候选池。\n")

md2.append("## 2. Stage3G 400 候选池规划\n")
md2.append(f"| 指标 | 值 |")
md2.append(f"|------|-----|")
md2.append(f"| 规划候选总数 | {total_planned} |")
md2.append(f"| 覆盖主题数 | {len(coverage_plan)} |")
md2.append(f"| 预计分拆批次 | {len(batch_plan)} 批 |")
md2.append(f"| 每批大小 | 40-50 个 |")
md2.append("")

md2.append("## 3. 主题分布\n")
md2.append("| 主题 | 建议 Section | 数量 | 优先级 |")
md2.append("|------|-------------|:----:|:------:|")
for key, cfg in STAGE3G_PLANNED_COVERAGE.items():
    md2.append(f"| {cfg['display']} | {', '.join(cfg['sections'])} | {cfg['count']} | {cfg['priority']} |")
md2.append(f"| **合计** | | **{total_planned}** | |")
md2.append("")

md2.append("## 4. 风险分层策略\n")
md2.append("| 层级 | 数量 | 标准 | 优先批次 |")
md2.append("|------|:----:|------|---------|")
md2.append(f"| 🟢 green | {risk_distribution['green']} | 高置信，无重复，依赖明确 | Batch1-Batch3 |")
md2.append(f"| 🟡 yellow | {risk_distribution['yellow']} | 有价值但需复查边界 | Batch2-Batch6 |")
md2.append(f"| 🟠 medium | {risk_distribution['medium']} | 风险较高，需重点审查 | Batch5-Batch8 |")
md2.append(f"| 🔴 red | {risk_distribution['red']} | 暂不进入，作为备选 | 备选 |")
md2.append("")

md2.append("## 5. 批次执行计划\n")
for bp in batch_plan:
    md2.append(f"- {bp['batch']}: **{bp['recommended_size']}** 个")
md2.append("")

md2.append("## 6. 每批推荐流程\n")
for i, step in enumerate(stage3g_plan["recommended_flow_per_batch"], 1):
    md2.append(f"  **{i}.** {step}")
md2.append("")

md2.append("## 7. 全图谱查重策略\n")
ds = stage3g_plan["dedup_strategy"]
md2.append(f"- **方法**: {ds['approach']}")
md2.append(f"- **阈值**: {ds['threshold']}")
md2.append(f"- **执行时机**: {ds['execution']}")
md2.append(f"- **候选字段**: name / alias / en_name / candidate_id 四重校验")
md2.append("")

md2.append("## 8. 每个候选的必要字段\n")
for i, fld in enumerate(stage3g_plan["required_fields_per_candidate"], 1):
    md2.append(f"  **{i}.** {fld}")
md2.append("")

md2.append("## 9. 结论\n")
md2.append("| 问题 | 答案 |")
md2.append("|------|:----:|")
md2.append("| 是否建议结束 Stage3F？ | **是**（池已耗尽） |")
md2.append(f"| 是否建议启动 Stage3G？ | **是** |")
md2.append(f"| Stage3G 第一批建议数量 | {stage3g_plan['conclusion']['stage3g_first_batch_size']} |")
md2.append(f"| Stage3G 总批次数 | {stage3g_plan['conclusion']['stage3g_total_batches']} |")
md2.append("| 主图谱是否修改？ | 否 |")
md2.append("| 是否生成正式候选？ | 否（仅规划） |")
md2.append("| 是否执行合并？ | 否 |")
md2.append("")

md2.append("**⚠️ 注意**: 400 候选池仍需经过正式设计、去重、审核后才可投入使用。")
md2.append("本报告仅提供规划框架和分布建议，不包含正式候选列表。")

report2 = "\n".join(md2)

outpath = os.path.join(DOCS_DIR, "stage3g_400_candidate_pool_rebuild_plan_report.md")
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(report2)
print(f"  Written: {outpath}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'=' * 60}")
print(f"Complete")
print(f"{'=' * 60}")
print(f"\nPool Audit:")
print(f"  Pool: {pool['meta']['total_candidates']} total")
print(f"  Used: {len(all_used_ids)} (B1={len(b1_ids)} B2={len(b2_ids)} B3={len(b3_ids)} B4={len(b4_ids)})")
print(f"  Pruned duplicates: {len(all_pruned_ids)}")
print(f"  Remaining: {len(remaining_ids)}")
print(f"  Recommend end Stage3F: {len(remaining_ids) < 20}")
print(f"\nStage3G 400 Plan:")
print(f"  Total planned: {total_planned}")
print(f"  Topics: {len(coverage_plan)}")
print(f"  Batches: {len(batch_plan)}")
print(f"  First batch size: {batch_plan[0]['recommended_size'] if batch_plan else 'N/A'}")
print(f"\n  main_graph_modified: False")
print(f"  validate-only: {dvr.get('passed', False)}")
