"""
Детальная проверка russianHint в runtime
"""
import re

source_file = r'F:\AiKlientBank\KingLearComic\static\js\journey_runtime.js'

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем все места где должен быть russianHint
checks = {
    "buildPhaseQuizWords с russianHint": r"russianHint:\s*word\.russian_hint",
    "generateForwardQuestion с if": r"if\s*\(word\.russianHint\)",
    "generateForwardQuestion questionText": r"word\.russianHint\)\?",
    "renderQuestion с if": r"if\s*\(question\.russianHint\)",
}

print("[INFO] Проверка наличия russianHint в ключевых местах:")
print("=" * 60)

all_found = True
for name, pattern in checks.items():
    if re.search(pattern, content):
        print(f"[OK] {name}")
    else:
        print(f"[ERROR] {name} - НЕ НАЙДЕНО!")
        all_found = False

# Проверим функцию buildPhaseQuizWords
func_pattern = r'function buildPhaseQuizWords\(phase\)\s*{([^}]+(?:{[^}]*}[^}]*)*)?}'
match = re.search(func_pattern, content, re.DOTALL)

if match:
    func_body = match.group(0)
    print("\n[INFO] Содержимое buildPhaseQuizWords:")
    # Показать только часть с return
    lines = func_body.split('\n')
    for i, line in enumerate(lines):
        if 'return' in line:
            # Показать несколько строк вокруг return
            start = max(0, i - 2)
            end = min(len(lines), i + 8)
            print("    ...")
            for j in range(start, end):
                print(f"    {lines[j]}")
            print("    ...")
            break

if all_found:
    print("\n[OK] Все проверки пройдены! russianHint полностью интегрирован.")
else:
    print("\n[ERROR] Некоторые проверки не пройдены. Нужно обновить файл.")
