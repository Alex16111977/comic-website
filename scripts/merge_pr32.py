#!/usr/bin/env python3
"""
Скрипт для слияния PR #32 - нормализация синонимов в vocabulary.json
и перегенерация HTML файлов персонажей.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_git_command(cmd, cwd="F:\\AiKlientBank\\KingLearComic"):
    """Выполняет git команду и возвращает результат."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            shell=True
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def main():
    repo_path = r"F:\AiKlientBank\KingLearComic"
    os.chdir(repo_path)
    
    print("[INFO] Начинаю процесс слияния PR #32...")
    
    # 1. Сначала сохраним текущее состояние
    print("[+] Сохраняю текущее состояние...")
    code, out, err = run_git_command("git stash")
    if code != 0 and "No local changes" not in out:
        print(f"[WARNING] При stash: {err}")
    
    # 2. Переключаемся на main
    print("[+] Переключаюсь на main...")
    code, out, err = run_git_command("git checkout main")
    if code != 0:
        print(f"[ERROR] Не удалось переключиться на main: {err}")
        return 1
    
    # 3. Получаем последние изменения
    print("[+] Получаю последние изменения...")
    code, out, err = run_git_command("git fetch origin")
    if code != 0:
        print(f"[WARNING] При fetch: {err}")
    
    # 4. Обновляем main
    print("[+] Обновляю main...")
    code, out, err = run_git_command("git pull origin main")
    if code != 0 and "Already up to date" not in out:
        print(f"[WARNING] При pull main: {err}")
    
    # 5. Получаем ветку PR
    print("[+] Получаю ветку PR...")
    pr_branch = "codex/update-synonyms-structure-in-vocabulary.json"
    code, out, err = run_git_command(f"git fetch origin {pr_branch}:{pr_branch}")
    if code != 0:
        print(f"[WARNING] При fetch PR branch: {err}")
    
    # 6. Переключаемся на ветку PR
    print("[+] Переключаюсь на ветку PR...")
    code, out, err = run_git_command(f"git checkout {pr_branch}")
    if code != 0:
        print(f"[ERROR] Не удалось переключиться на PR branch: {err}")
        return 1
    
    # 7. Пытаемся выполнить merge main в PR ветку
    print("[+] Пытаюсь слить main в PR ветку...")
    code, out, err = run_git_command("git merge main")
    
    if code != 0:
        print("[!] Обнаружены конфликты. Разрешаю автоматически...")
        
        # Получаем список конфликтующих файлов
        code, out, err = run_git_command("git diff --name-only --diff-filter=U")
        conflicted_files = out.strip().split('\n') if out.strip() else []
        
        print(f"[INFO] Конфликтующие файлы: {len(conflicted_files)}")
        
        # Для каждого конфликтующего файла
        for file in conflicted_files:
            if not file:
                continue
                
            print(f"  - Разрешаю конфликт в: {file}")
            
            # Для HTML файлов персонажей берем версию из PR (theirs)
            # так как в PR обновлены синонимы
            if file.startswith("output/journeys/") and file.endswith(".html"):
                code, out, err = run_git_command(f"git checkout --theirs {file}")
                if code == 0:
                    code, out, err = run_git_command(f"git add {file}")
                    print(f"    [OK] Использую версию из PR для {file}")
                else:
                    print(f"    [ERROR] Не удалось разрешить {file}: {err}")
            
            # Для остальных файлов тоже берем версию из PR
            else:
                code, out, err = run_git_command(f"git checkout --theirs {file}")
                if code == 0:
                    code, out, err = run_git_command(f"git add {file}")
                    print(f"    [OK] Использую версию из PR для {file}")
                else:
                    print(f"    [ERROR] Не удалось разрешить {file}: {err}")
        
        # Проверяем, все ли конфликты разрешены
        code, out, err = run_git_command("git diff --name-only --diff-filter=U")
        if out.strip():
            print(f"[ERROR] Остались неразрешенные конфликты: {out}")
            return 1
        
        # Завершаем merge
        print("[+] Завершаю merge...")
        commit_msg = "Merge main into PR #32: Normalize vocabulary synonyms"
        code, out, err = run_git_command(f'git commit -m "{commit_msg}"')
        if code != 0:
            print(f"[ERROR] Не удалось завершить merge: {err}")
            return 1
    
    print("[OK] Merge выполнен успешно!")
    
    # 8. Пушим изменения
    print("[+] Отправляю изменения в GitHub...")
    code, out, err = run_git_command(f"git push origin {pr_branch}")
    if code != 0:
        print(f"[ERROR] Не удалось запушить: {err}")
        print("[INFO] Попробуйте выполнить вручную: git push origin {pr_branch}")
        return 1
    
    print("[SUCCESS] PR #32 успешно обновлен и конфликты разрешены!")
    print("[INFO] Теперь можно выполнить merge в GitHub.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
