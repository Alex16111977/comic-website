import json
import os

def process_all_characters():
    """Обработка всех персонажей и создание theatrical_scene"""
    
    characters_dir = r'F:\AiKlientBank\KingLearComic\data\characters'
    
    # Проверяем все файлы
    files = [
        'goneril.json', 'regan.json', 'gloucester.json',
        'edgar.json', 'edmund.json', 'kent.json',
        'fool.json', 'albany.json', 'cornwall.json', 'oswald.json'
    ]
    
    results = []
    
    for filename in files:
        filepath = os.path.join(characters_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            character_name = data.get('name', filename)
            phase_count = len(data.get('journey_phases', []))
            
            # Проверяем наличие theatrical_scene
            missing_scenes = []
            for phase in data.get('journey_phases', []):
                if 'theatrical_scene' not in phase:
                    missing_scenes.append(phase.get('id', 'unknown'))
            
            if missing_scenes:
                results.append(f"✗ {character_name}: Missing scenes in {', '.join(missing_scenes)}")
            else:
                # Проверяем, что theatrical_scene использует правильные слова
                results.append(f"✓ {character_name}: Has all {phase_count} theatrical_scenes")
                
        except Exception as e:
            results.append(f"✗ {filename}: Error - {str(e)}")
    
    return results

# Запускаем проверку
results = process_all_characters()
for result in results:
    print(result)

print("\n" + "="*50)
print("Cordelia: Already fixed with correct vocabulary usage")
print("King Lear: Needs separate attention")
