"""
Тест універсальної системи тренування
Дата: 20.09.2025
"""
import subprocess
import sys
from pathlib import Path
import json

print("[!] Тестування універсальної системи тренування")

# 1. Проверяем наличие шаблона
template_file = Path(r'F:\AiKlientBank\KingLearComic\templates\training.html')
if template_file.exists():
    print("[OK] Шаблон training.html найден")
else:
    print("[ERROR] Шаблон training.html НЕ найден")

# 2. Генерируем сайт
print("\n[!] Генерирую сайт...")
result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

if result.returncode == 0:
    print("[OK] Сайт сгенерирован")
else:
    print("[ERROR] Ошибка генерации")
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)

# 3. Проверяем что training.html создан
output_file = Path(r'F:\AiKlientBank\KingLearComic\output\training.html')
if output_file.exists():
    print("[OK] Файл output/training.html создан")
    
    # Проверяем содержимое
    content = output_file.read_text(encoding='utf-8')
    checks = [
        ('TrainingSystem.init()', 'Инициализация системы'),
        ('showIntroduction', 'Упражнение знакомства'),
        ('showChooseTranslation', 'Упражнение выбора перевода'),
        ('showReverseTranslation', 'Упражнение обратного перевода'),
        ('showArticleExercise', 'Упражнение с артиклем'),
        ('showContextExercise', 'Упражнение контекста'),
        ('loadWordExamples', 'Загрузка примеров'),
        ('localStorage', 'Работа с localStorage')
    ]
    
    print("\n[!] Проверка функционала:")
    for check_str, desc in checks:
        if check_str in content:
            print(f"  [OK] {desc}")
        else:
            print(f"  [ERROR] НЕ найдено: {desc}")
else:
    print("[ERROR] Файл output/training.html НЕ создан")

# 4. Проверяем что ссылки правильные в index.html
index_file = Path(r'F:\AiKlientBank\KingLearComic\output\index.html')
if index_file.exists():
    content = index_file.read_text(encoding='utf-8')
    
    if 'training.html?word=' in content:
        print("\n[OK] Ссылки на training.html с параметрами найдены")
    else:
        print("\n[ERROR] Ссылки на training.html НЕ найдены")

# 5. Симуляция добавления слов в localStorage
print("\n[!] Тестовые данные для localStorage:")
test_words = [
    {
        "id": "der_thron",
        "word": "der Thron",
        "translation": "трон",
        "transcription": "[трон]",
        "emoji": "👑",
        "level": "A2"
    },
    {
        "id": "die_macht",
        "word": "die Macht", 
        "translation": "власть",
        "transcription": "[махт]",
        "emoji": "⚡",
        "level": "B1"
    }
]

print(f"  Слова для тестирования: {len(test_words)}")
for word in test_words:
    print(f"  - {word['word']} -> training.html?word={word['id']}")

print("\n[!] Тестирование завершено")
print("[!] Для полного теста откройте в браузере:")
print("  1. output/index.html")
print("  2. Добавьте слова через 'Изучить' на страницах персонажей")
print("  3. Нажмите 'Тренировка' на главной странице")
