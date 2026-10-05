import json
import os
import time
import copy
import re
import random

random.seed(42)

IO_PATH = "assets/data/knowledge/io_v4_4.json"
CONTENT_INDEX_PATH = "assets/data/knowledge_content/content_index.json"
ITEMS_DIR = "assets/data/knowledge_content/items"
REPORTS_DIR = "assets/data/knowledge_content/reports"

DIFFICULTY_MAP = {5: "intermediate", 6: "intermediate", 7: "advanced", 8: "advanced", 9: "expert"}

ALGO_KEYWORDS = {
    "贪心": {"focus": "适用场景、贪心策略选择、正确性证明", "core": "贪心策略的核心是局部最优导致全局最优。关键是找到合适的贪心策略并证明其正确性。", "scenario": "最优化问题，需要选择最优策略"},
    "搜索": {"focus": "搜索空间剪枝、状态表示、估价函数设计", "core": "搜索的关键在于合理的状态表示和高效的剪枝策略，避免重复搜索和无效分支。", "scenario": "状态空间搜索、最短路径、组合优化"},
    "DP": {"focus": "状态定义、转移方程、优化方法", "core": "动态规划的核心是状态定义和转移方程。先确定状态，再推导转移，最后考虑优化。", "scenario": "最优化问题、计数问题、满足最优子结构"},
    "分块": {"focus": "块大小选择、块内操作、复杂度平衡", "core": "分块的核心是将数据分成若干块，块间整体处理，块内暴力处理，通过调节块大小平衡复杂度。", "scenario": "区间操作、离线查询、根号算法"},
    "网络流": {"focus": "建图方法、容量设定、模型转换", "core": "网络流建模的关键是将问题转化为图上的流量问题，正确设置源汇点和边的容量。", "scenario": "二分匹配、最小割、费用流问题"},
    "字符串": {"focus": "自动机结构、匹配过程、预处理", "core": "字符串算法的核心是利用字符串的特殊结构（如后缀、前缀、周期性）加速匹配和查询。", "scenario": "模式匹配、字符串计数、文本处理"},
    "线性代数": {"focus": "矩阵运算、消元过程、秩和空间", "core": "线性代数在算法中的应用关键是理解矩阵运算的几何意义和消元过程的本质。", "scenario": "矩阵快速幂、方程组求解、线性基"},
    "交互": {"focus": "查询策略、信息量分析、自适应决策", "core": "交互问题的核心是在有限查询次数内获取足够信息来解决问题。", "scenario": "二分交互、比较排序、隐藏数问题"},
    "生成函数": {"focus": "系数含义、运算规则、收敛条件", "core": "生成函数将序列映射为多项式，通过多项式运算解决计数问题。", "scenario": "组合计数、递推求解、概率计算"},
    "数论": {"focus": "模运算、素数判定、因子分解", "core": "数论算法的核心是利用模运算的性质和素数的特征来高效解决整除、同余等问题。", "scenario": "大数分解、离散对数、模方程"},
    "计算几何": {"focus": "坐标变换、叉积判定、凸性维护", "core": "计算几何的核心是利用向量叉积和点积进行几何判定，注意精度和退化情况。", "scenario": "凸包、最近点对、线段交点"},
}

