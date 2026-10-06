# -*- coding: utf-8 -*-
"""M1-5：生成 graph_overrides.json（Publish 独有、无法从 Draft 推导的显式补丁）。

来源：现 io_v4_4（Publish 产物）中的补全值，refined（Draft 源）无对应信息：
- 475 个 stage5_hard_batch1 知识点的 level（L1-L4，生成时独立评估）
- item 2.13.30 的 pickup_group/block_id/pickup_order 空值补全
- meta 的 sync_* 字段与统计修正（时间戳等不可推导）
"""
import json

REFINED = r"merged_knowledge_graph_item_dependencies_refined.json"
IO_V4_4 = r"assets/data/knowledge/io_v4_4.json"
OUT = r"tools/publish/graph_overrides.json"

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

level_overrides = {}
for iid in ri:
    if "level" not in ri[iid] and "level" in ii[iid]:
        level_overrides[iid] = ii[iid]["level"]

pickup_overrides = {}
for iid in ri:
    patch = {}
    for f in ("pickup_group", "block_id", "pickup_order"):
        if f not in ri[iid] and f in ii[iid]:
            patch[f] = ii[iid][f]
    if patch:
        pickup_overrides[iid] = patch

im = io["meta"]
meta_patch = {
    "add": {
        k: im[k]
        for k in ("sync_batch", "synced_at", "synced_by", "synced_from")
        if k in im
    },
    "set": {
        k: im[k]
        for k in ("final_fusion_statistics", "expected_sections",
                  "expected_items", "revision_note")
        if k in im
    },
}

out = {
    "version": 1,
    "description": (
        "Publish 独有信息显式补丁：refined(Draft) 中不存在、"
        "io_v4_4(Publish) 生成时引入且无法从 Draft 推导的值。"
        "由 gen_graph_overrides.py 从现 Publish 产物提取固化。"
    ),
    "meta_patch": meta_patch,
    "level_overrides": level_overrides,
    "pickup_overrides": pickup_overrides,
}
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"overrides written: level x{len(level_overrides)}, "
      f"pickup x{len(pickup_overrides)}, meta add "
      f"x{len(meta_patch['add'])}, set x{len(meta_patch['set'])}")
