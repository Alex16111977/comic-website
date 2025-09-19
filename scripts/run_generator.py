"""
Запуск генератора King Lear с упражнениями
"""
import subprocess
import sys
from pathlib import Path

project_path = Path(r'F:\AiKlientBank\KingLearComic')

print("[GENERATING] Running main.py...")

# Запускаем main.py
result = subprocess.run(
    [sys.executable, str(project_path / 'main.py')],
    capture_output=True,
    text=True,
    cwd=str(project_path)
)

print(f"[EXIT CODE]: {result.returncode}")

if result.stdout:
    print("\n[OUTPUT]:")
    print(result.stdout)

if result.stderr:
    print("\n[ERRORS]:")
    print(result.stderr)

# Проверяем результат
html_file = project_path / 'output' / 'journeys' / 'king_lear.html'

if html_file.exists():
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Анализ содержимого
    has_exercises = 'exercise-section' in content
    exercise_count = content.count('exercise-section')
    blank_count = content.count('class="blank"')
    
    print(f"\n[ANALYSIS OF king_lear.html]")
    print(f"  File size: {len(content):,} bytes")
    print(f"  Has exercises: {has_exercises}")
    print(f"  Exercise sections: {exercise_count}")
    print(f"  Blank fields: {blank_count}")
    
    if has_exercises:
        print("\n[SUCCESS] Exercises are included!")
    else:
        print("\n[WARNING] No exercises found")
else:
    print("\n[ERROR] File not generated")
