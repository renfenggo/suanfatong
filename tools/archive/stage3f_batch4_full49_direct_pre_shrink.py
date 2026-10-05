#!/usr/bin/env python3
"""
Stage3F Batch4 Full49 direct_pre Shrink Plan
为31个 dependency_fix_candidates 生成缩减方案，不修改主图谱
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

def find_items_in_section(all_items, sec_id):
    return [item for item in all_items.values()
            if item.get("parent") == sec_id or item["id"].startswith(sec_id + ".")]

def name_match_score(name, keywords):
    name_lower = name.lower()
    kws = [kw.lower() for kw in keywords]
    return sum(1 for kw in kws if kw in name_lower)

def best_item_match(all_items, section_id, keywords, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = set()
    best_score = -1
    best_items = []
    items = find_items_in_section(all_items, section_id)
    for item in items:
        if item["id"] in exclude_ids:
            continue
        score = name_match_score(item.get("name", ""), keywords)
        if score > best_score:
            best_score = score
            best_items = [item]
        elif score == best_score and score > 0:
            best_items.append(item)
    return best_items[:3]

print("=" * 60)
print("Stage3F Batch4 Full49 direct_pre Shrink Plan")
print("=" * 60)

# Load inputs
graph = load_json(os.path.join(BASE_DIR, "merged_knowledge_graph_item_dependencies_refined.json"))
fix_candidates = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_dependency_fix_candidates.json"))
mapping = load_json(os.path.join(BASE_DIR, "data/stage3f_batch4_full49_candidate_to_item_id_mapping.json"))

# Build comprehensive item lookup
all_items = {}
all_sections = {}
for cat in graph["categories"]:
    for sec in cat.get("sections", []):
        all_sections[sec["id"]] = sec.get("name", "")
        for item in sec.get("items", []):
            all_items[item["id"]] = item

print(f"  Total items: {len(all_items)}, sections: {len(all_sections)}")

# Build section -> items lookup
section_items = {}
for iid, item in all_items.items():
    sid = item.get("parent") or extract_section_id(iid)
    section_items.setdefault(sid, []).append(item)

# Build set of new batch4 item IDs
new_item_ids = set(m["item_id"] for m in mapping["mappings"])

# ============================================================
# Knowledge base: for each problem item, define rules to find
# core direct_pre from the existing graph items
# ============================================================

# Domain-specific rules: item_id_pattern -> (source_sections_to_search, keywords_to_find, max_items, manual_review)
SHRINK_RULES = {
    # === 2.21 图论 ===
    "2.21.152": {  # 最大权闭合子图：Penalty Modeling
        "reason": "闭合子图建模变体，依赖最大流基础、闭合子图概念、图建模基础",
        "sources": {
            "2.16": ["最大流", "流", "dinic", "ek", "ford fulkerson", "增广"],
            "2.21": ["闭合子图", "最大权闭合子图", "最大权闭合"],
            "2.9": ["图建模", "建模基础", "图的 DFS", "图论基础"],
        },
        "max": 6,
        "manual": False
    },
    "2.21.153": {  # 动态图连通性：Connectivity Snapshots
        "reason": "动态连通性快照，依赖并查集、动态连通性概念、线段树分治、图遍历",
        "sources": {
            "3.1": ["并查集", "查并", "disjoint", "DSU", "union find"],
            "2.21": ["动态连通", "连通性", "连通分量"],
            "3.3": ["线段树", "segment tree", "树"],
            "2.9": ["图", "DFS", "BFS", "遍历"],
        },
        "max": 6,
        "manual": False
    },
    "2.21.154": {  # 动态图连通性：Dynamic Biconnectivity
        "reason": "动态双连通性，依赖边双连通、点双连通、并查集",
        "sources": {
            "2.12": ["双连通", "边双", "点双", "桥", "割点", "tarjan"],
            "3.1": ["并查集", "DSU", "union find"],
            "2.21": ["动态连通", "动态图连通"],
            "2.9": ["图", "DFS", "遍历"],
        },
        "max": 6,
        "manual": False
    },
    "2.21.155": {  # 动态图连通性：Dynamic Bridge
        "reason": "动态桥，依赖桥/割边概念、并查集、连通性",
        "sources": {
            "2.12": ["桥", "割边", "边双", "双连通", "tarjan"],
            "3.1": ["并查集", "DSU"],
            "2.21": ["动态连通", "连通性"],
            "2.9": ["图", "DFS"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.156": {  # 全局最小割：Minimum Cut Modeling
        "reason": "最小割建模，依赖最大流、最小割概念、图建模",
        "sources": {
            "2.16": ["最小割", "最大流", "割", "流", "dinic"],
            "2.21": ["最小割", "割"],
            "2.9": ["图建模", "建模基础"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.157": {  # 强连通分量 DAG：Component Topo Order
        "reason": "SCC拓扑序，依赖强连通分量、缩点、拓扑排序、DAG",
        "sources": {
            "2.12": ["强连通", "SCC", "缩点", "tarjan"],
            "2.11": ["拓扑", "topo", "排序"],
            "2.8": ["DAG", "DAG DP", "dp on dag"],
            "2.9": ["图", "DFS"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.158": {  # 强连通分量 DAG：Scc Dp
        "reason": "DAG上的SCC DP，依赖SCC、缩点、DAG DP",
        "sources": {
            "2.12": ["强连通", "SCC", "缩点", "tarjan"],
            "2.11": ["拓扑", "topo"],
            "2.8": ["DAG", "DP", "动态规划"],
            "2.21.157": [],  # direct reference to sibling
        },
        "max": 5,
        "manual": False
    },
    "2.21.159": {  # 差分约束系统建模
        "reason": "差分约束建模，依赖最短路、三角不等式、图建模",
        "sources": {
            "2.15": ["最短路", "spfa", "bellman", "dijkstra", "shortest"],
            "2.9": ["图建模", "建模基础"],
            "2.21": ["差分约束"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.160": {  # 动态图连通性：Fully Dynamic Overview
        "reason": "全动态连通性概览，依赖并查集、线段树分治、连通性概念",
        "sources": {
            "3.1": ["并查集", "DSU"],
            "3.3": ["线段树", "segment tree", "树"],
            "2.21": ["动态连通", "连通性"],
            "2.9": ["图", "DFS"],
        },
        "max": 6,
        "manual": False
    },
    "2.21.161": {  # Hall 定理及应用
        "reason": "Hall定理及应用，依赖二分图匹配、图论基础",
        "sources": {
            "2.17": ["二分图", "匹配", "匈牙利", "bipartite", "hall"],
            "4.5": ["二分图", "匹配", "定理"],
            "2.9": ["图", "DFS", "图论"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.162": {  # 最大权闭合子图
        "reason": "最大权闭合子图核心概念，依赖最大流、闭合子图",
        "sources": {
            "2.16": ["最大流", "流", "dinic"],
            "2.21": ["闭合子图", "最大权闭合"],
            "2.9": ["图建模"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.163": {  # 平面图：Embedding Basics
        "reason": "平面图嵌入基础，依赖图论基础、平面图概念",
        "sources": {
            "4.5": ["平面图", "图", "点边"],
            "2.9": ["图", "DFS", "图论"],
            "2.21": ["平面图"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.164": {  # 高级最短路：Eppstein K Shortest
        "reason": "Eppstein K短路，依赖最短路、堆、图遍历",
        "sources": {
            "2.15": ["最短路", "dijkstra", "shortest", "spfa"],
            "2.21": ["最短路", "shortest", "K short"],
            "3.2": ["堆", "priority", "heap"],
            "2.9": ["图", "DFS"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.165": {  # 高级最短路：Johnson Potentials
        "reason": "Johnson势能算法，依赖最短路、势能、图建模",
        "sources": {
            "2.15": ["最短路", "dijkstra", "bellman", "spfa", "johnson"],
            "2.21": ["最短路"],
            "2.9": ["图", "图论"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.166": {  # 高级最短路：Min Cost Path Cover
        "reason": "最小费用路径覆盖，依赖最小费用流、最短路、图论",
        "sources": {
            "2.16": ["费用流", "最小费用", "最大流"],
            "2.15": ["最短路", "shortest"],
            "2.21": ["最短路", "路径覆盖"],
            "2.9": ["图建模"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.167": {  # 高级最短路：Replacement Paths
        "reason": "替换路径，依赖最短路、次短路、图遍历",
        "sources": {
            "2.15": ["最短路", "dijkstra", "shortest"],
            "2.21": ["最短路", "K short"],
            "2.9": ["图", "DFS"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.168": {  # 高级最短路：Resource Constrained
        "reason": "资源约束最短路，依赖最短路、DP、状态图",
        "sources": {
            "2.15": ["最短路", "dijkstra", "shortest"],
            "2.8": ["DP", "状态", "动态规划"],
            "2.21": ["最短路"],
            "2.9": ["图"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.169": {  # 高级最短路：Yen K Shortest
        "reason": "Yen K短路算法，依赖最短路、堆、次短路",
        "sources": {
            "2.15": ["最短路", "dijkstra", "shortest"],
            "3.2": ["堆", "priority", "heap"],
            "2.21": ["最短路", "K short"],
            "2.9": ["图"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.170": {  # 高级最短路：Zero One Bfs Modeling
        "reason": "01BFS建模，依赖最短路、BFS、01权重图建模",
        "sources": {
            "2.15": ["最短路", "bfs", "shortest", "dijkstra"],
            "2.9": ["BFS", "图建模", "建模"],
            "2.21": ["最短路"],
        },
        "max": 5,
        "manual": False
    },
    "2.21.171": {  # 2-SAT 建模技巧
        "reason": "2-SAT建模，依赖2-SAT、强连通分量、布尔逻辑建模",
        "sources": {
            "2.21": ["2-SAT", "SAT", "sat"],
            "2.12": ["强连通", "SCC", "缩点", "tarjan"],
            "2.9": ["图建模", "建模基础"],
        },
        "max": 5,
        "manual": False
    },
    # === 2.8 DP ===
    "2.8.151": {  # 博弈DP基础
        "reason": "博弈DP基础，依赖DP思想、状态设计、博弈论基础",
        "sources": {
            "2.8": ["DP 思想", "状态设计", "转移", "DP", "动态规划", "博弈", "game"],
            "2.1": ["递推", "递归", "分治"],
        },
        "max": 6,
        "manual": False
    },
    "2.8.152": {  # Grundy数DP
        "reason": "Grundy数DP，依赖博弈DP、SG函数、Nim博弈",
        "sources": {
            "2.8": ["博弈", "game", "DP", "Grundy", "sg"],
            "2.8.151": [],  # direct sibling
        },
        "max": 5,
        "manual": False
    },
    "2.8.153": {  # 矩阵DP基础
        "reason": "矩阵DP基础，依赖DP思想、矩阵运算、线性代数",
        "sources": {
            "2.8": ["DP 思想", "状态设计", "转移", "DP"],
            "4.6": ["矩阵", "matrix", "乘法", "线性代数"],
            "2.1": ["递推"],
        },
        "max": 5,
        "manual": False
    },
    "2.8.154": {  # 矩阵快速幂DP
        "reason": "矩阵快速幂DP，依赖矩阵DP、快速幂、线性递推",
        "sources": {
            "2.8": ["DP", "矩阵", "矩阵DP"],
            "2.12": ["矩阵", "快速幂", "幂", "矩阵快速幂"],
            "2.1": ["快速幂", "快速", "幂"],
            "2.8.153": [],
        },
        "max": 5,
        "manual": False
    },
    "2.8.155": {  # 期望DP
        "reason": "期望DP，依赖DP思想、概率论、期望概念",
        "sources": {
            "2.8": ["DP 思想", "状态设计", "DP", "期望"],
            "4.2": ["概率", "期望", "期望值", "分布", "随机"],
            "2.1": ["递推"],
        },
        "max": 5,
        "manual": False
    },
    "2.8.156": {  # 马尔可夫链DP
        "reason": "马尔可夫链DP，依赖期望DP、概率转移、状态图",
        "sources": {
            "2.8": ["DP", "期望", "概率"],
            "4.2": ["概率", "马尔可夫", "markov", "转移"],
            "2.8.155": [],
        },
        "max": 5,
        "manual": False
    },
    # === 2.10 字符串 ===
    "2.10.39": {  # Sunday算法
        "reason": "Sunday字符串匹配，依赖朴素匹配、KMP、字符串基础",
        "sources": {
            "2.10": ["朴素匹配", "KMP", "字符串匹配", "匹配", "string", "哈希"],
            "1.6": ["string", "字符串", "数组"],
        },
        "max": 5,
        "manual": True
    },
    "2.10.40": {  # Duval算法最小表示
        "reason": "Duval算法（最小表示），依赖字符串匹配、最小表示概念",
        "sources": {
            "2.10": ["KMP", "字符串匹配", "匹配", "string", "最小表示"],
            "1.6": ["string", "字符串"],
        },
        "max": 5,
        "manual": False
    },
    "2.10.41": {  # 二维滚动哈希
        "reason": "二维滚动哈希，依赖字符串哈希、滚动哈希、矩阵",
        "sources": {
            "2.10": ["哈希", "字符串哈希", "滚动哈希", "hash"],
            "4.6": ["矩阵", "matrix"],
            "1.6": ["数组", "array"],
        },
        "max": 5,
        "manual": False
    },
    "2.10.42": {  # 哈希碰撞处理策略
        "reason": "哈希碰撞处理，依赖哈希基础、哈希表、冲突解决",
        "sources": {
            "2.10": ["哈希", "字符串哈希", "hash"],
            "3.8": ["哈希", "哈希表", "hash", "冲突", "碰撞"],
            "1.6": ["数组"],
        },
        "max": 4,
        "manual": False
    },
    # === 4.4 离散数学 ===
    "4.4.15": {  # 线性递推基础
        "reason": "线性递推基础，依赖递推、数列、线性代数",
        "sources": {
            "4.4": ["递推", "recurrence", "数列", "序列"],
            "4.1": ["整数", "自然数", "数"],
            "2.1": ["递推"],
            "2.12": ["矩阵", "快速幂", "线性"],
        },
        "max": 5,
        "manual": True
    },
    "4.4.16": {  # Kitamasa算法
        "reason": "Kitamasa算法，依赖线性递推、矩阵快速幂、多项式",
        "sources": {
            "4.4": ["递推", "recurrence"],
            "2.12": ["矩阵", "快速幂", "幂", "矩阵快速幂"],
            "4.4.15": [],
        },
        "max": 5,
        "manual": True
    },
    # === 4.5 图与树的数学基础 ===
    "4.5.17": {  # GF(2)上的高斯消元
        "reason": "GF(2)高斯消元，依赖线性代数、高斯消元、域论基础",
        "sources": {
            "2.17": ["高斯消元", "消元", "线性代数", "异或"],
            "4.5": ["图", "树", "点边"],
        },
        "max": 5,
        "manual": False
    },
    "4.5.18": {  # 矩阵树定理
        "reason": "矩阵树定理，依赖矩阵、树、行列式、图论",
        "sources": {
            "2.17": ["行列式", "矩阵", "线性"],
            "2.12": ["矩阵", "乘法", "逆"],
            "4.5": ["树", "生成树", "图", "点边"],
            "4.5.17": [],
        },
        "max": 5,
        "manual": False
    },
}

# ============================================================
# Generate shrink plan for each candidate
# ============================================================
print("\n[Analysis] Generating shrink plan...")

shrink_plan = []
manual_review_count = 0
total_old = 0
total_new = 0

for fc in fix_candidates["candidates"]:
    item_id = fc["id"]
    item = all_items.get(item_id, {})
    name = fc["name"]
    section = fc.get("section", extract_section_id(item_id))
    old_dp = item.get("direct_pre", [])
    old_count = len(old_dp)
    total_old += old_count

    rules = SHRINK_RULES.get(item_id, None)

    if rules is None:
        # No specific rule - mark as manual review
        new_dp = []
        confidence = "low"
        manual = True
        reason = "未定义缩减规则"
        shrink_plan.append({
            "item_id": item_id, "name": name, "section": section,
            "old_direct_pre_count": old_count,
            "old_direct_pre_sample": old_dp[:5],
            "new_direct_pre": [],
            "new_direct_pre_count": 0,
            "removed_count": old_count,
            "mapping_confidence": "low",
            "manual_review_required": True,
            "reason": f"无预定义缩减规则，请人工确定 {name} 的核心前置"
        })
        manual_review_count += 1
        continue

    # Find best matching items for each source section
    new_dp = []
    used_ids = set()

    for src_sec, keywords in rules["sources"].items():
        # Item ID reference (e.g. "2.21.157" with 2+ dots)
        if src_sec.count(".") >= 2:
            if src_sec in all_items and src_sec not in used_ids:
                new_dp.append(src_sec)
                used_ids.add(src_sec)
            continue

        if not keywords:
            continue

        # Section ID with keywords (e.g. "2.16")

        # Find top matching items from this section that are NOT batch4 items
        sec_items = section_items.get(src_sec, [])
        scored = []
        for si in sec_items:
            # Skip batch4 new items
            if si["id"] in new_item_ids:
                continue
            score = name_match_score(si.get("name", ""), keywords)
            if score > 0:
                scored.append((score, si["id"], si.get("name", "")))

        scored.sort(key=lambda x: -x[0])
        # Pick top 1-2 per source section
        max_per_section = 2
        for score, sid, sname in scored:
            if len([x for x in new_dp if x.startswith(src_sec)]) >= max_per_section:
                break
            if sid not in used_ids:
                new_dp.append(sid)
                used_ids.add(sid)

    # Limit to max specified in rules
    max_items = rules.get("max", 6)
    if len(new_dp) > max_items:
        new_dp = new_dp[:max_items]

    confidence = "high"
    manual = rules.get("manual", False)
    reason = rules.get("reason", "")

    if len(new_dp) == 0:
        manual = True
        confidence = "low"
        reason = "未能自动匹配到核心前置"
    elif len(new_dp) <= 2:
        confidence = "medium"
        reason = reason + f"，仅匹配到 {len(new_dp)} 个前置"
    else:
        reason = reason + f"，匹配到 {len(new_dp)} 个核心前置"

    if manual:
        manual_review_count += 1

    new_count = len(new_dp)
    total_new += new_count
    removed = old_count - new_count

    entry = {
        "item_id": item_id,
        "name": name,
        "section": section,
        "old_direct_pre_count": old_count,
        "old_direct_pre_sample": old_dp[:5],
        "new_direct_pre": new_dp,
        "new_direct_pre_count": new_count,
        "removed_count": removed,
        "mapping_confidence": confidence,
        "manual_review_required": manual,
        "reason": reason
    }
    shrink_plan.append(entry)

print(f"  Plans generated: {len(shrink_plan)}")
print(f"  Manual review required: {manual_review_count}")

# ============================================================
# Build outputs
# ============================================================
print("\n[Output] Writing files...")

# 1. shrink_plan.json
shrink_plan_json = {
    "batch_id": "stage3f_batch4_full49",
    "meta": {
        "title": "Stage3F Batch4 Full49 direct_pre Shrink Plan",
        "generated_by": "GLM5",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "main_graph_modified": False,
        "total_candidates": len(shrink_plan)
    },
    "summary": {
        "total_to_shrink": len(shrink_plan),
        "total_old_direct_pre": total_old,
        "total_new_direct_pre": total_new,
        "total_removed": total_old - total_new,
        "average_old": round(total_old / max(len(shrink_plan), 1), 1),
        "average_new": round(total_new / max(len(shrink_plan), 1), 1),
        "manual_review_required": manual_review_count,
        "by_section": dict(Counter(e["section"] for e in shrink_plan)),
        "section_old_stats": {},
        "all_safe_to_shrink": manual_review_count == 0
    },
    "items": shrink_plan
}

# Add per-section stats
for sec_id in sorted(set(e["section"] for e in shrink_plan)):
    sec_items = [e for e in shrink_plan if e["section"] == sec_id]
    sec_old = sum(e["old_direct_pre_count"] for e in sec_items)
    sec_new = sum(e["new_direct_pre_count"] for e in sec_items)
    shrink_plan_json["summary"]["section_old_stats"][sec_id] = {
        "count": len(sec_items),
        "old_total": sec_old,
        "new_total": sec_new,
        "removed": sec_old - sec_new,
        "avg_old": round(sec_old / len(sec_items), 1),
        "avg_new": round(sec_new / len(sec_items), 1)
    }

outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_direct_pre_shrink_plan.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(shrink_plan_json, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# 2. patch_preview.json
patches = []
for entry in shrink_plan:
    if entry["new_direct_pre"]:
        patches.append({
            "item_id": entry["item_id"],
            "name": entry["name"],
            "field": "direct_pre",
            "old": entry["old_direct_pre_sample"] + [f"...({entry['old_direct_pre_count']} total)"],
            "new": entry["new_direct_pre"],
            "patch_action": f"将 direct_pre 从 {entry['old_direct_pre_count']} 个缩减至 {entry['new_direct_pre_count']} 个",
            "manual_review_required": entry["manual_review_required"],
            "confidence": entry["mapping_confidence"]
        })

patch_preview = {
    "batch_id": "stage3f_batch4_full49",
    "description": "direct_pre 缩减补丁预览。未应用。1号线程可在 Fix Lite 阶段决定是否执行。",
    "main_graph_modified": False,
    "total_patches": len(patches),
    "patches": patches
}
outpath = os.path.join(BASE_DIR, "data/stage3f_batch4_full49_direct_pre_shrink_patch_preview.json")
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(patch_preview, f, ensure_ascii=False, indent=2)
print(f"  Written: {outpath}")

# ============================================================
# Report
# ============================================================
md = []
md.append("# Stage3F Batch4 Full49 direct_pre Shrink Report\n")
md.append(f"**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
md.append(f"**生成者**: GLM5 (2号线程)")
md.append(f"**任务类型**: direct_pre 缩减方案（仅方案，不修改主图谱）\n")
md.append("---\n")

md.append("## 1. 缩减概览\n")
md.append(f"| 指标 | 值 |")
md.append(f"|------|-----|")
md.append(f"| 需缩减节点总数 | {len(shrink_plan)} |")
md.append(f"| 缩减前 direct_pre 总数 | {total_old} |")
md.append(f"| 缩减后 direct_pre 总数 | {total_new} |")
md.append(f"| 总计移除 | {total_old - total_new} |")
md.append(f"| 平均 direct_pre（缩减前） | {round(total_old/max(len(shrink_plan),1),1)} |")
md.append(f"| 平均 direct_pre（缩减后） | {round(total_new/max(len(shrink_plan),1),1)} |")
md.append(f"| manual_review_required | {manual_review_count} |")
md.append(f"| 主图谱是否修改 | **否** |")
md.append("")

md.append("## 2. 按 Section 缩减统计\n")
md.append("| Section | 名称 | 节点数 | 原总数 | 缩减后 | 移除 | avg原→新 |")
md.append("|---------|------|:-----:|:------:|:------:|:----:|:--------:|")
for sec_id in sorted(set(e["section"] for e in shrink_plan)):
    sec_name = all_sections.get(sec_id, "")
    stats = shrink_plan_json["summary"]["section_old_stats"][sec_id]
    md.append(f"| {sec_id} | {sec_name} | {stats['count']} | {stats['old_total']} | {stats['new_total']} | {stats['removed']} | {stats['avg_old']}→{stats['avg_new']} |")
md.append("")

md.append("## 3. 各节点缩减明细\n")
md.append("| # | item_id | name | section | 缩减前 | 缩减后 | 移除 | 置信度 | manual |")
md.append("|---|--------|------|---------|:------:|:------:|:----:|:------:|:------:|")
for i, entry in enumerate(shrink_plan, 1):
    manual_str = "⚠️" if entry["manual_review_required"] else "-"
    md.append(f"| {i} | {entry['item_id']} | {entry['name']} | {entry['section']} | {entry['old_direct_pre_count']} | {entry['new_direct_pre_count']} | {entry['removed_count']} | {entry['mapping_confidence']} | {manual_str} |")
md.append("")

md.append("## 4. 缩减方案说明\n")
for entry in shrink_plan:
    if entry["new_direct_pre"]:
        dp_names = []
        for ref in entry["new_direct_pre"]:
            other = all_items.get(ref, {})
            dp_names.append(f"{ref}:{other.get('name','?')}")
        dp_str = "; ".join(dp_names)
    else:
        dp_str = "（无自动匹配）"
    tag = "⚠️ MANUAL" if entry["manual_review_required"] else "✅"
    md.append(f"### {tag} {entry['item_id']} {entry['name']}\n")
    md.append(f"- **理由**: {entry['reason']}")
    md.append(f"- **缩减**: {entry['old_direct_pre_count']} → {entry['new_direct_pre_count']}（移除 {entry['removed_count']}）")
    md.append(f"- **新 direct_pre**: {dp_str}")
    if entry["manual_review_required"]:
        md.append(f"- **需人工确认**: 建议合并时由 1 号线程检查并确认")
    md.append("")

md.append("## 5. 无法安全缩减的节点\n")
unsafe = [e for e in shrink_plan if e["manual_review_required"] and e["new_direct_pre_count"] == 0]
if unsafe:
    md.append("以下节点未能自动匹配到核心前置：\n")
    for e in unsafe:
        md.append(f"- {e['item_id']} {e['name']}: {e['reason']}")
else:
    md.append("所有节点均可自动生成缩减方案，部分需人工复核。\n")

md.append("## 6. 结论与建议\n")
md.append(f"| 建议项 | 值 |")
md.append(f"|-------|-----|")
md.append(f"| 是否建议交给 1号执行 direct_pre 缩减修复 | **是** |")
md.append(f"| 需人工复核节点数 | {manual_review_count} |")
md.append(f"| 主图谱是否修改 | 否 |")
md.append(f"| 补丁是否已应用 | 否 |")
md.append("")
md.append(f"**核心结论**: 31 个 dependency_fix_candidates 的 direct_pre 缩减方案已生成。")
md.append(f"建议 1号线程在 Fix Lite 阶段根据 patch_preview 执行缩减，")
md.append(f"将每个节点的 direct_pre 从 {round(total_old/max(len(shrink_plan),1),1)} 个缩减至 {round(total_new/max(len(shrink_plan),1),1)} 个。")
md.append(f"其中 {manual_review_count} 个节点标注了 manual_review_required，需人工确认后再执行。")

report_md = "\n".join(md)
report_path = os.path.join(DOCS_DIR, "stage3f_batch4_full49_direct_pre_shrink_report.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_md)
print(f"  Written: {report_path}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'=' * 60}")
print(f"Stage3F Batch4 Full49 direct_pre Shrink Complete")
print(f"{'=' * 60}")
print(f"\nSummary:")
print(f"  Nodes to shrink: {len(shrink_plan)}")
print(f"  Old total: {total_old}, New total: {total_new}, Removed: {total_old - total_new}")
print(f"  Average: {round(total_old/max(len(shrink_plan),1),1)} -> {round(total_new/max(len(shrink_plan),1),1)}")
print(f"  Manual review: {manual_review_count}")
print(f"  main_graph_modified: False")
print(f"\n  Per section:")
for sec_id in sorted(set(e["section"] for e in shrink_plan)):
    stats = shrink_plan_json["summary"]["section_old_stats"][sec_id]
    print(f"    {sec_id}: {stats['count']} nodes, {stats['old_total']} -> {stats['new_total']}")
