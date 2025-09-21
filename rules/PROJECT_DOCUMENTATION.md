# 📚 Повна документація проекту **King Lear Comic Generator**

## 1. Призначення та бачення
- **Мета**: автоматизована генерація навчального веб-сайту рівня B1 з німецької мови на основі трагедії Шекспіра «Король Лір».
- **Функціонал**: створює головну сторінку з картками та 12 детальних сторінок подорожей персонажів із театральними сценами, словником і інтерактивними вправами.
- **Ключова ідея**: використовувати емоційний сюжет для закріплення лексики та граматики через практику (підбір слів, вікторини, конструктори речень).

## 2. Структура репозиторію
```
F:\AiKlientBank\KingLearComic\
├── config.py                 # Глобальна конфігурація, шляхи та порядок персонажів
├── main.py                   # Точка входу генератора
├── data\
│   ├── characters\           # 12 JSON-файлів персонажів
│   ├── journey\              # Допоміжні сценарії подорожей
│   ├── comics\               # Візуальні матеріали (опційно)
│   └── vocabulary\           # Загальний словник vocabulary.json
├── generators\
│   ├── base.py               # Базовий рендерер (Jinja2)
│   ├── html_lira.py          # Збірка сторінок подорожей
│   ├── index_gen.py          # Головна сторінка
│   ├── css_lira.py           # Менеджер CSS-ресурсів
│   ├── js_lira.py            # Експортер JS-пакету
│   ├── html\...              # Модулі для фаз, словника, head-секції
│   └── js\...                # Серіалізація даних для браузера
├── templates\               # Jinja2-шаблони: index.html, journey.html, training.html
├── static\                  # Базові CSS/JS/шрифти (копіюються в output/static)
├── output\                  # Результат генерації: index.html, journeys/, static/
├── scripts\                 # Утиліти та тести
├── utils\                   # Допоміжні функції (обробка тексту)
└── rules\                   # Документація проекту (цей файл, інструкції)
```

## 3. Потік генерації
1. **Запуск**: `python main.py` (Windows) або `python3 main.py` (Linux/macOS). Рекомендовано через `subprocess.run()` для скриптів.
2. **Підготовка виводу**: створення `output/`, підпапок `journeys/` і копіювання `static/` + `training.html`.
3. **Збір даних**: послідовне читання JSON-файлів у порядку `config.CHARACTER_ORDER` (12 персонажів).
4. **Збагачення словника**: `VocabularyProcessor` додає відсутні підказки з `data/vocabulary/vocabulary.json`.
5. **Побудова фаз**: `JourneyBuilder` формує таймлайн, словник, вправи з пропусками, вікторини та конструктори речень.
6. **Генерація JS**: `LiraJSGenerator` серіалізує фази в глобальні структури (`window.phaseData`, ключі збереження прогресу).
7. **Рендер сторінки**: `JourneyTemplateEngine` підставляє дані у `templates/journey.html`.
8. **Головна сторінка**: `IndexGenerator` створює сітку карток з першою іконкою фази й кількістю етапів.
9. **Післязапуск**: спроба автоматично відкрити `output/index.html` у браузері.

## 4. Конфігурація (`config.py`)
- `BASE_DIR`, `DATA_DIR`, `OUTPUT_DIR`, `CHARACTERS_DIR`, `TEMPLATES_DIR`, `GENERATORS_DIR` — централізовані шляхи.
- `CHARACTER_ORDER` — **критичний** порядок від головних до слуг. Не змінювати без узгодження.
- `THEME_COLORS` — глобальна палітра (primary, secondary, accent, text, background).

