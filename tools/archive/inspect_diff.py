# -*- coding: utf-8 -*-
"""M1-5 侦查 2：refined vs io_v4_4 逐字段深度 diff，量化 mapper 需要的规则。"""
import json
import collections

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
IO_V4_4 = r"assets/data/knowledge/io_v4_4.json"

refined = json.load(open(REFINED, encoding="utf-8"))
io = json.load(open(IO_V4_4, encoding="utf-8"))

# ---------- meta diff ----------
rm, im = refined.get("meta", {}), io.get("meta", {})
print("== meta keys refined-only:", sorted(set(rm) - set(im)))
print("== meta keys io-only    :", sorted(set(im) - set(rm)))
common_diff = [k for k in set(rm) & set(im) if rm[k] != im[k]]
print("== meta value diff keys :", common_diff)
for k in common_diff[:5]:
    print(f"  {k}: refined={json.dumps(rm[k], ensure_ascii=False)[:150]}")
    print(f"  {k}: io    ={json.dumps(im[k], ensure_ascii=False)[:150]}")

# ---------- section level ----------
def sections(doc):
    out = {}
    for c in doc["categories"]:
        for s in c.get("sections", []):
            out[s["id"]] = s
    return out

rs, iss = sections(refined), sections(io)
print("\n== sections:", len(rs), len(iss), "id equal:", set(rs) == set(iss))
sec_field_added = collections.Counter()
sec_field_removed = collections.Counter()
sec_field_valdiff = collections.Counter()
for sid in rs:
    a, b = rs[sid], iss[sid]
    for k in set(a) - set(b) - {"items"}:
        sec_field_added[k] += 1
    for k in set(b) - set(a) - {"items"}:
        sec_field_removed[k] += 1
    for k in set(a) & set(b) - {"items"}:
        if a[k] != b[k]:
            sec_field_valdiff[k] += 1
print("section refined-only fields:", dict(sec_field_added))
print("section io-only fields:", dict(sec_field_removed))
print("section value diff:", dict(sec_field_valdiff))

# ---------- item level ----------
def items(doc):
    out = {}
    for c in doc["categories"]:
        for s in c.get("sections", []):
            for i in s.get("items", []):
                out[i["id"]] = i
    return out

ri, ii = items(refined), items(io)
print("\n== items:", len(ri), len(ii), "id equal:", set(ri) == set(ii))

io_only_fields = collections.Counter()     # refined 无 io 有
ref_only_fields = collections.Counter()    # refined 有 io 无
val_diff = collections.Counter()           # 共有但值不同
val_diff_examples = collections.defaultdict(list)

for iid in ri:
    a, b = ri[iid], ii[iid]
    for k in set(b) - set(a):
        io_only_fields[k] += 1
    for k in set(a) - set(b):
        ref_only_fields[k] += 1
    for k in set(a) & set(b):
        if a[k] != b[k]:
            val_diff[k] += 1
            if len(val_diff_examples[k]) < 2:
                val_diff_examples[k].append((iid, a[k], b[k]))

print("\n== item io-only fields（refined 缺，io 有 -> mapper 需补默认值）==")
for k, v in sorted(io_only_fields.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print("\n== item refined-only fields（refined 有，io 无 -> mapper 需丢弃）==")
for k, v in sorted(ref_only_fields.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print("\n== item value diffs（共有字段值不同 -> 需找转换规则）==")
for k, v in sorted(val_diff.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
    for iid, av, bv in val_diff_examples[k]:
        print(f"    e.g. {iid}: refined={json.dumps(av, ensure_ascii=False)[:120]}")
        print(f"          io    ={json.dumps(bv, ensure_ascii=False)[:120]}")
