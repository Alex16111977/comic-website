# ІНСТРУКЦІЯ ДЛЯ ПРОЕКТУ King Lear Comic Generator
(Система генерації навчального сайту "Німецька через Короля Ліра")  
**Версія: 1.0 | Створено: 14.09.2025**

## 🚀 КРИТИЧНЕ ВІДКРИТТЯ - РІШЕННЯ ПРОБЛЕМИ СТВОРЕННЯ ФАЙЛІВ!

### ✅ SUBPROCESS.RUN() ПРАЦЮЄ ДЛЯ СТВОРЕННЯ ФАЙЛІВ!

**ВАЖЛИВЕ:** subprocess.run() в python-runner МОЖЕ створювати файли на диску!

```python
# ✅ ЦЕЙ КОД ПРАЦЮЄ і СТВОРЮЄ файли:
import subprocess
import sys

result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,  
    cwd=r'F:\AiKlientBank\KingLearComic'
)
# ВСІ 13 HTML файлів будуть створені на диску!
print(f"Exit code: {result.returncode}")
print(f"Створено файлів: {result.stdout}")
```

### 📊 ПОРІВНЯННЯ МЕТОДІВ:

| Метод | Створює файли? | Примітка |
|--------|---------------|----------|
| **subprocess.run()** | ✅ ТАК | ПОВНИЙ доступ до файлової системи |
| exec() | ❌ НІ | Код виконується, але файли в пам'яті |
| with open() | ❌ НІ | Файли не записуються на диск |
| **filesystem:write_file** | ✅ ТАК | Прямий запис через MCP API |

### 🎯 ПРАКТИЧНІ ПРИКЛАДИ:

#### 1️⃣ Генерація сайту (створює 13 файлів):
```python
import subprocess
import sys

# ПРАЦЮЄ! Створює всі HTML файли
result = subprocess.run(
    [sys.executable, r'F:\AiKlientBank\KingLearComic\main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

if result.returncode == 0:
    print("[OK] Сайт згенеровано!")
```

#### 2️⃣ Запуск тестових скриптів:
```python
# Перевірка театральних сцен
result = subprocess.run(
    [sys.executable, 'scripts/check_theatrical_scenes.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)
```

---

## 🎯 СТИЛЬ РОБОТИ

DO NOT GIVE ME HIGH LEVEL STUFF! Якщо прошу виправлення або пояснення, хочу РЕАЛЬНИЙ КОД або ПОЯСНЕННЯ!
НЕ хочу "Here's how you can blablabla"
Be casual unless otherwise specified
Be terse - коротко і по суті
Suggest solutions that I didn't think about—anticipate my needs
Treat me as an expert
Be accurate and thorough
Give the answer immediately - детальні пояснення ПІСЛЯ відповіді якщо потрібно
Value good arguments over authorities, the source is irrelevant
Consider new technologies and contrarian ideas, not just conventional wisdom
High levels of speculation or prediction OK, just flag it for me
No moral lectures
WHEN UPDATING THE CODEBASE BE 100% SURE TO NOT BREAK ANYTHING
Спілкуйся зі мною завжди українською

## 🔴 ОБОВ'ЯЗКОВО НА ПОЧАТКУ КОЖНОЇ СЕСІЇ:

1. ПЕРЕВІР структуру проекту через list_directory()
2. ПЕРЕВІР що в корені 3 основні файли: config.py, main.py, README.md
3. НЕ СТВОРЮЙ нові файли в корені проекту
4. ВСІ тестові скрипти → ТІЛЬКИ в папку scripts/
5. ВСЯ документація → ТІЛЬКИ в папку rules/ (створити якщо немає)
6. Для створення файлів використовуй subprocess.run() або filesystem:write_file
7. НЕ створюй .bat, .cmd файли в корені (тільки якщо явно прошу)
8. Якщо порушиш Critical Rule = зламаєш проект!

