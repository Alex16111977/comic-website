"""
Финальное добавление упражнений в king_lear.json
"""
import json
import re
from pathlib import Path

def create_exercise_text(narrative_text):
    """Преобразует текст с немецкими словами в упражнение с пропусками"""
    # Паттерн для поиска: <b>СЛОВО (перевод)</b>
    pattern = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
    # Заменяем на ___ (перевод)
    return re.sub(pattern, r'___ (\2)', narrative_text)

# Путь к файлу
json_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')

print("[ADDING EXERCISES TO KING_LEAR.JSON]")
print("=" * 60)

# Читаем файл
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Добавляем упражнения к каждой театральной сцене
added_count = 0
for i, phase in enumerate(data['journey_phases']):
    if 'theatrical_scene' in phase:
        scene = phase['theatrical_scene']
        if 'narrative' in scene:
            # Создаем упражнение
            original_narrative = scene['narrative']
            exercise_text = create_exercise_text(original_narrative)
            scene['exercise_text'] = exercise_text
            
            # Подсчитываем изменения
            original_words = original_narrative.count('<b>')
            blanks = exercise_text.count('___')
            
            print(f"\n[Phase {i+1}] {phase['title']}")
            print(f"  Scene: {scene['title'][:40]}...")
            print(f"  German words: {original_words}")
            print(f"  Blanks created: {blanks}")
            
            added_count += 1

# Сохраняем обновленный файл
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print(f"[SUCCESS] Added exercises to {added_count} scenes")
print(f"[SAVED] {json_path}")

# Проверяем результат
print("\n[VERIFICATION]")
with open(json_path, 'r', encoding='utf-8') as f:
    verify_data = json.load(f)

first_scene = verify_data['journey_phases'][0]['theatrical_scene']
has_exercise = 'exercise_text' in first_scene

print(f"First scene has exercise_text: {has_exercise}")
if has_exercise:
    print(f"Exercise length: {len(first_scene['exercise_text'])} chars")
    print(f"\n[EXERCISE PREVIEW]:")
    print(first_scene['exercise_text'][:200] + "...")
