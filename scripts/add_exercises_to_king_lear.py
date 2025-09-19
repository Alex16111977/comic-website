"""
Добавление упражнений к театральным сценам King Lear
Дата: 14.09.2025
Мета: Добавить версии текста с пропусками для изучения немецких слов
"""
import json
import re
from pathlib import Path

def create_exercise_text(narrative_text):
    """
    Преобразует текст с немецкими словами в упражнение с пропусками
    Заменяет <b>НЕМЕЦКОЕ (перевод)</b> на ___ (перевод)
    """
    # Паттерн для поиска немецких слов: <b>НЕМЕЦКОЕ_СЛОВО (перевод)</b>
    pattern = r'<b>([A-ZÄÖÜ][A-ZÄÖÜ\-\s]*)\s*\(([^)]+)\)</b>'
    
    # Заменяем на ___ (перевод)
    exercise_text = re.sub(pattern, r'___ (\2)', narrative_text)
    
    return exercise_text

def process_king_lear():
    """Обновляет файл king_lear.json, добавляя упражнения"""
    
    # Путь к файлу
    file_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')
    
    # Читаем файл
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Обрабатываем каждую фазу
    for phase in data['journey_phases']:
        if 'theatrical_scene' in phase:
            scene = phase['theatrical_scene']
            
            # Создаем упражнение из narrative
            if 'narrative' in scene:
                original_text = scene['narrative']
                exercise_text = create_exercise_text(original_text)
                
                # Добавляем поле с упражнением
                scene['exercise_text'] = exercise_text
                
                print(f"[OK] Обработана сцена: {scene.get('title', 'Без названия')}")
                print(f"    Оригинал: {len(original_text)} символов")
                print(f"    Упражнение: {len(exercise_text)} символов")
                print(f"    Немецких слов заменено: {original_text.count('<b>') }")
                print()
    
    # Сохраняем обновленный файл
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Файл king_lear.json успешно обновлен!")
    print(f"[OK] Добавлено упражнений: {len(data['journey_phases'])}")
    
    # Проверка первого упражнения
    first_exercise = data['journey_phases'][0]['theatrical_scene']['exercise_text']
    print("\n[ПРОВЕРКА] Первое упражнение:")
    print("-" * 60)
    print(first_exercise[:300] + "...")
    
    return data

if __name__ == "__main__":
    print("=" * 60)
    print("ДОБАВЛЕНИЕ УПРАЖНЕНИЙ К KING LEAR")
    print("=" * 60)
    
    try:
        process_king_lear()
        print("\n[SUCCESS] Все упражнения добавлены!")
    except Exception as e:
        print(f"\n[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
