"""
Скрипт для додавання слова die Zeremonie з прикладом в localStorage
Виконайте цей код в консолі браузера на сторінці output/index.html
"""

# JavaScript код для вставки в консоль браузера:
js_code = """
// Додаємо слово die Zeremonie з прикладом
const testWord = {
    id: "die_zeremonie", 
    word: "die Zeremonie",
    translation: "церемония",
    transcription: "[ди це-ре-мо-НИ]",
    emoji: "👸",
    level: "A2",
    theme: "royal",
    // Додаємо приклади використання
    examples: [
        {
            character: "Корделія",
            characterId: "cordelia",
            phase: "Тронный зал",
            phaseNumber: "Етап 1",
            german: "Neben der ausgerollten Reichskarte beugt sich Cordelia über Lears schweren Tisch. Ich atme tief ein und lasse nur das Wort „die Zeremonie" wieder hinaus.",
            russian: "У развернутой карты королевства Корделия склоняется над тяжёлым столом Лира. Я глубоко вдыхаю и выпускаю только слово «церемония»."
        }
    ],
    addedAt: new Date().toISOString()
};

// Зберігаємо в localStorage
localStorage.setItem('liraJourney:studyWords', JSON.stringify([testWord]));

console.log('✅ Слово die Zeremonie додано з прикладом!');
console.log('Тепер оновіть сторінку та натисніть "Тренировка"');
"""

print("=" * 60)
print("ІНСТРУКЦІЯ ДЛЯ ТЕСТУВАННЯ")
print("=" * 60)
print("\n1. Відкрийте output/index.html в браузері")
print("2. Відкрийте консоль (F12)")
print("3. Вставте наступний код:")
print("-" * 60)
print(js_code)
print("-" * 60)
print("\n4. Оновіть сторінку (F5)")
print("5. Побачите 'die Zeremonie' в розділі 'Повторить сегодня'")
print("6. Натисніть 'Тренировка'")
print("\n✅ Приклад має відобразитися!")
