import subprocess
import sys
from pathlib import Path

# Запускаем генерацию сайта
print("[ГЕНЕРАЦИЯ САЙТА С ОБНОВЛЕННЫМИ ПОДСКАЗКАМИ]")
print("=" * 60)

result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

print(f"\nExit code: {result.returncode}")

# Проверяем созданные файлы
output_dir = Path(r'F:\AiKlientBank\KingLearComic\output')
if output_dir.exists():
    index_file = output_dir / 'index.html'
    journey_dir = output_dir / 'journeys'
    
    if journey_dir.exists():
        journey_files = list(journey_dir.glob('*.html'))
        
        print("\n[РЕЗУЛЬТАТ ГЕНЕРАЦИИ]")
        print("-" * 60)
        print(f"  [OK] index.html создан: {index_file.exists()}")
        print(f"  [OK] Journey файлов создано: {len(journey_files)}")
        
        if len(journey_files) == 12:
            print("  [OK] Все 12 персонажей сгенерированы!")
        else:
            print(f"  [!] Ожидалось 12 файлов, создано {len(journey_files)}")
            
        # Показываем список файлов
        if journey_files:
            print("\n  Созданные файлы:")
            for f in sorted(journey_files):
                print(f"    - {f.name}")
    else:
        print("  [!] Папка journeys не создана")
else:
    print("[ERROR] Папка output не существует")

print("\n[ЗАВЕРШЕНО] Проверка генерации завершена")