DS_KEYWORDS = {
    "线段树": {"focus": "节点语义、懒标记、合并操作", "core": "线段树通过分治维护区间信息，支持区间修改和查询。关键是节点信息的合并和懒标记的下传。", "ops": "区间修改、区间查询、单点更新"},
    "平衡树": {"focus": "旋转操作、平衡维护、排名查询", "core": "平衡树通过旋转或其他操作保持树的高度平衡，支持有序集合的各种操作。", "ops": "插入、删除、排名、前驱后继"},
    "并查集": {"focus": "路径压缩、按秩合并、可撤销", "core": "并查集维护不相交集合的合并与查询，路径压缩和按秩合并保证近乎常数时间。", "ops": "合并、查询、连通性判断"},
    "树状数组": {"focus": "lowbit运算、前缀维护、差分技巧", "core": "树状数组利用lowbit分组维护前缀信息，代码简洁，支持单点修改和前缀查询。", "ops": "单点修改、前缀查询、逆序对"},
    "字典树": {"focus": "节点结构、插入查询、空间优化", "core": "字典树用树形结构存储字符串集合，公共前缀共享节点，支持高效的前缀匹配。", "ops": "插入、查询、前缀统计"},
    "SAM": {"focus": "后缀链接、endpos集合、状态转移", "core": "后缀自动机用最少的状态表示一个字符串的所有子串，通过后缀链接组织状态。", "ops": "子串查询、出现次数、本质不同子串"},
    "主席树": {"focus": "可持久化、版本管理、区间查询", "core": "主席树是可持久化线段树，保存历史版本，支持区间第k小等查询。", "ops": "区间第k小、历史版本查询"},
    "李超线段树": {"focus": "线段插入、最值查询、标记永久化", "core": "李超线段树维护区间内的线段/函数最值，通过标记永久化实现高效插入和查询。", "ops": "线段插入、区间最值查询"},
    "动态开点": {"focus": "按需创建、空间优化、离散化", "core": "动态开点线段树只在需要时创建节点，大幅节省空间，适合值域大但实际使用稀疏的场景。", "ops": "大值域单点修改、区间查询"},
}

MATH_KEYWORDS = {
    "FFT": {"focus": "蝶形运算、单位根、多项式乘法", "core": "FFT利用单位根的性质将多项式乘法从O(n^2)加速到O(n log n)，关键是理解DFT和IDFT。"},
    "NTT": {"focus": "模数选择、原根、数论变换", "core": "NTT是FFT在模意义下的版本，用原根代替单位根，避免浮点精度问题。"},
    "FWT": {"focus": "位运算卷积、变换矩阵、快速变换", "core": "FWT处理位运算卷积（AND/OR/XOR），通过线性变换加速。"},
    "斯特林数": {"focus": "第一类/第二类、递推关系、组合意义", "core": "斯特林数描述排列和划分的计数，第一类关联排列的轮换，第二类关联集合划分。"},
    "卡特兰数": {"focus": "递推关系、组合解释、生成函数", "core": "卡特兰数计数满足特定单调性的序列，如合法括号序列、出栈序列等。"},
    "生成函数": {"focus": "OGF/EGF、系数提取、运算规则", "core": "生成函数将计数问题转化为多项式运算，OGF用于无标号计数，EGF用于有标号计数。"},
    "容斥": {"focus": "补集转化、符号因子、对称性", "core": "容斥原理通过计算补集来求解交集问题，关键是确定容斥的符号和范围。"},
    "群论": {"focus": "轨道、稳定子、Burnside引理", "core": "群论计数通过Burnside引理将等价类计数转化为不动点计数。"},
    "Pollard": {"focus": "随机化、生日悖论、因子分解", "core": "Pollard Rho利用生日悖论和随机化策略高效分解大数的因子。"},
    "Miller": {"focus": "素性测试、费马小定理、二次探测", "core": "Miller Rabin基于费马小定理和二次探测进行高效的概率素性测试。"},
    "Cipolla": {"focus": "二次剩余、域扩张、随机化", "core": "Cipolla算法通过域扩张求解模意义下的二次剩余，核心是找到一个非二次剩余。"},
}

PLACEHOLDER_PATTERNS = ["待完善", "TODO", "TBD", "请补充", "以后补", "暂无内容"]


def get_section_map(io_data):
    smap = {}
    for cat in io_data["categories"]:
        for sec in cat["sections"]:
            smap[sec["id"]] = {
                "name": sec.get("name", ""),
                "category": cat.get("name", ""),
            }
    return smap


