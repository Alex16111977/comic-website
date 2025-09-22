"""
Тест: Проверка подсказок в викторине
Дата: 09.01.2025
Мета: Проверяем что russian_hint правильно отображается в викторине
"""

import json
import re
from pathlib import Path

def check_quiz_hints():
    """Проверка наличия подсказок в коде викторины"""
    
    print("[INFO] Проверка подсказок в викторине...")
    print("=" * 60)
    
    # Путь к файлу journey_runtime.js
    runtime_path = Path(r"F:\AiKlientBank\KingLearComic\output\static\js\journey_runtime.js")
    
    if not runtime_path.exists():
        print("[ERROR] Файл journey_runtime.js не найден!")
        return False
    
    # Читаем содержимое файла
    content = runtime_path.read_text(encoding='utf-8')
    
    # Проверки наличия ключевых изменений
    checks = {
        "generateForwardQuestion с подсказкой": "if (word.russianHint)",
        "questionText с подсказкой": "(${word.russianHint})?",
        "russianHint в возвращаемом объекте": "russianHint: word.russianHint ||",
        "Отображение подсказки в renderQuestion": "if (question.russianHint)",
        "Стиль подсказки фиолетовый": "hintSpan.style.color = '#7c3aed'",
        "Размер шрифта подсказки": "hintSpan.style.fontSize = '0.9em'",
        "buildPhaseQuizWords с russianHint": "russianHint: word.russian_hint ||",
        "quiz-hint класс": "hintSpan.className = 'quiz-hint'"
    }
    
    print("[+] Проверка наличия изменений в коде:")
    all_passed = True
    
    for check_name, check_pattern in checks.items():
        if check_pattern in content:
            print(f"    [OK] {check_name}")
        else:
            print(f"    [ERROR] {check_name} - НЕ НАЙДЕНО!")
            all_passed = False
    
    # Проверяем наличие подсказок в данных персонажей
    print("\n[+] Проверка наличия russian_hint в данных персонажей:")
    
    characters_path = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    if not characters_path.exists():
        print("[ERROR] Папка data/characters не найдена!")
        return False
    
    hint_stats = {
        "total_words": 0,
        "words_with_hints": 0,
        "characters_with_hints": []
    }
    
    for json_file in characters_path.glob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding='utf-8'))
            char_name = data.get('name', json_file.stem)
            
            # Новая структура: journey_phases вместо journey.phases
            if 'journey_phases' in data:
                char_has_hints = False
                
                for phase in data['journey_phases']:
                    # Словарь находится в поле vocabulary
                    if 'vocabulary' in phase:
                        for word in phase['vocabulary']:
                            hint_stats["total_words"] += 1
                            
                            if 'russian_hint' in word and word['russian_hint']:
                                hint_stats["words_with_hints"] += 1
                                char_has_hints = True
                
                if char_has_hints:
                    hint_stats["characters_with_hints"].append(char_name)
        
        except Exception as e:
            print(f"    [WARNING] Ошибка чтения {json_file.name}: {e}")
    
    # Выводим статистику
    print(f"\n[+] Статистика подсказок:")
    print(f"    Всего слов: {hint_stats['total_words']}")
    print(f"    Слов с подсказками: {hint_stats['words_with_hints']}")
    
    if hint_stats['total_words'] > 0:
        percentage = (hint_stats['words_with_hints'] / hint_stats['total_words']) * 100
        print(f"    Процент покрытия: {percentage:.1f}%")
    
    if hint_stats['characters_with_hints']:
        print(f"\n    Персонажи с подсказками ({len(hint_stats['characters_with_hints'])}):")
        for char in hint_stats['characters_with_hints'][:5]:  # Показываем первые 5
            print(f"        - {char}")
        if len(hint_stats['characters_with_hints']) > 5:
            print(f"        ... и еще {len(hint_stats['characters_with_hints']) - 5} персонажей")
    
    # Финальная проверка
    print("\n" + "=" * 60)
    
    if all_passed and hint_stats['words_with_hints'] > 0:
        print("[OK] Все проверки пройдены успешно!")
        print("[OK] Подсказки добавлены в викторину и готовы к использованию!")
        
        # Пример отображения
        print("\n[+] Пример отображения в викторине:")
        print("    Вопрос: Что означает немецкое слово «herrschen» (управлять государством)?")
        print("    ")
        print("    herrschen (управлять государством)")
        print("    [ХЕР-шен]")
        print("    ")
        print("    О править    О виновный")
        print("    О голый      О правда")
        
        return True
    else:
        print("[ERROR] Некоторые проверки не пройдены!")
        return False

if __name__ == "__main__":
    check_quiz_hints()