## 📁 МІЙ ШЛЯХ ДО ПРОЕКТУ: F:\AiKlientBank\KingLearComic

## 🛠️ ІНСТРУМЕНТИ:

### Для роботи з кодом:
- **filesystem:read_file** - для читання файлів
- **filesystem:write_file** - для створення файлів (НЕ в корені!)
- **filesystem:edit_file** - для редагування коду
- **filesystem:list_directory** - для перегляду структури
- **filesystem:search_files** - для пошуку в проекті
- **filesystem:create_directory** - для створення директорій

### Для запуску Python:
- **subprocess.run()** - ✅ СТВОРЮЄ файли на диску!
- **exec()** - ❌ НЕ створює файли (тільки для аналізу)

### Для перевірки результатів:
- **puppeteer:puppeteer_navigate** - відкрити згенерований HTML
- **puppeteer:puppeteer_screenshot** - зробити скріншот сайту
- **puppeteer:puppeteer_evaluate** - виконати JavaScript для перевірки

## 🚫 КРИТИЧНО ВАЖЛИВО - СТРУКТУРА ПРОЕКТУ:

### ПРАВИЛЬНА структура:
```
F:\AiKlientBank\KingLearComic\
├── config.py         # Конфігурація персонажів
├── main.py          # Головний генератор
├── README.md        # Документація
├── generators/      # Генератори HTML/CSS/JS
│   ├── base.py      # Базовий клас
│   ├── css_lira.py  # CSS генератор
│   ├── html_lira.py # HTML генератор
│   ├── index_gen.py # Генератор головної
│   └── js_lira.py   # JS генератор
├── data/            # Дані проекту
│   ├── characters/  # 12 JSON файлів персонажів
│   ├── books/       # Книги та контент
│   ├── comics/      # Комікси
│   ├── journey/     # Шляхи персонажів
│   ├── journeys/    # Детальні подорожі
│   ├── templates/   # Шаблони
│   └── vocabulary/  # Словники
├── output/          # Згенерований сайт
│   ├── index.html   # Головна сторінка
│   └── journeys/    # 12 HTML сторінок персонажів
├── scripts/         # Допоміжні скрипти
└── rules/           # Правила та інструкції (ТУТ!)
```

## 🚨 ПРАВИЛЬНІ СПОСОБИ ЗАПУСКУ:

### Для генерації сайту (створює файли):
```python
# ✅ ПРАВИЛЬНО - створює файли:
import subprocess
import sys

result = subprocess.run(
    [sys.executable, 'main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)
```

### Для аналізу даних (НЕ створює файли):
```python
# Для читання та аналізу використовуй exec():
exec(open('scripts/check_theatrical_scenes.py', encoding='utf-8').read())
```

### Для створення окремих файлів:
```python
# Через filesystem:
filesystem:write_file(
    path="F:\\AiKlientBank\\KingLearComic\\scripts\\test_report.txt",
    content="Вміст файлу"
)
```

## ⚠️ КРИТИЧНІ ПРАВИЛА ГЕНЕРАЦІЇ:

✅ **ПРАВИЛЬНИЙ підхід:**
- Читай JSON з папки data/characters/
- Генеруй HTML в папку output/journeys/
- Використовуй subprocess.run() для запуску main.py
- Зберігай структуру даних персонажів
- Дотримуйся CHARACTER_ORDER з config.py

❌ **ЗАБОРОНЕНО:**
- Змінювати структуру проекту
- Додавати файли в корінь (крім явної вимоги)
- Створювати .bat файли без запиту
- Видаляти папку data/
- Модифікувати config.py без потреби

## 📋 ПРАВИЛА ПРОЕКТУ:

- **Персонажів:** 12 (король, дочки, слуги, злодії)
- **JSON файлів:** 12 в data/characters/
- **Генерується:** 13 HTML файлів (index + 12 journeys)
- **Етапів подорожі:** 15 для кожного персонажа
- **Німецьких цитат:** 100+ з транскрипцією
- **Python версія:** 3.13
- **Залежності:** Без зовнішніх бібліотек!

