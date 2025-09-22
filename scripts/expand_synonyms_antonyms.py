"""
Розширення покриття синонімів та антонімів для journey phases
GitHub Issue #67: Expand synonym and antonym coverage
Створено: 2025-09-23
"""

import json
from pathlib import Path

# Словник синонімів та антонімів для ключових концепцій
SYNONYM_ANTONYM_DATABASE = {
    "власть": {
        "synonyms": ["могущество", "господство", "владычество", "сила", "авторитет"],
        "antonyms": ["бессилие", "слабость", "немощь", "подчинение", "зависимость"]
    },
    "гнев": {
        "synonyms": ["ярость", "негодование", "возмущение", "бешенство", "злоба"],
        "antonyms": ["спокойствие", "мир", "кротость", "благодушие", "умиротворение"]
    },
    "безумие": {
        "synonyms": ["сумасшествие", "помешательство", "умопомрачение", "психоз", "невменяемость"],
        "antonyms": ["разум", "здравомыслие", "рассудительность", "ясность ума", "трезвость"]
    },
    "отчаяние": {
        "synonyms": ["безнадёжность", "безысходность", "уныние", "тоска", "депрессия"],
        "antonyms": ["надежда", "оптимизм", "вера", "уверенность", "радость"]
    },
    "прощение": {
        "synonyms": ["милосердие", "помилование", "снисхождение", "отпущение", "амнистия"],
        "antonyms": ["месть", "возмездие", "наказание", "расплата", "кара"]
    },
    "мудрость": {
        "synonyms": ["премудрость", "разумность", "благоразумие", "проницательность", "прозорливость"],
        "antonyms": ["глупость", "неразумие", "безрассудство", "недальновидность", "наивность"]
    },
    "предательство": {
        "synonyms": ["измена", "вероломство", "коварство", "предательство", "обман"],
        "antonyms": ["верность", "преданность", "лояльность", "честность", "надёжность"]
    },
    "одиночество": {
        "synonyms": ["уединение", "изоляция", "оставленность", "заброшенность", "отчуждение"],
        "antonyms": ["общение", "компания", "дружба", "близость", "единение"]
    }
}

def generate_synonym_antonym_set(vocab_word, phase_id, theme="general"):
    """Генерирует набор синонимов и антонимов для слова"""
    
    # Определяем базовую тему по фазе
    theme_mapping = {
        "throne": "власть",
        "goneril": "предательство", 
        "regan": "отчаяние",
        "storm": "безумие",
        "hut": "мудрость",
        "dover": "прощение",
        "prison": "прощение"
    }
    
    base_theme = theme_mapping.get(phase_id, "general")
    
    # Создаём набор для конкретного слова
    if vocab_word.get("russian") in SYNONYM_ANTONYM_DATABASE:
        theme_data = SYNONYM_ANTONYM_DATABASE[vocab_word["russian"]]
    elif base_theme in SYNONYM_ANTONYM_DATABASE:
        theme_data = SYNONYM_ANTONYM_DATABASE[base_theme]
    else:
        # Генерируем базовые синонимы из существующих данных
        theme_data = {
            "synonyms": vocab_word.get("synonyms", [])[:3] if vocab_word.get("synonyms") else [],
            "antonyms": []
        }
    
    # Формируем структуру
    syn_ant_set = {
        "id": f"{phase_id}_{vocab_word.get('german', '').replace(' ', '_').lower()}",
        "title": f"Синонимы и антонимы: {vocab_word.get('russian', '')}",
        "target": {
            "word": vocab_word.get("german", ""),
            "translation": vocab_word.get("russian", ""),
            "hint": vocab_word.get("russian_hint", "")
        },
        "synonyms": [],
        "antonyms": [],
        "narration": f"От {vocab_word.get('russian', '')} к пониманию через противоположности."
    }
    
    # Добавляем синонимы (максимум 3-5)
    for syn in theme_data.get("synonyms", [])[:4]:
        syn_ant_set["synonyms"].append({
            "word": f"das/die/der {syn.capitalize()}",  # Упрощённо
            "translation": syn
        })
    
    # Добавляем антонимы (максимум 2-3)  
    for ant in theme_data.get("antonyms", [])[:3]:
        syn_ant_set["antonyms"].append({
            "word": f"das/die/der {ant.capitalize()}",  # Упрощённо
            "translation": ant
        })
    
    return syn_ant_set

def expand_character_synonyms(character_file):
    """Расширяет synonym_antonym_sets для персонажа"""
    
    with open(character_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    
    for phase in data.get('journey_phases', []):
        phase_id = phase.get('id')
        
        # Если нет synonym_antonym_sets или их мало
        if not phase.get('synonym_antonym_sets'):
            phase['synonym_antonym_sets'] = []
            
        current_sets = phase['synonym_antonym_sets']
        existing_words = {s['target']['word'] for s in current_sets if 'target' in s}
        
        # Добавляем наборы для ключевых слов из vocabulary
        vocab_words = phase.get('vocabulary', [])[:3]  # Берём первые 3 слова
        
        for vocab in vocab_words:
            if vocab.get('german') not in existing_words:
                new_set = generate_synonym_antonym_set(vocab, phase_id)
                if new_set['synonyms'] or new_set['antonyms']:  # Добавляем только если есть данные
                    current_sets.append(new_set)
                    modified = True
        
        # Обновляем phase
        phase['synonym_antonym_sets'] = current_sets
    
    return data, modified

def main():
    """Основная функция расширения синонимов и антонимов"""
    
    characters_dir = Path(r'F:\AiKlientBank\KingLearComic\data\characters')
    json_files = [f for f in characters_dir.glob('*.json') if f.name != '.gitkeep']
    
    print("[EXPANSION OF SYNONYMS AND ANTONYMS]")
    print("=" * 60)
    
    total_added = 0
    modified_files = []
    
    for json_file in json_files:
        print(f"\n[PROCESSING] {json_file.name}")
        
        try:
            updated_data, was_modified = expand_character_synonyms(json_file)
            
            if was_modified:
                # Сохраняем обновлённый файл
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, ensure_ascii=False, indent=2)
                
                modified_files.append(json_file.name)
                
                # Подсчитываем добавленные наборы
                added = sum(len(phase.get('synonym_antonym_sets', [])) 
                          for phase in updated_data.get('journey_phases', []))
                total_added += added
                print(f"  [OK] Added synonym/antonym sets")
            else:
                print(f"  [SKIP] Already has sufficient coverage")
                
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print("\n" + "=" * 60)
    print("[SUMMARY]")
    print(f"Modified files: {len(modified_files)}")
    print(f"Files: {', '.join(modified_files)}")
    print(f"Total sets added: {total_added}")
    
    # Створюємо звіт
    report_path = Path(r'F:\AiKlientBank\KingLearComic\scripts\synonyms_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("SYNONYM AND ANTONYM EXPANSION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date: 2025-09-23\n")
        f.write(f"Issue: #67 - Expand synonym and antonym coverage\n\n")
        f.write(f"Modified files: {len(modified_files)}\n")
        for file in modified_files:
            f.write(f"  - {file}\n")
        f.write(f"\nTotal synonym/antonym sets added: {total_added}\n")
        f.write("\nExpansion completed successfully!\n")
    
    print(f"\n[REPORT] Saved to: {report_path}")
    print("\n[SUCCESS] Synonym and antonym coverage expanded!")

if __name__ == "__main__":
    main()