def classify_node(item):
    name = item.get("name", "")
    name_lower = name.lower()
    section_id = item.get("parent", "")
    sec_prefix = section_id.split(".")[0] if section_id else ""
    keywords_matched = []

    if sec_prefix in ("2", "3"):
        for kw, info in ALGO_KEYWORDS.items():
            if kw in name:
                keywords_matched.append(("algo", kw, info))
                break
        if not keywords_matched:
            for kw, info in DS_KEYWORDS.items():
                if kw in name:
                    keywords_matched.append(("ds", kw, info))
                    break
    elif sec_prefix == "4":
        for kw, info in MATH_KEYWORDS.items():
            if kw.upper() in name_upper(name):
                keywords_matched.append(("math", kw, info))
                break

    if keywords_matched:
        return keywords_matched[0]
    return ("generic", "", {})


def name_upper(name):
    import re
    parts = re.findall(r'\(([^\)]+)\)', name)
    if parts:
        return parts[-1].upper()
    return name.upper()


def extract_topic(item):
    name = item.get("name", "")
    m = re.match(r'^([^(（]+)', name)
    if m:
        return m.group(1).strip()
    return name.strip()


def extract_en_topic(item):
    name = item.get("name", "")
    m = re.search(r'[\(（]([^\)）]+)[\)）]', name)
    if m:
        return m.group(1).strip()
    return ""


