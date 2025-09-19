"""
Добавление упражнений ко всем персонажам King Lear
Использует структуру king_lear.json как эталон
"""
import json
import re
from pathlib import Path

def create_exercise_text(narrative_text):
    """
    Преобразует текст с немецкими словами в упражнение
    <b>НЕМЕЦКОЕ (перевод)</b> → ___ (перевод)
    """
    if not narrative_text:
        return ""
    
    pattern = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
    return re.sub(pattern, r'___ (\2)', narrative_text)

def process_character_file(json_path):
    """Добавляет exercise_text к персонажу"""
    
    # Загружаем данные
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    character_name = data.get('name', 'Unknown')
    exercises_added = 0
    
    # Обрабатываем каждую фазу
    for phase in data.get('journey_phases', []):
        if 'theatrical_scene' in phase:
            scene = phase['theatrical_scene']
            
            # Добавляем упражнение если есть narrative
            if 'narrative' in scene and scene['narrative']:
                scene['exercise_text'] = create_exercise_text(scene['narrative'])
                exercises_added += 1
    
    # Сохраняем обновленный файл
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return character_name, exercises_added

def main():
    """Обновляет все файлы персонажей"""
    
    print("=" * 60)
    print("ДОБАВЛЕНИЕ УПРАЖНЕНИЙ КО ВСЕМ ПЕРСОНАЖАМ")
    print("=" * 60)
    
    # Путь к персонажам
    characters_dir = Path(r'F:\AiKlientBank\KingLearComic\data\characters')
    
    # Порядок персонажей из config.py
    character_order = [
        "king_lear", "cordelia", "goneril", "regan",
        "gloucester", "edgar", "edmund", "kent",
        "fool", "albany", "cornwall", "oswald"
    ]
    
    total_exercises = 0
    processed_count = 0
    
    # Обрабатываем каждого персонажа
    for char_id in character_order:
        json_file = characters_dir / f"{char_id}.json"
        
        if json_file.exists():
            try:
                name, exercises = process_character_file(json_file)
                total_exercises += exercises
                processed_count += 1
                
                status = "[OK]" if exercises > 0 else "[SKIP]"
                print(f"{status} {char_id}.json")
                print(f"     Персонаж: {name}")
                print(f"     Добавлено упражнений: {exercises}")
                
            except Exception as e:
                print(f"[ERROR] {char_id}.json: {e}")
        else:
            print(f"[MISSING] {char_id}.json")
    
    print("\n" + "=" * 60)
    print(f"[SUMMARY]")
    print(f"  Обработано файлов: {processed_count}/12")
    print(f"  Всего упражнений добавлено: {total_exercises}")
    print("=" * 60)
    
    # Проверка king_lear.json
    king_lear_path = characters_dir / "king_lear.json"
    if king_lear_path.exists():
        with open(king_lear_path, 'r', encoding='utf-8') as f:
            king_data = json.load(f)
        
        # Проверяем первое упражнение
        first_phase = king_data['journey_phases'][0]
        if 'theatrical_scene' in first_phase:
            exercise = first_phase['theatrical_scene'].get('exercise_text', '')
            if exercise:
                print("\n[ПРОВЕРКА] Пример упражнения (king_lear):")
                print(exercise[:200] + "...")
    
    return processed_count == 12

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n[SUCCESS] Все персонажи готовы!")
        print("[NEXT] Запустите main.py для генерации сайта")
    else:
        print("\n[WARNING] Некоторые файлы отсутствуют")
        print("[NEXT] Проверьте наличие всех JSON файлов")
