"""
Исправление упражнений для King Lear
Дата: 14.09.2025
"""
import json
import re
from pathlib import Path

def create_exercise_text(narrative_text):
    """Преобразует текст с немецкими словами в упражнение"""
    # Паттерн для замены <b>СЛОВО (перевод)</b> на ___ (перевод)
    pattern = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
    exercise = re.sub(pattern, r'___ (\2)', narrative_text)
    return exercise

# Путь к файлу
json_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')

print("[LOADING] Reading king_lear.json...")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[INFO] Found {len(data['journey_phases'])} phases")

# Добавляем упражнения
count = 0
for phase in data['journey_phases']:
    if 'theatrical_scene' in phase:
        scene = phase['theatrical_scene']
        if 'narrative' in scene:
            # Создаем упражнение
            original_text = scene['narrative']
            exercise_text = create_exercise_text(original_text)
            scene['exercise_text'] = exercise_text
            
            # Подсчет замен
            replacements = original_text.count('<b>')
            count += 1
            
            print(f"[+] Phase: {phase['title']}")
            print(f"    Scene: {scene['title']}")
            print(f"    German words replaced: {replacements}")
            
            # Показываем первые 200 символов упражнения
            if count == 1:
                print(f"\n[EXAMPLE] First exercise preview:")
                print(exercise_text[:200] + "...")
                print()

print(f"\n[SUMMARY] Added exercises to {count} scenes")

# Сохраняем обновленный файл
print("[SAVING] Writing updated JSON...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("[SUCCESS] File saved!")

# Проверка
print("\n[VERIFICATION]")
with open(json_path, 'r', encoding='utf-8') as f:
    check_data = json.load(f)
    
for i, phase in enumerate(check_data['journey_phases'][:3]):  # Проверяем первые 3
    if 'theatrical_scene' in phase:
        has_exercise = 'exercise_text' in phase['theatrical_scene']
        print(f"  Phase {i+1}: exercise_text exists = {has_exercise}")

print("\n[DONE] Ready to regenerate HTML!")
