"""
Читаем секции упражнений для замены
"""

from pathlib import Path

js_file = Path(r'F:\AiKlientBank\KingLearComic\generators\js_lira.py')

with open(js_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Word Families section
print("[Word Families Section] Lines 1315-1400:")
print("="*70)
for i in range(1314, min(1400, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
    
print("\n" + "="*70)
print("\n[Collocations Section] Lines 1400-1485:")
print("="*70)
for i in range(1399, min(1485, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
