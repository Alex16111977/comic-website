"""
Проверка версии buildPhaseQuizWords в HTML
"""

import re
from pathlib import Path

html_path = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найти функцию buildPhaseQuizWords
pattern = r'function buildPhaseQuizWords\(phase\)\s*{([^}]+(?:{[^}]*}[^}]*)*)}' 
match = re.search(pattern, content)

if match:
    func_body = match.group(0)
    print("[FOUND] buildPhaseQuizWords function:")
    print(func_body)
    
    # Проверить есть ли russianHint в функции
    if 'russianHint' in func_body:
        print("\n[OK] russianHint НАЙДЕН в функции!")
    else:
        print("\n[ERROR] russianHint НЕ НАЙДЕН в функции!")
else:
    print("[ERROR] Функция buildPhaseQuizWords не найдена")

# Также проверим generateForwardQuestion
pattern2 = r'generateForwardQuestion\(word\)\s*{([^}]+(?:{[^}]*}[^}]*)*)}' 
match2 = re.search(pattern2, content)

if match2:
    func2_body = match2.group(0)
    if 'russianHint' in func2_body:
        print("\n[OK] russianHint найден в generateForwardQuestion!")
    else:
        print("\n[ERROR] russianHint НЕ найден в generateForwardQuestion!")
