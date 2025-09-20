"""Автоматичний рефакторинг JS файлів"""
from pathlib import Path


def split_js_file(file_path, max_lines=300):
    """Розбиває JS файл на модулі"""
    lines = file_path.read_text(encoding='utf-8').splitlines(keepends=True)
    if len(lines) <= max_lines:
        print(f"[OK] {file_path.name} - {len(lines)} рядків")
        return

    print(f"[SPLIT] {file_path.name} - {len(lines)} рядків")
    modules = {
        'vocabulary': [],
        'navigation': [],
        'exercises': [],
        'utils': []
    }
    current_module = 'utils'

    for line in lines:
        lowered = line.lower()
        if 'vocabulary' in lowered or 'vocab' in lowered:
            current_module = 'vocabulary'
        elif 'phase' in lowered or 'navigate' in lowered:
            current_module = 'navigation'
        elif 'exercise' in lowered or 'quiz' in lowered:
            current_module = 'exercises'
        modules[current_module].append(line)

    for module_name, content in modules.items():
        if not content:
            continue
        output_dir = file_path.parent / 'modules' / module_name
        output_dir.mkdir(parents=True, exist_ok=True)
        chunks = [content[i:i + max_lines] for i in range(0, len(content), max_lines)]
        for idx, chunk in enumerate(chunks, start=1):
            output_file = output_dir / f"{file_path.stem}_part{idx}.js"
            output_file.write_text(''.join(chunk), encoding='utf-8')
            print(f"  [CREATED] {output_file.relative_to(file_path.parent)}")


def main():
    js_dir = Path(__file__).resolve().parents[1] / 'static' / 'js'
    for js_file in js_dir.glob('*.js'):
        if js_file.stat().st_size > 10_000:
            split_js_file(js_file)


if __name__ == '__main__':
    main()
