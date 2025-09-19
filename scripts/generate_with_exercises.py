"""
Прямая генерация HTML для King Lear с упражнениями
"""
import json
from pathlib import Path

# Загружаем данные
json_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')
with open(json_path, 'r', encoding='utf-8') as f:
    character = json.load(f)

print(f"[LOADED] {character['name']}")

# Проверяем наличие exercise_text
for i, phase in enumerate(character['journey_phases']):
    if 'theatrical_scene' in phase:
        scene = phase['theatrical_scene']
        has_exercise = 'exercise_text' in scene
        print(f"  Phase {i+1} ({phase['title']}): has exercise = {has_exercise}")

# CSS стили
css = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: 'Inter', -apple-system, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
h1 {
    color: #2d3748;
    font-size: 2.5em;
    margin-bottom: 10px;
    text-align: center;
}
.subtitle {
    color: #718096;
    text-align: center;
    margin-bottom: 40px;
}
.theatrical-scene {
    background: linear-gradient(135deg, #f6f8fb 0%, #e9ecf1 100%);
    border: 1px solid rgba(102, 126, 234, 0.2);
    padding: 35px;
    border-radius: 20px;
    margin: 30px 0;
    box-shadow: 0 5px 25px rgba(0,0,0,0.08);
}
.scene-title {
    color: #2d3748;
    font-size: 1.8em;
    font-weight: 700;
    margin-bottom: 25px;
    text-align: center;
    text-transform: uppercase;
    border-bottom: 3px solid #667eea;
    padding-bottom: 15px;
}
.scene-narrative {
    color: #4a5568;
    font-size: 1.15em;
    line-height: 1.9;
    margin-bottom: 25px;
    text-align: justify;
}
.scene-narrative b {
    color: #667eea;
    font-weight: 700;
    background: linear-gradient(180deg, transparent 60%, rgba(102, 126, 234, 0.15) 60%);
    padding: 0 2px;
}
.emotional-peak {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 4px solid #667eea;
    color: #2d3748;
    font-size: 1.1em;
    font-style: italic;
    margin-top: 25px;
}
.exercise-section {
    background: linear-gradient(135deg, #fff9e6 0%, #fff4d6 100%);
    border: 2px solid #f6ad55;
    padding: 30px;
    border-radius: 15px;
    margin-top: 35px;
}
.exercise-title {
    color: #d97706;
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
    text-transform: uppercase;
}
.exercise-text {
    color: #4a5568;
    font-size: 1.1em;
    line-height: 1.9;
    text-align: justify;
}
.blank {
    display: inline-block;
    min-width: 120px;
    border-bottom: 2px solid #f6ad55;
    margin: 0 4px;
    color: #a0aec0;
    font-style: italic;
    font-size: 0.9em;
    padding: 0 4px;
}
.show-answer-btn {
    background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 1em;
    font-weight: 600;
    cursor: pointer;
    margin-top: 20px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
}
.show-answer-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(237, 137, 54, 0.4);
}
.nav-link {
    display: inline-block;
    margin-top: 40px;
    padding: 12px 24px;
    background: #667eea;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
}
"""

# JavaScript
js = """
function toggleAnswers(button) {
    const exerciseSection = button.closest('.exercise-section');
    const blanks = exerciseSection.querySelectorAll('.blank');
    
    if (button.dataset.showing === 'true') {
        // Скрываем ответы
        blanks.forEach(blank => {
            const answer = blank.dataset.answer;
            blank.innerHTML = `_______ (${blank.dataset.hint})`;
            blank.style.color = '#a0aec0';
            blank.style.fontWeight = 'normal';
            blank.style.borderBottomColor = '#f6ad55';
        });
        button.textContent = 'Показать ответы';
        button.dataset.showing = 'false';
        button.style.background = 'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)';
    } else {
        // Показываем ответы
        blanks.forEach(blank => {
            const answer = blank.dataset.answer;
            blank.innerHTML = `${answer} (${blank.dataset.hint})`;
            blank.style.color = '#d97706';
            blank.style.fontWeight = '600';
            blank.style.borderBottomColor = '#22c55e';
        });
        button.textContent = 'Скрыть ответы';
        button.dataset.showing = 'true';
        button.style.background = 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)';
    }
}
"""

# Генерируем HTML для каждой фазы
scenes_html = ""
for phase in character['journey_phases']:
    if 'theatrical_scene' in phase:
        scene = phase['theatrical_scene']
        
        # Обрабатываем упражнение
        exercise_html = ""
        if 'exercise_text' in scene:
            import re
            
            # Находим все немецкие слова в оригинальном тексте
            pattern_orig = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
            german_words = re.findall(pattern_orig, scene['narrative'])
            
            # Создаем упражнение с data атрибутами
            exercise_text = scene['exercise_text']
            
            # Создаем словарь немецких слов
            words_dict = {}
            for german, russian in german_words:
                german = german.strip().upper()  # Приводим к верхнему регистру
                russian = russian.strip()
                words_dict[russian] = german
            
            # Заменяем пропуски с правильными data-атрибутами
            import re
            def replace_blank(match):
                hint = match.group(1)
                answer = words_dict.get(hint, 'UNKNOWN')
                return f'<span class="blank" data-answer="{answer}" data-hint="{hint}">_______ ({hint})</span>'
            
            exercise_text = re.sub(r'___ \(([^)]+)\)', replace_blank, exercise_text)
            
            exercise_html = f"""
            <div class="exercise-section">
                <h4 class="exercise-title">📝 Упражнение: Вставьте немецкие слова</h4>
                <div class="exercise-text">{exercise_text}</div>
                <button class="show-answer-btn" onclick="toggleAnswers(this)" data-showing="false">
                    Показать ответы
                </button>
            </div>
            """
        
        scenes_html += f"""
        <div class="theatrical-scene">
            <h3 class="scene-title">🎭 {scene['title']}</h3>
            <div class="scene-narrative">{scene['narrative']}</div>
            <div class="emotional-peak">{scene['emotional_peak']}</div>
            {exercise_html}
        </div>
        """

# Создаем полный HTML
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{character['title']} | König Lear</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <h1>👑 {character['title']}</h1>
        <p class="subtitle">Изучаем немецкий через трагедию Шекспира</p>
        
        {scenes_html}
        
        <a href="../index.html" class="nav-link">← К главной</a>
    </div>
    
    <script>{js}</script>
</body>
</html>"""

# Сохраняем файл
output_path = Path(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n[SAVED] {output_path}")
print(f"[SIZE] {len(html):,} bytes")

# Проверка
has_exercise = 'exercise-section' in html
has_blanks = 'class="blank"' in html
blank_count = html.count('class="blank"')

print(f"\n[VERIFICATION]")
print(f"  Has exercise sections: {has_exercise}")
print(f"  Has blank fields: {has_blanks}")
print(f"  Total blanks: {blank_count}")

print("\n[SUCCESS] HTML с упражнениями создан!")
