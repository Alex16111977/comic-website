"""
Скрипт для поиска секций упражнений в js_lira.py
"""

import re
from pathlib import Path

project_root = Path(__file__).parent.parent
js_file = project_root / 'generators' / 'js_lira.py'

print(f"[Analyzing] {js_file}")

with open(js_file, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"[OK] File size: {len(content)} characters, {len(lines)} lines")

# Ищем упоминания families и collocations
print("\n[Searching for Word Families and Collocations...]")

families_found = False
collocations_found = False

for i, line in enumerate(lines):
    if 'word-families-section' in line.lower():
        print(f"Line {i+1}: Found word-families-section")
        print(f"  Content: {line[:150]}")
        families_found = True
        
    if 'collocations-section' in line.lower():
        print(f"Line {i+1}: Found collocations-section")
        print(f"  Content: {line[:150]}")
        collocations_found = True

if not families_found:
    print("[!] word-families-section NOT found in file")
    # Попробуем найти альтернативные варианты
    for i, line in enumerate(lines):
        if 'families' in line.lower() and ('section' in line.lower() or 'querySelector' in line.lower()):
            print(f"  Alternative at line {i+1}: {line[:100]}")

if not collocations_found:
    print("[!] collocations-section NOT found in file")
    # Попробуем найти альтернативные варианты
    for i, line in enumerate(lines):
        if 'collocation' in line.lower() and ('section' in line.lower() or 'querySelector' in line.lower()):
            print(f"  Alternative at line {i+1}: {line[:100]}")

# Найдем где начинается JavaScript код
print("\n[Looking for JavaScript generation code...]")
for i, line in enumerate(lines):
    if 'vocab_js = """' in line or "vocab_js = '''" in line or 'vocab_js = f"""' in line:
        print(f"[OK] Found vocab_js start at line {i+1}")
        
        # Показываем следующие 20 строк для контекста
        print("\nFirst 20 lines of JavaScript:")
        for j in range(i+1, min(i+21, len(lines))):
            print(f"  {j+1}: {lines[j][:80]}...")
        break

# Проверка ключевых функций
print("\n[Checking for key functions...]")
key_functions = [
    'displayVocabulary',
    'attachRelationHandlers',
    'initializeRelationSection',
    'toggleAnswers',
    'attachQuizHandlers',
    'Word Families section',
    'Collocations section'
]

for func in key_functions:
    if func in content:
        print(f"[OK] Found: {func}")
        # Найдем позицию
        index = content.find(func)
        line_num = content[:index].count('\n') + 1
        print(f"     At line: {line_num}")
    else:
        print(f"[!] NOT found: {func}")
