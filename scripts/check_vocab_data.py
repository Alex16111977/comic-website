import re

with open(r'F:\AiKlientBank\KingLearComic\output\journeys\king_lear.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем определение phaseVocabularies
start = content.find('const phaseVocabularies = {')
if start != -1:
    print(f'[OK] Найдено определение phaseVocabularies на позиции {start}')
    
    # Ищем конец объекта
    brackets = 1
    pos = start + len('const phaseVocabularies = {')
    end = pos
    
    while brackets > 0 and end < len(content):
        if content[end] == '{':
            brackets += 1
        elif content[end] == '}':
            brackets -= 1
        end += 1
    
    # Проверяем размер объекта
    vocab_text = content[start:end]
    
    # Считаем фазы
    phases = re.findall(r'"(throne|goneril|regan|storm|hut|dover|prison)"\s*:', vocab_text)
    print(f'[OK] Найдено фаз в объекте: {len(set(phases))}')
    print(f'[OK] Фазы: {", ".join(set(phases))}')
    
    # Проверяем полноту первой фазы
    if 'throne' in vocab_text:
        throne_start = vocab_text.find('"throne"')
        throne_snippet = vocab_text[throne_start:throne_start+500]
        
        has_title = '"title"' in throne_snippet
        has_words = '"words"' in throne_snippet
        has_vocabulary = '"vocabulary"' in throne_snippet
        
        print(f'')
        print(f'[INFO] Проверка фазы "throne":')
        print(f'  {"[OK]" if has_title else "[ERROR]"} title: {has_title}')
        print(f'  {"[OK]" if has_words else "[ERROR]"} words: {has_words}')
        print(f'  {"[OK]" if has_vocabulary else "[ERROR]"} vocabulary: {has_vocabulary}')
        
        if not has_words and not has_vocabulary:
            print(f'')
            print(f'[ERROR] Фаза "throne" не содержит данных словаря!')
            print(f'[INFO] Начало фазы:')
            print(throne_snippet[:200])
else:
    print('[ERROR] Определение phaseVocabularies не найдено!')
    
    # Проверим альтернативное определение
    alt_start = content.find('window.phaseVocabularies = {')
    if alt_start != -1:
        print('[INFO] Найдено альтернативное определение через window.phaseVocabularies')
        snippet = content[alt_start:alt_start+500]
        print(snippet)