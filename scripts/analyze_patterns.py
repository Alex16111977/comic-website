#!/usr/bin/env python
"""
Детальний аналіз патернів для вставки мнемотехніки
"""
import re
from pathlib import Path

html_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"

if not html_file.exists():
    print("[ERROR] Файл не існує!")
    exit(1)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("[АНАЛІЗ] Шукаємо точку між exercises та bottom-nav:")
print("=" * 60)

# Знаходимо позиції ключових елементів
exercises_pos = html.find('exercises-container')
bottom_nav_pos = html.find('bottom-nav')

if exercises_pos > 0 and bottom_nav_pos > exercises_pos:
    # Витягуємо текст між ними
    between = html[exercises_pos:bottom_nav_pos]
    
    # Шукаємо закриваючі теги
    print("[DEBUG] Текст між exercises і nav (останні 500 символів):")
    print(between[-500:])
    print("-" * 60)
    
    # Шукаємо патерни закриття
    patterns = [
        ('</div>\n        </div>\n\n        <nav', "Патерн 1: з відступами"),
        ('</div>\n    </div>\n\n    <nav', "Патерн 2: менші відступи"), 
        ('</div>\n</div>\n\n<nav', "Патерн 3: без відступів"),
        ('</div>\n            \n        </div>\n\n        <nav', "Патерн 4: з табуляціями"),
    ]
    
    for pattern, desc in patterns:
        if pattern in html:
            print(f"[OK] Знайдено: {desc}")
            print(f"     Патерн: {repr(pattern)}")
        else:
            print(f"[MISS] НЕ знайдено: {desc}")
    
    # Спробуємо знайти будь-який патерн з </div> перед <nav
    match = re.search(r'(</div>\s*</div>\s*)<nav class="bottom-nav"', html)
    if match:
        print("\n[OK] Знайдено регулярний вираз!")
        print(f"     Знайдений патерн: {repr(match.group(1))}")
        print(f"     Можна використати для replace()")

# Також перевіримо наявність style тегів
print("\n[STYLE] Перевірка CSS:")
if '<style>' in html:
    style_count = html.count('<style>')
    print(f"[OK] Знайдено <style> тегів: {style_count}")
    
    # Знайти всі style блоки
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    print(f"[INFO] Кількість style блоків: {len(style_blocks)}")
    
    # Знайти позицію останнього </style>
    last_style_close = html.rfind('</style>')
    if last_style_close > 0:
        print(f"[OK] Останній </style> на позиції: {last_style_close}")
else:
    print("[INFO] CSS інлайновий, немає <style> тегів")

print("\n[РЕКОМЕНДАЦІЯ] Оптимальна стратегія:")
print("1. CSS: Додати перед </head> або створити новий <style> блок")
print("2. HTML: Вставити між exercises-container та bottom-nav")
print("3. Використати regex для гнучкого пошуку патерну")
