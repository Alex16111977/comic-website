"""
Проверка доступности данных для новых упражнений
Дата: 14.09.2025
"""
import json
import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def analyze_character_data():
    """Анализ данных персонажей для упражнений."""
    characters_dir = Path(__file__).parent.parent / 'data' / 'characters'
    
    print("[АНАЛИЗ ДАННЫХ ДЛЯ УПРАЖНЕНИЙ]")
    print("=" * 50)
    
    total_stats = {
        'characters': 0,
        'total_words': 0,
        'with_articles': 0,
        'with_sentences': 0,
        'with_both': 0
    }
    
    for char_file in sorted(characters_dir.glob('*.json')):
        if char_file.name == '.gitkeep':
            continue
            
        with open(char_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_stats['characters'] += 1
        char_name = data.get('name', char_file.stem)
        # Проверяем два варианта структуры
        stages = data.get('journey_phases', [])
        if not stages:
            stages = data.get('journey', {}).get('stages', [])
        
        char_stats = {
            'words': 0,
            'articles': 0,
            'sentences': 0,
            'both': 0
        }
        
        for stage in stages:
            vocab = stage.get('vocabulary', [])
            for word in vocab:
                char_stats['words'] += 1
                
                # Проверка артиклей
                german = word.get('german', '')
                has_article = german.startswith(('der ', 'die ', 'das '))
                if has_article:
                    char_stats['articles'] += 1
                
                # Проверка предложений
                has_sentence = all(
                    word.get(k) for k in ['german', 'russian', 'sentence', 'sentence_translation']
                )
                if has_sentence:
                    char_stats['sentences'] += 1
                    
                if has_article and has_sentence:
                    char_stats['both'] += 1
        
        # Обновляем общую статистику
        total_stats['total_words'] += char_stats['words']
        total_stats['with_articles'] += char_stats['articles']
        total_stats['with_sentences'] += char_stats['sentences']
        total_stats['with_both'] += char_stats['both']
        
        # Выводим для важных персонажей
        if char_name in ['Король Лир', 'Корделия', 'King Lear', 'Cordelia']:
            print(f"\n[{char_name}]")
            print(f"  Всего слов: {char_stats['words']}")
            print(f"  С артиклями: {char_stats['articles']}")
            print(f"  С предложениями: {char_stats['sentences']}")
            print(f"  С обоими: {char_stats['both']}")
    
    print("\n" + "=" * 50)
    print("[ИТОГОВАЯ СТАТИСТИКА]")
    print(f"  Персонажей: {total_stats['characters']}")
    print(f"  Всего слов: {total_stats['total_words']}")
    
    if total_stats['total_words'] > 0:
        art_pct = total_stats['with_articles'] * 100 // total_stats['total_words']
        sent_pct = total_stats['with_sentences'] * 100 // total_stats['total_words']
        both_pct = total_stats['with_both'] * 100 // total_stats['total_words']
        
        print(f"  С артиклями: {total_stats['with_articles']} ({art_pct}%)")
        print(f"  С предложениями: {total_stats['with_sentences']} ({sent_pct}%)")
        print(f"  С обоими: {total_stats['with_both']} ({both_pct}%)")
        
    print("\n[ВЫВОД]")
    if total_stats['with_articles'] > 100:
        print("  [OK] Достаточно данных для упражнения 'Артикли и род'")
    else:
        print("  [!] Мало данных для упражнения 'Артикли и род'")
        
    if total_stats['with_sentences'] > 100:
        print("  [OK] Достаточно данных для 'Контекстного перевода'")
    else:
        print("  [!] Мало данных для 'Контекстного перевода'")

if __name__ == "__main__":
    analyze_character_data()
