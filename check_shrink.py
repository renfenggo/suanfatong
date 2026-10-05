import json
pp = json.load(open("data/stage3f_batch4_full49_direct_pre_shrink_patch_preview.json","r",encoding="utf-8"))
print("Total patches:", pp.get("total_patches"))
print("Actual patches len:", len(pp.get("patches",[])))
manual = [p for p in pp.get("patches",[]) if p.get("manual_review_required")]
print("Manual review count:", len(manual))
for m in manual:
    print(f"  {m['item_id']} ({m.get('name','')})")
ids = set(p["item_id"] for p in pp.get("patches",[]))
print("Unique item_ids:", len(ids))
has_issue = False
for p in pp.get("patches",[]):
    for dp in p.get("new",[]):
        if dp.count(".") != 2:
            print(f"  Section ref in {p['item_id']}: {dp}")
            has_issue = True
if not has_issue:
    print("All new_direct_pre are item IDs (3-part)")
