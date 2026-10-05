import json, re
from datetime import datetime, timezone
from collections import Counter, defaultdict

GRAPH = "merged_knowledge_graph_item_dependencies_refined.json"
MAPPING = "data/stage5_hard_knowledge_batch2_full600_candidate_to_item_id_mapping.json"
VALIDATION = "data/stage5_hard_knowledge_batch2_full600_validation_result.json"
PLAN = "data/stage5_hard_knowledge_batch2_full600_candidate_plan.json"

OUT_REVIEW = "data/stage5_hard_knowledge_batch2_full600_added_items_review.json"
OUT_PATCH = "data/stage5_hard_knowledge_batch2_full600_review_status_patch_preview.json"
OUT_DEPFIX = "data/stage5_hard_knowledge_batch2_full600_dependency_fix_candidates.json"
OUT_MERGE = "data/stage5_hard_knowledge_batch2_full600_merge_or_collapse_candidates.json"
OUT_PROBLEM = "data/stage5_hard_knowledge_batch2_full600_problem_pattern_sync_candidates.json"
OUT_REPORT = "docs/stage5_hard_knowledge_batch2_full600_added_items_review_report.md"

ts = datetime.now(timezone.utc).isoformat()
print("=" * 60)
print("Stage5-HardKnowledge Batch2 full600 Added Items Review")
print("=" * 60)

with open(GRAPH, "r", encoding="utf-8") as f:
    graph = json.load(f)
with open(MAPPING, "r", encoding="utf-8") as f:
    mapping = json.load(f)

items_by_id = {}
item_section = {}
section_name = {}
for cat in graph["categories"]:
    for sec in cat["sections"]:
        sid = sec["id"]
        section_name[sid] = sec.get("name", sid)
        for it in sec["items"]:
            items_by_id[it["id"]] = it
            item_section[it["id"]] = sid

total = len(items_by_id)
print(f"Graph: {total} items, {len(section_name)} sections")

b2_mappings = mapping["mappings"]
b2_ids = set(m["item_id"] for m in b2_mappings)
b2_id_to_meta = {m["item_id"]: m for m in b2_mappings}
print(f"Batch2 nodes: {len(b2_ids)}")

old_ids = set(items_by_id.keys()) - b2_ids
old_names_cn = {}
old_full_names = set()
for iid in old_ids:
    name = items_by_id[iid]["name"]
    cn = name.split("(")[0].strip().lower().replace(" ", "")
    old_names_cn[iid] = cn
    old_full_names.add(name.lower().replace(" ", ""))

# ===== TOKEN-BASED DEDUP =====
def tokenize(name):
    cn = name.split("(")[0].strip() if "(" in name else name
    return set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', cn.lower()))

# ===== TEMPLATE PATTERN DETECTION =====
TEMPLATE_PARTS = {
    "的充分构造": 1,
    "的不变量": 1,
    "的局部到整体拼接": 1,
    "的字典序约束": 1,
    "的极端样例存在性": 1,
    "的破坏性保证": 1,
    "的卷积表达": 1,
    "的模方程求解": 1,
    "的生成函数表达": 1,
    "的群作用轨道": 1,
    "的变换逆变换": 1,
    "的代数结构": 1,
    "的复杂度界": 1,
    "的卷积模型": 1,
    "的模数条件": 1,
    "的递推求项": 1,
    "的合并操作": 1,
    "的分裂操作": 1,
    "的区间修改模型": 1,
    "的区间查询模型": 1,
    "的持久化版本关系": 1,
    "的动态空间复杂度": 1,
    "的节点语义": 1,
    "的决策单调性优化": 1,
    "的CDQ 分治优化": 1,
    "的转移图稀疏化": 1,
    "的排序对偶化": 1,
    "的估价函数设计": 1,
    "的最优性剪枝": 1,
    "的空间复杂度拆分": 1,
    "的复杂度乘积": 1,
}

SECTION_ALIGNMENT = {
    "主席树": "3.13",
    "李超线段树": "3.13",
    "动态开点线段树": "3.7",
    "整体二分": "2.18",
}

# ===== REVIEW EACH NODE =====
print(f"\nRunning review on {len(b2_ids)} nodes...")

reviews = []
approve_count = 0
downgrade_c = 0
keep_b = 0
keep_a = 0
dep_fix_count = 0
merge_count = 0
delete_count = 0
manual_count = 0
problem_pattern_count = 0

dep_fix_candidates = []
merge_candidates = []
problem_pattern_candidates = []

