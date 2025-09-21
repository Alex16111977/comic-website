"""
Скрипт для проверки упражнений в HTML файлах
"""
import os
import re
from pathlib import Path

def check_html_file(filepath):
    """Проверяет наличие ключевых элементов в HTML файле"""
    print(f"\n[INFO] Проверка файла: {filepath.name}")
    print("=" * 60)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверки наличия элементов
    checks = {
        'window.phaseVocabularies': 'window.phaseVocabularies' in content,
        'window.phaseKeys': 'window.phaseKeys' in content, 
        'window.initializeExercises': 'window.initializeExercises' in content,
        'script теги': '<script' in content,
        'matching-container': 'data-matching-container' in content,
        'articles-container': 'data-articles-container' in content,
        'context-container': 'data-context-container' in content,
        'exercise-phase блоки': 'exercise-phase' in content
    }
    
    print("[+] Проверка наличия ключевых элементов:")
    for key, present in checks.items():
        status = "[OK]" if present else "[ERROR]"
        print(f"  {status} {key}: {present}")
    
    # Ищем определение phaseVocabularies
    if 'window.phaseVocabularies' in content:
        pos = content.find('window.phaseVocabularies')
        
        # Извлекаем объект phaseVocabularies
        start = content.find('{', pos)
        if start != -1:
            # Находим конец объекта (простой подсчет скобок)
            brackets = 1
            end = start + 1
            while brackets > 0 and end < len(content):
                if content[end] == '{':
                    brackets += 1
                elif content[end] == '}':
                    brackets -= 1
                end += 1
            
            vocab_data = content[start:end]
            
            # Анализ структуры данных
            print("\n[+] Анализ структуры phaseVocabularies:")
            
            # Находим все фазы
            phases = re.findall(r'"(\w+)":\s*{', vocab_data)
            print(f"  [OK] Найдено фаз: {len(phases)}")
            if phases:
                print(f"  [OK] Фазы: {', '.join(phases[:5])}...")
            
            # Проверяем структуру первой фазы
            if phases:
                first_phase = phases[0]
                phase_pattern = f'"{first_phase}":\\s*{{([^}}]+)}}'
                phase_match = re.search(phase_pattern, vocab_data)
                
                if phase_match:
                    phase_content = phase_match.group(1)
                    
                    # Проверяем наличие полей
                    has_title = '"title"' in phase_content
                    has_words = '"words"' in phase_content or '"vocabulary"' in phase_content
                    
                    print(f"\n[+] Структура фазы '{first_phase}':")
                    print(f"  {'[OK]' if has_title else '[ERROR]'} Поле 'title': {has_title}")
                    print(f"  {'[OK]' if has_words else '[ERROR]'} Поле 'words/vocabulary': {has_words}")
                    
                    # Проверяем структуру слов
                    if has_words:
                        # Находим первое слово
                        word_match = re.search(r'{[^}]*"word"[^}]*}', phase_content)
                        if word_match:
                            word_data = word_match.group()
                            
                            word_fields = {
                                'word': '"word"' in word_data,
                                'translation': '"translation"' in word_data,
                                'sentence': '"sentence"' in word_data,
                                'sentenceTranslation': '"sentenceTranslation"' in word_data,
                                'gender': '"gender"' in word_data
                            }
                            
                            print("\n[+] Структура слова:")
                            for field, present in word_fields.items():
                                status = "[OK]" if present else "[!]"
                                print(f"    {status} {field}: {present}")
    
    # Проверка функций упражнений
    print("\n[+] Проверка функций упражнений:")
    
    functions = [
        'initializeMatchingExercise',
        'initializeArticlesExercise', 
        'initializeContextExercise',
        'refreshActiveExerciseContentHeight'
    ]
    
    for func in functions:
        present = func in content
        status = "[OK]" if present else "[ERROR]"
        print(f"  {status} {func}: {present}")
    
    # Проверка вызова инициализации
    init_call = re.search(r'window\.initializeExercises\([^)]*\)', content)
    if init_call:
        print(f"\n[OK] Найден вызов инициализации: {init_call.group()[:100]}")
    else:
        print("\n[ERROR] Вызов window.initializeExercises не найден!")
    
    return checks

if __name__ == "__main__":
    output_dir = Path(r'F:\AiKlientBank\KingLearComic\output\journeys')
    
    if not output_dir.exists():
        print("[ERROR] Папка output/journeys не существует!")
        exit(1)
    
    # Проверяем king_lear.html
    king_lear_file = output_dir / 'king_lear.html'
    
    if king_lear_file.exists():
        check_html_file(king_lear_file)
    else:
        print(f"[ERROR] Файл {king_lear_file} не найден!")
        
        # Список всех HTML файлов
        html_files = list(output_dir.glob('*.html'))
        if html_files:
            print(f"\n[INFO] Найдено HTML файлов: {len(html_files)}")
            for f in html_files[:3]:
                print(f"  - {f.name}")
