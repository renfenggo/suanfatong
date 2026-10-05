# -*- coding: utf-8 -*-
"""M1-2: 将 7 个页面的 Navigator 1.0 pushNamed 调用迁移到 go_router context.push。

一次性脚本（tools/archive 风格，执行后即弃）。幂等：重复执行无副作用。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'suanfatong'

FILES = [
    'lib/pages/home_page.dart',
    'lib/pages/cpp_basic_path_page.dart',
    'lib/pages/cpp_learning_unit_page.dart',
    'lib/pages/cpp_search_page.dart',
    'lib/pages/knowledge_item_page.dart',
    'lib/pages/knowledge_map_page.dart',
    'lib/pages/knowledge_section_page.dart',
]

RIVERPOD = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
GO_ROUTER = "import 'package:go_router/go_router.dart';"

# Navigator.pushNamed(context, 'X', arguments: Y,) -> context.push('X', extra: Y)
push_args = re.compile(
    r"Navigator\.pushNamed\(\s*context,\s*'([^']*)',\s*arguments:\s*([A-Za-z0-9_.']+),\s*\)",
    re.S,
)
# Navigator.pushNamed(context, 'X') -> context.push('X')
push_plain = re.compile(r"Navigator\.pushNamed\(\s*context,\s*'([^']*)'\s*\)")
# Navigator.pushNamed(context, expr) -> context.push(expr)（变量目标，如 action.route）
push_var = re.compile(r"Navigator\.pushNamed\(\s*context,\s*([A-Za-z_][\w.]*)\s*\)")

# cpp_learning_unit_page.dart 特例：pushReplacement 直构 MaterialPageRoute
push_repl_old = """Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (_) => CppLearningUnitPage(itemId: nextItem.id),
              settings: RouteSettings(
                name: '/cpp_learning_unit',
                arguments: nextItem.id,
              ),
            ),
          );"""
push_repl_new = "context.pushReplacement('/cpp_learning_unit', extra: nextItem.id);"

total_args = total_plain = total_var = 0
for rel in FILES:
    p = ROOT / rel
    raw = p.read_bytes()
    crlf = b'\r\n' in raw
    src = raw.decode('utf-8')

    if push_repl_old in src:
        src = src.replace(push_repl_old, push_repl_new)
        total_var += 1
        print(f'{rel}: pushReplacement 特例 -> done')

    n1 = len(push_args.findall(src))
    src = push_args.sub(lambda m: "context.push('%s', extra: %s)" % (m.group(1), m.group(2)), src)
    n2 = len(push_plain.findall(src))
    src = push_plain.sub(lambda m: "context.push('%s')" % m.group(1), src)
    n3 = len(push_var.findall(src))
    src = push_var.sub(lambda m: 'context.push(%s)' % m.group(1), src)

    added_import = False
    if GO_ROUTER in src:
        added_import = True
    elif RIVERPOD in src:
        src = src.replace(RIVERPOD, RIVERPOD + '\r\n' + GO_ROUTER if crlf else RIVERPOD + '\n' + GO_ROUTER, 1)
        added_import = True

    data = src.encode('utf-8')
    p.write_bytes(data)
    total_args += n1
    total_plain += n2
    total_var += n3
    print(f'{rel}: args={n1} plain={n2} var={n3} import={"ok" if added_import else "MISSING"} crlf={crlf}')

print(f'TOTAL: args={total_args} plain={total_plain} var={total_var}')

# 校验：不应再有 pushNamed / pushReplacement(Material 残留
leftover = []
for rel in FILES:
    src = (ROOT / rel).read_text(encoding='utf-8')
    for i, line in enumerate(src.splitlines(), 1):
        if 'Navigator.pushNamed' in line or 'Navigator.pushReplacement' in line:
            leftover.append(f'{rel}:{i}: {line.strip()}')
print('LEFTOVER:', len(leftover))
for l in leftover:
    print(' ', l)
