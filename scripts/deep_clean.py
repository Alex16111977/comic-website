import json
from pathlib import Path

def deep_clean_hints():
    """Глубокая очистка всех проблемных подсказок"""
    
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    
    # Словарь проблемных слов для ручной правки
    PROBLEM_FIXES = {
        "das Erbe": "наследство отца",
        "die Gier": "жадность к власти", 
        "der Spaß": "веселая забава",
        "scherzen": "шутить горько",
        "die Lüge": "сознательный обман",
        "heucheln": "притворяться искусно",
        "der Neid": "зависть к брату",
        "die Ambition": "жажда власти",
        "benachteiligt": "обделенный правами"
    }
    
    # Названия фаз для удаления
    PHASE_NAMES = [
        "Фальшивая любовь", "Предательство", "Изгнание", "Буря", 
        "Безумие", "Прозрение", "Разделение королевства", "У Гонерильи",
        "Слепота", "Интриги", "Верность", "Мудрость", "Жестокость",
        "Пробуждение", "Смерть", "Трагический финал", "Служба"
    ]
    
    print("[ГЛУБОКАЯ ОЧИСТКА ПОДСКАЗОК]")
    print("=" * 60)
    
    total_fixed = 0
    
    for char_file in characters_dir.glob("*.json"):
        if char_file.name == ".gitkeep":
            continue
            
        char = char_file.stem
        
        try:
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            char_fixed = 0
            
            for phase in data.get("journey_phases", []):
                for vocab in phase.get("vocabulary", []):
                    german = vocab.get("german", "")
                    hint = vocab.get("russian_hint", "")
                    
                    # Применяем ручные исправления
                    if german in PROBLEM_FIXES:
                        vocab["russian_hint"] = PROBLEM_FIXES[german]
                        char_fixed += 1
                        continue
                    
                    # Убираем названия фаз из подсказок
                    if hint:
                        original_hint = hint
                        for phase_name in PHASE_NAMES:
                            hint = hint.replace(phase_name, "").strip()
                        
                        # Убираем двойные пробелы
                        hint = " ".join(hint.split())
                        
                        # Если подсказка изменилась
                        if hint != original_hint:
                            vocab["russian_hint"] = hint if hint else "важное понятие"
                            char_fixed += 1
            
            # Сохраняем если были изменения
            if char_fixed > 0:
                with open(char_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  [OK] {char:12} - Исправлено {char_fixed} подсказок")
            else:
                print(f"  [--] {char:12} - Чисто")
            
            total_fixed += char_fixed
            
        except Exception as e:
            print(f"  [ERROR] {char}: {e}")
    
    print("-" * 60)
    print(f"ИТОГО исправлено: {total_fixed} подсказок")
    
    # Показываем результаты
    print("\n[ФИНАЛЬНАЯ ПРОВЕРКА]")
    print("-" * 60)
    
    for char in ["goneril", "edmund", "fool", "king_lear"]:
        file_path = characters_dir / f"{char}.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n{char.upper()}:")
        examples_shown = 0
        
        for phase in data.get("journey_phases", []):
            for vocab in phase.get("vocabulary", []):
                if examples_shown < 5:
                    german = vocab.get("german", "")
                    hint = vocab.get("russian_hint", "")
                    russian = vocab.get("russian", "")
                    print(f"  {german:20} -> {hint:25} ({russian})")
                    examples_shown += 1

if __name__ == "__main__":
    deep_clean_hints()