## 5. Дані персонажів (`data/characters/*.json`)
### 5.1. Мінімальна структура
```json
{
  "id": "king_lear",
  "name": "König Lear",
  "title": "Путь Короля Лира",
  "gradient": ["#8B4513", "#CD853F"],
  "journey": {
    "stages": [
      {
        "id": "throne",
        "title": "Тронный зал",
        "icon": "👑",
        "german_words": ["der Thron", "die Macht"],
        "narrative": "...",
        "emotional_peak": "..."
      }
    ]
  },
  "journey_phases": [
    {
      "id": "phase-0",
      "title": "...",
      "description": "...",
      "icon": "👑",
      "theatrical_scene": {
        "title": "...",
        "narrative": "<b>der Thron (трон)</b> ...",
        "exercise_text": "... ___ (трон) ..."
      },
      "vocabulary": [
        {
          "german": "der Thron",
          "russian": "трон",
          "russian_hint": "символ влади",
          "transcription": "[дер ТРОН]",
          "sentence": "...",
          "sentence_translation": "...",
          "sentence_parts": ["der", "Thron", "ist", "..."],
          "synonyms": ["der Sitz"],
          "themes": ["Monarchie"],
          "visual_hint": "throne.png"
        }
      ],
      "quizzes": [
        {
          "question": "Що означає «der Thron»?",
          "choices": ["трон", "король", "замок"],
          "correct_index": 0
        }
      ]
    }
  ]
}
```

### 5.2. Автоматичні доповнення
- Відсутні `synonyms`, `themes`, `visual_hint` додаються із глобального словника (VocabularyProcessor).
- `sentence_parts` створюють задачі drag & drop; потрібен щонайменше двоелементний масив.
- `theatrical_scene.exercise_text` підтримує патерн `___ (підказка)` — під час генерації підставляється `<span class="blank" data-answer="...">`.
- Якщо немає `quizzes`, генератор створить питання за словником фази.

## 6. Генератори та підсистеми
| Модуль | Роль |
|--------|------|
| `generators/base.py` | Фундамент: Jinja2, зчитування/запис файлів, завантаження JSON.
| `generators/html_lira.py` | Координує збагачення даних і рендер `journey.html`.
| `generators/html/journey_builder.py` | Формує фази, вправи, вікторини, словникові конструктори.
| `generators/html/head_generator.py` | Готує заголовок сторінки (опис, прогрес, титул першої фази).
| `generators/html/template_engine.py` | Проксі до Jinja2-шаблону.
| `generators/html/vocabulary_processor.py` | Поєднує локальні слова з глобальним словником, будує метадані відносин.
| `generators/js_lira.py` + `generators/js/*` | Серіалізація фаз у JS (`window.phaseData`, ключі localStorage).
| `generators/css_lira.py` | Керує CSS-файлами (`static/css/journey.css`) і анімаціями.
| `generators/index_gen.py` | Побудова головної сторінки (картки персонажів, посилання на journeys/ID.html).

## 7. Шаблони та стилі
- **`templates/journey.html`**: містить таймлайн, секції «Theatrical Scenes», «Vocabulary», «Exercises», «Quiz Deck».
- **`templates/index.html`**: грід карток персонажів із градієнтами й лічильником фаз.
- **`templates/training.html`**: додаткова сторінка для теорії/повторення (копіюється в `output/`).
- **CSS**: базові стилі у `static/css/journey.css` та `static/css/index.css`. Персональні теми — через `LiraCSSGenerator.register_theme()` або правки файлів.
- **JS**: згенерований скрипт вбудовується inline у HTML та використовує глобальні константи (`STORAGE_PREFIX`, `REVIEW_QUEUE_KEY`).

## 8. Запуск і автоматизація
### 8.1. Ручний запуск
```bash
cd F:\AiKlientBank\KingLearComic
python main.py
```
Після завершення відкриється `output/index.html`.

### 8.2. Через Python-скрипт
```python
import subprocess, sys
subprocess.run([
    sys.executable,
    'main.py'
], cwd=r'F:\\AiKlientBank\\KingLearComic', check=True)
```

### 8.3. Перевірка результату
```python
from pathlib import Path
project = Path(r'F:\\AiKlientBank\\KingLearComic')
print('JSON персонажів:', len(list((project/'data/characters').glob('*.json'))))
print('Згенеровано сторінок:', len(list((project/'output/journeys').glob('*.html'))))
```

## 9. Типові робочі сценарії
1. **Додати нове слово персонажу**
   - Відкрити `data/characters/<id>.json`.
   - Додати елемент у `journey_phases[n].vocabulary`.
   - Заповнити `sentence`, `sentence_translation`, `sentence_parts` (мін. 2 частини).
   - Запустити `python main.py`.

