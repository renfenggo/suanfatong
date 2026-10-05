#!/usr/bin/env python3
"""验证动画 MVP Demo 的 4 个新动画。

检查项:
1. 4 个 animationId 唯一
2. 4 个 itemId 在 manifest 中能找到
3. JSON 格式合法
4. 每个动画 steps 非空
5. 不破坏已有 111 个动画（manifest 总数应为 115）
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

MANIFEST_PATH = BASE / "assets" / "data" / "cpp" / "animations" / "cpp_animation_manifest.json"

NEW_ANIMATIONS = [
    ("cpp_dfs_graph_traversal", "2.7.16", "dfs_graph_traversal.json"),
    ("cpp_bfs_graph_traversal", "2.7.17", "bfs_graph_traversal.json"),
    ("cpp_prefix_sum_1d",       "2.4.17", "prefix_sum_1d.json"),
    ("cpp_prefix_sum_2d",       "2.4.18", "prefix_sum_2d.json"),
]

EXPECTED_TOTAL = 115  # 111 old + 4 new

passed = 0
failed = 0
results = []


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        results.append(("PASS", name, detail))
    else:
        failed += 1
        results.append(("FAIL", name, detail))


def main():
    # --- 加载 manifest ---
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        check("manifest JSON 格式合法", True)
    except Exception as e:
        check("manifest JSON 格式合法", False, str(e))
        print("FATAL: 无法读取 manifest，终止。")
        sys.exit(1)

    animations = manifest.get("animations", [])
    check(f"manifest 总数 = {EXPECTED_TOTAL}", len(animations) == EXPECTED_TOTAL,
          f"实际 {len(animations)} 个")

    # --- animationId 唯一性 ---
    all_ids = [a["animationId"] for a in animations]
    unique_ids = set(all_ids)
    check("animationId 全局唯一", len(all_ids) == len(unique_ids),
          f"总数 {len(all_ids)}，唯一 {len(unique_ids)}")

    # --- 4 个新动画的 itemId 在 manifest 中 ---
    for anim_id, item_id, file_name in NEW_ANIMATIONS:
        found = any(a["animationId"] == anim_id and a["itemId"] == item_id
                    for a in animations)
        check(f"manifest 包含 {anim_id} (itemId={item_id})", found)

    # --- 4 个动画 JSON 文件合法性 + steps 非空 ---
    anim_dir = BASE / "assets" / "data" / "cpp" / "animations"
    for anim_id, item_id, file_name in NEW_ANIMATIONS:
        fpath = anim_dir / file_name
        # JSON 合法
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            check(f"{file_name} JSON 格式合法", True)
        except Exception as e:
            check(f"{file_name} JSON 格式合法", False, str(e))
            continue

        # 必要字段
        for field in ["animationId", "itemId", "title", "description",
                      "expectedLearningPoint", "initialState", "steps"]:
            check(f"{file_name} 含字段 {field}", field in data,
                  f"缺失 {field}" if field not in data else "")

        # animationId / itemId 匹配
        check(f"{file_name} animationId = {anim_id}",
              data.get("animationId") == anim_id,
              f"实际 = {data.get('animationId')}")
        check(f"{file_name} itemId = {item_id}",
              data.get("itemId") == item_id,
              f"实际 = {data.get('itemId')}")

        # steps 非空
        steps = data.get("steps", [])
        check(f"{file_name} steps 非空", len(steps) > 0,
              f"共 {len(steps)} 步")

        # 每个 step 有必要字段
        if steps:
            for i, s in enumerate(steps):
                for sf in ["step", "title", "description", "state"]:
                    check(f"{file_name} step[{i}] 含 {sf}", sf in s,
                          f"缺失 {sf}" if sf not in s else "")

    # --- 已有动画未被删除 ---
    check("已有 111 个动画保持", len(animations) >= 111,
          f"manifest 中共 {len(animations)} 个")

    # --- 输出 ---
    print("=" * 60)
    print("动画 MVP Demo 验证报告")
    print("=" * 60)
    for status, name, detail in results:
        tag = f"[{status}]"
        line = f"  {tag} {name}"
        if detail:
            line += f"  -- {detail}"
        print(line)
    print("=" * 60)
    print(f"总计: {passed} PASS, {failed} FAIL")
    if failed == 0:
        print("全部验证通过!")
    else:
        print(f"有 {failed} 项未通过，请检查。")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
