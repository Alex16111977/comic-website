"""
Проверка и обновление runtime файлов
"""

source_file = r'F:\AiKlientBank\KingLearComic\static\js\journey_runtime.js'
output_file = r'F:\AiKlientBank\KingLearComic\output\static\js\journey_runtime.js'

# Читаем оба файла
with open(source_file, 'r', encoding='utf-8') as f:
    source_content = f.read()

with open(output_file, 'r', encoding='utf-8') as f:
    output_content = f.read()

print("[INFO] Анализ файлов...")
print("=" * 60)

# Проверяем наличие russianHint
source_has_hint = 'russianHint' in source_content
output_has_hint = 'russianHint' in output_content

print(f"static/js/journey_runtime.js:")
print(f"  - Размер: {len(source_content)} символов")
print(f"  - russianHint: {'НАЙДЕН' if source_has_hint else 'НЕ НАЙДЕН'}")
if source_has_hint:
    print(f"  - Вхождений: {source_content.count('russianHint')}")

print(f"\noutput/static/js/journey_runtime.js:")
print(f"  - Размер: {len(output_content)} символов")
print(f"  - russianHint: {'НАЙДЕН' if output_has_hint else 'НЕ НАЙДЕН'}")
if output_has_hint:
    print(f"  - Вхождений: {output_content.count('russianHint')}")

# Если в output есть, а в source нет - копируем
if output_has_hint and not source_has_hint:
    print("\n[ACTION] Копирование обновленного файла из output в static...")
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    print("[OK] Файл скопирован!")
    print("[OK] Теперь нужно перегенерировать сайт!")
elif source_has_hint:
    print("\n[OK] Исходный файл уже содержит russianHint")
else:
    print("\n[ERROR] russianHint не найден ни в одном файле!")
