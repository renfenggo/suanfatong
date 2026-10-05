#!/usr/bin/env python3
"""
前端学习体验设计输入数据审计工具（修正版）

该工具用于审计现有数据结构是否满足前端学习体验设计的需求，
检查数据完整性、一致性，并生成改进建议。

使用方法:
    python tools/audit_frontend_learning_experience_inputs.py

审计范围:
- 知识图谱数据结构
- 内容索引数据
- 知识点内容数据
- 动画数据
- 依赖关系数据

修正内容:
- 移除emoji，使用[INFO]、[PASS]、[WARN]、[FAIL]标签
- 正确识别categories->sections->items结构
- 自动探测字段，不硬编码
- 正确统计知识点数量
- 生成可信的审计结论
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict, Counter
from datetime import datetime


class FrontendLearningExperienceAuditor:
    """前端学习体验设计数据审计器（修正版）"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results = {
            'audit_timestamp': datetime.now().isoformat(),
            'project_root': str(project_root),
            'data_sources': {},
            'schema_detection': {},
            'field_coverage': {},
            'frontend_readiness': {},
            'data_quality_issues': [],
            'recommendations': [],
            'final_assessment': {}
        }
        
    def log_info(self, message: str):
        """输出INFO日志"""
        print(f"[INFO] {message}")
        
    def log_pass(self, message: str):
        """输出PASS日志"""
        print(f"[PASS] {message}")
        
    def log_warn(self, message: str):
        """输出WARN日志"""
        print(f"[WARN] {message}")
        
    def log_fail(self, message: str):
        """输出FAIL日志"""
        print(f"[FAIL] {message}")
        
    def load_json_file(self, file_path: Path) -> Dict:
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.results['data_quality_issues'].append({
                'type': 'file_load_error',
                'file': str(file_path),
                'error': str(e)
            })
            self.log_fail(f"无法加载文件 {file_path}: {e}")
            return {}
    
    def detect_schema_structure(self, data: Dict) -> Dict:
        """自动探测数据结构"""
        schema_info = {
            'detected_structure': None,
            'top_level_keys': [],
            'categories_count': 0,
            'sections_count': 0,
            'items_count': 0,
            'structure_path': None
        }
        
        if not data:
            schema_info['detected_structure'] = 'empty_or_error'
            return schema_info
        
        # 检查顶层键
        schema_info['top_level_keys'] = list(data.keys())
        
        # 尝试不同的结构模式
        # 模式1: categories -> sections -> items
        if 'categories' in data and isinstance(data['categories'], list):
            categories = data['categories']
            schema_info['categories_count'] = len(categories)
            total_sections = 0
            total_items = 0
            
            for category in categories:
                if isinstance(category, dict) and 'sections' in category:
                    sections = category['sections']
                    total_sections += len(sections)
                    
                    for section in sections:
                        if isinstance(section, dict) and 'items' in section:
                            items = section['items']
                            total_items += len(items)
            
            schema_info['sections_count'] = total_sections
            schema_info['items_count'] = total_items
            schema_info['structure_path'] = 'categories -> sections -> items'
            schema_info['detected_structure'] = 'categories_sections_items'
            
        # 模式2: sections -> items
        elif 'sections' in data and isinstance(data['sections'], list):
            sections = data['sections']
            schema_info['sections_count'] = len(sections)
            total_items = 0
            
            for section in sections:
                if isinstance(section, dict) and 'items' in section:
                    items = section['items']
                    total_items += len(items)
            
            schema_info['items_count'] = total_items
            schema_info['structure_path'] = 'sections -> items'
            schema_info['detected_structure'] = 'sections_items'
            
        # 模式3: 顶层 items
        elif 'items' in data and isinstance(data['items'], list):
            schema_info['items_count'] = len(data['items'])
            schema_info['structure_path'] = 'items'
            schema_info['detected_structure'] = 'top_level_items'
            
        else:
            schema_info['detected_structure'] = 'unknown'
            schema_info['structure_path'] = '无法识别'
        
        return schema_info
    
    def extract_all_items(self, data: Dict) -> List[Dict]:
        """从不同结构中提取所有知识点"""
        items = []
        
        if not data:
            return items
            
        # 模式1: categories -> sections -> items
        if 'categories' in data and isinstance(data['categories'], list):
            for category in data['categories']:
                if isinstance(category, dict) and 'sections' in category:
                    for section in category['sections']:
                        if isinstance(section, dict) and 'items' in section:
                            items.extend(section['items'])
                            
        # 模式2: sections -> items
        elif 'sections' in data and isinstance(data['sections'], list):
            for section in data['sections']:
                if isinstance(section, dict) and 'items' in section:
                    items.extend(section['items'])
                    
        # 模式3: 顶层 items
        elif 'items' in data and isinstance(data['items'], list):
            items.extend(data['items'])
            
        return items
    
    def detect_item_fields(self, items: List[Dict]) -> Dict:
        """自动探测知识点字段"""
        field_stats = defaultdict(lambda: {'count': 0, 'total': len(items), 'types': set()})
        
        for item in items:
            if isinstance(item, dict):
                for key, value in item.items():
                    field_stats[key]['count'] += 1
                    field_stats[key]['types'].add(type(value).__name__)
        
        # 计算覆盖率和字段类型
        field_info = {}
        for field_name, stats in field_stats.items():
            coverage = (stats['count'] / stats['total']) * 100 if stats['total'] > 0 else 0
            field_info[field_name] = {
                'coverage': round(coverage, 2),
                'count': stats['count'],
                'total': stats['total'],
                'types': list(stats['types'])
            }
        
        return field_info
    
    def audit_main_knowledge_graph(self) -> Dict:
        """审计主知识图谱"""
        self.log_info("开始审计主知识图谱...")
        
        # 尝试多个可能的文件路径
        possible_paths = [
            'merged_knowledge_graph_item_dependencies_refined.json',
            'assets/data/knowledge/io_v4_4.json'
        ]
        
        graph_data = None
        graph_file = None
        
        for path in possible_paths:
            file_path = self.project_root / path
            if file_path.exists():
                graph_data = self.load_json_file(file_path)
                if graph_data:
                    graph_file = file_path
                    self.log_pass(f"找到主知识图谱文件: {path}")
                    break
        
        if not graph_data or not graph_file:
            self.log_fail("无法找到有效的主知识图谱文件")
            return {
                'status': 'error',
                'message': '无法找到有效的主知识图谱文件'
            }
        
        # 探测数据结构
        schema_info = self.detect_schema_structure(graph_data)
        self.results['schema_detection']['main_graph'] = schema_info
        
        # 提取所有知识点
        items = self.extract_all_items(graph_data)
        
        # 探测字段
        field_info = self.detect_item_fields(items)
        
        audit_result = {
            'status': 'success',
            'file': str(graph_file),
            'schema_info': schema_info,
            'total_items': len(items),
            'field_coverage': field_info,
            'data_quality': {}
        }
        
        # 检查关键字段
        self.log_info(f"探测到 {len(items)} 个知识点")
        self.log_info(f"数据结构: {schema_info['structure_path']}")
        
        # 检查ID字段
        id_fields = ['id', 'item_id', 'name', 'title']
        found_id_field = None
        for field in id_fields:
            if field in field_info and field_info[field]['coverage'] > 50:
                found_id_field = field
                self.log_pass(f"找到ID字段: {field} (覆盖率: {field_info[field]['coverage']}%)")
                break
        
        if not found_id_field:
            self.log_warn("未找到明显的ID字段")
        
        # 检查常见字段
        common_field_patterns = {
            'section_id': ['section_id', 'parent', 'section'],
            'name': ['name', 'title', 'label'],
            'level': ['level', 'difficulty', 'grade'],
            'pre': ['direct_pre', 'prerequisite', 'pre', 'depends_on'],
            'resolved_pre': ['resolved_pre', 'resolved_prerequisites'],
            'rel': ['rel', 'related', 'relations']
        }
        
        frontend_fields_status = {}
        for frontend_field, possible_names in common_field_patterns.items():
            found = False
            for possible_name in possible_names:
                if possible_name in field_info:
                    frontend_fields_status[frontend_field] = {
                        'actual_field': possible_name,
                        'coverage': field_info[possible_name]['coverage'],
                        'status': 'found'
                    }
                    found = True
                    break
            
            if not found:
                frontend_fields_status[frontend_field] = {
                    'actual_field': None,
                    'coverage': 0,
                    'status': 'missing'
                }
        
        audit_result['frontend_fields_status'] = frontend_fields_status
        
        # 检查依赖关系
        dependency_fields = ['direct_pre', 'resolved_pre', 'rel']
        dependency_coverage = {}
        for field in dependency_fields:
            if field in field_info:
                dependency_coverage[field] = field_info[field]['coverage']
            else:
                dependency_coverage[field] = 0
        
        audit_result['dependency_coverage'] = dependency_coverage
        
        self.results['data_sources']['main_knowledge_graph'] = audit_result
        
        # 生成质量报告
        if len(items) == 0:
            self.log_fail("主知识图谱中没有找到任何知识点")
        elif len(items) < 3000:
            self.log_warn(f"知识点数量({len(items)})少于预期的3240个")
        else:
            self.log_pass(f"知识点数量正常: {len(items)}")
        
        return audit_result
    
    def audit_frontend_knowledge_graph(self) -> Dict:
        """审计前端知识图谱"""
        self.log_info("开始审计前端知识图谱...")
        
        frontend_graph_file = self.project_root / 'assets/data/knowledge/io_v4_4.json'
        if not frontend_graph_file.exists():
            self.log_warn("前端知识图谱文件不存在，跳过审计")
            return {
                'status': 'skipped',
                'message': '前端知识图谱文件不存在'
            }
        
        frontend_data = self.load_json_file(frontend_graph_file)
        if not frontend_data:
            return {
                'status': 'error',
                'message': '无法加载前端知识图谱数据'
            }
        
        # 探测结构和提取知识点
        schema_info = self.detect_schema_structure(frontend_data)
        items = self.extract_all_items(frontend_data)
        
        audit_result = {
            'status': 'success',
            'file': str(frontend_graph_file),
            'schema_info': schema_info,
            'total_items': len(items)
        }
        
        self.results['data_sources']['frontend_knowledge_graph'] = audit_result
        
        self.log_info(f"前端知识图谱知识点数量: {len(items)}")
        
        return audit_result
    
    def audit_content_index(self) -> Dict:
        """审计内容索引"""
        self.log_info("开始审计内容索引...")
        
        index_file = self.project_root / 'assets/data/knowledge_content/content_index.json'
        if not index_file.exists():
            self.log_warn("内容索引文件不存在")
            return {
                'status': 'error',
                'message': '内容索引文件不存在'
            }
        
        index_data = self.load_json_file(index_file)
        if not index_data:
            return {
                'status': 'error',
                'message': '无法加载内容索引数据'
            }
        
        audit_result = {
            'status': 'success',
            'file': str(index_file),
            'version': index_data.get('version', 'unknown'),
            'source_item_count': index_data.get('source_item_count', 0),
            'generated_item_count': index_data.get('generated_item_count', 0),
            'total_parts': index_data.get('total_parts', 0),
            'expected_count': 3240
        }
        
        # 检查数量是否匹配
        if audit_result['generated_item_count'] == 3240:
            self.log_pass(f"内容索引数量正确: {audit_result['generated_item_count']}")
        else:
            self.log_warn(f"内容索引数量({audit_result['generated_item_count']})不匹配预期的3240")
        
        self.results['data_sources']['content_index'] = audit_result
        
        return audit_result
    
    def check_id_consistency(self) -> Dict:
        """检查ID一致性"""
        self.log_info("检查主图谱和前端图谱的ID一致性...")
        
        consistency_result = {
            'status': 'success',
            'consistency_check': {},
            'id_discrepancies': {
                'missing_in_frontend': [],
                'extra_in_frontend': []
            }
        }
        
        main_graph_ids = set()
        frontend_graph_ids = set()
        
        # 提取主图谱ID
        if 'main_knowledge_graph' in self.results['data_sources']:
            main_result = self.results['data_sources']['main_knowledge_graph']
            if main_result['status'] == 'success':
                main_file = main_result['file']
                main_data = self.load_json_file(Path(main_file))
                main_items = self.extract_all_items(main_data)
                
                # 尝试识别ID字段
                for item in main_items:
                    if isinstance(item, dict):
                        if 'id' in item:
                            main_graph_ids.add(item['id'])
                        elif 'item_id' in item:
                            main_graph_ids.add(item['item_id'])
        
        # 提取前端图谱ID
        if 'frontend_knowledge_graph' in self.results['data_sources']:
            frontend_result = self.results['data_sources']['frontend_knowledge_graph']
            if frontend_result['status'] == 'success':
                frontend_file = frontend_result['file']
                frontend_data = self.load_json_file(Path(frontend_file))
                frontend_items = self.extract_all_items(frontend_data)
                
                for item in frontend_items:
                    if isinstance(item, dict):
                        if 'id' in item:
                            frontend_graph_ids.add(item['id'])
                        elif 'item_id' in item:
                            frontend_graph_ids.add(item['item_id'])
        
        # 检查一致性
        main_count = len(main_graph_ids)
        frontend_count = len(frontend_graph_ids)
        intersection = main_graph_ids & frontend_graph_ids
        intersection_count = len(intersection)
        
        missing_in_frontend = main_graph_ids - frontend_graph_ids
        extra_in_frontend = frontend_graph_ids - main_graph_ids
        
        consistency_result['consistency_check'] = {
            'main_graph_count': main_count,
            'frontend_graph_count': frontend_count,
            'intersection_count': intersection_count,
            'consistency_percentage': round((intersection_count / max(main_count, frontend_count, 1)) * 100, 2),
            'missing_in_frontend_count': len(missing_in_frontend),
            'extra_in_frontend_count': len(extra_in_frontend)
        }
        
        # 只保存样本，最多20个
        if missing_in_frontend:
            consistency_result['id_discrepancies']['missing_in_frontend'] = list(missing_in_frontend)[:20]
        
        if extra_in_frontend:
            consistency_result['id_discrepancies']['extra_in_frontend'] = list(extra_in_frontend)[:20]
        
        if main_count == frontend_count == intersection_count:
            self.log_pass(f"ID完全一致: {main_count} 个")
        else:
            self.log_warn(f"ID不完全一致 - 主图谱:{main_count}, 前端图谱:{frontend_count}, 交集:{intersection_count}")
            if missing_in_frontend:
                self.log_warn(f"主图谱有 {len(missing_in_frontend)} 个ID在前端图谱缺失")
            if extra_in_frontend:
                self.log_warn(f"前端图谱有 {len(extra_in_frontend)} 个额外ID")
        
        self.results['id_consistency'] = consistency_result
        
        return consistency_result
    
    def assess_frontend_readiness(self) -> Dict:
        """评估前端就绪度"""
        self.log_info("评估前端学习体验就绪度...")
        
        readiness_assessment = {
            'overall_readiness': 'unknown',
            'readiness_score': 0,
            'field_readiness': {},
            'data_gaps': [],
            'recommendations': []
        }
        
        # 检查基础字段就绪度
        if 'main_knowledge_graph' in self.results['data_sources']:
            main_result = self.results['data_sources']['main_knowledge_graph']
            
            # 基础字段（应该已有）
            basic_fields = {
                'id': {'status': 'unknown', 'importance': 'critical'},
                'name': {'status': 'unknown', 'importance': 'critical'},
                'section_id': {'status': 'unknown', 'importance': 'high', 'derivable': True},
                'level': {'status': 'unknown', 'importance': 'medium'},
                'direct_pre': {'status': 'unknown', 'importance': 'high'},
                'resolved_pre': {'status': 'unknown', 'importance': 'high'},
                'rel': {'status': 'unknown', 'importance': 'medium'}
            }
            
            frontend_fields_status = main_result.get('frontend_fields_status', {})
            
            # 检查 id 字段（从 field_coverage 中直接检查）
            field_coverage = main_result.get('field_coverage', {})
            if 'id' in field_coverage and field_coverage['id']['coverage'] >= 90:
                basic_fields['id']['status'] = 'ready'
                basic_fields['id']['coverage'] = field_coverage['id']['coverage']
            elif 'id' in field_coverage:
                basic_fields['id']['status'] = 'partial'
                basic_fields['id']['coverage'] = field_coverage['id']['coverage']
            
            # 检查 direct_pre 字段（从 field_coverage 中直接检查）
            if 'direct_pre' in field_coverage and field_coverage['direct_pre']['coverage'] >= 90:
                basic_fields['direct_pre']['status'] = 'ready'
                basic_fields['direct_pre']['coverage'] = field_coverage['direct_pre']['coverage']
            elif 'direct_pre' in field_coverage:
                basic_fields['direct_pre']['status'] = 'partial'
                basic_fields['direct_pre']['coverage'] = field_coverage['direct_pre']['coverage']
            
            # 检查其他字段
            for field_name, field_info in basic_fields.items():
                if field_name in ['id', 'direct_pre']:
                    # 已经处理过，直接添加到结果
                    readiness_assessment['field_readiness'][field_name] = field_info
                    continue
                    
                if field_name in frontend_fields_status:
                    if frontend_fields_status[field_name]['status'] == 'found':
                        coverage = frontend_fields_status[field_name]['coverage']
                        
                        # 特殊处理 section_id：如果是派生的，标记为 derived_ready
                        if field_name == 'section_id' and field_info.get('derivable', False):
                            if coverage >= 50:
                                field_info['status'] = 'derived_ready'
                            else:
                                field_info['status'] = 'derived_partial'
                        else:
                            if coverage >= 90:
                                field_info['status'] = 'ready'
                            elif coverage >= 50:
                                field_info['status'] = 'partial'
                            else:
                                field_info['status'] = 'poor'
                        field_info['coverage'] = coverage
                    else:
                        # 对于可派生字段，如果没有找到，检查是否可以从外层结构派生
                        if field_name == 'section_id' and field_info.get('derivable', False):
                            # 检查数据结构是否支持派生
                            schema_info = main_result.get('schema_info', {})
                            if schema_info.get('detected_structure') == 'categories_sections_items':
                                field_info['status'] = 'derived_ready'
                                field_info['coverage'] = 100  # 从结构派生，覆盖率视为100%
                            else:
                                field_info['status'] = 'missing'
                                field_info['coverage'] = 0
                        else:
                            field_info['status'] = 'missing'
                            field_info['coverage'] = 0
                
                readiness_assessment['field_readiness'][field_name] = field_info
            
            # 前端体验字段（需要补充或派生）
            frontend_experience_fields = {
                'estimated_time': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'medium'},
                'importance_level': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'medium'},
                'learning_status': {'status': 'missing', 'source': 'frontend_derived', 'importance': 'high'},
                'learning_readiness': {'status': 'missing', 'source': 'frontend_derived', 'importance': 'high'},
                'animation_priority': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'low'},
                'quiz_difficulty': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'low'},
                'one_sentence_explanation': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'high'},
                'core_intuition': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'high'},
                'common_traps': {'status': 'missing', 'source': 'needs_supplement', 'importance': 'medium'}
            }
            
            readiness_assessment['frontend_experience_fields'] = frontend_experience_fields
        
        # 计算就绪分数
        ready_count = sum(1 for f in readiness_assessment.get('field_readiness', {}).values() 
                         if f.get('status') == 'ready')
        total_count = len(readiness_assessment.get('field_readiness', {}))
        
        if total_count > 0:
            basic_readiness = (ready_count / total_count) * 100
        else:
            basic_readiness = 0
        
        # 考虑知识点数量
        total_items = 0
        if 'main_knowledge_graph' in self.results['data_sources']:
            total_items = self.results['data_sources']['main_knowledge_graph'].get('total_items', 0)
        
        item_readiness = min(100, (total_items / 3240) * 100) if total_items > 0 else 0
        
        # 综合就绪度
        readiness_assessment['readiness_score'] = round((basic_readiness * 0.7 + item_readiness * 0.3), 2)
        
        # 确定总体状态
        if readiness_assessment['readiness_score'] >= 80:
            readiness_assessment['overall_readiness'] = 'ready'
        elif readiness_assessment['readiness_score'] >= 60:
            readiness_assessment['overall_readiness'] = 'acceptable'
        elif readiness_assessment['readiness_score'] >= 40:
            readiness_assessment['overall_readiness'] = 'needs_work'
        else:
            readiness_assessment['overall_readiness'] = 'not_ready'
        
        # 生成数据缺口和建议
        for field_name, field_info in readiness_assessment.get('field_readiness', {}).items():
            if field_info['status'] in ['missing', 'poor']:
                readiness_assessment['data_gaps'].append({
                    'field': field_name,
                    'status': field_info['status'],
                    'importance': field_info['importance']
                })
        
        # 生成建议
        if readiness_assessment['overall_readiness'] == 'ready':
            readiness_assessment['recommendations'].append({
                'priority': 'immediate',
                'action': '可以开始前端MVP开发',
                'reason': '基础数据就绪度良好，核心字段覆盖充分'
            })
        else:
            readiness_assessment['recommendations'].append({
                'priority': 'high',
                'action': '优先补充关键字段',
                'reason': f'当前就绪度{readiness_assessment["readiness_score"]}%，需要提升到80%以上'
            })
        
        self.results['frontend_readiness'] = readiness_assessment
        
        return readiness_assessment
    
    def generate_final_assessment(self) -> Dict:
        """生成最终评估"""
        self.log_info("生成最终评估报告...")
        
        final_assessment = {
            'can_start_structure_mvp': False,
            'can_start_recommendation_mvp': False,
            'readiness_score': 0,
            'critical_issues': [],
            'high_priority_recommendations': [],
            'data_quality_score': 0,
            'suitable_for_structure_mvp': [],
            'not_suitable_for_recommendation_mvp': [],
            'recommendation_for_next_steps': []
        }
        
        # 生成顶层 field_coverage 摘要
        top_level_field_coverage = {}
        if 'main_knowledge_graph' in self.results['data_sources']:
            main_result = self.results['data_sources']['main_knowledge_graph']
            field_coverage = main_result.get('field_coverage', {})
            frontend_fields_status = main_result.get('frontend_fields_status', {})
            
            # 为每个重要字段生成摘要
            important_fields = ['id', 'name', 'section_id', 'level', 'direct_pre', 'resolved_pre', 'rel']
            
            for field in important_fields:
                field_summary = {
                    'status': 'unknown',
                    'coverage': 0,
                    'note': ''
                }
                
                # 检查字段覆盖率
                if field in field_coverage:
                    field_summary['coverage'] = field_coverage[field]['coverage']
                    field_summary['actual_field'] = field
                    
                    # 确定状态
                    if field_summary['coverage'] >= 90:
                        field_summary['status'] = 'ready'
                        field_summary['note'] = '字段覆盖率良好，可直接使用'
                    elif field_summary['coverage'] >= 50:
                        field_summary['status'] = 'partial'
                        field_summary['note'] = '字段覆盖率中等，基本满足需求'
                    else:
                        field_summary['status'] = 'poor'
                        field_summary['note'] = '字段覆盖率较低，需要补充'
                
                # 检查特殊字段状态
                if field == 'section_id':
                    # section_id 可以从结构派生，原始字段可能是 parent
                    if 'parent' in field_coverage:
                        field_summary['coverage'] = field_coverage['parent']['coverage']
                        field_summary['actual_field'] = 'parent'
                    field_summary['status'] = 'derived_ready'
                    field_summary['source'] = 'structural_derivation'
                    field_summary['note'] = '可从 categories->sections->items 结构派生，原始字段为 parent'
                elif field in frontend_fields_status:
                    # 使用前端字段状态
                    frontend_status = frontend_fields_status[field]
                    if frontend_status['status'] == 'found':
                        field_summary['actual_field'] = frontend_status['actual_field']
                        field_summary['source'] = 'direct_field'
                        field_summary['note'] = f'原始字段名为 {frontend_status["actual_field"]}'
                
                top_level_field_coverage[field] = field_summary
        
        # 将摘要添加到结果中
        self.results['field_coverage'] = top_level_field_coverage
        
        # 获取就绪度评估
        if 'frontend_readiness' in self.results:
            readiness = self.results['frontend_readiness']
            final_assessment['readiness_score'] = readiness['readiness_score']
            
            # 收集关键问题
            for gap in readiness.get('data_gaps', []):
                if gap['importance'] == 'critical':
                    final_assessment['critical_issues'].append(gap)
            
            # 收集高优先级建议
            for rec in readiness.get('recommendations', []):
                if rec.get('priority') in ['high', 'immediate']:
                    final_assessment['high_priority_recommendations'].append(rec)
            
            # 评估是否可以开始结构 MVP
            structure_ready_fields = ['id', 'name', 'section_id', 'level', 'direct_pre', 'resolved_pre', 'rel']
            structure_field_status = readiness.get('field_readiness', {})
            
            structure_ready_count = 0
            for field in structure_ready_fields:
                if field in structure_field_status:
                    status = structure_field_status[field]['status']
                    if status in ['ready', 'derived_ready', 'partial']:  # partial 也算基本就绪
                        structure_ready_count += 1
            
            structure_readiness_percentage = (structure_ready_count / len(structure_ready_fields)) * 100
            
            # 检查数据质量
            data_quality_good = True
            if 'main_knowledge_graph' in self.results['data_sources']:
                main_result = self.results['data_sources']['main_knowledge_graph']
                if main_result['status'] != 'success':
                    data_quality_good = False
                
                total_items = main_result.get('total_items', 0)
                if total_items < 3000:
                    data_quality_good = False
            
            if 'content_index' in self.results['data_sources']:
                index_result = self.results['data_sources']['content_index']
                if index_result['status'] != 'success':
                    data_quality_good = False
                
                if index_result.get('generated_item_count', 0) != 3240:
                    data_quality_good = False
            
            # 判断是否可以开始结构 MVP
            final_assessment['can_start_structure_mvp'] = (
                structure_readiness_percentage >= 70 and  # 至少70%的基础字段就绪（包括partial）
                data_quality_good  # 数据质量良好
            )
            
            # 判断是否可以开始推荐 MVP
            # 需要额外的学习体验字段
            experience_fields_status = readiness.get('frontend_experience_fields', {})
            experience_ready_count = sum(1 for f in experience_fields_status.values() 
                                        if f.get('status') == 'ready')
            experience_readiness = (experience_ready_count / len(experience_fields_status)) * 100 if experience_fields_status else 0
            
            final_assessment['can_start_recommendation_mvp'] = (
                structure_readiness_percentage >= 90 and  # 结构字段高度就绪
                experience_readiness >= 60  # 体验字段中度就绪
            )
            
            # 填充适合结构 MVP 的功能
            if final_assessment['can_start_structure_mvp']:
                final_assessment['suitable_for_structure_mvp'] = [
                    {
                        'feature': '首页继续学习区域',
                        'reason': '基础图谱结构和ID关系稳定，可以展示学习进度和继续学习入口'
                    },
                    {
                        'feature': '章节页核心/进阶/扩展布局原型',
                        'reason': '章节结构完整，知识点分类清晰，可以实现分层展示'
                    },
                    {
                        'feature': '知识点页结构化展示壳',
                        'reason': '基础字段完整，可以构建知识点的展示框架'
                    },
                    {
                        'feature': '前置知识提示基础版',
                        'reason': '依赖关系字段完整，可以实现基础的前置条件检查'
                    }
                ]
            
            # 填充不适合推荐 MVP 的功能
            if not final_assessment['can_start_recommendation_mvp']:
                final_assessment['not_suitable_for_recommendation_mvp'] = [
                    {
                        'feature': '智能推荐',
                        'reason': '缺少 estimated_time、importance_level 等推荐算法需要的字段'
                    },
                    {
                        'feature': '个性化排序',
                        'reason': '缺少用户行为数据和学习偏好字段'
                    },
                    {
                        'feature': '完整学习卡片内容展示',
                        'reason': '缺少 one_sentence_explanation、core_intuition、common_traps 等体验字段'
                    },
                    {
                        'feature': '大规模动画入口策略',
                        'reason': '缺少 animation_priority 和内容质量评估字段'
                    }
                ]
        
        # 检查数据质量
        data_quality_score = 100
        
        if 'main_knowledge_graph' in self.results['data_sources']:
            main_result = self.results['data_sources']['main_knowledge_graph']
            if main_result['status'] != 'success':
                data_quality_score -= 30
            
            total_items = main_result.get('total_items', 0)
            if total_items < 3000:
                data_quality_score -= 20
        
        if 'content_index' in self.results['data_sources']:
            index_result = self.results['data_sources']['content_index']
            if index_result['status'] != 'success':
                data_quality_score -= 20
            
            if index_result.get('generated_item_count', 0) != 3240:
                data_quality_score -= 10
        
        final_assessment['data_quality_score'] = max(0, data_quality_score)
        
        # 生成下一步建议
        if final_assessment['can_start_structure_mvp']:
            final_assessment['recommendation_for_next_steps'].append({
                'step': 1,
                'action': '开始前端结构 MVP 开发',
                'focus': '实现首页、章节页、知识点页的结构展示和基础交互',
                'estimated_duration': '2-3周',
                'priority': 'high'
            })
        else:
            # 先解决数据问题
            if final_assessment['critical_issues']:
                final_assessment['recommendation_for_next_steps'].append({
                    'step': 1,
                    'action': '补充关键数据字段',
                    'focus': '解决ID、name等核心字段的缺失或低覆盖率问题',
                    'estimated_duration': '3-5天',
                    'priority': 'critical'
                })
            
            if final_assessment['data_quality_score'] < 80:
                final_assessment['recommendation_for_next_steps'].append({
                    'step': len(final_assessment['recommendation_for_next_steps']) + 1,
                    'action': '提升数据质量',
                    'focus': '确保知识点数量正确，依赖关系完整',
                    'estimated_duration': '5-7天',
                    'priority': 'high'
                })
            
            final_assessment['recommendation_for_next_steps'].append({
                'step': len(final_assessment['recommendation_for_next_steps']) + 1,
                'action': '重新评估就绪度',
                'focus': '在数据问题解决后重新运行审计',
                'estimated_duration': '1天',
                'priority': 'medium'
            })
        
        # 如果结构 MVP 就绪但推荐 MVP 不就绪，添加补充建议
        if final_assessment['can_start_structure_mvp'] and not final_assessment['can_start_recommendation_mvp']:
            final_assessment['recommendation_for_next_steps'].append({
                'step': len(final_assessment['recommendation_for_next_steps']) + 1,
                'action': '并行补充学习体验字段',
                'focus': '在开发结构 MVP 的同时，逐步补充 estimated_time、importance_level 等字段',
                'estimated_duration': '持续进行',
                'priority': 'medium'
            })
        
        self.results['final_assessment'] = final_assessment
        
        return final_assessment
    
    def save_audit_report(self, output_path: str = None) -> str:
        """保存审计报告"""
        if output_path is None:
            output_path = self.project_root / 'assets/data/knowledge_content/reports/frontend_learning_experience_audit.json'
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换不可序列化的对象
        def make_serializable(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            else:
                return obj
        
        serializable_results = make_serializable(self.results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        
        self.log_pass(f"审计报告已保存到: {output_path}")
        
        return str(output_path)
    
    def print_summary(self):
        """打印审计摘要"""
        print("\n" + "=" * 60)
        print("前端学习体验输入数据审计摘要")
        print("=" * 60)
        
        # 打印数据源状态
        if 'data_sources' in self.results:
            print("\n[DATA SOURCES]")
            for source_name, source_result in self.results['data_sources'].items():
                status = source_result.get('status', 'unknown').upper()
                print(f"  {source_name}: {status}")
                
                if source_result.get('status') == 'success':
                    if 'total_items' in source_result:
                        print(f"    知识点数量: {source_result['total_items']}")
                    if 'schema_info' in source_result:
                        schema = source_result['schema_info']
                        print(f"    数据结构: {schema.get('structure_path', 'unknown')}")
                        print(f"    Categories: {schema.get('categories_count', 0)}")
                        print(f"    Sections: {schema.get('sections_count', 0)}")
        
        # 打印字段覆盖率
        if 'main_knowledge_graph' in self.results.get('data_sources', {}):
            main_result = self.results['data_sources']['main_knowledge_graph']
            if 'frontend_fields_status' in main_result:
                print("\n[FIELD COVERAGE]")
                for field_name, field_status in main_result['frontend_fields_status'].items():
                    status_symbol = "[PASS]" if field_status['status'] == 'found' else "[FAIL]"
                    coverage = field_status.get('coverage', 0)
                    actual_field = field_status.get('actual_field', 'none')
                    print(f"  {status_symbol} {field_name}: {coverage}% (actual: {actual_field})")
        
        # 打印ID一致性
        if 'id_consistency' in self.results:
            consistency = self.results['id_consistency']
            if 'consistency_check' in consistency:
                check = consistency['consistency_check']
                print("\n[ID CONSISTENCY]")
                print(f"  主图谱ID数量: {check.get('main_graph_count', 0)}")
                print(f"  前端图谱ID数量: {check.get('frontend_graph_count', 0)}")
                print(f"  交集数量: {check.get('intersection_count', 0)}")
                print(f"  一致性: {check.get('consistency_percentage', 0)}%")
        
        # 打印就绪度评估
        if 'frontend_readiness' in self.results:
            readiness = self.results['frontend_readiness']
            print("\n[FRONTEND READINESS]")
            print(f"  总体状态: {readiness.get('overall_readiness', 'unknown').upper()}")
            print(f"  就绪分数: {readiness.get('readiness_score', 0)}/100")
            
            if readiness.get('data_gaps'):
                print(f"  数据缺口: {len(readiness['data_gaps'])}个")
                for gap in readiness['data_gaps'][:5]:  # 只显示前5个
                    print(f"    - {gap['field']}: {gap['status']} ({gap['importance']})")
        
        # 打印最终评估
        if 'final_assessment' in self.results:
            assessment = self.results['final_assessment']
            print("\n[FINAL ASSESSMENT]")
            structure_mvp = assessment.get('can_start_structure_mvp', False)
            recommendation_mvp = assessment.get('can_start_recommendation_mvp', False)
            print(f"  可以开始结构MVP: {'是' if structure_mvp else '否'}")
            print(f"  可以开始推荐MVP: {'是' if recommendation_mvp else '否'}")
            print(f"  数据质量分数: {assessment.get('data_quality_score', 0)}/100")
            
            if assessment.get('critical_issues'):
                print(f"  关键问题: {len(assessment['critical_issues'])}个")
                for issue in assessment['critical_issues']:
                    print(f"    - {issue['field']}: {issue['status']} ({issue['importance']})")
            
            if assessment.get('suitable_for_structure_mvp'):
                print(f"\n  适合结构MVP的功能:")
                for feature in assessment['suitable_for_structure_mvp']:
                    print(f"    + {feature['feature']}")
                    print(f"      理由: {feature['reason']}")
            
            if assessment.get('not_suitable_for_recommendation_mvp'):
                print(f"\n  不适合推荐MVP的功能:")
                for feature in assessment['not_suitable_for_recommendation_mvp']:
                    print(f"    - {feature['feature']}")
                    print(f"      理由: {feature['reason']}")
        
        print("\n" + "=" * 60)
    
    def run_full_audit(self) -> Dict:
        """运行完整审计"""
        print("开始前端学习体验输入数据审计...")
        print("=" * 60)
        
        # 执行各项审计
        self.audit_main_knowledge_graph()
        self.audit_frontend_knowledge_graph()
        self.audit_content_index()
        self.check_id_consistency()
        self.assess_frontend_readiness()
        self.generate_final_assessment()
        
        # 保存报告
        report_path = self.save_audit_report()
        
        # 打印摘要
        self.print_summary()
        
        return self.results


def main():
    """主函数"""
    # 项目根目录
    project_root = Path(__file__).parent.parent
    
    # 创建审计器
    auditor = FrontendLearningExperienceAuditor(str(project_root))
    
    # 运行完整审计
    try:
        results = auditor.run_full_audit()
        print(f"\n审计完成! 详细报告已保存。")
        print(f"报告路径: {auditor.project_root / 'assets/data/knowledge_content/reports/frontend_learning_experience_audit.json'}")
    except Exception as e:
        print(f"\n[ERROR] 审计过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()