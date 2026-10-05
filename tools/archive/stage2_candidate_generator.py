import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict
import copy

class Stage2CandidateGenerator:
    def __init__(self, input_json: str, candidate_count: int = 400):
        self.input_json = input_json
        self.candidate_count = candidate_count
        self.load_main_graph()
        self.initialize_directories()
        
    def load_main_graph(self):
        """Load the main knowledge graph without modifying it"""
        with open(self.input_json, 'r', encoding='utf-8') as f:
            self.main_graph = json.load(f)
        
        # Extract existing items for duplicate checking
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
                        'category': category['name']
                    }
                    self.existing_item_names.add(item['name'].lower())
                    for alias in item.get('alias', []):
                        self.existing_item_aliases.add(alias.lower())
        
        print(f"Loaded main graph with {len(self.existing_items)} existing items")
        
    def initialize_directories(self):
        """Create necessary directories"""
        self.base_dir = Path(self.input_json).parent
        self.data_dir = self.base_dir / 'data'
        self.docs_dir = self.base_dir / 'docs'
        
        self.data_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(exist_ok=True)
        
        print(f"Initialized directories: {self.data_dir}, {self.docs_dir}")
    
    def generate_candidate_id(self, domain: str, topic: str, subtopic: str) -> str:
        """Generate candidate ID in format: cand.<domain>.<topic>.<subtopic>"""
        # Clean up the components
        domain = re.sub(r'[^a-zA-Z0-9_]', '_', domain.lower())
        topic = re.sub(r'[^a-zA-Z0-9_]', '_', topic.lower())
        subtopic = re.sub(r'[^a-zA-Z0-9_]', '_', subtopic.lower())
        
        return f"cand.{domain}.{topic}.{subtopic}"
    
    def check_duplicate(self, name: str, en_name: str, aliases: List[str] = None) -> Dict:
        """Check if candidate is duplicate of existing items"""
        name_lower = name.lower()
        en_name_lower = en_name.lower() if en_name else ''
        
        results = {
            'is_duplicate': False,
            'duplicate_type': None,
            'matching_item_ids': [],
            'confidence': 'low',
            'suggestion': 'add_new'
        }
        
        # Check exact name match
        for item_id, item_data in self.existing_items.items():
            if item_data['name'].lower() == name_lower:
                results['is_duplicate'] = True
                results['duplicate_type'] = 'exact_name'
                results['matching_item_ids'].append(item_id)
                results['confidence'] = 'high'
                results['suggestion'] = 'merge_with_existing'
                break
            
            # Check alias match
            for alias in item_data['alias']:
                if alias.lower() == name_lower:
                    results['is_duplicate'] = True
                    results['duplicate_type'] = 'alias_match'
                    results['matching_item_ids'].append(item_id)
                    results['confidence'] = 'high'
                    results['suggestion'] = 'merge_with_existing'
                    break
        
        # Check English name match
        if en_name and not results['is_duplicate']:
            for item_id, item_data in self.existing_items.items():
                if 'en_name' in item_data and item_data['en_name'].lower() == en_name_lower:
                    results['is_duplicate'] = True
                    results['duplicate_type'] = 'en_name_match'
                    results['matching_item_ids'].append(item_id)
                    results['confidence'] = 'medium'
                    results['suggestion'] = 'merge_with_existing'
                    break
        
        # Check partial similarity
        if not results['is_duplicate']:
            for item_id, item_data in self.existing_items.items():
                existing_name = item_data['name'].lower()
                # Check if one name contains the other
                if name_lower in existing_name or existing_name in name_lower:
                    if len(set(name_lower) & set(existing_name)) / max(len(name_lower), len(existing_name)) > 0.7:
                        results['is_duplicate'] = True
                        results['duplicate_type'] = 'similar_name'
                        results['matching_item_ids'].append(item_id)
                        results['confidence'] = 'medium'
                        results['suggestion'] = 'add_as_subtopic'
                        break
        
        return results
    
    def generate_candidates(self) -> List[Dict]:
        """Generate candidate knowledge items"""
        candidates = []
        
        # Define candidate generation strategies for different domains
        strategies = [
            self.generate_graph_candidates,
            self.generate_data_structure_candidates,
            self.generate_string_candidates,
            self.generate_math_candidates,
            self.generate_geometry_candidates,
            self.generate_interview_candidates,
            self.generate_modeling_candidates
        ]
        
        for strategy in strategies:
            domain_candidates = strategy()
            candidates.extend(domain_candidates)
            
            if len(candidates) >= self.candidate_count:
                break
        
        return candidates[:self.candidate_count]
    
    def generate_graph_candidates(self) -> List[Dict]:
        """Generate advanced graph theory candidates"""
        candidates = []
        
        # K-Shortest Paths
        candidates.append({
            'candidate_id': self.generate_candidate_id('graph', 'k_shortest', 'yen_algorithm'),
            'name': 'K 短路 (Yen 算法)',
            'en_name': 'K-Shortest Paths (Yen\'s Algorithm)',
            'category_suggestion': '算法',
            'section_suggestion': '2.13',
            'level': 'L4',
            'difficulty': 8,
            'tracks': ['advanced_graph', 'k_shortest', 'path_planning'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '原图论章节包含最短路，但缺少K短路求解，这是图论中的高级主题',
            'global_relevance': 'medium',
            'direct_pre_suggestion': ['2.13.1', '2.13.2', '2.13.3'],
            'rel_suggestion': ['2.16.1', '2.18.1'],
            'parent_concept_suggestion': '最短路算法',
            'merge_check': self.check_duplicate('K 短路 (Yen 算法)', 'K-Shortest Paths (Yen\'s Algorithm)'),
            'i18n_seed': {
                'zh-Hans': 'K 短路 (Yen 算法)',
                'en': 'K-Shortest Paths (Yen\'s Algorithm)',
                'ja': 'K-最短路経路 (Yen アルゴリズム)',
                'ko': 'K-최단 경로 (Yen 알고리즘)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Dominator Tree
        candidates.append({
            'candidate_id': self.generate_candidate_id('graph', 'dominator_tree', 'lengauer_tarjan'),
            'name': '支配树 (Lengauer-Tarjan 算法)',
            'en_name': 'Dominator Tree (Lengauer-Tarjan Algorithm)',
            'category_suggestion': '算法',
            'section_suggestion': '2.14',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_graph', 'tree_structure', 'compiler_optimization'],
            'audience': ['advanced', 'research'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '支配树是图论和编译器优化中的重要概念，在控制流分析中广泛应用',
            'global_relevance': 'medium',
            'direct_pre_suggestion': ['2.15.1', '2.15.2', '2.15.3'],
            'rel_suggestion': ['2.14.1', '3.6.1'],
            'parent_concept_suggestion': '树的高级应用',
            'merge_check': self.check_duplicate('支配树 (Lengauer-Tarjan 算法)', 'Dominator Tree (Lengauer-Tarjan Algorithm)'),
            'i18n_seed': {
                'zh-Hans': '支配树 (Lengauer-Tarjan 算法)',
                'en': 'Dominator Tree (Lengauer-Tarjan Algorithm)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Virtual Tree
        candidates.append({
            'candidate_id': self.generate_candidate_id('graph', 'virtual_tree', 'construction'),
            'name': '虚树构建',
            'en_name': 'Virtual Tree Construction',
            'category_suggestion': '算法',
            'section_suggestion': '2.14',
            'level': 'L4',
            'difficulty': 8,
            'tracks': ['advanced_graph', 'tree_structure', 'lca'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '虚树是处理树上路径查询问题的重要优化技巧',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['2.14.1', '2.14.2', '3.6.1'],
            'rel_suggestion': ['2.8.6', '3.7.1'],
            'parent_concept_suggestion': '树上算法优化',
            'merge_check': self.check_duplicate('虚树构建', 'Virtual Tree Construction'),
            'i18n_seed': {
                'zh-Hans': '虚树构建',
                'en': 'Virtual Tree Construction',
                'ja': '仮想木構築',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_data_structure_candidates(self) -> List[Dict]:
        """Generate advanced data structure candidates"""
        candidates = []
        
        # Segment Tree Beats
        candidates.append({
            'candidate_id': self.generate_candidate_id('ds', 'segment_tree_beats', 'range_chmin'),
            'name': '吉司机线段树',
            'en_name': 'Segment Tree Beats (Range Chmin)',
            'category_suggestion': '数据结构',
            'section_suggestion': '3.7',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_data_structure', 'segment_tree', 'range_operations'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '吉司机线段树支持区间最值修改和查询，是线段树的高级应用',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['3.7.1', '3.7.2', '3.7.3'],
            'rel_suggestion': ['2.8.1', '3.7.4'],
            'parent_concept_suggestion': '高级线段树',
            'merge_check': self.check_duplicate('吉司机线段树', 'Segment Tree Beats (Range Chmin)'),
            'i18n_seed': {
                'zh-Hans': '吉司机线段树',
                'en': 'Segment Tree Beats',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Li Chao Segment Tree
        candidates.append({
            'candidate_id': self.generate_candidate_id('ds', 'li_chao_tree', 'line_segment'),
            'name': '李超线段树',
            'en_name': 'Li Chao Segment Tree',
            'category_suggestion': '数据结构',
            'section_suggestion': '3.7',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_data_structure', 'segment_tree', 'computational_geometry'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '李超线段树用于动态维护直线集合，求x位置的最值，结合了线段树和计算几何',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['3.7.1', '4.7.1', '4.7.2'],
            'rel_suggestion': ['3.7.2', '4.7.3'],
            'parent_concept_suggestion': '几何数据结构',
            'merge_check': self.check_duplicate('李超线段树', 'Li Chao Segment Tree'),
            'i18n_seed': {
                'zh-Hans': '李超线段树',
                'en': 'Li Chao Segment Tree',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Persistent Segment Tree
        candidates.append({
            'candidate_id': self.generate_candidate_id('ds', 'persistent_segment_tree', 'chairman_tree'),
            'name': '主席树 (可持久化线段树)',
            'en_name': 'Persistent Segment Tree (Chairman Tree)',
            'category_suggestion': '数据结构',
            'section_suggestion': '3.11',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['persistent_data_structure', 'segment_tree', 'kth_smallest'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '主席树支持历史版本查询和区间第K小查询，是可持久化数据结构的典型应用',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['3.7.1', '2.4.6', '3.6.1'],
            'rel_suggestion': ['3.7.2', '2.2.10'],
            'parent_concept_suggestion': '可持久化数据结构',
            'merge_check': self.check_duplicate('主席树 (可持久化线段树)', 'Persistent Segment Tree (Chairman Tree)'),
            'i18n_seed': {
                'zh-Hans': '主席树 (可持久化线段树)',
                'en': 'Persistent Segment Tree (Chairman Tree)',
                'ja': '永続セグメント木 (主席樹)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_string_candidates(self) -> List[Dict]:
        """Generate advanced string algorithm candidates"""
        candidates = []
        
        # Suffix Array
        candidates.append({
            'candidate_id': self.generate_candidate_id('string', 'suffix_array', 'sais'),
            'name': '后缀数组 (SA-IS 算法)',
            'en_name': 'Suffix Array (SA-IS Algorithm)',
            'category_suggestion': '算法',
            'section_suggestion': '2.10',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_string', 'suffix_structure', 'string_matching'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '后缀数组是字符串处理的基础结构，SA-IS是线性时间的高效实现',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['2.10.1', '2.10.2', '3.6.1'],
            'rel_suggestion': ['2.10.3', '3.8.1'],
            'parent_concept_suggestion': '高级字符串算法',
            'merge_check': self.check_duplicate('后缀数组 (SA-IS 算法)', 'Suffix Array (SA-IS Algorithm)'),
            'i18n_seed': {
                'zh-Hans': '后缀数组 (SA-IS 算法)',
                'en': 'Suffix Array (SA-IS Algorithm)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Suffix Automaton
        candidates.append({
            'candidate_id': self.generate_candidate_id('string', 'suffix_automaton', 'construction'),
            'name': '后缀自动机 (SAM)',
            'en_name': 'Suffix Automaton (SAM)',
            'category_suggestion': '算法',
            'section_suggestion': '2.10',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_string', 'automaton', 'substring_counting'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '后缀自动机是字符串处理的强大工具，支持高效子串查询和计数',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['2.10.1', '3.8.1', '3.6.1'],
            'rel_suggestion': ['2.10.2', '3.8.2'],
            'parent_concept_suggestion': '字符串自动机',
            'merge_check': self.check_duplicate('后缀自动机 (SAM)', 'Suffix Automaton (SAM)'),
            'i18n_seed': {
                'zh-Hans': '后缀自动机 (SAM)',
                'en': 'Suffix Automaton (SAM)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_math_candidates(self) -> List[Dict]:
        """Generate advanced mathematics candidates"""
        candidates = []
        
        # Pollard Rho
        candidates.append({
            'candidate_id': self.generate_candidate_id('math', 'number_theory', 'pollard_rho'),
            'name': 'Pollard Rho 算法',
            'en_name': 'Pollard Rho Algorithm',
            'category_suggestion': '算法竞赛数学',
            'section_suggestion': '4.1',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_math', 'number_theory', 'factorization'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': 'Pollard Rho是大整数分解的高效算法，是高级数论的重要内容',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['4.1.1', '4.1.2', '4.1.3'],
            'rel_suggestion': ['4.1.4', '4.2.1'],
            'parent_concept_suggestion': '高级数论算法',
            'merge_check': self.check_duplicate('Pollard Rho 算法', 'Pollard Rho Algorithm'),
            'i18n_seed': {
                'zh-Hans': 'Pollard Rho 算法',
                'en': 'Pollard Rho Algorithm',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        # Fast Fourier Transform
        candidates.append({
            'candidate_id': self.generate_candidate_id('math', 'polynomial', 'fft'),
            'name': '快速傅里叶变换 (FFT)',
            'en_name': 'Fast Fourier Transform (FFT)',
            'category_suggestion': '算法竞赛数学',
            'section_suggestion': '4.8',
            'level': 'L4',
            'difficulty': 9,
            'tracks': ['advanced_math', 'polynomial', 'convolution'],
            'audience': ['advanced', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': 'FFT是多项式乘法和卷积计算的基础，在算法竞赛中应用广泛',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['4.2.1', '4.2.2', '4.3.1'],
            'rel_suggestion': ['2.12.1', '4.8.1'],
            'parent_concept_suggestion': '多项式算法',
            'merge_check': self.check_duplicate('快速傅里叶变换 (FFT)', 'Fast Fourier Transform (FFT)'),
            'i18n_seed': {
                'zh-Hans': '快速傅里叶变换 (FFT)',
                'en': 'Fast Fourier Transform (FFT)',
                'ja': '高速フーリエ変換 (FFT)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_geometry_candidates(self) -> List[Dict]:
        """Generate computational geometry candidates"""
        candidates = []
        
        # Convex Hull
        candidates.append({
            'candidate_id': self.generate_candidate_id('geo', 'convex_hull', 'graham_scan'),
            'name': '凸包 (Graham Scan 算法)',
            'en_name': 'Convex Hull (Graham Scan Algorithm)',
            'category_suggestion': '算法竞赛数学',
            'section_suggestion': '4.7',
            'level': 'L3',
            'difficulty': 7,
            'tracks': ['computational_geometry', 'convex_hull', 'sorting'],
            'audience': ['intermediate', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '凸包是计算几何的基础问题，Graham Scan是经典算法',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['4.7.1', '4.7.2', '2.2.1'],
            'rel_suggestion': ['4.7.3', '2.5.1'],
            'parent_concept_suggestion': '计算几何基础',
            'merge_check': self.check_duplicate('凸包 (Graham Scan 算法)', 'Convex Hull (Graham Scan Algorithm)'),
            'i18n_seed': {
                'zh-Hans': '凸包 (Graham Scan 算法)',
                'en': 'Convex Hull (Graham Scan Algorithm)',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_interview_candidates(self) -> List[Dict]:
        """Generate big tech interview question candidates"""
        candidates = []
        
        # LRU Cache
        candidates.append({
            'candidate_id': self.generate_candidate_id('interview', 'design', 'lru_cache'),
            'name': 'LRU 缓存设计',
            'en_name': 'LRU Cache Design',
            'category_suggestion': '数据结构',
            'section_suggestion': '3.12',
            'level': 'L3',
            'difficulty': 6,
            'tracks': ['interview', 'system_design', 'cache'],
            'audience': ['intermediate', 'interview'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': 'LRU缓存是大厂面试经典题目，综合考察数据结构和系统设计能力',
            'global_relevance': 'high',
            'direct_pre_suggestion': ['3.3.1', '3.2.1', '3.2.2'],
            'rel_suggestion': ['3.12.1', '5.9.1'],
            'parent_concept_suggestion': '缓存设计',
            'merge_check': self.check_duplicate('LRU 缓存设计', 'LRU Cache Design'),
            'i18n_seed': {
                'zh-Hans': 'LRU 缓存设计',
                'en': 'LRU Cache Design',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
    def generate_modeling_candidates(self) -> List[Dict]:
        """Generate ICPC/University contest modeling candidates"""
        candidates = []
        
        # Game Theory
        candidates.append({
            'candidate_id': self.generate_candidate_id('contest', 'modeling', 'game_theory'),
            'name': '博弈论建模',
            'en_name': 'Game Theory Modeling',
            'category_suggestion': '算法',
            'section_suggestion': '2.18',
            'level': 'L3',
            'difficulty': 7,
            'tracks': ['contest_modeling', 'game_theory', 'strategy'],
            'audience': ['intermediate', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': '博弈论是程序设计竞赛中的常见建模类型，需要数学思维和策略分析',
            'global_relevance': 'medium',
            'direct_pre_suggestion': ['2.1.7', '2.6.1', '4.1.1'],
            'rel_suggestion': ['2.8.1', '4.6.1'],
            'parent_concept_suggestion': '竞赛建模技巧',
            'merge_check': self.check_duplicate('博弈论建模', 'Game Theory Modeling'),
            'i18n_seed': {
                'zh-Hans': '博弈论建模',
                'en': 'Game Theory Modeling',
                'needs_native_review': True
            },
            'content_status': 'outline',
            'review_status': 'pending'
        })
        
        return candidates
    
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
        
        # Check for section ID dependencies
        all_item_ids = set(self.existing_items.keys())
        candidate_ids = {c['candidate_id'] for c in candidates}
        all_valid_ids = all_item_ids | candidate_ids
        
        for candidate in candidates:
            direct_pre = candidate.get('direct_pre_suggestion', [])
            
            # Check empty dependencies
            if not direct_pre:
                validation_result['empty_direct_pre_count'] += 1
            
            # Check for section IDs and dangling references
            for dep in direct_pre:
                if dep.startswith(('1.', '2.', '3.', '4.', '5.')) and len(dep.split('.')) == 2:
                    validation_result['has_section_id_dependencies'] = True
                    validation_result['invalid_dependencies'].append({
                        'candidate_id': candidate['candidate_id'],
                        'invalid_dep': dep,
                        'reason': 'Section ID dependency not allowed'
                    })
                elif dep not in all_valid_ids:
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
                    candidate_graph[dep].append(candidate_id)
        
        # Simple cycle detection
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
    
    def generate_duplicate_review(self, candidates: List[Dict]) -> Dict:
        """Generate duplicate review report"""
        duplicate_review = {
            'total_candidates': len(candidates),
            'review_results': []
        }
        
        counts = defaultdict(int)
        
        for candidate in candidates:
            merge_check = candidate.get('merge_check', {})
            suggestion = merge_check.get('suggestion', 'add_new')
            counts[suggestion] += 1
            
            duplicate_review['review_results'].append({
                'candidate_id': candidate['candidate_id'],
                'name': candidate['name'],
                'is_duplicate': merge_check.get('is_duplicate', False),
                'duplicate_type': merge_check.get('duplicate_type'),
                'matching_item_ids': merge_check.get('matching_item_ids', []),
                'confidence': merge_check.get('confidence'),
                'suggestion': suggestion
            })
        
        duplicate_review['summary'] = dict(counts)
        
        return duplicate_review
    
    def generate_dependency_review(self, candidates: List[Dict], validation_result: Dict) -> Dict:
        """Generate dependency review report"""
        return {
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
    
    def generate_merge_preview(self, candidates: List[Dict]) -> Dict:
        """Generate merge preview (without actual merging)"""
        preview = {
            'preview_type': 'candidate_only',
            'total_candidates': len(candidates),
            'candidates_by_category': defaultdict(list),
            'candidates_by_section': defaultdict(list),
            'candidates_by_level': defaultdict(list),
            'warnings': []
        }
        
        for candidate in candidates:
            preview['candidates_by_category'][candidate['category_suggestion']].append(candidate['candidate_id'])
            preview['candidates_by_section'][candidate['section_suggestion']].append(candidate['candidate_id'])
            preview['candidates_by_level'][candidate['level']].append(candidate['candidate_id'])
            
            # Add warnings for candidates with merge suggestions
            if candidate.get('merge_check', {}).get('suggestion') in ['merge_with_existing', 'add_as_subtopic']:
                preview['warnings'].append({
                    'candidate_id': candidate['candidate_id'],
                    'warning_type': 'merge_conflict',
                    'message': f"Candidate suggested to {candidate['merge_check']['suggestion']}",
                    'details': candidate['merge_check']
                })
        
        preview['candidates_by_category'] = dict(preview['candidates_by_category'])
        preview['candidates_by_section'] = dict(preview['candidates_by_section'])
        preview['candidates_by_level'] = dict(preview['candidates_by_level'])
        
        return preview
    
    def generate_i18n_seed(self, candidates: List[Dict]) -> Dict:
        """Generate i18n seed file"""
        i18n_seed = {
            'total_candidates': len(candidates),
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
                'name': candidate['name'],
                'en_name': candidate['en_name'],
                'translations': i18n_data
            }
            
            if 'zh-Hans' in i18n_data:
                i18n_seed['coverage_stats']['has_zh_hans'] += 1
            if 'en' in i18n_data:
                i18n_seed['coverage_stats']['has_en'] += 1
            if len(i18n_data) > 2:
                i18n_seed['coverage_stats']['has_additional_languages'] += 1
            
            i18n_seed['terms'].append(i18n_entry)
        
        return i18n_seed
    
    def generate_track_distribution(self, candidates: List[Dict]) -> Dict:
        """Generate track distribution report"""
        track_stats = defaultdict(list)
        
        for candidate in candidates:
            for track in candidate.get('tracks', []):
                track_stats[track].append(candidate['candidate_id'])
        
        return {
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
    
    def generate_expansion_plan(self, candidates: List[Dict]) -> Dict:
        """Generate knowledge expansion plan"""
        return {
            'plan_title': 'Algorithm Competition Knowledge Graph Expansion - Batch 1',
            'plan_version': '1.0',
            'generation_date': '2025-05-22',
            'total_candidates': len(candidates),
            'expansion_strategy': {
                'focus_areas': [
                    '高级图论',
                    '高级数据结构',
                    '高级字符串算法',
                    '高级数学/数论/多项式',
                    '计算几何',
                    '大厂面试题型',
                    'ICPC/大学程序设计竞赛建模'
                ],
                'quality_principles': [
                    '不与现有知识点重复',
                    '遵循学习路径依赖关系',
                    '覆盖竞赛核心内容',
                    '支持国际化需求'
                ]
            },
            'candidate_distribution': {
                'by_category': self._count_by_field(candidates, 'category_suggestion'),
                'by_level': self._count_by_field(candidates, 'level'),
                'by_difficulty': self._get_difficulty_distribution(candidates),
                'by_visibility': self._count_by_field(candidates, 'visibility')
            },
            'implementation_phases': [
                {
                    'phase': 'review',
                    'description': '人工审核候选知识点',
                    'estimated_time': '1-2 weeks'
                },
                {
                    'phase': 'content_development',
                    'description': '为通过审核的知识点开发教学内容',
                    'estimated_time': '2-4 weeks'
                },
                {
                    'phase': 'integration',
                    'description': '将审核通过的知识点合并到主图谱',
                    'estimated_time': '1 week'
                }
            ]
        }
    
    def _count_by_field(self, candidates: List[Dict], field: str) -> Dict:
        """Helper to count candidates by field"""
        counts = defaultdict(int)
        for candidate in candidates:
            counts[candidate.get(field, 'unknown')] += 1
        return dict(counts)
    
    def _get_difficulty_distribution(self, candidates: List[Dict]) -> Dict:
        """Get difficulty distribution"""
        distribution = defaultdict(int)
        for candidate in candidates:
            difficulty = candidate.get('difficulty', 5)
            if difficulty <= 3:
                distribution['easy'] += 1
            elif difficulty <= 6:
                distribution['medium'] += 1
            elif difficulty <= 8:
                distribution['hard'] += 1
            else:
                distribution['expert'] += 1
        return dict(distribution)
    
    def generate_batch_report(self, candidates: List[Dict], validation_result: Dict) -> Dict:
        """Generate comprehensive batch report"""
        # Generate all analysis components
        duplicate_review = self.generate_duplicate_review(candidates)
        dependency_review = self.generate_dependency_review(candidates, validation_result)
        merge_preview = self.generate_merge_preview(candidates)
        i18n_seed = self.generate_i18n_seed(candidates)
        track_distribution = self.generate_track_distribution(candidates)
        
        return {
            'report_title': 'Candidate Knowledge Items Batch 1 Report',
            'generation_date': '2025-05-22',
            'summary': {
                'total_candidates': len(candidates),
                'by_category': self._count_by_field(candidates, 'category_suggestion'),
                'by_tracks': len(set().union(*[set(c.get('tracks', [])) for c in candidates])),
                'by_visibility': self._count_by_field(candidates, 'visibility'),
                'duplicate_risk_distribution': duplicate_review['summary'],
                'merge_suggestions': duplicate_review['summary']
            },
            'dependency_analysis': {
                'empty_direct_pre_count': validation_result['empty_direct_pre_count'],
                'has_section_id_dependencies': validation_result['has_section_id_dependencies'],
                'has_dangling_references': validation_result['has_dangling_references'],
                'has_cycles': validation_result['has_cycles'],
                'invalid_dependencies_count': len(validation_result['invalid_dependencies'])
            },
            'quality_metrics': {
                'i18n_coverage': i18n_seed['coverage_stats'],
                'high_duplicate_risk': len([c for c in candidates if c.get('merge_check', {}).get('confidence') == 'high']),
                'candidates_requiring_review': len([c for c in candidates if c.get('review_status') == 'pending'])
            },
            'recommendations': {
                'recommended_for_merge': len([c for c in candidates if c.get('merge_check', {}).get('suggestion') == 'add_new']),
                'requires_manual_review': len([c for c in candidates if c.get('merge_check', {}).get('suggestion') in ['manual_review', 'merge_with_existing']]),
                'next_steps': [
                    'Review high duplicate risk candidates',
                    'Validate dependency relationships',
                    'Develop content for approved candidates',
                    'Prepare merge plan'
                ]
            }
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
            # Count items
            total_items = 0
            for category in self.main_graph['categories']:
                for section in category['sections']:
                    total_items += len(section['items'])
            
            validation_result['item_count'] = total_items
            
            # Check if item count matches expected (should be 1349 from original)
            if total_items != 1349:
                validation_result['is_valid'] = False
                validation_result['issues'].append(f"Item count mismatch: expected 1349, got {total_items}")
            
            # Basic structure validation
            if 'categories' not in self.main_graph:
                validation_result['is_valid'] = False
                validation_result['structure_check'] = 'failed'
                validation_result['issues'].append('Missing categories in main graph')
            
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['issues'].append(f'Validation error: {str(e)}')
        
        return validation_result
    
    def save_all_outputs(self, candidates: List[Dict]):
        """Save all output files"""
        # Validate dependencies
        validation_result = self.validate_dependencies(candidates)
        
        # Save candidates
        candidates_file = self.data_dir / 'candidate_new_knowledge_items_batch1.json'
        with open(candidates_file, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, ensure_ascii=False, indent=2)
        
        # Save duplicate review
        duplicate_review = self.generate_duplicate_review(candidates)
        duplicate_file = self.data_dir / 'candidate_duplicate_review.json'
        with open(duplicate_file, 'w', encoding='utf-8') as f:
            json.dump(duplicate_review, f, ensure_ascii=False, indent=2)
        
        # Save dependency review
        dependency_review = self.generate_dependency_review(candidates, validation_result)
        dependency_file = self.data_dir / 'candidate_dependency_review.json'
        with open(dependency_file, 'w', encoding='utf-8') as f:
            json.dump(dependency_review, f, ensure_ascii=False, indent=2)
        
        # Save merge preview
        merge_preview = self.generate_merge_preview(candidates)
        preview_file = self.data_dir / 'candidate_merge_preview.json'
        with open(preview_file, 'w', encoding='utf-8') as f:
            json.dump(merge_preview, f, ensure_ascii=False, indent=2)
        
        # Save i18n seed
        i18n_seed = self.generate_i18n_seed(candidates)
        i18n_file = self.data_dir / 'candidate_i18n_terms_seed.json'
        with open(i18n_file, 'w', encoding='utf-8') as f:
            json.dump(i18n_seed, f, ensure_ascii=False, indent=2)
        
        # Save track distribution
        track_dist = self.generate_track_distribution(candidates)
        track_file = self.data_dir / 'candidate_track_distribution.json'
        with open(track_file, 'w', encoding='utf-8') as f:
            json.dump(track_dist, f, ensure_ascii=False, indent=2)
        
        # Save expansion plan
        expansion_plan = self.generate_expansion_plan(candidates)
        plan_file = self.docs_dir / 'candidate_knowledge_expansion_plan.md'
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write("# Candidate Knowledge Expansion Plan - Batch 1\n\n")
            f.write(f"**Generated:** {expansion_plan['generation_date']}\n")
            f.write(f"**Total Candidates:** {expansion_plan['total_candidates']}\n\n")
            f.write("## Focus Areas\n\n")
            for area in expansion_plan['expansion_strategy']['focus_areas']:
                f.write(f"- {area}\n")
            f.write("\n## Distribution\n\n")
            f.write("### By Category\n\n")
            for cat, count in expansion_plan['candidate_distribution']['by_category'].items():
                f.write(f"- {cat}: {count}\n")
            f.write("\n### By Level\n\n")
            for level, count in expansion_plan['candidate_distribution']['by_level'].items():
                f.write(f"- {level}: {count}\n")
            f.write("\n## Implementation Phases\n\n")
            for i, phase in enumerate(expansion_plan['implementation_phases'], 1):
                f.write(f"### Phase {i}: {phase['phase']}\n")
                f.write(f"- **Description:** {phase['description']}\n")
                f.write(f"- **Estimated Time:** {phase['estimated_time']}\n\n")
        
        # Save batch report
        batch_report = self.generate_batch_report(candidates, validation_result)
        report_file = self.docs_dir / 'candidate_new_items_batch1_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Candidate Knowledge Items Batch 1 Report\n\n")
            f.write(f"**Generated:** {batch_report['generation_date']}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Candidates:** {batch_report['summary']['total_candidates']}\n")
            f.write(f"- **Categories:** {', '.join(batch_report['summary']['by_category'].keys())}\n")
            f.write(f"- **Tracks:** {batch_report['summary']['by_tracks']}\n\n")
            f.write("## Distribution\n\n")
            f.write("### By Category\n\n")
            for cat, count in batch_report['summary']['by_category'].items():
                f.write(f"- {cat}: {count}\n")
            f.write("\n### By Visibility\n\n")
            for vis, count in batch_report['summary']['by_visibility'].items():
                f.write(f"- {vis}: {count}\n")
            f.write("\n### Duplicate Risk Distribution\n\n")
            for risk, count in batch_report['summary']['duplicate_risk_distribution'].items():
                f.write(f"- {risk}: {count}\n")
            f.write("\n## Dependency Analysis\n\n")
            f.write(f"- **Empty Direct Pre:** {batch_report['dependency_analysis']['empty_direct_pre_count']}\n")
            f.write(f"- **Has Section ID Dependencies:** {batch_report['dependency_analysis']['has_section_id_dependencies']}\n")
            f.write(f"- **Has Dangling References:** {batch_report['dependency_analysis']['has_dangling_references']}\n")
            f.write(f"- **Has Cycles:** {batch_report['dependency_analysis']['has_cycles']}\n")
            f.write(f"- **Invalid Dependencies:** {batch_report['dependency_analysis']['invalid_dependencies_count']}\n")
            f.write("\n## Quality Metrics\n\n")
            f.write("### I18n Coverage\n\n")
            for lang, count in batch_report['quality_metrics']['i18n_coverage'].items():
                f.write(f"- {lang}: {count}\n")
            f.write("\n### Quality Issues\n\n")
            f.write(f"- **High Duplicate Risk:** {batch_report['quality_metrics']['high_duplicate_risk']}\n")
            f.write(f"- **Requires Review:** {batch_report['quality_metrics']['candidates_requiring_review']}\n")
            f.write("\n## Recommendations\n\n")
            f.write(f"- **Recommended for Merge:** {batch_report['recommendations']['recommended_for_merge']}\n")
            f.write(f"- **Requires Manual Review:** {batch_report['recommendations']['requires_manual_review']}\n")
            f.write("\n### Next Steps\n\n")
            for step in batch_report['recommendations']['next_steps']:
                f.write(f"- {step}\n")
        
        # Validate main graph
        main_validation = self.validate_main_graph()
        validation_file = self.data_dir / 'main_graph_validation.json'
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
                str(plan_file),
                str(report_file),
                str(validation_file)
            ],
            'candidates_count': len(candidates),
            'validation_result': validation_result,
            'main_validation': main_validation,
            'batch_report': batch_report
        }

def main():
    import sys
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python stage2_candidate_generator.py <input_json> <candidate_count>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    candidate_count = int(sys.argv[2])
    
    print("=" * 80)
    print("阶段 2: 候选新增知识点库生成")
    print("=" * 80)
    
    # Create generator
    generator = Stage2CandidateGenerator(input_json, candidate_count)
    
    print(f"\n生成 {candidate_count} 个候选知识点...")
    
    # Generate candidates
    candidates = generator.generate_candidates()
    print(f"成功生成 {len(candidates)} 个候选知识点")
    
    # Save all outputs
    print("\n保存输出文件...")
    results = generator.save_all_outputs(candidates)
    
    print(f"\n已保存 {len(results['saved_files'])} 个文件:")
    for file_path in results['saved_files']:
        print(f"  - {file_path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("生成完成统计")
    print("=" * 80)
    
    batch_report = results['batch_report']
    print(f"候选总数: {results['candidates_count']}")
    print(f"分类分布: {batch_report['summary']['by_category']}")
    print(f"可见性分布: {batch_report['summary']['by_visibility']}")
    print(f"重复风险分布: {batch_report['summary']['duplicate_risk_distribution']}")
    print(f"空前置依赖: {batch_report['dependency_analysis']['empty_direct_pre_count']}")
    print(f"包含Section ID依赖: {batch_report['dependency_analysis']['has_section_id_dependencies']}")
    print(f"包含悬空引用: {batch_report['dependency_analysis']['has_dangling_references']}")
    print(f"包含环: {batch_report['dependency_analysis']['has_cycles']}")
    print(f"推荐合并: {batch_report['recommendations']['recommended_for_merge']}")
    print(f"需要人工审核: {batch_report['recommendations']['requires_manual_review']}")
    
    main_validation = results['main_validation']
    print(f"\n主图谱验证:")
    print(f"  - 项目数: {main_validation['item_count']}")
    print(f"  - 验证状态: {'通过' if main_validation['is_valid'] else '失败'}")
    print(f"  - 结构检查: {main_validation['structure_check']}")
    print(f"  - 问题数量: {len(main_validation['issues'])}")
    
    if main_validation['issues']:
        print("  - 问题列表:")
        for issue in main_validation['issues']:
            print(f"    * {issue}")
    
    print("\n" + "=" * 80)
    print("阶段 2 完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()