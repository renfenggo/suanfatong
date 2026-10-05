import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

class Stage2Round2CandidateGenerator:
    def __init__(self, main_graph_path: str, existing_candidates_path: str, target_count: int = 280):
        self.main_graph_path = main_graph_path
        self.existing_candidates_path = existing_candidates_path
        self.target_count = target_count
        
        self.load_main_graph()
        self.load_existing_candidates()
        self.initialize_directories()
        
        # 收集所有现有ID用于去重
        self.all_existing_ids = set(self.existing_items.keys()) | set(self.existing_candidate_ids)
        
    def load_main_graph(self):
        """Load main knowledge graph"""
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
    
    def load_existing_candidates(self):
        """Load existing candidates from round1"""
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
    
    def enhanced_duplicate_check(self, candidate: Dict) -> Tuple[str, str, str, float]:
        """
        Enhanced duplicate checking with better classification
        Returns: (duplicate_type, suggestion, reason, confidence)
        """
        candidate_name = candidate['name'].lower()
        candidate_en_name = candidate.get('en_name', '').lower()
        candidate_id = candidate['candidate_id']
        
        # Check exact matches with existing items
        for item_id, item_data in self.existing_items.items():
            existing_name = item_data['name'].lower()
            
            # Exact name match
            if candidate_name == existing_name or candidate_en_name == existing_name:
                return ('exact_match', 'merge_with_existing', f'Exact name match with existing item {item_id}', 0.95)
            
            # Check aliases
            for alias in item_data.get('alias', []):
                if candidate_name == alias.lower() or candidate_en_name == alias.lower():
                    return ('alias_match', 'merge_with_existing', f'Alias match with existing item {item_id}', 0.90)
        
        # Check semantic similarity for subtopic relationships
        subtopic_patterns = [
            (r'(.+)\s*\(.*\)', r'\1'),  # Remove parenthetical content
            (r'(.+)\s*-\s*.+', r'\1'),   # Remove dash-separated content
            (r'(.+)\s*::\s*.+', r'\1'),  # Remove colon-separated content
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
                    return ('subtopic', 'add_as_subtopic', f'Appears to be a subtopic of existing item {item_id}', 0.75)
                else:
                    return ('parent_topic', 'manual_review', f'Appears to be parent topic of existing item {item_id}', 0.70)
        
        # Check for high similarity (potential duplicates)
        for item_id, item_data in self.existing_items.items():
            existing_name = item_data['name'].lower()
            similarity = self.calculate_similarity(candidate_name, existing_name)
            
            if similarity > 0.85:
                return ('high_similarity', 'manual_review', f'High similarity ({similarity:.2f}) with existing item {item_id}', 0.80)
            elif similarity > 0.75:
                return ('medium_similarity', 'manual_review', f'Medium similarity ({similarity:.2f}) with existing item {item_id}', 0.60)
        
        # Check with existing candidates
        for existing_candidate in self.existing_candidates:
            existing_name = existing_candidate['name'].lower()
            existing_en = existing_candidate.get('en_name', '').lower()
            
            if candidate_name == existing_name or candidate_en_name == existing_en:
                return ('candidate_duplicate', 'reject', f'Duplicate with existing candidate {existing_candidate["candidate_id"]}', 0.95)
            
            similarity = max(
                self.calculate_similarity(candidate_name, existing_name),
                self.calculate_similarity(candidate_en_name, existing_en) if existing_en else 0
            )
            
            if similarity > 0.85:
                return ('candidate_high_similarity', 'reject', f'High similarity with existing candidate {existing_candidate["candidate_id"]}', 0.85)
        
        # No significant duplicates found
        return ('no_duplicate', 'add_new', 'No significant duplicates found', 0.90)
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using simple overlap"""
        if not str1 or not str2:
            return 0.0
        
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def validate_dependencies(self, candidate: Dict) -> Tuple[bool, List[str]]:
        """Validate candidate dependencies"""
        issues = []
        
        # Check direct_pre_suggestion
        direct_pre = candidate.get('direct_pre_suggestion', [])
        
        for dep in direct_pre:
            # Check for section IDs (should be item IDs only)
            if re.match(r'^\d+\.\d+$', dep):
                issues.append(f"Section ID found in direct_pre_suggestion: {dep}")
            
            # Check if reference exists
            if dep not in self.existing_items and dep not in self.existing_candidate_ids:
                issues.append(f"Dangling reference: {dep}")
        
        return len(issues) == 0, issues
    
    def check_for_cycles(self, candidates: List[Dict]) -> List[str]:
        """Check for cycles in candidate dependencies"""
        # Build dependency graph
        graph = defaultdict(list)
        candidate_ids = {c['candidate_id'] for c in candidates}
        
        for candidate in candidates:
            candidate_id = candidate['candidate_id']
            for dep in candidate.get('direct_pre_suggestion', []):
                if dep in candidate_ids:
                    graph[candidate_id].append(dep)
        
        # Detect cycles using DFS
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph[node]:
                if dfs(neighbor, path + [node]):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in candidate_ids:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    # A. 高级图论 - 50~70个候选
    def generate_advanced_graph_candidates(self) -> List[Dict]:
        candidates = []
        
        # Dominator Tree 细分
        candidates.extend([
            {
                "candidate_id": "cand.graph.dominator_tree.lengauer_tarjan",
                "name": "支配树 (Lengauer-Tarjan)",
                "en_name": "Dominator Tree (Lengauer-Tarjan)",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_graph", "dominator_tree", "graph_analysis"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "支配树的高效构造算法，用于快速求解支配关系和路径问题",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.13.1", "2.13.2"],
                "rel_suggestion": ["2.13.6", "2.16.1"],
                "parent_concept_suggestion": "支配树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "支配树 (Lengauer-Tarjan)",
                    "en": "Dominator Tree (Lengauer-Tarjan)",
                    "ja": "支配木 (Lengauer-Tarjan)",
                    "ko": "지배 트리 (Lengauer-Tarjan)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.dominator_tree.applications",
                "name": "支配树应用",
                "en_name": "Dominator Tree Applications",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L4",
                "difficulty": 8,
                "tracks": ["advanced_graph", "dominator_tree", "problem_solving"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "支配树在必经点、关键路径、支配查询等问题中的应用",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["cand.graph.dominator_tree.lengauer_tarjan"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "支配树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "支配树应用",
                    "en": "Dominator Tree Applications",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Dynamic Connectivity
        candidates.extend([
            {
                "candidate_id": "cand.graph.dynamic_connectivity.offline",
                "name": "动态连通性 (离线)",
                "en_name": "Dynamic Connectivity (Offline)",
                "category_suggestion": "算法",
                "section_suggestion": "2.16",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_graph", "dynamic_graph", "offline_algorithms"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "离线处理动态连通性问题，使用时间分治和DSU rollback",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.16.1", "2.16.2"],
                "rel_suggestion": ["2.13.6", "cand.ds.rollback_dsu"],
                "parent_concept_suggestion": "动态连通性",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "动态连通性 (离线)",
                    "en": "Dynamic Connectivity (Offline)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.dynamic_connectivity.euler_tour_tree",
                "name": "欧拉游走树 (Euler Tour Tree)",
                "en_name": "Euler Tour Tree",
                "category_suggestion": "算法",
                "section_suggestion": "2.16",
                "level": "L5",
                "difficulty": 10,
                "tracks": ["advanced_graph", "dynamic_graph", "advanced_data_structure"],
                "audience": ["expert", "contest"],
                "visibility": "public",
                "learning_path_policy": "expert_branch",
                "reason_to_add": "使用ETT支持在线动态森林连通性查询和更新",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.16.1", "cand.ds.implicit_treap"],
                "rel_suggestion": ["2.16.2", "cand.graph.dynamic_connectivity.offline"],
                "parent_concept_suggestion": "动态连通性",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "欧拉游走树 (Euler Tour Tree)",
                    "en": "Euler Tour Tree",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Directed MST / Zhu-Liu
        candidates.extend([
            {
                "candidate_id": "cand.graph.directed_mst.zhu_liu",
                "name": "有向最小生成树 (朱刘算法)",
                "en_name": "Directed MST (Zhu-Liu Algorithm)",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_graph", "mst", "minimum_spanning_tree"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "求解有向图的最小生成树，朱刘算法的经典实现",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.13.1", "2.13.3"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "最小生成树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "有向最小生成树 (朱刘算法)",
                    "en": "Directed MST (Zhu-Liu Algorithm)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Gomory-Hu Tree
        candidates.append({
            "candidate_id": "cand.graph.gomory_hu_tree",
            "name": "Gomory-Hu 树",
            "en_name": "Gomory-Hu Tree",
            "category_suggestion": "算法",
            "section_suggestion": "2.18",
            "level": "L5",
            "difficulty": 10,
            "tracks": ["advanced_graph", "network_flow", "graph_optimization"],
            "audience": ["expert", "contest"],
            "visibility": "public",
            "learning_path_policy": "expert_branch",
            "reason_to_add": "用O(n)次最大流构建所有点对最小割的紧凑表示",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.18.1", "2.18.2"],
            "rel_suggestion": ["2.18.3", "2.13.6"],
            "parent_concept_suggestion": "网络流",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "Gomory-Hu 树",
                "en": "Gomory-Hu Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Stoer-Wagner
        candidates.append({
            "candidate_id": "cand.graph.global_min_cut.stoer_wagner",
            "name": "全局最小割 (Stoer-Wagner)",
            "en_name": "Global Minimum Cut (Stoer-Wagner)",
            "category_suggestion": "算法",
            "section_suggestion": "2.13",
            "level": "L4",
            "difficulty": 8,
            "tracks": ["advanced_graph", "graph_optimization", "minimum_cut"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "非加权图全局最小割的高效算法",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.13.1", "2.13.2"],
            "rel_suggestion": ["2.18.1", "cand.graph.gomory_hu_tree"],
            "parent_concept_suggestion": "最小割",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "全局最小割 (Stoer-Wagner)",
                "en": "Global Minimum Cut (Stoer-Wagner)",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Minimum Mean Cycle
        candidates.extend([
            {
                "candidate_id": "cand.graph.minimum_mean_cycle.karp",
                "name": "最小平均权环 (Karp)",
                "en_name": "Minimum Mean Cycle (Karp)",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_graph", "graph_optimization", "cycle_detection"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "寻找图中平均权值最小的环，Karp算法实现",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.13.2", "2.13.3"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "环问题",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "最小平均权环 (Karp)",
                    "en": "Minimum Mean Cycle (Karp)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.minimum_mean_cycle.hartmann_orlin",
                "name": "最小平均权环 (Hartmann-Orlin)",
                "en_name": "Minimum Mean Cycle (Hartmann-Orlin)",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L5",
                "difficulty": 10,
                "tracks": ["advanced_graph", "graph_optimization", "cycle_detection"],
                "audience": ["expert", "contest"],
                "visibility": "public",
                "learning_path_policy": "expert_branch",
                "reason_to_add": "改进的最小平均权环算法，更优的常数因子",
                "global_relevance": "low",
                "direct_pre_suggestion": ["cand.graph.minimum_mean_cycle.karp"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "环问题",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "最小平均权环 (Hartmann-Orlin)",
                    "en": "Minimum Mean Cycle (Hartmann-Orlin)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # General Graph Matching / Blossom
        candidates.extend([
            {
                "candidate_id": "cand.graph.general_matching.blossom",
                "name": "一般图最大匹配 (Blossom)",
                "en_name": "General Graph Maximum Matching (Blossom)",
                "category_suggestion": "算法",
                "section_suggestion": "2.18",
                "level": "L5",
                "difficulty": 10,
                "tracks": ["advanced_graph", "matching", "graph_theory"],
                "audience": ["expert", "contest"],
                "visibility": "public",
                "learning_path_policy": "expert_branch",
                "reason_to_add": "求解一般图（非二分图）的最大匹配，Blossom算法",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.18.1", "2.18.2"],
                "rel_suggestion": ["2.18.3", "2.13.6"],
                "parent_concept_suggestion": "匹配问题",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "一般图最大匹配 (Blossom)",
                    "en": "General Graph Maximum Matching (Blossom)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.general_matching.weighted",
                "name": "一般图最大权匹配",
                "en_name": "General Graph Maximum Weight Matching",
                "category_suggestion": "算法",
                "section_suggestion": "2.18",
                "level": "L5",
                "difficulty": 10,
                "tracks": ["advanced_graph", "matching", "graph_theory"],
                "audience": ["expert", "contest"],
                "visibility": "public",
                "learning_path_policy": "expert_branch",
                "reason_to_add": "一般图的最大权完美匹配算法",
                "global_relevance": "low",
                "direct_pre_suggestion": ["cand.graph.general_matching.blossom"],
                "rel_suggestion": ["2.18.3", "2.13.6"],
                "parent_concept_suggestion": "匹配问题",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "一般图最大权匹配",
                    "en": "General Graph Maximum Weight Matching",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Matroid
        candidates.extend([
            {
                "candidate_id": "cand.graph.matroid.basics",
                "name": "拟阵基础",
                "en_name": "Matroid Basics",
                "category_suggestion": "算法",
                "section_suggestion": "2.18",
                "level": "L4",
                "difficulty": 8,
                "tracks": ["advanced_graph", "combinatorial_optimization", "matroid"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "拟阵的定义、性质和基本应用",
                "global_relevance": "low",
                "direct_pre_suggestion": ["2.18.1", "2.18.2"],
                "rel_suggestion": ["2.13.6", "cand.graph.matroid.intersection"],
                "parent_concept_suggestion": "组合优化",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "拟阵基础",
                    "en": "Matroid Basics",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.matroid.intersection",
                "name": "拟阵交",
                "en_name": "Matroid Intersection",
                "category_suggestion": "算法",
                "section_suggestion": "2.18",
                "level": "L5",
                "difficulty": 10,
                "tracks": ["advanced_graph", "combinatorial_optimization", "matroid"],
                "audience": ["expert", "contest"],
                "visibility": "public",
                "learning_path_policy": "expert_branch",
                "reason_to_add": "两个拟阵的最大交集算法及优化应用",
                "global_relevance": "low",
                "direct_pre_suggestion": ["cand.graph.matroid.basics"],
                "rel_suggestion": ["2.18.3", "2.13.6"],
                "parent_concept_suggestion": "组合优化",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "拟阵交",
                    "en": "Matroid Intersection",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Functional Graph
        candidates.extend([
            {
                "candidate_id": "cand.graph.functional_tree.advanced",
                "name": "函数图进阶",
                "en_name": "Functional Graph Advanced",
                "category_suggestion": "算法",
                "section_suggestion": "2.16",
                "level": "L3",
                "difficulty": 7,
                "tracks": ["advanced_graph", "functional_graph", "graph_analysis"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "函数图的高级应用：环检测、路径计数、期望计算",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.16.1", "2.16.2"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "函数图",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "函数图进阶",
                    "en": "Functional Graph Advanced",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # 2-SAT 变形
        candidates.extend([
            {
                "candidate_id": "cand.graph.sat2.modeling_variants",
                "name": "2-SAT 建模变形",
                "en_name": "2-SAT Modeling Variants",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L3",
                "difficulty": 7,
                "tracks": ["advanced_graph", "sat", "modeling"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "各种复杂约束的2-SAT建模技巧和变形",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.13.1", "2.13.4"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "2-SAT",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "2-SAT 建模变形",
                    "en": "2-SAT Modeling Variants",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Difference Constraints 变形
        candidates.extend([
            {
                "candidate_id": "cand.graph.difference_constraints.modeling",
                "name": "差分约束建模变形",
                "en_name": "Difference Constraints Modeling",
                "category_suggestion": "算法",
                "section_suggestion": "2.13",
                "level": "L3",
                "difficulty": 7,
                "tracks": ["advanced_graph", "difference_constraints", "modeling"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "复杂不等式约束的差分约束建模技巧",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.13.2", "2.13.3"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "差分约束",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "差分约束建模变形",
                    "en": "Difference Constraints Modeling",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Bridge Tree / Block-Cut Tree
        candidates.extend([
            {
                "candidate_id": "cand.graph.bridge_tree.applications",
                "name": "桥树应用",
                "en_name": "Bridge Tree Applications",
                "category_suggestion": "算法",
                "section_suggestion": "2.16",
                "level": "L3",
                "difficulty": 7,
                "tracks": ["advanced_graph", "graph_decomposition", "problem_solving"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "桥树在路径查询、连通性问题中的应用",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.16.1", "2.16.2"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "桥树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "桥树应用",
                    "en": "Bridge Tree Applications",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.graph.block_cut_tree.applications",
                "name": "点双连通分量树应用",
                "en_name": "Block-Cut Tree Applications",
                "category_suggestion": "算法",
                "section_suggestion": "2.16",
                "level": "L3",
                "difficulty": 7,
                "tracks": ["advanced_graph", "graph_decomposition", "problem_solving"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "点双连通分量树在节点查询、连通性问题中的应用",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.16.1", "2.16.2"],
                "rel_suggestion": ["2.13.6", "2.18.1"],
                "parent_concept_suggestion": "点双连通分量树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "点双连通分量树应用",
                    "en": "Block-Cut Tree Applications",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        return candidates[:15]  # 控制数量
    
    # B. 高级数据结构 - 50~70个候选
    def generate_advanced_data_structure_candidates(self) -> List[Dict]:
        candidates = []
        
        # Segment Tree Beats 细分
        candidates.extend([
            {
                "candidate_id": "cand.ds.segment_tree_beats.range_chmin",
                "name": "Segment Tree Beats (Range Chmin)",
                "en_name": "Segment Tree Beats (Range Chmin)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_data_structure", "segment_tree", "range_operations"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "支持区间取最小值操作的线段树高级变种",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.15.1", "2.15.2"],
                "rel_suggestion": ["2.15.4", "cand.ds.segment_tree_beats.range_chmax"],
                "parent_concept_suggestion": "Segment Tree Beats",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "Segment Tree Beats (Range Chmin)",
                    "en": "Segment Tree Beats (Range Chmin)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.ds.segment_tree_beats.range_chmax",
                "name": "Segment Tree Beats (Range Chmax)",
                "en_name": "Segment Tree Beats (Range Chmax)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_data_structure", "segment_tree", "range_operations"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "支持区间取最大值操作的线段树高级变种",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.15.1", "2.15.2"],
                "rel_suggestion": ["2.15.4", "cand.ds.segment_tree_beats.range_chmin"],
                "parent_concept_suggestion": "Segment Tree Beats",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "Segment Tree Beats (Range Chmax)",
                    "en": "Segment Tree Beats (Range Chmax)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.ds.segment_tree_beats.range_add",
                "name": "Segment Tree Beats (Range Add)",
                "en_name": "Segment Tree Beats (Range Add)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_data_structure", "segment_tree", "range_operations"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "结合区间加法的Segment Tree Beats完整实现",
                "global_relevance": "high",
                "direct_pre_suggestion": ["cand.ds.segment_tree_beats.range_chmin"],
                "rel_suggestion": ["2.15.4", "2.15.5"],
                "parent_concept_suggestion": "Segment Tree Beats",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "Segment Tree Beats (Range Add)",
                    "en": "Segment Tree Beats (Range Add)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Li Chao Tree 细分
        candidates.extend([
            {
                "candidate_id": "cand.ds.li_chao_tree.minimum",
                "name": "李超线段树 (最小值)",
                "en_name": "Li Chao Tree (Minimum)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 8,
                "tracks": ["advanced_data_structure", "convex_hull", "optimization"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "动态维护直线集合，支持查询最小值的李超树",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.15.1", "2.15.2"],
                "rel_suggestion": ["2.15.4", "cand.ds.li_chao_tree.maximum"],
                "parent_concept_suggestion": "李超线段树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "李超线段树 (最小值)",
                    "en": "Li Chao Tree (Minimum)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.ds.li_chao_tree.maximum",
                "name": "李超线段树 (最大值)",
                "en_name": "Li Chao Tree (Maximum)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 8,
                "tracks": ["advanced_data_structure", "convex_hull", "optimization"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "动态维护直线集合，支持查询最大值的李超树",
                "global_relevance": "high",
                "direct_pre_suggestion": ["2.15.1", "2.15.2"],
                "rel_suggestion": ["2.15.4", "cand.ds.li_chao_tree.minimum"],
                "parent_concept_suggestion": "李超线段树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "李超线段树 (最大值)",
                    "en": "Li Chao Tree (Maximum)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.ds.li_chao_tree.segment",
                "name": "李超线段树 (线段)",
                "en_name": "Li Chao Tree (Segment)",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_data_structure", "convex_hull", "optimization"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "支持线段插入和查询的扩展李超树",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["cand.ds.li_chao_tree.minimum"],
                "rel_suggestion": ["2.15.4", "2.15.5"],
                "parent_concept_suggestion": "李超线段树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "李超线段树 (线段)",
                    "en": "Li Chao Tree (Segment)",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Wavelet Tree / Wavelet Matrix
        candidates.extend([
            {
                "candidate_id": "cand.ds.wavelet_tree.basic",
                "name": "小波树基础",
                "en_name": "Wavelet Tree Basic",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 8,
                "tracks": ["advanced_data_structure", "wavelet_tree", "range_query"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "小波树的基本结构和区间查询功能",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["2.15.1", "2.15.2"],
                "rel_suggestion": ["2.15.4", "cand.ds.wavelet_matrix"],
                "parent_concept_suggestion": "小波树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "小波树基础",
                    "en": "Wavelet Tree Basic",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            },
            {
                "candidate_id": "cand.ds.wavelet_matrix",
                "name": "小波矩阵",
                "en_name": "Wavelet Matrix",
                "category_suggestion": "数据结构",
                "section_suggestion": "2.15",
                "level": "L4",
                "difficulty": 9,
                "tracks": ["advanced_data_structure", "wavelet_tree", "range_query"],
                "audience": ["advanced", "contest"],
                "visibility": "public",
                "learning_path_policy": "optional",
                "reason_to_add": "小波树的高效实现，支持更快速的区间查询",
                "global_relevance": "medium",
                "direct_pre_suggestion": ["cand.ds.wavelet_tree.basic"],
                "rel_suggestion": ["2.15.4", "2.15.5"],
                "parent_concept_suggestion": "小波树",
                "merge_check": "pending",
                "i18n_seed": {
                    "zh-Hans": "小波矩阵",
                    "en": "Wavelet Matrix",
                    "needs_native_review": True
                },
                "content_status": "outline",
                "review_status": "pending"
            }
        ])
        
        # Merge Sort Tree
        candidates.append({
            "candidate_id": "cand.ds.merge_sort_tree",
            "name": "归并排序树",
            "en_name": "Merge Sort Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "segment_tree", "range_query"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "线段树节点维护排序数组，支持区间第k大查询",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "cand.ds.wavelet_tree.basic"],
            "parent_concept_suggestion": "线段树变种",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "归并排序树",
                "en": "Merge Sort Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Sqrt Tree
        candidates.append({
            "candidate_id": "cand.ds.sqrt_tree",
            "name": "平方根树",
            "en_name": "Sqrt Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L4",
            "difficulty": 8,
            "tracks": ["advanced_data_structure", "sqrt_decomposition", "range_query"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "结合线段树和分块思想的混合数据结构",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "2.15.5"],
            "parent_concept_suggestion": "混合数据结构",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "平方根树",
                "en": "Sqrt Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Disjoint Sparse Table
        candidates.append({
            "candidate_id": "cand.ds.disjoint_sparse_table",
            "name": "不交稀疏表",
            "en_name": "Disjoint Sparse Table",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "sparse_table", "range_query"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持区间可结合查询的稀疏表变种",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "2.15.5"],
            "parent_concept_suggestion": "稀疏表",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "不交稀疏表",
                "en": "Disjoint Sparse Table",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Rollback DSU
        candidates.append({
            "candidate_id": "cand.ds.rollback_dsu",
            "name": "可撤销并查集",
            "en_name": "Rollback DSU",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.16",
            "level": "L4",
            "difficulty": 8,
            "tracks": ["advanced_data_structure", "dsu", "offline_algorithms"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持撤销操作的并查集，用于离线算法",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.16.1", "2.16.2"],
            "rel_suggestion": ["2.16.4", "cand.graph.dynamic_connectivity.offline"],
            "parent_concept_suggestion": "并查集变种",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "可撤销并查集",
                "en": "Rollback DSU",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Persistent DSU
        candidates.append({
            "candidate_id": "cand.ds.persistent_dsu",
            "name": "可持久化并查集",
            "en_name": "Persistent DSU",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L4",
            "difficulty": 9,
            "tracks": ["advanced_data_structure", "dsu", "persistent"],
                "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持历史版本查询的可持久化并查集",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "cand.ds.rollback_dsu"],
            "parent_concept_suggestion": "并查集变种",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "可持久化并查集",
                "en": "Persistent DSU",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Dynamic Segment Tree
        candidates.append({
            "candidate_id": "cand.ds.dynamic_segment_tree",
            "name": "动态开点线段树",
            "en_name": "Dynamic Segment Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "segment_tree", "dynamic"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "按需创建节点的线段树，适用于大坐标范围",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "2.15.5"],
            "parent_concept_suggestion": "线段树变种",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "动态开点线段树",
                "en": "Dynamic Segment Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Implicit Treap
        candidates.append({
            "candidate_id": "cand.ds.implicit_treap",
            "name": "无旋Treap (Implicit Key)",
            "en_name": "Implicit Treap",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "treap", "balanced_tree"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "基于下标的无旋Treap，支持序列操作",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "2.15.5"],
            "parent_concept_suggestion": "Treap",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "无旋Treap (Implicit Key)",
                "en": "Implicit Treap",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Order Statistic Tree
        candidates.append({
            "candidate_id": "cand.ds.order_statistic_tree",
            "name": "顺序统计树",
            "en_name": "Order Statistic Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 6,
            "tracks": ["advanced_data_structure", "balanced_tree", "order_statistics"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持排名和第k大查询的平衡搜索树",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "2.15.5"],
            "parent_concept_suggestion": "平衡搜索树",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "顺序统计树",
                "en": "Order Statistic Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # 2D Fenwick Tree
        candidates.append({
            "candidate_id": "cand.ds.fenwick_tree_2d",
            "name": "二维树状数组",
            "en_name": "2D Fenwick Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "fenwick_tree", "2d_structures"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持二维区间查询和更新的树状数组",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "cand.ds.segment_tree_2d"],
            "parent_concept_suggestion": "树状数组",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "二维树状数组",
                "en": "2D Fenwick Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # 2D Segment Tree
        candidates.append({
            "candidate_id": "cand.ds.segment_tree_2d",
            "name": "二维线段树",
            "en_name": "2D Segment Tree",
            "category_suggestion": "数据结构",
            "section_suggestion": "2.15",
            "level": "L4",
            "difficulty": 8,
            "tracks": ["advanced_data_structure", "segment_tree", "2d_structures"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "支持二维区间查询和更新的线段树",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.15.1", "2.15.2"],
            "rel_suggestion": ["2.15.4", "cand.ds.fenwick_tree_2d"],
            "parent_concept_suggestion": "线段树变种",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "二维线段树",
                "en": "2D Segment Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # DSU on Tree
        candidates.append({
            "candidate_id": "cand.ds.dsu_on_tree",
            "name": "树上启发式合并",
            "en_name": "DSU on Tree",
            "category_suggestion": "算法",
            "section_suggestion": "2.16",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "tree_algorithms", "divide_and_conquer"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "高效的子树信息统计算法，结合重链和DSU",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.16.1", "2.16.2"],
            "rel_suggestion": ["2.16.4", "2.13.6"],
            "parent_concept_suggestion": "树算法",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "树上启发式合并",
                "en": "DSU on Tree",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Small-to-Large Merging
        candidates.append({
            "candidate_id": "cand.ds.small_to_large",
            "name": "小启发式合并",
            "en_name": "Small-to-Large Merging",
            "category_suggestion": "算法",
            "section_suggestion": "2.16",
            "level": "L2",
            "difficulty": 6,
            "tracks": ["advanced_data_structure", "merge_techniques", "optimization"],
            "audience": ["intermediate", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "通用的启发式合并技巧，用于优化时间复杂度",
            "global_relevance": "high",
            "direct_pre_suggestion": ["2.16.1", "2.16.2"],
            "rel_suggestion": ["2.16.4", "cand.ds.dsu_on_tree"],
            "parent_concept_suggestion": "优化技巧",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "小启发式合并",
                "en": "Small-to-Large Merging",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        # Centroid Decomposition Applications
        candidates.append({
            "candidate_id": "cand.ds.centroid_decomposition_applications",
            "name": "点分治应用",
            "en_name": "Centroid Decomposition Applications",
            "category_suggestion": "算法",
            "section_suggestion": "2.16",
            "level": "L3",
            "difficulty": 7,
            "tracks": ["advanced_data_structure", "tree_algorithms", "divide_and_conquer"],
            "audience": ["advanced", "contest"],
            "visibility": "public",
            "learning_path_policy": "optional",
            "reason_to_add": "点分治在各种树问题中的应用技巧",
            "global_relevance": "medium",
            "direct_pre_suggestion": ["2.16.1", "2.16.2"],
            "rel_suggestion": ["2.16.4", "2.13.6"],
            "parent_concept_suggestion": "树算法",
            "merge_check": "pending",
            "i18n_seed": {
                "zh-Hans": "点分治应用",
                "en": "Centroid Decomposition Applications",
                "needs_native_review": True
            },
            "content_status": "outline",
            "review_status": "pending"
        })
        
        return candidates[:20]  # 控制数量
    