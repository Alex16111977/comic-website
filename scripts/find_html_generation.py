"""
Поиск генерации HTML для relation секций
"""

with open(r'F:\AiKlientBank\KingLearComic\generators\js_lira.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"[Analyzing js_lira.py] Total lines: {len(lines)}")

# Ищем где генерируется HTML для relation sections
html_patterns = [
    '<div class="relation-section',
    'relation-section word-families',
    'relation-section collocations',
    'Семья слов</h4>',
    'Коллокации</h4>',
    'class="word-families-section"',
    'class="collocations-section"'
]

found_html = False
for pattern in html_patterns:
    for i, line in enumerate(lines):
        if pattern in line:
            if not found_html:
                print("\n[Found HTML generation code:]")
                found_html = True
            print(f"\nPattern: '{pattern}' at line {i+1}")
            # Показываем большой контекст
            start = max(0, i - 10)
            end = min(len(lines), i + 20)
            print("Context:")
            for j in range(start, end):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j+1}: {lines[j][:120]}{'...' if len(lines[j]) > 120 else ''}", end='')

if not found_html:
    print("\n[!] HTML for relation sections not found directly")
    print("[?] Checking if HTML is generated in a different way...")
    
    # Может быть HTML генерируется через template strings
    for i, line in enumerate(lines):
        if 'innerHTML' in line and ('families' in lines[i:i+5] or 'collocations' in lines[i:i+5]):
            print(f"\nFound innerHTML generation at line {i+1}")
            # Показываем контекст
            for j in range(max(0, i-2), min(len(lines), i+5)):
                print(f"  {j+1}: {lines[j][:100]}")
