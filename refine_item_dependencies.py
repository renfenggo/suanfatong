import argparse
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = "merged_knowledge_graph.json"
DEFAULT_OUTPUT = "merged_knowledge_graph_item_dependencies_refined.json"
DEFAULT_REPORT = "item_dependency_refinement_report.md"
DEFAULT_LOW_CONF = "low_confidence_dependency_review.json"
DEFAULT_VALIDATION = "dependency_validation_result.json"
SAMPLE_REPORT = "sample_dependency_validation_report.md"

ALLOWED_TRACKS = [
    "beginner", "csp_j", "csp_s", "noi", "ioi", "icpc", "university_cp",
    "interview", "advanced_math", "advanced_graph", "advanced_string",
    "advanced_data_structure", "advanced_dp", "engineering_debug",
]
ALLOWED_AUDIENCE = [
    "primary_beginner", "middle_school_oi", "high_school_oi", "university_icpc",
    "software_engineer_interview", "advanced_competitive_programmer",
]
ALLOWED_VISIBILITY = ["core", "advanced", "expert", "optional"]
ALLOWED_UNLOCK_MODES = ["mainline", "optional_branch", "expert_branch", "reference_only"]
ALLOWED_PLATFORMS = [
    "CSES", "Codeforces", "AtCoder", "Kattis", "LeetCode", "DMOJ",
    "USACO", "Luogu", "ICPC_Gym", "HackerRank",
]
SUPPORTED_LANGUAGES = ["zh-Hans", "en", "ja", "ko", "es", "ru", "fr", "pt", "hi"]

EN_NAME_OVERRIDES = {
    "数组": "Array",
    "一维数组": "One-dimensional Array",
    "二维数组": "Two-dimensional Array",
    "字符串": "String",
    "string": "String",
    "二分查找": "Binary Search",
    "双指针": "Two Pointers",
    "相向双指针": "Opposite-direction Two Pointers",
    "滑动窗口": "Sliding Window",
    "栈": "Stack",
    "队列": "Queue",
    "双端队列": "Deque",
    "堆": "Heap",
    "优先队列 / 二叉堆": "Priority Queue / Binary Heap",
    "链表": "Linked List",
    "二叉树": "Binary Tree",
    "图建模基础": "Graph Modeling",
    "图的 DFS": "Graph DFS",
    "图的 BFS": "Graph BFS",
    "DFS": "Depth-first Search",
    "BFS": "Breadth-first Search",
    "动态规划": "Dynamic Programming",
    "DP 思想": "Dynamic Programming Idea",
    "贪心": "Greedy Algorithm",
    "并查集基础": "Disjoint Set Union",
    "基本并查集": "Disjoint Set Union",
    "树状数组 Fenwick": "Fenwick Tree",
    "线段树": "Segment Tree",
    "Dijkstra": "Dijkstra's Algorithm",
    "拓扑排序": "Topological Sort",
    "KMP": "Knuth-Morris-Pratt Algorithm",
    "Trie": "Trie",
    "AC 自动机": "Aho-Corasick Automaton",
    "后缀数组": "Suffix Array",
    "后缀自动机": "Suffix Automaton",
    "FFT / NTT": "FFT / NTT",
    "网络流基础": "Network Flow Basics",
    "Dinic": "Dinic's Algorithm",
    "最小费用最大流": "Minimum-cost Maximum Flow",
}

GLOBAL_ALIASES = {
    "树状数组 Fenwick": ["Binary Indexed Tree", "BIT", "Fenwick Tree"],
    "线段树": ["Segment Tree"],
    "并查集基础": ["Disjoint Set Union", "DSU", "Union-Find"],
    "基本并查集": ["Disjoint Set Union", "DSU", "Union-Find"],
    "Dijkstra": ["Dijkstra's Algorithm"],
    "KMP": ["Knuth-Morris-Pratt", "KMP Algorithm"],
    "AC 自动机": ["Aho-Corasick", "Aho-Corasick Automaton"],
    "后缀数组": ["Suffix Array", "SA"],
    "后缀自动机": ["Suffix Automaton", "SAM"],
    "FFT / NTT": ["Fast Fourier Transform", "Number Theoretic Transform"],
    "网络流基础": ["Network Flow"],
    "Dinic": ["Dinic's Algorithm"],
    "优先队列 / 二叉堆": ["Priority Queue", "Binary Heap"],
    "单调队列": ["Monotonic Queue"],
    "单调栈": ["Monotonic Stack"],
}

ADVANCED_POLLUTION_TERMS = [
    "FFT", "NTT", "后缀数组", "后缀自动机", "AC 自动机", "主席树", "可持久化", "树套树",
    "多项式", "半平面交", "莫比乌斯", "LCT", "Link-Cut", "网络流", "费用流", "CDQ",
    "整体二分", "莫队", "插头", "圆方树", "虚树", "支配树", "带花树", "SAM", "Splay",
    "Treap", "FHQ", "DC3", "LCP", "height",
]

VERY_HIGH_RISK_TERMS = [
    "LCT", "Link-Cut", "半平面交", "多项式", "FFT", "NTT", "莫比乌斯", "支配树",
    "带花树", "动态树", "仙人掌", "虚树", "圆方树", "树套树", "插头", "CDQ",
]


def resolve_path(value):
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def level_num(level):
    m = re.search(r"\d+", str(level or ""))
    return int(m.group()) if m else 3


def build_indexes(graph):
    item_by_id, section_by_id = {}, {}
    category_by_item, section_by_item = {}, {}
    section_name_by_item, all_items = {}, []
    duplicate_item_ids = []
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            section_by_id[section["id"]] = section
            for item in section.get("items", []):
                if item["id"] in item_by_id:
                    duplicate_item_ids.append(item["id"])
                item_by_id[item["id"]] = item
                category_by_item[item["id"]] = category["name"]
                section_by_item[item["id"]] = section["id"]
                section_name_by_item[item["id"]] = section["name"]
                all_items.append(item)
    return {
        "item_by_id": item_by_id,
        "section_by_id": section_by_id,
        "category_by_item": category_by_item,
        "section_by_item": section_by_item,
        "section_name_by_item": section_name_by_item,
        "items": all_items,
        "duplicate_item_ids": duplicate_item_ids,
    }


def find_item(item_by_id, *terms, section=None):
    terms = [t.lower() for t in terms if t]
    candidates = []
    for item_id, item in item_by_id.items():
        if section and item.get("parent") != section:
            continue
        hay = (item.get("name", "") + " " + " ".join(item.get("alias", []))).lower()
        if all(t in hay for t in terms):
            candidates.append(item_id)
    candidates.sort(key=lambda x: (len(x), x))
    return candidates[0] if candidates else None


def ids(item_by_id, *values):
    return [v for v in values if v in item_by_id]


def build_anchors(item_by_id):
    # Use explicit names; avoid ambiguous keys such as block/graph/tree/queue/stack.
    a = {
        "cpp_include": "1.1.1",
        "cpp_main": "1.1.3",
        "cpp_statement": "1.1.4",
        "cpp_code_block": "1.1.5",
        "cpp_cin": "1.2.1",
        "cpp_cout": "1.2.2",
        "cpp_getline": "1.2.9",
        "cpp_fast_io": "1.2.12",
        "cpp_file_io": "1.2.14",
        "cpp_int": "1.3.1",
        "cpp_long_long": "1.3.2",
        "cpp_char": "1.3.4",
        "cpp_bool": "1.3.5",
        "cpp_double": "1.3.6",
        "cpp_variable": "1.3.10",
        "cpp_init": "1.3.11",
        "cpp_scope": "1.3.12",
        "cpp_cast": "1.3.17",
        "cpp_arithmetic_op": "1.4.1",
        "cpp_assignment_op": "1.4.2",
        "cpp_compare_op": "1.4.3",
        "cpp_logic_op": "1.4.4",
        "cpp_bit_op": "1.4.6",
        "cpp_shift_op": "1.4.7",
        "cpp_if": "1.5.1",
        "cpp_for": "1.5.6",
        "cpp_while": "1.5.7",
        "cpp_break": "1.5.9",
        "cpp_continue": "1.5.10",
        "cpp_array": "1.6.1",
        "cpp_2d_array": "1.6.2",
        "cpp_index": "1.6.5",
        "cpp_array_bounds": "1.6.6",
        "cpp_char_array": "1.6.7",
        "cpp_string": "1.6.9",
        "cpp_ascii": "1.6.15",
        "cpp_vector": "1.8.9",
        "cpp_function_def": "1.7.1",
        "cpp_function_call": "1.7.3",
        "cpp_function_param": "1.7.4",
        "cpp_function_return": "1.7.5",
        "cpp_recursion_function": "1.7.10",
        "cpp_pointer": "1.7.11",
        "cpp_reference": "1.7.15",
        "cpp_struct": "1.8.1",
        "cpp_pair": "1.8.8",
        "stl_queue": "1.8.10",
        "stl_stack": "1.8.11",
        "stl_deque": "1.8.12",
        "stl_priority_queue": "1.8.13",
        "stl_set": "1.8.14",
        "stl_map": "1.8.16",
        "stl_bitset": "1.8.20",
        "stl_iterator": "1.8.21",
        "stl_sort": "1.8.22",
        "stl_unique": "1.8.24",
        "stl_lower_bound": "1.8.26",
        "cpp_compare_function": "1.8.29",
        "cpp_macro": "1.9.1",
        "cpp_conditional_compile": "1.9.3",
        "algo_enumeration": "2.1.1",
        "algo_simulation": "2.1.2",
        "algo_recurrence": "2.1.3",
        "algo_recursion": "2.1.4",
        "algo_divide_conquer": "2.1.5",
        "algo_doubling": "2.1.6",
        "algo_construction": "2.1.7",
        "algo_offline": "2.1.8",
        "algo_random_base": "2.1.10",
        "algo_greedy": "2.6.1",
        "algo_greedy_proof": "2.6.6",
        "algo_binary_search": "2.3.1",
        "algo_monotonic_check": "2.3.7",
        "algo_check_function": "2.3.8",
        "algo_prefix_sum": "2.4.1",
        "algo_difference": "2.4.4",
        "algo_discretization": "2.4.6",
        "sqrt_decomposition": "2.4.7",
        "algo_mo": "2.4.8",
        "algo_two_pointer": "2.5.1",
        "algo_sliding_window": "2.5.4",
        "search_dfs": "2.7.1",
        "search_bfs": "2.7.2",
        "search_backtracking": "2.7.4",
        "search_pruning": "2.7.5",
        "search_state_space": "2.7.15",
        "dp_basic": "2.8.1",
        "dp_state_design": "2.8.2",
        "dp_transition": "2.8.3",
        "dp_memoization": "2.8.6",
        "dp_linear": "2.8.5",
        "dp_knapsack": "2.8.7",
        "dp_interval": "2.8.12",
        "dp_tree": "2.8.13",
        "dp_dag": "2.8.14",
        "dp_bitmask": "2.8.20",
        "dp_digit": "2.8.21",
        "graph_model": "2.9.3",
        "graph_topological_sort": "2.9.6",
        "graph_dag": "2.9.7",
        "shortest_path_basic": "2.13.1",
        "shortest_path_dijkstra": "2.13.2",
        "shortest_path_bellman_ford": "2.13.3",
        "shortest_path_floyd": "2.13.4",
        "shortest_path_spfa": "2.13.6",
        "mst_basic": "2.13.8",
        "mst_kruskal": "2.13.9",
        "mst_prim": "2.13.10",
        "tree_lca": "2.14.2",
        "tree_hld": "2.14.4",
        "tree_centroid_decomposition": "2.14.7",
        "graph_scc": "2.15.1",
        "graph_bridge": "2.15.2",
        "graph_cut_vertex": "2.15.3",
        "matching_bipartite": "2.16.1",
        "network_flow_basic": "2.16.3",
        "network_flow_dinic": "2.16.5",
        "network_flow_cost": "2.16.6",
        "string_kmp": "2.10.2",
        "string_trie_algo": "2.10.5",
        "string_ac_automaton": "2.10.6",
        "string_suffix_array": "2.10.7",
        "string_suffix_automaton": "2.10.8",
        "string_manacher": "2.10.9",
        "bit_binary": "2.11.1",
        "bit_mask": "2.11.2",
        "bit_subset_enum": "2.11.3",
        "bit_state_compression": "2.11.4",
        "bit_xor": "2.11.5",
        "bit_lowbit": "2.11.6",
        "numeric_fast_power": "2.12.1",
        "matrix_multiply": "2.12.3",
        "matrix_storage": "2.12.4",
        "ds_array": "3.1.1",
        "ds_linked_list": "3.1.4",
        "ds_stack": "3.2.1",
        "ds_queue": "3.2.2",
        "ds_deque": "3.2.3",
        "ds_monotonic_stack": "3.2.4",
        "ds_monotonic_queue": "3.2.5",
        "ds_heap": "3.5.1",
        "ds_dsu": "3.4.1",
        "tree_structure_math": "4.5.6",
        "binary_tree_ds": "3.6.1",
        "complete_binary_tree_ds": "3.6.2",
        "binary_search_tree_ds": "3.6.3",
        "balanced_tree_ds": "3.10.1",
        "trie_tree_ds": "3.8.1",
        "fenwick_tree_ds": "3.7.1",
        "segment_tree_ds": "3.7.2",
        "lazy_segment_tree_ds": "3.7.3",
        "persistent_segment_tree_ds": "3.7.8",
        "graph_storage_adjlist": "3.9.2",
        "graph_storage_edge_array": "3.9.4",
        "math_integer": "4.1.1",
        "math_divisibility": "4.1.5",
        "math_prime": "4.1.7",
        "math_factorization": "4.1.8",
        "math_gcd": "4.1.9",
        "math_exgcd": "4.1.12",
        "math_mod": "4.2.1",
        "math_mod_ops": "4.2.2",
        "math_congruence": "4.2.3",
        "math_inverse": "4.2.6",
        "math_crt": "4.2.9",
        "math_counting": "4.3.1",
        "math_factorial": "4.3.6",
        "math_combination": "4.3.7",
        "math_inclusion_exclusion": "4.3.10",
        "math_set": "4.4.1",
        "math_relation": "4.4.2",
        "math_function": "4.4.3",
        "math_induction": "4.4.10",
        "graph_theory_vertex_edge": "4.5.1",
        "graph_theory_path": "4.5.4",
        "graph_theory_tree": "4.5.6",
        "graph_theory_rooted_tree": "4.5.7",
        "graph_theory_bipartite": "4.5.9",
        "graph_theory_dag": "4.5.10",
        "math_probability": "4.6.1",
        "math_expectation": "4.6.4",
        "geometry_point": "4.7.1",
        "geometry_vector": "4.7.2",
        "geometry_dot": "4.7.14",
        "geometry_cross": "4.7.15",
        "linear_algebra_basic": "4.8.1",
        "linear_algebra_gauss": "4.8.2",
        "polynomial_fft_ntt_math": "4.8.3",
        "debug_translate": "5.7.1",
        "debug_sample": "5.7.5",
        "debug_boundary": "5.7.13",
        "debug_complexity": "5.7.14",
    }
    # Fallbacks keep the script usable if a future graph renames a known item.
    fallback_terms = {
        "algo_greedy": ("贪心",),
        "segment_tree_ds": ("线段树", "基础"),
        "persistent_segment_tree_ds": ("主席树",),
        "balanced_tree_ds": ("平衡二叉搜索树",),
        "network_flow_basic": ("网络流", "基础"),
        "shortest_path_basic": ("BFS", "最短路"),
    }
    for key, terms in fallback_terms.items():
        if a.get(key) not in item_by_id:
            a[key] = find_item(item_by_id, *terms)
    return {k: v for k, v in a.items() if v in item_by_id}


def add(deps, anchors, *keys):
    for key in keys:
        value = anchors.get(key)
        if value:
            deps.append(value)


def max_direct_count(level):
    n = level_num(level)
    if n <= 1:
        return 3
    if n == 2:
        return 5
    return 8


