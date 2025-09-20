"""
Тест: Проверка обновления упражнения "Подбор слов"
Дата: 2025-09-20
Мета: Проверяем что упражнение использует ВСЕ слова фазы
"""

import json
import re
from pathlib import Path

print("[TEST] Проверка обновленного упражнения 'Подбор слов'")
print("=" * 60)

# 1. Проверяем что в JS коде нет упоминаний synonymGroups для упражнения
js_file = Path(r"F:\AiKlientBank\KingLearComic\generators\js_lira.py")
with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Проверяем что используется wordMatchingGroups
if 'wordMatchingGroups' in js_content:
    print("[OK] Используется wordMatchingGroups вместо synonymGroups")
else:
    print("[WARN] wordMatchingGroups не найден в коде")

# Проверяем что нет старого кода с synonyms
if 'if (word.synonyms && word.synonyms.length > 0)' in js_content:
    print("[ERROR] Старый код проверки синонимов все еще присутствует!")
else:
    print("[OK] Старый код проверки синонимов удален")

# Проверяем новый код
if 'if (word.word && word.translation)' in js_content:
    print("[OK] Новый код использует ВСЕ слова с переводами")
else:
    print("[ERROR] Новый код не найден")

# 2. Проверяем шаблон HTML
template_file = Path(r"F:\AiKlientBank\KingLearComic\templates\journey.html")
with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

if '🔗 Подбор слов' in template_content:
    print("[OK] Название изменено на 'Подбор слов' в шаблоне")
elif '🤝 Синонимы' in template_content:
    print("[ERROR] Старое название 'Синонимы' все еще в шаблоне!")
else:
    print("[WARN] Название секции не найдено")

# 3. Проверяем сгенерированный HTML
output_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
if output_file.exists():
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()
    
    # Проверяем что используются правильные заголовки колонок
    if 'Немецкие' in output_content and 'Русские' in output_content:
        print("[OK] Колонки названы 'Немецкие' и 'Русские'")
    else:
        print("[WARN] Заголовки колонок не найдены в выводе")
    
    # Проверяем что есть упражнение подбора
    if 'buildPairMatchingActivity' in output_content:
        print("[OK] Функция создания упражнения подбора присутствует")
    
    # Проверяем что используются все слова фазы
    if 'phase.words.forEach((word, wordIdx)' in output_content:
        print("[OK] Используются ВСЕ слова текущей фазы")
else:
    print("[ERROR] Файл king_lear.html не найден в output")

# 4. Проверяем что поле synonyms больше не собирается для словаря
if "'synonyms': synonyms," in js_content:
    print("[ERROR] Поле synonyms все еще добавляется в словарь!")
else:
    print("[OK] Поле synonyms удалено из словаря")

print("\n" + "=" * 60)
print("[SUMMARY] Тестирование завершено")
print("\nИзменения:")
print("1. Упражнение 'Синонимы' -> 'Подбор слов'")
print("2. Используются ВСЕ слова фазы (не только с синонимами)")
print("3. Колонки: 'Немецкие' и 'Русские'") 
print("4. Русские переводы включают подсказки в скобках")
print("5. Поле synonyms больше не используется для упражнения")