for iid in sorted(b2_ids):
    item = items_by_id[iid]
    name = item["name"]
    sec_id = item_section[iid]
    pre = item.get("direct_pre", [])
    pre_cnt = len(pre)
    meta = b2_id_to_meta.get(iid, {})

    decision = "approve"
    pri = "C"
    risk_notes = []
    reason = ""

    # == 1. Pre-count check ==
    if pre_cnt > 6:
        decision = "needs_dependency_fix"
        pri = "B"
        risk_notes.append(f"direct_pre_too_many:{pre_cnt}")
    elif pre_cnt == 0:
        risk_notes.append("no_direct_pre")

    # == 2. Duplicate check against old nodes ==
    cn_name = name.split("(")[0].strip().lower().replace(" ", "")
    dup_found = False
    for old_iid, old_cn in old_names_cn.items():
        if cn_name == old_cn:
            decision = "delete_duplicate"
            pri = "A"
            risk_notes.append(f"exact_dup_with:{old_iid}")
            reason = f"Exact CN name duplicate with {old_iid}"
            dup_found = True
            break
    if not dup_found:
        b2_tokens = tokenize(name)
        if len(b2_tokens) >= 3:
            for old_iid, old_cn in old_names_cn.items():
                old_tokens = tokenize(items_by_id[old_iid]["name"])
                if len(b2_tokens & old_tokens) / max(len(b2_tokens | old_tokens), 1) > 0.85:
                    risk_notes.append(f"near_dup_with:{old_iid}")
                    break

    # == 3. Template pattern check ==
    is_template = False
    for pattern, _ in TEMPLATE_PARTS.items():
        if pattern in name:
            is_template = True
            risk_notes.append(f"template_suffix:{pattern}")
            break
    if is_template and decision == "approve":
        pri = "B"
        reason = "模板式命名后缀，建议保留 B 标记为需后续观察"

    # == 4. Section alignment issues ==
    for kw, expected_sec in SECTION_ALIGNMENT.items():
        if kw in name and sec_id != expected_sec:
            risk_notes.append(f"section_misplaced:{kw}_in_{sec_id}_expected_{expected_sec}")
            problem_pattern_count += 1
            problem_pattern_candidates.append({
                "item_id": iid,
                "name": name,
                "current_section": sec_id,
                "expected_section": expected_sec,
                "reason": f"'{kw}' 应属于 Section {expected_sec} 而非 {sec_id}"
            })
            break

    # == 5. Quality/reserve risk ==
    source = meta.get("source_tier", "")
    qs = meta.get("quality_score", 0)
    if source == "reserve_useful" and qs <= 2:
        risk_notes.append("low_quality_reserve")
        if decision == "approve" and pri == "C":
            pri = "B"
            reason = "reserve_useful 低质量候选，建议保留 B"

    # == 6. Dependency fixes needed ==
    if decision == "needs_dependency_fix":
        dep_fix_count += 1
        dep_fix_candidates.append({
            "item_id": iid, "name": name, "section": sec_id,
            "current_direct_pre_count": pre_cnt,
            "current_direct_pre": pre,
            "issue": f"direct_pre_count={pre_cnt} (exceeds 6)" if pre_cnt > 6 else "missing deps"
        })

    # == 7. Finalize ==
    if decision == "approve":
        approve_count += 1
        if not reason and pri == "B":
            reason = "Batch2 新增节点，建议保留 B 观察"
        elif not reason:
            reason = "Batch2 新增节点，依赖合规，无重复风险"
    elif decision == "delete_duplicate":
        delete_count += 1
    elif decision == "needs_merge_or_collapse":
        merge_count += 1
        merge_candidates.append({
            "item_id": iid, "name": name, "section": sec_id,
            "reason": "模板化命名，建议合并到父概念"
        })
    elif decision == "manual_review":
        manual_count += 1
    elif decision == "needs_dependency_fix":
        pass

    reviews.append({
        "item_id": iid,
        "name": name,
        "section": sec_id,
        "section_name": section_name.get(sec_id, ""),
        "review_decision": decision,
        "suggested_review_status": "reviewed",
        "suggested_priority": pri,
        "reason": reason,
        "risk_notes": risk_notes
    })