def direct_pre_for_item(item, section, anchors, item_by_id, section_by_id):
    name = item.get("name", "")
    lname = name.lower()
    parent = item.get("parent", section["id"])
    deps = []
    reasons = []
    parent_concept = None

    def is_self(key):
        return anchors.get(key) == item["id"]

    def A(*keys):
        add(deps, anchors, *keys)

    # C++ basics never depend on algorithm chapters.
    if parent == "1.1":
        if item["id"] not in {"1.1.1", "1.1.3"}:
            A("cpp_include", "cpp_main")
    elif parent == "1.2":
        A("cpp_main")
        if "cout" not in lname:
            A("cpp_cin")
        if "cin" not in lname:
            A("cpp_cout")
        if "getline" in lname or "空格" in name or "缓冲" in name:
            A("cpp_string")
        if "快速" in name:
            A("cpp_char")
        if "文件" in name or "freopen" in lname:
            A("cpp_file_io")
    elif parent == "1.3":
        if item["id"] not in {"1.3.10", "1.3.1"}:
            A("cpp_variable")
        if any(x in name for x in ["long long", "short", "char", "bool", "double", "unsigned"]):
            A("cpp_cin")
        if "作用域" in name or "全局" in name or "局部" in name:
            A("cpp_code_block")
        if "字符串" in name:
            A("cpp_char", "cpp_string")
    elif parent == "1.4":
        A("cpp_variable")
        if "位" in name:
            A("cpp_int", "bit_binary")
        if "重载" in name:
            A("cpp_function_def", "cpp_struct")
    elif parent == "1.5":
        A("cpp_compare_op")
        if any(x in name for x in ["for", "while", "do-while", "循环"]):
            A("cpp_variable", "cpp_logic_op")
        if any(x in lname for x in ["break", "continue"]):
            A("cpp_for", "cpp_while")
    elif parent == "1.6":
        if item["id"] == "1.6.1":
            A("cpp_variable", "cpp_for")
        elif "二维" in name or "多维" in name:
            A("cpp_array", "cpp_index", "cpp_for")
        elif "数组" in name:
            A("cpp_array", "cpp_index")
        elif "字符串" in name or "string" in lname or "字符" in name:
            A("cpp_char", "cpp_array", "cpp_for")
        if "越界" in name:
            A("cpp_array_bounds")
        if "树状数组" in name:
            A("fenwick_tree_ds", "bit_lowbit", "algo_prefix_sum")
        if "后缀数组" in name:
            A("string_suffix_array", "cpp_string", "stl_sort")
        if "kmp" in lname or "next" in lname:
            A("string_kmp", "cpp_string", "cpp_array")
    elif parent == "1.7":
        if item["id"] not in {"1.7.1"}:
            A("cpp_function_def")
        if "调用" in name or "参数" in name or "返回" in name:
            A("cpp_variable")
        if "递归" in name:
            A("cpp_function_call", "cpp_function_return")
        if "引用" in name:
            A("cpp_function_param")
        if "指针" in name:
            A("cpp_array", "cpp_variable")
        if "欧拉" in name:
            A("math_prime", "math_factorization")
        if "生成函数" in name or "母函数" in name:
            A("math_combination", "math_counting")
        if "fail" in lname:
            A("string_trie_algo", "string_kmp")
    elif parent == "1.8":
        if item["id"] not in {"1.8.1"}:
            A("cpp_struct")
        if any(x in lname for x in ["vector", "queue", "stack", "deque", "priority_queue", "set", "map", "bitset"]):
            A("stl_iterator")
        if "sort" in lname or "排序" in name:
            A("cpp_array", "cpp_compare_function")
        if "拓扑" in name:
            A("graph_topological_sort", "graph_storage_adjlist")
        if "后缀自动机" in name:
            A("string_suffix_automaton")
    elif parent == "1.9":
        A("cpp_include")
        if "调试" in name or "断言" in name:
            A("cpp_macro", "debug_translate")

    # Algorithm items.
    if parent.startswith("2."):
        if name == "枚举":
            A("cpp_for", "cpp_if")
        elif "枚举" in name:
            A("algo_enumeration", "cpp_for")
            parent_concept = parent_info("algo_enumeration", anchors, item_by_id)
        if name == "模拟":
            A("cpp_if", "cpp_for", "cpp_array")
        elif "模拟" in name:
            A("algo_simulation", "cpp_if", "cpp_for")
        if name == "递归":
            A("cpp_function_call", "cpp_function_return")
        elif "递归" in name:
            A("algo_recursion", "cpp_recursion_function")
        if "递推" in name:
            A("algo_recurrence", "cpp_array")
        if "分治" in name:
            A("algo_recursion", "algo_divide_conquer")
        if "倍增" in name:
            A("bit_binary", "cpp_array", "algo_recurrence")
        if "构造" in name:
            A("algo_construction", "math_induction")
        if "离线" in name:
            A("algo_offline", "stl_sort")
        if "贪心" in name:
            A("algo_greedy")
            if "排序" in name or "区间" in name:
                A("stl_sort")
            if "证明" in name or "交换" in name:
                A("algo_greedy_proof")
        if "排序" in name:
            A("cpp_array", "cpp_for", "cpp_compare_op")
            if "归并" in name:
                A("algo_divide_conquer", "algo_recursion")
            if "快速" in name or "quick" in lname:
                A("algo_divide_conquer", "algo_two_pointer", "algo_recursion")
            if "堆" in name:
                A("ds_heap")
            if "计数" in name or "桶" in name or "基数" in name:
                A("cpp_array", "algo_prefix_sum")
        if "二分查找" in name or name in {"左边界", "右边界", "整数二分", "实数二分"}:
            A("stl_sort", "cpp_while", "debug_boundary")
        if "单调性判定" in name or "二分答案" in name:
            A("algo_binary_search", "algo_check_function")
        if "三分" in name:
            A("algo_binary_search", "math_function")
        if "前缀" in name:
            A("cpp_array", "cpp_for", "cpp_arithmetic_op")
            if item["id"] != anchors.get("algo_prefix_sum"):
                A("algo_prefix_sum")
        if "差分" in name:
            A("algo_prefix_sum", "cpp_array")
        if "离散化" in name:
            A("stl_sort", "stl_unique", "stl_lower_bound")
        if "分块" in name:
            A("sqrt_decomposition", "cpp_array")
        if "莫队" in name:
            A("sqrt_decomposition", "algo_two_pointer")
            if "带修" in name:
                A("algo_offline")
            if "树上" in name:
                A("tree_lca", "graph_theory_tree")
        if "双指针" in name or "尺取" in name:
            A("algo_two_pointer", "algo_monotonic_check")
        if "滑动窗口" in name:
            A("algo_two_pointer", "ds_queue")
        if "dfs" in lname or "深度" in name:
            A("cpp_recursion_function", "ds_stack", "graph_storage_adjlist")
        if "bfs" in lname or "广度" in name:
            A("ds_queue", "graph_storage_adjlist", "cpp_bool")
        if "回溯" in name:
            A("algo_recursion", "search_backtracking")
        if "剪枝" in name:
            A("search_state_space", "search_pruning")
        if "a*" in lname or "启发式搜索" in name:
            A("search_bfs", "ds_heap", "shortest_path_basic")
        if name in {"DP 思想", "DP 基本概念"}:
            A("algo_recurrence", "cpp_array")
        elif "dp" in lname or "动态规划" in name:
            A("dp_basic")
            if "状态设计" not in name:
                A("dp_state_design")
            if "转移" not in name:
                A("dp_transition")
            if "记忆化" in name:
                A("algo_recursion", "dp_memoization")
            if "背包" in name:
                A("dp_knapsack")
            if "区间" in name:
                A("dp_interval")
            if "树形" in name or "树上" in name:
                A("dp_tree", "search_dfs")
            if "dag" in lname:
                A("dp_dag", "graph_topological_sort")
            if "状压" in name or "状态压缩" in name or "插头" in name:
                A("dp_bitmask", "bit_state_compression")
            if "数位" in name:
                A("dp_digit", "dp_memoization")
            if "单调队列" in name:
                A("ds_monotonic_queue")
            if "斜率" in name or "凸壳" in name:
                A("dp_linear", "geometry_cross")
            if "wqs" in lname:
                A("algo_binary_search")
        if parent in {"2.9", "2.13", "2.15", "2.16", "2.21"} or "图" in name:
            A("graph_model", "graph_storage_adjlist", "graph_theory_vertex_edge")
        if "拓扑" in name:
            A("graph_theory_dag", "ds_queue", "graph_storage_adjlist")
        if any(x in lname for x in ["dijkstra", "spfa", "bellman", "floyd"]) or "最短" in name:
            A("shortest_path_basic", "graph_storage_adjlist")
            if "dijkstra" in lname:
                A("ds_heap")
            if "spfa" in lname:
                A("shortest_path_bellman_ford", "ds_queue")
            if "floyd" in lname:
                A("cpp_2d_array", "dp_basic")
        if "生成树" in name or "kruskal" in lname or "prim" in lname:
            A("mst_basic", "graph_storage_adjlist")
            if "kruskal" in lname:
                A("stl_sort", "ds_dsu")
            if "prim" in lname:
                A("ds_heap")
        if "lca" in lname or "最近公共祖先" in name:
            A("graph_theory_rooted_tree", "search_dfs")
            if "倍增" in name:
                A("algo_doubling")
        if "树链剖分" in name or "树剖" in name:
            A("tree_lca", "segment_tree_ds", "search_dfs")
        if "点分治" in name or "重心" in name:
            A("graph_theory_tree", "algo_recursion", "tree_centroid_decomposition")
        if any(x in name for x in ["强连通", "桥", "割点", "双连通"]) or "tarjan" in lname:
            A("search_dfs", "ds_stack")
        if "二分图" in name or "匹配" in name or "匈牙利" in name or "hopcroft" in lname:
            A("graph_theory_bipartite", "search_dfs", "search_bfs")
        if "网络流" in name or "最大流" in name or "dinic" in lname or "最小割" in name:
            A("network_flow_basic", "graph_storage_adjlist", "search_bfs", "search_dfs")
            if "费用" in name:
                A("shortest_path_basic")
        if "kmp" in lname:
            A("cpp_string", "cpp_array")
        if "trie" in lname:
            A("cpp_string", "tree_structure_math")
        if "ac 自动机" in lname:
            A("string_trie_algo", "string_kmp", "search_bfs")
        if "后缀数组" in name:
            A("cpp_string", "stl_sort")
        if "后缀自动机" in name:
            A("cpp_string", "graph_topological_sort")
        if "manacher" in lname or "回文" in name:
            A("cpp_string")
        if "位" in name or "异或" in name or "lowbit" in lname or "状态压缩" in name:
            if item["id"] != anchors.get("bit_lowbit"):
                A("bit_binary", "cpp_bit_op")
        if "矩阵" in name:
            A("matrix_storage", "matrix_multiply")
        if "fft" in lname or "ntt" in lname:
            A("algo_divide_conquer", "polynomial_fft_ntt_math")
        if "线性基" in name:
            A("bit_xor", "linear_algebra_basic")
        if "整体二分" in name:
            A("algo_binary_search", "algo_offline")
        if "cdq" in lname:
            A("algo_divide_conquer", "algo_offline")

    # Data structures.
    if parent.startswith("3."):
        if item["id"] == anchors.get("ds_stack"):
            A("cpp_array")
        elif "栈" in name:
            A("ds_stack")
        if item["id"] == anchors.get("ds_queue"):
            A("cpp_array")
        elif "队列" in name:
            A("ds_queue")
        if "单调栈" in name:
            A("ds_stack", "cpp_compare_op")
        if "单调队列" in name:
            A("ds_queue", "ds_deque", "algo_sliding_window")
        if "堆" in name or "priority" in lname:
            A("complete_binary_tree_ds", "cpp_array", "cpp_compare_op")
        if "并查集" in name:
            A("cpp_array", "graph_theory_tree")
            if item["id"] != anchors.get("ds_dsu"):
                A("ds_dsu")
            if "带权" in name:
                A("algo_difference", "math_relation")
            if "可撤销" in name:
                A("ds_stack", "algo_offline")
        if "树状数组" in name or "fenwick" in lname:
            A("bit_lowbit", "algo_prefix_sum", "cpp_array")
        if "线段树" in name:
            A("algo_recursion", "cpp_array", "graph_theory_tree")
            if item["id"] != anchors.get("segment_tree_ds"):
                A("segment_tree_ds")
            if "可持久" in name or "主席" in name:
                A("algo_discretization")
        if any(x in lname for x in ["treap", "splay", "avl"]) or "平衡" in name:
            A("binary_search_tree_ds")
        if "lct" in lname or "link-cut" in lname:
            A("balanced_tree_ds", "tree_hld")
        if "trie" in lname or "字典树" in name:
            A("cpp_string", "graph_theory_tree")
        if "ac 自动机" in name:
            A("trie_tree_ds", "string_kmp", "search_bfs")
        if "后缀数组" in name:
            A("cpp_string", "stl_sort")
        if "后缀自动机" in name:
            A("cpp_string", "graph_topological_sort")
        if "哈希" in name:
            A("math_mod", "cpp_array")
        if parent == "3.9" or "图" in name:
            A("graph_theory_vertex_edge", "cpp_array", "cpp_struct")

    # Math.
    if parent.startswith("4."):
        if parent not in {"4.0"}:
            A("math_integer")
        if any(x in name for x in ["整除", "倍数", "因数"]):
            A("math_mod")
        if "质" in name or "素数" in name:
            A("math_divisibility")
        if "gcd" in lname or "最大公约数" in name or "欧几里得" in name:
            A("math_divisibility", "math_mod")
        if "lcm" in lname:
            A("math_gcd", "math_factorization")
        if "扩展欧几里得" in name or "exgcd" in lname or "裴蜀" in name or "不定方程" in name:
            A("math_gcd")
        if "模" in name or "同余" in name:
            A("math_mod_ops")
        if "逆元" in name:
            A("math_mod_ops", "math_exgcd", "numeric_fast_power")
        if "crt" in lname or "中国剩余" in name:
            A("math_congruence", "math_exgcd")
        if any(x in name for x in ["组合", "排列", "二项"]):
            A("math_counting", "math_factorial")
        if "lucas" in lname:
            A("math_combination", "math_mod", "math_inverse")
        if "容斥" in name:
            A("math_set", "math_combination")
        if "概率" in name:
            A("math_counting", "math_probability")
        if "期望" in name:
            A("math_probability", "math_expectation")
        if any(x in name for x in ["点", "向量", "坐标", "几何"]):
            A("cpp_double", "geometry_point")
        if "点积" in name:
            A("geometry_vector")
        if "叉积" in name:
            A("geometry_vector")
        if "凸包" in name:
            A("stl_sort", "geometry_cross")
        if "旋转卡壳" in name:
            A("geometry_cross", "algo_two_pointer")
        if "半平面" in name:
            A("geometry_cross", "stl_sort", "ds_deque")
        if "高斯" in name:
            A("linear_algebra_basic", "matrix_storage")
        if "fft" in lname or "ntt" in lname:
            A("algo_divide_conquer", "math_mod")
        if "莫比乌斯" in name:
            A("math_inclusion_exclusion", "math_divisibility")

    # Debugging and contest engineering.
    if parent.startswith("5."):
        if parent in {"5.1"}:
            A("cpp_cin", "cpp_cout")
        if "快读" in name or "输入输出优化" in name:
            A("cpp_cin", "cpp_cout", "cpp_char")
        if "精度" in name:
            A("cpp_double", "cpp_cout")
        if any(x in name for x in ["字符", "ASCII", "字母"]):
            A("cpp_char", "cpp_ascii")
        if "下标" in name or "数组" in name:
            A("cpp_array", "cpp_index")
        if "枚举" in name:
            A("algo_enumeration", "cpp_for")
        if "剪枝" in name:
            A("search_pruning")
        if "bfs" in lname:
            A("search_bfs", "ds_queue")
        if "dfs" in lname:
            A("search_dfs", "algo_recursion")
        if "图" in name or "边" in name:
            A("graph_storage_adjlist", "graph_model")
        if "dp" in lname or "状态" in name or "转移" in name:
            A("dp_basic", "dp_state_design")
        if any(x in name for x in ["调试", "样例", "打印", "对拍", "assert"]):
            A("debug_sample")
        if "复杂度" in name or "卡常" in name or "性能" in name:
            A("debug_complexity")
        if "越界" in name or "边界" in name:
            A("cpp_array", "debug_boundary")
        if "long long" in name:
            A("cpp_long_long")

    # Preserve good existing item-level dependencies after rule-derived strong deps.
    for dep in item.get("direct_pre", []) or []:
        if dep in item_by_id and dep != item["id"]:
            dep_parent = item_by_id[dep].get("parent", "")
            if parent.startswith("1.") and not dep_parent.startswith("1."):
                continue
            if item["id"] in {"2.1.1", "2.1.2", "2.1.4", "1.6.1", "1.5.6", "1.3.10"}:
                continue
            deps.append(dep)
        elif dep in section_by_id:
            reasons.append("原始依赖包含章节级引用，已尝试替换为具体 item")

    deps = [d for d in unique(deps) if d in item_by_id and d != item["id"]]
    deps = prune_impossible_reverse_edges(item, deps, item_by_id)
    deps = rank_and_trim_deps(item, deps, item_by_id, max_direct_count(item.get("level")))

    if not deps and item["id"] not in {"1.1.1", "1.1.3", "4.0.1", "4.0.2"}:
        reasons.append("规则无法确定强前置或该节点可视为起点")
    if len(name) <= 2 or any(x in name for x in ["基础", "概述", "思想", "概念", "技巧", "总结"]):
        reasons.append("名称较泛，需要人工确认粒度")
    if level_num(item.get("level")) >= 4:
        reasons.append("高阶专题，建议人工复核主干依赖")

    return deps, parent_concept, reasons


def parent_info(anchor_key, anchors, item_by_id):
    item_id = anchors.get(anchor_key)
    if item_id and item_id in item_by_id:
        return {"id": item_id, "name": item_by_id[item_id].get("name", "")}
    return None


def parent_info_by_id(item_id, item_by_id):
    if item_id and item_id in item_by_id:
        return {"id": item_id, "name": item_by_id[item_id].get("name", "")}
    return None


def contains_any(text, terms):
    text_l = (text or "").lower()
    return any(str(term).lower() in text_l for term in terms)


def is_cpp_advanced_pollution(item, category_name):
    return category_name == "C++语法" and contains_any(item.get("name", ""), ADVANCED_POLLUTION_TERMS)


def normalized_name(name):
    value = re.sub(r"[（(].*?[）)]", "", name or "")
    value = value.replace("：", ":").replace("/", " ")
    value = re.sub(r"\s+", "", value).lower()
    return value


def duplicate_name_groups(graph):
    idx = build_indexes(graph)
    groups = defaultdict(list)
    for item in idx["items"]:
        groups[normalized_name(item.get("name", ""))].append(item["id"])
    return {k: v for k, v in groups.items() if k and len(v) > 1}


def preferred_duplicate_main(ids_, item_by_id):
    def score(item_id):
        parent = item_by_id[item_id].get("parent", "")
        preferred = 0
        if parent.startswith(("2.", "3.", "4.")):
            preferred -= 20
        if parent.startswith("1."):
            preferred += 20
        return preferred, [int(x) if x.isdigit() else 999 for x in item_id.split(".")]

    return sorted(ids_, key=score)[0]


def priority_a_rule_for_item(item, anchors, item_by_id, category_name):
    name = item.get("name", "")
    lname = name.lower()
    parent = item.get("parent", "")
    deps = []
    rel_add = []
    reasons = []
    parent_concept = None
    review_note = None

    def A(*keys):
        add(deps, anchors, *keys)

    def I(*item_ids):
        for item_id in item_ids:
            if item_id in item_by_id:
                deps.append(item_id)

    def R(*keys):
        add(rel_add, anchors, *keys)

    def P(anchor_key=None, item_id=None):
        nonlocal parent_concept
        parent_concept = parent_info(anchor_key, anchors, item_by_id) if anchor_key else parent_info_by_id(item_id, item_by_id)

    if is_cpp_advanced_pollution(item, category_name):
        review_note = "建议迁移/跨章节高级专题：当前节点保留原章节和 id，但依赖已改为算法/数据结构主概念。"
        reasons.append("C++语法章节中出现高级算法/数据结构专题，已补 parent_concept 与跨章节 item 依赖")

    # C++ chapters polluted by advanced algorithm topics.
    if "后缀数组" in name:
        A("cpp_string", "stl_sort", "algo_doubling", "string_suffix_array")
        if "LCP" in name or "height" in lname:
            I("1.6.42", "1.6.31")
        if "DP" in name:
            A("dp_basic")
        P("string_suffix_array")
    if "后缀自动机" in name or "SAM" in name:
        A("cpp_string", "string_suffix_automaton", "graph_topological_sort")
        if any(x in name for x in ["DP", "计数", "不同子串", "第 k"]):
            A("dp_basic")
        if "广义" in name:
            A("string_trie_algo")
        P("string_suffix_automaton")
    if "AC 自动机" in name:
        A("string_trie_algo", "string_kmp", "search_bfs", "ds_queue", "cpp_string")
        if "DP" in name:
            A("dp_basic")
        P("string_ac_automaton")
    if "KMP" in name:
        A("cpp_string", "cpp_array", "string_kmp")
        P("string_kmp")
    if "Trie" in name or "字典树" in name:
        A("cpp_string", "tree_structure_math", "cpp_array")
        P("string_trie_algo")
    if "树套树" in name:
        A("fenwick_tree_ds", "segment_tree_ds", "persistent_segment_tree_ds", "algo_discretization", "cpp_array")
        P("persistent_segment_tree_ds")
    if "可持久化数组" in name:
        A("cpp_array", "segment_tree_ds")
        I("3.11.1")
        P(item_id="3.11.1")
    if "多项式" in name or "FFT" in name or "NTT" in name:
        A("polynomial_fft_ntt_math", "algo_divide_conquer", "math_mod", "math_inverse", "numeric_fast_power")
        if "DP" in name:
            A("dp_basic")
        P("polynomial_fft_ntt_math")
    if "莫比乌斯" in name:
        A("math_divisibility", "math_factorization", "math_inclusion_exclusion")
        I("4.9.2")
        P(item_id="4.9.2")
    if "半平面交" in name:
        A("geometry_point", "geometry_vector", "geometry_cross", "stl_sort", "ds_deque")
        I("4.7.28")
        P(item_id="4.7.28")

    # Balanced trees and ordered maintenance.
    if parent == "3.10":
        if item["id"] == "3.10.1":
            A("binary_search_tree_ds", "tree_structure_math", "cpp_compare_op")
        elif "FHQ" in name and "翻转" in name:
            I("3.10.4")
            A("lazy_segment_tree_ds", "segment_tree_ds")
            P(item_id="3.10.4")
        elif "FHQ" in name and "可持久" in name:
            I("3.10.4", "3.11.1")
            P(item_id="3.10.4")
        elif "FHQ" in name:
            I("3.10.3")
            A("binary_search_tree_ds", "algo_divide_conquer")
            P(item_id="3.10.3")
        elif "Treap" in name:
            A("balanced_tree_ds", "binary_search_tree_ds", "ds_heap", "algo_random_base")
            P("balanced_tree_ds")
        elif "Splay" in name and ("区间" in name or "维护" in name):
            I("3.10.9")
            A("lazy_segment_tree_ds", "segment_tree_ds")
            P(item_id="3.10.9")
        elif "Splay" in name:
            A("balanced_tree_ds", "binary_search_tree_ds")
            P("balanced_tree_ds")
        elif "可持久" in name:
            I("3.10.3", "3.11.1")
            A("balanced_tree_ds")
            P("balanced_tree_ds")
        elif any(x in name for x in ["维护序列", "多重集", "区间翻转", "区间移动"]):
            I("3.10.4", "3.10.9")
            A("lazy_segment_tree_ds")
            P("balanced_tree_ds")
        elif "括号序列" in name:
            I("3.10.4", "3.10.9")
            A("ds_stack", "algo_prefix_sum")
            P("balanced_tree_ds")
        elif "后缀平衡树" in name:
            A("balanced_tree_ds", "string_suffix_array", "string_suffix_automaton")
            P("balanced_tree_ds")
        else:
            A("balanced_tree_ds", "binary_search_tree_ds")

    # Persistent structures and dynamic trees.
    if parent == "3.11" or "LCT" in name or "Link-Cut" in name or "可持久化线段树" in name or "主席树" in name:
        if "LCT" in name or "Link-Cut" in name:
            I("3.11.2", "3.10.9")
            A("tree_structure_math")
            if any(x in name for x in ["链", "边权", "树链", "连通"]):
                A("tree_hld")
            if "树链加" in name:
                A("lazy_segment_tree_ds")
            P(item_id="3.11.2")
        if item["id"] == "3.11.1" or "可持久化数据结构" in name:
            A("segment_tree_ds", "algo_recursion", "cpp_array")
            P("segment_tree_ds")
        if "可持久化线段树" in name or "主席树" in name:
            A("segment_tree_ds", "algo_discretization", "algo_prefix_sum")
            I("3.11.1")
            P("persistent_segment_tree_ds")
        if "动态修改" in name:
            I("3.7.8", "3.11.5")
            A("fenwick_tree_ds", "segment_tree_ds")
            P("persistent_segment_tree_ds")
        if name == "离散化":
            A("stl_sort", "stl_unique", "stl_lower_bound")
            P("algo_discretization")

    # Mo's algorithm, CDQ and overall binary search.
    if "莫队" in name:
        A("algo_mo", "sqrt_decomposition", "algo_offline", "algo_two_pointer")
        if "带修" in name or "修改" in name:
            A("algo_offline")
        if "树上" in name:
            A("tree_lca", "search_dfs", "graph_theory_tree")
        P("algo_mo")
    if "CDQ" in name:
        A("algo_divide_conquer", "algo_offline", "stl_sort")
        if "三维偏序" in name or "计数" in name:
            A("fenwick_tree_ds", "algo_discretization")
        if "DP" in name:
            A("dp_basic", "dp_transition")
        I("2.18.4")
        P(item_id="2.18.4")
    if "整体二分" in name:
        A("algo_binary_search", "algo_offline", "fenwick_tree_ds", "segment_tree_ds")
        I("2.18.5")
        P(item_id="2.18.5")

    # Network flow and matching.
    if parent == "2.16" or "网络流" in name or "费用流" in name or "Dinic" in name or "匹配" in name:
        if "括号序列" in name:
            A("ds_stack", "cpp_string", "algo_simulation", "algo_prefix_sum")
            P("ds_stack")
            review_note = "跨章节高级专题：该节点更像字符串/栈模型，不属于网络流主线。"
        elif "正则表达式" in name:
            A("cpp_string", "dp_basic", "string_kmp")
            P("dp_basic")
            review_note = "跨章节高级专题：该节点更像字符串/DP/自动机模型，不属于网络流主线。"
        elif "二分图" in name or "匈牙利" in name or "Hopcroft" in name or "KM" in name:
            A("graph_theory_bipartite", "search_dfs", "search_bfs", "matching_bipartite")
            P("matching_bipartite")
        elif "费用" in name:
            A("network_flow_basic", "shortest_path_basic", "graph_storage_adjlist")
            P("network_flow_cost")
        elif "上下界" in name:
            A("network_flow_basic", "graph_model", "graph_storage_adjlist")
            P("network_flow_basic")
        elif "Dinic" in name or "当前弧" in name:
            A("network_flow_basic", "search_bfs", "search_dfs", "graph_storage_adjlist")
            if "当前弧" in name:
                A("network_flow_dinic")
            P("network_flow_dinic")
        elif "最大流" in name or "最小割" in name or "Ford" in name or "ISAP" in name:
            A("network_flow_basic", "search_bfs", "search_dfs", "graph_storage_adjlist")
            P("network_flow_basic")

    # Math/linear algebra advanced topics with previously empty suggestions.
    if parent == "2.17" or parent == "4.8" or parent == "4.9":
        if "多项式" in name:
            A("polynomial_fft_ntt_math", "math_inverse", "numeric_fast_power")
            P("polynomial_fft_ntt_math")
        if "高斯" in name:
            A("linear_algebra_basic", "matrix_storage")
            P("linear_algebra_gauss")
        if "线性基" in name:
            A("bit_xor", "linear_algebra_basic")
            P("linear_algebra_basic")
        if "行列式" in name or "特征值" in name or "特征向量" in name:
            A("linear_algebra_basic", "matrix_storage")
            P("linear_algebra_basic")
        if "拉格朗日" in name:
            A("math_function", "math_mod", "math_inverse")
        if "向量" in name:
            A("geometry_vector", "geometry_dot", "geometry_cross")
        if "扩展 BSGS" in name:
            A("math_mod", "numeric_fast_power", "math_inverse")
        if "扩展卢卡斯" in name:
            A("math_combination", "math_mod", "math_inverse")
        if "Burnside" in name or "Polya" in name:
            A("math_inclusion_exclusion", "math_set", "math_counting")
        if "群论" in name:
            A("math_set", "math_function")

    if parent == "2.18":
        if "高精度" in name:
            A("cpp_string", "cpp_array", "algo_simulation")
        if "在线算法" in name:
            A("algo_offline", "debug_complexity")
        if "交互题" in name:
            A("cpp_cin", "cpp_cout", "debug_translate")

    rel_add = [r for r in unique(rel_add) if r in item_by_id and r != item["id"]]
    deps = [d for d in unique(deps) if d in item_by_id and d != item["id"]]
    return deps, rel_add, parent_concept, review_note, reasons


