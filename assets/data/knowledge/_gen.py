import json

data = {
    "meta": {
        "title": "IO知识点_修正版_依赖标记版_v4.4",
        "encoding": "UTF-8",
        "categories_count": 5
    },
    "categories": []
}

def mk_item(item_id, name, parent, direct_pre=None, resolved_pre=None, rel=None, alias=None):
    return {
        "id": item_id,
        "name": name,
        "alias": alias or [],
        "parent": parent,
        "direct_pre": direct_pre or [],
        "resolved_pre": resolved_pre or [],
        "rel": rel or [],
        "block_id": "",
        "block_name": "",
        "pickup_group": "",
        "pickup_group_name": "",
        "pickup_order": 1
    }

def mk_section(sec_id, name, level, pre=None, rel=None, items=None):
    return {
        "id": sec_id,
        "name": name,
        "level": level,
        "pre": pre or [],
        "rel": rel or [],
        "items": items or []
    }

def chain_items(parent_id, names_aliases, resolved_pre=None):
    items = []
    for i, (name, alias) in enumerate(names_aliases):
        dp = [parent_id + "." + str(i)] if i > 0 else []
        iid = parent_id + "." + str(i + 1)
        items.append(mk_item(iid, name, parent_id, dp, resolved_pre=resolved_pre, alias=alias))
    return items

# ============ Category 1: C++语法 ============
cat1_sections = []

cat1_sections.append(mk_section("1.1", "程序基本结构", "L1",
    items=chain_items("1.1", [
        ("#include", []), ("using namespace std", []), ("main函数", []),
        ("语句与分号", []), ("代码块与大括号", []), ("注释", []),
        ("return 0", []), ("头文件基础", []), ("编译与运行基础", [])
    ])))

cat1_sections.append(mk_section("1.2", "输入输出", "L1",
    items=chain_items("1.2", [
        ("cin输入", []), ("cout输出", []), ("格式化输出", []), ("读写文件基础", [])
    ])))

cat1_sections.append(mk_section("1.3", "变量与数据类型", "L1",
    items=chain_items("1.3", [
        ("整数类型", []), ("浮点数类型", []), ("字符类型", []),
        ("布尔类型", []), ("类型转换", []), ("常量与宏定义", [])
    ])))

cat1_sections.append(mk_section("1.4", "运算符与表达式", "L1",
    items=chain_items("1.4", [
        ("算术运算", []), ("比较运算", []), ("逻辑运算", []),
        ("位运算", []), ("赋值运算", []), ("运算符优先级", [])
    ])))

cat1_sections.append(mk_section("1.5", "数组与字符串", "L1", pre=["1.3"],
    items=chain_items("1.5", [
        ("数组基础", []), ("二维数组", []), ("vector", []),
        ("字符数组", []), ("string类", []), ("数组越界", [])
    ], resolved_pre=["1.3.1", "1.3.5"])))

cat1_sections.append(mk_section("1.6", "控制结构", "L1", pre=["1.4"],
    items=chain_items("1.6", [
        ("if分支", []), ("switch语句", []), ("for循环", []),
        ("while循环", []), ("do-while循环", []), ("break和continue", []), ("嵌套循环", [])
    ], resolved_pre=["1.4.2", "1.4.3"])))

cat1_sections.append(mk_section("1.7", "函数", "L1", pre=["1.6"],
    items=chain_items("1.7", [
        ("函数定义", []), ("参数传递", []), ("返回值", []),
        ("递归函数", []), ("函数重载", []), ("变量作用域", [])
    ], resolved_pre=["1.6.1", "1.6.3"])))

cat1_sections.append(mk_section("1.8", "STL基础", "L2", pre=["1.5", "1.7"],
    items=chain_items("1.8", [
        ("sort", []), ("lower_bound/upper_bound", []), ("min/max/swap", []),
        ("reverse/unique", []), ("accumulate/fill", [])
    ], resolved_pre=["1.5.1", "1.5.3", "1.7.1"])))

cat1_sections.append(mk_section("1.9", "结构体与枚举", "L1", pre=["1.3"],
    items=chain_items("1.9", [
        ("struct定义", []), ("结构体数组", []), ("结构体排序", []), ("enum枚举", [])
    ], resolved_pre=["1.3.1", "1.3.5"])))

