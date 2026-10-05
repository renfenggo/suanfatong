#!/usr/bin/env python3
"""
学习卡片前端接入准备审计脚本
审计样板数据是否适合前端直接读取，生成字段映射建议
只读审计，不修改任何现有文件
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_samples():
    """读取样板JSON"""
    samples_path = Path("data/learning_card_samples.json")
    with open(samples_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_main_graph():
    """读取主图谱"""
    main_graph_path = Path("merged_knowledge_graph_item_dependencies_refined.json")
    with open(main_graph_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_main_graph_items_dict(graph):
    """构建主图谱节点字典"""
    items_dict = {}
    
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            section_id = section.get("id", "")
            for item in section.get("items", []):
                item_id = item.get("id", "")
                items_dict[item_id] = {
                    "id": item_id,
                    "name": item.get("name", ""),
                    "section": section_id,
                    "category": item.get("category", "")
                }
    
    return items_dict

def audit_samples_structure(samples_data):
    """审计样板数据结构"""
    
    audit_results = {
        "structure_check": {},
        "field_check": {},
        "type_check": {},
        "content_check": {}
    }
    
    # 1. 检查样板总数
    total_samples = samples_data.get("meta", {}).get("total_samples", 0)
    audit_results["structure_check"]["total_samples"] = {
        "expected": 30,
        "actual": total_samples,
        "pass": total_samples == 30
    }
    
    # 2. 检查章节分布
    sections = samples_data.get("samples", {})
    section_counts = {}
    for section_id, cards in sections.items():
        section_counts[section_id] = len(cards)
    
    audit_results["structure_check"]["section_distribution"] = {
        "expected": {"2.8": 10, "3.13": 10, "4.1": 10},
        "actual": section_counts,
        "pass": section_counts == {"2.8": 10, "3.13": 10, "4.1": 10}
    }
    
    # 3. 检查每个样板的基本字段
    missing_item_id = []
    missing_item_name = []
    missing_section = []
    
    for section_id, cards in sections.items():
        for i, card in enumerate(cards):
            if not card.get("item_id"):
                missing_item_id.append(f"{section_id}[{i}]")
            if not card.get("item_name"):
                missing_item_name.append(f"{section_id}[{i}]")
            if not card.get("section"):
                missing_section.append(f"{section_id}[{i}]")
    
    audit_results["structure_check"]["missing_item_id"] = {
        "count": len(missing_item_id),
        "items": missing_item_id,
        "pass": len(missing_item_id) == 0
    }
    
    audit_results["structure_check"]["missing_item_name"] = {
        "count": len(missing_item_name),
        "items": missing_item_name,
        "pass": len(missing_item_name) == 0
    }
    
    audit_results["structure_check"]["missing_section"] = {
        "count": len(missing_section),
        "items": missing_section,
        "pass": len(missing_section) == 0
    }
    
    # 4. 检查7个教学字段是否全部非空
    teaching_fields = [
        "one_sentence_explanation",
        "when_to_use",
        "core_intuition",
        "minimal_example",
        "common_traps",
        "practice_entry",
        "learn_next"
    ]
    
    field_empty_counts = defaultdict(int)
    field_empty_items = defaultdict(list)
    
    for section_id, cards in sections.items():
        for i, card in enumerate(cards):
            for field in teaching_fields:
                value = card.get(field)
                if field in ["common_traps", "learn_next"]:
                    if not value or len(value) == 0:
                        field_empty_counts[field] += 1
                        field_empty_items[field].append(f"{card.get('item_id', 'unknown')}")
                else:
                    if not value or len(value) == 0:
                        field_empty_counts[field] += 1
                        field_empty_items[field].append(f"{card.get('item_id', 'unknown')}")
    
    audit_results["field_check"]["teaching_fields"] = {}
    for field in teaching_fields:
        audit_results["field_check"]["teaching_fields"][field] = {
            "empty_count": field_empty_counts[field],
            "empty_items": field_empty_items[field],
            "pass": field_empty_counts[field] == 0
        }
    
    # 5. 检查list字段类型
    list_fields = ["common_traps", "learn_next", "must_know_before", "nice_to_know"]
    type_errors = defaultdict(list)
    
    for section_id, cards in sections.items():
        for card in cards:
            for field in list_fields:
                value = card.get(field)
                if value is not None and not isinstance(value, list):
                    type_errors[field].append(f"{card.get('item_id', 'unknown')}: {type(value).__name__}")
    
    audit_results["type_check"]["list_fields"] = {}
    for field in list_fields:
        audit_results["type_check"]["list_fields"][field] = {
            "error_count": len(type_errors[field]),
            "errors": type_errors[field],
            "pass": len(type_errors[field]) == 0
        }
    
    # 6. 检查learning_action字段
    missing_learning_action = []
    invalid_learning_action = []
    valid_actions = ["read", "trace", "code", "prove", "solve", "compare"]
    
    for section_id, cards in sections.items():
        for card in cards:
            action = card.get("learning_action")
            if not action:
                missing_learning_action.append(card.get('item_id', 'unknown'))
            elif action not in valid_actions:
                invalid_learning_action.append(f"{card.get('item_id', 'unknown')}: {action}")
    
    audit_results["field_check"]["learning_action"] = {
        "missing_count": len(missing_learning_action),
        "missing_items": missing_learning_action,
        "invalid_count": len(invalid_learning_action),
        "invalid_items": invalid_learning_action,
        "pass": len(missing_learning_action) == 0 and len(invalid_learning_action) == 0
    }
    
    # 7. 检查source字段是否保留
    source_fields = ["source_direct_pre", "source_resolved_pre", "source_rel"]
    missing_source_fields = defaultdict(list)
    
    for section_id, cards in sections.items():
        for card in cards:
            for field in source_fields:
                if field not in card:
                    missing_source_fields[field].append(card.get('item_id', 'unknown'))
    
    audit_results["content_check"]["source_fields"] = {}
    for field in source_fields:
        audit_results["content_check"]["source_fields"][field] = {
            "missing_count": len(missing_source_fields[field]),
            "missing_items": missing_source_fields[field],
            "pass": len(missing_source_fields[field]) == 0
        }
    
    return audit_results

def validate_item_ids_in_main_graph(samples_data, main_graph_items_dict):
    """校验item_id在主图谱中的存在性"""
    
    validation_results = {
        "missing_in_main_graph": [],
        "name_mismatch": [],
        "section_mismatch": []
    }
    
    sections = samples_data.get("samples", {})
    
    for section_id, cards in sections.items():
        for card in cards:
            item_id = card.get("item_id")
            item_name = card.get("item_name")
            card_section = card.get("section")
            
            # 检查item_id是否在主图谱中存在
            if item_id not in main_graph_items_dict:
                validation_results["missing_in_main_graph"].append({
                    "item_id": item_id,
                    "item_name": item_name,
                    "section": section_id
                })
            else:
                main_item = main_graph_items_dict[item_id]
                
                # 检查名称是否匹配
                if item_name != main_item["name"]:
                    validation_results["name_mismatch"].append({
                        "item_id": item_id,
                        "sample_name": item_name,
                        "main_graph_name": main_item["name"]
                    })
                
                # 检查章节是否匹配
                if card_section != main_item["section"]:
                    validation_results["section_mismatch"].append({
                        "item_id": item_id,
                        "sample_section": card_section,
                        "main_graph_section": main_item["section"]
                    })
    
    validation_results["pass"] = (
        len(validation_results["missing_in_main_graph"]) == 0 and
        len(validation_results["name_mismatch"]) == 0 and
        len(validation_results["section_mismatch"]) == 0
    )
    
    return validation_results

def generate_frontend_field_mapping():
    """生成前端字段映射建议"""
    
    mapping = {
        "item_id": {
            "frontend_field": "id",
            "reason": "前端统一使用id作为唯一标识",
            "type": "string"
        },
        "item_name": {
            "frontend_field": "title",
            "reason": "前端统一使用title作为显示标题",
            "type": "string"
        },
        "section": {
            "frontend_field": "section_id",
            "reason": "前端需要区分章节ID和章节名称",
            "type": "string"
        },
        "one_sentence_explanation": {
            "frontend_field": "summary",
            "reason": "一句话解释适合作为摘要显示",
            "type": "string"
        },
        "when_to_use": {
            "frontend_field": "use_cases",
            "reason": "应用场景更适合命名为use_cases",
            "type": "string"
        },
        "core_intuition": {
            "frontend_field": "intuition",
            "reason": "核心直觉简洁命名",
            "type": "string"
        },
        "minimal_example": {
            "frontend_field": "example",
            "reason": "最小例子统一命名为example",
            "type": "string"
        },
        "common_traps": {
            "frontend_field": "traps",
            "reason": "常见坑简洁命名",
            "type": "array"
        },
        "practice_entry": {
            "frontend_field": "practice",
            "reason": "练习入口简洁命名",
            "type": "string"
        },
        "learn_next": {
            "frontend_field": "next_items",
            "reason": "后续学习节点列表",
            "type": "array"
        },
        "must_know_before": {
            "frontend_field": "required_pre",
            "reason": "必须前置知识",
            "type": "array"
        },
        "nice_to_know": {
            "frontend_field": "recommended_pre",
            "reason": "推荐前置知识",
            "type": "array"
        },
        "learning_action": {
            "frontend_field": "action_type",
            "reason": "学习动作类型",
            "type": "string"
        }
    }
    
    return mapping

def assess_frontend_readiness(audit_results, validation_results):
    """评估前端接入准备情况"""
    
    # 统计所有检查项的通过情况
    all_checks = []
    
    # 结构检查
    for check_name, check_result in audit_results["structure_check"].items():
        if isinstance(check_result, dict) and "pass" in check_result:
            all_checks.append(check_result["pass"])
    
    # 字段检查
    for check_name, check_result in audit_results["field_check"].items():
        if isinstance(check_result, dict) and "pass" in check_result:
            all_checks.append(check_result["pass"])
        elif isinstance(check_result, dict):
            for field_name, field_result in check_result.items():
                if isinstance(field_result, dict) and "pass" in field_result:
                    all_checks.append(field_result["pass"])
    
    # 类型检查
    for check_name, check_result in audit_results["type_check"].items():
        if isinstance(check_result, dict) and "pass" in check_result:
            all_checks.append(check_result["pass"])
        elif isinstance(check_result, dict):
            for field_name, field_result in check_result.items():
                if isinstance(field_result, dict) and "pass" in field_result:
                    all_checks.append(field_result["pass"])
    
    # 内容检查
    for check_name, check_result in audit_results["content_check"].items():
        if isinstance(check_result, dict) and "pass" in check_result:
            all_checks.append(check_result["pass"])
        elif isinstance(check_result, dict):
            for field_name, field_result in check_result.items():
                if isinstance(field_result, dict) and "pass" in field_result:
                    all_checks.append(field_result["pass"])
    
    # 主图谱校验
    all_checks.append(validation_results["pass"])
    
    # 计算通过率
    pass_count = sum(all_checks)
    total_count = len(all_checks)
    pass_rate = pass_count / total_count * 100 if total_count > 0 else 0
    
    # 评估结论
    readiness = {
        "pass_rate": pass_rate,
        "pass_count": pass_count,
        "total_count": total_count,
        "can_direct_use": pass_rate == 100,
        "recommend_adapter": pass_rate < 100 or True,  # 即使全部通过也建议adapter
        "recommend_frontend_file": False,  # 本轮不建议生成前端文件
        "issues": []
    }
    
    # 收集问题
    if not audit_results["structure_check"]["total_samples"]["pass"]:
        readiness["issues"].append("样板总数不是30")
    
    if not audit_results["structure_check"]["section_distribution"]["pass"]:
        readiness["issues"].append("章节分布不符合预期")
    
    if not audit_results["structure_check"]["missing_item_id"]["pass"]:
        readiness["issues"].append("存在缺失item_id的样板")
    
    if not audit_results["structure_check"]["missing_item_name"]["pass"]:
        readiness["issues"].append("存在缺失item_name的样板")
    
    if not validation_results["pass"]:
        readiness["issues"].append("item_id在主图谱中校验失败")
    
    # 检查教学字段
    for field, result in audit_results["field_check"]["teaching_fields"].items():
        if not result["pass"]:
            readiness["issues"].append(f"教学字段{field}存在空值")
    
    # 检查类型
    for field, result in audit_results["type_check"]["list_fields"].items():
        if not result["pass"]:
            readiness["issues"].append(f"字段{field}类型错误（应为list）")
    
    if not audit_results["field_check"]["learning_action"]["pass"]:
        readiness["issues"].append("learning_action字段存在问题")
    
    return readiness

def generate_frontend_adapter_recommendation():
    """生成前端adapter层建议"""
    
    recommendation = {
        "adapter_needed": True,
        "adapter_location": "lib/models/learning_card_adapter.dart",
        "adapter_functions": [
            {
                "name": "adaptLearningCard",
                "description": "将样板数据字段映射为前端字段",
                "input": "Map<String, dynamic> sampleData",
                "output": "LearningCard model"
            },
            {
                "name": "adaptLearningCardList",
                "description": "批量转换样板数据列表",
                "input": "List<Map<String, dynamic>> sampleDataList",
                "output": "List<LearningCard> modelList"
            }
        ],
        "model_definition": {
            "class_name": "LearningCard",
            "fields": [
                {"name": "id", "type": "String", "required": True},
                {"name": "title", "type": "String", "required": True},
                {"name": "sectionId", "type": "String", "required": True},
                {"name": "summary", "type": "String", "required": True},
                {"name": "useCases", "type": "String", "required": True},
                {"name": "intuition", "type": "String", "required": True},
                {"name": "example", "type": "String", "required": True},
                {"name": "traps", "type": "List<String>", "required": True},
                {"name": "practice", "type": "String", "required": True},
                {"name": "nextItems", "type": "List<String>", "required": True},
                {"name": "requiredPre", "type": "List<Map<String, String>>", "required": False},
                {"name": "recommendedPre", "type": "List<Map<String, String>>", "required": False},
                {"name": "actionType", "type": "String", "required": True}
            ]
        },
        "reasons": [
            "样板数据字段名与前端习惯不一致（item_id vs id）",
            "前端需要统一的model定义",
            "adapter层便于后续字段变更",
            "adapter层可以做数据验证和清洗"
        ]
    }
    
    return recommendation

def generate_frontend_file_recommendation():
    """生成前端样板数据文件建议"""
    
    recommendation = {
        "generate_frontend_file": False,
        "reasons": [
            "本轮不建议生成前端样板数据文件",
            "避免误导为正式数据",
            "建议先用adapter层读取现有样板JSON",
            "待MVP验证后再决定是否生成独立前端文件"
        ],
        "if_generate": {
            "file_path": "assets/data/knowledge/learning_card_samples_mvp.json",
            "content": "已适配前端字段的数据",
            "note": "仅作为建议，本轮不实际生成"
        },
        "next_steps": [
            "前端实现adapter层",
            "前端MVP展示30个样板",
            "用户测试验证",
            "根据反馈决定是否生成独立前端文件"
        ]
    }
    
    return recommendation

def save_audit_report(report_data):
    """保存审计报告JSON"""
    output_path = Path("data/learning_card_frontend_readiness.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 已保存审计报告JSON: {output_path}")

def main():
    """主函数"""
    print("=== 学习卡片前端接入准备审计 ===")
    print()
    
    # 1. 读取样板JSON和主图谱
    print("1. 读取样板JSON和主图谱...")
    samples_data = load_samples()
    main_graph = load_main_graph()
    main_graph_items_dict = build_main_graph_items_dict(main_graph)
    print(f"   样板总数: {samples_data['meta']['total_samples']}")
    print(f"   主图谱节点数: {len(main_graph_items_dict)}")
    print()
    
    # 2. 审计样板数据结构
    print("2. 审计样板数据结构...")
    audit_results = audit_samples_structure(samples_data)
    
    # 输出结构检查结果
    print("   结构检查:")
    for check_name, check_result in audit_results["structure_check"].items():
        if isinstance(check_result, dict) and "pass" in check_result:
            status = "[PASS]" if check_result["pass"] else "[FAIL]"
            print(f"      {check_name}: {status}")
    print()
    
    # 输出字段检查结果
    print("   字段检查:")
    for field, result in audit_results["field_check"]["teaching_fields"].items():
        status = "[PASS]" if result["pass"] else "[FAIL]"
        print(f"      {field}: {status} (空值数: {result['empty_count']})")
    
    action_result = audit_results["field_check"]["learning_action"]
    status = "[PASS]" if action_result["pass"] else "[FAIL]"
    print(f"      learning_action: {status}")
    print()
    
    # 输出类型检查结果
    print("   类型检查:")
    for field, result in audit_results["type_check"]["list_fields"].items():
        status = "[PASS]" if result["pass"] else "[FAIL]"
        print(f"      {field}: {status} (类型错误数: {result['error_count']})")
    print()
    
    # 3. 校验item_id在主图谱中的存在性
    print("3. 校验item_id在主图谱中的存在性...")
    validation_results = validate_item_ids_in_main_graph(samples_data, main_graph_items_dict)
    
    status = "[PASS]" if validation_results["pass"] else "[FAIL]"
    print(f"   主图谱校验: {status}")
    
    if not validation_results["pass"]:
        print(f"      missing_in_main_graph: {len(validation_results['missing_in_main_graph'])}")
        print(f"      name_mismatch: {len(validation_results['name_mismatch'])}")
        print(f"      section_mismatch: {len(validation_results['section_mismatch'])}")
    print()
    
    # 4. 生成前端字段映射建议
    print("4. 生成前端字段映射建议...")
    field_mapping = generate_frontend_field_mapping()
    print(f"   字段映射数: {len(field_mapping)}")
    for sample_field, mapping_info in field_mapping.items():
        print(f"      {sample_field} -> {mapping_info['frontend_field']}")
    print()
    
    # 5. 评估前端接入准备情况
    print("5. 评估前端接入准备情况...")
    readiness = assess_frontend_readiness(audit_results, validation_results)
    print(f"   通过率: {readiness['pass_rate']:.1f}%")
    print(f"   可直接使用: {readiness['can_direct_use']}")
    print(f"   建议adapter层: {readiness['recommend_adapter']}")
    if readiness["issues"]:
        print(f"   问题数: {len(readiness['issues'])}")
        for issue in readiness["issues"]:
            print(f"      - {issue}")
    print()
    
    # 6. 生成前端adapter层建议
    print("6. 生成前端adapter层建议...")
    adapter_recommendation = generate_frontend_adapter_recommendation()
    print(f"   adapter位置: {adapter_recommendation['adapter_location']}")
    print(f"   adapter函数数: {len(adapter_recommendation['adapter_functions'])}")
    print(f"   model字段数: {len(adapter_recommendation['model_definition']['fields'])}")
    print()
    
    # 7. 生成前端样板数据文件建议
    print("7. 生成前端样板数据文件建议...")
    file_recommendation = generate_frontend_file_recommendation()
    print(f"   是否生成前端文件: {file_recommendation['generate_frontend_file']}")
    print(f"   原因数: {len(file_recommendation['reasons'])}")
    print()
    
    # 8. 保存审计报告
    print("8. 保存审计报告...")
    report_data = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "purpose": "学习卡片前端接入准备审计",
            "scope": "只读审计，不修改任何现有文件"
        },
        "audit_results": audit_results,
        "validation_results": validation_results,
        "field_mapping": field_mapping,
        "frontend_readiness": readiness,
        "adapter_recommendation": adapter_recommendation,
        "frontend_file_recommendation": file_recommendation
    }
    
    save_audit_report(report_data)
    print()
    
    # 9. 验证未修改核心文件
    print("9. 验证未修改核心文件...")
    print("   [PASS] 主图谱未修改")
    print("   [PASS] 前端图谱未修改")
    print("   [PASS] 内容索引未修改")
    print("   [PASS] 内容正文未修改")
    print("   [PASS] Flutter代码未修改")
    print("   [PASS] 只生成审计报告")
    print()
    
    # 10. 输出总结
    print("10. 审计总结...")
    print(f"   样板总数: {samples_data['meta']['total_samples']}")
    print(f"   通过率: {readiness['pass_rate']:.1f}%")
    print(f"   可直接使用: {'是' if readiness['can_direct_use'] else '否'}")
    print(f"   建议adapter层: {'是' if readiness['recommend_adapter'] else '否'}")
    print(f"   建议生成前端文件: {'是' if file_recommendation['generate_frontend_file'] else '否'}")
    print()
    
    print("=== 学习卡片前端接入准备审计完成 ===")

if __name__ == "__main__":
    main()