## 🎭 ПЕРСОНАЖІ ПРОЕКТУ:

### Головні герої:
1. **king_lear** - Король Лір
2. **cordelia** - Корделія (молодша дочка)
3. **goneril** - Гонерілья (старша дочка)
4. **regan** - Регана (середня дочка)

### Другорядні персонажі:
5. **gloucester** - Граф Глостер
6. **edgar** - Едгар (законний син)
7. **edmund** - Едмунд (незаконний син)
8. **kent** - Граф Кент (вірний слуга)

### Служителі та злодії:
9. **fool** - Шут (блазень)
10. **albany** - Герцог Олбані
11. **cornwall** - Герцог Корнуолл
12. **oswald** - Освальд (слуга)

## 🏗️ СТРУКТУРА МОДУЛІВ:

```
F:\AiKlientBank\KingLearComic\generators\
├── base.py          # Базовий клас генератора
├── css_lira.py      # CSS з градієнтами та анімаціями
├── html_lira.py     # HTML генератор подорожей
├── index_gen.py     # Генератор головної сторінки
└── js_lira.py       # JavaScript для інтерактивності
```

## 🎯 СПЕЦИФІКА ПРОЕКТУ:

- 12 персонажів з унікальними шляхами
- 15 етапів подорожі кожного героя
- Німецькі цитати з транскрипцією [укр]
- Timeline візуалізація подорожі
- Градієнтні картки персонажів
- Responsive дизайн без Bootstrap
- Чистий Python без залежностей

## 📊 АЛГОРИТМ РОБОТИ:

1. Читання JSON персонажів з data/characters/
2. Ініціалізація генераторів (HTML, CSS, JS)
3. Генерація journey HTML для кожного персонажа
4. Створення index.html з картками
5. Збереження в output/
6. Відкриття в браузері

## ✅ ОЧІКУВАНІ РЕЗУЛЬТАТИ:

- **Файлів згенеровано:** 13
- **HTML сторінок:** index.html + 12 journeys
- **Персонажів:** 12 (від короля до слуги)
- **Етапів подорожі:** 15 для кожного
- **Німецьких цитат:** 100+
- **CSS стилів:** Вбудовані inline

## 🔍 ПЕРЕВІРКА РЕЗУЛЬТАТІВ:

### Через Puppeteer:
```javascript
// Відкрити згенерований сайт
puppeteer:puppeteer_navigate({
    url: "file:///F:/AiKlientBank/KingLearComic/output/index.html"
})

// Зробити скріншот
puppeteer:puppeteer_screenshot({
    name: "kinglear_generated",
    width: 1920,
    height: 1080
})

// Перевірити кількість персонажів
puppeteer:puppeteer_evaluate({
    script: `
        const cards = document.querySelectorAll('.character-card');
        console.log('Character cards:', cards.length);
        cards.length
    `
})
```

### Через файлову систему:
```python
# Перевірка створених файлів
from pathlib import Path

output_dir = Path(r'F:\AiKlientBank\KingLearComic\output')
journey_files = list((output_dir / 'journeys').glob('*.html'))
print(f"[OK] Створено journey файлів: {len(journey_files)}")
print(f"[OK] Index.html: {(output_dir / 'index.html').exists()}")
```

## 🚫 КРИТИЧНІ ЗАБОРОНИ:

- НЕ створюй файли в корені проекту без запиту!
- НЕ створюй .BAT файли без явної вимоги!
- НЕ змінюй структуру проекту!
- НЕ видаляй папку data/!
- НЕ модифікуй config.py без обговорення!
- НЕ використовуй Unicode символи в консолі (✓, ✗, →)!
- Використовуй: [OK], [ERROR], [!], [+], [-]

## 🧪 ПРАВИЛА ТЕСТУВАННЯ:

