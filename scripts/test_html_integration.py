#!/usr/bin/env python
"""
Тест інтеграції мнемотехніки в HTML генератор
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.html_lira import LiraHTMLGenerator
import config

try:
    # Створюємо генератор
    html_gen = LiraHTMLGenerator(config)
    print("[OK] HTML генератор створено")
    
    # Тестуємо на одному персонажі
    test_char = config.CHARACTERS_DIR / "king_lear.json"
    
    if test_char.exists():
        html = html_gen.generate_journey(test_char)
        
        # Перевіряємо наявність мнемотехніки
        checks = [
            ('vocabulary-section' in html, "Секція словника"),
            ('articles-quiz' in html, "Вправа на артиклі"),
            ('articles-legend' in html, "Легенда артиклів"),
            ('vocab-card' in html, "Картки слів"),
            ('--der-primary' in html, "CSS змінні"),
            ('initArticlesQuiz' in html, "JavaScript функції")
        ]
        
        print("\nПеревірка компонентів:")
        for check, name in checks:
            status = "[OK]" if check else "[FAIL]"
            print(f"  {status} {name}: {check}")
        
        # Зберігаємо тестову сторінку
        test_output = Path(__file__).parent / "test_king_lear_mnemo.html"
        with open(test_output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n[OK] Тестова сторінка збережена: {test_output}")
        
        # Підрахунок елементів
        vocab_count = html.count('vocab-card')
        quiz_count = html.count('quiz-item')
        print(f"\nСтатистика:")
        print(f"  Карток словника: {vocab_count}")
        print(f"  Питань вправи: {quiz_count}")
        
    else:
        print("[ERROR] Файл king_lear.json не знайдено!")
        
except Exception as e:
    print(f"[ERROR] Помилка тестування: {e}")
    import traceback
    traceback.print_exc()
