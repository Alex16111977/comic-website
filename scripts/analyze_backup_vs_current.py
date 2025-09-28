#!/usr/bin/env python
"""
АНАЛІЗ: Порівняння backup_mnemo з поточним html_lira.py
"""
from pathlib import Path
import difflib

print("=" * 70)
print("ПОРІВНЯННЯ: html_lira.py.backup_mnemo VS html_lira.py")
print("=" * 70)

backup_file = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py.backup_mnemo")
current_file = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py")

if not backup_file.exists():
    print("❌ Backup файл не знайдено!")
    exit(1)

if not current_file.exists():
    print("❌ Поточний файл не знайдено!")
    exit(1)

# Читаємо файли
with open(backup_file, 'r', encoding='utf-8') as f:
    backup_content = f.read()

with open(current_file, 'r', encoding='utf-8') as f:
    current_content = f.read()

print(f"\n📊 СТАТИСТИКА:")
print(f"Backup розмір: {len(backup_content)} символів")
print(f"Поточний розмір: {len(current_content)} символів")
print(f"Різниця: {len(current_content) - len(backup_content)} символів")

# Ключові перевірки
print("\n🔍 КЛЮЧОВІ ЕЛЕМЕНТИ В BACKUP:")
print("-" * 60)

key_elements = {
    "Вставка мнемотехніки після exercises": "# Вставляємо HTML секції мнемотехніки" in backup_content,
    "Пошук exercises-container": "'exercises-container' in html" in backup_content,
    "Пошук bottom-nav": "'bottom-nav' in html" in backup_content,
    "Вставка між exercises та nav": "html[:exercises_pos]" in backup_content,
    "mnemo_vocabulary вставка": "mnemo_vocabulary" in backup_content,
    "mnemo_quiz вставка": "mnemo_quiz" in backup_content,
    "Генерація мнемотехніки": "self.mnemo_gen.generate_" in backup_content
}

for element, exists in key_elements.items():
    print(f"  {'✅' if exists else '❌'} {element}")

print("\n🔍 КЛЮЧОВІ ЕЛЕМЕНТИ В ПОТОЧНОМУ:")
print("-" * 60)

key_elements_current = {
    "exercises_pattern визначено": "exercises_pattern = " in current_content,
    "Вставка articles_quiz": "{articles_quiz}" in current_content,
    "generate_vocabulary_cards метод": "def generate_vocabulary_cards" in current_content,
    "Старий код вимкнено (if False)": "if False:" in current_content,
    "Видалений старий блок": "# СТАРИЙ КОД ВИМКНЕНО" in current_content
}

for element, exists in key_elements_current.items():
    print(f"  {'✅' if exists else '❌'} {element}")

# Знайдемо критичні відмінності
print("\n🔴 КРИТИЧНІ ВІДМІННОСТІ:")
print("-" * 60)

# Перевірка методу generate_journey
import re

# В backup
backup_journey = re.search(r'def generate_journey\(self.*?\n(?=    def|\Z)', backup_content, re.DOTALL)
# В current  
current_journey = re.search(r'def generate_journey\(self.*?\n(?=    def|\Z)', current_content, re.DOTALL)

if backup_journey and current_journey:
    backup_lines = backup_journey.group().count('\n')
    current_lines = current_journey.group().count('\n')
    
    print(f"Метод generate_journey:")
    print(f"  Backup: {backup_lines} рядків")
    print(f"  Current: {current_lines} рядків")
    print(f"  Різниця: {current_lines - backup_lines} рядків")
    
    # Що втрачено з backup
    if "exercises_pos = html.find('exercises-container')" in backup_journey.group():
        print("\n✅ BACKUP МАЄ: Пошук позиції exercises-container")
    
    if "html[:exercises_pos]" in backup_journey.group():
        print("✅ BACKUP МАЄ: Вставку мнемотехніки в правильну позицію")
    
    # Що додано в current
    if "exercises_pattern = " in current_journey.group():
        print("\n❌ CURRENT ЗАМІНИВ: Простий пошук на pattern matching")
    
    if "if exercises_pattern in html:" in current_journey.group():
        print("❌ CURRENT ПРОБЛЕМА: Перевірка pattern, але не позиції")

print("\n" + "=" * 70)
print("📊 ВИСНОВОК:")
print("-" * 60)
print("""
ПРОБЛЕМА НА КРОЦІ 5:

В BACKUP (backup_mnemo) була ПРАВИЛЬНА логіка:
1. Знаходила позицію exercises-container
2. Вставляла мнемотехніку ПІСЛЯ exercises перед bottom-nav
3. Використовувала позиційну вставку через html[:pos]

В CURRENT (після кроку 5) логіка ЗЛАМАНА:
1. Використовує pattern matching замість позицій
2. Видалено критичний код позиційної вставки
3. Додано новий код, який не працює правильно

РІШЕННЯ: Потрібно ВІДНОВИТИ код з backup_mnemo
з правильною позиційною вставкою мнемотехніки!
""")

# Покажемо критичний код з backup
print("\n🔧 КРИТИЧНИЙ КОД З BACKUP, ЯКИЙ ПОТРІБНО ВІДНОВИТИ:")
print("-" * 60)

critical_section = re.search(
    r'# Вставляємо HTML секції мнемотехніки.*?else:\s+print\(f"\[ERROR\]',
    backup_content,
    re.DOTALL
)

if critical_section:
    print("```python")
    print(critical_section.group()[:500], "...")
    print("```")
