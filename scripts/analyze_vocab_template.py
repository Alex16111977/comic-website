"""
Поиск проблемы со словарем
"""
import re

template_path = r'F:\AiKlientBank\KingLearComic\templates\journey.html'

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Найдем секцию словаря
vocab_start = content.find('<section class="vocabulary-section">')
if vocab_start != -1:
    vocab_end = content.find('</section>', vocab_start)
    vocab_section = content[vocab_start:vocab_end+10]
    
    print("[VOCABULARY SECTION FOUND]")
    print("-" * 50)
    
    # Найдем все переменные в секции
    variables = re.findall(r'\{\{[^}]+\}\}', vocab_section)
    print("[VARIABLES USED IN VOCABULARY]:")
    for var in variables:
        print(f"  - {var}")
    
    # Проверим есть ли цикл для словаря
    if '{% for' in vocab_section:
        loops = re.findall(r'\{%\s*for[^%]+%\}', vocab_section)
        print("\n[LOOPS IN VOCABULARY]:")
        for loop in loops:
            print(f"  - {loop}")
    
    # Проверим условия
    if '{% if' in vocab_section:
        conditions = re.findall(r'\{%\s*if[^%]+%\}', vocab_section)
        print("\n[CONDITIONS IN VOCABULARY]:")
        for cond in conditions:
            print(f"  - {cond}")
            
    # Покажем первые 500 символов секции
    print("\n[FIRST 500 CHARS OF VOCABULARY SECTION]:")
    print(vocab_section[:500])
else:
    print("[ERROR] vocabulary-section not found!")
