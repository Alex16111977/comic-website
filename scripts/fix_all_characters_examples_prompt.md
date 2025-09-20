# ПРОМПТ ДЛЯ МАССОВОГО ИСПРАВЛЕНИЯ ПРИМЕРОВ ВСЕХ ПЕРСОНАЖЕЙ

## 📊 ТЕКУЩИЙ СТАТУС (20.09.2025)

### ✅ УЖЕ ИСПРАВЛЕНО:
1. **cordelia.json** - ВСЕ 56 слов исправлены на простые учебные примеры

### ❌ ТРЕБУЮТ ИСПРАВЛЕНИЯ (11 файлов):
1. **king_lear.json** - 56 слов (главный герой)
2. **goneril.json** - 56 слов (старшая дочь) 
3. **regan.json** - 56 слов (средняя дочь)
4. **gloucester.json** - 56 слов (граф)
5. **edgar.json** - 56 слов (законный сын)
6. **edmund.json** - 56 слов (незаконный сын)
7. **kent.json** - 56 слов (верный слуга)
8. **fool.json** - 56 слов (шут)
9. **albany.json** - 56 слов (герцог)
10. **cornwall.json** - 56 слов (герцог)
11. **oswald.json** - 56 слов (слуга)

**ИТОГО:** 616 слов требуют исправления (11 персонажей × 56 слов)

## 🎯 ЗАДАЧА

Исправить ВСЕ примеры (поля "sentence" и "sentence_translation") во всех оставшихся файлах персонажей в папке `F:\AiKlientBank\KingLearComic\data\characters\`

## ⚠️ ГЛАВНАЯ ПРОБЛЕМА

Сейчас во всех файлах вместо учебных примеров - художественные тексты про персонажей пьесы "Король Лир". Это НЕ подходит для изучения немецкого языка!

### Примеры ПЛОХИХ предложений (из текущих файлов):
```json
// king_lear.json - ПЛОХО!
"sentence": "Auf dem Thron sitzend betrachtet Lear die ausgerollte Landkarte. Ich presse das Wort „die Macht" zwischen die Zähne..."

// goneril.json - ПЛОХО!  
"sentence": "Im hallenden Thronsaal verneigt sich Goneril tief vor Lear. Das kalte Licht lässt das Wort „die Liebe" wie geschmolzenes Gold erscheinen."

// fool.json - ПЛОХО!
"sentence": "Mit bunten Flicken am Narrenkostüm wirbelt der Fool um Lear herum..."
```

## ✅ ТРЕБОВАНИЯ К ИСПРАВЛЕНИЮ

### Для КАЖДОГО слова в vocabulary КАЖДОГО персонажа:

1. **Заменить "sentence"** → простое учебное предложение (5-12 слов)
2. **Заменить "sentence_translation"** → точный русский перевод
3. **Обновить "sentence_parts"** → разбить на 2-3 логические части
4. **НЕ МЕНЯТЬ** поля: german, russian, transcription

### КРИТЕРИИ ХОРОШИХ ПРИМЕРОВ:
- ✅ Простые и понятные для уровня B1-B2
- ✅ Демонстрируют типичное использование слова
- ✅ БЕЗ персонажей пьесы (Лир, Гонерилья, Шут и т.д.)
- ✅ БЕЗ художественных описаний
- ✅ БЕЗ сложных конструкций
- ✅ Реальные жизненные ситуации

## 📝 ЭТАЛОННЫЕ ПРИМЕРЫ (из исправленной Корделии)

### ХОРОШО - Простые учебные предложения:
```json
{
  "german": "die Wahrheit",
  "russian": "правда",
  "sentence": "Die Wahrheit über den Vorfall wurde gestern bekannt.",
  "sentence_translation": "Правда о происшествии стала известна вчера.",
  "sentence_parts": [
    "Die Wahrheit über den Vorfall",
    "wurde gestern bekannt."
  ]
}

{
  "german": "verzeihen",
  "russian": "прощать",
  "sentence": "Kannst du mir meinen Fehler bitte verzeihen?",
  "sentence_translation": "Можешь ли ты простить мне мою ошибку?",
  "sentence_parts": [
    "Kannst du mir meinen Fehler",
    "bitte verzeihen?"
  ]
}

