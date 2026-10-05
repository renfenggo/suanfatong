# Stage3F Batch3 Full40 Dependency Cleanup 报告

## 基本信息

| 项目 | 值 |
|------|------|
| **批次** | Stage3F Batch3 Full40 |
| **清理候选数** | 11 |
| **全部清理成功** | 是 |
| **生成时间** | 2026-05-25T17:30:00 |
| **主图谱修改** | 否 |

## 清理前后对比

| 指标 | 清理前 | 清理后 |
|------|--------|--------|
| dependency_cleanup_required | true | **false** |
| dependency_mapping_risk 数量 | 11 | **0** |
| 未解析依赖 | 11 | **0** |
| section ref 依赖 | 待检查 | **0** |

## 各候选依赖清理详情

| # | 候选 | Section | direct_pre | rel | Confidence |
|---|------|---------|-----------|-----|-----------|
| 1 | 强连通分量 DAG：Dag Reachability | 2.21 | 2.15.1, 2.9.7 | 2.21.32 | high |
| 2 | 动态图连通性：Divide And Conquer On Time | 2.21 | 2.1.34, 3.4.1 | 2.21.36 | high |
| 3 | 强连通分量 DAG：Dominating Components | 2.21 | 2.15.1, 2.15.10 | 2.21.32 | high |
| 4 | 动态图连通性：Edge Interval Model | 2.21 | 2.21.27, 3.4.1 | 2.21.36 | high |
| 5 | 强连通分量 DAG：Minimum Edges To Strong | 2.21 | 2.15.1, 2.15.10 | 2.21.32, 2.21.49 | high |
| 6 | 位集与线性基：Rollback Linear Basis | 3.13 | 2.18.3, 3.13.49 | 3.13.25 | high |
| 7 | 位集与线性基：Maximum Xor Query | 3.13 | 2.18.3, 2.17.6 | 3.13.39 | high |
| 8 | 位集与线性基：Rank Over Gf2 | 3.13 | 2.18.3, 2.17.8 | - | high |
| 9 | 位集与线性基：Basis With Deletion | 3.13 | 2.18.3, 3.13.49 | - | high |
| 10 | 线段树变体：Split | 3.13 | 3.7.2 | 3.7.22 | high |
| 11 | 高级并查集：Parity | 3.13 | 3.4.1, 3.4.4 | - | high |

## 清理明细

### 2.21 高级图论扩展 (5 个)

#### 1. 强连通分量 DAG：Dag Reachability
- **原始依赖建议**: SCC, DAG, 强连通分量
- **清理后 direct_pre**: 2.15.1 (强连通分量 SCC), 2.9.7 (DAG 判定)
- **清理后 rel**: 2.21.32 (强连通分量 DAG：Condensation Applications)
- **说明**: 依赖明确，SCC 和 DAG 是前置知识；rel 指向同类 DAG 概念节点

#### 2. 动态图连通性：Divide And Conquer On Time
- **原始依赖建议**: 线段树分治, 动态连通性, 并查集
- **清理后 direct_pre**: 2.1.34 (线段树分治), 3.4.1 (并查集)
- **清理后 rel**: 2.21.36 (离线动态连通性线段树分治)
- **说明**: 线段树分治是核心前置，rel 指向已有同类节点

#### 3. 强连通分量 DAG：Dominating Components
- **原始依赖建议**: SCC, DAG, 强连通分量缩点
- **清理后 direct_pre**: 2.15.1 (强连通分量 SCC), 2.15.10 (强连通分量缩点)
- **清理后 rel**: 2.21.32
- **说明**: SCC 缩点是必需的前置操作

#### 4. 动态图连通性：Edge Interval Model
- **原始依赖建议**: 动态连通性, 线段树, 并查集
- **清理后 direct_pre**: 2.21.27 (动态图连通性：Offline Deletion), 3.4.1 (并查集)
- **清理后 rel**: 2.21.36
- **说明**: 依赖已有动态连通性节点

#### 5. 强连通分量 DAG：Minimum Edges To Strong
- **原始依赖建议**: SCC, DAG, 强连通分量缩点
- **清理后 direct_pre**: 2.15.1, 2.15.10
- **清理后 rel**: 2.21.32, 2.21.49
- **说明**: 指向 SCC 基础节点和同类 DAG 节点

### 3.13 高级数据结构扩展 (6 个)

#### 6. 位集与线性基：Rollback Linear Basis
- **原始依赖建议**: 线性基, 可持久化
- **清理后 direct_pre**: 2.18.3 (线性基), 3.13.49 (Linear Basis Merge)
- **清理后 rel**: 3.13.25 (Persistent Linear Basis)
- **说明**: 线性基 + Merge 操作是回滚线性基的前置

#### 7. 位集与线性基：Maximum Xor Query
- **原始依赖建议**: 线性基, 最大异或
- **清理后 direct_pre**: 2.18.3 (线性基), 2.17.6 (线性基求第 k 小异或和)
- **清理后 rel**: 3.13.39 (Range Xor Basis)
- **说明**: 线性基基础 + 异或查询操作

#### 8. 位集与线性基：Rank Over Gf2
- **原始依赖建议**: 线性基, GF(2)
- **清理后 direct_pre**: 2.18.3 (线性基), 2.17.8 (线性基与拟阵)
- **清理后 rel**: -
- **说明**: 依赖明确，无需 rel

#### 9. 位集与线性基：Basis With Deletion
- **原始依赖建议**: 线性基, 删除操作
- **清理后 direct_pre**: 2.18.3 (线性基), 3.13.49 (Linear Basis Merge)
- **清理后 rel**: -
- **说明**: 线性基 + Merge 是带删除线性基的前置

#### 10. 线段树变体：Split
- **原始依赖建议**: 线段树, 线段树分裂
- **清理后 direct_pre**: 3.7.2 (线段树基础)
- **清理后 rel**: 3.7.22 (线段树分裂)
- **说明**: 3.7.22 已存在"线段树分裂"节点

#### 11. 高级并查集：Parity
- **原始依赖建议**: 并查集, 带权并查集, 奇偶性
- **清理后 direct_pre**: 3.4.1 (并查集), 3.4.4 (带权并查集)
- **清理后 rel**: -
- **说明**: 依赖明确，带权并查集是 Parity DSU 的前置

## 验证结果

| 检查项 | 结果 |
|--------|------|
| 所有 direct_pre 为现有 item id | 通过 |
| 无 section id 引用 | 通过 |
| 无 dangling refs | 通过 |
| 无候选依赖环 | 通过 |
| 无低置信依赖 | 通过 |

## 结论

| 项目 | 值 |
|------|------|
| dependency_cleanup_required | **false** |
| 推荐操作 | **ready_for_1号线程_merge_full40** |
| recommended_merge_count | **40** |
| 主图谱修改 | **否** |

---

*本清理计划不修改主图谱。仅修复依赖映射。*
