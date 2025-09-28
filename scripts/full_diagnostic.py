#!/usr/bin/env python
"""
Повна діагностика генерації з очищенням кешу
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Видаляємо старий тестовий файл якщо існує
test_output = Path(__file__).parent / "test_mnemo_integrated.html"
if test_output.exists():
    os.remove(test_output)
    print("[CLEAN] Старий тестовий файл видалено")

# Імпортуємо та генеруємо заново
from generators.html_lira import LiraHTMLGenerator
import config

print("[START] Нова генерація...")

# Генеруємо HTML
html_gen = LiraHTMLGenerator(config)
test_file = config.CHARACTERS_DIR / "king_lear.json"

if not test_file.exists():
    print("[ERROR] king_lear.json не знайдено!")
    sys.exit(1)

# Генеруємо HTML
html = html_gen.generate_journey(test_file)

# Детальний аналіз позицій
print("\n[АНАЛІЗ] Позиції елементів в згенерованому HTML:")
print("=" * 60)

elements = {
    'journey-timeline': html.find('journey-timeline'),
    'exercises-container': html.find('exercises-container'),
    'vocabulary-grid (HTML)': html.find('<div class="vocabulary-grid">'),
    'vocabulary-grid (CSS)': html.find('.vocabulary-grid'),
    'articles-quiz': html.find('articles-quiz'),
    'bottom-nav': html.find('bottom-nav'),
}

for name, pos in elements.items():
    if pos > 0:
        print(f"[{pos:6}] {name}")
    else:
        print(f"[  MISS] {name}")

# Перевірка правильного порядку
exercises_pos = elements['exercises-container']
vocab_html_pos = elements['vocabulary-grid (HTML)']
quiz_pos = elements['articles-quiz']
nav_pos = elements['bottom-nav']

print("\n[ПЕРЕВІРКА] Порядок секцій:")
if exercises_pos > 0 and vocab_html_pos > 0:
    if vocab_html_pos > exercises_pos and nav_pos > vocab_html_pos:
        print("✅ ПРАВИЛЬНО: exercises → vocabulary → nav")
        correct_order = True
    else:
        print("❌ НЕПРАВИЛЬНО: vocabulary перед exercises")
        correct_order = False
        
        # Додаткова діагностика
        print("\n[DEBUG] Деталі:")
        if vocab_html_pos < exercises_pos:
            # Знайдемо контекст де вставлено vocabulary
            context_start = max(0, vocab_html_pos - 100)
            context_end = min(len(html), vocab_html_pos + 200)
            print("Контекст навколо vocabulary-grid:")
            print(html[context_start:context_end])

# Зберігаємо файл
with open(test_output, 'w', encoding='utf-8') as f:
    f.write(html)
    
print(f"\n[SAVED] Файл збережено: {test_output}")

# Фінальний статус
if correct_order:
    print("\n✅ УСПІХ: Інтеграція працює правильно!")
    sys.exit(0) 
else:
    print("\n❌ ПРОБЛЕМА: Потрібно додаткове налагодження")
    sys.exit(1)
