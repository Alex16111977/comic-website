"""Современный помощник по интеграции упражнений."""
from pathlib import Path
import sys


def apply_exercises_patch() -> bool:
    """Сообщает о состоянии модульной архитектуры и запускает анализ."""
    project_root = Path(__file__).resolve().parents[1]
    legacy_runtime = project_root / 'static' / 'js' / 'journey_runtime.js'

    if legacy_runtime.exists():
        print('[WARN] Обнаружен legacy-файл static/js/journey_runtime.js.')
        print('       Перейдите на модульную структуру из static/js/pages и static/js/modules.')
        return False

    print('[OK ] Модульная архитектура активна — патч не требуется.')
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from analyze_runtime import main as analyze_modules  # type: ignore
    except Exception as exc:  # noqa: BLE001 - диагностическое сообщение
        print(f'[WARN] Не удалось запустить дополнительный анализ: {exc}')
        return True

    print('\nЗапускаем краткий анализ структуры...')
    analyze_modules()
    return True


if __name__ == '__main__':
    try:
        success = apply_exercises_patch()
        if success:
            print('\n[SUCCESS] Проверка завершена. Модули готовы к использованию.')
        else:
            print('\n[INFO] Требуется миграция на модульную архитектуру.')
    except Exception as error:  # noqa: BLE001 - верхнеуровневый вывод
        print(f'\n[ERROR] Не удалось выполнить проверку: {error}')
        sys.exit(1)
