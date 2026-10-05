import json
import re
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict

class FinalKnowledgeGraphFusion:
    def __init__(self, json_path, docx_path, mappings_path):
        self.json_path = json_path
        self.docx_path = docx_path
        self.mappings_path = mappings_path
        self.load_data()
        self.initialize_dependency_system()
        
    def load_data(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
            
        with open(self.docx_path, 'r', encoding='utf-8') as f:
            self.docx_kps = json.load(f)
            
        with open(self.mappings_path, 'r', encoding='utf-8') as f:
            self.mappings_data = json.load(f)
            
        print(f"Loaded JSON with {self.get_total_items()} items")
        print(f"Loaded {len(self.docx_kps)} docx knowledge points")
        print(f"Loaded mappings: {len(self.mappings_data['exact_matches'])} exact, {len(self.mappings_data['pattern_matches'])} pattern")
        
    def get_total_items(self):
        return sum(len(s['items']) for cat in self.json_data['categories'] for s in cat['sections'])
    
    def initialize_dependency_system(self):
        """Initialize comprehensive dependency system"""
        
        # Section level dependencies
        self.section_dependencies = {
            # C++ Syntax dependencies
            '1.1': [],  # Program structure - no dependencies
            '1.2': ['1.1'],  # I/O requires basic structure
            '1.3': ['1.1'],  # Variables require basic structure
            '1.4': ['1.3'],  # Operators require variables
            '1.5': ['1.3', '1.4'],  # Control structures require variables and operators
            '1.6': ['1.3', '1.5'],  # Arrays require variables and control structures
            '1.7': ['1.3', '1.5'],  # Functions require variables and control structures
            '1.8': ['1.3', '1.6', '1.7'],  # STL requires variables, arrays, and functions
            '1.9': ['1.1', '1.2'],  # Preprocessing requires basic structure and I/O
            '1.10': ['1.1', '1.2', '1.3', '1.5'],  # Common errors require basics
            
            # Algorithm dependencies
            '2.1': ['1.3', '1.4', '1.5', '1.6', '1.7'],  # Basic algorithms require C++ basics
            '2.2': ['1.3', '1.5', '1.6', '1.8', '2.1'],  # Sorting requires arrays, functions, STL, basic algorithms
            '2.3': ['1.3', '1.4', '1.5', '2.1'],  # Binary search requires basics and algorithms
            '2.4': ['1.3', '1.4', '1.5', '1.6', '2.1'],  # Prefix/difference require basics and algorithms
            '2.5': ['1.3', '1.5', '2.1'],  # Two pointers require basics and algorithms
            '2.6': ['1.3', '1.5', '2.1'],  # Greedy requires basics and algorithms
            '2.7': ['1.3', '1.5', '1.7', '2.1', '3.1'],  # Search requires recursion, algorithms, and basic data structures
            '2.8': ['1.3', '1.5', '1.7', '2.1', '2.3', '2.4'],  # DP requires recursion, binary search, prefix sums
            '2.9': ['1.3', '1.7', '2.1', '3.1', '3.9'],  # Graph basics require algorithms and graph storage
            '2.13': ['1.3', '1.7', '2.1', '2.3', '2.9', '3.2', '3.3', '3.5'],  # Shortest path requires search, heap, etc.
            '2.14': ['1.3', '1.7', '2.1', '2.9', '3.6'],  # Tree algorithms require tree structures
            '2.15': ['1.3', '1.7', '2.1', '2.7', '2.9', '3.4'],  # Connected components require search and union-find
            '2.16': ['1.3', '1.7', '2.1', '2.9', '2.15', '3.4'],  # Flow algorithms require connected components and union-find
            '2.10': ['1.3', '1.5', '1.6', '2.1', '3.6'],  # String algorithms require tree structures
            '2.11': ['1.4', '2.1'],  # Bit operations require operators and algorithms
            '2.12': ['1.3', '2.1', '2.8', '4.2'],  # Numerical methods require DP and modular arithmetic
            '2.17': ['1.3', '2.1', '4.2', '4.8'],  # Linear algebra requires mathematics
            '2.18': ['2.1', '2.4', '2.7', '2.8', '3.7', '3.12'],  # Advanced techniques require advanced algorithms and data structures
            
            # Data Structure dependencies
            '3.1': ['1.3', '1.5', '1.6', '1.7'],  # Linear structures require C++ basics
            '3.2': ['1.3', '1.5', '1.7', '3.1'],  # Stack/Queue require linear structures and recursion
            '3.3': ['1.3', '1.5', '1.7', '1.8', '3.1'],  # Set/Map require STL and linear structures
            '3.4': ['1.3', '1.5', '1.7', '2.1', '3.1'],  # Union-find requires algorithms and linear structures
            '3.5': ['1.3', '1.5', '1.7', '2.1', '3.1'],  # Heap requires algorithms and linear structures
            '3.6': ['1.3', '1.5', '1.7', '2.1', '3.1', '3.5'],  # Tree structures require heap
            '3.7': ['1.3', '1.5', '1.7', '2.1', '2.4', '3.6'],  # Segment tree requires prefix sums and trees
            '3.8': ['1.3', '1.5', '1.7', '2.1', '3.6', '2.10'],  # String structures require string algorithms
            '3.9': ['1.3', '1.5', '1.7', '3.1'],  # Graph storage requires linear structures
            '3.10': ['1.3', '1.5', '1.7', '2.1', '3.6'],  # Balanced trees require tree structures
            '3.11': ['1.3', '1.5', '1.7', '2.1', '3.6', '3.7'],  # Persistent data structures require segment trees
            '3.12': ['1.3', '1.5', '1.7', '2.1', '2.4', '3.7'],  # Decomposition structures require segment trees
            
            # Mathematics dependencies
            '4.1': ['1.3'],  # Integer theory requires variables
            '4.2': ['1.3', '1.4', '4.1'],  # Modular arithmetic requires integer theory
            '4.3': ['1.3', '2.1', '4.1'],  # Combinatorics requires algorithms and integer theory
            '4.4': ['1.3', '2.1'],  # Discrete mathematics requires algorithms
            '4.5': ['1.3', '2.1', '4.3', '4.4'],  # Graph mathematics requires combinatorics
            '4.6': ['1.3', '2.1', '4.3'],  # Probability requires combinatorics
            '4.7': ['1.3', '1.4', '2.1', '4.1'],  # Geometry requires integer theory
            '4.8': ['1.3', '2.1', '4.1', '4.2', '4.3'],  # Advanced mathematics requires all basics
            '4.0': ['1.3', '2.1', '4.1'],  # Math basics require integer theory
            
            # C++ Programming/Debugging dependencies
            '5.1': ['1.2', '1.3'],  # I/O tricks require basic I/O and variables
            '5.2': ['1.3', '1.4', '1.6', '2.11'],  # Character/number tricks require bit operations
            '5.3': ['1.3', '1.5', '1.6'],  # Index/enumeration tricks require basics
            '5.4': ['1.1', '1.8', '2.1'],  # Code tricks require STL and algorithms
            '5.5': ['1.3', '1.7', '2.9', '3.9'],  # Graph implementation tricks require graph storage
            '5.6': ['1.3', '1.7', '2.8'],  # DP implementation tricks require DP
            '5.7': ['1.1', '1.2', '1.3'],  # Debugging requires basics
            '5.8': ['1.1', '1.2', '1.3', '5.7'],  # Error location requires debugging
            '5.9': ['1.1', '1.2', '5.1', '5.7'],  # Engineering habits require I/O and debugging
        }
        
        # Item level dependency patterns
        self.item_dependency_patterns = {
            # Sorting dependencies
            '冒泡排序': [],
            '选择排序': [],
            '插入排序': [],
            '归并排序': ['2.1.5'],
            '快速排序': ['2.1.5'],
            '堆排序': ['3.5.1'],
            '计数排序': [],
            '桶排序': [],
            '基数排序': [],
            
            # Binary search dependencies
            '二分查找': [],
            '左边界': ['2.3.1'],
            '右边界': ['2.3.1'],
            '整数二分': ['2.3.1'],
            '实数二分': ['2.3.4'],
            '二分答案': ['2.3.4', '2.3.7', '2.3.8'],
            
            # DP dependencies
            '线性DP': ['2.1.3', '2.1.4'],
            '背包DP': ['2.8.1', '2.8.2'],
            '区间DP': ['2.1.5', '2.4.1'],
            '树形DP': ['3.6.1', '2.7.1'],
            '状态压缩DP': ['2.11.1', '4.3.1'],
            
            # Graph dependencies
            'DFS': ['2.7.1'],
            'BFS': ['3.2.1'],
            '最短路': ['2.7.1', '2.3.1'],
            '最小生成树': ['2.7.1', '3.4.1'],
            
            # Data structure dependencies
            '并查集': ['3.1.1'],
            '线段树': ['3.6.1', '2.4.1'],
            '树状数组': ['2.4.1', '3.6.1'],
            '主席树': ['3.7.1', '2.4.6'],
            '平衡树': ['3.6.1', '2.3.1'],
        }
    
    def determine_merge_type(self, docx_name, json_item_name):
        """Determine the merge type for knowledge points"""
        docx_lower = docx_name.lower()
        json_lower = json_item_name.lower()
        
        if docx_lower == json_lower:
            return 'same_concept'
        elif docx_lower in json_lower or json_lower in docx_lower:
            return 'alias'
        elif self.is_subtopic(docx_name, json_item_name):
            return 'subtopic'
        else:
            return 'new_concept'
    
    def is_subtopic(self, potential_subtopic, potential_parent):
        """Check if one concept is a subtopic of another"""
        sub_keywords = ['：', ':', '的', '实现', '技巧', '方法', '基础', '入门']
        
        for keyword in sub_keywords:
            if keyword in potential_subtopic:
                base_name = potential_subtopic.split(keyword)[0].strip()
                if base_name == potential_parent:
                    return True
                    
        return False
    
    def assign_difficulty_level(self, kp_name, section_level):
        """Assign difficulty level based on knowledge point name and section"""
        kp_lower = kp_name.lower()
        
        # L5: Extended/Non-mainstream topics
        l5_keywords = ['机器学习', '数据库', '操作系统', '汇编', '线程', '进程', '分布式', 
                      '嵌入式', '驱动', '内核', '操作系统', '数据库', 'web', '网络编程',
                      '人工智能', '深度学习', '神经网络', '计算机视觉', '自然语言处理']
        
        # L4: Advanced topics
        l4_keywords = ['主席树', '可持久化', 'lct', '动态树', '网络流', '费用流', '上下界',
                      '后缀自动机', '后缀数组', 'manacher', 'ac自动机', '最小生成树',
                      '树链剖分', '动态树', '平衡树', 'treap', 'splay', '线段树分裂',
                      'cdq分治', '整体二分', '分块', '莫队', '群论', 'polya', '反演',
                      '多项式', 'fft', 'ntt', '数论变换', '高次剩余', '二次剩余']
        
        # L3: Core competitive programming topics
        l3_keywords = ['dp', '动态规划', '线段树', '树状数组', '并查集', '最短路', '网络流',
                      '最大流', '最小割', '二分图', '匹配', '匈牙利', 'tarjan', '强连通',
                      '割点', '桥', '树上算法', 'lca', '倍增', '搜索', 'dfs', 'bfs',
                      '概率dp', '期望dp', '树形dp', '区间dp', '状态压缩', '数论', '组合数学',
                      '计算几何', '凸包', '旋转卡壳', '半平面交', '字符串', 'kmp', 'hash']
        
        for keyword in l5_keywords:
            if keyword in kp_lower:
                return 'L5'
                
        for keyword in l4_keywords:
            if keyword in kp_lower:
                return 'L4'
                
        for keyword in l3_keywords:
            if keyword in kp_lower:
                return 'L3'
        
        # Default to section level or L2 for most algorithm topics
        if section_level in ['L1', 'L2', 'L3', 'L4']:
            return section_level
        return 'L2'
    
    def process_item_mapping(self, mapping):
        """Process a single item mapping and add source information"""
        result = {
            'docx_id': mapping['docx_id'],
            'docx_name': mapping['docx_name'],
            'target_category': mapping.get('category'),
            'target_section_id': mapping.get('section_id'),
            'target_section_name': mapping.get('section_name'),
            'action': 'merge_into_existing_section',
            'reason': mapping.get('reason', ''),
        }
        
        # Add merge type if exact match
        if mapping.get('match_type') == 'exact':
            result['merge_type'] = 'same_concept'
            result['item_id'] = mapping.get('item_id')
        elif mapping.get('match_type') == 'pattern':
            result['merge_type'] = 'new_concept'
            result['score'] = mapping.get('score', 0)
        
        # Determine difficulty level
        section_id = mapping.get('section_id', '')
        section_level = 'L2'  # Default level
        
        # Find the section level from the original data
        for cat in self.json_data['categories']:
            for section in cat['sections']:
                if section['id'] == section_id:
                    section_level = section.get('level', 'L2')
                    break
            if section_level != 'L2':
                break
        
        result['level'] = self.assign_difficulty_level(mapping['docx_name'], section_level)
        
        return result
    
    def create_merged_structure(self):
        """Create the final merged knowledge graph structure"""
        merged_data = {
            'meta': {
                'title': '算法竞赛知识图谱融合版',
                'source_files': ['io_v4_4.json', '算法知识图谱aa.docx'],
                'merge_strategy': '以原JSON五大类为骨架，docx作为扩展知识点来源',
                'dependency_rule': {
                    'pre': '强前置依赖',
                    'rel': '弱相关关系'
                },
                'statistics': {
                    'original_items': 592,
                    'docx_items': 1000,
                    'exact_matches': len(self.mappings_data['exact_matches']),
                    'pattern_matches': len(self.mappings_data['pattern_matches']),
                    'new_sections_needed': len(self.mappings_data['new_sections']),
                    'manual_review_needed': len(self.mappings_data['manual_review']),
                    'total_merged': len(self.mappings_data['exact_matches']) + len(self.mappings_data['pattern_matches'])
                }
            },
            'categories': []
        }
        
        # Process each category
        for category in self.json_data['categories']:
            merged_category = {
                'name': category['name'],
                'sections': []
            }
            
            # Process each section in the category
            for section in category['sections']:
                merged_section = self.process_section(section)
                merged_category['sections'].append(merged_section)
            
            merged_data['categories'].append(merged_category)
        
        return merged_data
    
    def process_section(self, section):
        """Process a single section and add merged knowledge points"""
        merged_section = {
            'id': section['id'],
            'name': section['name'],
            'level': section.get('level', 'L1'),
            'pre': self.section_dependencies.get(section['id'], section.get('pre', [])),
            'rel': section.get('rel', []),
            'items': [],
            'learning_blocks': section.get('learning_blocks', []),
            'docx_mappings': []
        }
        
        # Process existing items
        for item in section['items']:
            processed_item = self.process_item(item, section['id'])
            merged_section['items'].append(processed_item)
        
        # Add docx mappings for this section
        section_mappings = self.get_section_mappings(section['id'])
        merged_section['docx_mappings'] = section_mappings
        
        return merged_section
    
    def process_item(self, item, section_id):
        """Process a single item and add metadata"""
        processed_item = item.copy()
        
        # Add merge information
        processed_item['merge_type'] = 'original'
        processed_item['source'] = ['json']
        processed_item['docx_ids'] = []
        
        # Find docx items that map to this item
        matching_docx = self.find_matching_docx_items(item['name'], section_id)
        if matching_docx:
            processed_item['docx_ids'].extend([m['docx_id'] for m in matching_docx])
            processed_item['source'].append('docx')
            if matching_docx[0].get('match_type') == 'exact':
                processed_item['merge_type'] = 'same_concept'
        
        return processed_item
    
    def find_matching_docx_items(self, item_name, section_id):
        """Find docx items that map to a specific item"""
        matches = []
        
        # Check exact matches
        for match in self.mappings_data['exact_matches']:
            if (match.get('section_id') == section_id and 
                match.get('item_id') and match.get('item_id').endswith(item_name)):
                matches.append(match)
        
        # Check pattern matches with high score
        for match in self.mappings_data['pattern_matches']:
            if (match.get('section_id') == section_id and 
                match.get('score', 0) >= 2):
                matches.append(match)
        
        return matches
    
    def get_section_mappings(self, section_id):
        """Get all docx mappings for a specific section"""
        mappings = []
        
        for match in self.mappings_data['exact_matches']:
            if match.get('section_id') == section_id:
                mappings.append(self.process_item_mapping(match))
        
        for match in self.mappings_data['pattern_matches']:
            if match.get('section_id') == section_id:
                mappings.append(self.process_item_mapping(match))
        
        return mappings
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        total_docx = len(self.docx_kps)
        exact_matches = len(self.mappings_data['exact_matches'])
        pattern_matches = len(self.mappings_data['pattern_matches'])
        new_sections = len(self.mappings_data['new_sections'])
        manual_review = len(self.mappings_data['manual_review'])
        
        report = {
            'overall_statistics': {
                'total_docx_knowledge_points': total_docx,
                'exact_matches': exact_matches,
                'pattern_matches': pattern_matches,
                'new_section_suggestions': new_sections,
                'manual_review_needed': manual_review,
                'successfully_mapped': exact_matches + pattern_matches,
                'mapping_success_rate': f"{((exact_matches + pattern_matches) / total_docx * 100):.2f}%"
            },
            
            'merge_types': {
                'same_concept': exact_matches,
                'new_concept': pattern_matches,
                'create_new_section': new_sections,
                'needs_manual_review': manual_review
            },
            
            'category_distribution': self.analyze_category_distribution(),
            
            'new_sections_analysis': self.analyze_new_sections(),
            
            'dependency_updates': self.analyze_dependency_changes(),
            
            'quality_issues': self.identify_quality_issues(),
            
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def analyze_category_distribution(self):
        """Analyze distribution of mappings across categories"""
        distribution = {}
        
        for match in self.mappings_data['exact_matches'] + self.mappings_data['pattern_matches']:
            category = match.get('category', 'Unknown')
            distribution[category] = distribution.get(category, 0) + 1
        
        return distribution
    
    def analyze_new_sections(self):
        """Analyze suggested new sections"""
        sections_analysis = {}
        
        for match in self.mappings_data['new_sections']:
            section_name = match.get('suggested_section', {}).get('name', 'Unknown')
            if section_name not in sections_analysis:
                sections_analysis[section_name] = {
                    'category': match.get('suggested_section', {}).get('category', 'Unknown'),
                    'level': match.get('suggested_section', {}).get('level', 'Unknown'),
                    'count': 0,
                    'examples': []
                }
            sections_analysis[section_name]['count'] += 1
            if len(sections_analysis[section_name]['examples']) < 3:
                sections_analysis[section_name]['examples'].append(match['docx_name'])
        
        return sections_analysis
    
    def analyze_dependency_changes(self):
        """Analyze what dependency changes were made"""
        changes = {
            'section_dependencies_updated': len(self.section_dependencies),
            'new_dependency_patterns_added': len(self.item_dependency_patterns),
            'improved_sections': []
        }
        
        # Sections with significantly improved dependencies
        for section_id, deps in self.section_dependencies.items():
            original_deps = []
            # Find original section
            for cat in self.json_data['categories']:
                for section in cat['sections']:
                    if section['id'] == section_id:
                        original_deps = section.get('pre', [])
                        break
            
            if len(deps) > len(original_deps):
                changes['improved_sections'].append({
                    'section_id': section_id,
                    'original_count': len(original_deps),
                    'new_count': len(deps),
                    'new_dependencies': [d for d in deps if d not in original_deps]
                })
        
        return changes
    
    def identify_quality_issues(self):
        """Identify potential quality issues in the merged data"""
        issues = {
            'potential_duplicates': [],
            'overly_specific_items': [],
            'overly_generic_items': [],
            'non_mainstream_topics': []
        }
        
        # Find potential duplicates
        for match in self.mappings_data['pattern_matches']:
            if match.get('score', 0) >= 3:
                issues['potential_duplicates'].append({
                    'docx_name': match['docx_name'],
                    'section': match['section_name'],
                    'confidence': 'high'
                })
        
        # Find overly specific items (very detailed or niche)
        for kp in self.docx_kps:
            if len(kp['name']) > 50 or '：' in kp['name'] and kp['name'].count('：') >= 2:
                issues['overly_specific_items'].append(kp['name'])
        
        # Find overly generic items
        generic_keywords = ['技巧', '方法', '优化', '基础', '入门', '总结', '概述']
        for kp in self.docx_kps:
            for keyword in generic_keywords:
                if kp['name'].endswith(keyword):
                    issues['overly_generic_items'].append(kp['name'])
                    break
        
        # Find non-mainstream topics
        l5_keywords = ['机器学习', '数据库', '操作系统', '汇编', '线程', '分布式', 'web', '网络编程']
        for kp in self.docx_kps:
            for keyword in l5_keywords:
                if keyword.lower() in kp['name'].lower():
                    issues['non_mainstream_topics'].append(kp['name'])
                    break
        
        return issues
    
    def generate_recommendations(self):
        """Generate recommendations for further improvements"""
        recommendations = [
            {
                'category': 'Mapping Quality',
                'recommendation': 'Consider creating new chapters for advanced topics that have 5+ related knowledge points',
                'priority': 'high'
            },
            {
                'category': 'Dependency Refinement',
                'recommendation': 'Review and refine dependency relationships for advanced algorithms and data structures',
                'priority': 'medium'
            },
            {
                'category': 'Content Quality',
                'recommendation': 'Split overly specific knowledge points into more granular, learnable units',
                'priority': 'medium'
            },
            {
                'category': 'Manual Review',
                'recommendation': f'Conduct manual review of {len(self.mappings_data["manual_review"])} unmapped knowledge points',
                'priority': 'high'
            },
            {
                'category': 'Progressive Learning',
                'recommendation': 'Add learning paths and skill trees for different difficulty levels (L1-L5)',
                'priority': 'low'
            }
        ]
        
        return recommendations

# Create final fusion system
final_fusion = FinalKnowledgeGraphFusion(
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\io_v4_4.json',
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points_clean.json',
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\advanced_knowledge_mappings.json'
)

# Generate merged structure
merged_structure = final_fusion.create_merged_structure()

# Save merged structure
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\merged_knowledge_graph.json', 'w', encoding='utf-8') as f:
    json.dump(merged_structure, f, ensure_ascii=False, indent=2)

# Generate and save analysis report
analysis_report = final_fusion.generate_analysis_report()
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\fusion_analysis_report.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_report, f, ensure_ascii=False, indent=2)

print("Knowledge Graph Fusion Complete!")
print(f"Saved merged structure to merged_knowledge_graph.json")
print(f"Saved analysis report to fusion_analysis_report.json")

# Print summary statistics
print(f"\n" + "="*60)
print("FUSION SUMMARY")
print("="*60)
print(f"Original items: 592")
print(f"Docx knowledge points: 1000")
print(f"Exact matches: {analysis_report['overall_statistics']['exact_matches']}")
print(f"Pattern matches: {analysis_report['overall_statistics']['pattern_matches']}")
print(f"New sections needed: {analysis_report['overall_statistics']['new_section_suggestions']}")
print(f"Manual review needed: {analysis_report['overall_statistics']['manual_review_needed']}")
print(f"Successfully mapped: {analysis_report['overall_statistics']['successfully_mapped']}")
print(f"Success rate: {analysis_report['overall_statistics']['mapping_success_rate']}")
print("="*60)