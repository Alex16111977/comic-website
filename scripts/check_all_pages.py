"""
Проверка упражнений на всех страницах персонажей
"""
from pathlib import Path

def check_html_page(html_path):
    """Проверяет наличие упражнений в HTML файле"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        'name': html_path.stem,
        'size': len(content),
        'has_exercises': 'exercise-container' in content,
        'has_data_answer': 'data-answer=' in content,
        'has_data_hint': 'data-hint=' in content,
        'has_toggle_function': 'toggleAnswers' in content,
        'exercises_count': content.count('exercise-container'),
        'blanks_count': content.count('class="blank"')
    }

def main():
    output_dir = Path(r'F:\AiKlientBank\KingLearComic\output\journeys')
    
    print("ПРОВЕРКА УПРАЖНЕНИЙ НА ВСЕХ СТРАНИЦАХ")
    print("=" * 60)
    
    # Порядок персонажей
    character_order = [
        "king_lear", "cordelia", "goneril", "regan",
        "gloucester", "edgar", "edmund", "kent",
        "fool", "albany", "cornwall", "oswald"
    ]
    
    all_good = True
    total_exercises = 0
    total_blanks = 0
    
    for char_id in character_order:
        html_file = output_dir / f"{char_id}.html"
        
        if html_file.exists():
            stats = check_html_page(html_file)
            
            # Определяем статус
            is_ok = (stats['has_exercises'] and 
                    stats['has_data_answer'] and 
                    stats['has_data_hint'] and
                    stats['has_toggle_function'])
            
            status = "[OK]" if is_ok else "[FAIL]"
            if not is_ok:
                all_good = False
            
            print(f"\n{status} {char_id}.html")
            print(f"  Размер: {stats['size']:,} bytes")
            print(f"  Упражнений: {stats['exercises_count']}")
            print(f"  Пропусков: {stats['blanks_count']}")
            print(f"  Проверки:")
            print(f"    - exercise-container: {'✓' if stats['has_exercises'] else '✗'}")
            print(f"    - data-answer: {'✓' if stats['has_data_answer'] else '✗'}")
            print(f"    - data-hint: {'✓' if stats['has_data_hint'] else '✗'}")
            print(f"    - toggleAnswers: {'✓' if stats['has_toggle_function'] else '✗'}")
            
            total_exercises += stats['exercises_count']
            total_blanks += stats['blanks_count']
        else:
            print(f"\n[MISSING] {char_id}.html")
            all_good = False
    
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 60)
    print(f"  Файлов проверено: {len(list(output_dir.glob('*.html')))}")
    print(f"  Всего упражнений: {total_exercises}")
    print(f"  Всего пропусков: {total_blanks}")
    print(f"  Статус: {'✅ ВСЕ ГОТОВО!' if all_good else '⚠️ ЕСТЬ ПРОБЛЕМЫ'}")
    
    # Проверяем index.html
    index_file = output_dir.parent / 'index.html'
    if index_file.exists():
        print(f"\n[INDEX] index.html существует ({index_file.stat().st_size:,} bytes)")
    
    return all_good

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] Все страницы содержат рабочие упражнения!")
        print("[READY] Сайт готов к использованию!")
    else:
        print("[WARNING] Некоторые страницы требуют проверки")
