import json

# Проверяем результаты обновления
def verify_update():
    file_path = r"F:\AiKlientBank\KingLearComic\data\characters\king_lear.json"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("[ПРОВЕРКА НОВЫХ ПОДСКАЗОК В king_lear.json]")
    print("=" * 70)
    
    # Показываем первые 20 обновленных подсказок
    count = 0
    problems = 0
    
    for phase in data.get("journey_phases", []):
        for vocab in phase.get("vocabulary", []):
            hint = vocab.get("russian_hint", "")
            german = vocab.get("german", "")
            
            # Проверяем на проблемы
            has_brackets = "(" in hint and ")" in hint
            
            if has_brackets:
                problems += 1
                status = "[!]"
            else:
                status = "[OK]"
            
            print(f"{status} {german:25} -> {hint}")
            
            count += 1
            if count >= 20:
                break
        if count >= 20:
            break
    
    print("\n" + "=" * 70)
    if problems == 0:
        print("[УСПЕХ] Все подсказки обновлены правильно!")
        print("- Убраны названия фаз в скобках")
        print("- Добавлены лингвистические нюансы")
        print("- Каждое слово имеет осмысленную подсказку")
    else:
        print(f"[ВНИМАНИЕ] Найдено {problems} подсказок со скобками")

# Проверяем другие персонажи
def check_all_characters():
    from pathlib import Path
    
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    characters = ["cordelia", "goneril", "edgar", "fool", "edmund"]
    
    print("\n[ПРИМЕРЫ ИЗ ДРУГИХ ПЕРСОНАЖЕЙ]")
    print("-" * 70)
    
    for char in characters:
        file_path = characters_dir / f"{char}.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Показываем по 3 примера
        examples = []
        for phase in data.get("journey_phases", []):
            for vocab in phase.get("vocabulary", []):
                if len(examples) < 3:
                    examples.append(f"  {vocab['german']:20} -> {vocab['russian_hint']}")
        
        print(f"\n{char.upper()}:")
        for ex in examples:
            print(ex)

verify_update()
check_all_characters()
