"""Index page generator with character cards"""
from .base import BaseGenerator

class IndexGenerator(BaseGenerator):
    """Generate index page with all character journeys"""
    
    def generate(self, character_files):
        """Generate index page with character grid"""
        
        # Character role descriptions
        role_descriptions = {
            "king_lear": "Трагический король",
            "cordelia": "Верная дочь",
            "goneril": "Старшая дочь-предательница",
            "regan": "Младшая дочь-предательница",
            "gloucester": "Благородный граф",
            "edgar": "Законный сын Глостера",
            "edmund": "Бастард Глостера",
            "kent": "Верный советник",
            "fool": "Мудрый шут",
            "albany": "Муж Гонерильи",
            "cornwall": "Муж Реганы",
            "oswald": "Управляющий Гонерильи"
        }
        
        # Build character cards
        cards_html = ""
        for char_file in character_files:
            character = self.load_character(char_file)
            char_id = char_file.stem
            
            # Get first phase icon
            first_icon = character['journey_phases'][0]['icon'] if character.get('journey_phases') else "👤"
            
            # Get role description
            role = role_descriptions.get(char_id, character.get('title', 'Персонаж'))
            
            # Card HTML
            cards_html += f'''
            <div class="character-card" data-character="{char_id}">
                <div class="card-icon">{first_icon}</div>
                <h3>{character['name']}</h3>
                <p class="role">{role}</p>
                <div class="phase-count">{len(character.get('journey_phases', []))} фаз путешествия</div>
                <a href="journeys/{char_file.stem}.html" class="journey-link">
                    Начать путешествие →
                </a>
            </div>'''
        
        # Complete HTML
        html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>König Lear - Интерактивное путешествие</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #333;
            padding-bottom: 40px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            color: white;
            padding: 60px 20px 40px;
            animation: fadeInDown 0.8s ease;
        }}
        
        .header h1 {{
            font-size: 4em;
            font-weight: 900;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            letter-spacing: -2px;
        }}
        
        .header .subtitle {{
            font-size: 1.4em;
            opacity: 0.95;
            max-width: 700px;
            margin: 0 auto 30px;
            line-height: 1.6;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: 700;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .characters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 40px;
        }}
        
        .character-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideUp 0.6s ease;
            animation-fill-mode: both;
            position: relative;
            overflow: hidden;
        }}
        
        .character-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .character-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .character-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }}
        
        .card-icon {{
            font-size: 72px;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
            animation: bounce 2s infinite;
        }}
        
        .character-card h3 {{
            font-size: 1.8em;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        
        .role {{
            color: #718096;
            font-size: 1.1em;
            margin-bottom: 15px;
        }}
        
        .phase-count {{
            display: inline-block;
            padding: 6px 12px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        
        .journey-link {{
            display: inline-block;
            padding: 14px 32px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .journey-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #764ba2, #667eea);
        }}
        
        /* Animation delays for staggered effect */
        .character-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .character-card:nth-child(2) {{ animation-delay: 0.15s; }}
        .character-card:nth-child(3) {{ animation-delay: 0.2s; }}
        .character-card:nth-child(4) {{ animation-delay: 0.25s; }}
        .character-card:nth-child(5) {{ animation-delay: 0.3s; }}
        .character-card:nth-child(6) {{ animation-delay: 0.35s; }}
        .character-card:nth-child(7) {{ animation-delay: 0.4s; }}
        .character-card:nth-child(8) {{ animation-delay: 0.45s; }}
        .character-card:nth-child(9) {{ animation-delay: 0.5s; }}
        .character-card:nth-child(10) {{ animation-delay: 0.55s; }}
        .character-card:nth-child(11) {{ animation-delay: 0.6s; }}
        .character-card:nth-child(12) {{ animation-delay: 0.65s; }}
        
        @keyframes fadeInDown {{
            from {{ 
                opacity: 0; 
                transform: translateY(-30px); 
            }}
            to {{ 
                opacity: 1; 
                transform: translateY(0); 
            }}
        }}
        
        @keyframes slideUp {{
            from {{ 
                opacity: 0; 
                transform: translateY(30px); 
            }}
            to {{ 
                opacity: 1; 
                transform: translateY(0); 
            }}
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2.5em; }}
            .characters-grid {{ grid-template-columns: 1fr; }}
            .stats {{ flex-direction: column; gap: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>👑 Путешествие Короля Лира</h1>
            <p class="subtitle">
                Изучаем немецкий через трагедию Шекспира<br>
                Интерактивное путешествие с 12 персонажами
            </p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{len(character_files)}</span>
                    <span class="stat-label">Персонажей</span>
                </div>
                <div class="stat">
                    <span class="stat-number">84</span>
                    <span class="stat-label">Фазы пути</span>
                </div>
                <div class="stat">
                    <span class="stat-number">588</span>
                    <span class="stat-label">Слов B1</span>
                </div>
            </div>
        </header>
        
        <div class="characters-grid">
            {cards_html}
        </div>
    </div>
</body>
</html>'''
        
        return html
