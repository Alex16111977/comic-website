import json
from pathlib import Path

def final_cleanup():
    """Финальная очистка подсказок - убираем остатки названий фаз"""
    
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    characters = [
        "king_lear", "cordelia", "goneril", "regan",
        "gloucester", "edgar", "edmund", "kent",
        "fool", "albany", "cornwall", "oswald"
    ]
    
    print("[ФИНАЛЬНАЯ ОЧИСТКА ПОДСКАЗОК]")
    print("=" * 60)
    
    total_cleaned = 0
    
    for char in characters:
        file_path = characters_dir / f"{char}.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            char_cleaned = 0
            
            for phase in data.get("journey_phases", []):
                phase_name = phase.get("name", "")
                
                for vocab in phase.get("vocabulary", []):
                    german = vocab.get("german", "")
                    hint = vocab.get("russian_hint", "")
                    
                    # Проверяем на остатки названий фаз
                    if hint and phase_name and phase_name in hint:
                        # Убираем название фазы из подсказки
                        new_hint = hint.replace(phase_name, "").strip()
                        # Убираем лишние пробелы
                        new_hint = " ".join(new_hint.split())
                        vocab["russian_hint"] = new_hint
                        char_cleaned += 1
                    
                    # Проверяем на скобки
                    elif hint and "(" in hint:
                        # Берем только часть до скобки
                        new_hint = hint.split("(")[0].strip()
                        vocab["russian_hint"] = new_hint
                        char_cleaned += 1
                    
                    # Если подсказка слишком длинная (более 4 слов)
                    elif hint and len(hint.split()) > 4:
                        # Оставляем первые 3-4 слова
                        words = hint.split()[:4]
                        new_hint = " ".join(words)
                        if not new_hint.endswith((".", "!", "?")):
                            vocab["russian_hint"] = new_hint
                            char_cleaned += 1
                    
                    # Если подсказки нет вообще - создаем базовую
                    elif not hint:
                        if german.startswith(('der ', 'die ', 'das ')):
                            vocab["russian_hint"] = "важное понятие"
                        elif german.endswith('en'):
                            vocab["russian_hint"] = "действие героя"
                        else:
                            vocab["russian_hint"] = "качество или состояние"
                        char_cleaned += 1
            
            # Сохраняем если были изменения
            if char_cleaned > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  [OK] {char:12} - Очищено {char_cleaned} подсказок")
            else:
                print(f"  [--] {char:12} - Все подсказки чистые")
            
            total_cleaned += char_cleaned
            
        except Exception as e:
            print(f"  [ERROR] {char}: {e}")
    
    print("-" * 60)
    print(f"ИТОГО очищено: {total_cleaned} подсказок")
    return total_cleaned

def show_final_results():
    """Показываем финальные результаты"""
    
    print("\n[ФИНАЛЬНЫЕ ПРИМЕРЫ ПОДСКАЗОК]")
    print("=" * 60)
    
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    
    # Показываем примеры из разных персонажей
    for char in ["goneril", "edmund", "fool"]:
        file_path = characters_dir / f"{char}.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n{char.upper()}:")
        count = 0
        for phase in data.get("journey_phases", []):
            for vocab in phase.get("vocabulary", []):
                if count < 5:
                    german = vocab.get("german", "")
                    hint = vocab.get("russian_hint", "")
                    russian = vocab.get("russian", "")
                    
                    # Проверяем качество
                    quality = "[OK]" if hint and len(hint.split()) <= 4 else "[!]"
                    print(f"  {quality} {german:20} -> {hint:25} ({russian})")
                    count += 1

if __name__ == "__main__":
    cleaned = final_cleanup()
    print(f"\n[РЕЗУЛЬТАТ] Очищено {cleaned} подсказок")
    
    show_final_results()