cat1_sections.append(mk_section("1.10", "指针与引用", "L2", pre=["1.7"],
    items=chain_items("1.10", [
        ("指针基础", []), ("引用", []), ("指针与数组", []), ("动态内存", [])
    ], resolved_pre=["1.7.1", "1.7.2"])))

data["categories"].append({"name": "C++语法", "sections": cat1_sections})

# ============ Category 2: 算法 ============
cat2_sections = []

cat2_sections.append(mk_section("2.1", "基础算法思想", "L1",
    items=chain_items("2.1", [
        ("枚举", []), ("模拟", []), ("递推", []), ("递归", []), ("分治", []),
        ("倍增", []), ("构造", []), ("离线思想", []), ("启发式基础", []), ("随机化基础", [])
    ])))

cat2_sections.append(mk_section("2.2", "排序与顺序统计", "L1", pre=["2.1"],
    items=chain_items("2.2", [
        ("冒泡排序", []), ("选择排序", []), ("插入排序", []), ("归并排序", []),
        ("快速排序", []), ("堆排序", []), ("计数排序", []), ("桶排序", []),
        ("基数排序", []), ("sort函数", []), ("逆序对统计", [])
    ], resolved_pre=["2.1.1", "2.1.5"])))

cat2_sections.append(mk_section("2.3", "二分与答案搜索", "L1", pre=["2.1"],
    items=chain_items("2.3", [
        ("二分查找基础", []), ("lower_bound/upper_bound", []),
        ("二分答案", []), ("实数二分", [])
    ], resolved_pre=["2.1.5"])))

cat2_sections.append(mk_section("2.4", "贪心", "L1", pre=["2.1"],
    items=chain_items("2.4", [
        ("贪心基础", []), ("区间贪心", []), ("哈夫曼编码", [])
    ], resolved_pre=["2.1.1", "2.1.2"])))

cat2_sections.append(mk_section("2.5", "动态规划", "L2", pre=["2.1", "2.3"],
    items=chain_items("2.5", [
        ("DP基础", []), ("背包DP", []), ("线性DP", []),
        ("区间DP", []), ("树形DP", []), ("状态压缩DP", [])
    ], resolved_pre=["2.1.3", "2.1.4", "2.3.3"])))

cat2_sections.append(mk_section("2.6", "图论算法", "L2", pre=["2.7"],
    items=chain_items("2.6", [
        ("最短路Dijkstra", []), ("最短路Floyd", []), ("最小生成树", []), ("二分图", [])
    ], resolved_pre=["2.7.2", "2.7.4"])))

cat2_sections.append(mk_section("2.7", "搜索与回溯", "L1", pre=["2.1"],
    items=[
        mk_item("2.7.1", "递归基础", "2.7", alias=["递归", "recursion"],
            direct_pre=[], resolved_pre=["2.1.4"], rel=[]),
        mk_item("2.7.2", "DFS基础", "2.7", alias=["深度优先搜索", "DFS", "depth-first search"],
            direct_pre=["2.7.1"], resolved_pre=["2.7.1"], rel=[]),
        mk_item("2.7.3", "网格DFS", "2.7", alias=["网格搜索", "岛屿问题", "grid DFS"],
            direct_pre=["2.7.2"], resolved_pre=["2.7.2"], rel=[]),
        mk_item("2.7.4", "树与图DFS", "2.7", alias=["树DFS", "图DFS", "树的遍历", "tree DFS"],
            direct_pre=["2.7.2"], resolved_pre=["2.7.2"], rel=["3.9.4"]),
        mk_item("2.7.5", "BFS基础", "2.7", alias=["广度优先搜索", "BFS", "breadth-first search"],
            direct_pre=["2.7.2"], resolved_pre=["2.7.2"], rel=[]),
        mk_item("2.7.6", "回溯枚举", "2.7", alias=["回溯", "backtracking", "子集", "排列", "组合"],
            direct_pre=["2.7.2"], resolved_pre=["2.7.2"], rel=[]),
        mk_item("2.7.7", "剪枝优化", "2.7", alias=["剪枝", "pruning", "搜索优化"],
            direct_pre=["2.7.6"], resolved_pre=["2.7.6"], rel=[]),
        mk_item("2.7.8", "记忆化搜索", "2.7", alias=["memo", "记忆化", "memoization", "自顶向下DP"],
            direct_pre=["2.7.2"], resolved_pre=["2.7.2"], rel=["2.5.1"]),
    ]))