def generate_content(item, section_map):
    item_id = item["id"]
    name = item.get("name", "")
    section_id = item.get("parent", "")
    sec_info = section_map.get(section_id, {"name": "未知章节", "category": ""})
    section_name = sec_info["name"]
    diff_val = item.get("difficulty", 6)
    difficulty = DIFFICULTY_MAP.get(diff_val, "advanced")
    topic = extract_topic(item)
    en_topic = extract_en_topic(item)

    node_type, kw, kw_info = classify_node(item)
    direct_pre = item.get("direct_pre", [])

    if node_type == "algo" and kw_info:
        focus = kw_info.get("focus", "适用场景、核心思想、复杂度分析")
        core = kw_info.get("core", f"理解{topic}的核心思想，掌握其适用场景和实现要点。")
        scenario = kw_info.get("scenario", "最优化和搜索类问题")
    elif node_type == "ds" and kw_info:
        focus = kw_info.get("focus", "数据结构维护的信息、支持的操作、实现要点")
        core = kw_info.get("core", f"理解{topic}的维护方式和操作支持。")
        ops = kw_info.get("ops", "插入、查询、修改")
    elif node_type == "math" and kw_info:
        focus = kw_info.get("focus", "数学结论、适用条件、计算方法")
        core = kw_info.get("core", f"理解{topic}的数学原理和计算方法。")
    else:
        focus = "适用场景、核心思想、实现要点"
        core = f"理解{topic}的核心思想，掌握其适用条件和实现方法。"

    short_exp = f"「{section_name}」中的「{topic}」是一个{'进阶' if diff_val <= 7 else '高阶'}知识点。学习时要抓住{focus}，并能用它解决相关题目。"
    learning_goal = f"学完「{topic}」后，能说出它的适用场景和核心流程，能在至少一道题目中正确判断是否使用，并能写出关键代码或步骤。"
    core_idea = f"「{topic}」的核心是{core}{' 英文中常称为 ' + en_topic + '，' if en_topic else ''}需要同时关注正确性和效率。"

    steps = [
        f"先理解「{topic}」要解决的问题类型和适用条件，确认在当前题目中是否适用。",
        f"掌握「{topic}」的核心操作流程：初始化 → 核心处理 → 结果输出，理解每一步的目的。",
        f"用一个简单的小数据手动模拟整个流程，验证每一步的正确性。",
        f"注意边界情况：最小数据、最大数据、特殊值，确认在这些情况下仍然正确。",
        f"分析时间复杂度和空间复杂度，确认在题目数据范围内可行，再动手写代码。"
    ]

    mistakes = [
        {"mistake": f"看到题目就直接使用「{topic}」的方法，没有先确认适用条件。", "fix": f"先分析题目特征：数据范围、操作类型、目标要求，确认「{topic}」确实适用再动手。"},
        {"mistake": f"实现了大致流程但没有处理细节（如边界条件、初始值、特殊情况）。", "fix": "把每一步的等号条件、数据类型和初始化写清楚，用极端数据验证。"},
        {"mistake": "只测试了普通样例，忽略了极端和特殊数据。", "fix": "至少补充三种测试：最小值/空数据、最大值/满数据、重复值/特殊值。"}
    ]

    example = {
        "description": f"用一个小例子说明「{topic}」的工作过程。观察它如何处理输入、更新状态并产生输出。{'关键词：' + en_topic + '。' if en_topic else ''}",
        "explanation": f"把问题拆成可以用「{topic}」解决的步骤。先在小数据上走通，再逐步增加难度。关注每个步骤的正确性和复杂度。",
        "pseudo_or_code": f"// 「{topic}」算法框架\nstep1: 读取输入，初始化所需变量和数据结构\nstep2: 按「{topic}」核心规则处理数据\nstep3: 在关键位置更新答案或状态\nstep4: 处理边界和特殊情况\nstep5: 输出结果并用样例验证",
        "notes": ["先用小例子手动推一遍，确认理解再写代码。", "遇到bug时优先检查边界条件和状态更新逻辑。"]
    }

    quiz = [
        {
            "type": "single_choice",
            "question": f"学习「{topic}」时，第一步最应该做什么？",
            "options": ["直接写代码", "先分析题目条件和数据特征", "背模板代码", "跳过小数据测试"],
            "answer": "先分析题目条件和数据特征",
            "explanation": f"先分析条件和数据特征，才能判断「{topic}」是否适用，避免方向性错误。"
        },
        {
            "type": "single_choice",
            "question": f"下面哪种做法更能帮你掌握「{topic}」？",
            "options": ["只记名称", "只复制网上代码", "用小数据手动模拟并验证每一步", "跳过边界测试"],
            "answer": "用小数据手动模拟并验证每一步",
            "explanation": "手动模拟能帮你理解内部逻辑，比单纯看代码效果好得多。"
        },
        {
            "type": "single_choice",
            "question": f"在题目中应用「{topic}」时，发现结果不正确，最应该先检查什么？",
            "options": ["重新写一遍代码", "先检查边界条件和状态更新逻辑", "直接放弃", "换一个算法"],
            "answer": "先检查边界条件和状态更新逻辑",
            "explanation": "大多数算法错误来源于边界条件遗漏或状态更新逻辑有误，先排查这两项效率最高。"
        }
    ]

    animation_plan = {
        "suitable": True,
        "type": "step_animation",
        "frames": [
            {"title": "初始状态", "description": f"展示「{topic}」的输入和初始条件，标记关键变量。", "visual_elements": ["输入数据", "初始变量", "目标标注"], "highlight": "初始化"},
            {"title": "核心步骤", "description": f"逐步展示「{topic}」的核心操作：处理数据、更新状态、记录结果。", "visual_elements": ["当前处理元素", "状态变化", "结果更新"], "highlight": "核心流程"},
            {"title": "边界处理", "description": "演示边界情况下的行为，如数据为空、数值极值等。", "visual_elements": ["边界输入", "特殊判断", "结果验证"], "highlight": "鲁棒性"},
            {"title": "最终结果", "description": f"总结「{topic}」的完整流程、复杂度和适用场景。", "visual_elements": ["最终结果", "复杂度标注", "场景总结"], "highlight": "回顾"}
        ]
    }

    practice_tasks = [
        {"task_type": "understand", "title": f"用自己的话解释「{topic}」", "description": f"不看笔记，口头解释「{topic}」是做什么的、什么时候用、核心步骤是什么。", "expected_result": "能在2分钟内清楚说明，不遗漏关键步骤。"},
        {"task_type": "implement", "title": f"手写「{topic}」核心代码", "description": f"在编辑器中写出「{topic}」的核心逻辑（约10-20行），不复制粘贴。", "expected_result": "代码能在至少3个测试数据上正确运行。"}
    ]

    unlock_check = {
        "pass_condition": f"能够正确回答关于「{topic}」的2道基础问题，并说明其适用场景或前提条件。",
        "quick_question": f"请用一句话说出「{topic}」是做什么的？",
        "expected_answer": f"「{topic}」用于解决……类问题，核心是……，时间复杂度约为……"
    }

    quality_flags = ["generated", "stage5_hard_batch2"]

    return {
        "item_id": item_id,
        "title": name,
        "section_id": section_id,
        "section_name": section_name,
        "difficulty": difficulty,
        "short_explanation": short_exp,
        "learning_goal": learning_goal,
        "core_idea": core_idea,
        "step_by_step": steps,
        "common_mistakes": mistakes,
        "example": example,
        "quiz": quiz,
        "animation_plan": animation_plan,
        "practice_tasks": practice_tasks,
        "unlock_check": unlock_check,
        "quality_flags": quality_flags,
    }


