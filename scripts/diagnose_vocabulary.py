#!/usr/bin/env python3
"""
Диагностика проблемы со словарем на Android/iOS
Дата: 14.09.2025
"""

import json
from pathlib import Path
import re

print("[INFO] Диагностика проблемы словаря на Android/iOS")
print("=" * 60)

# 1. Проверка константы в journey_runtime.js
print("\n[1] Проверка journey_runtime.js")
print("-" * 40)

js_runtime = Path(__file__).parent.parent / 'static' / 'js' / 'journey_runtime.js'
if js_runtime.exists():
    content = js_runtime.read_text(encoding='utf-8')
    
    # Ищем определение константы
    const_match = re.search(r"const\s+REVIEW_QUEUE_KEY\s*=\s*['\"]([^'\"]+)['\"]", content)
    if const_match:
        journey_key = const_match.group(1)
        print(f"[OK] REVIEW_QUEUE_KEY = '{journey_key}'")
    else:
        print("[ERROR] REVIEW_QUEUE_KEY не определена!")
        journey_key = None
else:
    print(f"[ERROR] Файл не найден: {js_runtime}")
    journey_key = None

# 2. Проверка index.html
print("\n[2] Проверка главной страницы (index.html)")
print("-" * 40)

index_template = Path(__file__).parent.parent / 'templates' / 'index.html'
if index_template.exists():
    content = index_template.read_text(encoding='utf-8')
    
    # Ищем ключ в ReviewManager
    storage_match = re.search(r"STORAGE_KEY:\s*['\"]([^'\"]+)['\"]", content)
    if storage_match:
        index_key = storage_match.group(1)
        print(f"[OK] ReviewManager.STORAGE_KEY = '{index_key}'")
    else:
        print("[ERROR] ReviewManager.STORAGE_KEY не найден!")
        index_key = None
else:
    print(f"[ERROR] Файл не найден: {index_template}")
    index_key = None

# 3. Сравнение ключей
print("\n[3] Проверка синхронизации")
print("-" * 40)

if journey_key and index_key:
    if journey_key == index_key:
        print(f"[OK] Ключи синхронизированы: '{journey_key}'")
    else:
        print(f"[ERROR] РАССИНХРОНИЗАЦИЯ КЛЮЧЕЙ!")
        print(f"  journey_runtime.js: '{journey_key}'")
        print(f"  index.html:         '{index_key}'")
        print(f"[!] ЭТО ПРИЧИНА ПРОБЛЕМЫ на Android/iOS!")
elif not journey_key:
    print("[ERROR] Ключ не определен в journey_runtime.js")
elif not index_key:
    print("[ERROR] Ключ не определен в index.html")

# 4. Проверка структуры данных
print("\n[4] Проверка структуры данных словаря")
print("-" * 40)

# Проверяем, какие поля используются для слов
if journey_key:
    # В journey_runtime.js проверяем структуру
    fields_in_journey = []
    
    # Поля для создания записи
    create_fields = re.findall(r'sanitized\.(\w+)\s*=', content[:20000])
    if create_fields:
        fields_in_journey = list(set(create_fields))
        print("[OK] Поля в journey_runtime.js:")
        for field in sorted(fields_in_journey)[:10]:
            print(f"  - {field}")

if index_key and index_template.exists():
    # В index.html проверяем используемые поля
    index_content = index_template.read_text(encoding='utf-8')
    
    # Ищем обращения к полям word.*
    word_fields = re.findall(r'word\.(\w+)', index_content)
    if word_fields:
        unique_fields = list(set(word_fields))
        print("\n[OK] Поля используемые в index.html:")
        for field in sorted(unique_fields)[:10]:
            print(f"  - word.{field}")

# 5. Проверка обработки событий
print("\n[5] Проверка обработки событий")
print("-" * 40)

# Проверяем addEventListener для storage событий
if journey_key and js_runtime.exists():
    js_content = js_runtime.read_text(encoding='utf-8')
    
    if "addEventListener('storage'" in js_content or 'addEventListener("storage"' in js_content:
        print("[OK] journey_runtime.js слушает события storage")
    else:
        print("[WARNING] journey_runtime.js НЕ слушает события storage")
        
if index_key and index_template.exists():
    if "addEventListener('storage'" in index_content or 'addEventListener("storage"' in index_content:
        print("[OK] index.html слушает события storage")
    else:
        print("[WARNING] index.html НЕ слушает события storage")

# 6. Генерация отчета
print("\n[ОТЧЕТ]")
print("=" * 60)

if journey_key and index_key and journey_key == index_key:
    print("[OK] Система словаря настроена правильно")
    print(f"[OK] Единый ключ localStorage: '{journey_key}'")
    print("\n[INFO] Возможные причины проблемы на Android/iOS:")
    print("  1. Браузер блокирует localStorage в режиме инкогнито")
    print("  2. Превышен лимит localStorage (5-10 MB)")
    print("  3. Приложение не имеет прав на localStorage")
    print("  4. WebView настройки блокируют localStorage")
    print("\n[РЕКОМЕНДАЦИИ]:")
    print("  - Проверьте настройки WebView в приложении")
    print("  - Убедитесь что localStorage включен в браузере")
    print("  - Проверьте консоль браузера на ошибки")
else:
    print("[ERROR] КРИТИЧЕСКАЯ ПРОБЛЕМА КОНФИГУРАЦИИ!")
    if journey_key != index_key:
        print("[!] Ключи localStorage не синхронизированы")
        print(f"[!] journey_runtime.js использует: '{journey_key}'")
        print(f"[!] index.html использует: '{index_key}'")
        print("\n[РЕШЕНИЕ]:")
        print(f"  1. Установите одинаковый ключ в обоих файлах")
        print(f"  2. Рекомендуемый ключ: 'liraJourney:reviewQueue'")
        print(f"  3. Очистите localStorage после исправления")

# 7. Проверка мобильной совместимости
print("\n[6] Проверка мобильной совместимости")
print("-" * 40)

# Проверяем viewport meta tag
if index_template.exists():
    if '<meta name="viewport"' in index_content:
        print("[OK] Viewport meta tag присутствует")
    else:
        print("[WARNING] Viewport meta tag отсутствует")
        
    # Проверяем touch события
    if 'touchstart' in index_content or 'touchend' in index_content:
        print("[OK] Touch события обрабатываются")
    else:
        print("[INFO] Touch события не используются (может быть OK)")

print("\n[ГОТОВО] Диагностика завершена")
