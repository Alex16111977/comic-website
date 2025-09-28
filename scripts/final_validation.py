#!/usr/bin/env python
"""
Фінальна валідація виправлень мнемотехніки
"""
from pathlib import Path

def validate():
    html_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"

    if not html_file.exists():
        print("[ERROR] king_lear.html не існує! Запустіть генерацію.")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    print("[ВАЛІДАЦІЯ] Результати виправлення:")
    print("=" * 60)

    checks = {
        "CSS мнемотехніки в HEAD": '.vocab-card' in html and '.articles-quiz' in html,
        "JavaScript для артиклів": 'initArticlesQuiz' in html,
        "Кольорові класи (der)": 'is-der' in html or 'color-der' in html,
        "Кольорові класи (die)": 'is-die' in html or 'color-die' in html, 
        "Кольорові класи (das)": 'is-das' in html or 'color-das' in html,
        "Існує vocabulary-grid": 'vocabulary-grid' in html,
        "Словник з мнемотехнікою": 'vocab-card' in html,
        "Вправа на артиклі": 'articles-quiz' in html or 'articles-exercise' in html,
        "Російська мова інтерфейсу": 'Выберите правильный артикль' in html or 'Артикли и род' in html,
        "Легенда артиклів": 'чоловічий' in html or 'мужской' in html,
        "НЕ українська в інтерфейсі": 'Виберіть правильний артикль' not in html
    }

    success = 0
    failed_checks = []
    for check, status in checks.items():
        print(f"  {'[OK]' if status else '[FAIL]'} {check}")
        if status:
            success += 1
        else:
            failed_checks.append(check)

    print("-" * 60)
    
    # Додаткова діагностика exercises
    if 'exercises-container' in html:
        print("[INFO] exercises-container знайдено в HTML")
    else:
        print("[WARNING] exercises-container НЕ знайдено в HTML")
    
    # Перевірка позицій елементів
    vocab_pos = html.find('vocabulary-grid') if 'vocabulary-grid' in html else -1
    exercises_pos = html.find('exercises-container') if 'exercises-container' in html else -1
    nav_pos = html.find('bottom-nav') if 'bottom-nav' in html else -1
    
    if vocab_pos > 0 and exercises_pos > 0:
        if vocab_pos < exercises_pos:
            print("[OK] Словник розташовано ПЕРЕД exercises")
        else:
            print("[FAIL] Словник розташовано ПІСЛЯ exercises")
    
    print("-" * 60)
    
    if success == len(checks):
        print(f"[SUCCESS] Всі {len(checks)} перевірок пройдені!")
        return True
    else:
        print(f"[ERROR] Пройдено {success}/{len(checks)} перевірок")
        print(f"[FAILED] Не пройдені: {', '.join(failed_checks)}")
        return False

if __name__ == "__main__":
    import sys
    success = validate()
    sys.exit(0 if success else 1)
