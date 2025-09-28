#!/usr/bin/env python
"""
Аналіз німецького словника з усіх персонажів
Дата створення: 28.09.2025
"""
import json
import sys
from pathlib import Path
from collections import Counter

# Додаємо корінь проекту в path
sys.path.insert(0, str(Path(__file__).parent.parent))

def analyze_vocabulary():
    """Аналіз всіх німецьких слів у проекті"""
    characters_dir = Path(__file__).parent.parent / "data" / "characters"
    
    all_words = []
    articles_count = Counter()
    
    # Читаємо всіх персонажів
    for char_file in characters_dir.glob("*.json"):
        try:
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Збираємо слова з vocabulary
            for phase in data.get('journey_phases', []):
                for word in phase.get('vocabulary', []):
                    german = word.get('german', '')
                    all_words.append(german)
                    
                    # Визначаємо артикль
                    if german.startswith('der '):
                        articles_count['der'] += 1
                    elif german.startswith('die '):
                        articles_count['die'] += 1
                    elif german.startswith('das '):
                        articles_count['das'] += 1
                    else:
                        articles_count['none'] += 1
        except Exception as e:
            print(f"[ERROR] Помилка при читанні {char_file.name}: {e}")
    
    print(f"[OK] Знайдено персонажів: {len(list(characters_dir.glob('*.json')))}")
    print(f"[OK] Всього німецьких слів: {len(all_words)}")
    print(f"[OK] Розподіл артиклів:")
    print(f"  - der (чоловічий): {articles_count['der']}")
    print(f"  - die (жіночий): {articles_count['die']}")
    print(f"  - das (середній): {articles_count['das']}")
    print(f"  - без артикля: {articles_count['none']}")
    
    return all_words, articles_count

if __name__ == "__main__":
    words, stats = analyze_vocabulary()
