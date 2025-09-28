#!/usr/bin/env python
"""Фінальна перевірка ВСІХ 4 виправлень"""
from pathlib import Path
import json

# Спочатку генеруємо сайт
import subprocess
print("Генерація сайту...")
result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)
print(f"Результат генерації: {result.returncode}")
if result.returncode != 0:
    print("ПОМИЛКА генерації:")
    print(result.stderr)
    exit(1)

html_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
json_file = Path(r"F:\AiKlientBank\KingLearComic\data\characters\king_lear.json")

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("ФІНАЛЬНА ПЕРЕВІРКА 4 ПРОБЛЕМ")
print("=" * 60)

# 1. РОЗТАШУВАННЯ
print("\n1. РОЗТАШУВАННЯ КОМПОНЕНТІВ:")
theatrical_pos = html.find('theatrical-scene')
vocab_pos = html.find('vocabulary-grid')
exercises_pos = html.find('exercises-container')
articles_pos = html.find('articles-quiz')

print(f"  theatrical-scene позиція: {theatrical_pos}")
print(f"  vocabulary-grid позиція: {vocab_pos}")
print(f"  exercises-container позиція: {exercises_pos}")
print(f"  articles-quiz позиція: {articles_pos}")

if theatrical_pos > 0 and theatrical_pos < vocab_pos < exercises_pos:
    print("  [OK] Словник ПІСЛЯ сцени, ПЕРЕД exercises")
else:
    print("  [FAIL] Неправильне розташування словника")

if articles_pos > exercises_pos:
    print("  [OK] Вправа після exercises")
else:
    print("  [FAIL] Вправа НЕ після exercises")

# 2. СЛОВА З ФАЗИ
print("\n2. СЛОВА З ПОТОЧНОЇ ФАЗИ:")
throne_words = []
for phase in data['journey_phases']:
    if phase['id'] == 'throne':
        throne_words = [v['german'] for v in phase['vocabulary'][:5]]
        break

print(f"  Слова фази throne: {throne_words[:3]}")
found = sum(1 for word in throne_words if word in html)
print(f"  Знайдено {found}/5 слів з фази throne")
if found >= 3:
    print("  [OK] Використовуються слова з фази")
else:
    print("  [FAIL] Використовуються НЕ ті слова")

# 3. МОВА ІНТЕРФЕЙСУ  
print("\n3. МОВА ІНТЕРФЕЙСУ:")
ru_texts = ["Артикли и род", "Выберите правильный артикль", "мужской", "женский", "средний"]
found_ru = sum(1 for text in ru_texts if text in html)
print(f"  Знайдено {found_ru}/5 російських текстів")
if found_ru >= 3:
    print("  [OK] Російська мова")
else:
    print("  [FAIL] Неправильна мова")

# 4. КОЛЬОРОВА КОДИРОВКА
print("\n4. КОЛЬОРОВА КОДИРОВКА:")
colors = {
    "der синій": "linear-gradient(135deg, #e3f2fd" in html,
    "die червоний": "linear-gradient(135deg, #fce4ec" in html,
    "das зелений": "linear-gradient(135deg, #e8f5e9" in html,
    "is-der клас": "is-der" in html,
    "is-die клас": "is-die" in html,
    "is-das клас": "is-das" in html
}

for color, found in colors.items():
    print(f"  {'[OK]' if found else '[FAIL]'} {color}")

# ФІНАЛ
print("\n" + "=" * 60)
all_ok = (
    theatrical_pos > 0 and theatrical_pos < vocab_pos < exercises_pos and
    articles_pos > exercises_pos and
    found >= 3 and
    found_ru >= 3 and
    all(colors.values())
)

if all_ok:
    print("[SUCCESS] ВСІ 4 ПРОБЛЕМИ ВИПРАВЛЕНО!")
    print("\nДеталі:")
    print(f"  1. Словник на позиції {vocab_pos} (після сцени {theatrical_pos})")
    print(f"  2. Використано {found} слів з поточної фази")
    print(f"  3. Російська мова ({found_ru}/5 текстів)")
    print(f"  4. Кольорова кодировка працює (всі 6 стилів)")
else:
    print("[FAIL] Є невиправлені проблеми!")
    exit(1)
