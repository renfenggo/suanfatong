# -*- coding: utf-8 -*-
"""M1-5 侦查 3：补全默认值 / key 顺序规则 / 序列化格式。"""
import json
import collections

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
IO_V4_4 = r"assets/data/knowledge/io_v4_4.json"

refined = json.load(open(REFINED, encoding="utf-8"))
io = json.load(open(IO_V4_4, encoding="utf-8"))

# ---------- 序列化格式 ----------
raw = open(IO_V4_4, "rb").read()
print("== io_v4_4 格式 ==")
print("BOM:", raw[:3] == b"\xef\xbb\xbf", "CRLF:", b"\r\n" in raw[:5000])
head = raw[:400].decode("utf-8")
print("head snippet:", repr(head[:200]))
# 找 indent：数行首空格
import re
m = re.search(br'\n( +)"', raw)
print("indent sample:", m.group(1) if m else None)

raw_r = open(REFINED, "rb").read()
print("\n== refined 格式 ==")
print("BOM:", raw_r[:3] == b"\xef\xbb\xbf", "CRLF:", b"\r\n" in raw_r[:5000])
m2 = re.search(br'\n( +)"', raw_r)
print("indent sample:", m2.group(1) if m2 else None)


def items(doc):
    out = {}
    for c in doc["categories"]:
        for s in c.get("sections", []):
            for i in s.get("items", []):
                out[i["id"]] = i
    return out


ri, ii = items(refined), items(io)

# ---------- io-only 字段的默认值 ----------
print("\n== io-only 字段补全值分布 ==")
for field in ["docx_ids", "merge_type", "parent", "alias", "source",
              "aliases", "level", "pickup_group", "block_id", "pickup_order"]:
    vals = collections.Counter()
    for iid in ri:
        if field not in ri[iid] and field in ii[iid]:
            vals[json.dumps(ii[iid][field], ensure_ascii=False)] += 1
    print(f"  {field}: {dict(vals.most_common(5))}")

# ---------- key 顺序规则 ----------
print("\n== io item key 顺序 ==")
orders = collections.Counter(tuple(ii[iid].keys()) for iid in ii)
print("不同 key 顺序数:", len(orders))
base_order = orders.most_common(1)[0][0]
print("主顺序（出现次数 %d）:" % orders.most_common(1)[0][1])
print(" ", list(base_order))
for order, cnt in orders.most_common(6)[1:]:
    diff_pos = [i for i, (a, b) in enumerate(zip(base_order, order)) if a != b]
    extra = [k for k in order if k not in base_order]
    print(f"  变体 x{cnt}: extra={extra[:6]} 长度={len(order)}")

# ---------- category/section 顺序与结构 ----------
print("\n== category 顺序 ==")
print("refined:", [c["name"] for c in refined["categories"]])
print("io    :", [c["name"] for c in io["categories"]])

# section key 顺序
sec_orders = collections.Counter()
for c in io["categories"]:
    for s in c["sections"]:
        sec_orders[tuple(k for k in s.keys() if k != "items")] += 1
print("io section key 顺序变体:", len(sec_orders))
print(" ", [dict(o and zip(range(len(o)), o)) and list(sec_orders.most_common(2)[0][0])])
