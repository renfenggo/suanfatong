# Stage3E-Batch1 Resolved Pre Validator Logic 分析报告

**报告生成时间**: 2026-05-22  
**批次标识**: Stage3E-Batch1  
**分析模式**: 只读分析，不修改主图谱

---

## 执行摘要

### 任务目标
- 深入分析官方 resolved_pre 计算和校验逻辑
- 找出之前手动修复失败的根本原因
- 生成基于官方逻辑的精确修复方案
- 确保下一阶段能够通过 validate-only

### 分析结果
- ✅ **找到官方计算函数**: `compute_resolved` (line 1336)
- ✅ **找到官方校验函数**: `validate_resolved_closure` (line 1954)
- ✅ **理解失败根因**: 之前的实现与官方逻辑在多个关键点上不一致
- ✅ **生成修复方案**: 复制官方函数精确修复 10 个节点
- 🎯 **成功概率**: 极高

---

## 当前状态

### 基础状态
- **item_count**: 1512 ✅
- **section_count**: 65 ✅
- **mismatch 数量**: 10 个
- **主图谱修改状态**: ❌ 未修改

### 10 个 Mismatch 节点
| 节点 ID | 预期数量 | 实际数量 | 缺失数 |
|---------|---------|---------|-------|
| 2.21.88 | 26 | 22 | 4 |
| 2.21.89 | 26 | 22 | 4 |
| 2.21.90 | 26 | 22 | 4 |
| 2.21.91 | 26 | 22 | 4 |
| 2.21.92 | 26 | 22 | 4 |
| 2.21.93 | 26 | 22 | 4 |
| 2.21.96 | 37 | 33 | 4 |
| 2.21.97 | 37 | 33 | 4 |
| 2.21.98 | 37 | 33 | 4 |
| 2.21.81 | 24 | 22 | 2 |

---

## 官方函数分析

### 1. Resolved Pre 计算函数

**函数名**: `compute_resolved`  
**位置**: refine_item_dependencies.py line 1336  
**签名**: `def compute_resolved(edges, item_ids):`

#### 官方实现逻辑
```python
def compute_resolved(edges, item_ids):
    memo, visiting = {}, set()

    def resolve(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return []  # 环检测
        visiting.add(node)
        out = []
        for dep in edges.get(node, []):
            if dep in item_ids:
                out.extend(resolve(dep))  # 先递归展开依赖
                out.append(dep)           # 再添加依赖本身
        visiting.remove(node)
        memo[node] = unique([x for x in out if x != node])  # 去重并排除自身
        return memo[node]

    return {item_id: resolve(item_id) for item_id in item_ids}
```

#### 关键特性
1. **算法**: DFS 递归 + Memoization
2. **顺序**: 深度优先，先展开依赖再添加依赖本身
3. **去重**: 使用 `unique` 函数保持首次出现顺序
4. **环检测**: 使用 `visiting` 集合检测环
5. **自身排除**: `if x != node` 条件

### 2. Mismatch 校验函数

**函数名**: `validate_resolved_closure`  
**位置**: refine_item_dependencies.py line 1954  
**签名**: `def validate_resolved_closure(graph):`

#### 官方实现逻辑
```python
def validate_resolved_closure(graph):
    idx = build_indexes(graph)
    item_by_id = idx["item_by_id"]
    edges = {item["id"]: [d for d in item.get("direct_pre", []) if d in item_by_id] 
             for item in idx["items"]}
    expected = compute_resolved(edges, set(item_by_id))  # 重新计算预期
    mismatches = []
    for item_id, exp in expected.items():
        actual = item_by_id[item_id].get("resolved_pre", []) or []
        if actual != exp:
            # 只记录数量，不记录具体列表
            mismatches.append({"id": item_id, "expected_count": len(exp), 
                              "actual_count": len(actual)})
            if len(mismatches) >= 50:
                break
    return mismatches
```

#### 关键特性
1. **预期生成**: 使用相同的 `compute_resolved` 函数
2. **过滤机制**: 只保留 `item_by_id` 中的依赖（排除 section id）
3. **比较方式**: 列表完全比较 `actual != exp`
4. **输出格式**: 只输出数量，不输出预期 resolved_pre 列表
5. **限制**: 最多记录 50 个 mismatches

