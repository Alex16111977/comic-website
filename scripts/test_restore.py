#!/usr/bin/env python
"""Тест відновлення з backup"""
from pathlib import Path

html_lira = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py")
with open(html_lira, 'r', encoding='utf-8') as f:
    content = f.read()

# Перевірка критичного коду з backup
checks = {
    "exercises_pos пошук": "exercises_pos = html.find('exercises-container')" in content,
    "Патерн для nav": "pattern = r'(</div>" in content,
    "Позиційна вставка": "html[:insert_pos]" in content,
    "mnemo_vocabulary": "mnemo_vocabulary" in content,
    "mnemo_quiz": "mnemo_quiz" in content
}

for check, status in checks.items():
    print(f"  {'[OK]' if status else '[ERROR]'} {check}")

if all(checks.values()):
    print("[SUCCESS] Backup відновлено!")
else:
    print("[FAIL] Backup НЕ відновлено правильно!")
    exit(1)