{
  "german": "die Hoffnung",
  "russian": "надежда",
  "sentence": "Die Hoffnung auf bessere Zeiten stirbt zuletzt.",
  "sentence_translation": "Надежда на лучшие времена умирает последней.",
  "sentence_parts": [
    "Die Hoffnung auf bessere Zeiten",
    "stirbt zuletzt."
  ]
}
```

## 🔧 АЛГОРИТМ ИСПРАВЛЕНИЯ

### ДЛЯ КАЖДОГО ПЕРСОНАЖА:
1. Открыть файл персонажа (например, king_lear.json)
2. Найти секцию "vocabulary" в КАЖДОЙ из 7 фаз
3. Для КАЖДОГО из 8 слов в фазе:
   - Создать простое предложение с этим словом
   - Перевести на русский
   - Разбить на части
4. Сохранить исправленный файл

## 📊 СТРУКТУРА ФАЙЛОВ ПЕРСОНАЖЕЙ

Каждый файл содержит 7 фаз journey_phases:
1. **Фаза 1** - начало истории (8 слов)
2. **Фаза 2** - развитие конфликта (8 слов)
3. **Фаза 3** - кульминация 1 (8 слов)
4. **Фаза 4** - поворот сюжета (8 слов)
5. **Фаза 5** - кульминация 2 (8 слов)
6. **Фаза 6** - развязка (8 слов)
7. **Фаза 7** - финал (8 слов)

**Итого:** 7 фаз × 8 слов = 56 слов на персонажа

## ⚡ ПРИОРИТЕТ ИСПРАВЛЕНИЯ

### ПЕРВАЯ ОЧЕРЕДЬ (главные персонажи):
1. **king_lear.json** - центральный персонаж
2. **goneril.json** - старшая дочь
3. **regan.json** - средняя дочь

### ВТОРАЯ ОЧЕРЕДЬ (важные персонажи):
4. **gloucester.json** - второй по важности граф
5. **edgar.json** - положительный герой
6. **edmund.json** - главный антагонист
7. **kent.json** - верный друг

### ТРЕТЬЯ ОЧЕРЕДЬ (второстепенные):
8. **fool.json** - шут
9. **albany.json** - муж Гонерильи
10. **cornwall.json** - муж Реганы
11. **oswald.json** - слуга

## 🎓 ТЕМАТИКИ ДЛЯ ПРИМЕРОВ

Используй разнообразные жизненные ситуации:
- 📚 Учёба и образование
- 💼 Работа и карьера
- 👨‍👩‍👧‍👦 Семья и отношения
- 🏠 Дом и быт
- 🚗 Путешествия и транспорт
- 🏥 Здоровье и медицина
- 🛒 Покупки и услуги
- 🎭 Культура и развлечения
- ⚖️ Право и общество
- 🌍 Природа и экология

## 💡 ПРИМЕРЫ ЗАМЕН ДЛЯ ТИПИЧНЫХ СЛОВ

### Власть и управление:
- **die Macht** → "Die Macht des neuen Gesetzes ist begrenzt."
- **herrschen** → "Der König herrscht über das ganze Land."
- **befehlen** → "Der General befahl den sofortigen Rückzug."

### Эмоции и чувства:
- **der Zorn** → "Der Zorn des Chefs war deutlich zu spüren."
- **die Wut** → "Seine Wut legte sich nach einigen Minuten."
- **die Trauer** → "Die Trauer über den Verlust war groß."

### Семейные отношения:
- **die Tochter** → "Meine Tochter studiert Medizin in Berlin."
- **der Vater** → "Der Vater bringt die Kinder zur Schule."
- **die Familie** → "Die ganze Familie trifft sich zum Abendessen."

### Действия и поступки:
- **verlassen** → "Wir müssen das Gebäude sofort verlassen."
- **kämpfen** → "Die Mannschaft kämpft um den ersten Platz."
- **retten** → "Die Feuerwehr konnte alle Menschen retten."

## 🚫 ЧЕГО ИЗБЕГАТЬ

❌ НЕ использовать имена персонажей (Lear, Cordelia, Goneril, etc.)
❌ НЕ писать "Король на троне..." или "Шут танцует..."
❌ НЕ создавать театральные сцены
❌ НЕ использовать архаичные обороты
❌ НЕ делать предложения длиннее 12 слов
❌ НЕ использовать сложноподчинённые конструкции

## ✅ КОНТРОЛЬНЫЙ ЧЕКЛИСТ

После исправления КАЖДОГО файла проверить:
- [ ] ВСЕ 56 слов имеют новые примеры
- [ ] НЕТ упоминаний персонажей пьесы
- [ ] Предложения простые (5-12 слов)
- [ ] Переводы точные и естественные
- [ ] sentence_parts правильно разбиты
- [ ] Примеры подходят для уровня B1-B2

## 🎯 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ

### После исправления всех файлов:
- ✅ 12 файлов персонажей (включая cordelia.json)
- ✅ 672 учебных примера (12 × 56)
- ✅ 0 художественных текстов
- ✅ 100% готовность для изучения немецкого

## 📋 ПОРЯДОК ВЫПОЛНЕНИЯ

1. **Прочитать файл** персонажа
2. **Извлечь все слова** из vocabulary
3. **Создать простые примеры** для каждого слова
4. **Заменить** старые примеры новыми
5. **Сохранить** исправленный файл
6. **Перейти** к следующему персонажу
7. **Повторить** для всех 11 оставшихся файлов

## 💾 КОМАНДА ДЛЯ ЗАПУСКА

```python
# Пример обработки одного персонажа
import json

# 1. Читаем файл
with open('F:\\AiKlientBank\\KingLearComic\\data\\characters\\king_lear.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Для каждой фазы и каждого слова
for phase in data['journey_phases']:
    for word in phase['vocabulary']:
        # 3. Заменяем примеры
        word['sentence'] = "НОВОЕ ПРОСТОЕ ПРЕДЛОЖЕНИЕ"
        word['sentence_translation'] = "ПЕРЕВОД"
        word['sentence_parts'] = ["ЧАСТЬ 1", "ЧАСТЬ 2"]

# 4. Сохраняем
with open('F:\\AiKlientBank\\KingLearComic\\data\\characters\\king_lear.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## 🏆 КРИТЕРИЙ УСПЕХА

**ВСЕ 672 примера во ВСЕХ 12 файлах персонажей должны быть:**
- Простыми учебными предложениями
- БЕЗ персонажей пьесы
- Уровня B1-B2
- С точными переводами
- Готовыми для изучения немецкого языка

---

**ВАЖНО:** Это массовая операция по исправлению 616 примеров в 11 файлах. Требуется систематический подход и внимание к деталям!

**СРОЧНОСТЬ:** Высокая - сайт уже сгенерирован, но примеры непригодны для обучения!

**РЕЗУЛЬТАТ:** После исправления - полноценный учебный сайт немецкого языка через историю Короля Лира!