### 3. 辅助函数

#### unique 函数
**位置**: refine_item_dependencies.py line 127  
**签名**: `def unique(seq):`

```python
def unique(seq):
    out, seen = [], set()
    for item in seq:
        if item and item not in seen:  # 过滤空值并去重
            seen.add(item)
            out.append(item)
    return out
```

#### 关键特性
1. **去重**: 使用 set 确保唯一性
2. **顺序保持**: 保持首次出现的顺序
3. **空值过滤**: `if item` 条件

---

## 官方 Resolved Pre 生成规则详解

### 包含内容
✅ **Direct Pre 依赖**: 直接前置依赖  
✅ **间接依赖**: 递归展开的所有前置依赖  
✅ **保持顺序**: 首次出现顺序  
✅ **去重**: 使用 unique 函数  
✅ **排除自身**: `if x != node`

### 排除内容
❌ **Section 依赖**: 通过 `if d in item_by_id` 过滤  
❌ **自身引用**: 通过 `if x != node` 排除  
❌ **空值**: 通过 `if item` 条件过滤

### 依赖展开规则
1. **递归顺序**: 先展开依赖 (`resolve(dep)`)，再添加依赖本身 (`out.append(dep)`)
2. **深度优先**: 使用递归实现 DFS
3. **记忆化**: 使用 `memo` 缓存计算结果
4. **环处理**: 使用 `visiting` 集合检测环，返回空列表

### 排序规则
- **无显式排序**: 不使用 `sorted` 或其他排序函数
- **自然顺序**: 保持首次出现的顺序
- **稳定性**: 相同的输入总是产生相同的输出

---

## 之前修复失败原因分析

### 尝试 1: 完全重新计算（BFS + section 依赖）

**方法**: 使用 BFS 遍历，包含 section 依赖，显式排序  
**结果**: ❌ 失败  
**差异**: 期望 26/37/24，实际 130/142/133  
**根因分析**:
- ❌ 包含了 section 依赖（官方逻辑排除）
- ❌ 使用了显式排序（官方逻辑保持首次出现顺序）
- ❌ 使用 BFS 而不是 DFS
- ❌ 先添加依赖再展开（官方逻辑相反）

### 尝试 2: 改进的计算逻辑

**方法**: 改进 section 处理，但仍然使用显式排序  
**结果**: ❌ 失败  
**差异**: 期望 26/37/24，实际 134/144/133  
**根因分析**:
- ❌ 仍然包含 section 依赖
- ❌ 仍然使用显式排序
- ❌ 递归顺序可能不正确
- ❌ 没有 memoization 机制

### 尝试 3: 基于差异分析的手动修复

**方法**: 分析 2.21.44、2.21.45 等节点的 resolved_pre，找出缺失依赖  
**结果**: ⚠️ 部分成功  
**差异**: 期望 26/37/24，实际 25/36/22  
**根因分析**:
- ✅ 找到了大部分缺失依赖
- ❌ 仍然缺少少量依赖（可能是递归深度问题）
- ❌ 顺序可能与官方不一致
- ❌ 没有完全遵循官方的展开规则

### 尝试 4: 使用 expected_resolved_pre

**方法**: 尝试使用 validate-only 提供的 expected_resolved_pre  
**结果**: ❌ 失败  
**差异**: N/A - 缺少数据  
**根因分析**:
- ❌ validate-only 不提供 expected_resolved_pre 列表
- ❌ 只提供 expected_count 和 actual_count
- ❌ 无法直接使用预期数据进行修复

---

## 关键差异总结

### 1. Section 依赖处理
| 项目 | 我的实现 | 官方逻辑 |
|------|---------|---------|
| 是否包含 | ✅ 包含 | ❌ 排除 |
| 处理方式 | 添加 section 下所有 item | 通过 `if d in item_by_id` 过滤 |
| 影响 | 导致 resolved_pre 数量过大 | 只处理 item 依赖 |

