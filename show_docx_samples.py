import json

# Load the docx knowledge points
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points.json', 'r', encoding='utf-8') as f:
    docx_kps = json.load(f)

# Remove the first item if it's just an introduction
if '以下是完整的前1000个知识点的纯文本格式' in docx_kps[0]['name']:
    docx_kps = docx_kps[1:]

print(f"Valid knowledge points: {len(docx_kps)}")

# Show some samples from different ranges
print("\nFirst 30 knowledge points:")
for i, kp in enumerate(docx_kps[:30]):
    print(f"{i+1}. {kp['name']}")

print("\n" + "="*50)
print("\nKnowledge points 100-120:")
for i, kp in enumerate(docx_kps[99:119], 100):
    print(f"{i}. {kp['name']}")

print("\n" + "="*50)
print("\nKnowledge points 300-320:")
for i, kp in enumerate(docx_kps[299:319], 300):
    print(f"{i}. {kp['name']}")

print("\n" + "="*50)
print("\nKnowledge points 600-620:")
for i, kp in enumerate(docx_kps[599:619], 600):
    print(f"{i}. {kp['name']}")

print("\n" + "="*50)
print("\nKnowledge points 900-1000:")
for i, kp in enumerate(docx_kps[899:], 900):
    print(f"{i}. {kp['name']}")

# Save cleaned version
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points_clean.json', 'w', encoding='utf-8') as f:
    json.dump(docx_kps, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(docx_kps)} cleaned knowledge points to docx_knowledge_points_clean.json")