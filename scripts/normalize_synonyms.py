"""
Скрипт нормалізації синонімів у vocabulary.json
Мета: очистити синоніми від inline пояснень та перенести їх в окреме поле
"""

import json
import re
from pathlib import Path

def normalize_synonyms(vocab_data):
    """
    Нормалізує синоніми:
    1. Видаляє inline пояснення (текст після — або в дужках)
    2. Переносить пояснення в поле synonym_notes
    3. Розділяє змішані мови на окремі елементи
    """
    
    changes_count = 0
    
    # Обробка слів у словнику
    for word in vocab_data.get('vocabulary', vocab_data.get('words', [])):
        if 'synonyms' not in word or not word['synonyms']:
            continue
            
        original_synonyms = word['synonyms'].copy() if isinstance(word['synonyms'], list) else [word['synonyms']]
        normalized_synonyms = []
        synonym_notes = []
        
        for syn in original_synonyms:
            if not isinstance(syn, str):
                normalized_synonyms.append(syn)
                continue
                
            # Шукаємо inline пояснення
            # Патерн 1: "слово — пояснення"
            if ' — ' in syn or ' – ' in syn:
                parts = re.split(r' [—–] ', syn)
                main_word = parts[0].strip()
                explanation = ' — '.join(parts[1:]).strip() if len(parts) > 1 else None
                
                # Якщо основне слово кирилицею
                if re.search(r'[а-яА-ЯёЁ]', main_word):
                    normalized_synonyms.append(main_word)
                    if explanation:
                        # Якщо пояснення містить німецьке слово
                        german_match = re.search(r'([a-zA-ZäöüÄÖÜß]+)', explanation)
                        if german_match:
                            normalized_synonyms.append(german_match.group(1))
                            synonym_notes.append(f"{german_match.group(1)}: {explanation}")
                        else:
                            synonym_notes.append(f"{main_word}: {explanation}")
                # Якщо основне слово латиницею (німецька)
                elif re.search(r'[a-zA-ZäöüÄÖÜß]', main_word):
                    normalized_synonyms.append(main_word)
                    if explanation:
                        # Витягуємо російський переклад якщо є
                        russian_match = re.search(r'«([^»]+)»', explanation)
                        if russian_match:
                            normalized_synonyms.append(russian_match.group(1))
                        synonym_notes.append(f"{main_word}: {explanation}")
                        
            # Патерн 2: текст в дужках
            elif '(' in syn and ')' in syn:
                main_part = re.sub(r'\s*\([^)]*\)', '', syn).strip()
                bracket_content = re.search(r'\(([^)]*)\)', syn)
                
                if main_part:
                    normalized_synonyms.append(main_part)
                if bracket_content:
                    note = bracket_content.group(1)
                    synonym_notes.append(f"{main_part}: {note}")
                    
            # Патерн 3: розділені комою різномовні синоніми  
            elif ',' in syn:
                parts = [p.strip() for p in syn.split(',')]
                for part in parts:
                    if part and not part in normalized_synonyms:
                        normalized_synonyms.append(part)
                        
            else:
                # Чистий синонім без пояснень
                if syn.strip() and syn.strip() not in normalized_synonyms:
                    normalized_synonyms.append(syn.strip())
        
        # Видаляємо дублікати
        seen = set()
        unique_synonyms = []
        for s in normalized_synonyms:
            if s and s not in seen:
                seen.add(s)
                unique_synonyms.append(s)
        
        # Оновлюємо слово якщо були зміни
        if unique_synonyms != original_synonyms:
            word['synonyms'] = unique_synonyms
            if synonym_notes:
                # Об'єднуємо з існуючими нотатками якщо вони є
                existing_notes = word.get('synonym_notes', '')
                if existing_notes:
                    word['synonym_notes'] = existing_notes + '; ' + '; '.join(synonym_notes)
                else:
                    word['synonym_notes'] = '; '.join(synonym_notes)
            changes_count += 1
            
            print(f"[OK] Нормалізовано '{word.get('german', word.get('word', 'unknown'))}':")
            print(f"     Було: {original_synonyms}")
            print(f"     Стало: {unique_synonyms}")
            if 'synonym_notes' in word:
                print(f"     Примітки: {word['synonym_notes']}")
    
    return vocab_data, changes_count

def main():
    """Головна функція"""
    
    # Шляхи до файлів
    vocab_path = Path(r"F:\AiKlientBank\KingLearComic\data\vocabulary\vocabulary.json")
    
    print("[START] Нормалізація синонімів у vocabulary.json")
    print(f"[INFO] Файл: {vocab_path}")
    
    # Читання файлу
    try:
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        print(f"[OK] Прочитано {len(vocab_data.get('vocabulary', vocab_data.get('words', [])))} слів")
    except Exception as e:
        print(f"[ERROR] Помилка читання файлу: {e}")
        return 1
    
    # Нормалізація
    normalized_data, changes = normalize_synonyms(vocab_data)
    
    print(f"\n[OK] Нормалізовано синоніми для {changes} слів")
    
    # Збереження результату
    try:
        with open(vocab_path, 'w', encoding='utf-8') as f:
            json.dump(normalized_data, json_dumps_params={
                'ensure_ascii': False,
                'indent': 2
            }, f)
        print(f"[OK] Збережено оновлений файл: {vocab_path}")
    except Exception as e:
        print(f"[ERROR] Помилка збереження файлу: {e}")
        return 1
    
    # Тепер потрібно перегенерувати HTML файли
    print("\n[INFO] Запускаю генератор для оновлення HTML...")
    import subprocess
    import sys
    
    result = subprocess.run(
        [sys.executable, 'main.py'],
        capture_output=True,
        text=True,
        cwd=r'F:\AiKlientBank\KingLearComic'
    )
    
    if result.returncode == 0:
        print("[OK] HTML файли успішно перегенеровані")
        print(result.stdout)
    else:
        print(f"[ERROR] Помилка генерації: {result.stderr}")
        return 1
        
    print("\n[DONE] Нормалізація завершена успішно!")
    return 0

if __name__ == "__main__":
    exit(main())
