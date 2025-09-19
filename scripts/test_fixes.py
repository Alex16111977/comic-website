"""
Тест: Проверка исправлений кнопок "Изучить" и удаления разделов повторения
Дата: 20.09.2025
Цель: Убедиться что все исправления применены корректно
"""
import subprocess
import sys
from pathlib import Path

print("[!] Генерирую сайт...")

# 1. Генерируем сайт
result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

print(f"[OK] Сайт сгенерирован: {result.returncode == 0}")
if result.returncode != 0:
    print(f"[ERROR] Ошибка генерации: {result.stderr[:500]}")
else:
    print(f"[OK] Вывод: {result.stdout[:200]}")

# 2. Проверяем что в journey.html НЕТ review-section
journey_file = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
if journey_file.exists():
    content = journey_file.read_text(encoding='utf-8')
    
    # Проверка на наличие раздела повторения
    has_review = 'review-section' in content or 'review-today-section' in content or 'Повторить сегодня' in content
    print(f"[{'ERROR' if has_review else 'OK'}] Journey страница {'содержит' if has_review else 'НЕ содержит'} раздел повторения")
    
    # Проверка наличия обработчика study-btn
    has_study_handler = 'study-btn' in content and 'localStorage' in content
    print(f"[{'OK' if has_study_handler else 'ERROR'}] Обработчик study-btn {'найден' if has_study_handler else 'НЕ найден'}")
    
    # Проверка debug инфо
    has_debug = "console.log('Journey page loaded:'" in content
    print(f"[{'OK' if has_debug else 'ERROR'}] Debug информация {'добавлена' if has_debug else 'НЕ добавлена'}")
else:
    print("[ERROR] Файл king_lear.html не создан")

# 3. Проверяем что в index.html ЕСТЬ review-section  
index_file = Path(r'F:\AiKlientBank\KingLearComic\output\index.html')
if index_file.exists():
    content = index_file.read_text(encoding='utf-8')
    
    has_review = 'review-section' in content or 'review-grid' in content
    print(f"[{'OK' if has_review else 'ERROR'}] Главная страница {'содержит' if has_review else 'НЕ содержит'} раздел повторения")
    
    has_manager = 'StudyManager' in content
    print(f"[{'OK' if has_manager else 'ERROR'}] StudyManager {'найден' if has_manager else 'НЕ найден'} на главной")
else:
    print("[ERROR] Файл index.html не создан")

# 4. Детальная проверка обработчика
if journey_file.exists():
    content = journey_file.read_text(encoding='utf-8')
    
    # Проверяем ключевые части нового обработчика
    checks = [
        ("DOMContentLoaded", "Обработчик в DOMContentLoaded"),
        ("liraJourney:studyWords", "Правильный STORAGE_KEY"),
        ("console.log('Word added to localStorage:'", "Логирование добавления слова"),
        ("characterId === 'king_lear'", "Проверка персонажа для эмодзи"),
        ("words.slice(-5)", "Ограничение 5 слов"),
    ]
    
    print("\n[!] Детальная проверка обработчика:")
    for check_str, desc in checks:
        if check_str in content:
            print(f"  [OK] {desc}")
        else:
            print(f"  [ERROR] НЕ найдено: {desc}")

print("\n[!] Тестирование завершено")
