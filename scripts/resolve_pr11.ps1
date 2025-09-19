Write-Host "================================" -ForegroundColor Cyan
Write-Host "  PR #11 CONFLICT RESOLVER" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Проверяем что мы в git репозитории
if (-not (Test-Path ".git")) {
    Write-Host "[ERROR] Not in a git repository!" -ForegroundColor Red
    Write-Host "Please run this script from comic-website folder" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/7] Fetching latest changes..." -ForegroundColor Yellow
git fetch origin

Write-Host "[2/7] Checking out PR branch..." -ForegroundColor Yellow
git checkout codex/update-vocabulary-and-implement-interactive-features

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Cannot checkout PR branch!" -ForegroundColor Red
    exit 1
}

Write-Host "[3/7] Starting merge with main..." -ForegroundColor Yellow
git merge main --no-commit --no-ff

Write-Host "[4/7] Checking for conflicts..." -ForegroundColor Yellow
$status = git status --porcelain

if ($status -match "UU ") {
    Write-Host "[5/7] Conflicts detected! Opening in VS Code..." -ForegroundColor Yellow
    
    # Список конфликтных файлов
    $conflicts = @(
        "data/vocabulary/vocabulary.json",
        "generators/js_lira.py",
        "static/css/journey.css"
    )
    
    Write-Host ""
    Write-Host "MANUAL RESOLUTION REQUIRED:" -ForegroundColor Red
    Write-Host "===========================" -ForegroundColor Red
    
    foreach ($file in $conflicts) {
        Write-Host "  - $file" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "RESOLUTION GUIDE:" -ForegroundColor Cyan
    Write-Host "----------------" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. vocabulary.json:" -ForegroundColor Green
    Write-Host "   - Accept PR version (with word_family, synonyms)" -ForegroundColor White
    Write-Host ""
    Write-Host "2. js_lira.py:" -ForegroundColor Green
    Write-Host "   - MERGE both changes:" -ForegroundColor White
    Write-Host "     * Keep quizzes functions from main" -ForegroundColor White
    Write-Host "     * Add relations functions from PR" -ForegroundColor White
    Write-Host ""
    Write-Host "3. journey.css:" -ForegroundColor Green
    Write-Host "   - MERGE styles:" -ForegroundColor White
    Write-Host "     * Keep existing styles from main" -ForegroundColor White
    Write-Host "     * Add new .word-relations-section styles" -ForegroundColor White
    Write-Host ""
    
    # Открываем файлы в VS Code если установлен
    $hasVSCode = Get-Command code -ErrorAction SilentlyContinue
    if ($hasVSCode) {
        Write-Host "[6/7] Opening conflicts in VS Code..." -ForegroundColor Yellow
        foreach ($file in $conflicts) {
            code $file
        }
    }
    
    Write-Host ""
    Write-Host "After resolving conflicts manually, run:" -ForegroundColor Cyan
    Write-Host "  git add ." -ForegroundColor Green
    Write-Host "  git commit -m 'Merge main: Add vocabulary relations'" -ForegroundColor Green
    Write-Host "  git push origin codex/update-vocabulary-and-implement-interactive-features" -ForegroundColor Green
    
} else {
    Write-Host "[5/7] No conflicts detected!" -ForegroundColor Green
    Write-Host "[6/7] Committing merge..." -ForegroundColor Yellow
    git commit -m "Merge main into PR #11: Add interactive vocabulary relations"
    
    Write-Host "[7/7] Done! Push with:" -ForegroundColor Green
    Write-Host "  git push origin codex/update-vocabulary-and-implement-interactive-features" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "        PROCESS COMPLETE" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan