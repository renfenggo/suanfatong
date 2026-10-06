# -*- coding: utf-8 -*-
"""M1-5 侦查 4：验证 io-only 补全字段的可推导规则。"""
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

# a) new_knowledge 600 批次 == refined 有 source_tier 的集合？
new_kn = {k for k in ii if ii[k].get("merge_type") == "new_knowledge"}
ref_tier = {k for k in ri if "source_tier" in ri[k]}
ref_cat = {k for k in ri if "category" in ri[k]}
print("a) new_knowledge:", len(new_kn), "ref source_tier:", len(ref_tier),
      "equal:", new_kn == ref_tier, "category equal:", new_kn == ref_cat)

# b) io 补的 parent == id 前缀？
ok = bad = 0
for iid in ri:
    if "parent" not in ri[iid] and "parent" in ii[iid]:
        expect = iid.rsplit(".", 1)[0] if iid.count(".") >= 1 else ""
        if ii[iid]["parent"] == expect:
            ok += 1
        else:
            bad += 1
            if bad <= 3:
                print("   parent mismatch:", iid, "io=", ii[iid]["parent"], "expect=", expect)
print("b) parent==id前缀:", ok, "mismatch:", bad)

# c) io 补的 alias 来源：refined global_aliases / aliases / en_name?
cnt = collections.Counter()
mismatches = []
for iid in ri:
    if "alias" not in ri[iid] and "alias" in ii[iid]:
        v = ii[iid]["alias"]
        if v == []:
            cnt["empty->[]"] += 1
        elif v == ri[iid].get("global_aliases"):
            cnt["==global_aliases"] += 1
        elif v == ri[iid].get("aliases"):
            cnt["==aliases"] += 1
        else:
            cnt["other"] += 1
            if len(mismatches) < 5:
                mismatches.append((iid, v, ri[iid].get("aliases"), ri[iid].get("global_aliases"), ri[iid].get("en_name")))
print("c) alias 补全来源:", dict(cnt))
for m in mismatches:
    print("   ", m)

# d) io 补的 level（475）来源：refined difficulty？
cnt2 = collections.Counter()
lvl_mismatch = collections.Counter()
for iid in ri:
    if "level" not in ri[iid] and "level" in ii[iid]:
        lv = ii[iid]["level"]
        d = ri[iid].get("difficulty")
        cnt2[(lv, d)] += 1
print("d) level x difficulty 组合（io补level的475个）:")
for combo, n in cnt2.most_common(20):
    print("   ", combo, n)

# e) stage3g_full400 的 623 个：refined 是否有可识别标记？
g400 = {k for k in ii if ii[k].get("merge_type") == "stage3g_full400"}
marks = collections.Counter()
for iid in g400:
    r = ri[iid]
    if "quality_score" in r or "subcategory" in r or "candidate_id" in r:
        marks["has_quality/subcat/candidate"] += 1
    if "difficulty" in r:
        marks["has_difficulty"] += 1
    if "stage3e_batch" in r:
        marks["has_stage3e_batch"] += 1
print("e) stage3g_full400 623 个 refined 标记分布:", dict(marks))
# 与其他缺 merge_type 组对照：new_kn 的标记
marks2 = collections.Counter()
for iid in new_kn:
    r = ri[iid]
    marks2["has_quality" if "quality_score" in r else "no_quality"] += 1
print("   new_knowledge 600 个 quality_score:", dict(marks2))
