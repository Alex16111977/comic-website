#!/usr/bin/env python
"""Швидка перевірка змін"""
from pathlib import Path

print("ГЕНЕРАЦІЯ...")
import subprocess
import sys

result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)
print(f"Код завершення: {result.returncode}")

html_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
if html_file.exists():
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print("\nПЕРЕВІРКА:")
    
    # Нові градієнти
    if "linear-gradient(135deg, #e3f2fd, #bbdefb)" in html:
        print("[OK] Новий градієнт der")
    else:
        print("[FAIL] Старий градієнт der")
    
    # Російська мова
    if "Артикли и род" in html:
        print("[OK] Російська мова")
    else:
        print("[FAIL] Українська мова")
        
    # Позиції
    vocab_pos = html.find('vocabulary-section')
    articles_pos = html.find('articles-quiz')
    print(f"Позиції: vocab={vocab_pos}, articles={articles_pos}")
