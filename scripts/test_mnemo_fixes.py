#!/usr/bin/env python
"""
Тест виправлення 4 проблем мнемотехніки
Автор: Senior Software Engineer
Дата: 28.09.2025
"""
from pathlib import Path
import json
import subprocess
import sys

def test_mnemonics_fixes():
    """Тестує всі 4 виправлення мнемотехніки"""
    
    print("=" * 60)
    print("ТЕСТ ВИПРАВЛЕННЯ МНЕМОТЕХНІКИ")
    print("=" * 60)
    
    # 1. Спочатку генеруємо сайт
    print("\n[1] Генерація сайту...")
    result = subprocess.run(
        [sys.executable, 'main.py'],
        capture_output=True,
        text=True,
        cwd=r'F:\AiKlientBank\KingLearComic'
    )
    
    if result.returncode != 0:
        print(f"[ERROR] Помилка генерації: {result.stderr}")
        return False
    
    print("[OK] Сайт згенеровано")
    
    # 2. Перевіряємо king_lear.html
    html_file = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
    if not html_file.exists():
        print(f"[ERROR] Файл не знайдено: {html_file}")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 3. Перевіряємо JSON для отримання слів фази
    json_file = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Отримуємо слова першої фази
    first_phase = None
    throne_words = []
    for phase in data.get('journey_phases', []):
        if not first_phase:
            first_phase = phase
        if phase.get('id') == 'throne':
            for word in phase.get('vocabulary', []):
                german = word.get('german', '')
                # Видаляємо артикль
                for art in ['der ', 'die ', 'das ']:
                    if german.startswith(art):
                        throne_words.append(german[len(art):])
                        break
            break
    
    print(f"\n[INFO] Перша фаза: {first_phase.get('id') if first_phase else 'не знайдено'}")
    print(f"[INFO] Слова фази throne: {throne_words[:5]}")
    
    # 4. ТЕСТ 1: РОЗТАШУВАННЯ
    print("\n" + "=" * 50)
    print("ТЕСТ 1: РОЗТАШУВАННЯ КОМПОНЕНТІВ")
    print("=" * 50)
    
    # Знаходимо позиції основних блоків
    theatrical_pos = html.find('theatrical-scene')
    vocab_section_pos = html.find('vocabulary-section')
    exercises_container_pos = html.find('exercises-container')
    articles_quiz_pos = html.find('articles-quiz')
    bottom_nav_pos = html.find('bottom-nav')
    
    print(f"theatrical-scene: позиція {theatrical_pos}")
    print(f"vocabulary-section: позиція {vocab_section_pos}")
    print(f"exercises-container: позиція {exercises_container_pos}")
    print(f"articles-quiz: позиція {articles_quiz_pos}")
    print(f"bottom-nav: позиція {bottom_nav_pos}")
    
    test1_pass = True
    
    # Перевірка 1.1: Словник після theatrical-scene, перед exercises
    if theatrical_pos < vocab_section_pos < exercises_container_pos:
        print("[OK] Словник розташований ПРАВИЛЬНО (після сцени, перед вправами)")
    else:
        print("[FAIL] Словник розташований НЕПРАВИЛЬНО")
        test1_pass = False
    
    # Перевірка 1.2: Вправа ВСЕРЕДИНІ exercises-container
    if exercises_container_pos < articles_quiz_pos < bottom_nav_pos:
        # Додаткова перевірка - чи вправа дійсно всередині exercises
        exercises_end = html.find('</div><!-- end exercises-container -->')
        if exercises_end > 0:
            if articles_quiz_pos < exercises_end:
                print("[OK] Вправа розташована ВСЕРЕДИНІ exercises-container")
            else:
                print("[FAIL] Вправа НЕ всередині exercises-container")
                test1_pass = False
        else:
            # Альтернативна перевірка через структуру
            print("[WARNING] Використовуємо альтернативну перевірку розташування")
            if exercises_container_pos < articles_quiz_pos < bottom_nav_pos:
                print("[OK] Вправа між exercises та nav (прийнятно)")
            else:
                print("[FAIL] Вправа в неправильному місці")
                test1_pass = False
    else:
        print("[FAIL] Вправа розташована НЕПРАВИЛЬНО")
        test1_pass = False
    
    # 5. ТЕСТ 2: СЛОВА З ПОТОЧНОЇ ФАЗИ
    print("\n" + "=" * 50)
    print("ТЕСТ 2: СЛОВА З ПОТОЧНОЇ ФАЗИ")
    print("=" * 50)
    
    test2_pass = True
    found_words = 0
    
    # Шукаємо слова у вправі articles-quiz
    quiz_start = html.find('<section class="articles-quiz"')
    quiz_end = html.find('</section>', quiz_start) if quiz_start > 0 else -1
    
    if quiz_start > 0 and quiz_end > quiz_start:
        quiz_html = html[quiz_start:quiz_end]
        
        for word in throne_words[:5]:
            if word in quiz_html:
                found_words += 1
                print(f"[OK] Знайдено слово з фази: {word}")
        
        if found_words >= 3:
            print(f"[OK] Використовуються правильні слова ({found_words}/5)")
        else:
            print(f"[FAIL] Мало слів з фази ({found_words}/5)")
            test2_pass = False
    else:
        print("[FAIL] Не знайдено секцію articles-quiz")
        test2_pass = False
    
    # 6. ТЕСТ 3: РОСІЙСЬКА МОВА
    print("\n" + "=" * 50)
    print("ТЕСТ 3: МОВА ІНТЕРФЕЙСУ")
    print("=" * 50)
    
    test3_pass = True
    ru_checks = {
        "Заголовок вправи": "Артикли и род" in html,
        "Опис вправи": "Выберите правильный артикль" in html,
        "Мужской": "мужской" in html,
        "Женский": "женский" in html,
        "Средний": "средний" in html,
        "Словарь урока": "Словарь урока" in html
    }
    
    for check_name, check_result in ru_checks.items():
        if check_result:
            print(f"[OK] {check_name}")
        else:
            print(f"[FAIL] {check_name}")
            test3_pass = False
    
    # 7. ТЕСТ 4: КОЛЬОРОВА КОДИРОВКА
    print("\n" + "=" * 50)
    print("ТЕСТ 4: КОЛЬОРОВА КОДИРОВКА")
    print("=" * 50)
    
    test4_pass = True
    color_checks = {
        "Градієнт der (синій)": "linear-gradient(135deg, #e3f2fd, #bbdefb)" in html,
        "Градієнт die (червоний)": "linear-gradient(135deg, #fce4ec, #f8bbd0)" in html,
        "Градієнт das (зелений)": "linear-gradient(135deg, #e8f5e9, #c8e6c9)" in html,
        "Клас is-der": "is-der" in html,
        "Клас is-die": "is-die" in html,
        "Клас is-das": "is-das" in html,
        "Border der": "border-left: 4px solid #1976d2" in html,
        "Border die": "border-left: 4px solid #d32f2f" in html,
        "Border das": "border-left: 4px solid #388e3c" in html
    }
    
    for check_name, check_result in color_checks.items():
        if check_result:
            print(f"[OK] {check_name}")
        else:
            print(f"[FAIL] {check_name}")
            test4_pass = False
    
    # 8. ФІНАЛЬНИЙ РЕЗУЛЬТАТ
    print("\n" + "=" * 60)
    print("ФІНАЛЬНИЙ РЕЗУЛЬТАТ")
    print("=" * 60)
    
    all_tests_passed = test1_pass and test2_pass and test3_pass and test4_pass
    
    if all_tests_passed:
        print("\n✅ [SUCCESS] ВСІ 4 ПРОБЛЕМИ ВИПРАВЛЕНО!")
        print("✅ Розташування: Словник зверху, вправа в exercises")
        print("✅ Слова: Використовуються слова з поточної фази")
        print("✅ Мова: Російська мова інтерфейсу")
        print("✅ Кольори: Градієнтна кодировка працює")
    else:
        print("\n❌ [FAIL] НЕ ВСІ ПРОБЛЕМИ ВИПРАВЛЕНО:")
        if not test1_pass:
            print("❌ Проблема з розташуванням")
        if not test2_pass:
            print("❌ Проблема зі словами")
        if not test3_pass:
            print("❌ Проблема з мовою")
        if not test4_pass:
            print("❌ Проблема з кольорами")
    
    print("\n[INFO] Перегляньте файл:")
    print(f"file:///{html_file}")
    
    return all_tests_passed

if __name__ == "__main__":
    success = test_mnemonics_fixes()
    sys.exit(0 if success else 1)
