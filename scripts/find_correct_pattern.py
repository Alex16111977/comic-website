#!/usr/bin/env python
"""
Знаходження правильного патерну після exercises-container
"""
from pathlib import Path

# Читаємо оригінальний файл без мнемотехніки
orig_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"

if not orig_file.exists():
    print("[ERROR] Оригінальний файл не існує!")
    exit(1)

with open(orig_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Знаходимо позиції
exercises_pos = html.find('exercises-container')
bottom_nav_pos = html.find('bottom-nav')

if exercises_pos > 0 and bottom_nav_pos > exercises_pos:
    print("[OK] Знайдено обидві секції")
    print(f"  exercises-container: {exercises_pos}")
    print(f"  bottom-nav: {bottom_nav_pos}")
    
    # Витягуємо текст між ними
    between = html[exercises_pos:bottom_nav_pos]
    
    # Знаходимо останні 500 символів перед bottom-nav
    last_part = between[-500:] if len(between) > 500 else between
    
    print("\n[ТЕКСТ] Останні 500 символів перед bottom-nav:")
    print("=" * 60)
    print(repr(last_part))
    
    # Шукаємо закриваючі div
    import re
    
    # Знайти всі закриваючі div перед nav
    closing_divs = re.findall(r'((?:</div>\s*)+)<nav', last_part, re.DOTALL)
    if closing_divs:
        print("\n[ЗНАЙДЕНО] Закриваючі div перед nav:")
        for div in closing_divs:
            print(f"  Патерн: {repr(div)}")
    
    # Пробуємо знайти точний патерн
    nav_pattern = re.search(r'(</div>\s*</div>\s*)<nav class="bottom-nav">', last_part, re.DOTALL)
    if nav_pattern:
        print("\n[REGEX] Знайдено патерн:")
        print(f"  {repr(nav_pattern.group(1))}")
        
        # Перевіряємо скільки разів цей патерн зустрічається
        full_pattern = nav_pattern.group(0)
        count = html.count(full_pattern)
        print(f"\n[COUNT] Патерн зустрічається {count} раз(ів)")

print("\n[РІШЕННЯ]:")
print("Використовувати rfind() для пошуку ОСТАННЬОГО входження патерну")
print("або шукати конкретно після позиції exercises-container")
