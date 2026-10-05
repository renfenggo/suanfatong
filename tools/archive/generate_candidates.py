import json

def create_candidate(candidate_id, name, en_name, category, difficulty, tracks, direct_pre, reason, en_aliases=None, zh_aliases=None):
    """创建候选的基础结构"""
    if en_aliases is None:
        en_aliases = []
    if zh_aliases is None:
        zh_aliases = []
    
    return {
        "candidate_id": candidate_id,
        "name": name,
        "en_name": en_name,
        "category_suggestion": category,
        "section_suggestion": {
            "name": "高级" + category,
            "action": "create_new_section"
        },
        "level": "L4" if difficulty == "advanced" else "L5" if difficulty == "expert" else "L3",
        "difficulty": difficulty,
        "tracks": tracks,
        "audience": ["high_school_oi", "university_icpc"] if "noi" in tracks else ["university_icpc", "advanced_competitive_programmer"],
        "visibility": difficulty,
        "learning_path_policy": {
            "show_in_beginner_path": False,
            "show_in_interview_path": False,
            "show_in_icpc_path": "icpc" in tracks,
            "show_in_noi_path": "noi" in tracks,
            "unlock_mode": "expert_branch" if difficulty == "expert" else "optional_branch"
        },
        "reason_to_add": reason,
        "global_relevance": {
            "noi": "noi" in tracks,
            "ioi": "ioi" in tracks or "noi" in tracks,
            "icpc": "icpc" in tracks,
            "interview": False,
            "university_cp": "icpc" in tracks,
            "notes": category + "高级技术"
        },
        "direct_pre_name_suggestion": direct_pre,
        "rel_name_suggestion": [category + "技术"],
        "parent_concept_name_suggestion": category,
        "merge_risk_hint": {
            "possible_duplicate_keywords": [name, en_name],
            "duplicate_risk": "low" if difficulty == "expert" else "medium",
            "merge_action_hint": "add_new"
        },
        "i18n_seed": {
            "zh-Hans": {"name": name, "aliases": zh_aliases + [en_name]},
            "en": {"name": en_name, "aliases": en_aliases + [name]},
            "ja": {"name": "", "aliases": [], "needs_native_review": True},
            "ko": {"name": "", "aliases": [], "needs_native_review": True}
        },
        "content_status": {
            "has_explanation": False,
            "has_examples": False,
            "has_code_template": False,
            "has_visualization": False,
            "has_practice_refs": False,
            "content_priority": "P1"
        },
        "review_status": {
            "need_manual_review": False,
            "review_priority": "A" if difficulty == "expert" else "B",
            "review_reason": category + "高级技术"
        },
        "source": "thread2_batch2_generation"
    }

