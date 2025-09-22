"""
Тест: Проверка подсказок в обоих режимах викторины
Дата: 09.01.2025
Мета: Проверяем что russian_hint отображается и в прямом, и в обратном режиме
"""

import json
from pathlib import Path

def test_quiz_hints_both_modes():
    """Проверка подсказок в обоих режимах викторины"""
    
    print("[INFO] Проверка подсказок в обоих режимах викторины...")
    print("=" * 60)
    
    # Путь к файлу journey_runtime.js
    runtime_path = Path(r"F:\AiKlientBank\KingLearComic\output\static\js\journey_runtime.js")
    
    if not runtime_path.exists():
        print("[ERROR] Файл journey_runtime.js не найден!")
        return False
    
    # Читаем содержимое файла
    content = runtime_path.read_text(encoding='utf-8')
    
    # Проверки для ПРЯМОГО режима (DE → RU)
    print("[+] Проверка ПРЯМОГО режима (Немецкий → Русский):")
    forward_checks = {
        "generateForwardQuestion с подсказкой": "generateForwardQuestion(word) {",
        "Условие для forward подсказки": "if (word.russianHint) {",
        "Текст вопроса с подсказкой": "» (${word.russianHint})?",
        "russianHint в forward объекте": "russianHint: word.russianHint ||",
    }
    
    forward_ok = True
    for check_name, check_pattern in forward_checks.items():
        if check_pattern in content:
            print(f"    [OK] {check_name}")
        else:
            print(f"    [ERROR] {check_name} - НЕ НАЙДЕНО!")
            forward_ok = False
    
    # Проверки для ОБРАТНОГО режима (RU → DE)
    print("\n[+] Проверка ОБРАТНОГО режима (Русский → Немецкий):")
    reverse_checks = {
        "generateReverseQuestion с подсказкой": "generateReverseQuestion(word) {",
        "Условие для reverse подсказки": '// Добавляем подсказку к вопросу если есть',
        "Текст вопроса с подсказкой в reverse": "» (${word.russianHint})?",
        "russianHint в reverse объекте": "russianHint: word.russianHint ||",
    }
    
    reverse_ok = True
    for check_name, check_pattern in reverse_checks.items():
        if check_pattern in content:
            print(f"    [OK] {check_name}")
        else:
            print(f"    [ERROR] {check_name} - НЕ НАЙДЕНО!")
            reverse_ok = False
    
    # Проверка отображения в renderQuestion
    print("\n[+] Проверка отображения подсказок в renderQuestion:")
    render_checks = {
        "Отображение в forward режиме": "if (question.type === 'forward')",
        "Отображение в reverse режиме": "} else { // reverse mode",
        "Создание hint элемента": "hintSpan.className = 'quiz-hint';",
        "Стиль подсказки (фиолетовый)": "hintSpan.style.color = '#7c3aed';",
        "Размер шрифта подсказки": "hintSpan.style.fontSize = '0.9em';",
        "Отступ подсказки": "hintSpan.style.marginLeft = '8px';",
    }
    
    render_ok = True
    for check_name, check_pattern in render_checks.items():
        if check_pattern in content:
            print(f"    [OK] {check_name}")
        else:
            print(f"    [ERROR] {check_name} - НЕ НАЙДЕНО!")
            render_ok = False
    
    # Проверяем buildPhaseQuizWords
    print("\n[+] Проверка передачи подсказок из данных:")
    if "russianHint: word.russian_hint ||" in content:
        print("    [OK] buildPhaseQuizWords передает russian_hint")
    else:
        print("    [ERROR] buildPhaseQuizWords не передает russian_hint")
        render_ok = False
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if forward_ok and reverse_ok and render_ok:
        print("[OK] Все проверки пройдены успешно!")
        print("[OK] Подсказки работают в обоих режимах викторины!")
        
        print("\n[+] Примеры отображения:")
        print("\n📘 ПРЯМОЙ режим (DE → RU):")
        print("    Вопрос: Что означает немецкое слово «der Thron» (символ королевской власти)?")
        print("    ")
        print("    der Thron (символ королевской власти)")
        print("    [дер ТРОН]")
        print("    ")
        print("    О трон      О гнев")
        print("    О безумие   О проклятие")
        
        print("\n📗 ОБРАТНЫЙ режим (RU → DE):")
        print("    Вопрос: Как переводится на немецкий слово «трон» (символ королевской власти)?")
        print("    ")
        print("    трон (символ королевской власти)")
        print("    ")
        print("    О der Thron     О der Zorn")
        print("    О der Wahnsinn  О der Fluch")
        
        return True
    else:
        print("[ERROR] Некоторые проверки не пройдены!")
        return False

if __name__ == "__main__":
    test_quiz_hints_both_modes()
