#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖图转学习路径方案分析工具
Read-Only Audit Tool - 仅用于分析和派生，不修改原始数据
"""

import json
import os
import sys
import argparse
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, Tuple

class DependencyToLearningPathAnalyzer:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.data = None
        self.sections = {}
        self.items = {}
        self.load_data()
        
    def load_data(self):
        """加载并解析主图谱数据"""
        print(f"正在加载数据: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # 解析章节和知识点 - 数据结构为 categories -> sections -> items
        for category in self.data.get('categories', []):
            for section in category.get('sections', []):
                self.sections[section['id']] = section
                
                for item in section.get('items', []):
                    # 添加类别信息到知识点
                    item['_category'] = category.get('name', '')
                    self.items[item['id']] = item
                
        print(f"加载完成: {len(self.sections)} 个章节, {len(self.items)} 个知识点")

    def analyze_dependency_distribution(self) -> Dict[str, Any]:
        """分析依赖数量分布"""
        print("\n=== 分析依赖数量分布 ===")
        
        direct_pre_counts = []
        resolved_pre_counts = []
        rel_counts = []
        
        for item_id, item in self.items.items():
            direct_pre_counts.append(len(item.get('direct_pre', [])))
            resolved_pre_counts.append(len(item.get('resolved_pre', [])))
            rel_counts.append(len(item.get('rel', [])))
        
        def get_distribution_stats(counts: List[int]) -> Dict[str, Any]:
            if not counts:
                return {}
            return {
                'total': len(counts),
                'zero': counts.count(0),
                'min': min(counts),
                'max': max(counts),
                'avg': sum(counts) / len(counts),
                'median': sorted(counts)[len(counts)//2] if counts else 0,
                'distribution': Counter(counts)
            }
        
        return {
            'direct_pre': get_distribution_stats(direct_pre_counts),
            'resolved_pre': get_distribution_stats(resolved_pre_counts),
            'rel': get_distribution_stats(rel_counts)
        }

    def identify_problematic_nodes(self) -> Dict[str, Any]:
        """识别问题节点"""
        print("\n=== 识别问题节点 ===")
        
        over_dense_nodes = []  # 依赖过密节点
        missing_pre_nodes = []  # 依赖缺失节点
        problematic_resolved_pre = []  # 不适合直接展示的 resolved_pre
        
        for item_id, item in self.items.items():
            direct_pre = item.get('direct_pre', [])
            resolved_pre = item.get('resolved_pre', [])
            rel = item.get('rel', [])
            
            # 依赖过密节点：resolved_pre 数量 > 10
            if len(resolved_pre) > 10:
                over_dense_nodes.append({
                    'id': item_id,
                    'name': item.get('name', ''),
                    'resolved_pre_count': len(resolved_pre),
                    'resolved_pre': resolved_pre
                })
            
            # 依赖缺失节点：没有 resolved_pre 且不是基础知识点
            if len(resolved_pre) == 0 and not item.get('level') == 'L0':
                missing_pre_nodes.append({
                    'id': item_id,
                    'name': item.get('name', ''),
                    'level': item.get('level', ''),
                    'category': item.get('category', '')
                })
            
            # 识别可能不适合直接展示的 resolved_pre
            # 1. 过于技术性的实现细节
            # 2. 跨章节的间接依赖
            # 3. 过于基础的通用知识点
            technical_terms = ['实现', '优化', '底层', '内存', '复杂度', '边界', '细节']
            for pre_id in resolved_pre:
                if pre_id in self.items:
                    pre_item = self.items[pre_id]
                    pre_name = pre_item.get('name', '')
                    
                    # 检查是否包含技术术语
                    if any(term in pre_name for term in technical_terms):
                        problematic_resolved_pre.append({
                            'item_id': item_id,
                            'item_name': item.get('name', ''),
                            'problematic_pre_id': pre_id,
                            'problematic_pre_name': pre_name,
                            'reason': '技术实现细节'
                        })
                    
                    # 检查是否跨章节的间接依赖
                    item_section = item_id.split('.')[0]
                    pre_section = pre_id.split('.')[0]
                    if item_section != pre_section and len(resolved_pre) > 5:
                        if not any(p['item_id'] == item_id and p['problematic_pre_id'] == pre_id for p in problematic_resolved_pre):
                            problematic_resolved_pre.append({
                                'item_id': item_id,
                                'item_name': item.get('name', ''),
                                'problematic_pre_id': pre_id,
                                'problematic_pre_name': pre_name,
                                'reason': '跨章节间接依赖'
                            })
        
        return {
            'over_dense_nodes': sorted(over_dense_nodes, key=lambda x: x['resolved_pre_count'], reverse=True),
            'missing_pre_nodes': missing_pre_nodes,
            'problematic_resolved_pre': problematic_resolved_pre[:50]  # 限制数量
        }

    def analyze_chapter_structure(self) -> Dict[str, Any]:
        """分析章节结构和推荐学习顺序"""
        print("\n=== 分析章节结构 ===")
        
        chapter_analysis = {}
        
        for section_id, section in self.sections.items():
            items = section.get('items', [])
            
            # 分析章节内知识点的依赖关系
            item_dependencies = {}
            for item in items:
                item_id = item['id']
                # 只保留同一章节内的前置依赖
                same_section_pre = [
                    pre_id for pre_id in item.get('resolved_pre', [])
                    if pre_id.split('.')[0] == section_id.split('.')[0]
                ]
                item_dependencies[item_id] = {
                    'name': item.get('name', ''),
                    'level': item.get('level', ''),
                    'pre_count': len(same_section_pre),
                    'dependencies': same_section_pre,
                    'resolved_pre_count': len(item.get('resolved_pre', []))
                }
            
            # 基于依赖关系构建学习顺序
            # 简单拓扑排序：前置依赖少的优先
            sorted_items = sorted(
                item_dependencies.items(),
                key=lambda x: (x[1]['pre_count'], x[1]['level'], x[0])
            )
            
            chapter_analysis[section_id] = {
                'name': section.get('name', ''),
                'total_items': len(items),
                'internal_dependencies': item_dependencies,
                'recommended_order': [item_id for item_id, _ in sorted_items],
                'complexity': 'high' if len(items) > 10 else 'medium' if len(items) > 5 else 'low'
            }
        
        return chapter_analysis

    def design_derived_fields(self) -> Dict[str, Any]:
        """设计派生字段逻辑"""
        print("\n=== 设计派生字段 ===")
        
        derived_data = {}
        
        for item_id, item in self.items.items():
            direct_pre = item.get('direct_pre', [])
            resolved_pre = item.get('resolved_pre', [])
            rel = item.get('rel', [])
            level = item.get('level', 'L1')
            
            # 1. required_pre: 必须前置 - 从 resolved_pre 中筛选核心依赖
            required_pre = []
            for pre_id in resolved_pre[:5]:  # 取前5个最重要的
                if pre_id in self.items:
                    pre_item = self.items[pre_id]
                    # 只包含不同章节的核心前置或同章节的高级前置
                    if (pre_id.split('.')[0] != item_id.split('.')[0] or 
                        pre_item.get('level') in ['L2', 'L3']):
                        required_pre.append(pre_id)
            
            # 2. recommended_pre: 推荐前置 - 从 rel 和部分 resolved_pre 中选择
            recommended_pre = []
            for rel_id in rel:
                if rel_id in self.items:
                    recommended_pre.append(rel_id)
            
            # 3. related_after: 学完继续 - 基于其他知识点依赖此知识点
            related_after = []
            for other_id, other_item in self.items.items():
                if item_id in other_item.get('resolved_pre', []):
                    # 只包含直接相关的后续知识点
                    if (other_id.split('.')[0] == item_id.split('.')[0] or 
                        len(related_after) < 3):
                        related_after.append(other_id)
            
            # 4. unlock_reason: 解锁原因
            unlock_reasons = []
            if required_pre:
                unlock_reasons.append(f"需要掌握 {len(required_pre)} 个核心前置知识点")
            if recommended_pre:
                unlock_reasons.append(f"建议了解 {len(recommended_pre)} 个相关知识点")
            if level == 'L3':
                unlock_reasons.append("高级知识点，需要扎实基础")
            elif level == 'L0':
                unlock_reasons.append("基础知识点，可直接开始学习")
            
            # 5. path_rank: 路径排序 - 基于依赖数量和难度
            dependency_score = len(resolved_pre) * 2 + len(rel)
            level_score = {'L0': 0, 'L1': 1, 'L2': 2, 'L3': 3}.get(level, 1)
            path_rank = dependency_score + level_score * 10
            
            # 6. path_role: 路径角色
            if len(related_after) > 5:
                path_role = "hub"  # 核心枢纽
            elif len(required_pre) > 5:
                path_role = "advanced"  # 高级知识点
            elif len(required_pre) == 0:
                path_role = "entry"  # 入门点
            else:
                path_role = "intermediate"  # 中间知识点
            
            derived_data[item_id] = {
                'required_pre': required_pre,
                'recommended_pre': recommended_pre[:3],  # 限制数量
                'related_after': related_after[:5],  # 限制数量
                'unlock_reason': unlock_reasons,
                'path_rank': path_rank,
                'path_role': path_role,
                'metadata': {
                    'original_direct_pre_count': len(direct_pre),
                    'original_resolved_pre_count': len(resolved_pre),
                    'original_rel_count': len(rel),
                    'level': level
                }
            }
        
        return derived_data

    def generate_sample_learning_paths(self) -> Dict[str, Dict[str, Any]]:
        """为 2.8、3.13、4.1 生成优化的样板学习路径"""
        print("\n=== 生成优化样板学习路径 ===")
        
        sample_paths = {}
        
        # 为每个指定章节生成三种路径
        target_sections = ['2.8', '3.13', '4.1']
        
        # 辅助函数：检查知识点ID是否属于指定章节
        def is_item_in_section(item_id: str, section_id: str) -> bool:
            """检查知识点是否属于指定章节"""
            item_section = item_id.split('.')[0]
            return item_section == section_id.split('.')[0]
        
        # 基础关键词 - 用于识别入门级知识点
        beginner_keywords = [
            '基础', '入门', '简介', '概述', '基本', '简单', '初步', 
            '思想', '概念', '定义', '模板', '模型', '原理', '简介',
            'DP思想', '状态设计', '状态转移', '记忆化', '线性', '背包',
            '基础', '入门', '简单', '基本', '初步', '思想', '概念',
            '定义', '模板', '模型', '原理', '线段树', '主席树', '李超',
            '动态开点', '合并', '整数', '整除', '同余', '素数', '最大公约数'
        ]
        
        # 提高关键词 - 用于识别中级知识点
        intermediate_keywords = [
            '常用', '标准', '典型', '常见', '一般', '常规', '技巧',
            '优化', '实现', '应用', '进阶', '提高', '深入', '扩展',
            '区间', '树形', '状压', '数位', '背包', '优化', '斜率',
            '常见模型', '常用技巧', '标准实现', '进阶', '提高', '应用',
            '扩展', '技巧', '优化', '实现', '倍增', '线段树', '主席树',
            '李超树', '动态开点', '合并', '整数', '整除', '同余', '素数',
            '最大公约数', '欧几里得', '快速幂', '模运算', '中国剩余'
        ]
        
        # 高级关键词 - 用于识别高级知识点
        advanced_keywords = [
            '高级', '复杂', '困难', '综合', '深入', '高阶', '拓展',
            '优化', '难题', '竞赛', '高级', '复杂', '综合', '高阶',
            '数位DP', '状压DP', '树形DP', '优化', '斜率优化', '四边形优化',
            '高级', '复杂', '综合', '高阶', '难题', '竞赛', '高级',
            '复杂', '综合', '高阶', '拓展', '高级', '困难', '优化',
            '难题', '竞赛', '高级数据结构', '复杂模型', '综合应用'
        ]
        
        for section_id in target_sections:
            if section_id not in self.sections:
                print(f"警告: 章节 {section_id} 不存在")
                continue
                
            section = self.sections[section_id]
            section_items = [item for item in section.get('items', [])]
            
            # 增强的排序函数 - 综合考虑多个因素
            def enhanced_sort_key(item):
                level_order = {'L0': 0, 'L1': 1, 'L2': 2, 'L3': 3}
                direct_pre_count = len(item.get('direct_pre', []))
                resolved_pre_count = len(item.get('resolved_pre', []))
                level = level_order.get(item.get('level', 'L1'), 1)
                name = item.get('name', '').lower()
                
                # 检查关键词匹配
                beginner_score = sum(1 for kw in beginner_keywords if kw in name)
                intermediate_score = sum(1 for kw in intermediate_keywords if kw in name)
                advanced_score = sum(1 for kw in advanced_keywords if kw in name)
                
                # 综合排序：级别 + 依赖数量 + 关键词匹配
                # 级别越低越好，依赖越少越好，入门关键词越多越好
                return (
                    level,  # 级别
                    resolved_pre_count,  # 解析前置数量
                    direct_pre_count,  # 直接前置数量  
                    -beginner_score,  # 入门关键词（越多越好，用负号）
                    intermediate_score,  # 提高关键词（越少越好）
                    advanced_score  # 高级关键词（越少越好）
                )
            
            sorted_items = sorted(section_items, key=enhanced_sort_key)
            
            # 优化的入门路径生成逻辑
            beginner_candidates = []
            for item in sorted_items:
                name = item.get('name', '').lower()
                level = item.get('level', 'L1')
                direct_pre_count = len(item.get('direct_pre', []))
                resolved_pre_count = len(item.get('resolved_pre', []))
                
                # 多条件筛选：
                # 1. 级别要求：L0-L2（放宽要求）
                # 2. 直接前置要求：相对较少（≤5个）
                # 3. 解析前置要求：适中（≤20个）
                # 4. 关键词匹配：包含入门关键词或章节内相对基础
                # 5. 特殊处理：对3.13章节，允许"基础"类知识点
                
                is_beginner_level = level in ['L0', 'L1', 'L2']
                has_few_direct_pre = direct_pre_count <= 5
                has_reasonable_resolved_pre = resolved_pre_count <= 20
                has_beginner_keyword = any(kw in name for kw in beginner_keywords)
                
                # 章节特殊处理
                if section_id == '3.13':
                    # 3.13章节：允许包含"基础"、"线段树"、"主席树"等关键词的知识点
                    section_specific_keywords = ['基础', '线段树', '主席树', '李超', '动态开点', '合并']
                    has_section_keyword = any(kw in name for kw in section_specific_keywords)
                    is_suitable = (is_beginner_level and has_few_direct_pre and 
                                 (has_beginner_keyword or has_section_keyword))
                elif section_id == '2.8':
                    # 2.8章节：重点识别DP基础内容
                    dp_keywords = ['dp', '动态规划', '思想', '状态', '记忆化', '线性', '背包']
                    has_dp_keyword = any(kw in name for kw in dp_keywords)
                    is_suitable = (is_beginner_level and has_reasonable_resolved_pre and 
                                 (has_beginner_keyword or has_dp_keyword))
                else:
                    # 其他章节使用通用规则
                    is_suitable = (is_beginner_level and has_few_direct_pre and 
                                 has_reasonable_resolved_pre)
                
                if is_suitable:
                    beginner_candidates.append(item)
            
            beginner_path = [item['id'] for item in beginner_candidates[:12]]
            
            # 优化的提高路径生成逻辑
            intermediate_candidates = []
            for item in sorted_items:
                # 确保只包含本章节内的节点
                if not is_item_in_section(item['id'], section_id):
                    continue
                    
                if item['id'] in beginner_path:
                    continue  # 跳过已选的入门路径
                    
                name = item.get('name', '').lower()
                level = item.get('level', 'L1')
                direct_pre_count = len(item.get('direct_pre', []))
                resolved_pre_count = len(item.get('resolved_pre', []))
                
                # 提高路径条件：
                # 1. 级别要求：L1-L3
                # 2. 直接前置适中：3-8个
                # 3. 解析前置适中：10-30个
                # 4. 包含提高关键词或常见模型
                # 5. 被入门路径解锁或相对独立
                
                is_intermediate_level = level in ['L1', 'L2', 'L3']
                has_moderate_direct_pre = 3 <= direct_pre_count <= 8
                has_moderate_resolved_pre = 10 <= resolved_pre_count <= 30
                has_intermediate_keyword = any(kw in name for kw in intermediate_keywords)
                
                # 检查是否被入门路径知识点解锁（仅限本章节内的）
                unlocks_beginner = any(
                    is_item_in_section(beginner_id, section_id) and  # 确保前置也是本章节内的
                    beginner_id in item.get('resolved_pre', []) 
                    for beginner_id in beginner_path
                )
                
                is_suitable = (is_intermediate_level and 
                             has_moderate_direct_pre and 
                             (has_moderate_resolved_pre or has_intermediate_keyword or unlocks_beginner))
                
                if is_suitable:
                    intermediate_candidates.append(item)
            
            intermediate_path = [item['id'] for item in intermediate_candidates[:15]]
            
            # 优化的冲刺路径生成逻辑
            advanced_candidates = []
            for item in sorted_items:
                # 确保只包含本章节内的节点
                if not is_item_in_section(item['id'], section_id):
                    continue
                    
                if item['id'] in beginner_path or item['id'] in intermediate_path:
                    continue  # 跳过已选的知识点
                    
                name = item.get('name', '').lower()
                level = item.get('level', 'L1')
                
                # 冲刺路径条件：
                # 1. 优先选择高级知识点（L2、L3）
                # 2. 包含高级关键词
                # 3. 复杂应用、优化技巧类
                # 4. 综合性强的知识点
                
                is_advanced_level = level in ['L2', 'L3']
                has_advanced_keyword = any(kw in name for kw in advanced_keywords)
                
                # 综合性判断
                complexity_keywords = ['优化', '综合', '复杂', '高级', '难题', '竞赛', '应用']
                has_complexity = any(kw in name for kw in complexity_keywords)
                
                is_suitable = is_advanced_level or has_advanced_keyword or has_complexity
                
                if is_suitable:
                    advanced_candidates.append(item)
            
            # 如果冲刺路径候选不足，补充剩余知识点（只包含本章节内的）
            if len(advanced_candidates) < 15:
                remaining_items = [
                    item for item in sorted_items 
                    if is_item_in_section(item['id'], section_id) and  # 确保只包含本章节内的节点
                       item['id'] not in beginner_path and 
                       item['id'] not in intermediate_path and
                       item['id'] not in [c['id'] for c in advanced_candidates]
                ]
                advanced_candidates.extend(remaining_items[:15-len(advanced_candidates)])
            
            advanced_path = [item['id'] for item in advanced_candidates[:15]]
            
            # 生成路径说明
            def get_path_description(path_items, path_type, section_name):
                if not path_items:
                    return f"当前筛选条件下，{section_name}没有符合条件的{path_type}知识点。"
                
                descriptions = []
                for item_id in path_items[:5]:  # 只描述前5个
                    if item_id in self.items:
                        item = self.items[item_id]
                        name = item.get('name', '')
                        level = item.get('level', '')
                        direct_count = len(item.get('direct_pre', []))
                        
                        if path_type == "入门路径":
                            if level in ['L0', 'L1']:
                                descriptions.append(f"{name} (基础级别{level}，{direct_count}个直接前置)")
                            else:
                                descriptions.append(f"{name} (中级级别{level}，但包含基础概念)")
                        elif path_type == "提高路径":
                            descriptions.append(f"{name} (级别{level}，{direct_count}个直接前置)")
                        else:
                            descriptions.append(f"{name} (高级内容，级别{level})")
                
                return f"包含{len(path_items)}个知识点: " + "; ".join(descriptions)
            
            # 生成跨章节前置路径
            def generate_cross_section_prerequisites(all_section_items, chapter_path):
                """生成跨章节前置路径，提取有价值的补基础内容"""
                cross_section_prereqs = []
                
                # 收集章节内路径节点的所有前置依赖
                all_prerequisites = set()
                for item_id in chapter_path:
                    if item_id in self.items:
                        item = self.items[item_id]
                        # 收集resolved_pre中的跨章节前置
                        for pre_id in item.get('resolved_pre', []):
                            if pre_id in self.items and not is_item_in_section(pre_id, section_id):
                                all_prerequisites.add(pre_id)
                
                # 筛选有价值的跨章节前置
                for pre_id in all_prerequisites:
                    if pre_id in self.items:
                        pre_item = self.items[pre_id]
                        pre_name = pre_item.get('name', '').lower()
                        pre_level = pre_item.get('level', 'L1')
                        
                        # 筛选条件：
                        # 1. 基础级别（L0-L2）
                        # 2. 包含基础、入门等关键词
                        # 3. 或者是被多次引用的重要节点
                        is_basic_level = pre_level in ['L0', 'L1', 'L2']
                        has_basic_keyword = any(kw in pre_name for kw in beginner_keywords)
                        
                        # 计算被引用次数
                        reference_count = sum(
                            1 for item_id in chapter_path
                            if item_id in self.items and pre_id in self.items[item_id].get('resolved_pre', [])
                        )
                        
                        is_important = reference_count >= 2  # 被至少2个节点引用
                        
                        if is_basic_level and (has_basic_keyword or is_important):
                            cross_section_prereqs.append({
                                'id': pre_id,
                                'name': pre_item.get('name', ''),
                                'level': pre_level,
                                'reference_count': reference_count,
                                'reason': '补基础/前置回顾' if has_basic_keyword else '重要前置节点'
                            })
                
                # 按引用次数和级别排序
                cross_section_prereqs.sort(key=lambda x: (-x['reference_count'], x['level']))
                return cross_section_prereqs[:8]  # 限制数量
            
            # 生成跨章节前置路径
            all_chapter_path = beginner_path + intermediate_path + advanced_path
            cross_section_prerequisites = generate_cross_section_prerequisites(section_items, all_chapter_path)
            
            sample_paths[section_id] = {
                'section_name': section.get('name', ''),
                'beginner_path': beginner_path,
                'beginner_description': get_path_description(beginner_path, "入门路径", section.get('name', '')),
                'intermediate_path': intermediate_path,
                'intermediate_description': get_path_description(intermediate_path, "提高路径", section.get('name', '')),
                'advanced_path': advanced_path,
                'advanced_description': get_path_description(advanced_path, "冲刺路径", section.get('name', '')),
                'cross_section_prerequisites': cross_section_prerequisites
            }
        
        return sample_paths

    def validate_path_correctness(self, sample_paths: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """验证路径正确性，确保章节内路径只包含本章节节点"""
        print("\n=== 验证路径正确性 ===")
        
        validation_results = {}
        
        # 辅助函数：检查知识点ID是否属于指定章节
        def is_item_in_section(item_id: str, section_id: str) -> bool:
            item_section = item_id.split('.')[0]
            return item_section == section_id.split('.')[0]
        
        for section_id, paths in sample_paths.items():
            section_name = paths.get('section_name', '')
            
            validation_result = {
                'section_id': section_id,
                'section_name': section_name,
                'chapter_path_validations': {},
                'cross_section_analysis': {}
            }
            
            # 检查入门路径
            beginner_path = paths.get('beginner_path', [])
            beginner_cross_section = []
            beginner_valid = []
            
            for item_id in beginner_path:
                if is_item_in_section(item_id, section_id):
                    beginner_valid.append(item_id)
                else:
                    beginner_cross_section.append(item_id)
            
            validation_result['chapter_path_validations']['beginner_path'] = {
                'total_count': len(beginner_path),
                'valid_count': len(beginner_valid),
                'cross_section_count': len(beginner_cross_section),
                'cross_section_items': beginner_cross_section,
                'is_valid': len(beginner_cross_section) == 0
            }
            
            # 检查提高路径
            intermediate_path = paths.get('intermediate_path', [])
            intermediate_cross_section = []
            intermediate_valid = []
            
            for item_id in intermediate_path:
                if is_item_in_section(item_id, section_id):
                    intermediate_valid.append(item_id)
                else:
                    intermediate_cross_section.append(item_id)
            
            validation_result['chapter_path_validations']['intermediate_path'] = {
                'total_count': len(intermediate_path),
                'valid_count': len(intermediate_valid),
                'cross_section_count': len(intermediate_cross_section),
                'cross_section_items': intermediate_cross_section,
                'is_valid': len(intermediate_cross_section) == 0
            }
            
            # 检查冲刺路径
            advanced_path = paths.get('advanced_path', [])
            advanced_cross_section = []
            advanced_valid = []
            
            for item_id in advanced_path:
                if is_item_in_section(item_id, section_id):
                    advanced_valid.append(item_id)
                else:
                    advanced_cross_section.append(item_id)
            
            validation_result['chapter_path_validations']['advanced_path'] = {
                'total_count': len(advanced_path),
                'valid_count': len(advanced_valid),
                'cross_section_count': len(advanced_cross_section),
                'cross_section_items': advanced_cross_section,
                'is_valid': len(advanced_cross_section) == 0
            }
            
            # 分析跨章节前置
            cross_section_prerequisites = paths.get('cross_section_prerequisites', [])
            cross_section_stats = {
                'total_count': len(cross_section_prerequisites),
                'by_section': defaultdict(int),
                'by_reason': defaultdict(int)
            }
            
            for prereq in cross_section_prerequisites:
                prereq_id = prereq.get('id', '')
                prereq_section = prereq_id.split('.')[0]
                cross_section_stats['by_section'][prereq_section] += 1
                cross_section_stats['by_reason'][prereq.get('reason', '未知')] += 1
            
            validation_result['cross_section_analysis'] = {
                'cross_section_prerequisites': cross_section_prerequisites,
                'statistics': {
                    'total_count': cross_section_stats['total_count'],
                    'by_section': dict(cross_section_stats['by_section']),
                    'by_reason': dict(cross_section_stats['by_reason'])
                }
            }
            
            # 总体验证结果
            all_paths_valid = all(
                path_data['is_valid'] 
                for path_data in validation_result['chapter_path_validations'].values()
            )
            
            validation_result['overall_valid'] = all_paths_valid
            validation_results[section_id] = validation_result
            
            # 打印验证结果
            print(f"\n{section_id} ({section_name}):")
            print(f"  入门路径: {len(beginner_valid)}/{len(beginner_path)} 有效 - [PASS]" if len(beginner_cross_section) == 0 else f"  入门路径: {len(beginner_valid)}/{len(beginner_path)} 有效 - [FAIL] 发现{len(beginner_cross_section)}个跨章节节点")
            print(f"  提高路径: {len(intermediate_valid)}/{len(intermediate_path)} 有效 - [PASS]" if len(intermediate_cross_section) == 0 else f"  提高路径: {len(intermediate_valid)}/{len(intermediate_path)} 有效 - [FAIL] 发现{len(intermediate_cross_section)}个跨章节节点")
            print(f"  冲刺路径: {len(advanced_valid)}/{len(advanced_path)} 有效 - [PASS]" if len(advanced_cross_section) == 0 else f"  冲刺路径: {len(advanced_valid)}/{len(advanced_path)} 有效 - [FAIL] 发现{len(advanced_cross_section)}个跨章节节点")
            print(f"  跨章节前置: {len(cross_section_prerequisites)}个")
            
            if len(cross_section_prerequisites) > 0:
                print(f"    按章节分布: {dict(cross_section_stats['by_section'])}")
        
        # 总体验证结果
        all_sections_valid = all(
            section_result['overall_valid'] 
            for section_result in validation_results.values()
        )
        
        validation_results['overall_valid'] = all_sections_valid
        
        if all_sections_valid:
            print(f"\n[PASS] 所有章节路径验证通过 - 无跨章节节点混入")
        else:
            print(f"\n[FAIL] 部分章节路径验证失败 - 存在跨章节节点混入")
        
        return validation_results

    def run_full_analysis(self) -> Dict[str, Any]:
        """执行完整分析"""
        print("=== 开始依赖图转学习路径方案分析 ===")
        
        # 1. 依赖数量分布分析
        dependency_distribution = self.analyze_dependency_distribution()
        
        # 2. 问题节点识别
        problematic_nodes = self.identify_problematic_nodes()
        
        # 3. 章节结构分析
        chapter_structure = self.analyze_chapter_structure()
        
        # 4. 派生字段设计
        derived_fields = self.design_derived_fields()
        
        # 5. 样板学习路径生成
        sample_paths = self.generate_sample_learning_paths()
        
        # 6. 路径正确性验证
        path_validation = self.validate_path_correctness(sample_paths)
        
        # 汇总结果
        analysis_result = {
            'metadata': {
                'analysis_date': '2026-06-16',
                'total_sections': len(self.sections),
                'total_items': len(self.items),
                'source_file': self.input_file
            },
            'dependency_distribution': dependency_distribution,
            'problematic_nodes': problematic_nodes,
            'chapter_structure': chapter_structure,
            'derived_fields': derived_fields,
            'sample_learning_paths': sample_paths,
            'path_validation': path_validation,
            'statistics': {
                'over_dense_node_count': len(problematic_nodes['over_dense_nodes']),
                'missing_pre_node_count': len(problematic_nodes['missing_pre_nodes']),
                'problematic_resolved_pre_count': len(problematic_nodes['problematic_resolved_pre']),
                'chapters_with_paths': len(sample_paths)
            }
        }
        
        return analysis_result

    def save_results(self, analysis_result: Dict[str, Any], output_dir: str):
        """保存分析结果"""
        print(f"\n=== 保存分析结果到 {output_dir} ===")
        
        # 保存完整的派生 JSON
        derived_json_path = os.path.join(output_dir, 'dependency_to_learning_path.json')
        with open(derived_json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        print(f"已保存派生数据: {derived_json_path}")
        
        # 生成简化版报告数据
        report_data = {
            'summary': {
                'total_items': analysis_result['metadata']['total_items'],
                'over_dense_node_count': analysis_result['statistics']['over_dense_node_count'],
                'missing_pre_node_count': analysis_result['statistics']['missing_pre_node_count'],
                'problematic_resolved_pre_count': analysis_result['statistics']['problematic_resolved_pre_count'],
                'chapters_with_paths': analysis_result['statistics']['chapters_with_paths']
            },
            'dependency_distribution': analysis_result['dependency_distribution'],
            'top_problematic_nodes': {
                'over_dense': analysis_result['problematic_nodes']['over_dense_nodes'][:10],
                'missing_pre': analysis_result['problematic_nodes']['missing_pre_nodes'][:10]
            },
            'sample_paths': analysis_result['sample_learning_paths']
        }
        
        report_json_path = os.path.join(output_dir, 'learning_path_report_data.json')
        with open(report_json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"已保存报告数据: {report_json_path}")

def main():
    """主函数，支持命令行参数"""
    parser = argparse.ArgumentParser(description='依赖图转学习路径方案分析工具')
    parser.add_argument('-i', '--input', type=str, 
                       default='merged_knowledge_graph_item_dependencies_refined.json',
                       help='输入JSON文件路径（默认: merged_knowledge_graph_item_dependencies_refined.json）')
    parser.add_argument('-o', '--output', type=str, 
                       default='data',
                       help='输出目录路径（默认: data）')
    
    args = parser.parse_args()
    
    # 获取脚本所在目录的父目录作为项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 构建文件路径
    input_file = os.path.join(project_root, args.input) if not os.path.isabs(args.input) else args.input
    output_dir = os.path.join(project_root, args.output) if not os.path.isabs(args.output) else args.output
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"项目根目录: {project_root}")
    print(f"输入文件: {input_file}")
    print(f"输出目录: {output_dir}")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        print(f"请确认文件路径是否正确，或使用 -i 参数指定正确的文件路径")
        sys.exit(1)
    
    try:
        # 创建分析器
        analyzer = DependencyToLearningPathAnalyzer(input_file)
        
        # 执行分析
        analysis_result = analyzer.run_full_analysis()
        
        # 保存结果
        analyzer.save_results(analysis_result, output_dir)
        
        # 打印摘要信息
        print("\n=== 分析完成摘要 ===")
        print(f"总知识点数: {analysis_result['metadata']['total_items']}")
        print(f"依赖过密节点数: {analysis_result['statistics']['over_dense_node_count']}")
        print(f"依赖缺失节点数: {analysis_result['statistics']['missing_pre_node_count']}")
        print(f"问题resolved_pre数: {analysis_result['statistics']['problematic_resolved_pre_count']}")
        print(f"生成路径章节数: {analysis_result['statistics']['chapters_with_paths']}")
        
        print("\n=== 优化后样板学习路径 ===")
        for section_id, paths in analysis_result['sample_learning_paths'].items():
            print(f"\n{section_id} ({paths['section_name']}):")
            print(f"  入门路径: {len(paths['beginner_path'])} 个知识点")
            if paths['beginner_path']:
                print(f"    示例: {', '.join(paths['beginner_path'][:3])}")
            print(f"  提高路径: {len(paths['intermediate_path'])} 个知识点")
            if paths['intermediate_path']:
                print(f"    示例: {', '.join(paths['intermediate_path'][:3])}")
            print(f"  冲刺路径: {len(paths['advanced_path'])} 个知识点")
            if paths['advanced_path']:
                print(f"    示例: {', '.join(paths['advanced_path'][:3])}")
        
        print(f"\n分析结果已保存到: {output_dir}")
        print(f"- dependency_to_learning_path.json (完整派生数据)")
        print(f"- learning_path_report_data.json (报告用简化数据)")
        
    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 分析过程中发生异常 - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()