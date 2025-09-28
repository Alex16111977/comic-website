#!/usr/bin/env python
"""
Тест отримання слів конкретної фази
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.mnemonics_gen import MnemonicsGenerator
import config

# Ініціалізація
gen = MnemonicsGenerator(config)

# Завантаження даних персонажа
json_file = Path(__file__).parent.parent / "data" / "characters" / "king_lear.json"

with open(json_file, 'r', encoding='utf-8') as f:
    character_data = json.load(f)

# Тест методу get_phase_vocabulary
print("[TEST] Перевірка get_phase_vocabulary...")
print("-" * 60)

# Фази для тестування
test_phases = ['throne', 'storm', 'heath']

for phase_id in test_phases:
    vocab = gen.get_phase_vocabulary(character_data, phase_id)
    print(f"[INFO] Фаза '{phase_id}':")
    print(f"  Знайдено слів: {len(vocab)}")
    
    if vocab:
        # Показуємо перші 3 слова
        for i, word in enumerate(vocab[:3], 1):
            print(f"  {i}. {word['german']} - {word['russian']} {word['transcription']}")
    else:
        print("  [ERROR] Слова не знайдені!")
    print()

# Тест генерації вправи з конкретної фази
print("[TEST] Генерація вправи для фази 'throne'...")
quiz_html = gen.generate_articles_quiz(character_data, phase_id='throne')

# Перевірка результату
checks = {
    "Російська мова": "Выберите правильный артикль" in quiz_html,
    "Артикли и род": "Артикли и род" in quiz_html,
    "quiz-item": "quiz-item" in quiz_html,
    "article-btn": "article-btn" in quiz_html
}

print("Перевірки:")
success = 0
for check, status in checks.items():
    print(f"  {'[OK]' if status else '[FAIL]'} {check}")
    if status:
        success += 1

print("-" * 60)
if success == len(checks):
    print(f"[SUCCESS] Всі {len(checks)} перевірок пройдені!")
else:
    print(f"[ERROR] Пройдено {success}/{len(checks)} перевірок")
    sys.exit(1)
