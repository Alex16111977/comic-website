"""
Отладка упражнений в King Lear
Дата: 14.09.2025
"""
import sys
import json
import re
from pathlib import Path

# Добавляем путь к проекту
project_path = Path(r'F:\AiKlientBank\KingLearComic')
sys.path.insert(0, str(project_path))

print("=" * 60)
print("DEBUG: EXERCISE GENERATION")
print("=" * 60)

# 1. Проверяем JSON
print("\n[1] CHECKING JSON FILE")
json_path = project_path / 'data' / 'characters' / 'king_lear.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, phase in enumerate(data['journey_phases'][:2]):  # Первые 2 фазы
    print(f"\nPhase {i}: {phase['id']}")
    if 'theatrical_scene' in phase:
        scene = phase['theatrical_scene']
        has_exercise = 'exercise_text' in scene
        print(f"  Has exercise_text: {has_exercise}")
        if has_exercise:
            exercise_preview = scene['exercise_text'][:100]
            print(f"  Exercise preview: {exercise_preview}...")
            print(f"  Blanks count: {scene['exercise_text'].count('___')}")

# 2. Импортируем генератор
print("\n[2] LOADING GENERATOR")
from generators.html_lira import LiraHTMLGenerator

generator = LiraHTMLGenerator()

# 3. Генерируем HTML методом _generate_theatrical_scenes
print("\n[3] GENERATING THEATRICAL SCENES")

# Используем метод напрямую
scenes_html = generator._generate_theatrical_scenes(data)

# Проверяем результат
has_exercise_section = 'exercise-section' in scenes_html
exercise_count = scenes_html.count('exercise-section')
blank_count = scenes_html.count('class="blank"')

print(f"  Has exercise-section: {has_exercise_section}")
print(f"  Exercise sections: {exercise_count}")
print(f"  Blank spans: {blank_count}")

if exercise_count > 0:
    # Находим первое упражнение
    start = scenes_html.find('exercise-section')
    end = scenes_html.find('</div>', start + 200)
    snippet = scenes_html[start:end]
    print(f"\n[EXERCISE HTML SNIPPET]:")
    print(snippet[:300])

# 4. Генерируем полную страницу
print("\n[4] GENERATING FULL PAGE")
full_html = generator.generate_journey(json_path)

full_has_exercise = 'exercise-section' in full_html
full_exercise_count = full_html.count('exercise-section')

print(f"  Full HTML has exercises: {full_has_exercise}")
print(f"  Exercise count in full HTML: {full_exercise_count}")

# 5. Сохраняем для анализа
output_file = project_path / 'output' / 'journeys' / 'king_lear_debug.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"\n[5] SAVED DEBUG HTML")
print(f"  File: {output_file}")
print(f"  Size: {len(full_html):,} bytes")

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
