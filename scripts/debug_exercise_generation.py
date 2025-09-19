"""
Детальная отладка генерации упражнений
"""
import sys
import json
from pathlib import Path

# Добавляем путь к проекту
project_path = Path(r'F:\AiKlientBank\KingLearComic')
sys.path.insert(0, str(project_path))

# Загружаем JSON
json_path = project_path / 'data' / 'characters' / 'king_lear.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("[JSON DATA CHECK]")
# Проверяем первую фазу
first_phase = data['journey_phases'][0]
if 'theatrical_scene' in first_phase:
    scene = first_phase['theatrical_scene']
    print(f"Scene title: {scene.get('title', 'NO TITLE')}")
    print(f"Has narrative: {'narrative' in scene}")
    print(f"Has exercise_text: {'exercise_text' in scene}")
    
    if 'exercise_text' in scene:
        exercise = scene['exercise_text']
        print(f"Exercise text exists: {len(exercise)} chars")
        print(f"Exercise preview: {exercise[:100]}...")
    else:
        print("NO EXERCISE_TEXT IN JSON!")

print("\n[TESTING GENERATOR]")
# Импортируем генератор
from generators.html_lira import LiraHTMLGenerator

# Создаем экземпляр
generator = LiraHTMLGenerator()

# Вызываем метод _generate_theatrical_scenes напрямую с данными
scenes_html = generator._generate_theatrical_scenes(data)

print(f"Generated HTML length: {len(scenes_html)}")
print(f"Has exercise-section: {'exercise-section' in scenes_html}")
print(f"Exercise sections count: {scenes_html.count('exercise-section')}")

if 'exercise-section' in scenes_html:
    print("\n[SUCCESS] Exercises are in generated HTML!")
    # Найдем первое упражнение
    idx = scenes_html.find('exercise-section')
    print("\n[EXERCISE HTML FRAGMENT]:")
    print(scenes_html[idx-50:idx+300])
else:
    print("\n[PROBLEM] No exercises in generated HTML")
    # Проверим, что генерируется
    print(f"Has theatrical-scene: {'theatrical-scene' in scenes_html}")
    
    # Покажем фрагмент первой сцены
    if 'theatrical-scene' in scenes_html:
        idx = scenes_html.find('emotional-peak')
        if idx > 0:
            print("\n[FRAGMENT AFTER EMOTIONAL-PEAK]:")
            print(scenes_html[idx:idx+300])
