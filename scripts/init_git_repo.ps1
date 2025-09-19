# Скрипт инициализации Git репозитория для KingLearComic
# Привязка к https://github.com/Alex16111977/comic-website

Write-Host "[INFO] Starting Git repository initialization..." -ForegroundColor Cyan

# Переходим в директорию проекта
Set-Location "F:\AiKlientBank\KingLearComic"
Write-Host "[OK] Changed to project directory: $(Get-Location)" -ForegroundColor Green

# Проверяем наличие .git папки
if (Test-Path ".git") {
    Write-Host "[WARNING] Git repository already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to reinitialize? (y/n)"
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force .git
        Write-Host "[OK] Removed existing .git directory" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Keeping existing repository" -ForegroundColor Cyan
        exit 0
    }
}

# Инициализируем новый репозиторий
Write-Host "`n[STEP 1] Initializing Git repository..." -ForegroundColor Cyan
git init
Write-Host "[OK] Git repository initialized" -ForegroundColor Green

# Добавляем remote origin
Write-Host "`n[STEP 2] Adding remote origin..." -ForegroundColor Cyan
git remote add origin https://github.com/Alex16111977/comic-website.git
Write-Host "[OK] Remote origin added" -ForegroundColor Green

# Проверяем remote
Write-Host "`n[STEP 3] Checking remotes..." -ForegroundColor Cyan
git remote -v

# Устанавливаем основную ветку
Write-Host "`n[STEP 4] Setting main branch..." -ForegroundColor Cyan
git branch -M main
Write-Host "[OK] Main branch set" -ForegroundColor Green

# Добавляем все файлы
Write-Host "`n[STEP 5] Adding files to staging..." -ForegroundColor Cyan
git add .
Write-Host "[OK] Files added" -ForegroundColor Green

# Показываем статус
Write-Host "`n[STEP 6] Current status:" -ForegroundColor Cyan
git status

Write-Host "`n[SUCCESS] Repository setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Make initial commit: git commit -m 'Initial commit: King Lear Comic Generator'"
Write-Host "2. Push to GitHub: git push -u origin main"
Write-Host "   Note: Use --force if repository already has content"