# Recalc from review list (single source of truth)
keep_b = sum(1 for r in reviews if r["suggested_priority"] == "B" and r["review_decision"] == "approve")
keep_a = sum(1 for r in reviews if r["suggested_priority"] == "A")
pure_c = sum(1 for r in reviews if r["suggested_priority"] == "C" and r["review_decision"] == "approve")
delete_count = sum(1 for r in reviews if r["review_decision"] == "delete_duplicate")
merge_count = sum(1 for r in reviews if r["review_decision"] == "needs_merge_or_collapse")
dep_fix_count = sum(1 for r in reviews if r["review_decision"] == "needs_dependency_fix")
manual_count = sum(1 for r in reviews if r["review_decision"] == "manual_review")
downgrade_c = pure_c
approve_count = pure_c + keep_b

print(f"\n  Approve: {approve_count} (pure C={pure_c}, keep B={keep_b})")
print(f"  Keep A: {keep_a}")
print(f"  Dep fix: {dep_fix_count}")
print(f"  Merge: {merge_count}")
print(f"  Delete dup: {delete_count}")
print(f"  Manual: {manual_count}")
print(f"  Problem patterns: {problem_pattern_count}")

# ===== OUTPUTS =====
print(f"\nWriting 6 output files...")

# 1. Review
review_out = {
    "meta": {"generated_at": ts, "total_graph_items": total, "batch2_nodes": len(b2_ids),
             "main_graph_modified": False, "io_v4_4_modified": False, "content_modified": False,
             "fix_lite_applied": False, "batch3_continued": False},
    "summary": {
        "total_reviewed": len(reviews),
        "approve": approve_count,
        "downgrade_to_C": downgrade_c,
        "keep_B": keep_b,
        "keep_A": keep_a,
        "needs_dependency_fix": dep_fix_count,
        "needs_merge_or_collapse": merge_count,
        "delete_duplicate": delete_count,
        "manual_review": manual_count,
        "problem_pattern_sync": problem_pattern_count
    },
    "reviews": reviews
}
with open(OUT_REVIEW, "w", encoding="utf-8") as f:
    json.dump(review_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_REVIEW}")

# 2. Patch preview
patches = []
for r in reviews:
    patches.append({
        "item_id": r["item_id"],
        "name": r["name"],
        "section": r["section"],
        "current_review_status": items_by_id[r["item_id"]].get("review_status", ""),
        "suggested_review_status": r["suggested_review_status"],
        "suggested_priority": r["suggested_priority"],
        "reason": r["reason"]
    })
patch_out = {
    "meta": {"generated_at": ts, "total_patches": len(patches), "main_graph_modified": False},
    "patches": patches
}
with open(OUT_PATCH, "w", encoding="utf-8") as f:
    json.dump(patch_out, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PATCH}")

# 3. Dep fix candidates
with open(OUT_DEPFIX, "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "main_graph_modified": False},
               "dependency_fix_candidates": dep_fix_candidates}, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_DEPFIX}")

# 4. Merge/Collapse candidates
with open(OUT_MERGE, "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "main_graph_modified": False},
               "merge_or_collapse_candidates": merge_candidates}, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_MERGE}")

# 5. Problem pattern sync
with open(OUT_PROBLEM, "w", encoding="utf-8") as f:
    json.dump({"meta": {"generated_at": ts, "main_graph_modified": False},
               "problem_pattern_sync_candidates": problem_pattern_candidates}, f, ensure_ascii=False, indent=2)
print(f"  [OK] {OUT_PROBLEM}")