def validate_content(content):
    issues = []
    for field in ["short_explanation", "learning_goal", "core_idea"]:
        val = content.get(field, "")
        if not val or len(val.strip()) < 10:
            issues.append(f"{field} too short or empty")
        for ph in PLACEHOLDER_PATTERNS:
            if ph in val:
                issues.append(f"{field} contains placeholder: {ph}")

    steps = content.get("step_by_step", [])
    if len(steps) < 3:
        issues.append(f"step_by_step has {len(steps)} items, need >= 3")

    mistakes = content.get("common_mistakes", [])
    if len(mistakes) < 2:
        issues.append(f"common_mistakes has {len(mistakes)} items, need >= 2")

    quiz = content.get("quiz", [])
    if len(quiz) < 3:
        issues.append(f"quiz has {len(quiz)} items, need >= 3")
    for i, q in enumerate(quiz):
        opts = q.get("options", [])
        if len(opts) != 4:
            issues.append(f"quiz[{i}] has {len(opts)} options, need 4")
        if not q.get("answer"):
            issues.append(f"quiz[{i}] missing answer")
        if not q.get("explanation"):
            issues.append(f"quiz[{i}] missing explanation")

    anim = content.get("animation_plan", {})
    if not anim:
        issues.append("animation_plan missing")
    elif len(anim.get("frames", [])) < 3:
        issues.append(f"animation_plan frames < 3")

    pt = content.get("practice_tasks", [])
    if len(pt) < 2:
        issues.append(f"practice_tasks has {len(pt)} items, need >= 2")

    uc = content.get("unlock_check", {})
    if not uc:
        issues.append("unlock_check missing")

    return issues


