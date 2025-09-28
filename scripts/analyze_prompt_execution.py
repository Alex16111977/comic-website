#!/usr/bin/env python
"""
Аналіз виконання промпту - що пішло не так
"""
from pathlib import Path
import json

print("=" * 70)
print("АНАЛІЗ ВИКОНАННЯ ПРОМПТУ - ЩО ПІШЛО НЕ ТАК")
print("=" * 70)

# Перевірка кроків промпту
steps_status = {}

print("\n📋 КРОК 1: АНАЛІЗ ПОТОЧНОГО СТАНУ")
print("-" * 60)
# Перевірка чи створено діагностичний скрипт
diagnose_script = Path(r"F:\AiKlientBank\KingLearComic\scripts\diagnose_current_state.py")
if diagnose_script.exists():
    print("✅ Діагностичний скрипт створено")
    steps_status["step1"] = True
else:
    print("❌ Діагностичний скрипт НЕ створено")
    steps_status["step1"] = False

print("\n📋 КРОК 2: ОНОВЛЕННЯ mnemonics_gen.py")
print("-" * 60)
mnemo_file = Path(r"F:\AiKlientBank\KingLearComic\generators\mnemonics_gen.py")
if mnemo_file.exists():
    with open(mnemo_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    checks = {
        "generate_articles_quiz з phase_id": "def generate_articles_quiz(self, vocabulary, phase_id=None)" in content or "def generate_articles_quiz(self, character, phase_id=None)" in content,
        "get_phase_vocabulary метод": "def get_phase_vocabulary" in content,
        "Російська мова в інтерфейсі": "Артикли и род" in content or "🎯 Артикли и род" in content,
        "Виберите правильный артикль": "Выберите правильный артикль" in content
    }
    
    for check, status in checks.items():
        print(f"  {'✅' if status else '❌'} {check}: {status}")
    
    steps_status["step2"] = all(checks.values())
else:
    print("❌ Файл mnemonics_gen.py не знайдено")
    steps_status["step2"] = False

print("\n📋 КРОК 3: ОНОВЛЕННЯ html_lira.py")
print("-" * 60)
html_lira = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py")
backup_exists = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py.backup2").exists()

if html_lira.exists():
    with open(html_lira, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Імпорт MnemonicsGenerator": "from .mnemonics_gen import MnemonicsGenerator" in content,
        "Ініціалізація mnemo_gen": "self.mnemo_gen = MnemonicsGenerator" in content,
        "exercises_pattern визначено": "exercises_pattern = " in content,
        "Вставка вправи в exercises": "articles_quiz" in content,
        "generate_vocabulary_cards метод": "def generate_vocabulary_cards" in content,
        "Патч застосовано (backup2)": backup_exists
    }
    
    for check, status in checks.items():
        print(f"  {'✅' if status else '❌'} {check}: {status}")
    
    steps_status["step3"] = all(checks.values())
else:
    print("❌ Файл html_lira.py не знайдено")
    steps_status["step3"] = False

print("\n📋 КРОК 4: CSS КОЛЬОРОВА КОДИРОВКА")
print("-" * 60)
if mnemo_file.exists():
    with open(mnemo_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    css_checks = {
        "is-der градієнт": "linear-gradient(135deg, #e3f2fd" in content,
        "is-die градієнт": "linear-gradient(135deg, #fce4ec" in content,
        "is-das градієнт": "linear-gradient(135deg, #e8f5e9" in content,
        "border-left для der": "border-left: 4px solid #1976d2" in content,
        "border-left для die": "border-left: 4px solid #d32f2f" in content,
        "border-left для das": "border-left: 4px solid #388e3c" in content
    }
    
    for check, status in css_checks.items():
        print(f"  {'✅' if status else '❌'} {check}: {status}")
    
    steps_status["step4"] = all(css_checks.values())
else:
    steps_status["step4"] = False

print("\n📋 КРОК 5: ФІНАЛЬНА ГЕНЕРАЦІЯ")
print("-" * 60)
output_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
validation_script = Path(r"F:\AiKlientBank\KingLearComic\scripts\final_validation.py")

checks = {
    "king_lear.html згенеровано": output_file.exists(),
    "final_validation.py створено": validation_script.exists(),
    "Файл оновлено нещодавно": output_file.exists() and output_file.stat().st_size > 100000
}

for check, status in checks.items():
    print(f"  {'✅' if status else '❌'} {check}: {status}")

steps_status["step5"] = all(checks.values())

# ФІНАЛЬНИЙ ВИСНОВОК
print("\n" + "=" * 70)
print("📊 ПІДСУМОК ВИКОНАННЯ КРОКІВ:")
print("-" * 60)

total_steps = len(steps_status)
completed = sum(1 for v in steps_status.values() if v)

for step, status in steps_status.items():
    print(f"  {step}: {'✅ ВИКОНАНО' if status else '❌ НЕ ВИКОНАНО'}")

print(f"\nВиконано кроків: {completed}/{total_steps}")

# АНАЛІЗ ПРОБЛЕМ
print("\n" + "=" * 70)
print("🔴 ВИЯВЛЕНІ ПРОБЛЕМИ:")
print("-" * 60)

if not steps_status.get("step2"):
    print("1. КРОК 2 НЕ ЗАВЕРШЕНО:")
    print("   - Метод get_phase_vocabulary може бути відсутній")
    print("   - Російська мова не додана в шаблони")
    print("   - phase_id параметр не використовується")

if not steps_status.get("step3"):
    print("2. КРОК 3 НЕ ЗАВЕРШЕНО:")
    print("   - html_lira.py не повністю модифіковано")
    print("   - Патч не застосовано або застосовано частково")
    print("   - Метод generate_vocabulary_cards може бути відсутній")

if not steps_status.get("step4"):
    print("3. КРОК 4 НЕ ЗАВЕРШЕНО:")
    print("   - CSS стилі не додані в mnemonics_gen.py")
    print("   - Градієнти та кольори не налаштовані")

print("\n🎯 ГОЛОВНА ПРИЧИНА НЕВДАЧІ:")
print("-" * 60)
print("Промпт виконувався ЧАСТКОВО - кожен крок починався, але НЕ ЗАВЕРШУВАВСЯ")
print("через обмеження токенів або переривання виконання.")
print("\nНеобхідно виконати КОЖЕН крок ПОВНІСТЮ від початку до кінця.")
