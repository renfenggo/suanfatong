import json
import re
from typing import Dict, List, Tuple

class KnowledgeGraphMerger:
    def __init__(self, json_path, docx_path):
        self.json_path = json_path
        self.docx_path = docx_path
        self.load_data()
        self.create_keyword_mapping()
        
    def load_data(self):
        # Load JSON data
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
            
        # Load docx knowledge points
        with open(self.docx_path, 'r', encoding='utf-8') as f:
            self.docx_kps = json.load(f)
            
        print(f"Loaded {len(self.json_data['categories'])} categories, {self.get_total_sections()} sections, {self.get_total_items()} items")
        print(f"Loaded {len(self.docx_kps)} docx knowledge points")
        
    def get_total_sections(self):
        return sum(len(cat['sections']) for cat in self.json_data['categories'])
    
    def get_total_items(self):
        return sum(len(s['items']) for cat in self.json_data['categories'] for s in cat['sections'])
    
    def create_keyword_mapping(self):
        # Create keyword mapping for better matching
        self.section_keywords = {}
        for cat in self.json_data['categories']:
            for section in cat['sections']:
                self.section_keywords[section['id']] = {
                    'name': section['name'],
                    'category': cat['name'],
                    'level': section.get('level', 'L1'),
                    'keywords': self.extract_keywords(section['name'])
                }
                
    def extract_keywords(self, text):
        # Extract meaningful keywords from text
        keywords = []
        text = text.lower()
        
        # Add original name
        keywords.append(text)
        
        # Remove common separators and split
        for sep in ['、', '与', '与', '和', '/', '，', ' ']:
            if sep in text:
                parts = text.split(sep)
                keywords.extend(parts)
                
        # Remove empty strings and duplicates
        keywords = [k.strip() for k in keywords if k.strip()]
        keywords = list(set(keywords))
        
        return keywords
    
    def find_best_match(self, docx_kp):
        """Find the best section match for a docx knowledge point"""
        kp_name = docx_kp['name'].lower()
        kp_keywords = self.extract_keywords(kp_name)
        
        best_score = 0
        best_matches = []
        
        for section_id, section_info in self.section_keywords.items():
            score = 0
            
            # Check keyword matches
            for keyword in kp_keywords:
                for section_keyword in section_info['keywords']:
                    if keyword in section_keyword or section_keyword in keyword:
                        score += 1
            
            # Check algorithm-specific patterns
            score += self.check_algorithm_patterns(kp_name, section_info)
            
            if score > 0 and score >= best_score:
                best_score = score
                best_matches.append({
                    'section_id': section_id,
                    'section_name': section_info['name'],
                    'category': section_info['category'],
                    'score': score
                })
        
        # Return the best match with highest score
        if best_matches:
            best_matches.sort(key=lambda x: x['score'], reverse=True)
            return best_matches[0]
        return None
    
    def check_algorithm_patterns(self, kp_name, section_info):
        """Additional pattern matching for algorithm-specific terms"""
        score = 0
        section_name = section_info['name'].lower()
        
        # Algorithm patterns
        if any(term in kp_name for term in ['排序', 'sort', 'sort']):
            if '排序' in section_name:
                score += 3
                
        if any(term in kp_name for term in ['搜索', 'search', 'dfs', 'bfs']):
            if any(term in section_name for term in ['搜索', 'search']):
                score += 3
                
        if any(term in kp_name for term in ['dp', '动态规划', 'dynamic programming']):
            if '动态规划' in section_name:
                score += 3
                
        if any(term in kp_name for term in ['图', 'graph', '最短路', '生成树']):
            if any(term in section_name for term in ['图', 'graph']):
                score += 2
                
        if any(term in kp_name for term in ['数学', '数学', '概率', '期望']):
            if any(term in section_name for term in ['数学', 'math', '概率']):
                score += 2
                
        if any(term in kp_name for term in ['数据结构', '线段树', '树状数组', '并查集']):
            if any(term in section_name for term in ['数据结构', '结构', 'segment', 'union']):
                score += 2
                
        return score
    
    def map_all_knowledge_points(self):
        """Map all docx knowledge points to JSON sections"""
        mappings = []
        unmapped = []
        
        for kp in self.docx_kps:
            match = self.find_best_match(kp)
            
            if match:
                mapping = {
                    'docx_id': kp['id'],
                    'docx_name': kp['name'],
                    'target_category': match['category'],
                    'target_section_id': match['section_id'],
                    'target_section_name': match['section_name'],
                    'score': match['score'],
                    'action': 'merge_into_existing_section'
                }
                mappings.append(mapping)
            else:
                unmapped.append({
                    'docx_id': kp['id'],
                    'docx_name': kp['name'],
                    'reason': '无法匹配到现有章节'
                })
        
        return mappings, unmapped

# Create the merger and process
merger = KnowledgeGraphMerger(
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\io_v4_4.json',
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points_clean.json'
)

mappings, unmapped = merger.map_all_knowledge_points()

print(f"\nSuccessfully mapped {len(mappings)} knowledge points")
print(f"Failed to map {len(unmapped)} knowledge points")

# Show some sample mappings
print("\nSample mappings:")
for i, mapping in enumerate(mappings[:20]):
    print(f"{mapping['docx_id']}. {mapping['docx_name'][:40]}... -> {mapping['target_section_id']}: {mapping['target_section_name']} (score: {mapping['score']})")

# Save mappings
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\knowledge_mappings.json', 'w', encoding='utf-8') as f:
    json.dump({
        'mappings': mappings,
        'unmapped': unmapped
    }, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(mappings)} mappings to knowledge_mappings.json")