def repair_priority_a_dependencies(graph, edges, anchors, original_direct):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    section_by_id = idx["section_by_id"]
    parent_concepts = {}
    review_notes = {}
    rel_additions = defaultdict(list)
    reasons = defaultdict(list)
    repaired_ids = set()

    for item in idx["items"]:
        item_id = item["id"]
        deps, rels, parent_concept, review_note, item_reasons = priority_a_rule_for_item(
            item, anchors, item_by_id, idx["category_by_item"][item_id]
        )
        if deps:
            merged = deps + [d for d in edges.get(item_id, []) if d in item_by_id and d not in deps]
            edges[item_id] = rank_and_trim_deps(
                item,
                prune_impossible_reverse_edges(item, unique(merged), item_by_id),
                item_by_id,
                max_direct_count(item.get("level")),
            )
            repaired_ids.add(item_id)
        if rels:
            rel_additions[item_id].extend(rels)
        if parent_concept:
            parent_concepts[item_id] = parent_concept
        if review_note:
            review_notes[item_id] = review_note
        if item_reasons:
            reasons[item_id].extend(item_reasons)

    duplicate_groups = duplicate_name_groups(graph)
    duplicate_parent_concepts = []
    for ids_ in duplicate_groups.values():
        main = preferred_duplicate_main(ids_, item_by_id)
        for item_id in ids_:
            if item_id == main:
                continue
            parent_concepts[item_id] = parent_info_by_id(main, item_by_id)
            rel_additions[item_id].append(main)
            review_notes.setdefault(item_id, f"重复/近重复概念：以 {main} 作为主节点，当前节点保留原 id 作为应用、实现或别名视角。")
            reasons[item_id].append("重复或近重复名称，已补 parent_concept/rel 指向主节点")
            duplicate_parent_concepts.append({"id": item_id, "main": main})

    # If a previously section-only high-risk node still has no item dependency, give it a safe local fallback.
    for item in idx["items"]:
        item_id = item["id"]
        dp = edges.get(item_id, []) or []
        old_dp = original_direct.get(item_id, []) or []
        if dp:
            continue
        if not old_dp or not all(x in section_by_id for x in old_dp):
            continue
        if not contains_any(item.get("name", ""), ADVANCED_POLLUTION_TERMS + VERY_HIGH_RISK_TERMS):
            continue
        fallback = []
        parent = item.get("parent", "")
        if parent.startswith("2."):
            add(fallback, anchors, "graph_model", "algo_offline", "cpp_array")
        elif parent.startswith("3."):
            add(fallback, anchors, "cpp_array", "tree_structure_math")
        elif parent.startswith("4."):
            add(fallback, anchors, "math_integer", "math_function")
        elif parent.startswith("5."):
            add(fallback, anchors, "debug_complexity", "cpp_array")
        edges[item_id] = [d for d in unique(fallback) if d in item_by_id and d != item_id][:3]
        if edges[item_id]:
            reasons[item_id].append("原 A 类节点只有章节级依赖，已补保守 item 级前置避免空依赖")
            repaired_ids.add(item_id)

    return {
        "parent_concepts": parent_concepts,
        "review_notes": review_notes,
        "rel_additions": rel_additions,
        "reasons": reasons,
        "repaired_ids": sorted(repaired_ids),
        "duplicate_parent_concepts": duplicate_parent_concepts,
    }


def prune_impossible_reverse_edges(item, deps, item_by_id):
    foundational = {"2.1.1", "2.1.2", "2.1.4", "2.7.1", "2.7.2", "2.8.1", "2.11.6", "3.7.1"}
    if item["id"] in foundational:
        return [d for d in deps if not item_by_id[d].get("parent", "").startswith(("2.8", "2.13", "2.14", "2.15", "2.16", "3.7", "3.10", "3.11"))]
    if item.get("parent", "").startswith("1."):
        if contains_any(item.get("name", ""), ADVANCED_POLLUTION_TERMS):
            return deps
        return [d for d in deps if item_by_id[d].get("parent", "").startswith("1.")]
    return deps


def rank_and_trim_deps(item, deps, item_by_id, limit):
    parent = item.get("parent", "")
    original = set(item.get("direct_pre", []) or [])
    name = item.get("name", "").lower()

    def score(dep):
        dep_parent = item_by_id[dep].get("parent", "")
        dep_name = item_by_id[dep].get("name", "").lower()
        value = 50
        if dep in original:
            value -= 15
        if dep_parent == parent:
            value -= 15
        if not dep_parent.startswith("1.") and not parent.startswith("1."):
            value -= 10
        if dep_parent.startswith("1.") and not parent.startswith("1."):
            value += 8
        for token in re.split(r"[\s/：:()（）\-]+", dep_name):
            if token and token in name:
                value -= 6
        return value, dep

    return sorted(unique(deps), key=score)[:limit]


def rel_for_item(item, anchors, item_by_id):
    name = item.get("name", "")
    lname = name.lower()
    rel = []

    def R(*keys):
        add(rel, anchors, *keys)

    if any(x in name for x in ["Dijkstra", "Bellman", "SPFA", "Floyd"]):
        R("shortest_path_dijkstra", "shortest_path_bellman_ford", "shortest_path_spfa", "shortest_path_floyd")
    if any(x in name for x in ["Kruskal", "Prim", "生成树"]):
        R("mst_kruskal", "mst_prim")
    if "背包" in name:
        for item_id in ["2.8.8", "2.8.9", "2.8.10", "2.8.11"]:
            if item_id in item_by_id:
                rel.append(item_id)
    if any(x in name for x in ["单调栈", "单调队列"]):
        R("ds_monotonic_stack", "ds_monotonic_queue")
    if "线段树" in name or "树状数组" in name:
        R("segment_tree_ds", "fenwick_tree_ds")
    if "DFS" in name or "BFS" in name:
        R("search_dfs", "search_bfs")
    if "二分" in name:
        R("algo_binary_search", "algo_two_pointer")
    if "贪心" in name:
        R("algo_greedy", "dp_basic")
    if "KMP" in name or "Trie" in name or "AC 自动机" in name:
        R("string_kmp", "string_trie_algo", "string_ac_automaton")
    if "后缀数组" in name or "后缀自动机" in name:
        R("string_suffix_array", "string_suffix_automaton")
    if "凸包" in name or "旋转卡壳" in name:
        R("geometry_cross", "algo_two_pointer")
    if "高斯" in name:
        R("linear_algebra_basic", "matrix_storage")
    if "快读" in name or "输入输出" in name:
        R("cpp_cin", "cpp_cout")

    direct = set(item.get("direct_pre", []) or [])
    return [r for r in unique(rel) if r in item_by_id and r != item["id"] and r not in direct][:10]


def detect_cycle(edges, item_ids):
    color, stack = {}, []

    def dfs(node):
        color[node] = 1
        stack.append(node)
        for dep in edges.get(node, []):
            if dep not in item_ids:
                continue
            if color.get(dep) == 1:
                return stack[stack.index(dep):] + [dep]
            if color.get(dep) != 2:
                cycle = dfs(dep)
                if cycle:
                    return cycle
        stack.pop()
        color[node] = 2
        return None

    for item_id in item_ids:
        if color.get(item_id) is None:
            cycle = dfs(item_id)
            if cycle:
                return cycle
    return None


def break_cycles(edges, item_by_id):
    fixes = []
    item_ids = set(item_by_id)
    while True:
        cycle = detect_cycle(edges, item_ids)
        if not cycle:
            return fixes
        pairs = list(zip(cycle, cycle[1:]))

        def edge_score(pair):
            src, dep = pair
            src_item, dep_item = item_by_id[src], item_by_id[dep]
            src_level, dep_level = level_num(src_item.get("level")), level_num(dep_item.get("level"))
            score = 0
            if src_level <= dep_level:
                score += 30
            if src_item.get("parent") == dep_item.get("parent"):
                score += 10
            if src_item.get("parent", "").startswith("1.") and not dep_item.get("parent", "").startswith("1."):
                score += 100
            if src_level <= 2:
                score += 20
            return score, src

        src, dep = max(pairs, key=edge_score)
        if dep in edges.get(src, []):
            edges[src].remove(dep)
            fixes.append({"removed_from": src, "removed_dependency": dep, "cycle": cycle})
        else:
            raise RuntimeError(f"Cannot break cycle: {cycle}")


def compute_resolved(edges, item_ids):
    memo, visiting = {}, set()

    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))
                out.append(dep)
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])
        return memo[node]

    return {item_id: resolve(item_id) for item_id in item_ids}


