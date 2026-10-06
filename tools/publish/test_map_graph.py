# -*- coding: utf-8 -*-
"""map_graph.py 轻量单测（无 pytest 依赖，python 直接运行）。

覆盖：映射规则单元（补全/丢弃/白名单）、validator 错误检测
（重复 ID/悬空引用/依赖环/节点数不守恒）、semantic_diff 差异检出。
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "map_graph", os.path.join(HERE, "map_graph.py")
)
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

failures = []
LO = {"9.9.9": "L3"}
PO = {"2.9.99": {"pickup_group": ""}}


def check(name, fn):
    try:
        fn()
        print(f"  ok: {name}")
    except AssertionError as e:
        failures.append(name)
        print(f"  FAIL: {name}: {e}")


def expect_map_fail(item):
    """断言 map_item 以 SystemExit 退出。"""
    try:
        mg.map_item(item, LO, PO)
    except SystemExit:
        return
    raise AssertionError("应当失败但没有")


def base_item(**kw):
    item = {
        "id": "2.9.99",
        "name": "测试点",
        "direct_pre": [],
        "resolved_pre": [],
        "rel": [],
        "level": "L1",
        "en_name": "Test",
        "global_aliases": [],
        "tracks": ["beginner"],
        "audience": ["primary_beginner"],
        "visibility": "core",
        "learning_path_policy": {},
        "localization_status": {},
        "content_status": {},
    }
    item.update(kw)
    return item


def t_default_fill():
    out = mg.map_item(base_item(), LO, PO)
    assert out["merge_type"] == "stage3g_full400", out["merge_type"]
    assert out["parent"] == "2.9", out["parent"]
    assert out["alias"] == ["测试点"], out["alias"]
    assert out["aliases"] == [] and out["source"] == [] and out["docx_ids"] == []


check("普通缺省补全：merge_type/parent=id前缀/alias=[name]/空数组", t_default_fill)


def t_alias_from_aliases():
    out = mg.map_item(base_item(aliases=["别名A"]), LO, PO)
    assert out["alias"] == ["别名A"], out["alias"]


check("alias 缺省取 aliases 非空", t_alias_from_aliases)


def t_stage5():
    out = mg.map_item(
        base_item(
            source_tier="seed",
            review_status="pending",
            difficulty=7,
            platform_tags=["A"],
            review_priority=1,
        ),
        LO, PO,
    )
    assert out["merge_type"] == "new_knowledge", out["merge_type"]
    for f in ("review_status", "difficulty", "platform_tags", "review_priority",
              "source_tier"):
        assert f not in out, f


check("stage5 批次：source_tier 标记 -> new_knowledge 且丢评审字段", t_stage5)


def t_drop_pipeline_fields():
    out = mg.map_item(
        base_item(subcategory="x", quality_score=4, candidate_id="c1",
                  need_manual_review=False),
        LO, PO,
    )
    for f in ("subcategory", "quality_score", "candidate_id", "source_tier",
              "category", "need_manual_review"):
        assert f not in out, f


check("全局丢弃 Draft 管线字段", t_drop_pipeline_fields)


def t_level_missing_fails():
    no_level = base_item(id="8.8.8")
    no_level.pop("level")
    expect_map_fail(no_level)


check("level 缺且无 overrides -> 失败", t_level_missing_fails)


def t_unknown_field_fails():
    expect_map_fail(base_item(mystery_field=1))


check("未知字段 -> 白名单拦截失败", t_unknown_field_fails)


def t_pickup_sparse():
    out = mg.map_item(base_item(), LO, PO)
    assert out.get("pickup_group") == "", out.get("pickup_group")
    assert "block_id" not in out and "pickup_order" not in out
    other = mg.map_item(base_item(id="1.1.1", parent="1.1"), LO, PO)
    assert "pickup_group" not in other


check("pickup 稀疏补丁：仅补丁项新增空字段", t_pickup_sparse)


# ---------- validator ----------
def mini_doc(items, sections=("2.1",)):
    return {
        "meta": {},
        "categories": [
            {
                "name": "cat",
                "sections": [
                    {
                        "id": sid,
                        "name": "sec",
                        "items": [i for i in items if i["parent"] == sid],
                    }
                    for sid in sections
                ],
            }
        ],
    }


good_item = dict(base_item(), parent="2.1", id="2.1.1")


def t_validate_ok():
    errs = mg.validate(mini_doc([good_item]), expected_count=1)
    assert errs == [], errs


check("validator：合法小图通过", t_validate_ok)


def t_validate_dup():
    errs = mg.validate(mini_doc([good_item, dict(good_item)]))
    assert any("重复" in e for e in errs), errs


check("validator：重复 item id 检出", t_validate_dup)


def t_validate_dangling():
    item = dict(base_item(), parent="2.1", id="2.1.2", direct_pre=["7.7.7"])
    errs = mg.validate(mini_doc([item]))
    assert any("7.7.7" in e for e in errs), errs


check("validator：悬空引用检出", t_validate_dangling)


def t_validate_count():
    errs = mg.validate(mini_doc([good_item]), expected_count=99)
    assert any("守恒" in e for e in errs), errs


check("validator：节点数不守恒检出", t_validate_count)


def t_validate_cycle():
    a = dict(base_item(), parent="2.1", id="2.1.1", resolved_pre=["2.1.2"])
    b = dict(base_item(), parent="2.1", id="2.1.2", resolved_pre=["2.1.1"])
    errs = mg.validate(mini_doc([a, b]))
    assert any("环" in e for e in errs), errs


check("validator：依赖环检出", t_validate_cycle)


def t_validate_parent():
    doc = {
        "meta": {},
        "categories": [{
            "name": "cat",
            "sections": [{
                "id": "2.1", "name": "sec",
                "items": [dict(base_item(), parent="9.9", id="2.1.5")],
            }],
        }],
    }
    errs = mg.validate(doc)
    assert any("parent" in e for e in errs), errs


check("validator：parent 不存在检出", t_validate_parent)


# ---------- semantic_diff ----------
def t_semantic_diff():
    assert mg.semantic_diff({"a": 1, "b": {"x": 1}},
                            {"b": {"x": 1}, "a": 1}) == []
    assert mg.semantic_diff({"a": 1}, {"a": 2}) != []
    assert mg.semantic_diff({"a": 1}, {"a": 1, "c": 3}) != []
    assert mg.semantic_diff({"a": [1, 2]}, {"a": [1, 2, 3]}) != []


check("semantic_diff：键序无关 / 值差 / 缺字段 / 长度差检出", t_semantic_diff)


# ---------- meta 映射 ----------
def t_meta():
    out = mg.map_meta(
        {"title": "T1", "stage5_hard_batch1_x": 1},
        {"meta_patch": {"add": {"sync_batch": "b2"}, "set": {"title": "T2"}}},
    )
    assert "stage5_hard_batch1_x" not in out
    assert out["sync_batch"] == "b2"
    assert out["title"] == "T2", out["title"]


check("meta：丢过程前缀键 + patch add/set", t_meta)


print()
if failures:
    print(f"FAILED: {len(failures)} -> {failures}")
    sys.exit(1)
print("ALL MAP_GRAPH TESTS PASSED")
