"""
Найти где генерируется HTML для упражнений
"""

with open(r'F:\AiKlientBank\KingLearComic\generators\html_lira.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print("[Looking for section classes in html_lira.py...]")
print(f"File size: {len(lines)} lines")

# Ищем строки с классами секций
patterns = [
    'word-families-section',
    'collocations-section', 
    'relation-section',
    'Семья слов',
    'Коллокации',
    '👪 Семья слов',
    '🧩 Коллокации'
]

for pattern in patterns:
    if pattern in content:
        print(f"\n[Found: {pattern}]")
        # Найдем все вхождения
        index = 0
        while True:
            index = content.find(pattern, index)
            if index == -1:
                break
            line_num = content[:index].count('\n') + 1
            print(f"  Line {line_num}")
            # Показать контекст
            start_line = max(0, line_num - 2)
            end_line = min(len(lines), line_num + 2)
            for i in range(start_line, end_line):
                marker = ">>>" if i == line_num - 1 else "   "
                print(f"  {marker} {lines[i][:120]}")
            print()
            index += 1
