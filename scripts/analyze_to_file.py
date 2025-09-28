#!/usr/bin/env python
"""Детальний аналіз king_lear.html з виведенням у файл"""
from pathlib import Path

output_file = Path(r'F:\AiKlientBank\KingLearComic\scripts\analysis_result.txt')

# Читаємо HTML
html_file = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

result = []
result.append("=" * 60)
result.append("ДЕТАЛЬНИЙ АНАЛІЗ KING_LEAR.HTML")
result.append("=" * 60)
result.append(f"\nРозмір файлу: {len(html)} символів")

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

result.append("\n=== ПОЗИЦІЇ БЛОКІВ ===")
for name, pos in blocks.items():
    if pos == -1:
        result.append(f"{name}: НЕ ЗНАЙДЕНО ❌")
    else:
        result.append(f"{name}: {pos}")

# ПРОБЛЕМА 1: РОЗТАШУВАННЯ
result.append("\n=== ПРОБЛЕМА 1: РОЗТАШУВАННЯ ===")
vocab_pos = blocks['vocabulary-section']
theatrical_end = blocks['theatrical-scene END']
exercises_start = blocks['exercises-container START']
exercises_end = blocks['exercises-container END']
quiz_pos = blocks['articles-quiz']
nav_pos = blocks['bottom-nav']

if vocab_pos == -1:
    result.append("❌ КРИТИЧНА ПОМИЛКА: vocabulary-section НЕ ІСНУЄ!")
    result.append("   Словник НЕ БУВ ВСТАВЛЕНИЙ взагалі")
else:
    if theatrical_end > 0 and vocab_pos > theatrical_end:
        result.append("✅ Словник ПІСЛЯ theatrical-scene")
    else:
        result.append("❌ Словник НЕ після theatrical-scene")
    
    if vocab_pos < exercises_start:
        result.append("✅ Словник ПЕРЕД exercises-container")
    else:
        result.append("❌ Словник НЕ перед exercises-container")

if quiz_pos == -1:
    result.append("❌ КРИТИЧНА ПОМИЛКА: articles-quiz НЕ ІСНУЄ!")
    result.append("   Вправа НЕ БУЛА ВСТАВЛЕНА взагалі")
else:
    if quiz_pos > exercises_start:
        result.append("✅ Вправа ПІСЛЯ початку exercises-container")
        
        if exercises_end > 0 and quiz_pos < exercises_end:
            result.append("✅✅ ВІДМІННО! Вправа ВСЕРЕДИНІ exercises-container!")
        elif exercises_end == -1:
            result.append("⚠️ Немає коментаря end exercises-container")
            # Альтернативна перевірка
            if quiz_pos < nav_pos:
                result.append("✅ Вправа перед bottom-nav (прийнятно)")
        else:
            result.append("❌ Вправа ПОЗА exercises-container")
    else:
        result.append("❌ Вправа НЕ після exercises-container")

# ПРОБЛЕМА 2: МОВА
result.append("\n=== ПРОБЛЕМА 2: МОВА ІНТЕРФЕЙСУ ===")
ru_checks = {
    "Артикли и род": html.find("Артикли и род") > 0,
    "Выберите правильный артикль": html.find("Выберите правильный артикль") > 0,
    "мужской": html.find("мужской") > 0,
    "женский": html.find("женский") > 0,
    "средний": html.find("средний") > 0,
    "Словарь урока": html.find("Словарь урока") > 0
}

for text, found in ru_checks.items():
    result.append(f"{'✅' if found else '❌'} '{text}' - {'знайдено' if found else 'НЕ знайдено'}")

# ПРОБЛЕМА 3: КОЛЬОРИ
result.append("\n=== ПРОБЛЕМА 3: КОЛЬОРОВА КОДИРОВКА ===")
color_checks = {
    "Градієнт der": "linear-gradient(135deg, #e3f2fd, #bbdefb)" in html,
    "Градієнт die": "linear-gradient(135deg, #fce4ec, #f8bbd0)" in html,
    "Градієнт das": "linear-gradient(135deg, #e8f5e9, #c8e6c9)" in html,
    "Клас is-der": "is-der" in html,
    "Клас is-die": "is-die" in html,
    "Клас is-das": "is-das" in html
}

for check, found in color_checks.items():
    result.append(f"{'✅' if found else '❌'} {check}")

# ПРОБЛЕМА 4: СЛОВА З ФАЗИ
result.append("\n=== ПРОБЛЕМА 4: СЛОВА З ФАЗИ ===")
found_words = []
if quiz_pos > 0:
    # Витягуємо секцію quiz
    quiz_end = html.find('</section>', quiz_pos)
    quiz_html = html[quiz_pos:quiz_end] if quiz_end > 0 else ""
    
    # Слова з першої фази (throne)
    throne_words = ["Thron", "Königreich", "Macht", "Krone", "Reich", "Erbe"]
    
    for word in throne_words:
        if word in quiz_html:
            found_words.append(word)
    
    if found_words:
        result.append(f"✅ Знайдено {len(found_words)} слів з фази throne: {', '.join(found_words)}")
    else:
        result.append("❌ НЕ знайдено слів з фази throne у вправі")
        # Перевірка що взагалі є у вправі
        result.append("\nАналіз вмісту вправи:")
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
            result.append(f"Слова у вправі: {', '.join(quiz_words[:10])}")
else:
    result.append("❌ Вправа articles-quiz НЕ ЗНАЙДЕНА")

# ФІНАЛЬНИЙ ВИСНОВОК
result.append("\n" + "=" * 60)
result.append("ФІНАЛЬНИЙ ВИСНОВОК")
result.append("=" * 60)

problems_status = {
    "1. Розташування": vocab_pos > 0 and quiz_pos > 0,
    "2. Мова": all(ru_checks.values()),
    "3. Кольори": all(color_checks.values()),
    "4. Слова з фази": len(found_words) > 0
}

for problem, status in problems_status.items():
    result.append(f"{'✅' if status else '❌'} {problem}")

if all(problems_status.values()):
    result.append("\n✅✅✅ ВСІ 4 ПРОБЛЕМИ ВИПРАВЛЕНО!")
else:
    result.append("\n❌ НЕ ВСІ ПРОБЛЕМИ ВИПРАВЛЕНО")
    result.append("\nЩО НЕ ПРАЦЮЄ:")
    for problem, status in problems_status.items():
        if not status:
            result.append(f"  - {problem}")

# Записуємо результат у файл
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))

print(f"Результат записано у {output_file}")
