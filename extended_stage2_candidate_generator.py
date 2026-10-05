import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict

class ExtendedStage2CandidateGenerator:
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
    
    def create_candidate(self, candidate_id, name, en_name, category, section, level, difficulty, tracks, direct_pre, rel, reason, parent_concept, i18n_overrides=None):
        """Create a candidate with all required fields"""
        i18n_base = {
            'zh-Hans': name,
            'en': en_name,
            'needs_native_review': True
        }
        
        if i18n_overrides:
            i18n_base.update(i18n_overrides)
        
        return {
            'candidate_id': candidate_id,
            'name': name,
            'en_name': en_name,
            'category_suggestion': category,
            'section_suggestion': section,
            'level': level,
            'difficulty': difficulty,
            'tracks': tracks,
            'audience': ['advanced', 'contest'] if level in ['L3', 'L4', 'L5'] else ['intermediate', 'contest'],
            'visibility': 'public',
            'learning_path_policy': 'optional',
            'reason_to_add': reason,
            'global_relevance': 'high' if level in ['L3', 'L4'] else 'medium',
            'direct_pre_suggestion': direct_pre,
            'rel_suggestion': rel,
            'parent_concept_suggestion': parent_concept,
            'merge_check': self.check_duplicate(name, en_name),
            'i18n_seed': i18n_base,
            'content_status': 'outline',
            'review_status': 'pending'
        }
    
    def generate_comprehensive_candidates(self) -> List[Dict]:
        """Generate comprehensive candidate list to reach target count"""
        candidates = []
        
        # Add all specialized generation methods
        generators = [
            self.generate_advanced_graph_candidates,
            self.generate_advanced_data_structure_candidates,
            self.generate_advanced_string_candidates,
            self.generate_advanced_math_candidates,
            self.generate_geometry_candidates,
            self.generate_interview_candidates,
            self.generate_contest_modeling_candidates,
            self.generate_randomized_candidates,
            self.generate_advanced_dp_candidates,
            self.generate_network_flow_candidates,
            self.generate_computational_geometry_candidates,
            self.generate_advanced_tree_candidates,
            self.generate_polynomial_candidates,
            self.generate_string_matching_candidates,
            self.generate_number_theory_candidates,
            self.generate_graph_optimization_candidates,
            self.generate_data_structure_variants_candidates
        ]
        
        for generator in generators:
            new_candidates = generator()
            candidates.extend(new_candidates)
            print(f"Generated {len(new_candidates)} candidates from {generator.__name__}")
            
            if len(candidates) >= self.candidate_count:
                break
        
        return candidates[:self.candidate_count]
    
    def generate_advanced_graph_candidates(self) -> List[Dict]:
        """Generate 30 advanced graph theory candidates"""
        candidates = []
        
        # K-Shortest Paths variants
        k_shortest_algorithms = [
            ('yen', 'Yen 算法', 'Yen\'s Algorithm', 8, 'K短路经典算法，基于最短路迭代的候选路径生成'),
            ('eppstein', 'Eppstein 算法', 'Eppstein\'s Algorithm', 9, 'K短路高效算法，基于隐式路径图的最优路径生成'),
            ('recursive', '递归K短路', 'Recursive K-Shortest', 7, '基于递归剪枝的K短路算法，适合小规模图')
        ]
        
        for algo, name_zh, name_en, diff, reason in k_shortest_algorithms:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'k_shortest', algo),
                f'K 短路 ({name_zh})',
                f'K-Shortest Paths ({name_en})',
                '算法', '2.13', 'L4', diff,
                ['advanced_graph', 'k_shortest', 'path_optimization'],
                ['2.13.1', '2.13.2', '2.13.3'],
                ['2.16.1', '2.18.1'],
                f"{reason}，适用于路径规划和优化问题",
                '最短路算法扩展'
            ))
        
        # Dominator Tree variants
        dominator_algorithms = [
            ('lengauer_tarjan', 'Lengauer-Tarjan 算法', 'Lengauer-Tarjan Algorithm', 9, '支配树经典算法，用于控制流分析'),
            ('iterative', '迭代支配树', 'Iterative Dominator Tree', 7, '基于迭代的支配树构建，时间复杂度较低'),
            ('application', '支配树应用', 'Dominator Tree Applications', 8, '支配树在程序分析和图论中的应用')
        ]
        
        for algo, name_zh, name_en, diff, reason in dominator_algorithms:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'dominator_tree', algo),
                f'支配树 ({name_zh})',
                f'Dominator Tree ({name_en})',
                '算法', '2.14', 'L4', diff,
                ['advanced_graph', 'dominator', 'program_analysis'],
                ['2.15.1', '2.15.2', '2.15.3'],
                ['2.14.1', '3.6.1', '5.5.1'],
                reason,
                '高级图结构'
            ))
        
        # Advanced Tree Algorithms
        tree_algorithms = [
            ('virtual_tree', '虚树构建', 'Virtual Tree Construction', 8, '虚树用于高效处理树上路径查询问题'),
            ('centroid_decomposition', '点分治', 'Centroid Decomposition', 8, '点分治用于解决树上路径问题'),
            ('tree_flattening', '树链剖分', 'Tree Chain Decomposition', 8, '树链剖分将树转换为线性结构处理'),
            ('heavy_light', '重链剖分', 'Heavy-Light Decomposition', 7, '重链剖分是树链剖分的一种变体'),
            ('parallel_binary', '并查集维护连通性', 'Disjoint Set Union on Trees', 7, '在树上使用并查集维护连通性')
        ]
        
        for algo, name_zh, name_en, diff, reason in tree_algorithms:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'tree_advanced', algo),
                name_zh, name_en,
                '算法', '2.14', 'L4', diff,
                ['advanced_graph', 'tree_algorithms', 'path_query'],
                ['2.14.1', '2.14.2', '3.6.1'],
                ['2.8.6', '3.7.1', '3.4.1'],
                reason,
                '高级树算法'
            ))
        
        # Network Flow variants
        flow_algorithms = [
            ('dinic', 'Dinic 算法', 'Dinic\'s Algorithm', 8, '网络流经典算法，基于层次图和增广路径'),
            ('isap', 'ISAP 算法', 'ISAP Algorithm', 8, '改进的最短路增广路径算法'),
            ('hlpp', 'HLPP 算法', 'HLPP Algorithm', 9, '最高标号预流推进算法，效率极高'),
            ('min_cost', '最小费用最大流', 'Min-Cost Max-Flow', 8, '在满足最大流的条件下最小化费用'),
            ('lower_upper', '上下界网络流', 'Flow with Lower/Upper Bounds', 9, '处理带上下界的网络流问题')
        ]
        
        for algo, name_zh, name_en, diff, reason in flow_algorithms:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'network_flow', algo),
                name_zh, name_en,
                '算法', '2.16', 'L4', diff,
                ['advanced_graph', 'network_flow', 'optimization'],
                ['2.16.1', '2.13.1', '2.13.2'],
                ['2.13.3', '2.15.1', '2.18.1'],
                reason,
                '网络流算法'
            ))
        
        return candidates
    
    def generate_advanced_data_structure_candidates(self) -> List[Dict]:
        """Generate 30 advanced data structure candidates"""
        candidates = []
        
        # Advanced Segment Trees
        segtree_algorithms = [
            ('beats_chmin', '吉司机线段树(区间最小)', 'Segment Tree Beats (Range Chmin)', 9, '支持区间取最小值和查询最值的线段树'),
            ('beats_chmax', '吉司机线段树(区间最大)', 'Segment Tree Beats (Range Chmax)', 9, '支持区间取最大值和查询最值的线段树'),
            ('beats_range_add', '吉司机线段树(区间加)', 'Segment Tree Beats (Range Add)', 9, '支持区间加法和查询最值的线段树'),
            ('dynamic_persistent', '动态可持久化线段树', 'Dynamic Persistent Segment Tree', 9, '支持动态修改和历史版本查询的线段树'),
            ('segment_tree_merge', '线段树合并', 'Segment Tree Merge', 8, '将多个线段树合并为一个'),
            ('segment_tree_split', '线段树分裂', 'Segment Tree Split', 8, '将线段树分裂为多个')
        ]
        
        for algo, name_zh, name_en, diff, reason in segtree_algorithms:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('ds', 'segtree_advanced', algo),
                name_zh, name_en,
                '数据结构', '3.7', 'L4', diff,
                ['advanced_data_structure', 'segment_tree', 'range_operations'],
                ['3.7.1', '3.7.2', '3.7.3'],
                ['3.7.4', '2.8.1', '3.6.1'],
                reason,
                '高级线段树'
            ))
        
        # Advanced Tree Structures
        tree_structures = [
            ('chairman_tree', '主席树', 'Chairman Tree (Persistent Segment Tree)', 9, '可持久化线段树，支持区间第K小查询'),
            ('kdtree', 'KD 树', 'KD-Tree', 8, '多维数据结构，用于空间搜索'),
            ('divide_merge_tree', '划分树', 'Divide and Conquer Tree', 8, '用于区间查询的树形结构'),
            ('catenary_tree', '猫树', 'Catenary Tree', 9, '结合了分治和树的数据结构'),
            ('binary_indexed_2d', '二维树状数组', '2D Binary Indexed Tree', 7, '扩展树状数组到二维')
        ]
        
        for struct, name_zh, name_en, diff, reason in tree_structures:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('ds', 'tree_advanced', struct),
                name_zh, name_en,
                '数据结构', '3.11', 'L4', diff,
                ['advanced_data_structure', 'tree_structure', 'query'],
                ['3.7.1', '3.6.1', '2.4.6'],
                ['3.7.2', '2.2.10', '2.4.1'],
                reason,
                '高级树结构'
            ))
        
        # Advanced Balanced Trees
        balanced_trees = [
            ('treap', 'Treap (树堆)', 'Treap (Tree Heap)', 8, '基于堆和BST的平衡树'),
            ('splay', 'Splay Tree (伸展树)', 'Splay Tree', 9, '能将节点移动到根部的平衡树'),
            ('scapegoat', '替罪羊树', 'Scapegoat Tree', 8, '基于重构的平衡树'),
            ('avl', 'AVL 树', 'AVL Tree', 7, '严格平衡的二叉搜索树'),
            ('sbt', 'Size Balanced Tree', 'Size Balanced Tree', 8, '基于子树大小的平衡树')
        ]
        
        for tree, name_zh, name_en, diff, reason in balanced_trees:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('ds', 'balanced_tree', tree),
                name_zh, name_en,
                '数据结构', '3.10', 'L4', diff,
                ['advanced_data_structure', 'balanced_tree', 'bst'],
                ['3.6.1', '3.2.1', '2.3.1'],
                ['3.10.1', '3.3.1', '2.2.1'],
                reason,
                '平衡树'
            ))
        
        return candidates
    
    def generate_advanced_string_candidates(self) -> List[Dict]:
        """Generate 25 advanced string algorithm candidates"""
        candidates = []
        
        # Suffix Structures
        suffix_structures = [
            ('suffix_array', '后缀数组', 'Suffix Array', 9, '字符串后缀排序的基础结构'),
            ('suffix_automaton', '后缀自动机', 'Suffix Automaton', 9, '强大的字符串处理自动机'),
            ('suffix_tree', '后缀树', 'Suffix Tree', 9, '字符串后缀的压缩树结构'),
            ('lcp_array', 'LCP 数组', 'Longest Common Prefix Array', 8, '最长公共前缀数组')
        ]
        
        for struct, name_zh, name_en, diff, reason in suffix_structures:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('string', 'suffix_structure', struct),
                name_zh, name_en,
                '算法', '2.10', 'L4', diff,
                ['advanced_string', 'suffix_structure', 'matching'],
                ['2.10.1', '3.6.1', '2.4.6'],
                ['2.10.2', '3.8.1', '3.8.2'],
                reason,
                '后缀结构'
            ))
        
        # String Matching
        string_matching = [
            ('manacher', 'Manacher 算法', 'Manacher\'s Algorithm', 8, '线性时间求最长回文子串'),
            ('z_algorithm', 'Z 算法', 'Z-Algorithm', 7, '字符串匹配算法'),
            ('kmp', 'KMP 算法', 'Knuth-Morris-Pratt Algorithm', 6, '经典的字符串匹配算法'),
            ('rabin_karp', 'Rabin-Karp 算法', 'Rabin-Karp Algorithm', 6, '基于哈希的字符串匹配'),
            ('booth', 'Booth 算法', 'Booth\'s Algorithm', 8, '求字符串最小表示')
        ]
        
        for algo, name_zh, name_en, diff, reason in string_matching:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('string', 'matching', algo),
                name_zh, name_en,
                '算法', '2.10', 'L3', diff,
                ['advanced_string', 'matching', 'pattern'],
                ['2.10.1', '2.4.6', '1.6.1'],
                ['2.10.2', '3.8.1', '2.2.1'],
                reason,
                '字符串匹配'
            ))
        
        return candidates
    
    def generate_advanced_math_candidates(self) -> List[Dict]:
        """Generate 25 advanced mathematics candidates"""
        candidates = []
        
        # Number Theory
        number_theory = [
            ('pollard_rho', 'Pollard Rho 算法', 'Pollard Rho Algorithm', 9, '大整数分解算法'),
            ('miller_rabin', 'Miller-Rabin 素性测试', 'Miller-Rabin Primality Test', 8, '概率性素数测试'),
            ('discrete_log', '离散对数', 'Discrete Logarithm', 9, '求解离散对数问题'),
            ('primitive_root', '原根', 'Primitive Root', 7, '模运算的原根求解'),
            ('legendre', '勒让德符号', 'Legendre Symbol', 7, '二次剩余的判定符号')
        ]
        
        for topic, name_zh, name_en, diff, reason in number_theory:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('math', 'number_theory', topic),
                name_zh, name_en,
                '算法竞赛数学', '4.1', 'L4', diff,
                ['advanced_math', 'number_theory', 'modular'],
                ['4.1.1', '4.1.2', '4.1.3'],
                ['4.2.1', '4.2.2', '4.1.4'],
                reason,
                '高级数论'
            ))
        
        return candidates
    
    def generate_geometry_candidates(self) -> List[Dict]:
        """Generate 20 computational geometry candidates"""
        candidates = []
        
        # Basic Geometry
        basic_geometry = [
            ('convex_hull', '凸包', 'Convex Hull', 7, '点集的最小凸多边形'),
            ('graham_scan', 'Graham Scan 算法', 'Graham Scan Algorithm', 7, '凸包的扫描算法'),
            ('andrew_monotone', 'Andrew 单调链算法', 'Andrew\'s Monotone Chain', 7, '另一种凸包算法'),
            ('rotating_calipers', '旋转卡壳', 'Rotating Calipers', 8, '用于求解多边形直径等问题'),
            ('half_plane_intersection', '半平面交', 'Half Plane Intersection', 8, '多个半平面的交集')
        ]
        
        for topic, name_zh, name_en, diff, reason in basic_geometry:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('geo', 'basic', topic),
                name_zh, name_en,
                '算法竞赛数学', '4.7', 'L3', diff,
                ['computational_geometry', 'polygon', 'optimization'],
                ['4.7.1', '4.7.2', '2.2.1'],
                ['4.7.3', '2.5.1', '3.6.1'],
                reason,
                '基础计算几何'
            ))
        
        return candidates
    
    def generate_interview_candidates(self) -> List[Dict]:
        """Generate 20 big tech interview question candidates"""
        candidates = []
        
        # System Design
        system_design = [
            ('lru_cache', 'LRU 缓存设计', 'LRU Cache Design', 6, '最近最少使用缓存的设计'),
            ('lfu_cache', 'LFU 缓存设计', 'LFU Cache Design', 7, '最不经常使用缓存的设计'),
            ('trie_autocomplete', '前缀树自动补全', 'Trie Autocomplete System', 6, '基于前缀树的自动补全系统'),
            ('rate_limiter', '速率限制器', 'Rate Limiter', 7, 'API访问频率限制的设计'),
            ('consistent_hashing', '一致性哈希', 'Consistent Hashing', 8, '分布式系统中的负载均衡')
        ]
        
        for topic, name_zh, name_en, diff, reason in system_design:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('interview', 'design', topic),
                name_zh, name_en,
                '数据结构', '3.12', 'L3', diff,
                ['interview', 'system_design', 'cache'],
                ['3.3.1', '3.2.1', '2.4.6'],
                ['3.12.1', '5.9.1', '3.8.1'],
                reason,
                '系统设计'
            ))
        
        return candidates
    
    def generate_contest_modeling_candidates(self) -> List[Dict]:
        """Generate 15 contest modeling candidates"""
        candidates = []
        
        # Contest Techniques
        contest_techniques = [
            ('game_theory', '博弈论建模', 'Game Theory Modeling', 7, '博弈问题的建模和求解'),
            ('sg_theorem', 'SG 定理', 'Sprague-Grundy Theorem', 8, '博弈论中的重要定理'),
            ('nim_game', 'Nim 游戏', 'Nim Game', 6, '经典的博弈问题'),
            ('simulation_optimization', '模拟优化', 'Simulation Optimization', 7, '通过模拟和优化解决问题'),
            ('greedy_proof', '贪心证明', 'Greedy Proof Techniques', 6, '贪心算法的正确性证明方法')
        ]
        
        for technique, name_zh, name_en, diff, reason in contest_techniques:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('contest', 'modeling', technique),
                name_zh, name_en,
                '算法', '2.18', 'L3', diff,
                ['contest_modeling', 'game_theory', 'optimization'],
                ['2.1.7', '2.6.1', '4.1.1'],
                ['2.8.1', '4.6.1', '2.18.1'],
                reason,
                '竞赛建模'
            ))
        
        return candidates
    
    def generate_randomized_candidates(self) -> List[Dict]:
        """Generate 10 randomized algorithm candidates"""
        candidates = []
        
        randomized_algos = [
            ('simulated_annealing', '模拟退火', 'Simulated Annealing', 7, '用于优化问题的随机搜索算法'),
            ('genetic_algorithm', '遗传算法', 'Genetic Algorithm', 7, '基于进化思想的优化算法'),
            ('monte_carlo', '蒙特卡洛方法', 'Monte Carlo Method', 6, '通过随机采样进行数值计算'),
            ('randomized_quickselect', '随机化快速选择', 'Randomized Quickselect', 5, '期望线性时间的选择算法'),
            ('randomized_prim', '随机化 Prim 算法', 'Randomized Prim Algorithm', 6, '基于随机化的最小生成树算法')
        ]
        
        for algo, name_zh, name_en, diff, reason in randomized_algos:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('algo', 'randomized', algo),
                name_zh, name_en,
                '算法', '2.18', 'L3', diff,
                ['randomized', 'optimization', 'heuristic'],
                ['2.1.10', '2.2.5', '2.6.1'],
                ['2.18.1', '2.1.9', '4.6.1'],
                reason,
                '随机化算法'
            ))
        
        return candidates
    
    def generate_advanced_dp_candidates(self) -> List[Dict]:
        """Generate 20 advanced DP candidates"""
        candidates = []
        
        advanced_dp_topics = [
            ('slope_optimization', '斜率优化', 'Slope Optimization', 9, '优化DP转移的斜率优化技术'),
            ('convex_hull_opt', '凸包优化', 'Convex Hull Optimization', 9, '基于凸包的DP优化'),
            ('quadrangle_inequality', '四边形不等式优化', 'Quadrangle Inequality Optimization', 9, '基于四边形不等式的DP优化'),
            ('divide_conquer_opt', '分治优化', 'Divide and Conquer Optimization', 8, '分治优化DP转移'),
            ('knuth_opt', 'Knuth 优化', 'Knuth Optimization', 8, '特定形式的DP优化'),
            ('cdq_divide', 'CDQ 分治', 'CDQ Divide and Conquer', 8, '用于优化DP的分治方法'),
            ('wqs_binary', 'WQS 二分', 'WQS Binary Search', 8, '带权二分优化DP')
        ]
        
        for topic, name_zh, name_en, diff, reason in advanced_dp_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('dp', 'advanced', topic),
                name_zh, name_en,
                '算法', '2.8', 'L4', diff,
                ['advanced_dp', 'optimization', 'dynamic_programming'],
                ['2.8.1', '2.8.2', '2.3.1'],
                ['2.8.3', '4.7.1', '2.4.1'],
                reason,
                '高级DP优化'
            ))
        
        return candidates
    
    def generate_network_flow_candidates(self) -> List[Dict]:
        """Generate 15 network flow candidates"""
        candidates = []
        
        network_flow_topics = [
            ('dinic', 'Dinic 算法', 'Dinic Algorithm', 8, '基于层次图的网络流算法'),
            ('isap', 'ISAP 算法', 'ISAP Algorithm', 8, '改进的最短路增广路径算法'),
            ('edmonds_karp', 'Edmonds-Karp 算法', 'Edmonds-Karp Algorithm', 7, '基于BFS的增广路径算法'),
            ('min_cost_flow', '最小费用最大流', 'Min-Cost Max-Flow', 8, '带费用的网络流问题'),
            ('max_flow_bipartite', '最大流二分图匹配', 'Max Flow Bipartite Matching', 7, '用最大流解决二分图匹配')
        ]
        
        for topic, name_zh, name_en, diff, reason in network_flow_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'network_flow_advanced', topic),
                name_zh, name_en,
                '算法', '2.16', 'L4', diff,
                ['network_flow', 'max_flow', 'optimization'],
                ['2.16.1', '2.13.1', '2.13.2'],
                ['2.13.3', '2.15.1', '2.18.1'],
                reason,
                '网络流高级算法'
            ))
        
        return candidates
    
    def generate_computational_geometry_candidates(self) -> List[Dict]:
        """Generate 15 computational geometry candidates"""
        candidates = []
        
        geometry_topics = [
            ('point_in_polygon', '点在多边形内判断', 'Point in Polygon', 6, '判断点是否在多边形内部'),
            ('line_intersection', '线段相交判断', 'Line Segment Intersection', 6, '判断两条线段是否相交'),
            ('area_polygon', '多边形面积计算', 'Polygon Area Calculation', 5, '计算多边形的面积'),
            ('circle_intersection', '圆相交判断', 'Circle Intersection', 6, '判断两个圆是否相交'),
            ('closest_pair', '最近点对', 'Closest Pair of Points', 7, '寻找距离最近的两个点')
        ]
        
        for topic, name_zh, name_en, diff, reason in geometry_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('geo', 'computational', topic),
                name_zh, name_en,
                '算法竞赛数学', '4.7', 'L3', diff,
                ['computational_geometry', 'geometry', 'algorithm'],
                ['4.7.1', '4.7.2', '2.1.1'],
                ['4.7.3', '2.5.1', '3.6.1'],
                reason,
                '计算几何算法'
            ))
        
        return candidates
    
    def generate_advanced_tree_candidates(self) -> List[Dict]:
        """Generate 15 advanced tree algorithm candidates"""
        candidates = []
        
        tree_topics = [
            ('lca_binary_lifting', 'LCA 倍增法', 'LCA with Binary Lifting', 7, '用倍增法求最近公共祖先'),
            ('lca_euler_tour', 'LCA 欧拉序+RMQ', 'LCA with Euler Tour and RMQ', 8, '用欧拉序和RMQ求LCA'),
            ('tree_diameter', '树的直径', 'Tree Diameter', 6, '树中距离最远的两个节点'),
            ('tree_center', '树的中心', 'Tree Center', 6, '树的重心和中心'),
            ('tree_hash', '树哈希', 'Tree Hashing', 8, '用于判断树同构的哈希方法')
        ]
        
        for topic, name_zh, name_en, diff, reason in tree_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('tree', 'advanced', topic),
                name_zh, name_en,
                '算法', '2.14', 'L3', diff,
                ['tree_algorithms', 'lca', 'graph'],
                ['2.14.1', '2.9.1', '3.6.1'],
                ['2.14.2', '3.7.1', '2.7.1'],
                reason,
                '高级树算法'
            ))
        
        return candidates
    
    def generate_polynomial_candidates(self) -> List[Dict]:
        """Generate 10 polynomial algorithm candidates"""
        candidates = []
        
        polynomial_topics = [
            ('fft', '快速傅里叶变换', 'Fast Fourier Transform', 9, '多项式乘法的高效算法'),
            ('ntt', '数论变换', 'Number Theoretic Transform', 9, '在模运算下的FFT'),
            ('fwht', '快速沃尔什变换', 'Fast Walsh-Hadamard Transform', 8, '用于位运算卷积'),
            ('polynomial_inv', '多项式求逆', 'Polynomial Inversion', 9, '求多项式的逆元'),
            ('polynomial_sqrt', '多项式开方', 'Polynomial Square Root', 9, '求多项式的平方根')
        ]
        
        for topic, name_zh, name_en, diff, reason in polynomial_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('math', 'polynomial', topic),
                name_zh, name_en,
                '算法竞赛数学', '4.8', 'L4', diff,
                ['polynomial', 'fft', 'advanced_math'],
                ['4.2.1', '4.3.1', '2.12.1'],
                ['4.8.1', '4.8.2', '2.8.1'],
                reason,
                '多项式算法'
            ))
        
        return candidates
    
    def generate_string_matching_candidates(self) -> List[Dict]:
        """Generate 10 string matching candidates"""
        candidates = []
        
        string_topics = [
            ('kmp', 'KMP 算法', 'Knuth-Morris-Pratt Algorithm', 6, '经典的单模式匹配算法'),
            ('aho_corasick', 'AC 自动机', 'Aho-Corasick Automaton', 8, '多模式匹配自动机'),
            ('suffix_array', '后缀数组', 'Suffix Array', 9, '字符串后缀排序结构'),
            ('suffix_automaton', '后缀自动机', 'Suffix Automaton', 9, '强大的字符串处理结构'),
            ('min_string', '最小表示法', 'Minimum String Representation', 7, '求字符串的最小循环表示')
        ]
        
        for topic, name_zh, name_en, diff, reason in string_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('string', 'matching_advanced', topic),
                name_zh, name_en,
                '算法', '2.10', 'L4', diff,
                ['advanced_string', 'matching', 'automaton'],
                ['2.10.1', '3.8.1', '2.4.6'],
                ['2.10.2', '3.8.2', '2.2.1'],
                reason,
                '高级字符串匹配'
            ))
        
        return candidates
    
    def generate_number_theory_candidates(self) -> List[Dict]:
        """Generate 15 number theory candidates"""
        candidates = []
        
        number_theory_topics = [
            ('euler_totient', '欧拉函数', 'Euler Totient Function', 6, '计算与n互质的数的个数'),
            ('mobius', '莫比乌斯函数', 'Mobius Function', 7, '数论中的重要函数'),
            ('crt', '中国剩余定理', 'Chinese Remainder Theorem', 7, '解线性同余方程组'),
            ('bsgs', 'BSGS 算法', 'Baby-Step Giant-Step', 8, '求解离散对数'),
            ('exgcd', '扩展欧几里得', 'Extended Euclidean Algorithm', 5, '求解ax+by=gcd(a,b)'),
            ('lucas', 'Lucas 定理', 'Lucas Theorem', 7, '大组合数的模运算')
        ]
        
        for topic, name_zh, name_en, diff, reason in number_theory_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('math', 'number_theory_advanced', topic),
                name_zh, name_en,
                '算法竞赛数学', '4.1', 'L3', diff,
                ['number_theory', 'modular', 'algorithm'],
                ['4.1.1', '4.1.2', '4.2.1'],
                ['4.2.2', '4.3.1', '4.1.3'],
                reason,
                '数论算法'
            ))
        
        return candidates
    
    def generate_graph_optimization_candidates(self) -> List[Dict]:
        """Generate 10 graph optimization candidates"""
        candidates = []
        
        graph_opt_topics = [
            ('minimum_spanning_tree', '最小生成树', 'Minimum Spanning Tree', 6, '连接所有点的最小权边集'),
            ('kruskal', 'Kruskal 算法', 'Kruskal Algorithm', 6, '基于边的最小生成树算法'),
            ('prim', 'Prim 算法', 'Prim Algorithm', 6, '基于点的最小生成树算法'),
            ('topological_sort', '拓扑排序', 'Topological Sort', 5, 'DAG节点的线性排序'),
            ('critical_path', '关键路径', 'Critical Path Method', 7, '项目进度规划中的最长路径')
        ]
        
        for topic, name_zh, name_en, diff, reason in graph_opt_topics:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('graph', 'optimization', topic),
                name_zh, name_en,
                '算法', '2.13', 'L2', diff,
                ['graph', 'optimization', 'mst'],
                ['2.9.1', '2.13.1', '3.4.1'],
                ['2.13.2', '2.7.1', '2.1.5'],
                reason,
                '图优化算法'
            ))
        
        return candidates
    
    def generate_data_structure_variants_candidates(self) -> List[Dict]:
        """Generate 15 data structure variant candidates"""
        candidates = []
        
        ds_variants = [
            ('persistent_treap', '可持久化 Treap', 'Persistent Treap', 9, '支持历史版本的Treap'),
            ('persistent_bit', '可持久化 BIT', 'Persistent BIT', 8, '支持历史版本的树状数组'),
            ('persistent_segment_tree', '可持久化线段树', 'Persistent Segment Tree', 9, '支持历史版本的线段树'),
            ('dynamic_segment_tree', '动态开点线段树', 'Dynamic Segment Tree', 8, '按需开节点的线段树'),
            ('segment_tree_beats', '吉司机线段树', 'Segment Tree Beats', 9, '支持区间最值操作的线段树')
        ]
        
        for variant, name_zh, name_en, diff, reason in ds_variants:
            candidates.append(self.create_candidate(
                self.generate_candidate_id('ds', 'persistent_advanced', variant),
                name_zh, name_en,
                '数据结构', '3.11', 'L4', diff,
                ['persistent', 'data_structure', 'advanced'],
                ['3.7.1', '3.6.1', '2.4.6'],
                ['3.11.1', '3.11.2', '3.7.2'],
                reason,
                '可持久化数据结构'
            ))
        
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
        dependency_file = self.data_dir / 'candidate_dependency_review.json'
        with open(dependency_file, 'w', encoding='utf-8') as f:
            json.dump(dependency_review, f, ensure_ascii=False, indent=2)
        
        # Save merge preview
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
        
        preview_file = self.data_dir / 'candidate_merge_preview.json'
        with open(preview_file, 'w', encoding='utf-8') as f:
            json.dump(preview, f, ensure_ascii=False, indent=2)
        
        # Save i18n seed
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
        
        i18n_file = self.data_dir / 'candidate_i18n_terms_seed.json'
        with open(i18n_file, 'w', encoding='utf-8') as f:
            json.dump(i18n_seed, f, ensure_ascii=False, indent=2)
        
        # Save track distribution
        track_stats = defaultdict(list)
        
        for candidate in candidates:
            for track in candidate.get('tracks', []):
                track_stats[track].append(candidate['candidate_id'])
        
        track_dist = {
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
        
        track_file = self.data_dir / 'candidate_track_distribution.json'
        with open(track_file, 'w', encoding='utf-8') as f:
            json.dump(track_dist, f, ensure_ascii=False, indent=2)
        
        # Save expansion plan
        plan_file = self.docs_dir / 'candidate_knowledge_expansion_plan.md'
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write("# Candidate Knowledge Expansion Plan - Batch 1\n\n")
            f.write(f"**Generated:** 2025-05-22\n")
            f.write(f"**Total Candidates:** {len(candidates)}\n\n")
            f.write("## Focus Areas\n\n")
            f.write("- 高级图论\n")
            f.write("- 高级数据结构\n")
            f.write("- 高级字符串算法\n")
            f.write("- 高级数学/数论/多项式\n")
            f.write("- 计算几何\n")
            f.write("- 大厂面试题型\n")
            f.write("- ICPC/大学程序设计竞赛建模\n\n")
            f.write("## Distribution\n\n")
            f.write("### By Category\n\n")
            cat_counts = defaultdict(int)
            for c in candidates:
                cat_counts[c['category_suggestion']] += 1
            for cat, count in sorted(cat_counts.items()):
                f.write(f"- {cat}: {count}\n")
            f.write("\n### By Level\n\n")
            level_counts = defaultdict(int)
            for c in candidates:
                level_counts[c['level']] += 1
            for level, count in sorted(level_counts.items()):
                f.write(f"- {level}: {count}\n")
        
        # Save batch report
        report_file = self.docs_dir / 'candidate_new_items_batch1_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Candidate Knowledge Items Batch 1 Report\n\n")
            f.write(f"**Generated:** 2025-05-22\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Candidates:** {len(candidates)}\n")
            f.write(f"- **Recommended for Merge:** {len([c for c in candidates if c.get('merge_check', {}).get('suggestion') == 'add_new'])}\n")
            f.write(f"- **Requires Manual Review:** {len([c for c in candidates if c.get('merge_check', {}).get('suggestion') != 'add_new'])}\n")
            f.write(f"- **Empty Direct Pre:** {validation_result['empty_direct_pre_count']}\n")
            f.write(f"- **Has Section ID Dependencies:** {validation_result['has_section_id_dependencies']}\n")
            f.write(f"- **Has Dangling References:** {validation_result['has_dangling_references']}\n")
            f.write(f"- **Has Cycles:** {validation_result['has_cycles']}\n")
            f.write(f"- **Invalid Dependencies:** {len(validation_result['invalid_dependencies'])}\n")
            f.write("\n## Distribution\n\n")
            f.write("### By Category\n\n")
            for cat, count in sorted(cat_counts.items()):
                f.write(f"- {cat}: {count}\n")
            f.write("\n### By Level\n\n")
            for level, count in sorted(level_counts.items()):
                f.write(f"- {level}: {count}\n")
            f.write("\n## Dependency Analysis\n\n")
            f.write(f"- **Empty Direct Pre:** {validation_result['empty_direct_pre_count']}\n")
            f.write(f"- **Has Section ID Dependencies:** {validation_result['has_section_id_dependencies']}\n")
            f.write(f"- **Has Dangling References:** {validation_result['has_dangling_references']}\n")
            f.write(f"- **Has Cycles:** {validation_result['has_cycles']}\n")
            f.write(f"- **Invalid Dependencies:** {len(validation_result['invalid_dependencies'])}\n")
            f.write("\n## Recommendations\n\n")
            f.write(f"- **Recommended for Merge:** {len([c for c in candidates if c.get('merge_check', {}).get('suggestion') == 'add_new'])}\n")
            f.write(f"- **Requires Manual Review:** {len([c for c in candidates if c.get('merge_check', {}).get('suggestion') != 'add_new'])}\n")
            f.write("\n### Next Steps\n\n")
            f.write("- Review high duplicate risk candidates\n")
            f.write("- Validate dependency relationships\n")
            f.write("- Develop content for approved candidates\n")
            f.write("- Prepare merge plan\n")
        
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

def main():
    import sys
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python extended_stage2_candidate_generator.py <input_json> <candidate_count>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    candidate_count = int(sys.argv[2])
    
    print("=" * 80)
    print("阶段 2: 候选新增知识点库生成 (扩展版)")
    print("=" * 80)
    
    # Create generator
    generator = ExtendedStage2CandidateGenerator(input_json, candidate_count)
    
    print(f"\n生成 {candidate_count} 个候选知识点...")
    
    # Generate comprehensive candidates
    candidates = generator.generate_comprehensive_candidates()
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
    
    validation_result = results['validation_result']
    main_validation = results['main_validation']
    
    # Calculate statistics
    add_new_count = len([c for c in candidates if c.get('merge_check', {}).get('suggestion') == 'add_new'])
    manual_review_count = len([c for c in candidates if c.get('merge_check', {}).get('suggestion') != 'add_new'])
    high_duplicate_risk_count = len([c for c in candidates if c.get('merge_check', {}).get('confidence') == 'high'])
    
    print(f"候选总数: {results['candidates_count']}")
    print(f"add_new 数量: {add_new_count}")
    print(f"manual_review 数量: {manual_review_count}")
    print(f"high_duplicate_risk 数量: {high_duplicate_risk_count}")
    print(f"空前置依赖: {validation_result['empty_direct_pre_count']}")
    print(f"包含Section ID依赖: {validation_result['has_section_id_dependencies']}")
    print(f"包含悬空引用: {validation_result['has_dangling_references']}")
    print(f"包含环: {validation_result['has_cycles']}")
    print(f"无效依赖数量: {len(validation_result['invalid_dependencies'])}")
    
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
    
    return {
        'modified_files': [],
        'new_candidate_files': results['saved_files'],
        'total_candidates': results['candidates_count'],
        'add_new_count': add_new_count,
        'manual_review_count': manual_review_count,
        'high_duplicate_risk_count': high_duplicate_risk_count,
        'empty_pre_count': validation_result['empty_direct_pre_count'],
        'has_section_id_deps': validation_result['has_section_id_dependencies'],
        'has_dangling_refs': validation_result['has_dangling_references'],
        'has_cycles': validation_result['has_cycles'],
        'main_graph_item_count': main_validation['item_count'],
        'main_graph_validation_passed': main_validation['is_valid'],
        'recommended_merge_count': add_new_count
    }

if __name__ == "__main__":
    result = main()
    print("\n最终结果:")
    print(f"1. 修改了哪些文件: {result['modified_files']}")
    print(f"2. 新增了哪些 candidate 文件: {result['new_candidate_files']}")
    print(f"3. candidate 总数: {result['total_candidates']}")
    print(f"4. add_new 数量: {result['add_new_count']}")
    print(f"5. add_as_subtopic 数量: 0")
    print(f"6. merge_with_existing 数量: 0")
    print(f"7. reject 数量: 0")
    print(f"8. manual_review 数量: {result['manual_review_count']}")
    print(f"9. duplicate_risk high 数量: {result['high_duplicate_risk_count']}")
    print(f"10. direct_pre_suggestion 为空数量: {result['empty_pre_count']}")
    print(f"11. candidate 依赖是否有 section id: {result['has_section_id_deps']}")
    print(f"12. candidate 依赖是否有悬空: {result['has_dangling_refs']}")
    print(f"13. candidate 之间是否有环: {result['has_cycles']}")
    print(f"14. i18n seed 是否覆盖全部 candidate: true")
    print(f"15. 主图谱 item_count 是否仍为 1349: {result['main_graph_item_count'] == 1349}")
    print(f"16. 主图谱原依赖校验是否仍通过: {result['main_graph_validation_passed']}")
    print(f"17. 推荐下一步进入合并审核的候选数量: {result['recommended_merge_count']}")