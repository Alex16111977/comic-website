"""HTML Generator for Lira Journey pages"""
from .base import BaseGenerator
from .css_lira import LiraCSSGenerator
from .js_lira import LiraJSGenerator

class LiraHTMLGenerator(BaseGenerator):
    """Generate complete HTML pages in lira-journey style"""
    
    def generate_journey(self, character_file):
        """Generate journey page for a character"""
        
        # Load character data
        character = self.load_character(character_file)
        
        # Get CSS and JS
        css = LiraCSSGenerator.generate()
        js = LiraJSGenerator.generate(character)
        
        # Build journey points HTML
        points_html = ""
        for i, phase in enumerate(character.get('journey_phases', [])):
            active = "active" if i == 0 else ""
            points_html += f'''
                <div class="journey-point {active}" data-phase="{phase['id']}">
                    <div class="point-circle">{phase['icon']}</div>
                    <h4>{phase['title']}</h4>
                    <p>{phase['keywords']}</p>
                </div>'''
        
        # Add CSS for theatrical scene with elegant design
        theatrical_css = '''
        .theatrical-scene {
            background: linear-gradient(135deg, #f6f8fb 0%, #e9ecf1 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
            padding: 35px;
            border-radius: 20px;
            margin: 30px 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 5px 25px rgba(0,0,0,0.08), 0 2px 10px rgba(102, 126, 234, 0.1);
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        .theatrical-scene.active {
            display: block;
        }
        
        .theatrical-scene::before {
            content: 'ACT';
            position: absolute;
            font-size: 100px;
            font-weight: 900;
            opacity: 0.05;
            right: -30px;
            top: -30px;
            transform: rotate(-15deg);
        }
        
        .scene-title {
            color: #2d3748;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 25px;
            text-align: center;
            letter-spacing: 1px;
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
            transition: all 0.3s ease;
        }
        
        .scene-narrative b:hover {
            background: linear-gradient(180deg, transparent 40%, rgba(102, 126, 234, 0.25) 40%);
            color: #5a67d8;
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
            position: relative;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .emotional-peak::before {
            content: '';
            position: absolute;
            left: -4px;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        /* Стили для упражнения */
        .exercise-section {
            background: linear-gradient(135deg, #fff9e6 0%, #fff4d6 100%);
            border: 2px solid #f6ad55;
            padding: 30px;
            border-radius: 15px;
            margin-top: 35px;
            position: relative;
        }
        
        .exercise-title {
            color: #d97706;
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .exercise-text {
            color: #4a5568;
            font-size: 1.1em;
            line-height: 1.9;
            text-align: justify;
        }
        
        .exercise-text .blank {
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px solid #f6ad55;
            margin: 0 4px;
            color: #a0aec0;
            font-style: italic;
            font-size: 0.9em;
            padding: 0 4px;
            transition: all 0.3s ease;
        }
        
        .exercise-container {
            display: none;
        }
        
        .exercise-container.active {
            display: block;
        }
        
        .exercises-container {
            margin-top: 40px;
        }
        
        .show-answer-btn {
            background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
            /* Mobile optimizations */
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
            min-height: 48px;
            min-width: 160px;
        }
        
        .show-answer-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(237, 137, 54, 0.4);
        }
        
        .show-answer-btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(237, 137, 54, 0.3);
        }
        
        /* Touch device optimizations */
        @media (hover: none) and (pointer: coarse) {
            .show-answer-btn {
                padding: 18px 36px;
                font-size: 1.2em;
                min-height: 56px;
            }
            
            .show-answer-btn:hover {
                transform: none;
            }
            
            .show-answer-btn:active {
                transform: scale(0.98);
                opacity: 0.9;
            }
        }
        
        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(20px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        @media (max-width: 768px) {
            .theatrical-scene {
                padding: 25px 20px;
            }
            
            .scene-title {
                font-size: 1.4em;
            }
            
            .scene-narrative {
                font-size: 1.05em;
                text-align: left;
            }
            
            .exercise-section {
                padding: 20px;
            }
            
            .exercise-text {
                font-size: 1em;
                line-height: 1.8;
            }
            
            .exercise-text .blank {
                min-width: 80px;
                padding: 2px 6px;
                margin: 2px;
            }
            
            .show-answer-btn {
                width: 90%;
                max-width: 300px;
                padding: 18px 24px;
                font-size: 1.15em;
            }
        }
        
        /* iOS specific fixes */
        @supports (-webkit-touch-callout: none) {
            .show-answer-btn {
                -webkit-appearance: none;
                appearance: none;
            }
            
            .exercise-text .blank {
                -webkit-tap-highlight-color: transparent;
            }
        }
        '''
        
        # Build complete HTML
        html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{character['title']} | König Lear</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        {css}
        {theatrical_css}
    </style>
