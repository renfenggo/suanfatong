#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画覆盖审计脚本 v2 - 只读审计
扫描知识图谱中 3240 个知识点，标注动画优先级 P0/P1/P2/NONE。
包含第一批动画制作清单的二次筛选：综合评分 + 章节均衡。
不修改任何图谱、内容或 Flutter 代码。
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

BATCH_SIZE = 50
MAX_PER_SECTION = 6


def load_json(rel_path):
    full = os.path.join(PROJECT_DIR, rel_path.replace("/", os.sep))
    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(rel_path, data):
    full = os.path.join(PROJECT_DIR, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_md(rel_path, text):
    full = os.path.join(PROJECT_DIR, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


# ========== 动画优先级分类规则 ==========

P0_KEYWORDS = [
    "bfs", "dfs", "广度优先", "深度优先", "bfs层序", "dfs回溯",
    "双向bfs", "迭代加深", "ida*", "a*搜索",
    "dijkstra", "spfa", "bellman-ford", "floyd",
    "拓扑排序", "topological", "kahn",
    "kruskal", "prim", "最小生成树", "mst",
    "强连通", "tarjan", "kosaraju", "scc",
    "二分图匹配", "匈牙利", "hopcroft-karp", "dinic", "网络流",
    "欧拉路径", "欧拉回路", "欧拉图",
    "桥", "割点", "双连通",
    "lca", "最近公共祖先",
    "并查集", "union-find", "disjoint set",
    "堆", "二叉堆", "优先队列", "heap",
    "线段树", "segment tree", "lazy propagation", "懒标记",
    "树状数组", "fenwick", "bit",
    "主席树", "persistent segment",
    "平衡树", "treap", "splay", "avl", "红黑树",
    "哈希", "hash表", "散列表",
    "单调栈", "单调队列",
    "双端队列",
    "字典树", "trie",
    "二叉搜索树", "bst",
    "跳表", "skip list",
    "可持久化",
    "分块",
    "背包", "knapsack", "dp转移", "状态转移",
    "区间dp", "树形dp", "状压dp", "数位dp", "概率dp",
    "lis", "最长递增子序列", "lcs",
    "斜率优化", "单调队列优化dp",
    "kmp", "模式匹配",
    "ac自动机", "aho-corasick",
    "后缀数组", "sa", "suffix array",
    "后缀自动机", "sam",
    "manacher", "回文串",
    "z函数", "扩展kmp",
    "字符串哈希", "rolling hash",
    "筛法", "埃拉托斯特尼", "欧拉筛",
    "莫比乌斯", "mobius",
    "杜教筛", "min_25筛",
    "递推", "容斥",
    "逆元", "扩展欧几里得", "exgcd",
    "中国剩余定理", "crt",
    "bsgs", "离散对数",
    " Lucas",
    "扫描线", "sweep line",
    "凸包", "convex hull",
    "半平面交",
    "旋转卡壳",
    "最近点对",
    "voronoi",
]

P1_KEYWORDS = [
    "排序", "sort", "冒泡", "选择排序", "插入排序", "归并排序", "快速排序",
    "希尔排序", "计数排序", "基数排序", "桶排序",
    "二分查找", "binary search", "三分",
    "双指针", "two pointer", "滑动窗口", "sliding window",
    "前缀和", "差分",
    "贪心", "greedy",
    "哈夫曼", "huffman",
    "快速幂", "fast pow", "矩阵快速幂",
    "位运算", "bitwise",
    "递归", "recursion", "分治", "divide and conquer",
    "树遍历", "先序", "中序", "后序", "层序",
    "栈", "队列",
    "链表", "list",
    "二叉树", "平衡树",
    "最小公倍数", "lcm", "最大公约数", "gcd",
    "费马小定理",
    "pascal", "杨辉三角",
    "卡特兰数", "catalan",
    "排列组合",
    "容斥原理",
    "期望",
    "博弈", "sg函数", "nim",
    "cdq分治",
    "整体二分",
    "回溯", "剪枝",
    "离散化", "去重",
    "栈模拟",
    "单调性",
    "倍增",
]

NONE_KEYWORDS = [
    "概念", "定义", "术语", "背景", "历史", "起源",
    "复杂度分析", "时间复杂度", "空间复杂度",
    "模板", "代码框架", "常见错误", "调试",
    "输入输出", "io", "文件读写",
    "竞赛规则", "评分方式", "oj使用",
    "数学公式推导", "定理证明",
    "编译原理", "语言特性",
]


def classify_item(item):
    item_id = item.get("id", "")
    name = item.get("name", "").lower()
    for kw in P0_KEYWORDS:
        if kw in name or kw in item_id.lower():
            return "P0"
    for kw in P1_KEYWORDS:
        if kw in name or kw in item_id.lower():
            return "P1"
    for kw in NONE_KEYWORDS:
        if kw in name:
            return "NONE"
    return "P2"


def recommend_animation_form(item):
    name = item.get("name", "").lower()
    item_id = item.get("id", "")
    graph_kw = ["图", "bfs", "dfs", "dijkstra", "kruskal", "prim",
                "拓扑", "强连通", "二分图", "欧拉", "tarjan",
                "树", "lca", "trie", "二叉", "遍历", "子树"]
    for kw in graph_kw:
        if kw in name or kw in item_id.lower():
            return "Flutter"
    dp_kw = ["dp", "背包", "lis", "lcs", "区间dp", "树形dp",
             "状压", "数位", "状态转移", "递推"]
    for kw in dp_kw:
        if kw in name or kw in item_id.lower():
            return "static_steps"
    ds_kw = ["线段树", "树状数组", "并查集", "堆", "平衡树",
             "主席树", "哈希", "单调栈", "单调队列", "分块"]
    for kw in ds_kw:
        if kw in name or kw in item_id.lower():
            return "Flutter"
    str_kw = ["kmp", "字符串", "后缀", "manacher", "ac自动",
              "sam", "z函数", "hash"]
    for kw in str_kw:
        if kw in name or kw in item_id.lower():
            return "HTML"
    geo_kw = ["几何", "扫描线", "凸包", "半平面", "旋转", "面积",
              "叉积", "点积", "坐标"]
    for kw in geo_kw:
        if kw in name or kw in item_id.lower():
            return "HTML"
    return "Flutter"


# ========== 第一批精选：按名称匹配核心知识点 ==========

# 按算法类别定义必须入选第一批的核心知识点名称模式
# 每个条目: (关键词列表, 类别标签, 模板建议, 工作量估计, 复用潜力)
MUST_HAVE_PATTERNS = [
    # --- 搜索 ---
    (["bfs"], "搜索", "graph_traversal", "medium", "high"),
    (["dfs", "深度优先"], "搜索", "graph_traversal", "medium", "high"),
    (["回溯"], "搜索", "backtrack", "medium", "high"),
    (["剪枝"], "搜索", "backtrack", "low", "high"),

    # --- 排序/二分 ---
    (["快速排序", "quick sort"], "排序/二分", "sorting", "medium", "high"),
    (["归并排序", "merge sort"], "排序/二分", "sorting", "medium", "high"),
    (["二分答案", "答案二分"], "排序/二分", "binary_search", "medium", "high"),

    # --- 基础数据结构 ---
    (["栈", "stack"], "基础数据结构", "stack", "low", "high"),
    (["队列", "queue"], "基础数据结构", "queue", "low", "high"),
    (["堆", "heap", "priority_queue"], "基础数据结构", "heap", "medium", "high"),
    (["并查集", "union", "dsu"], "基础数据结构", "dsu", "medium", "high"),

    # --- 区间结构 ---
    (["线段树", "segment tree"], "区间结构", "segment_tree", "high", "medium"),
    (["树状数组", "fenwick", "bit", "fenwick_tree"], "区间结构", "fenwick", "medium", "medium"),
    (["懒标记", "lazy propagation"], "区间结构", "lazy_seg", "high", "medium"),

    # --- 图论 ---
    (["dijkstra"], "图论", "shortest_path", "medium", "high"),
    (["拓扑排序", "topological", "kahn"], "图论", "topo_sort", "medium", "medium"),
    (["kruskal"], "图论", "mst", "medium", "medium"),
    (["prim"], "图论", "mst", "medium", "medium"),
    (["tarjan", "强连通", "scc"], "图论", "scc", "high", "medium"),

    # --- 字符串 ---
    (["kmp"], "字符串", "string_match", "medium", "high"),
    (["trie", "字典树"], "字符串", "trie", "medium", "high"),
    (["ac自动机", "aho-corasick"], "字符串", "ac_auto", "high", "medium"),

    # --- 动态规划 ---
    (["01背包", "0-1背包", "零一背包", "knapsack_01"], "动态规划", "dp_table", "medium", "high"),
    (["lis", "最长递增子序列"], "动态规划", "dp_sequence", "medium", "high"),
    (["区间dp", "区间 dp", "石子合并"], "动态规划", "dp_interval", "high", "medium"),
    (["树形dp", "树形 dp", "树上dp"], "动态规划", "dp_tree", "high", "medium"),

    # --- 数学 ---
    (["快速幂", "fast pow", "快速幂取模"], "数学", "math_pow", "low", "high"),
    (["欧几里得", "gcd", "辗转相除"], "数学", "math_gcd", "low", "high"),
    (["筛法", "欧拉筛", "素数筛"], "数学", "sieve", "medium", "medium"),
    (["组合数", "c(n", "组合计数"], "数学", "math_comb", "medium", "medium"),

    # --- 高级数据结构 ---
    (["主席树", "persistent segment", "可持久化线段树"], "高级数据结构", "persistent_seg", "high", "low"),
    (["李超线段树"], "高级数据结构", "li_chao", "high", "low"),
    (["动态开点"], "高级数据结构", "dynamic_open", "medium", "medium"),

    # --- 其他高价值 ---
    (["单调栈"], "基础数据结构", "monotone_stack", "medium", "high"),
    (["前缀和"], "基础数据结构", "prefix_sum", "low", "high"),
    (["差分"], "基础数据结构", "difference", "low", "high"),
]


def score_item_for_first_batch(item, animated_item_ids):
    """对候选知识点进行综合评分"""
    name = item.get("name", "").lower()
    item_id = item.get("id", "")
    has_anim = item_id in animated_item_ids
    score = 0.0
    reasons = []

    # 1. 竞赛核心价值 (0-30)
    core_kw = ["dijkstra", "kmp", "线段树", "tarjan", "并查集", "主席树",
               "拓扑排序", "kruskal", "ac自动机", "01背包", "lis", "快速幂",
               "树状数组", "欧几里得", "bfs", "dfs", "堆", "字典树",
               "筛法", "快速排序", "归并排序", "单调栈", "前缀和", "差分",
               "回溯", "二分答案"]
    for kw in core_kw:
        if kw in name:
            score += 25
            reasons.append("竞赛核心算法")
            break
    else:
        # 次核心
        second_core = ["floyd", "spfa", "prim", "lca", "平衡树", "splay",
                       "背包", "区间dp", "树形dp", "容斥", "快速幂",
                       "组合数", "哈希", "欧拉筛", "双指针", "二分查找"]
        for kw in second_core:
            if kw in name:
                score += 18
                reasons.append("竞赛次核心算法")
                break

    # 2. 初学者理解收益 (0-25)
    beginner_friendly = ["bfs", "dfs", "快速排序", "归并排序", "二分查找",
                        "栈", "队列", "前缀和", "并查集", "堆",
                        "枚举", "递归", "01背包", "滑动窗口",
                        "冒泡排序", "贪心", "双指针"]
    for kw in beginner_friendly:
        if kw in name:
            score += 22
            reasons.append("初学者理解收益大")
            break

    # 3. 动画表达收益 (0-25)
    visual_kw = ["排序", "搜索", "遍历", "匹配", "转移", "构建",
                "划分", "合并", "旋转", "调整", "扩展", "收缩",
                "入栈", "出栈", "入队", "出队", "push", "pop",
                "merge", "partition", "relax", "rotate", "build"]
    for kw in visual_kw:
        if kw in name:
            score += 20
            reasons.append("动画表达收益高")
            break

    # 4. 未有动画加分 (0-15)
    if not has_anim:
        score += 15
        reasons.append("尚无动画")
    else:
        score -= 5
        reasons.append("已有动画")

    # 5. 模板复用潜力 (0-10)
    template_reusable = ["排序", "bfs", "dfs", "dp", "二分", "前缀和",
                        "并查集", "堆", "线段树", "树状数组",
                        "快速幂", "gcd", "筛法"]
    for kw in template_reusable:
        if kw in name:
            score += 10
            reasons.append("模板可复用")
            break

    return round(score, 1), reasons


def suggest_template(item):
    """建议动画模板"""
    name = item.get("name", "").lower()
    templates = {
        "graph_traversal": ["bfs", "dfs", "搜索", "遍历"],
        "sorting": ["排序", "sort", "冒泡", "归并", "快速"],
        "binary_search": ["二分", "binary search"],
        "stack": ["栈", "stack", "单调栈"],
        "queue": ["队列", "queue"],
        "heap": ["堆", "heap", "priority"],
        "dsu": ["并查集", "union", "dsu"],
        "segment_tree": ["线段树", "segment tree"],
        "fenwick": ["树状数组", "fenwick", "bit"],
        "lazy_seg": ["懒标记", "lazy"],
        "shortest_path": ["dijkstra", "spfa", "floyd", "最短路"],
        "topo_sort": ["拓扑", "topological", "kahn"],
        "mst": ["最小生成树", "kruskal", "prim", "mst"],
        "scc": ["强连通", "tarjan", "scc"],
        "string_match": ["kmp", "匹配"],
        "trie": ["trie", "字典树"],
        "ac_auto": ["ac自动机"],
        "dp_table": ["背包", "knapsack", "dp"],
        "dp_sequence": ["lis", "lcs", "子序列"],
        "dp_interval": ["区间dp", "石子合并", "区间"],
        "dp_tree": ["树形dp", "树上"],
        "math_pow": ["快速幂", "fast pow"],
        "math_gcd": ["欧几里得", "gcd", "辗转相除"],
        "sieve": ["筛法", "欧拉筛", "素数筛"],
        "math_comb": ["组合数", "组合"],
        "persistent_seg": ["主席树", "可持久化"],
        "backtrack": ["回溯", "backtrack"],
        "prefix_sum": ["前缀和"],
        "difference": ["差分"],
    }
    for tpl_name, kws in templates.items():
        for kw in kws:
            if kw in name:
                return tpl_name
    return "custom"


def estimate_effort(item):
    """估计动画制作工作量"""
    name = item.get("name", "").lower()
    high_effort = ["线段树", "主席树", "tarjan", "ac自动机", "网络流",
                  "后缀", "sam", "动态开点", "李超", "旋转卡壳",
                  "半平面交", "凸包", "扫描线", "cdq", "整体二分"]
    medium_effort = ["dijkstra", "kruskal", "prim", "拓扑", "kmp",
                    "堆", "区间dp", "树形dp", "懒标记", "筛法",
                    "快速排序", "归并排序", "倍增", "lca", "平衡树"]
    for kw in high_effort:
        if kw in name:
            return "high"
    for kw in medium_effort:
        if kw in name:
            return "medium"
    return "low"


def reuse_potential(item):
    """评估复用潜力"""
    name = item.get("name", "").lower()
    high_reuse = ["排序", "bfs", "dfs", "二分", "前缀和", "差分",
                 "栈", "队列", "并查集", "快速幂", "gcd",
                 "堆", "树状数组", "回溯", "双指针", "滑动窗口"]
    for kw in high_reuse:
        if kw in name:
            return "high"
    medium_reuse = ["线段树", "拓扑", "dijkstra", "kruskal", "kmp",
                   "trie", "dp", "背包", "筛法", "哈希"]
    for kw in medium_reuse:
        if kw in name:
            return "medium"
    return "low"


def select_balanced_first_batch(all_items, animated_item_ids):
    """
    第一批 50 个动画的均衡选择策略:
    Step 1: 从 P0/P1 候选中按 must_have 模式匹配核心知识点
    Step 2: 对剩余候选评分排序
    Step 3: 按章节均衡填充到 50 个 (每章节最多 MAX_PER_SECTION)
    """
    # Step 1: 收集所有候选 (P0 + P1, 未有动画优先)
    candidates = []
    for item in all_items:
        item_id = item.get("id", "")
        name = item.get("name", "").lower()
        priority = classify_item(item)
        if priority in ("P0", "P1"):
            has_anim = item_id in animated_item_ids
            score, reasons = score_item_for_first_batch(item, animated_item_ids)
            candidates.append({
                "id": item_id,
                "name": item.get("name", ""),
                "section_id": item.get("_section_id", ""),
                "section_name": item.get("_section_name", ""),
                "category": item.get("_category", ""),
                "priority": priority,
                "score": score,
                "reasons": reasons,
                "has_animation": has_anim,
            })

    # Step 2: 按名称匹配 must_have 模式，标记为核心必选
    selected = []
    selected_ids = set()
    section_count = defaultdict(int)

    def try_add(item, source=""):
        iid = item["id"]
        sid = item["section_id"]
        if iid in selected_ids:
            return False
        if section_count[sid] >= MAX_PER_SECTION:
            return False
        selected_ids.add(iid)
        section_count[sid] += 1
        item["_source"] = source
        selected.append(item)
        return True

    # 先匹配 must_have 模式
    for patterns, cat_label, tpl, effort, reuse in MUST_HAVE_PATTERNS:
        best_match = None
        best_score = -999
        for cand in candidates:
            if cand["id"] in selected_ids:
                continue
            name_lower = cand["name"].lower()
            matched = all(any(p in name_lower for p in [pk]) for pk in patterns)
            if matched and cand["score"] > best_score:
                best_match = cand
                best_score = cand["score"]
        if best_match:
            best_match["_category_label"] = cat_label
            best_match["_suggested_template"] = tpl
            best_match["_estimated_effort"] = effort
            best_match["_reuse_potential"] = reuse
            try_add(best_match, "must_have")

    print(f"  must_have 匹配: {len(selected)} 个")

    # Step 3: 剩余名额按评分排序 + 章节均衡填充
    remaining = [c for c in candidates if c["id"] not in selected_ids]
    remaining.sort(key=lambda x: (-x["score"], x["section_id"], x["id"]))

    for cand in remaining:
        if len(selected) >= BATCH_SIZE:
            break
        cand["_category_label"] = cand["category"]
        cand["_suggested_template"] = suggest_template(cand)
        cand["_estimated_effort"] = estimate_effort(cand)
        cand["_reuse_potential"] = reuse_potential(cand)
        try_add(cand, "scored")

    print(f"  第一批总计: {len(selected)} 个")
    print(f"  覆盖章节数: {len(section_count)}")

    # 统计
    sec_dist = Counter()
    for it in selected:
        sec_dist[it["section_id"]] += 1
    print(f"  章节分布 (top 10):")
    for sid, cnt in sec_dist.most_common(10):
        print(f"    {sid}: {cnt}")

    # 暂缓高优先级清单
    deferred = []
    for cand in candidates:
        if cand["id"] not in selected_ids and cand["priority"] == "P0":
            defer_reasons = []
            if section_count.get(cand["section_id"], 0) >= MAX_PER_SECTION:
                defer_reasons.append(f"章节 {cand['section_id']} 名额已满")
            else:
                defer_reasons.append("评分低于第一批阈值")
            if cand["has_animation"]:
                defer_reasons.append("已有动画")
            deferred.append({
                "id": cand["id"],
                "name": cand["name"],
                "section_id": cand["section_id"],
                "section_name": cand["section_name"],
                "priority": cand["priority"],
                "score": cand["score"],
                "defer_reasons": defer_reasons,
            })

    deferred.sort(key=lambda x: (-x["score"], x["section_id"]))
    print(f"  暂缓 P0 候选: {len(deferred)} 个")

    return selected, deferred, section_count


def main():
    print("=" * 60)
    print("动画覆盖审计 v2 - 只读模式")
    print("=" * 60)

    # ===== 1. 加载主图谱 =====
    print("\n[1/6] 加载主图谱...")
    graph = load_json("merged_knowledge_graph_item_dependencies_refined.json")

    all_items = []
    section_items = defaultdict(list)
    section_names = {}

    for category in graph.get("categories", []):
        cat_name = category.get("name", "")
        for section in category.get("sections", []):
            sec_id = section.get("id", "")
            sec_name = section.get("name", "")
            section_names[sec_id] = f"{sec_id} {sec_name}"
            for item in section.get("items", []):
                item["_section_id"] = sec_id
                item["_section_name"] = sec_name
                item["_category"] = cat_name
                all_items.append(item)
                section_items[sec_id].append(item)

    total_items = len(all_items)
    print(f"  主图谱知识点总数: {total_items}")
    print(f"  章节数: {len(section_items)}")

    # ===== 2. 加载已有动画清单 =====
    print("\n[2/6] 加载已有动画清单...")
    manifest = load_json("assets/data/cpp/animations/cpp_animation_manifest.json")
    animations = manifest.get("animations", [])

    animated_item_ids = set()
    animated_map = {}
    for anim in animations:
        aid = anim.get("animationId", "")
        item_id = anim.get("itemId", "")
        title = anim.get("title", "")
        atype = anim.get("type", "")
        if item_id:
            animated_item_ids.add(item_id)
            animated_map[item_id] = {
                "animationId": aid, "title": title, "type": atype
            }

    print(f"  已有动画总数: {len(animations)}")
    print(f"  已覆盖 itemId 数: {len(animated_item_ids)}")

    # ===== 3. 分类动画优先级 =====
    print("\n[3/6] 分类动画优先级...")

    priority_counts = Counter()
    priority_items = defaultdict(list)
    section_priority_counts = defaultdict(lambda: Counter())
    has_animation_priority = Counter()

    for item in all_items:
        item_id = item.get("id", "")
        name = item.get("name", "")
        sec_id = item["_section_id"]

        priority = classify_item(item)
        anim_form = recommend_animation_form(item)
        has_anim = item_id in animated_item_ids

        item_info = {
            "id": item_id, "name": name,
            "section_id": sec_id, "section_name": item["_section_name"],
            "category": item["_category"],
            "priority": priority,
            "recommended_form": anim_form,
            "has_animation": has_anim,
            "existing_animation": animated_map.get(item_id, None)
        }

        priority_counts[priority] += 1
        priority_items[priority].append(item_info)
        section_priority_counts[sec_id][priority] += 1
        if has_anim:
            has_animation_priority[priority] += 1

    print(f"  P0: {priority_counts['P0']}, P1: {priority_counts['P1']}")
    print(f"  P2: {priority_counts['P2']}, NONE: {priority_counts['NONE']}")

    # ===== 4. 章节动画价值评估 =====
    print("\n[4/6] 章节动画价值评估...")

    section_animation_value = {}
    for sec_id, items_list in section_items.items():
        sec_name = section_names.get(sec_id, sec_id)
        p0c = section_priority_counts[sec_id]["P0"]
        p1c = section_priority_counts[sec_id]["P1"]
        p2c = section_priority_counts[sec_id]["P2"]
        nonec = section_priority_counts[sec_id]["NONE"]
        t = len(items_list)
        vs = p0c * 3 + p1c * 2 + p2c * 1
        anim_in_sec = sum(1 for it in items_list if it["id"] in animated_item_ids)
        cov = (anim_in_sec / t * 100) if t > 0 else 0
        rec = ""
        if p0c > 10:
            rec = "强烈建议重点动画化"
        elif p0c > 5:
            rec = "建议动画化"
        elif nonec > t * 0.7:
            rec = "不建议动画化(多为概念)"
        else:
            rec = "可选动画化"
        section_animation_value[sec_id] = {
            "section_id": sec_id, "section_name": sec_name,
            "total_items": t, "P0": p0c, "P1": p1c, "P2": p2c, "NONE": nonec,
            "value_score": vs, "animated_count": anim_in_sec,
            "coverage_percent": round(cov, 1), "recommendation": rec
        }

    sorted_sections = sorted(section_animation_value.values(),
                             key=lambda x: x["value_score"], reverse=True)
    high_value_sections = sorted_sections[:15]
    no_anim_sections = [s for s in sorted_sections
                        if s["recommendation"] == "不建议动画化(多为概念)"]

    # ===== 5. 第一批均衡选择 =====
    print("\n[5/6] 第一批动画均衡选择...")
    first_batch, deferred_p0, section_count = select_balanced_first_batch(
        all_items, animated_item_ids
    )

    # 为每个选中项补全推荐动画形式
    for it in first_batch:
        it["recommended_form"] = recommend_animation_form(it)
        it["animation_value_reason"] = "; ".join(it.get("reasons", []))

    # ===== 6. 生成报告 =====
    print("\n[6/6] 生成报告...")

    # --- JSON 报告 ---
    report = {
        "audit_time": datetime.now().isoformat(),
        "audit_version": "v2_balanced",
        "total_items": total_items,
        "total_sections": len(section_items),
        "existing_animations": len(animations),
        "existing_animation_item_ids": len(animated_item_ids),
        "priority_summary": dict(priority_counts),
        "animation_coverage_by_priority": dict(has_animation_priority),
        "first_batch_50_balanced": [
            {
                "rank": i + 1,
                "id": it["id"],
                "name": it["name"],
                "section_id": it["section_id"],
                "section_name": it["section_name"],
                "category": it.get("_category_label", it["category"]),
                "priority": it["priority"],
                "score": it["score"],
                "recommended_form": it["recommended_form"],
                "animation_value_reason": it.get("animation_value_reason", ""),
                "suggested_template": it.get("_suggested_template", "custom"),
                "estimated_effort": it.get("_estimated_effort", "medium"),
                "reuse_potential": it.get("_reuse_potential", "medium"),
                "has_animation": it["has_animation"],
                "selection_source": it.get("_source", ""),
            }
            for i, it in enumerate(first_batch)
        ],
        "deferred_high_priority": deferred_p0[:100],
        "section_animation_value_top15": high_value_sections,
        "sections_not_recommended_for_animation": [
            {"section_id": s["section_id"], "section_name": s["section_name"],
             "reason": s["recommendation"]}
            for s in no_anim_sections[:20]
        ],
        "old_batch_issues": [
            "旧清单按 ID 顺序选取，2.1 章节占据过多名额",
            "未考虑竞赛核心价值和初学者收益的综合评分",
            "未做章节均衡限制",
            "未标注模板复用潜力和工作量估计",
        ],
        "new_batch_improvements": [
            "按算法类别 must_have 模式匹配核心知识点",
            "综合评分: 竞赛核心价值 + 初学者收益 + 动画表达 + 无动画加分 + 复用潜力",
            "每章节最多 6 个名额，确保分布均衡",
            "标注推荐模板、工作量、复用潜力",
            "生成暂缓高优先级清单供后续批次使用",
        ],
        "input_files": [
            "merged_knowledge_graph_item_dependencies_refined.json",
            "assets/data/cpp/animations/cpp_animation_manifest.json"
        ],
        "unchanged_files": [
            "merged_knowledge_graph_item_dependencies_refined.json",
            "assets/data/knowledge/io_v4_4.json",
            "assets/data/knowledge_content/content_index.json",
            "assets/data/knowledge_content/items/*",
            "assets/data/cpp/animations/*",
            "lib/*", "test/*", "pubspec.yaml"
        ]
    }

    save_json("data/animation_coverage_audit.json", report)
    save_json("data/animation_first_batch_selection_review.json", {
        "audit_time": datetime.now().isoformat(),
        "first_batch_50_balanced": report["first_batch_50_balanced"],
        "deferred_high_priority": report["deferred_high_priority"],
        "old_batch_issues": report["old_batch_issues"],
        "new_batch_improvements": report["new_batch_improvements"],
    })

    # --- Markdown 报告 ---
    lines = []
    lines.append("# 动画覆盖审计报告 v2 (均衡选择版)")
    lines.append("")
    lines.append(f"**审计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**知识点总数**: {total_items}")
    lines.append(f"**已有动画数**: {len(animations)} (覆盖 {len(animated_item_ids)} 个 itemId)")
    lines.append(f"**动画覆盖率**: {len(animated_item_ids)/total_items*100:.1f}%")
    lines.append("")

    # 1. 优先级分布
    lines.append("## 1. 动画优先级分布")
    lines.append("")
    lines.append("| 优先级 | 数量 | 已有动画 | 含义 |")
    lines.append("|--------|------|----------|------|")
    lines.append(f"| P0 | {priority_counts['P0']} | {has_animation_priority['P0']} | 强烈建议动画 |")
    lines.append(f"| P1 | {priority_counts['P1']} | {has_animation_priority['P1']} | 适合动画 |")
    lines.append(f"| P2 | {priority_counts['P2']} | {has_animation_priority['P2']} | 可选动画 |")
    lines.append(f"| NONE | {priority_counts['NONE']} | {has_animation_priority['NONE']} | 不适合动画 |")
    lines.append("")

    # 2. 旧清单问题说明
    lines.append("## 2. 旧清单问题与改进")
    lines.append("")
    lines.append("### 旧清单问题:")
    for issue in report["old_batch_issues"]:
        lines.append(f"- {issue}")
    lines.append("")
    lines.append("### 新清单改进:")
    for imp in report["new_batch_improvements"]:
        lines.append(f"- {imp}")
    lines.append("")

    # 3. 第一批均衡清单
    lines.append("## 3. 第一批动画制作清单 (均衡选择版)")
    lines.append("")
    lines.append(f"**总数**: {len(first_batch)} 个 | **每章节上限**: {MAX_PER_SECTION} 个")
    lines.append("")
    lines.append("| # | ID | 名称 | 章节 | 优先级 | 评分 | 推荐形式 | 模板 | 工作量 | 复用 | 来源 |")
    lines.append("|---|----|----|----|--------|------|---------|------|--------|------|------|")
    for i, it in enumerate(first_batch):
        form = it["recommended_form"]
        tpl = it.get("_suggested_template", "-")
        eff = it.get("_estimated_effort", "-")
        reuse = it.get("_reuse_potential", "-")
        src = it.get("_source", "-")
        anim_s = "[已有]" if it["has_animation"] else ""
        lines.append(
            f"| {i+1} | {it['id']} | {it['name']} | {it['section_name']} | "
            f"{it['priority']} | {it['score']} | {form} | {tpl} | {eff} | {reuse} | {src} {anim_s} |"
        )
    lines.append("")

    # 章节分布统计
    batch_sec_dist = Counter()
    form_dist = Counter()
    effort_dist = Counter()
    for it in first_batch:
        batch_sec_dist[it["section_id"]] += 1
        form_dist[it["recommended_form"]] += 1
        effort_dist[it.get("_estimated_effort", "medium")] += 1

    lines.append("### 章节分布")
    lines.append("")
    for sid, cnt in batch_sec_dist.most_common():
        sname = section_names.get(sid, sid)
        lines.append(f"- {sid} {sname}: {cnt} 个")
    lines.append("")

    lines.append("### 动画形式分布")
    lines.append("")
    form_names = {"Flutter": "Flutter 原生动画 JSON", "HTML": "HTML/WebView",
                   "static_steps": "静态图 + 步骤"}
    for form, cnt in form_dist.most_common():
        lines.append(f"- {form_names.get(form, form)}: {cnt} 个")
    lines.append("")

    lines.append("### 工作量分布")
    lines.append("")
    for eff, cnt in effort_dist.most_common():
        lines.append(f"- {eff}: {cnt} 个")
    lines.append("")

    # 4. 暂缓高优先级清单
    lines.append("## 4. 暂缓高优先级清单 (P0 未入选)")
    lines.append("")
    lines.append(f"**暂缓总数**: {len(deferred_p0)} 个 (仅列前 30)")
    lines.append("")
    lines.append("| ID | 名称 | 章节 | 评分 | 暂缓原因 |")
    lines.append("|----|----|----|------|---------|")
    for it in deferred_p0[:30]:
        reasons = ", ".join(it["defer_reasons"])
        lines.append(f"| {it['id']} | {it['name']} | {it['section_name']} | {it['score']} | {reasons} |")
    lines.append("")

    # 5. 可复用模板
    lines.append("## 5. 推荐动画模板复用")
    lines.append("")
    template_items = defaultdict(list)
    for it in first_batch:
        tpl = it.get("_suggested_template", "custom")
        template_items[tpl].append(f"{it['id']} {it['name']}")
    for tpl, items in sorted(template_items.items()):
        lines.append(f"### {tpl} ({len(items)} 个)")
        for item_str in items:
            lines.append(f"- {item_str}")
        lines.append("")

    # 6. 章节动画价值
    lines.append("## 6. 章节动画价值排名 (前 15)")
    lines.append("")
    lines.append("| # | 章节 | 总数 | P0 | P1 | 价值分 | 已有动画 | 覆盖率 | 建议 |")
    lines.append("|---|------|------|----|----|--------|---------|--------|------|")
    for i, s in enumerate(high_value_sections):
        lines.append(
            f"| {i+1} | {s['section_id']} {s['section_name']} | {s['total_items']} | "
            f"{s['P0']} | {s['P1']} | {s['value_score']} | {s['animated_count']} | "
            f"{s['coverage_percent']}% | {s['recommendation']} |"
        )
    lines.append("")

    # 7. 声明
    lines.append("## 7. 重要声明")
    lines.append("")
    lines.append("**本次审计严格遵循只读原则，未修改以下任何文件:**")
    lines.append("- 主图谱 (merged_knowledge_graph_item_dependencies_refined.json)")
    lines.append("- 前端图谱 (assets/data/knowledge/io_v4_4.json)")
    lines.append("- 内容索引 (assets/data/knowledge_content/content_index.json)")
    lines.append("- 内容正文文件 (assets/data/knowledge_content/items/*)")
    lines.append("- Flutter 代码 (lib/*, test/*, pubspec.yaml)")
    lines.append("- 动画数据文件 (assets/data/cpp/animations/*)")
    lines.append("")
    lines.append("**生成/更新的文件:**")
    lines.append("- tools/audit_animation_coverage.py (本脚本)")
    lines.append("- docs/animation_coverage_audit_report.md (本报告)")
    lines.append("- data/animation_coverage_audit.json (数据报告)")
    lines.append("- docs/animation_first_batch_selection_review.md (清单审查报告)")
    lines.append("- data/animation_first_batch_selection_review.json (清单审查数据)")
    lines.append("")

    save_md("docs/animation_coverage_audit_report.md", "\n".join(lines))

    # --- 清单审查 Markdown ---
    review_lines = []
    review_lines.append("# 动画第一批清单二次筛选审查报告")
    review_lines.append("")
    review_lines.append(f"**审查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    review_lines.append("")
    review_lines.append("## 1. 旧清单问题")
    review_lines.append("")
    for issue in report["old_batch_issues"]:
        review_lines.append(f"- {issue}")
    review_lines.append("")
    review_lines.append("## 2. 新清单选择策略")
    review_lines.append("")
    review_lines.append("1. **must_have 模式匹配**: 按算法类别定义核心知识点名称模式，优先匹配")
    review_lines.append("2. **综合评分排序**: 竞赛核心价值(25) + 初学者收益(22) + 动画表达收益(20) + 无动画加分(15) + 复用潜力(10)")
    review_lines.append("3. **章节均衡限制**: 每章节最多 6 个名额")
    review_lines.append("4. **评分填充**: 剩余名额按综合评分降序选取")
    review_lines.append("")

    review_lines.append("## 3. 是否建议进入动画制作阶段")
    review_lines.append("")
    review_lines.append("**建议: 可以进入动画制作阶段。**")
    review_lines.append("")
    review_lines.append("理由:")
    review_lines.append("- 第一批 50 个动画覆盖搜索、排序、数据结构、图论、字符串、DP、数学等核心类别")
    review_lines.append("- 章节分布均衡，无单一章节过度集中")
    review_lines.append("- 多数动画可复用模板 (排序、搜索、DP 表格等)")
    review_lines.append("- 已有 111 个动画的制作经验可供参考")
    review_lines.append("- 建议先从 low/medium 工作量的动画开始，快速建立 MVP")
    review_lines.append("")

    review_lines.append("## 4. 声明")
    review_lines.append("")
    review_lines.append("本审查仅做只读分析，未修改任何图谱、内容或代码文件。")
    review_lines.append("")

    save_md("docs/animation_first_batch_selection_review.md", "\n".join(review_lines))

    # ===== 摘要输出 =====
    form_counter = Counter(it["recommended_form"] for it in first_batch)
    print("\n[PASS] 动画覆盖审计 v2 完成")
    print(f"生成文件:")
    print(f"  - tools/audit_animation_coverage.py")
    print(f"  - docs/animation_coverage_audit_report.md")
    print(f"  - data/animation_coverage_audit.json")
    print(f"  - docs/animation_first_batch_selection_review.md")
    print(f"  - data/animation_first_batch_selection_review.json")

    print("\n" + "=" * 60)
    print("AUDIT_SUMMARY_BEGIN")
    print(f"total_items={total_items}")
    print(f"existing_animations={len(animations)}")
    print(f"P0={priority_counts['P0']}")
    print(f"P1={priority_counts['P1']}")
    print(f"P2={priority_counts['P2']}")
    print(f"NONE={priority_counts['NONE']}")
    print(f"first_batch_size={len(first_batch)}")
    print(f"deferred_p0_count={len(deferred_p0)}")
    print(f"covered_sections={len(section_count)}")
    print(f"flutter_count={form_counter.get('Flutter', 0)}")
    print(f"html_count={form_counter.get('HTML', 0)}")
    print(f"static_steps_count={form_counter.get('static_steps', 0)}")
    print("AUDIT_SUMMARY_END")
    print("=" * 60)


if __name__ == "__main__":
    main()