# 生成字符串候选
string_candidates = [
    # 基础字符串算法
    create_candidate("cand.string.z_algorithm.basic", "Z算法基础", "Z Algorithm Basic", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["String Matching", "Linear Time Algorithms"], 
                    "Z算法是一种线性时间字符串匹配算法，用于计算字符串的Z函数，适用于模式匹配和字符串分析。"),
    create_candidate("cand.string.z_algorithm.pattern_matching", "Z算法模式匹配应用", "Z Algorithm Pattern Matching", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Z Algorithm Basic", "String Matching"], 
                    "Z算法在模式匹配中的应用，包括多模式匹配、字符串查找等场景。"),
    create_candidate("cand.string.ex_kmp.basic", "扩展KMP算法基础", "Extended KMP Basic", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["KMP Algorithm", "Z Algorithm Basic"], 
                    "扩展KMP算法用于计算字符串的扩展Z函数，适用于字符串匹配和边界分析。"),
    create_candidate("cand.string.kmp_automaton.basic", "KMP自动机基础", "KMP Automaton Basic", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["KMP Algorithm", "Finite Automata"], 
                    "KMP自动机基于KMP算法的失败函数构建有限状态自动机，用于处理字符串匹配和状态转移。"),
    
    # AC自动机高级应用
    create_candidate("cand.string.ac_automaton.applications", "AC自动机高级应用", "AC Automaton Advanced Applications", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["AC Automaton", "Trie Data Structure"], 
                    "AC自动机的高级应用，包括多模式匹配、模式计数、动态路径查询等复杂场景。"),
    create_candidate("cand.string.ac_failure_tree.analysis", "AC自动机失败树分析", "AC Automaton Failure Tree Analysis", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["AC Automaton", "Tree Data Structure"], 
                    "AC自动机的失败树结构分析，利用失败函数构建树形结构进行模式匹配和查询优化。"),
    
    # 后缀算法
    create_candidate("cand.string.suffix_array.sa_is", "后缀数组SA-IS算法", "Suffix Array SA-IS Algorithm", "算法", "expert", 
                    ["icpc", "advanced_string", "university_cp"], ["Suffix Array", "Divide and Conquer"], 
                    "SA-IS算法是一种线性时间后缀数组构建算法，效率高且实现相对简洁，是竞赛中重要的字符串算法。"),
    create_candidate("cand.string.lcp_rmq.optimization", "LCP RMQ优化", "LCP RMQ Optimization", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["LCP Array", "RMQ", "Sparse Table"], 
                    "最长公共前缀数组的RMQ优化，包括稀疏表、线段树等多种数据结构的应用和选择。"),
    
    # SAM高级
    create_candidate("cand.string.generalized_sam.construction", "广义SAM构建", "Generalized SAM Construction", "算法", "expert", 
                    ["icpc", "advanced_string", "university_cp"], ["Suffix Automaton", "Trie Data Structure"], 
                    "广义后缀自动机用于处理多个字符串的公共子串问题，在竞赛中用于复杂字符串分析。"),
    create_candidate("cand.string.sam_parent_tree.structure", "SAM父树结构", "SAM Parent Tree Structure", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Suffix Automaton", "Tree Data Structure"], 
                    "后缀自动机的父树结构分析，利用后缀自动机构建树形结构进行子串分析和查询。"),
    
    # 其他高级字符串结构
    create_candidate("cand.string.eertree.construction", "回文树Eertree构建", "Eertree Palindromic Tree Construction", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Palindrome", "Tree Data Structure"], 
                    "回文树（Eertree）是一种专门处理回文子串的数据结构，能够高效处理回文相关的问题。"),
    create_candidate("cand.string.suffix_tree.ukkonen", "后缀树Ukkonen算法", "Suffix Tree Ukkonen Algorithm", "算法", "expert", 
                    ["icpc", "advanced_string", "university_cp"], ["Suffix Tree", "Linear Time Algorithms"], 
                    "Ukkonen算法是一种线性时间后缀树构建算法，虽然实现复杂，但在竞赛中有重要理论价值。"),
    create_candidate("cand.string.lyndon_decomposition.basic", "Lyndon分解基础", "Lyndon Decomposition Basic", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["String Manipulation", "Greedy Algorithm"], 
                    "Lyndon分解是将字符串分解为Lyndon单词的技术，在字符串排序和最小表示中有重要应用。"),
    create_candidate("cand.string.duval_algorithm.minimal_rotation", "Duval算法最小表示", "Duval Algorithm Minimal Rotation", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Lyndon Decomposition", "String Rotation"], 
                    "Duval算法用于Lyndon分解和字符串最小表示求解，时间复杂度线性。"),
    create_candidate("cand.string.runs_repetitions.basic", "Runs重复子串分析", "Runs and Repetitions Analysis", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["String Periodicity", "Suffix Automaton"], 
                    "Runs（最大重复子串）分析是字符串算法的重要研究方向，在周期性检测中有广泛应用。"),
    create_candidate("cand.string.border_tree.structure", "Border树结构", "Border Tree Structure", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["String Border", "Tree Data Structure"], 
                    "Border树是基于字符串的边界函数构建的树形结构，用于分析字符串的周期性和结构。"),
    
    # 哈希技术
    create_candidate("cand.string.hashing.2d_rolling_hash", "二维滚动哈希", "2D Rolling Hash", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Rolling Hash", "2D Arrays"], 
                    "二维滚动哈希用于处理二维字符串/矩阵的匹配和查询问题。"),
    create_candidate("cand.string.hashing.collision_strategy", "哈希碰撞处理策略", "Hash Collision Strategy", "算法", "intermediate", 
                    ["icpc", "advanced_string", "noi"], ["Rolling Hash", "Probability"], 
                    "处理字符串哈希碰撞的策略，包括双哈希、随机化哈希等防碰撞技术。"),
    
    # 更多字符串候选
    create_candidate("cand.string.manacher.algorithm", "Manacher算法", "Manacher Algorithm", "算法", "advanced", 
                    ["icpc", "advanced_string", "noi"], ["Palindrome", "String Matching"], 
                    "Manacher算法用于在线性时间内求解最长回文子串问题。"),
    create_candidate("cand.string.boyer_moore.algorithm", "Boyer-Moore算法", "Boyer-Moore Algorithm", "算法", "intermediate", 
                    ["icpc", "advanced_string", "noi"], ["String Matching", "Pattern Matching"], 
                    "Boyer-Moore算法是一种高效的字符串匹配算法，通过坏字符和好后缀规则进行跳转。"),
    create_candidate("cand.string.rabin_karp.algorithm", "Rabin-Karp算法", "Rabin-Karp Algorithm", "算法", "intermediate", 
                    ["icpc", "advanced_string", "noi"], ["String Matching", "Rolling Hash"], 
                    "Rabin-Karp算法基于哈希的字符串匹配算法，适合多模式匹配。"),
    create_candidate("cand.string.string_matching.kmp", "KMP算法详解", "KMP Algorithm Detailed", "算法", "intermediate", 
                    ["icpc", "advanced_string", "noi"], ["String Matching", "Greedy Algorithm"], 
                    "KMP算法的详细分析，包括next数组的构建和算法的正确性证明。"),
    create_candidate("cand.string.string_matching.sunday", "Sunday算法", "Sunday Algorithm", "算法", "intermediate", 
                    ["icpc", "advanced_string", "noi"], ["String Matching", "Pattern Matching"], 
                    "Sunday算法是一种简单的字符串匹配算法，在平均情况下性能优秀。"),
]

