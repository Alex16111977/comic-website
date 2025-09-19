# Git Workflow для King Lear Comic Generator

## ✅ Статус настройки

**Репозиторий:** https://github.com/Alex16111977/comic-website
**Локальная папка:** F:\AiKlientBank\KingLearComic
**Ветка:** main
**Статус:** ПОДКЛЮЧЕНО и СИНХРОНИЗИРОВАНО

## 📝 Основные команды

### Проверка статуса
```bash
git status
```

### Добавление изменений
```bash
# Добавить все изменения
git add .

# Добавить конкретный файл
git add main.py
```

### Создание коммита
```bash
git commit -m "Описание изменений"
```

### Отправка на GitHub
```bash
git push
```

### Получение изменений с GitHub
```bash
git pull
```

## 🔄 Типичный workflow

1. **Внесли изменения в код**
2. **Проверяем что изменилось:**
   ```bash
   git status
   ```

3. **Добавляем изменения:**
   ```bash
   git add .
   ```

4. **Делаем коммит:**
   ```bash
   git commit -m "feat: добавил нового персонажа"
   ```

5. **Отправляем на GitHub:**
   ```bash
   git push
   ```

## 📋 Примеры коммитов

- `feat: добавил персонажа Goneril`
- `fix: исправил генерацию timeline`
- `docs: обновил README`
- `style: улучшил CSS градиенты`
- `refactor: упростил генератор HTML`

## 🚀 Быстрые команды

### Все изменения одной командой
```bash
git add . && git commit -m "update: обновил проект" && git push
```

### Создал файл для этого:
```bash
scripts\quick_push.bat
```

## ⚠️ Важно

- НЕ коммитьте папку `.venv` (она в .gitignore)
- НЕ коммитьте папку `__pycache__` (она в .gitignore)
- НЕ коммитьте папку `output` если не хотите HTML в репозитории
- ВСЕГДА пишите понятные сообщения коммитов

## 🔍 Полезные команды

### История коммитов
```bash
git log --oneline -10
```

### Отмена последнего коммита (локально)
```bash
git reset --soft HEAD~1
```

### Просмотр изменений
```bash
git diff
```

### Клонирование на другой компьютер
```bash
git clone https://github.com/Alex16111977/comic-website.git
cd comic-website
python main.py
```

## 📱 GitHub Pages (опционально)

Можешь включить GitHub Pages для автоматического хостинга:

1. Зайди в Settings репозитория
2. Найди раздел Pages
3. Source: Deploy from a branch
4. Branch: main
5. Folder: /output (если закоммитишь output папку)

Тогда сайт будет доступен по адресу:
https://alex16111977.github.io/comic-website/

---

**Создано:** 19.09.2025
**Статус:** Git репозиторий полностью настроен и готов к работе