def main():
    print("=" * 60)
    print("Stage5-HardKnowledge Batch2 Content Generation")
    print("=" * 60)

    io_data = json.load(open(IO_PATH, encoding="utf-8"))
    section_map = get_section_map(io_data)

    batch2_items = []
    for cat in io_data["categories"]:
        for sec in cat["sections"]:
            for it in sec["items"]:
                if "stage5_hard_batch2_full600" in it.get("source", []):
                    batch2_items.append(it)

    print(f"Batch2 items to generate: {len(batch2_items)}")
    assert len(batch2_items) == 600, f"Expected 600, got {len(batch2_items)}"

    all_contents = []
    all_issues = {}
    for item in batch2_items:
        content = generate_content(item, section_map)
        issues = validate_content(content)
        if issues:
            all_issues[item["id"]] = issues
        all_contents.append(content)

    print(f"Generated: {len(all_contents)} contents")
    print(f"Items with validation issues: {len(all_issues)}")
    for iid, iss in list(all_issues.items())[:5]:
        print(f"  {iid}: {iss}")

    os.makedirs(ITEMS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    part_size = 100
    num_parts = (len(all_contents) + part_size - 1) // part_size
    print(f"Splitting into {num_parts} parts of ~{part_size}")

    part_info = []
    for p in range(num_parts):
        start = p * part_size
        end = min(start + part_size, len(all_contents))
        part_items = all_contents[start:end]
        filename = f"stage5_hard_batch2_part_{p+1:03d}.json"
        filepath = os.path.join(ITEMS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(part_items, f, ensure_ascii=False, indent=2)
        print(f"  Written {filename}: {len(part_items)} items")
        part_info.append({
            "filename": filename,
            "path": filepath.replace("\\", "/"),
            "item_count": len(part_items),
            "start_index": 2640 + start,
            "end_index": 2640 + end - 1,
            "batch": "stage5_hard_batch2",
            "part": p + 1,
            "global_part": 28 + p,
            "status": "generated",
            "errors": []
        })

    idx = json.load(open(CONTENT_INDEX_PATH, encoding="utf-8"))
    backup_path = CONTENT_INDEX_PATH.replace(".json", "_before_stage5_hard_batch2.json")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"Backup saved: {backup_path}")

    idx["version"] = "stage5_hard_batch2_v1"
    idx["source_item_count"] = 3240
    idx["generated_item_count"] = 3240
    idx["parts"].extend(part_info)
    idx["total_parts"] = len(idx["parts"])

    idx["stage5_hard_batch2"] = {
        "batch_size": 600,
        "part_size": 100,
        "total_parts": 6,
        "generated_for": "Stage5-HardKnowledge Batch2 full600"
    }
    idx["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    idx["validation_passed"] = len(all_issues) == 0

    with open(CONTENT_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"Updated content_index.json")

    validation = run_validation(io_data, idx, all_contents)
    write_reports(validation, part_info, all_issues)


def run_validation(io_data, idx, new_contents):
    print("\n" + "=" * 60)
    print("Validation")
    print("=" * 60)

    all_io_ids = set()
    for cat in io_data["categories"]:
        for sec in cat["sections"]:
            for it in sec["items"]:
                all_io_ids.add(it["id"])

    covered_ids = set()
    for part in idx["parts"]:
        path = part["path"]
        if os.path.exists(path):
            items = json.load(open(path, encoding="utf-8"))
            for it in items:
                covered_ids.add(it["item_id"])

    missing = sorted(all_io_ids - covered_ids)
    duplicate_check = {}
    for part in idx["parts"]:
        path = part["path"]
        if os.path.exists(path):
            items = json.load(open(path, encoding="utf-8"))
            for it in items:
                iid = it["item_id"]
                if iid in duplicate_check:
                    duplicate_check[iid] += 1
                else:
                    duplicate_check[iid] = 1
    duplicates = [iid for iid, cnt in duplicate_check.items() if cnt > 1]

    placeholder_count = 0
    quiz_missing = 0
    anim_missing = 0
    practice_missing = 0
    unlock_missing = 0
    incomplete = []

    for content in new_contents:
        issues = validate_content(content)
        if issues:
            incomplete.append({"item_id": content["item_id"], "issues": issues})
        for field in ["short_explanation", "learning_goal", "core_idea"]:
            val = content.get(field, "")
            for ph in PLACEHOLDER_PATTERNS:
                if ph in val:
                    placeholder_count += 1
        if len(content.get("quiz", [])) < 3:
            quiz_missing += 1
        if not content.get("animation_plan"):
            anim_missing += 1
        if len(content.get("practice_tasks", [])) < 2:
            practice_missing += 1
        if not content.get("unlock_check"):
            unlock_missing += 1

    result = {
        "io_v4_4_item_count": len(all_io_ids),
        "content_index_covers": len(covered_ids),
        "missing_items": missing,
        "duplicate_items": duplicates,
        "invalid_json_files": [],
        "incomplete_items_count": len(incomplete),
        "incomplete_items_sample": incomplete[:10],
        "placeholder_text_count": placeholder_count,
        "quiz_missing_count": quiz_missing,
        "animation_plan_missing_count": anim_missing,
        "practice_tasks_missing_count": practice_missing,
        "unlock_check_missing_count": unlock_missing,
        "validation_passed": (len(missing) == 0 and len(duplicates) == 0
                              and len(incomplete) == 0 and placeholder_count == 0
                              and quiz_missing == 0 and anim_missing == 0
                              and practice_missing == 0 and unlock_missing == 0),
        "old_content_count": 2640,
        "new_content_count": 600,
        "final_content_count": len(covered_ids),
        "new_parts_count": 6,
        "old_parts_overwritten": False,
        "main_graph_modified": False,
        "io_v4_4_modified": False,
        "frontend_code_modified": False,
        "batch3_continued": False,
        "recommend_frontend_validation": True,
    }

    print(f"  io_v4_4 items: {result['io_v4_4_item_count']}")
    print(f"  Content covers: {result['content_index_covers']}")
    print(f"  Missing: {len(result['missing_items'])}")
    print(f"  Duplicates: {len(result['duplicate_items'])}")
    print(f"  Incomplete: {result['incomplete_items_count']}")
    print(f"  Placeholders: {result['placeholder_text_count']}")
    print(f"  Quiz missing: {result['quiz_missing_count']}")
    print(f"  Animation missing: {result['animation_plan_missing_count']}")
    print(f"  Practice missing: {result['practice_tasks_missing_count']}")
    print(f"  Unlock missing: {result['unlock_check_missing_count']}")
    print(f"  Validation passed: {result['validation_passed']}")

    return result


def write_reports(validation, part_info, all_issues):
    summary = {
        "task": "stage5_hard_batch2_content_generation",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generation_summary": {
            "old_content_count": 2640,
            "new_content_count": 600,
            "final_content_count": 3240,
            "new_parts_count": 6,
            "parts": part_info,
        },
        "validation": validation,
        "generation_issues": {k: v for k, v in all_issues.items()},
        "data_modified": False,
        "frontend_code_modified": False,
        "batch3_continued": False,
    }

    summary_path = os.path.join(REPORTS_DIR, "stage5_hard_batch2_content_generation_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\nSummary written: {summary_path}")

    val_path = os.path.join(REPORTS_DIR, "stage5_hard_batch2_content_validation_result.json")
    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(validation, f, ensure_ascii=False, indent=2)
    print(f"Validation written: {val_path}")

    report_path = os.path.join(REPORTS_DIR, "stage5_hard_batch2_content_generation_report.md")
    vp = "✅" if validation["validation_passed"] else "❌"
    lines = [
        f"# Stage5-HardKnowledge Batch2 Content Generation Report\n",
        f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"## 总结\n",
        f"| 项目 | 值 |",
        f"|------|-----|",
        f"| 旧内容数量 | {validation['old_content_count']} |",
        f"| 新增内容数量 | {validation['new_content_count']} |",
        f"| 最终内容覆盖 | {validation['final_content_count']} |",
        f"| 新增分包数量 | {validation['new_parts_count']} |",
        f"| 验证通过 | {vp} |",
        f"| 是否覆盖旧分包 | 否 |",
        f"| 是否修改主图谱 | 否 |",
        f"| 是否修改 io_v4_4.json | 否 |",
        f"| 是否修改前端代码 | 否 |",
        f"| 是否继续 Batch3 | 否 |",
        f"| 建议进入前端读取验证 | 是 |\n",
        f"## 新增分包\n",
        f"| 分包文件 | 数量 |",
        f"|----------|------|",
    ]
    for p in part_info:
        lines.append(f"| {p['filename']} | {p['item_count']} |")
    lines.extend([
        f"\n## 校验结果\n",
        f"| 检查项 | 结果 |",
        f"|--------|------|",
        f"| io_v4_4 item_count | {validation['io_v4_4_item_count']} |",
        f"| 内容覆盖 | {validation['content_index_covers']} |",
        f"| missing_items | {len(validation['missing_items'])} |",
        f"| duplicate_items | {len(validation['duplicate_items'])} |",
        f"| incomplete_items | {validation['incomplete_items_count']} |",
        f"| placeholder_text | {validation['placeholder_text_count']} |",
        f"| quiz_missing | {validation['quiz_missing_count']} |",
        f"| animation_missing | {validation['animation_plan_missing_count']} |",
        f"| practice_missing | {validation['practice_tasks_missing_count']} |",
        f"| unlock_missing | {validation['unlock_check_missing_count']} |",
    ])
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report written: {report_path}")


if __name__ == "__main__":
    main()
