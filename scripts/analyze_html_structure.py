#!/usr/bin/env python
"""
Аналіз структури згенерованого HTML для знаходження точок вставки
"""
import re
from pathlib import Path

# Читаємо згенерований файл
html_file = Path(__file__).parent.parent / "output" / "journeys" / "king_lear.html"

if not html_file.exists():
    print("[ERROR] Файл не існує! Спочатку згенеруйте сайт.")
    exit(1)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("[АНАЛІЗ] Структура HTML файлу:")
print("=" * 60)

# Шукаємо ключові теги та структури
searches = [
    ('</style>', "Тег закриття style"),
    ('</main>', "Тег закриття main"),
    ('</body>', "Тег закриття body"),
    ('</div>\n    <script>', "Закриття div перед script"),
    ('exercises-container', "Контейнер вправ"),
    ('bottom-nav', "Нижня навігація"),
    ('journey-timeline', "Timeline подорожі"),
]

for pattern, description in searches:
    if pattern in html:
        # Показуємо контекст навколо знайденого патерну
        index = html.find(pattern)
        context_start = max(0, index - 100)
        context_end = min(len(html), index + 100)
        context = html[context_start:context_end]
        
        print(f"[OK] Знайдено: {description}")
        print(f"     Позиція: {index}")
        print(f"     Контекст: ...{context}...")
    else:
        print(f"[MISS] НЕ знайдено: {description}")
    print("-" * 60)

# Знаходимо найкращу точку для вставки
print("\n[РЕКОМЕНДАЦІЯ] Найкращі точки вставки:")

# Варіант 1: Після exercises-container
if 'exercises-container' in html:
    pattern = '</div>\n        </div>\n\n        <nav class="bottom-nav">'
    if pattern in html:
        print("[1] Після exercises-container, перед bottom-nav")
        print(f"    Патерн: {repr(pattern[:50])}")

# Варіант 2: Перед закриваючим script
if '</div>\n    <script>' in html:
    print("[2] Перед секцією script")
    print("    Патерн: '</div>\\n    <script>'")

# Варіант 3: Після journey секції
if 'journey-section' in html:
    # Знаходимо закриття journey-section
    match = re.search(r'</div>\s*<!--\s*end journey-section\s*-->', html)
    if match:
        print("[3] Після journey-section")
    else:
        # Шукаємо інший варіант закриття
        if re.search(r'</div>\s*<div class="exercises-container"', html):
            print("[3] Між journey-section та exercises-container")

print("\n[INFO] Використайте знайдені патерни для replace()")
