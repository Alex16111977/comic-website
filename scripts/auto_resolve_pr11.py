#!/usr/bin/env python
"""
Автоматическое решение конфликтов PR #11 через GitHub API
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("РЕШАЮ КОНФЛИКТЫ PR #11")
    print("=" * 60)
    
    repo_dir = r"F:\AiKlientBank\comic-website-pr11"
    
    # 1. Клонируем если еще нет
    if not os.path.exists(repo_dir):
        print("\n[1/8] Клонирую репозиторий...")
        subprocess.run([
            'git', 'clone', 
            'https://github.com/Alex16111977/comic-website.git',
            repo_dir
        ], check=True)
    else:
        print("\n[1/8] Репозиторий уже клонирован")
    
    os.chdir(repo_dir)
    
    # 2. Обновляем
    print("[2/8] Обновляю репозиторий...")
    subprocess.run(['git', 'fetch', 'origin'], check=True)
    
    # 3. Переключаемся на ветку PR
    print("[3/8] Переключаюсь на ветку PR #11...")
    subprocess.run([
        'git', 'checkout', 
        'codex/update-vocabulary-and-implement-interactive-features'
    ], check=True)
    
    # 4. Пробуем мерж
    print("[4/8] Начинаю слияние с main...")
    result = subprocess.run(
        ['git', 'merge', 'main', '--no-commit'],
        capture_output=True,
        text=True
    )
    
    if "CONFLICT" in result.stdout or result.returncode != 0:
        print("[5/8] Обнаружены конфликты! Решаю...")
        
        # Копируем объединенный файл js_lira.py
        merged_file = r"F:\AiKlientBank\KingLearComic\generators\js_lira_merged_pr11.py"
        target_file = os.path.join(repo_dir, "generators", "js_lira.py")
        
        print(f"  - Копирую объединенный generators/js_lira.py")
        with open(merged_file, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(target_file, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        # Для остальных файлов берем версию из PR (они не конфликтуют с функционалом)
        print("  - Принимаю версию PR для vocabulary.json")
        subprocess.run(['git', 'checkout', '--theirs', 'data/vocabulary/vocabulary.json'], check=True)
        
        print("  - Принимаю версию PR для journey.css")
        subprocess.run(['git', 'checkout', '--theirs', 'static/css/journey.css'], check=True)
        
        # 5. Добавляем файлы
        print("[6/8] Добавляю решенные файлы...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # 6. Коммитим
        print("[7/8] Создаю коммит...")
        subprocess.run([
            'git', 'commit', '-m',
            'Merge main into PR #11: Add vocabulary relations with quiz support'
        ], check=True)
        
        print("[8/8] Готово к пушу!")
        print("\nТеперь выполните:")
        print("  cd", repo_dir)
        print("  git push origin codex/update-vocabulary-and-implement-interactive-features")
        
        print("\n✅ КОНФЛИКТЫ РЕШЕНЫ!")
        print("PR #11 готов к слиянию!")
    else:
        print("✅ Конфликтов нет!")

if __name__ == "__main__":
    main()