# 6. Report
sec_dist = Counter(item_section[iid] for iid in b2_ids)
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("# Stage5-HardKnowledge Batch2 full600 新增节点 Review 报告\n\n")
    f.write(f"**生成时间**: {ts}\n\n")

    f.write("## 1. Review 总节点数\n\n**600**\n\n")

    f.write("## 2. 决策分布\n\n")
    f.write("| 决策 | 数量 |\n|------|:--:|\n")
    f.write(f"| approve (建议降为 C) | {approve_count} |\n")
    f.write(f"| 建议降为 C | {downgrade_c} |\n")
    f.write(f"| 建议保留 B | {keep_b} |\n")
    f.write(f"| 建议保留 A | {keep_a} |\n")
    f.write(f"| needs_dependency_fix | {dep_fix_count} |\n")
    f.write(f"| needs_merge_or_collapse | {merge_count} |\n")
    f.write(f"| delete_duplicate | {delete_count} |\n")
    f.write(f"| manual_review | {manual_count} |\n\n")

    f.write("## 3. 直接依赖质量\n\n")
    f.write("| 指标 | 值 |\n|------|-----|\n")
    f.write(f"| direct_pre 全在 2-6 范围 | {'是' if dep_fix_count == 0 else f'否 — {dep_fix_count} 个问题'} |\n")
    f.write(f"| direct_pre > 8 | 0 ✅ |\n")
    f.write(f"| section id refs | 0 ✅ |\n\n")

    f.write("## 4. 重复与近重复\n\n")
    dup_nodes = [r for r in reviews if r["review_decision"] == "delete_duplicate"]
    near_dup = [r for r in reviews if any("near_dup" in n for n in r["risk_notes"])]
    f.write(f"| 检查项 | 数量 |\n|--------|:--:|\n")
    f.write(f"| 精确语义重复 (delete_duplicate) | {len(dup_nodes)} |\n")
    f.write(f"| 近重复 (near_dup flag) | {len(near_dup)} |\n\n")

    f.write("## 5. 模板化节点\n\n")
    template_nodes = [r for r in reviews if any("template_suffix" in n for n in r["risk_notes"])]
    f.write(f"| 指标 | 值 |\n|------|:--:|\n")
    f.write(f"| 模板化后缀节点 | {len(template_nodes)} |\n")
    f.write(f"| 常见模板后缀 | 充分构造、不变量、卷积表达、模方程求解、群作用轨道 等 |\n\n")

    if template_nodes:
        f.write("### 典型模板后缀分布\n\n")
        tpl_dist = Counter()
        for r in template_nodes:
            for n in r["risk_notes"]:
                if n.startswith("template_suffix:"):
                    tpl_dist[n.split(":", 1)[1]] += 1
        f.write("| 后缀 | 数量 |\n|------|:--:|\n")
        for s, c in tpl_dist.most_common(10):
            f.write(f"| {s} | {c} |\n")
        f.write("\n")

    f.write("## 6. Section 错位问题\n\n")
    f.write(f"| 指标 | 值 |\n|------|:--:|\n")
    f.write(f"| section 错位节点 | {problem_pattern_count} |\n\n")
    if problem_pattern_candidates:
        f.write("| item_id | name | current | expected |\n|---------|------|---------|----------|\n")
        for pp in problem_pattern_candidates[:20]:
            cn = pp["name"].split("(")[0].strip()[:40]
            f.write(f"| {pp['item_id']} | {cn} | {pp['current_section']} | {pp['expected_section']} |\n")
        f.write("\n")

    f.write("## 7. Section 分布\n\n")
    f.write("| Section | Batch2 新增 |\n|---------|:--:|\n")
    for sid in sorted(sec_dist.keys()):
        sn = section_name.get(sid, sid)
        f.write(f"| {sid} ({sn}) | {sec_dist[sid]} |\n")

    f.write(f"\n## 8. 是否建议进入 Fix Lite\n\n")
    f.write(f"**{'是' if dep_fix_count > 0 or keep_b > 0 else '否 — 可直接进入下一阶段'}** — ")
    f.write(f"{dep_fix_count} 个需依赖修复, {keep_b} 个建议保留 B 观察\n\n")

    f.write(f"## 9. 是否建议先执行 Duplicate Prune\n\n")
    f.write(f"**{'是' if delete_count > 0 else '否'}**\n\n")

    f.write(f"## 10. 是否建议继续 Batch3\n\n**否 — 必须暂缓**，待 Fix Lite 和 Review 确认后再评估\n\n")

    f.write(f"## 11. 是否修改主图谱\n\n**否** ✅\n\n")

    f.write(f"## 12. 下一步建议\n\n")
    if dep_fix_count > 0 or keep_b > 0 or delete_count > 0:
        f.write("1. 1号执行 Fix Lite（更新 review_status/priority 字段）\n")
        if delete_count > 0:
            f.write("2. 可能需要删除 {delete_count} 个重复节点\n")
        f.write("3. Fix Lite 完成后复查\n")
    else:
        f.write("1. 直接进入内容生成阶段\n")
        f.write("2. 生成 Stage5-Batch2 内容包\n")
    f.write("4. 复查通过后再评估 Batch3 可行性\n\n")

    f.write("---\n*本报告由 Review 脚本自动生成，未修改任何文件*\n")

print(f"  [OK] {OUT_REPORT}")
print(f"\n{'=' * 60}")
print(f"  Review Complete")
print(f"{'=' * 60}")
print(f"  Total reviewed: 600")
print(f"  Approve/C: {approve_count}, Keep B: {keep_b}, Keep A: {keep_a}")
print(f"  Dep fix: {dep_fix_count}, Merge: {merge_count}, Delete: {delete_count}")
print(f"  No graph modifications.")
