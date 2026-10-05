#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习路径分层审计脚本（含前端可用性复核）
只读审计，不修改任何主数据文件。

基于 3240 个知识点的多维度信号，将其分为四个学习层级：
  1. core      - 核心主线
  2. standard  - 常用进阶
  3. advanced  - 专题扩展
  4. optional  - 冷门/可折叠

区分两个概念：
  - graph_layer：根据图谱字段计算出的层级
  - frontend_display_layer：真正建议前端展示用的层级

分层信号：
  - visibility 字段（已有）
  - level 字段
  - content_status.content_priority
  - learning_path_policy.unlock_mode
  - tracks / audience
  - 依赖深度（resolved_pre 长度）
  - 章节容量
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import date

# ── 路径 ──
ROOT = Path(__file__).resolve().parent.parent
MAIN_GRAPH = ROOT / "merged_knowledge_graph_item_dependencies_refined.json"
OUTPUT_JSON = ROOT / "data" / "learning_path_layers_audit.json"
OUTPUT_MD = ROOT / "docs" / "learning_path_layers_audit_report.md"

# ── 重点章节 ──
FOCUS_SECTIONS = {
    "2.8": "动态规划",
    "3.13": "高级数据结构扩展",
    "4.1": "整数与数论基础",
    "2.9": "图基础与遍历",
    "2.7": "搜索",
    "2.10": "字符串算法",
}

# ── 分层规则 ──
# visibility 映射
VIS_MAP = {
    "core": "core",
    "advanced": "advanced",
    "expert": "advanced",
    "optional": "optional",
}

# level 权重
LEVEL_WEIGHT = {
    "L1": 1, "low": 1,
    "L2": 2, "medium": 2,
    "L3": 3, "high": 3,
    "L4": 4, "advanced": 4,
    "L5": 5,
    "": 2,  # 默认中等
}

# content_priority 权重
PRIORITY_WEIGHT = {
    "P0": 0,   # 最高优先级 -> 偏核心
    "P1": 1,
    "P2": 2,
    "P3": 3,   # 最低优先级 -> 偏冷门
    "draft": 3,
    "needs_content": 3,
    "pending": 2,
    "": 2,
}

# unlock_mode 映射
UNLOCK_MAP = {
    "mainline": "core",
    "optional": "optional",
    "optional_branch": "optional",
    "expert_branch": "advanced",
    "reference_only": "optional",
}


