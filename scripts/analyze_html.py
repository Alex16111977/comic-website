#!/usr/bin/env python
"""Детальний аналіз king_lear.html"""
from pathlib import Path

# Читаємо HTML
html_file = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("=" * 60)
print("ДЕТАЛЬНИЙ АНАЛІЗ KING_LEAR.HTML")
print("=" * 60)
print(f"\nРозмір файлу: {len(html)} символів")

# Шукаємо всі ключові блоки
blocks = {
    'theatrical-scene START': html.find('<div class="theatrical-scene'),
    'theatrical-scene END': html.find('</div><!-- end theatrical-scene -->'),
    'vocabulary-section': html.find('<section class="vocabulary-section">'),
    'exercises-container START': html.find('<div class="exercises-container">'),
    'exercises-container END': html.find('</div><!-- end exercises-container -->'),
    'articles-quiz': html.find('<section class="articles-quiz"'),
    'bottom-nav': html.find('<nav class="bottom-nav">')
}

print("\n=== ПОЗИЦІЇ БЛОКІВ ===")
for name, pos in blocks.items():
    if pos == -1:
        print(f"{name}: НЕ ЗНАЙДЕНО ❌")
    else:
        print(f"{name}: {pos}")

# ПРОБЛЕМА 1: РОЗТАШУВАННЯ
print("\n=== ПРОБЛЕМА 1: РОЗТАШУВАННЯ ===")
vocab_pos = blocks['vocabulary-section']
theatrical_end = blocks['theatrical-scene END']
exercises_start = blocks['exercises-container START']
exercises_end = blocks['exercises-container END']
quiz_pos = blocks['articles-quiz']
nav_pos = blocks['bottom-nav']

if vocab_pos == -1:
    print("❌ КРИТИЧНА ПОМИЛКА: vocabulary-section НЕ ІСНУЄ!")
    print("   Словник НЕ БУВ ВСТАВЛЕНИЙ взагалі")
else:
    if theatrical_end > 0 and vocab_pos > theatrical_end:
        print("✅ Словник ПІСЛЯ theatrical-scene")
    else:
        print("❌ Словник НЕ після theatrical-scene")
    
    if vocab_pos < exercises_start:
        print("✅ Словник ПЕРЕД exercises-container")
    else:
        print("❌ Словник НЕ перед exercises-container")

if quiz_pos == -1:
    print("❌ КРИТИЧНА ПОМИЛКА: articles-quiz НЕ ІСНУЄ!")
    print("   Вправа НЕ БУЛА ВСТАВЛЕНА взагалі")
else:
    if quiz_pos > exercises_start:
        print("✅ Вправа ПІСЛЯ початку exercises-container")
        
        if exercises_end > 0 and quiz_pos < exercises_end:
            print("✅✅ ВІДМІННО! Вправа ВСЕРЕДИНІ exercises-container!")
        elif exercises_end == -1:
            print("⚠️ Немає коментаря end exercises-container")
            # Альтернативна перевірка
            if quiz_pos < nav_pos:
                print("✅ Вправа перед bottom-nav (прийнятно)")
        else:
            print("❌ Вправа ПОЗА exercises-container")
    else:
        print("❌ Вправа НЕ після exercises-container")

# ПРОБЛЕМА 2: МОВА
print("\n=== ПРОБЛЕМА 2: МОВА ІНТЕРФЕЙСУ ===")
ru_checks = {
    "Артикли и род": html.find("Артикли и род") > 0,
    "Выберите правильный артикль": html.find("Выберите правильный артикль") > 0,
    "мужской": html.find("мужской") > 0,
    "женский": html.find("женский") > 0,
    "средний": html.find("средний") > 0,
    "Словарь урока": html.find("Словарь урока") > 0
}

for text, found in ru_checks.items():
    print(f"{'✅' if found else '❌'} '{text}' - {'знайдено' if found else 'НЕ знайдено'}")

# ПРОБЛЕМА 3: КОЛЬОРИ
print("\n=== ПРОБЛЕМА 3: КОЛЬОРОВА КОДИРОВКА ===")
color_checks = {
    "Градієнт der": "linear-gradient(135deg, #e3f2fd, #bbdefb)" in html,
    "Градієнт die": "linear-gradient(135deg, #fce4ec, #f8bbd0)" in html,
    "Градієнт das": "linear-gradient(135deg, #e8f5e9, #c8e6c9)" in html,
    "Клас is-der": "is-der" in html,
    "Клас is-die": "is-die" in html,
    "Клас is-das": "is-das" in html
}

for check, found in color_checks.items():
    print(f"{'✅' if found else '❌'} {check}")

# ПРОБЛЕМА 4: СЛОВА З ФАЗИ
print("\n=== ПРОБЛЕМА 4: СЛОВА З ФАЗИ ===")
if quiz_pos > 0:
    # Витягуємо секцію quiz
    quiz_end = html.find('</section>', quiz_pos)
    quiz_html = html[quiz_pos:quiz_end] if quiz_end > 0 else ""
    
    # Слова з першої фази (throne)
    throne_words = ["Thron", "Königreich", "Macht", "Krone", "Reich", "Erbe"]
    found_words = []
    
    for word in throne_words:
        if word in quiz_html:
            found_words.append(word)
    
    if found_words:
        print(f"✅ Знайдено {len(found_words)} слів з фази throne: {', '.join(found_words)}")
    else:
        print("❌ НЕ знайдено слів з фази throne у вправі")
        # Перевірка що взагалі є у вправі
        print("\nАналіз вмісту вправи:")
        quiz_words = []
        lines = quiz_html.split('\n')
        for line in lines:
            if 'quiz-word' in line:
                # Витягуємо слово
                start = line.find('">') + 2
                end = line.find('</div>')
                if start > 1 and end > start:
                    quiz_words.append(line[start:end])
        if quiz_words:
            print(f"Слова у вправі: {', '.join(quiz_words[:10])}")
else:
    print("❌ Вправа articles-quiz НЕ ЗНАЙДЕНА")

# ФІНАЛЬНИЙ ВИСНОВОК
print("\n" + "=" * 60)
print("ФІНАЛЬНИЙ ВИСНОВОК")
print("=" * 60)

problems_status = {
    "1. Розташування": vocab_pos > 0 and quiz_pos > 0,
    "2. Мова": all(ru_checks.values()),
    "3. Кольори": all(color_checks.values()),
    "4. Слова з фази": len(found_words) > 0 if quiz_pos > 0 else False
}

for problem, status in problems_status.items():
    print(f"{'✅' if status else '❌'} {problem}")

if all(problems_status.values()):
    print("\n✅✅✅ ВСІ 4 ПРОБЛЕМИ ВИПРАВЛЕНО!")
else:
    print("\n❌ НЕ ВСІ ПРОБЛЕМИ ВИПРАВЛЕНО")
    print("\nЩО НЕ ПРАЦЮЄ:")
    for problem, status in problems_status.items():
        if not status:
            print(f"  - {problem}")
