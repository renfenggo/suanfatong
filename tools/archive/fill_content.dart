import 'dart:convert';
import 'dart:io';

void main() async {
  final updates = <String, Map<String, Map<String, dynamic>>>{};

  final f2_3 = 'assets/data/algorithm/section_2_3_units.json';
  updates[f2_3] = {
    '2.3.5': {
      'itemId': '2.3.5',
      'title': '实数二分',
      'learningGoal': '掌握实数域上的二分搜索方法，能正确处理精度和终止条件',
      'explanation': '实数二分在连续值域上搜索答案，与整数二分不同之处：\n\n1. 终止条件：用固定迭代次数（推荐 80~100 次）或精度 eps\n2. 不需要 +1/-1 的调整\n3. 中值直接取 (l+r)/2\n\n两种写法：\n- for 循环固定次数：简单可靠，100 次精度约 10^-30\n- while (r-l > eps)：eps 取题目要求精度多 2 位\n\n典型应用：\n- 求方程的根\n- 几何中的距离/角度优化\n- 物理模拟中的参数搜索\n\n注意：输出时用 printf(\"%.nf\") 控制精度。',
      'exampleCode': '#include <iostream>\n#include <cstdio>\nusing namespace std;\n\nint main() {\n    double l = 1, r = 2;\n    for (int i = 0; i < 100; i++) {\n        double mid = (l + r) / 2;\n        if (mid * mid < 2) l = mid;\n        else r = mid;\n    }\n    printf("%.6f\\n", l);\n    return 0;\n}',
      'codeNotes': [
        '实数二分不需要 +1/-1',
        '推荐固定 100 次迭代',
        '100 次迭代精度约 10^-30',
        '输出用 printf 控制小数位数'
      ],
      'commonMistakes': [
        {
          'title': 'eps 设太大精度不够',
          'description': '题目要求 6 位小数但 eps 只设了 1e-4。',
          'fix': 'eps 一般比要求精度多 2 位，或直接用固定次数迭代。'
        },
        {
          'title': '用 cout 输出精度不够',
          'description': 'cout 默认只输出 6 位有效数字。',
          'fix': '用 printf("%.nf", ans) 控制小数位数。'
        }
      ],
      'practice': {
        'prompt': '用实数二分求 sqrt(3) 的值，精确到小数点后 6 位。',
        'hint': '二分 [1, 2]，判断 mid*mid 与 3 的关系。',
        'expectedIdea': 'double l=1, r=2; for(100次) if(mid*mid<3) l=mid; else r=mid;'
      },
      'quiz': [
        {
          'question': '实数二分中，固定迭代 100 次的精度约为？',
          'options': ['10^-6', '10^-10', '10^-30', '10^-100'],
          'answerIndex': 2,
          'explanation': '每次迭代范围缩小一半，100 次后范围缩小 2^-100 ≈ 10^-30。'
        }
      ]
    },
    '2.3.6': {
      'itemId': '2.3.6',
      'title': '二分答案',
      'learningGoal': '掌握二分答案框架，学会将最优化问题转化为判定问题求解',
      'explanation': '二分答案是竞赛中极常用的技巧：当答案具有单调性时，可以二分搜索最优解。\n\n核心思想：\n- 如果「答案为 x 可行」这个条件关于 x 单调（x 越大越容易/越难可行），就能二分\n- 把「求最优解」转化为「判断某个值是否可行」\n\n框架：\n1. 确定答案范围 [L, R]\n2. while (L < R) { mid = ...; if (check(mid)) 更新一侧 else 更新另一侧 }\n3. 输出 L 或 R\n\ncheck() 函数是关键：给定一个候选答案，判断是否可行。\n\n典型题型：\n- 最小化最大值（如最大跳跃距离最小化）\n- 最大化最小值（如最近点对距离最大化）\n- 第 k 大/小问题',
      'exampleCode': '#include <iostream>\nusing namespace std;\n\nint n, k;\nint a[100005];\n\nbool check(int len) {\n    int cnt = 0;\n    for (int i = 0; i < n; i++)\n        cnt += a[i] / len;\n    return cnt >= k;\n}\n\nint main() {\n    cin >> n >> k;\n    for (int i = 0; i < n; i++) cin >> a[i];\n    int l = 1, r = 100000000;\n    while (l < r) {\n        int mid = (l + r + 1) / 2;\n        if (check(mid)) l = mid;\n        else r = mid - 1;\n    }\n    cout << l << endl;\n    return 0;\n}',
      'codeNotes': [
        '二分答案需要答案满足单调性',
        'check(mid) 判断候选答案是否可行',
        '求最大可行解用 l=mid, mid=(l+r+1)/2',
        '求最小可行解用 r=mid, mid=(l+r)/2'
      ],
      'commonMistakes': [
        {
          'title': '二分模板选错导致死循环',
          'description': '用 l=mid 但 mid=(l+r)/2，当 l=r-1 时死循环。',
          'fix': 'l=mid 时必须用 mid=(l+r+1)/2 向上取整。'
        },
        {
          'title': 'check 函数逻辑写反',
          'description': '可行性判断的方向搞反了。',
          'fix': '先手动验证 check(l) 和 check(r) 的结果是否符合预期。'
        }
      ],
      'practice': {
        'prompt': 'n 根木头，长度分别为 a[i]，要锯出 k 根等长的木头，求最大长度。',
        'hint': '二分答案 mid，check: 统计所有木头能切出的段数之和 >= k。',
        'expectedIdea': 'check(mid): sum(a[i]/mid) >= k'
      },
      'quiz': [
        {
          'question': '二分答案适用的前提是？',
          'options': ['数据规模小', '答案具有单调性', '必须是整数', '只能求最大值'],
          'answerIndex': 1,
          'explanation': '答案必须关于判定条件单调，即答案越大/小，越容易（或越难）满足条件。'
        }
      ]
    },
    '2.3.7': {
      'itemId': '2.3.7',
      'title': '单调性判定',
      'learningGoal': '理解单调性在二分答案中的核心作用，学会分析问题是否可二分',
      'explanation': '单调性是二分答案的核心前提：如果答案从小到大，判定函数 check(x) 的结果单调变化（从可行变为不可行，或反过来），则可以二分。\n\n常见的单调性模式：\n1. 最小化最大值：答案越大越容易满足 check → 找最小可行解\n2. 最大化最小值：答案越大越难满足 check → 找最大可行解\n3. 计数类：答案越大，满足条件的数越少\n\n如何判断单调性：\n- 如果 check(x) 为 true 能推出 check(x-1) 也为 true（或反之），则具有单调性\n- 画图分析：x 轴为答案，y 轴为 check 结果，应该是「一段 true 一段 false」\n\n注意：不是所有最优化问题都有单调性！比如 NP-hard 问题通常不能二分。',
      'exampleCode': '#include <iostream>\nusing namespace std;\n\nint a[100005];\nint n, m;\n\nbool check(int maxSum) {\n    int cnt = 1, sum = 0;\n    for (int i = 0; i < n; i++) {\n        if (sum + a[i] > maxSum) {\n            cnt++;\n            sum = a[i];\n        } else {\n            sum += a[i];\n        }\n    }\n    return cnt <= m;\n}\n\nint main() {\n    cin >> n >> m;\n    for (int i = 0; i < n; i++) cin >> a[i];\n    int l = 1, r = 1e9;\n    while (l < r) {\n        int mid = (l + r) / 2;\n        if (check(mid)) r = mid;\n        else l = mid + 1;\n    }\n    cout << l << endl;\n    return 0;\n}',
      'codeNotes': [
        'check(x) 关于 x 单调是二分前提',
        '最小化最大值：check 越大越容易为 true',
        '最大化最小值：check 越大越容易为 false',
        '画图检验：true/false 应各占连续一段'
      ],
      'commonMistakes': [
        {
          'title': '误判单调性',
          'description': '没有验证 check 的单调性就直接二分，可能得到错误答案。',
          'fix': '先手动验证几个 check 值，确认 true/false 是否各占一段。'
        }
      ],
      'practice': {
        'prompt': '将数组分成 m 段，使每段之和的最大值最小。判断此问题是否具有单调性。',
        'hint': '分析：最大值上限越大，需要的段数越少（单调）。',
        'expectedIdea': 'check(mid) = 是否能在 m 段内分完，mid 越大越容易为 true。'
      },
      'quiz': [
        {
          'question': '以下哪种情况说明问题可以二分答案？',
          'options': [
            'check(3)=true, check(5)=false, check(4)=true',
            'check(1)=true, check(2)=true, check(3)=false, check(4)=false',
            'check 的结果全是 true',
            'check 的结果与答案无关'
          ],
          'answerIndex': 1,
          'explanation': 'check 结果从 true 变为 false 且不回头，说明具有单调性，可以二分。'
        }
      ]
    },
    '2.3.8': {
      'itemId': '2.3.8',
      'title': 'check 函数设计',
      'learningGoal': '掌握二分答案中 check 函数的设计方法，能正确实现判定逻辑',
      'explanation': 'check 函数是二分答案的核心：给定候选答案 mid，判断该答案是否可行。\n\n设计原则：\n1. check(mid) 返回 bool：mid 作为候选答案是否满足条件\n2. check 必须与答案单调性配合\n3. check 的时间复杂度决定整体效率（总复杂度 = O(logV × check复杂度)）\n\n常见 check 设计模式：\n- 贪心验证：按贪心策略检查 mid 是否可行\n- 计数验证：统计满足条件的数量是否达标\n- 模拟验证：模拟过程看 mid 是否满足要求\n\ncheck 方向约定：\n- 求最小值：check(mid) = true 时 r=mid，找第一个 true\n- 求最大值：check(mid) = true 时 l=mid，找最后一个 true',
      'exampleCode': '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint n, c;\nint a[100005];\n\nbool check(int dist) {\n    int cnt = 1, last = a[0];\n    for (int i = 1; i < n; i++) {\n        if (a[i] - last >= dist) {\n            cnt++;\n            last = a[i];\n        }\n    }\n    return cnt >= c;\n}\n\nint main() {\n    cin >> n >> c;\n    for (int i = 0; i < n; i++) cin >> a[i];\n    sort(a, a + n);\n    int l = 1, r = a[n-1] - a[0];\n    while (l < r) {\n        int mid = (l + r + 1) / 2;\n        if (check(mid)) l = mid;\n        else r = mid - 1;\n    }\n    cout << l << endl;\n    return 0;\n}',
      'codeNotes': [
        'check 接收候选答案 mid',
        '返回 bool 表示 mid 是否可行',
        '常用贪心/计数/模拟实现',
        '总复杂度 = O(logV × check复杂度)'
      ],
      'commonMistakes': [
        {
          'title': 'check 中贪心策略错误',
          'description': 'check 内部的贪心判断不正确，导致整体答案错误。',
          'fix': '单独测试 check 函数，手动验证几个 case。'
        },
        {
          'title': 'check 方向与二分模板不匹配',
          'description': 'check 返回 true 时应该更新 l 还是 r 搞混了。',
          'fix': '求最大值：check(mid)=true → l=mid；求最小值：check(mid)=true → r=mid。'
        }
      ],
      'practice': {
        'prompt': '在数轴上放 c 头牛，使最近两头牛的距离最大。设计 check 函数。',
        'hint': 'check(dist): 贪心放置，看能否放 c 头牛。',
        'expectedIdea': '从左到右贪心放牛，如果当前牛与上一头距离 >= dist 就放。'
      },
      'quiz': [
        {
          'question': '二分答案的总时间复杂度取决于什么？',
          'options': ['仅取决于答案范围大小', 'O(logV × check复杂度)', '仅取决于 check 的复杂度', 'O(n log n)'],
          'answerIndex': 1,
          'explanation': '二分共执行 O(logV) 次 check，总复杂度 = 二分次数 × check 复杂度。'
        }
      ]
    },
    '2.3.9': {
      'itemId': '2.3.9',
      'title': '三分法',
      'learningGoal': '掌握三分法求单峰/单谷函数极值的原理和实现',
      'explanation': '三分法用于求单峰函数的极大值或单谷函数的极小值。\n\n原理：\n- 在 [l, r] 内取两个三分点 m1 = l + (r-l)/3, m2 = r - (r-l)/3\n- 比较 f(m1) 和 f(m2) 的值\n- 求极大值：如果 f(m1) < f(m2)，则极值在 [m1, r]，令 l = m1\n- 求极小值：如果 f(m1) > f(m2)，则极值在 [m1, r]，令 l = m1\n\n应用场景：\n- 几何问题中的距离极值\n- 函数最值\n- 物理模拟优化\n\n注意：三分法要求函数是严格单峰/单谷的。和实数二分类似，用固定次数迭代控制精度。',
      'exampleCode': '#include <iostream>\n#include <cmath>\nusing namespace std;\n\ndouble f(double x) {\n    return -(x - 2) * (x - 2) + 3;\n}\n\nint main() {\n    double l = -100, r = 100;\n    for (int i = 0; i < 100; i++) {\n        double m1 = l + (r - l) / 3;\n        double m2 = r - (r - l) / 3;\n        if (f(m1) < f(m2)) l = m1;\n        else r = m2;\n    }\n    printf("%.6f\\n", l);\n    return 0;\n}',
      'codeNotes': [
        'm1 = l + (r-l)/3, m2 = r - (r-l)/3',
        '求极大值：f(m1)<f(m2) 则 l=m1',
        '求极小值：f(m1)>f(m2) 则 l=m1',
        '每次缩小 1/3 的范围'
      ],
      'commonMistakes': [
        {
          'title': '函数不是单峰就使用三分',
          'description': '函数有多个极值点时三分法可能找到局部极值而非全局。',
          'fix': '确认函数是单峰/单谷的，或者使用其他方法。'
        }
      ],
      'practice': {
        'prompt': '求函数 f(x) = -x^2 + 4x + 1 的最大值及取最大值时的 x。',
        'hint': '三分 [−100, 100]，比较 f(m1) 和 f(m2)。',
        'expectedIdea': '三分求极大值，x=2 时 f(x)=5 最大。'
      },
      'quiz': [
        {
          'question': '三分法每次迭代将搜索范围缩小多少？',
          'options': ['1/2', '1/3', '2/3', '1/4'],
          'answerIndex': 1,
          'explanation': '每次比较两个三分点后，范围缩小为原来的 2/3，即去掉了 1/3。'
        }
      ]
    },
  };

  final f2_6 = 'assets/data/algorithm/section_2_6_units.json';
  updates[f2_6] = {
    '2.6.5': {
      'itemId': '2.6.5',
      'title': '局部最优到全局最优',
      'learningGoal': '理解贪心算法从局部最优推导全局最优的原理，掌握交换论证法',
      'explanation': '贪心算法的核心问题：局部最优选择能否导致全局最优？\n\n关键性质：\n1. 贪心选择性质：通过局部最优选择可以得到全局最优解\n2. 最优子结构：问题的最优解包含子问题的最优解\n\n证明贪心正确性的方法：\n- 交换论证法：假设最优解不按贪心策略选，交换后不更差\n- 贪心在前：证明贪心选的元素一定在某个最优解中\n- 反证法：假设有更优解，推出矛盾\n\n常见的正确贪心：\n- 活动选择：按结束时间排序\n- Huffman 编码：每次合并最小的两个\n- Dijkstra：每次选最近的未访问节点\n\n常见错误贪心：\n- 0/1 背包按性价比排序（反例：重量限制导致无法装入）',
      'exampleCode': '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nstruct Activity {\n    int start, end;\n};\n\nbool cmp(Activity a, Activity b) {\n    return a.end < b.end;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    Activity act[1005];\n    for (int i = 0; i < n; i++)\n        cin >> act[i].start >> act[i].end;\n    sort(act, act + n, cmp);\n    int cnt = 1, lastEnd = act[0].end;\n    for (int i = 1; i < n; i++) {\n        if (act[i].start >= lastEnd) {\n            cnt++;\n            lastEnd = act[i].end;\n        }\n    }\n    cout << cnt << endl;\n    return 0;\n}',
      'codeNotes': [
        '活动选择：按结束时间排序是贪心策略',
        '每次选最早结束的活动（局部最优）',
        '用交换论证法可证明正确性',
        '贪心不保证对所有问题都正确'
      ],
      'commonMistakes': [
        {
          'title': '不证明就认为贪心正确',
          'description': '想当然地认为贪心策略一定对，没有严格证明。',
          'fix': '用交换论证法证明，或至少举不出反例。'
        },
        {
          'title': '把需要 DP 的问题用贪心',
          'description': '0/1 背包按性价比贪心是错的。',
          'fix': '如果贪心无法证明正确，考虑 DP。'
        }
      ],
      'practice': {
        'prompt': '有 n 个活动，每个有开始和结束时间，求最多能参加多少个不重叠的活动。',
        'hint': '按结束时间排序，贪心选择。',
        'expectedIdea': '按结束时间排序，每次选最早结束且与已选不冲突的活动。'
      },
      'quiz': [
        {
          'question': '证明贪心正确性最常用的方法是？',
          'options': ['数学归纳法', '交换论证法', '构造法', '反证法'],
          'answerIndex': 1,
          'explanation': '交换论证法：假设最优解不按贪心选，交换后证明不更差，说明贪心也是最优。'
        }
      ]
    },
    '2.6.6': {
      'itemId': '2.6.6',
      'title': '贪心正确性基础',
      'learningGoal': '理解判断贪心正确性的基本方法，能区分可贪心与不可贪心的问题',
      'explanation': '贪心正确性的判断是竞赛中的重要能力。\n\n贪心成立的必要条件：\n1. 贪心选择性质：局部最优选择不会影响后续子问题的最优性\n2. 最优子结构：原问题的最优解包含子问题的最优解\n\n验证贪心正确性的步骤：\n1. 构造反例：尝试找使贪心失败的输入\n2. 如果找不到反例，尝试证明：\n   - 交换论证法\n   - 贪心在前法\n   - 归纳法\n\n典型可贪心问题：\n- 活动选择、找零（特定币制）、Huffman、Kruskal、Prim、Dijkstra\n\n典型不可贪心问题：\n- 0/1 背包（需要 DP）\n- TSP 旅行商问题（NP-hard）\n- 一般的整数规划问题',
      'exampleCode': '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int coins[] = {1, 5, 10, 25};\n    int n = 4, amount;\n    cin >> amount;\n    int cnt = 0;\n    for (int i = n - 1; i >= 0; i--) {\n        cnt += amount / coins[i];\n        amount %= coins[i];\n    }\n    cout << cnt << endl;\n    return 0;\n}',
      'codeNotes': [
        '找零问题：从大面额开始选（贪心）',
        '对 1,5,10,25 币制贪心正确',
        '但并非所有币制都能贪心（如 1,3,4 凑 6）',
        '贪心正确性需要严格证明'
      ],
      'commonMistakes': [
        {
          'title': '找零问题中盲目贪心',
          'description': '币制为 {1,3,4}，要凑 6 元。贪心 4+1+1=3 枚，但最优 3+3=2 枚。',
          'fix': '不是所有币制都能贪心，需要验证。不能贪心时用 DP。'
        }
      ],
      'practice': {
        'prompt': '币制为 {1,5,10,25}，求凑出 amount 元的最少硬币数。',
        'hint': '从大面额到小面额贪心选择。',
        'expectedIdea': 'for 从大到小: cnt += amount/coin; amount %= coin;'
      },
      'quiz': [
        {
          'question': '以下哪个问题不能用贪心正确求解？',
          'options': ['活动选择', 'Huffman 编码', '0/1 背包', '最小生成树'],
          'answerIndex': 2,
          'explanation': '0/1 背包按性价比贪心不正确，需要用动态规划求解。'
        }
      ]
    },
  };

  final f2_7 = 'assets/data/algorithm/section_2_7_units.json';
  updates[f2_7] = {
    '2.7.9': {
      'itemId': '2.7.9',
      'title': '连通块搜索',
      'learningGoal': '掌握用 DFS/BFS 搜索连通块的方法，能解决网格图和一般图的连通性问题',
      'explanation': '连通块搜索是图论中的基础操作：找出图中所有互相连通的节点集合。\n\n方法：\n1. 遍历所有未访问的节点\n2. 从该节点出发做 DFS 或 BFS，标记所有能到达的节点\n3. 这些被标记的节点构成一个连通块\n4. 重复直到所有节点都被访问\n\n网格图中的连通块：\n- 将网格看作图，每个格子是节点\n- 上下左右四个方向（或八个方向）为边\n- 常见问题：数岛屿数量、最大连通区域面积\n\n时间复杂度：O(V + E)，每个节点和边最多访问一次。',
      'exampleCode': '#include <iostream>\nusing namespace std;\n\nint n, m;\nchar grid[105][105];\nbool vis[105][105];\nint dx[] = {0, 0, 1, -1};\nint dy[] = {1, -1, 0, 0};\n\nvoid dfs(int x, int y) {\n    vis[x][y] = true;\n    for (int d = 0; d < 4; d++) {\n        int nx = x + dx[d], ny = y + dy[d];\n        if (nx >= 0 && nx < n && ny >= 0 && ny < m\n            && !vis[nx][ny] && grid[nx][ny] == \'1\') {\n            dfs(nx, ny);\n        }\n    }\n}\n\nint main() {\n    cin >> n >> m;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++)\n            cin >> grid[i][j];\n    int cnt = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++)\n            if (grid[i][j] == \'1\' && !vis[i][j]) {\n                dfs(i, j);\n                cnt++;\n            }\n    cout << cnt << endl;\n    return 0;\n}',
      'codeNotes': [
        '遍历所有格子，从未访问的起点开始 DFS',
        '四方向扩展：上下左右',
        '每次 DFS 完成一个连通块',
        '连通块数量 = DFS 调用次数'
      ],
      'commonMistakes': [
        {
          'title': '忘记检查边界',
          'description': 'DFS 中没有判断 nx, ny 是否越界。',
          'fix': '每次扩展前检查 nx >= 0 && nx < n && ny >= 0 && ny < m。'
        }
      ],
      'practice': {
        'prompt': '给定 n×m 的 01 网格，求最大的 1 连通块面积。',
        'hint': 'DFS 时统计每个连通块的大小。',
        'expectedIdea': 'DFS 返回连通块大小，取最大值。'
      },
      'quiz': [
        {
          'question': '用 DFS 搜索连通块的时间复杂度是？',
          'options': ['O(n^2)', 'O(V+E)', 'O(V^2)', 'O(E^2)'],
          'answerIndex': 1,
          'explanation': '每个节点和边最多访问一次，总复杂度 O(V+E)。'
        }
      ]
    },
    '2.7.10': {
      'itemId': '2.7.10',
      'title': '最短步数搜索',
      'learningGoal': '掌握用 BFS 求最短步数/最少操作次数的方法',
      'explanation': 'BFS 天然适合求最短步数问题：从起点出发，逐层扩展，第一次到达目标时的步数就是最少的。\n\n为什么 BFS 能求最短路：\n- BFS 按距离从小到大依次访问节点\n- 第一次到达某个状态时，所用步数一定最少\n\n常见题型：\n1. 迷宫最短路：网格中从起点到终点的最少步数\n2. 状态空间搜索：八数码、华容道等\n3. 最少操作次数：每次操作改变状态，求最少操作次数\n\n关键：状态去重！用 vis 数组或 set 记录已访问的状态，避免重复搜索。',
      'exampleCode': '#include <iostream>\n#include <queue>\nusing namespace std;\n\nint n, m;\nchar grid[1005][1005];\nint dist[1005][1005];\nint dx[] = {0, 0, 1, -1};\nint dy[] = {1, -1, 0, 0};\n\nint main() {\n    cin >> n >> m;\n    int sx, sy, ex, ey;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++) {\n            cin >> grid[i][j];\n            if (grid[i][j] == \'S\') { sx = i; sy = j; }\n            if (grid[i][j] == \'E\') { ex = i; ey = j; }\n            dist[i][j] = -1;\n        }\n    queue<pair<int,int>> q;\n    q.push({sx, sy});\n    dist[sx][sy] = 0;\n    while (!q.empty()) {\n        auto [x, y] = q.front(); q.pop();\n        for (int d = 0; d < 4; d++) {\n            int nx = x + dx[d], ny = y + dy[d];\n            if (nx >= 0 && nx < n && ny >= 0 && ny < m\n                && grid[nx][ny] != \'#\' && dist[nx][ny] == -1) {\n                dist[nx][ny] = dist[x][y] + 1;\n                q.push({nx, ny});\n            }\n        }\n    }\n    cout << dist[ex][ey] << endl;\n    return 0;\n}',
      'codeNotes': [
        'BFS 天然求最短路',
        'dist 数组同时充当 vis 和记录距离',
        'dist = -1 表示未访问',
        '第一次到达时距离最短'
      ],
      'commonMistakes': [
        {
          'title': '忘记初始化 dist 为 -1',
          'description': 'dist 默认为 0，无法区分未访问和距离为 0。',
          'fix': '初始化 memset(dist, -1, sizeof(dist))。'
        }
      ],
      'practice': {
        'prompt': '在 n×m 迷宫中，S 是起点，E 是终点，# 是墙，求 S 到 E 的最短步数。',
        'hint': 'BFS 从 S 出发，逐层扩展。',
        'expectedIdea': '标准 BFS 最短路模板'
      },
      'quiz': [
        {
          'question': 'BFS 为什么能保证第一次到达时的步数最少？',
          'options': [
            'BFS 使用队列',
            'BFS 按距离从小到大访问',
            'BFS 不重复访问',
            'BFS 比 DFS 快'
          ],
          'answerIndex': 1,
          'explanation': 'BFS 逐层扩展，距离为 1 的先访问完，再访问距离为 2 的，所以第一次到达时距离最小。'
        }
      ]
    },
    '2.7.11': {
      'itemId': '2.7.11',
      'title': 'A* 搜索基础',
      'learningGoal': '理解 A* 搜索算法的原理，掌握启发式函数的设计方法',
      'explanation': 'A* 算法是 BFS 的改进版本，通过启发式函数引导搜索方向，更快找到最短路径。\n\n核心公式：f(n) = g(n) + h(n)\n- g(n)：从起点到 n 的实际代价\n- h(n)：从 n 到终点的估计代价（启发式函数）\n- f(n)：经过 n 的估计总代价\n\nA* 用优先队列按 f(n) 排序，每次取 f 最小的节点扩展。\n\n关键要求：\n- h(n) 必须「不高估」实际代价（可容许性）\n- 常见启发式：曼哈顿距离、欧几里得距离、切比雪夫距离\n\n优点：比纯 BFS 搜索更少的节点\n缺点：需要设计合适的启发式函数',
      'exampleCode': '#include <iostream>\n#include <queue>\n#include <cmath>\nusing namespace std;\n\nint n, m;\nint grid[105][105];\nint dist[105][105];\nint ex, ey;\n\nint h(int x, int y) {\n    return abs(x - ex) + abs(y - ey);\n}\n\nstruct State {\n    int x, y, f;\n    bool operator>(const State& s) const { return f > s.f; }\n};\n\nint main() {\n    cin >> n >> m;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < m; j++) dist[i][j] = 1e9;\n    int sx, sy;\n    cin >> sx >> sy >> ex >> ey;\n    priority_queue<State, vector<State>, greater<State>> pq;\n    dist[sx][sy] = 0;\n    pq.push({sx, sy, h(sx, sy)});\n    int dx[] = {0,0,1,-1}, dy[] = {1,-1,0,0};\n    while (!pq.empty()) {\n        auto [x, y, f] = pq.top(); pq.pop();\n        if (x == ex && y == ey) break;\n        if (dist[x][y] < f - h(x, y)) continue;\n        for (int d = 0; d < 4; d++) {\n            int nx = x+dx[d], ny = y+dy[d];\n            if (nx>=0&&nx<n&&ny>=0&&ny<m&&grid[nx][ny]==0) {\n                int ng = dist[x][y] + 1;\n                if (ng < dist[nx][ny]) {\n                    dist[nx][ny] = ng;\n                    pq.push({nx, ny, ng + h(nx, ny)});\n                }\n            }\n        }\n    }\n    cout << dist[ex][ey] << endl;\n    return 0;\n}',
      'codeNotes': [
        'f(n) = g(n) + h(n)',
        'h(n) 不能高估实际代价',
        '用优先队列按 f 值排序',
        '常用曼哈顿距离作启发式'
      ],
      'commonMistakes': [
        {
          'title': '启发式函数高估代价',
          'description': 'h(n) 大于实际最短路径，A* 可能找不到最优解。',
          'fix': '确保 h(n) 不超过实际代价，如用曼哈顿距离（四方向移动时不高估）。'
        }
      ],
      'practice': {
        'prompt': '在网格中用 A* 求起点到终点的最短路径，启发式用曼哈顿距离。',
        'hint': 'f = g + h，h = |x-ex| + |y-ey|。',
        'expectedIdea': '优先队列按 f 排序，每次取 f 最小的扩展。'
      },
      'quiz': [
        {
          'question': 'A* 算法中启发式函数 h(n) 必须满足什么条件才能保证最优解？',
          'options': [
            'h(n) 必须等于 0',
            'h(n) 不能高估实际代价',
            'h(n) 必须大于实际代价',
            'h(n) 必须是整数'
          ],
          'answerIndex': 1,
          'explanation': 'h(n) 必须「可容许」，即 h(n) <= 实际最短路径代价，否则可能找不到最优解。'
        }
      ]
    },
    '2.7.12': {
      'itemId': '2.7.12',
      'title': '启发式搜索基础',
      'learningGoal': '理解启发式搜索的基本概念，了解常见启发式策略',
      'explanation': '启发式搜索是在搜索过程中利用额外信息（启发式）来引导搜索方向，减少不必要的探索。\n\n基本概念：\n- 启发式（Heuristic）：一种估计函数，帮助判断哪些状态更有希望\n- 盲目搜索 vs 启发式搜索：BFS/DFS 是盲目的，A* 是启发式的\n\n常见启发式策略：\n1. 贪心最佳优先：只看 h(n)，不考虑已走代价 g(n)\n2. A* 搜索：f(n) = g(n) + h(n)，兼顾已走和预估\n3. IDA*：迭代加深 + 启发式，空间效率高\n\n启发式函数的选择：\n- 越接近真实代价，搜索效率越高\n- 常用距离函数：曼哈顿、欧几里得、切比雪夫\n- 在八数码问题中，可用「不在位数码数」作为启发式',
      'exampleCode': '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint h(int board[3][3], int target[3][3]) {\n    int cnt = 0;\n    for (int i = 0; i < 3; i++)\n        for (int j = 0; j < 3; j++)\n            if (board[i][j] != target[i][j]) cnt++;\n    return cnt;\n}\n\nint main() {\n    int board[3][3] = {{1,2,3},{4,0,6},{7,5,8}};\n    int target[3][3] = {{1,2,3},{4,5,6},{7,8,0}};\n    cout << "heuristic value: " << h(board, target) << endl;\n    return 0;\n}',
      'codeNotes': [
        '启发式函数评估状态到目标的距离',
        'h 越接近真实代价效率越高',
        '常见：曼哈顿距离、不在位数',
        '启发式搜索减少不必要的探索'
      ],
      'commonMistakes': [
        {
          'title': '启发式函数设计不当',
          'description': 'h(n) 与真实代价差距太大，搜索效率反而不如 BFS。',
          'fix': '选择尽量接近真实代价但不高估的启发式函数。'
        }
      ],
      'practice': {
        'prompt': '为八数码问题设计一个启发式函数，并计算一个给定状态的 h 值。',
        'hint': '统计不在目标位置的数码个数。',
        'expectedIdea': '遍历 3×3 网格，统计 board[i][j] != target[i][j] 的个数。'
      },
      'quiz': [
        {
          'question': '以下哪个不是常见的启发式函数？',
          'options': ['曼哈顿距离', '欧几里得距离', '随机数', '切比雪夫距离'],
          'answerIndex': 2,
          'explanation': '随机数不反映到目标的距离信息，不能作为有效的启发式函数。'
        }
      ]
    },
  };

  for (final entry in updates.entries) {
    final filePath = entry.key;
    final itemUpdates = entry.value;
    final file = File(filePath);
    final json = jsonDecode(await file.readAsString()) as Map<String, dynamic>;
    final units = json['units'] as List;

    for (int i = 0; i < units.length; i++) {
      final unit = units[i] as Map<String, dynamic>;
      final itemId = unit['itemId'] as String;
      if (itemUpdates.containsKey(itemId)) {
        units[i] = itemUpdates[itemId];
      }
    }

    final encoder = JsonEncoder.withIndent('  ');
    await file.writeAsString(encoder.convert(json));
    print('Updated: $filePath (${itemUpdates.length} items)');
  }

  print('\nDone: section 2.3/2.6/2.7');
}
