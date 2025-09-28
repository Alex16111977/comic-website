#!/usr/bin/env python
"""
Фікс інтеграції мнемотехніки в html_lira.py
"""
import sys
from pathlib import Path

# Читаємо поточний файл
gen_file = Path(__file__).parent.parent / "generators" / "html_lira.py"
with open(gen_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Створюємо бекап
backup_file = gen_file.with_suffix('.py.backup')
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"[OK] Бекап створено: {backup_file}")

# ФІКС 1: Виправляємо метод вставки CSS
# Оскільки немає <style> тегів, CSS буде додано інлайново в HTML
old_css_insert = "html = html.replace('</style>', mnemo_css + '\\n</style>')"
new_css_insert = """# CSS вже включено інлайново в HTML елементи мнемотехніки
        # Додатковий CSS не потрібен, оскільки використовується inline styling"""

# ФІКС 2: Виправляємо метод вставки HTML секцій  
old_html_insert = "html = html.replace('</main>', mnemo_vocabulary + mnemo_quiz + '</main>')"
new_html_insert = """# Вставляємо HTML секції мнемотехніки між exercises та bottom-nav
        # Використовуємо точний патерн знайдений аналізом
        insert_pattern = '</div>\\n            \\n        </div>\\n\\n        <nav class="bottom-nav">'
        
        if insert_pattern in html:
            # Вставляємо мнемотехніку перед навігацією
            replacement = f'</div>\\n            \\n        </div>\\n\\n        {mnemo_vocabulary}\\n        {mnemo_quiz}\\n\\n        <nav class="bottom-nav">'
            html = html.replace(insert_pattern, replacement)
            print(f"[DEBUG] Мнемотехніка вставлена для {character_id}")
        else:
            # Запасний варіант з regex для більшої гнучкості
            import re
            pattern = r'(</div>\\s*</div>\\s*)(<nav class="bottom-nav">)'
            match = re.search(pattern, html)
            if match:
                # Вставляємо між закриваючими div і nav
                html = re.sub(pattern, rf'\\1\\n        {mnemo_vocabulary}\\n        {mnemo_quiz}\\n\\n        \\2', html)
                print(f"[DEBUG] Мнемотехніка вставлена через regex для {character_id}")
            else:
                print(f"[WARNING] Не вдалось вставити мнемотехніку для {character_id}")"""

# ФІКС 3: Додаємо стилі через style тег в head
css_in_head = """
        # Додаємо CSS стилі в head через style тег
        if mnemo_css and '</head>' in html:
            style_block = f'<style>\\n{mnemo_css}\\n</style>'
            html = html.replace('</head>', f'{style_block}\\n</head>')
            print(f"[DEBUG] CSS мнемотехніки додано в head для {character_id}")
"""

# Застосовуємо фікси
fixes_applied = []

# Фікс CSS вставки
if old_css_insert in content:
    # Замінюємо старий метод на новий з додаванням в head
    content = content.replace(old_css_insert, css_in_head.strip())
    fixes_applied.append("CSS вставка (додано в head)")

# Фікс HTML вставки
if old_html_insert in content:
    content = content.replace(old_html_insert, new_html_insert.strip())
    fixes_applied.append("HTML вставка (між exercises та nav)")

# Додаємо import re якщо його немає
if 'import re' not in content:
    # Знаходимо місце після інших імпортів
    import_pos = content.find('from pathlib import Path')
    if import_pos > 0:
        end_of_line = content.find('\n', import_pos)
        content = content[:end_of_line+1] + 'import re\n' + content[end_of_line+1:]
        fixes_applied.append("Додано import re")

# Зберігаємо виправлений файл
if fixes_applied:
    with open(gen_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[SUCCESS] html_lira.py виправлено!")
    print("[FIXES] Застосовано:")
    for fix in fixes_applied:
        print(f"  - {fix}")
else:
    print("[WARNING] Не знайдено що виправляти - можливо вже виправлено?")
