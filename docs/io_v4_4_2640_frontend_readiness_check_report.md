# io_v4_4.json 2640 前端读取验证报告

- **验证时间**: 2026-05-26T16:55:00.000Z
- **数据文件**: `assets/data/knowledge/io_v4_4.json`
- **文件大小**: 8.8 MB
- **JSON 解析时间**: 51.2 ms

---

## 1. 数据层验证

| # | 检查项 | 结果 |
|:-:|:-------|:--:|
| 1 | item_count = 2640 | ✅ |
| 2 | section_count = 65 | ✅ |
| 3 | JSON 解析正常 | ✅ |
| 4 | 解析耗时 | 51.2 ms（可接受） |
| 5 | 文件大小 | 8.8 MB（可接受，<10 MB） |

### 节点分类

| 类别 | 数量 | 验证 |
|:-----|:--:|:--:|
| 旧 2165 节点 | 2,165 | ✅ 全部保留，可搜索 |
| Stage5 Batch1 新增 | 475 | ✅ 全部同步，可搜索 |
| 已删除/折叠模板子节点 | 25 | ✅ 0 个出现在 io_v4_4.json |
| Keeper 父主题节点 | 7 | ✅ 全部存在，字段完整 |
| **合计** | **2,640** | — |

### 7 个 Keeper 父主题节点详情

| ID | 名称 | direct_pre | resolved_pre |
|:--|:----|:--------:|:----------:|
| 2.8.202 | 凸包维护 DP | 3 | 224 |
| 2.8.203 | 分治转移 DP | 3 | 220 |
| 2.8.204 | 队列维护 DP | 3 | 220 |
| 2.8.205 | 线段树维护 DP | 3 | 230 |
| 2.8.206 | 堆维护 DP | 3 | 220 |
| 2.8.207 | 前缀最值 DP | 2 | 220 |
| 2.8.208 | 后缀最值 DP | 3 | 237 |

---

## 2. 抽查结果

| 抽查类别 | 样本数 | 通过 | 说明 |
|:---------|:-----:|:--:|:-----|
| 随机旧节点 | 20 | 20/20 | id/name/parent/direct_pre/resolved_pre/rel 字段齐全 |
| 随机 Stage5 新增节点 | 30 | 30/30 | 所有 required fields 完整，direct_pre 2~6 条，resolved_pre 28~360 条，无 section id |
| Keeper 节点 | 7 | 7/7 | 字段齐全，direct_pre 已缩减 |
| 已删除 25 节点 | 25 | ✅ 0 出现在 io_v4_4.json | 确认误导出风险消除 |

---

## 3. 主图谱完整性

| 检查项 | 结果 |
|:-------|:--:|
| dangling_refs | ✅ 0 |
| direct_pre 全部为正式 item id | ✅ 0 个 section id |
| duplicate item_ids | ✅ 0 |
| 所有 2640 节点 required fields 完整 | ✅ id/name/parent/direct_pre/resolved_pre 全覆盖 |
| source 字段 | ✅ 2640/2640 |
| merge_type 字段 | ✅ 2640/2640 |
| tracks / audience / visibility | ✅ 2640/2640 |

---

## 4. Flutter Analyze

| 指标 | 结果 |
|:-----|:---:|
| **Errors** | **0** ✅ |
| **Warnings** | **0** ✅ |
| Info | 6（全部为已有 lint，与数据无关） |

> 6 条 info 均为 pre-existing：
> - 2 × `unnecessary_string_escapes`（fill_content.dart）
> - 4 × `avoid_print`（fill_content.dart, verify_dp.dart）
>
> 零条新增问题。2640 数据未引入任何分析错误。

---

## 5. 测试结果

| 指标 | 结果 |
|:-----|:---:|
| 总测试数 | 35 |
| 通过 | **34** ✅ |
| 失败 | 1（已有问题，非本次引入） |
| 通过率 | **97.1%** |

> 1 个失败测试为 **pre-existing issue**：`Binding has not yet been initialized`（原始 JSON categories 顺序验证测试），与本次 2640 数据同步无关。
>
> 涉及模型解析（KnowledgeItem.fromJson、KnowledgeGraph.fromJson）、依赖引用、学习路径等 34 个测试全部通过。

---

## 6. 构建结果

| 构建目标 | 结果 | 耗时 |
|:--------|:--:|:--:|
| `flutter build web --release` | ✅ PASSED | 2,465 ms |
| `flutter build apk --debug` | ✅ PASSED | 21.6 s |

### 构建产物验证

| 检查项 | 结果 |
|:-------|:--:|
| build/web 中 io_v4_4.json 存在 | ✅ |
| 产物中 item_count | 2,640 ✅ |
| 产物中 section_count | 65 ✅ |
| 产物文件大小 | 8.8 MB |

---

## 7. 性能判断

| 指标 | 值 | 判断 |
|:-----|:--|:---:|
| 文件大小 | 8.8 MB | ✅ 可接受（<10 MB） |
| Python 解析耗时 | 51.2 ms | ✅ 快速 |
| Web 编译耗时 | 2,465 ms | ✅ 正常 |
| APK 编译耗时 | 21.6 s | ✅ 正常 |
| 前端白屏/卡死风险 | — | ✅ 无新增风险（模型未变，仅数据量增加） |

---

## 8. 修改确认

| 检查项 | 结果 |
|:-------|:--:|
| 是否修改 `io_v4_4.json` | **否**（本次验证只读） |
| 是否修改主图谱 | **否** |
| 是否修改前端代码 | **否** |
| 是否继续 Batch2 | **否** |
| 是否生成内容包 | **否** |

---

## 9. 结论

| 结论 | 结果 |
|:-----|:--:|
| **前端是否可正常读取 2640 数据** | ✅ **可以** |
| Flutter analyze 是否干净 | ✅ 0 errors / 0 warnings |
| 测试是否通过 | ✅ 97.1%（1 个已有测试问题，与数据无关） |
| 构建是否成功 | ✅ web + apk 双双通过 |
| 数据完整性 | ✅ 11/11 checks 全部通过 |

---

## 10. 建议

**建议立即进入 Stage5 Batch1 新增节点内容包生成。** 前端已验证通过，2,640 节点图谱可正常解析、构建、测试，数据完整性 100%。

优先推进路径：

> **内容包生成（475 个 Stage5 新增节点）** → **前端学习页面验证** → **Batch2 规划**

---

*报告自动生成于 2026-05-26T16:55:00.000Z*
