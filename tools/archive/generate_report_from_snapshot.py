import json

def generate_report_from_snapshot():
    """从快照文件生成报告"""
    
    # 读取快照文件
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\data\thread2_candidate_pool_snapshot.json', 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)
    
    stats = snapshot_data['statistics']
    
    # 生成报告
    report = f"""# 2号线程候选池状态快照报告

## 执行概况

- 执行线程: 2号线程
- 执行时间: 2026-05-22T14:00:00.000Z
- 任务类型: 候选池状态快照统计
- 主图谱状态: 未修改
- 任务目的: 等待1号线程完成主图谱修复

## 统计数据

### 外部候选池状态

- **外部候选总数**: {stats['external_candidates']['total_count']}
- **Green (intermediate)**: {stats['external_candidates']['green_count']}
- **Yellow (advanced)**: {stats['external_candidates']['yellow_count']}
- **Red (expert)**: {stats['external_candidates']['red_count']}

### Aggressive 计划状态

- **已进入 aggressive 计划数量**: {stats['aggressive_planning']['total_aggressive_count']}
- **数据来源**: thread2_stage3e_aggressive_batches.json

### Stage3F 储备池状态

- **Stage3F 储备池总数**: {stats['stage3f_reserve_pool']['total_count']}
- **储备池数据来源**: thread2_candidate_cleanup_stage3f_reserve_pool.json

**储备池按状态分布:**
"""

    # 添加储备池详细分布
    for status, count in stats['stage3f_reserve_pool']['breakdown'].items():
        report += f"- {status}: {count}\n"

    report += f"""
### Problem Patterns Handoff 状态

- **Problem patterns handoff 总数**: {stats['problem_patterns_handoff']['total_count']}
- **Handoff 数据来源**: thread2_problem_patterns_handoff_clean.json

**按优先级分布:**
"""

    # 添加优先级分布
    for priority, count in stats['problem_patterns_handoff']['priority_breakdown'].items():
        report += f"- {priority}: {count}\n"

    report += f"""
## 当前瓶颈分析

### 主图谱状态
- **状态**: 待1号线程修复 resolved_pre_mismatch
- **可用性**: 暂时不能作为继续合并依据

### 暂不能生成 Stage3F whitelist 的原因

1. **主图谱存在 resolved_pre_mismatch**
   - 1号线程正在进行修复
   - 修复前无法作为合并依据

2. **依赖验证准确性受限**
   - 修复前无法准确依赖验证
   - 可能导致候选合并错误

3. **合并依据不稳定**
   - 主图谱当前基线不稳定
   - 合并决策可能基于错误状态

4. **协调流程要求**
   - 需要等待1号线程完成修复
   - 需要确认 stable_baseline

### 阻塞的操作

以下操作当前被阻塞:
- candidate merging (候选合并)
- whitelist generation (白名单生成)
- dependency validation (依赖验证)
- graph modification (图谱修改)

## 2号线程下一步行动计划

### 等待1号线程修复完成后的操作步骤

1. **等待1号线程完成主图谱修复并确认 stable_baseline**
   - 监控1号线程修复进度
   - 确认修复后的主图谱稳定状态

2. **重新读取修复后的主图谱进行候选依赖验证**
   - 更新候选依赖关系
   - 重新验证候选的可行性

3. **更新 Stage3F 储备池状态**
   - 移除与1号线程修复冲突的候选
   - 刷新储备池状态标记

4. **生成正式的 Stage3F whitelist**
   - 基于修复后的主图谱
   - 与1号线程协调合并优先级

5. **与1号线程协调 Stage3F 合并批次执行计划**
   - 确定合并批次顺序
   - 避免冲突和重复工作

6. **准备 Stage3G 子话题合并规划**
   - 基于Stage3F合并结果
   - 提前准备下一阶段工作

## 线程协调状态

### 资源状态

- **1号线程**: 修复主图谱 resolved_pre_mismatch
- **2号线程**: 等待中 - 仅做状态统计
- **3号线程**: 待接收 problem_patterns handoff
- **线程协调需求**: 是

### 数据源状态

- **外部候选池数据**: 可用
- **Stage3E 批次数据**: 可用
- **Stage3F 储备池数据**: 可用
- **Problem patterns handoff 数据**: 可用

## 主图谱状态确认

- **主图谱是否修改**: **否**
- **本次任务目的**: 仅状态统计，不涉及图谱修改
- **图谱状态**: 等待1号线程修复完成

## 输出文件

1. `data/thread2_candidate_pool_snapshot.json` - 候选池状态快照数据
2. `docs/thread2_candidate_pool_snapshot_report.md` - 本报告

## 重要提醒

1. **不进行合并**: 本次任务仅做状态统计，不进行任何候选合并
2. **不生成白名单**: 不生成任何形式的合并白名单
3. **不修复主图谱**: 不参与主图谱修复工作，等待1号线程完成
4. **不运行验证**: 不运行任何形式的图谱验证
5. **等待为主**: 当前阶段以等待和状态监控为主

## 候选池整体状态

- **外部候选池**: {stats['external_candidates']['total_count']} 个候选待处理
- **Aggressive 计划**: {stats['aggressive_planning']['total_aggressive_count']} 个候选已规划
- **Stage3F 储备池**: {stats['stage3f_reserve_pool']['total_count']} 个候选待合并
- **Problem patterns**: {stats['problem_patterns_handoff']['total_count']} 个模式待处理

---

报告生成时间: 2026-05-22T14:00:00.000Z
生成者: 2号线程
任务类型: 候选池状态快照统计
主图谱修改状态: 否
下一阶段: 等待1号线程完成主图谱修复
"""

    # 保存报告
    with open(r'c:\Users\renfenggo\Documents\trae_projects\suanfatong\docs\thread2_candidate_pool_snapshot_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("✓ 报告文件已保存到 docs/thread2_candidate_pool_snapshot_report.md")
    print("\n✓ 任务完成！仅进行了状态统计，未进行任何合并或修改操作。")
    
    return report

# 生成报告
report = generate_report_from_snapshot()
print("报告生成完成！")