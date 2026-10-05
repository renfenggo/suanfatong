from docx import Document
import json

def read_docx_knowledge_points(file_path):
    try:
        doc = Document(file_path)
        
        knowledge_points = []
        current_number = 0
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue
                
            # Try to find patterns like "1. ", "2. ", etc.
            # Or patterns like "1、", "2、" etc.
            import re
            
            # Pattern for numbered items
            match = re.match(r'^(\d+)[.、\s](.+)$', text)
            if match:
                number = int(match.group(1))
                name = match.group(2).strip()
                current_number = number
                knowledge_points.append({
                    'id': number,
                    'name': name
                })
            else:
                # Check if this is a continuation of previous item
                if knowledge_points and current_number > 0:
                    knowledge_points[-1]['name'] += ' ' + text
                elif current_number == 0 and text:
                    # Maybe this is a title or unnumbered item
                    if len(text) < 50:  # Likely a title
                        knowledge_points.append({
                            'id': len(knowledge_points) + 1,
                            'name': text
                        })
        
        return knowledge_points
        
    except Exception as e:
        print(f"Error reading docx: {e}")
        return []

# Read the docx file
docx_path = r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\算法知识图谱aa.docx'
knowledge_points = read_docx_knowledge_points(docx_path)

print(f"Total knowledge points found: {len(knowledge_points)}")
print("\nFirst 20 knowledge points:")
for i, kp in enumerate(knowledge_points[:20]):
    print(f"{kp['id']}. {kp['name']}")

# Save to JSON for easier processing
with open(r'C:\Users\renfenggo\Documents\trae_projects\suanfatong\docx_knowledge_points.json', 'w', encoding='utf-8') as f:
    json.dump(knowledge_points, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(knowledge_points)} knowledge points to docx_knowledge_points.json")