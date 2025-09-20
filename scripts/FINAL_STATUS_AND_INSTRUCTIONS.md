# ФИНАЛЬНЫЙ СТАТУС И ИНСТРУКЦИИ ПО ИСПРАВЛЕНИЮ ПРИМЕРОВ
**Дата проверки: 20.09.2025**

## 📊 ТЕКУЩИЙ СТАТУС ПРОЕКТА

### ✅ ЗАВЕРШЕНО: 1/12 файлов (8%)
- **cordelia.json** - 56 слов исправлены на простые учебные примеры

### ❌ ТРЕБУЮТ ИСПРАВЛЕНИЯ: 11/12 файлов (92%)

| Файл | Персонаж | Слов с худ. текстом | Статус |
|------|----------|---------------------|--------|
| king_lear.json | Король Лир | 56/56 | 🔴 Критично |
| goneril.json | Гонерилья | 55/55 | 🔴 Критично |
| regan.json | Регана | 53/53 | 🔴 Критично |
| gloucester.json | Глостер | 54/54 | 🟠 Важно |
| edgar.json | Эдгар | 56/56 | 🟠 Важно |
| edmund.json | Эдмунд | 56/56 | 🟠 Важно |
| kent.json | Кент | 53/53 | 🟠 Важно |
| fool.json | Шут | 53/53 | 🟡 Средне |
| albany.json | Олбани | 53/53 | 🟡 Средне |
| cornwall.json | Корнуолл | 53/53 | 🟡 Средне |
| oswald.json | Освальд | 53/53 | 🟡 Средне |

**ИТОГО: 595 слов требуют замены примеров**

## 🎯 ЧТО ИМЕННО НУЖНО ИСПРАВИТЬ

### Примеры ПЛОХИХ (художественных) предложений:
```json
// ❌ ПЛОХО - из king_lear.json
"sentence": "König Lear steht unter dem glühenden Kronleuchter des Thronsaals. Mein Atem zeichnet das Wort „der Thron" in die kalte Luft zwischen uns."

// ❌ ПЛОХО - из goneril.json  
"sentence": "Goneril steht unter dem glühenden Kronleuchter des Thronsaals. Mit jeder Faser meines Körpers verspreche ich: Das Wort „die Lüge" bleibt lebendig."

// ❌ ПЛОХО - из fool.json
"sentence": "Im grellen Licht des Thronsaals schlägt Fool die Laute an. Ich presse das Wort „der Narr" zwischen die Zähne..."
```

### Примеры ХОРОШИХ (учебных) предложений из cordelia.json:
```json
// ✅ ХОРОШО - простое и понятное
"sentence": "Die Wahrheit über den Vorfall wurde gestern bekannt.",
"sentence_translation": "Правда о происшествии стала известна вчера."

// ✅ ХОРОШО - типичное использование
"sentence": "Kannst du mir meinen Fehler bitte verzeihen?",
"sentence_translation": "Можешь ли ты простить мне мою ошибку?"

// ✅ ХОРОШО - жизненная ситуация
"sentence": "Die Hoffnung auf bessere Zeiten stirbt zuletzt.",
"sentence_translation": "Надежда на лучшие времена умирает последней."
```

## 🔍 МАРКЕРЫ ХУДОЖЕСТВЕННОГО ТЕКСТА

Если в примере есть эти слова - он точно требует замены:
- Имена персонажей: Lear, Goneril, Cordelia, Edgar, Edmund, Gloucester, Kent, Fool, Albany, Cornwall, Oswald
- Театральные локации: Thronsaal, Kronleuchter, Thron, Krone, Burg, Schloss
- Художественные фразы:
  - "Ich presse das Wort ... zwischen die Zähne"
  - "Mein Atem zeichnet das Wort..."  
  - "Ich umarme das Wort..."
  - "wie geschmolzenes Gold erscheinen"
  - "Mit jeder Faser meines Körpers"
  - "Das Echo des Wortes übertönt..."

## 📝 ПОШАГОВАЯ ИНСТРУКЦИЯ

### ШАГ 1: Выбрать персонажа по приоритету
1. king_lear.json (главный герой)
2. goneril.json (старшая дочь)
3. regan.json (средняя дочь)
4. gloucester.json (граф)
5. edgar.json (сын)
6. edmund.json (бастард)
7. kent.json (слуга)
8. fool.json (шут)
9. albany.json (герцог)
10. cornwall.json (герцог)
11. oswald.json (слуга)