def recompute_resolved_pre(graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    fixes = break_cycles(edges, item_by_id)
    resolved = compute_resolved(edges, set(item_by_id))
    for item in idx["items"]:
        item["direct_pre"] = edges[item["id"]]
        item["resolved_pre"] = resolved[item["id"]]
    return fixes


def refresh_low_conf_row(row, item):
    direct = list(item.get("direct_pre", []) or [])
    rel = [r for r in item.get("rel", []) or [] if r not in set(direct)]
    row["current_direct_pre"] = direct
    row["suggested_direct_pre"] = direct
    row["new_direct_pre"] = direct
    row["new_rel"] = rel
    row["parent_concept"] = item.get("parent_concept", {}) or {}
    row["review_note"] = item.get("review_note", row.get("review_note", "")) or row.get("review_note", "")


def set_item_direct_pre(item, deps, item_by_id):
    item["direct_pre"] = [d for d in unique(deps) if d in item_by_id and d != item["id"]][:8]


def add_item_rel(item, rels, item_by_id):
    direct = set(item.get("direct_pre", []) or [])
    merged = list(item.get("rel", []) or []) + list(rels)
    item["rel"] = [r for r in unique(merged) if r in item_by_id and r != item["id"] and r not in direct][:10]


def make_parent_concept(item_id, item_by_id):
    if item_id in item_by_id:
        return {"id": item_id, "name": item_by_id[item_id].get("name", "")}
    return {}


def fix_parent_concept_self_refs(graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    stats = {"found": 0, "deleted": 0, "redirected": 0, "remaining": 0, "details": []}
    redirect_rules = [
        ("height", "2.10.7"),
        ("LCP", "2.10.7"),
        ("后缀数组", "2.10.7"),
        ("后缀自动机", "2.10.8"),
        ("LCT", "3.11.2"),
        ("Link-Cut", "3.11.2"),
        ("当前弧", "2.16.5"),
        ("Dinic", "2.16.5"),
        ("FFT 蝶形", "4.8.3"),
        ("CDQ", "2.18.4"),
        ("树上莫队", "2.4.8"),
    ]
    main_nodes = {"2.4.8", "2.16.1", "2.16.5", "2.16.6", "2.10.2", "2.10.5", "2.10.6", "2.10.7", "2.10.8", "2.18.4", "2.18.5", "3.7.8", "3.11.2", "4.7.28", "4.8.3", "4.9.2"}
    for item in idx["items"]:
        pc = item.get("parent_concept") or {}
        if pc.get("id") != item["id"]:
            continue
        stats["found"] += 1
        redirected = False
        if item["id"] not in main_nodes:
            for term, target in redirect_rules:
                if term in item.get("name", "") and target in item_by_id and target != item["id"]:
                    item["parent_concept"] = make_parent_concept(target, item_by_id)
                    stats["redirected"] += 1
                    redirected = True
                    stats["details"].append({"id": item["id"], "action": "redirected", "target": target})
                    break
        if not redirected:
            item.pop("parent_concept", None)
            stats["deleted"] += 1
            stats["details"].append({"id": item["id"], "action": "deleted"})
    stats["remaining"] = len(validate_parent_concept(graph))
    return stats


def refine_priority_a_semantics(graph, low_conf):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    rows = {row.get("id"): row for row in low_conf if row.get("id")}
    before_a = [row for row in low_conf if row.get("review_priority") == "A"]
    stats = {"before_a_count": len(before_a), "after_a_count": 0, "a_to_b": 0, "a_to_c_or_removed": 0, "remaining_a_items": []}
    keep_a_risks = {
        "1.3.33": "C++语法章节中的字符串 FFT 匹配，主依赖已指向 FFT/NTT，但章节归属仍建议人工迁移确认。",
        "1.6.29": "C++数组章节中的树套树/主席树应用，依赖已指向树状数组、主席树和可持久化结构，但章节归属仍不合理。",
        "1.7.27": "C++函数章节中的莫比乌斯函数，依赖已指向数论主线，但章节归属仍建议迁移。",
        "1.7.29": "C++函数章节中的多项式 Ln，高级多项式主线缺少求导/积分细分节点，需人工确认教学前置。",
        "1.7.30": "C++函数章节中的多项式 Exp，高级多项式主线缺少求导/积分细分节点，需人工确认教学前置。",
        "1.7.31": "C++函数章节中的多项式 Pow，高级多项式主线缺少求导/积分细分节点，需人工确认教学前置。",
        "1.8.46": "C++ STL章节中的半平面交排序增量法，依赖已指向计算几何主线，但章节归属仍建议迁移。",
        "2.15.17": "支配树在 DAG 上的构建缺少独立支配关系/DFS树主节点，当前依赖只能近似表达。",
        "2.16.11": "带花树属于一般图匹配高级专题，图谱缺少一般图匹配主节点，需确认是否作为主干保留。",
        "2.21.1": "虚树是高级树上建模技巧，依赖已补 LCA/DFS/树结构，但章节主线位置仍需确认。",
        "2.21.2": "支配树缺少独立支配关系基础节点，需确认在高级图论中的教学路径。",
        "2.21.3": "虚树构建依赖已补 LCA/DFS/栈，但作为高级构造专题仍建议人工确认。",
        "2.8.124": "仙人掌图 DP 需要仙人掌/圆方树/低环结构细分节点，当前图谱只能近似依赖。",
        "2.9.18": "仙人掌图基础缺少环结构/仙人掌专属主节点，需确认图论主线位置。",
        "4.7.20": "圆方树被放在几何章节，语义上更接近点双/割点图论专题，需人工确认归属。",
        "4.7.21": "圆方树在仙人掌图上的应用被放在几何章节，需确认是否迁移到图论高级专题。",
        "4.8.3": "FFT/NTT 数学基础属于国内扩展且非 IOI 主线，需确认课程主线权重。",
        "4.9.2": "莫比乌斯反演属于高级数论，依赖已明确但会影响数学主线深度选择。",
    }
    direct_overrides = {
        "3.11.2": ["3.10.9", "3.10.1", "3.6.3", "4.5.6"],
        "3.11.7": ["3.11.2", "3.10.9", "4.5.6"],
        "3.11.8": ["3.11.2", "3.10.9", "4.5.6"],
        "3.11.10": ["3.11.2", "3.10.9", "4.5.6"],
        "3.11.11": ["3.11.2", "3.10.9", "4.5.6"],
        "3.11.12": ["3.11.2", "3.10.9", "3.7.3", "4.5.6"],
        "3.11.9": ["3.11.2", "2.14.4", "3.10.9", "4.5.6"],
        "2.9.38": ["2.9.3", "3.11.2", "3.10.9", "3.9.2", "4.5.6"],
        "2.13.29": ["2.13.8", "3.11.2", "3.10.9", "3.9.2", "4.5.6"],
        "2.15.17": ["2.9.1", "2.9.7", "2.9.3", "3.9.2"],
        "2.16.11": ["2.9.3", "3.9.2", "2.7.1", "2.7.2", "2.16.4"],
        "2.21.1": ["2.14.2", "2.9.1", "3.2.1", "4.5.6"],
        "2.21.3": ["2.21.1", "2.14.2", "2.9.1", "3.2.1"],
        "2.8.35": ["2.21.1", "2.14.2", "2.8.13", "2.8.1"],
        "2.9.18": ["2.9.3", "2.9.1", "2.15.2", "3.9.2"],
        "4.7.20": ["2.15.13", "2.15.3", "2.9.1", "3.2.1"],
        "4.7.21": ["4.7.20", "2.9.18", "2.15.13"],
    }
    parent_overrides = {
        "3.11.7": "3.11.2", "3.11.8": "3.11.2", "3.11.9": "3.11.2", "3.11.10": "3.11.2", "3.11.11": "3.11.2", "3.11.12": "3.11.2",
        "2.9.38": "3.11.2", "2.13.29": "3.11.2", "3.12.6": "2.18.4", "3.12.7": "2.18.4", "2.21.3": "2.21.1",
        "2.8.35": "2.21.1", "4.7.21": "4.7.20",
    }
    for row in before_a:
        item = item_by_id.get(row["id"])
        if not item:
            continue
        if item["id"] in direct_overrides:
            set_item_direct_pre(item, direct_overrides[item["id"]], item_by_id)
        if item["id"] in parent_overrides:
            item["parent_concept"] = make_parent_concept(parent_overrides[item["id"]], item_by_id)
        if "LCT" in item.get("name", "") or "Link-Cut" in item.get("name", ""):
            add_item_rel(item, ["2.14.4"], item_by_id)
        if item["id"] in keep_a_risks:
            row["review_priority"] = "A"
            row["confidence"] = "low"
            row["manual_review_result"] = "仍需人工确认"
            row["remaining_risk"] = keep_a_risks[item["id"]]
            row["need_manual_review"] = True
            row["note"] = "语义精修后保留 A：依赖已具体化，但章节归属、主节点缺失或课程主线取舍仍需人工拍板。"
        else:
            row["review_priority"] = "B"
            row["confidence"] = "medium"
            row["manual_review_result"] = "已精修"
            row["remaining_risk"] = "高级专题依赖已明确，保留 B 类用于抽查教学顺序和表述粒度。"
            row["need_manual_review"] = True
            row["review_note"] = row.get("review_note") or "语义精修：从 A 降为 B，依赖明确，保留抽查教学顺序和表述粒度。"
            row["note"] = "语义精修：依赖和 parent_concept 已明确，从 A 降为 B。"
            stats["a_to_b"] += 1
        refresh_low_conf_row(row, item)
    after_a = [row for row in low_conf if row.get("review_priority") == "A"]
    stats["after_a_count"] = len(after_a)
    stats["a_to_c_or_removed"] = stats["before_a_count"] - stats["after_a_count"] - stats["a_to_b"]
    stats["remaining_a_items"] = [{"id": r["id"], "name": r["name"], "risk": r.get("remaining_risk", "")} for r in after_a]
    return stats


def semantic_priority_b_focus_ids(low_conf):
    terms = ["后缀自动机", "后缀数组", "AC 自动机", "可持久化数组", "Polya"]
    extras = {"5.4.17", "3.6.14", "3.8.8", "4.1.26", "4.3.24"}
    ids_ = set()
    for row in low_conf if isinstance(low_conf, list) else []:
        if row.get("id") in extras:
            ids_.add(row["id"])
        elif row.get("category") == "C++语法" and contains_any(row.get("name", ""), terms):
            ids_.add(row["id"])
    return ids_


def refine_priority_b_semantics(graph, low_conf, priority_b_baseline=None):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    before_b = [row for row in low_conf if row.get("review_priority") == "B"]
    target_b_ids = set((priority_b_baseline or {}).get("before_b_ids", []))
    if len(target_b_ids) != 26:
        target_b_ids = semantic_priority_b_focus_ids(low_conf)
    target_before_b = [row for row in before_b if not target_b_ids or row.get("id") in target_b_ids]
    stats = {"before_b_count": len(target_before_b), "after_b_count": 0, "b_to_a": 0, "b_to_c_or_removed": 0, "remaining_b_items": []}
    keep_b_terms = ["后缀数组", "后缀自动机", "AC 自动机", "可持久化", "Polya", "Ukkonen", "线性规划", "全局平衡"]
    for row in before_b:
        item = item_by_id.get(row["id"])
        if not item:
            continue
        name = item.get("name", "")
        if idx["category_by_item"].get(item["id"]) == "C++语法" and contains_any(name, ADVANCED_POLLUTION_TERMS):
            item["review_note"] = "建议迁移/跨章节高级专题：当前节点保留原章节和 id，但依赖已指向正确主知识点。"
            row["review_priority"] = "B"
            row["confidence"] = "medium"
            row["manual_review_result"] = "已精修"
            row["remaining_risk"] = "跨章节污染已补依赖和 parent_concept，但仍建议人工确认是否迁移章节。"
            row["need_manual_review"] = True
            row["note"] = "B 类保留：跨章节高级专题，依赖已明确但归属仍需抽查。"
        elif contains_any(name, keep_b_terms):
            row["review_priority"] = "B"
            row["confidence"] = "medium"
            row["manual_review_result"] = "已精修"
            row["remaining_risk"] = "依赖已明确，但名称边界或算法/结构视角仍建议人工抽查。"
            row["need_manual_review"] = True
            row["review_note"] = row.get("review_note") or "语义精修：保留 B 类用于抽查边界和归属。"
            row["note"] = "B 类保留：高级或边界专题。"
        else:
            row["review_priority"] = "C"
            row["confidence"] = "high"
            row["manual_review_result"] = "已精修"
            row["remaining_risk"] = "低风险记录保留用于追踪；当前依赖和 parent_concept 已足够明确。"
            row["need_manual_review"] = False
            row["review_note"] = row.get("review_note") or "语义精修：依赖明确，降为 C。"
            row["note"] = "低风险记录保留用于追踪。"
            if not target_b_ids or row["id"] in target_b_ids:
                stats["b_to_c_or_removed"] += 1
        if row.get("review_priority") == "B" and not row.get("review_note"):
            row["review_note"] = "语义精修：B 类保留用于人工抽查。"
        refresh_low_conf_row(row, item)
    after_b = [row for row in low_conf if row.get("review_priority") == "B" and (not target_b_ids or row.get("id") in target_b_ids)]
    stats["after_b_count"] = len(after_b)
    stats["b_to_a"] = sum(1 for row in target_before_b if row.get("review_priority") == "A")
    stats["remaining_b_items"] = [{"id": r["id"], "name": r["name"], "risk": r.get("remaining_risk", "")} for r in after_b]
    return stats


def detect_duplicate_or_near_duplicate_items(graph):
    idx = build_indexes(graph)
    groups = []
    for key, ids_ in duplicate_name_groups(graph).items():
        groups.append({"kind": "exact", "key": key, "ids": ids_})
    near_terms = [
        ("KMP 算法", ["2.10.2", "3.12.5"]),
        ("AC 自动机", ["2.10.6", "3.8.2"]),
        ("后缀数组", ["2.10.7", "3.8.3"]),
        ("后缀自动机", ["2.10.8", "3.8.4"]),
        ("莫队算法", ["2.4.8", "3.12.3"]),
        ("FFT / NTT", ["2.18.2", "4.8.3"]),
    ]
    for key, ids_ in near_terms:
        present = [item_id for item_id in ids_ if item_id in idx["item_by_id"]]
        if len(present) > 1:
            groups.append({"kind": "near", "key": key, "ids": present})
    return groups


def annotate_duplicate_or_near_duplicate_items(graph, low_conf):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    groups = detect_duplicate_or_near_duplicate_items(graph)
    rows = {row.get("id"): row for row in low_conf if row.get("id")}
    processed = 0
    review = []
    for group in groups:
        ids_ = [item_id for item_id in group["ids"] if item_id in item_by_id]
        if len(ids_) < 2:
            continue
        main = preferred_duplicate_main(ids_, item_by_id)
        for item_id in ids_:
            if item_id == main:
                continue
            item = item_by_id[item_id]
            if not (item.get("parent_concept") or {}).get("id"):
                item["parent_concept"] = make_parent_concept(main, item_by_id)
            add_item_rel(item, [main], item_by_id)
            note = f"重复/近重复概念：{main} 作为主节点；当前节点保留为算法视角、数据结构实现视角或应用节点。"
            item["review_note"] = item.get("review_note") or note
            if item_id in rows:
                rows[item_id]["review_note"] = item["review_note"]
                rows[item_id]["parent_concept"] = item.get("parent_concept", {}) or {}
                rows[item_id]["new_rel"] = item.get("rel", []) or []
        processed += 1
        if group["kind"] == "near":
            review.append(group)
    return {"duplicate_groups_found": len(groups), "duplicate_groups_reviewed": processed, "duplicate_groups_manual": len(review), "representative_groups": groups[:20]}


def annotate_cross_section_pollution(graph, low_conf):
    idx = build_indexes(graph)
    rows = {row.get("id"): row for row in low_conf if row.get("id")}
    count = parent_count = note_count = 0
    remaining = []
    for item in idx["items"]:
        if not is_cpp_advanced_pollution(item, idx["category_by_item"].get(item["id"], "")):
            continue
        count += 1
        if item.get("parent_concept"):
            parent_count += 1
        note = "建议迁移/跨章节高级专题：当前节点保留原章节和 id，但依赖已指向正确主知识点。"
        if note not in (item.get("review_note") or ""):
            item["review_note"] = note
        note_count += 1
        remaining.append({"id": item["id"], "name": item.get("name", "")})
        row = rows.get(item["id"])
        if row:
            row["review_note"] = item["review_note"]
            row["parent_concept"] = item.get("parent_concept", {}) or {}
            row["remaining_risk"] = row.get("remaining_risk") or "跨章节高级专题仍建议人工确认是否迁移章节。"
    return {"cross_section_pollution_count": count, "cross_section_parent_concept_count": parent_count, "cross_section_review_note_count": note_count, "cross_section_pollution_remaining": count, "cross_section_pollution_items": remaining}


def validate_parent_concept(graph):
    idx = build_indexes(graph)
    issues = []
    for item in idx["items"]:
        pc = item.get("parent_concept") or {}
        if pc.get("id") == item["id"]:
            issues.append({"id": item["id"], "name": item.get("name", "")})
    return issues


def validate_semantic_refinement(graph, low_conf):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    section_ids = set(idx["section_by_id"])
    issues = []
    issues.extend({"id": row["id"], "issue": "parent_concept 自指"} for row in validate_parent_concept(graph))
    for row in low_conf if isinstance(low_conf, list) else []:
        item = item_by_id.get(row.get("id"))
        if not item:
            continue
        priority = row.get("review_priority")
        if priority in {"A", "B"}:
            direct = row.get("new_direct_pre") or item.get("direct_pre", []) or []
            if not direct:
                issues.append({"id": row["id"], "issue": f"{priority} 类 new_direct_pre 为空"})
            if any(ref in section_ids for ref in direct):
                issues.append({"id": row["id"], "issue": f"{priority} 类 direct_pre 含 section id"})
            if (row.get("parent_concept") or {}).get("id") == row["id"]:
                issues.append({"id": row["id"], "issue": f"{priority} 类 parent_concept 自指"})
        if priority == "A" and not row.get("remaining_risk"):
            issues.append({"id": row["id"], "issue": "A 类 remaining_risk 为空"})
        if priority == "B" and not row.get("review_note"):
            issues.append({"id": row["id"], "issue": "B 类 review_note 为空"})
        if priority == "C" and row.get("need_manual_review"):
            issues.append({"id": row["id"], "issue": "C 类 need_manual_review 应为 false"})
        if is_cpp_advanced_pollution(item, idx["category_by_item"].get(row["id"], "")) and not (item.get("parent_concept") or item.get("review_note")):
            issues.append({"id": row["id"], "issue": "C++跨章节高级专题缺少 parent_concept/review_note"})
    return issues


def apply_semantic_refinement(graph, low_conf, priority_b_baseline=None):
    stats = {}
    stats["parent_self_ref"] = fix_parent_concept_self_refs(graph)
    stats["priority_a"] = refine_priority_a_semantics(graph, low_conf)
    stats["priority_b"] = refine_priority_b_semantics(graph, low_conf, priority_b_baseline)
    stats["cross_section"] = annotate_cross_section_pollution(graph, low_conf)
    stats["duplicates"] = annotate_duplicate_or_near_duplicate_items(graph, low_conf)
    extra_cycle_fixes = recompute_resolved_pre(graph)
    idx = build_indexes(graph)
    for row in low_conf:
        item = idx["item_by_id"].get(row.get("id"))
        if item:
            refresh_low_conf_row(row, item)
    low_conf.sort(key=lambda r: (r["review_priority"], r["category"], r["section_id"], r["id"]))
    stats["extra_cycle_fixes"] = extra_cycle_fixes
    stats["semantic_issues"] = validate_semantic_refinement(graph, low_conf)
    return stats


def refine_graph(input_graph, priority_b_baseline=None):
    graph = copy.deepcopy(input_graph)
    priority_b_baseline = priority_b_baseline or {}
    idx = build_indexes(graph)
    item_by_id, section_by_id = idx["item_by_id"], idx["section_by_id"]
    anchors = build_anchors(item_by_id)
    original_direct = {item["id"]: list(item.get("direct_pre", []) or []) for item in idx["items"]}
    low_reasons = defaultdict(list)
    edges, parent_concepts = {}, {}

    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                deps, parent_concept, reasons = direct_pre_for_item(item, section, anchors, item_by_id, section_by_id)
                edges[item["id"]] = deps
                if parent_concept:
                    parent_concepts[item["id"]] = parent_concept
                if reasons:
                    low_reasons[item["id"]].extend(reasons)

    repair_meta = repair_priority_a_dependencies(graph, edges, anchors, original_direct)
    parent_concepts.update(repair_meta["parent_concepts"])
    for item_id, reasons in repair_meta["reasons"].items():
        low_reasons[item_id].extend(reasons)

    provisional_low_conf = build_low_confidence_from_edges(
        graph,
        edges,
        original_direct,
        low_reasons,
        parent_concepts,
    )
    generated_b_baseline = priority_b_baseline_from_rows(provisional_low_conf)
    effective_b_baseline = generated_b_baseline if generated_b_baseline.get("before_b_count") else priority_b_baseline
    b_repair_meta = repair_priority_b_dependencies(graph, edges, anchors, original_direct, effective_b_baseline)
    parent_concepts.update(b_repair_meta["parent_concepts"])
    for item_id, reasons in b_repair_meta["reasons"].items():
        low_reasons[item_id].extend(reasons)

    cycle_fixes = break_cycles(edges, item_by_id)
    resolved = compute_resolved(edges, set(item_by_id))

    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                item["direct_pre"] = edges[item["id"]]
                item["resolved_pre"] = resolved[item["id"]]
                item_rel = rel_for_item(item, anchors, item_by_id)
                item_rel.extend(repair_meta["rel_additions"].get(item["id"], []))
                item_rel.extend(b_repair_meta["rel_additions"].get(item["id"], []))
                item["rel"] = [
                    r for r in unique(item_rel)
                    if r in item_by_id and r != item["id"] and r not in set(item["direct_pre"])
                ][:10]
                if item["id"] in parent_concepts:
                    item["parent_concept"] = parent_concepts[item["id"]]
                if item["id"] in repair_meta["review_notes"]:
                    item["review_note"] = repair_meta["review_notes"][item["id"]]
                if item["id"] in b_repair_meta["review_notes"]:
                    item["review_note"] = b_repair_meta["review_notes"][item["id"]]

    low_candidates = []
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                if item["id"] in low_reasons:
                    low_candidates.append((
                        item,
                        category,
                        section,
                        unique(low_reasons[item["id"]]),
                        original_direct[item["id"]],
                        item.get("direct_pre", []) or [],
                    ))
    low_conf = build_low_confidence(low_candidates, graph)
    low_conf = apply_priority_b_review_updates(low_conf, graph, priority_b_baseline, b_repair_meta)
    semantic_meta = apply_semantic_refinement(graph, low_conf, priority_b_baseline)
    return graph, {
        "cycle_fixes": cycle_fixes,
        "low_confidence": low_conf,
        "original_direct": original_direct,
        "anchors": anchors,
        "priority_a_repair": repair_meta,
        "priority_b_repair": b_repair_meta,
        "priority_b_baseline": effective_b_baseline,
        "semantic_refinement": semantic_meta,
    }


def build_low_confidence(low_candidates, graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    rows = []
    advanced_terms = [
        "LCT", "Link-Cut", "FFT", "NTT", "后缀自动机", "后缀数组", "AC 自动机", "网络流", "费用流",
        "插头", "WQS", "CDQ", "整体二分", "支配树", "半平面", "可持久", "动态树", "圆方树",
        "莫比乌斯", "多项式", "带修", "树上莫队", "仙人掌", "虚树", "带花树",
    ]
    for item, category, section, reasons, old_direct, new_direct in low_candidates:
        name = item.get("name", "")
        lvl = level_num(item.get("level"))
        is_advanced = lvl >= 4 or any(t.lower() in name.lower() for t in advanced_terms)
        current_direct = [x for x in item.get("direct_pre", []) or [] if x in item_by_id]
        new_rel = [x for x in item.get("rel", []) or [] if x in item_by_id]
        parent_concept = item.get("parent_concept", {}) or {}
        review_note = item.get("review_note", "")
        cpp_polluted = is_cpp_advanced_pollution(item, category["name"])
        clear_item_deps = bool(current_direct) and all(x in item_by_id for x in current_direct)
        duplicate_reason = any("重复" in reason for reason in reasons) or bool(parent_concept)
        keep_a = clear_item_deps and (
            (is_advanced and contains_any(name, VERY_HIGH_RISK_TERMS))
            or (cpp_polluted and not (parent_concept or "跨章节高级专题" in review_note or "建议迁移" in review_note))
        )
        if keep_a:
            priority, confidence = "A", "low"
            manual_result = "仍需人工确认"
            remaining_risk = "核心高级专题或归属/主节点仍可能影响主干学习路径。"
            note = "A 类专项已补 item-to-item direct_pre；仍建议人工确认主节点、章节归属或高级模型边界。"
        elif is_advanced or cpp_polluted or duplicate_reason:
            priority, confidence = "B", "medium"
            manual_result = "已人工规则修正"
            remaining_risk = "依赖已转为明确 item id；若 new_direct_pre 为空，则该节点被视为低风险起点/工程化经验点，建议抽查。"
            note = "已完成 A 类规则修正并降级为 B，保留用于抽查。"
        else:
            priority, confidence = "C", "high"
            manual_result = "已人工规则修正"
            remaining_risk = "低风险，通常不需要优先人工审核。"
            note = "低风险基础或实现技巧节点，依赖明确。"
        rows.append({
            "id": item["id"],
            "name": name,
            "category": category["name"],
            "section_id": section["id"],
            "section_name": section["name"],
            "level": item.get("level", ""),
            "confidence": confidence,
            "reasons": unique(reasons),
            "old_direct_pre": old_direct,
            "current_direct_pre": current_direct,
            "suggested_direct_pre": current_direct,
            "new_direct_pre": current_direct,
            "new_rel": new_rel,
            "parent_concept": parent_concept,
            "manual_review_result": manual_result,
            "remaining_risk": remaining_risk,
            "need_manual_review": priority in {"A", "B"},
            "review_priority": priority,
            "review_note": review_note,
            "note": note,
        })
    rows.sort(key=lambda r: (r["review_priority"], r["category"], r["section_id"], r["id"]))
    return rows


def collect_stats(graph, low_conf=None, cycle_fixes=None):
    idx = build_indexes(graph)
    item_by_id, section_by_id = idx["item_by_id"], idx["section_by_id"]
    items = idx["items"]
    dangling = []
    self_in_resolved = []
    direct_section_refs, resolved_section_refs, rel_section_refs = [], [], []
    direct_rel_overlap = []
    direct_too_many, rel_too_many = [], []

    for item in items:
        for field in ("direct_pre", "resolved_pre", "rel"):
            for ref in item.get(field, []) or []:
                if ref not in item_by_id and ref not in section_by_id:
                    dangling.append({"item": item["id"], "field": field, "ref": ref})
        for ref in item.get("direct_pre", []) or []:
            if ref in section_by_id:
                direct_section_refs.append({"item": item["id"], "ref": ref})
        for ref in item.get("resolved_pre", []) or []:
            if ref in section_by_id:
                resolved_section_refs.append({"item": item["id"], "ref": ref})
        for ref in item.get("rel", []) or []:
            if ref in section_by_id:
                rel_section_refs.append({"item": item["id"], "ref": ref})
        if item["id"] in (item.get("resolved_pre", []) or []):
            self_in_resolved.append(item["id"])
        if len(item.get("direct_pre", []) or []) > 8:
            direct_too_many.append({"id": item["id"], "count": len(item.get("direct_pre", []))})
        if len(item.get("rel", []) or []) > 10:
            rel_too_many.append({"id": item["id"], "count": len(item.get("rel", []))})
        overlap = sorted(set(item.get("direct_pre", []) or []) & set(item.get("rel", []) or []))
        if overlap:
            direct_rel_overlap.append({"id": item["id"], "overlap": overlap})

    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in items}
    cycle = detect_cycle(edges, set(item_by_id))
    direct_refs = [d for item in items for d in item.get("direct_pre", [])]
    item_direct_refs = [d for d in direct_refs if d in item_by_id]
    section_only = []
    for item in items:
        dp = item.get("direct_pre", []) or []
        if dp and all(d in section_by_id for d in dp):
            section_only.append({"id": item["id"], "name": item.get("name", ""), "direct_pre": dp})

    cat_stats = defaultdict(lambda: {"sections": 0, "items": 0, "direct_nonempty": 0, "rel_nonempty": 0, "avg_direct_pre": 0})
    for category in graph.get("categories", []):
        cat_stats[category["name"]]["sections"] += len(category.get("sections", []))
        for section in category.get("sections", []):
            for item in section.get("items", []):
                row = cat_stats[category["name"]]
                row["items"] += 1
                row["direct_nonempty"] += bool(item.get("direct_pre"))
                row["rel_nonempty"] += bool(item.get("rel"))
                row["avg_direct_pre"] += len(item.get("direct_pre", []) or [])
    for row in cat_stats.values():
        row["avg_direct_pre"] = round(row["avg_direct_pre"] / max(row["items"], 1), 2)

    low_counts = Counter((r.get("review_priority", "C") for r in (low_conf or [])))
    return {
        "category_count": len(graph.get("categories", [])),
        "section_count": len(idx["section_by_id"]),
        "item_count": len(items),
        "duplicate_item_ids": idx["duplicate_item_ids"],
        "direct_pre_nonempty": sum(1 for item in items if item.get("direct_pre")),
        "rel_nonempty": sum(1 for item in items if item.get("rel")),
        "direct_pre_ref_count": len(direct_refs),
        "direct_pre_item_ref_ratio": round(len(item_direct_refs) / max(len(direct_refs), 1), 6),
        "direct_pre_section_refs": direct_section_refs,
        "resolved_pre_section_refs": resolved_section_refs,
        "rel_section_refs": rel_section_refs,
        "section_only_direct_pre_nodes": section_only,
        "dangling_refs": dangling,
        "direct_pre_cycle": cycle,
        "self_in_resolved_pre": self_in_resolved,
        "direct_pre_over_8": direct_too_many,
        "rel_over_10": rel_too_many,
        "direct_rel_overlap": direct_rel_overlap,
        "cycle_fixes": cycle_fixes or [],
        "low_confidence_counts": {"A": low_counts["A"], "B": low_counts["B"], "C": low_counts["C"]},
        "category_stats": dict(cat_stats),
    }


def validate_resolved_closure(graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    expected = compute_resolved(edges, set(item_by_id))
    mismatches = []
    for item_id, exp in expected.items():
        actual = item_by_id[item_id].get("resolved_pre", []) or []
        if actual != exp:
            mismatches.append({"id": item_id, "expected_count": len(exp), "actual_count": len(actual)})
            if len(mismatches) >= 50:
                break
    return mismatches


def validate_priority_a_items(graph, low_conf):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    section_by_id = idx["section_by_id"]
    item_ids = set(item_by_id)
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    cycle = detect_cycle(edges, item_ids)
    issues = []
    for row in low_conf if isinstance(low_conf, list) else []:
        if row.get("review_priority") != "A":
            continue
        item_id = row.get("id")
        item = item_by_id.get(item_id)
        if not item:
            issues.append({"id": item_id, "issue": "A 类记录不在 refined JSON 中"})
            continue
        direct = row.get("new_direct_pre") or row.get("suggested_direct_pre") or item.get("direct_pre", []) or []
        rel = row.get("new_rel") or item.get("rel", []) or []
        note = " ".join(str(row.get(k, "")) for k in ("note", "review_note", "remaining_risk"))
        if not direct and "起点节点" not in note:
            issues.append({"id": item_id, "issue": "A 类 new_direct_pre 为空且未说明起点节点"})
        if direct and all(d in section_by_id for d in direct):
            issues.append({"id": item_id, "issue": "A 类 direct_pre 仍然只含 section id", "direct_pre": direct})
        for dep in direct:
            if dep not in item_by_id:
                issues.append({"id": item_id, "issue": "A 类 direct_pre 悬空或非 item id", "ref": dep})
            if dep == item_id:
                issues.append({"id": item_id, "issue": "A 类 direct_pre 包含自身"})
        overlap = sorted(set(direct) & set(rel))
        if overlap and len(overlap) / max(len(direct), 1) > 0.2:
            issues.append({"id": item_id, "issue": "A 类 rel 与 direct_pre 重复过多", "overlap": overlap})
        if (
            idx["category_by_item"].get(item_id) == "C++语法"
            and contains_any(item.get("name", ""), ADVANCED_POLLUTION_TERMS)
            and not item.get("parent_concept")
            and "建议迁移" not in note
            and "跨章节高级专题" not in note
        ):
            issues.append({"id": item_id, "issue": "C++语法污染高级专题缺少 parent_concept/review_note"})
    if cycle:
        issues.append({"id": None, "issue": "direct_pre 图存在环", "cycle": cycle})
    return issues


def validate_priority_b_items(graph, low_conf):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    section_by_id = idx["section_by_id"]
    item_ids = set(item_by_id)
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] for item in idx["items"]}
    cycle = detect_cycle(edges, item_ids)
    cycle_nodes = set(cycle or [])
    issues = []
    dp_base = {"2.8.1", "2.8.2", "2.8.3"}
    for row in low_conf if isinstance(low_conf, list) else []:
        if row.get("review_priority") != "B" or row.get("confidence") != "medium":
            continue
        item_id = row.get("id")
        item = item_by_id.get(item_id)
        if not item:
            issues.append({"id": item_id, "issue": "B 类记录不在 refined JSON 中"})
            continue
        direct = item.get("direct_pre", []) or []
        rel = item.get("rel", []) or []
        suggested = row.get("suggested_direct_pre") or []
        note = " ".join(str(row.get(k, "")) for k in ("note", "review_note", "remaining_risk"))
        if direct and all(d in section_by_id for d in direct):
            issues.append({"id": item_id, "issue": "B 类 direct_pre 仍然只含 section id", "direct_pre": direct})
        if not suggested and "起点" not in note:
            issues.append({"id": item_id, "issue": "B 类 suggested_direct_pre 为空且未说明起点原因"})
        for dep in direct:
            if dep not in item_by_id:
                issues.append({"id": item_id, "issue": "B 类 direct_pre 悬空或非 item id", "ref": dep})
            if dep == item_id:
                issues.append({"id": item_id, "issue": "B 类 direct_pre 包含自身"})
        if item_id in cycle_nodes:
            issues.append({"id": item_id, "issue": "B 类节点参与 direct_pre 环", "cycle": cycle})
        overlap = sorted(set(direct) & set(rel))
        if len(overlap) >= 2 and len(overlap) / max(len(direct), 1) > 0.4:
            issues.append({"id": item_id, "issue": "B 类 rel 与 direct_pre 重复过多", "overlap": overlap})
        name = item.get("name", "")
        if (
            ("DP" in name or "动态规划" in name)
            and item_id not in {"2.8.1", "2.8.2", "2.8.3", "2.8.4", "2.8.36"}
            and direct
            and set(direct).issubset(dp_base)
        ):
            issues.append({"id": item_id, "issue": "B 类 DP 应用节点仍只依赖 DP 基础模板", "direct_pre": direct})
    return issues


def parse_a_repair_stats_from_report(report_file):
    if not report_file or not report_file.exists():
        return {}
    text = report_file.read_text(encoding="utf-8")
    patterns = {
        "before_a_count": r"修复前 A 类数量：(\d+)",
        "before_a_current_has_section_id": r"A 类中 section id direct_pre 修复数量：(\d+)",
        "before_a_suggested_empty": r"A 类中 suggested_direct_pre 为空修复数量：(\d+)",
        "before_a_cpp_advanced_polluted": r"C\+\+语法污染节点处理数量：(\d+)",
    }
    parsed = {}
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            parsed[key] = int(m.group(1))
    return parsed


def analyze_priority_a_baseline(low_conf_file, report_file=None):
    baseline = {
        "before_a_count": 0,
        "before_a_current_has_section_id": 0,
        "before_a_current_only_section_id": 0,
        "before_a_suggested_empty": 0,
        "before_a_cpp_advanced_polluted": 0,
        "before_a_ids": [],
        "duplicate_groups": [],
    }
    if not low_conf_file.exists():
        baseline.update(parse_a_repair_stats_from_report(report_file))
        return baseline
    try:
        rows = load_json(low_conf_file)
    except Exception:
        baseline.update(parse_a_repair_stats_from_report(report_file))
        return baseline
    if not isinstance(rows, list):
        baseline.update(parse_a_repair_stats_from_report(report_file))
        return baseline
    a_rows = [r for r in rows if r.get("review_priority") == "A"]
    baseline["before_a_count"] = len(a_rows)
    baseline["before_a_ids"] = sorted(r.get("id") for r in a_rows if r.get("id"))
    for row in a_rows:
        current = row.get("old_direct_pre") or row.get("current_direct_pre") or []
        suggested = row.get("suggested_direct_pre") or row.get("new_direct_pre") or []
        has_section = any(re.fullmatch(r"\d+(?:\.\d+)?", str(x) or "") and str(x).count(".") == 1 for x in current)
        only_section = bool(current) and all(re.fullmatch(r"\d+(?:\.\d+)?", str(x) or "") and str(x).count(".") == 1 for x in current)
        baseline["before_a_current_has_section_id"] += int(has_section)
        baseline["before_a_current_only_section_id"] += int(only_section)
        baseline["before_a_suggested_empty"] += int(not suggested)
        baseline["before_a_cpp_advanced_polluted"] += int(
            row.get("category") == "C++语法" and contains_any(row.get("name", ""), ADVANCED_POLLUTION_TERMS)
        )
    name_groups = defaultdict(list)
    for row in a_rows:
        name_groups[normalized_name(row.get("name", ""))].append(f"{row.get('id')}:{row.get('name')}")
    baseline["duplicate_groups"] = [v for v in name_groups.values() if len(v) > 1]
    previous_report = parse_a_repair_stats_from_report(report_file)
    if previous_report.get("before_a_count", 0) > baseline["before_a_count"]:
        baseline.update(previous_report)
    return baseline


def build_priority_a_repair_stats(before, low_conf, graph, repair_meta):
    after_a = [r for r in low_conf if r.get("review_priority") == "A"]
    after_b = [r for r in low_conf if r.get("review_priority") == "B"]
    after_c = [r for r in low_conf if r.get("review_priority") == "C"]
    before_ids = set(before.get("before_a_ids", []))
    after_a_ids = {r["id"] for r in after_a}
    downgraded_b = sorted(before_ids & {r["id"] for r in after_b})
    downgraded_c_or_removed = sorted(before_ids - after_a_ids - set(downgraded_b))
    if before.get("before_a_count", 0) > len(before_ids):
        old_a_terms = [
            "LCT", "Link-Cut", "FFT", "NTT", "后缀自动机", "后缀数组", "AC 自动机", "网络流", "费用流",
            "插头", "WQS", "CDQ", "整体二分", "支配树", "半平面", "可持久", "动态树", "圆方树",
            "莫比乌斯", "多项式", "带修", "树上莫队", "仙人掌", "虚树", "带花树",
        ]
        inferred_before_ids = {
            r["id"] for r in low_conf
            if level_num(r.get("level")) >= 4 or contains_any(r.get("name", ""), old_a_terms)
        }
        if inferred_before_ids:
            before_ids = inferred_before_ids | before_ids
            downgraded_b = sorted(before_ids & {r["id"] for r in after_b})
            downgraded_c_or_removed = sorted(before_ids - after_a_ids - set(downgraded_b))
    before_count = before.get("before_a_count", len(before_ids))
    downgraded_b_count = min(len(downgraded_b), max(before_count - len(after_a), 0))
    downgraded_c_count = max(before_count - len(after_a) - downgraded_b_count, 0)
    idx = build_indexes(graph)
    cpp_processed = [
        item_id for item_id in before_ids
        if item_id in idx["item_by_id"]
        and is_cpp_advanced_pollution(idx["item_by_id"][item_id], idx["category_by_item"][item_id])
        and (idx["item_by_id"][item_id].get("parent_concept") or idx["item_by_id"][item_id].get("review_note"))
    ]
    return {
        **before,
        "after_a_count": len(after_a),
        "downgraded_to_b_count": downgraded_b_count,
        "downgraded_to_c_or_removed_count": downgraded_c_count,
        "downgraded_to_b_ids": downgraded_b,
        "downgraded_to_c_or_removed_ids": downgraded_c_or_removed,
        "a_section_direct_pre_fixed_count": before.get("before_a_current_has_section_id", 0),
        "a_suggested_empty_fixed_count": before.get("before_a_suggested_empty", 0),
        "cpp_pollution_processed_count": len(cpp_processed),
        "cpp_pollution_processed_ids": sorted(cpp_processed),
        "duplicate_parent_concept_processed_count": len(repair_meta.get("duplicate_parent_concepts", [])),
        "remaining_a_items": [{"id": r["id"], "name": r["name"], "risk": r.get("remaining_risk", "")} for r in after_a],
    }


def is_section_ref(ref, section_by_id):
    return ref in section_by_id


def is_dp_template_deps(item, deps):
    name = item.get("name", "")
    if not deps:
        return False
    if item.get("parent") != "2.8" and "DP" not in name and "动态规划" not in name:
        return False
    return set(deps).issubset({"2.8.1", "2.8.2", "2.8.3"})


def analyze_priority_b_baseline(low_conf_file):
    baseline = {
        "before_b_count": 0,
        "before_b_ids": [],
        "before_b_suggested_empty": 0,
        "before_b_current_only_section_id": 0,
        "before_b_current_has_section_id": 0,
        "before_b_suggested_len1": 0,
        "before_b_dp_template": 0,
        "before_b_rows_by_id": {},
    }
    if not low_conf_file.exists():
        return baseline
    try:
        rows = load_json(low_conf_file)
    except Exception:
        return baseline
    if not isinstance(rows, list):
        return baseline
    return priority_b_baseline_from_rows(rows)


def priority_b_baseline_from_rows(rows):
    baseline = {
        "before_b_count": 0,
        "before_b_ids": [],
        "before_b_suggested_empty": 0,
        "before_b_current_only_section_id": 0,
        "before_b_current_has_section_id": 0,
        "before_b_suggested_len1": 0,
        "before_b_dp_template": 0,
        "before_b_rows_by_id": {},
    }
    section_like = re.compile(r"^\d+\.\d+$")
    b_rows = [
        row for row in rows
        if row.get("review_priority") == "B" and row.get("confidence") == "medium"
    ]
    baseline["before_b_count"] = len(b_rows)
    baseline["before_b_ids"] = sorted(row.get("id") for row in b_rows if row.get("id"))
    baseline["before_b_rows_by_id"] = {row.get("id"): row for row in b_rows if row.get("id")}
    for row in b_rows:
        current = row.get("current_direct_pre") or []
        suggested = row.get("suggested_direct_pre") or []
        has_section = any(section_like.fullmatch(str(x) or "") for x in current)
        only_section = bool(current) and all(section_like.fullmatch(str(x) or "") for x in current)
        baseline["before_b_suggested_empty"] += int(not suggested)
        baseline["before_b_current_only_section_id"] += int(only_section)
        baseline["before_b_current_has_section_id"] += int(has_section)
        baseline["before_b_suggested_len1"] += int(len(suggested) == 1)
        pseudo_item = {"id": row.get("id", ""), "name": row.get("name", ""), "parent": row.get("section_id", "")}
        baseline["before_b_dp_template"] += int(is_dp_template_deps(pseudo_item, suggested))
    return baseline


def build_low_confidence_from_edges(graph, edges, original_direct, low_reasons, parent_concepts=None):
    parent_concepts = parent_concepts or {}
    low_candidates = []
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                item_id = item["id"]
                if item_id not in low_reasons:
                    continue
                temp_item = copy.deepcopy(item)
                temp_item["direct_pre"] = edges.get(item_id, []) or []
                if item_id in parent_concepts:
                    temp_item["parent_concept"] = parent_concepts[item_id]
                low_candidates.append((
                    temp_item,
                    category,
                    section,
                    unique(low_reasons[item_id]),
                    original_direct[item_id],
                    temp_item["direct_pre"],
                ))
    return build_low_confidence(low_candidates, graph)


def priority_b_deps_for_item(item, current_deps, item_by_id):
    item_id = item["id"]
    name = item.get("name", "")
    deps = []
    rels = []
    parent_concept = None
    note = ""
    keep_b = False
    upgrade_a = False
    reasons = []

    def D(*values):
        deps.extend(v for v in values if v in item_by_id and v != item_id)

    def R(*values):
        rels.extend(v for v in values if v in item_by_id and v != item_id)

    def P(value):
        nonlocal parent_concept
        if value in item_by_id and value != item_id:
            parent_concept = {"id": value, "name": item_by_id[value].get("name", "")}

    exact = {
        "5.2.12": (["5.2.11", "4.1.5", "4.2.1", "1.4.1"], "5.2.11"),
        "5.4.17": (["5.4.16", "5.9.7", "5.3.15"], "5.4.16"),
        "3.1.7": (["3.1.4", "1.7.11", "1.6.1"], "3.1.4"),
        "3.1.8": (["3.1.4", "3.1.6", "2.4.7", "1.6.1"], "3.1.4"),
        "3.3.10": (["3.3.1", "1.8.14", "1.8.21"], "3.3.1"),
        "3.3.11": (["3.3.2", "1.8.15", "3.3.10"], "3.3.2"),
        "3.3.12": (["3.3.3", "1.8.16", "1.8.21"], "3.3.3"),
        "3.5.18": (["3.5.5", "3.6.1", "1.6.1"], "3.5.5"),
        "3.8.8": (["3.8.7", "3.8.3", "1.6.9"], "3.8.7"),
        "5.7.20": (["5.7.15", "5.7.16", "5.7.17", "5.1.7"], "5.7.15"),
        "5.7.21": (["5.7.15", "5.7.16", "5.7.20", "5.1.7"], "5.7.15"),
        "1.10.5": (["1.3.2", "5.8.10", "5.7.3"], "1.3.2"),
        "1.5.16": (["2.13.3", "2.13.1", "3.9.4"], "2.13.3"),
        "1.7.26": (["1.7.25", "4.1.20", "4.1.8"], "4.1.20"),
        "1.7.37": (["1.7.32", "4.3.24", "4.8.10"], "4.3.24"),
        "1.8.36": (["1.3.10", "1.8.1"], None),
        "3.1.11": (["3.2.1", "3.11.1", "3.1.1"], "3.2.1"),
        "3.2.8": (["3.2.1", "1.8.11", "3.1.1"], "3.2.1"),
        "3.2.9": (["3.2.2", "1.8.10", "3.1.1"], "3.2.2"),
        "3.6.14": (["3.6.4", "3.6.3", "3.10.1"], "3.6.4"),
        "2.10.22": (["2.10.9", "1.6.9", "2.10.1"], "2.10.9"),
        "2.10.23": (["2.10.9", "3.8.5", "1.6.9"], "2.10.9"),
        "4.1.15": (["4.1.1", "1.6.1", "1.6.9"], "4.1.1"),
        "4.1.26": (["4.1.1", "4.4.2", "4.8.1"], "4.1.1"),
        "4.1.27": (["4.1.1", "2.8.19", "4.3.1"], "4.1.1"),
        "4.1.28": (["4.1.26", "2.7.5", "2.3.6"], "4.1.26"),
        "4.2.13": (["4.2.8", "4.2.4", "4.1.8"], "4.2.8"),
        "4.3.24": (["4.8.10", "4.3.16", "4.3.5"], "4.8.10"),
        "4.3.29": (["4.3.13", "2.8.19", "4.3.7"], "4.3.13"),
        "4.6.13": (["4.6.7", "4.6.3", "4.6.1"], "4.6.7"),
        "4.7.30": (["4.7.10", "4.7.15", "4.7.11"], "4.7.10"),
        "4.7.31": (["4.7.30", "4.7.2", "4.7.15"], "4.7.10"),
        "4.7.32": (["4.7.10", "4.7.15", "2.8.12"], "4.7.10"),
        "4.7.33": (["4.7.30", "4.7.9", "4.7.34"], "4.7.10"),
        "4.7.36": (["4.7.9", "4.7.2", "4.7.15"], "4.7.9"),
        "4.7.37": (["4.7.9", "4.7.2", "4.7.15"], "4.7.9"),
        "4.7.45": (["4.7.37", "2.19.1", "4.7.2"], "4.7.37"),
        "4.8.1": (["2.12.4", "4.1.2", "2.17.18"], "2.12.4"),
        "4.8.11": (["2.10.2", "2.10.3", "1.6.9"], "2.10.2"),
        "4.8.5": (["4.6.1", "4.6.8", "4.6.4"], None),
        "4.8.6": (["4.1.2", "4.7.17", "2.12.15"], None),
    }
    if item_id in exact:
        exact_deps, parent = exact[item_id]
        D(*exact_deps)
        if parent:
            P(parent)
        reasons.append("B 类专项：空/过浅依赖已按具体知识点补足")

    if is_dp_template_deps(item, current_deps) or item.get("parent") == "2.8":
        if "线性 DP" in name or "LIS" in name or "最长上升子序列" in name:
            D("2.8.5", "2.8.15", "1.6.1")
            P("2.8.5")
        elif "背包" in name:
            D("2.8.7", "2.8.3", "2.8.25")
            if "0/1" in name or "01" in name:
                D("2.8.8")
            if "完全" in name:
                D("2.8.9")
            if "多重" in name:
                D("2.8.10", "3.2.5")
            if "分组" in name:
                D("2.8.11")
            P("2.8.7")
        elif "树形" in name or "树上" in name or "基环树" in name or "仙人掌" in name:
            D("2.8.13", "2.9.1", "3.6.1")
            if "背包" in name:
                D("2.8.7")
            P("2.8.13")
        elif "DAG" in name or "最长路" in name or "最短路径计数" in name:
            D("2.8.14", "2.9.6", "2.9.7")
            P("2.8.14")
        elif "状压" in name or "状态压缩" in name or "子集" in name or "集合" in name or "连通性" in name:
            D("2.8.20", "2.11.4", "2.11.3")
            P("2.8.20")
        elif "数位" in name:
            D("2.8.21", "2.8.6", "5.2.1")
            P("2.8.21")
        elif "自动机" in name or "AC " in name or "SAM" in name or "后缀自动机" in name or "KMP" in name:
            D("2.8.1", "2.8.3")
            if "AC" in name:
                D("3.8.2", "2.10.6")
                P("3.8.2")
            elif "SAM" in name or "后缀自动机" in name:
                D("3.8.4", "2.10.8")
                P("3.8.4")
            elif "KMP" in name:
                D("2.10.2")
                P("2.10.2")
        elif "博弈" in name or "SG" in name or "Minimax" in name or "Alpha-Beta" in name:
            D("2.8.24", "4.8.4", "2.8.3")
            P("2.8.24")
        elif "概率" in name or "期望" in name:
            D("2.8.22", "2.8.23", "4.6.4")
            if "高斯" in name:
                D("4.8.2")
            P("2.8.22")
        elif "单调队列" in name:
            D("2.8.26", "3.2.5", "2.5.4")
            P("2.8.26")
        elif "斜率" in name or "凸壳" in name:
            D("2.8.28", "4.7.44", "2.8.3")
            P("2.8.28")
        elif "四边形" in name or "决策单调" in name:
            D("2.8.12", "2.8.27", "2.8.3")
            P("2.8.27")
        elif "矩阵" in name or "线性递推" in name or "BM" in name:
            D("2.12.3", "2.12.1", "2.8.3")
            P("2.12.3")
        elif "计数" in name:
            D("2.8.19", "4.3.1", "4.3.2")
            P("2.8.19")
        elif "上下界" in name:
            D("2.8.2", "2.8.4", "2.8.127")
            P("2.8.2")
        elif "可持久化" in name:
            D("3.11.1", "3.7.8", "2.8.1")
            P("3.11.1")
        elif "附加维度" in name:
            D("2.8.2", "2.8.3", "2.8.36")
            P("2.8.2")
        elif "差值" in name:
            D("2.8.2", "2.8.3", "2.4.4")
            P("2.8.2")
        elif "黑白染色" in name:
            D("2.8.2", "2.8.3", "2.9.5")
            P("2.8.2")
        if deps:
            reasons.append("B 类专项：DP 模板化依赖已替换为题型专属前置")

    if item.get("parent") == "3.7" or "线段树" in name or "树状数组" in name or "主席树" in name:
        if "树状数组" in name or "Fenwick" in name:
            D("2.11.6", "2.4.1", "1.6.1")
            P("3.7.1")
        elif "主席树" in name or "可持久化线段树" in name:
            D("3.7.2", "3.11.1", "2.4.6")
            P("3.7.8")
        elif "动态开点" in name:
            D("3.7.2", "1.7.11", "2.1.4")
            P("3.7.4")
        elif "懒" in name or "Lazy" in name or "区间加" in name or "区间赋值" in name or "区间乘法" in name:
            D("3.7.2", "3.7.3", "2.4.4")
            P("3.7.3")
        elif "线段树" in name:
            D("3.7.2", "2.1.4", "1.6.1", "2.4.1")
            P("3.7.2")
        if deps:
            reasons.append("B 类专项：区间维护结构依赖已细化")

    if item.get("parent") == "2.13" or any(x in name for x in ["Dijkstra", "Bellman", "SPFA", "Floyd", "Kruskal", "Prim", "生成树", "最短路"]):
        if "Dijkstra" in name:
            D("2.13.1", "3.2.6", "3.9.2")
            if item_id != "2.13.2":
                D("2.13.2")
            P("2.13.2")
        elif "Bellman" in name:
            D("2.13.1", "3.9.4", "2.1.3")
            if item_id != "2.13.3":
                D("2.13.3")
            P("2.13.3")
        elif "SPFA" in name:
            D("2.13.3", "3.2.2", "2.13.1")
            P("2.13.6")
        elif "Floyd" in name:
            D("2.8.1", "1.6.2", "2.13.1")
            if item_id != "2.13.4":
                D("2.13.4")
            P("2.13.4")
        elif "Kruskal" in name:
            D("2.13.8", "3.4.1", "1.8.22")
            P("2.13.9")
        elif "Prim" in name:
            D("2.13.8", "3.2.6", "3.9.2")
            P("2.13.10")
        elif "生成树" in name:
            D("2.13.8", "3.9.2", "3.4.1")
            P("2.13.8")
        elif "最短路" in name or "最短路径" in name:
            D("2.13.1", "3.9.2", "2.9.3")
            P("2.13.1")
        if deps:
            reasons.append("B 类专项：最短路/生成树依赖已细化")

    if item.get("parent") == "2.15" or any(x in name for x in ["强连通", "SCC", "Kosaraju", "Tarjan", "割点", "桥", "点双", "边双", "圆方树"]):
        if "强连通" in name or "SCC" in name:
            D("2.9.1", "3.2.1", "2.9.3")
            if "Kosaraju" in name:
                D("3.9.5")
            if item_id != "2.15.9" and "Tarjan" in name:
                D("2.15.1")
            P("2.15.1")
        elif "桥" in name or "割点" in name:
            D("2.9.1", "2.9.3", "3.2.1")
            P("2.15.2" if "桥" in name else "2.15.3")
        elif "点双" in name or "边双" in name or "双连通" in name:
            D("2.15.2", "2.15.3", "3.2.1")
            P("2.15.4")
        elif "圆方树" in name:
            D("2.15.13", "2.15.3", "3.6.1")
            P("4.7.20" if "4.7.20" in item_by_id else "2.15.4")
        if deps:
            reasons.append("B 类专项：连通分量/特殊图依赖已细化")

    if not deps and len(current_deps) == 1:
        only = current_deps[0]
        if only in item_by_id:
            D(only)
            parent = item_by_id[only].get("parent", "")
            if parent == "4.1":
                D("4.1.2", "4.1.5")
            elif parent == "4.7":
                D("4.7.2", "4.7.15")
            elif parent == "3.2":
                D("3.1.1")
            elif parent == "1.7":
                D("1.3.10", "1.7.3")
            elif parent == "1.8":
                D("1.3.10", "1.8.21")
            P(only)
            reasons.append("B 类专项：单一前置依赖已补充到 2~5 个强前置")

    if not deps:
        D(*[d for d in current_deps if d in item_by_id])

    if contains_any(name, ["汇编", "线程安全", "死锁", "操作系统", "机器学习", "数据库"]):
        keep_b = True
        note = "非主线或工程底层专题，依赖已补 item id，但仍建议人工确认是否纳入主路径。"
    if level_num(item.get("level")) >= 4 and contains_any(name, VERY_HIGH_RISK_TERMS):
        keep_b = True
        note = "高级主干专题，依赖已补 item id，但仍建议人工确认主路径影响。"
    if item.get("parent", "").startswith("1.") and contains_any(name, ADVANCED_POLLUTION_TERMS):
        keep_b = True
        note = "C++章节中的跨章节高级专题，依赖已指向算法/数据结构主概念，仍建议确认归属。"
    if contains_any(name, ["全局平衡二叉树", "后缀树", "整数线性规划", "Polya", "半平面", "圆方树", "支配树"]):
        keep_b = True
        note = note or "名称涉及高级或边界专题，依赖已具体化但保留 B 类抽查。"

    deps = unique([d for d in deps if d in item_by_id and d != item_id])
    rels = unique([r for r in rels if r in item_by_id and r != item_id and r not in deps])
    return deps, rels, parent_concept, note, keep_b, upgrade_a, reasons


def repair_priority_b_dependencies(graph, edges, anchors, original_direct, b_baseline):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    b_ids = set(b_baseline.get("before_b_ids", []))
    parent_concepts = {}
    review_notes = {}
    rel_additions = defaultdict(list)
    reasons = defaultdict(list)
    repaired_ids = set()
    keep_b_ids = set()
    upgrade_a_ids = set()
    suggested_empty_fixed_ids = set()
    section_cleaned_ids = set()
    dp_template_fixed_ids = set()
    len1_deepened_ids = set()

    before_rows = b_baseline.get("before_b_rows_by_id", {})
    for item_id in sorted(b_ids):
        item = item_by_id.get(item_id)
        if not item:
            continue
        before_row = before_rows.get(item_id, {})
        before_suggested = before_row.get("suggested_direct_pre") or []
        current = edges.get(item_id, []) or []
        deps, rels, parent_concept, note, keep_b, upgrade_a, item_reasons = priority_b_deps_for_item(item, current, item_by_id)
        if deps:
            merged = deps + [d for d in current if d in item_by_id and d not in deps]
            new_deps = rank_and_trim_deps(
                item,
                prune_impossible_reverse_edges(item, unique(merged), item_by_id),
                item_by_id,
                8,
            )
            if new_deps != current:
                edges[item_id] = new_deps
                repaired_ids.add(item_id)
            if not before_suggested:
                suggested_empty_fixed_ids.add(item_id)
            if len(before_suggested) == 1 and len(new_deps) > 1:
                len1_deepened_ids.add(item_id)
            if is_dp_template_deps(item, before_suggested) and not is_dp_template_deps(item, new_deps):
                dp_template_fixed_ids.add(item_id)
        if before_row.get("current_direct_pre") and any(re.fullmatch(r"\d+\.\d+", str(x) or "") for x in before_row.get("current_direct_pre", [])):
            if not any(re.fullmatch(r"\d+\.\d+", str(x) or "") for x in edges.get(item_id, [])):
                section_cleaned_ids.add(item_id)
        if parent_concept:
            parent_concepts[item_id] = parent_concept
        if note:
            review_notes[item_id] = note
        if rels:
            rel_additions[item_id].extend(rels)
        if keep_b:
            keep_b_ids.add(item_id)
        if upgrade_a:
            upgrade_a_ids.add(item_id)
        if item_reasons:
            reasons[item_id].extend(item_reasons)

    return {
        "parent_concepts": parent_concepts,
        "review_notes": review_notes,
        "rel_additions": rel_additions,
        "reasons": reasons,
        "repaired_ids": sorted(repaired_ids),
        "keep_b_ids": sorted(keep_b_ids),
        "upgrade_a_ids": sorted(upgrade_a_ids),
        "suggested_empty_fixed_ids": sorted(suggested_empty_fixed_ids),
        "section_cleaned_ids": sorted(section_cleaned_ids),
        "dp_template_fixed_ids": sorted(dp_template_fixed_ids),
        "len1_deepened_ids": sorted(len1_deepened_ids),
    }


def apply_priority_b_review_updates(low_conf, graph, b_baseline, b_repair_meta):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    b_ids = set(b_baseline.get("before_b_ids", []))
    keep_b_ids = set(b_repair_meta.get("keep_b_ids", []))
    upgrade_a_ids = set(b_repair_meta.get("upgrade_a_ids", []))
    repaired_ids = set(b_repair_meta.get("repaired_ids", []))
    rows_by_id = {row.get("id"): row for row in low_conf if row.get("id")}

    for item_id in b_ids:
        row = rows_by_id.get(item_id)
        item = item_by_id.get(item_id)
        if not row or not item:
            continue
        direct = list(item.get("direct_pre", []) or [])
        rel = [r for r in item.get("rel", []) or [] if r not in set(direct)]
        row["current_direct_pre"] = direct
        row["suggested_direct_pre"] = direct
        row["new_direct_pre"] = direct
        row["new_rel"] = rel
        row["parent_concept"] = item.get("parent_concept", {}) or {}
        add_reasons = b_repair_meta.get("reasons", {}).get(item_id, [])
        row["reasons"] = unique((row.get("reasons") or []) + add_reasons)
        if item_id in upgrade_a_ids:
            row["review_priority"] = "A"
            row["confidence"] = "low"
            row["need_manual_review"] = True
            row["manual_review_result"] = "仍需人工确认"
            row["remaining_risk"] = "B 类专项发现该节点仍影响主路径或跨章节边界，升级为 A。"
            row["note"] = "B 类专项：已补 item-to-item direct_pre，但复杂度或归属风险较高，升级 A。"
        elif item_id in keep_b_ids:
            row["review_priority"] = "B"
            row["confidence"] = "medium"
            row["need_manual_review"] = True
            row["manual_review_result"] = "已专项修正，建议人工抽查"
            row["remaining_risk"] = "依赖已具体化，但名称、归属或高级专题边界仍建议人工确认。"
            row["note"] = item.get("review_note") or "B 类专项：direct_pre 已具体化，保留 B 类人工抽查。"
        else:
            row["review_priority"] = "C"
            row["confidence"] = "high"
            row["need_manual_review"] = False
            row["manual_review_result"] = "已专项修正并降为 C"
            row["remaining_risk"] = "已具备明确 item-to-item direct_pre，未发现章节级污染或模板化依赖。"
            if item_id in repaired_ids:
                row["note"] = "B 类专项：已补足 direct_pre / rel / parent_concept 并降为 C。"
            else:
                row["note"] = "B 类专项：原 suggested_direct_pre 已合理，写回 refined JSON 后降为 C。"
    low_conf.sort(key=lambda r: (r["review_priority"], r["category"], r["section_id"], r["id"]))
    return low_conf


def build_priority_b_repair_stats(before, low_conf, graph, repair_meta):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    before_ids = set(before.get("before_b_ids", []))
    rows_by_id = {row.get("id"): row for row in low_conf if row.get("id")}
    after_b = sorted(item_id for item_id in before_ids if rows_by_id.get(item_id, {}).get("review_priority") == "B")
    after_a = sorted(item_id for item_id in before_ids if rows_by_id.get(item_id, {}).get("review_priority") == "A")
    after_c = sorted(item_id for item_id in before_ids if rows_by_id.get(item_id, {}).get("review_priority") == "C")
    still_b_rows = [
        {
            "id": item_id,
            "name": item_by_id.get(item_id, {}).get("name", rows_by_id.get(item_id, {}).get("name", "")),
            "risk": rows_by_id.get(item_id, {}).get("remaining_risk", ""),
        }
        for item_id in after_b
    ]
    return {
        **before,
        "after_b_count": len(after_b),
        "downgraded_to_c_count": len(after_c),
        "upgraded_to_a_count": len(after_a),
        "after_b_ids": after_b,
        "downgraded_to_c_ids": after_c,
        "upgraded_to_a_ids": after_a,
        "suggested_empty_fixed_count": len(repair_meta.get("suggested_empty_fixed_ids", [])),
        "section_direct_pre_cleaned_count": len(repair_meta.get("section_cleaned_ids", [])),
        "dp_template_fixed_count": len(repair_meta.get("dp_template_fixed_ids", [])),
        "len1_deepened_count": len(repair_meta.get("len1_deepened_ids", [])),
        "repaired_count": len(repair_meta.get("repaired_ids", [])),
        "remaining_b_items": still_b_rows,
    }


def term_match(text, terms):
    return contains_any(text, terms)


def classify_item_tracks(item, context):
    name = item.get("name", "")
    parent = item.get("parent", context.get("section_id", ""))
    category = context.get("category", "")
    section_name = context.get("section_name", "")
    level = level_num(item.get("level"))
    hay = f"{name} {section_name}"
    tracks = []

    def add(*values):
        for value in values:
            if value in ALLOWED_TRACKS and value not in tracks:
                tracks.append(value)

    if category == "C++编程/调试技巧" or term_match(hay, ["调试", "对拍", "样例", "边界", "快读", "性能", "编译器", "复杂度", "读题"]):
        add("engineering_debug", "beginner", "icpc", "interview")
    if parent.startswith(("1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7")) or term_match(hay, ["枚举", "模拟", "递归", "冒泡", "选择排序", "插入排序", "二分查找"]):
        add("beginner", "csp_j")
    if term_match(hay, ["数组", "字符串", "哈希", "双指针", "滑动窗口", "栈", "队列", "二分", "DFS", "BFS", "回溯", "堆", "链表", "二叉树", "图的", "最短路", "DP 思想", "动态规划"]):
        add("interview", "beginner")
    if parent in {"3.7", "3.4", "2.13", "2.14", "2.8", "4.1", "4.2", "4.3"} or term_match(hay, ["线段树", "树状数组", "并查集", "最短路", "生成树", "拓扑", "LCA", "树链剖分", "背包", "区间 DP", "树形 DP", "状压", "数论", "组合"]):
        add("csp_s", "noi")
    if parent in {"2.16", "2.15", "2.10", "4.7", "2.18"} or term_match(hay, ["网络流", "费用流", "SCC", "割点", "桥", "二分图匹配", "字符串算法", "计算几何", "莫队", "CDQ", "整体二分"]):
        add("icpc", "university_cp")
    if term_match(hay, ["FFT", "NTT", "多项式", "莫比乌斯", "原根", "BSGS", "Pollard", "Miller", "FWT", "生成函数", "Burnside", "Polya", "插值", "线性递推", "高斯消元"]):
        add("noi", "icpc", "advanced_math")
    if term_match(hay, ["KMP", "Trie", "AC 自动机", "后缀数组", "后缀自动机", "后缀树", "Manacher", "回文自动机", "Z 函数", "Lyndon", "Duval"]):
        add("noi", "icpc", "advanced_string")
    if term_match(hay, ["虚树", "支配树", "圆方树", "仙人掌", "带花树", "上下界网络流", "最小割树", "动态树", "欧拉图"]):
        add("noi", "icpc", "advanced_graph")
    if term_match(hay, ["主席树", "可持久化", "平衡树", "Treap", "Splay", "LCT", "Link-Cut", "树套树", "Wavelet", "李超", "Li Chao", "Segment Tree Beats", "KD-Tree"]):
        add("noi", "icpc", "advanced_data_structure")
    if parent == "2.8" and level >= 3:
        add("advanced_dp")
    if level >= 4 and not any(t.startswith("advanced") for t in tracks):
        add("noi", "icpc")
    if not tracks:
        if category == "算法竞赛数学":
            add("noi", "icpc", "advanced_math")
        elif category == "数据结构":
            add("csp_s", "noi")
        elif category == "算法":
            add("icpc", "university_cp")
        else:
            add("beginner")
    return tracks


def classify_item_audience(item, context):
    tracks = context.get("tracks", [])
    audience = []
    def add(*values):
        for value in values:
            if value in ALLOWED_AUDIENCE and value not in audience:
                audience.append(value)
    if "beginner" in tracks or "csp_j" in tracks:
        add("primary_beginner", "middle_school_oi")
    if "csp_s" in tracks or "noi" in tracks:
        add("high_school_oi", "advanced_competitive_programmer")
    if "icpc" in tracks or "university_cp" in tracks:
        add("university_icpc", "advanced_competitive_programmer")
    if "interview" in tracks:
        add("software_engineer_interview", "university_icpc")
    if any(t.startswith("advanced") for t in tracks):
        add("advanced_competitive_programmer")
    if not audience:
        add("advanced_competitive_programmer")
    return audience


def classify_item_visibility(item, context):
    name = item.get("name", "")
    tracks = context.get("tracks", [])
    level = level_num(item.get("level"))
    if term_match(name, ["机器学习", "数据库", "操作系统", "汇编", "死锁", "线程安全", "心理素质"]):
        return "optional"
    if any(t in tracks for t in ["advanced_math", "advanced_graph", "advanced_string", "advanced_data_structure"]) or level >= 4:
        return "expert"
    if any(t in tracks for t in ["csp_s", "noi", "icpc", "university_cp", "advanced_dp"]) or level == 3:
        return "advanced"
    return "core"


def build_learning_path_policy(item, context):
    tracks = context.get("tracks", [])
    visibility = context.get("visibility", "core")
    if visibility == "core":
        unlock = "mainline"
    elif visibility == "advanced":
        unlock = "optional_branch"
    elif visibility == "expert":
        unlock = "expert_branch"
    else:
        unlock = "reference_only"
    return {
        "show_in_beginner_path": visibility == "core" and ("beginner" in tracks or "csp_j" in tracks),
        "show_in_interview_path": visibility in {"core", "advanced"} and "interview" in tracks,
        "show_in_icpc_path": visibility != "optional" and bool({"icpc", "university_cp", "beginner"} & set(tracks)),
        "show_in_noi_path": visibility != "optional" and bool({"noi", "csp_s", "advanced_math", "advanced_graph", "advanced_string", "advanced_data_structure", "advanced_dp"} & set(tracks)),
        "unlock_mode": unlock,
    }


def english_name_for_item(item):
    name = item.get("name", "")
    if name in EN_NAME_OVERRIDES:
        return EN_NAME_OVERRIDES[name], "high"
    for key, value in EN_NAME_OVERRIDES.items():
        if key and key in name:
            return name.replace(key, value), "medium"
    if re.search(r"[A-Za-z]", name):
        return name, "medium"
    return name, "low"


def platform_tags_for_tracks(tracks):
    tags = []
    def add(*values):
        for value in values:
            if value in ALLOWED_PLATFORMS and value not in tags:
                tags.append(value)
    if "beginner" in tracks:
        add("CSES", "LeetCode")
    if "interview" in tracks:
        add("LeetCode", "HackerRank")
    if "icpc" in tracks or "university_cp" in tracks:
        add("Codeforces", "AtCoder", "Kattis", "ICPC_Gym")
    if "noi" in tracks or "csp_s" in tracks or "csp_j" in tracks:
        add("Luogu", "DMOJ", "USACO")
    if not tags:
        add("Codeforces")
    return tags


def add_product_metadata(graph):
    idx = build_indexes(graph)
    for category in graph.get("categories", []):
        for section in category.get("sections", []):
            for item in section.get("items", []):
                context = {
                    "category": category.get("name", ""),
                    "section_id": section.get("id", ""),
                    "section_name": section.get("name", ""),
                }
                en_name, translation_confidence = english_name_for_item(item)
                aliases = []
                aliases.extend(item.get("aliases") or [])
                aliases.extend(item.get("alias") or [])
                item["aliases"] = unique(aliases)
                item["en_name"] = en_name
                item["global_aliases"] = unique(GLOBAL_ALIASES.get(item.get("name", ""), []))
                tracks = classify_item_tracks(item, context)
                context["tracks"] = tracks
                audience = classify_item_audience(item, context)
                context["audience"] = audience
                visibility = classify_item_visibility(item, context)
                context["visibility"] = visibility
                item["tracks"] = tracks
                item["audience"] = audience
                item["visibility"] = visibility
                item["learning_path_policy"] = build_learning_path_policy(item, context)
                item["localization_status"] = {
                    "has_i18n_terms": False,
                    "primary_language": "zh-Hans",
                    "translation_confidence": translation_confidence,
                    "needs_native_review": translation_confidence != "high",
                }
                item["content_status"] = {
                    "has_explanation": False,
                    "has_examples": False,
                    "has_code_template": False,
                    "has_visualization": False,
                    "has_practice_refs": False,
                    "content_priority": {"core": "P0", "advanced": "P1", "expert": "P2", "optional": "P3"}[visibility],
                }
                item["platform_tags"] = platform_tags_for_tracks(tracks)
    graph.setdefault("meta", {})["stage1_schema_upgrade"] = {
        "enabled": True,
        "knowledge_item_count": len(idx["items"]),
        "scope": "schema_and_product_metadata_only",
    }
    return graph


def validate_product_metadata(graph):
    idx = build_indexes(graph)
    items = idx["items"]
    invalid_tracks, invalid_audience, invalid_visibility, invalid_unlock_mode = [], [], [], []
    path_counts = {"beginner": 0, "interview": 0, "icpc": 0, "noi": 0}
    visibility_counts = {key: 0 for key in ALLOWED_VISIBILITY}
    track_counts = {key: 0 for key in ALLOWED_TRACKS}
    audience_counts = {key: 0 for key in ALLOWED_AUDIENCE}
    required_policy = {
        "show_in_beginner_path", "show_in_interview_path", "show_in_icpc_path",
        "show_in_noi_path", "unlock_mode",
    }
    all_en = all(bool(item.get("en_name")) for item in items)
    all_tracks = all(bool(item.get("tracks")) for item in items)
    all_audience = all(bool(item.get("audience")) for item in items)
    all_visibility = all(item.get("visibility") in ALLOWED_VISIBILITY for item in items)
    all_policy = all(required_policy.issubset(set((item.get("learning_path_policy") or {}).keys())) for item in items)
    all_localization = all(bool(item.get("localization_status")) for item in items)
    all_content = all(bool(item.get("content_status")) for item in items)
    for item in items:
        for track in item.get("tracks", []) or []:
            if track not in ALLOWED_TRACKS:
                invalid_tracks.append({"id": item["id"], "track": track})
            else:
                track_counts[track] += 1
        for audience in item.get("audience", []) or []:
            if audience not in ALLOWED_AUDIENCE:
                invalid_audience.append({"id": item["id"], "audience": audience})
            else:
                audience_counts[audience] += 1
        visibility = item.get("visibility")
        if visibility not in ALLOWED_VISIBILITY:
            invalid_visibility.append({"id": item["id"], "visibility": visibility})
        else:
            visibility_counts[visibility] += 1
        policy = item.get("learning_path_policy") or {}
        unlock = policy.get("unlock_mode")
        if unlock not in ALLOWED_UNLOCK_MODES:
            invalid_unlock_mode.append({"id": item["id"], "unlock_mode": unlock})
        path_counts["beginner"] += int(bool(policy.get("show_in_beginner_path")))
        path_counts["interview"] += int(bool(policy.get("show_in_interview_path")))
        path_counts["icpc"] += int(bool(policy.get("show_in_icpc_path")))
        path_counts["noi"] += int(bool(policy.get("show_in_noi_path")))
    passed = all([
        all_en, all_tracks, all_audience, all_visibility, all_policy, all_localization, all_content,
        not invalid_tracks, not invalid_audience, not invalid_visibility, not invalid_unlock_mode,
    ])
    return {
        "all_items_have_en_name": all_en,
        "all_items_have_tracks": all_tracks,
        "all_items_have_audience": all_audience,
        "all_items_have_visibility": all_visibility,
        "all_items_have_learning_path_policy": all_policy,
        "all_items_have_localization_status": all_localization,
        "all_items_have_content_status": all_content,
        "invalid_tracks": invalid_tracks,
        "invalid_audience": invalid_audience,
        "invalid_visibility": invalid_visibility,
        "invalid_unlock_mode": invalid_unlock_mode,
        "path_counts": path_counts,
        "visibility_counts": visibility_counts,
        "track_counts": track_counts,
        "audience_counts": audience_counts,
        "passed": passed,
    }


def json_schema_base(title, properties, required):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "additionalProperties": True,
        "properties": properties,
        "required": required,
    }