2. **Налаштувати стиль**
   - Правити `static/css/journey.css` або використовувати `LiraCSSGenerator.register_theme()` у кастомному скрипті.
   - Оновити градієнти в JSON (`gradient` масив).

3. **Додати нову вправу**
   - У фазі додати/оновити `theatrical_scene.exercise_text` з підказками `___ (слово)`.
   - За потреби додати власні `quizzes` з полями `question`, `choices`, `correct_index`.

4. **Створити нового персонажа**
   - Скопіювати наявний JSON як шаблон.
   - Надати унікальний `id`, `name`, `journey_phases` (7–15 етапів рекомендовано).
   - Додати `id` у `CHARACTER_ORDER`.

## 10. Правила розробки
- ✅ Можна редагувати файли всередині `generators/`, `data/characters/`, `scripts/`, `static/`.
- ✅ Документація — **лише** в `rules/`.
- ❌ Не створювати файли в корені (`F:\AiKlientBank\KingLearComic`).
- ❌ Не видаляти `data/` і не змінювати формат JSON без попередньої домовленості.
- ❌ Без сторонніх бібліотек — використовується стандартний Python + Jinja2 (див. `requirements.txt`).
- ❌ Зберігати порядок персонажів (`CHARACTER_ORDER`).

## 11. Тестування та скрипти
| Скрипт | Призначення |
|--------|-------------|
| `scripts/check_exercise_data.py` | Валідація вправ та пропусків у сценах.
| `scripts/test_exercises.py` | Перевірка логіки вправ.
| `scripts/test_new_exercises.py` | Тестування нових інтерактивів.
| `scripts/analyze_runtime.py` | Аналіз продуктивності генерації.
| `scripts/apply_exercises_patch.py` | Масове оновлення структур вправ.
| `scripts/refactor_js.py` | Оновлення JS-даних для сторінок.

> Всі тести запускати командою `python scripts/<назва>.py` з кореня проекту або через `subprocess.run()`.

## 12. Вивід та розгортання
- Результат у `output/`: `index.html`, `journeys/*.html`, `static/`.
- Файли містять inline CSS/JS для швидкого розгортання без бекенда.
- `output/static` дублює `static/` для кешування браузером.
- Для публікації достатньо розмістити вміст `output/` на будь-якому статичному хостингу.

## 13. Усунення неполадок
| Симптом | Причина | Рішення |
|---------|---------|---------|
| `[MISSING] <id>.json` | Відсутній файл персонажа або помилка в `CHARACTER_ORDER` | Переконайтеся, що JSON існує в `data/characters/` і назва збігається з `id`.
| `Status: [WARNING] PARTIAL SUCCESS` | Згенеровано не всі 12 сторінок | Перевірити лог помилок для конкретного персонажа.
| Порожні вправи | Відсутні `___ (підказка)` або словникові пари | Заповнити `exercise_text` і `vocabulary`.
| Немає вікторин | Фаза не містить словникових пар | Додати `vocabulary` або явні `quizzes`.
| Неправильний градієнт | Масив `gradient` < 2 кольорів | Додати два шістнадцяткові кольори.

## 14. Контрольний список перед комітом
- [ ] `python main.py` завершується без помилок.
- [ ] Усі 12 `journeys/*.html` оновлені.
- [ ] Дані персонажів містять 7–15 фаз.
- [ ] Вправи, вікторини й словник мають переклад та транскрипцію.
- [ ] Стилі/JS не мають зовнішніх залежностей.
- [ ] Документація (за потреби) додана до `rules/`.

## 15. Корисні поради
- Використовуйте `utils/text_processing.collapse_whitespace()` для нормалізації тексту при постобробці.
- Для slug-ідентифікаторів скористайтесь `utils.text_processing.slugify()`.
- Зберігайте іконки фаз у форматі emoji — вони потрапляють на картки персонажів.
- Виносьте повторювану лексику в `data/vocabulary/vocabulary.json`, щоб автоматично заповнювати підказки.
- Пам’ятайте, що локальне сховище в браузері (localStorage) використовує ключ `liraJourney` — це полегшує відладку прогресу учня.

---
**Версія документації:** 1.0  
**Дата оновлення:** 2025-09-14  
**Автори:** команда King Lear Comic Generator
