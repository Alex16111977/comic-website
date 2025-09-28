#!/usr/bin/env python
"""
Детальний аналіз структури згенерованого файлу з мнемотехнікою
"""
from pathlib import Path

test_file = Path(__file__).parent / "test_mnemo_integrated.html"

if not test_file.exists():
    print("[ERROR] Тестовий файл не існує!")
    exit(1)

with open(test_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("[АНАЛІЗ] Позиції ключових елементів:")
print("=" * 60)

elements = [
    'journey-timeline',
    'vocabulary-grid',
    'articles-quiz',  
    'exercises-container',
    'bottom-nav',
    '</body>'
]

positions = {}
for element in elements:
    pos = html.find(element)
    positions[element] = pos
    if pos > 0:
        print(f"[{pos:6}] {element}")

print("\n[ПРОБЛЕМА]:")
print(f"vocabulary-grid на позиції {positions['vocabulary-grid']}")
print(f"exercises-container на позиції {positions['exercises-container']}")
print("Мнемотехніка вставлена ПЕРЕД exercises, а не ПІСЛЯ!")

# Знаходимо де саме вставлена мнемотехніка
vocab_start = positions['vocabulary-grid']
if vocab_start > 0:
    context_start = max(0, vocab_start - 200)
    context = html[context_start:vocab_start + 100]
    print("\n[КОНТЕКСТ] Де вставлена мнемотехніка:")
    print("-" * 60)
    print(context)
    
# Шукаємо патерн який спрацював
patterns = [
    '</div>\n            \n        </div>\n\n        <nav class="bottom-nav">',
    '</div>\n    </div>\n\n    <nav class="bottom-nav">',
]

print("\n[ПАТЕРНИ]:")
for pattern in patterns:
    count = html.count(pattern)
    if count > 0:
        print(f"[FOUND] Патерн знайдено {count} раз(ів)")
        # Знайти всі позиції
        start = 0
        while True:
            pos = html.find(pattern, start)
            if pos == -1:
                break
            print(f"  - позиція: {pos}")
            start = pos + 1

print("\n[РЕКОМЕНДАЦІЯ]:")
print("Потрібно шукати патерн ПІСЛЯ exercises-container, а не першого співпадіння!")
