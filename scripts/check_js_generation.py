"""
Тест: Проверка генерации JavaScript с подсказками
Дата: 09.01.2025
Мета: Проверяем что russian_hint правильно передается в JavaScript
"""

import sys
import json
from pathlib import Path

sys.path.append(r'F:\AiKlientBank\KingLearComic')

from generators.js.serializer import PhaseSerializer

def check_js_generation():
    print("[INFO] Проверка генерации JavaScript кода с подсказками...")
    print("=" * 60)
    
    # Загрузим данные персонажа
    char_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')
    with open(char_path, 'r', encoding='utf-8') as f:
        character = json.load(f)
    
    # Создадим сериализатор
    serializer = PhaseSerializer(character)
    
    # Получим сериализованные данные
    js_code = serializer.serialize()
    
    # Проверим наличие phaseVocabularies
    if 'const phaseVocabularies' in js_code:
        print("[OK] phaseVocabularies найден в сгенерированном коде")
    else:
        print("[ERROR] phaseVocabularies НЕ найден!")
        return
    
    # Парсим JSON из JS кода
    import re
    match = re.search(r'const phaseVocabularies = ({.*?});', js_code, re.DOTALL)
    if match:
        vocab_json = match.group(1)
        try:
            vocab_data = json.loads(vocab_json)
            print(f"[OK] Распарсили данные фаз: {len(vocab_data)} фаз")
            
            # Проверим первую фазу
            first_phase_key = list(vocab_data.keys())[0]
            first_phase = vocab_data[first_phase_key]
            
            print(f"\n[+] Анализ фазы '{first_phase_key}':")
            print(f"    - title: {first_phase.get('title', 'N/A')}")
            print(f"    - vocabulary entries: {len(first_phase.get('vocabulary', []))}")
            print(f"    - words entries: {len(first_phase.get('words', []))}")
            
            # Проверим наличие russian_hint в words
            words_with_hints = 0
            for word in first_phase.get('words', []):
                if word.get('russian_hint'):
                    words_with_hints += 1
            
            print(f"    - words with russian_hint: {words_with_hints}")
            
            # Покажем первое слово с подсказкой
            for word in first_phase.get('words', []):
                if word.get('russian_hint'):
                    print(f"\n[+] Пример слова с подсказкой:")
                    print(f"    word: {word.get('word')}")
                    print(f"    translation: {word.get('translation')}")
                    print(f"    russian_hint: {word.get('russian_hint')}")
                    print(f"    transcription: {word.get('transcription')}")
                    break
            
            return vocab_data
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Не удалось распарсить JSON: {e}")
    
    return None

if __name__ == "__main__":
    data = check_js_generation()
    
    # Проверим также что в HTML файле есть правильные данные
    print("\n" + "=" * 60)
    print("[INFO] Проверка HTML файла...")
    
    html_path = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Проверим наличие ключевых элементов
        checks = {
            "phaseVocabularies": "const phaseVocabularies",
            "journey_runtime.js": "journey_runtime.js",
            "buildPhaseQuizWords": "buildPhaseQuizWords"
        }
        
        for name, pattern in checks.items():
            if pattern in html_content:
                print(f"[OK] {name} найден в HTML")
            else:
                print(f"[ERROR] {name} НЕ найден в HTML!")
