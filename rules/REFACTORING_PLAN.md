# План рефакторингу King Lear Comic Generator

## 1. Поточний стан проєкту
- Ядро розташоване в `generators/` з файлами `base.py`, `css_lira.py`, `html_lira.py`, `index_gen.py`, `js_lira.py`.
- Допоміжні скрипти знаходяться в `scripts/` (39 файлів, більшість дрібних утиліт).
- Вихідні дані в `data/`, скомпільовані сторінки в `output/`.
- Основний вхід `main.py` створює 12 сторінок подорожей + index.

### Ліміти рядків (>300)
| Файл | Рядків |
| --- | --- |
| `generators/js_lira.py` | 2222 |
| `scripts/update_vocabulary_sentences.py` | 1622 |
| `generators/html_lira.py` | 364 |
| `scripts/create_mobile_test.py` | 322 |
| `scripts/enrich_vocabulary.py` | 419 |

## 2. Цілі рефакторингу
1. Розбити великі моноліти на модулі ≤300 рядків (пріоритет ядра генератора).
2. Вирівняти архітектуру відповідно до заданої цільової структури для CSS/HTML генераторів.
3. Винести загальну функціональність у `utils/` (файли, текст, консоль, валідація).
4. Налаштувати імпорти та `__init__.py` для пакетів, забезпечивши зворотну сумісність `main.py`.
5. Побудувати автоматичну перевірку (`scripts/validate_refactoring.py`) та логування тестів.

## 3. Запропонована нова архітектура
```
generators/
├── base.py                 # Базовий клас генераторів (розширити для спільних методів)
├── css/
│   ├── base_styles.py      # Загальні стилі, змінні, тема (≤150)
│   ├── character_styles.py # Карти персонажів, кольори (≤150)
│   └── animations.py       # Анімації та transition (≤100)
├── html/
│   ├── head_generator.py       # <head>, мета, CSS/JS інклуди (≤100)
│   ├── journey_builder.py      # Побудова контенту сторінок, сцени (≤150)
│   ├── vocabulary_processor.py # Обробка словника, збагачення, квізи (≤100)
│   └── template_engine.py      # Формування фінального HTML, jinja-like (≤100)
├── js/
│   ├── __init__.py
│   ├── serializer.py           # Підготовка JSON-структур (≤120)
│   ├── fragments.py            # Фрагменти JS (модулі, шаблони) (≤120)
│   └── generator.py            # Компонування та експорт (≤150)
├── index_gen.py            # без змін (≤300)
└── __init__.py             # Експортує публічні генератори
```

### Утиліти (`utils/`)
- `file_operations.py` – читання/запис файлів, JSON, бекапи.
- `text_processing.py` – нормалізація, шаблонні підстановки, фільтри.
- `console_output.py` – уніфіковані повідомлення `[INFO] ...`.
- `validation.py` – перевірки структури даних, перевірка довжини файлів.

### Скрипти
- Великі скрипти розбити на пакети в `scripts/` (наприклад, `scripts/update_vocabulary/` з модулями `loader.py`, `processor.py`, `writer.py`, `__main__.py`).
- Створити лог `scripts/refactoring_log.txt` для відмітки кожного етапу.

## 4. Послідовність робіт
1. **Бекап** (`backups/{timestamp}`) – виконано 20250920_135655.
2. **План** – поточний документ.
3. **Рефакторинг ядра CSS/HTML**
   - Створити `utils/` + базові утиліти.
   - Винести функції з `html_lira.py` у нові модулі (`vocabulary_processor`, `journey_builder`, `template_engine`).
   - Переписати `css_lira.py` згідно структури (`base_styles`, `character_styles`, `animations`).
   - Оновити `generators/__init__.py` та `main.py` (імпорти, ASCII вивід через `console_output`).
4. **JS генератор**
   - Створити пакет `generators/js/`.
   - Розділити логіку: серіалізація даних, шаблони JS, складання фінального скрипту.
5. **Скрипти >300 рядків**
   - `scripts/update_vocabulary_sentences.py` → пакет `scripts/update_vocabulary/`.
   - `scripts/enrich_vocabulary.py` → пакет `scripts/enrich_vocabulary/`.
   - `scripts/create_mobile_test.py` → пакет `scripts/mobile_tests/` (розподілити задачі).
   - Залишити точку входу в тому ж місці (`python -m scripts.update_vocabulary`).
6. **Валідація та документація**
   - Оновити `README.md` (нова структура).
   - Створити `rules/NEW_STRUCTURE.md` з описом модулів.
   - Написати `scripts/validate_refactoring.py`.
   - Оновити `scripts/refactoring_log.txt` з результатами тестів.

## 5. Тестування
- Після кожного основного етапу запускати `main.py` через `subprocess.run()`.
- Перевіряти наявність 13 HTML файлів у `output/`.
- Фіксувати результати у `scripts/test_log_{timestamp}.txt`.

## 6. Ризики та стратегії
- **Циркулярні імпорти** – уникати за рахунок чітких пакетів (`utils` без залежності від `generators`).
- **Зміни у форматі даних** – покривати тестами (порівняння JSON структури квізів).
- **Довжина файлів** – автоматична перевірка в `validate_refactoring.py`.

## 7. Артефакти
- `backups/20250920_135655` – повна копія перед змінами.
- Логи тестів у `scripts/test_log_*.txt`.
- Фінальна документація у `rules/NEW_STRUCTURE.md`.