### 2. 排序策略
| 项目 | 我的实现 | 官方逻辑 |
|------|---------|---------|
| 是否排序 | ✅ 显式排序 | ❌ 保持首次出现顺序 |
| 排序函数 | `sorted(result)` | `unique(seq)` 保持顺序 |
| 影响 | 改变依赖顺序 | 保持原始出现顺序 |

### 3. 依赖展开顺序
| 项目 | 我的实现 | 官方逻辑 |
|------|---------|---------|
| 展开顺序 | 先添加依赖再展开 | 先展开依赖再添加 |
| 代码逻辑 | `out.append(dep); out.extend(resolve(dep))` | `out.extend(resolve(dep)); out.append(dep)` |
| 影响 | 可能影响依赖的深度和顺序 |

### 4. 算法类型
| 项目 | 我的实现 | 官方逻辑 |
|------|---------|---------|
| 算法类型 | BFS（队列） | DFS（递归） |
| 缓存机制 | 无 | 有 memoization |
| 环检测 | 无 | 有 visiting 集合 |
| 影响 | 可能产生不同的计算路径 |

---

## 推荐的 v4-Step2 修复方案

### 方案 1: 复制官方函数（推荐）

**方法**: 精确复制 `compute_resolved` 和 `unique` 函数到临时脚本  
**可行性**: ✅ 极高  
**成功率**: ✅ 极高  
**步骤**:
1. 创建临时脚本 `fix_resolved_pre_using_official_logic.py`
2. 精确复制官方 `compute_resolved` 函数
3. 精确复制官方 `unique` 函数
4. 只对 10 个 mismatch 节点应用修复
5. 比较修复后的数量与预期数量
6. 如果匹配，保存修改
7. 运行 validate-only 验证

**优势**:
- ✅ 与官方逻辑完全一致
- ✅ 保证能够通过校验
- ✅ 风险最低
- ✅ 实现最简单

**预期结果**: 0 个 mismatches

### 方案 2: 导入官方函数

**方法**: 尝试从 refine_item_dependencies 导入官方函数  
**可行性**: ⚠️ 中等  
**成功率**: ✅ 高  
**步骤**:
1. 测试是否可以导入模块而不运行主函数
2. 导入 `compute_resolved` 和 `unique` 函数
3. 对 10 个 mismatch 节点应用修复
4. 验证结果

**优势**:
- ✅ 保持单一真相源
- ✅ 无需复制代码

**劣势**:
- ⚠️ 可能无法导入（脚本结构限制）
- ⚠️ 依赖外部模块

### 方案 3: 重写实现

**方法**: 基于官方逻辑规范重写实现  
**可行性**: ✅ 高  
**成功率**: ✅ 高  
**要求**:
- ✅ 使用 DFS 递归 + memoization
- ✅ 先展开依赖再添加依赖本身
- ✅ 使用 unique 函数保持首次出现顺序
- ✅ 排除 section 依赖
- ✅ 实现环检测机制

**优势**:
- ✅ 不依赖外部文件
- ✅ 完全控制实现

**劣势**:
- ⚠️ 需要严格遵循规范
- ⚠️ 可能遗漏细节

---

## 修复策略详细说明

### 目标节点
10 个 mismatch 节点：
- Dynamic MST 系列: 2.21.88, 2.21.89, 2.21.90, 2.21.91, 2.21.92, 2.21.93
- Global Min-Cut 系列: 2.21.96, 2.21.97, 2.21.98  
- Directed MST 系列: 2.21.81

### 修复流程
1. **预验证**: 运行 validate-only 确认 10 个 mismatches
2. **创建备份**: `backups/merged_knowledge_graph_item_dependencies_refined_before_stage3e_batch1_resolved_pre_fix_v4.json`
3. **应用修复**: 使用官方逻辑计算预期 resolved_pre
4. **替换数据**: 只替换 10 个节点的 `resolved_pre` 字段
5. **后验证**: 运行 validate-only 确认 0 个 mismatches
6. **生成报告**: 记录修复详情