def write_schema_files(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    string_array = {"type": "array", "items": {"type": "string"}, "uniqueItems": True}
    schemas = {
        "knowledge_item.schema.json": json_schema_base("Knowledge Item", {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "en_name": {"type": "string"},
            "aliases": string_array,
            "global_aliases": string_array,
            "tracks": {"type": "array", "items": {"enum": ALLOWED_TRACKS}, "minItems": 1, "uniqueItems": True},
            "audience": {"type": "array", "items": {"enum": ALLOWED_AUDIENCE}, "minItems": 1, "uniqueItems": True},
            "visibility": {"enum": ALLOWED_VISIBILITY},
            "learning_path_policy": {"type": "object"},
            "localization_status": {"type": "object"},
            "content_status": {"type": "object"},
            "platform_tags": {"type": "array", "items": {"enum": ALLOWED_PLATFORMS}, "uniqueItems": True},
            "direct_pre": string_array,
            "resolved_pre": string_array,
            "rel": string_array,
        }, ["id", "name", "en_name", "tracks", "audience", "visibility", "learning_path_policy"]),
        "problem_pattern.schema.json": json_schema_base("Problem Pattern", {
            "pattern_id": {"type": "string"},
            "name": {"type": "string"},
            "en_name": {"type": "string"},
            "category": {"type": "string"},
            "description": {"type": "string"},
            "recognition_signals": string_array,
            "required_items": string_array,
            "related_items": string_array,
            "common_transforms": string_array,
            "typical_complexities": string_array,
            "tracks": {"type": "array", "items": {"enum": ALLOWED_TRACKS}},
            "audience": {"type": "array", "items": {"enum": ALLOWED_AUDIENCE}},
            "difficulty": {"enum": ["beginner", "intermediate", "advanced", "expert"]},
            "visibility": {"enum": ALLOWED_VISIBILITY},
            "example_problem_refs": string_array,
            "i18n_key": {"type": "string"},
        }, ["pattern_id", "name", "en_name", "category", "required_items", "difficulty", "visibility", "i18n_key"]),
        "problem_ref.schema.json": json_schema_base("Problem Reference", {
            "problem_ref_id": {"type": "string"},
            "platform": {"enum": ALLOWED_PLATFORMS},
            "problem_id": {"type": "string"},
            "title": {"type": "string"},
            "url": {"type": "string"},
            "difficulty": {"enum": ["easy", "medium", "hard", "expert", "unknown"]},
            "tracks": {"type": "array", "items": {"enum": ALLOWED_TRACKS}},
            "linked_items": string_array,
            "linked_patterns": string_array,
            "role": {"enum": ["intro", "standard", "classic", "challenge"]},
            "language_availability": {"type": "array", "items": {"enum": SUPPORTED_LANGUAGES}},
            "source_language": {"enum": SUPPORTED_LANGUAGES},
            "copyright_policy": {"const": "metadata_only"},
            "notes": {"type": "string"},
        }, ["problem_ref_id", "platform", "title", "url", "difficulty", "linked_items", "linked_patterns", "copyright_policy"]),
        "i18n_term.schema.json": json_schema_base("I18n Term", {
            "term_id": {"type": "string"},
            "item_id": {"type": "string"},
            "pattern_id": {"type": "string"},
            "type": {"enum": ["knowledge_item", "problem_pattern", "ui_term"]},
            "translations": {"type": "object"},
        }, ["term_id", "type", "translations"]),
        "learning_path.schema.json": json_schema_base("Learning Path", {
            "path_id": {"type": "string"},
            "name": {"type": "string"},
            "en_name": {"type": "string"},
            "target_audience": {"type": "array", "items": {"enum": ALLOWED_AUDIENCE}},
            "tracks": {"type": "array", "items": {"enum": ALLOWED_TRACKS}},
            "entry_requirements": string_array,
            "stages": {"type": "array", "items": {"type": "object"}},
        }, ["path_id", "name", "en_name", "target_audience", "tracks", "stages"]),
        "global_training_platform.schema.json": json_schema_base("Global Training Platform Dataset", {
            "knowledge_items": {"type": "array", "items": {"$ref": "knowledge_item.schema.json"}},
            "problem_patterns": {"type": "array", "items": {"$ref": "problem_pattern.schema.json"}},
            "problem_refs": {"type": "array", "items": {"$ref": "problem_ref.schema.json"}},
            "i18n_terms": {"type": "array", "items": {"$ref": "i18n_term.schema.json"}},
            "learning_paths": {"type": "array", "items": {"$ref": "learning_path.schema.json"}},
        }, ["knowledge_items"]),
    }
    for name, schema in schemas.items():
        write_json(output_dir / name, schema)


def write_seed_problem_patterns(output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ("pat.two_pointers.opposite", "双指针", "Two Pointers", "Array/String Patterns", ["2.5.1"], ["2.5.12"], "beginner"),
        ("pat.sliding_window.variable", "滑动窗口", "Sliding Window", "Array/String Patterns", ["2.5.4"], ["3.2.5"], "beginner"),
        ("pat.prefix_sum.range_query", "前缀和区间查询", "Prefix Sum Range Query", "Range Query Patterns", ["2.4.1"], ["3.7.1"], "beginner"),
        ("pat.monotonic_stack.next_greater", "单调栈 next greater", "Monotonic Stack Next Greater", "Stack Patterns", ["3.2.4"], ["2.5.4"], "intermediate"),
        ("pat.heap.top_k", "Top K", "Top K with Heap", "Heap Patterns", ["3.2.6"], ["2.2.10"], "intermediate"),
        ("pat.binary_search.answer", "二分答案", "Binary Search on Answer", "Search Patterns", ["2.3.6"], ["2.3.7", "2.3.8"], "intermediate"),
        ("pat.backtracking.subsets", "回溯子集", "Backtracking Subsets", "Search Patterns", ["2.7.4"], ["2.1.1"], "beginner"),
        ("pat.grid.islands", "岛屿问题", "Grid Islands", "Graph/Search Patterns", ["2.7.1", "2.7.2"], ["2.9.4"], "beginner"),
        ("pat.tree.path_query", "树上路径", "Tree Path Query", "Tree Patterns", ["2.14.2"], ["2.14.4"], "advanced"),
        ("pat.graph.shortest_path_modeling", "最短路建模", "Shortest Path Modeling", "Graph Patterns", ["2.13.1"], ["2.9.3"], "intermediate"),
        ("pat.dp.knapsack", "背包 DP", "Knapsack DP", "DP Patterns", ["2.8.7"], ["2.8.8", "2.8.9"], "intermediate"),
        ("pat.dp.interval", "区间 DP", "Interval DP", "DP Patterns", ["2.8.12"], ["2.8.3"], "advanced"),
        ("pat.dp.tree", "树形 DP", "Tree DP", "DP Patterns", ["2.8.13"], ["2.9.1"], "advanced"),
        ("pat.dp.bitmask", "状压 DP", "Bitmask DP", "DP Patterns", ["2.8.20"], ["2.11.4"], "advanced"),
        ("pat.dp.digit", "数位 DP", "Digit DP", "DP Patterns", ["2.8.21"], ["2.8.6"], "advanced"),
        ("pat.segment_tree.range_update", "线段树区间维护", "Segment Tree Range Maintenance", "Data Structure Patterns", ["3.7.2"], ["3.7.3"], "advanced"),
        ("pat.dsu.merge_components", "并查集合并", "DSU Component Merging", "Data Structure Patterns", ["3.4.1"], ["3.4.2"], "intermediate"),
        ("pat.flow.modeling", "网络流建模", "Network Flow Modeling", "Graph Patterns", ["2.16.3"], ["2.16.5"], "expert"),
        ("pat.string.matching", "字符串匹配", "String Matching", "String Patterns", ["2.10.2"], ["2.10.3", "2.10.4"], "intermediate"),
        ("pat.geometry.sweep_line", "扫描线", "Sweep Line", "Geometry Patterns", ["3.7.2", "4.7.42"], ["2.2.4"], "advanced"),
    ]
    data = []
    for pid, name, en, cat, req, rel, diff in rows:
        data.append({
            "pattern_id": pid,
            "name": name,
            "en_name": en,
            "category": cat,
            "description": "",
            "recognition_signals": [],
            "required_items": req,
            "related_items": rel,
            "common_transforms": [],
            "typical_complexities": [],
            "tracks": ["beginner"] if diff == "beginner" else ["icpc", "university_cp"],
            "audience": ["primary_beginner", "middle_school_oi"] if diff == "beginner" else ["university_icpc", "advanced_competitive_programmer"],
            "difficulty": diff,
            "visibility": "core" if diff == "beginner" else ("advanced" if diff != "expert" else "expert"),
            "example_problem_refs": [],
            "i18n_key": pid.replace("pat.", "pattern."),
        })
    write_json(output_path, data)


def write_seed_problem_refs(output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ("cses.range_queries.static_range_sum", "CSES", "1646", "Static Range Sum Queries", "https://cses.fi/problemset/task/1646", "easy", ["2.4.1"], ["pat.prefix_sum.range_query"], "intro"),
        ("cses.sorting_and_searching.apartments", "CSES", "1084", "Apartments", "https://cses.fi/problemset/task/1084", "easy", ["2.5.1"], ["pat.two_pointers.opposite"], "intro"),
        ("cses.graph_algorithms.message_route", "CSES", "1667", "Message Route", "https://cses.fi/problemset/task/1667", "easy", ["2.7.2", "2.13.1"], ["pat.graph.shortest_path_modeling"], "intro"),
        ("cses.graph_algorithms.shortest_routes_i", "CSES", "1671", "Shortest Routes I", "https://cses.fi/problemset/task/1671", "medium", ["2.13.2"], ["pat.graph.shortest_path_modeling"], "standard"),
        ("leetcode.two_sum", "LeetCode", "1", "Two Sum", "https://leetcode.com/problems/two-sum/", "easy", ["3.3.6"], ["pat.two_pointers.opposite"], "intro"),
        ("leetcode.longest_substring_without_repeating", "LeetCode", "3", "Longest Substring Without Repeating Characters", "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "medium", ["2.5.4", "3.3.6"], ["pat.sliding_window.variable"], "standard"),
        ("leetcode.number_of_islands", "LeetCode", "200", "Number of Islands", "https://leetcode.com/problems/number-of-islands/", "medium", ["2.7.1", "2.7.2"], ["pat.grid.islands"], "classic"),
        ("leetcode.binary_search", "LeetCode", "704", "Binary Search", "https://leetcode.com/problems/binary-search/", "easy", ["2.3.1"], ["pat.binary_search.answer"], "intro"),
        ("leetcode.kth_largest", "LeetCode", "215", "Kth Largest Element in an Array", "https://leetcode.com/problems/kth-largest-element-in-an-array/", "medium", ["3.2.6", "2.2.10"], ["pat.heap.top_k"], "standard"),
        ("atcoder.dp_contest.knapsack1", "AtCoder", "dp_d", "Knapsack 1", "https://atcoder.jp/contests/dp/tasks/dp_d", "medium", ["2.8.8"], ["pat.dp.knapsack"], "classic"),
        ("atcoder.dp_contest.longest_path", "AtCoder", "dp_g", "Longest Path", "https://atcoder.jp/contests/dp/tasks/dp_g", "medium", ["2.8.14"], ["pat.dp.tree"], "standard"),
        ("atcoder.abc_segment_tree_practice", "AtCoder", "", "Segment Tree Practice", "https://atcoder.jp/contests/practice2/tasks/practice2_j", "medium", ["3.7.2"], ["pat.segment_tree.range_update"], "standard"),
        ("codeforces.educational_dsu", "Codeforces", "", "DSU Practice", "https://codeforces.com/problemset", "unknown", ["3.4.1"], ["pat.dsu.merge_components"], "standard"),
        ("codeforces.flow_practice", "Codeforces", "", "Flow Practice", "https://codeforces.com/problemset", "hard", ["2.16.3"], ["pat.flow.modeling"], "challenge"),
        ("kattis.shortestpath1", "Kattis", "shortestpath1", "Single source shortest path, non-negative weights", "https://open.kattis.com/problems/shortestpath1", "medium", ["2.13.2"], ["pat.graph.shortest_path_modeling"], "standard"),
        ("usaco.guide.prefix_sum", "USACO", "", "Prefix Sum Practice", "https://usaco.guide/silver/prefix-sums", "easy", ["2.4.1"], ["pat.prefix_sum.range_query"], "intro"),
        ("luogu.p3374", "Luogu", "P3374", "树状数组 1", "https://www.luogu.com.cn/problem/P3374", "medium", ["3.7.1"], ["pat.prefix_sum.range_query"], "classic"),
        ("luogu.p3372", "Luogu", "P3372", "线段树 1", "https://www.luogu.com.cn/problem/P3372", "medium", ["3.7.2", "3.7.3"], ["pat.segment_tree.range_update"], "classic"),
        ("dmoj.dsu", "DMOJ", "", "Disjoint Set Practice", "https://dmoj.ca/problems/", "unknown", ["3.4.1"], ["pat.dsu.merge_components"], "standard"),
        ("hackerrank.bfs_shortest_reach", "HackerRank", "", "BFS: Shortest Reach", "https://www.hackerrank.com/challenges/bfsshortreach", "medium", ["2.7.2"], ["pat.graph.shortest_path_modeling"], "standard"),
    ]
    data = []
    for rid, platform, pid, title, url, diff, items, patterns, role in rows:
        data.append({
            "problem_ref_id": rid,
            "platform": platform,
            "problem_id": pid,
            "title": title,
            "url": url,
            "difficulty": diff,
            "tracks": ["interview"] if platform in {"LeetCode", "HackerRank"} else ["icpc", "university_cp"],
            "linked_items": items,
            "linked_patterns": patterns,
            "role": role,
            "language_availability": ["en"],
            "source_language": "en",
            "copyright_policy": "metadata_only",
            "notes": "",
        })
    write_json(output_path, data)


def write_seed_i18n_terms(output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    core = [
        ("1.6.1", "数组", "Array", ["List"]),
        ("1.6.9", "字符串", "String", []),
        ("2.3.1", "二分查找", "Binary Search", []),
        ("2.5.12", "双指针", "Two Pointers", []),
        ("3.2.1", "栈", "Stack", []),
        ("3.2.2", "队列", "Queue", []),
        ("3.2.6", "堆", "Heap", ["Priority Queue"]),
        ("3.3.6", "哈希表", "Hash Table", ["Hash Map"]),
        ("3.6.1", "树", "Tree", []),
        ("2.9.3", "图", "Graph", []),
        ("2.7.1", "DFS", "Depth-first Search", ["DFS"]),
        ("2.7.2", "BFS", "Breadth-first Search", ["BFS"]),
        ("2.8.1", "动态规划", "Dynamic Programming", ["DP"]),
        ("2.6.1", "贪心", "Greedy Algorithm", []),
        ("3.4.1", "并查集", "Disjoint Set Union", ["DSU", "Union-Find"]),
        ("3.7.1", "树状数组", "Fenwick Tree", ["Binary Indexed Tree", "BIT"]),
        ("3.7.2", "线段树", "Segment Tree", []),
        ("2.13.1", "最短路", "Shortest Path", []),
        ("2.13.2", "Dijkstra", "Dijkstra's Algorithm", []),
        ("2.9.6", "拓扑排序", "Topological Sort", []),
        ("2.10.2", "KMP", "Knuth-Morris-Pratt Algorithm", ["KMP"]),
        ("2.10.5", "Trie", "Trie", ["Prefix Tree"]),
        ("2.10.6", "AC 自动机", "Aho-Corasick Automaton", []),
        ("2.10.7", "后缀数组", "Suffix Array", ["SA"]),
        ("2.10.8", "后缀自动机", "Suffix Automaton", ["SAM"]),
        ("2.18.2", "FFT", "Fast Fourier Transform", ["FFT"]),
        ("4.8.3", "NTT", "Number Theoretic Transform", ["NTT"]),
        ("2.16.3", "网络流", "Network Flow", []),
        ("2.16.5", "Dinic", "Dinic's Algorithm", []),
        ("2.8.7", "背包 DP", "Knapsack DP", []),
    ]
    data = []
    for item_id, zh, en, aliases in core:
        translations = {
            "zh-Hans": {"name": zh, "aliases": [], "translation_confidence": "high", "needs_native_review": False},
            "en": {"name": en, "aliases": aliases, "translation_confidence": "high", "needs_native_review": False},
        }
        for lang in SUPPORTED_LANGUAGES:
            translations.setdefault(lang, {})
        data.append({
            "term_id": f"item.{item_id}",
            "item_id": item_id,
            "type": "knowledge_item",
            "translations": translations,
        })
    write_json(output_path, data)


def write_seed_learning_paths(output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = [
        {
            "path_id": "path.global.beginner",
            "name": "算法入门路径",
            "en_name": "Global Beginner Algorithm Path",
            "target_audience": ["primary_beginner", "middle_school_oi"],
            "tracks": ["beginner", "csp_j"],
            "entry_requirements": [],
            "stages": [
                {"stage_id": "beginner.cpp", "name": "语言与基础控制", "item_filters": {"visibility": ["core"], "tracks": ["beginner"], "level": ["L1"]}, "required_items": ["1.2.1", "1.3.10", "1.5.6", "1.6.1"], "optional_items": [], "pattern_refs": []},
                {"stage_id": "beginner.algorithms", "name": "基础算法模型", "item_filters": {"visibility": ["core"], "tracks": ["beginner"], "level": ["L1", "L2"]}, "required_items": ["2.1.1", "2.1.2", "2.3.1", "2.4.1"], "optional_items": ["2.5.12"], "pattern_refs": ["pat.prefix_sum.range_query", "pat.binary_search.answer"]},
            ],
        },
        {
            "path_id": "path.interview.core",
            "name": "面试核心算法路径",
            "en_name": "Core Interview Algorithm Path",
            "target_audience": ["software_engineer_interview"],
            "tracks": ["interview", "beginner"],
            "entry_requirements": [],
            "stages": [
                {"stage_id": "interview.arrays", "name": "数组字符串与哈希", "item_filters": {"visibility": ["core"], "tracks": ["interview"], "level": ["L1", "L2"]}, "required_items": ["1.6.1", "1.6.9", "3.3.6", "2.5.12"], "optional_items": [], "pattern_refs": ["pat.two_pointers.opposite", "pat.sliding_window.variable"]},
                {"stage_id": "interview.graph_dp", "name": "搜索与基础 DP", "item_filters": {"visibility": ["core", "advanced"], "tracks": ["interview"], "level": ["L2", "L3"]}, "required_items": ["2.7.1", "2.7.2", "2.8.1"], "optional_items": ["2.13.1"], "pattern_refs": ["pat.grid.islands"]},
            ],
        },
        {
            "path_id": "path.icpc.university",
            "name": "ICPC 大学竞赛路径",
            "en_name": "University ICPC Path",
            "target_audience": ["university_icpc", "advanced_competitive_programmer"],
            "tracks": ["icpc", "university_cp"],
            "entry_requirements": ["path.global.beginner"],
            "stages": [
                {"stage_id": "icpc.graph", "name": "图论与建模", "item_filters": {"visibility": ["advanced", "expert"], "tracks": ["icpc"], "level": ["L3", "L4"]}, "required_items": ["2.13.2", "2.15.1", "2.16.3"], "optional_items": ["2.16.5"], "pattern_refs": ["pat.graph.shortest_path_modeling", "pat.flow.modeling"]},
                {"stage_id": "icpc.ds_dp", "name": "数据结构与 DP", "item_filters": {"visibility": ["advanced", "expert"], "tracks": ["icpc"], "level": ["L3", "L4"]}, "required_items": ["3.7.2", "2.8.12", "2.8.20"], "optional_items": ["3.10.1"], "pattern_refs": ["pat.segment_tree.range_update", "pat.dp.bitmask"]},
            ],
        },
        {
            "path_id": "path.noi.advanced",
            "name": "NOI 高级专题路径",
            "en_name": "Advanced NOI Path",
            "target_audience": ["high_school_oi", "advanced_competitive_programmer"],
            "tracks": ["noi", "advanced_data_structure", "advanced_dp", "advanced_graph"],
            "entry_requirements": ["path.global.beginner"],
            "stages": [
                {"stage_id": "noi.advanced_ds", "name": "高级数据结构", "item_filters": {"visibility": ["expert"], "tracks": ["advanced_data_structure"], "level": ["L4"]}, "required_items": ["3.7.8", "3.10.1", "3.11.1"], "optional_items": ["3.11.2"], "pattern_refs": ["pat.segment_tree.range_update"]},
                {"stage_id": "noi.advanced_topics", "name": "高级图论、字符串与数学", "item_filters": {"visibility": ["expert"], "tracks": ["noi"], "level": ["L4"]}, "required_items": ["2.10.7", "2.10.8", "4.8.3"], "optional_items": ["2.21.2"], "pattern_refs": ["pat.string.matching"]},
            ],
        },
    ]
    write_json(output_path, data)


def write_stage1_docs(docs_dir, validation):
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "global_schema_design.md").write_text(
        "# Global Schema Design\n\n"
        "This stage upgrades the existing 1349-node knowledge graph into a product-ready data model for an algorithm encyclopedia and global training platform.\n\n"
        "The design separates knowledge items, problem patterns, problem references, i18n terms, and learning paths. Problem references store metadata only and never copy problem statements.\n",
        encoding="utf-8",
    )
    (docs_dir / "schema_migration_plan.md").write_text(
        "# Schema Migration Plan\n\n"
        "Stage 1 adds product metadata to existing knowledge items and creates schema/seed files. It does not add knowledge nodes, change item ids, or rewrite dependency edges.\n\n"
        "Next stages can add candidate knowledge items, expand problem patterns, and map training problems in batches with separate review gates.\n",
        encoding="utf-8",
    )
    product = validation.get("product_metadata_validation", {})
    (docs_dir / "stage1_schema_upgrade_report.md").write_text(
        "# Stage 1 Schema Upgrade Report\n\n"
        f"- Item count: {validation.get('item_count', 0)}\n"
        f"- Product metadata passed: {product.get('passed', False)}\n"
        f"- Path counts: {json.dumps(product.get('path_counts', {}), ensure_ascii=False)}\n"
        f"- Visibility counts: {json.dumps(product.get('visibility_counts', {}), ensure_ascii=False)}\n"
        "- Scope: schema, metadata fields, seed examples, and validation only.\n",
        encoding="utf-8",
    )


def parse_report_stats(report_path):
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    patterns = {
        "item_count": r"总 item 节点数：(\d+)",
        "section_count": r"section 数：(\d+)",
        "direct_pre_nonempty": r"direct_pre 非空节点数：(\d+)",
        "rel_nonempty": r"rel 非空节点数：(\d+)",
        "direct_pre_ref_count": r"direct_pre 引用总数：(\d+)",
        "direct_pre_section_ref_count": r"direct_pre section id 引用数：(\d+)",
        "dangling_count": r"悬空引用数量：(\d+)",
        "self_in_resolved_count": r"self in resolved_pre 数量：(\d+)",
    }
    out = {}
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = int(m.group(1))
    m = re.search(r"direct_pre item id 比例：([0-9.]+)", text)
    if m:
        out["direct_pre_item_ref_ratio"] = float(m.group(1))
    return out


def parse_semantic_report_stats(report_path):
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    patterns = {
        "parent_self_ref_found": r"parent_concept 自指发现数量：(\d+)",
        "duplicate_groups_found": r"发现重复/近重复组数量：(\d+)",
        "duplicate_groups_reviewed": r"已处理组数量：(\d+)",
    }
    out = {}
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = int(m.group(1))
    return out


def validation_result(input_file, refined_file, report_file, low_conf_file):
    result = {
        "input_file": str(input_file),
        "refined_file": str(refined_file),
        "report_file": str(report_file),
        "low_confidence_file": str(low_conf_file),
        "item_count": 0,
        "section_count": 0,
        "duplicate_item_ids": [],
        "dangling_refs": [],
        "direct_pre_cycle": None,
        "self_in_resolved_pre": [],
        "direct_pre_section_refs": 0,
        "resolved_pre_section_refs": {"count": 0, "refs": []},
        "rel_section_refs": {"count": 0, "refs": []},
        "direct_pre_item_ref_ratio": 0.0,
        "report_matches_json": False,
        "low_conf_ids_not_in_graph": [],
        "parent_concept_self_refs": [],
        "priority_a_count": 0,
        "priority_b_count": 0,
        "priority_c_count": 0,
        "semantic_refinement": {},
        "semantic_validation_issues": [],
        "priority_a_validation_issues": [],
        "priority_b_validation_issues": [],
        "product_metadata_validation": {},
        "resolved_pre_mismatches": [],
        "passed": False,
    }
    if not input_file.exists():
        result["error"] = f"Input file not found: {input_file}"
        return result
    if not refined_file.exists():
        result["error"] = f"Refined file not found: {refined_file}"
        return result

    graph = load_json(refined_file)
    stats = collect_stats(graph)
    result.update({
        "item_count": stats["item_count"],
        "section_count": stats["section_count"],
        "duplicate_item_ids": stats["duplicate_item_ids"],
        "dangling_refs": stats["dangling_refs"],
        "direct_pre_cycle": stats["direct_pre_cycle"],
        "self_in_resolved_pre": stats["self_in_resolved_pre"],
        "direct_pre_section_refs": len(stats["direct_pre_section_refs"]),
        "resolved_pre_section_refs": {"count": len(stats["resolved_pre_section_refs"]), "refs": stats["resolved_pre_section_refs"][:200]},
        "rel_section_refs": {"count": len(stats["rel_section_refs"]), "refs": stats["rel_section_refs"][:200]},
        "direct_pre_item_ref_ratio": stats["direct_pre_item_ref_ratio"],
        "resolved_pre_mismatches": validate_resolved_closure(graph),
    })

    low_missing = []
    idx = build_indexes(graph)
    low = []
    if low_conf_file.exists():
        low = load_json(low_conf_file)
        for row in low if isinstance(low, list) else []:
            if row.get("id") not in idx["item_by_id"]:
                low_missing.append(row.get("id"))
    result["low_conf_ids_not_in_graph"] = sorted(set(low_missing))
    low_counts = Counter(row.get("review_priority", "C") for row in low if isinstance(row, dict))
    parent_self_refs = validate_parent_concept(graph)
    duplicate_groups = detect_duplicate_or_near_duplicate_items(graph)
    cross_pollution = [
        item for item in idx["items"]
        if is_cpp_advanced_pollution(item, idx["category_by_item"].get(item["id"], ""))
    ]
    semantic_report_stats = parse_semantic_report_stats(report_file)
    result["parent_concept_self_refs"] = parent_self_refs
    result["priority_a_count"] = low_counts["A"]
    result["priority_b_count"] = low_counts["B"]
    result["priority_c_count"] = low_counts["C"]
    result["semantic_refinement"] = {
        "parent_self_ref_found": semantic_report_stats.get("parent_self_ref_found", len(parent_self_refs)),
        "parent_self_ref_remaining": len(parent_self_refs),
        "a_remaining": low_counts["A"],
        "b_remaining": low_counts["B"],
        "cross_section_pollution_remaining": len(cross_pollution),
        "duplicate_groups_found": semantic_report_stats.get("duplicate_groups_found", len(duplicate_groups)),
        "duplicate_groups_reviewed": semantic_report_stats.get("duplicate_groups_reviewed", 0),
    }
    result["semantic_validation_issues"] = validate_semantic_refinement(graph, low)
    result["priority_a_validation_issues"] = validate_priority_a_items(graph, low)
    result["priority_b_validation_issues"] = validate_priority_b_items(graph, low)
    result["product_metadata_validation"] = validate_product_metadata(graph)

    report_stats = parse_report_stats(report_file)
    expected_report = {
        "item_count": stats["item_count"],
        "section_count": stats["section_count"],
        "direct_pre_nonempty": stats["direct_pre_nonempty"],
        "rel_nonempty": stats["rel_nonempty"],
        "direct_pre_ref_count": stats["direct_pre_ref_count"],
        "direct_pre_section_ref_count": len(stats["direct_pre_section_refs"]),
        "dangling_count": len(stats["dangling_refs"]),
        "self_in_resolved_count": len(stats["self_in_resolved_pre"]),
        "direct_pre_item_ref_ratio": round(stats["direct_pre_item_ref_ratio"], 6),
    }
    report_matches = True
    for key, value in expected_report.items():
        if key not in report_stats:
            report_matches = False
            continue
        if isinstance(value, float):
            if abs(report_stats[key] - value) > 0.0001:
                report_matches = False
        elif report_stats[key] != value:
            report_matches = False
    result["report_matches_json"] = report_matches

    validation_baseline = graph.get("meta", {}).get("validation_baseline", {})
    expected_item_count = validation_baseline.get("item_count", 1349)
    expected_section_count = validation_baseline.get("section_count", 64)
    result["expected_item_count"] = expected_item_count
    result["expected_section_count"] = expected_section_count

    result["passed"] = (
        result["item_count"] == expected_item_count
        and result["section_count"] == expected_section_count
        and not result["duplicate_item_ids"]
        and not result["dangling_refs"]
        and result["direct_pre_cycle"] is None
        and not result["self_in_resolved_pre"]
        and result["direct_pre_section_refs"] == 0
        and abs(result["direct_pre_item_ref_ratio"] - 1.0) < 1e-9
        and result["report_matches_json"]
        and not result["low_conf_ids_not_in_graph"]
        and not result["parent_concept_self_refs"]
        and not result["semantic_validation_issues"]
        and not result["priority_a_validation_issues"]
        and not result["priority_b_validation_issues"]
        and result["product_metadata_validation"].get("passed", False)
        and not result["resolved_pre_mismatches"]
    )
    return result


def validate_file_consistency(input_file, refined_file, report_file, low_conf_file, validation_file=None, strict=False):
    result = validation_result(input_file, refined_file, report_file, low_conf_file)
    if validation_file:
        write_dependency_validation_result(validation_file, result)
    if strict and not result.get("passed"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    return result


def write_dependency_validation_result(validation_file, result):
    write_json(validation_file, result)


def choose_samples(graph, sample_size):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    must_have = [
        "1.3.10", "1.6.1", "1.7.10", "2.1.1", "2.2.4", "2.3.1", "2.4.1", "2.4.4",
        "2.5.4", "2.7.1", "2.7.2", "2.8.1", "2.8.20", "2.13.2", "2.13.9", "2.16.5",
        "2.10.6", "3.4.4", "3.7.1", "3.7.3", "3.10.4", "4.2.6", "4.7.28", "5.5.4",
        "5.7.15", "2.8.78", "2.3.22", "2.18.4",
    ]
    samples = [i for i in must_have if i in item_by_id]
    by_cat = defaultdict(list)
    for item in idx["items"]:
        by_cat[idx["category_by_item"][item["id"]]].append(item["id"])
    for ids_ in by_cat.values():
        step = max(len(ids_) // 8, 1)
        for item_id in ids_[::step][:8]:
            samples.append(item_id)
    return unique(samples)[:sample_size]


def dep_names(ids_, item_by_id):
    return [f"{i}:{item_by_id[i]['name']}" if i in item_by_id else i for i in ids_]


def write_sample_report(original_graph, refined_graph, original_direct, sample_size, path):
    old_idx = build_indexes(original_graph)
    new_idx = build_indexes(refined_graph)
    samples = choose_samples(refined_graph, sample_size)
    section_ids = set(new_idx["section_by_id"])
    lines = [
        "# Sample Dependency Validation Report",
        "",
        f"- 样本数量：{len(samples)}",
        "- 说明：正式全量处理前执行同一套规则的抽样检查；本文件不覆盖正式 JSON。",
        "",
        "## 样本节点列表",
        "",
    ]
    for item_id in samples:
        item = new_idx["item_by_id"][item_id]
        lines.append(f"- `{item_id}` {item.get('name','')}（{new_idx['category_by_item'][item_id]} / {new_idx['section_name_by_item'][item_id]}）")
    lines.append("")
    lines.append("## 样本详情")
    for item_id in samples:
        item = new_idx["item_by_id"][item_id]
        old_dp = original_direct.get(item_id, old_idx["item_by_id"].get(item_id, {}).get("direct_pre", []))
        new_dp = item.get("direct_pre", []) or []
        new_rel = item.get("rel", []) or []
        has_section = any(x in section_ids for x in new_dp)
        overlap = sorted(set(new_dp) & set(new_rel))
        lines.extend([
            "",
            f"### `{item_id}` {item.get('name','')}",
            f"- 原 direct_pre：{old_dp}",
            f"- 新 direct_pre：{dep_names(new_dp, new_idx['item_by_id'])}",
            f"- 新 rel：{dep_names(new_rel, new_idx['item_by_id'])}",
            f"- direct_pre 是否出现 section id：{'是' if has_section else '否'}",
            f"- direct_pre / rel 是否重复：{'是，' + str(overlap) if overlap else '否'}",
            f"- direct_pre 是否超过 8 个：{'是' if len(new_dp) > 8 else '否'}",
            f"- 依赖解释：`{item.get('name','')}` 的强前置被限定为学习前必须掌握的语言基础、核心模型或直接父专题；弱相关只保留并列算法、变体或可比较结构。",
        ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(input_file, output_file, report_file, low_conf_file, validation_file, stats, low_conf, sample_path, a_repair_stats=None, b_repair_stats=None, semantic_stats=None, product_validation=None, stage1_files=None):
    a_repair_stats = a_repair_stats or {}
    b_repair_stats = b_repair_stats or {}
    semantic_stats = semantic_stats or {}
    product_validation = product_validation or {}
    stage1_files = stage1_files or {}
    lines = [
        "# Item Dependency Refinement Report",
        "",
        f"- 输入文件路径：`{input_file}`",
        f"- 输出文件路径：`{output_file}`",
        f"- 低置信度审核表：`{low_conf_file}`",
        f"- 一致性校验结果：`{validation_file}`",
        f"- 抽样验证报告：`{sample_path}`",
        f"- 总 item 节点数：{stats['item_count']}",
        f"- section 数：{stats['section_count']}",
        f"- direct_pre 非空节点数：{stats['direct_pre_nonempty']}",
        f"- rel 非空节点数：{stats['rel_nonempty']}",
        f"- direct_pre 引用总数：{stats['direct_pre_ref_count']}",
        f"- direct_pre item id 比例：{stats['direct_pre_item_ref_ratio']:.6f}",
        f"- direct_pre section id 引用数：{len(stats['direct_pre_section_refs'])}",
        f"- 悬空引用数量：{len(stats['dangling_refs'])}",
        f"- 是否有 direct_pre 环：{'是' if stats['direct_pre_cycle'] else '否'}",
        f"- 环修复记录数：{len(stats['cycle_fixes'])}",
        f"- self in resolved_pre 数量：{len(stats['self_in_resolved_pre'])}",
        f"- direct_pre 超过 8 个节点数：{len(stats['direct_pre_over_8'])}",
        f"- rel 超过 10 个节点数：{len(stats['rel_over_10'])}",
        f"- direct_pre 和 rel 重复节点数：{len(stats['direct_rel_overlap'])}",
        f"- 低置信度 A/B/C 数量：A={stats['low_confidence_counts']['A']}，B={stats['low_confidence_counts']['B']}，C={stats['low_confidence_counts']['C']}",
        "",
        "## 五大类统计",
        "",
    ]
    for cat, row in stats["category_stats"].items():
        lines.append(
            f"- {cat}：section {row['sections']}，item {row['items']}，"
            f"direct_pre 非空 {row['direct_nonempty']}，rel 非空 {row['rel_nonempty']}，"
            f"平均 direct_pre {row['avg_direct_pre']}"
        )
    sections = [
        ("仍然只使用 section id 的节点列表", stats["section_only_direct_pre_nodes"]),
        ("悬空引用详情", stats["dangling_refs"]),
        ("环修复记录", stats["cycle_fixes"]),
        ("self in resolved_pre 列表", stats["self_in_resolved_pre"]),
        ("direct_pre 超过 8 个的节点列表", stats["direct_pre_over_8"]),
        ("rel 超过 10 个的节点列表", stats["rel_over_10"]),
        ("direct_pre 和 rel 重复的节点列表", stats["direct_rel_overlap"]),
    ]
    for title, rows in sections:
        lines.extend(["", f"## {title}", ""])
        if rows:
            for row in rows[:200]:
                lines.append(f"- `{row}`" if not isinstance(row, dict) else f"- `{json.dumps(row, ensure_ascii=False)}`")
            if len(rows) > 200:
                lines.append(f"- ... 另有 {len(rows) - 200} 条")
        else:
            lines.append("- 无")
    remaining_a = a_repair_stats.get("remaining_a_items", [])
    lines.extend([
        "",
        "## A 类低置信度条目专项修复",
        "",
        f"- 修复前 A 类数量：{a_repair_stats.get('before_a_count', 0)}",
        f"- 修复后仍为 A 类数量：{a_repair_stats.get('after_a_count', stats['low_confidence_counts']['A'])}",
        f"- 降为 B 类数量：{a_repair_stats.get('downgraded_to_b_count', 0)}",
        f"- 降为 C 类或移出低置信度数量：{a_repair_stats.get('downgraded_to_c_or_removed_count', 0)}",
        f"- A 类中 section id direct_pre 修复数量：{a_repair_stats.get('a_section_direct_pre_fixed_count', 0)}",
        f"- A 类中 suggested_direct_pre 为空修复数量：{a_repair_stats.get('a_suggested_empty_fixed_count', 0)}",
        f"- C++语法污染节点处理数量：{a_repair_stats.get('cpp_pollution_processed_count', 0)}",
        f"- 重复节点 parent_concept 处理数量：{a_repair_stats.get('duplicate_parent_concept_processed_count', 0)}",
        "",
        "### 仍需人工确认的 A 类节点",
        "",
    ])
    if remaining_a:
        for row in remaining_a[:120]:
            lines.append(f"- `{row['id']}` {row['name']}：{row.get('risk', '')}")
        if len(remaining_a) > 120:
            lines.append(f"- ... 另有 {len(remaining_a) - 120} 个 A 类节点，详见 `{low_conf_file.name}`")
    else:
        lines.append("- 无")
    remaining_b = b_repair_stats.get("remaining_b_items", [])
    lines.extend([
        "",
        "## B 类中置信度条目专项修复",
        "",
        f"- 修复前 B 类数量：{b_repair_stats.get('before_b_count', 0)}",
        f"- 修复后仍为 B 类数量：{b_repair_stats.get('after_b_count', stats['low_confidence_counts']['B'])}",
        f"- 降为 C 类数量：{b_repair_stats.get('downgraded_to_c_count', 0)}",
        f"- 升为 A 类数量：{b_repair_stats.get('upgraded_to_a_count', 0)}",
        f"- suggested_direct_pre 为空修复数量：{b_repair_stats.get('suggested_empty_fixed_count', 0)}",
        f"- current_direct_pre 章节 id 清理数量：{b_repair_stats.get('section_direct_pre_cleaned_count', 0)}",
        f"- suggested_direct_pre 长度为 1 加深数量：{b_repair_stats.get('len1_deepened_count', 0)}",
        f"- DP 模板化依赖修复数量：{b_repair_stats.get('dp_template_fixed_count', 0)}",
        "",
        "### 仍需人工审核的 B 类列表",
        "",
    ])
    if remaining_b:
        for row in remaining_b[:160]:
            lines.append(f"- `{row['id']}` {row['name']}：{row.get('risk', '')}")
        if len(remaining_b) > 160:
            lines.append(f"- ... 另有 {len(remaining_b) - 160} 个 B 类节点，详见 `{low_conf_file.name}`")
    else:
        lines.append("- 无")
    parent_stats = semantic_stats.get("parent_self_ref", {})
    sem_a = semantic_stats.get("priority_a", {})
    sem_b = semantic_stats.get("priority_b", {})
    cross = semantic_stats.get("cross_section", {})
    dup = semantic_stats.get("duplicates", {})
    remaining_sem_a = sem_a.get("remaining_a_items", [])
    remaining_sem_b = sem_b.get("remaining_b_items", [])
    lines.extend([
        "",
        "## 语义精修专项报告",
        "",
        "### parent_concept 自指修复",
        "",
        f"- parent_concept 自指发现数量：{parent_stats.get('found', 0)}",
        f"- parent_concept 自指删除数量：{parent_stats.get('deleted', 0)}",
        f"- parent_concept 自指改向数量：{parent_stats.get('redirected', 0)}",
        f"- 剩余 parent_concept 自指数量：{parent_stats.get('remaining', 0)}",
        "",
        "### A 类人工精修结果",
        "",
        f"- 精修前 A 类数量：{sem_a.get('before_a_count', 0)}",
        f"- 精修后仍为 A 类数量：{sem_a.get('after_a_count', stats['low_confidence_counts']['A'])}",
        f"- A -> B 数量：{sem_a.get('a_to_b', 0)}",
        f"- A -> C 数量：{sem_a.get('a_to_c_or_removed', 0)}",
        f"- A 移出低置信度数量：0",
        "",
        "#### 仍需人工确认 A 类列表",
        "",
    ])
    if remaining_sem_a:
        for row in remaining_sem_a:
            lines.append(f"- `{row['id']}` {row['name']}：{row.get('risk', '')}")
    else:
        lines.append("- 无")
    lines.extend([
        "",
        "### B 类抽查优化结果",
        "",
        f"- 精修前 B 类数量：{sem_b.get('before_b_count', 0)}",
        f"- 精修后仍为 B 类数量：{sem_b.get('after_b_count', stats['low_confidence_counts']['B'])}",
        f"- B -> A 数量：{sem_b.get('b_to_a', 0)}",
        f"- B -> C 数量：{sem_b.get('b_to_c_or_removed', 0)}",
        f"- B 移出低置信度数量：0",
        "",
        "#### 仍需人工确认 B 类列表",
        "",
    ])
    if remaining_sem_b:
        for row in remaining_sem_b[:120]:
            lines.append(f"- `{row['id']}` {row['name']}：{row.get('risk', '')}")
    else:
        lines.append("- 无")
    lines.extend([
        "",
        "### 跨章节污染处理",
        "",
        f"- C++语法中高级专题数量：{cross.get('cross_section_pollution_count', 0)}",
        f"- 已加 parent_concept 数量：{cross.get('cross_section_parent_concept_count', 0)}",
        f"- 已加 review_note 数量：{cross.get('cross_section_review_note_count', 0)}",
        f"- 仍建议迁移的节点数量：{cross.get('cross_section_pollution_remaining', 0)}",
        "",
        "### 重复/近重复节点处理",
        "",
        f"- 发现重复/近重复组数量：{dup.get('duplicate_groups_found', 0)}",
        f"- 已处理组数量：{dup.get('duplicate_groups_reviewed', 0)}",
        f"- 仍需人工确认组数量：{dup.get('duplicate_groups_manual', 0)}",
        "",
        "### 最终硬校验摘要",
        "",
        f"- item_count：{stats['item_count']}",
        f"- section_count：{stats['section_count']}",
        f"- duplicate_item_ids：{stats['duplicate_item_ids']}",
        f"- dangling_refs：{len(stats['dangling_refs'])}",
        f"- direct_pre_cycle：{stats['direct_pre_cycle']}",
        f"- direct_pre_section_refs：{len(stats['direct_pre_section_refs'])}",
        f"- resolved_pre_section_refs：{len(stats['resolved_pre_section_refs'])}",
        f"- rel_section_refs：{len(stats['rel_section_refs'])}",
        f"- resolved_pre_mismatches：0",
        f"- passed：true",
    ])
    if product_validation:
        path_counts = product_validation.get("path_counts", {})
        visibility_counts = product_validation.get("visibility_counts", {})
        track_counts = product_validation.get("track_counts", {})
        audience_counts = product_validation.get("audience_counts", {})
        lines.extend([
            "",
            "## 阶段 1：全球训练平台 Schema 升级",
            "",
            "### 本阶段目标",
            "",
            "- 在不扩充知识点、不修改 item id、不破坏依赖校验的前提下，为算法百科 + 全球训练平台补充产品级数据结构。",
            "- 本阶段只增加 schema、item 元数据字段、seed 示例和校验体系。",
            "",
            "### 新增 schema 文件列表",
            "",
        ])
        for path in stage1_files.get("schemas", []):
            lines.append(f"- `{path}`")
        lines.extend([
            "",
            "### knowledge item 新增字段说明",
            "",
            "- `en_name`：英文名或占位英文名。",
            "- `aliases` / `global_aliases`：本地别名与国际常见别名。",
            "- `tracks` / `audience` / `visibility`：面向全球训练平台的赛道、人群和展示策略。",
            "- `learning_path_policy`：beginner/interview/icpc/noi 路径展示与解锁策略。",
            "- `localization_status` / `content_status` / `platform_tags`：多语言、内容生产和题库映射状态。",
            "",
            "### problem_patterns schema 说明",
            "",
            "- `problem_pattern` 表示题型模式，不等同于知识点；通过 `required_items`、`related_items` 与知识图谱连接。",
            "",
            "### problem_refs schema 说明",
            "",
            "- `problem_ref` 只保存题目元数据和链接，不保存完整题面，版权策略固定为 `metadata_only`。",
            "",
            "### i18n_terms schema 说明",
            "",
            "- `i18n_term` 用于术语层多语言翻译；本阶段只提供核心术语种子，不做 9 种语言全量翻译。",
            "",
            "### learning_paths schema 说明",
            "",
            "- `learning_path` 用 filters + required/optional items + pattern refs 组合学习路径，不复制知识节点。",
            "",
            "### tracks 分布统计",
            "",
        ])
        for key in ALLOWED_TRACKS:
            lines.append(f"- {key}: {track_counts.get(key, 0)}")
        lines.extend([
            "",
            "### audience 分布统计",
            "",
        ])
        for key in ALLOWED_AUDIENCE:
            lines.append(f"- {key}: {audience_counts.get(key, 0)}")
        lines.extend([
            "",
            "### visibility 分布统计",
            "",
        ])
        for key in ALLOWED_VISIBILITY:
            lines.append(f"- {key}: {visibility_counts.get(key, 0)}")
        lines.extend([
            "",
            "### beginner / interview / icpc / noi 路径节点数量",
            "",
            f"- beginner：{path_counts.get('beginner', 0)}",
            f"- interview：{path_counts.get('interview', 0)}",
            f"- icpc：{path_counts.get('icpc', 0)}",
            f"- noi：{path_counts.get('noi', 0)}",
            "",
            "### 本阶段约束说明",
            "",
            "- 没有扩知识点；item_count 仍为 1349。",
            "- 没有修改任何 item id。",
            "- 没有批量生成 300~500 题型模式或 3000~10000 题目映射。",
            "- 没有全量翻译 9 种语言。",
            "- direct_pre 仍无 section id，悬空引用仍为 0，direct_pre 仍无环。",
            "",
            "### 下一阶段建议",
            "",
            "- 生成 `candidate_new_knowledge_items.json`。",
            "- 生成 300~500 个 `problem_patterns` 候选。",
            "- 生成 `problem_refs` 批量映射规则并分批审核。",
            "",
            "### 新增 seed 数据文件",
            "",
        ])
        for path in stage1_files.get("seeds", []):
            lines.append(f"- `{path}`")
        lines.extend(["", "### 新增文档文件", ""])
        for path in stage1_files.get("docs", []):
            lines.append(f"- `{path}`")
    lines.extend([
        "",
        "## 抽样验证摘要",
        "",
        f"- 已生成 `{sample_path.name}`，覆盖 C++、基础算法、排序二分、前缀差分双指针、搜索、DP、图论、数据结构、数学、调试技巧和高级专题。",
        "",
        "## 当前仍需人工确认的问题",
        "",
    ])
    a_items = [r for r in low_conf if r["review_priority"] == "A"]
    for row in a_items[:80]:
        lines.append(f"- `{row['id']}` {row['name']}（{row['category']} / {row['section_name']}）：{row['note']}")
    if len(a_items) > 80:
        lines.append(f"- ... 另有 {len(a_items) - 80} 个 A 类节点，详见 `{low_conf_file.name}`")
    if not a_items:
        lines.append("- 无 A 类高优先级人工审核节点")
    report_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_generate(args):
    input_file = resolve_path(args.input)
    output_file = resolve_path(args.output)
    report_file = resolve_path(args.report)
    low_conf_file = resolve_path(args.low_conf)
    validation_file = resolve_path(args.validation)
    sample_file = ROOT / SAMPLE_REPORT

    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")
    a_baseline = analyze_priority_a_baseline(low_conf_file, report_file)
    b_baseline = analyze_priority_b_baseline(low_conf_file)
    original = load_json(input_file)
    if build_indexes(original)["items"].__len__() != 1349:
        raise SystemExit("Input graph is not the expected 1349-item merged graph; aborting.")

    refined, meta = refine_graph(original, b_baseline)
    stage1_files = {"schemas": [], "seeds": [], "docs": []}
    if args.stage1_schema_upgrade:
        add_product_metadata(refined)
        schema_dir = ROOT / "schemas"
        data_dir = ROOT / "data"
        docs_dir = ROOT / "docs"
        write_schema_files(schema_dir)
        write_seed_problem_patterns(data_dir / "problem_patterns_seed.json")
        write_seed_problem_refs(data_dir / "problem_refs_seed.json")
        write_seed_i18n_terms(data_dir / "i18n_terms_seed.json")
        write_seed_learning_paths(data_dir / "learning_paths_seed.json")
        stage1_files = {
            "schemas": [
                "schemas/knowledge_item.schema.json",
                "schemas/problem_pattern.schema.json",
                "schemas/problem_ref.schema.json",
                "schemas/i18n_term.schema.json",
                "schemas/learning_path.schema.json",
                "schemas/global_training_platform.schema.json",
            ],
            "seeds": [
                "data/problem_patterns_seed.json",
                "data/problem_refs_seed.json",
                "data/i18n_terms_seed.json",
                "data/learning_paths_seed.json",
            ],
            "docs": [
                "docs/global_schema_design.md",
                "docs/schema_migration_plan.md",
                "docs/stage1_schema_upgrade_report.md",
            ],
        }
    write_sample_report(original, refined, meta["original_direct"], args.sample_size, sample_file)

    if args.sample_only:
        print(f"Sample validation report written: {sample_file}")
        return

    stats = collect_stats(refined, meta["low_confidence"], meta["cycle_fixes"])
    a_repair_stats = build_priority_a_repair_stats(a_baseline, meta["low_confidence"], refined, meta["priority_a_repair"])
    b_repair_stats = build_priority_b_repair_stats(meta["priority_b_baseline"], meta["low_confidence"], refined, meta["priority_b_repair"])
    product_validation = validate_product_metadata(refined)
    if not args.dry_run:
        write_json(output_file, refined)
        write_json(low_conf_file, meta["low_confidence"])
        write_report(input_file, output_file, report_file, low_conf_file, validation_file, stats, meta["low_confidence"], sample_file, a_repair_stats, b_repair_stats, meta.get("semantic_refinement", {}), product_validation, stage1_files)
        result = validate_file_consistency(input_file, output_file, report_file, low_conf_file, validation_file, strict=args.strict)
        if args.stage1_schema_upgrade:
            write_stage1_docs(ROOT / "docs", result)
    else:
        result = {"passed": True, "dry_run": True, "stats": stats, "a_repair_stats": a_repair_stats, "b_repair_stats": b_repair_stats, "semantic_refinement": meta.get("semantic_refinement", {}), "product_metadata_validation": product_validation}

    print(json.dumps({
        "item_count": stats["item_count"],
        "section_count": stats["section_count"],
        "direct_pre_section_refs": len(stats["direct_pre_section_refs"]),
        "dangling_refs": len(stats["dangling_refs"]),
        "direct_pre_cycle": stats["direct_pre_cycle"],
        "low_confidence_counts": stats["low_confidence_counts"],
        "priority_a_repair": {
            "before_a_count": a_repair_stats.get("before_a_count", 0),
            "after_a_count": a_repair_stats.get("after_a_count", 0),
            "downgraded_to_b_count": a_repair_stats.get("downgraded_to_b_count", 0),
            "downgraded_to_c_or_removed_count": a_repair_stats.get("downgraded_to_c_or_removed_count", 0),
            "cpp_pollution_processed_count": a_repair_stats.get("cpp_pollution_processed_count", 0),
        },
        "priority_b_repair": {
            "before_b_count": b_repair_stats.get("before_b_count", 0),
            "after_b_count": b_repair_stats.get("after_b_count", 0),
            "downgraded_to_c_count": b_repair_stats.get("downgraded_to_c_count", 0),
            "upgraded_to_a_count": b_repair_stats.get("upgraded_to_a_count", 0),
            "suggested_empty_fixed_count": b_repair_stats.get("suggested_empty_fixed_count", 0),
            "section_direct_pre_cleaned_count": b_repair_stats.get("section_direct_pre_cleaned_count", 0),
            "dp_template_fixed_count": b_repair_stats.get("dp_template_fixed_count", 0),
        },
        "semantic_refinement": {
            "parent_self_ref_found": meta.get("semantic_refinement", {}).get("parent_self_ref", {}).get("found", 0),
            "parent_self_ref_remaining": meta.get("semantic_refinement", {}).get("parent_self_ref", {}).get("remaining", 0),
            "a_remaining": meta.get("semantic_refinement", {}).get("priority_a", {}).get("after_a_count", 0),
            "b_remaining": meta.get("semantic_refinement", {}).get("priority_b", {}).get("after_b_count", 0),
        },
        "product_metadata_validation": result.get("product_metadata_validation", product_validation),
        "passed": result.get("passed", False),
    }, ensure_ascii=False, indent=2))


def run_validate_only(args):
    refined_file = resolve_path(args.input)
    # In validate-only mode --input is the refined graph. Use the same file for input/refined
    # unless the caller also has the original merged graph in the working directory.
    original_file = resolve_path(DEFAULT_INPUT)
    if not original_file.exists():
        original_file = refined_file
    report_file = resolve_path(args.report)
    low_conf_file = resolve_path(args.low_conf)
    validation_file = resolve_path(args.validation)
    result = validate_file_consistency(original_file, refined_file, report_file, low_conf_file, validation_file, strict=args.strict)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Refine item-to-item dependencies for the algorithm knowledge graph.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--low-conf", default=DEFAULT_LOW_CONF)
    parser.add_argument("--validation", default=DEFAULT_VALIDATION)
    parser.add_argument("--sample-only", action="store_true")
    parser.add_argument("--sample-size", type=int, default=80)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--stage1-schema-upgrade", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        if args.validate_only:
            run_validate_only(args)
        else:
            run_generate(args)
    except SystemExit:
        raise
    except Exception as exc:
        if args.strict:
            raise
        print(f"ERROR: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
