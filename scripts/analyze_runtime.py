"""
Скрипт интеграции упражнений в runtime
Дата: 14.09.2025
"""
import sys
from pathlib import Path

# Путь к runtime файлу
runtime_path = Path(r'F:\AiKlientBank\KingLearComic\static\js\journey_runtime.js')

# Читаем содержимое
with open(runtime_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("[АНАЛИЗ JOURNEY_RUNTIME.JS]")
print("=" * 50)

# 1. Проверяем наличие ключевых переменных
checks = [
    ('phaseVocabularies', 'Глобальная переменная с данными фаз'),
    ('currentPhaseIndex', 'Индекс текущей фазы'),
    ('phaseKeys', 'Массив ключей фаз'),
    ('relations-container', 'Контейнер для упражнений'),
    ('word-families-section', 'Секция семьи слов'),
    ('collocations-section', 'Секция коллокаций')
]

for check, desc in checks:
    if check in content:
        print(f"  [OK] {check}: {desc}")
    else:
        print(f"  [!] {check}: НЕ НАЙДЕНО - {desc}")

print("\n[МЕСТА ДЛЯ ИНТЕГРАЦИИ]")
print("=" * 50)

# 2. Ищем функции смены фаз
lines = content.split('\n')
integration_points = []

for i, line in enumerate(lines):
    # Ищем места где происходит смена фазы
    if 'currentPhaseIndex' in line and '=' in line:
        integration_points.append({
            'line': i + 1,
            'content': line.strip()[:80],
            'type': 'phase_change'
        })
    
    # Ищем инициализацию страницы
    if 'DOMContentLoaded' in line or 'window.onload' in line:
        integration_points.append({
            'line': i + 1,
            'content': line.strip()[:80],
            'type': 'page_init'
        })
    
    # Ищем обработку relations
    if 'relation-toggle' in line or 'relations-container' in line:
        integration_points.append({
            'line': i + 1,
            'content': line.strip()[:80],
            'type': 'relations_handler'
        })

print(f"Найдено {len(integration_points)} точек интеграции:\n")
for point in integration_points[:10]:
    print(f"  Строка {point['line']} ({point['type']}):")
    print(f"    {point['content']}")

print("\n[РЕКОМЕНДАЦИИ ПО ИНТЕГРАЦИИ]")
print("=" * 50)
print("""
1. В начало файла добавить загрузку exercises.js:
   - Либо через <script> тег в HTML
   - Либо через динамический import

2. После каждой смены фазы вызывать:
   if (window.initializeExercises) {
       const phaseKey = phaseKeys[currentPhaseIndex];
       window.initializeExercises(phaseKey);
   }

3. При инициализации страницы вызвать для первой фазы:
   if (window.initializeExercises && phaseKeys.length > 0) {
       window.initializeExercises(phaseKeys[0]);
   }

4. Убедиться что exercises.css подключен в HTML
""")

# Сохраняем места для патчинга
patch_file = Path(r'F:\AiKlientBank\KingLearComic\scripts\integration_points.txt')
with open(patch_file, 'w', encoding='utf-8') as f:
    f.write("INTEGRATION POINTS FOR EXERCISES\n")
    f.write("=" * 50 + "\n\n")
    for point in integration_points:
        f.write(f"Line {point['line']} ({point['type']}):\n")
        f.write(f"  {point['content']}\n\n")

print(f"\n[OK] Точки интеграции сохранены в {patch_file.name}")
