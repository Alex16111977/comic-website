#!/usr/bin/env python
"""
ДЕТАЛЬНИЙ АНАЛІЗ ПРОБЛЕМ З ВИКОНАННЯМ ПРОМПТУ
"""
from pathlib import Path
import re

print("=" * 70)
print("ДЕТАЛЬНИЙ АНАЛІЗ: ЩО САМЕ ПІШЛО НЕ ТАК")
print("=" * 70)

# Перевірка mnemonics_gen.py
mnemo_file = Path(r"F:\AiKlientBank\KingLearComic\generators\mnemonics_gen.py")
print("\n🔍 АНАЛІЗ mnemonics_gen.py:")
print("-" * 60)

if mnemo_file.exists():
    with open(mnemo_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Знайти сигнатуру методу generate_articles_quiz
    quiz_method = re.search(r'def generate_articles_quiz\(self[^)]*\)', content)
    if quiz_method:
        print(f"Сигнатура методу: {quiz_method.group()}")
        if "phase_id" not in quiz_method.group():
            print("❌ ПРОБЛЕМА: phase_id параметр НЕ ДОДАНИЙ")
            print("   Метод не може отримати ID фази для вибору правильних слів")
    
    # Перевірка використання слів
    if "self.get_phase_vocabulary" in content:
        print("✅ Метод get_phase_vocabulary викликається")
    else:
        print("❌ ПРОБЛЕМА: get_phase_vocabulary НЕ використовується")
        print("   Замість слів з фази використовуються випадкові слова")
    
    # Перевірка CSS стилів
    css_section = re.search(r'def generate_css\(self\):(.*?)(?=def|\Z)', content, re.DOTALL)
    if css_section:
        css_content = css_section.group(1)
        if "linear-gradient" in css_content:
            print("✅ CSS містить градієнти")
        else:
            print("❌ ПРОБЛЕМА: CSS НЕ містить градієнтів для кольорової кодировки")
            print("   Картки не будуть мати кольорові фони")

# Перевірка html_lira.py
html_lira = Path(r"F:\AiKlientBank\KingLearComic\generators\html_lira.py")
print("\n🔍 АНАЛІЗ html_lira.py:")
print("-" * 60)

if html_lira.exists():
    with open(html_lira, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Перевірка передачі phase_id
    if "phase_id=first_phase_id" in content or "phase_id=" in content:
        print("✅ phase_id передається в generate_articles_quiz")
    else:
        print("❌ ПРОБЛЕМА: phase_id НЕ передається")
        print("   Вправа не знає, з якої фази брати слова")
    
    # Перевірка патчу
    if "exercises_pattern = " in content:
        print("✅ Патч для вставки вправи застосовано")
    else:
        print("❌ ПРОБЛЕМА: Патч НЕ застосовано")
    
    # Перевірка видалення старого коду
    if "if False:" in content:
        print("✅ Старий код вимкнено")
    else:
        print("❗ Старий код може все ще виконуватися")

# Перевірка результату в HTML
output_file = Path(r"F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html")
print("\n🔍 АНАЛІЗ ЗГЕНЕРОВАНОГО HTML:")
print("-" * 60)

if output_file.exists():
    with open(output_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Перевірка словника
    vocab_section = re.search(r'vocabulary-grid.*?</div>', html, re.DOTALL)
    if vocab_section:
        vocab_content = vocab_section.group()
        
        # Рахуємо картки
        vocab_cards = vocab_content.count('vocab-card')
        print(f"Знайдено карток словника: {vocab_cards}")
        
        # Перевірка кольорів
        has_colors = 'is-der' in vocab_content or 'is-die' in vocab_content
        if has_colors:
            print("✅ Картки мають кольорові класи")
        else:
            print("❌ ПРОБЛЕМА: Картки НЕ мають кольорових класів")
    
    # Перевірка вправи на артиклі
    articles_section = re.search(r'articles-quiz.*?</div>', html, re.DOTALL)
    if articles_section:
        articles_content = articles_section.group()
        
        # Перевірка слів у вправі
        wrong_words = ['Undankbarkeit', 'Kränkung', 'Fluch']
        has_wrong = any(word in articles_content for word in wrong_words)
        
        if has_wrong:
            print("❌ ПРОБЛЕМА: Вправа використовує НЕПРАВИЛЬНІ слова")
            found_wrong = [w for w in wrong_words if w in articles_content]
            print(f"   Знайдено випадкові слова: {found_wrong}")
        else:
            print("✅ Випадкові слова не знайдені")
    
    # Перевірка позиції
    vocab_pos = html.find('vocabulary-grid')
    exercises_pos = html.find('exercises-container')
    
    if vocab_pos > exercises_pos:
        print("❌ ПРОБЛЕМА: Словник розташовано ПІСЛЯ exercises")
        print(f"   Позиція словника: {vocab_pos}, exercises: {exercises_pos}")

print("\n" + "=" * 70)
print("📊 ВИСНОВОК:")
print("-" * 60)
print("""
ПРОМПТ НЕ БУВ ВИКОНАНИЙ ПОВНІСТЮ через:

1. КРОК 2 (mnemonics_gen.py):
   - phase_id НЕ додано до сигнатури методу
   - Метод не використовує слова з конкретної фази
   
2. КРОК 3 (html_lira.py):  
   - Патч застосовано ЧАСТКОВО
   - phase_id не передається правильно
   
3. КРОК 4 (CSS стилі):
   - Градієнти НЕ додані в CSS
   - Кольорова кодировка НЕ працює

4. РЕЗУЛЬТАТ:
   - Словник не переміщено наверх
   - Вправа використовує неправильні слова
   - Немає кольорової кодировки карток

ПРИЧИНА: Виконання промпту було ПЕРЕРВАНЕ на кроці 2-3,
тому зміни застосувалися лише ЧАСТКОВО.
""")
