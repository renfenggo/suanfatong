#!/usr/bin/env python3
"""
练习入口与 C++14 模板入口 MVP 审计工具
验证数据结构的完整性、一致性和可用性
"""

import json
import os
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from pathlib import Path

class PracticeAndCpp14EntryMVP_Auditor:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.assets_dir = self.project_root / "assets"
        
        self.results = {
            "audit_timestamp": "",
            "project_root": str(project_root),
            "practice_entry_audit": {},
            "cpp14_template_audit": {},
            "consistency_checks": {},
            "recommendations": []
        }
    
    def log_info(self, message: str):
        """输出信息日志"""
        print(f"[INFO] {message}")
    
    def log_pass(self, message: str):
        """输出通过日志"""
        print(f"[PASS] {message}")
    
    def log_warn(self, message: str):
        """输出警告日志"""
        print(f"[WARN] {message}")
    
    def log_fail(self, message: str):
        """输出失败日志"""
        print(f"[FAIL] {message}")
    
    def load_json_file(self, file_path: Path) -> Any:
        """加载 JSON 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.log_fail(f"文件不存在: {file_path}")
            return None
        except json.JSONDecodeError as e:
            self.log_fail(f"JSON 解析错误 {file_path}: {e}")
            return None
    
    def audit_practice_entry_index(self) -> Dict:
        """审计练习入口索引"""
        self.log_info("开始审计练习入口索引...")
        
        index_file = self.data_dir / "practice_entry_mvp_index.json"
        seed_file = self.data_dir / "problem_refs_seed.json"
        
        index_data = self.load_json_file(index_file)
        if not index_data:
            return {"status": "failed", "error": "无法加载练习入口索引文件"}
        
        seed_data = self.load_json_file(seed_file)
        if not seed_data:
            return {"status": "failed", "error": "无法加载题目引用种子文件"}
        
        audit_result = {
            "status": "success",
            "file_exists": True,
            "index_info": {},
            "field_validation": {},
            "coverage_analysis": {},
            "quality_metrics": {}
        }
        
        # 基本结构验证
        index_info = {
            "version": index_data.get("version", "missing"),
            "created_date": index_data.get("created_date", "missing"),
            "total_items": index_data.get("total_items", 0),
            "total_problems": index_data.get("total_problems", 0),
            "description": index_data.get("description", "")
        }
        
        audit_result["index_info"] = index_info
        
        # 字段完整性验证
        required_fields = ["item_id", "title", "section_id", "section_name", "problems"]
        field_validation = {
            "total_index_items": len(index_data.get("index", [])),
            "valid_items": 0,
            "invalid_items": 0,
            "field_coverage": {}
        }
        
        for field in required_fields:
            field_validation["field_coverage"][field] = 0
        
        valid_item_ids = set()
        platform_coverage = defaultdict(int)
        difficulty_distribution = defaultdict(int)
        
        for item in index_data.get("index", []):
            item_valid = True
            for field in required_fields:
                if field in item:
                    field_validation["field_coverage"][field] += 1
                else:
                    item_valid = False
            
            if item_valid:
                field_validation["valid_items"] += 1
                valid_item_ids.add(item["item_id"])
            else:
                field_validation["invalid_items"] += 1
            
            # 统计问题覆盖
            for problem in item.get("problems", []):
                if "platform" in problem:
                    platform_coverage[problem["platform"]] += 1
                if "difficulty" in problem:
                    difficulty_distribution[problem["difficulty"]] += 1
        
        audit_result["field_validation"] = field_validation
        
        # 覆盖率分析
        coverage_analysis = {
            "item_coverage": f"{field_validation['valid_items']}/{index_info['total_items']}",
            "coverage_percentage": (field_validation['valid_items'] / index_info['total_items'] * 100) if index_info['total_items'] > 0 else 0,
            "unique_item_ids": len(valid_item_ids),
            "platform_diversity": len(platform_coverage),
            "platform_coverage": dict(platform_coverage),
            "difficulty_distribution": dict(difficulty_distribution)
        }
        
        audit_result["coverage_analysis"] = coverage_analysis
        
        # 质量指标
        quality_metrics = {
            "has_description": len(index_info.get("description", "")) > 0,
            "has_version": index_info.get("version") != "missing",
            "has_created_date": index_info.get("created_date") != "missing",
            "field_completeness": sum(1 for count in field_validation["field_coverage"].values() if count > 0) / len(required_fields) * 100,
            "url_validity": 0,  # 将在下一步验证
            "metadata_complete": False
        }
        
        # 验证 URL 有效性
        total_urls = 0
        valid_urls = 0
        
        for item in index_data.get("index", []):
            for problem in item.get("problems", []):
                if "url" in problem:
                    total_urls += 1
                    url = problem["url"]
                    if url.startswith("http://") or url.startswith("https://"):
                        valid_urls += 1
        
        if total_urls > 0:
            quality_metrics["url_validity"] = (valid_urls / total_urls) * 100
        
        # 验证元数据完整性
        if "metadata" in index_data:
            metadata = index_data["metadata"]
            metadata_checks = {
                "has_source_files": "source_files" in metadata and len(metadata["source_files"]) > 0,
                "has_generation_method": "generation_method" in metadata,
                "has_quality_assurance": "quality_assurance" in metadata
            }
            quality_metrics["metadata_complete"] = all(metadata_checks.values())
        
        audit_result["quality_metrics"] = quality_metrics
        
        self.log_pass(f"练习入口索引审计完成: {field_validation['valid_items']}/{index_info['total_items']} 项有效")
        
        return audit_result
    
    def audit_cpp14_template_index(self) -> Dict:
        """审计 C++14 模板索引"""
        self.log_info("开始审计 C++14 模板索引...")
        
        index_file = self.data_dir / "cpp14_template_mvp_index.json"
        
        index_data = self.load_json_file(index_file)
        if not index_data:
            return {"status": "failed", "error": "无法加载 C++14 模板索引文件"}
        
        audit_result = {
            "status": "success",
            "file_exists": True,
            "index_info": {},
            "field_validation": {},
            "coverage_analysis": {},
            "quality_metrics": {}
        }
        
        # 基本结构验证
        index_info = {
            "version": index_data.get("version", "missing"),
            "created_date": index_data.get("created_date", "missing"),
            "cpp_standard": index_data.get("cpp_standard", "missing"),
            "total_items": index_data.get("total_items", 0),
            "description": index_data.get("description", "")
        }
        
        audit_result["index_info"] = index_info
        
        # 字段完整性验证
        required_fields = ["item_id", "title", "section_id", "section_name", "template_type", "difficulty", "complexity", "source_file", "template_info", "code_reference"]
        field_validation = {
            "total_index_items": len(index_data.get("index", [])),
            "valid_items": 0,
            "invalid_items": 0,
            "field_coverage": {}
        }
        
        for field in required_fields:
            field_validation["field_coverage"][field] = 0
        
        valid_item_ids = set()
        template_types = defaultdict(int)
        difficulty_levels = defaultdict(int)
        
        for item in index_data.get("index", []):
            item_valid = True
            for field in required_fields:
                if field in item:
                    field_validation["field_coverage"][field] += 1
                else:
                    item_valid = False
            
            if item_valid:
                field_validation["valid_items"] += 1
                valid_item_ids.add(item["item_id"])
                
                # 统计模板类型和难度
                if "template_type" in item:
                    template_types[item["template_type"]] += 1
                if "difficulty" in item:
                    difficulty_levels[item["difficulty"]] += 1
            else:
                field_validation["invalid_items"] += 1
        
        audit_result["field_validation"] = field_validation
        
        # 覆盖率分析
        coverage_analysis = {
            "item_coverage": f"{field_validation['valid_items']}/{index_info['total_items']}",
            "coverage_percentage": (field_validation['valid_items'] / index_info['total_items'] * 100) if index_info['total_items'] > 0 else 0,
            "unique_item_ids": len(valid_item_ids),
            "template_type_diversity": len(template_types),
            "template_types": dict(template_types),
            "difficulty_levels": dict(difficulty_levels)
        }
        
        audit_result["coverage_analysis"] = coverage_analysis
        
        # 质量指标
        quality_metrics = {
            "has_description": len(index_info.get("description", "")) > 0,
            "has_version": index_info.get("version") != "missing",
            "has_created_date": index_info.get("created_date") != "missing",
            "cpp_standard_correct": index_info.get("cpp_standard") == "C++14",
            "field_completeness": sum(1 for count in field_validation["field_coverage"].values() if count > 0) / len(required_fields) * 100,
            "complexity_info_available": 0,
            "source_files_exist": 0,
            "practice_problems_linked": 0
        }
        
        # 验证复杂度信息可用性
        for item in index_data.get("index", []):
            if "complexity" in item:
                quality_metrics["complexity_info_available"] += 1
            if "practice_problems" in item and len(item["practice_problems"]) > 0:
                quality_metrics["practice_problems_linked"] += 1
            if "source_file" in item:
                source_file_path = self.project_root / item["source_file"]
                if source_file_path.exists():
                    quality_metrics["source_files_exist"] += 1
        
        # 计算百分比
        if len(index_data.get("index", [])) > 0:
            quality_metrics["complexity_info_available"] = (quality_metrics["complexity_info_available"] / len(index_data.get("index", []))) * 100
            quality_metrics["source_files_exist"] = (quality_metrics["source_files_exist"] / len(index_data.get("index", []))) * 100
            quality_metrics["practice_problems_linked"] = (quality_metrics["practice_problems_linked"] / len(index_data.get("index", []))) * 100
        
        audit_result["quality_metrics"] = quality_metrics
        
        self.log_pass(f"C++14 模板索引审计完成: {field_validation['valid_items']}/{index_info['total_items']} 项有效")
        
        return audit_result
    
    def run_consistency_checks(self) -> Dict:
        """运行一致性检查"""
        self.log_info("开始运行一致性检查...")
        
        practice_index = self.load_json_file(self.data_dir / "practice_entry_mvp_index.json")
        cpp14_index = self.load_json_file(self.data_dir / "cpp14_template_mvp_index.json")
        
        consistency_result = {
            "practice_cpp14_intersection": [],
            "item_id_consistency": {},
            "section_consistency": {},
            "coverage_analysis": {}
        }
        
        if practice_index and cpp14_index:
            # 检查 practice 和 cpp14 索引的交集
            practice_item_ids = {item["item_id"] for item in practice_index.get("index", [])}
            cpp14_item_ids = {item["item_id"] for item in cpp14_index.get("index", [])}
            
            intersection = practice_item_ids & cpp14_item_ids
            consistency_result["practice_cpp14_intersection"] = sorted(list(intersection))
            
            # item_id 格式一致性
            item_id_consistency = {
                "practice_items": len(practice_item_ids),
                "cpp14_items": len(cpp14_item_ids),
                "intersection_count": len(intersection),
                "intersection_percentage": (len(intersection) / len(practice_item_ids | cpp14_item_ids) * 100) if (practice_item_ids | cpp14_item_ids) else 0
            }
            
            consistency_result["item_id_consistency"] = item_id_consistency
            
            # 章节一致性
            practice_sections = {item["section_id"] for item in practice_index.get("index", [])}
            cpp14_sections = {item["section_id"] for item in cpp14_index.get("index", [])}
            
            section_consistency = {
                "practice_sections": len(practice_sections),
                "cpp14_sections": len(cpp14_sections),
                "shared_sections": len(practice_sections & cpp14_sections),
                "section_intersection": sorted(list(practice_sections & cpp14_sections))
            }
            
            consistency_result["section_consistency"] = section_consistency
            
            # 覆盖率分析
            coverage_analysis = {
                "practice_only_items": sorted(list(practice_item_ids - cpp14_item_ids)),
                "cpp14_only_items": sorted(list(cpp14_item_ids - practice_item_ids)),
                "total_unique_items": len(practice_item_ids | cpp14_item_ids),
                "practice_coverage": len(practice_item_ids) / len(practice_item_ids | cpp14_item_ids) * 100 if (practice_item_ids | cpp14_item_ids) else 0,
                "cpp14_coverage": len(cpp14_item_ids) / len(practice_item_ids | cpp14_item_ids) * 100 if (practice_item_ids | cpp14_item_ids) else 0
            }
            
            consistency_result["coverage_analysis"] = coverage_analysis
        
        self.log_pass("一致性检查完成")
        return consistency_result
    
    def generate_recommendations(self) -> List[Dict]:
        """生成改进建议"""
        self.log_info("生成改进建议...")
        
        recommendations = []
        
        practice_audit = self.results.get("practice_entry_audit", {})
        cpp14_audit = self.results.get("cpp14_template_audit", {})
        consistency_checks = self.results.get("consistency_checks", {})
        
        # 练习入口建议
        if practice_audit.get("status") == "success":
            coverage = practice_audit.get("coverage_analysis", {})
            quality = practice_audit.get("quality_metrics", {})
            
            if coverage.get("coverage_percentage", 0) < 100:
                recommendations.append({
                    "category": "practice_entry",
                    "priority": "high",
                    "recommendation": f"补充练习入口缺失项，当前覆盖率 {coverage.get('coverage_percentage', 0):.1f}%",
                    "action": "为缺失的 item_id 添加练习问题"
                })
            
            if quality.get("url_validity", 0) < 100:
                recommendations.append({
                    "category": "practice_entry",
                    "priority": "medium",
                    "recommendation": f"修复无效 URL，当前有效比例 {quality.get('url_validity', 0):.1f}%",
                    "action": "检查并修复无效的题目链接"
                })
        
        # C++14 模板建议
        if cpp14_audit.get("status") == "success":
            coverage = cpp14_audit.get("coverage_analysis", {})
            quality = cpp14_audit.get("quality_metrics", {})
            
            if coverage.get("coverage_percentage", 0) < 100:
                recommendations.append({
                    "category": "cpp14_template",
                    "priority": "high",
                    "recommendation": f"补充 C++14 模板缺失项，当前覆盖率 {coverage.get('coverage_percentage', 0):.1f}%",
                    "action": "为缺失的 item_id 添加模板信息"
                })
            
            if quality.get("source_files_exist", 0) < 100:
                recommendations.append({
                    "category": "cpp14_template",
                    "priority": "medium",
                    "recommendation": f"补充缺失的源文件，当前存在比例 {quality.get('source_files_exist', 0):.1f}%",
                    "action": "创建或修复引用的算法单元文件"
                })
        
        # 一致性建议
        if consistency_checks.get("practice_cpp14_intersection"):
            intersection_count = len(consistency_checks["practice_cpp14_intersection"])
            recommendations.append({
                "category": "consistency",
                "priority": "low",
                "recommendation": f"练习入口和 C++14 模板有 {intersection_count} 个交集知识点，可考虑统一展示",
                "action": "在知识点页同时显示练习和模板入口"
            })
        
        # 总体建议
        recommendations.append({
            "category": "general",
            "priority": "high",
            "recommendation": "扩展知识点覆盖范围",
            "action": "按照优先级为更多知识点添加练习入口和 C++14 模板"
        })
        
        recommendations.append({
            "category": "general",
            "priority": "medium",
            "recommendation": "增强元数据完整性",
            "action": "完善所有索引文件的元数据信息"
        })
        
        return recommendations
    
    def generate_final_report(self) -> Dict:
        """生成最终审计报告"""
        from datetime import datetime
        
        self.results["audit_timestamp"] = datetime.now().isoformat()
        
        # 运行各项审计
        self.results["practice_entry_audit"] = self.audit_practice_entry_index()
        self.results["cpp14_template_audit"] = self.audit_cpp14_template_index()
        self.results["consistency_checks"] = self.run_consistency_checks()
        self.results["recommendations"] = self.generate_recommendations()
        
        # 总体评估
        practice_status = self.results["practice_entry_audit"].get("status", "unknown")
        cpp14_status = self.results["cpp14_template_audit"].get("status", "unknown")
        
        overall_assessment = {
            "practice_entry_status": practice_status,
            "cpp14_template_status": cpp14_status,
            "overall_status": "success" if practice_status == "success" and cpp14_status == "success" else "partial",
            "ready_for_integration": practice_status == "success" and cpp14_status == "success",
            "total_practice_items": self.results["practice_entry_audit"].get("index_info", {}).get("total_items", 0),
            "total_cpp14_items": self.results["cpp14_template_audit"].get("index_info", {}).get("total_items", 0),
            "total_practice_problems": self.results["practice_entry_audit"].get("index_info", {}).get("total_problems", 0),
            "intersection_count": len(self.results["consistency_checks"].get("practice_cpp14_intersection", [])),
            "recommendations_count": len(self.results["recommendations"])
        }
        
        self.results["overall_assessment"] = overall_assessment
        
        return self.results

def main():
    """主函数"""
    print("============================================================")
    print("开始练习入口与 C++14 模板入口 MVP 审计...")
    print("============================================================")
    
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建审计器
    auditor = PracticeAndCpp14EntryMVP_Auditor(project_root)
    
    # 生成审计报告
    report = auditor.generate_final_report()
    
    # 保存报告
    report_path = Path(project_root) / "data" / "practice_and_cpp14_entry_mvp_plan.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("============================================================")
    print("练习入口与 C++14 模板入口 MVP 审计摘要")
    print("============================================================")
    
    overall = report.get("overall_assessment", {})
    print(f"[OVERALL] 总体状态: {overall.get('overall_status', 'unknown')}")
    print(f"[OVERALL] 可接入前端: {overall.get('ready_for_integration', False)}")
    print(f"[PRACTICE] 练习入口: {overall.get('total_practice_items', 0)} 个知识点, {overall.get('total_practice_problems', 0)} 个题目")
    print(f"[CPP14] C++14 模板: {overall.get('total_cpp14_items', 0)} 个知识点")
    print(f"[INTERSECTION] 交集知识点: {overall.get('intersection_count', 0)} 个")
    print(f"[RECOMMENDATIONS] 改进建议: {overall.get('recommendations_count', 0)} 条")
    
    print("============================================================")
    print(f"审计报告已保存到: {report_path}")
    print("============================================================")

if __name__ == "__main__":
    main()