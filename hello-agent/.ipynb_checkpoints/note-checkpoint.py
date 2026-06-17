import sys, os
from datetime import date

CHEATSHEET = os.path.join(os.path.dirname(__file__), 'cheatsheet.md')

if len(sys.argv) < 3:
    print('\u7528\u6cd5: python note.py <\u7c7b\u522b> <\u5185\u5bb9>')
    print('\u7c7b\u522b: code, concept, tool, fix')
    print('\u793a\u4f8b:')
    print('  python note.py code "re.search(...) \u63d0\u53d6\u51fd\u6570\u540d"')
    print('  python note.py concept "\u5b57\u5178 .get(key, default)"')
    sys.exit(1)

category = sys.argv[1]
content = ' '.join(sys.argv[2:])
today = date.today().isoformat()
line = f'- [{category}] {content}  ({today})\n'

with open(CHEATSHEET, 'a', encoding='utf-8') as f:
    f.write(line)

print(f'[OK] \u5df2\u8bb0\u5f55: [{category}] {content}')