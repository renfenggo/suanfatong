# -*- coding: utf-8 -*-
"""M1-5 侦查 5：alias 'other' 229 个与 level 475 个的推导源。"""
import json
import collections

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
IO_V4_4 = r"assets/data/knowledge/io_v4_4.json"

refined = json.load(open(REFINED, encoding="utf-8"))
io = json.load(open(IO_V4_4, encoding="utf-8"))


def items(doc):
    out = {}
    for c in doc["categories"]:
        for s in c.get("sections", []):
            for i in s.get("items", []):
                out[i["id"]] = i
    return out


ri, ii = items(refined), items(io)

# c) 229 个 other alias：与 refined.name 的关系
cnt = collections.Counter()
samples = []
for iid in ri:
    if "alias" not in ri[iid] and "alias" in ii[iid]:
        v = ii[iid]["alias"]
        if v == []:
            continue
        if v == ri[iid].get("aliases"):
            continue
        r = ri[iid]
        if v == [r["name"]]:
            cnt["==[name]"] += 1
        elif r["name"] in v:
            cnt["name in v"] += 1
        elif v[0] in r["name"]:
            cnt["v0 in name"] += 1
        else:
            cnt["unrelated"] += 1
            if len(samples) < 5:
                samples.append((iid, v, r["name"], r.get("en_name")))
print("c) alias other 229 分类:", dict(cnt))
for s in samples:
    print("   ", s)

# d) level 475 个：与 quality_score/mapping_score/review_priority 的关系
pairs = collections.Counter()
for iid in ri:
    if "level" not in ri[iid] and "level" in ii[iid]:
        r = ri[iid]
        qs = r.get("quality_score")
        pairs[(ii[iid]["level"], qs)] += 1
print("\nd) level x quality_score:")
for combo, n in sorted(pairs.items()):
    print("   ", combo, n)

# 是否这 475 个 == refined 有 need_manual_review 的集合？
nlv = {k for k in ri if "level" not in ri[k] and "level" in ii[k]}
nmr = {k for k in ri if "need_manual_review" in ri[k]}
print("475 level 补全集 == need_manual_review 集:", nlv == nmr, len(nlv), len(nmr))
# level 与 need_manual_review 值的关系
nv = collections.Counter()
for iid in nlv:
    nv[(ii[iid]["level"], ri[iid].get("need_manual_review"))] += 1
print("level x need_manual_review 值:", dict(nv))
