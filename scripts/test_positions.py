#!/usr/bin/env python
"""Тест правильного розташування"""
import subprocess
result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

from pathlib import Path
html_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

theatrical_pos = html.find('theatrical-scene')
vocab_pos = html.find('vocabulary-grid')
exercises_pos = html.find('exercises-container')
nav_pos = html.find('bottom-nav')

print(f"Позиції: theatrical={theatrical_pos}, vocab={vocab_pos}, exercises={exercises_pos}, nav={nav_pos}")

if theatrical_pos < vocab_pos < exercises_pos < nav_pos:
    print("[SUCCESS] Розташування правильне!")
else:
    print("[FAIL] Розташування неправильне!")
    exit(1)
