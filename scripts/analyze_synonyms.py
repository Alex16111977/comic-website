"""
Аналіз покриття синонімів та антонімів для journey phases
Створено: 2025-09-23
Мета: перевірити поточний стан synonym_antonym_sets у всіх персонажів
"""

import json
from pathlib import Path

def analyze_synonyms():
    # Читаємо файл персонажа king_lear
    king_lear_path = Path(r'F:\AiKlientBank\KingLearComic\data\characters\king_lear.json')
    with open(king_lear_path, 'r', encoding='utf-8') as f:
        king_lear_data = json.load(f)
    
    print("[ANALIZ SYNONIMIV TA ANTONIMIV]")
    print("=" * 60)
    
    journey_phases = king_lear_data.get('journey_phases', [])
    print(f"King Lear - vsogo faz: {len(journey_phases)}")
    
    phases_with_syn = 0
    phases_without_syn = 0
    total_synonyms = 0
    total_antonyms = 0
    
    for i, phase in enumerate(journey_phases, 1):
        phase_id = phase.get('id', 'unknown')
        phase_title = phase.get('title', 'No title')
        
        # Перевіряємо наявність synonym_antonym_sets
        syn_ant_sets = phase.get('synonym_antonym_sets', [])
        
        print(f"\n[FAZA {i}] {phase_id}")
        
        if syn_ant_sets:
            phases_with_syn += 1
            print(f"  [OK] Mae {len(syn_ant_sets)} naboriv")
            for set_item in syn_ant_sets:
                target_word = set_item.get('target', {}).get('word', 'N/A')
                synonyms = set_item.get('synonyms', [])
                antonyms = set_item.get('antonyms', [])
                total_synonyms += len(synonyms)
                total_antonyms += len(antonyms)
                print(f"    - {target_word}: {len(synonyms)} syn, {len(antonyms)} ant")
        else:
            phases_without_syn += 1
            print(f"  [!] NEMAE synonimiv/antonimiv")
    
    print("\n" + "=" * 60)
    print("[PIDSUMOK DLA KING LEAR]")
    print(f"Faz z synonimamy: {phases_with_syn}")
    print(f"Faz BEZ synonimiv: {phases_without_syn}")
    print(f"Vsogo synonimiv: {total_synonyms}")
    print(f"Vsogo antonimiv: {total_antonyms}")
    
    # Перевірка всіх персонажів
    print("\n" + "=" * 60)
    print("[PEREVIRKA VSIH PERSONAZHIV]")
    
    characters_dir = Path(r'F:\AiKlientBank\KingLearComic\data\characters')
    json_files = [f for f in characters_dir.glob('*.json') if f.name != '.gitkeep']
    
    total_phases_all = 0
    total_with_syn_all = 0
    total_without_syn_all = 0
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
            char_name = char_data.get('name', json_file.stem)
            phases = char_data.get('journey_phases', [])
            
            phases_with = 0
            phases_without = 0
            
            for phase in phases:
                if phase.get('synonym_antonym_sets'):
                    phases_with += 1
                else:
                    phases_without += 1
            
            total_phases_all += len(phases)
            total_with_syn_all += phases_with
            total_without_syn_all += phases_without
            
            status = "[OK]" if phases_without == 0 else "[!]"
            print(f"  {status} {char_name}: {len(phases)} faz, {phases_with} z syn, {phases_without} bez syn")
    
    print("\n" + "=" * 60)
    print("[ZAGALNYJ PIDSUMOK]")
    print(f"Personazhiv: {len(json_files)}")
    print(f"Vsogo faz: {total_phases_all}")
    print(f"Faz z synonimamy: {total_with_syn_all}")
    print(f"Faz BEZ synonimiv: {total_without_syn_all}")
    coverage = (total_with_syn_all / total_phases_all * 100) if total_phases_all > 0 else 0
    print(f"Pokryttya: {coverage:.1f}%")
    
    if total_without_syn_all > 0:
        print("\n[REKOMENDACIYA]")
        print(f"Neobhidno dodaty synonym_antonym_sets do {total_without_syn_all} faz!")

if __name__ == "__main__":
    analyze_synonyms()
