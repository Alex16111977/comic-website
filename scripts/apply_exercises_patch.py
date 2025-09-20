"""
Патч для интеграции упражнений в journey_runtime.js
Дата: 14.09.2025
"""
import sys
from pathlib import Path

def apply_exercises_patch():
    """Применяет патч для интеграции упражнений."""
    
    runtime_path = Path(r'F:\AiKlientBank\KingLearComic\static\js\journey_runtime.js')
    backup_path = runtime_path.with_suffix('.js.backup')
    
    # Создаем резервную копию
    print(f"[1/4] Создание резервной копии...")
    with open(runtime_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"      [OK] Резервная копия: {backup_path.name}")
    
    # Читаем файл построчно
    lines = original_content.split('\n')
    modified = False
    
    # Патч 1: Добавляем функцию инициализации упражнений
    print(f"[2/4] Добавление функции инициализации упражнений...")
    
    # Ищем строку с currentPhaseIndex = index;
    for i, line in enumerate(lines):
        if 'currentPhaseIndex = index;' in line and 'function' in lines[max(0, i-5):i+5]:
            # Добавляем вызов initializeExercises после смены индекса
            indent = len(line) - len(line.lstrip())
            new_lines = [
                line,
                ' ' * indent + '// Инициализация упражнений для новой фазы',
                ' ' * indent + 'if (window.initializeExercises && phaseKeys[index]) {',
                ' ' * (indent + 4) + 'window.initializeExercises(phaseKeys[index]);',
                ' ' * indent + '}'
            ]
            lines[i] = '\n'.join(new_lines)
            modified = True
            print(f"      [OK] Добавлен вызов в строку {i+1}")
            break
    
    # Патч 2: Добавляем инициализацию при загрузке страницы
    print(f"[3/4] Добавление инициализации при загрузке...")
    
    # Ищем конец файла или место инициализации
    init_added = False
    for i in range(len(lines) - 1, 0, -1):
        if '})();' in lines[i] or 'window.addEventListener' in lines[i]:
            # Добавляем инициализацию перед закрытием
            new_init = """
// Инициализация упражнений при загрузке страницы
setTimeout(() => {
    if (window.initializeExercises && phaseKeys && phaseKeys.length > 0) {
        window.initializeExercises(phaseKeys[0]);
        console.log('[Exercises] Initialized for first phase:', phaseKeys[0]);
    }
}, 100);"""
            lines.insert(i, new_init)
            init_added = True
            modified = True
            print(f"      [OK] Добавлена инициализация в строку {i+1}")
            break
    
    if not init_added:
        # Добавляем в конец файла
        lines.append("""
// Инициализация упражнений при загрузке страницы
setTimeout(() => {
    if (window.initializeExercises && phaseKeys && phaseKeys.length > 0) {
        window.initializeExercises(phaseKeys[0]);
        console.log('[Exercises] Initialized for first phase:', phaseKeys[0]);
    }
}, 100);""")
        modified = True
        print(f"      [OK] Добавлена инициализация в конец файла")
    
    # Сохраняем модифицированный файл
    if modified:
        print(f"[4/4] Сохранение изменений...")
        new_content = '\n'.join(lines)
        with open(runtime_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"      [OK] Файл обновлен")
        return True
    else:
        print(f"      [!] Изменения не требуются")
        return False

if __name__ == "__main__":
    try:
        success = apply_exercises_patch()
        if success:
            print("\n[SUCCESS] Патч успешно применен!")
            print("\nСледующие шаги:")
            print("1. Добавьте в journey.html перед </body>:")
            print('   <script src="../static/js/exercises.js"></script>')
            print('   <link rel="stylesheet" href="../static/css/exercises.css">')
            print("\n2. Запустите генерацию сайта:")
            print("   python F:\\AiKlientBank\\KingLearComic\\main.py")
        else:
            print("\n[INFO] Патч уже применен или не требуется")
    except Exception as e:
        print(f"\n[ERROR] Ошибка при применении патча: {e}")
        sys.exit(1)
