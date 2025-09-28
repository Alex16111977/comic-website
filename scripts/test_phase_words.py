#!/usr/bin/env python
"""Тест використання слів з фази"""
import json
from pathlib import Path

# Перевірка JSON
json_file = Path(r"F:\AiKlientBank\KingLearComic\data\characters\king_lear.json")
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Слова першої фази (throne)
throne_words = []
for phase in data['journey_phases']:
    if phase['id'] == 'throne':
        throne_words = [v['german'] for v in phase['vocabulary'][:5]]
        break

print(f"Слова фази throne: {throne_words}")

# Перевірка HTML
import subprocess
result = subprocess.run([sys.executable, 'main.py'], capture_output=True, text=True, cwd=r'F:\AiKlientBank\KingLearComic')

html_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Перевірка вправи
found = 0
for word in throne_words:
    if word in html:
        found += 1
        print(f"  [OK] '{word}' знайдено у вправі")

if found >= 3:
    print(f"[SUCCESS] Знайдено {found} слів з фази!")
else:
    print(f"[FAIL] Знайдено лише {found} слів!")
    exit(1)

# Перевірка мови
if "Артикли и род" in html and "Выберите правильный артикль" in html:
    print("[SUCCESS] Російська мова!")
else:
    print("[FAIL] Неправильна мова!")
    exit(1)