# 生成数学候选
math_candidates = [
    # 数论基础
    create_candidate("cand.math.prime_testing.miller_rabin", "Miller-Rabin素数测试", "Miller-Rabin Primality Test", "算法", "intermediate", 
                    ["icpc", "advanced_math", "noi"], ["Prime Numbers", "Modular Arithmetic"], 
                    "Miller-Rabin素数测试是一种概率性素数判断算法，速度快且准确率高。"),
    create_candidate("cand.math.prime_factorization.pollard_rho", "Pollard Rho分解", "Pollard Rho Factorization", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Prime Factorization", "Random Algorithm"], 
                    "Pollard Rho算法用于快速分解大整数的素因数，结合Miller-Rabin可用于完全分解。"),
    create_candidate("cand.math.primitive_root.basic", "原根基础", "Primitive Root Basic", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Modular Arithmetic", "Number Theory"], 
                    "原根的概念和计算，在离散对数问题中有重要应用。"),
    
    # 离散对数
    create_candidate("cand.math.discrete_log.bsgs", "BSGS离散对数", "BSGS Discrete Logarithm", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Discrete Logarithm", "Meet in the Middle"], 
                    "Baby Step Giant Step算法用于求解离散对数问题，时间复杂度O(sqrt(n))。"),
    create_candidate("cand.math.discrete_log.exbsgs", "扩展BSGS", "Extended BSGS", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["BSGS Discrete Logarithm", "GCD"], 
                    "扩展BSGS算法处理模数非素数情况下的离散对数问题。"),
    
    # 二次剩余
    create_candidate("cand.math.quadratic_residue.legendre_symbol", "Legendre符号", "Legendre Symbol", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Quadratic Residue", "Number Theory"], 
                    "Legendre符号用于判断一个数是否为二次剩余。"),
    create_candidate("cand.math.quadratic_residue.tonelli_shanks", "Tonelli-Shanks算法", "Tonelli-Shanks Algorithm", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Quadratic Residue", "Modular Arithmetic"], 
                    "Tonelli-Shanks算法用于求解二次剩余问题。"),
    
    # 数论函数
    create_candidate("cand.math.dirichlet_convolution.basic", "狄利克雷卷积基础", "Dirichlet Convolution Basic", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Number Theory Functions", "Convolution"], 
                    "狄利克雷卷积是数论中重要的运算，用于处理数论函数的组合。"),
    create_candidate("cand.math.mobius_inversion.applications", "莫比乌斯反演应用", "Mobius Inversion Applications", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Mobius Function", "Number Theory"], 
                    "莫比乌斯反演在计数问题中的广泛应用。"),
    create_candidate("cand.math.euler_function.applications", "欧拉函数应用", "Euler Function Applications", "算法", "intermediate", 
                    ["icpc", "advanced_math", "noi"], ["Euler Function", "Number Theory"], 
                    "欧拉函数在数论和密码学中的应用。"),
    
    # 筛法
    create_candidate("cand.math.sieve.du_jiao", "杜教筛", "Du Jiao Sieve", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Sieve Algorithm", "Prefix Sum"], 
                    "杜教筛用于快速计算数论函数的前缀和。"),
    create_candidate("cand.math.sieve.min_25", "Min_25筛", "Min_25 Sieve", "算法", "expert", 
                    ["icpc", "advanced_math", "university_cp"], ["Sieve Algorithm", "Number Theory Functions"], 
                    "Min_25筛是一种高效的筛法，可以快速计算积性函数的前缀和。"),
    
    # 组合数学
    create_candidate("cand.math.combinatorial.lucas", "Lucas定理", "Lucas Theorem", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Combinatorial Math", "Modular Arithmetic"], 
                    "Lucas定理用于计算大数组合数模素数。"),
    create_candidate("cand.math.combinatorial.exlucas", "扩展Lucas定理", "Extended Lucas Theorem", "算法", "expert", 
                    ["icpc", "advanced_math", "university_cp"], ["Lucas Theorem", "Chinese Remainder Theorem"], 
                    "扩展Lucas定理处理模数非素数情况下的组合数计算。"),
    create_candidate("cand.math.combinatorial.catalan", "Catalan数", "Catalan Number", "算法", "intermediate", 
                    ["icpc", "advanced_math", "noi"], ["Combinatorial Math", "Dynamic Programming"], 
                    "Catalan数的性质和应用，包括括号匹配、二叉树计数等。"),
    
    # 中国剩余定理
    create_candidate("cand.math.crt.basic", "中国剩余定理", "Chinese Remainder Theorem", "算法", "intermediate", 
                    ["icpc", "advanced_math", "noi"], ["Modular Arithmetic", "Number Theory"], 
                    "中国剩余定理用于求解同余方程组。"),
    create_candidate("cand.math.crt.extended", "扩展中国剩余定理", "Extended Chinese Remainder Theorem", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Chinese Remainder Theorem", "GCD"], 
                    "扩展中国剩余定理处理模数不互质的情况。"),
    create_candidate("cand.math.crt.garner", "Garner算法", "Garner Algorithm", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Chinese Remainder Theorem", "Number Theory"], 
                    "Garner算法是另一种求解同余方程组的高效方法。"),
    
    # 多项式算法
    create_candidate("cand.math.polynomial.fwt", "快速沃尔什变换", "Fast Walsh Transform", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Polynomial", "Divide and Conquer"], 
                    "快速沃尔什变换用于处理多项式的位运算卷积。"),
    create_candidate("cand.math.polynomial.subset_convolution", "子集卷积", "Subset Convolution", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Polynomial", "Bitmask DP"], 
                    "子集卷积用于处理集合幂级数的乘法运算。"),
    create_candidate("cand.math.polynomial.lagrange", "拉格朗日插值", "Lagrange Interpolation", "算法", "intermediate", 
                    ["icpc", "advanced_math", "noi"], ["Polynomial", "Numerical Method"], 
                    "拉格朗日插值法用于构造多项式，在数值计算中有广泛应用。"),
    create_candidate("cand.math.polynomial.berlekamp_massey", "Berlekamp-Massey算法", "Berlekamp-Massey Algorithm", "算法", "expert", 
                    ["icpc", "advanced_math", "university_cp"], ["Linear Recurrence", "Polynomial"], 
                    "Berlekamp-Massey算法用于求解线性递推关系的最小多项式。"),
    
    # 线性递推
    create_candidate("cand.math.linear_recurrence.basic", "线性递推基础", "Linear Recurrence Basic", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Matrix", "Number Theory"], 
                    "线性递推关系的求解方法，包括矩阵快速幂和特征多项式法。"),
    create_candidate("cand.math.linear_recurrence.kitamasa", "Kitamasa算法", "Kitamasa Algorithm", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Linear Recurrence", "Polynomial"], 
                    "Kitamasa算法用于快速计算线性递推关系的第n项。"),
    
    # 生成函数
    create_candidate("cand.math.generating_function.ordinary", "普通生成函数", "Ordinary Generating Function", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Combinatorial Math", "Calculus"], 
                    "普通生成函数在组合计数中的应用。"),
    create_candidate("cand.math.generating_function.exponential", "指数生成函数", "Exponential Generating Function", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Ordinary Generating Function", "Combinatorial Math"], 
                    "指数生成函数在排列计数中的应用。"),
    
    # 群论应用
    create_candidate("cand.math.group_theory.burnside", "Burnside引理", "Burnside Lemma", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Group Theory", "Combinatorial Math"], 
                    "Burnside引理用于计算不等价对象的数目。"),
    create_candidate("cand.math.group_theory.polya", "Polya计数定理", "Polya Counting Theorem", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Burnside Lemma", "Group Theory"], 
                    "Polya计数定理是Burnside引理的推广，用于处理更复杂的对称计数问题。"),
    
    # 图论数学
    create_candidate("cand.math.graph.matrix_tree", "矩阵树定理", "Matrix Tree Theorem", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Matrix", "Graph Theory"], 
                    "矩阵树定理用于计算图的生成树数目。"),
    create_candidate("cand.math.graph.gaussian_elimination_gf2", "GF(2)上的高斯消元", "Gaussian Elimination over GF(2)", "算法", "advanced", 
                    ["icpc", "advanced_math", "noi"], ["Gaussian Elimination", "Linear Algebra"], 
                    "在二进制域上应用高斯消元，解决异或方程组问题。"),
]

