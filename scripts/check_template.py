"""
Проверка шаблона journey.html на наличие секции словаря
"""
import os

# Проверим размер файла journey.html
template_path = r'F:\AiKlientBank\KingLearComic\templates\journey.html'
if os.path.exists(template_path):
    size = os.path.getsize(template_path)
    print(f"[OK] journey.html exists, size: {size} bytes")
    
    # Читаем файл и ищем словарь
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Проверяем наличие разных ключевых слов
    checks = {
        'vocabulary': 'vocabulary' in content.lower(),
        'словарь': 'словарь' in content.lower(), 
        'dictionary': 'dictionary' in content.lower(),
        'Фаза': 'фаза' in content,
        'exercises': 'exercises' in content,
        'quiz': 'quiz' in content.lower()
    }
    
    print("\n[CHECK] Template contains:")
    for key, found in checks.items():
        status = "[+]" if found else "[-]"
        print(f"  {status} {key}")
    
    # Проверим какие блоки есть в шаблоне
    print("\n[BLOCKS] Found sections:")
    sections = ['journey-container', 'exercises-section', 'quiz-section', 'vocabulary-section', 'vocabulary-grid']
    for section in sections:
        if section in content:
            print(f"  [+] {section}")
        else:
            print(f"  [-] {section}")
            
    # Ищем как передается словарь из character
    print("\n[VARIABLES] Character fields used:")
    char_fields = ['character.vocabulary', 'character.quotes', 'journey_phases', 'exercises', 'quizzes']
    for field in char_fields:
        if field in content:
            print(f"  [+] {field}")
        else:
            print(f"  [-] {field}")
else:
    print("[ERROR] journey.html not found!")