def load_graph():
    with open(MAIN_GRAPH, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_dep_depth(item, all_items_map):
    """计算依赖深度（resolved_pre 链的最大深度）"""
    visited = set()
    def dfs(node_id):
        if node_id in visited:
            return 0
        visited.add(node_id)
        if node_id not in all_items_map:
            return 0
        node = all_items_map[node_id]
        pres = node.get("resolved_pre", [])
        if not pres:
            return 0
        return 1 + max(dfs(p) for p in pres)
    return dfs(item["id"])


def classify_item(item, all_items_map, section_item_count):
    """
    综合多维度信号对节点分层。
    返回 (layer, signals) 其中 signals 是各信号的原始值和映射值。
    """
    vis = item.get("visibility", "")
    level = item.get("level", "")
    cs = item.get("content_status", {})
    if isinstance(cs, dict):
        priority = cs.get("content_priority", "")
    else:
        priority = ""
    lp = item.get("learning_path_policy", {})
    if isinstance(lp, dict):
        unlock = lp.get("unlock_mode", "")
    else:
        unlock = ""
    tracks = item.get("tracks", [])
    audience = item.get("audience", [])
    resolved_pre = item.get("resolved_pre", [])

    # 信号收集
    signals = {
        "visibility": vis,
        "visibility_mapped": VIS_MAP.get(vis, "standard"),
        "level": level,
        "level_weight": LEVEL_WEIGHT.get(level, 2),
        "content_priority": priority,
        "priority_weight": PRIORITY_WEIGHT.get(priority, 2),
        "unlock_mode": unlock,
        "unlock_mapped": UNLOCK_MAP.get(unlock, "standard"),
        "has_beginner_track": "beginner" in tracks or "csp_j" in tracks,
        "has_advanced_track": any(t.startswith("advanced_") for t in tracks),
        "has_icpc_noi_track": "icpc" in tracks or "noi" in tracks or "ioi" in tracks,
        "dep_count": len(resolved_pre),
        "section_size": section_item_count,
    }

    # ── 分层评分 ──
    # 策略：以 visibility 为主框架，level 为核心细分信号
    # visibility=core(1439) -> core(L1/L2) / standard(L3+)
    # visibility=advanced(1388) -> standard(L1/L2) / advanced(L3+)
    # visibility=expert(411) -> advanced(L1-L3) / optional(L4+)
    # visibility=optional(2) -> optional
    score = 0

    # 1. visibility 基线分
    vis_base = {"core": 0, "advanced": 10, "expert": 20, "optional": 30, "": 10}
    score += vis_base.get(vis, 10)

    # 2. level 信号（核心细分信号，权重加大）
    lw = LEVEL_WEIGHT.get(level, 2)
    if lw <= 1:
        score -= 4
    elif lw == 2:
        score -= 2
    elif lw == 3:
        score += 3
    elif lw >= 4:
        score += 5

    # 3. content_priority 微调
    pw = PRIORITY_WEIGHT.get(priority, 2)
    if pw <= 0:
        score -= 1
    elif pw >= 3:
        score += 1

    # 4. unlock_mode 微调
    if unlock == "mainline":
        score -= 1
    elif unlock in ("optional", "optional_branch", "reference_only"):
        score += 1
    elif unlock == "expert_branch":
        score += 1

    # 5. tracks 微调
    if signals["has_beginner_track"]:
        score -= 1
    if signals["has_advanced_track"]:
        score += 1

    # ── 分层映射 ──
    # visibility=core 基线 0:
    #   L1: 0-4-1-1= -6 ~ -4 -> core
    #   L2: 0-2-1-1= -4 ~ -2 -> core
    #   L3: 0+3-1-1= 1 ~ 3 -> standard
    #   L4+: 0+5-1-1= 3 ~ 5 -> standard
    # visibility=advanced 基线 10:
    #   L1: 10-4+1+1= 6 ~ 8 -> standard
    #   L2: 10-2+1+1= 8 ~ 10 -> standard
    #   L3: 10+3+1+1= 13 ~ 15 -> advanced
    #   L4+: 10+5+1+1= 15 ~ 17 -> advanced
    # visibility=expert 基线 20:
    #   L1: 20-4+1+1= 16 ~ 18 -> advanced
    #   L2: 20-2+1+1= 18 ~ 20 -> advanced
    #   L3: 20+3+1+1= 23 ~ 25 -> optional
    #   L4+: 20+5+1+1= 25 ~ 27 -> optional
    if score <= 0:
        layer = "core"
    elif score <= 12:
        layer = "standard"
    elif score <= 22:
        layer = "advanced"
    else:
        layer = "optional"

    # 覆盖规则：visibility=optional 强制 optional
    if vis == "optional":
        layer = "optional"

    signals["score"] = score
    signals["layer"] = layer

    return layer, signals


def analyze_graph(data):
    """主分析函数"""
    # 构建索引
    all_items = []
    all_items_map = {}
    section_items = defaultdict(list)
    section_info = {}

    for cat in data["categories"]:
        for sec in cat["sections"]:
            section_info[sec["id"]] = {
                "id": sec["id"],
                "name": sec["name"],
                "category": cat["name"],
                "level": sec.get("level", ""),
            }
            for it in sec["items"]:
                all_items.append(it)
                all_items_map[it["id"]] = it
                section_items[sec["id"]].append(it)

    # 计算章节容量
    section_sizes = {sid: len(items) for sid, items in section_items.items()}

    # 分层
    item_layers = {}
    item_signals = {}
    for it in all_items:
        sec_id = it.get("parent", "")
        sec_size = section_sizes.get(sec_id, 0)
        layer, signals = classify_item(it, all_items_map, sec_size)
        item_layers[it["id"]] = layer
        item_signals[it["id"]] = signals

    # ── 统计 ──
    # 1. 每个大类的分层统计
    category_layer_stats = defaultdict(lambda: defaultdict(int))
    for cat in data["categories"]:
        for sec in cat["sections"]:
            for it in sec["items"]:
                layer = item_layers[it["id"]]
                category_layer_stats[cat["name"]][layer] += 1

    # 2. 每个章节的分层统计
    section_layer_stats = {}
    for sid, items in section_items.items():
        layer_counts = defaultdict(int)
        for it in items:
            layer = item_layers[it["id"]]
            layer_counts[layer] += 1
        info = section_info.get(sid, {})
        section_layer_stats[sid] = {
            "name": info.get("name", ""),
            "category": info.get("category", ""),
            "total": len(items),
            "core": layer_counts.get("core", 0),
            "standard": layer_counts.get("standard", 0),
            "advanced": layer_counts.get("advanced", 0),
            "optional": layer_counts.get("optional", 0),
        }

    # 3. 核心主线候选列表
    core_candidates = []
    for it in all_items:
        if item_layers[it["id"]] == "core":
            core_candidates.append({
                "id": it["id"],
                "name": it["name"],
                "parent": it.get("parent", ""),
                "visibility": it.get("visibility", ""),
                "level": it.get("level", ""),
            })

    # 4. 可折叠/冷门候选列表
    optional_candidates = []
    for it in all_items:
        if item_layers[it["id"]] == "optional":
            optional_candidates.append({
                "id": it["id"],
                "name": it["name"],
                "parent": it.get("parent", ""),
                "visibility": it.get("visibility", ""),
                "level": it.get("level", ""),
                "unlock_mode": (it.get("learning_path_policy", {})
                                if isinstance(it.get("learning_path_policy"), dict)
                                else {}).get("unlock_mode", ""),
            })

    # 5. 高拥挤章节分析
    # 阈值：章节 item 数 >= 60 为高拥挤
    OVERCROWD_THRESHOLD = 60
    overcrowded_sections = []
    for sid, stats in sorted(section_layer_stats.items(),
                              key=lambda x: x[1]["total"], reverse=True):
        if stats["total"] >= OVERCROWD_THRESHOLD:
            optional_ratio = stats["optional"] / stats["total"] if stats["total"] > 0 else 0
            advanced_ratio = stats["advanced"] / stats["total"] if stats["total"] > 0 else 0
            foldable_ratio = (stats["optional"] + stats["advanced"]) / stats["total"] if stats["total"] > 0 else 0
            overcrowded_sections.append({
                "section_id": sid,
                "section_name": stats["name"],
                "category": stats["category"],
                "total": stats["total"],
                "core": stats["core"],
                "standard": stats["standard"],
                "advanced": stats["advanced"],
                "optional": stats["optional"],
                "foldable_ratio": round(foldable_ratio, 3),
                "recommend_default_fold": foldable_ratio > 0.4,
            })

    # 6. 学习路径推荐
    # 入门路径：core + beginner track 的章节
    # 提高路径：core + standard 的章节
    # 冲刺路径：advanced + icpc/noi track 的章节
    path_recommendations = {
        "beginner_path": [],
        "improvement_path": [],
        "sprint_path": [],
    }

    for sid, stats in section_layer_stats.items():
        core_ratio = (stats["core"] + stats["standard"]) / stats["total"] if stats["total"] > 0 else 0
        advanced_ratio = (stats["advanced"] + stats["optional"]) / stats["total"] if stats["total"] > 0 else 0

        # 检查该章节是否有 beginner track 的 item
        has_beginner = any(
            "beginner" in it.get("tracks", []) or "csp_j" in it.get("tracks", [])
            for it in section_items.get(sid, [])
        )
        has_advanced_track = any(
            any(t.startswith("advanced_") for t in it.get("tracks", []))
            for it in section_items.get(sid, [])
        )

        entry = {
            "section_id": sid,
            "section_name": stats["name"],
            "category": stats["category"],
            "total": stats["total"],
            "core_ratio": round(core_ratio, 3),
        }

        if has_beginner and core_ratio >= 0.5:
            path_recommendations["beginner_path"].append(entry)
        if core_ratio >= 0.4:
            path_recommendations["improvement_path"].append(entry)
        if has_advanced_track or advanced_ratio >= 0.3:
            path_recommendations["sprint_path"].append(entry)

    # 7. 前端显示建议
    frontend_suggestions = [
        "1. 在章节列表中，core 节点默认展开，standard 默认展开但可折叠，advanced 默认折叠，optional 需手动展开",
        "2. 节点卡片右上角显示层级标签（核心/进阶/扩展/冷门），使用不同颜色区分",
        "3. 学习路径页面按层级筛选：入门路径=core，提高路径=core+standard，冲刺路径=advanced",
        "4. 高拥挤章节（如 2.8 动态规划）默认折叠 advanced 和 optional 节点",
        "5. 搜索结果按层级排序：core > standard > advanced > optional",
        "6. 依赖图可视化中，core 节点高亮显示，optional 节点淡化",
        "7. 用户可在设置中选择显示层级范围，控制信息密度",
    ]

    # ── 重点章节详细分析 ──
    focus_section_details = {}
    for sid, sname in FOCUS_SECTIONS.items():
        stats = section_layer_stats.get(sid, {})
        items = section_items.get(sid, [])
        focus_section_details[sid] = {
            "section_name": sname,
            "total": stats.get("total", 0),
            "core": stats.get("core", 0),
            "standard": stats.get("standard", 0),
            "advanced": stats.get("advanced", 0),
            "optional": stats.get("optional", 0),
            "core_items": [
                {"id": it["id"], "name": it["name"]}
                for it in items if item_layers[it["id"]] == "core"
            ],
            "optional_items": [
                {"id": it["id"], "name": it["name"]}
                for it in items if item_layers[it["id"]] == "optional"
            ],
        }

    # ── 汇总 ──
    layer_totals = defaultdict(int)
    for layer in item_layers.values():
        layer_totals[layer] += 1

    result = {
        "audit_time": str(date.today()),
        "total_items": len(all_items),
        "total_sections": len(section_info),
        "layer_totals": dict(layer_totals),
        "category_layer_stats": {k: dict(v) for k, v in category_layer_stats.items()},
        "section_layer_stats": section_layer_stats,
        "core_candidates": core_candidates,
        "optional_candidates": optional_candidates,
        "overcrowded_sections": overcrowded_sections,
        "path_recommendations": path_recommendations,
        "focus_section_details": focus_section_details,
        "frontend_suggestions": frontend_suggestions,
        "layering_rules": {
            "signals_used": [
                "visibility", "level", "content_status.content_priority",
                "learning_path_policy.unlock_mode", "tracks", "resolved_pre count",
                "section capacity"
            ],
            "scoring_method": "weighted_sum",
            "thresholds": {
                "core": "score <= 0 (visibility=core 且 level=L1/L2)",
                "standard": "0 < score <= 12 (visibility=core+L3+ 或 visibility=advanced+L1/L2)",
                "advanced": "12 < score <= 22 (visibility=advanced+L3+ 或 visibility=expert+L1-L2)",
                "optional": "score > 22 (visibility=expert+L3+ 或 visibility=optional)",
            },
            "overrides": [
                "visibility=optional -> forced optional",
            ],
        },
        "declaration": "本轮为只读审计，未修改主图谱、前端图谱、内容索引、内容正文、Flutter代码",
    }

    return result


def generate_markdown(result):
    """生成 Markdown 报告"""
    lines = []
    lines.append("# 学习路径分层审计报告")
    lines.append("")
    lines.append(f"审计时间：{result['audit_time']}")
    lines.append(f"总节点数：{result['total_items']}")
    lines.append(f"总章节数：{result['total_sections']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 一、分层总览
    lines.append("## 一、分层总览")
    lines.append("")
    lt = result["layer_totals"]
    lines.append("| 层级 | 节点数 | 占比 |")
    lines.append("|------|--------|------|")
    total = result["total_items"]
    for layer in ["core", "standard", "advanced", "optional"]:
        count = lt.get(layer, 0)
        ratio = f"{count/total*100:.1f}%" if total > 0 else "0%"
        label = {"core": "核心主线", "standard": "常用进阶",
                 "advanced": "专题扩展", "optional": "冷门/可折叠"}[layer]
        lines.append(f"| {label} ({layer}) | {count} | {ratio} |")
    lines.append(f"| **合计** | **{total}** | **100%** |")
    lines.append("")

    # 二、各大类分层统计
    lines.append("## 二、各大类分层统计")
    lines.append("")
    lines.append("| 大类 | core | standard | advanced | optional | 合计 |")
    lines.append("|------|------|----------|----------|----------|------|")
    for cat_name, layer_counts in result["category_layer_stats"].items():
        c = layer_counts.get("core", 0)
        s = layer_counts.get("standard", 0)
        a = layer_counts.get("advanced", 0)
        o = layer_counts.get("optional", 0)
        lines.append(f"| {cat_name} | {c} | {s} | {a} | {o} | {c+s+a+o} |")
    lines.append("")

    # 三、重点章节分层详情
    lines.append("## 三、重点章节分层详情")
    lines.append("")
    for sid, detail in result["focus_section_details"].items():
        lines.append(f"### {sid} {detail['section_name']}")
        lines.append("")
        lines.append(f"- 总节点：{detail['total']}")
        lines.append(f"- 核心：{detail['core']} | 进阶：{detail['standard']} | 扩展：{detail['advanced']} | 冷门：{detail['optional']}")
        lines.append("")
        if detail["core_items"]:
            lines.append("**核心主线节点：**")
            for it in detail["core_items"]:
                lines.append(f"- {it['id']} {it['name']}")
            lines.append("")
        if detail["optional_items"]:
            lines.append("**可折叠/冷门节点：**")
            for it in detail["optional_items"]:
                lines.append(f"- {it['id']} {it['name']}")
            lines.append("")

    # 四、高拥挤章节
    lines.append("## 四、高拥挤章节（>=60 节点）")
    lines.append("")
    if result["overcrowded_sections"]:
        lines.append("| 章节 | 大类 | 总数 | core | standard | advanced | optional | 可折叠比例 | 建议默认折叠 |")
        lines.append("|------|------|------|------|----------|----------|----------|------------|-------------|")
        for sec in result["overcrowded_sections"]:
            fold_rec = "是" if sec["recommend_default_fold"] else "否"
            lines.append(
                f"| {sec['section_id']} {sec['section_name']} | {sec['category']} | "
                f"{sec['total']} | {sec['core']} | {sec['standard']} | "
                f"{sec['advanced']} | {sec['optional']} | {sec['foldable_ratio']} | {fold_rec} |"
            )
        lines.append("")
    else:
        lines.append("无超过 60 节点的章节。")
        lines.append("")

    # 五、学习路径推荐
    lines.append("## 五、学习路径推荐")
    lines.append("")

    for path_name, label in [("beginner_path", "入门路径"),
                              ("improvement_path", "提高路径"),
                              ("sprint_path", "冲刺路径")]:
        entries = result["path_recommendations"][path_name]
        lines.append(f"### {label}")
        lines.append("")
        if entries:
            lines.append("| 章节 | 大类 | 总数 | 核心比例 |")
            lines.append("|------|------|------|----------|")
            for e in entries:
                lines.append(f"| {e['section_id']} {e['section_name']} | {e['category']} | {e['total']} | {e['core_ratio']} |")
            lines.append("")
        else:
            lines.append("无推荐章节。")
            lines.append("")

    # 六、核心主线候选列表
    lines.append("## 六、核心主线候选列表")
    lines.append("")
    lines.append(f"共 {len(result['core_candidates'])} 个核心主线节点。")
    lines.append("")
    # 按章节分组
    core_by_section = defaultdict(list)
    for it in result["core_candidates"]:
        core_by_section[it["parent"]].append(it)
    for sid in sorted(core_by_section.keys()):
        items = core_by_section[sid]
        sec_name = result["section_layer_stats"].get(sid, {}).get("name", sid)
        lines.append(f"**{sid} {sec_name}**（{len(items)} 个）")
        for it in items:
            lines.append(f"- {it['id']} {it['name']}")
        lines.append("")

    # 七、可折叠/冷门候选列表
    lines.append("## 七、可折叠/冷门候选列表")
    lines.append("")
    lines.append(f"共 {len(result['optional_candidates'])} 个可折叠/冷门节点。")
    lines.append("")
    opt_by_section = defaultdict(list)
    for it in result["optional_candidates"]:
        opt_by_section[it["parent"]].append(it)
    for sid in sorted(opt_by_section.keys()):
        items = opt_by_section[sid]
        sec_name = result["section_layer_stats"].get(sid, {}).get("name", sid)
        lines.append(f"**{sid} {sec_name}**（{len(items)} 个）")
        for it in items:
            lines.append(f"- {it['id']} {it['name']}")
        lines.append("")

    # 八、前端显示建议
    lines.append("## 八、前端显示建议")
    lines.append("")
    for s in result["frontend_suggestions"]:
        lines.append(f"- {s}")
    lines.append("")

    # 九、分层规则说明
    lines.append("## 九、分层规则说明")
    lines.append("")
    rules = result["layering_rules"]
    lines.append(f"使用信号：{', '.join(rules['signals_used'])}")
    lines.append(f"评分方法：{rules['scoring_method']}")
    lines.append("")
    lines.append("阈值：")
    for layer, desc in rules["thresholds"].items():
        lines.append(f"- {layer}: {desc}")
    lines.append("")
    lines.append("覆盖规则：")
    for o in rules["overrides"]:
        lines.append(f"- {o}")
    lines.append("")

    # 十、声明
    lines.append("## 十、声明")
    lines.append("")
    lines.append(result["declaration"])
    lines.append("")

    return "\n".join(lines)


# ── 前端可用性复核 ──

# 误分检测关键词
# 注意：关键词匹配需要精确，避免误杀（如"后缀最值"不应被"后缀"匹配）
ADVANCED_KEYWORDS = [
    "凸包", "分治转移", "线段树维护", "堆维护", "队列维护",
    "融合模型", "网络流", "自动机融合", "生成函数",
    "可持久化", "持久化", "整体二分", "扫描线",
    "树套树", "分块套", "莫队", "CDQ", "虚树",
    "后缀自动机", "AC自动机", "回文树", "后缀数组",
    "FFT", "NTT", "FWT", "多项式", "拉格朗日",
    "高斯消元", "矩阵求逆", "行列式", "线性基",
    "LCT", "Link-Cut", "动态树", "点分治", "边分治",
    "仙人掌", "圆方树", "支配树", "最短路树",
    "费用流", "最小割", "最大权闭合子图",
    "Lucas", "CRT", "BSGS", "Miller-Rabin", "Pollard",
    "欧拉函数", "莫比乌斯", "狄利克雷", "杜教筛",
    "Min_25", "洲阁筛", "数论分块",
    "KMP", "Trie", "Aho-Corasick", "Z函数", "Manacher",
    "字符串哈希", "最小表示",
    "SAM", "SA-IS",
]

ADVANCED_SECTION_PREFIXES = ["2.8", "3.13", "2.21", "4.3", "4.4", "4.5", "4.6", "4.7"]

FOCUS_SECTIONS_REVIEW = ["2.8", "3.13", "4.1", "2.9", "2.10"]


def detect_misclassified_core(item, graph_layer):
    """检测疑似误分到 core 的节点"""
    if graph_layer != "core":
        return None

    name = item.get("name", "")
    item_id = item.get("id", "")
    parent = item.get("parent", "")
    level = item.get("level", "")
    vis = item.get("visibility", "")
    lp = item.get("learning_path_policy", {})
    unlock = lp.get("unlock_mode", "") if isinstance(lp, dict) else ""
    tracks = item.get("tracks", [])

    reasons = []
    suggested_layer = "core"

    # 规则1：名称含高级关键词
    for kw in ADVANCED_KEYWORDS:
        if kw in name:
            reasons.append(f"名称含高级关键词: {kw}")
            suggested_layer = "advanced"
            break

    # 规则2：高级章节中的 L3+ 节点不应为 core
    if parent in ADVANCED_SECTION_PREFIXES and level in ("L3", "L4", "L5", "high", "advanced"):
        reasons.append(f"高级章节({parent})中 level={level}")
        if suggested_layer == "core":
            suggested_layer = "standard"

    # 规则3：unlock_mode=expert_branch 不应为 core
    if unlock == "expert_branch":
        reasons.append("unlock_mode=expert_branch")
        suggested_layer = "advanced"

    # 规则4：有 advanced track 但无 beginner track
    has_advanced = any(t.startswith("advanced_") for t in tracks)
    has_beginner = "beginner" in tracks or "csp_j" in tracks
    if has_advanced and not has_beginner:
        reasons.append("有 advanced track 但无 beginner track")
        if suggested_layer == "core":
            suggested_layer = "standard"

    # 规则5：visibility=core 但 level=L4/L5
    if vis == "core" and level in ("L4", "L5", "advanced"):
        reasons.append(f"visibility=core 但 level={level}")
        suggested_layer = "standard"

    if reasons:
        return {
            "id": item_id,
            "name": name,
            "section_id": parent,
            "current_layer": graph_layer,
            "suggested_frontend_layer": suggested_layer,
            "reason": "; ".join(reasons),
        }
    return None


def analyze_frontend_review(data, audit_result):
    """前端可用性复核"""
    all_items = []
    all_items_map = {}
    section_items = defaultdict(list)
    section_info = {}

    for cat in data["categories"]:
        for sec in cat["sections"]:
            section_info[sec["id"]] = {"id": sec["id"], "name": sec["name"], "category": cat["name"]}
            for it in sec["items"]:
                all_items.append(it)
                all_items_map[it["id"]] = it
                section_items[sec["id"]].append(it)

    # 重新计算 graph_layer 并检测误分
    suspected_misclassified_core = []
    item_graph_layer = {}
    item_frontend_layer = {}
    item_misclassified_map = {}

    for it in all_items:
        gl, score = classify_item(it, all_items_map, len(section_items.get(it.get("parent", ""), [])))
        item_graph_layer[it["id"]] = gl

        mis = detect_misclassified_core(it, gl)
        if mis:
            suspected_misclassified_core.append(mis)
            item_misclassified_map[it["id"]] = mis
            item_frontend_layer[it["id"]] = mis["suggested_frontend_layer"]
        else:
            item_frontend_layer[it["id"]] = gl

    # frontend_display_layer 统计
    frontend_layer_totals = defaultdict(int)
    for fl in item_frontend_layer.values():
        frontend_layer_totals[fl] += 1

    # 重点章节复核
    focus_section_review = {}
    for sid in FOCUS_SECTIONS_REVIEW:
        items = section_items.get(sid, [])
        info = section_info.get(sid, {})
        core_items = []
        misclassified_in_section = []
        for it in items:
            gl = item_graph_layer[it["id"]]
            fl = item_frontend_layer[it["id"]]
            if gl == "core":
                entry = {
                    "id": it["id"], "name": it["name"],
                    "graph_layer": gl, "frontend_display_layer": fl,
                    "level": it.get("level", ""), "visibility": it.get("visibility", ""),
                }
                core_items.append(entry)
                if gl != fl:
                    misclassified_in_section.append(entry)
        focus_section_review[sid] = {
            "section_name": info.get("name", ""),
            "total": len(items), "core_count": len(core_items),
            "misclassified_count": len(misclassified_in_section),
            "core_items": core_items, "misclassified_items": misclassified_in_section,
        }

    # frontend_display_layer_suggestions
    frontend_display_layer_suggestions = {
        "core": {"display": "默认展开", "description": "适合学习主线，入门必学",
                 "ui_behavior": "章节列表中默认展开，节点卡片高亮显示", "color_suggestion": "主色调（如蓝色）"},
        "standard": {"display": "默认显示，可分组", "description": "常用进阶，有一定基础后学习",
                     "ui_behavior": "默认显示但可按子主题分组折叠", "color_suggestion": "次色调（如绿色）"},
        "advanced": {"display": "默认折叠", "description": "专题扩展，需要较强前置知识",
                     "ui_behavior": "章节内默认折叠，点击展开", "color_suggestion": "中性色（如橙色）"},
        "optional": {"display": "深度折叠或搜索可见", "description": "冷门/竞赛专题，仅特定场景需要",
                     "ui_behavior": "需手动展开或仅搜索可见", "color_suggestion": "淡色（如灰色）"},
    }

    # 高拥挤章节折叠策略
    section_sizes = {sid: len(items) for sid, items in section_items.items()}
    overcrowded_section_collapse_policy = []
    for sid, size in sorted(section_sizes.items(), key=lambda x: -x[1]):
        if size < 40:
            continue
        items = section_items.get(sid, [])
        info = section_info.get(sid, {})
        fl_counts = defaultdict(int)
        for it in items:
            fl_counts[item_frontend_layer[it["id"]]] += 1
        foldable = fl_counts.get("advanced", 0) + fl_counts.get("optional", 0)
        foldable_ratio = foldable / size if size > 0 else 0
        if foldable_ratio > 0.5:
            default_collapse = "折叠 advanced+optional"
        elif foldable_ratio > 0.3:
            default_collapse = "折叠 optional"
        else:
            default_collapse = "不默认折叠"
        overcrowded_section_collapse_policy.append({
            "section_id": sid, "section_name": info.get("name", ""),
            "category": info.get("category", ""), "total": size,
            "frontend_core": fl_counts.get("core", 0),
            "frontend_standard": fl_counts.get("standard", 0),
            "frontend_advanced": fl_counts.get("advanced", 0),
            "frontend_optional": fl_counts.get("optional", 0),
            "foldable_ratio": round(foldable_ratio, 3),
            "default_collapse_policy": default_collapse,
        })

    # 首页入口章节推荐
    recommended_homepage_entry_sections = []
    for sid, items in section_items.items():
        info = section_info.get(sid, {})
        fl_counts = defaultdict(int)
        for it in items:
            fl_counts[item_frontend_layer[it["id"]]] += 1
        total = len(items)
        core_count = fl_counts.get("core", 0)
        core_ratio = core_count / total if total > 0 else 0
        if core_ratio >= 0.5 and 5 <= total <= 120:
            recommended_homepage_entry_sections.append({
                "section_id": sid, "section_name": info.get("name", ""),
                "category": info.get("category", ""), "total": total,
                "core_count": core_count, "core_ratio": round(core_ratio, 3),
                "priority": "high" if core_ratio >= 0.8 else "medium",
            })
    recommended_homepage_entry_sections.sort(key=lambda x: -x["core_ratio"])

    # 写回建议
    original_core_count = audit_result["layer_totals"]["core"]
    misclassified_ratio = len(suspected_misclassified_core) / max(original_core_count, 1)
    should_write_back = len(suspected_misclassified_core) == 0

    if should_write_back:
        write_back_recommendation = {
            "should_write_back": True,
            "reason": "无疑似误分节点，graph_layer 可直接作为前端展示层级",
        }
    else:
        write_back_recommendation = {
            "should_write_back": False,
            "reason": (
                f"存在 {len(suspected_misclassified_core)} 个疑似误分 core 节点，"
                f"占比 {misclassified_ratio:.1%}。"
                "建议先人工审核误分列表，确认后再写回图谱。"
            ),
            "verification_steps": [
                "1. 人工审核 suspected_misclassified_core 列表",
                "2. 确认每个节点的 suggested_frontend_layer 是否合理",
                "3. 如需调整，修改分层规则后重跑审计",
                "4. 确认无误后，再考虑写回图谱 visibility 字段",
            ],
        }

    return {
        "audit_time": str(date.today()),
        "total_items": len(all_items),
        "original_core_count": original_core_count,
        "suspected_misclassified_core_count": len(suspected_misclassified_core),
        "frontend_layer_totals": dict(frontend_layer_totals),
        "suspected_misclassified_core": suspected_misclassified_core,
        "focus_section_review": focus_section_review,
        "frontend_display_layer_suggestions": frontend_display_layer_suggestions,
        "overcrowded_section_collapse_policy": overcrowded_section_collapse_policy,
        "recommended_homepage_entry_sections": recommended_homepage_entry_sections,
        "write_back_recommendation": write_back_recommendation,
        "declaration": "本轮为只读审计，未修改主图谱、前端图谱、内容索引、内容正文、Flutter代码",
    }


def generate_frontend_markdown(result):
    """生成前端复核 Markdown 报告"""
    lines = []
    lines.append("# 学习路径分层前端可用性复核报告")
    lines.append("")
    lines.append(f"审计时间：{result['audit_time']}")
    lines.append(f"总节点数：{result['total_items']}")
    lines.append("")

    # 一、复核总览
    lines.append("## 一、复核总览")
    lines.append("")
    lines.append(f"- 原 core 数：{result['original_core_count']}")
    lines.append(f"- 疑似误分 core 数：{result['suspected_misclassified_core_count']}")
    lines.append("")
    lines.append("### frontend_display_layer 统计")
    lines.append("")
    fl = result["frontend_layer_totals"]
    total = result["total_items"]
    lines.append("| 层级 | 节点数 | 占比 |")
    lines.append("|------|--------|------|")
    for layer in ["core", "standard", "advanced", "optional"]:
        count = fl.get(layer, 0)
        ratio = f"{count/total*100:.1f}%" if total > 0 else "0%"
        label = {"core": "核心主线", "standard": "常用进阶",
                 "advanced": "专题扩展", "optional": "冷门/可折叠"}[layer]
        lines.append(f"| {label} ({layer}) | {count} | {ratio} |")
    lines.append("")

    # 二、疑似误分 core 节点
    lines.append("## 二、疑似误分 core 节点")
    lines.append("")
    mis = result["suspected_misclassified_core"]
    if mis:
        lines.append(f"共 {len(mis)} 个疑似误分节点：")
        lines.append("")
        lines.append("| ID | 名称 | 章节 | 建议层级 | 原因 |")
        lines.append("|----|------|------|----------|------|")
        for m in mis:
            lines.append(f"| {m['id']} | {m['name']} | {m['section_id']} | {m['suggested_frontend_layer']} | {m['reason']} |")
        lines.append("")
    else:
        lines.append("无疑似误分节点。")
        lines.append("")

    # 三、重点章节复核
    lines.append("## 三、重点章节复核")
    lines.append("")
    for sid, review in result["focus_section_review"].items():
        lines.append(f"### {sid} {review['section_name']}")
        lines.append("")
        lines.append(f"- 总节点：{review['total']}")
        lines.append(f"- core 节点：{review['core_count']}")
        lines.append(f"- 疑似误分：{review['misclassified_count']}")
        lines.append("")
        if review["misclassified_items"]:
            lines.append("**疑似误分节点：**")
            lines.append("")
            lines.append("| ID | 名称 | graph_layer | frontend_layer | level | visibility |")
            lines.append("|----|------|-------------|----------------|-------|------------|")
            for it in review["misclassified_items"]:
                lines.append(
                    f"| {it['id']} | {it['name']} | {it['graph_layer']} | "
                    f"{it['frontend_display_layer']} | {it['level']} | {it['visibility']} |"
                )
            lines.append("")

    # 四、前端展示层级建议
    lines.append("## 四、前端展示层级建议")
    lines.append("")
    suggestions = result["frontend_display_layer_suggestions"]
    for layer, sug in suggestions.items():
        label = {"core": "核心主线", "standard": "常用进阶",
                 "advanced": "专题扩展", "optional": "冷门/可折叠"}[layer]
        lines.append(f"### {label} ({layer})")
        lines.append("")
        lines.append(f"- **展示方式**：{sug['display']}")
        lines.append(f"- **说明**：{sug['description']}")
        lines.append(f"- **UI 行为**：{sug['ui_behavior']}")
        lines.append(f"- **颜色建议**：{sug['color_suggestion']}")
        lines.append("")

    # 五、高拥挤章节折叠策略
    lines.append("## 五、高拥挤章节折叠策略")
    lines.append("")
    ocs = result["overcrowded_section_collapse_policy"]
    if ocs:
        lines.append("| 章节 | 大类 | 总数 | core | standard | advanced | optional | 可折叠比例 | 默认策略 |")
        lines.append("|------|------|------|------|----------|----------|----------|------------|----------|")
        for sec in ocs:
            lines.append(
                f"| {sec['section_id']} {sec['section_name']} | {sec['category']} | "
                f"{sec['total']} | {sec['frontend_core']} | {sec['frontend_standard']} | "
                f"{sec['frontend_advanced']} | {sec['frontend_optional']} | "
                f"{sec['foldable_ratio']} | {sec['default_collapse_policy']} |"
            )
        lines.append("")

    # 六、首页入口章节推荐
    lines.append("## 六、首页入口章节推荐")
    lines.append("")
    entries = result["recommended_homepage_entry_sections"]
    if entries:
        lines.append("| 章节 | 大类 | 总数 | core 数 | core 比例 | 优先级 |")
        lines.append("|------|------|------|---------|-----------|--------|")
        for e in entries:
            lines.append(
                f"| {e['section_id']} {e['section_name']} | {e['category']} | "
                f"{e['total']} | {e['core_count']} | {e['core_ratio']} | {e['priority']} |"
            )
        lines.append("")

    # 七、写回建议
    lines.append("## 七、写回图谱建议")
    lines.append("")
    wb = result["write_back_recommendation"]
    if wb["should_write_back"]:
        lines.append(f"**建议写回**：{wb['reason']}")
    else:
        lines.append(f"**不建议立即写回**：{wb['reason']}")
        lines.append("")
        if "verification_steps" in wb:
            lines.append("验证步骤：")
            for step in wb["verification_steps"]:
                lines.append(f"- {step}")
    lines.append("")

    # 八、声明
    lines.append("## 八、声明")
    lines.append("")
    lines.append(result["declaration"])
    lines.append("")

    return "\n".join(lines)


def main():
    print("加载主图谱...")
    data = load_graph()

    print("分析分层...")
    result = analyze_graph(data)

    # 写入 JSON
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"JSON 报告已写入: {OUTPUT_JSON}")

    # 写入 Markdown
    md_content = generate_markdown(result)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown 报告已写入: {OUTPUT_MD}")

    # 前端可用性复核
    print("\n执行前端可用性复核...")
    frontend_result = analyze_frontend_review(data, result)

    FRONTEND_JSON = ROOT / "data" / "learning_path_layers_frontend_usage_review.json"
    FRONTEND_MD = ROOT / "docs" / "learning_path_layers_frontend_usage_review.md"

    FRONTEND_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(FRONTEND_JSON, "w", encoding="utf-8") as f:
        json.dump(frontend_result, f, ensure_ascii=False, indent=2)
    print(f"前端复核 JSON 已写入: {FRONTEND_JSON}")

    frontend_md = generate_frontend_markdown(frontend_result)
    FRONTEND_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(FRONTEND_MD, "w", encoding="utf-8") as f:
        f.write(frontend_md)
    print(f"前端复核 Markdown 已写入: {FRONTEND_MD}")

    # 输出摘要
    lt = result["layer_totals"]
    fl = frontend_result["frontend_layer_totals"]
    print("\n=== 学习路径分层审计结论 ===")
    print(f"graph_layer: core={lt.get('core',0)} standard={lt.get('standard',0)} advanced={lt.get('advanced',0)} optional={lt.get('optional',0)}")
    print(f"frontend_display_layer: core={fl.get('core',0)} standard={fl.get('standard',0)} advanced={fl.get('advanced',0)} optional={fl.get('optional',0)}")
    print(f"疑似误分 core 数: {frontend_result['suspected_misclassified_core_count']}")
    wb = frontend_result["write_back_recommendation"]
    print(f"是否建议写回图谱: {'是' if wb['should_write_back'] else '否'}")


if __name__ == "__main__":
    main()
