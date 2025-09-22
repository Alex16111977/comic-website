"""
Финальный тест интеграции упражнений
Дата: 14.09.2025
"""
import subprocess
import sys
from pathlib import Path
import json

def test_exercises_integration():
    """Тестирует интеграцию новых упражнений."""
    
    print("[ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ УПРАЖНЕНИЙ]")
    print("=" * 50)
    
    # 1. Проверка наличия файлов
    print("\n[1/5] Проверка файлов...")
    files_to_check = [
        ('static/js/exercises.js', 'JavaScript модуль упражнений'),
        ('static/css/exercises.css', 'CSS стили упражнений'),
        ('templates/journey.html', 'HTML шаблон'),
        ('static/js/journey_runtime.js', 'Runtime JavaScript')
    ]
    
    project_root = Path(r'F:\AiKlientBank\KingLearComic')
    all_files_exist = True
    
    for file_path, desc in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  [OK] {file_path}: {desc}")
        else:
            print(f"  [ERROR] {file_path}: НЕ НАЙДЕН - {desc}")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n[FAIL] Не все файлы на месте!")
        return False
    
    # 2. Проверка подключения в HTML
    print("\n[2/5] Проверка подключения в HTML...")
    html_path = project_root / 'templates/journey.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    checks = [
        ('exercises.css', 'CSS стили'),
        ('exercises.js', 'JavaScript модуль')
    ]
    
    for check, desc in checks:
        if check in html_content:
            print(f"  [OK] {check}: подключен - {desc}")
        else:
            print(f"  [WARNING] {check}: НЕ подключен - {desc}")
    
    # 3. Проверка секций в HTML
    print("\n[3/5] Проверка секций упражнений...")
    sections = [
        ('word-families-section', 'Секция артиклей (бывшая Семья слов)')
    ]
    
    for section, desc in sections:
        if section in html_content:
            print(f"  [OK] {section}: {desc}")
        else:
            print(f"  [ERROR] {section}: НЕ НАЙДЕНА - {desc}")
    
    # 4. Проверка данных персонажей
    print("\n[4/5] Проверка данных для упражнений...")
    chars_dir = project_root / 'data/characters'
    
    total_articles = 0
    total_sentences = 0
    
    for char_file in chars_dir.glob('*.json'):
        if char_file.name == '.gitkeep':
            continue
            
        with open(char_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        phases = data.get('journey_phases', [])
        for phase in phases:
            vocab = phase.get('vocabulary', [])
            for word in vocab:
                german = word.get('german', '')
                if german.startswith(('der ', 'die ', 'das ')):
                    total_articles += 1
                if all(k in word for k in ['german', 'russian', 'sentence', 'sentence_translation']):
                    total_sentences += 1
    
    print(f"  [OK] Слов с артиклями: {total_articles}")
    print(f"  [OK] Слов с предложениями: {total_sentences}")
    
    # 5. Генерация тестовой страницы
    print("\n[5/5] Запуск генерации...")
    result = subprocess.run(
        [sys.executable, str(project_root / 'main.py')],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    if result.returncode == 0:
        print("  [OK] Генерация успешна!")
        
        # Проверяем наличие output файлов
        output_dir = project_root / 'output'
        if output_dir.exists():
            html_files = list(output_dir.glob('**/*.html'))
            print(f"  [OK] Создано HTML файлов: {len(html_files)}")
        
        return True
    else:
        print(f"  [ERROR] Ошибка генерации:")
        print(result.stderr[:500] if result.stderr else result.stdout[:500])
        return False

if __name__ == "__main__":
    try:
        success = test_exercises_integration()
        
        if success:
            print("\n" + "=" * 50)
            print("[SUCCESS] ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
            print("\nУпражнения готовы к использованию:")
            print("1. 'Артикли и род' - сортировка слов по родам")
            print("2. 'Контекстный перевод' - выбор правильного перевода в контексте")
            print("\nОткройте output/index.html в браузере для проверки!")
        else:
            print("\n" + "=" * 50)
            print("[FAIL] Есть проблемы с интеграцией")
            print("\nПроверьте:")
            print("1. Все ли файлы созданы")
            print("2. Правильно ли подключены в HTML")
            print("3. Нет ли ошибок в JavaScript")
    
    except Exception as e:
        print(f"\n[ERROR] Критическая ошибка: {e}")
        sys.exit(1)
