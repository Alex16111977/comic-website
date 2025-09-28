#!/usr/bin/env python
"""
Тест модуля мнемотехніки
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.mnemonics_gen import MnemonicsGenerator
import config

# Тест 1: Створення генератора
mnemo = MnemonicsGenerator(config)
print("[TEST] Генератор створено")

# Тест 2: Перевірка extract_article
test_words = [
    "der Thron",
    "das Königreich",
    "die Krone"
]

for word in test_words:
    article = mnemo.extract_article(word)
    print(f"[TEST] '{word}' -> артикль: {article}")

# Тест 3: Генерація CSS
css = mnemo.generate_css()
print(f"[TEST] CSS згенеровано: {len(css)} символів")

# Тест 4: Генерація JavaScript
js = mnemo.generate_javascript()
print(f"[TEST] JavaScript згенеровано: {len(js)} символів")

print("[OK] Всі тести пройдено!")
