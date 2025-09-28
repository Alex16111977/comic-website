#!/usr/bin/env python
"""
Валідація всіх згенерованих файлів на наявність мнемотехніки
"""
from pathlib import Path

output_dir = Path(__file__).parent.parent / "output"
journeys_dir = output_dir / "journeys"

if not journeys_dir.exists():
    print("[ERROR] Папка journeys не існує!")
    exit(1)

html_files = list(journeys_dir.glob("*.html"))
print(f"[INFO] Знайдено файлів: {len(html_files)}")
print("=" * 60)

total_files = 0
with_mnemo = 0
without_mnemo = []
detailed_checks = {}

for html_file in html_files:
    total_files += 1
    character = html_file.stem
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Детальні перевірки для кожного компонента
    checks = {
        'vocabulary-grid': '<div class="vocabulary-grid">' in content,
        'articles-quiz': 'articles-quiz' in content,
        'articles-legend': 'articles-legend' in content,
        'CSS vars': '--der-primary' in content,
        'JS init': 'initArticlesQuiz' in content,
        'vocab-card': 'vocab-card' in content,
        'quiz-item': 'quiz-item' in content
    }
    
    detailed_checks[character] = checks
    all_present = all(checks.values())
    
    if all_present:
        with_mnemo += 1
        print(f"[OK] {html_file.name} - ВСІ компоненти ✅")
    else:
        without_mnemo.append(html_file.name)
        print(f"[FAIL] {html_file.name}")
        for component, present in checks.items():
            if not present:
                print(f"       ❌ Немає {component}")

print("=" * 60)
print(f"ПІДСУМОК:")
print(f"  Всього файлів: {total_files}")
print(f"  З повною мнемотехнікою: {with_mnemo}")
print(f"  З проблемами: {len(without_mnemo)}")

if without_mnemo:
    print(f"\n[WARNING] Файли з проблемами:")
    for name in without_mnemo:
        print(f"  - {name}")
        
# Детальна статистика по компонентам
print("\n[СТАТИСТИКА ПО КОМПОНЕНТАМ]")
component_stats = {}
for component in ['vocabulary-grid', 'articles-quiz', 'articles-legend', 
                  'CSS vars', 'JS init', 'vocab-card', 'quiz-item']:
    count = sum(1 for char_checks in detailed_checks.values() 
                if char_checks.get(component, False))
    component_stats[component] = count
    print(f"  {component}: {count}/{total_files}")

if with_mnemo == total_files:
    print("\n🎉 [SUCCESS] ВСІ ФАЙЛИ МАЮТЬ ПОВНУ МНЕМОТЕХНІКУ!")
    exit(0)
else:
    print("\n[ERROR] Не всі файли мають повну мнемотехніку!")
    exit(1)
