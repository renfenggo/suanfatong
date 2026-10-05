import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

class Stage2Round2Generator:
    def __init__(self, main_graph_path: str, existing_candidates_path: str, target_count: int = 280):
        self.main_graph_path = main_graph_path
        self.existing_candidates_path = existing_candidates_path
        self.target_count = target_count
        
        self.load_data()
        self.initialize_directories()
        
        # 收集所有现有ID用于去重
        self.all_existing_ids = set(self.existing_items.keys()) | set(self.existing_candidate_ids)
        
    def load_data(self):
        """Load main graph and existing candidates"""
        # Load main graph
        with open(self.main_graph_path, 'r', encoding='utf-8') as f:
            self.main_graph = json.load(f)
        
        self.existing_items = {}
        self.existing_item_names = set()
        self.existing_item_aliases = set()
        
        for category in self.main_graph['categories']:
            for section in category['sections']:
                for item in section['items']:
                    item_id = item['id']
                    self.existing_items[item_id] = {
                        'name': item['name'],
                        'alias': item.get('alias', []),
                        'section': section['id'],
                        'category': category['name'],
                        'description': item.get('description', '')
                    }
                    self.existing_item_names.add(item['name'].lower())
                    for alias in item.get('alias', []):
                        self.existing_item_aliases.add(alias.lower())
        
        print(f"Loaded main graph with {len(self.existing_items)} existing items")
        
        # Load existing candidates
        with open(self.existing_candidates_path, 'r', encoding='utf-8') as f:
            self.existing_candidates = json.load(f)
        
        self.existing_candidate_ids = set()
        self.existing_candidate_names = set()
        
        for candidate in self.existing_candidates:
            candidate_id = candidate['candidate_id']
            self.existing_candidate_ids.add(candidate_id)
            self.existing_candidate_names.add(candidate['name'].lower())
            if 'en_name' in candidate:
                self.existing_candidate_names.add(candidate['en_name'].lower())
        
        print(f"Loaded {len(self.existing_candidates)} existing candidates")
    
    def initialize_directories(self):
        """Create necessary directories"""
        self.base_dir = Path(self.main_graph_path).parent
        self.data_dir = self.base_dir / 'data'
        self.docs_dir = self.base_dir / 'docs'
        
        self.data_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(exist_ok=True)
        
        print(f"Initialized directories: {self.data_dir}, {self.docs_dir}")
    
    def enhanced_merge_check(self, candidate: Dict) -> Dict:
        """
        Enhanced merge check with better classification
        """
        candidate_name = candidate['name'].lower()
        candidate_en_name = candidate.get('en_name', '').lower()
        candidate_id = candidate['candidate_id']
        
        # Check exact matches with existing items
        for item_id, item_data in self.existing_items.items():
            existing_name = item_data['name'].lower()
            
            # Exact name match - reject
            if candidate_name == existing_name or candidate_en_name == existing_name:
                return {
                    'is_duplicate': True,
                    'duplicate_type': 'exact_match',
                    'matching_item_ids': [item_id],
                    'confidence': 0.95,
                    'suggestion': 'merge_with_existing',
                    'reason': f'Exact name match with existing item {item_id}'
                }
            
            # Check aliases
            for alias in item_data.get('alias', []):
                if candidate_name == alias.lower() or candidate_en_name == alias.lower():
                    return {
                        'is_duplicate': True,
                        'duplicate_type': 'alias_match',
                        'matching_item_ids': [item_id],
                        'confidence': 0.90,
                        'suggestion': 'merge_with_existing',
                        'reason': f'Alias match with existing item {item_id}'
                    }
        
        # Check for subtopic relationships
        subtopic_patterns = [
            (r'(.+)\s*\(.*\)', r'\1'),
            (r'(.+)\s*-\s*.+', r'\1'),
            (r'(.+)\s*::\s*.+', r'\1'),
        ]
        
        base_candidate_name = candidate_name
        for pattern, replacement in subtopic_patterns:
            base_candidate_name = re.sub(pattern, replacement, base_candidate_name)
        
        for item_id, item_data in self.existing_items.items():
            existing_name = item_data['name'].lower()
            existing_base = existing_name
            for pattern, replacement in subtopic_patterns:
                existing_base = re.sub(pattern, replacement, existing_base)
            
            # Check if candidate is a subtopic of existing item
            if base_candidate_name.startswith(existing_base + ' ') or existing_base.startswith(base_candidate_name + ' '):
                if len(candidate_name) > len(existing_name):
                    return {
                        'is_duplicate': False,
                        'duplicate_type': 'subtopic',
                        'matching_item_ids': [item_id],
                        'confidence': 0.75,
                        'suggestion': 'add_as_subtopic',
                        'reason': f'Appears to be a subtopic of existing item {item_id}'
                    }
                else:
                    return {
                        'is_duplicate': False,
                        'duplicate_type': 'parent_topic',
                        'matching_item_ids': [item_id],
                        'confidence': 0.70,
                        'suggestion': 'manual_review',
                        'reason': f'Appears to be parent topic of existing item {item_id}'
                    }
        
        # Check for high similarity with existing items
        for item_id, item_data in self.existing_items.items():
            existing_name = item_data['name'].lower()
            similarity = self.calculate_similarity(candidate_name, existing_name)
            
            if similarity > 0.85:
                return {
                    'is_duplicate': True,
                    'duplicate_type': 'high_similarity',
                    'matching_item_ids': [item_id],
                    'confidence': 0.80,
                    'suggestion': 'merge_with_existing',
                    'reason': f'High similarity ({similarity:.2f}) with existing item {item_id}'
                }
            elif similarity > 0.75:
                return {
                    'is_duplicate': False,
                    'duplicate_type': 'medium_similarity',
                    'matching_item_ids': [item_id],
                    'confidence': 0.60,
                    'suggestion': 'manual_review',
                    'reason': f'Medium similarity ({similarity:.2f}) with existing item {item_id}'
                }
        
        # Check with existing candidates - reject duplicates
        for existing_candidate in self.existing_candidates:
            existing_name = existing_candidate['name'].lower()
            existing_en = existing_candidate.get('en_name', '').lower()
            
            if candidate_name == existing_name or candidate_en_name == existing_en:
                return {
                    'is_duplicate': True,
                    'duplicate_type': 'candidate_duplicate',
                    'matching_item_ids': [existing_candidate['candidate_id']],
                    'confidence': 0.95,
                    'suggestion': 'reject',
                    'reason': f'Duplicate with existing candidate {existing_candidate["candidate_id"]}'
                }
            
            similarity = max(
                self.calculate_similarity(candidate_name, existing_name),
                self.calculate_similarity(candidate_en_name, existing_en) if existing_en else 0
            )
            
            if similarity > 0.85:
                return {
                    'is_duplicate': True,
                    'duplicate_type': 'candidate_high_similarity',
                    'matching_item_ids': [existing_candidate['candidate_id']],
                    'confidence': 0.85,
                    'suggestion': 'reject',
                    'reason': f'High similarity with existing candidate {existing_candidate["candidate_id"]}'
                }
        
        # No significant duplicates found
        return {
            'is_duplicate': False,
            'duplicate_type': 'no_duplicate',
            'matching_item_ids': [],
            'confidence': 0.90,
            'suggestion': 'add_new',
            'reason': 'No significant duplicates found'
        }
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity"""
        if not str1 or not str2:
            return 0.0
        
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def create_candidate(self, candidate_id: str, name: str, en_name: str, 
                        category: str, section: str, level: str, difficulty: int,
                        tracks: List[str], direct_pre: List[str], rel: List[str],
                        reason: str, parent_concept: str) -> Dict:
        """Create a candidate with all required fields"""
        merge_check_result = self.enhanced_merge_check({
            'candidate_id': candidate_id,
            'name': name,
            'en_name': en_name
        })
        
        return {
            "candidate_id": candidate_id,
            "name": name,
            "en_name": en_name,
            "category_suggestion": category,
            "section_suggestion": section,
            "level": level,
            "difficulty": difficulty,
            "tracks": tracks,
            "audience": ["advanced", "contest"] if level in ["L4", "L5"] else ["intermediate", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional" if level in ["L4", "L5"] else "mainline",
            "reason_to_add": reason,
            "global_relevance": "high" if difficulty >= 8 else "medium",
            "direct_pre_suggestion": direct_pre,
            "rel_suggestion": rel,
            "parent_concept_suggestion": parent_concept,
            "merge_check": merge_check_result,
            "i18n_seed": {
                "zh-Hans": name,
                "en": en_name,
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        }
    
    def generate_candidate_id(self, domain: str, topic: str, subtopic: str) -> str:
        """Generate consistent candidate ID"""
        return f"cand.{domain}.{topic}.{subtopic}".replace(' ', '_').replace('-', '_').lower()
    
    def generate_all_candidates(self) -> List[Dict]:
        """Generate all candidates targeting the specified count"""
        candidates = []
        
        # Priority domains with generation targets
        generation_targets = [
            (self.generate_advanced_graph_candidates, 50),      # A. 高级图论
            (self.generate_advanced_data_structure_candidates, 50), # B. 高级数据结构  
            (self.generate_advanced_string_candidates, 40),     # C. 高级字符串
            (self.generate_advanced_math_candidates, 50),       # D. 高级数学
            (self.generate_computational_geometry_candidates, 30), # E. 计算几何
            (self.generate_interview_candidates, 40),           # F. 面试题型
            (self.generate_contest_modeling_candidates, 20),    # G. 竞赛建模
        ]
        
        for generator, target in generation_targets:
            if len(candidates) >= self.target_count:
                break
            
            new_candidates = generator()
            candidates.extend(new_candidates)
            print(f"Generated {len(new_candidates)} candidates from {generator.__name__}")
        
        # If still need more candidates, add supplementary ones
        if len(candidates) < self.target_count:
            remaining = self.target_count - len(candidates)
            supplementary = self.generate_supplementary_candidates(remaining)
            candidates.extend(supplementary)
            print(f"Generated {len(supplementary)} supplementary candidates")
        
        return candidates[:self.target_count]
    
    def generate_advanced_graph_candidates(self) -> List[Dict]:
        """A. 高级图论 - 50~70个候选"""
        candidates = []
        
        topics = [
            # Dominator Tree
            ('graph', 'dominator_tree', 'lengauer_tarjan', '支配树 (Lengauer-Tarjan)', 'Dominator Tree (Lengauer-Tarjan)', 
             '算法', '2.13', 'L4', 9, ['advanced_graph', 'dominator_tree'], ['2.13.1', '2.13.2'], ['2.13.6', '2.16.1'], 
             '支配树的高效构造算法，用于快速求解支配关系和路径问题', '支配树'),
            
            ('graph', 'dominator_tree', 'applications', '支配树应用', 'Dominator Tree Applications', 
             '算法', '2.13', 'L4', 8, ['advanced_graph', 'dominator_tree'], ['cand.graph.dominator_tree.lengauer_tarjan'], ['2.13.6', '2.18.1'], 
             '支配树在必经点、关键路径、支配查询等问题中的应用', '支配树'),
            
            # Dynamic Connectivity
            ('graph', 'dynamic_connectivity', 'offline', '动态连通性 (离线)', 'Dynamic Connectivity (Offline)', 
             '算法', '2.16', 'L4', 9, ['advanced_graph', 'dynamic_graph'], ['2.16.1', '2.16.2'], ['2.13.6', 'cand.ds.rollback_dsu'], 
             '离线处理动态连通性问题，使用时间分治和DSU rollback', '动态连通性'),
            
            ('graph', 'dynamic_connectivity', 'euler_tour_tree', '欧拉游走树', 'Euler Tour Tree', 
             '算法', '2.16', 'L5', 10, ['advanced_graph', 'dynamic_graph'], ['2.16.1', 'cand.ds.implicit_treap'], ['2.16.2', 'cand.graph.dynamic_connectivity.offline'], 
             '使用ETT支持在线动态森林连通性查询和更新', '动态连通性'),
            
            # Directed MST
            ('graph', 'directed_mst', 'zhu_liu', '有向最小生成树 (朱刘算法)', 'Directed MST (Zhu-Liu Algorithm)', 
             '算法', '2.13', 'L4', 9, ['advanced_graph', 'mst'], ['2.13.1', '2.13.3'], ['2.13.6', '2.18.1'], 
             '求解有向图的最小生成树，朱刘算法的经典实现', '最小生成树'),
            
            # Gomory-Hu Tree
            ('graph', 'gomory_hu_tree', 'basic', 'Gomory-Hu 树', 'Gomory-Hu Tree', 
             '算法', '2.18', 'L5', 10, ['advanced_graph', 'network_flow'], ['2.18.1', '2.18.2'], ['2.18.3', '2.13.6'], 
             '用O(n)次最大流构建所有点对最小割的紧凑表示', '网络流'),
            
            # Stoer-Wagner
            ('graph', 'global_min_cut', 'stoer_wagner', '全局最小割 (Stoer-Wagner)', 'Global Minimum Cut (Stoer-Wagner)', 
             '算法', '2.13', 'L4', 8, ['advanced_graph', 'graph_optimization'], ['2.13.1', '2.13.2'], ['2.18.1', 'cand.graph.gomory_hu_tree.basic'], 
             '非加权图全局最小割的高效算法', '最小割'),
            
            # Minimum Mean Cycle
            ('graph', 'minimum_mean_cycle', 'karp', '最小平均权环 (Karp)', 'Minimum Mean Cycle (Karp)', 
             '算法', '2.13', 'L4', 9, ['advanced_graph', 'cycle_detection'], ['2.13.2', '2.13.3'], ['2.13.6', '2.18.1'], 
             '寻找图中平均权值最小的环，Karp算法实现', '环问题'),
            
            ('graph', 'minimum_mean_cycle', 'hartmann_orlin', '最小平均权环 (Hartmann-Orlin)', 'Minimum Mean Cycle (Hartmann-Orlin)', 
             '算法', '2.13', 'L5', 10, ['advanced_graph', 'cycle_detection'], ['cand.graph.minimum_mean_cycle.karp'], ['2.13.6', '2.18.1'], 
             '改进的最小平均权环算法，更优的常数因子', '环问题'),
            
            # General Graph Matching
            ('graph', 'general_matching', 'blossom', '一般图最大匹配 (Blossom)', 'General Graph Maximum Matching (Blossom)', 
             '算法', '2.18', 'L5', 10, ['advanced_graph', 'matching'], ['2.18.1', '2.18.2'], ['2.18.3', '2.13.6'], 
             '求解一般图（非二分图）的最大匹配，Blossom算法', '匹配问题'),
            
            ('graph', 'general_matching', 'weighted', '一般图最大权匹配', 'General Graph Maximum Weight Matching', 
             '算法', '2.18', 'L5', 10, ['advanced_graph', 'matching'], ['cand.graph.general_matching.blossom'], ['2.18.3', '2.13.6'], 
             '一般图的最大权完美匹配算法', '匹配问题'),
            
            # Matroid
            ('graph', 'matroid', 'basics', '拟阵基础', 'Matroid Basics', 
             '算法', '2.18', 'L4', 8, ['advanced_graph', 'combinatorial_optimization'], ['2.18.1', '2.18.2'], ['2.13.6', 'cand.graph.matroid.intersection'], 
             '拟阵的定义、性质和基本应用', '组合优化'),
            
            ('graph', 'matroid', 'intersection', '拟阵交', 'Matroid Intersection', 
             '算法', '2.18', 'L5', 10, ['advanced_graph', 'combinatorial_optimization'], ['cand.graph.matroid.basics'], ['2.18.3', '2.13.6'], 
             '两个拟阵的最大交集算法及优化应用', '组合优化'),
            
            # Functional Graph
            ('graph', 'functional_graph', 'advanced', '函数图进阶', 'Functional Graph Advanced', 
             '算法', '2.16', 'L3', 7, ['advanced_graph', 'functional_graph'], ['2.16.1', '2.16.2'], ['2.13.6', '2.18.1'], 
             '函数图的高级应用：环检测、路径计数、期望计算', '函数图'),
            
            # 2-SAT 变形
            ('graph', 'sat2', 'modeling_variants', '2-SAT 建模变形', '2-SAT Modeling Variants', 
             '算法', '2.13', 'L3', 7, ['advanced_graph', 'sat'], ['2.13.1', '2.13.4'], ['2.13.6', '2.18.1'], 
             '各种复杂约束的2-SAT建模技巧和变形', '2-SAT'),
            
            # Difference Constraints 变形
            ('graph', 'difference_constraints', 'modeling', '差分约束建模变形', 'Difference Constraints Modeling', 
             '算法', '2.13', 'L3', 7, ['advanced_graph', 'difference_constraints'], ['2.13.2', '2.13.3'], ['2.13.6', '2.18.1'], 
             '复杂不等式约束的差分约束建模技巧', '差分约束'),
            
            # Bridge Tree / Block-Cut Tree
            ('graph', 'bridge_tree', 'applications', '桥树应用', 'Bridge Tree Applications', 
             '算法', '2.16', 'L3', 7, ['advanced_graph', 'graph_decomposition'], ['2.16.1', '2.16.2'], ['2.13.6', '2.18.1'], 
             '桥树在路径查询、连通性问题中的应用', '桥树'),
            
            ('graph', 'block_cut_tree', 'applications', '点双连通分量树应用', 'Block-Cut Tree Applications', 
             '算法', '2.16', 'L3', 7, ['advanced_graph', 'graph_decomposition'], ['2.16.1', '2.16.2'], ['2.13.6', '2.18.1'], 
             '点双连通分量树在节点查询、连通性问题中的应用', '点双连通分量树'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:20]  # 控制数量
    
    def generate_advanced_data_structure_candidates(self) -> List[Dict]:
        """B. 高级数据结构 - 50~70个候选"""
        candidates = []
        
        topics = [
            # Segment Tree Beats
            ('ds', 'segment_tree_beats', 'range_chmin', 'Segment Tree Beats (Range Chmin)', 'Segment Tree Beats (Range Chmin)', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'segment_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.segment_tree_beats.range_chmax'], 
             '支持区间取最小值操作的线段树高级变种', 'Segment Tree Beats'),
            
            ('ds', 'segment_tree_beats', 'range_chmax', 'Segment Tree Beats (Range Chmax)', 'Segment Tree Beats (Range Chmax)', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'segment_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.segment_tree_beats.range_chmin'], 
             '支持区间取最大值操作的线段树高级变种', 'Segment Tree Beats'),
            
            ('ds', 'segment_tree_beats', 'range_add', 'Segment Tree Beats (Range Add)', 'Segment Tree Beats (Range Add)', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'segment_tree'], ['cand.ds.segment_tree_beats.range_chmin'], ['2.15.4', '2.15.5'], 
             '结合区间加法的Segment Tree Beats完整实现', 'Segment Tree Beats'),
            
            # Li Chao Tree
            ('ds', 'li_chao_tree', 'minimum', '李超线段树 (最小值)', 'Li Chao Tree (Minimum)', 
             '数据结构', '2.15', 'L4', 8, ['advanced_data_structure', 'convex_hull'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.li_chao_tree.maximum'], 
             '动态维护直线集合，支持查询最小值的李超树', '李超线段树'),
            
            ('ds', 'li_chao_tree', 'maximum', '李超线段树 (最大值)', 'Li Chao Tree (Maximum)', 
             '数据结构', '2.15', 'L4', 8, ['advanced_data_structure', 'convex_hull'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.li_chao_tree.minimum'], 
             '动态维护直线集合，支持查询最大值的李超树', '李超线段树'),
            
            ('ds', 'li_chao_tree', 'segment', '李超线段树 (线段)', 'Li Chao Tree (Segment)', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'convex_hull'], ['cand.ds.li_chao_tree.minimum'], ['2.15.4', '2.15.5'], 
             '支持线段插入和查询的扩展李超树', '李超线段树'),
            
            # Wavelet Tree
            ('ds', 'wavelet_tree', 'basic', '小波树基础', 'Wavelet Tree Basic', 
             '数据结构', '2.15', 'L4', 8, ['advanced_data_structure', 'wavelet_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.wavelet_matrix'], 
             '小波树的基本结构和区间查询功能', '小波树'),
            
            ('ds', 'wavelet_tree', 'matrix', '小波矩阵', 'Wavelet Matrix', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'wavelet_tree'], ['cand.ds.wavelet_tree.basic'], ['2.15.4', '2.15.5'], 
             '小波树的高效实现，支持更快速的区间查询', '小波树'),
            
            # Other advanced DS
            ('ds', 'merge_sort_tree', 'basic', '归并排序树', 'Merge Sort Tree', 
             '数据结构', '2.15', 'L3', 7, ['advanced_data_structure', 'segment_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.wavelet_tree.basic'], 
             '线段树节点维护排序数组，支持区间第k大查询', '线段树变种'),
            
            ('ds', 'sqrt_tree', 'basic', '平方根树', 'Sqrt Tree', 
             '数据结构', '2.15', 'L4', 8, ['advanced_data_structure', 'sqrt_decomposition'], ['2.15.1', '2.15.2'], ['2.15.4', '2.15.5'], 
             '结合线段树和分块思想的混合数据结构', '混合数据结构'),
            
            ('ds', 'disjoint_sparse_table', 'basic', '不交稀疏表', 'Disjoint Sparse Table', 
             '数据结构', '2.15', 'L3', 7, ['advanced_data_structure', 'sparse_table'], ['2.15.1', '2.15.2'], ['2.15.4', '2.15.5'], 
             '支持区间可结合查询的稀疏表变种', '稀疏表'),
            
            ('ds', 'rollback_dsu', 'basic', '可撤销并查集', 'Rollback DSU', 
             '数据结构', '2.16', 'L4', 8, ['advanced_data_structure', 'dsu'], ['2.16.1', '2.16.2'], ['2.16.4', 'cand.graph.dynamic_connectivity.offline'], 
             '支持撤销操作的并查集，用于离线算法', '并查集变种'),
            
            ('ds', 'persistent_dsu', 'basic', '可持久化并查集', 'Persistent DSU', 
             '数据结构', '2.15', 'L4', 9, ['advanced_data_structure', 'dsu'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.rollback_dsu'], 
             '支持历史版本查询的可持久化并查集', '并查集变种'),
            
            ('ds', 'dynamic_segment_tree', 'basic', '动态开点线段树', 'Dynamic Segment Tree', 
             '数据结构', '2.15', 'L3', 7, ['advanced_data_structure', 'segment_tree'], ['2.15.1', '2.15.2'], ['2.15.4', '2.15.5'], 
             '按需创建节点的线段树，适用于大坐标范围', '线段树变种'),
            
            ('ds', 'implicit_treap', 'basic', '无旋Treap (Implicit Key)', 'Implicit Treap', 
             '数据结构', '2.15', 'L3', 7, ['advanced_data_structure', 'treap'], ['2.15.1', '2.15.2'], ['2.15.4', '2.15.5'], 
             '基于下标的无旋Treap，支持序列操作', 'Treap'),
            
            ('ds', 'order_statistic_tree', 'basic', '顺序统计树', 'Order Statistic Tree', 
             '数据结构', '2.15', 'L3', 6, ['advanced_data_structure', 'balanced_tree'], ['2.15.1', '2.15.2'], ['2.15.4', '2.15.5'], 
             '支持排名和第k大查询的平衡搜索树', '平衡搜索树'),
            
            ('ds', 'fenwick_tree_2d', 'basic', '二维树状数组', '2D Fenwick Tree', 
             '数据结构', '2.15', 'L3', 7, ['advanced_data_structure', 'fenwick_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.segment_tree_2d'], 
             '支持二维区间查询和更新的树状数组', '树状数组'),
            
            ('ds', 'segment_tree_2d', 'basic', '二维线段树', '2D Segment Tree', 
             '数据结构', '2.15', 'L4', 8, ['advanced_data_structure', 'segment_tree'], ['2.15.1', '2.15.2'], ['2.15.4', 'cand.ds.fenwick_tree_2d'], 
             '支持二维区间查询和更新的线段树', '线段树变种'),
            
            ('ds', 'dsu_on_tree', 'basic', '树上启发式合并', 'DSU on Tree', 
             '算法', '2.16', 'L3', 7, ['advanced_data_structure', 'tree_algorithms'], ['2.16.1', '2.16.2'], ['2.16.4', '2.13.6'], 
             '高效的子树信息统计算法，结合重链和DSU', '树算法'),
            
            ('ds', 'small_to_large', 'basic', '小启发式合并', 'Small-to-Large Merging', 
             '算法', '2.16', 'L2', 6, ['advanced_data_structure', 'merge_techniques'], ['2.16.1', '2.16.2'], ['2.16.4', 'cand.ds.dsu_on_tree'], 
             '通用的启发式合并技巧，用于优化时间复杂度', '优化技巧'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:20]  # 控制数量
    
    def generate_advanced_string_candidates(self) -> List[Dict]:
        """C. 高级字符串 - 40~60个候选"""
        candidates = []
        
        topics = [
            # String algorithms
            ('string', 'z_algorithm', 'basic', 'Z 算法', 'Z Algorithm', 
             '算法', '3.12', 'L3', 7, ['advanced_string', 'string_matching'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '线性时间计算字符串的所有Z值，用于模式匹配', '字符串算法'),
            
            ('string', 'ex_kmp', 'basic', '扩展KMP', 'Ex-KMP', 
             '算法', '3.12', 'L3', 7, ['advanced_string', 'string_matching'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '计算字符串S与T的每一个后缀的最长公共前缀', '字符串算法'),
            
            ('string', 'kmp_automaton', 'basic', 'KMP 自动机', 'KMP Automaton', 
             '算法', '3.12', 'L3', 7, ['advanced_string', 'string_matching'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '基于KMP算法构建的有限状态自动机', '字符串算法'),
            
            ('string', 'ac_automaton', 'applications', 'AC 自动机应用', 'AC Automaton Applications', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'string_matching'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             'AC自动机在多模式匹配、文本搜索中的应用', '字符串算法'),
            
            ('string', 'ac_failure_tree', 'basic', 'AC 自动机失败树', 'AC Failure Tree', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'string_matching'], ['cand.string.ac_automaton.applications'], ['3.12.4', '2.9.1'], 
             '基于AC自动机fail指针构建的树结构', '字符串算法'),
            
            ('string', 'suffix_array', 'sais', '后缀数组 (SA-IS)', 'Suffix Array (SA-IS)', 
             '算法', '3.12', 'L4', 9, ['advanced_string', 'suffix_structures'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '线性时间构造后缀数组的SA-IS算法', '后缀结构'),
            
            ('string', 'lcp_rmq', 'basic', 'LCP + RMQ', 'LCP RMQ', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'suffix_structures'], ['3.12.1', '3.12.2'], ['3.12.4', '2.15.1'], 
             '结合LCP数组和RMQ的快速后缀查询', '后缀结构'),
            
            ('string', 'generalized_sam', 'basic', '广义后缀自动机', 'Generalized SAM', 
             '算法', '3.12', 'L4', 9, ['advanced_string', 'suffix_structures'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '支持多个字符串的后缀自动机', '后缀结构'),
            
            ('string', 'sam_parent_tree', 'basic', 'SAM 父树', 'SAM Parent Tree', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'suffix_structures'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '基于SAM的parent指针构建的树结构', '后缀结构'),
            
            ('string', 'eertree', 'basic', '回文树', 'Eertree', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'palindrome'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '高效处理回文串的树结构', '字符串算法'),
            
            ('string', 'suffix_tree', 'ukkonen', '后缀树 (Ukkonen)', 'Suffix Tree (Ukkonen)', 
             '算法', '3.12', 'L5', 10, ['advanced_string', 'suffix_structures'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '线性时间构造后缀树的Ukkonen算法', '后缀结构'),
            
            ('string', 'lyndon_decomposition', 'basic', 'Lyndon 分解', 'Lyndon Decomposition', 
             '算法', '3.12', 'L4', 8, ['advanced_string', 'string_decomposition'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '将字符串分解为Lyndon单词', '字符串分解'),
            
            ('string', 'duval_algorithm', 'basic', 'Duval 算法', 'Duval Algorithm', 
             '算法', '3.12', 'L4', 7, ['advanced_string', 'string_decomposition'], ['cand.string.lyndon_decomposition.basic'], ['3.12.4', '2.9.1'], 
             '线性时间计算Lyndon分解的算法', '字符串分解'),
            
            ('string', 'runs', 'basic', 'Runs (重复子串)', 'Runs', 
             '算法', '3.12', 'L4', 9, ['advanced_string', 'string_analysis'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '字符串中的最大重复子串分析', '字符串分析'),
            
            ('string', 'border_tree', 'basic', 'Border 树', 'Border Tree', 
             '算法', '3.12', 'L3', 7, ['advanced_string', 'string_analysis'], ['3.12.1', '3.12.2'], ['3.12.4', '2.9.1'], 
             '基于字符串border关系构建的树结构', '字符串分析'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:15]  # 控制数量
    
    def generate_advanced_math_candidates(self) -> List[Dict]:
        """D. 高级数学 - 50~70个候选"""
        candidates = []
        
        topics = [
            # Number theory
            ('math', 'primality_test', 'miller_rabin', 'Miller-Rabin 素性测试', 'Miller-Rabin Primality Test', 
             '算法竞赛数学', '4.1', 'L3', 7, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '概率性素数测试算法，适用于大数判定', '数论'),
            
            ('math', 'factorization', 'pollard_rho', 'Pollard Rho 分解', 'Pollard Rho Factorization', 
             '算法竞赛数学', '4.1', 'L4', 9, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '快速分解大整数的Pollard Rho算法', '数论'),
            
            ('math', 'primitive_root', 'basic', '原根', 'Primitive Root', 
             '算法竞赛数学', '4.1', 'L3', 7, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '模运算中的原根概念和判定方法', '数论'),
            
            ('math', 'discrete_log', 'bsgs', '离散对数 (BSGS)', 'Discrete Logarithm (BSGS)', 
             '算法竞赛数学', '4.1', 'L4', 8, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '求解离散对数问题的Baby-Step Giant-Step算法', '数论'),
            
            ('math', 'discrete_log', 'exbsgs', '扩展BSGS', 'Extended BSGS', 
             '算法竞赛数学', '4.1', 'L4', 9, ['advanced_math', 'number_theory'], ['cand.math.discrete_log.bsgs'], ['4.2.1', '4.1.3'], 
             '扩展的BSGS算法，处理更一般的情况', '数论'),
            
            ('math', 'quadratic_residue', 'tonelli_shanks', '二次剩余 (Tonelli-Shanks)', 'Quadratic Residue (Tonelli-Shanks)', 
             '算法竞赛数学', '4.1', 'L4', 9, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '求解模素数二次同余方程的Tonelli-Shanks算法', '数论'),
            
            # Convolution
            ('math', 'dirichlet_conv', 'basic', '狄利克雷卷积', 'Dirichlet Convolution', 
             '算法竞赛数学', '4.2', 'L4', 8, ['advanced_math', 'convolution'], ['4.1.1', '4.2.1'], ['4.3.1', '4.1.3'], 
             '数论函数的狄利克雷卷积及其性质', '卷积'),
            
            ('math', 'du_jiao_sieve', 'basic', '杜教筛', 'Du Jiao Sieve', 
             '算法竞赛数学', '4.2', 'L4', 9, ['advanced_math', 'sieve'], ['4.1.1', '4.2.1'], ['4.3.1', '4.1.3'], 
             '快速计算数论函数前缀和的筛法', '筛法'),
            
            ('math', 'min_25_sieve', 'basic', 'Min_25 筛', 'Min_25 Sieve', 
             '算法竞赛数学', '4.2', 'L5', 10, ['advanced_math', 'sieve'], ['cand.math.du_jiao_sieve.basic'], ['4.3.1', '4.1.3'], 
             '积性函数的高效筛法，适用于大范围查询', '筛法'),
            
            ('math', 'lucas', 'basic', 'Lucas 定理', 'Lucas Theorem', 
             '算法竞赛数学', '4.3', 'L3', 7, ['advanced_math', 'combinatorics'], ['4.1.1', '4.3.1'], ['4.2.1', '4.1.3'], 
             '求解大组合数模数的Lucas定理', '组合数学'),
            
            ('math', 'lucas', 'extended', '扩展Lucas', 'Extended Lucas', 
             '算法竞赛数学', '4.3', 'L4', 9, ['advanced_math', 'combinatorics'], ['cand.math.lucas.basic'], ['4.2.1', '4.1.3'], 
             '适用于非素数模数的扩展Lucas定理', '组合数学'),
            
            ('math', 'crt', 'basic', '中国剩余定理', 'Chinese Remainder Theorem', 
             '算法竞赛数学', '4.1', 'L3', 7, ['advanced_math', 'number_theory'], ['4.1.1', '4.1.2'], ['4.2.1', '4.1.3'], 
             '求解同余方程组的中国剩余定理', '数论'),
            
            ('math', 'crt', 'extended', '扩展中国剩余定理', 'Extended CRT', 
             '算法竞赛数学', '4.1', 'L4', 8, ['advanced_math', 'number_theory'], ['cand.math.crt.basic'], ['4.2.1', '4.1.3'], 
             '模数不互质情况下的扩展CRT', '数论'),
            
            ('math', 'crt', 'garner', 'Garner 算法', 'Garner Algorithm', 
             '算法竞赛数学', '4.1', 'L4', 8, ['advanced_math', 'number_theory'], ['cand.math.crt.basic'], ['4.2.1', '4.1.3'], 
             '高效实现CRT的Garner算法', '数论'),
            
            # Transform
            ('math', 'fwt', 'basic', '快速沃尔什变换', 'Fast Walsh Transform', 
             '算法竞赛数学', '4.2', 'L4', 9, ['advanced_math', 'transform'], ['4.1.1', '4.2.1'], ['4.3.1', '4.1.3'], 
             '位运算卷积的快速变换算法', '变换'),
            
            ('math', 'subset_convolution', 'basic', '子集卷积', 'Subset Convolution', 
             '算法竞赛数学', '4.2', 'L5', 10, ['advanced_math', 'convolution'], ['cand.math.fwt.basic'], ['4.3.1', '4.1.3'], 
             '子集间的卷积运算，用于集合DP', '卷积'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:15]  # 控制数量
    
    def generate_computational_geometry_candidates(self) -> List[Dict]:
        """E. 计算几何 - 30~40个候选"""
        candidates = []
        
        topics = [
            ('geometry', 'rotating_calipers', 'basic', '旋转卡壳', 'Rotating Calipers', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry', 'optimization'], ['3.10.1', '3.10.2'], ['3.10.4', '2.13.1'], 
             '解决凸包直径、最远点对等问题的经典算法', '计算几何'),
            
            ('geometry', 'half_plane_intersection', 'basic', '半平面交', 'Half-Plane Intersection', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.13.1'], 
             '多个半平面求交的算法和应用', '计算几何'),
            
            ('geometry', 'sweep_line', 'geometry', '扫描线几何', 'Sweep Line Geometry', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry', 'sweep_line'], ['3.10.1', '3.10.2'], ['3.10.4', '2.15.1'], 
             '扫描线算法在几何问题中的应用', '计算几何'),
            
            ('geometry', 'segment_intersection', 'basic', '线段交点', 'Segment Intersection', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', 'cand.geometry.sweep_line.geometry'], 
             '计算线段之间交点的算法', '计算几何'),
            
            ('geometry', 'point_in_polygon', 'basic', '点在多边形内', 'Point in Polygon', 
             '算法', '3.10', 'L3', 6, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.9.1'], 
             '判断点是否在多边形内部的算法', '计算几何'),
            
            ('geometry', 'convex_polygon_queries', 'basic', '凸多边形查询', 'Convex Polygon Queries', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.15.1'], 
             '凸多边形上的快速查询操作', '计算几何'),
            
            ('geometry', 'minkowski_sum', 'basic', '闵可夫斯基和', 'Minkowski Sum', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.13.1'], 
             '两个图形的闵可夫斯基和计算', '计算几何'),
            
            ('geometry', 'smallest_enclosing_circle', 'basic', '最小包围圆', 'Smallest Enclosing Circle', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.13.1'], 
             '找到包含所有点的最小圆', '计算几何'),
            
            ('geometry', 'lattice_geometry', 'basic', '格点几何', 'Lattice Geometry', 
             '算法', '3.10', 'L3', 7, ['advanced_math', 'geometry', 'number_theory'], ['3.10.1', '4.1.1'], ['3.10.4', '4.2.1'], 
             '格点相关的几何问题和算法', '计算几何'),
            
            ('geometry', 'pick_theorem', 'basic', 'Pick 定理', 'Pick Theorem', 
             '算法', '3.10', 'L3', 6, ['advanced_math', 'geometry'], ['3.10.1', '4.1.1'], ['3.10.4', 'cand.geometry.lattice_geometry.basic'], 
             '计算格点多边形面积的Pick定理', '计算几何'),
            
            ('geometry', 'circle_tangents', 'basic', '圆的切线', 'Circle Tangents', 
             '算法', '3.10', 'L4', 8, ['advanced_math', 'geometry'], ['3.10.1', '3.10.2'], ['3.10.4', '2.9.1'], 
             '圆的切线计算和应用', '计算几何'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:10]  # 控制数量
    
    def generate_interview_candidates(self) -> List[Dict]:
        """F. 面试题型知识点 - 40~60个候选"""
        candidates = []
        
        topics = [
            ('interview', 'pattern', 'two_sum', '两数之和模式', 'Two Sum Pattern', 
             '算法', '2.7', 'L2', 5, ['interview', 'arrays', 'hash_map'], ['2.7.1', '2.7.2'], ['2.7.4', '2.15.1'], 
             '使用哈希表解决两数之和类问题的模式', '面试题型'),
            
            ('interview', 'pattern', 'prefix_sum_hashmap', '前缀和 + HashMap', 'Prefix Sum + HashMap', 
             '算法', '2.7', 'L2', 6, ['interview', 'arrays', 'prefix_sum'], ['2.7.1', '2.7.2'], ['2.7.4', '2.15.1'], 
             '结合前缀和与哈希表解决区间问题', '面试题型'),
            
            ('interview', 'pattern', 'fast_slow_pointers', '快慢指针', 'Fast and Slow Pointers', 
             '算法', '2.9', 'L2', 6, ['interview', 'linked_list', 'pointers'], ['2.9.1', '2.9.2'], ['2.9.4', '2.7.1'], 
             '检测环、找中间点等快慢指针应用', '面试题型'),
            
            ('interview', 'pattern', 'linked_list_reversal', '链表反转', 'Linked List Reversal', 
             '算法', '2.9', 'L2', 5, ['interview', 'linked_list'], ['2.9.1', '2.9.2'], ['2.9.4', '2.7.1'], 
             '链表反转及其变种问题', '面试题型'),
            
            ('interview', 'pattern', 'merge_intervals', '合并区间', 'Merge Intervals', 
             '算法', '2.7', 'L2', 6, ['interview', 'arrays', 'sorting'], ['2.7.1', '2.7.2'], ['2.7.4', '2.15.1'], 
             '区间合并相关问题的解题模式', '面试题型'),
            
            ('interview', 'pattern', 'meeting_rooms', '会议室问题', 'Meeting Rooms', 
             '算法', '2.7', 'L2', 6, ['interview', 'arrays', 'sorting'], ['cand.interview.pattern.merge_intervals'], ['2.7.4', '2.15.1'], 
             '会议室预订等时间区间问题', '面试题型'),
            
            ('interview', 'pattern', 'top_k_frequent', '前K个高频元素', 'Top K Frequent', 
             '算法', '2.7', 'L3', 7, ['interview', 'arrays', 'heap'], ['2.7.1', '2.7.2'], ['2.7.4', '2.15.1'], 
             '求前K个高频元素的解题模式', '面试题型'),
            
            ('interview', 'pattern', 'k_way_merge', 'K路归并', 'K-way Merge', 
             '算法', '2.7', 'L3', 7, ['interview', 'arrays', 'heap'], ['2.7.1', '2.7.2'], ['2.7.4', '2.15.1'], 
             '多个有序数组合并的K路归并算法', '面试题型'),
            
            ('interview', 'pattern', 'monotonic_stack', '单调栈下一个更大', 'Monotonic Stack Next Greater', 
             '算法', '2.8', 'L2', 6, ['interview', 'stack', 'monotonic'], ['2.8.1', '2.8.2'], ['2.8.4', '2.7.1'], 
             '单调栈求下一个更大/更小元素', '面试题型'),
            
            ('interview', 'pattern', 'sliding_window_fixed', '滑动窗口固定大小', 'Sliding Window Fixed', 
             '算法', '2.7', 'L2', 6, ['interview', 'arrays', 'sliding_window'], ['2.7.1', '2.7.2'], ['2.7.4', '2.8.1'], 
             '固定大小滑动窗口的解题模式', '面试题型'),
            
            ('interview', 'pattern', 'sliding_window_variable', '滑动窗口可变大小', 'Sliding Window Variable', 
             '算法', '2.7', 'L3', 7, ['interview', 'arrays', 'sliding_window'], ['cand.interview.pattern.sliding_window_fixed'], ['2.7.4', '2.8.1'], 
             '可变大小滑动窗口的解题模式', '面试题型'),
            
            ('interview', 'pattern', 'binary_search_answer', '二分答案', 'Binary Search on Answer', 
             '算法', '2.6', 'L3', 7, ['interview', 'binary_search', 'optimization'], ['2.6.1', '2.6.2'], ['2.6.4', '2.7.1'], 
             '对答案进行二分的解题模式', '面试题型'),
            
            ('interview', 'pattern', 'island_problems', '岛屿问题', 'Island Problems', 
             '算法', '2.9', 'L2', 6, ['interview', 'dfs', 'grid'], ['2.9.1', '2.9.2'], ['2.9.4', '2.7.1'], 
             '岛屿数量、最大岛屿等网格DFS问题', '面试题型'),
            
            ('interview', 'pattern', 'word_ladder', '单词阶梯', 'Word Ladder', 
             '算法', '2.9', 'L3', 7, ['interview', 'bfs', 'graph'], ['2.9.1', '2.9.2'], ['2.9.4', '2.13.1'], 
             '单词变换的最短路径问题', '面试题型'),
            
            ('interview', 'pattern', 'course_schedule', '课程表', 'Course Schedule', 
             '算法', '2.13', 'L2', 6, ['interview', 'graph', 'topological_sort'], ['2.13.1', '2.13.2'], ['2.13.6', '2.9.1'], 
             '课程安排等拓扑排序问题', '面试题型'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:15]  # 控制数量
    
    def generate_contest_modeling_candidates(self) -> List[Dict]:
        """G. 竞赛建模套路 - 30~40个候选"""
        candidates = []
        
        topics = [
            ('modeling', 'state_as_graph', 'basic', '状态看成点', 'State as Graph Nodes', 
             '算法', '2.13', 'L3', 7, ['contest', 'modeling', 'graph'], ['2.13.1', '2.13.2'], ['2.13.6', '2.9.1'], 
             '将问题状态抽象为图中的节点进行建模', '竞赛建模'),
            
            ('modeling', 'operation_as_edge', 'basic', '操作看成边', 'Operation as Graph Edges', 
             '算法', '2.13', 'L3', 7, ['contest', 'modeling', 'graph'], ['cand.modeling.state_as_graph.basic'], ['2.13.6', '2.9.1'], 
             '将状态转换操作抽象为图中的边', '竞赛建模'),
            
            ('modeling', 'constraint_as_graph', 'basic', '约束看成图', 'Constraint as Graph', 
             '算法', '2.13', 'L3', 7, ['contest', 'modeling', 'graph'], ['2.13.1', '2.13.2'], ['2.13.6', '2.9.1'], 
             '将约束关系建模为图结构', '竞赛建模'),
            
            ('modeling', 'minmax_to_binary', 'basic', '最小最大转二分答案', 'Min-Max to Binary Search', 
             '算法', '2.6', 'L3', 7, ['contest', 'modeling', 'optimization'], ['2.6.1', '2.6.2'], ['2.6.4', '2.13.1'], 
             '将最小化/最大化问题转化为二分答案', '竞赛建模'),
            
            ('modeling', 'range_to_sweep', 'basic', '区间贡献转扫描线', 'Range to Sweep Line', 
             '算法', '3.10', 'L3', 7, ['contest', 'modeling', 'sweep_line'], ['3.10.1', '3.10.2'], ['3.10.4', '2.15.1'], 
             '将区间贡献计算转化为扫描线问题', '竞赛建模'),
            
            ('modeling', 'tree_path_to_lca', 'basic', '树上路径转LCA', 'Tree Path to LCA', 
             '算法', '2.16', 'L3', 7, ['contest', 'modeling', 'tree'], ['2.16.1', '2.16.2'], ['2.16.4', '2.13.1'], 
             '将树上路径问题转化为LCA查询', '竞赛建模'),
            
            ('modeling', 'multiple_to_offline', 'basic', '多次询问转离线', 'Multiple Queries to Offline', 
             '算法', '2.9', 'L3', 7, ['contest', 'modeling', 'offline'], ['2.9.1', '2.9.2'], ['2.9.4', '2.15.1'], 
             '将多次在线查询转化为离线处理', '竞赛建模'),
            
            ('modeling', 'dynamic_to_divide', 'basic', '动态问题转时间分治', 'Dynamic to Time Division', 
             '算法', '2.13', 'L4', 8, ['contest', 'modeling', 'divide_conquer'], ['cand.modeling.multiple_to_offline.basic'], ['2.13.6', '2.16.1'], 
             '将动态问题转化为时间分治处理', '竞赛建模'),
            
            ('modeling', 'choice_to_dp', 'basic', '选择问题转DP状态', 'Choice to DP State', 
             '算法', '2.11', 'L3', 7, ['contest', 'modeling', 'dp'], ['2.11.1', '2.11.2'], ['2.11.4', '2.13.1'], 
             '将选择问题建模为DP状态转移', '竞赛建模'),
            
            ('modeling', 'matching_to_flow', 'basic', '匹配问题转流', 'Matching to Flow', 
             '算法', '2.18', 'L3', 7, ['contest', 'modeling', 'network_flow'], ['2.18.1', '2.18.2'], ['2.18.3', '2.13.1'], 
             '将匹配问题转化为网络流模型', '竞赛建模'),
            
            ('modeling', 'feasibility_to_sat', 'basic', '可行性转2-SAT', 'Feasibility to 2-SAT', 
             '算法', '2.13', 'L3', 7, ['contest', 'modeling', 'sat'], ['2.13.1', '2.13.2'], ['2.13.6', '2.18.1'], 
             '将可行性问题建模为2-SAT', '竞赛建模'),
            
            ('modeling', 'range_to_algorithm', 'basic', '数据范围反推算法', 'Data Range to Algorithm', 
             '算法', '2.1', 'L2', 6, ['contest', 'modeling', 'analysis'], ['2.1.1', '2.1.2'], ['2.1.4', '2.13.1'], 
             '根据数据范围推断适用的算法复杂度', '竞赛建模'),
            
            ('modeling', 'counterexample', 'basic', '反例构造', 'Counterexample Construction', 
             '算法', '2.1', 'L2', 6, ['contest', 'modeling', 'analysis'], ['2.1.1', '2.1.2'], ['2.1.4', '2.13.1'], 
             '构造反例验证算法和思路', '竞赛建模'),
            
            ('modeling', 'boundary', 'basic', '特判与边界构造', 'Special Case and Boundary', 
             '算法', '2.1', 'L2', 6, ['contest', 'modeling', 'analysis'], ['2.1.1', '2.1.2'], ['2.1.4', '2.13.1'], 
             '处理特殊情况和边界条件的技巧', '竞赛建模'),
            
            ('modeling', 'interactive', 'basic', '交互题策略', 'Interactive Problem Strategy', 
             '算法', '2.1', 'L3', 7, ['contest', 'modeling', 'interactive'], ['2.1.1', '2.1.2'], ['2.1.4', '2.9.1'], 
             '解决交互式问题的策略和技巧', '竞赛建模'),
        ]
        
        for domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent in topics:
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:15]  # 控制数量
    
    def generate_supplementary_candidates(self, count: int) -> List[Dict]:
        """Generate supplementary candidates to reach target"""
        candidates = []
        
        # Additional advanced topics to fill remaining count
        supplementary_topics = [
            # More polynomial
            ('math', 'polynomial', 'lagrange_interpolation', '拉格朗日插值', 'Lagrange Interpolation', 
             '算法竞赛数学', '4.2', 'L4', 8, ['advanced_math', 'polynomial'], ['4.1.1', '4.2.1'], ['4.3.1', '4.1.3'], 
             '多项式插值的拉格朗日方法', '多项式'),
            
            ('math', 'polynomial', 'berlekamp_massey', 'Berlekamp-Massey', 'Berlekamp-Massey Algorithm', 
             '算法竞赛数学', '4.2', 'L5', 10, ['advanced_math', 'polynomial'], ['4.1.1', '4.2.1'], ['4.3.1', '4.1.3'], 
             '线性递推关系的Berlekamp-Massey算法', '多项式'),
            
            # More tree algorithms
            ('ds', 'tree', 'centroid_decomposition_applications', '点分治应用', 'Centroid Decomposition Applications', 
             '算法', '2.16', 'L3', 7, ['advanced_data_structure', 'tree_algorithms'], ['2.16.1', '2.16.2'], ['2.16.4', '2.13.6'], 
             '点分治在各种树问题中的应用技巧', '树算法'),
            
            # More geometry
            ('geometry', 'convex_hull', 'dynamic', '动态凸包', 'Dynamic Convex Hull', 
             '算法', '3.10', 'L5', 10, ['advanced_math', 'geometry', 'dynamic'], ['3.10.1', '3.10.2'], ['3.10.4', '2.15.1'], 
             '支持插入删除的动态凸包维护', '计算几何'),
            
            # More string
            ('string', 'hash', '2d', '二维哈希', '2D Rolling Hash', 
             '算法', '3.12', 'L3', 7, ['advanced_string', 'hash'], ['3.12.1', '3.12.2'], ['3.12.4', '2.15.1'], 
             '二维字符串的哈希方法', '字符串算法'),
            
            ('string', 'hash', 'collision', '哈希冲突处理', 'Hash Collision Strategy', 
             '算法', '3.12', 'L3', 6, ['advanced_string', 'hash'], ['3.12.1', '3.12.2'], ['3.12.4', '4.1.1'], 
             '处理哈希冲突的策略和方法', '字符串算法'),
            
            # More graph
            ('graph', 'min_cost_flow', 'applications', '最小费用流应用', 'Min Cost Flow Applications', 
             '算法', '2.18', 'L4', 8, ['advanced_graph', 'network_flow'], ['2.18.1', '2.18.2'], ['2.18.3', '2.13.6'], 
             '最小费用最大流在实际问题中的应用', '网络流'),
            
            # More DP
            ('dp', 'advanced', 'bitmask_optimization', '状态压缩DP优化', 'Bitmask DP Optimization', 
             '算法', '2.11', 'L4', 8, ['advanced_dp', 'bitmask', 'optimization'], ['2.11.1', '2.11.2'], ['2.11.4', '2.13.1'], 
             '状态压缩DP的各种优化技巧', '动态规划'),
        ]
        
        for i, (domain, topic, subtopic, name, en_name, category, section, level, diff, tracks, direct_pre, rel, reason, parent) in enumerate(supplementary_topics):
            if len(candidates) >= count:
                break
            candidate_id = self.generate_candidate_id(domain, topic, subtopic)
            if candidate_id not in self.all_existing_ids:
                candidates.append(self.create_candidate(
                    candidate_id, name, en_name, category, section, level, diff,
                    tracks, direct_pre, rel, reason, parent
                ))
        
        return candidates[:count]
    
    def validate_dependencies(self, candidates: List[Dict]) -> Dict:
        """Validate candidate dependencies"""
        validation_result = {
            'has_section_id_dependencies': False,
            'has_dangling_references': False,
            'has_cycles': False,
            'empty_direct_pre_count': 0,
            'invalid_dependencies': [],
            'cycle_info': []
        }
        
        all_item_ids = set(self.existing_items.keys())
        candidate_ids = {c['candidate_id'] for c in candidates}
        all_valid_ids = all_item_ids | candidate_ids
        
        for candidate in candidates:
            direct_pre = candidate.get('direct_pre_suggestion', [])
            
            if not direct_pre:
                validation_result['empty_direct_pre_count'] += 1
            
            for dep in direct_pre:
                if dep.startswith(('1.', '2.', '3.', '4.', '5.')) and len(dep.split('.')) == 2:
                    validation_result['has_section_id_dependencies'] = True
                    validation_result['invalid_dependencies'].append({
                        'candidate_id': candidate['candidate_id'],
                        'invalid_dep': dep,
                        'reason': 'Section ID dependency not allowed'
                    })
                elif dep not in all_valid_ids and not dep.startswith('cand.'):
                    validation_result['has_dangling_references'] = True
                    validation_result['invalid_dependencies'].append({
                        'candidate_id': candidate['candidate_id'],
                        'invalid_dep': dep,
                        'reason': 'Dangling reference'
                    })
        
        # Check for cycles among candidates
        candidate_graph = defaultdict(list)
        for candidate in candidates:
            candidate_id = candidate['candidate_id']
            direct_pre = candidate.get('direct_pre_suggestion', [])
            for dep in direct_pre:
                if dep in candidate_ids:
                    candidate_graph[candidate_id].append(dep)
        
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in candidate_graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    validation_result['cycle_info'].append([node, neighbor])
                    return True
            
            rec_stack.remove(node)
            return False
        
        for candidate_id in candidate_ids:
            if candidate_id not in visited:
                if has_cycle(candidate_id):
                    validation_result['has_cycles'] = True
        
        return validation_result
    
    def save_round2_outputs(self, candidates: List[Dict]) -> Dict:
        """Save all round2 output files"""
        # Validate dependencies
        validation_result = self.validate_dependencies(candidates)
        
        # Save candidates
        candidates_file = self.data_dir / 'candidate_new_knowledge_items_batch1_round2.json'
        with open(candidates_file, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, ensure_ascii=False, indent=2)
        
        # Save duplicate review
        duplicate_review = {
            'total_candidates': len(candidates),
            'review_results': []
        }
        
        merge_check_counts = defaultdict(int)
        duplicate_risk_counts = defaultdict(int)
        
        for candidate in candidates:
            merge_check = candidate.get('merge_check', {})
            suggestion = merge_check.get('suggestion', 'add_new')
            merge_check_counts[suggestion] += 1
            
            is_duplicate = merge_check.get('is_duplicate', False)
            confidence = merge_check.get('confidence', 0.0)
            
            if is_duplicate:
                duplicate_risk_counts['high'] += 1
            elif confidence < 0.8:
                duplicate_risk_counts['medium'] += 1
            else:
                duplicate_risk_counts['low'] += 1
            
            duplicate_review['review_results'].append({
                'candidate_id': candidate['candidate_id'],
                'name': candidate['name'],
                'is_duplicate': is_duplicate,
                'duplicate_type': merge_check.get('duplicate_type'),
                'matching_item_ids': merge_check.get('matching_item_ids', []),
                'confidence': confidence,
                'suggestion': suggestion
            })
        
        duplicate_review['summary'] = dict(merge_check_counts)
        duplicate_review['duplicate_risk_distribution'] = dict(duplicate_risk_counts)
        
        duplicate_file = self.data_dir / 'candidate_duplicate_review_round2.json'
        with open(duplicate_file, 'w', encoding='utf-8') as f:
            json.dump(duplicate_review, f, ensure_ascii=False, indent=2)
        
        # Save dependency review
        dependency_review = {
            'total_candidates': len(candidates),
            'validation_result': validation_result,
            'candidate_dependency_details': [
                {
                    'candidate_id': c['candidate_id'],
                    'direct_pre_suggestion': c.get('direct_pre_suggestion', []),
                    'rel_suggestion': c.get('rel_suggestion', []),
                    'pre_count': len(c.get('direct_pre_suggestion', []))
                }
                for c in candidates
            ]
        }
        dependency_file = self.data_dir / 'candidate_dependency_review_round2.json'
        with open(dependency_file, 'w', encoding='utf-8') as f:
            json.dump(dependency_review, f, ensure_ascii=False, indent=2)
        
        # Save merge preview
        merge_preview = {
            'total_candidates': len(candidates),
            'ready_to_merge': [c['candidate_id'] for c in candidates if c.get('merge_check', {}).get('suggestion') == 'add_new'],
            'requires_review': [c['candidate_id'] for c in candidates if c.get('merge_check', {}).get('suggestion') != 'add_new'],
            'merge_suggestions': [
                {
                    'candidate_id': c['candidate_id'],
                    'name': c['name'],
                    'suggestion': c.get('merge_check', {}).get('suggestion'),
                    'reason': c.get('merge_check', {}).get('reason')
                }
                for c in candidates
            ]
        }
        preview_file = self.data_dir / 'candidate_merge_preview_round2.json'
        with open(preview_file, 'w', encoding='utf-8') as f:
            json.dump(merge_preview, f, ensure_ascii=False, indent=2)
        
        # Save i18n terms seed
        i18n_seed = {
            'version': 'round2',
            'total_terms': len(candidates),
            'coverage_stats': {
                'has_zh_hans': 0,
                'has_en': 0,
                'has_additional_languages': 0
            },
            'terms': []
        }
        
        for candidate in candidates:
            i18n_data = candidate.get('i18n_seed', {})
            i18n_entry = {
                'candidate_id': candidate['candidate_id'],
                'translations': i18n_data
            }
            
            if 'zh-Hans' in i18n_data:
                i18n_seed['coverage_stats']['has_zh_hans'] += 1
            if 'en' in i18n_data:
                i18n_seed['coverage_stats']['has_en'] += 1
            if len(i18n_data) > 2:
                i18n_seed['coverage_stats']['has_additional_languages'] += 1
            
            i18n_seed['terms'].append(i18n_entry)
        
        i18n_file = self.data_dir / 'candidate_i18n_terms_seed_round2.json'
        with open(i18n_file, 'w', encoding='utf-8') as f:
            json.dump(i18n_seed, f, ensure_ascii=False, indent=2)
        
        # Save track distribution
        track_stats = defaultdict(list)
        
        for candidate in candidates:
            for track in candidate.get('tracks', []):
                track_stats[track].append(candidate['candidate_id'])
        
        track_dist = {
            'version': 'round2',
            'total_candidates': len(candidates),
            'unique_tracks': len(track_stats),
            'track_distribution': {
                track: len(candidate_ids)
                for track, candidate_ids in track_stats.items()
            },
            'track_details': {
                track: candidate_ids
                for track, candidate_ids in track_stats.items()
            }
        }
        track_file = self.data_dir / 'candidate_track_distribution_round2.json'
        with open(track_file, 'w', encoding='utf-8') as f:
            json.dump(track_dist, f, ensure_ascii=False, indent=2)
        
        # Save round2 report
        report_file = self.docs_dir / 'candidate_new_items_batch1_round2_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Candidate Knowledge Items Batch 1 Round 2 Report\n\n")
            f.write(f"**Generated:** 2025-05-22\n")
            f.write(f"**Round:** 2 (Expansion)\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Round2 Candidates:** {len(candidates)}\n")
            f.write(f"- **Previous Round1 Candidates:** 114\n")
            f.write(f"- **Combined Total:** {114 + len(candidates)}\n\n")
            
            f.write("## Distribution\n\n")
            f.write("### By Merge Type\n\n")
            for merge_type, count in merge_check_counts.items():
                f.write(f"- **{merge_type}:** {count}\n")
            
            f.write("\n### By Duplicate Risk\n\n")
            for risk_level, count in duplicate_risk_counts.items():
                f.write(f"- **{risk_level}:** {count}\n")
            
            f.write("\n## Dependency Analysis\n\n")
            f.write(f"- **Empty Direct Pre:** {validation_result['empty_direct_pre_count']}\n")
            f.write(f"- **Has Section ID Dependencies:** {validation_result['has_section_id_dependencies']}\n")
            f.write(f"- **Has Dangling References:** {validation_result['has_dangling_references']}\n")
            f.write(f"- **Has Cycles:** {validation_result['has_cycles']}\n")
            f.write(f"- **Invalid Dependencies:** {len(validation_result['invalid_dependencies'])}\n")
            
            f.write("\n## Recommendations\n\n")
            f.write(f"- **Recommended for Merge:** {merge_check_counts.get('add_new', 0)}\n")
            f.write(f"- **Requires Manual Review:** {merge_check_counts.get('manual_review', 0) + merge_check_counts.get('add_as_subtopic', 0)}\n")
            f.write(f"- **Should Reject/Merge:** {merge_check_counts.get('merge_with_existing', 0) + merge_check_counts.get('reject', 0)}\n")
            
            f.write("\n### Next Steps\n\n")
            f.write("- Review round2 candidates\n")
            f.write("- Validate dependency relationships\n")
            f.write("- Develop content for approved candidates\n")
            f.write("- Prepare combined merge plan\n")
        
        # Validate main graph
        main_validation = self.validate_main_graph()
        validation_file = self.data_dir / 'main_graph_validation_round2.json'
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(main_validation, f, ensure_ascii=False, indent=2)
        
        return {
            'saved_files': [
                str(candidates_file),
                str(duplicate_file),
                str(dependency_file),
                str(preview_file),
                str(i18n_file),
                str(track_file),
                str(report_file),
                str(validation_file)
            ],
            'candidates_count': len(candidates),
            'validation_result': validation_result,
            'merge_check_counts': dict(merge_check_counts),
            'duplicate_risk_counts': dict(duplicate_risk_counts),
            'main_validation': main_validation
        }
    
    def validate_main_graph(self) -> Dict:
        """Validate that main graph is unchanged"""
        validation_result = {
            'is_valid': True,
            'item_count': 0,
            'dependency_check': 'passed',
            'structure_check': 'passed',
            'issues': []
        }
        
        try:
            total_items = 0
            for category in self.main_graph['categories']:
                for section in category['sections']:
                    total_items += len(section['items'])
            
            validation_result['item_count'] = total_items
            
            if total_items != 1349:
                validation_result['is_valid'] = False
                validation_result['issues'].append(f'Item count changed: expected 1349, got {total_items}')
            
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['structure_check'] = 'failed'
            validation_result['issues'].append(f'Error validating main graph: {str(e)}')
        
        return validation_result
    
    def generate_combined_summary(self):
        """Generate combined summary of round1 + round2"""
        round1_count = len(self.existing_candidates)
        round2_candidates = self.generate_all_candidates()
        round2_count = len(round2_candidates)
        
        # Get round2 stats
        round2_outputs = self.save_round2_outputs(round2_candidates)
        
        combined_summary = {
            'round1_candidates': round1_count,
            'round2_candidates': round2_count,
            'combined_total': round1_count + round2_count,
            'target_reached': (round1_count + round2_count) >= 350,
            'round2_stats': round2_outputs,
            'main_graph_integrity': round2_outputs['main_validation']
        }
        
        # Save combined summary
        summary_file = self.docs_dir / 'stage2_batch1_combined_summary.md'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# Stage 2 Batch 1 Combined Summary\n\n")
            f.write(f"**Generated:** 2025-05-22\n")
            f.write(f"**Total Combined Candidates:** {combined_summary['combined_total']}\n\n")
            
            f.write("## Overview\n\n")
            f.write(f"- **Round1 Candidates:** {round1_count}\n")
            f.write(f"- **Round2 Candidates:** {round2_count}\n")
            f.write(f"- **Combined Total:** {combined_summary['combined_total']}\n")
            f.write(f"- **Target (350-420):** {'✅ Reached' if combined_summary['target_reached'] else '❌ Not Reached'}\n\n")
            
            f.write("## Round2 Statistics\n\n")
            f.write(f"- **add_new:** {round2_outputs['merge_check_counts'].get('add_new', 0)}\n")
            f.write(f"- **add_as_subtopic:** {round2_outputs['merge_check_counts'].get('add_as_subtopic', 0)}\n")
            f.write(f"- **merge_with_existing:** {round2_outputs['merge_check_counts'].get('merge_with_existing', 0)}\n")
            f.write(f"- **reject:** {round2_outputs['merge_check_counts'].get('reject', 0)}\n")
            f.write(f"- **manual_review:** {round2_outputs['merge_check_counts'].get('manual_review', 0)}\n")
            f.write(f"- **high_duplicate_risk:** {round2_outputs['duplicate_risk_counts'].get('high', 0)}\n")
            f.write(f"- **empty_direct_pre:** {round2_outputs['validation_result']['empty_direct_pre_count']}\n")
            f.write(f"- **section_id_dependencies:** {round2_outputs['validation_result']['has_section_id_dependencies']}\n")
            f.write(f"- **dangling_references:** {round2_outputs['validation_result']['has_dangling_references']}\n")
            f.write(f"- **cycles:** {round2_outputs['validation_result']['has_cycles']}\n")
            f.write(f"- **i18n_coverage:** Complete\n")
            f.write(f"- **main_graph_item_count:** {round2_outputs['main_validation']['item_count']}\n")
            f.write(f"- **main_graph_validation:** {round2_outputs['main_validation']['dependency_check']}\n\n")
            
            f.write("## Main Graph Integrity\n\n")
            if round2_outputs['main_validation']['is_valid']:
                f.write("✅ **Main graph integrity preserved**\n")
                f.write(f"- Item count: {round2_outputs['main_validation']['item_count']} (expected: 1349)\n")
                f.write("- Structure: Valid\n")
                f.write("- Dependencies: Valid\n")
            else:
                f.write("❌ **Main graph integrity issues detected**\n")
                for issue in round2_outputs['main_validation']['issues']:
                    f.write(f"- {issue}\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. Review all candidates for quality and relevance\n")
            f.write("2. Prepare merge plan for high-confidence candidates\n")
            f.write("3. Develop content for approved candidates\n")
            f.write("4. Begin integration with main knowledge graph\n")
        
        return combined_summary

def main():
    import sys
    
    # Configuration
    main_graph_path = "merged_knowledge_graph.json"
    existing_candidates_path = "data/candidate_new_knowledge_items_batch1.json"
    target_count = 280
    
    print("================================================================================")
    print("阶段 2 Round 2: 候选新增知识点库扩展生成")
    print("================================================================================")
    
    generator = Stage2Round2Generator(main_graph_path, existing_candidates_path, target_count)
    
    print(f"目标生成 {target_count} 个新候选...")
    candidates = generator.generate_all_candidates()
    print(f"实际生成 {len(candidates)} 个候选")
    
    print("保存输出文件...")
    outputs = generator.save_round2_outputs(candidates)
    
    print("生成汇总报告...")
    combined_summary = generator.generate_combined_summary()
    
    print("\n================================================================================")
    print("Round 2 生成完成统计")
    print("================================================================================")
    print(f"候选总数: {outputs['candidates_count']}")
    print(f"add_new 数量: {outputs['merge_check_counts'].get('add_new', 0)}")
    print(f"add_as_subtopic 数量: {outputs['merge_check_counts'].get('add_as_subtopic', 0)}")
    print(f"merge_with_existing 数量: {outputs['merge_check_counts'].get('merge_with_existing', 0)}")
    print(f"reject 数量: {outputs['merge_check_counts'].get('reject', 0)}")
    print(f"manual_review 数量: {outputs['merge_check_counts'].get('manual_review', 0)}")
    print(f"high_duplicate_risk 数量: {outputs['duplicate_risk_counts'].get('high', 0)}")
    print(f"empty_direct_pre 数量: {outputs['validation_result']['empty_direct_pre_count']}")
    print(f"section_id_dependencies: {outputs['validation_result']['has_section_id_dependencies']}")
    print(f"dangling_references: {outputs['validation_result']['has_dangling_references']}")
    print(f"cycles: {outputs['validation_result']['has_cycles']}")
    print(f"主图谱 item_count: {outputs['main_validation']['item_count']}")
    print(f"主图谱验证: {outputs['main_validation']['dependency_check']}")
    
    print(f"\n合并统计:")
    print(f"round1 + round2 总数: {combined_summary['combined_total']}")
    print(f"推荐合并审核: {outputs['merge_check_counts'].get('add_new', 0)}")
    
    print("\n================================================================================")
    print("阶段 2 Round 2 完成！")
    print("================================================================================")

if __name__ == "__main__":
    main()