### 验证标准
- ✅ item_count = 1512
- ✅ section_count = 65
- ✅ resolved_pre_mismatches = 0
- ✅ validation passed = true
- ✅ 不修改 direct_pre
- ✅ 不修改 rel
- ✅ 不修改其他字段

---

## 成功概率评估

| 方案 | 成功概率 | 实现难度 | 风险等级 | 推荐指数 |
|------|---------|---------|---------|---------|
| 方案1: 复制官方函数 | 95% | 极低 | 极低 | ⭐⭐⭐⭐⭐ |
| 方案2: 导入官方函数 | 85% | 低 | 低 | ⭐⭐⭐⭐ |
| 方案3: 重写实现 | 80% | 中等 | 中等 | ⭐⭐⭐ |

---

## 预期工作量

| 方案 | 预计时间 | 所需技能 | 复杂度 |
|------|---------|---------|-------|
| 方案1: 复制官方函数 | 5-10 分钟 | Python 基础 | 极低 |
| 方案2: 导入官方函数 | 10-15 分钟 | Python 模块导入 | 低 |
| 方案3: 重写实现 | 15-30 分钟 | 算法实现 | 中等 |

---

## 限制遵守情况

### 完全遵守的限制
- ✅ **不修改主图谱**: 未修改任何文件
- ✅ **不修改 dependency_validation_result.json**: 只读取
- ✅ **不修改 item_dependency_refinement_report.md**: 只读取
- ✅ **不修改 refine_item_dependencies.py**: 只分析
- ✅ **不新增 item**: 保持 1512 个
- ✅ **不删除 item**: 保持 1512 个
- ✅ **不修改 direct_pre**: 不涉及
- ✅ **不继续 batch_2**: 未执行
- ✅ **只输出分析报告**: 只生成了报告

### 本阶段执行的操作
- ✅ 读取并分析 refine_item_dependencies.py
- ✅ 定位官方函数
- ✅ 理解官方逻辑
- ✅ 分析失败原因
- ✅ 生成修复方案
- ✅ 输出分析报告 JSON 和 MD

---

## 下一步推荐

### v4-Step2 执行计划
**推荐方案**: 方案1 - 复制官方函数

**执行步骤**:
1. 创建 `fix_resolved_pre_using_official_logic.py` 脚本
2. 精确复制 `compute_resolved` 和 `unique` 函数
3. 对 10 个 mismatch 节点应用修复
4. 验证修复效果
5. 运行 validate-only 确认通过

**预期结果**: 0 个 mismatches，validation passed = true

---

## 技术洞察

### 官方设计的考虑
1. **性能优化**: 使用 memoization 避免重复计算
2. **环处理**: 优雅处理依赖环的情况
3. **顺序保持**: 保持首次出现顺序而非字母顺序
4. **类型过滤**: 只处理 item 依赖，排除 section 依赖
5. **简洁性**: 使用简单的递归 + 去重逻辑

### 与常见的误解
- ❌ **误解**: resolved_pre 应该按字母顺序排序
- ✅ **实际**: 保持首次出现的顺序

- ❌ **误解**: resolved_pre 应该包含 section 依赖
- ✅ **实际**: 只包含 item 依赖

- ❌ **误解**: resolved_pre 应该先添加依赖再展开
- ✅ **实际**: 先展开依赖再添加

---

## 结论

### 分析完成情况
✅ **完全完成**: 成功分析了所有官方函数，理解了计算逻辑，找到了失败根因

### 关键发现
🎯 **核心发现**: 之前的实现与官方逻辑在 section 依赖处理、排序策略、依赖展开顺序等关键点上不一致

### 解决方案
🎯 **最佳方案**: 精确复制官方函数进行修复，预计成功率 95%

### 下一阶段
🚀 **v4-Step2**: 使用官方逻辑修复 10 个 mismatch 节点，预期完全通过 validate-only

---

**报告结束**

**状态**: ✅ 分析完成，找到了失败根因，生成了精确的修复方案

**重要说明**: 本阶段为纯分析阶段，未对主图谱进行任何修改。下一阶段将使用官方逻辑精确修复 10 个 mismatch 节点，预期完全通过 validate-only 验证。