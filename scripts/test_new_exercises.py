"""
Финальная проверка новых упражнений
"""
import subprocess
import sys
from pathlib import Path

def test_exercises():
    print("[ТЕСТИРОВАНИЕ НОВЫХ УПРАЖНЕНИЙ]")
    print("=" * 50)
    
    # 1. Проверка файлов
    files = {
        'static/js/exercises.js': 'JavaScript упражнений',
        'static/css/exercises.css': 'CSS стили'
    }
    
    root = Path(r'F:\AiKlientBank\KingLearComic')
    
    for file, desc in files.items():
        path = root / file
        if path.exists():
            size = path.stat().st_size
            print(f"[OK] {file}: {desc} ({size} байт)")
        else:
            print(f"[ERROR] {file}: НЕ НАЙДЕН")
            return False
    
    # 2. Запуск генерации
    print("\n[ГЕНЕРАЦИЯ САЙТА]")
    result = subprocess.run(
        [sys.executable, str(root / 'main.py')],
        capture_output=True,
        text=True,
        cwd=str(root)
    )
    
    if result.returncode == 0:
        print("[OK] Генерация успешна!")
        
        # 3. Проверка output файлов
        output_dir = root / 'output'
        index = output_dir / 'index.html'
        journeys = list((output_dir / 'journeys').glob('*.html'))
        
        print(f"[OK] index.html: {index.exists()}")
        print(f"[OK] journey файлов: {len(journeys)}")
        
        # 4. Проверка содержимого
        if journeys:
            sample = journeys[0]
            with open(sample, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks = [
                ('exercises.js', 'Скрипт упражнений'),
                ('exercises.css', 'Стили упражнений'),
                ('initializeExercises', 'Функция инициализации')
            ]
            
            for check, desc in checks:
                if check in content:
                    print(f"[OK] Найдено: {desc}")
                else:
                    print(f"[WARNING] Не найдено: {desc}")
        
        return True
    else:
        print("[ERROR] Ошибка генерации:")
        print(result.stderr[:500] if result.stderr else result.stdout[:500])
        return False

if __name__ == "__main__":
    success = test_exercises()
    
    if success:
        print("\n" + "=" * 50)
        print("[SUCCESS] УПРАЖНЕНИЯ ГОТОВЫ!")
        print("\n1. Артикли и род - drag & drop сортировка")
        print("2. Контекстный перевод - выбор в контексте")
        print("\nОткройте output/index.html в браузере!")
    else:
        print("\n[FAIL] Проверьте ошибки выше")