data["categories"].append({"name": "算法", "sections": cat2_sections})

# ============ Category 3: 数据结构 ============
cat3_sections = []

cat3_sections.append(mk_section("3.1", "线性结构", "L1", pre=["2.1"],
    items=chain_items("3.1", [
        ("数组", ["array"]), ("字符数组", ["char[]", "C字符串"]),
        ("字符串string", ["string", "C++字符串"]),
        ("链表", ["linked list", "单链表"]),
        ("双向链表", ["doubly linked list"]),
        ("静态链表", ["数组模拟链表"])
    ], resolved_pre=["2.1.1", "2.1.2"])))

cat3_sections.append(mk_section("3.2", "栈与队列", "L1", pre=["3.1"],
    items=chain_items("3.2", [
        ("栈", ["stack", "LIFO"]), ("队列", ["queue", "FIFO"]),
        ("双端队列", ["deque"]), ("单调栈", ["monotonic stack"]),
        ("单调队列", ["monotonic queue"])
    ], resolved_pre=["3.1.1", "3.1.4"])))

cat3_sections.append(mk_section("3.3", "集合与映射", "L1", pre=["3.1"],
    items=chain_items("3.3", [
        ("set", ["集合", "有序集合"]), ("multiset", ["多重集合"]),
        ("map", ["映射", "字典", "键值对"]), ("pair", ["二元组"]),
        ("tuple", ["元组", "多元组"]),
        ("unordered_map / unordered_set", ["哈希表", "hash"])
    ], resolved_pre=["3.1.1"])))

cat3_sections.append(mk_section("3.4", "并查集", "L2", pre=["3.1"], rel=["3.2"],
    items=chain_items("3.4", [
        ("基本并查集", ["union-find", "DSU"]),
        ("路径压缩", ["path compression"]),
        ("按秩/按大小合并", ["union by rank", "union by size"])
    ], resolved_pre=["3.1.1", "3.1.4"])))

cat3_sections.append(mk_section("3.5", "堆", "L2", pre=["3.1"], rel=["2.2"],
    items=chain_items("3.5", [
        ("二叉堆基础", ["priority_queue", "优先队列"]),
        ("手写堆", ["heap", "大根堆", "小根堆"])
    ], resolved_pre=["3.1.1", "2.2.6"])))

cat3_sections.append(mk_section("3.6", "树结构", "L2", pre=["3.1", "2.1"], rel=["2.7"],
    items=chain_items("3.6", [
        ("二叉树基础", ["binary tree"]),
        ("树的存储与遍历", ["树遍历", "DFS树"]),
        ("LCA最近公共祖先", ["LCA", "最近公共祖先"])
    ], resolved_pre=["3.1.1", "2.1.4", "2.1.5"])))

cat3_sections.append(mk_section("3.7", "树状数组", "L2", pre=["3.1", "2.3"],
    items=chain_items("3.7", [
        ("树状数组BIT", ["BIT", "Fenwick Tree", "fenwick"]),
        ("树状数组求逆序对", ["BIT逆序对"]),
        ("二维树状数组", ["2D BIT"]),
        ("树状数组维护区间最值", ["BIT最值"])
    ], resolved_pre=["3.1.1", "2.3.1"])))

cat3_sections.append(mk_section("3.8", "线段树", "L3", pre=["3.1", "2.1"], rel=["3.7"],
    items=chain_items("3.8", [
        ("线段树基础", ["segment tree"]), ("懒标记", ["lazy tag", "懒标记线段树"]),
        ("线段树求区间最值", ["RMQ", "线段树RMQ"]),
        ("线段树维护区间赋值", ["区间赋值线段树"]),
        ("线段树扫描线", ["扫描线", "矩形面积并"])
    ], resolved_pre=["3.1.1", "2.1.5"])))

