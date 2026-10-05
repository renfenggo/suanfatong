# 学习路径分层前端可用性复核报告

审计时间：2026-09-02
总节点数：3240

## 一、复核总览

- 原 core 数：838
- 疑似误分 core 数：111

### frontend_display_layer 统计

| 层级 | 节点数 | 占比 |
|------|--------|------|
| 核心主线 (core) | 727 | 22.4% |
| 常用进阶 (standard) | 1264 | 39.0% |
| 专题扩展 (advanced) | 933 | 28.8% |
| 冷门/可折叠 (optional) | 316 | 9.8% |

## 二、疑似误分 core 节点

共 111 个疑似误分节点：

| ID | 名称 | 章节 | 建议层级 | 原因 |
|----|------|------|----------|------|
| 2.3.20 | 斜率优化：二分查找凸包 | 2.3 | advanced | 名称含高级关键词: 凸包 |
| 2.3.23 | 斜率优化中的凸包二分 | 2.3 | advanced | 名称含高级关键词: 凸包 |
| 2.5.5 | 单调队列维护窗口最值 | 2.5 | advanced | 名称含高级关键词: 队列维护 |
| 2.6.23 | 堆维护贪心的可交换性条件 (堆维护贪心 Exchangeability Condition) | 2.6 | advanced | 名称含高级关键词: 堆维护 |
| 2.6.24 | 堆维护贪心的单调选择性质 (堆维护贪心 Monotone Choice Property) | 2.6 | advanced | 名称含高级关键词: 堆维护 |
| 2.8.202 | 凸包维护 DP | 2.8 | advanced | 名称含高级关键词: 凸包 |
| 2.8.203 | 分治转移 DP | 2.8 | advanced | 名称含高级关键词: 分治转移 |
| 2.8.204 | 队列维护 DP | 2.8 | advanced | 名称含高级关键词: 队列维护 |
| 2.8.205 | 线段树维护 DP | 2.8 | advanced | 名称含高级关键词: 线段树维护 |
| 2.8.206 | 堆维护 DP | 2.8 | advanced | 名称含高级关键词: 堆维护 |
| 2.8.213 | DP 与最短路融合模型 (DP 与最短路融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.8.214 | DP 与网络流融合模型 (DP 与网络流融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.8.215 | DP 与字符串自动机融合模型 (DP 与字符串自动机融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.8.216 | DP 与生成函数融合模型 (DP 与生成函数融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.8.217 | DP 与数据结构查询融合模型 (DP 与数据结构查询融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.8.218 | DP 与连通性状态融合模型 (DP 与连通性状态融合模型) | 2.8 | advanced | 名称含高级关键词: 融合模型 |
| 2.9.33 | 可并堆维护最长路径 | 2.9 | advanced | 名称含高级关键词: 堆维护 |
| 2.9.166 | 最小割建模的点权转边权 (最小割建模 Vertex Weight to Edge Weight) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.9.167 | 最小割建模的拆点约束 (最小割建模 Vertex Splitting Constraint) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.9.168 | 最小割建模的拆边约束 (最小割建模 Edge Splitting Constraint) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.9.187 | 最小割建模的源汇选择 (最小割建模 Source Sink Selection) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.9.188 | 最小割建模的容量语义 (最小割建模 Capacity Semantics) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.9.189 | 最小割建模的费用语义 (最小割建模 Cost Semantics) | 2.9 | advanced | 名称含高级关键词: 最小割 |
| 2.10.65 | 广义 SAM的出现次数聚合 (广义 SAM Occurrence Aggregation) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.10.68 | 广义 SAM的状态链接树 (广义 SAM State Link Tree) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.10.69 | 广义 SAM的终止位置集合 (广义 SAM Endpos Set) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.10.70 | 广义 SAM的多串合并 (广义 SAM Multi-string Merge) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.10.71 | 广义 SAM的在线扩展 (广义 SAM Online Extension) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.10.72 | 广义 SAM的子串等价类 (广义 SAM Substring Equivalence Class) | 2.10 | advanced | 名称含高级关键词: SAM |
| 2.17.28 | 高斯消元的主元选择 (高斯消元 Pivot Selection) | 2.17 | advanced | 名称含高级关键词: 高斯消元 |
| 2.17.31 | 行列式计算的主元选择 (行列式计算 Pivot Selection) | 2.17 | advanced | 名称含高级关键词: 行列式 |
| 2.17.32 | 实数线性基的主元选择 (实数线性基 Pivot Selection) | 2.17 | advanced | 名称含高级关键词: 线性基 |
| 2.17.37 | 高斯消元的秩判定 (高斯消元 Rank Determination) | 2.17 | advanced | 名称含高级关键词: 高斯消元 |
| 2.17.38 | 高斯消元的模意义运算 (高斯消元 Modular Operation) | 2.17 | advanced | 名称含高级关键词: 高斯消元 |
| 2.17.39 | 高斯消元的线性无关维护 (高斯消元 Linear Independence Maintenance) | 2.17 | advanced | 名称含高级关键词: 高斯消元 |
| 2.17.46 | 行列式计算的秩判定 (行列式计算 Rank Determination) | 2.17 | advanced | 名称含高级关键词: 行列式 |
| 2.17.47 | 行列式计算的模意义运算 (行列式计算 Modular Operation) | 2.17 | advanced | 名称含高级关键词: 行列式 |
| 2.17.48 | 行列式计算的线性无关维护 (行列式计算 Linear Independence Maintenance) | 2.17 | advanced | 名称含高级关键词: 行列式 |
| 2.17.49 | 实数线性基的秩判定 (实数线性基 Rank Determination) | 2.17 | advanced | 名称含高级关键词: 线性基 |
| 2.17.50 | 实数线性基的模意义运算 (实数线性基 Modular Operation) | 2.17 | advanced | 名称含高级关键词: 线性基 |
| 2.17.51 | 实数线性基的线性无关维护 (实数线性基 Linear Independence Maintenance) | 2.17 | advanced | 名称含高级关键词: 线性基 |
| 1.3.22 | 循环字符串最小表示 | 1.3 | advanced | 名称含高级关键词: 最小表示 |
| 1.3.25 | 字符串的最小表示法 | 1.3 | advanced | 名称含高级关键词: 最小表示 |
| 1.3.44 | 字符串哈希判断回文 | 1.3 | advanced | 名称含高级关键词: 字符串哈希 |
| 1.3.45 | 字符串哈希判断循环节 | 1.3 | advanced | 名称含高级关键词: 字符串哈希 |
| 1.3.46 | 字符串哈希判等 O(1) | 1.3 | advanced | 名称含高级关键词: 字符串哈希 |
| 1.7.25 | 欧拉函数 | 1.7 | advanced | 名称含高级关键词: 欧拉函数 |
| 1.7.26 | 欧拉函数的线性筛求法 | 1.7 | advanced | 名称含高级关键词: 欧拉函数 |
| 3.13.235 | 凸包维护队列的支配关系 (凸包维护队列 Dominance Relation) | 3.13 | advanced | 名称含高级关键词: 凸包 |
| 3.13.236 | 凸包维护队列的弹出条件 (凸包维护队列 Pop Condition) | 3.13 | advanced | 名称含高级关键词: 凸包 |
| 3.13.243 | 可持久化并查集的集合语义 (可持久化并查集 Set Semantics) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.248 | 部分持久化数组 (部分持久化数组) | 3.13 | advanced | 名称含高级关键词: 持久化 |
| 3.13.249 | 完全持久化数组 (完全持久化数组) | 3.13 | advanced | 名称含高级关键词: 持久化 |
| 3.13.250 | 可持久化字典树版本合并 (可持久化字典树版本合并) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.251 | 可持久化堆版本合并 (可持久化堆版本合并) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.252 | 可持久化并查集版本树 (可持久化并查集版本树) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.253 | 整体二分结构的外层维度 (整体二分结构 Outer Dimension) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.255 | 可持久化字典树的外层维度 (可持久化字典树 Outer Dimension) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.256 | 分块套值域结构的外层维度 (分块套值域结构 Outer Dimension) | 3.13 | advanced | 名称含高级关键词: 分块套 |
| 3.13.257 | 扫描线事件结构的外层维度 (扫描线事件结构 Outer Dimension) | 3.13 | advanced | 名称含高级关键词: 扫描线 |
| 3.13.259 | 分块套线段树的离散化维度 (分块套线段树 Discretized Dimension) | 3.13 | advanced | 名称含高级关键词: 分块套 |
| 3.13.260 | 莫队套值域结构的离散化维度 (莫队套值域结构 Discretized Dimension) | 3.13 | advanced | 名称含高级关键词: 莫队 |
| 3.13.263 | 队列维护决策的支配关系 (队列维护决策 Dominance Relation) | 3.13 | advanced | 名称含高级关键词: 队列维护 |
| 3.13.264 | 队列维护决策的弹出条件 (队列维护决策 Pop Condition) | 3.13 | advanced | 名称含高级关键词: 队列维护 |
| 3.13.269 | 凸包维护队列的区间有效性 (凸包维护队列 Interval Validity) | 3.13 | advanced | 名称含高级关键词: 凸包 |
| 3.13.270 | 凸包维护队列的贡献统计 (凸包维护队列 Contribution Counting) | 3.13 | advanced | 名称含高级关键词: 凸包 |
| 3.13.275 | 队列维护决策的区间有效性 (队列维护决策 Interval Validity) | 3.13 | advanced | 名称含高级关键词: 队列维护 |
| 3.13.276 | 队列维护决策的贡献统计 (队列维护决策 Contribution Counting) | 3.13 | advanced | 名称含高级关键词: 队列维护 |
| 3.13.282 | 可持久化并查集的合并约束 (可持久化并查集 Merge Constraint) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.294 | 整体二分套树状数组的离散化维度 (整体二分套树状数组 Discretized Dimension) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.295 | 扫描线套线段树的离散化维度 (扫描线套线段树 Discretized Dimension) | 3.13 | advanced | 名称含高级关键词: 扫描线 |
| 3.13.296 | 可持久化结构套哈希的离散化维度 (可持久化结构套哈希 Discretized Dimension) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.297 | 整体二分结构的内层维护对象 (整体二分结构 Inner Maintained Object) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.298 | 整体二分结构的离线约束 (整体二分结构 Offline Constraint) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.299 | 整体二分结构的空间复杂度拆分 (整体二分结构 Space Complexity Decomposition) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.300 | 整体二分结构的矩形查询模型 (整体二分结构 Rectangle Query Model) | 3.13 | advanced | 名称含高级关键词: 整体二分 |
| 3.13.305 | 可持久化字典树的内层维护对象 (可持久化字典树 Inner Maintained Object) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.306 | 可持久化字典树的离线约束 (可持久化字典树 Offline Constraint) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.307 | 可持久化字典树的空间复杂度拆分 (可持久化字典树 Space Complexity Decomposition) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.308 | 可持久化字典树的矩形查询模型 (可持久化字典树 Rectangle Query Model) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 3.13.309 | 可持久化并查集的权值关系 (可持久化并查集 Weighted Relation) | 3.13 | advanced | 名称含高级关键词: 可持久化 |
| 4.1.56 | 洲阁筛的函数前缀和 (洲阁筛 Function Prefix Sum) | 4.1 | advanced | 名称含高级关键词: 洲阁筛 |
| 4.1.57 | 洲阁筛的积性拆分 (洲阁筛 Multiplicative Decomposition) | 4.1 | advanced | 名称含高级关键词: 洲阁筛 |
| 4.1.58 | 洲阁筛的离散对数方程 (洲阁筛 Discrete Log Equation) | 4.1 | advanced | 名称含高级关键词: 洲阁筛 |
| 4.1.59 | 洲阁筛的模平方根方程 (洲阁筛 Modular Square Root Equation) | 4.1 | advanced | 名称含高级关键词: 洲阁筛 |
| 4.1.68 | 欧拉函数的定义与判定 (欧拉函数 Definition and Recognition) | 4.1 | advanced | 名称含高级关键词: 欧拉函数 |
| 4.1.69 | 莫比乌斯函数的定义与判定 (莫比乌斯函数 Definition and Recognition) | 4.1 | advanced | 名称含高级关键词: 莫比乌斯 |
| 4.1.70 | Lucas 定理的定义与判定 (Lucas 定理 Definition and Recognition) | 4.1 | advanced | 名称含高级关键词: Lucas |
| 4.1.89 | 欧拉函数的构造方法 (欧拉函数 Construction Method) | 4.1 | advanced | 名称含高级关键词: 欧拉函数 |
| 4.1.90 | 欧拉函数的计数公式 (欧拉函数 Counting Formula) | 4.1 | advanced | 名称含高级关键词: 欧拉函数 |
| 4.1.91 | 莫比乌斯函数的构造方法 (莫比乌斯函数 Construction Method) | 4.1 | advanced | 名称含高级关键词: 莫比乌斯 |
| 4.1.92 | 莫比乌斯函数的计数公式 (莫比乌斯函数 Counting Formula) | 4.1 | advanced | 名称含高级关键词: 莫比乌斯 |
| 4.1.93 | Lucas 定理的构造方法 (Lucas 定理 Construction Method) | 4.1 | advanced | 名称含高级关键词: Lucas |
| 4.1.94 | Lucas 定理的计数公式 (Lucas 定理 Counting Formula) | 4.1 | advanced | 名称含高级关键词: Lucas |
| 4.3.48 | FFT的代数结构 (FFT Algebraic Structure) | 4.3 | advanced | 名称含高级关键词: FFT |
| 4.3.49 | FFT的复杂度界 (FFT Complexity Bound) | 4.3 | advanced | 名称含高级关键词: FFT |
| 4.3.50 | FFT的卷积模型 (FFT Convolution Model) | 4.3 | advanced | 名称含高级关键词: FFT |
| 4.3.51 | FFT的模数条件 (FFT Modulus Condition) | 4.3 | advanced | 名称含高级关键词: FFT |
| 4.3.52 | FFT的变换逆变换 (FFT Transform and Inverse Transform) | 4.3 | advanced | 名称含高级关键词: FFT |
| 4.3.53 | NTT的代数结构 (NTT Algebraic Structure) | 4.3 | advanced | 名称含高级关键词: NTT |
| 4.3.54 | NTT的复杂度界 (NTT Complexity Bound) | 4.3 | advanced | 名称含高级关键词: NTT |
| 4.3.55 | NTT的卷积模型 (NTT Convolution Model) | 4.3 | advanced | 名称含高级关键词: NTT |
| 4.3.64 | NTT的模数条件 (NTT Modulus Condition) | 4.3 | advanced | 名称含高级关键词: NTT |
| 4.3.65 | NTT的变换逆变换 (NTT Transform and Inverse Transform) | 4.3 | advanced | 名称含高级关键词: NTT |
| 4.7.46 | 凸包的有向面积 (凸包 Signed Area) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.47 | 凸包的叉积符号 (凸包 Cross Product Sign) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.52 | 凸包的极角排序 (凸包 Polar Angle Sorting) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.55 | 凸包的凸包切线 (凸包 Convex Hull Tangent) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.56 | 凸包的浮点误差界 (凸包 Floating Error Bound) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.57 | 最近点对的凸包切线 (最近点对 Convex Hull Tangent) | 4.7 | advanced | 名称含高级关键词: 凸包 |
| 4.7.59 | Delaunay 三角剖分的凸包切线 (Delaunay Triangulation Convex Hull Tangent) | 4.7 | advanced | 名称含高级关键词: 凸包 |

## 三、重点章节复核

### 2.8 动态规划

- 总节点：292
- core 节点：13
- 疑似误分：11

**疑似误分节点：**

| ID | 名称 | graph_layer | frontend_layer | level | visibility |
|----|------|-------------|----------------|-------|------------|
| 2.8.202 | 凸包维护 DP | core | advanced |  | core |
| 2.8.203 | 分治转移 DP | core | advanced |  | core |
| 2.8.204 | 队列维护 DP | core | advanced |  | core |
| 2.8.205 | 线段树维护 DP | core | advanced |  | core |
| 2.8.206 | 堆维护 DP | core | advanced |  | core |
| 2.8.213 | DP 与最短路融合模型 (DP 与最短路融合模型) | core | advanced |  | core |
| 2.8.214 | DP 与网络流融合模型 (DP 与网络流融合模型) | core | advanced |  | core |
| 2.8.215 | DP 与字符串自动机融合模型 (DP 与字符串自动机融合模型) | core | advanced |  | core |
| 2.8.216 | DP 与生成函数融合模型 (DP 与生成函数融合模型) | core | advanced |  | core |
| 2.8.217 | DP 与数据结构查询融合模型 (DP 与数据结构查询融合模型) | core | advanced |  | core |
| 2.8.218 | DP 与连通性状态融合模型 (DP 与连通性状态融合模型) | core | advanced |  | core |

### 3.13 高级数据结构扩展

- 总节点：374
- core 节点：79
- 疑似误分：33

**疑似误分节点：**

| ID | 名称 | graph_layer | frontend_layer | level | visibility |
|----|------|-------------|----------------|-------|------------|
| 3.13.235 | 凸包维护队列的支配关系 (凸包维护队列 Dominance Relation) | core | advanced |  | core |
| 3.13.236 | 凸包维护队列的弹出条件 (凸包维护队列 Pop Condition) | core | advanced |  | core |
| 3.13.243 | 可持久化并查集的集合语义 (可持久化并查集 Set Semantics) | core | advanced |  | core |
| 3.13.248 | 部分持久化数组 (部分持久化数组) | core | advanced |  | core |
| 3.13.249 | 完全持久化数组 (完全持久化数组) | core | advanced |  | core |
| 3.13.250 | 可持久化字典树版本合并 (可持久化字典树版本合并) | core | advanced |  | core |
| 3.13.251 | 可持久化堆版本合并 (可持久化堆版本合并) | core | advanced |  | core |
| 3.13.252 | 可持久化并查集版本树 (可持久化并查集版本树) | core | advanced |  | core |
| 3.13.253 | 整体二分结构的外层维度 (整体二分结构 Outer Dimension) | core | advanced |  | core |
| 3.13.255 | 可持久化字典树的外层维度 (可持久化字典树 Outer Dimension) | core | advanced |  | core |
| 3.13.256 | 分块套值域结构的外层维度 (分块套值域结构 Outer Dimension) | core | advanced |  | core |
| 3.13.257 | 扫描线事件结构的外层维度 (扫描线事件结构 Outer Dimension) | core | advanced |  | core |
| 3.13.259 | 分块套线段树的离散化维度 (分块套线段树 Discretized Dimension) | core | advanced |  | core |
| 3.13.260 | 莫队套值域结构的离散化维度 (莫队套值域结构 Discretized Dimension) | core | advanced |  | core |
| 3.13.263 | 队列维护决策的支配关系 (队列维护决策 Dominance Relation) | core | advanced |  | core |
| 3.13.264 | 队列维护决策的弹出条件 (队列维护决策 Pop Condition) | core | advanced |  | core |
| 3.13.269 | 凸包维护队列的区间有效性 (凸包维护队列 Interval Validity) | core | advanced |  | core |
| 3.13.270 | 凸包维护队列的贡献统计 (凸包维护队列 Contribution Counting) | core | advanced |  | core |
| 3.13.275 | 队列维护决策的区间有效性 (队列维护决策 Interval Validity) | core | advanced |  | core |
| 3.13.276 | 队列维护决策的贡献统计 (队列维护决策 Contribution Counting) | core | advanced |  | core |
| 3.13.282 | 可持久化并查集的合并约束 (可持久化并查集 Merge Constraint) | core | advanced |  | core |
| 3.13.294 | 整体二分套树状数组的离散化维度 (整体二分套树状数组 Discretized Dimension) | core | advanced |  | core |
| 3.13.295 | 扫描线套线段树的离散化维度 (扫描线套线段树 Discretized Dimension) | core | advanced |  | core |
| 3.13.296 | 可持久化结构套哈希的离散化维度 (可持久化结构套哈希 Discretized Dimension) | core | advanced |  | core |
| 3.13.297 | 整体二分结构的内层维护对象 (整体二分结构 Inner Maintained Object) | core | advanced |  | core |
| 3.13.298 | 整体二分结构的离线约束 (整体二分结构 Offline Constraint) | core | advanced |  | core |
| 3.13.299 | 整体二分结构的空间复杂度拆分 (整体二分结构 Space Complexity Decomposition) | core | advanced |  | core |
| 3.13.300 | 整体二分结构的矩形查询模型 (整体二分结构 Rectangle Query Model) | core | advanced |  | core |
| 3.13.305 | 可持久化字典树的内层维护对象 (可持久化字典树 Inner Maintained Object) | core | advanced |  | core |
| 3.13.306 | 可持久化字典树的离线约束 (可持久化字典树 Offline Constraint) | core | advanced |  | core |
| 3.13.307 | 可持久化字典树的空间复杂度拆分 (可持久化字典树 Space Complexity Decomposition) | core | advanced |  | core |
| 3.13.308 | 可持久化字典树的矩形查询模型 (可持久化字典树 Rectangle Query Model) | core | advanced |  | core |
| 3.13.309 | 可持久化并查集的权值关系 (可持久化并查集 Weighted Relation) | core | advanced |  | core |

### 4.1 整数与数论基础

- 总节点：193
- core 节点：39
- 疑似误分：13

**疑似误分节点：**

| ID | 名称 | graph_layer | frontend_layer | level | visibility |
|----|------|-------------|----------------|-------|------------|
| 4.1.56 | 洲阁筛的函数前缀和 (洲阁筛 Function Prefix Sum) | core | advanced |  | core |
| 4.1.57 | 洲阁筛的积性拆分 (洲阁筛 Multiplicative Decomposition) | core | advanced |  | core |
| 4.1.58 | 洲阁筛的离散对数方程 (洲阁筛 Discrete Log Equation) | core | advanced |  | core |
| 4.1.59 | 洲阁筛的模平方根方程 (洲阁筛 Modular Square Root Equation) | core | advanced |  | core |
| 4.1.68 | 欧拉函数的定义与判定 (欧拉函数 Definition and Recognition) | core | advanced |  | core |
| 4.1.69 | 莫比乌斯函数的定义与判定 (莫比乌斯函数 Definition and Recognition) | core | advanced |  | core |
| 4.1.70 | Lucas 定理的定义与判定 (Lucas 定理 Definition and Recognition) | core | advanced |  | core |
| 4.1.89 | 欧拉函数的构造方法 (欧拉函数 Construction Method) | core | advanced |  | core |
| 4.1.90 | 欧拉函数的计数公式 (欧拉函数 Counting Formula) | core | advanced |  | core |
| 4.1.91 | 莫比乌斯函数的构造方法 (莫比乌斯函数 Construction Method) | core | advanced |  | core |
| 4.1.92 | 莫比乌斯函数的计数公式 (莫比乌斯函数 Counting Formula) | core | advanced |  | core |
| 4.1.93 | Lucas 定理的构造方法 (Lucas 定理 Construction Method) | core | advanced |  | core |
| 4.1.94 | Lucas 定理的计数公式 (Lucas 定理 Counting Formula) | core | advanced |  | core |

### 2.9 图基础与遍历

- 总节点：204
- core 节点：42
- 疑似误分：7

**疑似误分节点：**

| ID | 名称 | graph_layer | frontend_layer | level | visibility |
|----|------|-------------|----------------|-------|------------|
| 2.9.33 | 可并堆维护最长路径 | core | advanced | L2 | core |
| 2.9.166 | 最小割建模的点权转边权 (最小割建模 Vertex Weight to Edge Weight) | core | advanced |  | core |
| 2.9.167 | 最小割建模的拆点约束 (最小割建模 Vertex Splitting Constraint) | core | advanced |  | core |
| 2.9.168 | 最小割建模的拆边约束 (最小割建模 Edge Splitting Constraint) | core | advanced |  | core |
| 2.9.187 | 最小割建模的源汇选择 (最小割建模 Source Sink Selection) | core | advanced |  | core |
| 2.9.188 | 最小割建模的容量语义 (最小割建模 Capacity Semantics) | core | advanced |  | core |
| 2.9.189 | 最小割建模的费用语义 (最小割建模 Cost Semantics) | core | advanced |  | core |

### 2.10 字符串算法

- 总节点：81
- core 节点：18
- 疑似误分：6

**疑似误分节点：**

| ID | 名称 | graph_layer | frontend_layer | level | visibility |
|----|------|-------------|----------------|-------|------------|
| 2.10.65 | 广义 SAM的出现次数聚合 (广义 SAM Occurrence Aggregation) | core | advanced |  | core |
| 2.10.68 | 广义 SAM的状态链接树 (广义 SAM State Link Tree) | core | advanced |  | core |
| 2.10.69 | 广义 SAM的终止位置集合 (广义 SAM Endpos Set) | core | advanced |  | core |
| 2.10.70 | 广义 SAM的多串合并 (广义 SAM Multi-string Merge) | core | advanced |  | core |
| 2.10.71 | 广义 SAM的在线扩展 (广义 SAM Online Extension) | core | advanced |  | core |
| 2.10.72 | 广义 SAM的子串等价类 (广义 SAM Substring Equivalence Class) | core | advanced |  | core |

## 四、前端展示层级建议

### 核心主线 (core)

- **展示方式**：默认展开
- **说明**：适合学习主线，入门必学
- **UI 行为**：章节列表中默认展开，节点卡片高亮显示
- **颜色建议**：主色调（如蓝色）

### 常用进阶 (standard)

- **展示方式**：默认显示，可分组
- **说明**：常用进阶，有一定基础后学习
- **UI 行为**：默认显示但可按子主题分组折叠
- **颜色建议**：次色调（如绿色）

### 专题扩展 (advanced)

- **展示方式**：默认折叠
- **说明**：专题扩展，需要较强前置知识
- **UI 行为**：章节内默认折叠，点击展开
- **颜色建议**：中性色（如橙色）

### 冷门/可折叠 (optional)

- **展示方式**：深度折叠或搜索可见
- **说明**：冷门/竞赛专题，仅特定场景需要
- **UI 行为**：需手动展开或仅搜索可见
- **颜色建议**：淡色（如灰色）

## 五、高拥挤章节折叠策略

| 章节 | 大类 | 总数 | core | standard | advanced | optional | 可折叠比例 | 默认策略 |
|------|------|------|------|----------|----------|----------|------------|----------|
| 3.13 高级数据结构扩展 | 数据结构 | 374 | 46 | 117 | 158 | 53 | 0.564 | 折叠 advanced+optional |
| 2.8 动态规划 | 算法 | 292 | 2 | 104 | 171 | 15 | 0.637 | 折叠 advanced+optional |
| 2.9 图基础与遍历 | 算法 | 204 | 35 | 90 | 74 | 5 | 0.387 | 折叠 optional |
| 4.1 整数与数论基础 | 算法竞赛数学 | 193 | 26 | 140 | 27 | 0 | 0.14 | 不默认折叠 |
| 2.20 交互题与构造题技巧 | 算法 | 187 | 64 | 120 | 3 | 0 | 0.016 | 不默认折叠 |
| 2.21 高级图论扩展 | 算法 | 186 | 0 | 13 | 129 | 44 | 0.93 | 折叠 advanced+optional |
| 4.3 计数与组合 | 算法竞赛数学 | 158 | 38 | 103 | 15 | 2 | 0.108 | 不默认折叠 |
| 2.1 基础算法思想 | 算法 | 108 | 13 | 81 | 13 | 1 | 0.13 | 不默认折叠 |
| 2.7 搜索 | 算法 | 94 | 53 | 39 | 2 | 0 | 0.021 | 不默认折叠 |
| 2.17 线性代数与插值专题 | 算法 | 84 | 12 | 35 | 18 | 19 | 0.44 | 折叠 optional |
| 2.4 前缀、差分、离散化、分块 | 算法 | 82 | 23 | 56 | 3 | 0 | 0.037 | 不默认折叠 |
| 2.10 字符串算法 | 算法 | 81 | 12 | 11 | 33 | 25 | 0.716 | 折叠 advanced+optional |
| 2.6 贪心 | 算法 | 70 | 28 | 39 | 3 | 0 | 0.043 | 不默认折叠 |
| 4.7 几何基础 | 算法竞赛数学 | 63 | 8 | 45 | 7 | 3 | 0.159 | 不默认折叠 |
| 1.8 结构体与 STL | C++语法 | 54 | 48 | 3 | 0 | 3 | 0.056 | 不默认折叠 |
| 3.7 区间维护结构 | 数据结构 | 52 | 0 | 13 | 33 | 6 | 0.75 | 折叠 advanced+optional |
| 1.3 数据类型与变量 | C++语法 | 50 | 40 | 1 | 9 | 0 | 0.18 | 不默认折叠 |
| 1.6 数组与字符串 | C++语法 | 50 | 23 | 9 | 3 | 15 | 0.36 | 折叠 optional |
| 4.5 图与树的数学基础 | 算法竞赛数学 | 46 | 25 | 6 | 15 | 0 | 0.326 | 折叠 optional |
| 1.7 函数、递归、引用与指针 | C++语法 | 44 | 31 | 1 | 11 | 1 | 0.273 | 不默认折叠 |
| 2.16 二分图、匹配与网络流 | 算法 | 42 | 0 | 9 | 2 | 31 | 0.786 | 折叠 advanced+optional |

## 六、首页入口章节推荐

| 章节 | 大类 | 总数 | core 数 | core 比例 | 优先级 |
|------|------|------|---------|-----------|--------|
| 1.1 程序基本结构 | C++语法 | 9 | 9 | 1.0 | high |
| 1.2 输入输出 | C++语法 | 16 | 16 | 1.0 | high |
| 1.4 运算符 | C++语法 | 15 | 15 | 1.0 | high |
| 1.9 预处理与代码组织 | C++语法 | 14 | 13 | 0.929 | high |
| 1.8 结构体与 STL | C++语法 | 54 | 48 | 0.889 | high |
| 1.10 常见易错点 | C++语法 | 15 | 13 | 0.867 | high |
| 3.1 线性结构 | 数据结构 | 12 | 10 | 0.833 | high |
| 1.5 控制结构 | C++语法 | 22 | 18 | 0.818 | high |
| 1.3 数据类型与变量 | C++语法 | 50 | 40 | 0.8 | high |
| 3.2 栈与队列 | 数据结构 | 17 | 12 | 0.706 | medium |
| 1.7 函数、递归、引用与指针 | C++语法 | 44 | 31 | 0.705 | medium |
| 3.5 堆 | 数据结构 | 26 | 18 | 0.692 | medium |
| 2.5 双指针与滑动窗口 | 算法 | 23 | 15 | 0.652 | medium |
| 2.3 二分与答案搜索 | 算法 | 29 | 18 | 0.621 | medium |
| 2.7 搜索 | 算法 | 94 | 53 | 0.564 | medium |
| 4.5 图与树的数学基础 | 算法竞赛数学 | 46 | 25 | 0.543 | medium |
| 4.6 概率与期望 | 算法竞赛数学 | 37 | 20 | 0.541 | medium |

## 七、写回图谱建议

**不建议立即写回**：存在 111 个疑似误分 core 节点，占比 13.2%。建议先人工审核误分列表，确认后再写回图谱。

验证步骤：
- 1. 人工审核 suspected_misclassified_core 列表
- 2. 确认每个节点的 suggested_frontend_layer 是否合理
- 3. 如需调整，修改分层规则后重跑审计
- 4. 确认无误后，再考虑写回图谱 visibility 字段

## 八、声明

本轮为只读审计，未修改主图谱、前端图谱、内容索引、内容正文、Flutter代码
