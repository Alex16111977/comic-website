import json
import sys
from pathlib import Path

# Анализ текущего состояния подсказок
def analyze_hints_coverage():
    """Анализируем покрытие russian_hint для всех персонажей"""
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    characters = ["king_lear", "cordelia", "goneril", "regan", "gloucester", "edgar", 
                  "edmund", "kent", "fool", "albany", "cornwall", "oswald"]
    
    print("[АНАЛИЗ ТЕКУЩЕГО СОСТОЯНИЯ RUSSIAN_HINT]")
    print("=" * 60)
    
    total_words = 0
    total_with_hints = 0
    problem_hints = []
    
    for char in characters:
        file_path = characters_dir / f"{char}.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            char_words = 0
            char_hints = 0
            char_problems = []
            
            for phase in data.get("journey_phases", []):
                for vocab in phase.get("vocabulary", []):
                    char_words += 1
                    if vocab.get("russian_hint"):
                        char_hints += 1
                        # Проверяем на проблемные подсказки (со скобками)
                        if "(" in vocab["russian_hint"] and ")" in vocab["russian_hint"]:
                            char_problems.append(vocab["german"])
                    
            coverage = (char_hints / char_words * 100) if char_words > 0 else 0
            status = "[OK]" if coverage == 100 else "[!]"
            
            print(f"{status} {char:12} - Слов: {char_words:3}, Подсказок: {char_hints:3} ({coverage:.0f}%)")
            
            if char_problems:
                problem_hints.append((char, char_problems))
            
            total_words += char_words
            total_with_hints += char_hints
            
        except Exception as e:
            print(f"[ERROR] {char}: {e}")
    
    print("-" * 60)
    total_coverage = (total_with_hints / total_words * 100) if total_words > 0 else 0
    print(f"ИТОГО: {total_words} слов, {total_with_hints} с подсказками ({total_coverage:.0f}%)")
    
    if problem_hints:
        print("\n[ПРОБЛЕМНЫЕ ПОДСКАЗКИ СО СКОБКАМИ]:")
        for char, problems in problem_hints:
            print(f"  {char}: {len(problems)} слов с '()' в подсказках")
    
    # Показываем примеры слов без подсказок
    print("\n[ПРИМЕРЫ СЛОВ БЕЗ ПОДСКАЗОК]:")
    for char in ["goneril", "edgar", "edmund"]:
        file_path = characters_dir / f"{char}.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            examples = []
            for phase in data.get("journey_phases", []):
                for vocab in phase.get("vocabulary", []):
                    if not vocab.get("russian_hint"):
                        examples.append(f"  {char:8}: {vocab['german']:20} -> {vocab['russian']}")
                    if len(examples) >= 3:
                        break
                if len(examples) >= 3:
                    break
            
            for ex in examples:
                print(ex)
                
        except Exception:
            pass
    
    return total_coverage

if __name__ == "__main__":
    coverage = analyze_hints_coverage()
    print(f"\n[РЕЗУЛЬТАТ] Общее покрытие: {coverage:.1f}%")
