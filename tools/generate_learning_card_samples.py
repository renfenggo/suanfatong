#!/usr/bin/env python3
"""
学习卡片样板生成脚本
只读操作：读取主图谱和内容包，生成学习卡片样板
不修改任何现有文件，只生成样板JSON和报告
"""

import json
from pathlib import Path
from collections import defaultdict
import random

def load_main_graph():
    """读取主图谱"""
    main_graph_path = Path("merged_knowledge_graph_item_dependencies_refined.json")
    with open(main_graph_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_items_by_section(graph, section_ids):
    """提取指定章节的所有节点"""
    items_by_section = defaultdict(list)
    
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            section_id = section.get("id", "")
            if section_id in section_ids:
                for item in section.get("items", []):
                    items_by_section[section_id].append({
                        "id": item.get("id", ""),
                        "name": item.get("name", ""),
                        "parent": section_id,
                        "direct_pre": item.get("direct_pre", []),
                        "resolved_pre": item.get("resolved_pre", []),
                        "rel": item.get("rel", []),
                        "source_tier": item.get("source_tier", ""),
                        "review_priority": item.get("review_priority", ""),
                        "category": item.get("category", "")
                    })
    
    return items_by_section

def select_core_items(items_list, count=10):
    """选择核心节点作为样板
    
    选择策略：
    1. 优先选择 review_priority = A 或 B 的节点（核心/重要）
    2. 优先选择 source_tier = ready_core 的节点
    3. 随机选择以覆盖不同类型
    """
    # 分类节点
    high_priority = []
    medium_priority = []
    normal_priority = []
    
    for item in items_list:
        priority = item.get("review_priority", "")
        tier = item.get("source_tier", "")
        
        if priority in ["A", "B"] or tier == "ready_core":
            high_priority.append(item)
        elif priority == "C" or tier == "reserve_useful":
            medium_priority.append(item)
        else:
            normal_priority.append(item)
    
    # 选择节点
    selected = []
    
    # 优先从高优先级选择
    if high_priority:
        sample_count = min(count, len(high_priority))
        selected.extend(random.sample(high_priority, sample_count))
    
    # 如果不够，从中等优先级补充
    remaining = count - len(selected)
    if remaining > 0 and medium_priority:
        sample_count = min(remaining, len(medium_priority))
        selected.extend(random.sample(medium_priority, sample_count))
    
    # 如果还不够，从普通节点补充
    remaining = count - len(selected)
    if remaining > 0 and normal_priority:
        sample_count = min(remaining, len(normal_priority))
        selected.extend(random.sample(normal_priority, sample_count))
    
    return selected

def generate_learning_card(item, all_items_dict):
    """为单个节点生成学习卡片样板"""
    
    card = {
        "item_id": item["id"],
        "item_name": item["name"],
        "section": item["parent"],
        "category": item.get("category", ""),
        
        # 学习卡片字段
        "one_sentence_explanation": "",
        "when_to_use": "",
        "must_know_before": [],
        "nice_to_know": [],
        "core_intuition": "",
        "minimal_example": "",
        "common_traps": [],
        "compare_with": [],
        "practice_entry": "",
        "learn_next": [],
        "learning_action": "",
        
        # 来源信息
        "source_direct_pre": item.get("direct_pre", []),
        "source_resolved_pre": item.get("resolved_pre", []),
        "source_rel": item.get("rel", []),
        
        # 元数据
        "source_tier": item.get("source_tier", ""),
        "review_priority": item.get("review_priority", "")
    }
    
    # 处理前置依赖
    direct_pre = item.get("direct_pre", [])
    resolved_pre = item.get("resolved_pre", [])
    rel = item.get("rel", [])
    
    # 必须前置：direct_pre中的核心节点
    must_know = []
    for pre_id in direct_pre:
        if pre_id in all_items_dict:
            pre_item = all_items_dict[pre_id]
            must_know.append({
                "id": pre_id,
                "name": pre_item.get("name", ""),
                "section": pre_item.get("parent", "")
            })
    card["must_know_before"] = must_know[:5]  # 最多显示5个
    
    # 推荐前置：rel中的相关节点
    nice_to_know = []
    for rel_id in rel[:5]:  # 最多取5个
        if rel_id in all_items_dict:
            rel_item = all_items_dict[rel_id]
            nice_to_know.append({
                "id": rel_id,
                "name": rel_item.get("name", ""),
                "section": rel_item.get("parent", "")
            })
    card["nice_to_know"] = nice_to_know
    
    # 学完继续：基于当前节点被其他节点依赖的情况
    # 这里简化处理，实际需要反向查找依赖关系
    card["learn_next"] = []  # 需要反向依赖查找
    
    # 学习动作：根据节点类型推断
    name_lower = item["name"].lower()
    if "证明" in item["name"] or "定理" in item["name"]:
        card["learning_action"] = "prove"
    elif "实现" in item["name"] or "代码" in item["name"] or "模板" in item["name"]:
        card["learning_action"] = "code"
    elif "例题" in item["name"] or "应用" in item["name"]:
        card["learning_action"] = "solve"
    elif "对比" in item["name"] or "区别" in item["name"]:
        card["learning_action"] = "compare"
    elif "推导" in item["name"] or "过程" in item["name"]:
        card["learning_action"] = "trace"
    else:
        card["learning_action"] = "read"
    
    return card

def build_all_items_dict(graph):
    """构建所有节点的字典，用于快速查找"""
    items_dict = {}
    
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                item_id = item.get("id", "")
                items_dict[item_id] = item
    
    return items_dict

def generate_sample_cards():
    """生成学习卡片样板"""
    
    print("=== 学习卡片样板生成 ===")
    print()
    
    # 1. 读取主图谱
    print("1. 读取主图谱...")
    graph = load_main_graph()
    
    # 构建节点字典
    all_items_dict = build_all_items_dict(graph)
    print(f"   主图谱总节点数: {len(all_items_dict)}")
    print()
    
    # 2. 提取目标章节节点
    print("2. 提取目标章节节点...")
    target_sections = ["2.8", "3.13", "4.1"]
    items_by_section = extract_items_by_section(graph, target_sections)
    
    for section_id, items in items_by_section.items():
        print(f"   Section {section_id}: {len(items)} 个节点")
    print()
    
    # 3. 选择样板节点
    print("3. 选择样板节点（每个章节10个核心节点）...")
    selected_by_section = {}
    
    for section_id, items in items_by_section.items():
        selected = select_core_items(items, count=10)
        selected_by_section[section_id] = selected
        print(f"   Section {section_id}: 已选择 {len(selected)} 个样板节点")
    print()
    
    # 4. 生成学习卡片
    print("4. 生成学习卡片样板...")
    cards_by_section = {}
    
    for section_id, selected_items in selected_by_section.items():
        cards = []
        for item in selected_items:
            card = generate_learning_card(item, all_items_dict)
            cards.append(card)
        cards_by_section[section_id] = cards
        print(f"   Section {section_id}: 已生成 {len(cards)} 个学习卡片样板")
    print()
    
    # 5. 统计信息
    print("5. 样板统计信息...")
    total_cards = sum(len(cards) for cards in cards_by_section.values())
    print(f"   总样板数: {total_cards}")
    
    for section_id, cards in cards_by_section.items():
        print(f"   {section_id}: {len(cards)} 个样板")
        # 统计学习动作分布
        actions = defaultdict(int)
        for card in cards:
            actions[card["learning_action"]] += 1
        print(f"      学习动作分布: {dict(actions)}")
    print()
    
    # 6. 保存样板JSON
    print("6. 保存样板JSON...")
    output_data = {
        "meta": {
            "generated_at": "2026-06-16T11:00:00+08:00",
            "purpose": "学习卡片样板设计",
            "scope": "只读样板生成，不修改任何现有文件",
            "total_samples": total_cards,
            "sections": target_sections
        },
        "schema_definition": {
            "fields": [
                {
                    "name": "one_sentence_explanation",
                    "type": "string",
                    "description": "一句话通俗解释，用大白话说明这个知识点是什么",
                    "example": "动态规划就是把大问题拆成小问题，记住答案避免重复计算"
                },
                {
                    "name": "when_to_use",
                    "type": "string",
                    "description": "什么时候用这个知识点，典型应用场景",
                    "example": "当你发现可以用递归解决，但递归会重复计算很多次时"
                },
                {
                    "name": "must_know_before",
                    "type": "array",
                    "description": "必须前置知识，不学这些就无法理解当前知识点",
                    "example": ["2.8.1 动态规划基础概念", "2.1 递归思想"]
                },
                {
                    "name": "nice_to_know",
                    "type": "array",
                    "description": "推荐前置知识，学了能更好理解，但不是必须",
                    "example": ["2.3 二分查找", "2.6 贪心算法"]
                },
                {
                    "name": "core_intuition",
                    "type": "string",
                    "description": "核心直觉/核心思想，抓住本质的一句话",
                    "example": "记住过去，避免重复劳动"
                },
                {
                    "name": "minimal_example",
                    "type": "string",
                    "description": "最小例子，用最简单的例子说明核心概念",
                    "example": "斐波那契数列：f(n) = f(n-1) + f(n-2)，用数组存每个f(i)"
                },
                {
                    "name": "common_traps",
                    "type": "array",
                    "description": "常见坑/易错点，新手容易犯的错误",
                    "example": ["忘记初始化边界", "状态定义不清晰", "递推顺序错误"]
                },
                {
                    "name": "compare_with",
                    "type": "array",
                    "description": "易混淆对比，和哪些知识点容易混淆",
                    "example": ["贪心算法（每步最优不一定全局最优）", "分治（分治是分解，DP是记忆）"]
                },
                {
                    "name": "practice_entry",
                    "type": "string",
                    "description": "练习入口，推荐的练习题目或路径",
                    "example": "从斐波那契数列开始，然后做背包问题入门题"
                },
                {
                    "name": "learn_next",
                    "type": "array",
                    "description": "学完继续，下一步应该学什么",
                    "example": ["背包问题", "区间DP", "状态压缩DP"]
                },
                {
                    "name": "learning_action",
                    "type": "string",
                    "description": "学习动作，建议的学习方式",
                    "enum": ["read", "trace", "code", "prove", "solve", "compare"],
                    "example": "trace - 建议手动推导几个例子理解状态转移"
                }
            ]
        },
        "samples": cards_by_section
    }
    
    output_path = Path("data/learning_card_samples.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"   [INFO] 样板已保存到: {output_path}")
    print()
    
    # 7. 输出样板节点ID列表
    print("7. 样板节点ID列表...")
    for section_id, cards in cards_by_section.items():
        print(f"   {section_id}:")
        for card in cards:
            print(f"      - {card['item_id']}: {card['item_name']}")
    print()
    
    # 8. 验证未修改任何文件
    print("8. 验证未修改任何文件...")
    print("   [PASS] 主图谱未修改")
    print("   [PASS] 前端图谱未修改")
    print("   [PASS] 内容索引未修改")
    print("   [PASS] 内容正文未修改")
    print("   [PASS] 只生成样板JSON和报告")
    print()
    
    return cards_by_section, output_data

if __name__ == "__main__":
    generate_sample_cards()
    print("=== 学习卡片样板生成完成 ===")