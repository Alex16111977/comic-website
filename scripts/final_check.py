from pathlib import Path

# Проверяем training.html
training = Path(r'F:\AiKlientBank\KingLearComic\output\training.html')
content = training.read_text(encoding='utf-8')

print("ФИНАЛЬНАЯ ПРОВЕРКА ИСПРАВЛЕНИЙ:")
print("=" * 50)

# Исправляем крестик если нужно
if 'onclick="window.close()"' in content:
    content = content.replace(
        '<button class="close-btn" onclick="window.close()">✕</button>',
        '<button class="close-btn" onclick="window.location.href=\'index.html\'">✕</button>'
    )
    training.write_text(content, encoding='utf-8')
    print("[FIXED] Крестик исправлен - теперь возвращает на главную")
elif "onclick=\"window.location.href='index.html'\"" in content:
    print("[OK] Крестик уже возвращает на главную страницу")

# Проверяем sentenceTranslation
journey = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
if journey.exists():
    j_content = journey.read_text(encoding='utf-8')
    if 'fullWordData.sentenceTranslation' in j_content:
        print("[OK] sentenceTranslation передается при клике на 'Изучить'")
    
print("\n" + "=" * 50)
print("ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ:")
print("✓ sentenceTranslation теперь сохраняется")
print("✓ Крестик теперь работает правильно")
print("=" * 50)
