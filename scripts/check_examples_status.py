"""
Скрипт для проверки статуса примеров во всех файлах персонажей
Дата: 20.09.2025
Цель: Определить какие файлы уже исправлены, а какие содержат художественные тексты
"""

import json
from pathlib import Path

def check_character_examples():
    """Проверяет все файлы персонажей на наличие художественных примеров"""
    
    characters_dir = Path(r'F:\AiKlientBank\KingLearComic\data\characters')
    
    # Слова-маркеры художественных текстов
    art_markers = [
        'Cordelia', 'Lear', 'Goneril', 'Regan', 'Edgar', 'Edmund', 
        'Gloucester', 'Kent', 'Fool', 'Albany', 'Cornwall', 'Oswald',
        'Thronsaal', 'Kronleuchter', 'Hofes', 'König', 'Narr',
        'verschränkt', 'presse', 'zwischen die Zähne', 'flüstere',
        'zeichne das Wort', 'umarme das Wort', 'wie geschmolzenes Gold'
    ]
    
    results = {
        'fixed': [],
        'needs_fixing': [],
        'total_words_to_fix': 0
    }
    
    print("[ПРОВЕРКА СТАТУСА ФАЙЛОВ ПЕРСОНАЖЕЙ]")
    print("=" * 60)
    
    # Проверяем каждый JSON файл
    for file_path in sorted(characters_dir.glob('*.json')):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        character_name = data.get('name', file_path.stem)
        total_words = 0
        artistic_examples = 0
        sample_artistic = []
        
        # Проверяем каждую фазу
        for phase in data.get('journey_phases', []):
            for word in phase.get('vocabulary', []):
                total_words += 1
                sentence = word.get('sentence', '')
                
                # Проверяем наличие маркеров художественного текста
                has_artistic = any(marker in sentence for marker in art_markers)
                
                if has_artistic:
                    artistic_examples += 1
                    if len(sample_artistic) < 2:  # Сохраняем примеры
                        sample_artistic.append({
                            'word': word.get('german'),
                            'sentence': sentence[:80] + '...' if len(sentence) > 80 else sentence
                        })
        
        # Определяем статус файла
        if artistic_examples == 0:
            status = "OK - ИСПРАВЛЕН"
            results['fixed'].append(file_path.name)
            print(f"\n[OK] {file_path.name} - {character_name}")
            print(f"     Статус: {status}")
            print(f"     Всего слов: {total_words}")
        else:
            status = "ТРЕБУЕТ ИСПРАВЛЕНИЯ"
            results['needs_fixing'].append(file_path.name)
            results['total_words_to_fix'] += total_words
            
            print(f"\n[!] {file_path.name} - {character_name}")
            print(f"    Статус: {status}")
            print(f"    Художественных примеров: {artistic_examples}/{total_words}")
            
            if sample_artistic:
                print(f"    Примеры проблемных предложений:")
                for sample in sample_artistic:
                    print(f"      - {sample['word']}: \"{sample['sentence']}\"")
    
    # Итоговая статистика
    print("\n" + "=" * 60)
    print("[ИТОГОВАЯ СТАТИСТИКА]")
    print(f"\nИсправлено файлов: {len(results['fixed'])}")
    for file in results['fixed']:
        print(f"  [OK] {file}")
    
    print(f"\nТребуют исправления: {len(results['needs_fixing'])}")
    for file in results['needs_fixing']:
        print(f"  [!] {file}")
    
    print(f"\nВсего слов для исправления: {results['total_words_to_fix']}")
    print(f"Прогресс: {len(results['fixed'])}/12 файлов ({len(results['fixed'])*100//12}%)")
    
    # Создаём отчёт
    report = {
        'date': '20.09.2025',
        'fixed_files': results['fixed'],
        'files_to_fix': results['needs_fixing'],
        'total_words_to_fix': results['total_words_to_fix'],
        'progress_percent': len(results['fixed']) * 100 // 12
    }
    
    # Сохраняем отчёт
    report_path = Path(r'F:\AiKlientBank\KingLearComic\scripts\examples_status_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Отчёт сохранён: {report_path}")
    
    return results

if __name__ == "__main__":
    check_character_examples()
