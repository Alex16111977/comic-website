#!/usr/bin/env python
"""
Валідація мнемотехніки в згенерованих файлах
"""
from pathlib import Path
import re

output_dir = Path(__file__).parent.parent / "output"
journeys_dir = output_dir / "journeys"

validation_results = []

print("=" * 60)
print("ВАЛІДАЦІЯ МНЕМОТЕХНІКИ")
print("=" * 60)

for html_file in journeys_dir.glob("*.html"):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Перевірки
    has_vocab = 'vocabulary-section' in content
    has_quiz = 'articles-quiz' in content
    has_legend = 'articles-legend' in content
    vocab_cards = content.count('vocab-card')
    quiz_items = content.count('quiz-item')
    has_css_vars = '--der-primary' in content
    has_js = 'initArticlesQuiz' in content
    
    validation_results.append({
        'file': html_file.name,
        'vocabulary': has_vocab,
        'quiz': has_quiz,
        'legend': has_legend,
        'cards': vocab_cards,
        'items': quiz_items,
        'css': has_css_vars,
        'js': has_js
    })
    
    print(f"\n[CHECK] {html_file.name}:")
    print(f"  Словник: {has_vocab} ({vocab_cards} карток)")
    print(f"  Вправа: {has_quiz} ({quiz_items} питань)")
    print(f"  Легенда: {has_legend}")
    print(f"  CSS: {has_css_vars}")
    print(f"  JavaScript: {has_js}")

# Підсумок
total = len(validation_results)
with_vocab = sum(1 for r in validation_results if r['vocabulary'])
with_quiz = sum(1 for r in validation_results if r['quiz'])
with_css = sum(1 for r in validation_results if r['css'])
with_js = sum(1 for r in validation_results if r['js'])
total_cards = sum(r['cards'] for r in validation_results)
total_items = sum(r['items'] for r in validation_results)

print("\n" + "=" * 60)
print("ПІДСУМОК")
print("=" * 60)
print(f"  Всього файлів: {total}")
print(f"  Зі словником: {with_vocab}/{total}")
print(f"  З вправами: {with_quiz}/{total}")
print(f"  З CSS: {with_css}/{total}")
print(f"  З JavaScript: {with_js}/{total}")
print(f"  Всього карток: {total_cards}")
print(f"  Всього питань: {total_items}")

if with_vocab == total and with_quiz == total:
    print("\n[SUCCESS] Мнемотехніка успішно інтегрована в усі файли!")
else:
    print("\n[WARNING] Не всі файли мають повну мнемотехніку")
