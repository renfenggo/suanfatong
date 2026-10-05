# -*- coding: utf-8 -*-
"""M1-2 补充：处理 3 处格式特例（三元路径 / CRLF pushReplacement / 无尾逗号单行）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'suanfatong'

# 1) home_page.dart: 三元路径
p = ROOT / 'lib/pages/home_page.dart'
src = p.read_text(encoding='utf-8')
old = """() => Navigator.pushNamed(
            context,
            isLearnableUnit ? '/cpp_learning_unit' : '/knowledge/item',
            arguments: lastItemId,
          ),"""
new = """() => context.push(
            isLearnableUnit ? '/cpp_learning_unit' : '/knowledge/item',
            extra: lastItemId,
          ),"""
assert old in src, 'home_page pattern missing'
src = src.replace(old, new)
p.write_text(src, encoding='utf-8', newline='')
print('home_page.dart ok')

# 2) cpp_learning_unit_page.dart: pushReplacement（容忍任意空白/行尾）
p = ROOT / 'lib/pages/cpp_learning_unit_page.dart'
src = p.read_text(encoding='utf-8')
pat = re.compile(
    r"Navigator\.pushReplacement\(\s*context,\s*MaterialPageRoute\(\s*"
    r"builder:\s*\(_\)\s*=>\s*CppLearningUnitPage\(itemId:\s*nextItem\.id\),\s*"
    r"settings:\s*RouteSettings\(\s*name:\s*'/cpp_learning_unit',\s*"
    r"arguments:\s*nextItem\.id,\s*\),\s*\),\s*\)",
    re.S,
)
src2, n = pat.subn("context.pushReplacement('/cpp_learning_unit', extra: nextItem.id)", src)
assert n == 1, f'pushReplacement matches: {n}'
p.write_text(src2, encoding='utf-8', newline='')
print('cpp_learning_unit_page.dart ok')

# 3) knowledge_section_page.dart: 无尾逗号单行
p = ROOT / 'lib/pages/knowledge_section_page.dart'
src = p.read_text(encoding='utf-8')
old = "Navigator.pushNamed(context, '/knowledge/item', arguments: item.id);"
new = "context.push('/knowledge/item', extra: item.id);"
assert old in src, 'knowledge_section pattern missing'
src = src.replace(old, new)
p.write_text(src, encoding='utf-8', newline='')
print('knowledge_section_page.dart ok')

# 终验
for rel in [
    'lib/pages/home_page.dart',
    'lib/pages/cpp_basic_path_page.dart',
    'lib/pages/cpp_learning_unit_page.dart',
    'lib/pages/cpp_search_page.dart',
    'lib/pages/knowledge_item_page.dart',
    'lib/pages/knowledge_map_page.dart',
    'lib/pages/knowledge_section_page.dart',
]:
    src = (ROOT / rel).read_text(encoding='utf-8')
    bad = [l for l in src.splitlines() if 'Navigator.pushNamed' in l or 'Navigator.pushReplacement' in l]
    assert not bad, f'{rel}: {bad}'
print('ALL CLEAN')