### ВСІ тести ТІЛЬКИ в scripts/:
```python
# Шаблон тестового файлу
"""
Тест: [назва]
Дата: [дата]
Мета: [що тестуємо]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Тестовий код...
```

### Запуск тестів з створенням файлів:
```python
# Через subprocess для створення файлів
result = subprocess.run(
    [sys.executable, 'scripts/generate_report.py'],
    cwd=r'F:\AiKlientBank\KingLearComic'
)
```

### Іменування тестів:
- check_*.py - перевірки
- test_*.py - unit тести
- debug_*.py - налагодження
- validate_*.py - валідація
- generate_*.py - генератори звітів

## 📁 ДОКУМЕНТАЦІЯ ПРОЕКТУ:

### ВСЯ документація в rules/:
- **INSTRUCTION.md** - Ця інструкція (головна!)
- **CRITICAL_RULES.md** - Критичні правила
- **CHARACTER_RULES.md** - Правила персонажів
- **GENERATION_RULES.md** - Правила генерації
- **TESTING_RULES.md** - Правила тестування
- **SUBPROCESS_SOLUTION.md** - Рішення для створення файлів

## 🔄 ШВИДКИЙ ЗАПУСК:

### Для генерації сайту (СТВОРЮЄ файли):
```python
# ПРАВИЛЬНО - через subprocess:
import subprocess
import sys

result = subprocess.run(
    [sys.executable, r'F:\AiKlientBank\KingLearComic\main.py'],
    capture_output=True,
    text=True,
    cwd=r'F:\AiKlientBank\KingLearComic'
)

# Результат: 13 файлів в output/
print(f"[OK] Згенеровано: index.html + 12 journey pages")
```

### Для додавання нового персонажа:
```python
# 1. Створи JSON файл
new_character = {
    "id": "new_character",
    "name": "New Character",
    "title": "Journey of New Character",
    "journey": {
        "stages": [...]
    },
    "quotes": {...}
}

# 2. Збережи в data/characters/
filesystem:write_file(
    path="F:\\AiKlientBank\\KingLearComic\\data\\characters\\new_character.json",
    content=json.dumps(new_character, ensure_ascii=False, indent=2)
)

# 3. Додай в config.py CHARACTER_ORDER
# 4. Запусти генератор
```

## 💡 ПІДСУМОК КРИТИЧНОГО ВІДКРИТТЯ:

**subprocess.run() - це РІШЕННЯ проблеми створення файлів!**

- ✅ subprocess.run() - СТВОРЮЄ файли
- ❌ exec() - НЕ створює файли
- ✅ filesystem:write_file - СТВОРЮЄ файли
- ❌ with open() в python-runner - НЕ створює файли

## ПАМ'ЯТАЙ:

- subprocess.run() ПРАЦЮЄ для створення файлів!
- Структура проекту стабільна - не змінювати без потреби
- 12 персонажів з унікальними подорожами
- ВСІ файли генеруються з data/ в output/
- НІКОЛИ не створюй файли в корені без запиту
- ЗАВЖДИ тести в scripts/
- ЗАВЖДИ документація в rules/
- Без зовнішніх залежностей - чистий Python!
- Простота та надійність - головні принципи!

## 🎨 ВІЗУАЛЬНІ ОСОБЛИВОСТІ:

- **Градієнтні картки** - унікальні для кожного персонажа
- **Timeline подорожі** - 15 етапів з іконками
- **Німецькі цитати** - з транскрипцією [укр]
- **Responsive design** - адаптивний без Bootstrap
- **CSS анімації** - плавні переходи
- **Inline стилі** - все в одному HTML

---

**Версія інструкції:** 1.0
**Дата створення:** 14.09.2025
**Статус проекту:** Production Ready
**Персонажів:** 12 (від Короля до Освальда)
**КРИТИЧНЕ:** subprocess.run() ПРАЦЮЄ для створення файлів!