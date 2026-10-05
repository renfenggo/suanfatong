#!/usr/bin/env python3
"""
Stage5-HardKnowledge Batch3 预备审计脚本
只读审计，不修改任何现有文件
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, Tuple
import datetime

class Stage5Batch3ReadinessAuditor:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.audit_time = datetime.datetime.now().isoformat()
        self.results = {
            "audit_time": self.audit_time,
            "project_root": str(project_root),
            "stable_state_check": {},
            "used_candidates": {},
            "candidate_pool": {},
            "filtered_candidates": {},
            "risk_audit": {},
            "section_capacity": {},
            "batch3_recommendations": {}
        }
        
    def load_json(self, relative_path: str) -> Dict:
        """加载 JSON 文件"""
        file_path = self.project_root / relative_path
        if not file_path.exists():
            print(f"警告: 文件不存在 {file_path}")
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_all_items_from_graph(self, graph_data: Dict) -> Tuple[List[Dict], Dict]:
        """从图谱数据中提取所有 items 和章节信息"""
        all_items = []
        section_info = {}
        
        categories = graph_data.get("categories", [])
        if isinstance(categories, list):
            for cat_idx, cat_data in enumerate(categories):
                cat_name = cat_data.get("name", f"cat_{cat_idx}")
                sections = cat_data.get("sections", [])
                
                if isinstance(sections, list):
                    for sec_data in sections:
                        sec_id = sec_data.get("id")
                        sec_name = sec_data.get("name", "unknown")
                        items = sec_data.get("items", [])
                        
                        # 记录章节信息
                        if sec_id:
                            section_info[sec_id] = {
                                "id": sec_id,
                                "name": sec_name,
                                "category": cat_name,
                                "item_count": len(items)
                            }
                        
                        # 提取所有 items
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict):
                                    # 添加章节信息到 item
                                    item_with_section = item.copy()
                                    item_with_section["section_id"] = sec_id
                                    item_with_section["section_name"] = sec_name
                                    item_with_section["category_name"] = cat_name
                                    all_items.append(item_with_section)
        
        return all_items, section_info
    
    def verify_stable_state(self) -> Dict:
        """步骤一：验证当前稳定状态"""
        print("=== 步骤一：验证当前稳定状态 ===")
        
        # 读取主图谱
        main_graph = self.load_json("merged_knowledge_graph_item_dependencies_refined.json")
        main_items, main_sections = self.extract_all_items_from_graph(main_graph)
        main_item_ids = set(item.get("id") for item in main_items)
        
        # 读取前端图谱
        frontend_graph = self.load_json("assets/data/knowledge/io_v4_4.json")
        frontend_items, frontend_sections = self.extract_all_items_from_graph(frontend_graph)
        frontend_item_ids = set(item.get("id") for item in frontend_items)
        
        # 读取内容索引
        content_index = self.load_json("assets/data/knowledge_content/content_index.json")
        
        stable_check = {
            "main_graph_item_count": len(main_items),
            "frontend_graph_item_count": len(frontend_items),
            "content_index_coverage": content_index.get("generated_item_count", 0),
            "main_graph_section_count": len(main_sections),
            "frontend_graph_section_count": len(frontend_sections),
            "id_sets_match": main_item_ids == frontend_item_ids,
            "section_sets_match": set(main_sections.keys()) == set(frontend_sections.keys()),
            "main_item_ids_sample": list(main_item_ids)[:5] if main_item_ids else [],
            "frontend_item_ids_sample": list(frontend_item_ids)[:5] if frontend_item_ids else [],
            "main_sections_sample": dict(list(main_sections.items())[:3]) if main_sections else {},
            "frontend_sections_sample": dict(list(frontend_sections.items())[:3]) if frontend_sections else {}
        }
        
        # 验证是否为 3240
        is_stable = (
            stable_check["main_graph_item_count"] == 3240 and
            stable_check["frontend_graph_item_count"] == 3240 and
            stable_check["content_index_coverage"] == 3240 and
            stable_check["id_sets_match"] and
            stable_check["section_sets_match"]
        )
        
        stable_check["is_stable_3240"] = is_stable
        stable_check["stability_status"] = "[PASS] 稳定" if is_stable else "[FAIL] 不稳定"
        
        self.results["stable_state_check"] = stable_check
        self.main_items_cache = main_items  # 缓存供后续使用
        self.main_sections_cache = main_sections  # 缓存供后续使用
        
        print(f"主图谱 item_count: {stable_check['main_graph_item_count']}")
        print(f"前端图谱 item_count: {stable_check['frontend_graph_item_count']}")
        print(f"内容索引覆盖: {stable_check['content_index_coverage']}")
        print(f"主图谱 section_count: {stable_check['main_graph_section_count']}")
        print(f"前端图谱 section_count: {stable_check['frontend_graph_section_count']}")
        print(f"ID 集合匹配: {stable_check['id_sets_match']}")
        print(f"章节集合匹配: {stable_check['section_sets_match']}")
        print(f"稳定性状态: {stable_check['stability_status']}")
        
        return stable_check
    
    def identify_used_candidates(self) -> Tuple[Set[str], Dict]:
        """步骤二：识别已使用候选"""
        print("\n=== 步骤二：识别已使用候选 ===")
        
        # 读取 Batch1 映射
        batch1_mapping = self.load_json("data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json")
        # 读取 Batch2 映射
        batch2_mapping = self.load_json("data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json")
        
        used_candidates = {
            "batch1": [],
            "batch2": [],
            "all_used_ids": set(),
            "all_used_titles": set()
        }
        
        # 自动探测字段并提取 Batch1
        if batch1_mapping:
            if isinstance(batch1_mapping, list):
                batch1_data = batch1_mapping
            elif "mappings" in batch1_mapping:
                batch1_data = batch1_mapping["mappings"]
            else:
                batch1_data = [batch1_mapping] if not isinstance(batch1_mapping, dict) else []
            
            for entry in batch1_data:
                if isinstance(entry, dict):
                    # 自动探测候选ID字段
                    candidate_id = entry.get("candidate_id") or entry.get("id") or entry.get("candidate")
                    title = entry.get("title") or entry.get("name") or entry.get("candidate_title")
                    item_id = entry.get("item_id") or entry.get("assigned_item_id") or entry.get("mapped_item_id")
                    
                    if candidate_id:
                        used_candidates["batch1"].append({
                            "candidate_id": candidate_id,
                            "title": title,
                            "item_id": item_id
                        })
                        used_candidates["all_used_ids"].add(str(candidate_id))
                        if title:
                            used_candidates["all_used_titles"].add(str(title).strip().lower())
        
        # 自动探测字段并提取 Batch2
        if batch2_mapping:
            if isinstance(batch2_mapping, list):
                batch2_data = batch2_mapping
            elif "mappings" in batch2_mapping:
                batch2_data = batch2_mapping["mappings"]
            else:
                batch2_data = [batch2_mapping] if not isinstance(batch2_mapping, dict) else []
            
            for entry in batch2_data:
                if isinstance(entry, dict):
                    # 自动探测候选ID字段
                    candidate_id = entry.get("candidate_id") or entry.get("id") or entry.get("candidate")
                    title = entry.get("title") or entry.get("name") or entry.get("candidate_title")
                    item_id = entry.get("item_id") or entry.get("assigned_item_id") or entry.get("mapped_item_id")
                    
                    if candidate_id:
                        used_candidates["batch2"].append({
                            "candidate_id": candidate_id,
                            "title": title,
                            "item_id": item_id
                        })
                        used_candidates["all_used_ids"].add(str(candidate_id))
                        if title:
                            used_candidates["all_used_titles"].add(str(title).strip().lower())
        
        used_summary = {
            "batch1_count": len(used_candidates["batch1"]),
            "batch2_count": len(used_candidates["batch2"]),
            "total_used_count": len(used_candidates["all_used_ids"]),
            "batch1_sample": used_candidates["batch1"][:3],
            "batch2_sample": used_candidates["batch2"][:3]
        }
        
        self.results["used_candidates"] = used_summary
        print(f"Batch1 已使用候选数: {used_summary['batch1_count']}")
        print(f"Batch2 已使用候选数: {used_summary['batch2_count']}")
        print(f"总计已使用候选数: {used_summary['total_used_count']}")
        
        return used_candidates["all_used_ids"], used_candidates["all_used_titles"], used_summary
    
    def read_candidate_pool(self) -> List[Dict]:
        """步骤三：读取候选池"""
        print("\n=== 步骤三：读取候选池 ===")
        
        # 按优先级顺序尝试读取候选池文件
        candidate_files = [
            "data/stage5_hard_knowledge_cleaned_candidates.json",
            "data/stage5_hard_knowledge_ready_core_candidates.json",
            "data/stage5_hard_knowledge_candidate_pool_1200.json"
        ]
        
        all_candidates = []
        source_info = []
        
        for file_path in candidate_files:
            data = self.load_json(file_path)
            if not data:
                continue
            
            # 自动探测数据结构
            if isinstance(data, list):
                candidates = data
            elif "candidates" in data:
                candidates = data["candidates"]
            elif "items" in data:
                candidates = data["items"]
            else:
                candidates = [data] if not isinstance(data, dict) else []
            
            # 规范化候选字段
            normalized = []
            for candidate in candidates:
                if isinstance(candidate, dict):
                    normalized_candidate = {
                        "original_id": candidate.get("candidate_id") or candidate.get("id") or candidate.get("candidate"),
                        "title": candidate.get("title") or candidate.get("name") or candidate.get("candidate_title"),
                        "category": candidate.get("category"),
                        "subcategory": candidate.get("subcategory"),
                        "section_id": candidate.get("target_section") or candidate.get("section_id") or candidate.get("section"),
                        "difficulty": candidate.get("difficulty") or candidate.get("tier") or candidate.get("source_tier"),
                        "duplicate_group": candidate.get("duplicate_group") or candidate.get("duplicate_risk") or candidate.get("merge_or_collapse"),
                        "dependencies": candidate.get("direct_pre") or candidate.get("dependencies") or candidate.get("dependency"),
                        "status": candidate.get("status") or candidate.get("state"),
                        "source_file": file_path
                    }
                    if normalized_candidate["original_id"]:
                        normalized.append(normalized_candidate)
            
            all_candidates.extend(normalized)
            source_info.append({
                "file": file_path,
                "count": len(normalized)
            })
        
        # 去重（按 original_id）
        seen_ids = set()
        unique_candidates = []
        for candidate in all_candidates:
            cid = str(candidate["original_id"])
            if cid not in seen_ids:
                seen_ids.add(cid)
                unique_candidates.append(candidate)
        
        pool_summary = {
            "source_files": source_info,
            "total_raw_count": len(all_candidates),
            "unique_count": len(unique_candidates),
            "field_sample": unique_candidates[:3] if unique_candidates else []
        }
        
        self.results["candidate_pool"] = pool_summary
        print(f"候选池来源文件: {len(source_info)}")
        print(f"原始候选数: {pool_summary['total_raw_count']}")
        print(f"去重后候选数: {pool_summary['unique_count']}")
        
        return unique_candidates
    
    def filter_batch3_candidates(self, candidates: List[Dict], used_ids: Set[str], used_titles: Set[str]) -> Dict:
        """步骤四：过滤 Batch3 候选"""
        print("\n=== 步骤四：过滤 Batch3 候选 ===")
        
        # 读取 defer/drop 列表
        defer_drop_data = self.load_json("data/stage5_hard_knowledge_defer_or_drop_candidates.json")
        defer_drop_ids = set()
        if defer_drop_data:
            if isinstance(defer_drop_data, list):
                defer_drop_list = defer_drop_data
            elif "candidates" in defer_drop_data:
                defer_drop_list = defer_drop_data["candidates"]
            else:
                defer_drop_list = [defer_drop_data] if not isinstance(defer_drop_data, dict) else []
            
            for item in defer_drop_list:
                if isinstance(item, dict):
                    cid = item.get("candidate_id") or item.get("id")
                    if cid:
                        defer_drop_ids.add(str(cid))
        
        # 读取当前图谱标题（用于重复检测） - 使用缓存的数据
        main_graph_titles = set()
        if hasattr(self, 'main_items_cache'):
            for item in self.main_items_cache:
                title = item.get("name") or item.get("title") or item.get("alias")
                if title:
                    main_graph_titles.add(str(title).strip().lower())
        
        # 过滤候选
        original_count = len(candidates)
        used_by_batch1 = []
        used_by_batch2 = []
        defer_or_drop = []
        duplicate_or_merge_risk = []
        remaining = []
        
        # 精确区分 Batch1/Batch2
        batch1_mapping = self.load_json("data/stage5_hard_knowledge_batch1_full500_candidate_to_item_id_mapping.json")
        batch2_mapping = self.load_json("data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json")
        
        batch1_ids = set()
        batch2_ids = set()
        
        if batch1_mapping:
            if isinstance(batch1_mapping, list):
                batch1_data = batch1_mapping
            elif "mappings" in batch1_mapping:
                batch1_data = batch1_mapping["mappings"]
            else:
                batch1_data = [batch1_mapping] if not isinstance(batch1_mapping, dict) else []
            
            for entry in batch1_data:
                if isinstance(entry, dict):
                    cid = entry.get("candidate_id") or entry.get("id")
                    if cid:
                        batch1_ids.add(str(cid))
        
        if batch2_mapping:
            if isinstance(batch2_mapping, list):
                batch2_data = batch2_mapping
            elif "mappings" in batch2_mapping:
                batch2_data = batch2_mapping["mappings"]
            else:
                batch2_data = [batch2_mapping] if not isinstance(batch2_mapping, dict) else []
            
            for entry in batch2_data:
                if isinstance(entry, dict):
                    cid = entry.get("candidate_id") or entry.get("id")
                    if cid:
                        batch2_ids.add(str(cid))
        
        for candidate in candidates:
            cid = str(candidate["original_id"])
            title = str(candidate["title"]).strip().lower() if candidate["title"] else ""
            
            # 检查是否已使用 - 精确区分
            if cid in batch1_ids:
                used_by_batch1.append(candidate)
                continue
            if cid in batch2_ids:
                used_by_batch2.append(candidate)
                continue
            
            # 检查是否 defer/drop
            if cid in defer_drop_ids:
                defer_or_drop.append(candidate)
                continue
            
            # 检查标题重复
            if title and title in main_graph_titles:
                duplicate_or_merge_risk.append(candidate)
                continue
            if title and title in used_titles:
                duplicate_or_merge_risk.append(candidate)
                continue
            
            # 检查明确的 duplicate/merge 标记
            dup_risk = str(candidate["duplicate_group"]).lower() if candidate["duplicate_group"] else ""
            if dup_risk and ("merge" in dup_risk or "collapse" in dup_risk or "duplicate" in dup_risk):
                duplicate_or_merge_risk.append(candidate)
                continue
            
            remaining.append(candidate)
        
        filter_result = {
            "original_candidate_count": original_count,
            "batch1_mapping_total_count": len(batch1_ids),
            "batch2_mapping_total_count": len(batch2_ids),
            "used_by_batch1_count": len(used_by_batch1),
            "used_by_batch2_count": len(used_by_batch2),
            "batch2_found_in_current_pool_count": len(used_by_batch2),
            "defer_or_drop_count": len(defer_or_drop),
            "duplicate_or_merge_risk_count": len(duplicate_or_merge_risk),
            "remaining_candidate_count": len(remaining),
            "remaining_sample": remaining[:5] if remaining else [],
            "filter_summary": {
                "排除_已使用": len(used_by_batch1) + len(used_by_batch2),
                "排除_defer_drop": len(defer_or_drop),
                "排除_重复合并风险": len(duplicate_or_merge_risk),
                "剩余可用": len(remaining)
            },
            "batch2_discrepancy_explanation": {
                "batch2_mapping_total": len(batch2_ids),
                "batch2_found_in_current_pool": len(used_by_batch2),
                "explanation": f"Batch2 mapping记录了{len(batch2_ids)}个已使用候选，但当前候选池中只匹配到{len(used_by_batch2)}个。差异原因：当前候选池主要来自ready_core_candidates(842个)和candidate_pool_1200(138个)，可能不包含所有Batch2使用的候选源。这不影响Batch3剩余候选判断，因为filtering已正确排除池中匹配的Batch2候选。"
            }
        }
        
        self.results["filtered_candidates"] = filter_result
        print(f"原始候选数: {original_count}")
        print(f"已使用 (Batch1): {len(used_by_batch1)}")
        print(f"已使用 (Batch2) - mapping总数: {len(batch2_ids)}, 当前池中匹配: {len(used_by_batch2)}")
        print(f"Defer/Drop: {len(defer_or_drop)}")
        print(f"重复/合并风险: {len(duplicate_or_merge_risk)}")
        print(f"剩余可用候选: {len(remaining)}")
        print(f"\nBatch2统计差异说明:")
        print(f"  Batch2 mapping总数: {len(batch2_ids)}")
        print(f"  当前候选池中匹配: {len(used_by_batch2)}")
        print(f"  差异: {len(batch2_ids) - len(used_by_batch2)}个候选不在当前池中")
        print(f"  原因: 当前候选池来源有限，可能未覆盖所有Batch2使用的候选源")
        
        return {
            "remaining": remaining,
            "filter_result": filter_result
        }
    
    def candidate_risk_audit(self, candidates: List[Dict]) -> Dict:
        """步骤五：候选风险审计"""
        print("\n=== 步骤五：候选风险审计 ===")
        
        risk_types = {
            "exact_title_duplicate": [],
            "near_title_duplicate": [],
            "ambiguous_section": [],
            "overcrowded_section": [],
            "cross_domain_category": [],
            "low_value_or_too_general": [],
            "dependency_missing": [],
            "content_generation_risk": []
        }
        
        # 记录每个候选的风险类型
        candidate_risks = {}  # candidate_id -> set of risk_types
        
        title_counter = Counter()
        section_counter = Counter()
        
        # 统计标题和章节分布
        for candidate in candidates:
            title = str(candidate["title"]).strip().lower() if candidate["title"] else ""
            section = str(candidate["section_id"]).strip() if candidate["section_id"] else ""
            
            if title:
                title_counter[title] += 1
            if section:
                section_counter[section] += 1
        
        # 检测风险
        for candidate in candidates:
            cid = str(candidate["original_id"])
            title = str(candidate["title"]).strip().lower() if candidate["title"] else ""
            section = str(candidate["section_id"]).strip() if candidate["section_id"] else ""
            category = str(candidate["category"]).strip().lower() if candidate["category"] else ""
            
            risks = set()
            
            # 精确标题重复
            if title and title_counter[title] > 1:
                risk_types["exact_title_duplicate"].append(candidate)
                risks.add("exact_title_duplicate")
            
            # 章节模糊
            if not section or section in ["unknown", "tbd", "待定"]:
                risk_types["ambiguous_section"].append(candidate)
                risks.add("ambiguous_section")
            
            # 低价值或过于通用
            if title:
                generic_keywords = ["基础", "入门", "简介", "概述", "总结", "介绍", "基本", "简单", "初步"]
                if any(keyword in title for keyword in generic_keywords):
                    risk_types["low_value_or_too_general"].append(candidate)
                    risks.add("low_value_or_too_general")
            
            # 依赖缺失
            deps = candidate["dependencies"]
            if not deps or (isinstance(deps, list) and len(deps) == 0):
                risk_types["dependency_missing"].append(candidate)
                risks.add("dependency_missing")
            
            # 内容生成风险（标题过短或过长）
            if title:
                if len(title) < 4 or len(title) > 50:
                    risk_types["content_generation_risk"].append(candidate)
                    risks.add("content_generation_risk")
            
            # 记录该候选的风险类型
            if risks:
                candidate_risks[cid] = risks
        
        # 统计去重后的风险候选数
        unique_risky_candidate_ids = set(candidate_risks.keys())
        unique_risky_candidate_count = len(unique_risky_candidate_ids)
        safe_candidate_count = len(candidates) - unique_risky_candidate_count
        risk_ratio = (unique_risky_candidate_count / len(candidates) * 100) if len(candidates) > 0 else 0
        
        # 依赖缺失统计
        dependency_missing_count = len(risk_types["dependency_missing"])
        dependency_missing_ratio = (dependency_missing_count / len(candidates) * 100) if len(candidates) > 0 else 0
        
        risk_summary = {}
        for risk_type, risky_candidates in risk_types.items():
            risk_summary[risk_type] = {
                "count": len(risky_candidates),
                "sample": risky_candidates[:3] if risky_candidates else []
            }
        
        # 添加汇总统计
        risk_summary["_summary"] = {
            "total_candidates": len(candidates),
            "risk_type_counts": {rt: info["count"] for rt, info in risk_summary.items() if rt != "_summary"},
            "unique_risky_candidate_count": unique_risky_candidate_count,
            "safe_candidate_count": max(0, safe_candidate_count),  # 确保不为负
            "risk_ratio": min(100, risk_ratio),  # 确保不超过100%
            "dependency_missing_count": dependency_missing_count,
            "dependency_missing_ratio": dependency_missing_ratio
        }
        
        self.results["risk_audit"] = risk_summary
        print("风险统计:")
        for risk_type, info in risk_summary.items():
            if risk_type != "_summary":
                print(f"  {risk_type}: {info['count']}")
        
        print(f"\n风险汇总:")
        print(f"  总候选数: {risk_summary['_summary']['total_candidates']}")
        print(f"  去重后风险候选数: {risk_summary['_summary']['unique_risky_candidate_count']}")
        print(f"  安全候选数: {risk_summary['_summary']['safe_candidate_count']}")
        print(f"  风险比例: {risk_summary['_summary']['risk_ratio']:.1f}%")
        print(f"  依赖缺失数: {risk_summary['_summary']['dependency_missing_count']}")
        print(f"  依赖缺失比例: {risk_summary['_summary']['dependency_missing_ratio']:.1f}%")
        
        return risk_summary
    
    def section_capacity_audit(self) -> Dict:
        """步骤六：章节容量审计"""
        print("\n=== 步骤六：章节容量审计 ===")
        
        # 使用缓存的主图谱数据
        if not hasattr(self, 'main_items_cache') or not hasattr(self, 'main_sections_cache'):
            print("警告: 缺少缓存数据，跳过章节容量审计")
            return {
                "total_sections": 0,
                "top_15_sections": [],
                "high_capacity_sections": [],
                "medium_capacity_sections": [],
                "low_capacity_sections": [],
                "recommendations": {
                    "avoid_expanding": [],
                    "priority_reinforce": [],
                    "manual_review": []
                }
            }
        
        section_counts = {}
        section_details = defaultdict(lambda: {"categories": set(), "items": []})
        
        # 使用缓存的章节信息
        for sec_id, sec_info in self.main_sections_cache.items():
            section_counts[sec_id] = sec_info["item_count"]
            section_details[sec_id]["categories"].add(sec_info["category"])
            section_details[sec_id]["name"] = sec_info["name"]
        
        # 统计每个章节的 items（使用缓存的 items）
        for item in self.main_items_cache:
            section_id = item.get("section_id")
            title = item.get("name") or item.get("title") or item.get("alias", "")
            
            if section_id and section_id in section_details:
                section_details[section_id]["items"].append(title)
        
        # 排序
        sorted_sections = sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 分类章节
        high_capacity_sections = [s for s in sorted_sections if s[1] > 100]
        medium_capacity_sections = [s for s in sorted_sections if 50 <= s[1] <= 100]
        low_capacity_sections = [s for s in sorted_sections if s[1] < 50]
        
        capacity_audit = {
            "total_sections": len(section_counts),
            "top_15_sections": [
                {
                    "section_id": sid,
                    "section_name": section_details[sid]["name"],
                    "item_count": count,
                    "categories": list(section_details[sid]["categories"])[:5],
                    "sample_items": section_details[sid]["items"][:3]
                }
                for sid, count in sorted_sections[:15]
            ],
            "high_capacity_sections": [
                {
                    "section_id": sid,
                    "section_name": section_details[sid]["name"],
                    "item_count": count
                }
                for sid, count in high_capacity_sections
            ],
            "medium_capacity_sections": [
                {
                    "section_id": sid,
                    "section_name": section_details[sid]["name"],
                    "item_count": count
                }
                for sid, count in medium_capacity_sections
            ],
            "low_capacity_sections": [
                {
                    "section_id": sid,
                    "section_name": section_details[sid]["name"],
                    "item_count": count
                }
                for sid, count in low_capacity_sections[:20]
            ],
            "recommendations": {
                "avoid_expanding": [sid for sid, count in high_capacity_sections],
                "priority_reinforce": [sid for sid, count in low_capacity_sections[:10]],
                "manual_review": []
            }
        }
        
        self.results["section_capacity"] = capacity_audit
        print(f"总章节数: {capacity_audit['total_sections']}")
        print(f"高容量章节 (>100): {len(high_capacity_sections)}")
        print(f"中等容量章节 (50-100): {len(medium_capacity_sections)}")
        print(f"低容量章节 (<50): {len(low_capacity_sections)}")
        
        # 显示前 10 个高容量章节
        print("\n前 10 个高容量章节:")
        for i, (sid, count) in enumerate(sorted_sections[:10], 1):
            sec_name = section_details[sid]["name"]
            print(f"  {i}. {sid} ({sec_name}): {count} 个知识点")
        
        return capacity_audit
    
    def generate_batch3_recommendations(self, filter_result: Dict, risk_summary: Dict, capacity_audit: Dict) -> Dict:
        """步骤七：生成 Batch3 启动建议"""
        print("\n=== 步骤七：生成 Batch3 启动建议 ===")
        
        remaining_count = filter_result["remaining_candidate_count"]
        
        # 使用修正后的风险统计
        summary = risk_summary.get("_summary", {})
        unique_risky_count = summary.get("unique_risky_candidate_count", 0)
        safe_count = summary.get("safe_candidate_count", 0)
        risk_ratio = summary.get("risk_ratio", 0)
        dep_missing_count = summary.get("dependency_missing_count", 0)
        dep_missing_ratio = summary.get("dependency_missing_ratio", 0)
        
        # 检查启动条件
        stable = self.results["stable_state_check"].get("is_stable_3240", False)
        section_ambiguity = risk_summary.get("ambiguous_section", {}).get("count", 0)
        
        # 启动条件判断
        blocking_conditions = []
        
        if not stable:
            blocking_conditions.append("系统稳定性检查未通过")
        
        if unique_risky_count / remaining_count > 0.5:
            blocking_conditions.append(f"风险候选比例过高 ({risk_ratio:.1f}%)")
    
        if dep_missing_ratio > 50:
            blocking_conditions.append(f"依赖缺失比例过高 ({dep_missing_ratio:.1f}%)")
        
        if safe_count < 30:
            blocking_conditions.append(f"安全候选数量不足 (仅{safe_count}个)")
        
        if section_ambiguity > remaining_count * 0.3:
            blocking_conditions.append(f"章节信息缺失过多 ({section_ambiguity}个候选无section_id)")
        
        # 生成启动建议
        if blocking_conditions:
            immediate_launch = "否，建议等待"
            launch_status = "BLOCKED"
            recommended_size = 0
            reason = f"存在阻塞性问题: {', '.join(blocking_conditions)}"
            next_steps = [
                "先补齐依赖信息 (dependency)",
                "先补齐章节信息 (section_id)",
                "等待一号、二号线程全部验收完成",
                f"当前{remaining_count}个候选中{dep_missing_count}个缺依赖，需先解决",
                "建议后续先做30-50个候选的试点，而非大规模Batch3",
                "再次验证稳定状态和候选质量后再启动"
            ]
        else:
            if remaining_count >= 400:
                recommended_size = 300
                reason = "候选充足，风险可控，建议较大规模"
            elif remaining_count >= 200:
                recommended_size = 150
                reason = "候选适中，风险可控，建议中等规模"
            elif remaining_count >= 100:
                recommended_size = 80
                reason = "候选有限但风险可控，建议保守规模"
            else:
                recommended_size = min(remaining_count, 50)
                reason = "候选有限，建议极小规模试点"
            
            immediate_launch = "是，可以启动"
            launch_status = "READY"
            next_steps = [
                "确认一号、二号线程已完成",
                "验证最终候选池质量",
                f"启动Batch3，规模{recommended_size}个候选",
                "优先补强低覆盖章节",
                "避免继续扩张高容量章节"
            ]
        
        recommendations = {
            "immediate_launch": immediate_launch,
            "launch_status": launch_status,
            "recommended_batch_size": recommended_size,
            "recommendation_reason": reason,
            "blocking_conditions": blocking_conditions,
            "risk_assessment": {
                "total_candidates": remaining_count,
                "unique_risky_candidate_count": unique_risky_count,
                "safe_candidate_count": safe_count,
                "risk_ratio": f"{risk_ratio:.1f}%",
                "dependency_missing_count": dep_missing_count,
                "dependency_missing_ratio": f"{dep_missing_ratio:.1f}%"
            },
            "priority_strategy": {
                "high_priority_sections": capacity_audit["recommendations"]["priority_reinforce"][:5],
                "avoid_sections": capacity_audit["recommendations"]["avoid_expanding"][:5],
                "risk_mitigation": "排除高风险候选，优先低风险章节"
            },
            "category_distribution": "均衡分布，优先补强低覆盖章节",
            "preconditions": {
                "stable_state_required": True,
                "stable_state_met": stable,
                "dependency_ratio_acceptable": dep_missing_ratio <= 50,
                "safe_candidates_sufficient": safe_count >= 30
            },
            "next_steps": next_steps
        }
        
        self.results["batch3_recommendations"] = recommendations
        print(f"是否立即启动: {recommendations['immediate_launch']}")
        print(f"启动状态: {recommendations['launch_status']}")
        print(f"推荐规模: {recommendations['recommended_batch_size']}")
        print(f"推荐理由: {recommendations['recommendation_reason']}")
        
        if blocking_conditions:
            print(f"阻塞性问题:")
            for condition in blocking_conditions:
                print(f"  - {condition}")
        
        print(f"风险评估:")
        print(f"  总候选数: {recommendations['risk_assessment']['total_candidates']}")
        print(f"  去重后风险候选数: {recommendations['risk_assessment']['unique_risky_candidate_count']}")
        print(f"  安全候选数: {recommendations['risk_assessment']['safe_candidate_count']}")
        print(f"  风险比例: {recommendations['risk_assessment']['risk_ratio']}")
        print(f"  依赖缺失数: {recommendations['risk_assessment']['dependency_missing_count']}")
        print(f"  依赖缺失比例: {recommendations['risk_assessment']['dependency_missing_ratio']}")
        
        return recommendations
    
    def generate_reports(self):
        """步骤八：生成报告文件"""
        print("\n=== 步骤八：生成报告文件 ===")
        
        # 生成 JSON 报告
        json_report_path = self.project_root / "data" / "stage5_hard_knowledge_batch3_readiness_plan.json"
        with open(json_report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已生成: {json_report_path}")
        
        # 生成 Markdown 报告
        md_report_path = self.project_root / "docs" / "stage5_hard_knowledge_batch3_readiness_plan.md"
        self._generate_markdown_report(md_report_path)
        print(f"Markdown 报告已生成: {md_report_path}")
        
        return {
            "json_report": str(json_report_path),
            "markdown_report": str(md_report_path)
        }
    
    def _generate_markdown_report(self, output_path: Path):
        """生成 Markdown 格式报告"""
        lines = [
            "# Stage5-HardKnowledge Batch3 预备审计报告",
            "",
            f"**审计时间**: {self.audit_time}",
            f"**项目路径**: {self.project_root}",
            "",
            "## 1. 当前稳定状态检查",
            ""
        ]
        
        stable = self.results["stable_state_check"]
        lines.extend([
            f"- 主图谱 item_count: **{stable['main_graph_item_count']}**",
            f"- 前端图谱 item_count: **{stable['frontend_graph_item_count']}**",
            f"- 内容索引覆盖: **{stable['content_index_coverage']}**",
            f"- 主图谱 section_count: **{stable['main_graph_section_count']}**",
            f"- 前端图谱 section_count: **{stable['frontend_graph_section_count']}**",
            f"- ID 集合匹配: **{'[PASS]' if stable['id_sets_match'] else '[FAIL]'}**",
            f"- 章节集合匹配: **{'[PASS]' if stable['section_sets_match'] else '[FAIL]'}**",
            f"- 稳定性状态: **{stable['stability_status']}**",
            ""
        ])
        
        lines.extend([
            "## 2. 已使用候选识别",
            ""
        ])
        
        used = self.results["used_candidates"]
        lines.extend([
            f"- Batch1 已使用: **{used['batch1_count']}** 个候选",
            f"- Batch2 已使用: **{used['batch2_count']}** 个候选",
            f"- 总计已使用: **{used['total_used_count']}** 个候选",
            ""
        ])
        
        lines.extend([
            "## 3. 候选池统计",
            ""
        ])
        
        pool = self.results["candidate_pool"]
        lines.extend([
            f"- 来源文件数: **{len(pool['source_files'])}**",
            f"- 原始候选数: **{pool['total_raw_count']}**",
            f"- 去重后候选数: **{pool['unique_count']}**",
            ""
        ])
        
        lines.extend([
            "## 4. Batch3 候选过滤结果",
            ""
        ])
        
        filtered = self.results["filtered_candidates"]
        filter_sum = filtered["filter_summary"]
        lines.extend([
            f"- 原始候选数: **{filtered['original_candidate_count']}**",
            f"- 排除_已使用: **{filter_sum['排除_已使用']}**",
            f"- 排除_defer_drop: **{filter_sum['排除_defer_drop']}**",
            f"- 排除_重复合并风险: **{filter_sum['排除_重复合并风险']}**",
            f"- **剩余可用候选: **{filter_sum['剩余可用']}****",
            ""
        ])
        
        # 添加Batch2统计差异解释
        batch2_expl = filtered.get("batch2_discrepancy_explanation", {})
        if batch2_expl:
            lines.extend([
                "### Batch2 统计差异说明",
                "",
                f"- **Batch2 mapping 总数**: **{batch2_expl.get('batch2_mapping_total', 0)}**",
                f"- **当前候选池中匹配**: **{batch2_expl.get('batch2_found_in_current_pool', 0)}**",
                f"- **差异**: **{batch2_expl.get('batch2_mapping_total', 0) - batch2_expl.get('batch2_found_in_current_pool', 0)}** 个候选不在当前候选池中",
                f"- **原因**: {batch2_expl.get('explanation', '未知')}",
                ""
            ])
        
        lines.extend([
            "## 5. 候选风险审计",
            ""
        ])
        
        # 风险类型统计
        risk_summary_key = "_summary"
        summary = self.results["risk_audit"].get(risk_summary_key, {})
        
        for risk_type, info in self.results["risk_audit"].items():
            if risk_type != risk_summary_key:
                lines.append(f"- {risk_type}: **{info['count']}** 个")
        
        lines.append("")
        
        # 风险汇总统计
        if summary:
            lines.extend([
                "### 风险汇总统计",
                "",
                f"- 总候选数: **{summary.get('total_candidates', 0)}**",
                f"- 去重后风险候选数: **{summary.get('unique_risky_candidate_count', 0)}**",
                f"- 安全候选数: **{summary.get('safe_candidate_count', 0)}**",
                f"- 风险比例: **{summary.get('risk_ratio', 0):.1f}%**",
                f"- 依赖缺失数: **{summary.get('dependency_missing_count', 0)}**",
                f"- 依赖缺失比例: **{summary.get('dependency_missing_ratio', 0):.1f}%**",
                ""
            ])
        
        lines.extend([
            "## 6. 章节容量审计",
            ""
        ])
        
        capacity = self.results["section_capacity"]
        lines.extend([
            f"- 总章节数: **{capacity['total_sections']}**",
            f"- 高容量章节 (>100): **{len(capacity['high_capacity_sections'])}**",
            f"- 中等容量章节 (50-100): **{len(capacity['medium_capacity_sections'])}**",
            f"- 低容量章节 (<50): **{len(capacity['low_capacity_sections'])}**",
            ""
        ])
        
        lines.extend([
            "### 前 15 个高容量章节:",
            ""
        ])
        
        for i, section in enumerate(capacity["top_15_sections"], 1):
            sec_name = section.get("section_name", "unknown")
            lines.append(f"{i}. {section['section_id']} ({sec_name}): {section['item_count']} 个知识点")
        
        lines.append("")
        
        lines.extend([
            "## 7. Batch3 启动建议",
            ""
        ])
        
        rec = self.results["batch3_recommendations"]
        lines.extend([
            f"- 是否立即启动: **{rec['immediate_launch']}**",
            f"- 启动状态: **{rec['launch_status']}**",
            f"- 推荐规模: **{rec['recommended_batch_size']}**",
            f"- 推荐理由: {rec['recommendation_reason']}",
            ""
        ])
        
        # 添加阻塞性问题
        if rec.get("blocking_conditions"):
            lines.extend([
                "### 阻塞性问题:",
                ""
            ])
            for condition in rec["blocking_conditions"]:
                lines.append(f"- {condition}")
            lines.append("")
        
        lines.extend([
            "### 风险评估:",
            f"- 总候选数: {rec['risk_assessment']['total_candidates']}",
            f"- 去重后风险候选数: {rec['risk_assessment']['unique_risky_candidate_count']}",
            f"- 安全候选数: {rec['risk_assessment']['safe_candidate_count']}",
            f"- 风险比例: {rec['risk_assessment']['risk_ratio']}",
            f"- 依赖缺失数: {rec['risk_assessment']['dependency_missing_count']}",
            f"- 依赖缺失比例: {rec['risk_assessment']['dependency_missing_ratio']}",
            ""
        ])
        
        lines.extend([
            "### 优先策略:",
            f"- 高优先级章节: {', '.join(rec['priority_strategy']['high_priority_sections'][:3])}",
            f"- 避免章节: {', '.join(rec['priority_strategy']['avoid_sections'][:3])}",
            ""
        ])
        
        lines.extend([
            "### 下一步建议:",
            ""
        ])
        for step in rec["next_steps"]:
            lines.append(f"- {step}")
        lines.append("")
        
        lines.extend([
            "## 8. 重要声明",
            "",
            "**本次审计严格遵循只读原则，未修改以下任何文件:**",
            "- 主图谱 (merged_knowledge_graph_item_dependencies_refined.json)",
            "- 前端图谱 (assets/data/knowledge/io_v4_4.json)",
            "- 内容索引 (assets/data/knowledge_content/content_index.json)",
            "- 内容正文文件",
            "- 候选池文件",
            "- 一号线程和二号线程的报告文件",
            "",
            "**生成的文件:**",
            "- tools/audit_stage5_batch3_readiness.py (审计脚本)",
            "- docs/stage5_hard_knowledge_batch3_readiness_plan.md (本报告)",
            "- data/stage5_hard_knowledge_batch3_readiness_plan.json (数据报告)",
            ""
        ])
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def run_full_audit(self):
        """执行完整审计流程"""
        print("=" * 60)
        print("Stage5-HardKnowledge Batch3 预备审计开始")
        print("=" * 60)
        
        try:
            # 步骤一：验证稳定状态
            self.verify_stable_state()
            
            # 步骤二：识别已使用候选
            used_ids, used_titles, used_summary = self.identify_used_candidates()
            
            # 步骤三：读取候选池
            candidates = self.read_candidate_pool()
            
            # 步骤四：过滤候选
            filter_result = self.filter_batch3_candidates(candidates, used_ids, used_titles)
            
            # 步骤五：风险审计
            risk_summary = self.candidate_risk_audit(filter_result["remaining"])
            
            # 步骤六：章节容量审计
            capacity_audit = self.section_capacity_audit()
            
            # 步骤七：生成建议
            recommendations = self.generate_batch3_recommendations(
                filter_result["filter_result"],
                risk_summary,
                capacity_audit
            )
            
            # 步骤八：生成报告
            report_files = self.generate_reports()
            
            print("\n" + "=" * 60)
            print("审计完成！")
            print("=" * 60)
            
            return {
                "status": "success",
                "results": self.results,
                "report_files": report_files
            }
            
        except Exception as e:
            print(f"\n审计过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }

if __name__ == "__main__":
    project_root = r"c:\Users\renfenggo\Documents\trae_projects\suanfatong"
    auditor = Stage5Batch3ReadinessAuditor(project_root)
    result = auditor.run_full_audit()
    
    if result["status"] == "success":
        print("\n[PASS] 所有审计步骤已完成")
        print(f"生成的报告文件:")
        for file_type, file_path in result["report_files"].items():
            print(f"  - {file_type}: {file_path}")
    else:
        print(f"\n[FAIL] 审计失败: {result['error']}")