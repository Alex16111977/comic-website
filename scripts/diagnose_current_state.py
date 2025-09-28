#!/usr/bin/env python
"""
Діагностика поточного стану мнемотехніки
"""
import json
from pathlib import Path

# Аналіз HTML
html_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"
if not html_file.exists():
    print("[ERROR] king_lear.html не існує! Запустіть генерацію.")
    exit(1)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("[ДІАГНОСТИКА] Поточний стан:")
print("=" * 60)

# Перевірка позицій компонентів
checks = {
    "Словник внизу (НЕПРАВИЛЬНО)": html.find('Словник з кольоровою мнемотехнікою') > html.find('exercises-container'),
    "Вправа внизу (НЕПРАВИЛЬНО)": 'Вправа: Артиклі та рід' in html and html.find('Вправа: Артиклі та рід') > html.find('bottom-nav'),
    "Українська мова (НЕПРАВИЛЬНО)": 'Виберіть правильний артикль' in html,
    "Випадкові слова (НЕПРАВИЛЬНО)": 'Undankbarkeit' in html or 'Kränkung' in html
}

for check, status in checks.items():
    print(f"  {'[BAD]' if status else '[OK]'} {check}: {status}")

# Аналіз JSON для слів уроку
json_file = Path(__file__).parent.parent / "data" / "characters" / "king_lear.json"
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

throne_room_vocab = None
for stage in data['journey']['stages']:
    if stage['id'] == 'throne_room':
        throne_room_vocab = stage.get('vocabulary', [])
        break

print(f"\n[JSON] Слова для throne_room:")
if throne_room_vocab:
    for word in throne_room_vocab[:5]:  # Показати перші 5
        print(f"  - {word.get('word', 'N/A')} ({word.get('article', 'N/A')})")
else:
    print("  [ERROR] Vocabulary не знайдено в JSON!")