# 生成DP候选
dp_candidates = [
    # 数位DP
    create_candidate("cand.dp.digit.basic", "数位DP基础", "Digit DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Number Theory"], 
                    "数位动态规划用于处理数字范围的计数问题。"),
    create_candidate("cand.dp.digit.complex", "复杂数位DP", "Complex Digit DP", "算法", "expert", 
                    ["icpc", "advanced_dp", "university_cp"], ["Digit DP Basic", "State Design"], 
                    "复杂条件下的数位DP，包括多重限制和记忆化优化。"),
    
    # 树DP
    create_candidate("cand.dp.tree.basic", "树DP基础", "Tree DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Tree"], 
                    "树上动态规划的基本模式和应用。"),
    create_candidate("cand.dp.tree.diameter", "树的直径DP", "Tree Diameter DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Tree DP Basic", "Tree"], 
                    "使用动态规划求解树的直径相关问题。"),
    create_candidate("cand.dp.tree.centroid", "树的重心DP", "Tree Centroid DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Tree DP Basic", "Tree"], 
                    "树重心的计算和应用。"),
    create_candidate("cand.dp.tree.rerooting", "换根DP", "Rerooting DP", "算法", "expert", 
                    ["icpc", "advanced_dp", "university_cp"], ["Tree DP Basic", "Dynamic Programming"], 
                    "换根动态规划技术，用于处理树上所有节点的DP转移。"),
    
    # DAG DP
    create_candidate("cand.dp.dag.topological", "拓扑排序DP", "Topological Sort DP", "算法", "intermediate", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Graph"], 
                    "在DAG上按拓扑序进行动态规划。"),
    create_candidate("cand.dp.dag.longest_path", "DAG最长路DP", "DAG Longest Path DP", "算法", "intermediate", 
                    ["icpc", "advanced_dp", "noi"], ["Topological Sort DP", "Graph"], 
                    "在DAG上求最长路的相关DP技术。"),
    
    # 状态压缩DP
    create_candidate("cand.dp.state_compression.basic", "状态压缩DP基础", "State Compression DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Bitmask"], 
                    "使用位运算压缩状态的动态规划技术。"),
    create_candidate("cand.dp.state_compression.traveling", "旅行商问题DP", "Traveling Salesman Problem DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["State Compression DP Basic", "Graph"], 
                    "使用状态压缩DP解决旅行商问题。"),
    
    # 集合DP
    create_candidate("cand.dp.subset.basic", "子集DP基础", "Subset DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["State Compression DP Basic", "Set"], 
                    "基于子集的动态规划技术。"),
    create_candidate("cand.dp.subset.enumeration", "子集枚举优化", "Subset Enumeration Optimization", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Subset DP Basic", "Bitmask"], 
                    "子集枚举的高效实现和优化技巧。"),
    
    # 轮廓DP
    create_candidate("cand.dp.profile.basic", "轮廓DP基础", "Profile DP Basic", "算法", "expert", 
                    ["icpc", "advanced_dp", "university_cp"], ["State Compression DP Basic", "Grid"], 
                    "轮廓DP用于处理网格问题中的复杂状态转移。"),
    create_candidate("cand.dp.profile.plug", "插头DP基础", "Plug DP Basic", "算法", "expert", 
                    ["icpc", "advanced_dp", "university_cp"], ["Profile DP Basic", "State Compression"], 
                    "插头DP是一种特殊的轮廓DP，用于处理连通性约束。"),
    
    # 自动机DP
    create_candidate("cand.dp.automaton.basic", "自动机DP基础", "Automaton DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Automata"], 
                    "在自动机结构上进行动态规划。"),
    create_candidate("cand.dp.automaton.matrix", "自动机矩阵DP", "Automaton Matrix DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Automaton DP Basic", "Matrix"], 
                    "使用矩阵快速幂优化自动机DP。"),
    
    # 概率DP
    create_candidate("cand.dp.probability.basic", "概率DP基础", "Probability DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Probability"], 
                    "处理概率问题的动态规划方法。"),
    create_candidate("cand.dp.probability.expectation", "期望DP", "Expectation DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Probability DP Basic", "Expected Value"], 
                    "计算期望值的动态规划技术。"),
    create_candidate("cand.dp.probability.markov", "马尔可夫链DP", "Markov Chain DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Probability DP Basic", "Matrix"], 
                    "马尔可夫链模型的动态规划求解。"),
    
    # 博弈DP
    create_candidate("cand.dp.game.basic", "博弈DP基础", "Game DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Game Theory"], 
                    "博弈论问题的动态规划求解方法。"),
    create_candidate("cand.dp.game.grundy", "Grundy数DP", "Grundy Number DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Game DP Basic", "Nim Game"], 
                    "Grundy数在组合博弈中的应用。"),
    
    # 单调队列优化
    create_candidate("cand.dp.optimization.monotone_queue", "单调队列优化", "Monotone Queue Optimization", "算法", "intermediate", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Monotone Queue"], 
                    "使用单调队列优化DP转移。"),
    create_candidate("cand.dp.optimization.monotone_queue_sliding", "滑动窗口DP", "Sliding Window DP", "算法", "intermediate", 
                    ["icpc", "advanced_dp", "noi"], ["Monotone Queue Optimization", "Dynamic Programming"], 
                    "滑动窗口模型的动态规划优化。"),
    
    # 斜率优化
    create_candidate("cand.dp.optimization.slope.basic", "斜率优化基础", "Slope Optimization Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Convex Hull"], 
                    "斜率优化用于优化特定形式的DP转移。"),
    create_candidate("cand.dp.optimization.slope.advanced", "斜率优化高级", "Slope Optimization Advanced", "算法", "expert", 
                    ["icpc", "advanced_dp", "university_cp"], ["Slope Optimization Basic", "Dynamic Programming"], 
                    "复杂的斜率优化技巧，包括维护凸包和处理边界情况。"),
    
    # 分治优化
    create_candidate("cand.dp.optimization.divide_conquer", "分治DP优化", "Divide and Conquer DP Optimization", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Divide and Conquer"], 
                    "使用分治思想优化DP转移。"),
    
    # Knuth优化
    create_candidate("cand.dp.optimization.knuth", "Knuth优化", "Knuth Optimization", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Optimization"], 
                    "Knuth优化用于满足特定条件的四边形不等式DP优化。"),
    
    # WQS二分
    create_candidate("cand.dp.optimization.wqs_binary", "WQS二分优化", "WQS Binary Search Optimization", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Binary Search", "Dynamic Programming"], 
                    "WQS（Williamson–Shmoys）二分用于优化具有约束的DP问题。"),
    
    # 矩阵DP
    create_candidate("cand.dp.matrix.basic", "矩阵DP基础", "Matrix DP Basic", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Dynamic Programming", "Matrix"], 
                    "使用矩阵乘法优化DP转移。"),
    create_candidate("cand.dp.matrix.fast_power", "矩阵快速幂DP", "Matrix Fast Power DP", "算法", "advanced", 
                    ["icpc", "advanced_dp", "noi"], ["Matrix DP Basic", "Binary Exponentiation"], 
                    "结合矩阵快速幂处理具有线性递推关系的DP问题。"),
]

# 合并所有候选
all_candidates = string_candidates + math_candidates + dp_candidates

# 写入JSON文件
with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\external_candidate_pool_batch2_string_math_dp.json', 'w', encoding='utf-8') as f:
    json.dump(all_candidates, f, ensure_ascii=False, indent=2)

print(f"生成了 {len(all_candidates)} 个候选")
print(f"字符串候选: {len(string_candidates)} 个")
print(f"数学候选: {len(math_candidates)} 个")
print(f"DP候选: {len(dp_candidates)} 个")