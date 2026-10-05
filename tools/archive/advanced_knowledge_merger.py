import json
import re
from typing import Dict, List, Tuple, Optional

class AdvancedKnowledgeGraphMerger:
    def __init__(self, json_path, docx_path):
        self.json_path = json_path
        self.docx_path = docx_path
        self.load_data()
        self.create_comprehensive_mapping()
        
    def load_data(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
            
        with open(self.docx_path, 'r', encoding='utf-8') as f:
            self.docx_kps = json.load(f)
            
        print(f"Loaded {len(self.json_data['categories'])} categories, {self.get_total_sections()} sections, {self.get_total_items()} items")
        print(f"Loaded {len(self.docx_kps)} docx knowledge points")
        
    def get_total_sections(self):
        return sum(len(cat['sections']) for cat in self.json_data['categories'])
    
    def get_total_items(self):
        return sum(len(s['items']) for cat in self.json_data['categories'] for s in cat['sections'])
    
    def create_comprehensive_mapping(self):
        # Create section index
        self.section_index = {}
        self.item_index = {}
        
        for cat in self.json_data['categories']:
            for section in cat['sections']:
                self.section_index[section['id']] = {
                    'name': section['name'],
                    'category': cat['name'],
                    'level': section.get('level', 'L1'),
                    'items': [item['name'].lower() for item in section['items']],
                    'aliases': []
                }
                
                # Collect aliases from items
                for item in section['items']:
                    self.item_index[item['name'].lower()] = {
                        'section_id': section['id'],
                        'section_name': section['name'],
                        'category': cat['name'],
                        'item_id': item['id']
                    }
                    
                    # Add aliases
                    if item.get('alias'):
                        for alias in item['alias']:
                            self.item_index[alias.lower()] = {
                                'section_id': section['id'],
                                'section_name': section['name'],
                                'category': cat['name'],
                                'item_id': item['id'],
                                'is_alias': True
                            }
                            
        # Create comprehensive matching rules
        self.matching_rules = self.create_matching_rules()
        
    def create_matching_rules(self):
        """Create comprehensive matching rules for knowledge points"""
        return {
            # C++ Syntax (1.x)
            '1.1': ['程序基本结构', 'main函数', '命名空间', 'include', '头文件', '程序入口', '编译单元'],
            '1.2': ['输入输出', 'cin', 'cout', 'scanf', 'printf', '输入输出优化', 'iostream', 'stdio', '格式化输出'],
            '1.3': ['数据类型', '变量', '整型', '浮点型', '精度控制', '字符串', '字符', 'bool', '常量', '全局变量', '局部变量', '作用域'],
            '1.4': ['运算符', '算术运算', '逻辑运算', '位运算', '重载', '优先级', '自增', '自减'],
            '1.5': ['控制结构', 'if', 'else', 'switch', 'case', '循环', 'for', 'while', 'do-while', 'break', 'continue', 'goto'],
            '1.6': ['数组', '字符串', '越界', '下标', '多维数组', '数组操作', 'vector', 'push_back', 'size'],
            '1.7': ['函数', '递归', '指针', '引用', '参数传递', '返回值', '函数调用', '递归深度', 'lambda', '函数指针'],
            '1.8': ['结构体', '类', 'stl', 'stack', 'queue', 'deque', 'priority_queue', 'set', 'map', 'vector', 'string', 'algorithm', '排序'],
            '1.9': ['预处理', '宏', 'define', 'pragma', '条件编译', '文件包含', 'inline', '模板'],
            '1.10': ['常见错误', '内存泄漏', '栈溢出', '异常处理', '调试', '错误定位'],
            
            # Algorithms (2.x)  
            '2.1': ['枚举', '暴力枚举', '模拟', '递推', '递归', '分治', '倍增', '构造', '贪心', '启发式', '随机化'],
            '2.2': ['排序', '冒泡排序', '选择排序', '插入排序', '归并排序', '快速排序', '堆排序', '计数排序', '桶排序', '基数排序', '第k小', '逆序对'],
            '2.3': ['二分', '二分查找', '二分答案', '左边界', '右边界', '整数二分', '实数二分', '单调性', 'check函数', '三分法'],
            '2.4': ['前缀和', '差分', '离散化', '分块', '莫队', '根号分治', '贪心', '图论贪心', '树上贪心', '数学贪心'],
            '2.5': ['双指针', '滑动窗口', '指针', '窗口', '尺取法'],
            '2.6': ['贪心', '区间贪心', '背包贪心', '活动选择', '调度', '贪心证明'],
            '2.7': ['搜索', 'dfs', 'bfs', '深度优先', '广度优先', '状态空间搜索', '迭代加深', '双向搜索', '启发式搜索', 'a*', '回溯'],
            '2.8': ['dp', '动态规划', '背包dp', '区间dp', '树形dp', '状态压缩dp', '概率dp', '期望dp', '记忆化搜索'],
            '2.9': ['图基础', '图的存储', '邻接矩阵', '邻接表', '图的遍历', '连通性', '环', '路径'],
            '2.13': ['最短路', 'dijkstra', 'floyd', 'bellman-ford', 'spfa', '生成树', '最小生成树', 'kruskal', 'prim', '拓扑排序', '关键路径'],
            '2.14': ['树上算法', 'lca', '树的遍历', '树的重心', '树的直径', '树形dp', '树上最短路'],
            '2.15': ['连通分量', 'tarjan', '强连通', '割点', '桥', '双连通', '特殊图', 'dag', '欧拉图', '哈密顿图'],
            '2.16': ['二分图', '匹配', '最大匹配', '完美匹配', '匈牙利算法', '网络流', '最大流', '最小割', '费用流', '上下界'],
            '2.10': ['字符串', 'kmp', 'manacher', 'z-algorithm', '后缀数组', '后缀自动机', 'ac自动机', 'hash', '字符串匹配'],
            '2.11': ['位运算', '状态压缩', '子集枚举', 'bitset'],
            '2.12': ['数值', '矩阵', '矩阵快速幂', '高精度', '复杂计算'],
            '2.17': ['线性代数', '矩阵', '向量', '行列式', '高斯消元', '线性基', '插值', '多项式'],
            '2.18': ['综合', '高级技巧', '交互题', '构造题', '离线算法', '在线算法'],
            
            # Data Structures (3.x)
            '3.1': ['线性结构', '链表', '数组', '队列', '栈', '指针'],
            '3.2': ['栈', '队列', 'stack', 'queue', '单调栈', '单调队列'],
            '3.3': ['集合', '映射', 'set', 'map', 'multiset', 'multimap', '哈希', 'unordered_map', 'unordered_set'],
            '3.4': ['并查集', 'disjoint set', 'union find', '路径压缩', '按秩合并', '带权并查集'],
            '3.5': ['堆', 'priority_queue', '二叉堆', '左偏树', '二项堆', '斐波那契堆'],
            '3.6': ['树结构', '二叉树', '遍历', '线索树', '字典树', 'trie', '哈夫曼树'],
            '3.7': ['线段树', '树状数组', '区间维护', 'fenwick', 'segment tree', '区间查询', '区间修改'],
            '3.8': ['字符串结构', 'trie', '后缀树', 'ac自动机'],
            '3.9': ['图存储', '邻接矩阵', '邻接表', '链式前向星', '边表'],
            '3.10': ['平衡树', 'treap', 'splay', 'avl', '红黑树', 'bst'],
            '3.11': ['可持久化', '主席树', '动态树', 'lct', 'link-cut-tree', '可持久化数据结构'],
            '3.12': ['莫队', 'cdq', '分治', '哈希扩展', '字符串哈希'],
            
            # Mathematics (4.x)
            '4.1': ['整数', '整除', '质数', '素数', 'gcd', 'gcd', 'lcm', '最大公约数', '最小公倍数', '分解', '数论基础'],
            '4.2': ['模运算', '同余', '取模', '逆元', '费马小定理', '欧拉定理', '中国剩余定理', '幂运算', '快速幂'],
            '4.3': ['计数', '组合', '排列', '组合数', '组合数学', '容斥', '二项式系数', '卡特兰数', '斯特林数'],
            '4.4': ['离散数学', '逻辑', '集合', '关系', '函数', '图论', '数理逻辑'],
            '4.5': ['图数学', '树数学', '生成函数', '母函数', '组合恒等式'],
            '4.6': ['概率', '期望', '随机变量', '概率分布', '贝叶斯', '条件概率', '马尔可夫', '蒙特卡洛'],
            '4.7': ['几何', '计算几何', '点线面', '向量', '叉积', '点积', '凸包', '圆', '多边形', '旋转卡壳', '半平面交'],
            '4.8': ['扩展', '群论', 'burnside', 'polya', '线性代数', '高斯消元', '矩阵'],
            '4.0': ['数学基础', '代数', '几何基础', '数学分析'],
            
            # C++ Programming/Debugging (5.x)
            '5.1': ['输入输出', '快读', '快写', '输入输出技巧', '格式化'],
            '5.2': ['字符', '字符串', '位运算', '数位', '进制转换'],
            '5.3': ['下标', '枚举', '技巧', '边界', '循环'],
            '5.4': ['代码技巧', '模板', '宏', '优化'],
            '5.5': ['图论实现', '图存储', '遍历', '搜索实现'],
            '5.6': ['dp实现', '状态设计', '记忆化', '递推'],
            '5.7': ['调试', '断点', '打印', '检查', '验证', '对拍', '测试'],
            '5.8': ['错误', '定位', '排查', '常见错误', '边界错误'],
            '5.9': ['工程化', '习惯', '规范', '项目组织', '代码风格'],
        }
    
    def find_exact_match(self, kp_name):
        """Find exact match in existing items"""
        kp_lower = kp_name.lower()
        
        # Check for exact match in items
        if kp_lower in self.item_index:
            item_info = self.item_index[kp_lower]
            return {
                'section_id': item_info['section_id'],
                'section_name': item_info['section_name'],
                'category': item_info['category'],
                'item_id': item_info.get('item_id'),
                'match_type': 'exact',
                'reason': '与现有知识点完全匹配'
            }
        
        return None
    
    def find_pattern_match(self, kp_name):
        """Find pattern-based match"""
        kp_lower = kp_name.lower()
        
        best_match = None
        best_score = 0
        
        for section_id, keywords in self.matching_rules.items():
            score = 0
            
            for keyword in keywords:
                if keyword.lower() in kp_lower:
                    score += 1
                elif kp_lower in keyword.lower():
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = {
                    'section_id': section_id,
                    'section_name': self.section_index[section_id]['name'],
                    'category': self.section_index[section_id]['category'],
                    'match_type': 'pattern',
                    'score': score,
                    'reason': f'基于关键词匹配: {keywords[:3]}'
                }
        
        return best_match if best_score > 0 else None
    
    def analyze_knowledge_point(self, kp):
        """Analyze a knowledge point and determine its best mapping"""
        kp_name = kp['name']
        
        # First try exact match
        exact_match = self.find_exact_match(kp_name)
        if exact_match:
            return exact_match
        
        # Then try pattern match
        pattern_match = self.find_pattern_match(kp_name)
        if pattern_match:
            return pattern_match
        
        # If no match, analyze content to suggest new section
        return self.suggest_new_section(kp)
    
    def suggest_new_section(self, kp):
        """Suggest a new section for unmapped knowledge points"""
        kp_name = kp['name'].lower()
        
        suggestions = [
            {
                'name': '高级图论扩展',
                'category': '算法',
                'level': 'L4',
                'keywords': ['k短路', '支配树', '圆方树', '虚树', '网络流', '最小割', '费用流', '上下界', '二分图高级', '强连通分量']
            },
            {
                'name': '高级字符串算法',
                'category': '算法', 
                'level': 'L4',
                'keywords': ['后缀自动机', '后缀数组', 'manacher', '字符串匹配', 'ac自动机', '字符串哈希', '最小表示法']
            },
            {
                'name': '高级数据结构',
                'category': '数据结构',
                'level': 'L4', 
                'keywords': ['主席树', '可持久化', 'lct', '动态树', '平衡树', 'treap', 'splay', '可持久化线段树', '动态开点']
            },
            {
                'name': '随机化与启发式算法',
                'category': '算法',
                'level': 'L3',
                'keywords': ['模拟退火', '遗传算法', '爬山算法', '蒙特卡洛', '随机增量', '粒子群', '禁忌搜索']
            },
            {
                'name': '高级数学与群论',
                'category': '算法竞赛数学',
                'level': 'L4',
                'keywords': ['群论', 'burnside', 'polya', '反演', '斯特林数', '卡特兰数', '母函数', '生成函数']
            },
            {
                'name': '竞赛工程化与优化',
                'category': 'C++编程/调试技巧',
                'level': 'L2',
                'keywords': ['卡常', '优化', '对拍', '调试', '性能分析', '编译器优化', '内存对齐', '缓存友好']
            },
            {
                'name': '交互题与构造题技巧',
                'category': '算法',
                'level': 'L3',
                'keywords': ['交互题', '构造题', '构造', '交互', '证明', '贪心证明', '交换论证']
            },
            {
                'name': '算法竞赛心理与策略',
                'category': 'C++编程/调试技巧',
                'level': 'L1',
                'keywords': ['心理素质', '抗压能力', '时间分配', '比赛策略', '样例分析', '读题策略']
            }
        ]
        
        for suggestion in suggestions:
            for keyword in suggestion['keywords']:
                if keyword.lower() in kp_name:
                    return {
                        'action': 'create_new_section',
                        'suggested_section': suggestion,
                        'reason': f'知识点包含"{keyword}"，建议归入{suggestion["name"]}章节'
                    }
        
        # Default fallback
        return {
            'action': 'needs_manual_review',
            'reason': '无法自动分类，需要人工审核'
        }
    
    def process_all_knowledge_points(self):
        """Process all knowledge points and generate mappings"""
        results = {
            'exact_matches': [],
            'pattern_matches': [],
            'new_sections': [],
            'manual_review': []
        }
        
        for kp in self.docx_kps:
            result = self.analyze_knowledge_point(kp)
            
            base_mapping = {
                'docx_id': kp['id'],
                'docx_name': kp['name']
            }
            base_mapping.update(result)
            
            if result.get('match_type') == 'exact':
                results['exact_matches'].append(base_mapping)
            elif result.get('match_type') == 'pattern':
                results['pattern_matches'].append(base_mapping)
            elif result.get('action') == 'create_new_section':
                results['new_sections'].append(base_mapping)
            else:
                results['manual_review'].append(base_mapping)
        
        return results

# Create advanced merger and process
advanced_merger = AdvancedKnowledgeGraphMerger(
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\io_v4_4.json',
    r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points_clean.json'
)

results = advanced_merger.process_all_knowledge_points()

print(f"\nProcessing Results:")
print(f"Exact matches: {len(results['exact_matches'])}")
print(f"Pattern matches: {len(results['pattern_matches'])}")
print(f"Need new sections: {len(results['new_sections'])}")
print(f"Need manual review: {len(results['manual_review'])}")

# Show samples
print(f"\nExact Match Samples:")
for match in results['exact_matches'][:10]:
    print(f"{match['docx_id']}. {match['docx_name'][:40]}... -> {match['section_id']}: {match['section_name']}")

print(f"\nPattern Match Samples:")
for match in results['pattern_matches'][:10]:
    print(f"{match['docx_id']}. {match['docx_name'][:40]}... -> {match['section_id']}: {match['section_name']} (score: {match['score']})")

print(f"\nNew Section Suggestions:")
for match in results['new_sections'][:10]:
    print(f"{match['docx_id']}. {match['docx_name'][:40]}... -> {match['suggested_section']['name']}")

# Save comprehensive results
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\advanced_knowledge_mappings.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSaved comprehensive results to advanced_knowledge_mappings.json")