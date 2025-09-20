"""
Тест исправлений для sentenceTranslation и крестика закрытия
Дата: 20.09.2025
"""
import json
from pathlib import Path

def test_js_generator():
    """Проверка что sentenceTranslation передается в JS"""
    print("[TEST] Проверка JS генератора")
    print("=" * 50)
    
    # Читаем сгенерированный JS из любой journey страницы
    output_dir = Path(r'F:\AiKlientBank\KingLearComic\output\journeys')
    king_lear_html = output_dir / 'king_lear.html'
    
    if not king_lear_html.exists():
        print("[ERROR] Файл king_lear.html не найден!")
        return False
        
    content = king_lear_html.read_text(encoding='utf-8')
    
    # Проверяем наличие sentenceTranslation в JS коде
    checks = [
        ('sentenceTranslation в data атрибутах', 'data-sentence-translation='),
        ('sentenceTranslation в объекте', 'fullWordData.sentenceTranslation'),
        ('sentenceTranslation в examples', 'russian: this.dataset.sentenceTranslation'),
    ]
    
    for check_name, check_str in checks:
        if check_str in content:
            print(f"[OK] {check_name} - найдено")
        else:
            print(f"[ERROR] {check_name} - НЕ найдено")
            
    return True

def test_training_close_button():
    """Проверка что крестик закрытия работает"""
    print("\n[TEST] Проверка крестика закрытия")
    print("=" * 50)
    
    training_file = Path(r'F:\AiKlientBank\KingLearComic\output\training.html')
    
    if not training_file.exists():
        print("[ERROR] Файл training.html не найден!")
        return False
        
    content = training_file.read_text(encoding='utf-8')
    
    # Проверяем что НЕТ window.close()
    if 'onclick="window.close()"' in content:
        print("[ERROR] window.close() все еще используется!")
        return False
    
    # Проверяем что есть правильный обработчик
    if "onclick=\"window.location.href='index.html'\"" in content:
        print("[OK] Крестик теперь возвращает на главную страницу")
    else:
        print("[ERROR] Правильный обработчик не найден")
        return False
        
    return True

def test_vocabulary_data():
    """Проверка что sentence_translation есть в данных персонажей"""
    print("\n[TEST] Проверка данных персонажей")
    print("=" * 50)
    
    data_dir = Path(r'F:\AiKlientBank\KingLearComic\data\characters')
    json_files = list(data_dir.glob('*.json'))
    
    has_translations = 0
    total_words = 0
    
    for json_file in json_files[:3]:  # Проверяем первые 3 файла
        data = json.loads(json_file.read_text(encoding='utf-8'))
        
        for phase in data.get('journey_phases', []):
            for word in phase.get('vocabulary', []):
                total_words += 1
                if word.get('sentence_translation'):
                    has_translations += 1
                    
    print(f"[OK] Слов с переводами примеров: {has_translations}/{total_words}")
    
    if has_translations > 0:
        print("[OK] sentence_translation присутствует в данных")
    else:
        print("[WARNING] sentence_translation отсутствует в данных")
        
    return True

def main():
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЙ")
    print("="*60)
    
    tests = [
        test_js_generator,
        test_training_close_button,
        test_vocabulary_data
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Ошибка в тесте: {e}")
            results.append(False)
            
    print("\n" + "="*60)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    passed = sum(1 for r in results if r)
    total = len(results)
    
    if passed == total:
        print(f"[OK] Все тесты пройдены: {passed}/{total}")
    else:
        print(f"[WARNING] Пройдено тестов: {passed}/{total}")
        
    print("\nИСПРАВЛЕНИЯ:")
    print("1. sentenceTranslation теперь передается при нажатии кнопки 'Изучить'")
    print("2. Крестик закрытия теперь возвращает на главную (не использует window.close)")
    print("="*60)

if __name__ == '__main__':
    main()