### ШАГ 2: Открыть файл и найти vocabulary
```python
import json
with open('F:\\AiKlientBank\\KingLearComic\\data\\characters\\[персонаж].json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### ШАГ 3: Для каждого слова создать новый пример
Структура замены:
```json
{
  "german": "НЕ МЕНЯТЬ",
  "russian": "НЕ МЕНЯТЬ", 
  "transcription": "НЕ МЕНЯТЬ",
  "sentence": "ЗАМЕНИТЬ на простое предложение 5-12 слов",
  "sentence_translation": "ЗАМЕНИТЬ на точный перевод",
  "sentence_parts": ["ОБНОВИТЬ", "разбивку на части"]
}
```

### ШАГ 4: Сохранить исправленный файл
```python
with open('F:\\AiKlientBank\\KingLearComic\\data\\characters\\[персонаж].json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## ✅ КРИТЕРИИ КАЧЕСТВА

### Каждое новое предложение должно быть:
1. **Простым** - уровень B1-B2, без сложных конструкций
2. **Коротким** - 5-12 слов максимум
3. **Реальным** - из повседневной жизни, не из театра
4. **Типичным** - показывать обычное использование слова
5. **Понятным** - легко переводиться на русский

## 📊 ПРОГРЕСС-ТРЕКЕР

```
[✅] cordelia.json    - 56/56 слов - ГОТОВО
[  ] king_lear.json   - 0/56 слов  - В РАБОТЕ
[  ] goneril.json     - 0/55 слов  - ОЖИДАЕТ
[  ] regan.json       - 0/53 слов  - ОЖИДАЕТ
[  ] gloucester.json  - 0/54 слов  - ОЖИДАЕТ
[  ] edgar.json       - 0/56 слов  - ОЖИДАЕТ
[  ] edmund.json      - 0/56 слов  - ОЖИДАЕТ
[  ] kent.json        - 0/53 слов  - ОЖИДАЕТ
[  ] fool.json        - 0/53 слов  - ОЖИДАЕТ
[  ] albany.json      - 0/53 слов  - ОЖИДАЕТ
[  ] cornwall.json    - 0/53 слов  - ОЖИДАЕТ
[  ] oswald.json      - 0/53 слов  - ОЖИДАЕТ

ОБЩИЙ ПРОГРЕСС: 56/651 слов (8.6%)
```

## 🎓 БАНК ПРИМЕРОВ ДЛЯ ТИПИЧНЫХ СЛОВ

### Власть и управление:
```json
"die Macht" → "Die Macht des Gesetzes schützt die Bürger."
"herrschen" → "In diesem Haus herrscht immer gute Stimmung."
"befehlen" → "Der Arzt befahl absolute Bettruhe."
"das Königreich" → "Das Königreich Norwegen ist sehr schön."
```

### Семья и отношения:
```json
"der Vater" → "Mein Vater arbeitet als Ingenieur."
"die Tochter" → "Ihre Tochter studiert Medizin in München."
"der Erbe" → "Der Erbe des Unternehmens ist noch minderjährig."
"die Familie" → "Die ganze Familie trifft sich am Sonntag."
```

### Эмоции:
```json
"der Zorn" → "Sein Zorn legte sich nach einigen Minuten."
"die Wut" → "Die Wut über die Ungerechtigkeit war groß."
"die Trauer" → "Die Trauer dauerte mehrere Monate."
"die Freude" → "Die Freude über den Sieg war unbeschreiblich."
```

### Действия:
```json
"verlassen" → "Wir müssen das Gebäude sofort verlassen."
"kämpfen" → "Die Mannschaft kämpft um den ersten Platz."
"retten" → "Die Ärzte konnten sein Leben retten."
"fliehen" → "Die Familie musste aus dem Land fliehen."
```

## 🚀 КОМАНДА ДЛЯ БЫСТРОГО СТАРТА

```python
"""
Скрипт для исправления примеров персонажа
"""
import json
from pathlib import Path

# Выберите персонажа для исправления
CHARACTER = 'king_lear'  # Измените на нужного персонажа

# Путь к файлу
file_path = Path(f'F:\\AiKlientBank\\KingLearComic\\data\\characters\\{CHARACTER}.json')

# Читаем файл
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Здесь нужно обновить примеры для каждого слова
# ...

# Сохраняем результат
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[OK] Файл {CHARACTER}.json исправлен!")
```

## 📌 ВАЖНЫЕ НАПОМИНАНИЯ

1. **НЕ МЕНЯТЬ** поля: german, russian, transcription
2. **ОБЯЗАТЕЛЬНО МЕНЯТЬ**: sentence, sentence_translation, sentence_parts
3. **БЕЗ ПЕРСОНАЖЕЙ** пьесы в примерах
4. **БЕЗ ТЕАТРАЛЬНЫХ** сцен и описаний
5. **ТОЛЬКО ПРОСТЫЕ** жизненные ситуации

## 🏁 КОНЕЧНАЯ ЦЕЛЬ

После исправления всех файлов:
- ✅ 12 файлов с правильными примерами
- ✅ 651 учебное предложение
- ✅ 0 художественных текстов
- ✅ Готовый учебный сайт немецкого языка

---

**СТАТУС:** Требуется исправить 595 слов в 11 файлах
**ПРИОРИТЕТ:** Высокий - сайт уже работает, но примеры непригодны для обучения
**ВРЕМЯ НА ИСПРАВЛЕНИЕ:** ~2-3 часа на все файлы