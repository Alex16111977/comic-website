"""
Тест тренування з реальними словами з JSON файлів
Дата: 20.09.2025
"""
import json
from pathlib import Path

print("[!] Перевірка доступних слів для тренування\n")

# Шукаємо слова з прикладами в king_lear.json
char_file = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')

with open(char_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Збираємо слова з прикладами
test_words = []
if 'journey_phases' in data:
    for phase in data['journey_phases'][:3]:  # перші 3 фази
        if 'vocabulary' in phase:
            for vocab in phase['vocabulary']:
                if 'sentence' in vocab and vocab['sentence']:
                    test_words.append({
                        'id': vocab['german'].replace(' ', '_').lower(),
                        'word': vocab['german'],
                        'translation': vocab['translation'],
                        'transcription': vocab.get('transcription', ''),
                        'sentence': vocab['sentence']
                    })
                    if len(test_words) >= 3:
                        break
        if len(test_words) >= 3:
            break

print("[OK] Знайдені слова з прикладами для тестування:\n")
for w in test_words:
    print(f"• {w['word']} - {w['translation']}")
    print(f"  ID: {w['id']}")
    print(f"  Приклад: \"{w['sentence'][:60]}...\"")
    print()

# Створюємо тестовий об'єкт для localStorage
test_storage = json.dumps(test_words, ensure_ascii=False, indent=2)

print("\n[!] Для тестування:")
print("1. Відкрийте output/index.html")
print("2. У консолі браузера виконайте:")
print(f"   localStorage.setItem('liraJourney:studyWords', `{test_words[0]}`)")
print(f"3. Оновіть сторінку - побачите слово '{test_words[0]['word']}' в розділі 'Повторить сегодня'")
print(f"4. Натисніть 'Тренировка' - відкриється training.html?word={test_words[0]['id']}")
print("5. Система знайде приклади цього слова в тексті персонажів")

print("\n[!] ВАЖЛИВО:")
print("• Слово 'die Zeremonie' НЕ працює, бо його немає в JSON файлах")
print("• Використовуйте слова зі списку вище для тестування")
print("• Або додайте 'die Zeremonie' в vocabulary персонажа з прикладом речення")