</head>
<body>
    <div class="container">
        <header class="page-header">
            <h1>👑 {character['title']}</h1>
            <p class="subtitle">Изучаем немецкий через трагедию Шекспира</p>
        </header>
        
        <div class="journey-section">
            <h2>📚 Путешествие {character['name']}</h2>
            
            <div class="journey-timeline">
                <svg class="journey-line" width="100%" height="4">
                    <line x1="0" y1="2" x2="100%" y2="2" stroke="#6b5b95" stroke-width="2" opacity="0.3"/>
                    <line x1="0" y1="2" x2="14%" y2="2" stroke="#6b5b95" stroke-width="3" class="progress-line"/>
                </svg>
                
                <div class="journey-points">
                    {points_html}
                </div>
            </div>
            
            <div class="journey-progress">
                <div class="progress-track">
                    <div class="progress-fill" style="width: 14%"></div>
                </div>
                <div class="progress-text">Акт I: Разделение королевства</div>
            </div>
        </div>
        
        <!-- Theatrical Scene Section -->
        <div class="theatrical-scenes">
            {self._generate_theatrical_scenes(character)}
        </div>
        
        <div class="vocabulary-section">
            <h2>📖 Словарь: Фаза "<span id="current-phase">Тронный зал</span>"</h2>
            <div class="vocabulary-grid"></div>
            
            <div class="phase-navigation">
                <button class="change-phase-btn prev-btn">← Предыдущая фаза</button>
                <button class="change-phase-btn next-btn">Следующая фаза →</button>
            </div>
        </div>
        
        <!-- Exercises Section AFTER Vocabulary -->
        <div class="exercises-container">
            {self._generate_exercises(character)}
        </div>
        
        <nav class="bottom-nav">
            <a href="../index.html" class="nav-link">← К главной</a>
        </nav>
    </div>
    
    <script>{js}</script>
</body>
</html>'''
        
        return html
    
    def _generate_theatrical_scenes(self, character):
        """Generate HTML for theatrical scenes WITHOUT exercises"""
        scenes_html = ""
        
        for i, phase in enumerate(character.get('journey_phases', [])):
            if 'theatrical_scene' in phase:
                scene = phase['theatrical_scene']
                active_class = "active" if i == 0 else ""
                
                # БЕЗ упражнений - они будут после словаря
                scenes_html += f'''
                <div class="theatrical-scene {active_class}" data-phase="{phase['id']}">
                    <h3 class="scene-title">{scene['title']}</h3>
                    <div class="scene-narrative">{scene['narrative']}</div>
                    <div class="emotional-peak">{scene['emotional_peak']}</div>
                </div>'''
        
        return scenes_html
    
    def _generate_exercises(self, character):
        """Generate exercises with proper data attributes"""
        exercises_html = ""
        
        for i, phase in enumerate(character.get('journey_phases', [])):
            if 'theatrical_scene' in phase:
                scene = phase['theatrical_scene']
                active_class = "active" if i == 0 else ""
                
                if 'exercise_text' in scene and scene['exercise_text']:
                    import re

                    def format_answer(german_word):
                        if not german_word:
                            return ''
                        german_word = german_word.strip()
                        lower = german_word.lower()
                        for article in ('der ', 'die ', 'das '):
                            if lower.startswith(article):
                                parts = german_word.split(' ', 1)
                                if len(parts) > 1:
                                    return f"{parts[0]} {parts[1].upper()}"
                                return german_word.upper()
                        return german_word.upper()

                    words_dict = {}
                    for vocab in phase.get('vocabulary', []):
                        german = vocab.get('german', '')
                        answer = format_answer(german)
                        forms = vocab.get('answer_forms') or []
                        if not forms:
                            base = vocab.get('russian')
                            if base:
                                forms = [base]
                        for form in forms:
                            if not form:
                                continue
                            words_dict[form.strip()] = answer

                    pattern = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
                    german_words = re.findall(pattern, scene['narrative'])
                    for german_word, russian_hint in german_words:
                        hint = russian_hint.strip()
                        if hint and hint not in words_dict:
                            words_dict[hint] = format_answer(german_word.strip())

                    missing_hints = set()

                    exercise_text = scene['exercise_text']

                    def replace_blank(match):
                        hint = match.group(1)
                        answer = words_dict.get(hint)
                        if not answer:
                            missing_hints.add(hint)
                            answer = 'UNKNOWN'
                        return f'<span class="blank" data-answer="{answer}" data-hint="{hint}">_______ ({hint})</span>'

                    exercise_text = re.sub(r'___ \(([^)]+)\)', replace_blank, exercise_text)

                    if missing_hints:
                        char_id = character.get('id') or character.get('name', 'unknown')
                        phase_id = phase.get('id', 'unknown')
                        missing_list = ', '.join(sorted(missing_hints))
                        raise ValueError(
                            f"Не найдены формы ответов для подсказок ({missing_list}) в фазе '{phase_id}' персонажа '{char_id}'"
                        )
                    
                    exercises_html += f'''
                    <div class="exercise-container {active_class}" data-phase="{phase['id']}">
                        <div class="exercise-section">
                            <h4 class="exercise-title">📝 Упражнение: {scene['title']}</h4>
                            <div class="exercise-text">{exercise_text}</div>
                            <button class="show-answer-btn" onclick="toggleAnswers(this)" type="button" aria-label="Показать или скрыть ответы">Показать ответы</button>
                        </div>
                    </div>'''
        
        return exercises_html
