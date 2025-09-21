"""
Детальный поиск словаря в шаблоне
"""
import re

template_path = r'F:\AiKlientBank\KingLearComic\templates\journey.html'

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем любое упоминание словаря
vocab_matches = []
lines = content.split('\n')

for i, line in enumerate(lines):
    if 'vocabulary' in line.lower() or 'словарь' in line.lower():
        vocab_matches.append((i+1, line.strip()))

print(f"[FOUND] {len(vocab_matches)} lines with vocabulary/словарь:")
for line_no, line in vocab_matches[:10]:  # Первые 10
    print(f"  Line {line_no}: {line[:100]}...")
    
# Найдем vocabulary-grid
grid_pos = content.find('vocabulary-grid')
if grid_pos != -1:
    # Показать контекст вокруг
    start = max(0, grid_pos - 200)
    end = min(len(content), grid_pos + 300)
    context = content[start:end]
    print("\n[VOCABULARY-GRID CONTEXT]:")
    print("-" * 50)
    print(context)
    print("-" * 50)
else:
    print("\n[ERROR] vocabulary-grid not found!")

# Проверим что передается в шаблон
print("\n[LOOKING FOR VOCABULARY DATA]:")
vocab_patterns = [
    r'character\.vocabulary',
    r'vocabulary\s*=',
    r'{% for.*vocabulary',
    r'{{ .*vocabulary'
]

for pattern in vocab_patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"  [+] Pattern '{pattern}' found: {matches[:2]}")
    else:
        print(f"  [-] Pattern '{pattern}' not found")
