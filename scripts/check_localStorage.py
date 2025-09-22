#!/usr/bin/env python3
"""Проверка константы REVIEW_QUEUE_KEY в journey_runtime.js"""

import re
from pathlib import Path

# Путь к файлу
js_file = Path(__file__).parent.parent / 'static' / 'js' / 'journey_runtime.js'

if not js_file.exists():
    print(f"[ERROR] Файл не найден: {js_file}")
    exit(1)

# Читаем файл
content = js_file.read_text(encoding='utf-8')

print("[INFO] Проверка localStorage в journey_runtime.js")
print("-" * 50)

# Проверяем REVIEW_QUEUE_KEY
if 'REVIEW_QUEUE_KEY' in content:
    print("[!] REVIEW_QUEUE_KEY найден в коде")
    
    # Проверяем определение константы
    const_match = re.search(r'const\s+REVIEW_QUEUE_KEY\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    let_match = re.search(r'let\s+REVIEW_QUEUE_KEY\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    var_match = re.search(r'var\s+REVIEW_QUEUE_KEY\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    
    if const_match:
        print(f"[OK] const REVIEW_QUEUE_KEY = '{const_match.group(1)}'")
    elif let_match:
        print(f"[OK] let REVIEW_QUEUE_KEY = '{let_match.group(1)}'")
    elif var_match:
        print(f"[OK] var REVIEW_QUEUE_KEY = '{var_match.group(1)}'")
    else:
        print("[ERROR] REVIEW_QUEUE_KEY используется, но НЕ определена!")
        print("[!] ЭТО КРИТИЧЕСКАЯ ОШИБКА!")
        print("[!] localStorage не будет работать на Android/iOS")
        
        # Подсчитаем использования
        count = content.count('REVIEW_QUEUE_KEY')
        print(f"[INFO] Используется {count} раз в коде")
        
        # Покажем где используется
        lines = content.split('\n')
        uses = []
        for i, line in enumerate(lines, 1):
            if 'REVIEW_QUEUE_KEY' in line:
                uses.append(f"  Строка {i}: {line.strip()[:80]}...")
        
        if uses:
            print("\n[INFO] Места использования:")
            for use in uses[:5]:
                print(use)
else:
    print("[ERROR] REVIEW_QUEUE_KEY вообще не найден в файле")

# Проверяем другие константы
print("\n[INFO] Проверка других констант localStorage:")
print("-" * 50)

# Ищем все localStorage операции
operations = re.findall(r'localStorage\.(getItem|setItem|removeItem)\(([^)]+)\)', content)
if operations:
    print(f"[INFO] Найдено {len(operations)} операций с localStorage")
    
    # Извлекаем уникальные ключи
    keys = set()
    for op, params in operations:
        # Пытаемся извлечь ключ
        key_match = re.match(r"['\"]([^'\"]+)['\"]", params.strip())
        if key_match:
            keys.add(key_match.group(1))
        else:
            # Возможно, это переменная
            var_match = re.match(r'(\w+)', params.strip())
            if var_match:
                keys.add(f"{{переменная: {var_match.group(1)}}}")
    
    print(f"[INFO] Уникальные ключи/переменные:")
    for key in sorted(keys):
        print(f"  - {key}")

# Проверяем определения констант в начале файла
print("\n[INFO] Константы в начале файла (первые 50 строк):")
print("-" * 50)

lines = content.split('\n')[:50]
for i, line in enumerate(lines, 1):
    if re.match(r'^\s*(const|let|var)\s+\w+\s*=', line):
        print(f"  Строка {i}: {line.strip()[:100]}")

print("\n[РЕЗУЛЬТАТ]")
print("-" * 50)
if 'REVIEW_QUEUE_KEY' in content and not (const_match or let_match or var_match):
    print("[CRITICAL] Необходимо добавить определение константы REVIEW_QUEUE_KEY!")
    print("[FIX] Добавьте в начало файла:")
    print("  const REVIEW_QUEUE_KEY = 'kinglear_review_queue';")
else:
    print("[OK] Проверка завершена")