cat3_sections.append(mk_section("3.9", "图的存储与遍历", "L2", pre=["3.1", "2.7"],
    items=chain_items("3.9", [
        ("图的邻接表存储", ["adjacency list"]),
        ("图的邻接矩阵存储", ["adjacency matrix"]),
        ("链式前向星", ["forward star"]),
        ("图的DFS遍历", ["图DFS"]),
        ("图的BFS遍历", ["图BFS"]),
        ("拓扑排序", ["topological sort", "Kahn"])
    ], resolved_pre=["3.1.1", "2.7.4", "2.7.5"])))

cat3_sections.append(mk_section("3.10", "平衡树与STL容器", "L3", pre=["3.3", "3.6"],
    items=chain_items("3.10", [
        ("平衡树简介", ["balanced tree", "AVL", "红黑树"]),
        ("pb_ds扩展容器", ["pbds", "policy based"]),
        ("Treap简介", ["treap", "树堆"]),
        ("FHQ Treap", ["无旋Treap", "分裂合并Treap"])
    ], resolved_pre=["3.3.1", "3.3.3", "3.6.1"])))

cat3_sections.append(mk_section("3.11", "哈希", "L2", pre=["3.3"],
    items=chain_items("3.11", [
        ("哈希表原理", ["hash table", "散列表"]),
        ("字符串哈希", ["string hash", "滚动哈希"]),
        ("哈希冲突处理", ["collision resolution"]),
        ("离散化", ["coordinate compression", "坐标压缩"])
    ], resolved_pre=["3.3.1", "3.3.6"])))

cat3_sections.append(mk_section("3.12", "高级数据结构进阶", "L3", pre=["3.7", "3.8"], rel=["3.10"],
    items=chain_items("3.12", [
        ("ST表", ["Sparse Table", "稀疏表"]),
        ("分块", ["sqrt decomposition", "根号分块"]),
        ("莫队算法", ["Mo's algorithm"]),
        ("字典树Trie", ["Trie", "前缀树"]),
        ("KMP算法", ["KMP", "模式匹配"])
    ], resolved_pre=["3.7.1", "3.8.1"])))

data["categories"].append({"name": "数据结构", "sections": cat3_sections})

# ============ Category 4: 算法竞赛数学 ============
cat4_sections = []

cat4_sections.append(mk_section("4.1", "数论基础", "L2",
    items=chain_items("4.1", [
        ("整除与取模", []), ("最大公约数GCD", []), ("素数判定", []),
        ("素因子分解", []), ("快速幂", [])
    ])))

cat4_sections.append(mk_section("4.2", "组合数学", "L2",
    items=chain_items("4.2", [
        ("排列组合", []), ("杨辉三角", []), ("二项式定理", []), ("容斥原理", [])
    ])))

cat4_sections.append(mk_section("4.3", "概率与期望", "L2",
    items=chain_items("4.3", [
        ("古典概型", []), ("条件概率", []), ("期望基础", [])
    ])))

data["categories"].append({"name": "算法竞赛数学", "sections": cat4_sections})

# ============ Category 5: C++编程/调试技巧 ============
cat5_sections = []

cat5_sections.append(mk_section("5.1", "调试技巧", "L2",
    items=chain_items("5.1", [
        ("常见编译错误", []), ("常见运行时错误", []), ("断点调试", []), ("输出调试", [])
    ])))

cat5_sections.append(mk_section("5.2", "编码规范", "L2",
    items=chain_items("5.2", [
        ("变量命名", []), ("代码格式", []), ("注释规范", [])
    ])))

cat5_sections.append(mk_section("5.3", "竞赛技巧", "L2",
    items=chain_items("5.3", [
        ("读题技巧", []), ("对拍方法", []), ("暴力对拍", []), ("特判处理", [])
    ])))

data["categories"].append({"name": "C++编程/调试技巧", "sections": cat5_sections})

out_path = r"C:\Users\rr\Documents\trae_projects\suanfatong\assets\data\knowledge\io_v4_4.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done. Verifying...")

with open(out_path, "r", encoding="utf-8") as f:
    d = json.load(f)

total_items = 0
total_sections = 0
for cat in d["categories"]:
    for sec in cat["sections"]:
        total_sections += 1
        total_items += len(sec["items"])

print("Categories: " + str(len(d["categories"])))
print("Sections: " + str(total_sections))
print("Items: " + str(total_items))
cat_names = [c["name"] for c in d["categories"]]
print("Category names: " + str(cat_names))
print("JSON is valid!")
