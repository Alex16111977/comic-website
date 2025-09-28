#!/usr/bin/env python
"""
Перевірка поточних проблем мнемотехніки
"""
from pathlib import Path
import json

html_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"
json_file = Path(__file__).parent.parent / "data" / "characters" / "king_lear.json"

print("[АНАЛІЗ] Поточні проблеми:")
print("=" * 60)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Проблема 1: Розташування компонентів
vocab_pos = html.find('vocabulary-grid') if 'vocabulary-grid' in html else -1
exercises_pos = html.find('exercises-container') if 'exercises-container' in html else -1
scene_pos = html.find('theatrical-scene') if 'theatrical-scene' in html else -1

print("1. РОЗТАШУВАННЯ КОМПОНЕНТІВ:")
if vocab_pos > 0 and exercises_pos > 0:
    if vocab_pos < exercises_pos:
        print("  [OK] Словник ПЕРЕД exercises")
    else:
        print("  [BAD] Словник ПІСЛЯ exercises")
else:
    print("  [ERROR] Не знайдено компоненти")

if vocab_pos > 0 and scene_pos > 0:
    if vocab_pos > scene_pos:
        print("  [OK] Словник ПІСЛЯ опису сцени")
    else:
        print("  [BAD] Словник ПЕРЕД описом сцени")

# Проблема 2: Слова в вправі
print("\n2. СЛОВА В ВПРАВІ:")
wrong_words = ['Undankbarkeit', 'Kränkung', 'Fluch']
has_wrong = any(word in html for word in wrong_words)
if has_wrong:
    print("  [BAD] Використовуються випадкові слова")
else:
    print("  [OK] Випадкових слів немає")

# Перевірка правильних слів з JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

throne_words = []
for phase in data.get('journey_phases', []):
    if phase.get('id') == 'throne':
        vocab = phase.get('vocabulary', [])
        throne_words = [v.get('german', '') for v in vocab[:4]]
        break

print(f"  Слова з throne фази: {throne_words}")
for word in throne_words:
    if word in html:
        print(f"    [OK] '{word}' знайдено")
    else:
        print(f"    [BAD] '{word}' НЕ знайдено")

# Проблема 3: Мова інтерфейсу
print("\n3. МОВА ІНТЕРФЕЙСУ:")
ukrainian_texts = ["Вправа: Артиклі та рід", "Виберіть правильний артикль"]
russian_texts = ["Артикли и род", "Выберите правильный артикль"]

for text in ukrainian_texts:
    if text in html:
        print(f"  [BAD] Українська: '{text}'")

for text in russian_texts:
    if text in html:
        print(f"  [OK] Російська: '{text}'")

# Проблема 4: Кольорова кодировка
print("\n4. КОЛЬОРОВА КОДИРОВКА:")
color_checks = {
    "is-der клас": "is-der" in html,
    "is-die клас": "is-die" in html, 
    "is-das клас": "is-das" in html,
    "linear-gradient для der": "linear-gradient" in html and "#e3f2fd" in html,
    "linear-gradient для die": "linear-gradient" in html and "#fce4ec" in html,
    "linear-gradient для das": "linear-gradient" in html and "#e8f5e9" in html
}

for check, status in color_checks.items():
    print(f"  {'[OK]' if status else '[BAD]'} {check}")

print("\n" + "=" * 60)
print("ВИСНОВОК: Потрібно виправити знайдені проблеми")
