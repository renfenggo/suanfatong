# -*- coding: utf-8 -*-
"""M1-5 侦查：refined（Draft 源）与 io_v4_4（Publish 产物）schema 差异分析。"""
import json
import collections

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
IO_V4_4 = r"assets/data/knowledge/io_v4_4.json"

refined = json.load(open(REFINED, encoding="utf-8"))
io = json.load(open(IO_V4_4, encoding="utf-8"))

print("== 顶层 keys ==")
print("refined:", list(refined.keys()))
print("io_v4_4:", list(io.keys()))

print("\n== meta ==")
print("refined meta:", json.dumps(refined.get("meta", {}), ensure_ascii=False)[:300])
print("io_v4_4 meta:", json.dumps(io.get("meta", {}), ensure_ascii=False)[:300])

rc = refined.get("categories", [])
ic = io.get("categories", [])
print("\n== categories ==")
print("refined:", len(rc), [c.get("name") for c in rc])
print("io_v4_4:", len(ic), [c.get("name") for c in ic])


def cat_fields(cats, label):
    print(f"\n== {label} category keys ==")
    ks = collections.Counter()
    for c in cats:
        ks.update(c.keys())
    print(dict(ks))
    secs = [s for c in cats for s in c.get("sections", [])]
    print(f"{label} section keys:", dict(collections.Counter(k for s in secs for k in s)))
    items = [i for s in secs for i in s.get("items", [])]
    print(f"{label} item keys:", dict(collections.Counter(k for i in items for k in i)))
    return secs, items


rsecs, ritems = cat_fields(rc, "refined")
isecs, iitems = cat_fields(ic, "io_v4_4")

print("\n== 数量 ==")
print("refined items:", len(ritems), "io_v4_4 items:", len(iitems))

print("\n== refined item 示例（首个） ==")
print(json.dumps(ritems[0], ensure_ascii=False, indent=1)[:1200])
print("\n== io_v4_4 item 示例（同 id） ==")
rid = ritems[0].get("id")
same = next((i for i in iitems if i.get("id") == rid), None)
print(json.dumps(same, ensure_ascii=False, indent=1)[:1200] if same else "NOT FOUND")
