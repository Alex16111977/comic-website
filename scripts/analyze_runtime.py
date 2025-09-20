"""Анализ модульной архитектуры JavaScript."""
from pathlib import Path

MAX_LINES = 300

MODULES = [
    ('pages/journey.js', 'Контроллер страницы путешествия'),
    ('pages/index.js', 'Логика главной страницы'),
    ('pages/training.js', 'Контроллер тренировки слова'),
    ('modules/vocabulary/loader.js', 'Загрузка словаря'),
    ('modules/vocabulary/display.js', 'Отображение карточек'),
    ('modules/vocabulary/study.js', 'Менеджер изучения'),
    ('modules/navigation/phases.js', 'Навигация по фазам'),
    ('modules/navigation/progress.js', 'Трекер прогресса'),
    ('modules/exercises/quiz.js', 'Викторина по словам'),
    ('modules/exercises/constructor.js', 'Конструктор предложений'),
    ('modules/exercises/word-match.js', 'Подбор слов'),
    ('modules/utils/dom.js', 'DOM помощники'),
    ('modules/utils/storage.js', 'Работа с localStorage')
]


def analyze_module(path: Path, description: str) -> None:
    if not path.exists():
        print(f"  [MISSING] {path.name:<35} — {description}")
        return
    line_count = sum(1 for _ in path.open('r', encoding='utf-8'))
    status = 'OK ' if line_count <= MAX_LINES else 'WARN'
    print(f"  [{status}] {path.relative_to(path.parents[2])} — {description} ({line_count} строк)")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    js_root = project_root / 'static' / 'js'
    template_path = project_root / 'templates' / 'journey.html'

    print('[АНАЛИЗ МОДУЛЬНОЙ СТРУКТУРЫ]')
    print('=' * 50)
    print('\n[1/3] Проверка модулей...')
    for relative_path, description in MODULES:
        analyze_module(js_root / relative_path, description)

    print('\n[2/3] Проверка импорта в шаблоне journey.html...')
    if not template_path.exists():
        print('  [MISSING] templates/journey.html не найден')
    else:
        html = template_path.read_text(encoding='utf-8')
        if "static/js/pages/journey.js" in html and "type=\"module\"" in html:
            print('  [OK ] Модуль JourneyApp подключен через type="module"')
        else:
            print('  [WARN] Не найден импорт модуля journey.js в шаблоне')

    print('\n[3/3] Дополнительные проверки...')
    loader_path = js_root / 'loader.js'
    if loader_path.exists():
        print('  [INFO] Найден loader.js — точка входа для интеграции модулей')
    else:
        print('  [INFO] loader.js отсутствует (не требуется)')

    print('\nАнализ завершён.')


if __name__ == '__main__':
    main()
