"""
Скрипт для полной замены всех файлов на GitHub
Дата: 22.09.2025
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Выполнить команду и вернуть результат"""
    print(f"[CMD] {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"[ERROR] {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    project_dir = Path(r"F:\AiKlientBank\KingLearComic")
    os.chdir(project_dir)
    
    print("[INFO] Начинаем полную замену файлов на GitHub...")
    print(f"[INFO] Рабочая папка: {project_dir}")
    
    # 1. Удаляем старую .git папку если есть
    git_dir = project_dir / ".git"
    if git_dir.exists():
        print("[INFO] Удаляем старую .git папку...")
        try:
            shutil.rmtree(git_dir)
            print("[OK] .git папка удалена")
        except Exception as e:
            print(f"[ERROR] Не удалось удалить .git: {e}")
            return False
    
    # 2. Инициализируем новый git репозиторий
    print("[INFO] Инициализируем новый git репозиторий...")
    if not run_command("git init", cwd=project_dir):
        print("[ERROR] Не удалось инициализировать git")
        return False
    
    # 3. Добавляем remote
    print("[INFO] Добавляем GitHub remote...")
    if not run_command("git remote add origin https://github.com/Alex16111977/comic-website.git", cwd=project_dir):
        print("[ERROR] Не удалось добавить remote")
        return False
    
    # 4. Создаем .gitignore если его нет
    gitignore_path = project_dir / ".gitignore"
    if not gitignore_path.exists():
        print("[INFO] Создаем .gitignore...")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
backups/
*.log
.DS_Store
Thumbs.db
"""
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print("[OK] .gitignore создан")
    
    # 5. Добавляем все файлы
    print("[INFO] Добавляем все файлы в git...")
    if not run_command("git add -A", cwd=project_dir):
        print("[ERROR] Не удалось добавить файлы")
        return False
    
    # 6. Делаем коммит
    print("[INFO] Создаем коммит...")
    commit_message = "Complete project replacement - King Lear Comic Website"
    if not run_command(f'git commit -m "{commit_message}"', cwd=project_dir):
        print("[ERROR] Не удалось создать коммит")
        return False
    
    # 7. Переименовываем ветку в main
    print("[INFO] Переименовываем ветку в main...")
    run_command("git branch -M main", cwd=project_dir)
    
    # 8. Форсированно пушим на GitHub (заменяем все)
    print("[INFO] Отправляем на GitHub (полная замена)...")
    print("[!] Это полностью заменит все файлы на GitHub!")
    
    if not run_command("git push -f origin main", cwd=project_dir):
        print("[ERROR] Не удалось отправить на GitHub")
        print("[TIP] Возможно нужна авторизация. Попробуйте:")
        print("  1. Установить GitHub CLI: winget install GitHub.cli")
        print("  2. Авторизоваться: gh auth login")
        print("  3. Или использовать Personal Access Token")
        return False
    
    print("[OK] Все файлы успешно заменены на GitHub!")
    print("[OK] GitHub Pages автоматически обновится через несколько минут")
    print(f"[OK] Сайт будет доступен по: https://alex16111977.github.io/comic-website/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
